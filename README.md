# dnc-academic-advisor-rag

> **Hệ thống Trợ lý học vụ hỗ trợ sinh viên giải đáp quy chế đào tạo Trường Đại học Nam Cần Thơ dựa trên kiến trúc RAG, Vietnamese Bi-Encoder và ChromaDB.**

---

## 1. Giới thiệu đề tài & Phạm vi

Dự án thuộc **Đồ án 2 - Chuyên ngành Công nghệ thông tin**, Trường Đại học Nam Cần Thơ (DNC). Mục tiêu của đề tài là xây dựng hệ thống hỏi đáp học vụ thông minh (Academic Advisor RAG) giúp sinh viên tra cứu chính xác, tức thì các quy định, quy chế đào tạo, chuẩn đầu ra, điều kiện tốt nghiệp và học phí với câu trả lời có trích dẫn nguồn minh bạch (Citations).

### Phạm vi giai đoạn hiện tại (Nhiệm vụ 03 - Baseline A v2.0):
- **Tài liệu mục tiêu:** Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024 ban hành Quy chế đào tạo trình độ đại học của Trường Đại học Nam Cần Thơ (26 trang PDF).
- **Kiến trúc cốt lõi:**
  - **Structural Chunking (Tokenizer-Aware):** Phân đoạn văn bản cấu trúc theo điều khoản, kiểm soát cứng $\le 256$ tokens (MAX_INPUT_TOKENS = 240), bảo toàn nguyên vẹn 100% bảng biểu và các điều khoản nối trang.
  - **Source Spans Tracking:** Truy nguyên chính xác tuyệt đối từng ký tự trên trang PDF nguồn (`page_start_char`, `page_end_char`) và vị trí trong chunk.
  - **Vector Ingestion & Storage:** Nạp vector embedding 768 chiều vào ChromaDB cục bộ với cơ chế `upsert` bất biến (idempotent), quản lý vòng đời trạng thái `BUILDING` $\rightarrow$ `READY`.
  - **Strict Retrieval Benchmark:** Đánh giá hiệu năng truy xuất trên bộ phát triển 10 ca kiểm thử bằng thuật toán giao khoảng ký tự (Span Intersection Ratio), phân biệt Full Coverage ($\ge 90\%$) và Partial Match.
- **Ranh giới kỹ thuật hiện tại:** Chưa tích hợp LLM Generation (Gemini API), chưa có Hybrid BM25, chưa có Reranker, chưa xây dựng API FastAPI và giao diện người dùng Streamlit/Admin.

---

## 2. Cấu trúc thư mục dự án

```
dnc-academic-advisor-rag/
├── .gitignore                         # Loại trừ venv, cache, ChromaDB, PDF gốc
├── README.md                          # Tài liệu tổng quan dự án tại Git root
├── PROJECT.md                         # Báo cáo phạm vi và kế hoạch giảm tải đồ án
├── LOGIC.md                           # Đặc tả kỹ thuật và kiến trúc xử lý RAG
├── ROADMAP.md                         # Kế hoạch thực hiện và nhật ký tiến độ chi tiết
├── 01_Kế Hoạch & Hướng Dẫn/           # Hướng dẫn đồ án của Khoa CNTT
├── 02_Dữ Liệu Quy Chế/
│   ├── 01_Tài Liệu Gốc (PDF)/         # Thư mục chứa PDF gốc (cần tự chuẩn bị)
│   ├── 02_Văn Bản Đã Làm Sạch (Text)/ # Bản text chuyển đổi ban đầu
│   ├── 03_Kiểm Tra Chất Lượng Dữ Liệu/# Báo cáo đối chiếu nguồn và danh sách vấn đề
│   └── 04_Dữ Liệu Đã Kiểm Chứng/
│       └── QD580/                     # Dữ liệu QĐ 580 đã kiểm chứng 100% từng trang
│           ├── QD580_PAGES.jsonl      # 26 trang JSONL chuẩn hóa có offset
│           ├── QD580_THEO_TRANG.md    # Văn bản Markdown đối soát từng trang
│           └── DEV_10_CAU_QD580.jsonl # Bộ 10 ca kiểm thử phát triển
└── 05_Mã Nguồn Chương Trình/          # Toàn bộ mã nguồn thực thi
    ├── .venv/                         # Môi trường ảo Python (local)
    ├── requirements.txt               # Khóa phiên bản thư viện cần thiết
    ├── .env.example                   # Mẫu cấu hình môi trường
    ├── README.md                      # Hướng dẫn chi tiết vận hành mã nguồn
    ├── backend/
    │   ├── config.py                  # Cấu hình đường dẫn, tham số chunking và model
    │   ├── chunking.py                # Pipeline phân đoạn nhận biết Tokenizer v2.0
    │   ├── ingestion.py               # Pipeline embedding & nạp vector (vòng đời READY)
    │   └── retrieval.py               # Module tìm kiếm vector & CLI tra cứu
    ├── tests/
    │   └── test_chunking_and_sources.py # 5 bài unit/integration test tự động
    ├── evaluation/
    │   ├── DEV_10_CAU_QD580.jsonl     # Snapshot bộ 10 ca kiểm thử
    │   ├── evaluate_retrieval.py      # Script đánh giá hiệu năng truy xuất nghiêm ngặt
    │   └── results/
    │       ├── top_k_results.jsonl    # Chi tiết Top-10 chunks trả về cho từng ca
    │       ├── retrieval_metrics.json # Tóm tắt chỉ số định lượng
    │       └── BAO_CAO_BASELINE_VECTOR_QD580.md # Báo cáo phân tích chuyên sâu v2.0
    ├── data/
    │   ├── QD580_CHUNKS.jsonl         # 104 chunks dữ liệu v2.0
    │   ├── QD580_MANIFEST.json        # Bản kê chi tiết metadata và 351 source spans
    │   └── INGESTION_STATUS.json      # Báo cáo trạng thái READY của kho vector
    └── chroma_db/                     # Cơ sở dữ liệu vector ChromaDB (local)
```

