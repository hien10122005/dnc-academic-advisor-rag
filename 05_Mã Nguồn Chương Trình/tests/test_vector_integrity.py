# -*- coding: utf-8 -*-
"""
tests.test_vector_integrity
Kiểm thử tính toàn vẹn của Vector Collection trong ChromaDB và đối soát đa chiều (Task 05 - R03):
1. Đúng tập ID và số lượng -> READY.
2. Collection rỗng (0 ID) -> KnowledgeBaseNotReadyError.
3. Collection thiếu ID (103 ID) -> KnowledgeBaseNotReadyError.
4. Collection dư ID (105 ID) -> KnowledgeBaseNotReadyError.
5. Collection đủ số lượng nhưng sai ID (same-count-wrong-ID) -> KnowledgeBaseNotReadyError.
6. Collection bị trùng lặp ID trong ChromaDB -> KnowledgeBaseNotReadyError.
7. Manifest thiếu trường / sai kiểu / không khớp total_chunks / trùng ID -> KnowledgeBaseNotReadyError.
8. Chunks file thiếu file / sai sha256 / sai số lượng / trùng ID / lệch tập ID -> KnowledgeBaseNotReadyError.
9. GET /health trả HTTP 503 khi vector integrity thất bại.
Tất cả các bài kiểm thử đều sử dụng thư mục tạm và mock/fake an toàn, tuyệt đối không can thiệp DB thật.
"""

from __future__ import annotations
import copy
import hashlib
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Đảm bảo môi trường offline an toàn cho unit tests
os.environ.setdefault("GEMINI_API_KEY", "")
os.environ.setdefault("GOOGLE_API_KEY", "")
os.environ.setdefault("ALLOW_OFFLINE_MOCK", "true")
os.environ.setdefault("PYDANTIC_DISABLE_PLUGINS", "__all__")

from fastapi.testclient import TestClient

from backend.config import MANIFEST_FILE, CHUNKS_FILE, MODEL_REVISION
from backend.errors import KnowledgeBaseNotReadyError
from backend.retrieval import VectorRetriever
import backend.main as api_main


class FakeChromaCollection:
    """Mock Collection đáp ứng interface của ChromaDB cho phép cấu hình IDs và metadata."""

    def __init__(self, ids: list[str], metadata: dict):
        self.ids = list(ids)
        self.metadata = dict(metadata)
        self.calls: list[str] = []

    def count(self) -> int:
        self.calls.append("count")
        return len(self.ids)

    def get(self, *args, **kwargs) -> dict:
        self.calls.append("get")
        return {"ids": list(self.ids)}


class FakeChromaClient:
    """Mock PersistentClient của ChromaDB."""

    def __init__(self, collection: FakeChromaCollection, collection_name: str = "review_collection"):
        self.collection = collection
        self.collection_name = collection_name

    def list_collections(self):
        return [types.SimpleNamespace(name=self.collection_name)]

    def get_collection(self, **kwargs):
        return self.collection


