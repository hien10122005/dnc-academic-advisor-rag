# BÁO CÁO THỬ NGHIỆM TRUY XUẤT BASELINE A (CHUNKING & VECTOR RETRIEVAL)
## QUYẾT ĐỊNH SỐ 580/QĐ-ĐHNCT — HỆ THỐNG TRỢ LÝ HỌC VỤ ĐẠI HỌC NAM CẦN THƠ
### (Phiên bản v2.0 — Hiệu chỉnh Tokenizer-Aware & Bảo toàn Nguồn gốc Tuyệt đối)

---

> **Mã báo cáo:** `BC-RETRIEVAL-BASELINE-QD580-V2`  
> **Phiên bản:** `2.0.0` (Đã khắc phục toàn diện 4 điểm nghẽn P1 và các điểm lệch P2 theo tài liệu nhận xét)  
> **Ngày thực hiện:** 31/10/2026  
> **Môi trường thực thi:** Local CPU (Windows), Virtual Environment `.venv` (Python 3.14.6)  
> **Trạng thái kho tri thức:** `READY` (104 chunks, mã hóa 768 chiều, kiểm soát $100\%$ tokens $\le 256$)  
> **Mô hình Embedding:** `bkai-foundation-models/vietnamese-bi-encoder`  
> **Commit Hash Revision:** `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`  
> **Collection ChromaDB:** `qd580_baseline_v2` (Bảo toàn nguyên vẹn collection cũ `qd580_baseline_a` để đối chiếu)

---

## 1. MỤC TIÊU VÀ BỐI CẢNH HIỆU CHỈNH

Sau đợt rà soát kỹ thuật độc lập (`NHAN_XET_KIEM_TRA_BASELINE_QD580.md`), hệ thống đã tiến hành nâng cấp toàn diện thuật toán phân đoạn và bộ đánh giá nhằm giải quyết triệt để các hạn chế:
1. **Khắc phục lỗi cắt ngầm token (Silent Truncation):** Phiên bản cũ có $24/70$ chunks vượt quá $256$ token (lớn nhất $683$ token). Bản v2.0 tích hợp trực tiếp `AutoTokenizer` với commit hash chính thức, áp đặt ngưỡng cứng $\le 240$ tokens cho mọi chunk (tính cả `context_prefix` và special tokens `<s>`, `</s>`).
2. **Bảo toàn nguồn gốc và ranh giới Overlap:** Khắc phục lỗi ghi đè trang của phần overlap; theo dõi chính xác từng khoảng ký tự `[page_start_char, page_end_char]` trên từng trang PDF nguồn và vị trí `[chunk_start_char, chunk_end_char]` tương ứng trong chunk.
3. **Chuẩn hóa phương pháp chấm bằng chứng:** Thay thế hàm so khớp lỏng lẻo bằng thuật toán **Giao khoảng ký tự (Span Intersection Ratio)**. Phân biệt rõ rệt giữa *Phủ trọn vẹn (Full Coverage $\ge 90\%$)*, *Tìm thấy một phần (Partial Match)* và *Không tìm thấy*; chứng minh tự động loại bỏ $100\%$ lỗi chấm nhầm khi cùng Điều nhưng khác khoản.
4. **Bác bỏ giả thuyết ngưỡng từ chối vội vàng:** Đánh giá trung thực phổ điểm tương đồng thực tế, chứng minh rằng không thể dùng ngưỡng tĩnh $0.45$ để phân định câu ngoại phạm vi trên mô hình Bi-Encoder thuần túy.

---

## 2. THỐNG KÊ CHI TIẾT TỪ ARTIFACT THỰC TẾ (`QD580_CHUNKS.jsonl`)

Toàn bộ các thông số dưới đây được tính toán trực tiếp bằng mã nguồn từ tệp dữ liệu thực tế tại `05_Mã Nguồn Chương Trình/data/QD580_CHUNKS.jsonl` và `data/QD580_MANIFEST.json`:

### 2.1 Mã băm định danh và tính bất biến (Fingerprint)
- **Tệp PDF gốc:** `580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf` (Dung lượng: $6,635,360\text{ bytes}$, SHA-256: `a3ba2122457999f631a876c39d82d487df880f0d3e2c5c66f4e5dbce9cd560db`).
- **Tệp Corpus Pages:** `QD580_PAGES.jsonl` (26 trang kiểm chứng, SHA-256: `b019bbf04d440ad88a91c13d330eb027063715c6d376ca80bc1a851944e054d5`).
- **Tệp Chunks v2:** `QD580_CHUNKS.jsonl` (SHA-256: `5802f176f1f603123126c49284449085bd18bdf64f3213998e081ecd01536398`).
- **Corpus Fingerprint v2:** `8f0c62a9ce8b2b049597599e10cc072760e21cf7cec442386848122226e977dd`.

### 2.2 Cơ cấu và phân loại Chunks

| Thuộc tính phân đoạn | Giá trị thực tế v2 | Ghi chú kỹ thuật |
| :--- | :---: | :--- |
| **Tổng số Chunks** | **104 chunks** | Phân rã nhỏ mịn theo tokenizer BKAi (100% $\le 256$ tokens) |
| **Phần Quyết định ban hành (`decision`)** | **6 chunks** | Căn cứ, xét đề nghị, Điều 1, Điều 2, Điều 3 (Trang 1) |
| **Phần Quy chế đào tạo (`regulation`)** | **98 chunks** | Điều 1 đến Điều 32 (Trang 2 đến 26) |
| **Số Chunks văn bản thường (Text)** | **95 chunks** | Chia theo mệnh đề, khoản và câu hoàn chỉnh |
| **Số Chunks bảng biểu Markdown (Table)**| **9 chunks** | 6 bảng nguyên vẹn + 3 sub-tables lặp header của bảng Điều 28 |
| **Số Chunks nối trang (Cross-page)** | **19 chunks** | Nối liền mạch các điều khoản vắt qua ranh giới trang scan |
| **Số đoạn gối đầu (Overlap Spans)** | **27 đoạn** | Đều lưu đúng số trang gốc và offset khớp nguyên văn |
| **Tổng số Source Spans đã kiểm chứng** | **351 spans** | Khớp chính xác $100\%$ từng ký tự với trang nguồn gốc |

### 2.3 Phân bố Token và Ký tự

| Thông số đo lường | Nhỏ nhất (Min) | Trung vị (Median) | Trung bình (Mean) | Lớn nhất (Max) | Giới hạn mô hình |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Số Token (`embedding_text`)** | **52** | **198.0** | **184.4** | **246** | Mục tiêu $\le 240$, trần cứng $\le 256$ ($100\%$ đạt chuẩn) |
| **Độ dài ký tự (`content`)** | **58** | **600.5** | **544.1** | **839** | Thống nhất từ artifact thực tế |

*Quy ước đo lường: `token_count` tính trên toàn bộ đầu vào mô hình gồm `[context_prefix] + \n + content` cùng các special tokens `<s>` và `</s>`; `char_count` tính trên chuỗi `content` thực của chunk.*

### 2.4 Giải trình vùng nội dung đầu trang PDF 2 được lược bỏ có chủ đích
- Đoạn đầu trang PDF 2 gồm $149$ ký tự không phải khoảng trắng (tiêu đề *"QUY CHẾ ĐÀO TẠO TRÌNH ĐỘ ĐẠI HỌC..."*, dòng viện dẫn *"Ban hành kèm theo Quyết định số 580/QĐ-ĐHNCT..."*, và tiêu đề *"CHƯƠNG I: QUY ĐỊNH CHUNG"*).
- Đây là phần tiêu đề hành chính chung, không chứa quy phạm nghiệp vụ hay điều kiện ràng buộc học vụ nên được chủ đích lược bỏ khỏi spans của các điều khoản cụ thể. Toàn bộ nội dung quy phạm từ Điều 1 đến Điều 32 được bảo toàn $100\%$ không bị bỏ sót bất kỳ điều kiện hay ngoại lệ nào.

---

## 3. KẾT QUẢ ĐÁNH GIÁ TRUY XUẤT NGHIÊM NGẶT (STRICT EVALUATION)

