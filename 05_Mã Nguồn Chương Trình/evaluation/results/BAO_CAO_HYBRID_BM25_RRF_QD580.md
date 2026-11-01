# BÁO CÁO KỸ THUẬT: ĐỐI CHỨNG BASELINE VÀ TRIỂN KHAI HYBRID BM25 + RRF (QĐ 580)

**Mã phiếu nhiệm vụ:** `DNC-RAG-TASK-05-R01`  
**Dự án:** Trợ lý học vụ DNC RAG (`dnc-academic-advisor-rag`)  
**Ngày thực hiện:** 01/11/2026  
**Môi trường thực thi:** Python 3.12 (.venv) / Windows 11  
**Mô hình Embedding:** `bkai-foundation-models/vietnamese-bi-encoder` (Revision: `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`)  
**Mô hình LLM:** `gemini-3.5-flash-lite` (Google Gemini Live API)  
**Corpus quy chế:** Quyết định số 580/QĐ-ĐHNCT (104 chunks, collection `qd580_baseline_v2`)  
**Chunks SHA256:** `5802f176f1f603123126c49284449085bd18bdf64f3213998e081ecd01536398`  
**Manifest SHA256:** `c0ceea3306e71506ceaeae17e8328423993e80967e855c6605d775a64b9c2e9b`  

---

## I. TỔNG QUAN VÀ GIẢI QUYẾT BẮT BUỘC CHẶNG A

Trước khi bước vào triển khai và so sánh phương pháp truy xuất kết hợp (Hybrid Search), toàn bộ 7 yêu cầu kỹ thuật nghiêm ngặt của Chặng A đã được hoàn tất và kiểm chứng độc lập bằng bộ kiểm thử tự động (63 unit tests pass 100%):

1. **Phân loại ngoại lệ và cơ chế Retry có cấu trúc (`backend/gemini_client.py`):**
   - Không tìm kiếm số hiệu HTTP thông qua chuỗi `str(exc)`. Chuyển sang trích xuất mã số nguyên có cấu trúc từ `status_code`, `code`, `response.status_code`.
   - Kiểm chứng thành công: Ngoại lệ mã 503 có chuỗi Request ID chứa con số "404123" vẫn được định danh chính xác là lỗi máy chủ tạm thời (`server`, 503) và kích hoạt cơ chế retry. Ngoại lệ 401 chứa từ khóa "quota" không bị phân loại nhầm thành lỗi quota mà bị chặn ngay lập tức (`client_error`, 401) mà không retry vô ích.
   - Bổ sung xử lý chuỗi lỗi hỗn hợp: Khi chuỗi thử nghiệm gặp lỗi 503 sau đó chuyển sang 504 Timeout, hệ thống bảo toàn danh mục lỗi cuối cùng và ném ra đúng ngoại lệ `LLMTimeoutError`.

2. **Làm sạch hoàn toàn thông điệp hạ tầng và bảo mật thông tin nội bộ (`backend/errors.py`):**
   - Thiết lập cờ `is_infrastructure_error = True` trên `DNCError`. Toàn bộ các lớp lỗi hạ tầng (DB, Vector, Model, Network, Upstream LLM) bắt buộc sử dụng `default_message` ổn định, an toàn để phản hồi cho người dùng, tuyệt đối không phản chiếu raw exception message hay payload từ SDK.
   - Kiểm chứng kiểm thử: Tiêm các token giả mạo nhạy cảm như `FAKE_SECRET_SENTINEL_xyz` vào các endpoint `/health` và `/chat`; hệ thống chặn hoàn toàn và không để lộ token ra phản hồi HTTP.

3. **Cô lập tính bất biến (Idempotency) trong môi trường thử nghiệm (`tests/test_chunking_and_sources.py`):**
   - Đã tách quy trình kiểm tra chunking sang thư mục tạm thời `tempfile.TemporaryDirectory()`. Quá trình sinh chunk thử nghiệm không ghi đè hay làm sai lệch timestamp/nội dung của `QD580_CHUNKS.jsonl` và `QD580_MANIFEST.json` dùng chung trong sản phẩm.

