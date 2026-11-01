# -*- coding: utf-8 -*-
"""
tests.test_hybrid_bm25_rrf
Bộ kiểm thử tự động toàn diện cho Module BM25 Okapi Sparse Search và Reciprocal Rank Fusion (RRF).
Kiểm thử độc lập không phụ thuộc mạng hay dịch vụ bên ngoài (Nhiệm vụ 05 - Chặng B & Chốt R02):
1. Tokenizer tiếng Việt: Chuẩn hóa NFC, lowercase, giữ nguyên dấu tiếng Việt và các con số quy chế (03, 10, 580...).
2. Chỉ mục BM25 Okapi: Xây dựng đúng 104 chunks, avgdl hợp lệ, IDF không âm.
3. Fail-closed & Integrity:
   - Thiếu chunks file -> KnowledgeBaseNotReadyError.
   - Trùng lặp chunk_id -> KnowledgeBaseNotReadyError.
   - Lệch tập ID với manifest -> KnowledgeBaseNotReadyError.
   - Cache invalidation khi corpus_fingerprint thay đổi.
4. Tìm kiếm BM25: Deterministic, không trả về zero-score hits, rỗng khi query không khớp.
5. RRF tính tay (Hand-calculated verification): So khớp chính xác số liệu tính tay từ ví dụ nhỏ.
6. Hợp đồng RRF:
   - Rank cuối cùng từ 1..k.
   - Sparse-only hits: similarity và distance là None (nullable), không giả mạo 0.0.
   - Sparse-only có thể xếp trước dense-only nếu RRF cao hơn.
   - is_cross_page bảo toàn dưới dạng boolean.
7. Deduplication và Tie-breaking ổn định: Không nhân đôi chunk_id, tie-break nhất quán.
8. VectorRetriever.retrieve_hybrid: Tích hợp mượt mà, bảo toàn source spans và metadata.
9. API /chat mode validation: Hỗ trợ 'dense' và 'hybrid', từ chối mode lạ với HTTP 422, test hoàn toàn độc lập qua mock/restore.
"""

import json
import math
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient

from backend.bm25_retriever import (
    BM25OkapiIndex,
    compute_sha256,
    reciprocal_rank_fusion,
    tokenize_vietnamese,
)
from backend.config import CHUNKS_FILE, MANIFEST_FILE
from backend.errors import KnowledgeBaseNotReadyError, ValidationError
import backend.main as main_module
from backend.main import app
from backend.rag_engine import CitationItem, RAGEngine, RAGResponse
from backend.retrieval import VectorRetriever


class TestVietnameseTokenizer(unittest.TestCase):
    """Kiểm thử tokenizer tiếng Việt cho BM25."""

    def test_tokenize_normalization_and_diacritics(self):
        text = "Quy chế Đào tạo ĐH (QĐ 580/QĐ-ĐHNCT) — Điều 17. Đánh giá và tính điểm học phần!"
        tokens = tokenize_vietnamese(text)
        self.assertIn("quy", tokens)
        self.assertIn("chế", tokens)
        self.assertIn("đào", tokens)
        self.assertIn("tạo", tokens)
        self.assertIn("đh", tokens)
        self.assertIn("qđ", tokens)
        self.assertIn("580", tokens)
        self.assertIn("đhnct", tokens)
        self.assertIn("điều", tokens)
        self.assertIn("17", tokens)
        self.assertIn("học", tokens)
        self.assertIn("phần", tokens)

    def test_tokenize_numbers_and_special_terms(self):
        text = "Mỗi năm gồm 03 học kỳ, thời lượng từ 10 đến 12 tuần."
        tokens = tokenize_vietnamese(text)
        self.assertIn("03", tokens)
        self.assertIn("10", tokens)
        self.assertIn("12", tokens)

    def test_tokenize_empty_and_spaces(self):
        self.assertEqual(tokenize_vietnamese(""), [])
        self.assertEqual(tokenize_vietnamese("   \n\t   "), [])


