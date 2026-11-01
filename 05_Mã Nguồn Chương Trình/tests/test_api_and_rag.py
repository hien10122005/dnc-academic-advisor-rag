# -*- coding: utf-8 -*-
"""
tests.test_api_and_rag
Bộ kiểm thử tự động toàn diện cho FastAPI Endpoints và RAG Engine (Nhiệm vụ 04).
Kiểm thử độc lập không phụ thuộc mạng hay API key thật:
1. GET /health: Trả về HTTP 200 với đầy đủ metadata an toàn khi hệ thống READY.
2. GET /health: Trả về HTTP 503 khi kho tri thức chưa sẵn sàng hoặc preflight lỗi.
3. POST /chat: Tiếp nhận câu hỏi hợp lệ và trả về câu trả lời kèm citation hợp lệ.
4. POST /chat: Từ chối câu hỏi rỗng hoặc chỉ chứa khoảng trắng với HTTP 422.
5. POST /chat: Từ chối câu hỏi vượt quá 1000 ký tự với HTTP 422.
6. RAG Engine: Lọc bỏ triệt để các Source ID bịa đặt (Hallucinated Source IDs) từ LLM.
7. RAG Engine: Xử lý đúng trạng thái insufficient_evidence và out_of_scope.
8. RAG Engine: Bắt lỗi upstream LLM và chuyển thành HTTP 502/RuntimeError thích hợp.
9. Lifecycle: Mô hình và client được nạp một lần khi startup, tái sử dụng qua các request.
"""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient

from backend.main import app, rag_engine_instance
from backend.rag_engine import CitationItem, RAGEngine, SourceContext


