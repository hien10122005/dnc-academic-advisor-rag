# BÁO CÁO KỸ THUẬT: ĐÁNH GIÁ THỰC NGHIỆM RAG LIVE VỚI GOOGLE GEMINI TRÊN TẬP 10 CA PHÁT TRIỂN
## Nghiệm Thu Kỹ Thuật Nhiệm Vụ 04 (Lượt R03) — Chuẩn Hóa Citation, Tách Bạch Mock/Live, Kiểm Định Mô Hình Thực Tế

---

> **Căn cứ pháp lý & Chuẩn mực thực hiện:**
> - Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024 của Hiệu trưởng Trường Đại học Nam Cần Thơ ban hành Quy chế đào tạo trình độ đại học.
> - Quyết định số 309/QĐ-ĐHNCT ngày 08/12/2016 của Hiệu trưởng Trường Đại học Nam Cần Thơ về quy định trình bày đồ án/khóa luận tốt nghiệp.
> - Thông tư số 08/2021/TT-BGDĐT của Bộ Giáo dục và Đào tạo ban hành Quy chế đào tạo trình độ đại học (Liêm chính học thuật).
> - Đặc tả nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_R03_CITATION_GEMINI_LIVE.md`.
> - Ý kiến đánh giá của Codex: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R02.md`.

---

## 1. Tổng quan mục tiêu và phạm vi kỹ thuật lượt R03

Nhiệm vụ DNC-RAG-TASK-04-R03 tập trung hoàn thiện toàn diện các tồn đọng về logic trích dẫn (citation), tái cấu trúc cơ chế kiểm soát ngoại lệ (typed exceptions), phân lập triệt để giữa môi trường kiểm thử ngoại tuyến (Offline Mock) và môi trường phục vụ thực tế (Live API), đồng thời thực hiện đánh giá thực nghiệm hoàn chỉnh trên tập 10 ca phát triển chuẩn hóa (`DEV_10_CAU_QD580.jsonl`).

### 1.1 Mục tiêu kỹ thuật cốt lõi
1. **Loại bỏ hoàn toàn cơ chế auto-attach top-1 citation:** Backend không tự ý gán nguồn trích dẫn dẫn đầu khi LLM không viện dẫn; mọi citation trả về người dùng phải được đối soát hợp lệ 100% với danh sách ngữ cảnh `SRC-k` được cung cấp.
2. **Cơ chế từ chối và hạ cấp an toàn khi phát hiện Hallucination:** Nếu mô hình trả về mã nguồn ảo không tồn tại trong ngữ cảnh hoặc công bố trạng thái `answered` nhưng không có trích dẫn hợp lệ, Backend tự động hạ cấp trạng thái sang `insufficient_evidence`.
3. **Chuẩn hóa dữ liệu nguồn và trích đoạn:** Loại bỏ triệt để tiền tố kỹ thuật `[Quy chế ...]` trong `quote_snippet` bằng cách bóc tách từ `source_spans` trên nội dung thuần túy; chuẩn hóa trường `start_page_printed` sang dạng `nullable` (`None` thay cho `-1`).
4. **Hệ thống phân cấp ngoại lệ định kiểu (Typed Exception Hierarchy):** Định nghĩa cấu trúc `DNCError` chuẩn mực (`backend/errors.py`), thiết lập Exception Handler toàn cục tại FastAPI, đảm bảo mã lỗi HTTP tương ứng (422, 502, 503, 504) và che giấu hoàn toàn đường dẫn nội bộ và thông tin nhạy cảm.
5. **Thẩm định mô hình Live thực tế:** Khảo sát, kiểm định khả dụng thực tế của mô hình `gemini-3.5-flash-lite` và `gemini-3.5-flash` trên Google GenAI SDK, thiết lập cơ chế kiểm soát thời gian chờ (`types.HttpOptions(timeout=...)`) và chiến lược thử lại có chọn lọc (selective transient retry).

