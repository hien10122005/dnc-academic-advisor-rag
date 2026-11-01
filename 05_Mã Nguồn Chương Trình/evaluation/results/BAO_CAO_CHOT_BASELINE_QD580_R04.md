# BÁO CÁO KỸ THUẬT NGHIỆM THU BASELINE A (RAG DENSE + GEMINI LIVE)
## QUY CHẾ ĐÀO TẠO ĐẠI HỌC DNC (QĐ 580/QĐ-ĐHNCT NGÀY 02/08/2024)

> **Mã nhiệm vụ:** `DNC-RAG-TASK-04-R04`  
> **Dự án:** `dnc-academic-advisor-rag` (Đồ án 2 — Chuyên ngành Công nghệ thông tin)  
> **Người thực hiện:** AI Assistant (Antigravity)  
> **Ngày thực hiện:** 01/11/2026  
> **Trạng thái:** HOÀN THÀNH — CHỜ CODEX KIỂM TRA  
> **Tài liệu đối chiếu:** Nhận xét độc lập của Codex tại `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R03.md`

---

## 1. TỔNG QUAN VÀ MỤC TIÊU LƯỢT R04

Lượt nhiệm vụ `DNC-RAG-TASK-04-R04` được thực hiện nhằm khắc phục triệt để các tồn tại kỹ thuật và thiếu sót phương pháp luận đã được Codex chỉ ra tại lượt R03, chính thức chốt **Baseline A (Dense Bi-encoder + Google Gemini Live)** làm cơ sở đối chứng khoa học vững chắc trước khi mở rộng sang Task 05 (Hybrid BM25 + Reciprocal Rank Fusion).

### 1.1. Các mục tiêu hoàn thành
1. **Bảo mật phản hồi & Chống rò rỉ đường dẫn nội bộ:**
   - Tách biệt hoàn toàn `public_message` (thông điệp an toàn cho người dùng) và `internal_detail` (chi tiết kỹ thuật chỉ lưu log nội bộ) trong lớp cơ sở `DNCError`.
   - Cơ chế tự động phát hiện và che giấu đường dẫn file cục bộ (Windows paths `E:\`, `C:\`, POSIX paths `/`) và token bí mật.
   - Chuẩn hóa HTTP Status Code của `LLMQuotaExceededError` thành `429 Too Many Requests` (theo RFC 6585 và chuẩn REST API của Google).
   - Viết test probe mô phỏng đường dẫn giả định bí mật (`E:\private\secret-location\manifest.json`) bảo đảm cả `/health` và `/chat` trả về HTTP 503 với thông điệp công khai sạch sẽ.

2. **Kiểm soát chặt chẽ cơ chế Thử lại (Retry) & SDK:**
   - Xây dựng hàm phân loại ngoại lệ `classify_exception(exc)` xác định chính xác bản chất lỗi dựa trên kiểu lớp và mã HTTP:
     - Lỗi lập trình (`ValueError`, `TypeError`, `KeyError`) và cấu trúc schema: Tuyệt đối không retry, gọi SDK đúng 1 lần duy nhất.
     - Lỗi máy khách 4xx (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`): Tuyệt đối không retry, ném `LLMUpstreamError` ngay lập tức.
     - Lỗi tạm thời (Transient): Timeout (408/504), Quota (429), Máy chủ (500/502/503/Mạng): Retry lũy tiến (tối đa `max_retries + 1` lần).
   - Thiết lập `types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1))` trong Google GenAI SDK để vô hiệu hóa retry nội bộ của SDK, trao quyền kiểm soát 100% số lần thử và worst-case timeout cho tầng ứng dụng.
   - Thêm cờ `is_using_live_api` bảo đảm khi tiêm mock handler kiểm thử thì hệ thống luôn báo cáo `is_live_llm=False`.

3. **Cải tiến Trích dẫn Chứng cứ Thực chất (Substantive Quote Snippet):**
   - Nâng cấp thuật toán trích đoạn preview trong `backend/rag_engine.py`: Ưu tiên chọn span nội dung chứng cứ thực chất (bỏ qua span tiêu đề điều khoản ngắn dạng `Điều ...` và header bảng lặp lại) trong khi vẫn bảo toàn tuyệt đối tọa độ span gốc (`chunk_start_char`, `chunk_end_char`, `source_start_char`, `source_end_char`, trang PDF).

