# -*- coding: utf-8 -*-
"""
backend.bm25_retriever
Module BM25 Okapi Sparse Search và Reciprocal Rank Fusion (RRF) cho hệ thống DNC RAG.
Đặc tả kỹ thuật (Nhiệm vụ 05 - Chặng B):
1. Tokenizer tiếng Việt chuẩn hóa: NFC, lowercase, tách từ/số, giữ nguyên dấu tiếng Việt và các con số quy chế.
2. BM25 Okapi chuẩn mực: k1=1.5, b=0.75, IDF = ln((N - df + 0.5)/(df + 0.5) + 1.0).
3. Đọc đúng 104 chunks từ QD580_CHUNKS.jsonl trên trường embedding_text (bao gồm context prefix và nội dung).
4. Không trả về zero-score hits (câu hỏi không khớp sparse trả về mảng rỗng).
5. Giải thuật Reciprocal Rank Fusion (RRF): k=60, rank bắt đầu 1, sum(1 / (k + rank)), deduplicate theo chunk_id, tie-break ổn định.
6. Lưu trữ tách bạch dense_rank/score, bm25_rank/score và rrf_score. Không cộng trực tiếp hay giả làm cosine similarity.
7. Cache chỉ mục BM25 theo SHA-256 fingerprint, tiền kiểm tra fail-closed nhất quán với VectorRetriever.
"""

from __future__ import annotations
import hashlib
import json
import math
import os
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from backend.config import CHUNKS_FILE, MANIFEST_FILE
from backend.errors import KnowledgeBaseNotReadyError


