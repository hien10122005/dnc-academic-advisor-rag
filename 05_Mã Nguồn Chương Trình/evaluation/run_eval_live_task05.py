# -*- coding: utf-8 -*-
"""
evaluation.run_eval_live_task05
Thực thi đánh giá thực nghiệm A/B Live (Dense vs Hybrid) với Google Gemini (gemini-3.5-flash-lite).
Đặc tả nhiệm vụ DNC-RAG-TASK-05-R01:
- Thu thập trace trực tiếp từ engine.answer_question(..., return_trace=True) không gọi truy xuất lần hai.
- Đo thời gian bằng time.perf_counter() cho retrieval_ms, llm_generation_ms, total_ms.
- Ghi nhận đầy đủ Run Metadata: run_id, git_commit, git_dirty, corpus_hash, manifest_hash, model_name, generation_config.
- Chạy cả 2 mode Dense và Hybrid trên tập 10 ca DEV_01 -> DEV_10.
- Xuất dữ liệu ra evaluation/results/DNC_RAG_AB_DEV10_TASK05.jsonl và DNC_RAG_AB_DEV10_TASK05.csv.
"""

from __future__ import annotations
import csv
from dataclasses import asdict
import hashlib
import json
import logging
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.config import (
    CHUNKS_FILE,
    COLLECTION_NAME,
    CORPUS_FILE,
    DEV_CASES_FILE,
    MANIFEST_FILE,
    RESULTS_DIR,
)
from backend.gemini_client import GeminiClient
from backend.rag_engine import RAGEngine
from backend.retrieval import VectorRetriever

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("dnc_rag.eval_live_task05")


def get_git_info() -> Dict[str, Any]:
    try:
        commit_res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=True,
        )
        commit_sha = commit_res.stdout.strip()
    except Exception:
        commit_sha = "UNKNOWN"

    try:
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=True,
        )
        is_dirty = bool(status_res.stdout.strip())
        dirty_files = [line.strip() for line in status_res.stdout.strip().splitlines() if line.strip()]
    except Exception:
        is_dirty = False
        dirty_files = []

    return {
        "git_commit": commit_sha,
        "is_dirty": is_dirty,
        "dirty_files_count": len(dirty_files),
    }