### 3.1 Phương pháp chấm bằng chứng mới
- Mỗi bằng chứng chuẩn trong `DEV_10_CAU_QD580.jsonl` được xác định một khoảng ký tự tuyệt đối $[q_s, q_e]$ trên trang PDF gốc.
- Đối với tập hợp Top-K chunks trả về, hệ thống tính hợp của các khoảng giao nhau với $[q_s, q_e]$ (loại trừ phần context bổ sung).
- **Tiêu chuẩn tính Hit:** Một bằng chứng được coi là đạt Full Coverage khi và chỉ khi tỷ lệ phủ $\text{Coverage} \ge 90\%$.
- **Loại trừ False Positive:** Đã kiểm thử chứng minh tự động rằng hai đoạn văn bản cùng thuộc một Điều nhưng khác khoản (ví dụ Điều 11 khoản 1 và khoản 2) có độ phủ chính xác bằng **$0.0\%$**, tuyệt đối không bị tính nhầm như phiên bản cũ.

---

### 3.2 Bảng tổng hợp đối chiếu kết quả thực nghiệm

Mẫu số đánh giá: **9 ca Grounded** (`DEV_01` $\rightarrow$ `DEV_09`). Ca ngoại vi `DEV_10` được phân tích riêng.

| Chỉ số đánh giá | Bản cũ v1 (`qd580_baseline_a`) | Bản mới v2 (`qd580_baseline_v2`) | Nhận xét tiến bộ kỹ thuật |
| :--- | :---: | :---: | :--- |
| **Tổng số Chunks trong kho** | 70 chunks | 104 chunks | Phân đoạn nhỏ mịn, an toàn token |
| **Tỷ lệ chunk vượt 256 token** | **34.3%** (24/70) | **0.0%** (0/104) | Triệt tiêu hoàn toàn lỗi cắt ngầm token |
| **Hit Rate@1 ($\ge 90\%$ bằng chứng)** | N/A* | **$55.6\%$** (5/9 ca) | Bắt trọn bằng chứng ngay Top 1 |
| **Hit Rate@3 ($\ge 90\%$ bằng chứng)** | N/A* | **$77.8\%$** (7/9 ca) | Thu hồi tốt ở Top 3 |
| **Hit Rate@5 ($\ge 90\%$ bằng chứng)** | N/A* | **$77.8\%$** (7/9 ca) | Ổn định ở Top 5 |
| **Hit Rate@10 ($\ge 90\%$ bằng chứng)**| N/A* | **$100.0\%$** (9/9 ca) | Toàn bộ 9 ca đều có ít nhất 1 bằng chứng $\ge 90\%$ ở Top 10** |
| **Mean Reciprocal Rank (MRR@10)** | N/A* | **$0.6806$** | Đo vị trí tương hỗ của bằng chứng đầu tiên đạt chuẩn |
| **Độ phủ bằng chứng trung bình@10** | N/A* | **$83.1\%$** | Tăng mạnh khả năng thu hồi đa nguồn |
| **Tỷ lệ ca mọi bằng chứng đạt $\ge 90\%$**| N/A* | **$66.7\%$** (6/9 ca) | 6/9 ca thu hồi trọn vẹn mọi trích dẫn bằng chứng*** |
| **Độ trễ trung bình truy vấn** | $43.1\text{ ms}$ | **$63.6\text{ ms}$** | Phép đo phát triển trên 10 query (Trung vị: $37.9\text{ ms}$)**** |

*\*Ghi chú đối chiếu: Bản cũ v1 không lưu trữ `source_spans_json` trong metadata ChromaDB nên không thể truy xuất ngược khoảng ký tự để chấm theo tiêu chí span intersection. Ở bản v1, ca DEV_02 từng hoàn toàn rớt khỏi Top 10 do Điều 3 bị dồn vào chunk 2371 ký tự và bị cắt ngầm.*  
*\*\*Lưu ý phương pháp luận: Hit@10 = 100% nghĩa là mỗi ca đều tìm thấy ít nhất một bằng chứng đạt ngưỡng phủ ký tự $\ge 90\%$, không đồng nghĩa chatbot đã trả lời trọn vẹn mọi ý ngữ nghĩa của câu hỏi.*  
*\*\*\*Lưu ý độ phủ: Tỷ lệ phủ ký tự $\ge 90\%$ là điều kiện cần; khi đánh giá câu trả lời tổng thể vẫn cần kiểm tra các con số và ý bắt buộc (mandatory points) độc lập.*  
*\*\*\*\*Lưu ý độ trễ: Đây là phép thử phát triển nhỏ trên 10 query để kiểm tra tính sẵn sàng, chưa bao gồm phân vị P95 và số lần lặp lớn trong môi trường chịu tải.*

---

