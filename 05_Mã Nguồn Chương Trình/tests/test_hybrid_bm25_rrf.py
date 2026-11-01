# -*- coding: utf-8 -*-
"""
tests.test_hybrid_bm25_rrf
Bộ kiểm thử tự động toàn diện cho Module BM25 Okapi Sparse Search và Reciprocal Rank Fusion (RRF).
Kiểm thử độc lập không phụ thuộc mạng hay dịch vụ bên ngoài (Nhiệm vụ 05 - Chặng B):
1. Tokenizer tiếng Việt: Chuẩn hóa NFC, lowercase, giữ nguyên dấu tiếng Việt và các con số quy chế (03, 10, 580...).
2. Chỉ mục BM25 Okapi: Xây dựng đúng 104 chunks, avgdl hợp lệ, IDF không âm.
3. Tìm kiếm BM25: Deterministic, không trả về zero-score hits, rỗng khi query không khớp.
4. RRF tính tay (Hand-calculated verification): So khớp chính xác số liệu tính tay từ ví dụ nhỏ.
5. Deduplication và Tie-breaking ổn định: Không nhân đôi chunk_id, tie-break nhất quán.
6. VectorRetriever.retrieve_hybrid: Tích hợp mượt mà, bảo toàn source spans và metadata.
7. API /chat mode validation: Hỗ trợ 'dense' và 'hybrid', từ chối mode lạ với HTTP 422.
"""

import json
import math
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient

from backend.bm25_retriever import (
    BM25OkapiIndex,
    reciprocal_rank_fusion,
    tokenize_vietnamese,
)
from backend.config import CHUNKS_FILE, MANIFEST_FILE
from backend.main import app
from backend.rag_engine import RAGEngine
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
    """Kiểm thử cấu trúc và tính toán BM25 Okapi."""

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
            {"chunk_id": "item_A", "similarity": 0.85},
            {"chunk_id": "item_B", "similarity": 0.70},
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

        # Kiểm tra metadata xếp hạng riêng biệt
        self.assertEqual(fused[0]["dense_rank"], 1)
        self.assertEqual(fused[0]["bm25_rank"], 2)
        self.assertEqual(fused[1]["dense_rank"], None)
        self.assertEqual(fused[1]["bm25_rank"], 1)

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

    def test_vector_retriever_retrieve_hybrid_integration(self):
        retriever = VectorRetriever()
        results = retriever.retrieve_hybrid("Thời lượng mỗi học kỳ là bao nhiêu tuần?", top_k=5)
        self.assertEqual(len(results), 5)

        for r in results:
            self.assertIn("chunk_id", r)
            self.assertIn("article", r)
            self.assertIn("rrf_score", r)
            self.assertIn("source_spans", r)
            self.assertIn("similarity", r)

    def test_api_chat_endpoint_mode_validation(self):
        client = TestClient(app, raise_server_exceptions=False)

        # 1. Mode không hợp lệ -> HTTP 422
        res_bad = client.post("/chat", json={"question": "Kiểm tra?", "mode": "invalid_mode_xyz"})
        self.assertEqual(res_bad.status_code, 422)
        self.assertIn("Chỉ chấp nhận 'dense' hoặc 'hybrid'", res_bad.json()["detail"])

        # 2. Mode dense hợp lệ -> HTTP 200
        res_dense = client.post("/chat", json={"question": "Học kỳ có mấy tuần?", "mode": "dense"})
        self.assertEqual(res_dense.status_code, 200)

        # 3. Mode hybrid hợp lệ -> HTTP 200
        res_hybrid = client.post("/chat", json={"question": "Học kỳ có mấy tuần?", "mode": "hybrid"})
        self.assertEqual(res_hybrid.status_code, 200)


if __name__ == "__main__":
    unittest.main()