def compute_file_sha256(path: Path) -> str:
    if not path.exists():
        return "NOT_FOUND"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def run_live_ab_evaluation():
    print("=" * 80)
    print("KHỞI ĐỘNG ĐÁNH GIÁ THỰC NGHIỆM A/B LIVE GEMINI (TASK 05: DENSE VS HYBRID)")
    print("=" * 80)

    run_id = f"eval_task05_{uuid.uuid4().hex[:8]}"
    start_iso = datetime.now(timezone.utc).isoformat()
    git_info = get_git_info()
    chunks_hash = compute_file_sha256(CHUNKS_FILE)
    manifest_hash = compute_file_sha256(MANIFEST_FILE)

    print(f"Run ID: {run_id}")
    print(f"Timestamp (UTC): {start_iso}")
    print(f"Git Commit: {git_info['git_commit']} (Dirty: {git_info['is_dirty']})")
    print(f"Chunks SHA256: {chunks_hash}")
    print(f"Manifest SHA256: {manifest_hash}")

    # 1. Khởi tạo Retriever và Live Gemini Client
    retriever = VectorRetriever()
    readiness = retriever.check_readiness()
    print(f"Kho tri thức: {readiness['collection_name']} ({readiness['total_chunks']} chunks) READY.")

    gemini_client = GeminiClient(allow_offline_mock=False)
    print(f"Gemini Client: model={gemini_client.model}, timeout={gemini_client.timeout}s")
    smoke = gemini_client.smoke_test()
    print(f"Smoke test Gemini Live: {smoke}")
    if not smoke.get("live") or smoke.get("status") != "CONNECTED":
        raise RuntimeError(f"Smoke test kết nối Gemini Live thất bại: {smoke}")

    engine = RAGEngine(retriever=retriever, llm_client=gemini_client, top_k=5)

    # 2. Đọc tập 10 ca phát triển
    dev_cases = []
    with open(DEV_CASES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                dev_cases.append(json.loads(line.strip()))
    print(f"Đã nạp {len(dev_cases)} ca phát triển từ {DEV_CASES_FILE}.")

    # 3. Chạy đánh giá cả 2 chế độ: dense, hybrid
    all_runs_data: List[Dict[str, Any]] = []
    csv_rows: List[Dict[str, Any]] = []

    modes = ["dense", "hybrid"]

    for mode in modes:
        print(f"\n{'=' * 30} CHẠY CHẾ ĐỘ: {mode.upper()} {'=' * 30}")
        for idx, case in enumerate(dev_cases, 1):
            cid = case["id"]
            cat = case["category"]
            question = case["question"]
            expected_points = case.get("mandatory_points", [])

            print(f"\n[{mode.upper()}][{idx}/10] Đang xử lý ca: {cid} ({cat})")
            print(f"  Câu hỏi: {question[:80]}...")

            t_case_start = time.perf_counter()
            try:
                # Gọi engine với mode tương ứng và return_trace=True
                resp = engine.answer_question(question, mode=mode, return_trace=True)
                wall_ms = (time.perf_counter() - t_case_start) * 1000.0

                # Trích xuất trace trực tiếp từ phản hồi (không gọi retrieval lần 2)
                trace = resp.trace or {}
                retrieved_contexts = trace.get("retrieved_contexts", [])
                user_prompt = trace.get("user_prompt", "")
                system_instruction = trace.get("system_instruction", "")
                generation_config = trace.get("generation_config", {})

                # Cấu trúc bản ghi JSONL
                run_record = {
                    "run_id": run_id,
                    "case_id": cid,
                    "mode": mode,
                    "category": cat,
                    "question": question,
                    "status": resp.status,
                    "answer": resp.answer,
                    "sources_considered": resp.sources_considered,
                    "sources_cited": resp.sources_cited,
                    "citations": [asdict(c) for c in resp.citations],
                    "timings": resp.timings,
                    "wall_time_ms": round(wall_ms, 2),
                    "is_live_llm": resp.is_live_llm,
                    "model_name": resp.model_name,
                    "retrieved_contexts": retrieved_contexts,
                    "user_prompt": user_prompt,
                    "system_instruction": system_instruction,
                    "generation_config": generation_config,
                    "mandatory_points": expected_points,
                    "metadata": {
                        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                        "git_commit": git_info["git_commit"],
                        "git_dirty": git_info["is_dirty"],
                        "chunks_hash": chunks_hash,
                        "manifest_hash": manifest_hash,
                        "collection_name": COLLECTION_NAME,
                    },
                }
                all_runs_data.append(run_record)

                # Chuẩn bị dòng CSV tóm tắt
                cited_str = "; ".join(
                    f"[{c.source_id}] {c.article} (Trang PDF {c.pdf_page})"
                    for c in resp.citations
                )
                csv_rows.append({
                    "run_id": run_id,
                    "mode": mode,
                    "case_id": cid,
                    "category": cat,
                    "question": question,
                    "status": resp.status,
                    "sources_considered": resp.sources_considered,
                    "sources_cited": resp.sources_cited,
                    "cited_sources": cited_str,
                    "retrieval_ms": resp.timings.get("retrieval_ms", 0.0),
                    "llm_generation_ms": resp.timings.get("llm_generation_ms", 0.0),
                    "total_ms": resp.timings.get("total_ms", 0.0),
                    "wall_ms": round(wall_ms, 2),
                    "model": resp.model_name,
                    "is_live": resp.is_live_llm,
                    "answer_preview": resp.answer[:250].replace("\n", " "),
                })

                print(f"  -> Trạng thái: {resp.status} | Trích dẫn: {resp.sources_cited}/{resp.sources_considered}")
                print(f"  -> Retrieval: {resp.timings.get('retrieval_ms')}ms | LLM: {resp.timings.get('llm_generation_ms')}ms | Total: {resp.timings.get('total_ms')}ms")

            except Exception as e:
                logger.error("Lỗi khi xử lý ca %s mode %s: %s", cid, mode, e, exc_info=True)
                err_record = {
                    "run_id": run_id,
                    "case_id": cid,
                    "mode": mode,
                    "category": cat,
                    "question": question,
                    "error": str(e),
                    "status": "ERROR",
                }
                all_runs_data.append(err_record)

            # Sleep 1.5s giữa các câu hỏi để tránh rate limit upstream
            time.sleep(1.5)

    # 4. Xuất file kết quả
    jsonl_path = RESULTS_DIR / "DNC_RAG_AB_DEV10_TASK05.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in all_runs_data:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nĐã xuất kết quả JSONL đầy đủ: {jsonl_path}")

    csv_path = RESULTS_DIR / "DNC_RAG_AB_DEV10_TASK05.csv"
    if csv_rows:
        fieldnames = list(csv_rows[0].keys())
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)
    print(f"Đã xuất bảng tóm tắt CSV: {csv_path}")

    print("\n" + "=" * 80)
    print("HOÀN THÀNH ĐÁNH GIÁ THỰC NGHIỆM A/B LIVE (TASK 05)")
    print("=" * 80)


if __name__ == "__main__":
    run_live_ab_evaluation()