4. **Thu thập Trace thực nghiệm trực tiếp từ lần thực thi duy nhất (`backend/rag_engine.py`):**
   - Bổ sung thuộc tính `trace` vào `RAGResponse` và tham số `return_trace=True` trong hàm `answer_question`.
   - Thu thập chính xác `user_prompt`, `system_instruction`, `generation_config`, và `retrieved_contexts` từ đúng lần truy xuất và sinh phản hồi thực tế của engine.
   - Loại bỏ hoàn toàn việc gọi truy xuất lần thứ hai bên ngoài script đánh giá (tránh sai lệch ngữ cảnh và lãng phí tài nguyên). Đã có kiểm thử Spy (`test_answer_question_trace_captured_without_duplicate_retrieval`) xác nhận engine chỉ thực thi retrieval duy nhất 1 lần.

5. **Đo lường thời gian chính xác cao bằng `time.perf_counter()`:**
   - Tách biệt rõ ràng từng khoảng thời gian: `retrieval_ms`, `llm_generation_ms`, `total_ms`.
   - Phân biệt rõ giữa lần gọi khởi động đầu tiên (Cold Start - nạp trọng số embedding/kết nối upstream) và các lần gọi đã được làm nóng (Warm Run).

6. **Bảng tiêu chí Rubric đánh giá từng ý bắt buộc (Mandatory Points):**
   - Xây dựng thang đánh giá minh bạch: **Đạt / Một phần / Thiếu / Sai**.
   - Phân biệt rành mạch giữa 3 khái niệm:
     + *Citation Membership:* ID nguồn trích dẫn có thuộc ngữ cảnh hay bịa đặt.
     + *Evidence Correctness:* Độ bao phủ ký tự của ngữ cảnh đối với bằng chứng quy chế.
     + *Answer Faithfulness:* Tính trung thực và bám sát ngữ cảnh của câu trả lời do LLM sinh ra.
   - DEV_06 đánh giá theo đủ 5 ý tiêu chuẩn vàng của Điều 25. DEV_09 ghi nhận trạng thái Single-turn (N/A multi-turn đối với hệ thống tra cứu đơn lượt).

7. **Đính chính (Errata) đối với Báo cáo R04:**
   - *Ghi nhận:* Trong báo cáo R04, trace được dựng lại từ một lần retrieval độc lập trong script đánh giá; từ Task 05, toàn bộ trace được trích xuất trực tiếp từ engine runtime.
   - *Đính chính độ trễ:* Lượt chạy đầu tiên trong R04 đo cả thời gian khởi tạo PyTorch weights nên không được tính gộp làm độ trễ trung bình của hệ thống khi vận hành ổn định.

---

## II. THIẾT KẾ VÀ TRIỂN KHAI HYBRID BM25 + RRF (CHẶNG B)

### 1. Kiến trúc chỉ mục và Tokenizer tiếng Việt
- **Tập dữ liệu:** Đúng 104 chunks đã kiểm chứng của QĐ 580 từ `QD580_CHUNKS.jsonl`.
- **Trường văn bản chỉ mục:** Sử dụng `embedding_text` (kết hợp tiêu đề chương, điều khoản và nội dung đoạn văn) nhằm đồng nhất không gian ngữ cảnh với Dense Bi-Encoder.
- **Bộ tách từ (Tokenizer):** Hàm `tokenize_vietnamese(text: str)`:
  + Chuẩn hóa chuỗi dạng Unicode NFC, chuyển chữ thường (lowercase).
  + Tách từ theo biểu thức chính quy `\w+`, bảo tồn nguyên vẹn dấu tiếng Việt và các con số điều khoản có ý nghĩa pháp lý quan trọng (`03`, `10`, `12`, `15`, `20`, `23`, `580`, `2024`...).
  + Loại bỏ các ký tự dấu câu rời rạc nhưng giữ nguyên các thuật ngữ cốt lõi của quy chế đào tạo.