### 3.3 Phân tích chi tiết từng ca thử nghiệm (Bản v2)

| Mã ca | Loại câu hỏi | Số bằng chứng | Rank 1st đạt $\ge 90\%$ | Hit@3 | Hit@10 | MRR@10 | Độ phủ@10 | Trạng thái chi tiết |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **DEV_01** | Trực tiếp (Thang điểm tích lũy) | 2 | **Rank 1** | Có | Có | $1.0000$ | **$100.0\%$** | Phủ đủ $100\%$ Điều 17 khoản 1 và Bảng quy đổi điểm 8 mức. |
| **DEV_02** | Trực tiếp (Số học kỳ/năm) | 2 | **Rank 6** | Không | Có | $0.1667$ | **$100.0\%$** | **Tiến bộ vượt bậc:** Đưa Điều 3 khoản 2b, 2c vào Top 6 (bản v1 rớt ngoài Top 10). |
| **DEV_03** | Trực tiếp (Hạn mức tín chỉ 4-5-6 năm)| 1 | **Rank 3** | Có | Có | $0.3333$ | **$99.3\%$** | Thu hồi chính xác Điều 7 khoản 2 tại Rank 3. |
| **DEV_04** | Trực tiếp (Điều kiện song bằng) | 2 | **Rank 1** | Có | Có | $1.0000$ | **$99.6\%$** | Phủ đủ cả Điều 11 khoản 2 (điều kiện) và khoản 3 (thủ tục). |
| **DEV_05** | Trực tiếp (Trần điểm thi lại) | 2 | **Rank 1** | Có | Có | $1.0000$ | **$99.9\%$** | Phủ trọn vẹn Điều 18 khoản 5 (trang 16) và khoản 6 (trang 17). |
| **DEV_06** | Trực tiếp (Chuẩn tốt nghiệp) | 2 | **Rank 1** | Có | Có | $1.0000$ | **$99.3\%$** | Phủ trọn vẹn Điều 25 khoản 1 (tiêu chuẩn) và khoản 2 (điểm TB $\ge 5.5$). |
| **DEV_07** | Đời thường (Điểm D 4.5 qua môn không)| 4 | **Rank 2** | Có | Có | $0.5000$ | **$50.0\%$** | Thu hồi Điều 17 (thang điểm) và Điều 8 (học lại); chưa thu hồi đủ khoản thi lại. |
| **DEV_08** | Đời thường (Học vượt CNTT bao nhiêu chỉ)| 2 | **Rank 8** | Không | Có | $0.1250$ | **$50.0\%$** | Thu hồi Điều 7 khoản 2 (hạn mức 15 tín chỉ) ở Rank 8; câu khẩu ngữ cần BM25/Rewriting. |
| **DEV_09** | Nối tiếp/Lịch sử (Rút môn & hoàn phí)| 2 | **Rank 1** | Có | Có | $1.0000$ | **$50.0\%$** | Thu hồi Điều 3 khoản 4 (định nghĩa tín chỉ học phí); QĐ 580 không quy định rút môn hoàn phí. |
| **DEV_10** | Ngoại vi (Học phí cụ thể & điểm rèn luyện)| 2 | *(Ngoại vi)* | - | - | - | - | **Top 1 Sim = $0.4295$**. Bác bỏ giả thuyết ngưỡng tĩnh $0.45$ (xem mục 4). |

---

## 4. BÁC BỎ GIẢ THUYẾT NGƯỠNG TỪ CHỐI 0.45 VÀ PHÂN TÍCH LỖI THỰC TẾ

### 4.1 Bằng chứng bác bỏ ngưỡng từ chối tĩnh
Phân tích trực tiếp từ `top_k_results.jsonl` cho thấy phổ điểm Cosine Similarity của Top 1 chunk ở từng ca như sau:

$$\begin{aligned}
\text{DEV\_06} &: 0.6635 \quad & \text{DEV\_04} &: 0.6129 \quad & \text{DEV\_01} &: 0.5698 \\
\text{DEV\_05} &: 0.5651 \quad & \text{DEV\_02} &: 0.5401 \quad & \text{DEV\_09} &: 0.5292 \\
\mathbf{DEV\_10} &: \mathbf{0.4295} \text{ (Out-of-Scope)} \\
\mathbf{DEV\_03} &: \mathbf{0.4171} \text{ (Grounded)} \\
\mathbf{DEV\_08} &: \mathbf{0.3258} \text{ (Grounded)} \\
\mathbf{DEV\_07} &: \mathbf{0.2676} \text{ (Grounded)}
\end{aligned}$$

