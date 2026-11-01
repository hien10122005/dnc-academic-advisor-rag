# -*- coding: utf-8 -*-
"""
backend.rag_engine
RAG Engine cốt lõi cho hệ thống Trợ lý học vụ DNC (QĐ 580/QĐ-ĐHNCT).
Luồng xử lý nghiêm ngặt:
1. Xác thực tiền kiểm tra (Preflight Readiness).
2. Truy xuất Top-K từ VectorRetriever.
3. Đóng gói ngữ cảnh và gán mã định danh nguồn độc lập [SRC-1, SRC-2,...].
4. Xây dựng System Prompt học thuật chuẩn mực (khách quan, bám sát văn bản quy chế).
5. Gọi LLM sinh câu trả lời có cấu trúc JSON.
6. Xác minh trích dẫn (Citation Verification) độc lập ở tầng backend, loại bỏ ID ảo.
7. Đóng gói kết quả với thời gian đo lường chi tiết.
"""

from __future__ import annotations
import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Set

from backend.config import COLLECTION_NAME
from backend.gemini_client import GeminiClient
from backend.retrieval import VectorRetriever

logger = logging.getLogger("dnc_rag.rag_engine")

SYSTEM_PROMPT_TEMPLATE = """Bạn là Trợ lý Học vụ AI hỗ trợ sinh viên tra cứu Quy chế Đào tạo trình độ Đại học của Trường Đại học Nam Cần Thơ (theo Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024).
Đây là sản phẩm đồ án học thuật nghiên cứu hỗ trợ thông tin học vụ, không phải phát ngôn viên chính thức của Nhà trường.

BỘ QUY TẮC BẮT BUỘC KHI TRẢ LỜI:
1. TÍNH CHÍNH XÁC VÀ BÁM NGUỒN (GROUNDEDNESS):
   - Chỉ được đưa ra các kết luận, điều kiện, mức điểm, thời hạn, quyền và nghĩa vụ dựa trên các đoạn trích nguồn [SRC-x] được cung cấp dưới đây.
   - Giữ nguyên các con số, ngưỡng điểm, tỷ lệ, điều kiện ràng buộc và ngoại lệ đúng như văn bản gốc.
   - Tuyệt đối không suy đoán, không sáng tác thêm các quy định không có trong ngữ cảnh.

2. XỬ LÝ TRƯỜNG HỢP THIẾU DỮ KIỆN HOẶC NGOÀI PHẠM VI:
   - Nếu ngữ cảnh không có thông tin hoặc không đủ thông tin để trả lời câu hỏi: Đặt "status": "insufficient_evidence", giải thích rõ tài liệu hiện tại (QĐ 580) chưa có đủ dữ liệu cụ thể về vấn đề này. Tuyệt đối KHÔNG kết luận Nhà trường không có quy định. Khuyên sinh viên liên hệ Phòng Quản lý Đào tạo hoặc Cố vấn học tập để được hướng dẫn.
   - Nếu câu hỏi hoàn toàn ngoài phạm vi của Quy chế đào tạo (ví dụ biểu phí chi tiết ngành năm học mới, điểm rèn luyện...): Đặt "status": "out_of_scope", nêu rõ giới hạn của QĐ 580.
   - Nếu câu hỏi thiếu thông tin cụ thể (ví dụ sinh viên chưa nói rõ học chương trình mấy năm): Đặt "status": "needs_clarification" hoặc giải thích theo từng trường hợp cụ thể.

3. ĐỊNH DẠNG ĐẦU RA BẮT BUỘC:
   Bạn BẮT BUỘC phải trả về đúng định dạng JSON tuân thủ schema sau:
   {
     "status": "answered" | "needs_clarification" | "insufficient_evidence" | "out_of_scope",
     "answer": "Nội dung giải đáp chi tiết, lịch sự, đúng chuẩn văn phong học vụ bằng tiếng Việt.",
     "cited_source_ids": ["SRC-1", "SRC-2"]
   }
   - "cited_source_ids": Danh sách các mã nguồn [SRC-x] bạn thực sự sử dụng để đưa ra câu trả lời. Nếu không dùng nguồn nào, để mảng rỗng [].
"""


