# -*- coding: utf-8 -*-
"""
backend.gemini_client
Lớp client kết nối Gemini API (Google GenAI SDK) hỗ trợ cả chế độ Live và Offline Stub/Mock.
- Sử dụng SDK chính thức mới nhất: `google-genai` (google.genai.Client).
- Cấu hình an toàn qua biến môi trường: GEMINI_API_KEY, GEMINI_MODEL.
- Thiết lập chặt chẽ: timeout thật tại tầng HTTP SDK (HttpOptions), tắt retry ngầm của SDK (attempts=1)
  để kiểm soát tập trung tại vòng retry bên ngoài, retry chọn lọc duy nhất cho lỗi tạm thời (transient).
- Phân định rạch ròi giữa test Mock và Live; bảo vệ thông tin bí mật.
"""

from __future__ import annotations
import json
import logging
import os
import time
from typing import Any, Callable, Dict, Optional, Tuple

import httpx

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


def classify_exception(exc: Exception) -> Tuple[bool, str, Optional[int]]:
    """
    Phân loại chính xác ngoại lệ có phải là lỗi tạm thời (transient) cần thử lại hay không.
    Trả về: (is_transient: bool, category: str, http_code: Optional[int])

    Quy tắc:
    - KHÔNG retry:
      1. Lỗi lập trình: ValueError, TypeError, KeyError, AttributeError, IndexError.
      2. Lỗi cấu trúc/schema: json.JSONDecodeError, RAGSchemaError, ConfigurationError.
      3. Lỗi máy khách (HTTP 4xx ngoại trừ 408 và 429): 400, 401, 403, 404...
    - CHỈ retry khi là lỗi tạm thời (transient):
      1. Timeout: httpx.TimeoutException, TimeoutError, mã 408, 504, DEADLINE_EXCEEDED.
      2. Hạn mức / Giới hạn tần suất: HTTP 429 (RESOURCE_EXHAUSTED).
      3. Lỗi máy chủ hoặc mạng tạm thời: HTTP 500, 502, 503, httpx.NetworkError, ConnectError.
    """
    # 1. Các lỗi lập trình hoặc schema: tuyệt đối không retry
    if isinstance(exc, (ValueError, TypeError, KeyError, AttributeError, IndexError, json.JSONDecodeError, RAGSchemaError, ConfigurationError)):
        return False, "programming", None

    # 2. Trích xuất mã HTTP trạng thái dạng số nguyên từ các thuộc tính cấu trúc
    code: Optional[int] = None
    if hasattr(exc, "status_code") and isinstance(exc.status_code, int):
        code = exc.status_code
    elif hasattr(exc, "code") and isinstance(exc.code, int):
        code = exc.code
    elif hasattr(exc, "response") and hasattr(exc.response, "status_code") and isinstance(exc.response.status_code, int):
        code = exc.response.status_code
    elif hasattr(exc, "http_status") and isinstance(exc.http_status, int):
        code = exc.http_status

    # 3. Khi đã có mã số HTTP có cấu trúc -> Phân loại HOÀN TOÀN dựa trên mã số, KHÔNG tìm số trong str(exc)
    if code is not None:
        if code in (400, 401, 403, 404):
            return False, "client_error", code
        if code == 429:
            return True, "quota", 429
        if code in (408, 504):
            return True, "timeout", code
        if 500 <= code <= 599:
            return True, "server", code
        if 400 <= code < 500:
            return False, "client_error", code
        if code >= 500:
            return True, "server", code

    # 4. Khi KHÔNG có mã số HTTP -> Phân loại dựa trên kiểu lớp ngoại lệ có cấu trúc
    if isinstance(exc, (httpx.TimeoutException, TimeoutError)):
        return True, "timeout", 504

    if isinstance(exc, (httpx.NetworkError, httpx.ConnectError, ConnectionResetError, BrokenPipeError)):
        return True, "server", 502

    exc_name = type(exc).__name__

    # Kiểm tra các lớp lỗi cụ thể từ Google GenAI SDK (ClientError, APIError, v.v.)
    if "Timeout" in exc_name or "DeadlineExceeded" in exc_name:
        return True, "timeout", 504
    if "ResourceExhausted" in exc_name or "QuotaExceeded" in exc_name:
        return True, "quota", 429
    if "ClientError" in exc_name or "BadRequest" in exc_name or "NotFound" in exc_name:
        return False, "client_error", 400
    if "ServerError" in exc_name or "ServiceUnavailable" in exc_name or "InternalServerError" in exc_name:
        return True, "server", 503

    # Các ngoại lệ không xác định khác: không retry để tránh vòng lặp vô hạn
    return False, "unknown", None


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

                # Gắn timeout và tắt retry nội bộ của SDK (attempts=1) để vòng retry bên ngoài
                # kiểm soát hoàn toàn số lần gọi và thời gian chờ
                http_options = types.HttpOptions(
                    timeout=int(self.timeout * 1000),
                    retry_options=types.HttpRetryOptions(attempts=1),
                )
                self._genai_client = genai.Client(api_key=self.api_key, http_options=http_options)
            except Exception as e:
                logger.warning("Không thể khởi tạo Google GenAI Client: %s", type(e).__name__)
                self._genai_client = None

    @property
    def is_live(self) -> bool:
        """Kiểm tra client có đang hoạt động với API Key thật hay không."""
        return self._genai_client is not None and bool(self.api_key)

    @property
    def is_using_live_api(self) -> bool:
        """Kiểm tra xem client có đang thực sự gọi Live API hay không (không bị tiêm mock handler)."""
        return self.is_live and self._mock_handler is None

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
        - Giới hạn thời gian mỗi lần thử: timeout giây.
        - Tổng số lần thử tối đa: max_retries + 1 (mặc định 3 lần thử).
        - Thời gian chờ xấu nhất (worst-case timeout): (max_retries + 1) * timeout + tổng backoffs.
        - Chỉ retry duy nhất các lỗi tạm thời (Timeout, 429, 5xx, NetworkError).
        - Tuyệt đối không retry lỗi lập trình (ValueError, TypeError), cấu trúc JSON hoặc 4xx cố định.
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

        timeout_ms = int(self.timeout * 1000)
        config = types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            system_instruction=system_instruction if system_instruction else None,
            http_options=types.HttpOptions(
                timeout=timeout_ms,
                retry_options=types.HttpRetryOptions(attempts=1),
            ),
        )

        last_exc: Optional[Exception] = None
        last_category: str = "unknown"

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
                    # Lỗi định dạng JSON từ mô hình là lỗi nội dung, không phải lỗi mạng -> Không retry
                    raise RAGSchemaError(f"Phản hồi từ LLM không đúng định dạng JSON: {jde}") from jde

                if not isinstance(parsed_json, dict):
                    raise RAGSchemaError("Phản hồi từ Gemini API không phải là một JSON object.")

                return parsed_json

            except RAGSchemaError:
                # Lỗi cấu trúc phản hồi: không retry
                raise

            except Exception as exc:
                last_exc = exc
                is_transient, category, code = classify_exception(exc)
                last_category = category

                # Nếu KHÔNG phải lỗi tạm thời: lập tức dừng và ném lỗi phù hợp
                if not is_transient:
                    if category == "programming":
                        logger.error("Lỗi lập trình phát sinh khi gọi LLM: %s", exc)
                        raise
                    if category == "client_error":
                        logger.error("Gemini API trả về lỗi cố định không thể thử lại (code=%s): %s", code, type(exc).__name__)
                        raise LLMUpstreamError(
                            message="Yêu cầu tới Gemini API bị từ chối với lỗi máy khách.",
                            internal_detail=str(exc),
                        ) from exc
                    logger.error("Lỗi không thể phục hồi khi gọi Gemini API (%s): %s", category, exc)
                    raise LLMUpstreamError(
                        message="Giao tiếp Gemini API thất bại với lỗi không xác định.",
                        internal_detail=str(exc),
                    ) from exc

                # Nếu là lỗi tạm thời nhưng đã hết số lần thử: thoát vòng lặp để raise
                if attempt >= self.max_retries:
                    logger.warning(
                        "Hết số lượt thử lại (%d/%d) với lỗi tạm thời [%s]: %s",
                        attempt + 1, self.max_retries + 1, category, exc
                    )
                    break

                # Tính toán thời gian backoff dựa trên loại lỗi
                if category == "quota":
                    backoff = 15.0 * (attempt + 1)
                    logger.warning("Đạt ngưỡng giới hạn tần suất (429), chờ %.1fs trước lần thử %d...", backoff, attempt + 2)
                elif category == "timeout":
                    backoff = 2.0 * (attempt + 1)
                    logger.warning("Gemini API timeout tại lần thử %d/%d, chờ %.1fs...", attempt + 1, self.max_retries + 1, backoff)
                else:
                    backoff = 1.0 * (attempt + 1)
                    logger.warning("Lỗi máy chủ/mạng tạm thời (thử lại %d/%d), chờ %.1fs...", attempt + 1, self.max_retries + 1, backoff)

                time.sleep(backoff)

        # Phân loại chính xác lỗi cuối cùng phát sinh trên lần thử cuối
        if last_category == "timeout":
            raise LLMTimeoutError(
                message="Yêu cầu tới dịch vụ Gemini API đã vượt quá thời gian chờ (timeout).",
                internal_detail=f"Gemini API timed out after {self.max_retries + 1} attempts (timeout={self.timeout}s): {last_exc}",
            ) from last_exc

        if last_category == "quota":
            raise LLMQuotaExceededError(
                message="Hạn mức truy vấn Gemini API đã bị vượt quá hoặc bị giới hạn tần suất.",
                internal_detail=f"Gemini API quota exceeded after {self.max_retries + 1} attempts: {last_exc}",
            ) from last_exc

        raise LLMUpstreamError(
            message="Dịch vụ mô hình ngôn ngữ lớn (Gemini API) gặp sự cố kết nối.",
            internal_detail=f"Gemini API communication failed after {self.max_retries + 1} attempts ({type(last_exc).__name__}): {last_exc}",
        ) from last_exc

    def smoke_test(self) -> Dict[str, Any]:
        """
        Kiểm tra nhanh kết nối tới Gemini API (không để lộ bí mật/API key).
        Bắt buộc phản hồi phải là JSON hợp lệ chứa đúng {'ping': 'pong'}.
        """
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
                        http_options=types.HttpOptions(
                            timeout=timeout_ms,
                            retry_options=types.HttpRetryOptions(attempts=1),
                        ),
                    ),
                )
                elapsed = time.time() - start_time
                parsed_text = response.text.strip() if response.text else "{}"

                try:
                    parsed_json = json.loads(parsed_text)
                except Exception:
                    parsed_json = {}

                # Kiểm tra chặt chẽ: phải là dict và chứa đúng ping=pong
                if not isinstance(parsed_json, dict) or parsed_json.get("ping") != "pong":
                    return {
                        "live": False,
                        "status": "CONNECTION_FAILED",
                        "model": self.model,
                        "latency_ms": round(elapsed * 1000, 2),
                        "error": "Phản hồi smoke test không đúng định dạng xác thực {'ping': 'pong'}.",
                    }

                return {
                    "live": True,
                    "status": "CONNECTED",
                    "model": self.model,
                    "latency_ms": round(elapsed * 1000, 2),
                    "response": parsed_json,
                }

            except Exception as exc:
                is_transient, category, _ = classify_exception(exc)
                if is_transient and attempt < self.max_retries:
                    backoff = 15.0 if category == "quota" else 2.0
                    logger.warning("Smoke test gặp lỗi tạm thời [%s], chờ %.1fs...", category, backoff)
                    time.sleep(backoff)
                    continue

                elapsed = time.time() - start_time
                return {
                    "live": False,
                    "status": "CONNECTION_FAILED",
                    "model": self.model,
                    "latency_ms": round(elapsed * 1000, 2),
                    "error": type(exc).__name__,
                }

        elapsed = time.time() - start_time
        return {
            "live": False,
            "status": "CONNECTION_FAILED",
            "model": self.model,
            "latency_ms": round(elapsed * 1000, 2),
            "error": "Exhausted smoke test retries",
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