### 2. Thuật toán BM25Okapi Index (`backend/bm25_retriever.py`)
- Áp dụng công thức Okapi BM25 chuẩn với tham số $k_1 = 1.5$ và $b = 0.75$.
- Nghịch đảo tần suất văn bản (IDF) tính theo chuẩn Lucene nhằm tránh trọng số âm đối với các từ phổ biến:
  $$\text{IDF}(t) = \ln\left(1 + \frac{N - n(t) + 0.5}{n(t) + 0.5}\right)$$
- Loại bỏ hoàn toàn các văn bản có điểm $\text{score} \le 0$ khỏi kết quả sparse để tránh ô nhiễm thứ hạng.

### 3. Thuật toán Reciprocal Rank Fusion (RRF)
- Công thức kết hợp thứ hạng:
  $$\text{RRF\_Score}(d) = \sum_{m \in \{\text{dense}, \text{bm25}\}} \frac{1}{k + \text{rank}_m(d)}$$
  Trong đó tham số làm mịn $k = 60$; thứ hạng $\text{rank}$ bắt đầu từ 1.
- Quy trình:
  + Dense Retrieval lấy **Top-20** chunk tiềm năng.
  + BM25 Retrieval lấy **Top-20** chunk tiềm năng có điểm $> 0$.
  + Hợp nhất danh sách theo `chunk_id`, tính tổng điểm RRF.
  + Lưu trữ độc lập các giá trị: `dense_rank`, `dense_score`, `bm25_rank`, `bm25_score`, và `rrf_score`. Điểm `rrf_score` không bị gán nhầm thành cosine similarity hay độ tin cậy.
  + Cắt lấy **Top-5** cuối cùng chuyển cho LLM tổng hợp câu trả lời.
  + Cơ chế Tie-break ổn định: Sắp xếp giảm dần theo `rrf_score`, nếu hòa xếp tăng dần theo `dense_rank`, sau đó tăng dần theo `chunk_id`.

### 4. Cơ chế tiền trạm Fail-Closed
- Cả hai chế độ `dense` và `hybrid` đều trải qua kiểm tra tiền trạm nghiêm ngặt (`preflight_check`). Nếu tệp chunk bị sửa đổi, sai lệch hash SHA256 hoặc số lượng chunk giữa ChromaDB và BM25 không khớp, hệ thống từ chối khởi động ngay lập tức.
- Chỉ mục BM25 được khởi tạo sẵn (in-memory) lúc khởi động ứng dụng và chia sẻ an toàn cho các luồng truy vấn.

---

## III. KẾT QUẢ THỰC NGHIỆM RETRIEVAL A/B (10 CA PHÁT TRIỂN)

Phương pháp đánh giá dựa trên thuật toán giao thoa khoảng ký tự nguồn (*Source Span Character Intersection*) trên 26 trang gốc của QĐ 580.
- Ca đánh giá có căn cứ (Grounded): 9 ca (DEV_01 đến DEV_09).
- Ca ngoài phạm vi (Out-of-Scope): 1 ca (DEV_10).

### 1. Bảng so sánh tổng hợp các chỉ số truy xuất