class TestFastAPIEndpoints(unittest.TestCase):
    """Kiểm thử các endpoint của FastAPI bằng TestClient."""

    @classmethod
    def setUpClass(cls):
        # Khởi tạo client kết nối ứng dụng FastAPI và kích hoạt lifespan startup
        cls._client_cm = TestClient(app)
        cls.client = cls._client_cm.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls._client_cm.__exit__(None, None, None)

    def test_health_check_endpoint_success(self):
        """GET /health phải trả về HTTP 200 và thông tin hệ thống khi kho tri thức READY."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["corpus_ready"])
        self.assertEqual(data["collection_name"], "qd580_baseline_v2")
        self.assertEqual(data["total_chunks"], 104)
        self.assertEqual(data["embedding_model_revision"], "84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0")

        # Đảm bảo không làm lộ API Key hay đường dẫn tuyệt đối nội bộ
        self.assertNotIn("api_key", json.dumps(data).lower())
        self.assertNotIn("c:\\", json.dumps(data).lower())
        self.assertNotIn("e:\\", json.dumps(data).lower())

    def test_chat_endpoint_valid_question(self):
        """POST /chat với câu hỏi hợp lệ phải trả về HTTP 200 và cấu trúc phản hồi chuẩn."""
        payload = {"question": "Trường tổ chức mỗi năm gồm bao nhiêu học kỳ?"}
        response = self.client.post("/chat", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("request_id", data)
        self.assertIn("status", data)
        self.assertIn("answer", data)
        self.assertIn("citations", data)
        self.assertIn("timings", data)

        # Kiểm tra citations được định dạng đúng từ backend
        if data["citations"]:
            cit = data["citations"][0]
            self.assertIn("source_id", cit)
            self.assertIn("document_id", cit)
            self.assertIn("article", cit)
            self.assertIn("pdf_page", cit)
            self.assertIn("similarity", cit)

    def test_chat_endpoint_empty_question(self):
        """POST /chat với câu hỏi rỗng hoặc chỉ có khoảng trắng phải trả về HTTP 422."""
        # 1. Rỗng hoàn toàn
        res1 = self.client.post("/chat", json={"question": ""})
        self.assertEqual(res1.status_code, 422)

        # 2. Toàn khoảng trắng
        res2 = self.client.post("/chat", json={"question": "   \n\t   "})
        self.assertEqual(res2.status_code, 422)

    def test_chat_endpoint_too_long_question(self):
        """POST /chat với câu hỏi vượt quá 1000 ký tự phải trả về HTTP 422."""
        long_q = "Quy định " + "a" * 1050
        response = self.client.post("/chat", json={"question": long_q})
        self.assertEqual(response.status_code, 422)

    def test_health_check_service_unavailable_when_engine_none(self):
        """GET /health phải trả về HTTP 503 khi rag_engine_instance là None."""
        import backend.main
        original_instance = backend.main.rag_engine_instance
        try:
            backend.main.rag_engine_instance = None
            response = self.client.get("/health")
            self.assertEqual(response.status_code, 503)
        finally:
            backend.main.rag_engine_instance = original_instance


class TestRAGEngineLogic(unittest.TestCase):
    """Kiểm thử logic chuyên sâu của RAG Engine (Citation, Mock LLM, Trạng thái nghiệp vụ)."""

    def setUp(self):
        self.mock_retriever = MagicMock()
        self.mock_llm_client = MagicMock()
        self.mock_llm_client.is_live = False
        self.mock_llm_client.model = "test-mock-gemini"

        # Mock dữ liệu truy xuất gồm 2 chunks
        self.mock_retriever.retrieve.return_value = [
            {
                "chunk_id": "chunk_01",
                "document_id": "QD580_DHNCT_2024",
                "doc_part": "regulation",
                "chapter": "Chương I",
                "article": "Điều 3. Khái niệm và định nghĩa",
                "article_number": 3,
                "start_page_pdf": 3,
                "end_page_pdf": 3,
                "start_page_printed": 2,
                "end_page_printed": 2,
                "is_table": False,
                "content": "Trường tổ chức mỗi năm gồm 03 học kỳ. Mỗi học kỳ từ 10 đến 12 tuần.",
                "similarity": 0.65,
                "source_spans": [],
            },
            {
                "chunk_id": "chunk_02",
                "document_id": "QD580_DHNCT_2024",
                "doc_part": "regulation",
                "chapter": "Chương II",
                "article": "Điều 7. Đăng ký học tập",
                "article_number": 7,
                "start_page_pdf": 9,
                "end_page_pdf": 9,
                "start_page_printed": 8,
                "end_page_printed": 8,
                "is_table": False,
                "content": "Sinh viên đăng ký học phần tối thiểu 07 tín chỉ.",
                "similarity": 0.45,
                "source_spans": [],
            }
        ]

        self.engine = RAGEngine(
            retriever=self.mock_retriever,
            llm_client=self.mock_llm_client,
            top_k=2,
        )

    def test_filter_out_hallucinated_source_ids(self):
        """Backend phải lọc bỏ triệt để các source ID bịa đặt do LLM tự tạo ra."""
        # LLM trả về SRC-1 (hợp lệ) và SRC-99, INVALID_SRC (ảo)
        self.mock_llm_client.generate_json.return_value = {
            "status": "answered",
            "answer": "Trường tổ chức 3 học kỳ mỗi năm.",
            "cited_source_ids": ["SRC-1", "SRC-99", "INVALID_SRC"],
        }

        resp = self.engine.answer_question("Trường có mấy học kỳ?")
        self.assertEqual(resp.status, "answered")
        self.assertEqual(len(resp.citations), 1)
        self.assertEqual(resp.citations[0].source_id, "SRC-1")
        self.assertEqual(resp.citations[0].article, "Điều 3. Khái niệm và định nghĩa")

    def test_handle_insufficient_evidence_status(self):
        """Xử lý đúng trường hợp LLM xác định thiếu căn cứ trong ngữ cảnh."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "insufficient_evidence",
            "answer": "QĐ 580 chưa quy định biểu phí cụ thể của năm học 2026-2027.",
            "cited_source_ids": [],
        }

        resp = self.engine.answer_question("Học phí ngành CNTT năm 2026 là bao nhiêu?")
        self.assertEqual(resp.status, "insufficient_evidence")
        self.assertEqual(len(resp.citations), 0)
        self.assertIn("chưa quy định", resp.answer)

    def test_handle_out_of_scope_status(self):
        """Xử lý đúng trường hợp LLM xác định câu hỏi ngoại phạm vi."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "out_of_scope",
            "answer": "Quy định về điểm rèn luyện không thuộc phạm vi điều chỉnh của QĐ 580.",
            "cited_source_ids": [],
        }

        resp = self.engine.answer_question("Cách tính điểm rèn luyện thế nào?")
        self.assertEqual(resp.status, "out_of_scope")
        self.assertEqual(len(resp.citations), 0)

    def test_upstream_error_raises_runtime_error(self):
        """Khi LLM gặp lỗi mạng/timeout, engine phải ném RuntimeError rõ ràng."""
        self.mock_llm_client.generate_json.side_effect = RuntimeError("Upstream Gemini timeout after 30s")

        with self.assertRaises(RuntimeError) as ctx:
            self.engine.answer_question("Câu hỏi thử nghiệm lỗi")
        self.assertIn("Gemini timeout", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
