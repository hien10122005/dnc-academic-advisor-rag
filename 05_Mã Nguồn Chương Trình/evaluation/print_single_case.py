# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSONL = BASE_DIR / "evaluation" / "results" / "DNC_RAG_AB_DEV10_TASK05.jsonl"
data = [json.loads(line) for line in open(INPUT_JSONL, encoding="utf-8") if line.strip()]

cid = sys.argv[1] if len(sys.argv) > 1 else "DEV_03"
d = [x for x in data if x["case_id"] == cid and x["mode"] == "dense"][0]
h = [x for x in data if x["case_id"] == cid and x["mode"] == "hybrid"][0]

print(f"=== {cid} ===")
print("DENSE STATUS:", d["status"], "| CITATIONS:", [c["article"] for c in d.get("citations", [])])
print("DENSE ANSWER:\n", d["answer"])
print("-" * 50)
print("HYBRID STATUS:", h["status"], "| CITATIONS:", [c["article"] for c in h.get("citations", [])])
print("HYBRID ANSWER:\n", h["answer"])
