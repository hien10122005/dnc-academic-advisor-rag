# -*- coding: utf-8 -*-
"""
backend.ingestion
Module Ingestion vector vào ChromaDB cho QĐ 580 (Phiên bản v2.0)
Nâng cấp toàn diện:
- Lưu trữ vào collection mới 'qd580_baseline_v2' (bảo toàn baseline cũ 'qd580_baseline_a').
- Quản lý vòng đời trạng thái: BUILDING -> READY / FAILED.
- Lưu trữ source_spans_json trong metadata ChromaDB để retriever và evaluator đọc trực tiếp.
- Ghi nhận đầy đủ thông tin: corpus_fingerprint, model_id, model_revision (commit sha).
- Đảm bảo tính bất biến (Idempotent): nạp lại không nhân đôi, kiểm tra tính tương thích phiên bản.
"""

from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings
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


class VietnameseEmbeddingFunction(EmbeddingFunction):
    """Lớp bọc SentenceTransformer tương thích chuẩn ChromaDB EmbeddingFunction."""

    def __init__(self, model_name: str = EMBEDDING_MODEL_CANDIDATE, revision: str = MODEL_REVISION):
        print(f"Khởi tạo mô hình embedding: {model_name} (Revision: {revision})...")
        self.model = load_embedding_model(model_name, revision=revision)
        self._name = f"vietnamese-bi-encoder-{revision[:7]}"
        print("Mô hình embedding đã sẵn sàng.")

    def name(self) -> str:
        return self._name

    def __call__(self, input: Documents) -> Embeddings:
        """Sinh vector embedding chuẩn hóa đơn vị L2 cho danh sách văn bản."""
        embeddings = self.model.encode(input, show_progress_bar=False, normalize_embeddings=True)
        return embeddings.tolist()


def load_chunks(chunks_path: Path) -> List[Dict[str, Any]]:
    """Đọc tệp JSONL chứa các chunk đã được chuẩn hóa."""
    if not chunks_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp chunk: {chunks_path}. Hãy chạy backend.chunking trước.")

    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line.strip()))
    return chunks


