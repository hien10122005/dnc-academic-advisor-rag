# -*- coding: utf-8 -*-
"""
backend.rag_engine
RAG Engine cốt lõi cho hệ thống Trợ lý học vụ DNC (QĐ 580/QĐ-ĐHNCT ngày 02/08/2024).
Luồng xử lý nghiêm ngặt:
1. Xác thực đầu vào (Validation): kiểm tra câu hỏi rỗng/quá dài (<= 1000 ký tự).
2. Tiền kiểm tra kho tri thức (Preflight Readiness) & Truy xuất Top-K từ VectorRetriever.
3. Đóng gói ngữ cảnh thuần túy (tách rời context_prefix) và gán mã định danh nguồn độc lập [SRC-1, SRC-2,...].
4. Xây dựng System Prompt học thuật chuẩn mực (khách quan, bám sát văn bản quy chế QĐ 580).
5. Gọi LLM sinh câu trả lời có cấu trúc JSON.
6. Xác minh trích dẫn (Citation Verification) độc lập ở backend:
   - BỎ HOÀN TOÀN việc tự gắn nguồn dựa trên similarity khi thiếu trích dẫn.
   - Kiểm tra schema nghiêm ngặt: không tự đổi status sai/answer rỗng thành 'answered'.
   - Nếu phát hiện ID bịa (hallucination), hạ trạng thái an toàn 'insufficient_evidence'.
   - Dựng trích đoạn (quote_snippet) chuẩn xác từ source_spans và nội dung gốc (không dính context prefix).
   - Trang in (printed_page) được quản lý dạng nullable (None khi không xác định).
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
from backend.errors import RAGSchemaError, ValidationError
from backend.gemini_client import GeminiClient
from backend.retrieval import VectorRetriever

logger = logging.getLogger("dnc_rag.rag_engine")

SYSTEM_PROMPT_TEMPLATE = """Bạn là Trợ lý Học vụ AI hỗ trợ sinh viên tra cứu Quy chế Đào tạo trình độ Đại học của Trường Đại học Nam Cần Thơ (theo Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024).
Đây là sản phẩm đồ án học thuật nghiên cứu hỗ trợ thông tin học vụ, không phải phát ngôn viên chính thức của Nhà trường.

