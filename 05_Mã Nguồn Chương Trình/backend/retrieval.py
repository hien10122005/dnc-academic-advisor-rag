# -*- coding: utf-8 -*-
"""
backend.retrieval
Module truy xuất vector semantic search từ ChromaDB cho QĐ 580 (Phiên bản v2.0)
Nâng cấp:
- Kiểm tra tính READY của corpus trước khi thực hiện truy vấn.
- Đọc source_spans trực tiếp từ metadata ChromaDB và đối chiếu manifest.
- Hỗ trợ CLI và thư viện hàm Python.
"""

from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from sentence_transformers import SentenceTransformer

from backend.config import (
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_CANDIDATE,
    INGESTION_STATUS_FILE,
    MANIFEST_FILE,
    MODEL_REVISION,
    load_embedding_model,
)


class VectorRetriever:
    """Retriever truy vấn vector ngữ nghĩa trên ChromaDB với kiểm tra vòng đời READY."""

    def __init__(
        self,
        persist_dir: str = str(CHROMA_PERSIST_DIR),
        collection_name: str = COLLECTION_NAME,
        model_name: str = EMBEDDING_MODEL_CANDIDATE,
        status_file_path: Optional[Path] = None,
        manifest_path: Optional[Path] = None,
    ):
        self.persist_dir = str(persist_dir)
        self.collection_name = collection_name
        self.model_name = model_name
        self.status_file_path = Path(status_file_path) if status_file_path else INGESTION_STATUS_FILE
        self.manifest_path = Path(manifest_path) if manifest_path else MANIFEST_FILE

        self._client: Optional[chromadb.PersistentClient] = None
        self._collection: Optional[chromadb.Collection] = None
        self._model: Optional[SentenceTransformer] = None
        self._manifest_data: Optional[Dict[str, Any]] = None

    def check_readiness(self):
        """Xác thực trạng thái READY của collection trước khi truy vấn. Chặn mọi trường hợp thiếu/hỏng/sai phiên bản."""
        if not self.status_file_path.exists():
            raise RuntimeError(
                f"Tệp trạng thái ingestion không tồn tại: {self.status_file_path}. Chưa có dữ liệu nào được nạp."
            )

        try:
            with open(self.status_file_path, "r", encoding="utf-8") as f:
                status_data = json.load(f)
        except Exception as exc:
            raise RuntimeError(
                f"Tệp trạng thái ingestion bị hỏng hoặc không đúng định dạng JSON ({self.status_file_path}): {exc}"
            )

        # Tìm thông tin trạng thái của collection tương ứng
        col_status = None
        if isinstance(status_data, dict):
            collections_map = status_data.get("collections", {})
            if isinstance(collections_map, dict) and self.collection_name in collections_map:
                col_status = collections_map[self.collection_name]
            elif status_data.get("collection_name") == self.collection_name:
                col_status = status_data

        if col_status is None:
            available_cols = list(status_data.get("collections", {}).keys()) if isinstance(status_data, dict) else []
            if not available_cols and isinstance(status_data, dict) and status_data.get("collection_name"):
                available_cols = [status_data.get("collection_name")]
            raise RuntimeError(
                f"Không tìm thấy trạng thái cho collection '{self.collection_name}' trong {self.status_file_path}. "
                f"Các collection hiện có: {available_cols}"
            )

        status_str = col_status.get("status")
        corpus_ready = col_status.get("corpus_ready", False)

        if status_str != "READY" or not corpus_ready:
            raise RuntimeError(
                f"Corpus collection '{self.collection_name}' chưa sẵn sàng (Trạng thái: {status_str}, corpus_ready: {corpus_ready}). "
                "Hãy hoàn tất ingestion thành công trước khi truy vấn."
            )

        # Kiểm tra tính tương thích giữa trạng thái và manifest
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, "r", encoding="utf-8") as f:
                    manifest_data = json.load(f)
                expected_fp = manifest_data.get("corpus_fingerprint")
                actual_fp = col_status.get("corpus_fingerprint")
                if expected_fp and actual_fp and expected_fp != actual_fp:
                    raise RuntimeError(
                        f"Corpus fingerprint trong trạng thái ({actual_fp}) không khớp với manifest hiện tại ({expected_fp})!"
                    )
            except RuntimeError:
                raise
            except Exception:
                pass

        # Kiểm tra model_id và model_revision
        status_model = col_status.get("model_id")
        if status_model and status_model != self.model_name:
            raise RuntimeError(
                f"Model ID trong trạng thái ingestion ({status_model}) không khớp với cấu hình retriever ({self.model_name})!"
            )

        status_rev = col_status.get("model_revision")
        if status_rev and status_rev != MODEL_REVISION:
            raise RuntimeError(
                f"Model revision trong trạng thái ingestion ({status_rev}) không khớp với cấu hình MODEL_REVISION ({MODEL_REVISION})!"
            )

    @property
    def client(self) -> chromadb.PersistentClient:
        if self._client is None:
            self._client = chromadb.PersistentClient(path=self.persist_dir)
        return self._client

    @property
    def collection(self) -> chromadb.Collection:
        self.check_readiness()
        if self._collection is None:
            self._collection = self.client.get_collection(name=self.collection_name)
        return self._collection

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = load_embedding_model(self.model_name, revision=MODEL_REVISION)
        return self._model

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """Truy vấn Top-K chunks tương đồng nhất với câu hỏi. Kiểm tra readiness trên mỗi request."""
        # Luôn xác thực readiness trên mỗi truy vấn (ngăn chặn stale cache khi trạng thái chuyển sang BUILDING/FAILED)
        self.check_readiness()

        if not query or not query.strip():
            return []

        # 1. Mã hóa câu hỏi thành vector embedding
        query_embedding = self.model.encode(
            [query.strip()],
            normalize_embeddings=True,
        ).tolist()

        # 2. Truy vấn ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        output: List[Dict[str, Any]] = []
        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        for rank, (cid, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists), start=1):
            distance = float(dist)
            similarity = round(1.0 - distance, 4)

            # Lấy source_spans từ metadata
            spans_json = meta.get("source_spans_json", "[]")
            try:
                source_spans = json.loads(spans_json)
            except Exception:
                source_spans = []

            item = {
                "rank": rank,
                "chunk_id": cid,
                "distance": round(distance, 4),
                "similarity": similarity,
                "doc_part": meta.get("doc_part", ""),
                "chapter": meta.get("chapter", ""),
                "article": meta.get("article", ""),
                "article_number": meta.get("article_number", 0),
                "start_page_pdf": meta.get("start_page_pdf", 0),
                "end_page_pdf": meta.get("end_page_pdf", 0),
                "start_page_printed": meta.get("start_page_printed", -1),
                "end_page_printed": meta.get("end_page_printed", -1),
                "is_table": meta.get("is_table", False),
                "is_cross_page": meta.get("start_page_pdf", 0) != meta.get("end_page_pdf", 0),
                "token_count": meta.get("token_count", 0),
                "char_count": meta.get("char_count", len(doc)),
                "content": doc,
                "source_spans": source_spans,
            }
            output.append(item)

        return output


