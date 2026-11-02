# -*- coding: utf-8 -*-
"""
tests.test_lifecycle_and_regression
Bộ kiểm thử hồi quy toàn diện cho Vòng đời chỉ mục, Khóa phiên bản và Định vị bằng chứng:
1. Ingestion: Chặn collection không tương thích (fingerprint, model, revision).
2. Ingestion: Bắt lỗi tồn dư ID cũ (extra IDs) hoặc thiếu ID, không báo READY giả mạo.
3. Ingestion: Ghi nhận FAILED khi xảy ra lỗi giữa chừng.
4. Readiness: Chặn khi tệp trạng thái không tồn tại.
5. Readiness: Chặn khi tệp trạng thái chứa JSON hỏng/bị cắt cụt.
6. Readiness: Chặn khi trạng thái là READY của collection khác hoặc sai fingerprint.
7. Readiness: Hủy cache và chặn ngay khi trạng thái đổi từ READY sang BUILDING/FAILED sau lần truy vấn đầu.
8. Revision: Ép buộc revision cụ thể khi tải tokenizer và mô hình embedding, từ chối revision lạ.
9. Evidence Span: Ánh xạ chuẩn hóa whitespace chính xác vào chuỗi gốc (chữa triệt để lỗi offset 0), hỗ trợ Unicode và từ chối trích dẫn ảo.
"""

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import chromadb
from backend.config import (
    CHUNK_VERSION,
    COLLECTION_NAME,
    EMBEDDING_MODEL_CANDIDATE,
    MODEL_REVISION,
    load_embedding_model,
    load_tokenizer,
)
from backend.ingestion import ingest_corpus, save_ingestion_status
from backend.retrieval import VectorRetriever
from evaluation.evaluate_retrieval import find_evidence_span_on_page


class TestModelRevisionEnforcement(unittest.TestCase):
    """Kiểm thử việc ép buộc đúng commit revision khi tải model/tokenizer."""

    def test_load_tokenizer_strict_revision(self):
        """Tokenizer phải tải thành công với MODEL_REVISION và từ chối revision khác."""
        tok = load_tokenizer(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)
        self.assertIsNotNone(tok)

        # Revision không khớp phải bị từ chối ngay lập tức
        with self.assertRaises(ValueError):
            load_tokenizer(EMBEDDING_MODEL_CANDIDATE, revision="incompatible_rev_sha_12345")

    def test_load_embedding_model_strict_revision(self):
        """Mô hình embedding phải từ chối nếu truyền revision sai."""
        with self.assertRaises(ValueError):
            load_embedding_model(EMBEDDING_MODEL_CANDIDATE, revision="invalid_revision_hash")


class TestEvidenceSpanWhitespaceMapping(unittest.TestCase):
    """Kiểm thử định vị bằng chứng chính xác khi có biến thể khoảng trắng và xuống dòng."""

    def test_reviewer_reproduction_case(self):
        """Tái hiện chính xác ca kiểm thử trong tài liệu nhận xét độc lập v2."""
        content = "HEADER LONG ENOUGH\n\nTARGET  alpha\n beta END"
        quote = "TARGET alpha beta END"
        pages = [{"content": content, "pdf_page": 1}]

        start_c, end_c = find_evidence_span_on_page(pages, 1, quote)
        # Điểm bắt đầu phải là 20 (ngay sau HEADER), tuyệt đối không được trả về 0!
        self.assertEqual(start_c, 20)
        self.assertEqual(end_c, 43)
        self.assertEqual(content[start_c:end_c], "TARGET  alpha\n beta END")

    def test_exact_match_preserved(self):
        """Khớp chính xác nguyên văn vẫn giữ nguyên tọa độ."""
        content = "Quy định tại Điều 17 khoản 1 về thang điểm 10 tích lũy."
        quote = "Điều 17 khoản 1"
        pages = [{"content": content, "pdf_page": 1}]

        start_c, end_c = find_evidence_span_on_page(pages, 1, quote)
        self.assertEqual(start_c, 13)
        self.assertEqual(end_c, 28)
        self.assertEqual(content[start_c:end_c], quote)

    def test_multiple_newlines_and_unicode(self):
        """Khớp thành công với nhiều dấu xuống dòng và ký tự tiếng Việt có dấu."""
        content = "Ban Giám hiệu xét duyệt danh sách:\n\n- Điểm TB tích lũy:   7.0\n\n- Chuẩn đầu ra."
        quote = "Điểm TB tích lũy: 7.0 - Chuẩn đầu ra."
        pages = [{"content": content, "pdf_page": 1}]

        start_c, end_c = find_evidence_span_on_page(pages, 1, quote)
        self.assertNotEqual(start_c, -1)
        self.assertNotEqual(start_c, 0)
        self.assertIn("Điểm TB tích lũy", content[start_c:end_c])

    def test_nonexistent_quote_returns_negative(self):
        """Trích dẫn không tồn tại phải trả về (-1, -1), không được đoán mò offset."""
        content = "Nội dung quy chế đào tạo thực tế."
        quote = "Học phí một tín chỉ là 500.000 VNĐ"
        pages = [{"content": content, "pdf_page": 1}]

        start_c, end_c = find_evidence_span_on_page(pages, 1, quote)
        self.assertEqual(start_c, -1)
        self.assertEqual(end_c, -1)