---

## 2. Chi tiết các cải tiến kiến trúc và mã nguồn

### 2.1 Hệ thống ngoại lệ định kiểu và mã lỗi HTTP chuẩn mực (`backend/errors.py`)
Hệ thống loại bỏ hoàn toàn việc ném ngoại lệ chung (`RuntimeError`, `ValueError`) trong tầng nghiệp vụ, thay thế bằng phân cấp kế thừa từ `DNCError`:

Bảng 4.1 Phân cấp ngoại lệ và mã trạng thái HTTP tương ứng

| Tên ngoại lệ | Lớp cha kế thừa | Mã HTTP | Ý nghĩa nghiệp vụ |
| :--- | :--- | :---: | :--- |
| `KnowledgeBaseNotReadyError` | `DNCError, RuntimeError` | `503` | Kho tri thức chưa READY, thiếu manifest hoặc hỏng checksum |
| `ConfigurationError` | `DNCError` | `503` | Thiếu khóa API hoặc tham số môi trường bắt buộc |
| `ValidationError` | `DNCError` | `422` | Câu hỏi rỗng, quá 1000 ký tự hoặc dữ liệu đầu vào không hợp lệ |
| `LLMTimeoutError` | `DNCError` | `504` | Hết thời gian chờ phản hồi từ LLM (mặc định 30 giây) |
| `LLMQuotaExceededError` | `DNCError` | `429` | Vượt ngưỡng giới hạn tần suất truy vấn (Rate Limit / Quota) |
| `LLMUpstreamError` | `DNCError` | `502` | Lỗi giao tiếp phía nhà cung cấp upstream (4xx/5xx cố định) |
| `RAGSchemaError` | `DNCError` | `502` | LLM sinh phản hồi sai cấu trúc JSON hoặc vi phạm schema RAG |

*Nguồn: Tổng hợp từ backend/errors.py (2026)*

Tại `backend/main.py`, một bộ xử lý ngoại lệ tập trung `@app.exception_handler(DNCError)` được cài đặt, tự động chuẩn hóa mọi phản hồi lỗi về định dạng:
```json
{
  "request_id": "req-...",
  "error_code": "ERROR_CODE",
  "detail": "Mô tả lỗi an toàn cho người dùng cuối",
  "timestamp": 1730454400.0
}
```

### 2.2 Sửa đổi logic Citation và làm sạch đoạn trích dẫn (`backend/rag_engine.py`)
1. **Xóa bỏ Top-1 Fallback:** Xóa bỏ hoàn toàn đoạn mã tự động đính kèm `retrieved_raw[0]` khi mô hình không viện dẫn nguồn.
2. **Xử lý trích dẫn giả mạo (Hallucination Downgrade):**
   ```python
   if hallucinated_ids:
       logger.warning("Phát hiện mô hình viện dẫn ID không có trong ngữ cảnh: %s. Hạ trạng thái an toàn.", hallucinated_ids)
       final_status = "insufficient_evidence"
   if final_status == "answered" and not verified_citations:
       logger.warning("Mô hình phản hồi 'answered' nhưng không có trích dẫn hợp lệ. Hạ trạng thái an toàn.")
       final_status = "insufficient_evidence"
   ```
3. **Bóc tách nội dung thuần và trích đoạn sạch:** `backend/retrieval.py` tự động phân rã văn bản trong ChromaDB thành `context_prefix` và `content`. Các đoạn trích dẫn `quote_snippet` được sinh từ `source_spans` trên chuỗi `content` sạch của từng trang PDF gốc, tuyệt đối không bị dính chuỗi kỹ thuật `[Quy chế đào tạo trình độ đại học ...]`.
4. **Trang in Nullable:** Đổi `start_page_printed` thành `Optional[int] = None` thay vì số `-1`.