_GLOBAL_RETRIEVER: Optional[VectorRetriever] = None


def get_retriever() -> VectorRetriever:
    global _GLOBAL_RETRIEVER
    if _GLOBAL_RETRIEVER is None:
        _GLOBAL_RETRIEVER = VectorRetriever()
    return _GLOBAL_RETRIEVER


def retrieve(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    retriever = get_retriever()
    return retriever.retrieve(query, top_k=top_k)


def main():
    parser = argparse.ArgumentParser(description="CLI truy xuất vector ChromaDB cho QĐ 580 (v2.0)")
    parser.add_argument("--query", "-q", type=str, required=True, help="Câu hỏi hoặc chuỗi truy vấn")
    parser.add_argument("--top_k", "-k", type=int, default=5, help="Số lượng kết quả lấy ra (mặc định 5)")
    parser.add_argument("--json", action="store_true", help="Xuất định dạng JSON thô")
    args = parser.parse_args()

    retriever = get_retriever()

    t0 = time.perf_counter()
    results = retriever.retrieve(args.query, top_k=args.top_k)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    print("=" * 80)
    print(f"KẾT QUẢ TRUY XUẤT VECTOR BASELINE (Collection: {retriever.collection_name} | Top {len(results)})")
    print(f"Câu hỏi: {args.query}")
    print(f"Thời gian truy xuất: {elapsed_ms:.2f} ms")
    print("=" * 80)

    for res in results:
        part = "Quy chế" if res["doc_part"] == "regulation" else "Quyết định"
        table_tag = "[BẢNG] " if res["is_table"] else ""
        cross_tag = "[NỐI TRANG] " if res["is_cross_page"] else ""
        print(f"#{res['rank']} | Chunk ID: {res['chunk_id']}")
        print(f"   Độ tương đồng (Cosine Sim): {res['similarity']} (Khoảng cách: {res['distance']})")
        print(f"   Vị trí: {part} | Chương: {res['chapter']} | Điều: {res['article']}")
        print(f"   Trang PDF: {res['start_page_pdf']} -> {res['end_page_pdf']} (Trang in: {res['start_page_printed']} -> {res['end_page_printed']}) {table_tag}{cross_tag}")
        print(f"   Số token: {res['token_count']} | Số ký tự: {res['char_count']}")
        excerpt = res['content'][:250].replace("\n", " ") + ("..." if len(res['content']) > 250 else "")
        print(f"   Nội dung: {excerpt}")
        print("-" * 80)


if __name__ == "__main__":
    main()
