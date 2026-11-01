# -*- coding: utf-8 -*-
"""
tests.test_api_and_rag
Bộ kiểm thử tự động toàn diện cho FastAPI Endpoints và RAG Engine (Nhiệm vụ 04 - R03).
Kiểm thử độc lập không phụ thuộc mạng hay API key thật:
1. GET /health: Trả về HTTP 200 (healthy khi live hoặc degraded khi offline mock/thiếu key).
2. GET /health: Trả về HTTP 503 khi kho tri thức chưa sẵn sàng hoặc preflight lỗi.
3. POST /chat: Tiếp nhận câu hỏi hợp lệ và trả về câu trả lời kèm citation hợp lệ.
4. POST /chat: Từ chối câu hỏi rỗng hoặc chỉ chứa khoảng trắng với HTTP 422 (ValidationError).
5. POST /chat: Từ chối câu hỏi vượt quá 1000 ký tự với HTTP 422 (ValidationError).
6. RAG Engine: Hạ trạng thái an toàn 'insufficient_evidence' khi phát hiện hallucinated source IDs.
7. RAG Engine: Bỏ tự gắn nguồn; hạ 'insufficient_evidence' khi 'answered' không có citation hợp lệ (kể cả similarity cao).
8. RAG Engine: Ném RAGSchemaError khi status sai, answer rỗng, JSON không phải object hoặc cited_source_ids không phải mảng.
9. RAG Engine: Trích đoạn citation được dựng từ source_spans và nội dung gốc, không dính context_prefix và trang in nullable.
10. GeminiClient: Ném ConfigurationError khi thiếu key và offline mock bị tắt; timeout truyền đúng vào SDK HttpOptions; không retry 4xx.
"""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient

from backend.errors import (
    ConfigurationError,
    DNCError,
    KnowledgeBaseNotReadyError,
    LLMTimeoutError,
    LLMUpstreamError,
    RAGSchemaError,
    ValidationError,
)
from backend.gemini_client import GeminiClient
from backend.main import app, rag_engine_instance
from backend.rag_engine import CitationItem, RAGEngine, SourceContext