BỘ QUY TẮC BẮT BUỘC KHI TRẢ LỜI:
1. TÍNH CHÍNH XÁC VÀ BÁM NGUỒN (GROUNDEDNESS):
   - Chỉ được đưa ra các kết luận, điều kiện, mức điểm, thời hạn, quyền và nghĩa vụ dựa trên các đoạn trích nguồn [SRC-x] được cung cấp dưới đây.
   - Giữ nguyên các con số, ngưỡng điểm, tỷ lệ, điều kiện ràng buộc và ngoại lệ đúng như văn bản gốc.
   - Trả lời đầy đủ, toàn diện các khía cạnh của quy định: bao gồm các điều kiện tiên quyết, ngoại lệ/trường hợp đặc biệt, các nhánh lựa chọn (nếu quy chế nêu nhiều phương án giải quyết), và quy tắc làm tròn số thập phân (nếu điều khoản có đề cập). Tuyệt đối không chỉ khẳng định một chiều mà bỏ sót các điều kiện hay nhánh xử lý liên quan.
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
   - Khi chọn "status": "answered", BẮT BUỘC phải trích dẫn ít nhất một mã nguồn [SRC-x] hợp lệ từ danh sách được cấp.
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
    start_page_printed: Optional[int]
    end_page_printed: Optional[int]
    is_table: bool
    context_prefix: str
    content: str
    embedding_text: str
    similarity: float
    source_spans: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CitationItem:
    """Thông tin trích dẫn nguồn được backend xác thực và xây dựng."""
    source_id: str
    chunk_id: str
    document_id: str
    article: str
    pdf_page: int
    printed_page: Optional[int]
    quote_snippet: str
    similarity: float
    spans: List[Dict[str, Any]] = field(default_factory=list)


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
    trace: Optional[Dict[str, Any]] = None

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
        return_trace: bool = False,
        mode: str = "dense",
    ) -> RAGResponse:
        """
        Thực thi quy trình RAG hoàn chỉnh cho một câu hỏi độc lập.
        """
        request_id = str(uuid.uuid4())
        total_start = time.perf_counter()
        timings: Dict[str, float] = {}

        # 1. Kiểm tra tính hợp lệ của câu hỏi đầu vào
        clean_question = question.strip() if question else ""
        if not clean_question:
            raise ValidationError("Câu hỏi không được để trống hoặc chỉ chứa khoảng trắng.")
        if len(clean_question) > 1000:
            raise ValidationError(f"Câu hỏi quá dài ({len(clean_question)} ký tự). Giới hạn tối đa là 1000 ký tự.")

        # 2. Tiền kiểm tra tính sẵn sàng của kho tri thức (Preflight) & Truy xuất
        k = top_k if top_k is not None else self.top_k
        retrieval_start = time.perf_counter()

        # Hỗ trợ cả 2 chế độ: dense và hybrid
        if mode == "hybrid" and hasattr(self.retriever, "retrieve_hybrid"):
            retrieved_raw = self.retriever.retrieve_hybrid(clean_question, top_k=k)
        else:
            retrieved_raw = self.retriever.retrieve(clean_question, top_k=k)

        retrieval_time = time.perf_counter() - retrieval_start
        timings["retrieval_ms"] = round(retrieval_time * 1000, 2)

        # 3. Chuẩn bị ngữ cảnh và gán Source ID định danh
        source_contexts: List[SourceContext] = []
        valid_source_map: Dict[str, SourceContext] = {}

        for idx, item in enumerate(retrieved_raw, 1):
            src_id = f"SRC-{idx}"
            pure_content = item.get("content", "")
            ctx_prefix = item.get("context_prefix", "")

            # Chuẩn hóa trang in dạng nullable
            pr_start = item.get("start_page_printed")
            if pr_start is not None and (int(pr_start) <= 0 or pr_start == -1):
                pr_start = None
            pr_end = item.get("end_page_printed")
            if pr_end is not None and (int(pr_end) <= 0 or pr_end == -1):
                pr_end = None

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
                start_page_printed=pr_start,
                end_page_printed=pr_end,
                is_table=item.get("is_table", False),
                context_prefix=ctx_prefix,
                content=pure_content,
                embedding_text=item.get("embedding_text", pure_content),
                similarity=float(item.get("similarity", 0.0)),
                source_spans=item.get("source_spans", []),
            )
            source_contexts.append(src_ctx)
            valid_source_map[src_id] = src_ctx

        # 4. Xây dựng Prompt cho LLM: Sử dụng nội dung thuần túy, không để context_prefix gây nhiễu
        context_blocks = []
        for s in source_contexts:
            page_info = f"Trang PDF {s.start_page_pdf}"
            if s.start_page_pdf != s.end_page_pdf:
                page_info += f"-{s.end_page_pdf}"
            if s.start_page_printed is not None:
                page_info += f" (Trang in: {s.start_page_printed})"

            block = f"[{s.source_id}] ({s.article} - {page_info}):\n{s.content}"
            context_blocks.append(block)

        joined_context = "\n\n---\n\n".join(context_blocks)
        user_prompt = (
            f"Dưới đây là các đoạn thông tin quy chế trích xuất từ kho tri thức:\n\n"
            f"{joined_context}\n\n"
            f"CÂU HỎI CỦA SINH VIÊN:\n{clean_question}\n\n"
            f"Hãy trả lời bằng định dạng JSON theo đúng hướng dẫn hệ thống."
        )

        # 5. Gọi LLM sinh phản hồi
        llm_start = time.perf_counter()
        raw_llm_output = self.llm_client.generate_json(
            prompt=user_prompt,
            system_instruction=SYSTEM_PROMPT_TEMPLATE,
            max_output_tokens=2048,
        )
        llm_time = time.perf_counter() - llm_start
        timings["llm_generation_ms"] = round(llm_time * 1000, 2)

        # 6. Kiểm định cấu trúc phản hồi và xác thực Citation từ Backend
        if not isinstance(raw_llm_output, dict):
            raise RAGSchemaError("Phản hồi từ LLM không phải là một JSON object.")

        # Xác thực trạng thái nghiệp vụ bắt buộc
        raw_status = raw_llm_output.get("status")
        valid_statuses = ("answered", "needs_clarification", "insufficient_evidence", "out_of_scope")
        if raw_status not in valid_statuses:
            raise RAGSchemaError(
                f"Trường 'status' không hợp lệ: '{raw_status}'. Yêu cầu một trong các giá trị: {valid_statuses}"
            )

        answer_text = raw_llm_output.get("answer")
        if not isinstance(answer_text, str) or not answer_text.strip():
            raise RAGSchemaError("Trường 'answer' bị rỗng hoặc không phải kiểu chuỗi văn bản.")

        raw_cited_ids = raw_llm_output.get("cited_source_ids")
        if not isinstance(raw_cited_ids, list):
            raise RAGSchemaError("Trường 'cited_source_ids' không phải kiểu danh sách.")

        # Phân loại Source IDs trích dẫn: nguồn hợp lệ vs nguồn bịa (hallucination)
        valid_cited_ids: Set[str] = set()
        hallucinated_ids: List[str] = []

        for c_id in raw_cited_ids:
            if isinstance(c_id, str):
                c_clean = c_id.strip().strip("[]").upper()
                if c_clean in valid_source_map:
                    valid_cited_ids.add(c_clean)
                else:
                    hallucinated_ids.append(str(c_id))
            else:
                hallucinated_ids.append(str(c_id))

        # CHÍNH SÁCH KIỂM ĐỊNH NGUỒN VÀ BẢO ĐẢM TÍNH LIÊM CHÍNH (CITATION INTEGRITY POLICY):
        final_status = raw_status
        final_answer = answer_text
        verified_citations: List[CitationItem] = []

        # 6.1. Trường hợp có bất kỳ ID trích dẫn bịa nào (Hallucination)
        if hallucinated_ids:
            logger.warning(
                "Phát hiện mô hình viện dẫn ID không có trong ngữ cảnh: %s. Hạ trạng thái an toàn.",
                hallucinated_ids
            )
            final_status = "insufficient_evidence"
            final_answer = (
                f"Phản hồi bị từ chối do mô hình viện dẫn nguồn không có trong ngữ cảnh truy xuất ({', '.join(hallucinated_ids)}). "
                "Quy chế đào tạo hiện tại chưa cung cấp đủ dữ liệu để chứng minh khẳng định này."
            )
            verified_citations = []

        # 6.2. Trường hợp mô hình tự nhận 'answered' nhưng KHÔNG có trích dẫn hợp lệ nào
        elif raw_status == "answered" and not valid_cited_ids:
            logger.warning("Mô hình phản hồi 'answered' nhưng không có trích dẫn hợp lệ. Hạ trạng thái an toàn.")
            final_status = "insufficient_evidence"
            final_answer = (
                "Câu trả lời bị hạ trạng thái do mô hình không trích dẫn được điều khoản quy chế cụ thể nào từ ngữ cảnh đã cấp."
            )
            verified_citations = []

        # 6.3. Trường hợp hợp lệ: Xây dựng CitationItem chuẩn từ source_spans và nội dung gốc
        else:
            for c_clean in sorted(valid_cited_ids):
                src_obj = valid_source_map[c_clean]

                # Trích xuất đoạn văn từ source_spans để bảo đảm tính truy nguyên PDF nguyên bản
                # Ưu tiên span nội dung chính thực chất (bỏ qua header bảng lặp lại, overlap, và tiêu đề ngắn)
                substantive_spans = []
                for sp in src_obj.source_spans:
                    if not sp.get("is_added_context") and not sp.get("is_overlap"):
                        cs = sp.get("chunk_start_char", 0)
                        ce = sp.get("chunk_end_char", len(src_obj.content))
                        stext = src_obj.content[cs:ce].strip()
                        substantive_spans.append((sp, len(stext), stext))

                primary_span = None
                if substantive_spans:
                    # Ưu tiên span có nội dung thực chất dài hơn (tránh chọn trúng tiêu đề điều khoản ngắn)
                    for sp, slen, stext in substantive_spans:
                        if slen > 50 and not stext.startswith("Điều ") and not stext.startswith("Chương "):
                            primary_span = sp
                            break
                    if primary_span is None:
                        substantive_spans.sort(key=lambda x: x[1], reverse=True)
                        primary_span = substantive_spans[0][0]
                elif src_obj.source_spans:
                    primary_span = src_obj.source_spans[0]

                if primary_span is not None:
                    c_s = primary_span.get("chunk_start_char", 0)
                    c_e = primary_span.get("chunk_end_char", len(src_obj.content))
                    span_text = src_obj.content[c_s:c_e].strip().replace("\n", " ")
                    snippet = span_text[:140] + ("..." if len(span_text) > 140 else "")
                    pdf_p = primary_span.get("pdf_page", src_obj.start_page_pdf)
                    pr_p = primary_span.get("printed_page", src_obj.start_page_printed)
                else:
                    raw_text = src_obj.content.strip().replace("\n", " ")
                    snippet = raw_text[:140] + ("..." if len(raw_text) > 140 else "")
                    pdf_p = src_obj.start_page_pdf
                    pr_p = src_obj.start_page_printed

                # Đảm bảo snippet là văn bản nguyên bản, không chứa tiền tố ngữ cảnh '['
                if snippet.startswith("["):
                    snippet = snippet.lstrip("[]").strip()

                cit = CitationItem(
                    source_id=src_obj.source_id,
                    chunk_id=src_obj.chunk_id,
                    document_id=src_obj.document_id,
                    article=src_obj.article,
                    pdf_page=pdf_p,
                    printed_page=pr_p,
                    quote_snippet=snippet,
                    similarity=src_obj.similarity,
                    spans=src_obj.source_spans,
                )
                verified_citations.append(cit)

        timings["total_ms"] = round((time.perf_counter() - total_start) * 1000, 2)

        trace_data: Optional[Dict[str, Any]] = None
        if return_trace:
            trace_data = {
                "user_prompt": user_prompt,
                "system_instruction": SYSTEM_PROMPT_TEMPLATE,
                "generation_config": {
                    "max_output_tokens": 2048,
                    "temperature": 0.0,
                    "model": self.llm_client.model,
                },
                "retrieved_contexts": [
                    {
                        "source_id": s.source_id,
                        "chunk_id": s.chunk_id,
                        "article": s.article,
                        "start_page_pdf": s.start_page_pdf,
                        "end_page_pdf": s.end_page_pdf,
                        "start_page_printed": s.start_page_printed,
                        "end_page_printed": s.end_page_printed,
                        "similarity": s.similarity,
                        "content": s.content,
                        "source_spans": s.source_spans,
                    }
                    for s in source_contexts
                ],
                "mode": mode,
            }

        return RAGResponse(
            request_id=request_id,
            question=clean_question,
            status=final_status,
            answer=final_answer,
            citations=verified_citations,
            sources_considered=len(source_contexts),
            sources_cited=len(verified_citations),
            timings=timings,
            is_live_llm=self.llm_client.is_using_live_api,
            model_name=self.llm_client.model,
            trace=trace_data,
        )
