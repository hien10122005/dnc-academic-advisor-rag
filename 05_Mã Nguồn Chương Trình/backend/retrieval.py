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
import hashlib
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
    CHUNKS_FILE,
    CHUNK_VERSION,
    COLLECTION_NAME,
    EMBEDDING_MODEL_CANDIDATE,
    INGESTION_STATUS_FILE,
    MANIFEST_FILE,
    MODEL_REVISION,
    load_embedding_model,
)
from backend.errors import KnowledgeBaseNotReadyError


def compute_sha256(filepath: Path) -> str:
    """Tính mã băm SHA-256 của tệp tin."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


class VectorRetriever:
    """Retriever truy vấn vector ngữ nghĩa trên ChromaDB với kiểm tra vòng đời READY và Preflight đối soát ba chiều."""

    def __init__(
        self,
        persist_dir: str = str(CHROMA_PERSIST_DIR),
        collection_name: str = COLLECTION_NAME,
        model_name: str = EMBEDDING_MODEL_CANDIDATE,
        status_file_path: Optional[Path] = None,
        manifest_path: Optional[Path] = None,
        chunks_file_path: Optional[Path] = None,
    ):
        self.persist_dir = str(persist_dir)
        self.collection_name = collection_name
        self.model_name = model_name
        self.status_file_path = Path(status_file_path) if status_file_path else INGESTION_STATUS_FILE
        self.manifest_path = Path(manifest_path) if manifest_path else MANIFEST_FILE
        self.chunks_file_path = Path(chunks_file_path) if chunks_file_path else CHUNKS_FILE

        self._client: Optional[chromadb.PersistentClient] = None
        self._collection: Optional[chromadb.Collection] = None
        self._model: Optional[SentenceTransformer] = None
        self._manifest_data: Optional[Dict[str, Any]] = None

    def check_readiness(self) -> Dict[str, Any]:
        """
        Xác thực tính sẵn sàng nghiêm ngặt (Preflight Readiness Verification).
        Đối soát 3 chiều: Ingestion Status <-> Manifest <-> ChromaDB Collection Metadata <-> Chunks SHA-256.
        Ném RuntimeError với thông báo lỗi cụ thể nếu phát hiện bất kỳ sự bất đồng nhất nào.
        """
        # 1. Kiểm tra sự tồn tại của tệp trạng thái
        if not self.status_file_path.exists():
            raise KnowledgeBaseNotReadyError(
                f"Tệp trạng thái ingestion không tồn tại: {self.status_file_path}. Chưa có dữ liệu nào được nạp."
            )

        # 2. Đọc và phân tích JSON tệp trạng thái
        try:
            with open(self.status_file_path, "r", encoding="utf-8") as f:
                status_data = json.load(f)
        except Exception as exc:
            raise KnowledgeBaseNotReadyError(
                f"Tệp trạng thái ingestion bị hỏng hoặc không đúng định dạng JSON ({self.status_file_path}): {exc}"
            )

        # 3. Tìm thông tin trạng thái theo collection
        col_status = None
        if isinstance(status_data, dict):
            collections_map = status_data.get("collections", {})
            if isinstance(collections_map, dict) and self.collection_name in collections_map:
                col_status = collections_map[self.collection_name]
            elif status_data.get("collection_name") == self.collection_name:
                col_status = status_data

        if col_status is None or not isinstance(col_status, dict):
            available_cols = list(status_data.get("collections", {}).keys()) if isinstance(status_data, dict) else []
            if not available_cols and isinstance(status_data, dict) and status_data.get("collection_name"):
                available_cols = [status_data.get("collection_name")]
            raise KnowledgeBaseNotReadyError(
                f"Không tìm thấy trạng thái cho collection '{self.collection_name}' trong {self.status_file_path}. "
                f"Các collection hiện có: {available_cols}"
            )

        # 4. Kiểm tra schema trạng thái nghiêm ngặt (kiểu boolean, trạng thái READY)
        status_str = col_status.get("status")
        corpus_ready = col_status.get("corpus_ready")

        if not isinstance(corpus_ready, bool) or corpus_ready is not True or status_str != "READY":
            raise KnowledgeBaseNotReadyError(
                f"Corpus collection '{self.collection_name}' chưa sẵn sàng (Trạng thái: {status_str}, corpus_ready: {corpus_ready}). "
                "Hãy hoàn tất ingestion thành công trước khi truy vấn."
            )

        required_status_fields = ["collection_name", "corpus_fingerprint", "chunks_sha256", "model_id", "model_revision"]
        for fld in required_status_fields:
            if not col_status.get(fld):
                raise KnowledgeBaseNotReadyError(
                    f"Trạng thái collection '{self.collection_name}' thiếu trường bắt buộc: '{fld}'."
                )

        # 5. Kiểm tra tệp Manifest bắt buộc (không được bỏ qua hay nuốt lỗi)
        if not self.manifest_path.exists():
            raise KnowledgeBaseNotReadyError(
                f"Tệp manifest không tồn tại: {self.manifest_path}. Không thể xác thực tính toàn vẹn của kho tri thức."
            )

        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except Exception as exc:
            raise KnowledgeBaseNotReadyError(
                f"Tệp manifest bị hỏng hoặc không đúng định dạng JSON ({self.manifest_path}): {exc}"
            )

        if not isinstance(manifest_data, dict):
            raise KnowledgeBaseNotReadyError(f"Tệp manifest ({self.manifest_path}) không phải là một JSON object hợp lệ.")

        required_manifest_fields = ["corpus_fingerprint", "chunks_sha256", "model_revision", "total_chunks"]
        for fld in required_manifest_fields:
            if not manifest_data.get(fld):
                raise KnowledgeBaseNotReadyError(f"Tệp manifest thiếu trường bắt buộc: '{fld}'.")

        # 6. Đối soát Fingerprint & Chunks SHA-256 giữa Status và Manifest
        expected_fp = manifest_data["corpus_fingerprint"]
        actual_fp = col_status["corpus_fingerprint"]
        if actual_fp != expected_fp:
            raise KnowledgeBaseNotReadyError(
                f"Corpus fingerprint trong trạng thái ({actual_fp}) không khớp với manifest hiện tại ({expected_fp})!"
            )

        expected_hash = manifest_data["chunks_sha256"]
        actual_hash = col_status["chunks_sha256"]
        if actual_hash != expected_hash:
            raise KnowledgeBaseNotReadyError(
                f"Chunks SHA-256 trong trạng thái ({actual_hash}) không khớp với manifest ({expected_hash})!"
            )

        # 7. Kiểm tra model_id và model_revision
        if col_status["model_id"] != self.model_name:
            raise KnowledgeBaseNotReadyError(
                f"Model ID trong trạng thái ingestion ({col_status['model_id']}) không khớp với cấu hình retriever ({self.model_name})!"
            )

        if col_status["model_revision"] != MODEL_REVISION:
            raise KnowledgeBaseNotReadyError(
                f"Model revision trong trạng thái ingestion ({col_status['model_revision']}) không khớp với cấu hình MODEL_REVISION ({MODEL_REVISION})!"
            )

        if manifest_data["model_revision"] != MODEL_REVISION:
            raise KnowledgeBaseNotReadyError(
                f"Model revision trong manifest ({manifest_data['model_revision']}) không khớp với cấu hình MODEL_REVISION ({MODEL_REVISION})!"
            )

        # 8. Đối soát Metadata thực tế trong ChromaDB Collection
        try:
            available_collections = [c.name for c in self.client.list_collections()]
            if self.collection_name not in available_collections:
                raise KnowledgeBaseNotReadyError(
                    f"Collection '{self.collection_name}' không tồn tại trong ChromaDB ({self.persist_dir}). "
                    f"Các collection hiện có: {available_collections}"
                )

            col = self.client.get_collection(name=self.collection_name)
            col_meta = col.metadata or {}

            if col_meta.get("corpus_fingerprint") != expected_fp:
                raise KnowledgeBaseNotReadyError(
                    f"Metadata collection ChromaDB có corpus_fingerprint ({col_meta.get('corpus_fingerprint')}) "
                    f"không khớp với manifest ({expected_fp})!"
                )

            if col_meta.get("chunks_sha256") != expected_hash:
                raise KnowledgeBaseNotReadyError(
                    f"Metadata collection ChromaDB có chunks_sha256 ({col_meta.get('chunks_sha256')}) "
                    f"không khớp với manifest ({expected_hash})!"
                )

            if col_meta.get("model_revision") != MODEL_REVISION:
                raise KnowledgeBaseNotReadyError(
                    f"Metadata collection ChromaDB có model_revision ({col_meta.get('model_revision')}) "
                    f"không khớp với cấu hình MODEL_REVISION ({MODEL_REVISION})!"
                )
        except KnowledgeBaseNotReadyError:
            raise
        except Exception as exc:
            raise KnowledgeBaseNotReadyError(f"Lỗi kiểm tra metadata ChromaDB collection: {exc}")

        # 9. Đối soát hash của tệp chunk thực tế trên đĩa
        if self.chunks_file_path and self.chunks_file_path.exists():
            disk_chunks_hash = compute_sha256(self.chunks_file_path)
            if disk_chunks_hash != expected_hash:
                raise KnowledgeBaseNotReadyError(
                    f"Mã băm tệp chunks trên đĩa ({disk_chunks_hash}) không khớp với manifest ({expected_hash})!"
                )

        return {
            "status": "READY",
            "collection_name": self.collection_name,
            "corpus_fingerprint": expected_fp,
            "chunks_sha256": expected_hash,
            "model_name": self.model_name,
            "model_revision": MODEL_REVISION,
            "total_chunks": manifest_data["total_chunks"],
        }

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

    @model.setter
    def model(self, value: Optional[SentenceTransformer]) -> None:
        self._model = value

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

            # Tách biệt tiền tố ngữ cảnh (context_prefix) và văn bản nguồn nguyên bản (content)
            if doc.startswith("[") and "\n" in doc:
                context_prefix, pure_content = doc.split("\n", 1)
            else:
                context_prefix = ""
                pure_content = doc

            # Chuẩn hóa trang in: Không sử dụng -1 làm số trang, phải là None khi chưa rõ
            raw_p_start = meta.get("start_page_printed")
            printed_start = int(raw_p_start) if raw_p_start is not None and int(raw_p_start) > 0 else None
            raw_p_end = meta.get("end_page_printed")
            printed_end = int(raw_p_end) if raw_p_end is not None and int(raw_p_end) > 0 else None

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
                "start_page_printed": printed_start,
                "end_page_printed": printed_end,
                "is_table": meta.get("is_table", False),
                "is_cross_page": meta.get("start_page_pdf", 0) != meta.get("end_page_pdf", 0),
                "token_count": meta.get("token_count", 0),
                "char_count": len(pure_content),
                "context_prefix": context_prefix,
                "content": pure_content,
                "embedding_text": doc,
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
