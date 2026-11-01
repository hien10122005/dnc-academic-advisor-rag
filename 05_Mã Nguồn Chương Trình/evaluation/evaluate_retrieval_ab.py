# -*- coding: utf-8 -*-
"""
evaluation.evaluate_retrieval_ab
Thực thi đánh giá so sánh thực nghiệm A/B Retrieval: Dense vs Hybrid (BM25 + RRF) trên 10 ca phát triển (QĐ 580).
Đặc tả nhiệm vụ DNC-RAG-TASK-05-R01:
- Đối chứng trung thực trên cùng tập 104 chunks (qd580_baseline_v2).
- Đo lường Hit@1, Hit@3, Hit@5, Hit@10, Partial Hit@10, Full Case Coverage@10, MRR@10.
- Đo thời gian truy xuất bằng time.perf_counter().
- Phân tích chi tiết từng ca (DEV_01 đến DEV_10), đặc biệt DEV_02, DEV_07, DEV_08.
- Xuất dữ liệu chi tiết ra evaluation/results/RETRIEVAL_AB_COMPARISON_TASK05.json.
"""

from __future__ import annotations
import json
import logging
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.config import (
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME,
    CORPUS_FILE,
    DEV_CASES_FILE,
    EMBEDDING_MODEL_CANDIDATE,
    RESULTS_DIR,
)
from backend.retrieval import VectorRetriever


def load_corpus_pages() -> List[Dict[str, Any]]:
    pages = []
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pages.append(json.loads(line.strip()))
    return pages


def find_evidence_span_on_page(pages: List[Dict[str, Any]], pdf_page: int, quote: str) -> Tuple[int, int]:
    if pdf_page < 1 or pdf_page > len(pages):
        return -1, -1

    p_content = pages[pdf_page - 1]["content"]
    clean_quote = quote.strip()
    if not clean_quote:
        return -1, -1

    pos = p_content.find(clean_quote)
    if pos != -1:
        return pos, pos + len(clean_quote)

    words = clean_quote.split()
    if not words:
        return -1, -1

    pattern = r"\s+".join(re.escape(w) for w in words)
    matches = list(re.finditer(pattern, p_content))
    if len(matches) >= 1:
        return matches[0].start(), matches[0].end()

    return -1, -1


def compute_span_intersection_ratio(
    evidence_span: Tuple[int, int],
    evidence_page: int,
    retrieved_chunks: List[Dict[str, Any]],
    top_k: int,
) -> float:
    q_s, q_e = evidence_span
    if q_s < 0 or q_e <= q_s:
        return 0.0

    target_len = q_e - q_s
    intersected_intervals: List[Tuple[int, int]] = []

    for ch in retrieved_chunks[:top_k]:
        spans = ch.get("source_spans", [])
        for sp in spans:
            if sp.get("is_added_context"):
                continue

            if sp.get("pdf_page") == evidence_page:
                sp_s = sp.get("page_start_char", 0)
                sp_e = sp.get("page_end_char", 0)

                overlap_s = max(q_s, sp_s)
                overlap_e = min(q_e, sp_e)

                if overlap_e > overlap_s:
                    intersected_intervals.append((overlap_s, overlap_e))

    if not intersected_intervals:
        return 0.0

    intersected_intervals.sort(key=lambda x: x[0])
    merged_intervals = [intersected_intervals[0]]

    for cur_s, cur_e in intersected_intervals[1:]:
        last_s, last_e = merged_intervals[-1]
        if cur_s <= last_e:
            merged_intervals[-1] = (last_s, max(last_e, cur_e))
        else:
            merged_intervals.append((cur_s, cur_e))

    total_covered_chars = sum(e - s for s, e in merged_intervals)
    coverage_ratio = total_covered_chars / target_len
    return min(1.0, round(coverage_ratio, 4))


