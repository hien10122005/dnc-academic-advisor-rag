# -*- coding: utf-8 -*-
"""
backend.errors
Định nghĩa hệ thống phân cấp ngoại lệ có kiểu và mã lỗi chuẩn mực cho DNC RAG.
Tránh hoàn toàn việc phân loại lỗi bằng tìm kiếm chuỗi trong thông báo ngoại lệ.
"""

from typing import Any, Dict, Optional


class DNCError(Exception):
    """Lớp ngoại lệ cơ sở cho toàn bộ hệ thống RAG DNC."""
    code: str = "INTERNAL_ERROR"
    status_code: int = 500
    message: str = "Đã xảy ra lỗi nội bộ trong hệ thống."

    def __init__(self, message: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message or self.__class__.message
        self.details = details or {}
        super().__init__(self.message)


class KnowledgeBaseNotReadyError(DNCError, RuntimeError):
    """Kho tri thức (ChromaDB / artifacts / status) chưa sẵn sàng hoặc tiền kiểm tra thất bại."""
    code: str = "KNOWLEDGE_BASE_NOT_READY"
    status_code: int = 503
    message: str = "Kho tri thức quy chế chưa sẵn sàng hoặc chưa hoàn tất kiểm tra tiền trạm."


class ConfigurationError(DNCError):
    """Cấu hình hệ thống (API key, model hoặc biến môi trường) chưa hoàn tất hoặc không hợp lệ."""
    code: str = "CONFIGURATION_ERROR"
    status_code: int = 503
    message: str = "Cấu hình hệ thống (API key, model hoặc biến môi trường) chưa hoàn tất."


class LLMUpstreamError(DNCError):
    """Lỗi giao tiếp hoặc dịch vụ Gemini API gặp sự cố phía máy chủ upstream."""
    code: str = "LLM_UPSTREAM_ERROR"
    status_code: int = 502
    message: str = "Dịch vụ mô hình ngôn ngữ lớn (Gemini API) gặp sự cố kết nối."


class LLMTimeoutError(DNCError):
    """Yêu cầu tới dịch vụ Gemini API đã vượt quá thời gian chờ (timeout)."""
    code: str = "LLM_TIMEOUT"
    status_code: int = 504
    message: str = "Yêu cầu tới dịch vụ Gemini API đã vượt quá thời gian chờ (timeout)."


class LLMQuotaExceededError(DNCError):
    """Hạn mức truy vấn Gemini API đã bị vượt quá (Rate limit / Quota exceeded)."""
    code: str = "LLM_QUOTA_EXCEEDED"
    status_code: int = 503
    message: str = "Hạn mức truy vấn Gemini API đã bị vượt quá hoặc bị giới hạn."


class RAGSchemaError(DNCError):
    """Phản hồi từ mô hình không tuân thủ cấu trúc dữ liệu JSON hoặc giá trị không hợp lệ."""
    code: str = "RAG_SCHEMA_ERROR"
    status_code: int = 502
    message: str = "Phản hồi từ mô hình ngôn ngữ không tuân thủ cấu trúc dữ liệu quy định."


class ValidationError(DNCError):
    """Dữ liệu đầu vào từ người dùng hoặc client không hợp lệ."""
    code: str = "VALIDATION_ERROR"
    status_code: int = 422
    message: str = "Dữ liệu đầu vào không hợp lệ hoặc vượt giới hạn cho phép."