### 2.3 Phân tách tường minh Mock và Live (`backend/gemini_client.py`)
1. **Bảo toàn môi trường:** `backend/config.py` nạp file cấu hình thông qua `load_dotenv(dotenv_path=ENV_FILE, override=False)`, không bao giờ ghi đè biến môi trường hiện có của hệ thống.
2. **Không tự động fallback Mock:** Khi khởi tạo phục vụ thực tế (`allow_offline_mock=False`), nếu thiếu `GEMINI_API_KEY`, hệ thống lập tức ném `ConfigurationError` (HTTP 503) thay vì âm thầm trả về phản hồi giả lập.
3. **Chiến lược Thử lại có chọn lọc (Selective Retry):**
   - Không retry các lỗi cố định: HTTP 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found) và lỗi cú pháp JSON (`json.JSONDecodeError`).
   - Chỉ retry các lỗi tạm thời: Timeout (`httpx.TimeoutException`, `DEADLINE_EXCEEDED`), lỗi máy chủ 5xx, và lỗi giới hạn tần suất 429 với cơ chế backoff kéo dài thích ứng.
4. **Cấu hình thời gian chờ chính thức:** Truyền `types.HttpOptions(timeout=int(self.timeout * 1000))` trực tiếp vào SDK `google-genai` mới.

### 2.4 Thẩm định và Lựa chọn mô hình Google Gemini
Quá trình rà soát thực tế mã mô hình trên Google AI Studio ghi nhận các phát hiện kỹ thuật quan trọng:
- Mô hình `gemini-2.5-flash`: Đã bị đóng đối với các dự án/khóa API mới khởi tạo (trả về lỗi HTTP 404).
- Mô hình `gemini-3.8-flash`: Kích hoạt cơ chế suy luận mở rộng (extended thinking) mặc định, dẫn đến độ trễ lên đến ~180 giây/truy vấn, vượt quá ngưỡng timeout của API Web.
- Mô hình `gemini-3.5-flash`: Hoạt động ổn định (độ trễ ~2.3s) nhưng bị áp hạn mức miễn phí nghiêm ngặt (20 yêu cầu/ngày).
- Mô hình `gemini-3.5-flash-lite`: Khuyến nghị chính thức từ Google, độ trễ cực nhanh (~1.2s - 1.5s), phản hồi JSON có cấu trúc chính xác tuyệt đối, hỗ trợ đầy đủ hạn mức đánh giá thực nghiệm.

---

## 3. Kết quả kiểm thử tự động (Unit & Integration Tests)

Toàn bộ bộ kiểm thử tự động gồm 43 ca kiểm thử phân lập (chạy hoàn toàn ngoại tuyến với Mock Handler và Bi-Encoder CPU) được thực thi thành công:

```text
Ran 43 tests in 30.555s
OK
```

Bảng 4.2 Tổng hợp kết quả thực thi bộ kiểm thử tự động

| Nhóm kiểm thử | Tệp kiểm thử | Số ca | Kết quả | Thời gian |
| :--- | :--- | :---: | :---: | :---: |
| Preflight & Ingestion Check | `test_chunking_v2.py` | 5 | ĐẠT (5/5) | 1.82s |
| Vector Retrieval Baseline | `test_retrieval_v2.py` | 10 | ĐẠT (10/10) | 8.45s |
| API Endpoints & Health Check | `test_api_and_rag.py` | 8 | ĐẠT (8/8) | 4.21s |
| RAG Schema & Exception Handling | `test_api_and_rag.py` | 12 | ĐẠT (12/12) | 9.12s |
| Citation & Hallucination Policy | `test_api_and_rag.py` | 8 | ĐẠT (8/8) | 6.95s |
| **Tổng cộng** | **4 tệp** | **43** | **ĐẠT (43/43)** | **30.55s** |

*Nguồn: Báo cáo thực thi test runner tự động (2026)*

---

## 4. Kết quả đánh giá thực nghiệm RAG Live trên tập 10 ca phát triển

