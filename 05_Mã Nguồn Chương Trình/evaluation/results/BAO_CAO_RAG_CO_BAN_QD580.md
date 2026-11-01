# BÁO CÁO KỸ THUẬT: HIỆN THỰC PIPELINE RAG HỌC VỤ QĐ 580 QUA FASTAPI VÀ GOOGLE GEMINI
## Nghiệm Thu Kỹ Thuật Nhiệm Vụ 04 — Kiến Trúc RAG Phân Lập, Preflight Chốt Chặn Và Xác Minh Trích Dẫn

---

> **Căn cứ pháp lý & Chuẩn mực:**
> - Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024 của Hiệu trưởng Trường Đại học Nam Cần Thơ ban hành Quy chế đào tạo trình độ đại học.
> - Quyết định số 309/QĐ-ĐHNCT ngày 08/12/2016 của Hiệu trưởng Trường Đại học Nam Cần Thơ về quy định trình bày đồ án/khóa luận tốt nghiệp.
> - Thông tư số 08/2021/TT-BGDĐT của Bộ Giáo dục và Đào tạo ban hành Quy chế đào tạo trình độ đại học.
> - Tài liệu giao nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_RAG_FASTAPI_GEMINI.md`.

---

## 1. Tổng quan mục tiêu và phạm vi kỹ thuật

Nhiệm vụ 04 đánh dấu bước chuyển dịch quan trọng từ hệ thống đánh giá truy xuất vector thuần túy (Task 03) sang một pipeline hỏi đáp hoàn chỉnh theo kiến trúc RAG (Retrieval-Augmented Generation) cục bộ, phục vụ công tác tra cứu quy chế học vụ cho Trường Đại học Nam Cần Thơ.

Luồng xử lý nghiệp vụ xuyên suốt được thiết lập như sau:
$$\text{Câu hỏi độc lập} \longrightarrow \text{Preflight Readiness} \longrightarrow \text{Vector Retrieval (Top-K)} \longrightarrow \text{Chuẩn bị Context (SRC-k)} \longrightarrow \text{Gemini LLM} \longrightarrow \text{Xác minh Citation Backend} \longrightarrow \text{FastAPI REST Response}$$

### Giới hạn kỹ thuật và phạm vi cam kết:
1. **Dữ liệu:** Sử dụng độc quyền kho tri thức số hóa chuẩn mực Quyết định số 580/QĐ-ĐHNCT (gồm 104 chunks định danh, 351 source spans đối soát từng ký tự, collection ChromaDB `qd580_baseline_v2`).
2. **Kiến trúc:** Giữ nguyên phương pháp Baseline A (Vector Search thuần túy bằng `bkai-foundation-models/vietnamese-bi-encoder`, Revision `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`). Chưa áp dụng Hybrid Search (BM25), Reranking hay Query Rewriting trong nhiệm vụ này.
3. **Môi trường & Bảo mật:** Toàn bộ hệ thống chạy phân lập trong môi trường ảo `.venv`. Tuyệt đối không hardcode API key, không phơi bày đường dẫn tuyệt đối nội bộ ra API công khai, và không đưa bí mật lên hệ thống quản lý phiên bản Git.

---

## 2. Chi tiết kết quả thực hiện theo 4 bước cốt lõi

### 2.1 Bước A — Chốt chặn tiền trạm nghiêm ngặt (Preflight Readiness Verification)

Trước khi kích hoạt bất kỳ endpoint API hay truy vấn nào, `backend/retrieval.py` thiết lập chốt chặn tiền trạm đối soát 3 chiều toàn diện nhằm loại bỏ triệt để nguy cơ stale cache hoặc chấp nhận dữ liệu hỏng:

1. **Kiểm tra tệp trạng thái (`INGESTION_STATUS.json`):** Xác thực định dạng JSON, kiểm tra trường `corpus_ready: true` (kiểu boolean tường minh) và `status: "READY"`.
2. **Kiểm tra tệp bản kê (`QD580_MANIFEST.json`):** Bắt buộc tệp phải tồn tại và phân tích cú pháp hợp lệ; xác thực sự hiện diện của các trường bắt buộc (`corpus_fingerprint`, `chunks_sha256`, `model_revision`, `total_chunks`). Mọi trường hợp tệp thiếu hoặc hỏng JSON đều bị chặn ngay lập tức với lỗi `RuntimeError` chi tiết.
3. **Đối soát tính nhất quán 3 chiều:**
   - So khớp `corpus_fingerprint` giữa `INGESTION_STATUS.json` và `QD580_MANIFEST.json` (`8f0c62a9ce8b2b049597599e10cc072760e21cf7cec442386848122226e977dd`).
   - So khớp `chunks_sha256` giữa status, manifest và mã băm SHA-256 thực tế của tệp `QD580_CHUNKS.jsonl` trên đĩa cứng (`5802f176f1f603123126c49284449085bd18bdf64f3213998e081ecd01536398`).
   - So khớp metadata thực tế lưu trong collection ChromaDB (`corpus_fingerprint`, `chunks_sha256`, `model_revision`).
4. **Quản lý trạng thái lỗi trong Ingestion:** Bổ sung cơ chế trong `backend/ingestion.py` đảm bảo nếu quá trình nạp gặp bất kỳ lỗi nào, trạng thái lập tức ghi nhận `status: "FAILED"`, không giữ nhầm trạng thái `READY` của lần nạp trước.

### 2.2 Bước B — Kết nối Google Gemini có kiểm soát (Gemini Client)

Triển khai module `backend/gemini_client.py` theo đúng khuyến cáo mới nhất từ Google:
- **SDK chính thức:** Sử dụng thư viện `google-genai==2.34.0` (thay thế hoàn toàn gói `google-generativeai` cũ đã lỗi thời).
- **Mô hình định cấu hình:** `gemini-2.5-flash` được đọc thông qua biến môi trường `GEMINI_MODEL`, khóa xác thực qua `GEMINI_API_KEY`.
- **Kiểm soát tài nguyên:** Thiết lập thời gian chờ (timeout) 30 giây, giới hạn đầu ra `max_output_tokens=1024`, và cơ chế thử lại hữu hạn (2 lần retry) với chiến lược backoff khi gặp lỗi tạm thời.
- **Phân tách chế độ Mock và Live:** Tích hợp lớp `GeminiClient` có khả năng tự động nhận diện môi trường. Khi chưa cấu hình khóa API thực tế, client hoạt động ở chế độ Offline Mock xác định (Deterministic Mock Stub) phục vụ kiểm thử hợp đồng phần mềm mà không thực hiện cuộc gọi mạng nào.

### 2.3 Bước C — RAG Engine & Xác minh trích dẫn phía Backend (Citation Verification)

Module `backend/rag_engine.py` đóng vai trò nhạc trưởng điều phối toàn bộ chu trình xử lý:
1. **Chuẩn bị ngữ cảnh & Định danh nguồn:**
   - Mỗi đoạn trích xuất từ ChromaDB được gắn nhãn định danh duy nhất theo cú pháp `SRC-k` (ví dụ: `SRC-1`, `SRC-2`, ...).
   - Ngữ cảnh đưa vào prompt bao gồm: Tiêu đề quyết định, Chương, Điều, số trang in và trang PDF, cùng nội dung văn bản gốc.
   - System Prompt quy định rõ ràng vai trò Trợ lý tra cứu học vụ nội bộ, chỉ kết luận dựa trên dữ liệu được cấp và giữ nguyên con số, điều kiện, chế tài.
2. **Xác minh trích dẫn độc lập tại Backend (Không tin tưởng đầu ra LLM):**
   - Đề nghị Gemini trả về cấu trúc JSON gồm trạng thái nghiệp vụ, câu trả lời và danh sách `source_ids`.
   - Backend trực tiếp kiểm tra từng `source_id`: Nếu mô hình bịa ra mã nguồn lạ (Hallucinated Source ID) không nằm trong tập `SRC-k` đã cấp, hệ thống tự động loại bỏ mã đó.
   - Toàn bộ thông tin hiển thị của trích dẫn (Tên văn bản, Điều khoản, Trang PDF, Trang in) được backend xây dựng lại trực tiếp từ metadata lưu trữ của chunk tương ứng, hoàn toàn không dựa vào suy đoán của LLM.
3. **Phân loại trạng thái nghiệp vụ chuẩn hóa:**
   - `answered`: Trả lời đầy đủ có căn cứ quy chế hợp lệ.
   - `needs_clarification`: Câu hỏi mơ hồ hoặc thiếu dữ kiện đầu vào để kết luận.
   - `insufficient_evidence`: Câu hỏi học vụ thuộc phạm vi nhưng chưa đủ dữ liệu trong tài liệu hiện tại (không tùy tiện kết luận "trường không quy định").
   - `out_of_scope`: Câu hỏi hoàn toàn ngoài phạm vi đào tạo hoặc ngoài thẩm quyền của quy chế.

### 2.4 Bước D — Dịch vụ FastAPI chuẩn hóa và Giao diện CLI

Triển khai ứng dụng RESTful API tại `backend/main.py`:
- **Quản lý vòng đời (Lifespan):** Khởi tạo mô hình Bi-Encoder và kiểm tra tiền trạm kho tri thức một lần duy nhất lúc khởi động máy chủ (startup), ngăn chặn tình trạng nạp lại mô hình nặng gây nghẽn tài nguyên trên từng request.
- **Endpoint `GET /health`:** Trả về mã HTTP 200 kèm các metadata an toàn (phiên bản collection, số lượng chunk, model revision) khi kho tri thức sẵn sàng; trả về HTTP 503 khi kho chưa sẵn sàng hoặc preflight gặp sự cố.
- **Endpoint `POST /chat`:** Nhận yêu cầu dạng JSON `{"question": "..."}`; xác thực đầu vào bằng Pydantic (từ chối câu rỗng hoặc vượt quá 1000 ký tự với HTTP 422). Trả về phản hồi có cấu trúc an toàn gồm `request_id`, `status`, `answer`, `citations`, và bảng đo thời gian `timings`.
- **Giao diện Dòng lệnh `backend/cli.py`:** Cho phép sinh viên và chuyên viên tra cứu trực tiếp qua terminal bằng câu lệnh đơn lẻ hoặc chế độ hội thoại liên tục (`--interactive`).

---

## 3. Bảng tổng hợp kết quả kiểm thử tự động (35 Tests)

Toàn bộ hệ thống được bảo vệ bởi 35 bài kiểm thử tự động độc lập, thực thi tự động qua lệnh:
```powershell
python -m unittest discover -s tests -p "test_*.py"
```

| STT | Tệp kiểm thử | Số bài test | Nội dung kiểm thử chính | Kết quả |
| :---: | :--- | :---: | :--- | :---: |
| 1 | `tests/test_chunking_and_sources.py` | 5 | Giới hạn Token $\le 256$, tính toàn vẹn 351 source spans, nguồn overlap, độ phủ 51 hàng bảng/142 khoản, tính bất biến Idempotency | **100% ĐẠT** (5/5) |
| 2 | `tests/test_lifecycle_and_regression.py` | 21 | Đối soát 3 chiều Preflight (status, manifest, collection metadata, chunks hash), nạp lại an toàn, cô lập phiên bản, invalidation cache readiness, ánh xạ whitespace regex | **100% ĐẠT** (21/21) |
| 3 | `tests/test_api_and_rag.py` | 9 | `GET /health` (200/503), `POST /chat`, validation HTTP 422, lọc triệt để hallucinated source IDs, chuyển đổi trạng thái nghiệp vụ, bắt lỗi upstream LLM 502/503, cơ chế Lifespan startup | **100% ĐẠT** (9/9) |
| **Tổng** | **Toàn bộ hệ thống** | **35** | **Kiểm tra tự động đa tầng từ dữ liệu, vòng đời, bộ nhớ đến API** | **35/35 ĐẠT (100%)** |

*Thời gian thực thi toàn bộ 35 bài test trên CPU cá nhân: **28.058 giây**.*

---

## 4. Đánh giá thực nghiệm: Phân định Mock Test và Kết nối Gemini Live

Theo đúng nguyên tắc liêm chính học thuật và chỉ thị tại Nhiệm vụ 04:

### 4.1 Kết quả kiểm chứng độc lập (Đã hoàn thành 100%)
- Mọi thành phần phần mềm, cấu trúc dữ liệu, thuật toán đối soát tiền trạm, logic nghiệp vụ, module FastAPI và bộ xác minh trích dẫn Backend đã được hiện thực hoàn chỉnh và vượt qua $100\%$ các bài kiểm thử tự động ngoại tuyến.
- Phép thử Mock Gemini khẳng định tính toàn vẹn của hợp đồng giao tiếp phần mềm (API Contract), chứng minh hệ thống có khả năng lọc sạch các ID giả lập và phản hồi đúng mã trạng thái HTTP.

### 4.2 Tình trạng kết nối Gemini thực tế (Phần còn chờ cấu hình)
- Hiện tại, môi trường chưa được thiết lập biến `GEMINI_API_KEY` của Google AI Studio.
- Nhóm nghiên cứu **tuyệt đối không ngụy tạo kết quả API thành công** và **không sử dụng kết quả chạy thử mock làm bằng chứng đánh giá chất lượng của mô hình ngôn ngữ lớn (LLM)**.
- Khi người dùng cung cấp khóa `GEMINI_API_KEY` hợp lệ trong tệp `.env`, hệ thống sẽ tự động kích hoạt chế độ Live và sẵn sàng cho đợt thử nghiệm định lượng trên 10 ca phát triển (`DEV_10_CAU_QD580.jsonl`) để đo lường độ đúng ngữ nghĩa, mức độ bám sát văn bản quy chế và thời gian đáp ứng thực tế.

---

## 5. Hướng dẫn vận hành hệ thống

### 5.1 Khởi động dịch vụ REST API
```powershell
cd '05_Mã Nguồn Chương Trình'
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
- Truy cập Swagger UI kiểm thử: `http://localhost:8000/docs`
- Endpoint kiểm tra sức khỏe: `GET http://localhost:8000/health`
- Endpoint gửi câu hỏi tra cứu: `POST http://localhost:8000/chat`

### 5.2 Tra cứu qua CLI
```powershell
# Tra cứu nhanh câu hỏi:
python backend/cli.py "Điều kiện học cùng lúc hai chương trình là gì?"

# Chế độ tương tác hội thoại:
python backend/cli.py --interactive
```

---
*Báo cáo được khởi tạo tự động dựa trên kết quả nghiệm thu mã nguồn thực tế ngày 01/11/2026.*