class TestBM25Index(unittest.TestCase):
    """Kiểm thử cấu trúc, tính toán và bảo vệ toàn vẹn BM25 Okapi."""

    @classmethod
    def setUpClass(cls):
        cls.bm25 = BM25OkapiIndex(chunks_file_path=CHUNKS_FILE, manifest_file_path=MANIFEST_FILE)

    def test_index_size_and_statistics(self):
        self.assertEqual(self.bm25.doc_count, 104)
        self.assertGreater(self.bm25.avgdl, 0.0)
        self.assertGreater(len(self.bm25.idf), 100)
        # Toàn bộ giá trị IDF phải dương
        for term, val in self.bm25.idf.items():
            self.assertGreater(val, 0.0)

    def test_search_empty_or_non_existent(self):
        # Query rỗng
        self.assertEqual(self.bm25.search(""), [])
        # Từ khóa hoàn toàn không tồn tại -> Không trả về zero-score hits
        self.assertEqual(self.bm25.search("xyzqweasdzxcnotexisting123456"), [])

    def test_search_relevant_query_has_positive_scores(self):
        results = self.bm25.search("học kỳ chính tối thiểu tín chỉ", top_k=5)
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertIn("chunk_id", r)
            self.assertIn("bm25_rank", r)
            self.assertIn("bm25_score", r)
            self.assertGreater(r["bm25_score"], 0.0)

        # Thứ hạng phải tăng dần liên tục 1, 2, 3...
        ranks = [r["bm25_rank"] for r in results]
        self.assertEqual(ranks, list(range(1, len(results) + 1)))

        # Điểm BM25 phải giảm dần hoặc bằng nhau
        scores = [r["bm25_score"] for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_missing_chunks_file_raises_error(self):
        """Tiền kiểm tra tính toàn vẹn: Tệp chunks không tồn tại -> Báo lỗi Fail-closed."""
        missing_path = Path("non_existent_dir_xyz/missing_chunks.jsonl")
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            BM25OkapiIndex(chunks_file_path=missing_path, manifest_file_path=MANIFEST_FILE)
        self.assertIn("không tồn tại", str(ctx.exception))

    def test_duplicate_chunk_ids_raises_error(self):
        """Phát hiện trùng lặp chunk_id trong tệp chunks -> Raise KnowledgeBaseNotReadyError."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_chunks = Path(tmp_dir) / "dup_chunks.jsonl"
            c1 = {"chunk_id": "chunk_dup", "content": "Nội dung 1", "embedding_text": "Nội dung 1"}
            c2 = {"chunk_id": "chunk_dup", "content": "Nội dung 2", "embedding_text": "Nội dung 2"}
            with open(tmp_chunks, "w", encoding="utf-8") as f:
                f.write(json.dumps(c1) + "\n")
                f.write(json.dumps(c2) + "\n")

            with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
                BM25OkapiIndex(chunks_file_path=tmp_chunks, manifest_file_path=Path(tmp_dir) / "none.json")
            self.assertIn("trùng lặp", str(ctx.exception).lower())

    def test_manifest_id_set_mismatch_raises_error(self):
        """Lệch tập ID giữa manifest và chunks file -> Raise KnowledgeBaseNotReadyError."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_chunks = Path(tmp_dir) / "chunks.jsonl"
            tmp_manifest = Path(tmp_dir) / "manifest.json"

            c1 = {"chunk_id": "chunk_01", "content": "Nội dung 1", "embedding_text": "Nội dung 1"}
            with open(tmp_chunks, "w", encoding="utf-8") as f:
                f.write(json.dumps(c1) + "\n")

            actual_hash = compute_sha256(tmp_chunks)
            manifest_content = {
                "corpus_fingerprint": "fake_fp",
                "chunks_sha256": actual_hash,
                "model_revision": "main",
                "total_chunks": 1,
                "chunks": [{"chunk_id": "chunk_DIFF"}]
            }
            with open(tmp_manifest, "w", encoding="utf-8") as f:
                json.dump(manifest_content, f)

            with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
                BM25OkapiIndex(chunks_file_path=tmp_chunks, manifest_file_path=tmp_manifest)
            self.assertIn("không khớp với manifest", str(ctx.exception))


class TestReciprocalRankFusion(unittest.TestCase):
    """Kiểm thử giải thuật Reciprocal Rank Fusion (RRF)."""

    def test_rrf_hand_calculated_example(self):
        """
        Ví dụ tính tay với k=60:
        Item A: dense rank 1, bm25 rank 2 -> RRF = 1/61 + 1/62 = 0.0163934 + 0.0161290 = 0.032522
        Item B: dense rank 2, không có trong bm25 -> RRF = 1/62 = 0.016129
        Item C: không có trong dense, bm25 rank 1 -> RRF = 1/61 = 0.016393
        Thứ tự xếp hạng kỳ vọng: Item A (0.032522) > Item C (0.016393) > Item B (0.016129)
        """
        dense_hits = [
            {"chunk_id": "item_A", "similarity": 0.85, "distance": 0.15},
            {"chunk_id": "item_B", "similarity": 0.70, "distance": 0.30},
        ]
        bm25_hits = [
            {"chunk_id": "item_C", "bm25_score": 12.5, "bm25_rank": 1},
            {"chunk_id": "item_A", "bm25_score": 9.2, "bm25_rank": 2},
        ]

        fused = reciprocal_rank_fusion(dense_hits, bm25_hits, rrf_k=60, top_k=3)
        self.assertEqual(len(fused), 3)

        # Kiểm tra thứ tự
        self.assertEqual(fused[0]["chunk_id"], "item_A")
        self.assertEqual(fused[1]["chunk_id"], "item_C")
        self.assertEqual(fused[2]["chunk_id"], "item_B")

        # Kiểm tra số điểm RRF tính toán
        expected_score_a = round(1.0 / 61.0 + 1.0 / 62.0, 6)
        expected_score_c = round(1.0 / 61.0, 6)
        expected_score_b = round(1.0 / 62.0, 6)

        self.assertAlmostEqual(fused[0]["rrf_score"], expected_score_a, places=5)
        self.assertAlmostEqual(fused[1]["rrf_score"], expected_score_c, places=5)
        self.assertAlmostEqual(fused[2]["rrf_score"], expected_score_b, places=5)

        # Kiểm tra rank cuối cùng từ 1..k
        self.assertEqual(fused[0]["rank"], 1)
        self.assertEqual(fused[1]["rank"], 2)
        self.assertEqual(fused[2]["rank"], 3)

        # Kiểm tra metadata xếp hạng riêng biệt
        self.assertEqual(fused[0]["dense_rank"], 1)
        self.assertEqual(fused[0]["bm25_rank"], 2)
        self.assertEqual(fused[1]["dense_rank"], None)
        self.assertEqual(fused[1]["bm25_rank"], 1)

    def test_rrf_sparse_only_contract(self):
        """Hit chỉ có ở BM25: similarity & distance là None (nullable), không giả mạo 0.0, rank = 1..k."""
        dense_hits = []
        bm25_hits = [
            {
                "chunk_id": "sparse_only_chunk",
                "bm25_score": 15.0,
                "bm25_rank": 1,
                "article": "Điều 10",
                "start_page_pdf": 5,
                "end_page_pdf": 6,
                "content": "Nội dung điều 10",
            }
        ]

        fused = reciprocal_rank_fusion(dense_hits, bm25_hits, rrf_k=60, top_k=5)
        self.assertEqual(len(fused), 1)
        item = fused[0]

        self.assertEqual(item["rank"], 1)
        self.assertIsNone(item["similarity"])
        self.assertIsNone(item["distance"])
        self.assertEqual(item["dense_rank"], None)
        self.assertEqual(item["dense_score"], None)
        self.assertEqual(item["bm25_rank"], 1)
        self.assertEqual(item["bm25_score"], 15.0)
        self.assertTrue(item["is_cross_page"])

    def test_rrf_sparse_only_can_rank_before_dense_only(self):
        """Sparse-only rank 1 (1/61=0.016393) đứng trước Dense-only rank 10 (1/70=0.014285)."""
        dense_hits = [
            {"chunk_id": "dense_low_rank", "similarity": 0.50, "distance": 0.50}  # dense_rank=1 nếu đứng 1 mình
        ]
        # Giả lập dense_hits đã có rank=10 bằng cách thêm dummy items
        dense_hits_10 = [{"chunk_id": f"d_{i}", "similarity": 0.9 - i*0.01} for i in range(1, 10)]
        dense_hits_10.append({"chunk_id": "dense_item_10", "similarity": 0.40, "distance": 0.60})

        bm25_hits = [
            {"chunk_id": "sparse_item_1", "bm25_score": 25.0, "bm25_rank": 1}
        ]

        fused = reciprocal_rank_fusion(dense_hits_10, bm25_hits, rrf_k=60, top_k=20)
        # sparse_item_1 có RRF = 1/61 = 0.016393
        # dense_item_10 có RRF = 1/70 = 0.014285
        # Do đó sparse_item_1 phải đứng trước dense_item_10!
        sparse_rank = next(item["rank"] for item in fused if item["chunk_id"] == "sparse_item_1")
        dense_10_rank = next(item["rank"] for item in fused if item["chunk_id"] == "dense_item_10")
        self.assertLess(sparse_rank, dense_10_rank)

    def test_rrf_tie_breaking(self):
        """Khi RRF score bằng nhau, ưu tiên dense_rank nhỏ hơn, rồi đến chunk_id theo chữ cái."""
        dense_hits = [
            {"chunk_id": "chunk_z", "similarity": 0.80},  # dense rank 1 -> rrf = 1/61
        ]
        bm25_hits = [
            {"chunk_id": "chunk_a", "bm25_score": 10.0, "bm25_rank": 1},  # bm25 rank 1 -> rrf = 1/61
        ]
        fused = reciprocal_rank_fusion(dense_hits, bm25_hits, rrf_k=60, top_k=2)
        # Cả 2 đều có điểm 1/61, chunk_z có dense_rank=1 còn chunk_a có dense_rank=None -> chunk_z đứng trước
        self.assertEqual(fused[0]["chunk_id"], "chunk_z")
        self.assertEqual(fused[1]["chunk_id"], "chunk_a")


class TestHybridIntegration(unittest.TestCase):
    """Kiểm thử tích hợp Hybrid Search trong VectorRetriever và RAGEngine."""

    def setUp(self):
        # Lưu trữ trạng thái ban đầu của rag_engine_instance
        self.original_engine = main_module.rag_engine_instance

        # Thiết lập mock engine độc lập hoàn toàn cho API testing
        self.mock_engine = MagicMock(spec=RAGEngine)
        self.mock_response = RAGResponse(
            request_id="test-isolated-req-id",
            question="Học kỳ có mấy tuần?",
            status="answered",
            answer="Mỗi năm gồm 03 học kỳ theo quy chế QĐ 580.",
            citations=[
                CitationItem(
                    source_id="SRC-1",
                    chunk_id="qd580_rec_chunk_003",
                    document_id="QD580_DHNCT_2024",
                    article="Điều 3",
                    pdf_page=4,
                    printed_page=2,
                    quote_snippet="Mỗi năm gồm 03 học kỳ...",
                    similarity=None,  # Thử nghiệm nullable similarity của sparse hit
                    spans=[],
                )
            ],
            sources_considered=5,
            sources_cited=1,
            timings={"total_ms": 50.0, "retrieval_ms": 10.0, "llm_generation_ms": 40.0},
            is_live_llm=False,
            model_name="mock-gemini-test",
        )
        self.mock_engine.answer_question.return_value = self.mock_response
        main_module.rag_engine_instance = self.mock_engine

    def tearDown(self):
        # Khôi phục trạng thái toàn cục nguyên vẹn
        main_module.rag_engine_instance = self.original_engine

    def test_vector_retriever_retrieve_hybrid_integration(self):
        retriever = VectorRetriever()
        results = retriever.retrieve_hybrid("Thời lượng mỗi học kỳ là bao nhiêu tuần?", top_k=5)
        self.assertEqual(len(results), 5)

        for rank, r in enumerate(results, start=1):
            self.assertEqual(r["rank"], rank)
            self.assertIn("chunk_id", r)
            self.assertIn("article", r)
            self.assertIn("rrf_score", r)
            self.assertIn("source_spans", r)
            self.assertIn("similarity", r)
            self.assertIn("is_cross_page", r)

    def test_retriever_check_readiness_fail_closed_missing_chunks(self):
        """Kiểm tra check_readiness từ chối dứt khoát khi thiếu chunks_file_path."""
        retriever = VectorRetriever(chunks_file_path=Path("non_existent_chunks.jsonl"))
        with self.assertRaises(KnowledgeBaseNotReadyError) as ctx:
            retriever.check_readiness()
        self.assertIn("không tồn tại", str(ctx.exception).lower())

    def test_bm25_cache_invalidation_on_fingerprint_change(self):
        """Chỉ mục BM25 tự động xây dựng lại khi corpus_fingerprint thay đổi."""
        retriever = VectorRetriever()
        bm25_first = retriever.bm25_index
        first_fp = bm25_first.indexed_fingerprint

        # Mock check_readiness trả về fingerprint mới
        with patch.object(retriever, "check_readiness", return_value={"status": "READY", "corpus_fingerprint": "new_fp_test_123"}):
            with patch("backend.bm25_retriever.BM25OkapiIndex") as mock_bm25_class:
                mock_new_bm25 = MagicMock()
                mock_new_bm25.indexed_fingerprint = "new_fp_test_123"
                mock_bm25_class.return_value = mock_new_bm25

                reloaded_bm25 = retriever.bm25_index
                mock_bm25_class.assert_called_once()
                self.assertEqual(reloaded_bm25.indexed_fingerprint, "new_fp_test_123")

    def test_api_chat_endpoint_mode_validation(self):
        client = TestClient(app, raise_server_exceptions=False)

        # 1. Mode không hợp lệ -> HTTP 422
        res_bad = client.post("/chat", json={"question": "Kiểm tra?", "mode": "invalid_mode_xyz"})
        self.assertEqual(res_bad.status_code, 422)
        self.assertIn("Chỉ chấp nhận 'dense' hoặc 'hybrid'", res_bad.json()["detail"])

        # 2. Mode dense hợp lệ -> HTTP 200, truyền đúng mode="dense" xuống engine
        res_dense = client.post("/chat", json={"question": "Học kỳ có mấy tuần?", "mode": "dense"})
        self.assertEqual(res_dense.status_code, 200)
        self.mock_engine.answer_question.assert_called_with("Học kỳ có mấy tuần?", mode="dense")
        data_dense = res_dense.json()
        self.assertEqual(data_dense["status"], "answered")
        self.assertIsNone(data_dense["citations"][0]["similarity"])

        # 3. Mode hybrid hợp lệ -> HTTP 200, truyền đúng mode="hybrid" xuống engine
        res_hybrid = client.post("/chat", json={"question": "Học kỳ có mấy tuần?", "mode": "hybrid"})
        self.assertEqual(res_hybrid.status_code, 200)
        self.mock_engine.answer_question.assert_called_with("Học kỳ có mấy tuần?", mode="hybrid")


if __name__ == "__main__":
    unittest.main()