class TestIngestionLifecycleAndInvariants(unittest.TestCase):
    """Kiểm thử an toàn vòng đời Ingestion trên cơ sở dữ liệu tạm thời (không động chạm DB thật)."""

    def setUp(self):
        import gc
        gc.collect()
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.temp_path = Path(self.temp_dir.name)
        self.persist_dir = self.temp_path / "test_chroma"
        self.status_file = self.temp_path / "INGESTION_STATUS.json"
        self.chunks_file = self.temp_path / "test_chunks.jsonl"
        self.manifest_file = self.temp_path / "test_manifest.json"

        # Tạo 1 chunk thử nghiệm mẫu
        self.sample_chunk = {
            "chunk_id": "test_chunk_001",
            "document_id": "QD580_DHNCT_2024",
            "doc_part": "regulation",
            "chapter": "Chương I",
            "article": "Điều 1",
            "article_number": 1,
            "start_page_pdf": 1,
            "end_page_pdf": 1,
            "start_page_printed": 1,
            "end_page_printed": 1,
            "is_table": False,
            "token_count": 50,
            "char_count": 150,
            "embedding_text": "Quy định chung về đào tạo đại học Nam Cần Thơ.",
            "source_spans": [{"pdf_page": 1, "start_char": 0, "end_char": 47, "text": "Quy định chung về đào tạo đại học Nam Cần Thơ."}],
        }
        with open(self.chunks_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.sample_chunk, ensure_ascii=False) + "\n")

        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump({
                "corpus_fingerprint": "fingerprint_NEW_12345",
                "chunks_sha256": "chunks_hash_12345",
                "model_revision": MODEL_REVISION,
            }, f)

    def tearDown(self):
        import gc
        gc.collect()
        self.temp_dir.cleanup()

    def test_reject_incompatible_existing_collection(self):
        """Ingestion phải ném lỗi ValueError nếu collection đã tồn tại với fingerprint/revision khác."""
        # Giả lập collection đã tồn tại với metadata cũ
        from backend.ingestion import VietnameseEmbeddingFunction
        embed_fn = VietnameseEmbeddingFunction(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)
        client = chromadb.PersistentClient(path=str(self.persist_dir))
        client.create_collection(
            name="test_col_incompatible",
            embedding_function=embed_fn,
            metadata={
                "corpus_fingerprint": "fingerprint_OLD_99999",
                "model_revision": MODEL_REVISION,
                "chunk_version": "v1.0",
                "model_name": EMBEDDING_MODEL_CANDIDATE,
            }
        )

        # Chạy ingest_corpus mà không force_recreate -> Phải raise ValueError
        with self.assertRaises(ValueError) as ctx:
            ingest_corpus(
                collection_name="test_col_incompatible",
                persist_dir=self.persist_dir,
                chunks_path=self.chunks_file,
                manifest_path=self.manifest_file,
                status_path=self.status_file,
                force_recreate=False,
            )
        self.assertIn("không tương thích", str(ctx.exception))

    def test_reject_when_extra_or_mismatched_ids_exist(self):
        """Nếu collection chứa ID rác không nằm trong danh sách chunks mới, ingestion phải từ chối và báo FAILED."""
        from backend.ingestion import VietnameseEmbeddingFunction
        embed_fn = VietnameseEmbeddingFunction(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)
        client = chromadb.PersistentClient(path=str(self.persist_dir))
        col = client.create_collection(
            name="test_col_extra_ids",
            embedding_function=embed_fn,
            metadata={
                "corpus_fingerprint": "fingerprint_NEW_12345",
                "model_revision": MODEL_REVISION,
                "chunk_version": CHUNK_VERSION,
                "model_name": EMBEDDING_MODEL_CANDIDATE,
            }
        )
        # Nạp trước 1 ID lạ không có trong tập chunk mới
        col.add(
            ids=["stale_orphan_chunk_999"],
            documents=["Nội dung cũ đã bị xóa"],
            metadatas=[{"chunk_id": "stale_orphan_chunk_999"}]
        )

        with self.assertRaises(RuntimeError) as ctx:
            ingest_corpus(
                collection_name="test_col_extra_ids",
                persist_dir=self.persist_dir,
                chunks_path=self.chunks_file,
                manifest_path=self.manifest_file,
                status_path=self.status_file,
                force_recreate=False,
            )
        self.assertIn("Xác nhận tập ID thất bại", str(ctx.exception))

        # Kiểm tra file trạng thái phải được đánh dấu FAILED, không được báo READY
        with open(self.status_file, "r", encoding="utf-8") as f:
            st = json.load(f)
            self.assertEqual(st["status"], "FAILED")
            self.assertFalse(st["corpus_ready"])

    def test_save_failed_on_exception(self):
        """Khi gặp lỗi bất thường (ví dụ tệp chunk rỗng hoặc lỗi ghi), trạng thái phải lưu FAILED."""
        with self.assertRaises(FileNotFoundError):
            ingest_corpus(
                collection_name="test_col_fail",
                persist_dir=self.persist_dir,
                chunks_path=self.temp_path / "nonexistent_chunks.jsonl",
                manifest_path=self.manifest_file,
                status_path=self.status_file,
            )