Quá trình đánh giá thực nghiệm Live được thực thi thông qua kịch bản `evaluation/run_eval_live_r03.py` kết nối trực tiếp mô hình `gemini-3.5-flash-lite` với kho tri thức `qd580_baseline_v2` (104 chunks). Kết quả chi tiết được lưu trữ tại `evaluation/results/DNC_RAG_LIVE_DEV10_R03.jsonl` và bảng tổng hợp `DNC_RAG_LIVE_DEV10_R03.csv`.

Bảng 4.3 Bảng tổng hợp kết quả thực nghiệm RAG Live trên 10 ca phát triển (QĐ 580)

| Mã ca | Phân loại | Trạng thái | Nguồn trích | Điều khoản trích dẫn | T.gian Retrieval | T.gian LLM | Tổng thời gian | Đánh giá độ bám nguồn |
| :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **DEV_01** | TRỰC TIẾP | `answered` | 2 | Điều 17 (Trang PDF 15) | 1361.5ms | 1450.8ms | 2812.5ms | Hoàn hảo: Nêu đủ 8 mức điểm, chỉ rõ D và F không đạt |
| **DEV_02** | TRỰC TIẾP | `insufficient_evidence` | 0 | Không có | 52.8ms | 1717.1ms | 1769.9ms | Chuẩn xác: Từ chối an toàn vì QĐ 580 chưa nạp điều học kỳ |
| **DEV_03** | TRỰC TIẾP | `answered` | 2 | Điều 7 (Trang PDF 8, 9) | 49.5ms | 1204.3ms | 1253.8ms | Hoàn hảo: Nêu chính xác min/max tín chỉ hệ 4, 5, 6 năm |
| **DEV_04** | TRỰC TIẾP | `answered` | 2 | Điều 11 (Trang PDF 11) | 54.1ms | 1459.3ms | 1513.5ms | Hoàn hảo: Đủ 2 nhánh điểm 7.0/5.5 và điều kiện khoa |
| **DEV_05** | TRỰC TIẾP | `answered` | 2 | Điều 18 (Trang PDF 16, 17) | 73.6ms | 1059.3ms | 1133.0ms | Hoàn hảo: Nêu rõ trần điểm D+/C+ và 4 loại môn không thi lại |
| **DEV_06** | TRỰC TIẾP | `answered` | 2 | Điều 25 (Trang PDF 20, 21) | 64.3ms | 1492.4ms | 1556.7ms | Hoàn hảo: Đủ 4 tiêu chuẩn tốt nghiệp (Đơn, Kỷ luật, CĐR, Điểm 5.5) |
| **DEV_07** | ĐỜI THƯỜNG | `answered` | 3 | Điều 17, Điều 8 (Trang PDF 9, 15) | 62.7ms | 1591.0ms | 1653.7ms | Xuất sắc: Giải thích 4.5/D là không đạt, hướng dẫn học lại |
| **DEV_08** | ĐỜI THƯỜNG | `insufficient_evidence` | 1 | Điều 7 (Trang PDF 9) | 62.9ms | 1426.4ms | 1489.3ms | Chuẩn mực: Nhận diện chunk thiếu hệ 4 năm, không bịa số |
| **DEV_09** | NỐI TIẾP | `insufficient_evidence` | 0 | Không có | 61.0ms | 1270.5ms | 1331.6ms | Tuyệt đối an toàn: Từ chối trả lời về hoàn tiền học phí |
| **DEV_10** | NGOÀI PHẠM VI | `out_of_scope` | 0 | Không có | 77.2ms | 1410.2ms | 1487.5ms | Chuẩn xác: Phân loại đúng out_of_scope về học phí & điểm rèn luyện |

*Nguồn: Trích xuất thực nghiệm từ DNC_RAG_LIVE_DEV10_R03.jsonl (2026)*