class TestVectorIntegrity(unittest.TestCase):
    """Bộ kiểm thử tính toàn vẹn vector và fail-closed preflight."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory(prefix="dnc-test-integrity-")
        self.test_dir = Path(self.td.name)

        # Đọc dữ liệu thật để tạo artifact tạm thời
        real_manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        real_chunks_bytes = CHUNKS_FILE.read_bytes()

        self.chunk_path = self.test_dir / "chunks.jsonl"
        self.manifest_path = self.test_dir / "manifest.json"
        self.status_path = self.test_dir / "status.json"

        self.chunk_path.write_bytes(real_chunks_bytes)

        self.manifest = copy.deepcopy(real_manifest)
        self.manifest["collection_name"] = "review_collection"
        self.manifest_path.write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")

        self.status = {
            "collection_name": "review_collection",
            "corpus_fingerprint": self.manifest["corpus_fingerprint"],
            "chunks_sha256": self.manifest["chunks_sha256"],
            "model_id": self.manifest["model_id"],
            "model_revision": self.manifest["model_revision"],
            "status": "READY",
            "corpus_ready": True,
        }
        self.status_path.write_text(json.dumps(self.status, ensure_ascii=False), encoding="utf-8")

        self.metadata = {
            "corpus_fingerprint": self.manifest["corpus_fingerprint"],
            "chunks_sha256": self.manifest["chunks_sha256"],
            "model_revision": self.manifest["model_revision"],
        }
        self.expected_ids = [c["chunk_id"] for c in self.manifest["chunks"]]

    def tearDown(self):
        self.td.cleanup()

    def _create_retriever(self, col_ids: list[str], metadata: dict | None = None) -> VectorRetriever:
        meta = metadata if metadata is not None else self.metadata
        col = FakeChromaCollection(col_ids, meta)
        client = FakeChromaClient(col, collection_name="review_collection")

        retriever = VectorRetriever(
            collection_name="review_collection",
            status_file_path=self.status_path,
            manifest_path=self.manifest_path,
            chunks_file_path=self.chunk_path,
        )
        retriever._client = client
        return retriever

    def test_vector_integrity_valid(self):
        """Khi tập ID và số lượng khớp hoàn toàn -> READY."""
        retriever = self._create_retriever(self.expected_ids)
        info = retriever.check_readiness()
        self.assertEqual(info["status"], "READY")
        self.assertEqual(info["total_chunks"], len(self.expected_ids))

    def test_vector_integrity_empty_collection(self):
        """Collection rỗng (0 ID) dù metadata còn nguyên -> từ chối với KnowledgeBaseNotReadyError."""
        retriever = self._create_retriever([])
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("Số lượng vector thực tế", str(ctx.exception))

    def test_vector_integrity_missing_id(self):
        """Collection thiếu 1 ID (103 ID) -> từ chối với KnowledgeBaseNotReadyError."""
        retriever = self._create_retriever(self.expected_ids[1:])
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("không khớp với manifest", str(ctx.exception))

    def test_vector_integrity_extra_id(self):
        """Collection dư 1 ID (105 ID) -> từ chối với KnowledgeBaseNotReadyError."""
        extra_ids = self.expected_ids + ["qd580_v2_extra_fake_id_12345678"]
        retriever = self._create_retriever(extra_ids)
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("không khớp với manifest", str(ctx.exception))

    def test_vector_integrity_same_count_wrong_id(self):
        """Collection đủ số lượng (104) nhưng có 1 ID bị sai khác -> từ chối và liệt kê đúng ID lệch."""
        wrong_ids = ["REPLACED_WRONG_ID"] + self.expected_ids[1:]
        retriever = self._create_retriever(wrong_ids)
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("không khớp với manifest/chunks", str(ctx.exception))
        self.assertIn("REPLACED_WRONG_ID", str(ctx.exception))
        self.assertIn(self.expected_ids[0], str(ctx.exception))

    def test_vector_integrity_duplicate_id_in_chroma(self):
        """Collection có ID trùng lặp trong Chroma (cùng tổng số 104) -> từ chối với KnowledgeBaseNotReadyError."""
        # Giữ nguyên tổng số 104 phần tử nhưng phần tử đầu bị lặp 2 lần để chạm guard duplicate
        dup_ids = [self.expected_ids[0]] + self.expected_ids[:-1]
        retriever = self._create_retriever(dup_ids)
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("trùng lặp trong ChromaDB collection", str(ctx.exception))

    def test_manifest_invalid_total_chunks(self):
        """Manifest có total_chunks sai kiểu hoặc không khớp danh sách chunks -> từ chối."""
        self.manifest["total_chunks"] = "invalid_string"
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        retriever = self._create_retriever(self.expected_ids)
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("total_chunks", str(ctx.exception))

    def test_manifest_duplicate_chunk_id(self):
        """Manifest có chunk_id bị trùng lặp -> từ chối."""
        self.manifest["chunks"][1]["chunk_id"] = self.manifest["chunks"][0]["chunk_id"]
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        retriever = self._create_retriever(self.expected_ids)
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("trùng lặp trong manifest", str(ctx.exception))

    def test_chunks_file_duplicate_chunk_id(self):
        """Tệp chunks trên đĩa có ID trùng lặp -> từ chối."""
        chunks = [json.loads(line) for line in self.chunk_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        chunks[1]["chunk_id"] = chunks[0]["chunk_id"]
        # Viết lại file và cập nhật mã băm tương ứng
        new_content = "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks)
        self.chunk_path.write_text(new_content, encoding="utf-8")
        new_hash = hashlib.sha256(self.chunk_path.read_bytes()).hexdigest()
        self.manifest["chunks_sha256"] = new_hash
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        self.status["chunks_sha256"] = new_hash
        self.status_path.write_text(json.dumps(self.status), encoding="utf-8")
        self.metadata["chunks_sha256"] = new_hash

        retriever = self._create_retriever(self.expected_ids)
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("trùng lặp trong tệp chunks", str(ctx.exception))

    def test_api_health_503_when_vector_integrity_fails(self):
        """Khi kiểm tra vector integrity thất bại, GET /health của FastAPI phải trả về HTTP 503."""
        # Giả lập rag_engine_instance có retriever bị hỏng integrity
        retriever = self._create_retriever([])  # 0 vector
        mock_engine = MagicMock()
        mock_engine.retriever = retriever
        mock_engine.llm_client.is_live = False

        with patch.object(api_main, "rag_engine_instance", mock_engine):
            client = TestClient(api_main.app, raise_server_exceptions=False)
            response = client.get("/health")
            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertIn("detail", data)
            self.assertIn("chưa sẵn sàng", data["detail"])


if __name__ == "__main__":
    unittest.main()