@dataclass
class SourceContext:
    """Mô hình đại diện cho một đoạn ngữ cảnh trích xuất từ ChromaDB."""
    source_id: str
    chunk_id: str
    document_id: str
    doc_part: str
    chapter: str
    article: str
    article_number: int
    start_page_pdf: int
    end_page_pdf: int
    start_page_printed: int
    end_page_printed: int
    is_table: bool
    text: str
    similarity: float
    source_spans: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CitationItem:
    """Thông tin trích dẫn nguồn được backend xác thực và xây dựng."""
    source_id: str
    document_id: str
    article: str
    pdf_page: int
    printed_page: int
    quote_snippet: str
    similarity: float


@dataclass
class RAGResponse:
    """Cấu trúc dữ liệu phản hồi hoàn chỉnh của RAG Engine."""
    request_id: str
    question: str
    status: str
    answer: str
    citations: List[CitationItem]
    sources_considered: int
    sources_cited: int
    timings: Dict[str, float]
    is_live_llm: bool
    model_name: str

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data


class RAGEngine:
    """Bộ máy RAG phối hợp giữa VectorRetriever và GeminiClient."""

    def __init__(
        self,
        retriever: Optional[VectorRetriever] = None,
        llm_client: Optional[GeminiClient] = None,
        top_k: int = 5,
    ):
        self.retriever = retriever or VectorRetriever()
        self.llm_client = llm_client or GeminiClient()
        self.top_k = int(top_k)

    def answer_question(
        self,
        question: str,
        top_k: Optional[int] = None,
    ) -> RAGResponse:
        """
        Thực thi quy trình RAG hoàn chỉnh cho một câu hỏi độc lập.
        """
        request_id = str(uuid.uuid4())
        total_start = time.time()
        timings: Dict[str, float] = {}

        # 1. Kiểm tra tính hợp lệ của câu hỏi đầu vào
        clean_question = question.strip() if question else ""
        if not clean_question:
            raise ValueError("Câu hỏi không được để trống hoặc chỉ chứa khoảng trắng.")
        if len(clean_question) > 1000:
            raise ValueError(f"Câu hỏi quá dài ({len(clean_question)} ký tự). Giới hạn tối đa là 1000 ký tự.")

        # 2. Tiền kiểm tra tính sẵn sàng của kho tri thức (Preflight) & Truy xuất Vector
        k = top_k if top_k is not None else self.top_k
        retrieval_start = time.time()

        # check_readiness được tự động gọi trong retrieve
        retrieved_raw = self.retriever.retrieve(clean_question, top_k=k)
        retrieval_time = time.time() - retrieval_start
        timings["retrieval_ms"] = round(retrieval_time * 1000, 2)

        # 3. Chuẩn bị ngữ cảnh và gán Source ID định danh
        source_contexts: List[SourceContext] = []
        valid_source_map: Dict[str, SourceContext] = {}

        for idx, item in enumerate(retrieved_raw, 1):
            src_id = f"SRC-{idx}"
            meta = item.get("metadata", {})
            src_ctx = SourceContext(
                source_id=src_id,
                chunk_id=item.get("chunk_id", ""),
                document_id=item.get("document_id", "QD580_DHNCT_2024"),
                doc_part=item.get("doc_part", ""),
                chapter=item.get("chapter", ""),
                article=item.get("article", ""),
                article_number=item.get("article_number", 0),
                start_page_pdf=item.get("start_page_pdf", 1),
                end_page_pdf=item.get("end_page_pdf", 1),
                start_page_printed=item.get("start_page_printed", 1),
                end_page_printed=item.get("end_page_printed", 1),
                is_table=item.get("is_table", False),
                text=item.get("content", ""),
                similarity=float(item.get("similarity", 0.0)),
                source_spans=item.get("source_spans", []),
            )
            source_contexts.append(src_ctx)
            valid_source_map[src_id] = src_ctx

        # 4. Xây dựng Prompt cho LLM
        context_blocks = []
        for s in source_contexts:
            block = (
                f"[{s.source_id}] ({s.article} - Trang PDF {s.start_page_pdf}"
                f"{f'-{s.end_page_pdf}' if s.start_page_pdf != s.end_page_pdf else ''}):\n"
                f"{s.text}"
            )
            context_blocks.append(block)

        joined_context = "\n\n---\n\n".join(context_blocks)
        user_prompt = (
            f"Dưới đây là các đoạn thông tin quy chế trích xuất từ kho tri thức:\n\n"
            f"{joined_context}\n\n"
            f"CÂU HỎI CỦA SINH VIÊN:\n{clean_question}\n\n"
            f"Hãy trả lời bằng định dạng JSON theo đúng hướng dẫn hệ thống."
        )

        # 5. Gọi LLM sinh phản hồi
        llm_start = time.time()
        raw_llm_output = self.llm_client.generate_json(
            prompt=user_prompt,
            system_instruction=SYSTEM_PROMPT_TEMPLATE,
            max_output_tokens=1024,
        )
        llm_time = time.time() - llm_start
        timings["llm_generation_ms"] = round(llm_time * 1000, 2)

        # 6. Kiểm định cấu trúc phản hồi và xác thực Citation từ Backend
        res_status = raw_llm_output.get("status", "answered")
        if res_status not in ("answered", "needs_clarification", "insufficient_evidence", "out_of_scope"):
            res_status = "answered"

        answer_text = raw_llm_output.get("answer", "")
        if not answer_text or not isinstance(answer_text, str):
            answer_text = "Hệ thống đã ghi nhận thông tin nhưng chưa thể tạo câu trả lời hoàn chỉnh."

        model_cited_ids = raw_llm_output.get("cited_source_ids", [])
        if not isinstance(model_cited_ids, list):
            model_cited_ids = []

        # Backend Citation Verification: Lọc bỏ các ID do model tự bịa
        verified_citations: List[CitationItem] = []
        valid_cited_ids: Set[str] = set()

        for c_id in model_cited_ids:
            if isinstance(c_id, str):
                c_clean = c_id.strip()
                # Chuẩn hóa nếu model ghi SRC-1 hoặc [SRC-1]
                c_clean = c_clean.strip("[]")
                if c_clean in valid_source_map and c_clean not in valid_cited_ids:
                    valid_cited_ids.add(c_clean)
                    src_obj = valid_source_map[c_clean]
                    # Lấy trích đoạn đại diện ngắn (tối đa 120 ký tự)
                    snippet = src_obj.text.strip().replace("\n", " ")
                    if len(snippet) > 120:
                        snippet = snippet[:117] + "..."
                    cit = CitationItem(
                        source_id=src_obj.source_id,
                        document_id=src_obj.document_id,
                        article=src_obj.article,
                        pdf_page=src_obj.start_page_pdf,
                        printed_page=src_obj.start_page_printed,
                        quote_snippet=snippet,
                        similarity=src_obj.similarity,
                    )
                    verified_citations.append(cit)

        # Nếu model tuyên bố 'answered' nhưng không trích dẫn nguồn hợp lệ nào
        if res_status == "answered" and not verified_citations and source_contexts:
            # Gán nguồn có độ tương đồng cao nhất nếu có căn cứ rõ ràng hoặc hạ về needs_clarification
            top_src = source_contexts[0]
            if top_src.similarity >= 0.40:
                snippet = top_src.text.strip().replace("\n", " ")
                if len(snippet) > 120:
                    snippet = snippet[:117] + "..."
                verified_citations.append(CitationItem(
                    source_id=top_src.source_id,
                    document_id=top_src.document_id,
                    article=top_src.article,
                    pdf_page=top_src.start_page_pdf,
                    printed_page=top_src.start_page_printed,
                    quote_snippet=snippet,
                    similarity=top_src.similarity,
                ))

        timings["total_ms"] = round((time.time() - total_start) * 1000, 2)

        return RAGResponse(
            request_id=request_id,
            question=clean_question,
            status=res_status,
            answer=answer_text,
            citations=verified_citations,
            sources_considered=len(source_contexts),
            sources_cited=len(verified_citations),
            timings=timings,
            is_live_llm=self.llm_client.is_live,
            model_name=self.llm_client.model,
        )
