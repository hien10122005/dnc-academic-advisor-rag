# -*- coding: utf-8 -*-
"""
evaluation.grade_ab_rubric
Script chấm điểm chi tiết Rubric từng ý bắt buộc (Mandatory Points) và phân tích tính trung thực (Faithfulness)
cho kết quả đánh giá A/B Live (Dense vs Hybrid) của DNC-RAG-TASK-05-R01.
"""

from __future__ import annotations
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
INPUT_JSONL = RESULTS_DIR / "DNC_RAG_AB_DEV10_TASK05.jsonl"


def main():
    if not INPUT_JSONL.exists():
        print(f"File not found: {INPUT_JSONL}")
        return

    records = []
    with open(INPUT_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line.strip()))

    print(f"Tổng số bản ghi Live: {len(records)} (Dense: {sum(1 for r in records if r['mode'] == 'dense')}, Hybrid: {sum(1 for r in records if r['mode'] == 'hybrid')})")

    # Phân nhóm theo ca
    cases = {}
    for r in records:
        cid = r["case_id"]
        if cid not in cases:
            cases[cid] = {}
        cases[cid][r["mode"]] = r

    for cid in sorted(cases.keys()):
        print("\n" + "=" * 90)
        print(f"CHI TIẾT CA ĐÁNH GIÁ: {cid}")
        print("=" * 90)
        c_dense = cases[cid].get("dense")
        c_hybrid = cases[cid].get("hybrid")

        print(f"Câu hỏi: {c_dense['question']}")
        print(f"Ý bắt buộc (Mandatory points):")
        for i, pt in enumerate(c_dense.get("mandatory_points", []), 1):
            print(f"  {i}. {pt}")

        print("\n--- [DENSE MODE] ---")
        print(f"Status: {c_dense['status']} | Citations: {c_dense['sources_cited']}/{c_dense['sources_considered']}")
        print(f"Timings: Retrieval={c_dense['timings'].get('retrieval_ms')}ms | LLM={c_dense['timings'].get('llm_generation_ms')}ms | Total={c_dense['timings'].get('total_ms')}ms")
        print(f"Answer: {c_dense['answer']}")
        print("Cited Sources:")
        for cit in c_dense.get("citations", []):
            print(f"  - [{cit['source_id']}] {cit['article']} (PDF p.{cit['pdf_page']}): {cit['quote_snippet'][:100]}...")

        print("\n--- [HYBRID MODE] ---")
        print(f"Status: {c_hybrid['status']} | Citations: {c_hybrid['sources_cited']}/{c_hybrid['sources_considered']}")
        print(f"Timings: Retrieval={c_hybrid['timings'].get('retrieval_ms')}ms | LLM={c_hybrid['timings'].get('llm_generation_ms')}ms | Total={c_hybrid['timings'].get('total_ms')}ms")
        print(f"Answer: {c_hybrid['answer']}")
        print("Cited Sources:")
        for cit in c_hybrid.get("citations", []):
            print(f"  - [{cit['source_id']}] {cit['article']} (PDF p.{cit['pdf_page']}): {cit['quote_snippet'][:100]}...")


if __name__ == "__main__":
    main()