4. **Kiểm thử Hồi quy và Kiểm thử Mới (Unit Tests):**
   - Mở rộng bộ kiểm thử tự động từ 43 lên **50 bài test** độc lập (0 fail, 0 error, 0 skip).
   - Bổ sung 7 test case mới cho `classify_exception`, retry logic với fake SDK và sleep mock, path sanitization, `is_using_live_api` và substantive span selection.

5. **Đánh giá Thực nghiệm RAG Live với Rubric Chấm Trung thực:**
   - Chạy toàn bộ 10 ca phát triển (`DEV_01` – `DEV_10`) trên API Live thực tế của Google Gemini (`gemini-3.5-flash-lite`).
   - Lưu trữ đầy đủ run metadata, toàn bộ 5 retrieved contexts (content, spans, similarity), user prompt và câu trả lời vào `evaluation/results/DNC_RAG_LIVE_DEV10_R04.jsonl` và `.csv`.
   - Đánh giá từng ý bắt buộc (mandatory points) theo rubric khách quan (Đạt / Đạt một phần / Thiếu / Sai / Từ chối an toàn do thiếu dữ liệu truy xuất / N/A multi-turn).

---

## 2. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG HỆ THỐNG (UNIT TESTS)

Bộ kiểm thử được thực thi trong môi trường offline hoàn toàn (`HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `GEMINI_API_KEY=""`), sử dụng mock transport và fake SDK, không gọi mạng.

### Bảng 2.1. Phân bổ kết quả kiểm thử tự động R04
| Tệp kiểm thử | Số bài test | Trạng thái | Nội dung trọng tâm |
| :--- | :---: | :---: | :--- |
| `tests/test_chunking_and_sources.py` | 5 | **5/5 OK** | Token limits, Source spans verbatim, Overlap sources, Content coverage, Idempotency. |
| `tests/test_lifecycle_and_regression.py` | 21 | **21/21 OK** | Xác thực 3 chiều kho tri thức (status, manifest, DB count), fingerprint model revision, preflight rejection. |
| `tests/test_api_and_rag.py` | 24 | **24/24 OK** | FastAPI `/health` và `/chat`, khử rò rỉ path `E:\private`, `classify_exception`, retry SDK=1, non-retry 401/404/ValueError, retry 503, hạ hallucination, substantive quote snippet, mock live flag. |
| **Tổng cộng** | **50** | **50/50 OK** | **100% đạt, thời gian chạy: 18.37 giây.** |

---

## 3. ĐÁNH GIÁ THỰC NGHIỆM LIVE R04 (TẬP 10 CA PHÁT TRIỂN)

### 3.1. Thông tin cấu hình thực nghiệm
- **Run ID:** `eval_r04_b01c385b`
- **Mô hình LLM:** `gemini-3.5-flash-lite` (Google AI Studio Live API).
- **Kho tri thức Vector:** `qd580_baseline_v2` (104 chunks, Bi-encoder `bkai-foundation-models/vietnamese-bi-encoder`, revision `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`).
- **Chiến lược truy xuất:** Top-5 Dense Retrieval thuần túy (Cosine Similarity).
- **Thời gian thực hiện:** 01/11/2026 18:10 – 18:13 (141.78 giây, giãn cách 12 giây/request để tuân thủ 15 RPM).

### 3.2. Bảng tổng hợp Telemetry và Độ trễ (Latency Statistics)
| Phân loại | Truy xuất (Retrieval) | Thế hệ LLM (Generation) | Tổng thời gian E2E (Total) |
| :--- | :---: | :---: | :---: |
| **Trung bình toàn bộ 10 ca (Mean)** | 65.88 ms | 1916.81 ms | 1982.75 ms |
| **Trung vị toàn bộ 10 ca (Median)** | 63.07 ms | 1699.59 ms | 1769.82 ms |
| **Trung bình trạng thái ấm (Warm - bỏ ca đầu)** | 63.48 ms | 1929.47 ms | 1993.01 ms |
| **Trung vị trạng thái ấm (Warm - bỏ ca đầu)** | 60.78 ms | 1665.70 ms | 1716.76 ms |
| **Ca đầu tiên (Cold Start)** | 87.48 ms | 1802.81 ms | 1890.37 ms |

> *Ghi chú thống kê:* Đây là số liệu đo lường trực tiếp trên mẫu thực nghiệm 10 ca phát triển nhằm theo dõi hiệu năng hệ thống cục bộ và API, không phải là cam kết SLA cho môi trường production tải cao.

---

## 4. BẢNG ĐỐI CHIẾU CHẤM RUBRIC TRUNG THỰC TỪNG CA PHÁT TRIỂN

Dưới đây là bảng đối chiếu minh bạch giữa câu trả lời thực tế của hệ thống với tiêu chí bắt buộc (mandatory points) trong Gold Standard.

### Bảng 4.1. Chi tiết đánh giá 10 ca phát triển (DEV_01 đến DEV_10)

| Mã ca | Loại câu hỏi | Trạng thái RAG | Số nguồn | Điểm đạt / Tổng | Phân loại Rubric | Nhận xét đối chiếu chi tiết |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **DEV_01** | Trực tiếp | `answered` | 2 | **3/4** (75%) | **Đạt một phần** | Trả lời chính xác ngưỡng tích lũy >= 5.0 (D+); cung cấp đủ 8 mức quy đổi thang 10 sang thang chữ và thang 4; nêu rõ D và F là Không đạt. **Thiếu:** Chưa đề cập quy định chấm điểm làm tròn đến 1 chữ số thập phân. |
| **DEV_02** | Trực tiếp | `insufficient_evidence` | 0 | **0/4** (0%) | **Từ chối an toàn (Retrieval Miss)** | Retriever Dense Top-5 không lấy được chunk chứa Điều 3 khoản 1 & 2 (3 học kỳ/năm, 10-12 tuần học, 2 tuần đánh giá). Hệ thống từ chối an toàn, không bịa nguồn. Đây là lỗi bỏ sót ở khâu truy xuất (Retrieval Miss). |
| **DEV_03** | Trực tiếp | `answered` | 2 | **3/3** (100%) | **Đạt hoàn toàn** | Nêu chính xác định mức tín chỉ tối thiểu/tối đa cho cả 3 chương trình: 4 năm (7-15 TC), 5 năm (9-20 TC), 6 năm (10-23 TC) theo Điều 7. |
| **DEV_04** | Trực tiếp | `answered` | 2 | **3/4** (75%) | **Đạt một phần** | Nêu đúng điều kiện năm 2; đúng 2 phương án ĐTB tích lũy (>=7.0 hoặc >=5.5 kèm ngưỡng tuyển sinh); đúng khả năng tiếp nhận của khoa 2. **Thiếu:** Bỏ sót quy định về thời điểm (đầu mỗi học kỳ) và thủ tục qua Phòng QLĐT trình BGH. |
| **DEV_05** | Trực tiếp | `answered` | 2 | **2/3** (66.7%) | **Đạt một phần** | Nêu chính xác giới hạn điểm sau thi lại ở mức D+ hoặc C+; liệt kê đầy đủ 4 loại học phần không tổ chức thi lại (Thực hành, thi trên lớp, Đồ án, Thực tập). **Thiếu:** Chưa đề cập nghĩa vụ đóng lệ phí thi lại / ngoại lệ hoãn thi hợp lệ. |
| **DEV_06** | Trực tiếp | `answered` | 2 | **4/4** (100%) | **Đạt hoàn toàn** | Đầy đủ 4 điều kiện tốt nghiệp Điều 25: Có đơn đề nghị; Không bị truy cứu TNHS/kỷ luật; Tích lũy đủ học phần, GDQP-AN, GDTC, CĐR ngoại ngữ & CNTT; ĐTBCTL toàn khóa >= 5.5. |
| **DEV_07** | Đời thường | `answered` | 2 | **2/4** (50%) | **Đạt một phần** | Xác định đúng điểm 4.5 (điểm D) là Không đạt và không được tích lũy tín chỉ. **Thiếu & Khẳng định phiến diện:** Kết luận "bắt buộc phải đăng ký học lại", bỏ sót nhánh giải quyết thi phụ (thi lại) nếu học phần có tổ chức thi lại, và chưa nêu phương án học học phần thay thế/tương đương. |
| **DEV_08** | Đời thường | `insufficient_evidence` | 1 | **0/3** (0%) | **Từ chối an toàn (Retrieval Miss)** | Dense Retriever chỉ mang về chunk quy định hệ 5 năm và 6 năm, bỏ sót dòng quy định hệ 4 năm (7-15 TC). LLM nhận diện không đủ dữ liệu hệ 4 năm nên từ chối an toàn. Đây là hạn chế truy xuất của Dense Bi-encoder. |
| **DEV_09** | Nối tiếp lịch sử | `insufficient_evidence` | 0 | **N/A** | **Single-turn Only (Từ chối an toàn)** | Trả lời chính xác giới hạn của QĐ 580 (không có điều khoản về thủ tục rút học phần và hoàn tiền học phí). Hệ thống hiện tại là kiến trúc Single-turn Stateless (chưa có session memory), do đó tiêu chí multi-turn được phân loại N/A. |
| **DEV_10** | Ngoài phạm vi | `out_of_scope` | 1 | **3/3** (100%) | **Đạt hoàn toàn (Từ chối đúng)** | Từ chối chính xác câu hỏi về mức học phí chi tiết năm 2026-2027 và cách tính điểm rèn luyện; trích dẫn Điều 3 khoản 4 nêu rõ đơn giá do Chủ tịch Hội đồng trường quy định; không võ đoán trường không có quy định. |

### 3.3. Tổng kết phân loại năng lực hệ thống
- **Tỷ lệ ca đạt hoàn toàn (Full Pass):** 3/10 ca (30%).
- **Tỷ lệ ca đạt một phần (Partial Pass):** 4/10 ca (40%).
- **Tỷ lệ từ chối an toàn do thiếu dữ liệu truy xuất (Retrieval Miss):** 2/10 ca (20% - `DEV_02`, `DEV_08`).
- **Tỷ lệ ngoài phạm vi / Single-turn:** 1/10 ca (10% - `DEV_09`).
- **Tỷ lệ bịa đặt nguồn / trích dẫn ảo (Hallucination Rate):** **0%** (0/10 ca viện dẫn nguồn sai hoặc ngoài ngữ cảnh).

---

## 5. BÀI HỌC KỸ THUẬT VÀ ĐỊNH HƯỚNG TASK 05 (HYBRID BM25 + RRF)

### 5.1. Phân tích nguyên nhân Retrieval Miss ở Baseline A
Hai ca `DEV_02` và `DEV_08` là minh chứng thực tế rõ ràng cho thấy giới hạn cố hữu của phương pháp **Dense Semantic Retrieval thuần túy**:
- Ở `DEV_02`: Các câu hỏi mang tính khái niệm cơ bản ("tổ chức năm học gồm bao nhiêu học kỳ", "thời lượng mỗi học kỳ") có khoảng cách ngữ nghĩa (semantic distance) khá xa so với câu văn pháp lý ("Mỗi năm học có 03 học kỳ..."), dẫn đến điểm cosine similarity bị phân tán sang các điều khoản về đăng ký học tập.
- Ở `DEV_08`: Câu hỏi đời thường ("hệ 4 năm", "học vượt") bị mô hình Bi-encoder bắt nhầm vào các đoạn văn bản có mật độ dày đặc về "chương trình 5 năm", "chương trình 6 năm", làm trôi mất chunk chứa dòng quy định của hệ 4 năm ra khỏi Top-5.

### 5.2. Đề xuất kỹ thuật cho Task 05
Kết quả này khẳng định tính đúng đắn và cấp thiết của kế hoạch triển khai **Task 05: BM25 + Reciprocal Rank Fusion (RRF)**:
1. Bộ truy xuất từ khóa BM25 (với tokenizer tiếng Việt chuẩn) sẽ khớp trực tiếp các từ khóa chính xác như `"03 học kỳ"`, `"10 đến 12 tuần"`, `"chương trình học 04 năm"`, `"15 tín chỉ"`.
2. Thuật toán RRF sẽ dung hợp điểm số xếp hạng giữa BM25 và Dense Bi-encoder, bảo đảm đưa các đoạn trích chứa đúng dữ kiện vào Top-5 ngữ cảnh.
3. Chốt Baseline A ở lượt R04 cung cấp số liệu đối chứng chính xác để chứng minh mức độ cải thiện của Hybrid Retrieval trong Task 05.

---

## 6. KẾT LUẬN VÀ BÀN GIAO

Hệ thống RAG Backend và bộ kiểm thử đã hoàn thành toàn bộ các yêu cầu sửa lỗi của Codex tại lượt R03:
- Không rò rỉ đường dẫn nội bộ.
- Phân loại lỗi và kiểm soát retry SDK deterministically.
- Trích đoạn preview hiển thị chứng cứ thực chất.
- 50 bài unit test chạy qua hoàn toàn trong môi trường offline.
- Báo cáo đánh giá 10 ca live trung thực, minh bạch, lưu trữ đầy đủ run metadata và artifacts tái lập.
- Baseline A đã hoàn tất và sẵn sàng để Codex kiểm tra nghiệm thu.
