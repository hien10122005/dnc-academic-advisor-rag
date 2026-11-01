# -*- coding: utf-8 -*-
"""
backend.gemini_client
Lớp client kết nối Gemini API (Google GenAI SDK) hỗ trợ cả chế độ Live và Offline Stub/Mock.
- Sử dụng SDK chính thức mới nhất: `google-genai` (google.genai.Client).
- Cấu hình an toàn qua biến môi trường: GEMINI_API_KEY, GEMINI_MODEL.
- Thiết lập chặt chẽ: timeout thật tại tầng HTTP SDK (HttpOptions), retry chọn lọc cho lỗi tạm thời,
  bảo vệ bí mật và phân định rạch ròi giữa test Mock và Live.
"""

from __future__ import annotations
import json
import logging
import os
import time
from typing import Any, Callable, Dict, Optional

from backend.config import (
    ALLOW_OFFLINE_MOCK,
    DEFAULT_GEMINI_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_RETRY_ATTEMPTS,
    REQUEST_TIMEOUT_SECONDS,
)
from backend.errors import (
    ConfigurationError,
    LLMQuotaExceededError,
    LLMTimeoutError,
    LLMUpstreamError,
    RAGSchemaError,
)

logger = logging.getLogger("dnc_rag.gemini_client")


class GeminiClient:
    """Client kết nối Gemini API với cơ chế quản lý vòng đời và dự phòng kiểm thử rõ ràng."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        allow_offline_mock: Optional[bool] = None,
    ):
        raw_key = api_key if api_key is not None else GEMINI_API_KEY
        self.api_key = raw_key.strip() if raw_key else None
        self.model = (model or GEMINI_MODEL or DEFAULT_GEMINI_MODEL).strip()
        self.timeout = float(timeout if timeout is not None else REQUEST_TIMEOUT_SECONDS)
        self.max_retries = int(max_retries if max_retries is not None else MAX_RETRY_ATTEMPTS)
        self.allow_offline_mock = (
            allow_offline_mock if allow_offline_mock is not None else ALLOW_OFFLINE_MOCK
        )

        self._mock_handler: Optional[Callable[[str, Optional[str]], Dict[str, Any]]] = None
        self._genai_client = None

        if self.api_key:
            try:
                from google import genai
                from google.genai import types

                # Gắn timeout trực tiếp vào cấu hình HTTP transport của SDK Client (miligiây)
                http_options = types.HttpOptions(timeout=int(self.timeout * 1000))
                self._genai_client = genai.Client(api_key=self.api_key, http_options=http_options)
            except Exception as e:
                logger.warning("Không thể khởi tạo Google GenAI Client: %s", type(e).__name__)
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
        max_output_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """
        Gửi yêu cầu sinh nội dung có cấu trúc JSON tới Gemini API.
        Hỗ trợ retry hữu hạn cho lỗi mạng tạm thời và chặn đứng lỗi cố định (4xx, schema error).
        """
        # 1. Nếu có mock_handler được tiêm vào rõ ràng -> Ưu tiên thực thi handler kiểm thử
        if self._mock_handler is not None:
            return self._mock_handler(prompt, system_instruction)

        # 2. Nếu không có kết nối Live (thiếu key hoặc SDK không nạp được)
        if not self.is_live:
            if self.allow_offline_mock:
                return self._default_offline_mock(prompt)
            raise ConfigurationError(
                "Dịch vụ LLM chưa sẵn sàng: GEMINI_API_KEY chưa được thiết lập và chế độ offline mock bị vô hiệu hóa."
            )

        # 3. Chế độ Live: Gọi Google GenAI SDK thật
        from google.genai import types
        import httpx

        timeout_ms = int(self.timeout * 1000)
        config = types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            system_instruction=system_instruction if system_instruction else None,
            http_options=types.HttpOptions(timeout=timeout_ms),
        )

        last_exc: Optional[Exception] = None
        is_timeout_err = False

        for attempt in range(self.max_retries + 1):
            try:
                response = self._genai_client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=config,
                )
                text_response = response.text
                if not text_response or not text_response.strip():
                    raise RAGSchemaError("Gemini API trả về chuỗi phản hồi rỗng.")

                try:
                    parsed_json = json.loads(text_response.strip())
                except json.JSONDecodeError as jde:
                    # Lỗi định dạng JSON từ mô hình không phải lỗi mạng tạm thời -> Không retry vô ích
                    raise RAGSchemaError(f"Phản hồi từ LLM không đúng định dạng JSON: {jde}") from jde

                if not isinstance(parsed_json, dict):
                    raise RAGSchemaError("Phản hồi từ Gemini API không phải là một JSON object.")

                return parsed_json

            except RAGSchemaError:
                # Lỗi schema cấu trúc không retry
                raise

            except Exception as exc:
                last_exc = exc
                err_str = str(exc)
                exc_type_name = type(exc).__name__

                # Kiểm tra lỗi timeout
                if (
                    isinstance(exc, (httpx.TimeoutException, TimeoutError))
                    or "DEADLINE_EXCEEDED" in err_str
                    or "timed out" in err_str.lower()
                    or "APITimeoutError" in exc_type_name
                ):
                    is_timeout_err = True
                    logger.warning("Gemini API timeout tại lần thử %d/%d", attempt + 1, self.max_retries + 1)

                # Kiểm tra lỗi Quota / Rate limit (429)
                elif "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                    logger.warning("Gemini API đạt ngưỡng giới hạn tần suất (429) tại lần thử %d/%d", attempt + 1, self.max_retries + 1)
                    if attempt >= self.max_retries:
                        raise LLMQuotaExceededError("Hạn mức truy vấn Gemini API đã bị vượt quá (Rate limit / Quota exceeded).") from exc
                    # Với 429, chờ lâu hơn (15s, 30s) để qua cửa sổ giới hạn tần suất của Google AI Studio
                    backoff_429 = 15.0 * (attempt + 1)
                    logger.info("Tạm dừng %.1fs trước khi thử lại sau lỗi 429...", backoff_429)
                    time.sleep(backoff_429)
                    continue

                # Kiểm tra lỗi Client không thể retry (400, 401, 403, 404)
                elif any(code in err_str for code in ("400", "401", "403", "404", "NOT_FOUND", "INVALID_ARGUMENT", "UNAUTHENTICATED", "PERMISSION_DENIED")):
                    logger.error("Gemini API trả về lỗi cố định không thể thử lại: %s", exc_type_name)
                    raise LLMUpstreamError(f"Yêu cầu tới Gemini API bị từ chối với lỗi máy khách ({exc_type_name}).") from exc

                else:
                    logger.warning("Lỗi tạm thời khi gọi Gemini API (thử lại %d/%d): %s", attempt + 1, self.max_retries + 1, exc_type_name)

                # Nếu chưa hết số lần thử, chờ với backoff luỹ tiến
                if attempt < self.max_retries:
                    time.sleep(1.0 * (attempt + 1))

        # Nếu đã thử hết các lượt retry
        if is_timeout_err:
            raise LLMTimeoutError(
                f"Yêu cầu tới Gemini API vượt quá thời gian chờ ({self.timeout}s) sau {self.max_retries + 1} lần thử."
            ) from last_exc

        raise LLMUpstreamError(
            f"Giao tiếp Gemini API thất bại sau {self.max_retries + 1} lần thử ({type(last_exc).__name__})."
        ) from last_exc

    def smoke_test(self) -> Dict[str, Any]:
        """Kiểm tra nhanh kết nối tới Gemini API (không để lộ bí mật/API key)."""
        if not self.is_live:
            return {
                "live": False,
                "status": "OFFLINE_NO_API_KEY",
                "model": self.model,
                "message": "GEMINI_API_KEY chưa được thiết lập. Chế độ live chưa khả dụng.",
            }

        start_time = time.time()
        for attempt in range(self.max_retries + 1):
            try:
                from google.genai import types

                timeout_ms = int(self.timeout * 1000)
                response = self._genai_client.models.generate_content(
                    model=self.model,
                    contents="Hãy trả về đúng JSON: {\"ping\": \"pong\"}",
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        max_output_tokens=30,
                        temperature=0.0,
                        http_options=types.HttpOptions(timeout=timeout_ms),
                    )
                )
                elapsed = time.time() - start_time
                parsed_text = response.text.strip() if response.text else "{}"
                parsed_json = json.loads(parsed_text)
                return {
                    "live": True,
                    "status": "CONNECTED",
                    "model": self.model,
                    "latency_ms": round(elapsed * 1000, 2),
                    "response": parsed_json,
                }
            except Exception as exc:
                err_str = str(exc)
                if ("429" in err_str or "RESOURCE_EXHAUSTED" in err_str) and attempt < self.max_retries:
                    logger.warning("Smoke test gặp giới hạn tần suất (429), chờ 15s...")
                    time.sleep(15.0)
                    continue
                elapsed = time.time() - start_time
                return {
                    "live": False,
                    "status": "CONNECTION_FAILED",
                    "model": self.model,
                    "latency_ms": round(elapsed * 1000, 2),
                    "error": type(exc).__name__,
                }

    def _default_offline_mock(self, prompt: str) -> Dict[str, Any]:
        """Phương thức Mock ngoại tuyến mặc định phục vụ kiểm thử."""
        if "CÂU HỎI CỦA SINH VIÊN:" in prompt:
            question_part = prompt.split("CÂU HỎI CỦA SINH VIÊN:")[-1].split("Hãy trả lời bằng")[0].strip()
        else:
            question_part = prompt[:50]

        has_sources = "[SRC-1]" in prompt

        if not has_sources:
            return {
                "status": "insufficient_evidence",
                "answer": "Quy chế đào tạo hiện tại chưa cung cấp đủ căn cứ để trả lời câu hỏi này.",
                "cited_source_ids": [],
            }

        return {
            "status": "answered",
            "answer": f"[MOCK] Dựa trên quy chế đào tạo QĐ 580/QĐ-ĐHNCT, nội dung câu hỏi '{question_part}' đã được quy định chi tiết.",
            "cited_source_ids": ["SRC-1"],
        }
