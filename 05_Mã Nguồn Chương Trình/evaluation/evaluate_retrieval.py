# -*- coding: utf-8 -*-
"""
evaluation.evaluate_retrieval
Script đánh giá hiệu năng truy xuất baseline (ChromaDB + Vietnamese Bi-Encoder) trên bộ phát triển 10 ca (QĐ 580).
Phiên bản v2.0 - Đánh giá nghiêm ngặt theo Source Span Character Intersection:
- Đối chiếu chính xác khoảng ký tự [start_char, end_char] của bằng chứng trên từng trang gốc.
- Phân biệt rõ rệt:
  + Phủ trọn vẹn (Full Evidence Coverage >= 90% ký tự bằng chứng).
  + Tìm thấy một phần (Partial Match: 10% - 89% ký tự bằng chứng).
  + Không tìm thấy (Coverage < 10%).
- Cho phép nhiều chunk hợp lại để phủ đủ một bằng chứng dài hoặc bằng chứng qua ranh giới chunk.
- Tuyệt đối loại bỏ false positive (cùng Điều nhưng khác khoản/nội dung cho kết quả 0% coverage).
- Tách biệt 9 ca có căn cứ (Grounded) với 1 ca ngoại phạm vi (DEV_10).
- Hỗ trợ đánh giá cả 2 collection (v1 'qd580_baseline_a' và v2 'qd580_baseline_v2') theo CÙNG MỘT TIÊU CHÍ nghiêm ngặt để so sánh công bằng.
"""

from __future__ import annotations
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.config import (
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME,
    COLLECTION_NAME_V1,
    CORPUS_FILE,
    DEV_CASES_FILE,
    EMBEDDING_MODEL_CANDIDATE,
    MANIFEST_FILE,
    MODEL_REVISION,
    RESULTS_DIR,
)
from backend.retrieval import VectorRetriever


def load_corpus_pages() -> List[Dict[str, Any]]:
    """Tải toàn bộ 26 trang gốc đã kiểm chứng."""
    pages = []
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pages.append(json.loads(line.strip()))
    return pages


def find_evidence_span_on_page(pages: List[Dict[str, Any]], pdf_page: int, quote: str) -> Tuple[int, int]:
    """Tìm khoảng ký tự [start_char, end_char] của trích dẫn nguyên văn trên trang PDF.

    Quy tắc định vị bằng chứng nghiêm ngặt (Strict Evidence Locator):
    1. Tìm chính xác (exact match) nguyên văn trước.
    2. Nếu có lệch khoảng trắng hoặc ký tự xuống dòng, phân rã các từ và ghép regex r'\\s+'
       để ánh xạ vị trí ký tự gốc thực sự trong chuỗi content của trang (chữa dứt điểm lỗi đoán offset 0).
    3. Tuyệt đối KHÔNG fallback về [0, len(quote)] hay phỏng đoán offset.
    4. Trả về (-1, -1) nếu không tìm thấy trích dẫn.
    """
    if pdf_page < 1 or pdf_page > len(pages):
        return -1, -1

    p_content = pages[pdf_page - 1]["content"]
    clean_quote = quote.strip()
    if not clean_quote:
        return -1, -1

    # 1. Tìm chính xác
    pos = p_content.find(clean_quote)
    if pos != -1:
        return pos, pos + len(clean_quote)

    # 2. Tìm bằng regex ánh xạ linh hoạt khoảng trắng/xuống dòng về chuỗi gốc
    words = clean_quote.split()
    if not words:
        return -1, -1

    pattern = r"\s+".join(re.escape(w) for w in words)
    matches = list(re.finditer(pattern, p_content))
    if len(matches) >= 1:
        return matches[0].start(), matches[0].end()

    # 3. Không tìm thấy: báo không hợp lệ (-1, -1)
    return -1, -1


