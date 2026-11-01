# -*- coding: utf-8 -*-
"""
backend.chunking
Module Chunking cấu trúc và bảo toàn nguồn gốc - QĐ 580/QĐ-ĐHNCT (Phiên bản v2.0)
Nâng cấp toàn diện:
- Nhận biết Tokenizer thực tế của mô hình 'bkai-foundation-models/vietnamese-bi-encoder' (revision 84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0).
- Giới hạn cứng: 100% chunks có total_tokens <= 256 (ngưỡng an toàn MAX_INPUT_TOKENS = 240).
- Lưu trữ chính xác source_spans (pdf_page, printed_page, page_start_char, page_end_char, chunk_start_char, chunk_end_char).
- Quy ước offset rõ ràng: start_char bao gồm, end_char không bao gồm, tính trên chuỗi content của từng trang.
- Phần overlap lưu đúng nguồn gốc trang phát sinh và đánh dấu is_overlap = True.
- Bảng biểu lớn (> 240 tokens) được chia theo hàng có lặp lại tiêu đề, đánh dấu is_added_context = True và dẫn về nguồn gốc.
- Bảo toàn trọn vẹn 100% nội dung (điều kiện, chế tài, ngoại lệ, bảng điểm).
"""

from __future__ import annotations
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from transformers import AutoTokenizer

from backend.config import (
    CHUNKS_FILE,
    CHUNK_VERSION,
    CORPUS_FILE,
    EMBEDDING_MODEL_CANDIDATE,
    MANIFEST_FILE,
    MAX_INPUT_TOKENS,
    MODEL_REVISION,
    ORIGINAL_PDF_FILE,
    load_tokenizer,
)


def compute_sha256(filepath: Path) -> str:
    """Tính mã băm SHA-256 của tệp tin."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def slice_with_offsets(full_text: str, s: int, e: int) -> Tuple[str, int, int]:
    """Cắt chuỗi từ s đến e và điều chỉnh offset theo lstrip / rstrip để bảo đảm 100% khớp chuỗi."""
    sub = full_text[s:e]
    if not sub.strip():
        return "", s, s
    leading = len(sub) - len(sub.lstrip())
    trailing = len(sub) - len(sub.rstrip())
    new_s = s + leading
    new_e = e - trailing
    return full_text[new_s:new_e], new_s, new_e


class SourceSpan:
    """Định danh vị trí nguồn chính xác cho từng phân đoạn văn bản."""

    def __init__(
        self,
        pdf_page: int,
        printed_page: Optional[int],
        page_start_char: int,
        page_end_char: int,
        chunk_start_char: int,
        chunk_end_char: int,
        is_added_context: bool = False,
        is_overlap: bool = False,
    ):
        self.pdf_page = pdf_page
        self.printed_page = printed_page
        self.page_start_char = page_start_char
        self.page_end_char = page_end_char
        self.chunk_start_char = chunk_start_char
        self.chunk_end_char = chunk_end_char
        self.is_added_context = is_added_context
        self.is_overlap = is_overlap

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pdf_page": self.pdf_page,
            "printed_page": self.printed_page,
            "page_start_char": self.page_start_char,
            "page_end_char": self.page_end_char,
            "chunk_start_char": self.chunk_start_char,
            "chunk_end_char": self.chunk_end_char,
            "is_added_context": self.is_added_context,
            "is_overlap": self.is_overlap,
        }


def validate_corpus(corpus_path: Path, pdf_path: Optional[Path] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Đọc và xác thực tính liêm chính của corpus đầu vào QD580_PAGES.jsonl."""
    if not corpus_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp corpus: {corpus_path}")

    pages = []
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            pages.append(json.loads(line_str))

    if len(pages) != 26:
        raise ValueError(f"Corpus không hợp lệ: Yêu cầu đủ 26 trang, thực tế nhận được {len(pages)} trang.")

    seen_pages = set()
    for p in pages:
        pno = p.get("pdf_page")
        if pno is None or pno in seen_pages or not (1 <= pno <= 26):
            raise ValueError(f"Trang PDF không hợp lệ hoặc bị trùng: {pno}")
        seen_pages.add(pno)

        if not p.get("content") or len(p["content"].strip()) == 0:
            raise ValueError(f"Nội dung trang PDF {pno} bị rỗng!")

        if p.get("source_verified") is not True:
            raise ValueError(f"Trang PDF {pno} chưa được kiểm chứng (source_verified != True)!")

    pages.sort(key=lambda x: x["pdf_page"])
    corpus_hash = compute_sha256(corpus_path)
    pdf_hash = compute_sha256(pdf_path) if pdf_path and pdf_path.exists() else None

    meta = {
        "document_id": "QD580_DHNCT_2024",
        "source_file": "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
        "source_pdf_sha256": pdf_hash,
        "corpus_pages_sha256": corpus_hash,
        "total_pages": len(pages),
        "status": "VALIDATED",
    }
    return pages, meta


