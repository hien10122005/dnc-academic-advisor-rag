# MÃ NGUỒN CHƯƠNG TRÌNH: HỆ THỐNG TRỢ LÝ HỌC VỤ ĐẠI HỌC NAM CẦN THƠ
## Module Chunking Tokenizer-Aware, Vector Storage, FastAPI REST API, RAG Engine & Hybrid BM25+RRF (Phiên bản v2.6 - Nhiệm vụ 05 Lượt R02)

---

## 1. Giới thiệu tổng quan

Thư mục này chứa toàn bộ mã nguồn của hệ thống Trợ lý học vụ hỗ trợ sinh viên dựa trên kỹ thuật RAG (Retrieval-Augmented Generation) cho Trường Đại học Nam Cần Thơ (DNC).

Tại giai đoạn hiện tại (Nhiệm vụ 05 - Lượt R02: Chốt kỹ thuật Hybrid BM25+RRF và kiểm định thực nghiệm):
1. **Module Cấu trúc hóa & Phân đoạn văn bản (`backend/chunking.py`):** Xử lý văn bản Quyết định số 580/QĐ-ĐHNCT thành **104 chunks** định danh bất biến, bảo toàn cấu trúc điều khoản, phân biệt phần quyết định ban hành với quy chế, giữ nguyên vẹn bảng điểm Markdown và ghép liền các điều khoản nối qua trang. Đảm bảo $100\%$ chunks tuân thủ giới hạn cứng $\le 256$ tokens của mô hình embedding.
2. **Bộ Tách từ & Chỉ mục BM25 Sparse (`backend/bm25_retriever.py`):** Xây dựng bộ tách từ `tokenize_vietnamese` bảo toàn dấu tiếng Việt và số hiệu quy chế, triển khai BM25Okapi Index tính IDF theo chuẩn Lucene (tránh IDF âm), kết hợp thuật toán Reciprocal Rank Fusion ($k=60$) hòa trộn Top-20 Dense và Top-20 Sparse. Đảm bảo rank cuối cùng từ $1..k$, điểm số nullable (`similarity=None`, `distance=None`) cho các hit chỉ xuất hiện ở sparse.
3. **Bộ Kiểm thử Tự động 70 Bài (`tests/`):** 
   - `test_chunking_and_sources.py` (5 bài): Giới hạn token, tính toàn vẹn 351 source spans, nguồn overlap, độ phủ 51 hàng bảng/142 khoản và tính bất biến cô lập trong TemporaryDirectory.
   - `test_lifecycle_and_regression.py` (21 bài): Vòng đời ingestion, đối soát 3 chiều Preflight (status <-> manifest <-> collection metadata <-> hash), chống stale cache, nạp lại an toàn và ánh xạ whitespace regex.
   - `test_api_and_rag.py` (27 bài): FastAPI `/health`, `/chat`, validation 422, lọc hallucinated source ID, hạ cấp an toàn khi trích dẫn ảo, kiểm định schema phản hồi, xử lý trang in nullable, khử rò rỉ đường dẫn nội bộ `E:\private` và sentinel token, kiểm soát retry SDK (`attempts=1`), non-retry 401/404/ValueError, transient 503 retry, trích đoạn chứng cứ thực chất, bọc ngoại lệ định kiểu `DNCError`, và kiểm thử spy thu thập trace không gọi lặp retrieval.
   - `test_hybrid_bm25_rrf.py` (17 bài): Kiểm định tokenizer tiếng Việt, tính đơn định BM25, công thức RRF tính tay, xử lý query sparse rỗng, hòa trộn Top-5, kiểm tra hợp đồng sparse-only nullable, kiểm tra fail-closed khi thiếu chunks file, kiểm tra đối soát ID set và trùng lặp chunk_id, kiểm tra tự động hủy/tái tạo cache BM25 khi đổi fingerprint, và kiểm tra tham số `mode` qua API `/chat` được cách ly tuyệt đối bằng mock engine.
