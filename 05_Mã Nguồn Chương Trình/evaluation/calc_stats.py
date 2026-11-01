# -*- coding: utf-8 -*-
import json
import statistics
from pathlib import Path

path = Path("05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_LIVE_DEV10_R04.jsonl")
with open(path, "r", encoding="utf-8") as f:
    items = [json.loads(line) for line in f]

ret_all = [x["retrieval_ms"] for x in items]
llm_all = [x["llm_generation_ms"] for x in items]
tot_all = [x["total_ms"] for x in items]

ret_warm = ret_all[1:]
llm_warm = llm_all[1:]
tot_warm = tot_all[1:]

print("--- TOÀN BỘ 10 CA ---")
print("Retrieval mean:", round(statistics.mean(ret_all), 3), "median:", round(statistics.median(ret_all), 3))
print("LLM mean:", round(statistics.mean(llm_all), 3), "median:", round(statistics.median(llm_all), 3))
print("Total mean:", round(statistics.mean(tot_all), 3), "median:", round(statistics.median(tot_all), 3))

print("\n--- WARM (BỎ CA ĐẦU TIÊN) ---")
print("Retrieval mean:", round(statistics.mean(ret_warm), 3), "median:", round(statistics.median(ret_warm), 3))
print("LLM mean:", round(statistics.mean(llm_warm), 3), "median:", round(statistics.median(llm_warm), 3))
print("Total mean:", round(statistics.mean(tot_warm), 3), "median:", round(statistics.median(tot_warm), 3))

print("\n--- CHI TIẾT DEV_04, DEV_05, DEV_07 ---")
for x in items:
    if x["id"] in ["DEV_04", "DEV_05", "DEV_07"]:
        print(f"\n==================== {x['id']} ====================")
        print("Expected behavior:", x.get("expected_behavior"))
        print("Status:", x.get("status"))
        print("Mandatory points:")
        for mp in x.get("mandatory_points", []):
            print(f"  * {mp}")
        print("Actual Answer:\n", x.get("answer"))

