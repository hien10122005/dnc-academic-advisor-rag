# -*- coding: utf-8 -*-
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSONL = BASE_DIR / "evaluation" / "results" / "DNC_RAG_AB_DEV10_TASK05.jsonl"

data = [json.loads(line) for line in open(INPUT_JSONL, encoding="utf-8") if line.strip()]

for c in [f"DEV_0{i}" for i in range(1, 10)] + ["DEV_10"]:
    d = [x for x in data if x["case_id"] == c and x["mode"] == "dense"][0]
    h = [x for x in data if x["case_id"] == c and x["mode"] == "hybrid"][0]
    print(f"\n==================== {c} ====================")
    print(f"QUESTION: {d['question']}")
    print(f"[DENSE] Status: {d['status']} | Citations: {d['sources_cited']}/{d['sources_considered']}")
    print(f"Cited Articles: {[x['article'] for x in d.get('citations', [])]}")
    print(f"Answer: {d['answer']}\n")
    print(f"[HYBRID] Status: {h['status']} | Citations: {h['sources_cited']}/{h['sources_considered']}")
    print(f"Cited Articles: {[x['article'] for x in h.get('citations', [])]}")
    print(f"Answer: {h['answer']}")