4. **Module Nạp dữ liệu Vector (`backend/ingestion.py`):** Sử dụng mô hình embedding ứng viên tiếng Việt `bkai-foundation-models/vietnamese-bi-encoder` (Revision: `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`), lưu trữ vào ChromaDB collection `qd580_baseline_v2` với cơ chế `upsert` bất biến và quản lý vòng đời trạng thái `BUILDING` $\rightarrow$ `READY`.
5. **Kiểm tra Tiền trạm Chốt chặn (Preflight Readiness - `backend/retrieval.py`):** Xác thực đa chiều trạng thái kho trước mọi truy vấn; tự động từ chối phục vụ (HTTP 503) nếu manifest hỏng/thiếu, lệch revision, lệch hash hoặc collection chưa nạp, đồng bộ đồng thời cho cả Dense và BM25 Index.
6. **Lớp Kết nối Gemini Đa chế độ (`backend/gemini_client.py`):** Tích hợp SDK chính thức `google-genai` (model mặc định `gemini-3.5-flash-lite`), phân loại lỗi có cấu trúc (HTTP status code), retry có chọn lọc trên lỗi tạm thời, vô hiệu hóa retry nội bộ của SDK, tự động ném `ConfigurationError` (HTTP 503) khi chưa cấu hình `GEMINI_API_KEY` ở chế độ phục vụ.
7. **RAG Engine & Xác minh Trích dẫn Backend (`backend/rag_engine.py`):** Định danh nguồn `SRC-k`, chuẩn bị ngữ cảnh kiểm soát, hỗ trợ lựa chọn chế độ truy xuất `mode="dense"` hoặc `mode="hybrid"`, trích xuất trace trực tiếp từ runtime mà không gọi lặp retrieval, trực tiếp xác thực source ID, loại bỏ triệt để hallucinated citations, hạ cấp an toàn sang `insufficient_evidence` và ưu tiên trích đoạn chứng cứ thực chất.
8. **Máy chủ Dịch vụ FastAPI (`backend/main.py`):** Cung cấp các endpoint REST API chuẩn hóa với cơ chế lifespan nạp trước mô hình vào RAM một lần duy nhất, hỗ trợ tham số `mode` ("dense" hoặc "hybrid"), tích hợp Global Exception Handler khử rò rỉ đường dẫn và sentinel tokens cho `DNCError`.
9. **Đánh giá Thực nghiệm A/B Độc lập (`evaluation/`):** Thực thi so sánh song song Dense vs Hybrid (BM25+RRF) trên toàn bộ 10 ca kiểm thử của bộ phát triển, đo lường bằng `time.perf_counter()` và lưu vết đầy đủ trong các tệp artifact chuyên biệt.

---

## 2. Cấu trúc thư mục mã nguồn

```
05_Mã Nguồn Chương Trình/
├── .venv/                         # Môi trường ảo Python phân lập
├── .gitignore                     # Bỏ qua cache, venv, checkpoint, .env
├── .env.example                   # Tệp mẫu cấu hình môi trường
├── requirements.txt               # Danh sách thư viện và phiên bản cụ thể
├── README.md                      # Tài liệu hướng dẫn cài đặt và vận hành
├── backend/
│   ├── __init__.py
│   ├── config.py                  # Quản lý đường dẫn, tham số chunking và model
│   ├── chunking.py                # Pipeline phân đoạn nhận biết Tokenizer
│   ├── ingestion.py               # Pipeline embedding và nạp vector (vòng đời READY)
│   ├── retrieval.py               # Vector retriever & Tiền trạm Preflight chốt chặn
│   ├── gemini_client.py           # Client kết nối Google Gemini SDK & Offline Mock stub
│   ├── rag_engine.py              # Engine điều phối RAG & Backend Citation Verification
│   ├── main.py                    # Ứng dụng FastAPI, Lifespan & REST Endpoints
│   └── cli.py                     # Giao diện CLI tra cứu thử nghiệm nhanh
├── data/
│   ├── QD580_CHUNKS.jsonl         # 104 chunks dữ liệu v2.0 đã xử lý
│   ├── QD580_MANIFEST.json        # Bản kê chi tiết metadata, SHA-256 và 351 source spans
│   └── INGESTION_STATUS.json      # Báo cáo trạng thái READY và lịch sử nạp vector
├── tests/
│   ├── __init__.py
│   ├── test_chunking_and_sources.py     # 5 bài test chunking, token & source spans
│   ├── test_lifecycle_and_regression.py # 21 bài test vòng đời, preflight & đối soát 3 chiều
│   └── test_api_and_rag.py              # 9 bài test FastAPI endpoints & RAG Engine
├── evaluation/
│   ├── __init__.py
│   ├── DEV_10_CAU_QD580.jsonl     # Snapshot bộ 10 ca kiểm thử đã chuẩn hóa bằng chứng
│   ├── evaluate_retrieval.py      # Script đánh giá hiệu năng truy xuất nghiêm ngặt
│   └── results/
│       ├── top_k_results.jsonl    # Chi tiết Top-10 chunks trả về cho từng ca kiểm thử
│       ├── retrieval_metrics.json # Tóm tắt chỉ số định lượng (Hit@K, MRR, Latency)
│       ├── BAO_CAO_BASELINE_VECTOR_QD580.md # Báo cáo phân tích chuyên sâu v2.0
│       └── BAO_CAO_RAG_CO_BAN_QD580.md     # Báo cáo kỹ thuật RAG FastAPI & Gemini
└── chroma_db/                     # Thư mục lưu trữ cơ sở dữ liệu vector ChromaDB
```