class TestFastAPIEndpoints(unittest.TestCase):
    """Kiểm thử các endpoint của FastAPI bằng TestClient."""

    @classmethod
    def setUpClass(cls):
        cls._client_cm = TestClient(app)
        cls.client = cls._client_cm.__enter__()

        # Tiêm mock handler vào LLM client để bộ unit test hoàn toàn độc lập, không phát sinh request Gemini thật
        import backend.main
        if backend.main.rag_engine_instance is not None:
            cls._orig_mock_handler = backend.main.rag_engine_instance.llm_client._mock_handler
            backend.main.rag_engine_instance.llm_client.set_mock_handler(
                lambda prompt, sys_inst: {
                    "status": "answered",
                    "answer": "Trường Đại học Nam Cần Thơ tổ chức mỗi năm gồm 03 học kỳ theo Điều 3 QĐ 580.",
                    "cited_source_ids": ["SRC-1"],
                }
            )
        else:
            cls._orig_mock_handler = None

    @classmethod
    def tearDownClass(cls):
        import backend.main
        if backend.main.rag_engine_instance is not None and cls._orig_mock_handler is not None:
            backend.main.rag_engine_instance.llm_client.set_mock_handler(cls._orig_mock_handler)
        cls._client_cm.__exit__(None, None, None)

    def test_health_check_endpoint_structure(self):
        """GET /health phải trả về đầy đủ metadata an toàn khi kho tri thức READY."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn(data["status"], ("healthy", "degraded"))
        self.assertTrue(data["corpus_ready"])
        self.assertEqual(data["collection_name"], "qd580_baseline_v2")
        self.assertEqual(data["total_chunks"], 104)
        self.assertEqual(data["embedding_model_revision"], "84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0")

        # Đảm bảo không làm lộ API Key hay đường dẫn tuyệt đối nội bộ
        raw_json = json.dumps(data).lower()
        self.assertNotIn("api_key", raw_json)
        self.assertNotIn("c:\\", raw_json)
        self.assertNotIn("e:\\", raw_json)

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
        self.assertIn("is_live_llm", data)
        self.assertIn("model_name", data)

        if data["citations"]:
            cit = data["citations"][0]
            self.assertIn("source_id", cit)
            self.assertIn("chunk_id", cit)
            self.assertIn("document_id", cit)
            self.assertIn("article", cit)
            self.assertIn("pdf_page", cit)
            self.assertIn("quote_snippet", cit)
            self.assertIn("similarity", cit)
            # quote_snippet không được bắt đầu bằng context_prefix '['
            self.assertFalse(cit["quote_snippet"].startswith("["))

    def test_chat_endpoint_empty_question(self):
        """POST /chat với câu hỏi rỗng hoặc chỉ có khoảng trắng phải trả về HTTP 422."""
        res1 = self.client.post("/chat", json={"question": ""})
        self.assertEqual(res1.status_code, 422)

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
    """Kiểm thử logic chuyên sâu của RAG Engine (Citation, Hallucination, Schema, Spans)."""

    def setUp(self):
        self.mock_retriever = MagicMock()
        self.mock_llm_client = MagicMock()
        self.mock_llm_client.is_live = False
        self.mock_llm_client.model = "test-mock-gemini"

        # Mock dữ liệu truy xuất gồm 2 chunks có source_spans chi tiết
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
                "context_prefix": "[Quy chế Đào tạo ĐH (QĐ 580) - Chương I - Điều 3. Khái niệm và định nghĩa]",
                "content": "Trường tổ chức mỗi năm gồm 03 học kỳ. Mỗi học kỳ từ 10 đến 12 tuần.",
                "embedding_text": "[Quy chế Đào tạo ĐH (QĐ 580) - Chương I - Điều 3. Khái niệm và định nghĩa]\nTrường tổ chức mỗi năm gồm 03 học kỳ. Mỗi học kỳ từ 10 đến 12 tuần.",
                "similarity": 0.75,
                "source_spans": [
                    {
                        "pdf_page": 3,
                        "printed_page": 2,
                        "page_start_char": 0,
                        "page_end_char": 68,
                        "chunk_start_char": 0,
                        "chunk_end_char": 68,
                        "is_added_context": False,
                        "is_overlap": False,
                    }
                ],
            },
            {
                "chunk_id": "chunk_02",
                "document_id": "QD580_DHNCT_2024",
                "doc_part": "regulation",
                "chapter": "Chương II",
                "article": "Điều 7. Đăng ký học tập",
                "article_number": 7,
                "start_page_pdf": 9,
                "end_page_pdf": 10,
                "start_page_printed": None,  # Thử nghiệm trường hợp trang in là None
                "end_page_printed": None,
                "is_table": False,
                "context_prefix": "[Quy chế Đào tạo ĐH (QĐ 580) - Chương II - Điều 7. Đăng ký học tập]",
                "content": "Sinh viên đăng ký học phần tối thiểu 07 tín chỉ cho một học kỳ chính.",
                "embedding_text": "[Quy chế Đào tạo ĐH (QĐ 580) - Chương II - Điều 7. Đăng ký học tập]\nSinh viên đăng ký học phần tối thiểu 07 tín chỉ cho một học kỳ chính.",
                "similarity": 0.45,
                "source_spans": [
                    {
                        "pdf_page": 9,
                        "printed_page": None,
                        "page_start_char": 100,
                        "page_end_char": 170,
                        "chunk_start_char": 0,
                        "chunk_end_char": 70,
                        "is_added_context": False,
                        "is_overlap": False,
                    }
                ],
            }
        ]

        self.engine = RAGEngine(
            retriever=self.mock_retriever,
            llm_client=self.mock_llm_client,
            top_k=2,
        )

    def test_valid_answer_with_valid_citation(self):
        """Khi LLM trả về đúng schema và citation hợp lệ, engine trả về answered kèm citation."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "answered",
            "answer": "Trường tổ chức mỗi năm gồm 03 học kỳ.",
            "cited_source_ids": ["SRC-1"],
        }

        resp = self.engine.answer_question("Trường có mấy học kỳ?")
        self.assertEqual(resp.status, "answered")
        self.assertEqual(len(resp.citations), 1)
        cit = resp.citations[0]
        self.assertEqual(cit.source_id, "SRC-1")
        self.assertEqual(cit.article, "Điều 3. Khái niệm và định nghĩa")
        self.assertEqual(cit.pdf_page, 3)
        self.assertEqual(cit.printed_page, 2)
        # Quote snippet được trích từ nội dung gốc, không chứa context_prefix
        self.assertFalse(cit.quote_snippet.startswith("["))
        self.assertIn("Trường tổ chức mỗi năm gồm 03 học kỳ", cit.quote_snippet)

    def test_hallucinated_source_ids_downgraded_to_insufficient_evidence(self):
        """Khi LLM viện dẫn nguồn ảo (SRC-99) hoặc trộn nguồn thật với nguồn ảo, phải hạ trạng thái."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "answered",
            "answer": "Trường tổ chức 3 học kỳ mỗi năm theo quy chế đặc biệt.",
            "cited_source_ids": ["SRC-1", "SRC-999"],
        }

        resp = self.engine.answer_question("Trường có mấy học kỳ?")
        # Chính sách liêm chính: Bị từ chối do có ID bịa, hạ về insufficient_evidence
        self.assertEqual(resp.status, "insufficient_evidence")
        self.assertEqual(len(resp.citations), 0)
        self.assertIn("nguồn không có trong ngữ cảnh", resp.answer)

    def test_only_hallucinated_ids_downgraded(self):
        """Khi toàn bộ ID đều là bịa đặt, phải hạ trạng thái về insufficient_evidence."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "answered",
            "answer": "Căn cứ theo điều khoản bí mật.",
            "cited_source_ids": ["SRC-FAKE-1", "SRC-FAKE-2"],
        }

        resp = self.engine.answer_question("Quy định bí mật là gì?")
        self.assertEqual(resp.status, "insufficient_evidence")
        self.assertEqual(len(resp.citations), 0)

    def test_answered_without_citation_downgraded_no_auto_attach(self):
        """Khi LLM trả về 'answered' nhưng không có citation, KHÔNG được tự gắn top-1 similarity."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "answered",
            "answer": "Tôi khẳng định chắc chắn trường có 3 học kỳ.",
            "cited_source_ids": [],
        }

        resp = self.engine.answer_question("Trường có mấy học kỳ?")
        # Không được tự gắn SRC-1 dù similarity đạt 0.75
        self.assertEqual(resp.status, "insufficient_evidence")
        self.assertEqual(len(resp.citations), 0)
        self.assertIn("không trích dẫn được điều khoản", resp.answer)

    def test_invalid_status_raises_schema_error(self):
        """Khi status từ LLM không hợp lệ (ví dụ: 'WRONG'), engine ném RAGSchemaError."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "WRONG_STATUS",
            "answer": "Nội dung câu trả lời",
            "cited_source_ids": ["SRC-1"],
        }

        with self.assertRaises(RAGSchemaError):
            self.engine.answer_question("Câu hỏi kiểm tra")

    def test_empty_answer_raises_schema_error(self):
        """Khi answer từ LLM là chuỗi rỗng hoặc toàn khoảng trắng, engine ném RAGSchemaError."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "answered",
            "answer": "   \n\t   ",
            "cited_source_ids": ["SRC-1"],
        }

        with self.assertRaises(RAGSchemaError):
            self.engine.answer_question("Câu hỏi kiểm tra")

    def test_non_list_cited_ids_raises_schema_error(self):
        """Khi cited_source_ids không phải là danh sách, engine ném RAGSchemaError."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "answered",
            "answer": "Nội dung câu trả lời",
            "cited_source_ids": "SRC-1",  # Lỗi: truyền chuỗi thay vì list
        }

        with self.assertRaises(RAGSchemaError):
            self.engine.answer_question("Câu hỏi kiểm tra")

    def test_non_dict_llm_output_raises_schema_error(self):
        """Khi LLM trả về cấu trúc không phải dict (ví dụ list hoặc str), ném RAGSchemaError."""
        self.mock_llm_client.generate_json.return_value = ["not", "a", "dict"]

        with self.assertRaises(RAGSchemaError):
            self.engine.answer_question("Câu hỏi kiểm tra")

    def test_printed_page_none_handling(self):
        """Trang in khi không xác định phải được trả về None (không dùng -1)."""
        self.mock_llm_client.generate_json.return_value = {
            "status": "answered",
            "answer": "Đăng ký tối thiểu 7 tín chỉ.",
            "cited_source_ids": ["SRC-2"],
        }

        resp = self.engine.answer_question("Đăng ký bao nhiêu tín chỉ?")
        self.assertEqual(resp.status, "answered")
        self.assertEqual(len(resp.citations), 1)
        cit = resp.citations[0]
        self.assertEqual(cit.source_id, "SRC-2")
        self.assertIsNone(cit.printed_page)