def compute_span_intersection_ratio(
    evidence_span: Tuple[int, int],
    evidence_page: int,
    retrieved_chunks: List[Dict[str, Any]],
    top_k: int,
) -> float:
    """
    Tính tỷ lệ phần trăm ký tự của bằng chứng được phủ bởi Top-K chunks.
    Sử dụng thuật toán hợp nhất các khoảng giao nhau (Interval Union).
    """
    q_s, q_e = evidence_span
    if q_s < 0 or q_e <= q_s:
        return 0.0

    target_len = q_e - q_s

    # Thu thập tất cả các khoảng giao nhau trên cùng trang PDF từ Top-K chunks
    intersected_intervals: List[Tuple[int, int]] = []

    for ch in retrieved_chunks[:top_k]:
        spans = ch.get("source_spans", [])
        for sp in spans:
            # Bỏ qua ngữ cảnh bổ sung lặp lại (ví dụ header lặp lại)
            if sp.get("is_added_context"):
                continue

            if sp.get("pdf_page") == evidence_page:
                sp_s = sp.get("page_start_char", 0)
                sp_e = sp.get("page_end_char", 0)

                # Tính giao giữa [q_s, q_e] và [sp_s, sp_e]
                overlap_s = max(q_s, sp_s)
                overlap_e = min(q_e, sp_e)

                if overlap_e > overlap_s:
                    intersected_intervals.append((overlap_s, overlap_e))

    if not intersected_intervals:
        return 0.0

    # Hợp nhất các khoảng giao nhau để tránh đếm trùng do chunk gối đầu (overlap)
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


def verify_negative_rejection(pages: List[Dict[str, Any]]):
    """
    Kiểm thử tự động chứng minh: Cùng Điều nhưng khác Khoản thì KHÔNG ĐƯỢC tính là khớp.
    Ví dụ: Lấy evidence của Điều 11 khoản 2 (song bằng), đối chiếu với chunk của Điều 11 khoản 1.
    """
    print("\n[Kiểm thử Tiêu chuẩn Phủ định (Negative Rejection)]")
    # Evidence Điều 11 khoản 2 (trang 11 [421:960])
    ev_span = (421, 960)
    ev_page = 11

    # Giả lập chunk của Điều 11 khoản 1 (trang 11 [275:420])
    dummy_chunk_khac_khoan = {
        "chunk_id": "dummy_d11_k1",
        "doc_part": "regulation",
        "article": "Điều 11. Học cùng lúc hai chương trình",
        "source_spans": [{
            "pdf_page": 11,
            "page_start_char": 275,
            "page_end_char": 420,
            "is_added_context": False,
        }]
    }

    cov = compute_span_intersection_ratio(ev_span, ev_page, [dummy_chunk_khac_khoan], top_k=1)
    assert cov == 0.0, f"LỖI: Chunk khác khoản cùng Điều bị chấm nhầm cov={cov} > 0!"
    print("-> XÁC NHẬN: Cùng Điều nhưng khác khoản có độ phủ chính xác = 0.0% (Loại bỏ triệt để False Positive).")