class TextSpan:
    def __init__(self, text: str, pdf_page: int, printed_page: Optional[int], page_start_char: int, page_end_char: int):
        self.text = text
        self.pdf_page = pdf_page
        self.printed_page = printed_page
        self.page_start_char = page_start_char
        self.page_end_char = page_end_char


def get_article_boundaries(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Phân định ranh giới 36 điều khoản (4 Quyết định ban hành, 32 Quy chế) trên 26 trang."""
    articles = []

    # Page 1: Quyết định ban hành (doc_part = 'decision')
    p1 = pages[0]
    p1_content = p1["content"]
    d1_m = re.search(r'\n(Điều 1\.\s*[^\n]*)', p1_content)
    d2_m = re.search(r'\n(Điều 2\.\s*[^\n]*)', p1_content)
    d3_m = re.search(r'\n(Điều 3\.\s*[^\n]*)', p1_content)

    t, s, e = slice_with_offsets(p1_content, 0, d1_m.start())
    articles.append({
        "doc_part": "decision",
        "chapter": "Quyết định số 580/QĐ-ĐHNCT: Căn cứ ban hành",
        "article_title": "Căn cứ pháp lý ban hành QĐ 580",
        "article_num": 0,
        "spans": [TextSpan(t, 1, None, s, e)],
    })

    t, s, e = slice_with_offsets(p1_content, d1_m.start(), d2_m.start())
    articles.append({
        "doc_part": "decision",
        "chapter": "Quyết định số 580/QĐ-ĐHNCT",
        "article_title": "Điều 1. Ban hành kèm theo quyết định này Quy chế tổ chức đào tạo trình độ đại học",
        "article_num": 1,
        "spans": [TextSpan(t, 1, None, s, e)],
    })

    t, s, e = slice_with_offsets(p1_content, d2_m.start(), d3_m.start())
    articles.append({
        "doc_part": "decision",
        "chapter": "Quyết định số 580/QĐ-ĐHNCT",
        "article_title": "Điều 2. Quyết định này có hiệu lực kể từ ngày ký",
        "article_num": 2,
        "spans": [TextSpan(t, 1, None, s, e)],
    })

    t, s, e = slice_with_offsets(p1_content, d3_m.start(), len(p1_content))
    articles.append({
        "doc_part": "decision",
        "chapter": "Quyết định số 580/QĐ-ĐHNCT",
        "article_title": "Điều 3. Trách nhiệm thi hành quyết định",
        "article_num": 3,
        "spans": [TextSpan(t, 1, None, s, e)],
    })

    # Pages 2-26: Quy chế đào tạo (doc_part = 'regulation')
    art_matches = []
    chapter_map = {
        1: "Chương I - NHỮNG QUY ĐỊNH CHUNG",
        5: "Chương II - TỔ CHỨC ĐÀO TẠO",
        17: "Chương III - ĐÁNH GIÁ KẾT QUẢ HỌC TẬP",
        23: "Chương IV - XÉT VÀ CÔNG NHẬN TỐT NGHIỆP",
        28: "Chương V - CÁC ĐIỀU KHOẢN KHÁC",
    }

    for p in pages[1:]:
        pno = p["pdf_page"]
        prno = p["printed_page"]
        c = p["content"]
        for m in re.finditer(r'(?:^|\n)(Điều\s+(\d+)\.\s*([^\n]*))', c):
            art_num = int(m.group(2))
            title = f"Điều {art_num}. {m.group(3).strip()}"
            art_matches.append({
                "pdf_page": pno,
                "printed_page": prno,
                "start_char": m.start() if m.group(0).startswith('Điều') else m.start() + 1,
                "art_num": art_num,
                "title": title,
            })

    cur_chap = "Chương I - NHỮNG QUY ĐỊNH CHUNG"
    for idx, am in enumerate(art_matches):
        art_num = am["art_num"]
        if art_num in chapter_map:
            cur_chap = chapter_map[art_num]

        art_title = am["title"]
        start_p = am["pdf_page"]
        start_c = am["start_char"]

        if idx + 1 < len(art_matches):
            next_am = art_matches[idx + 1]
            end_p = next_am["pdf_page"]
            end_c = next_am["start_char"]
        else:
            end_p = 26
            end_c = len(pages[25]["content"])

        spans = []
        for p_idx in range(start_p, end_p + 1):
            p_obj = pages[p_idx - 1]
            p_content = p_obj["content"]
            pr_no = p_obj["printed_page"]

            p_s = start_c if p_idx == start_p else 0
            p_e = end_c if p_idx == end_p else len(p_content)

            t, s, e = slice_with_offsets(p_content, p_s, p_e)
            if t:
                spans.append(TextSpan(t, p_idx, pr_no, s, e))

        articles.append({
            "doc_part": "regulation",
            "chapter": cur_chap,
            "article_title": art_title,
            "article_num": art_num,
            "spans": spans,
        })

    return articles


def extract_atomic_blocks(article_spans: List[TextSpan], pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Phân tách các đoạn văn bản của điều khoản thành các khối nguyên tử (Atomic Blocks)."""
    blocks = []

    for span in article_spans:
        pno = span.pdf_page
        prno = span.printed_page
        p_content = pages[pno - 1]["content"]
        s_base = span.page_start_char
        text = span.text

        lines = text.split('\n')
        cur_offset = s_base

        cur_text_lines = []
        cur_text_start = None
        cur_table_lines = []
        cur_table_start = None

        for line in lines:
            line_len = len(line)
            is_tbl_line = line.strip().startswith('|')

            if is_tbl_line:
                if cur_text_lines:
                    t_clean, s_off, e_off = slice_with_offsets(p_content, cur_text_start, cur_offset - 1)
                    if t_clean:
                        blocks.append({
                            "text": t_clean, "pdf_page": pno, "printed_page": prno,
                            "page_start_char": s_off, "page_end_char": e_off, "is_table": False
                        })
                    cur_text_lines = []
                    cur_text_start = None

                if cur_table_start is None:
                    cur_table_start = cur_offset
                cur_table_lines.append(line)
            else:
                if cur_table_lines:
                    tbl_clean, s_off, e_off = slice_with_offsets(p_content, cur_table_start, cur_offset - 1)
                    if tbl_clean:
                        blocks.append({
                            "text": tbl_clean, "pdf_page": pno, "printed_page": prno,
                            "page_start_char": s_off, "page_end_char": e_off, "is_table": True
                        })
                    cur_table_lines = []
                    cur_table_start = None

                if cur_text_start is None:
                    cur_text_start = cur_offset
                cur_text_lines.append(line)

            cur_offset += line_len + 1

        if cur_table_lines:
            tbl_clean, s_off, e_off = slice_with_offsets(p_content, cur_table_start, cur_offset - 1)
            if tbl_clean:
                blocks.append({
                    "text": tbl_clean, "pdf_page": pno, "printed_page": prno,
                    "page_start_char": s_off, "page_end_char": e_off, "is_table": True
                })
        if cur_text_lines:
            t_clean, s_off, e_off = slice_with_offsets(p_content, cur_text_start, cur_offset - 1)
            if t_clean:
                blocks.append({
                    "text": t_clean, "pdf_page": pno, "printed_page": prno,
                    "page_start_char": s_off, "page_end_char": e_off, "is_table": False
                })

    subdivided_blocks = []
    for b in blocks:
        if b["is_table"]:
            subdivided_blocks.append(b)
            continue

        pno = b["pdf_page"]
        prno = b["printed_page"]
        b_text = b["text"]
        b_start = b["page_start_char"]
        p_content = pages[pno - 1]["content"]

        split_pattern = r'(?:\n(?=(?:\d+\.|[a-z]\.|-|Căn cứ|Xét đề nghị)\s)|\n\s*\n)'
        parts = []
        last_idx = 0
        for m in re.finditer(split_pattern, b_text):
            parts.append((last_idx, m.start()))
            last_idx = m.end()
        parts.append((last_idx, len(b_text)))

        for s_idx, e_idx in parts:
            if s_idx >= e_idx:
                continue
            sub_s = b_start + s_idx
            sub_e = b_start + e_idx
            t_clean, s_off, e_off = slice_with_offsets(p_content, sub_s, sub_e)
            if t_clean:
                subdivided_blocks.append({
                    "text": t_clean, "pdf_page": pno, "printed_page": prno,
                    "page_start_char": s_off, "page_end_char": e_off, "is_table": False
                })

    return subdivided_blocks


def build_chunks_for_article(
    article: Dict[str, Any],
    pages: List[Dict[str, Any]],
    tokenizer: AutoTokenizer,
    max_tokens: int = MAX_INPUT_TOKENS,
) -> List[Dict[str, Any]]:
    """Tạo các chunk tuân thủ nghiêm ngặt giới hạn token cho một điều khoản."""
    chunks = []
    doc_part = article["doc_part"]
    chapter = article["chapter"]
    article_title = article["article_title"]
    art_num = article["article_num"]

    tag = "QUY CHẾ ĐÀO TẠO" if doc_part == "regulation" else "QUYẾT ĐỊNH BAN HÀNH"
    context_prefix = f"[{tag} | {chapter} | {article_title}]"

    def count_tokens(text: str) -> int:
        return len(tokenizer.encode(text, add_special_tokens=True))

    atomic_blocks = extract_atomic_blocks(article["spans"], pages)
    cur_text_parts = []
    cur_overlap_candidate = None

    def flush_chunk(is_table_chunk: bool = False):
        nonlocal cur_text_parts, cur_overlap_candidate
        if not cur_text_parts:
            return None

        full_content = ""
        source_spans = []
        pages_set = set()

        for idx, (t, pno, prno, ps, pe, is_ov, is_ac) in enumerate(cur_text_parts):
            if idx > 0:
                full_content += "\n\n"
            c_s = len(full_content)
            full_content += t
            c_e = len(full_content)
            pages_set.add(pno)

            source_spans.append(SourceSpan(
                pdf_page=pno,
                printed_page=prno,
                page_start_char=ps,
                page_end_char=pe,
                chunk_start_char=c_s,
                chunk_end_char=c_e,
                is_added_context=is_ac,
                is_overlap=is_ov,
            ))

        embedding_text = f"{context_prefix}\n{full_content}"
        tokens = tokenizer.encode(embedding_text, add_special_tokens=True)
        token_count = len(tokens)

        pdf_pages = sorted(list(pages_set))
        start_p = pdf_pages[0] if pdf_pages else 0
        end_p = pdf_pages[-1] if pdf_pages else 0

        pr_pages = [s.printed_page for s in source_spans if s.printed_page is not None]
        start_pr = pr_pages[0] if pr_pages else None
        end_pr = pr_pages[-1] if pr_pages else None

        c_record = {
            "doc_part": doc_part,
            "chapter": chapter,
            "article": article_title,
            "article_number": art_num,
            "start_page_pdf": start_p,
            "end_page_pdf": end_p,
            "start_page_printed": start_pr,
            "end_page_printed": end_pr,
            "is_table": is_table_chunk,
            "token_count": token_count,
            "char_count": len(full_content),
            "context_prefix": context_prefix,
            "content": full_content,
            "embedding_text": embedding_text,
            "source_spans": [s.to_dict() for s in source_spans],
        }
        chunks.append(c_record)

        non_ov_parts = [p for p in cur_text_parts if not p[5] and not p[6]]
        if non_ov_parts and not is_table_chunk:
            last_part = non_ov_parts[-1]
            if count_tokens(last_part[0]) <= 50:
                cur_overlap_candidate = (last_part[0], last_part[1], last_part[2], last_part[3], last_part[4], True, False)
            else:
                cur_overlap_candidate = None
        else:
            cur_overlap_candidate = None

        cur_text_parts = []
        return c_record

    for b in atomic_blocks:
        if b["is_table"]:
            flush_chunk(is_table_chunk=False)

            t_text = b["text"]
            t_tokens = count_tokens(f"{context_prefix}\n{t_text}")
            if t_tokens <= max_tokens:
                cur_text_parts.append((t_text, b["pdf_page"], b["printed_page"], b["page_start_char"], b["page_end_char"], False, False))
                flush_chunk(is_table_chunk=True)
            else:
                t_lines = t_text.split('\n')
                hdr_lines = t_lines[:2]
                hdr_text = '\n'.join(hdr_lines)
                hdr_len = len(hdr_text)
                data_rows = t_lines[2:]

                hdr_p_s = b["page_start_char"]
                hdr_p_e = hdr_p_s + hdr_len

                for r_idx, row in enumerate(data_rows):
                    is_added = (r_idx > 0)
                    cur_text_parts.append((hdr_text, b["pdf_page"], b["printed_page"], hdr_p_s, hdr_p_e, False, is_added))

                    r_offset = b["text"].find(row)
                    r_ps = b["page_start_char"] + r_offset
                    r_pe = r_ps + len(row)
                    cur_text_parts.append((row, b["pdf_page"], b["printed_page"], r_ps, r_pe, False, False))
                    flush_chunk(is_table_chunk=True)
        else:
            test_parts = list(cur_text_parts)
            if not test_parts and cur_overlap_candidate is not None:
                test_parts.append(cur_overlap_candidate)
            test_parts.append((b["text"], b["pdf_page"], b["printed_page"], b["page_start_char"], b["page_end_char"], False, False))

            test_content = "\n\n".join(tp[0] for tp in test_parts)
            test_tokens = count_tokens(f"{context_prefix}\n{test_content}")

            if test_tokens <= max_tokens:
                if not cur_text_parts and cur_overlap_candidate is not None:
                    cur_text_parts.append(cur_overlap_candidate)
                    cur_overlap_candidate = None
                cur_text_parts.append((b["text"], b["pdf_page"], b["printed_page"], b["page_start_char"], b["page_end_char"], False, False))
            else:
                if cur_text_parts:
                    flush_chunk(is_table_chunk=False)
                if cur_overlap_candidate is not None:
                    cur_text_parts.append(cur_overlap_candidate)
                    cur_overlap_candidate = None
                cur_text_parts.append((b["text"], b["pdf_page"], b["printed_page"], b["page_start_char"], b["page_end_char"], False, False))

    flush_chunk(is_table_chunk=False)
    return chunks


def run_chunking() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Hàm thực thi chính của pipeline chunking."""
    print("=" * 80)
    print("BẮT ĐẦU PIPELINE CHUNKING TOKENIZER-AWARE (QĐ 580 - v2.0)")
    print("=" * 80)

    pages, val_meta = validate_corpus(CORPUS_FILE, ORIGINAL_PDF_FILE)
    print(f"Xác thực nguồn thành công: {len(pages)} trang đã kiểm chứng.")

    print(f"Khởi tạo Tokenizer: {EMBEDDING_MODEL_CANDIDATE} (Revision {MODEL_REVISION})...")
    tokenizer = load_tokenizer(EMBEDDING_MODEL_CANDIDATE, revision=MODEL_REVISION)

    articles = get_article_boundaries(pages)
    print(f"Phân tích thành công {len(articles)} điều khoản quy chế.")

    all_chunks = []
    chunk_counter = 1

    for a in articles:
        art_chunks = build_chunks_for_article(a, pages, tokenizer, max_tokens=MAX_INPUT_TOKENS)
        for c in art_chunks:
            # Tạo deterministic ID
            doc_p = c["doc_part"][:3]
            art_n = c["article_number"]
            start_p = c["start_page_pdf"]
            content_hash = hashlib.sha256(f"{c['doc_part']}:{art_n}:{start_p}:{c['content']}".encode('utf-8')).hexdigest()[:8]
            cid = f"qd580_v2_c{chunk_counter:03d}_{doc_p}_d{art_n:02d}_p{start_p:02d}_{content_hash}"
            c["chunk_id"] = cid
            c["document_id"] = "QD580_DHNCT_2024"
            c["source_file"] = "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf"
            c["chunk_version"] = CHUNK_VERSION
            c["source_verified"] = True
            all_chunks.append(c)
            chunk_counter += 1

    print(f"Tạo thành công tổng cộng {len(all_chunks)} chunks.")

    # Kiểm tra giới hạn token
    max_tok = max(c["token_count"] for c in all_chunks)
    min_tok = min(c["token_count"] for c in all_chunks)
    avg_tok = sum(c["token_count"] for c in all_chunks) / len(all_chunks)
    print(f"Thống kê Token: Max={max_tok}, Min={min_tok}, Avg={avg_tok:.1f} (Giới hạn cho phép: 256)")
    if max_tok > 256:
        raise ValueError(f"Lỗi: Có chunk vượt quá giới hạn 256 tokens! (Max={max_tok})")

    # Kiểm tra tính khớp nguồn của toàn bộ source_spans
    print("Đối soát 100% source spans với chuỗi văn bản gốc trên từng trang...")
    for idx, c in enumerate(all_chunks):
        for sp in c["source_spans"]:
            pno = sp["pdf_page"]
            p_slice = pages[pno - 1]["content"][sp["page_start_char"]:sp["page_end_char"]]
            c_slice = c["content"][sp["chunk_start_char"]:sp["chunk_end_char"]]
            if p_slice != c_slice:
                raise ValueError(
                    f"Sai lệch nguồn tại chunk #{idx} ({c['chunk_id']}): Trang P{pno} "
                    f"[{sp['page_start_char']}:{sp['page_end_char']}] không khớp chunk [{sp['chunk_start_char']}:{sp['chunk_end_char']}]"
                )

    print("Đối soát nguồn thành công 100%!")

    # Xuất tệp QD580_CHUNKS.jsonl
    os.makedirs(CHUNKS_FILE.parent, exist_ok=True)
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Đã lưu tệp chunks tại: {CHUNKS_FILE}")

    chunks_sha256 = compute_sha256(CHUNKS_FILE)

    # Tính corpus fingerprint
    fingerprint_raw = f"{val_meta['source_pdf_sha256']}:{val_meta['corpus_pages_sha256']}:{chunks_sha256}:{MODEL_REVISION}:{CHUNK_VERSION}"
    corpus_fingerprint = hashlib.sha256(fingerprint_raw.encode('utf-8')).hexdigest()

    manifest_data = {
        "manifest_version": "2.0.0",
        "document_id": "QD580_DHNCT_2024",
        "corpus_fingerprint": corpus_fingerprint,
        "source_pdf_sha256": val_meta["source_pdf_sha256"],
        "corpus_pages_sha256": val_meta["corpus_pages_sha256"],
        "chunks_sha256": chunks_sha256,
        "model_id": EMBEDDING_MODEL_CANDIDATE,
        "model_revision": MODEL_REVISION,
        "chunk_version": CHUNK_VERSION,
        "max_input_tokens": MAX_INPUT_TOKENS,
        "total_pages": len(pages),
        "total_chunks": len(all_chunks),
        "statistics": {
            "token_count": {"max": max_tok, "min": min_tok, "avg": round(avg_tok, 2)},
            "char_count": {
                "max": max(c["char_count"] for c in all_chunks),
                "min": min(c["char_count"] for c in all_chunks),
                "avg": round(sum(c["char_count"] for c in all_chunks) / len(all_chunks), 2),
            },
            "table_chunks_count": sum(1 for c in all_chunks if c["is_table"]),
            "text_chunks_count": sum(1 for c in all_chunks if not c["is_table"]),
            "cross_page_chunks_count": sum(1 for c in all_chunks if c["start_page_pdf"] != c["end_page_pdf"]),
        },
        "chunks": all_chunks,
    }

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"Đã lưu tệp manifest tại: {MANIFEST_FILE}")
    print(f"Corpus Fingerprint SHA-256: {corpus_fingerprint}")
    print("=" * 80)
    return all_chunks, manifest_data


if __name__ == "__main__":
    run_chunking()
