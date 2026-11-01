# MÃ NGUỒN CHƯƠNG TRÌNH: HỆ THỐNG TRỢ LÝ HỌC VỤ ĐẠI HỌC NAM CẦN THƠ
## Module Chunking Tokenizer-Aware, Vector Storage và Đánh Giá Truy Xuất Baseline (Phiên bản v2.0)

---

## 1. Giới thiệu tổng quan

Thư mục này chứa toàn bộ mã nguồn của hệ thống Trợ lý học vụ hỗ trợ sinh viên dựa trên kỹ thuật RAG (Retrieval-Augmented Generation) cho Trường Đại học Nam Cần Thơ (DNC).

Tại giai đoạn hiện tại (Nhiệm vụ 03 - Phiên bản v2.0), hệ thống đã hoàn thiện:
1. **Module Cấu trúc hóa & Phân đoạn văn bản (`backend/chunking.py`):** Xử lý văn bản Quyết định số 580/QĐ-ĐHNCT thành **104 chunks** định danh bất biến, bảo toàn cấu trúc điều khoản, phân biệt phần quyết định ban hành với quy chế, giữ nguyên vẹn bảng điểm Markdown và ghép liền các điều khoản nối qua trang. Đảm bảo $100\%$ chunks tuân thủ giới hạn cứng $\le 256$ tokens của mô hình embedding.
2. **Bộ Kiểm thử Tự động (`tests/test_chunking_and_sources.py`):** Kiểm tra tự động 5 tiêu chí bắt buộc: giới hạn token, tính toàn vẹn của 351 source spans, nguồn overlap, độ phủ 51 hàng bảng biểu/142 khoản quy chế và tính bất biến (idempotency).
3. **Module Nạp dữ liệu Vector (`backend/ingestion.py`):** Sử dụng mô hình embedding ứng viên tiếng Việt `bkai-foundation-models/vietnamese-bi-encoder` (Revision: `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`), lưu trữ vào ChromaDB collection `qd580_baseline_v2` với cơ chế `upsert` bất biến và quản lý vòng đời trạng thái `BUILDING` $\rightarrow$ `READY`.
4. **Module Truy xuất Ngữ nghĩa (`backend/retrieval.py`):** Cung cấp API và giao diện CLI để tìm kiếm vector theo Cosine Distance/Similarity, kiểm tra trạng thái `READY` trước khi truy xuất.
5. **Bộ Đánh giá Thực nghiệm Nghiêm ngặt (`evaluation/evaluate_retrieval.py`):** Đánh giá dựa trên thuật toán giao khoảng ký tự (Span Intersection Ratio), phân biệt Full Coverage ($\ge 90\%$) và Partial Match, loại bỏ hoàn toàn lỗi chấm nhầm khi cùng Điều khác khoản.

---

## 2. Cấu trúc thư mục mã nguồn

```
05_Mã Nguồn Chương Trình/
├── .venv/                         # Môi trường ảo Python phân lập
├── .gitignore                     # Bỏ qua cache, venv, checkpoint
├── .env.example                   # Tệp mẫu cấu hình môi trường
├── requirements.txt               # Danh sách thư viện và phiên bản cụ thể
├── README.md                      # Tài liệu hướng dẫn cài đặt và vận hành
├── backend/
│   ├── __init__.py
│   ├── config.py                  # Quản lý đường dẫn, tham số chunking và model
│   ├── chunking.py                # Pipeline phân đoạn nhận biết Tokenizer
│   ├── ingestion.py               # Pipeline embedding và nạp vector (vòng đời READY)
│   └── retrieval.py               # Vector retriever (hàm Python & CLI tìm kiếm)
├── data/
│   ├── QD580_CHUNKS.jsonl         # 104 chunks dữ liệu v2.0 đã xử lý
│   ├── QD580_MANIFEST.json        # Bản kê chi tiết metadata, SHA-256 và 351 source spans
│   └── INGESTION_STATUS.json      # Báo cáo trạng thái READY và lịch sử nạp vector
├── tests/
│   ├── __init__.py
│   ├── test_chunking_and_sources.py     # 5 bài unit/integration test chunking & source spans
│   └── test_lifecycle_and_regression.py # 14 bài regression test vòng đời ingestion, readiness & regex offset
├── evaluation/
│   ├── __init__.py
│   ├── DEV_10_CAU_QD580.jsonl     # Snapshot bộ 10 ca kiểm thử đã chuẩn hóa bằng chứng
│   ├── evaluate_retrieval.py      # Script đánh giá hiệu năng truy xuất nghiêm ngặt
│   └── results/
│       ├── top_k_results.jsonl    # Chi tiết Top-10 chunks trả về cho từng ca kiểm thử
│       ├── retrieval_metrics.json # Tóm tắt chỉ số định lượng (Hit@K, MRR, Latency)
│       └── BAO_CAO_BASELINE_VECTOR_QD580.md # Báo cáo phân tích chuyên sâu v2.0
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

### 4.1 Chạy bộ kiểm thử tự động (Unit & Regression Tests)
Kiểm tra toàn diện 19 tiêu chí kỹ thuật:
```powershell
# 1. Kiểm tra 5 tiêu chí chunking, token limit, source spans, coverage & idempotency:
.\.venv\Scripts\python.exe -m tests.test_chunking_and_sources

# 2. Kiểm tra 14 tiêu chí vòng đời ingestion, readiness cache invalidation, revision & whitespace regex:
.\.venv\Scripts\python.exe -m tests.test_lifecycle_and_regression
```

### 4.2 Chạy quy trình phân đoạn (Chunking v2.0)
Đọc dữ liệu từ `QD580_PAGES.jsonl` và sinh các chunk cấu trúc tuân thủ tokenizer:
```powershell
.\.venv\Scripts\python.exe -m backend.chunking
```
- **Đầu ra:** `data/QD580_CHUNKS.jsonl` (104 chunks) và `data/QD580_MANIFEST.json`.

### 4.3 Chạy nạp dữ liệu vào ChromaDB (Ingestion v2.0)
Mã hóa vector 768 chiều và lưu vào collection `qd580_baseline_v2`:
```powershell
.\.venv\Scripts\python.exe -m backend.ingestion
```
- **Tính năng:** Đảm bảo tính bất biến (Idempotent). Chạy lại nhiều lần vẫn giữ nguyên đúng 104 chunks trong kho.
- **Đầu ra:** Cập nhật thư mục `chroma_db/` và tệp trạng thái `data/INGESTION_STATUS.json`.

### 4.4 Thử nghiệm tìm kiếm bằng dòng lệnh (CLI Retrieval)
Truy vấn trực tiếp câu hỏi học vụ từ terminal:
```powershell
.\.venv\Scripts\python.exe -m backend.retrieval --query "Điều kiện cảnh báo kết quả học tập là gì?" --top_k 3
```

### 4.5 Chạy bộ đánh giá chuẩn hóa (Benchmark Evaluation)
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