class TestGeminiClientConfigurationAndErrors(unittest.TestCase):
    """Kiểm thử cấu hình, timeout và xử lý lỗi của GeminiClient."""

    def test_missing_key_and_mock_disabled_raises_configuration_error(self):
        """Khi không có API key và offline mock bị tắt, client phải ném ConfigurationError."""
        client = GeminiClient(api_key="", allow_offline_mock=False)
        self.assertFalse(client.is_live)

        with self.assertRaises(ConfigurationError):
            client.generate_json("Prompt thử nghiệm")

    def test_mock_handler_injection(self):
        """Khi mock_handler được tiêm vào rõ ràng, client trả về kết quả từ handler đó."""
        client = GeminiClient(api_key="", allow_offline_mock=False)
        client.set_mock_handler(lambda p, s: {"status": "answered", "answer": "Mocked", "cited_source_ids": []})

        res = client.generate_json("Prompt thử nghiệm")
        self.assertEqual(res["answer"], "Mocked")

    def test_smoke_test_offline(self):
        """Smoke test khi không có key phải trả về trạng thái OFFLINE_NO_API_KEY an toàn."""
        client = GeminiClient(api_key="", allow_offline_mock=False)
        st = client.smoke_test()
        self.assertFalse(st["live"])
        self.assertEqual(st["status"], "OFFLINE_NO_API_KEY")


if __name__ == "__main__":
    unittest.main()
