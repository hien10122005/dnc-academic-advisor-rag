# -*- coding: utf-8 -*-
"""
backend.cli
Giao diện dòng lệnh (CLI) tra cứu thử nghiệm RAG Học vụ DNC (Quy chế QĐ 580).
Sử dụng:
    python backend/cli.py "Điều kiện học cùng lúc hai chương trình là gì?"
    python backend/cli.py --interactive
"""

import argparse
import json
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.config import load_embedding_model, EMBEDDING_MODEL_CANDIDATE, MODEL_REVISION
from backend.gemini_client import GeminiClient
from backend.rag_engine import RAGEngine
from backend.retrieval import VectorRetriever


def setup_cli_logging():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main():
    setup_cli_logging()
    parser = argparse.ArgumentParser(
        description="DNC Academic Advisor RAG - Giao diện dòng lệnh CLI tra cứu Quy chế QĐ 580"
    )
    parser.add_argument("query", nargs="?", type=str, help="Câu hỏi tra cứu học vụ")
    parser.add_argument("--top-k", type=int, default=5, help="Số đoạn trích xuất tối đa (mặc định: 5)")
    parser.add_argument("--mode", type=str, choices=["dense", "hybrid"], default="dense", help="Chế độ truy xuất: 'dense' (mặc định) hoặc 'hybrid'")
    parser.add_argument("--interactive", action="store_true", help="Chế độ hỏi đáp liên tục qua bàn phím")

    args = parser.parse_args()

    print("=" * 80)
    print("HỆ THỐNG TRỢ LÝ HỌC VỤ DNC - CLI TEST (QUY CHẾ QĐ 580)")
    print("=" * 80)

    # 1. Khởi tạo Retriever & Kiểm tra Tiền trạm (Preflight)
    print("[1/3] Kiểm tra tiền trạm kho tri thức (Preflight Check)...")
    retriever = VectorRetriever()
    try:
        readiness = retriever.check_readiness()
        print(f"      -> Kho tri thức SẴN SÀNG: {readiness.get('collection_name')} ({readiness.get('total_chunks')} chunks).")
    except Exception as err:
        print(f"[-] LỖI TIỀN TRẠM: Kho tri thức chưa sẵn sàng: {err}")
        print("    Vui lòng chạy 'python backend/ingestion.py' trước khi sử dụng.")
        sys.exit(1)

    # 2. Khởi tạo Model & Engine
    print("[2/3] Nạp mô hình nhúng và khởi tạo RAG Engine...")
    model = load_embedding_model(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)
    retriever.model = model
    gemini_client = GeminiClient()
    engine = RAGEngine(retriever=retriever, llm_client=gemini_client)
    print("      -> RAG Engine sẵn sàng.")

    def run_query(user_q: str):
        print("\n" + "-" * 80)
        print(f"CÂU HỎI: {user_q} [Chế độ: {args.mode.upper()}]")
        print("-" * 80)
        res = engine.answer_question(user_q, top_k=args.top_k, mode=args.mode)
        print(f"TRẠNG THÁI NGHIỆP VỤ: {res.status}")
        print(
            f"THỜI GIAN ĐÁP ỨNG:   Tổng {res.timings.get('total_ms', 0):.1f}ms "
            f"(Retrieval: {res.timings.get('retrieval_ms', 0):.1f}ms, LLM: {res.timings.get('llm_generation_ms', res.timings.get('llm_ms', 0)):.1f}ms)"
        )
        print("\nCÂU TRẢ LỜI:")
        print(res.answer)
        print("\nCĂN CỨ & TRÍCH DẪN (CITATIONS):")
        if res.citations:
            for c in res.citations:
                sim_str = f" | Cosine Sim: {c.similarity:.4f}" if c.similarity is not None else " | Sparse Hit"
                print(f"  [{c.source_id}] {c.document_id} - {c.article} (Trang PDF: {c.pdf_page}{sim_str})")
                print(f"        Trích dẫn: {c.quote_snippet}")
        else:
            print("  (Không có căn cứ trích dẫn phù hợp hoặc câu hỏi ngoài phạm vi)")
        print("-" * 80)

    if args.interactive:
        print("\nBắt đầu chế độ tương tác (Gõ 'exit' hoặc 'quit' để thoát):")
        while True:
            try:
                user_input = input("\n[Bạn hỏi]: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit"):
                    break
                run_query(user_input)
            except (KeyboardInterrupt, EOFError):
                break
        print("\nKết thúc phiên làm việc CLI.")
    elif args.query:
        run_query(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