def compute_sha256(filepath: Path) -> str:
    """Tính mã băm SHA-256 của tệp tin."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def tokenize_vietnamese(text: str) -> List[str]:
    """
    Tokenizer chuẩn hóa cho văn bản quy chế tiếng Việt:
    - Chuẩn hóa Unicode NFC để tránh phân rã ký tự có dấu.
    - Chuyển chữ thường (lowercase).
    - Tách các từ, số và ký tự chữ cái tiếng Việt có dấu.
    - Giữ lại các con số, số học kỳ, điều khoản, định mức tín chỉ (03, 04, 05, 07, 10, 15, 20, 23, 580...).
    - Tuyệt đối không tạo từ điển đặc chế theo DEV hay Gold standard.
    """
    if not text:
        return []
    normalized = unicodedata.normalize("NFC", text.lower())
    # Tách từ và số Unicode (giữ nguyên tiếng Việt có dấu)
    tokens = re.findall(r"[\w]+", normalized, re.UNICODE)
    return [t for t in tokens if t.strip()]


class BM25OkapiIndex:
    """Chỉ mục BM25 Okapi chạy thuần Python trên 104 chunks quy chế QĐ 580."""

    def __init__(
        self,
        chunks_file_path: Optional[Path] = None,
        manifest_file_path: Optional[Path] = None,
        k1: float = 1.5,
        b: float = 0.75,
    ):
        self.chunks_file_path = Path(chunks_file_path) if chunks_file_path else CHUNKS_FILE
        self.manifest_file_path = Path(manifest_file_path) if manifest_file_path else MANIFEST_FILE
        self.k1 = float(k1)
        self.b = float(b)

        self.corpus_chunks: List[Dict[str, Any]] = []
        self.doc_tokens: List[List[str]] = []
        self.doc_lens: List[int] = []
        self.avgdl: float = 0.0
        self.doc_count: int = 0
        self.df: Counter = Counter()
        self.idf: Dict[str, float] = {}
        self.doc_freqs: List[Counter] = []
        self.chunk_id_to_idx: Dict[str, int] = {}
        self.indexed_fingerprint: Optional[str] = None

        self._build_index()

    def _build_index(self) -> None:
        """Đọc chunks và xây dựng ma trận chỉ mục BM25."""
        if not self.chunks_file_path.exists():
            raise KnowledgeBaseNotReadyError(
                f"Tệp chunks không tồn tại để khởi tạo BM25: {self.chunks_file_path}"
            )

        # 1. Tiền kiểm tra tính toàn vẹn với manifest nếu có
        if self.manifest_file_path.exists():
            try:
                with open(self.manifest_file_path, "r", encoding="utf-8") as mf:
                    m_data = json.load(mf)
                    expected_hash = m_data.get("chunks_sha256")
                    actual_hash = compute_sha256(self.chunks_file_path)
                    if expected_hash and actual_hash != expected_hash:
                        raise KnowledgeBaseNotReadyError(
                            f"Mã băm chunks ({actual_hash}) không khớp manifest ({expected_hash}) khi khởi tạo BM25!"
                        )
            except KnowledgeBaseNotReadyError:
                raise
            except Exception as e:
                raise KnowledgeBaseNotReadyError(f"Lỗi kiểm tra manifest BM25: {e}")

        # 2. Nạp dữ liệu 104 chunks
        chunks = []
        with open(self.chunks_file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if line_str:
                    chunks.append(json.loads(line_str))

        if len(chunks) != 104:
            raise KnowledgeBaseNotReadyError(
                f"Kho tri thức BM25 yêu cầu đúng 104 chunks quy chế QĐ 580 (Thực tế: {len(chunks)} chunks)."
            )

        self.corpus_chunks = chunks
        self.doc_count = len(chunks)
        self.doc_tokens = []
        self.doc_lens = []
        self.doc_freqs = []
        self.df = Counter()
        self.chunk_id_to_idx = {}

        # 3. Phân tích token cho từng tài liệu (sử dụng embedding_text có context prefix)
        for idx, c in enumerate(chunks):
            cid = c.get("chunk_id", f"chunk_{idx}")
            self.chunk_id_to_idx[cid] = idx

            # Dùng embedding_text để bắt cả từ khóa trong tiêu đề điều/chương và thân bài
            raw_text = c.get("embedding_text") or c.get("content", "")
            tokens = tokenize_vietnamese(raw_text)
            self.doc_tokens.append(tokens)
            d_len = len(tokens)
            self.doc_lens.append(d_len)

            tf = Counter(tokens)
            self.doc_freqs.append(tf)

            # Cập nhật Document Frequency (mỗi từ chỉ tính 1 lần / văn bản)
            for term in tf.keys():
                self.df[term] += 1

        self.avgdl = sum(self.doc_lens) / self.doc_count if self.doc_count > 0 else 0.0

        # 4. Tính IDF chuẩn Okapi BM25 (không âm)
        self.idf = {}
        for term, freq in self.df.items():
            # Công thức chuẩn Lucene/Okapi: ln((N - df + 0.5) / (df + 0.5) + 1.0)
            self.idf[term] = math.log((self.doc_count - freq + 0.5) / (freq + 0.5) + 1.0)

        self.indexed_fingerprint = compute_sha256(self.chunks_file_path)

    def search(self, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """
        Tìm kiếm BM25 trên query câu hỏi.
        Chỉ trả về các chunk có điểm BM25 > 0.0 (loại bỏ hoàn toàn zero-score hits).
        """
        clean_q = query.strip() if query else ""
        if not clean_q:
            return []

        q_tokens = tokenize_vietnamese(clean_q)
        if not q_tokens:
            return []

        scores: List[Tuple[int, float]] = []

        # Tính điểm BM25 cho từng tài liệu
        for idx in range(self.doc_count):
            d_len = self.doc_lens[idx]
            d_tf = self.doc_freqs[idx]
            score = 0.0

            for q_term in q_tokens:
                if q_term in d_tf:
                    tf_val = d_tf[q_term]
                    term_idf = self.idf.get(q_term, 0.0)

                    # Công thức Okapi BM25
                    numerator = term_idf * tf_val * (self.k1 + 1.0)
                    denominator = tf_val + self.k1 * (1.0 - self.b + self.b * (d_len / self.avgdl))
                    score += numerator / denominator

            if score > 0.0:
                scores.append((idx, round(score, 4)))

        if not scores:
            return []

        # Sắp xếp giảm dần theo điểm BM25; nếu bằng điểm thì tie-break theo chunk_id
        scores.sort(key=lambda item: (-item[1], self.corpus_chunks[item[0]]["chunk_id"]))

        results: List[Dict[str, Any]] = []
        for rank, (doc_idx, sc) in enumerate(scores[:top_k], start=1):
            chunk_data = dict(self.corpus_chunks[doc_idx])
            chunk_data["bm25_rank"] = rank
            chunk_data["bm25_score"] = sc
            results.append(chunk_data)

        return results


def reciprocal_rank_fusion(
    dense_hits: List[Dict[str, Any]],
    bm25_hits: List[Dict[str, Any]],
    rrf_k: int = 60,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Hợp nhất thứ hạng Reciprocal Rank Fusion (RRF) từ hai luồng Dense và Sparse (BM25).
    Công thức: RRF(d) = sum( 1.0 / (rrf_k + rank_m(d)) )
    - rrf_k: hằng số làm mượt (mặc định k=60).
    - rank: thứ hạng bắt đầu từ 1.
    - Deduplicate theo chunk_id.
    - Tie-break ổn định: ưu tiên RRF cao hơn, sau đó dense_rank nhỏ hơn, cuối cùng theo chunk_id.
    - Lưu tách bạch dense_rank, dense_score, bm25_rank, bm25_score và rrf_score.
    """
    dense_map: Dict[str, Tuple[int, float, Dict[str, Any]]] = {}
    for rank, item in enumerate(dense_hits, start=1):
        cid = item.get("chunk_id", "")
        sc = float(item.get("similarity", 0.0))
        dense_map[cid] = (rank, sc, item)

    bm25_map: Dict[str, Tuple[int, float, Dict[str, Any]]] = {}
    for rank, item in enumerate(bm25_hits, start=1):
        cid = item.get("chunk_id", "")
        # Nếu item đã có bm25_rank từ search thì ưu tiên, nếu không dùng rank duyệt
        b_rank = item.get("bm25_rank", rank)
        b_sc = float(item.get("bm25_score", 0.0))
        bm25_map[cid] = (b_rank, b_sc, item)

    all_chunk_ids: Set[str] = set(dense_map.keys()) | set(bm25_map.keys())
    fused_candidates: List[Dict[str, Any]] = []

    for cid in all_chunk_ids:
        rrf_score = 0.0
        d_rank: Optional[int] = None
        d_score: Optional[float] = None
        b_rank: Optional[int] = None
        b_score: Optional[float] = None
        base_item: Dict[str, Any] = {}

        if cid in dense_map:
            d_rank, d_score, base_item = dense_map[cid]
            rrf_score += 1.0 / (rrf_k + d_rank)

        if cid in bm25_map:
            b_rank, b_score, bm25_item = bm25_map[cid]
            rrf_score += 1.0 / (rrf_k + b_rank)
            if not base_item:
                base_item = bm25_item

        fused_item = dict(base_item)
        fused_item["dense_rank"] = d_rank
        fused_item["dense_score"] = d_score
        fused_item["bm25_rank"] = b_rank
        fused_item["bm25_score"] = b_score
        fused_item["rrf_score"] = round(rrf_score, 6)

        # Giữ similarity là dense_score (nếu có) để tương thích với cấu trúc downstream,
        # đồng thời bảo đảm trường rrf_score độc lập rõ ràng
        fused_item["similarity"] = d_score if d_score is not None else 0.0
        fused_candidates.append(fused_item)

    # Tie-break ổn định:
    # 1. rrf_score giảm dần (-rrf_score)
    # 2. dense_rank tăng dần (ưu tiên dense cao hơn nếu bằng điểm rrf; nếu None thì gán 9999)
    # 3. chunk_id tăng dần theo chữ cái (ổn định tuyệt đối)
    fused_candidates.sort(
        key=lambda x: (
            -x["rrf_score"],
            x["dense_rank"] if x["dense_rank"] is not None else 9999,
            x.get("chunk_id", ""),
        )
    )

    return fused_candidates[:top_k]