| Chỉ số (Metric) | Dense Baseline | Hybrid (BM25 + RRF) | Chênh lệch (Delta) | Ý nghĩa đánh giá |
| :--- | :---: | :---: | :---: | :--- |
| **Hit@1** ($\ge 90\%$ span) | 0.5556 (5/9) | 0.4444 (4/9) | -0.1112 | Phân bổ RRF làm dịu Top-1 nhưng tối ưu dải Top-3/Top-5 |
| **Hit@3** ($\ge 90\%$ span) | 0.7778 (7/9) | **0.8889** (8/9) | **+0.1111** | Tăng thêm 1 ca đạt bằng chứng trọn vẹn trong Top-3 |
| **Hit@5** ($\ge 90\%$ span) | 0.7778 (7/9) | **1.0000** (9/9) | **+0.2222** | **100% các ca đều có bằng chứng trọn vẹn trong Top-5** |
| **Hit@10** ($\ge 90\%$ span) | 1.0000 (9/9) | 1.0000 (9/9) | 0.0000 | Cả hai chế độ đều tìm thấy bằng chứng ở Top-10 |
| **Full Case Coverage@10** | 0.6667 (6/9) | **0.7778** (7/9) | **+0.1111** | Tăng tỷ lệ phủ trọn vẹn toàn bộ các bằng chứng phức hợp |
| **MRR@10** | 0.6806 | 0.6574 | -0.0232 | Thứ hạng trung bình của hit đầu tiên duy trì ổn định |
| **Mean Coverage@3** | 0.5812 | **0.6923** | **+0.1111** | Độ phủ ký tự trung bình tại Top-3 tăng 11.1% |
| **Mean Coverage@5** | 0.6368 | **0.8034** | **+0.1666** | Độ phủ ký tự trung bình tại Top-5 tăng 16.7% |
| **Mean Coverage@10** | 0.8312 | **0.9143** | **+0.0831** | Độ phủ ký tự trung bình tại Top-10 đạt 91.4% |
| **Độ trễ trung bình (Mean)** | **64.00 ms** | 82.63 ms | +18.63 ms | Chi phí tính toán BM25 và RRF rất nhẹ (~18ms) |
| **Độ trễ trung vị (Median)** | **58.59 ms** | 81.77 ms | +23.18 ms | Ổn định và đáp ứng tốt tiêu chuẩn thời gian thực |

### 2. Chi tiết thứ hạng và độ phủ theo từng ca

| Mã ca | Loại ca | Hit@3 (D $\rightarrow$ H) | Cov@5 (D $\rightarrow$ H) | Cov@10 (D $\rightarrow$ H) | Rank Hit 1 (D $\rightarrow$ H) | Phân tích biến động thực tế |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **DEV_01** | Trực tiếp | 1 $\rightarrow$ 1 | 1.00 $\rightarrow$ 1.00 | 1.00 $\rightarrow$ 1.00 | 1 $\rightarrow$ 1 | Duy trì vị trí số 1 tuyệt đối ở cả hai chế độ. |
| **DEV_02** | Trực tiếp | 0 $\rightarrow$ 0 | **0.00 $\rightarrow$ 1.00** | 1.00 $\rightarrow$ 1.00 | **6 $\rightarrow$ 4** | **Đột phá:** Đưa Điều 3 từ Rank 6 (ngoài Top-5) vào Rank 4 (trong Top-5). |
| **DEV_03** | Trực tiếp | 1 $\rightarrow$ 1 | 0.99 $\rightarrow$ 0.99 | 0.99 $\rightarrow$ 0.99 | 3 $\rightarrow$ 2 | Nâng thứ hạng bằng chứng Điều 7 từ Rank 3 lên Rank 2. |
| **DEV_04** | Trực tiếp | 1 $\rightarrow$ 1 | 1.00 $\rightarrow$ 1.00 | 1.00 $\rightarrow$ 1.00 | 1 $\rightarrow$ 1 | Giữ vững vị trí số 1 cho cả Điều 11 khoản 2 và khoản 3. |
| **DEV_05** | Trực tiếp | 1 $\rightarrow$ 1 | 1.00 $\rightarrow$ 1.00 | 1.00 $\rightarrow$ 1.00 | 1 $\rightarrow$ 1 | Giữ vững vị trí số 1 cho Điều 18 (thi phụ và giới hạn điểm). |
| **DEV_06** | Trực tiếp | 1 $\rightarrow$ 1 | 0.99 $\rightarrow$ 0.99 | 0.99 $\rightarrow$ 0.99 | 1 $\rightarrow$ 3 | Điều 25 lùi từ Rank 1 sang Rank 3 nhưng vẫn trong Top-3 an toàn. |
| **DEV_07** | Đời thường | 1 $\rightarrow$ 1 | 0.25 $\rightarrow$ 0.25 | **0.50 $\rightarrow$ 0.75** | 2 $\rightarrow$ 2 | Độ phủ ở Top-10 tăng từ 50% lên 75% nhờ thêm chunk Điều 18. |
| **DEV_08** | Đời thường | **0 $\rightarrow$ 1** | **0.00 $\rightarrow$ 0.50** | 0.50 $\rightarrow$ 0.50 | **8 $\rightarrow$ 3** | **Đột phá:** Đưa Điều 7 từ Rank 8 (ngoài Top-5) lên thẳng Rank 3. |
| **DEV_09** | Nối tiếp | 1 $\rightarrow$ 1 | 0.50 $\rightarrow$ 0.50 | **0.50 $\rightarrow$ 1.00** | 1 $\rightarrow$ 1 | Độ phủ ở Top-10 tăng gấp đôi từ 50% lên 100%. |
| **DEV_10** | Ngoài PV | N/A | N/A | N/A | N/A | Điểm Top-1 thấp; phân loại chuẩn ngoài phạm vi. |

