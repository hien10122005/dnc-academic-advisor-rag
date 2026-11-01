# -*- coding: utf-8 -*-
"""
backend.errors
Định nghĩa hệ thống phân cấp ngoại lệ có kiểu và mã lỗi chuẩn mực cho DNC RAG.
Tách bạch hoàn toàn thông báo công khai (public message) an toàn cho người dùng
khỏi chi tiết kỹ thuật nội bộ (internal_detail) dùng cho logging quản trị.
"""

from typing import Any, Dict, Optional


class DNCError(Exception):
    """
    Lớp ngoại lệ cơ sở cho toàn bộ hệ thống RAG DNC.
    - public_message: Chuỗi thông báo ổn định, an toàn, KHÔNG bao giờ chứa đường dẫn ổ đĩa,
      tên tệp nội bộ, chuỗi trace hoặc khóa API.
    - internal_detail: Chi tiết kỹ thuật phục vụ ghi log nội bộ máy chủ.
    """
    code: str = "INTERNAL_ERROR"
    status_code: int = 500
    default_message: str = "Đã xảy ra lỗi nội bộ trong hệ thống trợ lý học vụ."

    def __init__(
        self,
        message: Optional[str] = None,
        internal_detail: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        raw_msg = str(message) if message else self.default_message

        # Chốt chặn an toàn: Nếu thông báo chứa đường dẫn ổ đĩa hoặc tệp nội bộ,
        # tự động chuyển nội dung nhạy cảm vào internal_detail và giữ public_message sạch.
        has_internal_path = any(token in raw_msg for token in ("\\", "/", ".json", ".py", ".md", ":\\"))

        if internal_detail is not None:
            self.internal_detail = str(internal_detail)
            self.public_message = self.default_message if has_internal_path else raw_msg
        else:
            if has_internal_path:
                self.internal_detail = raw_msg
                self.public_message = self.default_message
            else:
                self.internal_detail = raw_msg
                self.public_message = raw_msg

        self.message = self.public_message
        self.details = details or {}
        super().__init__(self.internal_detail or self.public_message)


class KnowledgeBaseNotReadyError(DNCError, RuntimeError):
    """Kho tri thức (ChromaDB / artifacts / status) chưa sẵn sàng hoặc tiền kiểm tra thất bại."""
    code: str = "KNOWLEDGE_BASE_NOT_READY"
    status_code: int = 503
    default_message: str = "Kho tri thức quy chế chưa sẵn sàng hoặc chưa hoàn tất kiểm tra tiền trạm."


class ConfigurationError(DNCError):
    """Cấu hình hệ thống (API key, model hoặc biến môi trường) chưa hoàn tất hoặc không hợp lệ."""
    code: str = "CONFIGURATION_ERROR"
    status_code: int = 503
    default_message: str = "Cấu hình hệ thống (API key, model hoặc biến môi trường) chưa hoàn tất."


class LLMUpstreamError(DNCError):
    """Lỗi giao tiếp hoặc dịch vụ Gemini API gặp sự cố phía máy chủ upstream."""
    code: str = "LLM_UPSTREAM_ERROR"
    status_code: int = 502
    default_message: str = "Dịch vụ mô hình ngôn ngữ lớn (Gemini API) gặp sự cố kết nối."


class LLMTimeoutError(DNCError):
    """Yêu cầu tới dịch vụ Gemini API đã vượt quá thời gian chờ (timeout)."""
    code: str = "LLM_TIMEOUT"
    status_code: int = 504
    default_message: str = "Yêu cầu tới dịch vụ Gemini API đã vượt quá thời gian chờ (timeout)."


class LLMQuotaExceededError(DNCError):
    """
    Hạn mức truy vấn Gemini API đã bị vượt quá (Rate limit / Quota exceeded).
    Sử dụng mã HTTP 429 (Too Many Requests - RFC 6585) để đồng bộ chuẩn mực với các giao thức web
    và phản ánh đúng bản chất giới hạn tần suất/hạn mức ngày của nhà cung cấp LLM upstream.
    """
    code: str = "LLM_QUOTA_EXCEEDED"
    status_code: int = 429
    default_message: str = "Hạn mức truy vấn Gemini API đã bị vượt quá hoặc bị giới hạn tần suất."


class RAGSchemaError(DNCError):
    """Phản hồi từ mô hình không tuân thủ cấu trúc dữ liệu JSON hoặc giá trị không hợp lệ."""
    code: str = "RAG_SCHEMA_ERROR"
    status_code: int = 502
    default_message: str = "Phản hồi từ mô hình ngôn ngữ không tuân thủ cấu trúc dữ liệu quy định."


class ValidationError(DNCError):
    """Dữ liệu đầu vào từ người dùng hoặc client không hợp lệ."""
    code: str = "VALIDATION_ERROR"
    status_code: int = 422
    default_message: str = "Dữ liệu đầu vào không hợp lệ hoặc vượt giới hạn cho phép."