def evaluate_collection(
    collection_name: str,
    dev_cases: List[Dict[str, Any]],
    pages: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Chạy đánh giá truy xuất trên một collection cụ thể."""
    print(f"\nKhởi tạo VectorRetriever cho collection '{collection_name}'...")
    t_load_start = time.perf_counter()
    retriever = VectorRetriever(
        persist_dir=str(CHROMA_PERSIST_DIR),
        collection_name=collection_name,
        model_name=EMBEDDING_MODEL_CANDIDATE,
    )
    _ = retriever.model
    t_load_model = time.perf_counter() - t_load_start

    grounded_eval_results: List[Dict[str, Any]] = []
    out_of_scope_results: List[Dict[str, Any]] = []
    top_k_records: List[Dict[str, Any]] = []
    query_latencies: List[float] = []

    for case in dev_cases:
        cid = case.get("id") or case.get("case_id", "UNKNOWN")
        question = case["question"]
        category = case.get("category", "")
        query_to_use = case.get("retrieval_query", "").strip() or question.strip()
        expected_evidences = case.get("evidence") or case.get("expected_evidence", [])
        is_grounded = category != "NGOAI_PHAM_VI_THIEU_CAN_CU" and len(expected_evidences) > 0

        # Đo thời gian truy xuất
        t0 = time.perf_counter()
        retrieved_chunks = retriever.retrieve(query_to_use, top_k=10)
        query_time_ms = (time.perf_counter() - t0) * 1000.0
        query_latencies.append(query_time_ms)

        # Chuẩn bị spans của từng evidence item
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

        # Ghi nhận thông tin top 10 chunks
        chunks_detail = []
        for ch in retrieved_chunks:
            chunks_detail.append({
                "rank": ch["rank"],
                "chunk_id": ch["chunk_id"],
                "distance": ch["distance"],
                "similarity": ch["similarity"],
                "doc_part": ch["doc_part"],
                "chapter": ch["chapter"],
                "article": ch["article"],
                "start_page_pdf": ch["start_page_pdf"],
                "end_page_pdf": ch["end_page_pdf"],
                "is_table": ch["is_table"],
                "token_count": ch.get("token_count", 0),
                "content_preview": ch["content"][:200].replace("\n", " ") + "...",
            })

        top_k_records.append({
            "case_id": cid,
            "question": question,
            "query_used": query_to_use,
            "grounded": is_grounded,
            "retrieval_time_ms": round(query_time_ms, 2),
            "expected_evidence_count": len(expected_evidences),
            "retrieved_chunks": chunks_detail,
        })

        if not is_grounded:
            max_sim = chunks_detail[0]["similarity"] if chunks_detail else 0.0
            out_of_scope_results.append({
                "case_id": cid,
                "question": question,
                "max_similarity": max_sim,
                "top_1_chunk": chunks_detail[0]["chunk_id"] if chunks_detail else "",
                "latency_ms": round(query_time_ms, 2),
            })
            continue

        # Đánh giá độ phủ bằng chứng chính xác theo từng mốc K
        total_ev = len(evidence_spans)
        ev_cov_at_k: Dict[int, List[float]] = {1: [], 3: [], 5: [], 10: []}
        first_hit_rank: Optional[int] = None

        for k in [1, 3, 5, 10]:
            for ev in evidence_spans:
                cov = compute_span_intersection_ratio(ev["span"], ev["pdf_page"], retrieved_chunks, top_k=k)
                ev_cov_at_k[k].append(cov)

        # Xác định thứ hạng chunk đầu tiên đạt tiêu chuẩn Full Coverage (>= 90%)
        for r in range(1, len(retrieved_chunks) + 1):
            any_full = any(
                compute_span_intersection_ratio(ev["span"], ev["pdf_page"], retrieved_chunks[:r], top_k=r) >= 0.90
                for ev in evidence_spans
            )
            if any_full:
                first_hit_rank = r
                break

        # Hit@K: Có ít nhất một bằng chứng đạt Full Coverage (>= 90%)
        hit_1 = 1 if any(c >= 0.90 for c in ev_cov_at_k[1]) else 0
        hit_3 = 1 if any(c >= 0.90 for c in ev_cov_at_k[3]) else 0
        hit_5 = 1 if any(c >= 0.90 for c in ev_cov_at_k[5]) else 0
        hit_10 = 1 if any(c >= 0.90 for c in ev_cov_at_k[10]) else 0

        # Partial Hit@K: Có ít nhất một bằng chứng được tìm thấy một phần (>= 10%)
        partial_hit_10 = 1 if any(c >= 0.10 for c in ev_cov_at_k[10]) else 0

        # Full Case Coverage@K: TẤT CẢ các bằng chứng đều đạt Full Coverage (>= 90%)
        all_cov_10 = 1 if all(c >= 0.90 for c in ev_cov_at_k[10]) else 0

        mrr_10 = round(1.0 / first_hit_rank, 4) if first_hit_rank is not None else 0.0

        mean_cov_3 = round(sum(ev_cov_at_k[3]) / total_ev, 4) if total_ev else 0.0
        mean_cov_5 = round(sum(ev_cov_at_k[5]) / total_ev, 4) if total_ev else 0.0
        mean_cov_10 = round(sum(ev_cov_at_k[10]) / total_ev, 4) if total_ev else 0.0

        case_res = {
            "case_id": cid,
            "question": question,
            "query_used": query_to_use,
            "total_evidence": total_ev,
            "first_hit_rank": first_hit_rank,
            "hit@1": hit_1,
            "hit@3": hit_3,
            "hit@5": hit_5,
            "hit@10": hit_10,
            "partial_hit@10": partial_hit_10,
            "all_evidence_covered@10": all_cov_10,
            "mrr@10": mrr_10,
            "evidence_coverage@3": mean_cov_3,
            "evidence_coverage@5": mean_cov_5,
            "evidence_coverage@10": mean_cov_10,
            "individual_coverage_ratios@10": ev_cov_at_k[10],
            "latency_ms": round(query_time_ms, 2),
        }
        grounded_eval_results.append(case_res)

    num_grounded = len(grounded_eval_results)
    hit_rate_1 = sum(c["hit@1"] for c in grounded_eval_results) / num_grounded if num_grounded else 0.0
    hit_rate_3 = sum(c["hit@3"] for c in grounded_eval_results) / num_grounded if num_grounded else 0.0
    hit_rate_5 = sum(c["hit@5"] for c in grounded_eval_results) / num_grounded if num_grounded else 0.0
    hit_rate_10 = sum(c["hit@10"] for c in grounded_eval_results) / num_grounded if num_grounded else 0.0
    mean_mrr_10 = sum(c["mrr@10"] for c in grounded_eval_results) / num_grounded if num_grounded else 0.0
    full_case_cov_10 = sum(c["all_evidence_covered@10"] for c in grounded_eval_results) / num_grounded if num_grounded else 0.0
    mean_cov_10 = sum(c["evidence_coverage@10"] for c in grounded_eval_results) / num_grounded if num_grounded else 0.0

    return {
        "collection_name": collection_name,
        "total_chunks": retriever.collection.count(),
        "num_grounded": num_grounded,
        "num_out_of_scope": len(out_of_scope_results),
        "hit_rate@1": round(hit_rate_1, 4),
        "hit_rate@3": round(hit_rate_3, 4),
        "hit_rate@5": round(hit_rate_5, 4),
        "hit_rate@10": round(hit_rate_10, 4),
        "mrr@10": round(mean_mrr_10, 4),
        "full_case_coverage_rate@10": round(full_case_cov_10, 4),
        "mean_evidence_coverage@10": round(mean_cov_10, 4),
        "mean_latency_ms": round(statistics.mean(query_latencies), 2) if query_latencies else 0.0,
        "median_latency_ms": round(statistics.median(query_latencies), 2) if query_latencies else 0.0,
        "load_model_time_s": round(t_load_model, 2),
        "grounded_detail": grounded_eval_results,
        "out_of_scope_detail": out_of_scope_results,
        "top_k_records": top_k_records,
    }


def run_evaluation():
    print("=" * 80)
    print("BẮT ĐẦU ĐÁNH GIÁ TRUY XUẤT NGHIÊM NGẶT (STRICT SPAN INTERSECTION)")
    print("=" * 80)

    pages = load_corpus_pages()
    print(f"Đã đọc {len(pages)} trang PDF.")

    verify_negative_rejection(pages)

    dev_cases = []
    eval_dev_file = BASE_DIR / "evaluation" / "DEV_10_CAU_QD580.jsonl"
    if not eval_dev_file.exists():
        eval_dev_file = DEV_CASES_FILE

    with open(eval_dev_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                dev_cases.append(json.loads(line.strip()))

    print(f"Đã nạp {len(dev_cases)} ca kiểm thử.")

    # 1. Đánh giá collection v2 mới
    print("\n>>> ĐÁNH GIÁ COLLECTION MỚI (v2):", COLLECTION_NAME)
    res_v2 = evaluate_collection(COLLECTION_NAME, dev_cases, pages)

    # 2. Đánh giá collection v1 cũ (nếu có) dưới CÙNG TIÊU CHÍ để so sánh công bằng
    res_v1 = None
    try:
        print("\n>>> ĐÁNH GIÁ COLLECTION CŨ (v1):", COLLECTION_NAME_V1)
        res_v1 = evaluate_collection(COLLECTION_NAME_V1, dev_cases, pages)
    except Exception as e:
        print(f"Không thể đánh giá collection v1 (bỏ qua): {e}")

    # 3. Xuất kết quả chi tiết
    os.makedirs(RESULTS_DIR, exist_ok=True)

    top_k_path = RESULTS_DIR / "top_k_results.jsonl"
    with open(top_k_path, "w", encoding="utf-8") as f:
        for r in res_v2["top_k_records"]:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\n-> Đã lưu Top-K chi tiết tại: {top_k_path}")

    summary_metrics = {
        "evaluation_name": "QD580_STRICT_EVALUATION_V2",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model_id": EMBEDDING_MODEL_CANDIDATE,
        "model_revision": MODEL_REVISION,
        "collection_v2": res_v2,
        "collection_v1_re_evaluated": res_v1,
    }

    metrics_path = RESULTS_DIR / "retrieval_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(summary_metrics, f, ensure_ascii=False, indent=2)
    print(f"-> Đã lưu chỉ số định lượng tại: {metrics_path}")

    # 4. In bảng tổng kết
    print("\n" + "=" * 80)
    print("BẢNG TỔNG KẾT ĐÁNH GIÁ TRUY XUẤT (TIÊU CHÍ BẢO TOÀN NGUỒN NGHIÊM NGẶT)")
    print("=" * 80)
    print(f"{'Chỉ số':<35} | {'Bản cũ (v1) cùng tiêu chí':<25} | {'Bản mới (v2)':<20}")
    print("-" * 80)
    v1_hit1 = f"{res_v1['hit_rate@1']*100:.1f}%" if res_v1 else "N/A"
    v1_hit3 = f"{res_v1['hit_rate@3']*100:.1f}%" if res_v1 else "N/A"
    v1_hit5 = f"{res_v1['hit_rate@5']*100:.1f}%" if res_v1 else "N/A"
    v1_hit10 = f"{res_v1['hit_rate@10']*100:.1f}%" if res_v1 else "N/A"
    v1_mrr = f"{res_v1['mrr@10']:.4f}" if res_v1 else "N/A"
    v1_cov = f"{res_v1['mean_evidence_coverage@10']*100:.1f}%" if res_v1 else "N/A"
    v1_full = f"{res_v1['full_case_coverage_rate@10']*100:.1f}%" if res_v1 else "N/A"

    print(f"{'Hit Rate@1 (Full Coverage >=90%)':<35} | {v1_hit1:<25} | {res_v2['hit_rate@1']*100:.1f}%")
    print(f"{'Hit Rate@3 (Full Coverage >=90%)':<35} | {v1_hit3:<25} | {res_v2['hit_rate@3']*100:.1f}%")
    print(f"{'Hit Rate@5 (Full Coverage >=90%)':<35} | {v1_hit5:<25} | {res_v2['hit_rate@5']*100:.1f}%")
    print(f"{'Hit Rate@10 (Full Coverage >=90%)':<35} | {v1_hit10:<25} | {res_v2['hit_rate@10']*100:.1f}%")
    print(f"{'Mean Reciprocal Rank (MRR@10)':<35} | {v1_mrr:<25} | {res_v2['mrr@10']:.4f}")
    print(f"{'Độ phủ bằng chứng trung bình@10':<35} | {v1_cov:<25} | {res_v2['mean_evidence_coverage@10']*100:.1f}%")
    print(f"{'Tỷ lệ phủ đủ tất cả bằng chứng@10':<35} | {v1_full:<25} | {res_v2['full_case_coverage_rate@10']*100:.1f}%")
    print(f"{'Độ trễ trung bình truy vấn':<35} | {res_v1['mean_latency_ms'] if res_v1 else 0:.1f} ms{'':<20} | {res_v2['mean_latency_ms']:.1f} ms")
    print("=" * 80)


if __name__ == "__main__":
    run_evaluation()