---

## 3. Yêu cầu hệ thống & Chuẩn bị dữ liệu

### 3.1 Môi trường phần mềm
- **Hệ điều hành:** Windows 10/11, Linux hoặc macOS.
- **Python:** Phiên bản 3.10 trở lên (khuyên dùng môi trường ảo riêng biệt).
- **Phần cứng:** Chạy hoàn toàn trên CPU thông thường, không yêu cầu card đồ họa rời GPU.
- **Không yêu cầu:** Không cần API key trả phí ở giai đoạn này. Mô hình embedding mã nguồn mở được tải tự động từ Hugging Face Hub.

### 3.2 Chuẩn bị tệp PDF gốc
Do quy định về kích thước và bản quyền tài liệu, tệp PDF gốc không được commit lên Git. Hãy đặt tệp PDF gốc vào đúng đường dẫn sau:
```
02_Dữ Liệu Quy Chế/01_Tài Liệu Gốc (PDF)/580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf
```
*(Dung lượng tệp: $6,635,360\text{ bytes}$, SHA-256: `a3ba2122457999f631a876c39d82d487df880f0d3e2c5c66f4e5dbce9cd560db`)*

---

## 4. Hướng dẫn cài đặt và thực thi

### Bước 1: Khởi tạo môi trường ảo và cài đặt thư viện
```powershell
cd '05_Mã Nguồn Chương Trình'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Bước 2: Chạy bộ kiểm thử tự động (Unit Tests)
Kiểm tra 5 tiêu chí kỹ thuật: giới hạn token, source spans, overlap, độ phủ và tính bất biến:
```powershell
.\.venv\Scripts\python.exe -m tests.test_chunking_and_sources
```

### Bước 3: Phân đoạn văn bản (Chunking v2.0)
Sinh 104 chunks định danh ổn định và bản kê manifest:
```powershell
.\.venv\Scripts\python.exe -m backend.chunking
```

### Bước 4: Nạp vector vào ChromaDB (Ingestion v2.0)
Mã hóa vector 768 chiều vào collection `qd580_baseline_v2`:
```powershell
.\.venv\Scripts\python.exe -m backend.ingestion
```

### Bước 5: Tra cứu dòng lệnh (CLI Retrieval)
Thử nghiệm tìm kiếm trực tiếp trên terminal:
```powershell
.\.venv\Scripts\python.exe -m backend.retrieval --query "Điều kiện cảnh báo kết quả học tập là gì?" --top_k 3
```

### Bước 6: Chạy đánh giá Benchmark nghiêm ngặt
Chạy script đo lường trên 10 ca kiểm thử chuẩn hóa:
```powershell
.\.venv\Scripts\python.exe -m evaluation.evaluate_retrieval
```

---

## 5. Kết quả thực nghiệm Baseline A (Phiên bản v2.0)

Thử nghiệm nghiêm ngặt theo phương pháp giao khoảng ký tự (Span Intersection Ratio) trên 9 ca có căn cứ học vụ thực tế:
- **Mô hình Embedding:** `bkai-foundation-models/vietnamese-bi-encoder` (Revision: `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`).
- **Tổng số Chunks:** **104 chunks** ($100\%$ chunks có token $\le 256$, max 246, avg 184.4).
- **Hit Rate@1 (Full Coverage $\ge 90\%$):** **$55.6\%$** (5/9 ca).
- **Hit Rate@3 (Full Coverage $\ge 90\%$):** **$77.8\%$** (7/9 ca).
- **Hit Rate@5 (Full Coverage $\ge 90\%$):** **$77.8\%$** (7/9 ca).
- **Hit Rate@10 (Full Coverage $\ge 90\%$):** **$100.0\%$** (9/9 ca).
- **Mean Reciprocal Rank (MRR@10):** **$0.6806$**.
- **Độ phủ bằng chứng trung bình@10:** **$83.1\%$**.
- **Tỷ lệ phủ đủ TẤT CẢ bằng chứng@10:** **$66.7\%$** (6/9 ca thu hồi trọn vẹn $100\%$ các ý đa nguồn).
- **Độ trễ trung bình truy vấn:** **$63.6\text{ ms}$** (trên CPU).

### Hạn chế hiện tại & Định hướng Tuần 3-4:
- Mô hình Dense Bi-Encoder thuần túy bị chi phối bởi các từ ngữ khẩu ngữ đời thường (như ở DEV_07, DEV_08).
- Điểm tương đồng của câu ngoại phạm vi DEV_10 ($0.4295$) cao hơn một số câu hợp lệ dùng từ ngữ đời thường, chứng minh **không thể dùng ngưỡng cắt tương đồng tĩnh ($0.45$) làm bộ lọc từ chối duy nhất**.
- Giai đoạn tới sẽ tích hợp **Hybrid BM25**, **Cross-Encoder Reranker** và **Tầng xác thực trích dẫn của LLM** để nâng cao độ chính xác và khả năng phòng vệ chống ảo giác.
