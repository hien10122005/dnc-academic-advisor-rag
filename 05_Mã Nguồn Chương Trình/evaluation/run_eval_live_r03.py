# -*- coding: utf-8 -*-
"""
evaluation.run_eval_live_r03
Thực thi đánh giá thực nghiệm RAG Live với Gemini 3.5 Flash trên tập 10 ca phát triển (QĐ 580).
Đặc tả nhiệm vụ DNC-RAG-TASK-04-R03:
- Kết nối mô hình Live thực tế (gemini-3.5-flash).
- Thu thập toàn diện số liệu telemetry: retrieval_ms, llm_ms, total_ms, status, answer, citations.
- Đối chiếu thủ công độ bám nguồn, tính chính xác của trích dẫn và các ý bắt buộc.
- Xuất kết quả dạng JSONL và CSV phục vụ báo cáo khoa học.
"""

from __future__ import annotations
import csv
import json
import logging
import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.config import DEV_CASES_FILE, RESULTS_DIR
from backend.gemini_client import GeminiClient
from backend.rag_engine import RAGEngine
from backend.retrieval import VectorRetriever

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("dnc_rag.eval_live")


def run_evaluation():
    print("=" * 80)
    print("KHỞI ĐỘNG ĐÁNH GIÁ RAG LIVE VỚI GOOGLE GEMINI (TẬP 10 CA PHÁT TRIỂN)")
    print("=" * 80)

    # 1. Khởi tạo Retriever và Gemini Live Client
    retriever = VectorRetriever()
    readiness = retriever.check_readiness()
    print(f"Kho tri thức: {readiness['collection_name']} ({readiness['total_chunks']} chunks) READY.")

    gemini_client = GeminiClient(allow_offline_mock=False)
    print(f"Mô hình đang sử dụng: {gemini_client.model}")
    smoke = gemini_client.smoke_test()
    print(f"Smoke test Gemini Live: {smoke}")
    if not smoke.get("live"):
        raise RuntimeError(f"Smoke test kết nối Gemini Live thất bại: {smoke}")

    engine = RAGEngine(retriever=retriever, llm_client=gemini_client, top_k=5)

    # 2. Đọc tập 10 ca phát triển
    cases = []
    with open(DEV_CASES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))

    print(f"Đã nạp {len(cases)} ca phát triển từ {DEV_CASES_FILE}.")

    results = []
    total_eval_start = time.time()

    for idx, case in enumerate(cases, 1):
        cid = case["id"]
        cat = case["category"]
        question = case["question"]
        print(f"\n[{idx}/10] Đang xử lý ca: {cid} ({cat})")
        print(f"  Câu hỏi: {question}")

        t0 = time.time()
        try:
            rag_res = engine.answer_question(question)
            eval_time = time.time() - t0

            item = {
                "id": cid,
                "category": cat,
                "question": question,
                "status": rag_res.status,
                "answer": rag_res.answer,
                "citations": [
                    {
                        "source_id": c.source_id,
                        "chunk_id": c.chunk_id,
                        "article": c.article,
                        "pdf_page": c.pdf_page,
                        "printed_page": c.printed_page,
                        "quote_snippet": c.quote_snippet,
                        "similarity": c.similarity,
                    }
                    for c in rag_res.citations
                ],
                "sources_considered": rag_res.sources_considered,
                "sources_cited": rag_res.sources_cited,
                "retrieval_ms": rag_res.timings.get("retrieval_ms", 0.0),
                "llm_generation_ms": rag_res.timings.get("llm_generation_ms", 0.0),
                "total_ms": rag_res.timings.get("total_ms", 0.0),
                "is_live_llm": rag_res.is_live_llm,
                "model_name": rag_res.model_name,
                "expected_behavior": case.get("expected_behavior", ""),
                "mandatory_points": case.get("mandatory_points", []),
            }

            print(f"  -> Trạng thái: {rag_res.status} | Trích dẫn: {len(rag_res.citations)} nguồn")
            print(f"  -> Thời gian: Truy xuất {item['retrieval_ms']}ms | LLM {item['llm_generation_ms']}ms | Tổng {item['total_ms']}ms")
            print(f"  -> Trả lời: {rag_res.answer[:160]}...")
            results.append(item)

        except Exception as exc:
            print(f"  -> LỖI khi xử lý {cid}: {exc}")
            results.append({
                "id": cid,
                "category": cat,
                "question": question,
                "error": str(exc),
                "status": "ERROR",
            })

        # Nghỉ giữa các request để đảm bảo không chạm ngưỡng 15 RPM của Google AI Studio (Free tier)
        time.sleep(12.0)

    total_time = time.time() - total_eval_start
    print("\n" + "=" * 80)
    print(f"HOÀN THÀNH ĐÁNH GIÁ 10 CA TRONG {total_time:.2f} GIÂY")
    print("=" * 80)

    # 3. Lưu kết quả JSONL
    jsonl_path = RESULTS_DIR / "DNC_RAG_LIVE_DEV10_R03.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Đã lưu kết quả chi tiết: {jsonl_path}")

    # 4. Lưu kết quả CSV (UTF-8 BOM)
    csv_path = RESULTS_DIR / "DNC_RAG_LIVE_DEV10_R03.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Mã ca",
            "Phân loại",
            "Câu hỏi",
            "Trạng thái",
            "Số nguồn trích dẫn",
            "Các điều khoản trích dẫn",
            "Trang PDF",
            "Trang in",
            "Thời gian Truy xuất (ms)",
            "Thời gian LLM (ms)",
            "Tổng thời gian (ms)",
            "Nội dung câu trả lời",
        ])

        for r in results:
            cited_articles = "; ".join([c["article"] for c in r.get("citations", [])])
            pdf_pages = "; ".join([str(c["pdf_page"]) for c in r.get("citations", [])])
            printed_pages = "; ".join([str(c["printed_page"]) if c["printed_page"] is not None else "N/A" for c in r.get("citations", [])])

            writer.writerow([
                r["id"],
                r["category"],
                r["question"],
                r.get("status", "ERROR"),
                r.get("sources_cited", 0),
                cited_articles,
                pdf_pages,
                printed_pages,
                r.get("retrieval_ms", 0.0),
                r.get("llm_generation_ms", 0.0),
                r.get("total_ms", 0.0),
                r.get("answer", r.get("error", "")),
            ])

    print(f"Đã lưu bảng tổng hợp CSV: {csv_path}")


if __name__ == "__main__":
    run_evaluation()
