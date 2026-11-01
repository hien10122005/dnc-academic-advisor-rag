# -*- coding: utf-8 -*-
"""
backend.config
Cấu hình hệ thống RAG - Đồ án Trợ lý học vụ NCTU (Phiên bản v2.0)
Quản lý các đường dẫn, thông số chunking nhận biết tokenizer và ChromaDB collection.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Thư mục gốc mã nguồn: 05_Mã Nguồn Chương Trình
BASE_DIR = Path(__file__).resolve().parent.parent

# Nạp tệp cấu hình .env (ưu tiên biến môi trường đã thiết lập bên ngoài, override=False)
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=False)
else:
    load_dotenv(override=False)

# Thư mục gốc toàn bộ đồ án
PROJECT_ROOT = BASE_DIR.parent

# Đường dẫn dữ liệu nguồn đã kiểm chứng
CORPUS_FILE = PROJECT_ROOT / "02_Dữ Liệu Quy Chế" / "04_Dữ Liệu Đã Kiểm Chứng" / "QD580" / "QD580_PAGES.jsonl"
DEV_CASES_FILE = PROJECT_ROOT / "02_Dữ Liệu Quy Chế" / "04_Dữ Liệu Đã Kiểm Chứng" / "QD580" / "DEV_10_CAU_QD580.jsonl"
ORIGINAL_PDF_FILE = PROJECT_ROOT / "02_Dữ Liệu Quy Chế" / "01_Tài Liệu Gốc (PDF)" / "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf"

# Thư mục lưu trữ trung gian và kết quả
DATA_DIR = BASE_DIR / "data"
CHUNKS_FILE = DATA_DIR / "QD580_CHUNKS.jsonl"
MANIFEST_FILE = DATA_DIR / "QD580_MANIFEST.json"
INGESTION_STATUS_FILE = DATA_DIR / "INGESTION_STATUS.json"

CHROMA_PERSIST_DIR = BASE_DIR / "chroma_db"
EVALUATION_DIR = BASE_DIR / "evaluation"
RESULTS_DIR = EVALUATION_DIR / "results"

# Đảm bảo các thư mục tồn tại
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
os.makedirs(EVALUATION_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Thông số kỹ thuật Chunking (Phiên bản v2.0 - Tokenizer Aware)
CHUNK_VERSION = "v2.0"
MAX_INPUT_TOKENS = 240         # Ngưỡng an toàn tuyệt đối (mô hình hard max là 256)
TARGET_CHUNK_TOKENS = 200      # Mốc mục tiêu cho nội dung
MIN_CHUNK_TOKENS = 30          # Ngưỡng tối thiểu để tránh chunk rác
OVERLAP_MAX_TOKENS = 40        # Giới hạn token gối đầu

# Cấu hình Vector Database & Embedding
COLLECTION_NAME_V1 = "qd580_baseline_a"  # Giữ nguyên bản baseline cũ để đối chiếu
COLLECTION_NAME = "qd580_baseline_v2"     # Bộ sưu tập phiên bản mới sau khi sửa
EMBEDDING_MODEL_CANDIDATE = "bkai-foundation-models/vietnamese-bi-encoder"
MODEL_REVISION = "84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0"
EMBEDDING_DIM = 768
DISTANCE_METRIC = "cosine"

# Cấu hình LLM Gemini (Mô hình gemini-3.5-flash-lite khuyến nghị chính thức từ Google, độ trễ ~1.5s)
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip()
ALLOW_OFFLINE_MOCK = os.getenv("ALLOW_OFFLINE_MOCK", "false").lower() in ("true", "1", "yes")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30.0"))
MAX_RETRY_ATTEMPTS = int(os.getenv("MAX_RETRY_ATTEMPTS", "2"))


def load_tokenizer(model_name: str = EMBEDDING_MODEL_CANDIDATE, revision: str = MODEL_REVISION):
    """Tải AutoTokenizer với revision commit hash bắt buộc và kiểm tra tính hợp lệ."""
    from transformers import AutoTokenizer
    if revision != MODEL_REVISION:
        raise ValueError(f"Revision '{revision}' không khớp MODEL_REVISION chuẩn '{MODEL_REVISION}'")
    tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)
    return tokenizer


def load_embedding_model(model_name: str = EMBEDDING_MODEL_CANDIDATE, revision: str = MODEL_REVISION):
    """Tải SentenceTransformer với revision commit hash bắt buộc và kiểm tra tính hợp lệ."""
    from sentence_transformers import SentenceTransformer
    if revision != MODEL_REVISION:
        raise ValueError(f"Revision '{revision}' không khớp MODEL_REVISION chuẩn '{MODEL_REVISION}'")
    model = SentenceTransformer(model_name, revision=revision)
    return model
