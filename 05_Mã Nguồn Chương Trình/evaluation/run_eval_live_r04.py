# -*- coding: utf-8 -*-
"""
evaluation.run_eval_live_r04
Thực thi đánh giá thực nghiệm RAG Live với Gemini 3.5 Flash-lite trên tập 10 ca phát triển (QĐ 580).
Đặc tả nhiệm vụ DNC-RAG-TASK-04-R04:
- Kết nối mô hình Live thực tế (gemini-3.5-flash-lite).
- Thu thập đầy đủ Run Metadata (run_id, timestamp, code_version, prompt template).
- Lưu trữ đầy đủ 5 retrieved contexts (chunk_id, article, pdf_page, similarity, content, source_spans) và user_prompt.
- Đo lường chi tiết thời gian: retrieval_ms, llm_generation_ms, total_ms.
- Xuất kết quả chi tiết ra DNC_RAG_LIVE_DEV10_R04.jsonl và DNC_RAG_LIVE_DEV10_R04.csv.
"""

from __future__ import annotations
import csv
import json
import logging
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.config import DEV_CASES_FILE, RESULTS_DIR
from backend.gemini_client import GeminiClient
from backend.rag_engine import RAGEngine, SYSTEM_PROMPT_TEMPLATE
from backend.retrieval import VectorRetriever

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("dnc_rag.eval_live_r04")


def get_git_commit() -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout.strip()
    except Exception:
        return "UNKNOWN"


def run_evaluation():
    print("=" * 80)
    print("KHỞI ĐỘNG ĐÁNH GIÁ RAG LIVE R04 VỚI GOOGLE GEMINI (TẬP 10 CA PHÁT TRIỂN)")
    print("=" * 80)

    run_id = f"eval_r04_{uuid.uuid4().hex[:8]}"
    start_iso = datetime.now(timezone.utc).isoformat()
    git_commit = get_git_commit()

    # 1. Khởi tạo Retriever và Gemini Live Client
    retriever = VectorRetriever()
    readiness = retriever.check_readiness()
    print(f"Kho tri thức: {readiness['collection_name']} ({readiness['total_chunks']} chunks) READY.")

    gemini_client = GeminiClient(allow_offline_mock=False)
    print(f"Mô hình đang sử dụng: {gemini_client.model}")
    smoke = gemini_client.smoke_test()
    print(f"Smoke test Gemini Live: {smoke}")
    if not smoke.get("live") or smoke.get("status") != "CONNECTED":
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

        try:
            # Thu thập retrieved contexts trước để lưu trữ artifact đầy đủ
            raw_retrieved = retriever.retrieve(question, top_k=5)
            retrieved_contexts_data = []
            context_blocks = []
            for s_idx, r in enumerate(raw_retrieved, 1):
                src_id = f"SRC-{s_idx}"
                retrieved_contexts_data.append({
                    "source_id": src_id,
                    "chunk_id": r.get("chunk_id", ""),
                    "article": r.get("article", ""),
                    "start_page_pdf": r.get("start_page_pdf", 1),
                    "end_page_pdf": r.get("end_page_pdf", 1),
                    "similarity": float(r.get("similarity", 0.0)),
                    "content": r.get("content", ""),
                    "source_spans": r.get("source_spans", []),
                })
                page_info = f"Trang PDF {r.get('start_page_pdf', 1)}"
                if r.get('start_page_pdf') != r.get('end_page_pdf'):
                    page_info += f"-{r.get('end_page_pdf')}"
                context_blocks.append(f"[{src_id}] ({r.get('article', '')} - {page_info}):\n{r.get('content', '')}")

            joined_context = "\n\n---\n\n".join(context_blocks)
            user_prompt = (
                f"Dưới đây là các đoạn thông tin quy chế trích xuất từ kho tri thức:\n\n"
                f"{joined_context}\n\n"
                f"CÂU HỎI CỦA SINH VIÊN:\n{question}\n\n"
                f"Hãy trả lời bằng định dạng JSON theo đúng hướng dẫn hệ thống."
            )

            # Thực thi RAG toàn trình
            rag_res = engine.answer_question(question)

            item = {
                "run_id": run_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "git_commit": git_commit,
                "id": cid,
                "category": cat,
                "question": question,
                "expected_behavior": case.get("expected_behavior", ""),
                "mandatory_points": case.get("mandatory_points", []),
                "status": rag_res.status,
                "answer": rag_res.answer,
                "citations": [
                    {
                        "source_id": c.source_id,
                        "chunk_id": c.chunk_id,
                        "document_id": c.document_id,
                        "article": c.article,
                        "pdf_page": c.pdf_page,
                        "printed_page": c.printed_page,
                        "quote_snippet": c.quote_snippet,
                        "similarity": c.similarity,
                        "spans": c.spans,
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
                "retrieved_contexts": retrieved_contexts_data,
                "user_prompt": user_prompt,
                "system_instruction": SYSTEM_PROMPT_TEMPLATE,
            }

            print(f"  -> Trạng thái: {rag_res.status} | Trích dẫn: {len(rag_res.citations)} nguồn")
            print(f"  -> Thời gian: Truy xuất {item['retrieval_ms']}ms | LLM {item['llm_generation_ms']}ms | Tổng {item['total_ms']}ms")
            print(f"  -> Trả lời: {rag_res.answer[:160]}...")
            results.append(item)

        except Exception as exc:
            print(f"  -> LỖI khi xử lý {cid}: {exc}")
            results.append({
                "run_id": run_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "git_commit": git_commit,
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
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    jsonl_path = RESULTS_DIR / "DNC_RAG_LIVE_DEV10_R04.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Đã lưu kết quả chi tiết: {jsonl_path}")

    # 4. Lưu kết quả CSV (UTF-8 BOM)
    csv_path = RESULTS_DIR / "DNC_RAG_LIVE_DEV10_R04.csv"
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
            "Câu trả lời",
        ])
        for r in results:
            if r.get("status") == "ERROR":
                writer.writerow([
                    r["id"], r["category"], r["question"], "ERROR", 0, "", "", "", 0, 0, 0, r.get("error", "")
                ])
                continue

            cits = r.get("citations", [])
            articles = "; ".join([c["article"] for c in cits])
            pdf_pages = "; ".join([str(c["pdf_page"]) for c in cits])
            printed_pages = "; ".join([str(c["printed_page"]) if c["printed_page"] is not None else "-" for c in cits])

            writer.writerow([
                r["id"],
                r["category"],
                r["question"],
                r["status"],
                r["sources_cited"],
                articles,
                pdf_pages,
                printed_pages,
                r["retrieval_ms"],
                r["llm_generation_ms"],
                r["total_ms"],
                r["answer"],
            ])
    print(f"Đã lưu tệp tổng hợp CSV: {csv_path}")


if __name__ == "__main__":
    run_evaluation()