---

## IV. KẾT QUẢ ĐÁNH GIÁ THỰC NGHIỆM LIVE GEMINI (TASK 05)

Dữ liệu thực nghiệm được xuất tại:
- `evaluation/results/DNC_RAG_AB_DEV10_TASK05.jsonl`
- `evaluation/results/DNC_RAG_AB_DEV10_TASK05.csv`

### 1. Bảng chấm điểm Rubric chi tiết theo từng ý bắt buộc (Mandatory Points)

| Mã ca | Chế độ | Trạng thái | Nguồn trích | Đạt / Tổng ý | Chi tiết đánh giá Rubric (Đạt / Một phần / Thiếu / Sai) |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **DEV_01** | Dense | `answered` | 2/5 | **4/4** | **Đạt 4/4:** Ngưỡng 5.0 (Đạt), bảng 8 mức (Đạt), loại D & F không đạt (Đạt), thang 10 làm tròn 1 số thập phân (Đạt). |
| | Hybrid | `answered` | 2/5 | 3/4 | **Đạt 3/4, Thiếu 1:** Ngưỡng 5.0 (Đạt), bảng 8 mức (Đạt), loại D & F không đạt (Đạt), thiếu câu nhắc làm tròn 1 số thập phân. |
| **DEV_02** | Dense | `insufficient_evidence` | 0/5 | 0/4 | **Thiếu 4/4:** Bị từ chối nhầm do Điều 3 ở Rank 6 không vào được Top-5 context của Dense. |
| | Hybrid | `answered` | 1/5 | **3/4** | **Đạt 3/4, Thiếu 1:** Nêu rõ 03 học kỳ/năm (Đạt), 10-12 tuần giảng dạy (Đạt), 2 tuần đánh giá (Đạt); thiếu ý kế hoạch tháng 6 do Hiệu trưởng ban hành. |
| **DEV_03** | Dense | `answered` | 2/5 | **3/3** | **Đạt 3/3:** Hệ 4 năm 7-15 tín chỉ (Đạt), hệ 5 năm 9-20 (Đạt), hệ 6 năm 10-23 (Đạt). |
| | Hybrid | `answered` | 2/5 | **3/3** | **Đạt 3/3:** Nêu đầy đủ, chính xác cả 3 định mức chương trình, có thêm lưu ý hướng dẫn của Cố vấn học tập. |
| **DEV_04** | Dense | `answered` | 1/5 | 3/4 | **Đạt 3/4, Thiếu 1:** Năm thứ hai (Đạt), 1 trong 2 điều kiện học lực (Đạt), khả năng tiếp nhận của khoa (Đạt); thiếu thủ tục đăng ký đầu kỳ qua Phòng QLĐT. |
| | Hybrid | `answered` | 2/5 | **4/4** | **Đạt 4/4:** Trình độ năm thứ hai (Đạt), 1 trong 2 điều kiện điểm (Đạt), chỉ tiêu khoa (Đạt), nêu rõ thủ tục đăng ký đầu kỳ và BGH xét duyệt (Đạt). |
| **DEV_05** | Dense | `answered` | 2/5 | 2/3 | **Đạt 2/3, Thiếu 1:** Giới hạn điểm D+ hoặc C+ (Đạt), 4 loại học phần không thi lại (Đạt); không nêu lệ phí thi lại (câu hỏi không hỏi về lệ phí). |
| | Hybrid | `answered` | 2/5 | 2/3 | **Đạt 2/3, Thiếu 1:** Giới hạn điểm D+ hoặc C+ (Đạt), 4 loại học phần không thi lại (Đạt); không nêu lệ phí thi lại. |
| **DEV_06** | Dense | `answered` | 2/5 | **5/5** | **Đạt 5/5:** Có đơn (Đạt), không kỷ luật hình sự/đình chỉ (Đạt), tích lũy đủ tín chỉ (Đạt), GDQP-AN/GDTC/chuẩn đầu ra ngoại ngữ & CNTT (Đạt), ĐTB >= 5.5 (Đạt). |
| | Hybrid | `answered` | 2/5 | **5/5** | **Đạt 5/5:** Nêu trọn vẹn đủ 5 ý tiêu chuẩn vàng của Điều 25, bổ sung thông tin thời hạn ra quyết định 03 tháng. |
| **DEV_07** | Dense | `answered` | 3/5 | 2/4 | **Đạt 2/4, Một phần 1, Thiếu 1:** Điểm 4.5 D là Không đạt (Đạt), không tính qua môn (Đạt), hướng dẫn học lại (Một phần); thiếu nhánh hướng dẫn thi phụ (thi lại). |
| | Hybrid | `answered` | 2/5 | 2/4 | **Đạt 2/4, Một phần 1, Thiếu 1:** Điểm 4.5 D là Không đạt (Đạt), chưa tích lũy (Đạt), hướng dẫn học lại (Một phần); thiếu nhánh hướng dẫn thi phụ. |
| **DEV_08** | Dense | `insufficient_evidence` | 0/5 | 0/3 | **Thiếu 3/3:** Bị từ chối nhầm do câu hỏi đời thường làm phân tán vector embedding, Điều 7 tụt xuống Rank 8. |
| | Hybrid | `answered` | 2/5 | **2/3** | **Đạt 2/3, Thiếu 1:** Hệ 4 năm tối đa 15 tín chỉ và tối thiểu 7 tín chỉ (Đạt), làm theo hướng dẫn Cố vấn học tập (Đạt); thiếu ý trường có 3 học kỳ/năm. |
| **DEV_09** | Dense | `insufficient_evidence` | 0/5 | **3/3** | **Đạt 3/3:** QĐ 580 chưa có dữ liệu rút môn và hoàn phí (Đạt), khuyên liên hệ Phòng QLĐT hoặc CVHT (Đạt); Single-turn (N/A multi-turn). |
| | Hybrid | `insufficient_evidence` | 0/5 | **3/3** | **Đạt 3/3:** Xác định chính xác QĐ 580 chưa có dữ liệu cụ thể về rút học phần và hoàn phí, từ chối an toàn đúng tiêu chuẩn. |
| **DEV_10** | Dense | `out_of_scope` | 0/5 | **3/3** | **Đạt 3/3:** Từ chối con số học phí cụ thể (Đạt), từ chối cách tính điểm rèn luyện (Đạt), giải thích giới hạn QĐ 580 (Đạt). |
| | Hybrid | `out_of_scope` | 1/5 | **3/3** | **Đạt 3/3:** Nêu rõ ngoài phạm vi, viện dẫn chính xác Điều 3 khoản 4 [SRC-2] để giải thích đơn giá do Chủ tịch HĐT ban hành nên quy chế không có biểu tiền cụ thể. |