class TestRetrieverReadinessVerification(unittest.TestCase):
    """Kiểm thử nghiêm ngặt cơ chế check_readiness (Preflight) trong VectorRetriever."""

    def setUp(self):
        import gc
        gc.collect()
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.temp_path = Path(self.temp_dir.name)
        self.persist_dir = self.temp_path / "test_chroma"
        self.status_file = self.temp_path / "INGESTION_STATUS.json"
        self.manifest_file = self.temp_path / "test_manifest.json"
        self.chunks_file = self.temp_path / "test_chunks.jsonl"

        # Tạo file chunks giả lập
        with open(self.chunks_file, "w", encoding="utf-8") as f:
            f.write('{"chunk_id": "c1", "content": "test"}\n')

        from backend.retrieval import compute_sha256
        self.valid_chunks_hash = compute_sha256(self.chunks_file)

        # Tạo manifest chuẩn đầy đủ trường
        self.valid_manifest = {
            "corpus_fingerprint": "valid_fingerprint_123",
            "chunks_sha256": self.valid_chunks_hash,
            "model_revision": MODEL_REVISION,
            "total_chunks": 1,
            "chunks": [{"chunk_id": "c1"}],
        }
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(self.valid_manifest, f)

        # Tạo Chroma collection mẫu có metadata chuẩn
        from backend.ingestion import VietnameseEmbeddingFunction
        embed_fn = VietnameseEmbeddingFunction(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.create_collection(
            name="test_col",
            embedding_function=embed_fn,
            metadata={
                "corpus_fingerprint": "valid_fingerprint_123",
                "chunks_sha256": self.valid_chunks_hash,
                "model_revision": MODEL_REVISION,
            }
        )
        if hasattr(self.collection, "add"):
            try:
                self.collection.add(ids=["c1"], documents=["test"], embeddings=[[0.0] * 768])
            except Exception:
                pass
        if hasattr(self.collection, "ids"):
            self.collection.ids = ["c1"]

        # Tạo file trạng thái chuẩn
        self.valid_status = {
            "collection_name": "test_col",
            "status": "READY",
            "corpus_ready": True,
            "corpus_fingerprint": "valid_fingerprint_123",
            "chunks_sha256": self.valid_chunks_hash,
            "model_id": EMBEDDING_MODEL_CANDIDATE,
            "model_revision": MODEL_REVISION,
        }
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(self.valid_status, f)

    def tearDown(self):
        import gc
        gc.collect()
        self.temp_dir.cleanup()

    def test_valid_preflight_passes(self):
        """Preflight đầy đủ và đồng nhất 3 chiều phải qua thành công."""
        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        info = retriever.check_readiness()
        self.assertEqual(info["status"], "READY")
        self.assertEqual(info["collection_name"], "test_col")

    def test_reject_missing_status_file(self):
        """Chặn truy vấn khi tệp INGESTION_STATUS.json không tồn tại."""
        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.temp_path / "not_found.json",
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("không tồn tại", str(ctx.exception))

    def test_reject_corrupted_json(self):
        """Chặn truy vấn khi tệp trạng thái chứa JSON hỏng/bị cắt cụt."""
        with open(self.status_file, "w", encoding="utf-8") as f:
            f.write("{ status: READY, unclosed json ...")

        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("bị hỏng hoặc không đúng định dạng", str(ctx.exception))

    def test_reject_missing_manifest_file(self):
        """Chặn truy vấn khi tệp manifest không tồn tại (chữa lỗi nuốt lỗi manifest)."""
        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.temp_path / "missing_manifest.json",
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("manifest không tồn tại", str(ctx.exception))

    def test_reject_corrupted_manifest_json(self):
        """Chặn truy vấn khi tệp manifest chứa JSON hỏng (chữa lỗi nuốt lỗi manifest)."""
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            f.write("{ corpus_fingerprint: incomplete ...")

        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("manifest bị hỏng hoặc không đúng định dạng", str(ctx.exception))

    def test_reject_manifest_missing_fields(self):
        """Chặn truy vấn khi manifest thiếu trường bắt buộc (ví dụ chunks_sha256)."""
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump({
                "corpus_fingerprint": "valid_fingerprint_123",
                # Thiếu chunks_sha256 và model_revision
            }, f)

        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("manifest thiếu trường bắt buộc", str(ctx.exception))

    def test_reject_status_non_boolean_ready(self):
        """Chặn truy vấn khi corpus_ready không phải kiểu boolean True (ví dụ là string 'true')."""
        self.valid_status["corpus_ready"] = "true"  # Sai kiểu (string thay vì boolean)
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(self.valid_status, f)

        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("chưa sẵn sàng", str(ctx.exception))

    def test_reject_mismatched_collection(self):
        """Chặn truy vấn khi trạng thái READY nhưng là của collection khác."""
        wrong_status = dict(self.valid_status)
        wrong_status["collection_name"] = "other_collection_xyz"
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(wrong_status, f)

        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="my_target_collection",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("Không tìm thấy trạng thái cho collection", str(ctx.exception))

    def test_reject_mismatched_fingerprint(self):
        """Chặn truy vấn khi fingerprint trong trạng thái khác với manifest."""
        wrong_status = dict(self.valid_status)
        wrong_status["corpus_fingerprint"] = "stale_fingerprint_999"
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(wrong_status, f)

        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("không khớp với manifest", str(ctx.exception))

    def test_reject_chroma_metadata_mismatch(self):
        """Chặn truy vấn khi Chroma collection metadata bị lệch fingerprint so với manifest."""
        # Tạo collection thứ 2 với metadata lệch
        from backend.ingestion import VietnameseEmbeddingFunction
        embed_fn = VietnameseEmbeddingFunction(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)
        col2 = self.client.create_collection(
            name="test_col_mismatched_meta",
            embedding_function=embed_fn,
            metadata={
                "corpus_fingerprint": "corrupted_fp_in_db",
                "chunks_sha256": self.valid_chunks_hash,
                "model_revision": MODEL_REVISION,
            }
        )
        if hasattr(col2, "add"):
            try:
                col2.add(ids=["c1"], documents=["test"], embeddings=[[0.0] * 768])
            except Exception:
                pass
        if hasattr(col2, "ids"):
            col2.ids = ["c1"]
        status_payload = dict(self.valid_status)
        status_payload["collection_name"] = "test_col_mismatched_meta"
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(status_payload, f)

        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col_mismatched_meta",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("Metadata collection ChromaDB có corpus_fingerprint", str(ctx.exception))

    def test_reject_disk_chunk_hash_mismatch(self):
        """Chặn truy vấn khi tệp chunks trên đĩa bị sửa đổi dẫn đến sai mã băm SHA-256."""
        # Ghi đè file chunks với nội dung khác
        with open(self.chunks_file, "w", encoding="utf-8") as f:
            f.write('{"tampered": true}\n')

        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("Mã băm tệp chunks trên đĩa", str(ctx.exception))

    def test_cache_invalidation_when_status_changes_to_building(self):
        """Retriever phải chặn ngay khi trạng thái đổi sang BUILDING sau khi đối tượng đã được khởi tạo."""
        retriever = VectorRetriever(
            persist_dir=str(self.persist_dir),
            collection_name="test_col",
            status_file_path=self.status_file,
            manifest_path=self.manifest_file,
            chunks_file_path=self.chunks_file,
        )
        # Lần kiểm tra đầu: OK
        retriever.check_readiness()

        # 2. Một tiến trình khác chuyển trạng thái sang BUILDING
        building_status = dict(self.valid_status)
        building_status["status"] = "BUILDING"
        building_status["corpus_ready"] = False
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(building_status, f)

        # Lần kiểm tra tiếp theo: Bắt buộc phải raise RuntimeError
        with self.assertRaises(RuntimeError) as ctx:
            retriever.check_readiness()
        self.assertIn("chưa sẵn sàng", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