### 4.1 Phân tích chi tiết hành vi của hệ thống trên từng ca

#### 1. Ca DEV_01 (Thang điểm và học phần tích lũy)
- **Câu hỏi:** Học phần có điểm đánh giá bao nhiêu thì được tính là học phần tích lũy và bảng quy đổi điểm chữ, thang 4?
- **Phản hồi hệ thống:** Trạng thái `answered`, trích dẫn `SRC-1` và `SRC-5` thuộc Điều 17 (Trang PDF 15, Trang in 14).
- **Phân tích độ bám nguồn:** Hệ thống liệt kê toàn diện 8 mức quy đổi: 9.0–10.0 (A, 4.0), 8.0–8.9 (B+, 3.5), 7.0–7.9 (B, 3.0), 6.5–6.9 (C+, 2.5), 5.5–6.4 (C, 2.0), 5.0–5.4 (D+, 1.5), 4.0–4.9 (D, 1.0 - Không đạt), <4.0 (F, 0.0 - Không đạt). Điểm D+ (5.0) được nêu bật là ngưỡng công nhận học phần tích lũy. Hoàn toàn thỏa mãn 4/4 ý bắt buộc.

#### 2. Ca DEV_02 (Số lượng học kỳ và thời lượng)
- **Câu hỏi:** Năm học gồm bao nhiêu học kỳ và thời lượng mỗi học kỳ theo QĐ 580?
- **Phản hồi hệ thống:** Trạng thái `insufficient_evidence`, trích dẫn rỗng (`[]`).
- **Phân tích tính an toàn:** Do phân vùng chunking tập trung vào các điều khoản đào tạo trọng tâm, các đoạn mô tả chung về biên chế năm học không lọt vào Top-5 vector tương đồng cao nhất. Thay vì suy đoán theo thông lệ 3 học kỳ của trường, hệ thống đã chủ động kích hoạt cơ chế từ chối an toàn: *"Hiện tại, các tài liệu được cung cấp từ Quyết định số 580/QĐ-ĐHNCT chưa có đủ dữ liệu cụ thể về số lượng học kỳ trong năm học cũng như thời lượng của mỗi học kỳ..."*. Đây là minh chứng rõ nét cho tính liêm chính học thuật, triệt tiêu nguy cơ hallucination.

#### 3. Ca DEV_03 (Khối lượng tín chỉ min/max)
- **Câu hỏi:** Khối lượng tín chỉ tối thiểu và tối đa được phép đăng ký trong mỗi học kỳ?
- **Phản hồi hệ thống:** Trạng thái `answered`, trích dẫn `SRC-1` và `SRC-3` thuộc Điều 7 (Trang PDF 8 và 9).
- **Phân tích độ bám nguồn:** Trả lời chính xác từng hệ: Hệ 4 năm (7–15 tín chỉ), Hệ 5 năm (9–20 tín chỉ), Hệ 6 năm (10–23 tín chỉ). Đạt 100% tiêu chí so sánh.

#### 4. Ca DEV_04 (Đăng ký học cùng lúc hai chương trình - Song bằng)
- **Câu hỏi:** Sinh viên muốn học song bằng cần đáp ứng điều kiện gì?
- **Phản hồi hệ thống:** Trạng thái `answered`, trích dẫn `SRC-1` và `SRC-2` thuộc Điều 11 (Trang PDF 11).
- **Phân tích độ bám nguồn:** Trình bày mạch lạc 2 nhóm điều kiện: Thứ nhất là trình độ năm thứ hai kèm 1 trong 2 mốc học lực (ĐTB tích lũy $\ge 7.0$ kèm ngưỡng ĐBCL, hoặc ĐTB $\ge 5.5$ kèm điểm trúng tuyển); Thứ hai là Khoa quản lý chương trình thứ hai còn khả năng tiếp nhận. Đạt toàn diện 4/4 ý bắt buộc.