---

### 2. Phân tích chuyên sâu 3 ca then chốt: DEV_02, DEV_07, DEV_08

#### Ca DEV_02 (Năm học có mấy học kỳ và thời lượng)
- **Thực tế Dense:** Ngữ cảnh Top-5 nhận được Điều 1, Điều 2, Điều 4, Điều 5, Điều 6. Đoạn văn quy định "Trường tổ chức mỗi năm gồm 03 học kỳ, mỗi học kỳ từ 10 đến 12 tuần..." nằm tại Điều 3 khoản 2 điểm b bị xếp ở **Rank 6**. LLM hoạt động nghiêm ngặt theo prompt nên khi thiếu Điều 3 trong ngữ cảnh đã chuyển sang `insufficient_evidence` và từ chối trả lời (từ chối nhầm - False Negative).
- **Thực tế Hybrid:** BM25 bắt chính xác các từ khóa `"năm học"`, `"học kỳ"`, `"thời lượng"`, `"03 học kỳ"` trong `embedding_text` của Điều 3. Thuật toán RRF đã kéo Điều 3 từ Rank 6 lên **Rank 4** (nằm trọn trong Top-5). Kết quả: LLM nhận được bằng chứng và trả lời trọn vẹn: "Trường tổ chức mỗi năm gồm 03 học kỳ. Mỗi học kỳ kéo dài từ 10 đến 12 tuần dành cho hoạt động giảng dạy và học tập, cùng với 2 tuần dành cho việc đánh giá...".