def run_retrieval_ab_evaluation():
    print("=" * 80)
    print("ĐÁNH GIÁ THỰC NGHIỆM RETRIEVAL A/B: DENSE VS HYBRID (BM25 + RRF)")
    print("=" * 80)

    pages = load_corpus_pages()
    print(f"Đã nạp {len(pages)} trang quy chế gốc.")

    dev_cases = []
    with open(DEV_CASES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                dev_cases.append(json.loads(line.strip()))
    print(f"Đã nạp {len(dev_cases)} ca phát triển (DEV_01 -> DEV_10).")

    retriever = VectorRetriever(
        persist_dir=str(CHROMA_PERSIST_DIR),
        collection_name=COLLECTION_NAME,
        model_name=EMBEDDING_MODEL_CANDIDATE,
    )
    readiness = retriever.check_readiness()
    print(f"Retriever sẵn sàng: {readiness['collection_name']}, {readiness['total_chunks']} chunks.")

    # Warm-up model
    print("Warm-up retriever...")
    _ = retriever.retrieve("warm up query", top_k=1)
    _ = retriever.retrieve_hybrid("warm up query", top_k=1)
    print("Warm-up hoàn tất.")

    modes = ["dense", "hybrid"]
    all_eval_data: Dict[str, Any] = {}

    for mode in modes:
        print(f"\n>>> ĐANG CHẠY ĐÁNH GIÁ Ở CHẾ ĐỘ: {mode.upper()} <<<")
        grounded_cases: List[Dict[str, Any]] = []
        out_of_scope_cases: List[Dict[str, Any]] = []
        latencies: List[float] = []

        for case in dev_cases:
            cid = case.get("id") or case.get("case_id", "UNKNOWN")
            question = case["question"]
            category = case.get("category", "")
            query = case.get("retrieval_query", "").strip() or question.strip()
            expected_evidences = case.get("evidence") or case.get("expected_evidence", [])
            is_grounded = category != "NGOAI_PHAM_VI_THIEU_CAN_CU" and len(expected_evidences) > 0

            t0 = time.perf_counter()
            if mode == "dense":
                chunks = retriever.retrieve(query, top_k=10)
            else:
                chunks = retriever.retrieve_hybrid(query, top_k=10, dense_top_k=20, bm25_top_k=20, rrf_k=60)
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            latencies.append(elapsed_ms)

            # Map evidence spans
            evidence_spans = []
            for ev in expected_evidences:
                pno = ev.get("pdf_page", 0)
                quote = ev.get("quote", "") or ev.get("verbatim_quote", "")
                s_char, e_char = find_evidence_span_on_page(pages, pno, quote)
                evidence_spans.append({
                    "pdf_page": pno,
                    "quote": quote,
                    "span": (s_char, e_char),
                    "article": ev.get("article", ""),
                })

            # Record chunks info
            chunks_summary = []
            for ch in chunks:
                item = {
                    "rank": ch.get("rank"),
                    "chunk_id": ch.get("chunk_id"),
                    "doc_part": ch.get("doc_part"),
                    "article": ch.get("article"),
                    "pdf_page": ch.get("start_page_pdf"),
                    "similarity": ch.get("similarity"),
                }
                if mode == "hybrid":
                    item["rrf_score"] = ch.get("rrf_score")
                    item["dense_rank"] = ch.get("dense_rank")
                    item["dense_score"] = ch.get("dense_score")
                    item["bm25_rank"] = ch.get("bm25_rank")
                    item["bm25_score"] = ch.get("bm25_score")
                chunks_summary.append(item)

            if not is_grounded:
                out_of_scope_cases.append({
                    "case_id": cid,
                    "question": question,
                    "latency_ms": round(elapsed_ms, 2),
                    "top_1_chunk": chunks[0]["chunk_id"] if chunks else "",
                    "top_1_score": chunks[0].get("similarity") if mode == "dense" else chunks[0].get("rrf_score"),
                    "chunks": chunks_summary[:5],
                })
                continue

            total_ev = len(evidence_spans)
            ev_cov_at_k: Dict[int, List[float]] = {1: [], 3: [], 5: [], 10: []}
            first_hit_rank: Optional[int] = None

            for k in [1, 3, 5, 10]:
                for ev in evidence_spans:
                    cov = compute_span_intersection_ratio(ev["span"], ev["pdf_page"], chunks, top_k=k)
                    ev_cov_at_k[k].append(cov)

            for r in range(1, len(chunks) + 1):
                any_full = any(
                    compute_span_intersection_ratio(ev["span"], ev["pdf_page"], chunks[:r], top_k=r) >= 0.90
                    for ev in evidence_spans
                )
                if any_full:
                    first_hit_rank = r
                    break

            hit_1 = 1 if any(c >= 0.90 for c in ev_cov_at_k[1]) else 0
            hit_3 = 1 if any(c >= 0.90 for c in ev_cov_at_k[3]) else 0
            hit_5 = 1 if any(c >= 0.90 for c in ev_cov_at_k[5]) else 0
            hit_10 = 1 if any(c >= 0.90 for c in ev_cov_at_k[10]) else 0
            partial_hit_10 = 1 if any(c >= 0.10 for c in ev_cov_at_k[10]) else 0
            all_cov_10 = 1 if all(c >= 0.90 for c in ev_cov_at_k[10]) else 0
            mrr_10 = round(1.0 / first_hit_rank, 4) if first_hit_rank is not None else 0.0

            mean_cov_3 = round(sum(ev_cov_at_k[3]) / total_ev, 4) if total_ev else 0.0
            mean_cov_5 = round(sum(ev_cov_at_k[5]) / total_ev, 4) if total_ev else 0.0
            mean_cov_10 = round(sum(ev_cov_at_k[10]) / total_ev, 4) if total_ev else 0.0

            grounded_cases.append({
                "case_id": cid,
                "question": question,
                "category": category,
                "latency_ms": round(elapsed_ms, 2),
                "expected_ev_count": total_ev,
                "first_hit_rank": first_hit_rank,
                "mrr_10": mrr_10,
                "hit_1": hit_1,
                "hit_3": hit_3,
                "hit_5": hit_5,
                "hit_10": hit_10,
                "partial_hit_10": partial_hit_10,
                "all_cov_10": all_cov_10,
                "mean_cov_3": mean_cov_3,
                "mean_cov_5": mean_cov_5,
                "mean_cov_10": mean_cov_10,
                "ev_cov_at_10": ev_cov_at_k[10],
                "retrieved_chunks": chunks_summary,
            })

        # Calculate metrics for mode
        n_grounded = len(grounded_cases)
        metrics = {
            "mode": mode,
            "n_grounded": n_grounded,
            "hit_at_1_ratio": round(sum(c["hit_1"] for c in grounded_cases) / n_grounded, 4),
            "hit_at_3_ratio": round(sum(c["hit_3"] for c in grounded_cases) / n_grounded, 4),
            "hit_at_5_ratio": round(sum(c["hit_5"] for c in grounded_cases) / n_grounded, 4),
            "hit_at_10_ratio": round(sum(c["hit_10"] for c in grounded_cases) / n_grounded, 4),
            "partial_hit_10_ratio": round(sum(c["partial_hit_10"] for c in grounded_cases) / n_grounded, 4),
            "full_case_coverage_10_ratio": round(sum(c["all_cov_10"] for c in grounded_cases) / n_grounded, 4),
            "mean_mrr_10": round(sum(c["mrr_10"] for c in grounded_cases) / n_grounded, 4),
            "mean_cov_at_3": round(sum(c["mean_cov_3"] for c in grounded_cases) / n_grounded, 4),
            "mean_cov_at_5": round(sum(c["mean_cov_5"] for c in grounded_cases) / n_grounded, 4),
            "mean_cov_at_10": round(sum(c["mean_cov_10"] for c in grounded_cases) / n_grounded, 4),
            "latency_mean_ms": round(statistics.mean(latencies), 2),
            "latency_median_ms": round(statistics.median(latencies), 2),
        }

        all_eval_data[mode] = {
            "metrics": metrics,
            "grounded_cases": grounded_cases,
            "out_of_scope_cases": out_of_scope_cases,
        }

    # In bảng so sánh
    print("\n" + "=" * 90)
    print("BẢNG SO SÁNH HIỆU NĂNG TRUY XUẤT (RETRIEVAL A/B METRICS): DENSE VS HYBRID")
    print("=" * 90)
    print(f"{'Chỉ số (Metric)':<35} | {'Dense (Baseline)':<20} | {'Hybrid (BM25+RRF)':<20} | {'Biến động':<10}")
    print("-" * 90)

    d_m = all_eval_data["dense"]["metrics"]
    h_m = all_eval_data["hybrid"]["metrics"]

    metrics_to_print = [
        ("Hit@1 (>=90% span)", "hit_at_1_ratio"),
        ("Hit@3 (>=90% span)", "hit_at_3_ratio"),
        ("Hit@5 (>=90% span)", "hit_at_5_ratio"),
        ("Hit@10 (>=90% span)", "hit_at_10_ratio"),
        ("Partial Hit@10 (>=10% span)", "partial_hit_10_ratio"),
        ("Full Case Coverage@10", "full_case_coverage_10_ratio"),
        ("MRR@10", "mean_mrr_10"),
        ("Mean Evidence Coverage@3", "mean_cov_at_3"),
        ("Mean Evidence Coverage@5", "mean_cov_at_5"),
        ("Mean Evidence Coverage@10", "mean_cov_at_10"),
        ("Mean Latency (ms)", "latency_mean_ms"),
        ("Median Latency (ms)", "latency_median_ms"),
    ]

    for label, key in metrics_to_print:
        dv = d_m[key]
        hv = h_m[key]
        delta = round(hv - dv, 4)
        sign = "+" if delta > 0 else ""
        print(f"{label:<35} | {dv:<20} | {hv:<20} | {sign}{delta}")

    print("=" * 90)

    # In chi tiết từng ca DEV
    print("\nCHI TIẾT TỪNG CA ĐÁNH GIÁ (DEV_01 -> DEV_10):")
    print(f"{'Case ID':<8} | {'Hit@3 (D vs H)':<15} | {'Cov@5 (D vs H)':<16} | {'Cov@10 (D vs H)':<17} | {'1st Hit Rank (D vs H)'}")
    print("-" * 80)

    d_cases = {c["case_id"]: c for c in all_eval_data["dense"]["grounded_cases"]}
    h_cases = {c["case_id"]: c for c in all_eval_data["hybrid"]["grounded_cases"]}

    for cid in sorted(d_cases.keys()):
        dc = d_cases[cid]
        hc = h_cases[cid]
        h3_str = f"{dc['hit_3']} -> {hc['hit_3']}"
        c5_str = f"{dc['mean_cov_5']:.2f} -> {hc['mean_cov_5']:.2f}"
        c10_str = f"{dc['mean_cov_10']:.2f} -> {hc['mean_cov_10']:.2f}"
        rank_str = f"{dc['first_hit_rank']} -> {hc['first_hit_rank']}"
        print(f"{cid:<8} | {h3_str:<15} | {c5_str:<16} | {c10_str:<17} | {rank_str}")

    out_file = RESULTS_DIR / "RETRIEVAL_AB_COMPARISON_TASK05.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_eval_data, f, ensure_ascii=False, indent=2)
    print(f"\nĐã lưu kết quả chi tiết vào: {out_file}")


if __name__ == "__main__":
    run_retrieval_ab_evaluation()