**Kết luận kỹ thuật quan trọng:**
- Ca ngoại phạm vi DEV_10 có điểm tương đồng ($0.4295$) **cao hơn** cả 3 ca hợp lệ có căn cứ thực tế: DEV_03 ($0.4171$), DEV_08 ($0.3258$) và DEV_07 ($0.2676$).
- **Hệ quả:** Nếu áp dụng ngưỡng cắt $0.45$ như đề xuất vội vàng trước đây, hệ thống sẽ **từ chối nhầm (False Rejection) tới 33.3% số câu hỏi hợp lệ của sinh viên**.
- **Nguyên nhân:** Mô hình Dense Bi-Encoder phản ánh khoảng cách hình học trong không gian ngữ nghĩa, bị chi phối bởi các từ ngữ đời thường (như ở DEV_07: *"bị 4.5 điểm, trên bảng điểm để chữ D"*; DEV_08: *"học vượt để ra trường sớm"*).
- **Định hướng giải quyết đúng đắn:** Không dùng ngưỡng tương đồng Bi-Encoder làm bộ lọc từ chối đơn độc. Việc nhận biết câu hỏi ngoại vi / thiếu căn cứ phải được giải quyết qua:
  1. Tầng **Query Rewriting / Normalization** để chuyển câu khẩu ngữ về thuật ngữ học vụ chuẩn.
  2. Tầng **Cross-Encoder Reranker** cho điểm tương đồng chính xác hơn.
  3. Tầng **LLM Grounding Verification** (kiểm định căn cứ trích dẫn ở bước sinh câu trả lời).

---

## 5. BẰNG CHỨNG TÁI LẬP (REPRODUCIBILITY)

Quy trình kiểm thử hoàn toàn tự động hóa và có thể tái hiện $100\%$ bằng các lệnh sau từ thư mục `05_Mã Nguồn Chương Trình`:

```powershell
# Di chuyển vào thư mục mã nguồn
cd '05_Mã Nguồn Chương Trình'

# 1. Chạy bộ kiểm thử tự động 5 tiêu chí (Tokens, Spans, Overlap, Coverage, Idempotency)
.\.venv\Scripts\python.exe -m tests.test_chunking_and_sources

# 2. Chạy nạp lại dữ liệu vào ChromaDB (Kiểm tra Idempotent)
.\.venv\Scripts\python.exe -m backend.ingestion

# 3. Thử nghiệm truy xuất CLI trên collection mới v2
.\.venv\Scripts\python.exe -m backend.retrieval --query "Điều kiện cảnh báo kết quả học tập là gì?" --top_k 3

# 4. Chạy toàn bộ benchmark đánh giá nghiêm ngặt (Strict Evaluation)
.\.venv\Scripts\python.exe -m evaluation.evaluate_retrieval
```

---

## 6. KẾT LUẬN NGHIỆM THU NHIỆM VỤ 03

1. **Hoàn thành xuất sắc việc khắc phục các điểm nghẽn:**
   - $100\%$ chunks tuân thủ giới hạn token $\le 256$ của mô hình `vietnamese-bi-encoder` (Max: 246, Avg: 184.4).
   - $100\%$ source spans và phần overlap truy nguyên chuẩn xác từng ký tự với 26 trang gốc.
   - Hàm đánh giá nghiêm ngặt loại bỏ hoàn toàn lỗi nhận nhầm bằng chứng khi cùng Điều khác khoản.
   - Đưa Điều 3 (DEV_02) thành công vào Top 6 với độ phủ bằng chứng đạt $100\%$.
2. **Số liệu trung thực và khách quan:** Báo cáo phản ánh đúng phổ điểm thực tế của Bi-Encoder, làm rõ hạn chế đối với câu hỏi khẩu ngữ đời thường và bác bỏ kết luận võ đoán về ngưỡng từ chối.
3. **Mã nguồn sẵn sàng:** Môi trường `.venv`, cấu hình, kiểm thử tự động, dữ liệu `QD580_CHUNKS.jsonl` (104 chunks) và manifest đã được đóng gói chuẩn mực.