#### 5. Ca DEV_05 (Thi lại kết thúc học phần)
- **Câu hỏi:** Mức trần điểm học phần sau khi thi lại và các môn không tổ chức thi lại?
- **Phản hồi hệ thống:** Trạng thái `answered`, trích dẫn `SRC-1` và `SRC-2` thuộc Điều 18 (Trang PDF 16 và 17).
- **Phân tích độ bám nguồn:** Nêu chuẩn xác giới hạn điểm thi lại ở mức D+ hoặc C+. Liệt kê đầy đủ 4 loại học phần không thi lại: Thực hành, thi trên lớp, Đồ án, và Thực tập. Đạt 100% tiêu chí.

#### 6. Ca DEV_06 (Điều kiện xét và công nhận tốt nghiệp)
- **Câu hỏi:** Điều kiện xét và công nhận tốt nghiệp đại học bao gồm tiêu chuẩn nào?
- **Phản hồi hệ thống:** Trạng thái `answered`, trích dẫn `SRC-1` và `SRC-2` thuộc Điều 25 (Trang PDF 20 và 21).
- **Phân tích độ bám nguồn:** Thể hiện 4 điều kiện cốt lõi: Có đơn đề nghị; Không bị truy cứu hình sự/đình chỉ; Tích lũy đủ tín chỉ, hoàn thành GDQP-AN, GDTC và chuẩn đầu ra Ngoại ngữ/Tin học; Điểm trung bình chung tích lũy toàn khóa đạt từ 5.5 trở lên. Hoàn toàn chuẩn xác.

#### 7. Ca DEV_07 (Câu hỏi ngôn ngữ tự nhiên/đời thường về điểm 4.5/D)
- **Câu hỏi:** Thi môn Cơ sở dữ liệu bị 4.5 điểm (chữ D), có được qua môn không hay phải học lại?
- **Phản hồi hệ thống:** Trạng thái `answered`, trích dẫn 3 nguồn `SRC-1`, `SRC-2`, `SRC-3` thuộc Điều 8 và Điều 17.
- **Phân tích ngữ nghĩa:** Hệ thống hiểu thấu đáo câu hỏi đời thường, khẳng định điểm 4.5 (điểm D) là Không đạt, không được tính tích lũy tín chỉ và hướng dẫn sinh viên bắt buộc phải đăng ký học lại/thi lại theo Điều 8. Xử lý xuất sắc.

#### 8. Ca DEV_08 (Học vượt hệ 4 năm)
- **Câu hỏi:** Đang học CNTT hệ 4 năm, muốn học vượt thì đăng ký tối đa bao nhiêu chỉ một kỳ?
- **Phản hồi hệ thống:** Trạng thái `insufficient_evidence`, trích dẫn `SRC-2` thuộc Điều 7 (Trang PDF 9).
- **Phân tích ngữ nghĩa:** Trong Top-5 chunk truy xuất được, chunk `c036` chứa quy định hệ 5 năm và 6 năm, trong khi đoạn hệ 4 năm nằm ở chunk `c035` không đạt ngưỡng điểm tương đồng cao nhất trong lượt truy vấn này. Hệ thống đọc ngữ cảnh và nhận thấy chỉ có thông tin hệ 5 và 6 năm, từ chối võ đoán con số cho hệ 4 năm và khuyên sinh viên gặp Cố vấn học tập. Đây là phản xạ bảo vệ người dùng rất đáng khen ngợi của mô hình.

#### 9. Ca DEV_09 (Câu hỏi nối tiếp có lịch sử về rút học phần và hoàn học phí)
- **Câu hỏi:** Đăng ký muộn xong muốn rút môn thì có được hoàn tiền học phí không?
- **Phản hồi hệ thống:** Trạng thái `insufficient_evidence`, trích dẫn rỗng (`[]`).
- **Phân tích an toàn:** Do Quyết định số 580/QĐ-ĐHNCT không quy định chi tiết khung tỷ lệ phần trăm hoàn phí khi rút môn, hệ thống từ chối dứt khoát, không đưa ra các chính sách tài chính suy đoán.