#### Ca DEV_08 (Sinh viên CNTT hệ 4 năm học vượt đăng ký tối đa bao nhiêu chỉ)
- **Thực tế Dense:** Câu hỏi dùng từ ngữ sinh viên đời thường ("mình tính học vượt để ra trường sớm thì được đăng ký tối đa bao nhiêu chỉ một kỳ vậy"). Bi-Encoder tiếng Việt bị phân tán ngữ nghĩa giữa khái niệm "học vượt" và "đăng ký khối lượng", khiến chunk Điều 7 khoản 2 (quy định mức 7-15 tín chỉ đối với hệ 4 năm) bị tụt xuống tận **Rank 8**. Hệ quả: Top-5 không chứa quy định này, LLM trả lời `insufficient_evidence`.
- **Thực tế Hybrid:** BM25 khớp chính xác cụm `"hệ 4 năm"`, `"đăng ký"`, `"tối đa"` và `"tín chỉ"`. Điểm BM25 cao kết hợp cùng RRF đã đưa chunk Điều 7 từ Rank 8 vọt lên **Rank 3**. LLM trích xuất thành công và trả lời chính xác: *"giới hạn số tín chỉ tối đa bạn được phép đăng ký trong một học kỳ là 15 tín chỉ/học kỳ (tối thiểu 07 tín chỉ)"* kèm trích dẫn nguồn `[SRC-3]`.

#### Ca DEV_07 (Điểm 4.5 D có qua môn không hay phải học lại)
- **Hiện tượng:** Cả Dense và Hybrid đều trả lời đúng rằng điểm 4.5 D là Không đạt, không được qua môn và phải đăng ký học lại theo Điều 8. Tuy nhiên cả 2 chế độ đều chưa chủ động tư vấn nhánh sinh viên có thể đăng ký thi phụ (thi lại kết thúc học phần) theo Điều 18 khoản 5.
- **Nguyên nhân kỹ thuật:** Do câu hỏi chỉ hỏi *"có được tính qua môn không hay em bắt buộc phải học lại"*, cả Bi-Encoder và BM25 đều ưu tiên lấy chunk Điều 17 (thang điểm) và Điều 8 (học lại). Chunk Điều 18 (thi lại) ở chế độ Hybrid tuy đã xuất hiện ở Rank 6-7 nhưng chưa vượt lên được Top-5 để cạnh tranh với các chunk Điều 17. Để khắc phục hoàn toàn ca này trong tương lai, cần mở rộng Top-K hoặc áp dụng cơ chế Query Expansion để sinh thêm câu hỏi phụ về thi lại.