---

## 3. Cài đặt môi trường

Hệ thống chạy hoàn toàn cục bộ trên CPU máy cá nhân, không yêu cầu GPU rời, không yêu cầu API key hay dịch vụ đám mây trả phí.

### Kích hoạt môi trường ảo Python
```powershell
# Trên Windows PowerShell:
cd '05_Mã Nguồn Chương Trình'
.\.venv\Scripts\Activate.ps1
```

*(Trường hợp thiết lập môi trường mới từ đầu:)*
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 4. Hướng dẫn thực thi các module

### 4.1 Chạy toàn bộ bộ kiểm thử tự động (70 Tests Toàn diện)
Hệ thống tích hợp 70 bài kiểm thử tự động phân lập, chạy hoàn toàn offline không cần internet hay API key:
```powershell
# Chạy toàn bộ 70 bài test trong thư mục tests/:
$env:HF_HUB_OFFLINE="1"; $env:TRANSFORMERS_OFFLINE="1"; $env:GEMINI_API_KEY=""; .\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"

# Hoặc chạy từng bộ test độc lập:
.\.venv\Scripts\python.exe -m unittest tests/test_chunking_and_sources.py     # 5 bài test chunking & source spans
.\.venv\Scripts\python.exe -m unittest tests/test_lifecycle_and_regression.py # 21 bài test vòng đời & preflight
.\.venv\Scripts\python.exe -m unittest tests/test_api_and_rag.py              # 27 bài test FastAPI & RAG engine
.\.venv\Scripts\python.exe -m unittest tests/test_hybrid_bm25_rrf.py          # 17 bài test BM25, RRF & hybrid mode
```

### 4.2 Chạy đánh giá so sánh thực nghiệm A/B (Retrieval & Live Gemini)
Thực hiện đánh giá đối chứng trung thực trên tập 10 ca phát triển (DEV_01 -> DEV_10):
```powershell
# 1. Đánh giá A/B thuần truy xuất (Hit@K, MRR, Source Span Evidence Coverage):
.\.venv\Scripts\python.exe evaluation/evaluate_retrieval_ab.py

# 2. Đánh giá A/B Live với Google Gemini (thu thập trace, rubric từng ý và telemetry):
.\.venv\Scripts\python.exe evaluation/run_eval_live_task05.py
```