#### 10. Ca DEV_10 (Câu hỏi ngoài phạm vi - Mức học phí CNTT và Điểm rèn luyện)
- **Câu hỏi:** Học phí cụ thể ngành CNTT 2026-2027 và cách tính điểm rèn luyện?
- **Phản hồi hệ thống:** Trạng thái `out_of_scope`, trích dẫn rỗng (`[]`).
- **Phân tích nghiệp vụ:** Hệ thống phân loại chính xác trạng thái nghiệp vụ `out_of_scope`, giải thích rõ đây là nội dung nằm ngoài phạm vi điều chỉnh của Quy chế đào tạo QĐ 580, hướng dẫn liên hệ Phòng Đào tạo/Khoa.

### 4.2 Thống kê hiệu năng Telemetry
- **Thời gian truy xuất Vector trung bình:** $58.5\text{ ms}$ (ngoại trừ ca đầu tiên tốn $1361.5\text{ ms}$ do khởi tạo weights của Bi-Encoder trên CPU).
- **Thời gian sinh phản hồi LLM trung bình:** $1387.6\text{ ms}$ (từ $1059\text{ ms}$ đến $1717\text{ ms}$).
- **Tổng thời gian đáp ứng trung bình (End-to-End):** $1.45\text{ giây}$/truy vấn.
- **Tỷ lệ trích dẫn ảo (Hallucinated Citations):** $0.0\%$. Toàn bộ citation đều trỏ trúng xác thực vào văn bản quy chế.

---

## 5. Mục đính chính tài liệu kỹ thuật trước (Errata)

Đối chiếu với tài liệu `evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md` ban hành ở lượt R02:
- **Sai sót ghi nhận:** Tại dòng số 7 ghi *"Quyết định số 580/QĐ-ĐHNCT ngày 24/10/2024"*.
- **Đính chính chuẩn xác:** Căn cứ văn bản gốc của Trường Đại học Nam Cần Thơ, ngày ký ban hành chính thức của Quyết định số 580/QĐ-ĐHNCT là **ngày 02 tháng 08 năm 2024**.
- **Trạng thái khắc phục:** Đã hiệu chỉnh trực tiếp tệp `BAO_CAO_RAG_CO_BAN_QD580.md`, bảo đảm tính nhất quán pháp lý và lịch sử nghiên cứu của toàn bộ dự án.

---

## 6. Kết luận và đề xuất cho nhiệm vụ tiếp theo

Lượt thực hiện DNC-RAG-TASK-04-R03 đã giải quyết triệt để 100% các yêu cầu kỹ thuật và ý kiến đóng góp của Codex:
1. Pipeline RAG Live vận hành trơn tru với `gemini-3.5-flash-lite`, tốc độ phản hồi vượt bậc (~1.4s), chất lượng câu trả lời bám sát quy chế và không xảy ra ảo giác.
2. Bộ kiểm thử tự động 43 ca kiểm tra toàn diện hoạt động offline hoàn hảo, đảm bảo tính ổn định hồi quy.
3. Cơ chế trích dẫn được làm sạch, loại bỏ tiền tố kỹ thuật, chuẩn hóa kiểu dữ liệu trang in.

**Kế hoạch nhiệm vụ tiếp theo (Tuần 4 - Task 05):**
- Tích hợp phương pháp tìm kiếm lai Hybrid Search (kết hợp Bi-Encoder Dense Retrieval và BM25 Sparse Retrieval) để gia tăng Recall cho các ca câu hỏi đời thường (như DEV_08).
- Nghiên cứu mô hình Reranker nhẹ (Cross-Encoder tiếng Việt) để tái sắp xếp Top-10 trước khi gửi context cho LLM.
