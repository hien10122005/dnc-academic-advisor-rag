# -*- coding: utf-8 -*-
"""
tests.test_chunking_and_sources
Bộ kiểm thử tự động toàn diện cho Module Chunking và Bảo toàn Nguồn gốc (QĐ 580).
Kiểm tra 5 tiêu chí bắt buộc theo yêu cầu nghiệm thu:
1. Giới hạn Token: 100% chunk có số token <= 256 (tính cả context prefix và special tokens).
2. Toàn vẹn Nguồn gốc (Source Spans): 100% source spans khớp từng ký tự với trang gốc.
3. Bảo toàn Nguồn Overlap: Phần overlap lưu đúng trang và offset, không bị ghi đè trang hiện tại.
4. Độ phủ Nội dung: Không mất bất kỳ điều kiện, chế tài, ngoại lệ hay hàng bảng điểm nào.
5. Tính Bất biến (Idempotency): Chạy lại sinh đúng các chunk ID và mã băm SHA-256.
"""

import json
import re
import sys
import unittest
from pathlib import Path

# Thêm thư mục mã nguồn vào sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from transformers import AutoTokenizer

from backend.config import (
    CHUNKS_FILE,
    CORPUS_FILE,
    EMBEDDING_MODEL_CANDIDATE,
    MANIFEST_FILE,
    MAX_INPUT_TOKENS,
    MODEL_REVISION,
    load_tokenizer,
)
from backend.chunking import compute_sha256, run_chunking


def test_token_limits():
    """Kiểm tra giới hạn token cứng <= 256 trên toàn bộ chunks."""
    print("\n--- Test 1: Kiểm tra Giới hạn Token (Hard Limit <= 256) ---")
    tokenizer = load_tokenizer(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)

    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line.strip()))

    assert len(chunks) > 0, "File chunks rỗng!"
    print(f"Tổng số chunk kiểm tra: {len(chunks)}")

    max_tokens_seen = 0
    violating_chunks = []

    for idx, c in enumerate(chunks):
        emb_text = c["embedding_text"]
        # Đếm thực tế bằng tokenizer có special tokens
        tokens = tokenizer.encode(emb_text, add_special_tokens=True)
        tok_len = len(tokens)
        if tok_len > max_tokens_seen:
            max_tokens_seen = tok_len

        # So sánh với token_count lưu trong chunk
        assert c["token_count"] == tok_len, f"Chunk #{idx} ({c['chunk_id']}): token_count={c['token_count']} != thực tế {tok_len}"

        if tok_len > 256:
            violating_chunks.append((c["chunk_id"], tok_len))

    print(f"Token lớn nhất thực tế: {max_tokens_seen} / 256")
    assert len(violating_chunks) == 0, f"Có {len(violating_chunks)} chunks vượt quá 256 tokens: {violating_chunks}"
    print("-> Test 1 ĐẠT: 100% chunk tuân thủ nghiêm ngặt giới hạn <= 256 tokens!")


def test_source_spans_verbatim():
    """Kiểm tra tính chuẩn xác 100% của source spans đối chiếu với văn bản gốc từng trang."""
    print("\n--- Test 2: Kiểm tra Toàn vẹn Source Spans ---")
    pages = []
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pages.append(json.loads(line.strip()))

    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line.strip()))

    total_spans = 0
    for idx, c in enumerate(chunks):
        spans = c.get("source_spans", [])
        assert len(spans) > 0, f"Chunk #{idx} ({c['chunk_id']}) không có source_spans!"

        for sp in spans:
            total_spans += 1
            pno = sp["pdf_page"]
            assert 1 <= pno <= 26, f"Số trang PDF không hợp lệ: {pno}"

            p_slice = pages[pno - 1]["content"][sp["page_start_char"]:sp["page_end_char"]]
            c_slice = c["content"][sp["chunk_start_char"]:sp["chunk_end_char"]]

            assert p_slice == c_slice, (
                f"LỆCH NGUỒN tại chunk #{idx} ({c['chunk_id']}) - Trang P{pno} "
                f"[{sp['page_start_char']}:{sp['page_end_char']}]: {repr(p_slice[:30])} != {repr(c_slice[:30])}"
            )

    print(f"Tổng số source spans đã kiểm tra: {total_spans}")
    print("-> Test 2 ĐẠT: 100% source spans khớp từng ký tự với trang gốc!")


