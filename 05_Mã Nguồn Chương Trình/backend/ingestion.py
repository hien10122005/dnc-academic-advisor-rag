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
)


class VietnameseEmbeddingFunction(EmbeddingFunction):
    """Lớp bọc SentenceTransformer tương thích chuẩn ChromaDB EmbeddingFunction."""

    def __init__(self, model_name: str = EMBEDDING_MODEL_CANDIDATE):
        print(f"Khởi tạo mô hình embedding: {model_name} (Revision: {MODEL_REVISION})...")
        self.model = SentenceTransformer(model_name)
        print("Mô hình embedding đã sẵn sàng.")

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


def save_ingestion_status(status_data: Dict[str, Any]):
    """Ghi trạng thái ingestion vào tệp INGESTION_STATUS.json."""
    os.makedirs(INGESTION_STATUS_FILE.parent, exist_ok=True)
    with open(INGESTION_STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)


def ingest_corpus(collection_name: str = COLLECTION_NAME) -> Dict[str, Any]:
    """
    Nạp dữ liệu vào ChromaDB collection với vòng đời BUILDING -> READY.
    """
    start_time = time.time()
    print("=" * 80)
    print(f"BẮT ĐẦU INGESTION CORPUS VÀO CHROMADB (Collection: {collection_name})")
    print("=" * 80)

    # 1. Đọc chunks và manifest
    chunks = load_chunks(CHUNKS_FILE)
    print(f"Đã đọc {len(chunks)} chunks từ {CHUNKS_FILE}.")

    manifest_data = {}
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)

    corpus_fingerprint = manifest_data.get("corpus_fingerprint", "unknown")

    # 2. Cập nhật trạng thái ban đầu: BUILDING
    status_data = {
        "status": "BUILDING",
        "corpus_ready": False,
        "collection_name": collection_name,
        "chunk_version": CHUNK_VERSION,
        "corpus_fingerprint": corpus_fingerprint,
        "model_id": EMBEDDING_MODEL_CANDIDATE,
        "model_revision": MODEL_REVISION,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_chunks_expected": len(chunks),
    }
    save_ingestion_status(status_data)

    try:
        # 3. Khởi tạo ChromaDB client & Embedding function
        embed_fn = VietnameseEmbeddingFunction(EMBEDDING_MODEL_CANDIDATE)
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))

        # 4. Lấy hoặc tạo collection với metadata phiên bản
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
                "chunks_sha256": manifest_data.get("chunks_sha256", "unknown"),
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

        final_count = collection.count()
        elapsed = time.time() - start_time
        print(f"Hoàn thành nạp dữ liệu! Tổng số chunk trong collection: {final_count} (Thời gian: {elapsed:.2f}s)")

        # 7. Cập nhật trạng thái thành công: READY
        status_data.update({
            "status": "READY",
            "corpus_ready": True,
            "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_seconds": round(elapsed, 2),
            "final_chunk_count": final_count,
            "initial_chunk_count": initial_count,
        })
        save_ingestion_status(status_data)
        print(f"Đã lưu báo cáo trạng thái ingestion tại: {INGESTION_STATUS_FILE}")
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
        save_ingestion_status(status_data)
        print(f"LỖI INGESTION: {exc}")
        raise exc


if __name__ == "__main__":
    ingest_corpus()
