# -*- coding: utf-8 -*-
"""
backend.gemini_client
Lớp client kết nối Gemini API (Google GenAI SDK) hỗ trợ cả chế độ Live và Offline Stub/Mock.
- Sử dụng SDK chính thức mới nhất: `google-genai` (google.genai.Client).
- Cấu hình qua biến môi trường: GEMINI_API_KEY, GEMINI_MODEL.
- Thiết lập chặt chẽ: timeout, max_retries, max_output_tokens, response_mime_type="application/json".
- Phân định rạch ròi giữa kiểm thử Mock (Offline) và kết nối Gemini thật (Live).
"""

from __future__ import annotations
import json
import logging
import os
import time
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger("dnc_rag.gemini_client")

# Mô hình mặc định hiện đại theo khuyến nghị Gemini API
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


class GeminiClient:
    """Client kết nối Gemini API với cơ chế dự phòng Offline Mock rõ ràng."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip() or None
        self.model = model or os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip()
        self.timeout = float(timeout)
        self.max_retries = int(max_retries)

        self._mock_handler: Optional[Callable[[str, Optional[str]], Dict[str, Any]]] = None
        self._genai_client = None

        if self.api_key:
            try:
                from google import genai
                self._genai_client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Không thể khởi tạo Google GenAI Client: {e}. Chuyển sang chế độ offline.")
                self._genai_client = None

    @property
    def is_live(self) -> bool:
        """Kiểm tra client có đang hoạt động với API Key thật hay không."""
        return self._genai_client is not None and bool(self.api_key)

    def set_mock_handler(self, handler: Optional[Callable[[str, Optional[str]], Dict[str, Any]]]):
        """Cung cấp handler giả lập phản hồi cho mục đích kiểm thử tự động."""
        self._mock_handler = handler

    def generate_json(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        max_output_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """
        Gửi yêu cầu sinh nội dung có cấu trúc JSON tới Gemini API.
        Hỗ trợ retry hữu hạn cho lỗi mạng tạm thời.
        """
        # 1. Nếu có mock_handler hoặc không có API key -> Chạy chế độ Offline Mock
        if self._mock_handler is not None:
            return self._mock_handler(prompt, system_instruction)

        if not self.is_live:
            # Chế độ Offline Mock mặc định: Trích xuất thông tin cơ bản từ prompt để phản hồi
            return self._default_offline_mock(prompt)

        # 2. Chế độ Live: Gọi Google GenAI SDK thật
        from google.genai import types

        config = types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            system_instruction=system_instruction if system_instruction else None,
        )

        last_exc = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self._genai_client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=config,
                )
                text_response = response.text
                if not text_response or not text_response.strip():
                    raise ValueError("Gemini API trả về chuỗi phản hồi rỗng.")

                parsed_json = json.loads(text_response.strip())
                if not isinstance(parsed_json, dict):
                    raise ValueError(f"Gemini API không trả về JSON object: {text_response[:100]}")
                return parsed_json

            except Exception as exc:
                last_exc = exc
                logger.warning(f"Lỗi gọi Gemini API (thử lại lần {attempt + 1}/{self.max_retries + 1}): {exc}")
                if attempt < self.max_retries:
                    time.sleep(1.0 * (attempt + 1))

        raise RuntimeError(f"Giao tiếp Gemini API thất bại sau {self.max_retries + 1} lần thử: {last_exc}")

    def smoke_test(self) -> Dict[str, Any]:
        """Kiểm tra nhanh kết nối tới Gemini API (không để lộ bí mật/API key)."""
        if not self.is_live:
            return {
                "live": False,
                "status": "OFFLINE_NO_API_KEY",
                "model": self.model,
                "message": "GEMINI_API_KEY chưa được thiết lập. Hệ thống đang chạy chế độ offline mock an toàn.",
            }

        start_time = time.time()
        try:
            from google.genai import types
            response = self._genai_client.models.generate_content(
                model=self.model,
                contents="Hãy trả về đúng JSON: {\"ping\": \"pong\"}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    max_output_tokens=30,
                    temperature=0.0,
                )
            )
            elapsed = time.time() - start_time
            return {
                "live": True,
                "status": "CONNECTED",
                "model": self.model,
                "latency_ms": round(elapsed * 1000, 2),
                "response": json.loads(response.text.strip()),
            }
        except Exception as exc:
            elapsed = time.time() - start_time
            return {
                "live": False,
                "status": "CONNECTION_FAILED",
                "model": self.model,
                "latency_ms": round(elapsed * 1000, 2),
                "error": str(exc),
            }

    def _default_offline_mock(self, prompt: str) -> Dict[str, Any]:
        """Xử lý giả lập ngoại tuyến chuẩn mực dựa trên ngữ cảnh đã trích xuất trong prompt."""
        # Kiểm tra xem trong prompt có nguồn nào được cấp không
        if "[SRC-" in prompt:
            # Giả lập trả lời có căn cứ với trích dẫn đầu tiên
            return {
                "status": "answered",
                "answer": "Theo Quyết định số 580/QĐ-ĐHNCT, nội dung quy chế đã được quy định chi tiết trong tài liệu.",
                "cited_source_ids": ["SRC-1"],
            }
        else:
            return {
                "status": "insufficient_evidence",
                "answer": "Không tìm thấy đủ thông tin quy chế trong kho tài liệu để giải đáp câu hỏi này.",
                "cited_source_ids": [],
            }