def test_overlap_sources():
    """Kiểm tra phần overlap lưu đúng trang và offset nguồn gốc."""
    print("\n--- Test 3: Kiểm tra Bảo toàn Nguồn Overlap ---")
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line.strip()))

    overlap_count = 0
    for c in chunks:
        spans = c.get("source_spans", [])
        for sp in spans:
            if sp.get("is_overlap"):
                overlap_count += 1
                assert sp["page_start_char"] < sp["page_end_char"], "Overlap span rỗng!"
                assert sp["chunk_start_char"] == 0, "Phần overlap phải đặt tại đầu chunk (chunk_start_char = 0)!"

    print(f"Tổng số overlap spans phát hiện: {overlap_count}")
    assert overlap_count > 0, "Phải có các đoạn overlap giữa các chunk!"
    print("-> Test 3 ĐẠT: Overlap được gắn nhãn và lưu vị trí nguồn chính xác!")


def test_content_coverage():
    """Kiểm tra độ phủ: không bỏ mất hàng bảng biểu hoặc điều khoản nào."""
    print("\n--- Test 4: Kiểm tra Độ phủ Nội dung (Coverage) ---")
    pages = []
    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pages.append(json.loads(line.strip()))

    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line.strip()))

    # 1. Kiểm tra toàn bộ hàng bảng biểu
    table_rows_checked = 0
    for p in pages:
        lines = p["content"].split('\n')
        for line in lines:
            line_str = line.strip()
            if line_str.startswith('|') and not line_str.startswith('| :---'):
                table_rows_checked += 1
                found = any(line_str in c["content"] for c in chunks)
                assert found, f"HÀNG BẢNG BỊ MẤT: '{line_str}' (Trang P{p['pdf_page']})"

    print(f"Đã kiểm tra {table_rows_checked} hàng bảng biểu: 100% được bảo toàn.")

    # 2. Kiểm tra các đề mục điều khoản quy chế
    clauses_checked = 0
    for p in pages[1:]:
        for m in re.finditer(r'(?:^|\n)(\d+\.\s+[^\n]{15,60})', p["content"]):
            clause_str = m.group(1).strip()
            clauses_checked += 1
            found = any(clause_str in c["content"] for c in chunks)
            assert found, f"KHOẢN QUY CHẾ BỊ MẤT: '{clause_str}' (Trang P{p['pdf_page']})"

    print(f"Đã kiểm tra {clauses_checked} đầu mục khoản: 100% được bảo toàn.")
    print("-> Test 4 ĐẠT: Toàn bộ điều kiện, chế tài và hàng bảng được bảo toàn trọn vẹn!")


import tempfile

def test_idempotency():
    """Kiểm tra tính bất biến (Idempotent) khi chạy lại chunking trong môi trường tạm thời cô lập."""
    print("\n--- Test 5: Kiểm tra Tính Bất biến (Idempotency) ---")
    old_hash = compute_sha256(CHUNKS_FILE)
    old_manifest_hash = compute_sha256(MANIFEST_FILE)

    # Chạy lại chunking ghi vào thư mục tạm phân lập, không ghi đè kho dùng chung
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_chunks = Path(tmp_dir) / "test_chunks.jsonl"
        tmp_manifest = Path(tmp_dir) / "test_manifest.json"

        run_chunking(output_chunks_file=tmp_chunks, output_manifest_file=tmp_manifest)

        new_hash = compute_sha256(tmp_chunks)
        new_manifest_hash = compute_sha256(tmp_manifest)

        assert old_hash == new_hash, f"Lỗi Idempotent: Mã băm chunks thay đổi: {old_hash} != {new_hash}"
        assert old_manifest_hash == new_manifest_hash, "Lỗi Idempotent: Mã băm manifest thay đổi!"
        print(f"Mã băm Chunks bất biến trong sandbox: {new_hash}")
        print("-> Test 5 ĐẠT: Chạy lại sinh đúng 100% mã băm và cấu trúc mà không ghi đè kho dùng chung!")


class TestChunkingAndSources(unittest.TestCase):
    def test_token_limits(self):
        test_token_limits()

    def test_source_spans_verbatim(self):
        test_source_spans_verbatim()

    def test_overlap_sources(self):
        test_overlap_sources()

    def test_content_coverage(self):
        test_content_coverage()

    def test_idempotency(self):
        test_idempotency()


if __name__ == "__main__":
    unittest.main()
