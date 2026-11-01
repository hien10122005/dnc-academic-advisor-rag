# -*- coding: utf-8 -*-
"""
backend.main
Ứng dụng FastAPI phục vụ API Trợ lý học vụ DNC (QĐ 580/QĐ-ĐHNCT ngày 02/08/2024).
Cung cấp hai endpoint tiêu chuẩn:
- GET /health: Kiểm tra tình trạng sẵn sàng của dịch vụ, kho tri thức (ChromaDB) và LLM Client.
- POST /chat: Tiếp nhận câu hỏi học vụ, thực thi quy trình RAG nghiêm ngặt và trả về câu trả lời kèm trích dẫn có căn cứ.
"""

from __future__ import annotations
import logging
import uuid
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend.config import COLLECTION_NAME, EMBEDDING_MODEL_CANDIDATE, MODEL_REVISION
from backend.errors import (
    ConfigurationError,
    DNCError,
    KnowledgeBaseNotReadyError,
    LLMQuotaExceededError,
    LLMTimeoutError,
    LLMUpstreamError,
    RAGSchemaError,
    ValidationError,
)
from backend.gemini_client import GeminiClient
from backend.rag_engine import RAGEngine
from backend.retrieval import VectorRetriever

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("dnc_rag.api")

# Biến toàn cục quản lý tài nguyên (Lifespan singleton)
rag_engine_instance: Optional[RAGEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Quản lý vòng đời ứng dụng: Khởi tạo model và kiểm tra tiền trạm (Preflight) một lần khi startup."""
    global rag_engine_instance
    logger.info("=== BẮT ĐẦU KHỞI ĐỘNG HỆ THỐNG TRỢ LÝ HỌC VỤ DNC (FASTAPI) ===")

    try:
        retriever = VectorRetriever()
        logger.info("Thực thi kiểm tra tiền trạm kho tri thức (Preflight Readiness)...")
        readiness_info = retriever.check_readiness()
        logger.info("Kho tri thức SẴN SÀNG: %s (%d chunks).", readiness_info['collection_name'], readiness_info['total_chunks'])

        # Nạp trước mô hình embedding vào bộ nhớ RAM
        _ = retriever.model
        logger.info("Mô hình Embedding Bi-Encoder đã được nạp sẵn sàng vào bộ nhớ.")

        # Nạp trước chỉ mục BM25 vào bộ nhớ RAM
        retriever.preload_bm25()
        logger.info("Chỉ mục BM25 Sparse Search đã được nạp sẵn sàng vào bộ nhớ.")

        gemini_client = GeminiClient()
        logger.info("Khởi tạo Gemini Client (Chế độ Live: %s, Model: %s).", gemini_client.is_live, gemini_client.model)

        rag_engine_instance = RAGEngine(
            retriever=retriever,
            llm_client=gemini_client,
            top_k=5,
        )
        logger.info("RAG Engine đã sẵn sàng tiếp nhận yêu cầu.")
    except Exception as exc:
        logger.error("Khởi động thất bại do lỗi kho tri thức hoặc tài nguyên: %s", exc)
        rag_engine_instance = None

    yield

    logger.info("=== DỪNG HỆ THỐNG TRỢ LÝ HỌC VỤ DNC ===")


app = FastAPI(
    title="DNC Academic Advisor RAG API",
    description="Hệ thống Trợ lý Học vụ AI tra cứu Quy chế Đào tạo Đại học Nam Cần Thơ (QĐ 580/QĐ-ĐHNCT).",
    version="1.0.0",
    lifespan=lifespan,
)

# Cho phép CORS cho các client kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler tập trung cho các ngoại lệ chuẩn mực DNCError
@app.exception_handler(DNCError)
async def dnc_exception_handler(request: Request, exc: DNCError):
    req_id = str(uuid.uuid4())
    logger.warning(
        "DNCError [%s]: %s (Mã HTTP: %d)",
        exc.code,
        getattr(exc, "internal_detail", None) or exc.public_message,
        exc.status_code,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "request_id": req_id,
            "error_code": exc.code,
            "detail": exc.public_message,
        },
    )


# Exception handler bắt lỗi chưa được xử lý, che giấu tuyệt đối stack trace và đường dẫn
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    req_id = str(uuid.uuid4())
    logger.error("Unhandled Exception [req=%s]: %s", req_id, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "request_id": req_id,
            "error_code": "INTERNAL_SERVER_ERROR",
            "detail": "Đã xảy ra lỗi nội bộ trong quá trình xử lý yêu cầu.",
        },
    )


# ==============================================================================
# SCHEMAS (Pydantic Models)
# ==============================================================================

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Câu hỏi học vụ của sinh viên (Ví dụ: 'Điều kiện cảnh báo kết quả học tập là gì?')",
        examples=["Trường tổ chức mỗi năm gồm bao nhiêu học kỳ?"]
    )
    mode: Optional[str] = Field(
        "dense",
        description="Chế độ truy xuất: 'dense' (mặc định) hoặc 'hybrid' (kết hợp Dense Bi-encoder + BM25 qua RRF)"
    )


class CitationModel(BaseModel):
    source_id: str = Field(..., description="Mã định danh đoạn trích dẫn (ví dụ: SRC-1)")
    chunk_id: str = Field(..., description="Mã chunk định danh duy nhất")
    document_id: str = Field(..., description="Mã tài liệu quy chế (QD580_DHNCT_2024)")
    article: str = Field(..., description="Điều khoản quy chế được trích dẫn")
    pdf_page: int = Field(..., description="Số trang trong tệp PDF gốc")
    printed_page: Optional[int] = Field(None, description="Số trang in trên văn bản gốc (None nếu không xác định)")
    quote_snippet: str = Field(..., description="Trích đoạn ngắn nội dung căn cứ")
    similarity: Optional[float] = Field(None, description="Độ tương đồng ngữ nghĩa (Cosine Similarity), None nếu là sparse-only hit")


class ChatResponse(BaseModel):
    request_id: str = Field(..., description="Mã định danh duy nhất của lượt hỏi đáp")
    status: str = Field(
        ...,
        description="Trạng thái nghiệp vụ: 'answered', 'needs_clarification', 'insufficient_evidence', 'out_of_scope'"
    )
    answer: str = Field(..., description="Nội dung giải đáp chi tiết bằng tiếng Việt")
    citations: List[CitationModel] = Field(default_factory=list, description="Danh sách các trích dẫn căn cứ được backend xác thực")
    timings: Dict[str, float] = Field(default_factory=dict, description="Thời gian thực thi từng công đoạn (miligiây)")
    is_live_llm: bool = Field(..., description="True nếu trả lời từ kết nối Gemini Live; False nếu chế độ Offline Mock")
    model_name: str = Field(..., description="Tên mô hình ngôn ngữ lớn được sử dụng")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Trạng thái dịch vụ: 'healthy' hoặc 'degraded'")
    service: str = "dnc-academic-advisor-rag"
    version: str = "1.0.0"
    corpus_ready: bool = Field(..., description="Tính sẵn sàng của kho tri thức ChromaDB")
    collection_name: str
    corpus_fingerprint: str
    total_chunks: int
    embedding_model: str
    embedding_model_revision: str
    llm_live: bool
    llm_model: str


# ==============================================================================
# ENDPOINTS
# ==============================================================================

@app.get("/health", response_model=HealthResponse, tags=["System Health"])
def health_check():
    """
    Kiểm tra tính sẵn sàng của hệ thống.
    Nếu kho tri thức chưa sẵn sàng hoặc cấu hình bị sai lệch, trả về HTTP 503.
    Không thực hiện gọi mạng ra bên ngoài trong health check.
    """
    if rag_engine_instance is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Hệ thống chưa hoàn tất khởi tạo hoặc tiền kiểm tra (Preflight) thất bại."
        )

    try:
        readiness = rag_engine_instance.retriever.check_readiness()
        is_live = rag_engine_instance.llm_client.is_live
        svc_status = "healthy" if is_live else "degraded"

        return HealthResponse(
            status=svc_status,
            corpus_ready=True,
            collection_name=readiness["collection_name"],
            corpus_fingerprint=readiness["corpus_fingerprint"],
            total_chunks=readiness["total_chunks"],
            embedding_model=readiness["model_name"],
            embedding_model_revision=readiness["model_revision"],
            llm_live=is_live,
            llm_model=rag_engine_instance.llm_client.model,
        )
    except KnowledgeBaseNotReadyError as knr:
        logger.warning("Health check failed preflight: %s", getattr(knr, "internal_detail", None) or knr.public_message)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=knr.public_message,
        )
    except Exception as exc:
        logger.error("Health check unexpected error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Kho tri thức quy chế chưa sẵn sàng phục vụ.",
        )


@app.post("/chat", response_model=ChatResponse, tags=["RAG Chat"])
def chat_endpoint(request: ChatRequest):
    """
    Tiếp nhận câu hỏi độc lập từ sinh viên và trả lời dựa trên quy chế QĐ 580/QĐ-ĐHNCT.
    """
    # 1. Kiểm tra câu hỏi đầu vào
    clean_q = request.question.strip()
    if not clean_q:
        raise ValidationError("Câu hỏi không được để trống hoặc chỉ chứa khoảng trắng.")
    if len(clean_q) > 1000:
        raise ValidationError(f"Câu hỏi quá dài ({len(clean_q)} ký tự). Giới hạn tối đa là 1000 ký tự.")

    # 2. Kiểm tra chế độ truy xuất (mode)
    clean_mode = (request.mode or "dense").strip().lower()
    if clean_mode not in ("dense", "hybrid"):
        raise ValidationError(f"Chế độ truy xuất không hợp lệ: '{clean_mode}'. Chỉ chấp nhận 'dense' hoặc 'hybrid'.")

    # 3. Kiểm tra tính sẵn sàng của RAG Engine
    if rag_engine_instance is None:
        raise KnowledgeBaseNotReadyError("Dịch vụ RAG chưa sẵn sàng phục vụ. Vui lòng kiểm tra trạng thái tại /health.")

    # 4. Thực thi RAG Engine
    try:
        response = rag_engine_instance.answer_question(clean_q, mode=clean_mode)
        return ChatResponse(
            request_id=response.request_id,
            status=response.status,
            answer=response.answer,
            citations=[
                CitationModel(
                    source_id=c.source_id,
                    chunk_id=c.chunk_id,
                    document_id=c.document_id,
                    article=c.article,
                    pdf_page=c.pdf_page,
                    printed_page=c.printed_page,
                    quote_snippet=c.quote_snippet,
                    similarity=c.similarity,
                )
                for c in response.citations
            ],
            timings=response.timings,
            is_live_llm=response.is_live_llm,
            model_name=response.model_name,
        )
    except DNCError:
        # Được xử lý tự động bởi dnc_exception_handler
        raise
    except Exception as exc:
        logger.error("Lỗi không mong muốn khi xử lý câu hỏi: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra sự cố nội bộ trong quá trình xử lý câu hỏi học vụ."
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