def save_ingestion_status(status_data: Dict[str, Any], status_path: Optional[Path] = None):
    """Ghi trạng thái ingestion vào tệp INGESTION_STATUS.json với thông tin theo từng collection."""
    target_file = Path(status_path) if status_path else INGESTION_STATUS_FILE
    os.makedirs(target_file.parent, exist_ok=True)

    existing_data: Dict[str, Any] = {}
    if target_file.exists():
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception:
            existing_data = {}

    collections_map = existing_data.get("collections", {})
    col_name = status_data.get("collection_name", COLLECTION_NAME)
    collections_map[col_name] = dict(status_data)

    full_payload = dict(status_data)
    full_payload["collections"] = collections_map
    full_payload["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(full_payload, f, ensure_ascii=False, indent=2)


def ingest_corpus(
    collection_name: str = COLLECTION_NAME,
    persist_dir: Optional[Path] = None,
    chunks_path: Optional[Path] = None,
    manifest_path: Optional[Path] = None,
    status_path: Optional[Path] = None,
    force_recreate: bool = False,
) -> Dict[str, Any]:
    """
    Nạp dữ liệu vào ChromaDB collection với vòng đời BUILDING -> READY.
    Kiểm tra tương thích phiên bản trước khi ghi và xác thực tập ID trước khi báo READY.
    Bất kỳ lỗi nào trước hoặc trong quá trình nạp đều lập tức ghi nhận FAILED.
    """
    start_time = time.time()
    p_dir = Path(persist_dir) if persist_dir else CHROMA_PERSIST_DIR
    c_file = Path(chunks_path) if chunks_path else CHUNKS_FILE
    m_file = Path(manifest_path) if manifest_path else MANIFEST_FILE
    s_file = Path(status_path) if status_path else INGESTION_STATUS_FILE

    print("=" * 80)
    print(f"BẮT ĐẦU INGESTION CORPUS VÀO CHROMADB (Collection: {collection_name})")
    print("=" * 80)

    # 1. Cập nhật trạng thái ban đầu ngay lập tức: BUILDING
    status_data = {
        "status": "BUILDING",
        "corpus_ready": False,
        "collection_name": collection_name,
        "chunk_version": CHUNK_VERSION,
        "corpus_fingerprint": "unknown",
        "chunks_sha256": "unknown",
        "model_id": EMBEDDING_MODEL_CANDIDATE,
        "model_revision": MODEL_REVISION,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_chunks_expected": 0,
    }
    save_ingestion_status(status_data, status_path=s_file)

    try:
        # 2. Đọc chunks và manifest
        chunks = load_chunks(c_file)
        print(f"Đã đọc {len(chunks)} chunks từ {c_file}.")

        manifest_data = {}
        if m_file.exists():
            with open(m_file, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)

        corpus_fingerprint = manifest_data.get("corpus_fingerprint", "unknown")
        chunks_sha256 = manifest_data.get("chunks_sha256", "unknown")

        status_data.update({
            "corpus_fingerprint": corpus_fingerprint,
            "chunks_sha256": chunks_sha256,
            "total_chunks_expected": len(chunks),
        })
        save_ingestion_status(status_data, status_path=s_file)
        # 3. Khởi tạo ChromaDB client & Embedding function
        embed_fn = VietnameseEmbeddingFunction(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)
        os.makedirs(p_dir, exist_ok=True)
        client = chromadb.PersistentClient(path=str(p_dir))

        # 4. Kiểm tra tương thích metadata nếu collection đã tồn tại
        existing_colls = [c.name for c in client.list_collections()]
        if collection_name in existing_colls:
            existing_col = client.get_collection(name=collection_name)
            existing_meta = existing_col.metadata or {}

            incompatible = []
            if existing_meta.get("corpus_fingerprint") and existing_meta.get("corpus_fingerprint") != corpus_fingerprint:
                incompatible.append(f"corpus_fingerprint không khớp (cũ: {existing_meta.get('corpus_fingerprint')}, mới: {corpus_fingerprint})")
            if existing_meta.get("model_revision") and existing_meta.get("model_revision") != MODEL_REVISION:
                incompatible.append(f"model_revision không khớp (cũ: {existing_meta.get('model_revision')}, mới: {MODEL_REVISION})")
            if existing_meta.get("model_name") and existing_meta.get("model_name") != EMBEDDING_MODEL_CANDIDATE:
                incompatible.append(f"model_name không khớp (cũ: {existing_meta.get('model_name')}, mới: {EMBEDDING_MODEL_CANDIDATE})")
            if existing_meta.get("chunk_version") and existing_meta.get("chunk_version") != CHUNK_VERSION:
                incompatible.append(f"chunk_version không khớp (cũ: {existing_meta.get('chunk_version')}, mới: {CHUNK_VERSION})")

            if incompatible and not force_recreate:
                err_msg = (
                    f"Collection '{collection_name}' đã tồn tại với phiên bản/metadata không tương thích: "
                    f"{'; '.join(incompatible)}. Yêu cầu cô lập phiên bản sang collection mới hoặc chỉ định force_recreate=True."
                )
                raise ValueError(err_msg)
            elif incompatible and force_recreate:
                print(f"force_recreate=True: Xóa và tạo mới collection '{collection_name}'...")
                client.delete_collection(name=collection_name)

        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=embed_fn,
            metadata={
                "hnsw:space": "cosine",
                "model_name": EMBEDDING_MODEL_CANDIDATE,
                "model_revision": MODEL_REVISION,
                "chunk_version": CHUNK_VERSION,
                "document_id": "QD580_DHNCT_2024",
                "corpus_fingerprint": corpus_fingerprint,
                "chunks_sha256": chunks_sha256,
            }
        )

        initial_count = collection.count()
        print(f"Số lượng chunk hiện có trong collection '{collection_name}': {initial_count}")

        # 5. Chuẩn bị danh sách nạp
        ids = []
        documents = []
        metadatas = []

        for c in chunks:
            ids.append(c["chunk_id"])
            documents.append(c["embedding_text"])

            meta = {
                "chunk_id": c["chunk_id"],
                "document_id": c["document_id"],
                "doc_part": c["doc_part"],
                "chapter": c["chapter"],
                "article": c["article"],
                "article_number": int(c["article_number"]),
                "start_page_pdf": int(c["start_page_pdf"]),
                "end_page_pdf": int(c["end_page_pdf"]),
                "start_page_printed": int(c["start_page_printed"]) if c["start_page_printed"] is not None else -1,
                "end_page_printed": int(c["end_page_printed"]) if c["end_page_printed"] is not None else -1,
                "is_table": bool(c["is_table"]),
                "token_count": int(c["token_count"]),
                "char_count": int(c["char_count"]),
                "source_spans_json": json.dumps(c.get("source_spans", []), ensure_ascii=False),
            }
            metadatas.append(meta)

        # 6. Upsert theo từng lô 32 để đảm bảo Idempotent
        batch_size = 32
        print(f"Bắt đầu nạp {len(ids)} chunks vào collection theo từng lô {batch_size}...")
        for i in range(0, len(ids), batch_size):
            end_idx = min(i + batch_size, len(ids))
            collection.upsert(
                ids=ids[i:end_idx],
                documents=documents[i:end_idx],
                metadatas=metadatas[i:end_idx]
            )
            print(f"  -> Đã nạp từ chunk {i + 1} đến {end_idx}/{len(ids)}")

        # 7. Xác thực nghiêm ngặt tính toàn vẹn ID và số lượng trước khi đặt READY
        actual_ids = set(collection.get()["ids"])
        expected_ids = set(ids)
        missing_ids = expected_ids - actual_ids
        extra_ids = actual_ids - expected_ids

        if missing_ids or extra_ids:
            err_msg = (
                f"Xác nhận tập ID thất bại trong collection '{collection_name}'! "
                f"Thiếu {len(missing_ids)} ID, tồn dư {len(extra_ids)} ID không hợp lệ."
            )
            raise RuntimeError(err_msg)

        final_count = len(actual_ids)
        if final_count != len(chunks):
            raise RuntimeError(
                f"Số lượng chunk trong collection ({final_count}) không khớp với tệp chunks ({len(chunks)})!"
            )

        elapsed = time.time() - start_time
        print(f"Hoàn thành nạp dữ liệu! Tổng số chunk trong collection: {final_count} (Thời gian: {elapsed:.2f}s)")

        # 8. Cập nhật trạng thái thành công: READY
        status_data.update({
            "status": "READY",
            "corpus_ready": True,
            "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_seconds": round(elapsed, 2),
            "final_chunk_count": final_count,
            "initial_chunk_count": initial_count,
            "all_ids_verified": True,
        })
        save_ingestion_status(status_data, status_path=s_file)
        print(f"Đã lưu báo cáo trạng thái ingestion tại: {s_file}")
        return status_data

    except Exception as exc:
        elapsed = time.time() - start_time
        status_data.update({
            "status": "FAILED",
            "corpus_ready": False,
            "error_message": str(exc),
            "failed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_seconds": round(elapsed, 2),
        })
        save_ingestion_status(status_data, status_path=s_file)
        print(f"LỖI INGESTION: {exc}")
        raise exc
        elapsed = time.time() - start_time
        status_data.update({
            "status": "FAILED",
            "corpus_ready": False,
            "error_message": str(exc),
            "failed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_seconds": round(elapsed, 2),
        })
        save_ingestion_status(status_data)
        print(f"LỖI INGESTION: {exc}")
        raise exc


if __name__ == "__main__":
    ingest_corpus()