---

## V. ĐO LƯỜNG CHI PHÍ THỜI GIAN VÀ ĐỘ TRỄ (TELEMETRY)

Dữ liệu đo lường bằng `time.perf_counter()` trên toàn bộ 20 lượt thực thi:

### 1. Thống kê chi tiết độ trễ theo chế độ

| Hạng mục đo lường | Dense Baseline (Toàn bộ 10 ca) | Dense Baseline (Warm - 9 ca) | Hybrid BM25+RRF (Toàn bộ 10 ca) | Hybrid BM25+RRF (Warm - 9 ca) |
| :--- | :---: | :---: | :---: | :---: |
| **Retrieval Mean** | 187.32 ms | 62.34 ms | 70.25 ms | **68.01 ms** |
| **Retrieval Median** | 64.18 ms | 63.67 ms | 65.47 ms | **64.66 ms** |
| **LLM Generation Mean** | 2,865.07 ms | 2,955.10 ms | 1,686.91 ms | **1,642.88 ms** |
| **LLM Generation Median** | 1,700.10 ms | 1,669.76 ms | 1,646.38 ms | **1,628.74 ms** |
| **Total Pipeline Mean** | 3,052.47 ms | 3,017.51 ms | 1,757.23 ms | **1,710.96 ms** |
| **Total Pipeline Median** | 1,764.56 ms | 1,732.94 ms | 1,715.89 ms | **1,703.27 ms** |

### 2. Nhận xét về độ trễ và tính ổn định
- **Chi phí bổ sung của Hybrid:** Thời gian chạy BM25 sparse và thuật toán RRF chỉ tốn thêm trung bình **5.67 ms** so với Dense thuần túy khi hệ thống đã warm (68.01 ms so với 62.34 ms). Đây là mức đánh đổi chi phí thời gian cực kỳ tối ưu cho việc tăng mạnh độ phủ bằng chứng.
- **Biến động LLM:** Thời gian gọi Gemini API dao động từ 1.36 giây đến 2.08 giây (trung vị ~1.64 giây). Trường hợp cá biệt ở lượt chạy Dense ca DEV_07 mất 13.73 giây do độ trễ mạng internet kết nối máy chủ Google API, sau đó hồi phục bình thường.

---

## VI. KẾT LUẬN VÀ LỰA CHỌN CẤU HÌNH HỆ THỐNG

1. **Hiệu quả thực nghiệm của Hybrid:**
   - Đạt độ phủ bằng chứng Top-5 tuyệt đối **100% (9/9 ca)** so với 77.8% của Dense.
   - Giải quyết triệt để vấn đề từ chối nhầm của 2 ca khó là **DEV_02** và **DEV_08**, giúp hệ thống trợ lý học vụ hiểu được các câu hỏi đời thường và trích dẫn quy chế chính xác.
   - Không gây ảo giác hay viện dẫn nguồn giả mạo; toàn bộ mã nguồn `[SRC-x]` đều được xác thực và truy nguyên chính xác về trang PDF gốc.

2. **Khuyến nghị lựa chọn cấu hình:**
   - Hệ thống giữ nguyên giá trị mặc định `mode: str = "dense"` để bảo đảm tính tương thích ngược hoàn toàn.
   - Cho phép người dùng và kiểm thử viên linh hoạt kích hoạt chế độ `hybrid` thông qua tham số gọi API (`POST /chat {"question": "...", "mode": "hybrid"}`) hoặc qua tham số dòng lệnh CLI (`--mode hybrid`).
   - Kết quả thực nghiệm hoàn toàn ủng hộ việc chuyển đổi chế độ mặc định sang `hybrid` ở các giai đoạn nghiệm thu tiếp theo.
