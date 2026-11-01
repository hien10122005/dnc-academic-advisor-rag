# -*- coding: utf-8 -*-
import json
import statistics
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR / "evaluation" / "results" / "DNC_RAG_AB_DEV10_TASK05.jsonl"
with open(path, "r", encoding="utf-8") as f:
    items = [json.loads(line) for line in f]

for mode in ["dense", "hybrid"]:
    mode_items = [x for x in items if x.get("mode") == mode]
    ret_all = [x["timings"]["retrieval_ms"] for x in mode_items]
    llm_all = [x["timings"]["llm_generation_ms"] for x in mode_items]
    tot_all = [x["timings"]["total_ms"] for x in mode_items]

    # Warm: bỏ ca đầu tiên nếu có startup embedding
    ret_warm = ret_all[1:]
    llm_warm = llm_all[1:]
    tot_warm = tot_all[1:]

    print(f"\n==================== MODE: {mode.upper()} ====================")
    print("--- TOÀN BỘ 10 CA ---")
    print(f"Retrieval: mean={statistics.mean(ret_all):.2f}ms, median={statistics.median(ret_all):.2f}ms, min={min(ret_all):.2f}ms, max={max(ret_all):.2f}ms")
    print(f"LLM:       mean={statistics.mean(llm_all):.2f}ms, median={statistics.median(llm_all):.2f}ms, min={min(llm_all):.2f}ms, max={max(llm_all):.2f}ms")
    print(f"Total:     mean={statistics.mean(tot_all):.2f}ms, median={statistics.median(tot_all):.2f}ms, min={min(tot_all):.2f}ms, max={max(tot_all):.2f}ms")

    print("\n--- WARM (BỎ CA ĐẦU TIÊN) ---")
    print(f"Retrieval: mean={statistics.mean(ret_warm):.2f}ms, median={statistics.median(ret_warm):.2f}ms")
    print(f"LLM:       mean={statistics.mean(llm_warm):.2f}ms, median={statistics.median(llm_warm):.2f}ms")
    print(f"Total:     mean={statistics.mean(tot_warm):.2f}ms, median={statistics.median(tot_warm):.2f}ms")