### 4.3 Khởi động Máy chủ Dịch vụ FastAPI (REST API)
Khởi chạy dịch vụ API học vụ với cơ chế Lifespan (nạp trước model và kiểm tra tiền trạm kho tri thức):
```powershell
# Chạy máy chủ Uvicorn tại cổng 8000:
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
- **Tài liệu trực quan Swagger UI:** Truy cập trình duyệt tại `http://localhost:8000/docs`.
- **Kiểm tra trạng thái hệ thống (`GET /health`):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get | ConvertTo-Json
```

- **Gửi câu hỏi học vụ (`POST /chat`):**
Mặc định hệ thống dùng chế độ `dense` (baseline). Người dùng có thể chỉ định `mode="hybrid"` để kích hoạt BM25+RRF:
```powershell
# Chế độ mặc định (Dense):
$body = @{ question = "Sinh viên hệ 4 năm được đăng ký tối đa bao nhiêu tín chỉ một kỳ?" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5

# Chế độ Hybrid (BM25 + RRF):
$body = @{ question = "Sinh viên hệ 4 năm được đăng ký tối đa bao nhiêu tín chỉ một kỳ?"; mode = "hybrid" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5
```

### 4.4 Tra cứu Thử nghiệm bằng Dòng lệnh (CLI RAG)
Tra cứu trực tiếp câu hỏi từ terminal qua RAG Engine với tham số `--mode`:
```powershell
# Tra cứu chế độ mặc định (Dense):
.\.venv\Scripts\python.exe backend/cli.py "Điều kiện học cùng lúc hai chương trình là gì?"

# Tra cứu chế độ Hybrid (Dense + BM25 + RRF):
.\.venv\Scripts\python.exe backend/cli.py "Điều kiện học cùng lúc hai chương trình là gì?" --mode hybrid

# Chế độ tương tác liên tục:
.\.venv\Scripts\python.exe backend/cli.py --interactive --mode hybrid
```

### 4.4 Chạy quy trình phân đoạn (Chunking v2.0)
Đọc dữ liệu từ `QD580_PAGES.jsonl` và sinh các chunk cấu trúc tuân thủ tokenizer:
```powershell
.\.venv\Scripts\python.exe -m backend.chunking
```
- **Đầu ra:** `data/QD580_CHUNKS.jsonl` (104 chunks) và `data/QD580_MANIFEST.json`.

### 4.5 Chạy nạp dữ liệu vào ChromaDB (Ingestion v2.0)
Mã hóa vector 768 chiều và lưu vào collection `qd580_baseline_v2`:
```powershell
.\.venv\Scripts\python.exe -m backend.ingestion
```
- **Tính năng:** Đảm bảo tính bất biến (Idempotent). Chạy lại nhiều lần vẫn giữ nguyên đúng 104 chunks trong kho.
- **Đầu ra:** Cập nhật thư mục `chroma_db/` và tệp trạng thái `data/INGESTION_STATUS.json`.

### 4.6 Chạy bộ đánh giá chuẩn hóa (Benchmark Evaluation)
Thực hiện đánh giá tự động nghiêm ngặt trên 10 ca kiểm thử của bộ phát triển:
```powershell
.\.venv\Scripts\python.exe -m evaluation.evaluate_retrieval
```
- **Đầu ra:**
  - `evaluation/results/top_k_results.jsonl`
  - `evaluation/results/retrieval_metrics.json`
  - Bảng tổng kết chỉ số (Hit Rate@1, @3, @5, @10, MRR@10, Evidence Coverage, Latency).

---

## 5. Kết quả hiệu năng Baseline A (Phiên bản v2.0)

Thử nghiệm nghiêm ngặt trên 9 ca hợp lệ (Grounded) của QĐ 580:
- **Hit Rate@1 (Full Coverage $\ge 90\%$):** **$55.6\%$** (5/9 ca)
- **Hit Rate@3 (Full Coverage $\ge 90\%$):** **$77.8\%$** (7/9 ca)
- **Hit Rate@5 (Full Coverage $\ge 90\%$):** **$77.8\%$** (7/9 ca)
- **Hit Rate@10 (Full Coverage $\ge 90\%$):** **$100.0\%$** (9/9 ca)
- **Mean Reciprocal Rank (MRR@10):** **$0.6806$**
- **Độ phủ bằng chứng trung bình@10:** **$83.1\%$**
- **Tỷ lệ phủ đủ tất cả bằng chứng@10:** **$66.7\%$** (6/9 ca phủ trọn vẹn $100\%$ các ý đa nguồn)
- **Độ trễ trung bình truy vấn:** **$63.6\text{ ms}$** (CPU)
- **Phân tích ca ngoại vi (DEV_10):** Đạt Top 1 similarity là $0.4295$, cao hơn một số câu hợp lệ dùng ngôn ngữ đời thường (như DEV_07: $0.2676$, DEV_08: $0.3258$). Do đó, hệ thống không dùng ngưỡng cắt tĩnh $0.45$ mà sẽ kết hợp Hybrid Search và LLM Guardrail ở giai đoạn sau.

Chi tiết phân tích chuyên sâu được trình bày tại [Báo cáo Baseline Vector QĐ 580 v2.0](file:///e:/Đám%20Mây/Năm%204/Học%20kỳ%201%20-%20Năm%20học%202026-2027/Đồ%20án%202%20-%20chuyên%20ngành%20(CNTT)/05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_BASELINE_VECTOR_QD580.md).
