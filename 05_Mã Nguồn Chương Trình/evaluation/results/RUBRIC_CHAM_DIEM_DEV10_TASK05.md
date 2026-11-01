# RUBRIC CHẤM ĐIỂM CHI TIẾT 10 CÂU PHÁT TRIỂN (DEV10) — NHIỆM VỤ TASK 05 (R01 & R02)

- **Dự án:** `dnc-academic-advisor-rag` (Đồ án 2 — Trợ lý học vụ DNC).
- **Ngày lập:** 01/11/2026.
- **Người / Agent chấm:** Antigravity AI Agent.
- **Tập dữ liệu nguồn đối soát:** `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_AB_DEV10_TASK05.jsonl` (nguyên bản, không sửa đổi).
- **Mã thực nghiệm:** `eval_task05_43c041f4`.
- **Mô hình sinh câu trả lời:** `gemini-3.5-flash-lite` (nhiệt độ $0.0$, seed cố định).

---

## 1. QUY ƯỚC ĐÁNH GIÁ (GRADING CRITERIA)

Mỗi ý bắt buộc (Mandatory Point) trong tiêu chuẩn vàng (Gold Standard) được chấm theo một trong 4 mức độc lập:
1. **ĐẠT (Full):** Câu trả lời phản ánh đầy đủ, chính xác nội dung của ý bắt buộc và có căn cứ ngữ cảnh hợp lệ.
2. **MỘT PHẦN (Partial):** Nêu được một phần quy định nhưng còn thiếu điều kiện ràng buộc, nhánh xử lý liên quan, hoặc thiếu con số chi tiết.
3. **THIẾU (Missing):** Bỏ sót hoàn toàn ý này trong câu trả lời (do retrieval không trích xuất được hoặc mô hình bỏ qua).
4. **SAI (Incorrect / Hallucination):** Đưa ra thông tin trái ngược với quy chế, hoặc khẳng định sai sự thật học vụ (claim error).

> **Lưu ý đặc biệt theo khuyến nghị Codex Task05-R01:**
> - Điểm số đánh giá trung thực theo nội dung thực sự phát sinh; không ép hybrid phải cao hơn dense, không che giấu lỗi.
> - DEV_06 giữ nguyên 5 ý bắt buộc theo tiêu chuẩn vàng.
> - DEV_09 được xử lý dưới dạng câu hỏi độc lập (Single-turn query); ghi nhận tính chất tiếp nối lịch sử là N/A do hệ thống hiện tại chưa tích hợp bộ nhớ hội thoại multi-turn.
> - Phân biệt rành mạch giữa *thiếu nhánh quy định* và *khẳng định sai quy chế*.

---

## 2. BẢNG TỔNG HỢP KẾT QUẢ ĐÁNH GIÁ THEO Ý BẮT BUỘC (MANDATORY POINTS)

| Case ID | Thể loại | Tổng số ý | Dense: Đạt | Dense: Một phần | Dense: Thiếu | Dense: Sai | Hybrid: Đạt | Hybrid: Một phần | Hybrid: Thiếu | Hybrid: Sai | Ghi chú so sánh |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **DEV_01** | Trực tiếp | 4 | 4 | 0 | 0 | 0 | 3 | 0 | 1 | 0 | Dense đạt 100%; Hybrid thiếu quy tắc làm tròn số thập phân. |
| **DEV_02** | Trực tiếp | 4 | 0 | 0 | 4 | 0 | 3 | 0 | 1 | 0 | Dense miss Điều 3; Hybrid trích xuất thành công Top-4, đạt 3/4 ý. |
| **DEV_03** | Trực tiếp | 3 | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | Cả hai mode trả lời chính xác, đầy đủ 3 khung tín chỉ. |
| **DEV_04** | Trực tiếp | 4 | 3 | 0 | 1 | 0 | 4 | 0 | 0 | 0 | Hybrid bổ sung được ý quy trình nộp đơn đầu kỳ qua P.QLĐT. |
| **DEV_05** | Trực tiếp | 3 | 2 | 0 | 1 | 0 | 2 | 0 | 1 | 0 | Cả hai mode đạt 2 ý chính (mức điểm D+/C+ và học phần cấm thi lại); cùng thiếu ý lệ phí. |
| **DEV_06** | Trực tiếp | 5 | 5 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | Cả hai mode đạt toàn bộ 5/5 điều kiện tốt nghiệp. |
| **DEV_07** | Đời thường | 4 | 2 | 1 | 1 | 0 | 1 | 1 | 1 | **1 (Sai)** | Hybrid mắc lỗi nhận định sai: *"từ điểm D+ trở xuống là dưới 5.0"*. |
| **DEV_08** | Đời thường | 3 | 1 | 0 | 2 | 0 | 2 | 0 | 1 | 0 | Dense miss CT 4 năm; Hybrid trả lời đúng 15 tín chỉ/kỳ. |
| **DEV_09** | Nối tiếp (Single-turn) | 3 | 2 | 0 | 1 | 0 | 2 | 0 | 1 | 0 | Cả hai mode nhận diện đúng thiếu dữ kiện, từ chối an toàn. |
| **DEV_10** | Ngoài phạm vi | 3 | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | Cả hai mode xác định đúng out-of-scope, trích dẫn Điều 3 khoản 4. |
| **TỔNG CỘNG** | **10 ca** | **36 ý** | **25 (69.4%)** | **1 (2.8%)** | **10 (27.8%)** | **0 (0.0%)** | **28 (77.8%)** | **1 (2.8%)** | **6 (16.7%)** | **1 (2.8%)** | **Hybrid tăng độ bao phủ (+3 ý đạt), nhưng phát sinh 1 lỗi sai.** |

---

## 3. BẢNG CHẤM CHI TIẾT TỪNG Ý BẮT BUỘC CHO 20 LƯỢT TRUY XUẤT VÀ TRẢ LỜI

### DEV_01: Quy định học phần tích lũy và bảng quy đổi điểm thang 4 (4 ý)
- **Câu hỏi:** Theo Quyết định 580/QĐ-ĐHNCT, học phần có điểm đánh giá bao nhiêu thì được tính là học phần tích lũy và bảng quy đổi điểm chữ, điểm số thang 4 được quy định như thế nào?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV01-P1 | Điểm đánh giá từ 5.0 trở lên (D+) được tính là học phần tích lũy | **ĐẠT** | *"Học phần có điểm đánh giá từ 5.0 trở lên (từ D+ trở lên) được tính là học phần tích lũy"* | `qd580_v2_c061_reg_d17_p15_b88b92a3` (PDF p.15, span char 77-434) | Nêu đúng ngưỡng 5.0 và điểm chữ D+. |
| **Dense** | DEV01-P2 | Bảng quy đổi 8 mức điểm tương ứng thang 10 sang thang 4 | **ĐẠT** | *"Bảng quy đổi điểm chữ và điểm số thang điểm 4 tương ứng với thang điểm 10: Từ 9.0 – 10.0: Điểm số hệ số 4 là 4.0, Điểm chữ là A ... Dưới 4.0: 0.0, F"* | `qd580_v2_c062_reg_d17_p15_b6de4df0` (PDF p.15, bảng quy đổi) | Liệt kê đủ 8 hàng của bảng quy đổi. |
| **Dense** | DEV01-P3 | Mức điểm 4.0 - 4.9 (D) và dưới 4.0 (F) là 'Không đạt' | **ĐẠT** | *"... Điểm chữ là D (Không đạt) ... Điểm chữ là F (Không đạt)"* | `qd580_v2_c062_reg_d17_p15_b6de4df0` (PDF p.15) | Xác định chính xác 2 mức Không đạt. |
| **Dense** | DEV01-P4 | Chấm theo thang điểm 10, làm tròn đến 1 chữ số thập phân | **ĐẠT** | *"Lưu ý: Điểm đánh giá học phần được chấm theo thang điểm 10 và làm tròn đến 1 chữ số thập phân"* | `qd580_v2_c061_reg_d17_p15_b88b92a3` (PDF p.15, Khoản 1) | Nêu rõ quy tắc làm tròn 1 chữ số thập phân. |
| **Hybrid** | DEV01-P1 | Điểm đánh giá từ 5.0 trở lên (D+) được tính là học phần tích lũy | **ĐẠT** | *"học phần có điểm đánh giá từ 5.0 trở lên (D+) được tính là học phần tích lũy"* | `qd580_v2_c061_reg_d17_p15_b88b92a3` (PDF p.15) | Nêu đúng ngưỡng 5.0 và điểm D+. |
| **Hybrid** | DEV01-P2 | Bảng quy đổi 8 mức điểm tương ứng thang 10 sang thang 4 | **ĐẠT** | *"Bảng quy đổi điểm chữ, điểm số thang 4 tương ứng với thang điểm hệ số 10 được quy định cụ thể như sau: - Từ 9.0 – 10.0: ... Dưới 4.0: 0.0, F"* | `qd580_v2_c062_reg_d17_p15_b6de4df0` (PDF p.15) | Đủ 8 hàng quy đổi thang 4. |
| **Hybrid** | DEV01-P3 | Mức điểm 4.0 - 4.9 (D) và dưới 4.0 (F) là 'Không đạt' | **ĐẠT** | *"... điểm chữ là D (Không đạt) ... điểm chữ là F (Không đạt)"* | `qd580_v2_c062_reg_d17_p15_b6de4df0` (PDF p.15) | Xác định đúng tính chất không đạt. |
| **Hybrid** | DEV01-P4 | Chấm theo thang điểm 10, làm tròn đến 1 chữ số thập phân | **THIẾU** | *(Không đề cập đến quy tắc làm tròn số thập phân trong câu trả lời)* | Không có trong câu trả lời Hybrid | Bỏ sót quy tắc làm tròn 1 chữ số thập phân. |

---

### DEV_02: Số lượng và thời lượng các học kỳ trong năm học (4 ý)
- **Câu hỏi:** Trường Đại học Nam Cần Thơ tổ chức năm học gồm bao nhiêu học kỳ và thời lượng của mỗi học kỳ được quy định ra sao theo QĐ 580?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV02-P1 | Mỗi năm gồm 03 học kỳ | **THIẾU** | *"chưa có dữ liệu cụ thể về số lượng học kỳ trong một năm học"* | Retrieval dense miss Điều 3 (Top 5 chỉ có Quyết định, Điều 2, Điều 14) | Dense không tìm thấy chunk Điều 3. |
| **Dense** | DEV02-P2 | Mỗi học kỳ từ 10 đến 12 tuần giảng dạy, học tập | **THIẾU** | *(Không có)* | Như trên | Retrieval miss. |
| **Dense** | DEV02-P3 | 2 tuần dành cho việc đánh giá (thi, kiểm tra...) | **THIẾU** | *(Không có)* | Như trên | Retrieval miss. |
| **Dense** | DEV02-P4 | Thời gian biểu quy định trong biểu đồ KHH do HT ban hành tháng 6 | **THIẾU** | *(Không có)* | Như trên | Retrieval miss. |
| **Hybrid** | DEV02-P1 | Mỗi năm gồm 03 học kỳ | **ĐẠT** | *"Trường Đại học Nam Cần Thơ tổ chức mỗi năm gồm 03 học kỳ"* | `qd580_v2_c011_reg_d03_p03_1b03fc2e` (PDF p.3, Điều 3 Khoản 1) | Hybrid đưa Điều 3 vào Top-4 (RRF score: 0.0156). |
| **Hybrid** | DEV02-P2 | Mỗi học kỳ từ 10 đến 12 tuần giảng dạy, học tập | **ĐẠT** | *"Mỗi học kỳ kéo dài từ 10 đến 12 tuần dành cho hoạt động giảng dạy và học tập"* | `qd580_v2_c011_reg_d03_p03_1b03fc2e` (PDF p.3) | Nêu đúng khoảng thời gian 10-12 tuần. |
| **Hybrid** | DEV02-P3 | 2 tuần dành cho việc đánh giá (thi, kiểm tra...) | **ĐẠT** | *"cùng với 2 tuần dành cho việc đánh giá (kiểm tra, thi, bảo vệ đồ án hoặc khóa luận...)"* | `qd580_v2_c011_reg_d03_p03_1b03fc2e` (PDF p.3) | Nêu đúng 2 tuần đánh giá. |
| **Hybrid** | DEV02-P4 | Thời gian biểu quy định trong biểu đồ KHH do HT ban hành tháng 6 | **THIẾU** | *(Câu trả lời chỉ nêu nghỉ hè, nghỉ lễ; không nhắc đến biểu đồ KHH do Hiệu trưởng ban hành vào tháng 6)* | Bỏ sót trong khâu tổng hợp LLM | LLM trích xuất thiếu ý Hiệu trưởng ban hành kế hoạch tháng 6. |

---

### DEV_03: Khối lượng tín chỉ đăng ký học kỳ theo từng chương trình (3 ý)
- **Câu hỏi:** Khối lượng tín chỉ tối thiểu và tối đa sinh viên được phép đăng ký trong mỗi học kỳ theo từng chương trình đào tạo là bao nhiêu?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV03-P1 | CT 4 năm: Tối thiểu 07 tín chỉ, tối đa 15 tín chỉ/kỳ | **ĐẠT** | *"Đối với chương trình học 04 năm: Tối thiểu 07 tín chỉ/học kỳ và tối đa 15 tín chỉ/học kỳ."* | `qd580_v2_c035_reg_d07_p08_811c2b53` (PDF p.8-9) | Trích xuất chính xác con số. |
| **Dense** | DEV03-P2 | CT 5 năm: Tối thiểu 09 tín chỉ, tối đa 20 tín chỉ/kỳ | **ĐẠT** | *"Đối với chương trình học 05 năm: Tối thiểu 09 tín chỉ/học kỳ và tối đa 20 tín chỉ/học kỳ."* | `qd580_v2_c035_reg_d07_p08_811c2b53` & `qd580_v2_c036` (PDF p.9) | Trích xuất chính xác con số. |
| **Dense** | DEV03-P3 | CT 6 năm: Tối thiểu 10 tín chỉ, tối đa 23 tín chỉ/kỳ | **ĐẠT** | *"Đối với chương trình học 06 năm: Tối thiểu 10 tín chỉ/học kỳ và tối đa 23 tín chỉ/học kỳ."* | `qd580_v2_c036_reg_d07_p09_9bac302f` (PDF p.9) | Trích xuất chính xác con số. |
| **Hybrid** | DEV03-P1 | CT 4 năm: Tối thiểu 07 tín chỉ, tối đa 15 tín chỉ/kỳ | **ĐẠT** | *"Đối với chương trình học 04 năm: Tối thiểu 07 tín chỉ/học kỳ và tối đa 15 tín chỉ/học kỳ"* | `qd580_v2_c035_reg_d07_p08_811c2b53` (PDF p.8-9) | Trích xuất chính xác con số. |
| **Hybrid** | DEV03-P2 | CT 5 năm: Tối thiểu 09 tín chỉ, tối đa 20 tín chỉ/kỳ | **ĐẠT** | *"Đối với chương trình học 05 năm: Tối thiểu 09 tín chỉ/học kỳ và tối đa 20 tín chỉ/học kỳ"* | `qd580_v2_c035` & `qd580_v2_c036` (PDF p.9) | Trích xuất chính xác con số. |
| **Hybrid** | DEV03-P3 | CT 6 năm: Tối thiểu 10 tín chỉ, tối đa 23 tín chỉ/kỳ | **ĐẠT** | *"Đối với chương trình học 06 năm: Tối thiểu 10 tín chỉ/học kỳ và tối đa 23 tín chỉ/học kỳ"* | `qd580_v2_c036_reg_d07_p09_9bac302f` (PDF p.9) | Trích xuất chính xác con số. |

---

### DEV_04: Điều kiện học cùng lúc hai chương trình (song bằng) (4 ý)
- **Câu hỏi:** Sinh viên muốn đăng ký học cùng lúc hai chương trình (song bằng) tại Trường Đại học Nam Cần Thơ cần đáp ứng những điều kiện gì?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV04-P1 | Xếp trình độ năm thứ hai của CT thứ nhất (Điều 16) | **ĐẠT** | *"Sinh viên phải được xếp trình độ năm thứ hai của chương trình thứ nhất theo quy định tại Điều 16"* | `qd580_v2_c046_reg_d11_p11_40c06ba1` (PDF p.11, Điều 11 Khoản 2) | Nêu đúng điều kiện năm 2 và dẫn chiếu Điều 16. |
| **Dense** | DEV04-P2 | 01 trong 02 ĐK: ĐTBTL >= 7.0 & ĐBCL; HOẶC ĐTBTL >= 5.5 & trúng tuyển | **ĐẠT** | *"đáp ứng 01 trong 02 điều kiện: Có ĐTBTL từ 7.0 trở lên và đáp ứng ngưỡng ĐBCL... HOẶC Có ĐTBTL từ 5.5 trở lên và đáp ứng ĐK trúng tuyển..."* | `qd580_v2_c046_reg_d11_p11_40c06ba1` (PDF p.11) | Nêu đúng cả 2 nhánh lựa chọn điểm số. |
| **Dense** | DEV04-P3 | Khoa quản lý CT thứ hai còn khả năng tiếp nhận | **ĐẠT** | *"Khoa quản lý chương trình thứ hai còn khả năng tiếp nhận thêm sinh viên"* | `qd580_v2_c046_reg_d11_p11_40c06ba1` (PDF p.11) | Nêu đúng điều kiện khoa tiếp nhận. |
| **Dense** | DEV04-P4 | Đăng ký vào đầu mỗi học kỳ qua P.QLĐT trình BGH duyệt | **THIẾU** | *(Dense chỉ retrieve được Khoản 2 của Điều 11, không có đoạn quy trình đăng ký Khoản 3 nằm ở chunk liền kề)* | `qd580_v2_c047` không lọt vào Top 5 dense | Thiếu quy trình nộp đơn đầu kỳ trình BGH. |
| **Hybrid** | DEV04-P1 | Xếp trình độ năm thứ hai của CT thứ nhất (Điều 16) | **ĐẠT** | *"Sinh viên được xếp trình độ năm thứ hai của chương trình thứ nhất theo quy định tại Điều 16"* | `qd580_v2_c046_reg_d11_p11_40c06ba1` (PDF p.11) | Đạt. |
| **Hybrid** | DEV04-P2 | 01 trong 02 ĐK: ĐTBTL >= 7.0 & ĐBCL; HOẶC ĐTBTL >= 5.5 & trúng tuyển | **ĐẠT** | *"phải đáp ứng 01 trong 02 điều kiện sau: Có ĐTBTL từ 7.0... HOẶC Có ĐTBTL từ 5.5..."* | `qd580_v2_c046_reg_d11_p11_40c06ba1` (PDF p.11) | Đạt cả 2 nhánh. |
| **Hybrid** | DEV04-P3 | Khoa quản lý CT thứ hai còn khả năng tiếp nhận | **ĐẠT** | *"Khoa quản lý chương trình thứ hai vẫn còn khả năng tiếp nhận thêm sinh viên"* | `qd580_v2_c046_reg_d11_p11_40c06ba1` (PDF p.11) | Đạt. |
| **Hybrid** | DEV04-P4 | Đăng ký vào đầu mỗi học kỳ qua P.QLĐT trình BGH duyệt | **ĐẠT** | *"Thời điểm đăng ký: Sinh viên đăng ký học chương trình thứ hai vào đầu mỗi học kỳ, sau đó Phòng Quản lý Đào tạo sẽ tập hợp, lập danh sách trình Ban Giám hiệu xét duyệt..."* | `qd580_v2_c047_reg_d11_p11_545cf0fe` (PDF p.11, [SRC-2]) | Hybrid kéo được chunk `qd580_v2_c047` vào Top 2, cung cấp đủ bằng chứng. |

---

### DEV_05: Giới hạn điểm sau thi lại và các học phần không tổ chức thi lại (3 ý)
- **Câu hỏi:** Theo quy chế 580, sau khi thi lại kết thúc học phần, điểm học phần của sinh viên được giới hạn ở mức tối đa là bao nhiêu và những loại học phần nào không tổ chức thi lại?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV05-P1 | Điểm sau thi lại giới hạn ở mức D+ hoặc C+ | **ĐẠT** | *"Điểm học phần sau khi thi lại chỉ được giới hạn ở mức điểm D+ hoặc điểm C+."* | `qd580_v2_c068_reg_d18_p17_d63aa6e2` (PDF p.17, Điều 18 Khoản 4) | Nêu đúng 2 mức trần D+ hoặc C+. |
| **Dense** | DEV05-P2 | Cấm thi lại: Thực hành, thi trên lớp, Đồ án, Thực tập | **ĐẠT** | *"Không tổ chức thi lại đối với các học phần Thực hành, học phần được tổ chức thi trên lớp, các học phần Đồ án, học phần Thực tập."* | `qd580_v2_c067_reg_d18_p16_3b65287f` (PDF p.16, Điều 18 Khoản 3) | Nêu đúng đủ 4 loại học phần không thi lại. |
| **Dense** | DEV05-P3 | Sinh viên nộp lệ phí trước theo thông báo của P.QLĐT (trừ hoãn thi) | **THIẾU** | *(Không có trong câu trả lời)* | Không nằm trong các đoạn trích retrieve được | Thiếu ý nghĩa vụ tài chính thi lại. |
| **Hybrid** | DEV05-P1 | Điểm sau thi lại giới hạn ở mức D+ hoặc C+ | **ĐẠT** | *"Điểm học phần sau khi thi lại chỉ được giới hạn ở mức điểm D+ hoặc điểm C+"* | `qd580_v2_c068_reg_d18_p17_d63aa6e2` (PDF p.17) | Đạt. |
| **Hybrid** | DEV05-P2 | Cấm thi lại: Thực hành, thi trên lớp, Đồ án, Thực tập | **ĐẠT** | *"Không tổ chức thi lại đối với các học phần Thực hành, học phần được tổ chức thi trên lớp, các học phần Đồ án, và học phần Thực tập"* | `qd580_v2_c067_reg_d18_p16_3b65287f` (PDF p.16) | Đạt đủ 4 loại học phần. |
| **Hybrid** | DEV05-P3 | Sinh viên nộp lệ phí trước theo thông báo của P.QLĐT (trừ hoãn thi) | **THIẾU** | *(Không có trong câu trả lời)* | Không nằm trong ngữ cảnh trích xuất | Thiếu ý nghĩa vụ tài chính thi lại. |

---

### DEV_06: Tiêu chuẩn xét và công nhận tốt nghiệp đại học (5 ý)
- **Câu hỏi:** Điều kiện để sinh viên được xét và công nhận tốt nghiệp đại học theo Quyết định 580/QĐ-ĐHNCT bao gồm những tiêu chuẩn nào?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV06-P1 | Có đơn đề nghị công nhận tốt nghiệp | **ĐẠT** | *"1. Có đơn đề nghị công nhận tốt nghiệp."* | `qd580_v2_c074_reg_d25_p20_c0fc3fe6` (PDF p.20, Điều 25 Khoản 1) | Nêu đúng điều kiện 1. |
| **Dense** | DEV06-P2 | Không bị truy cứu TN hình sự hoặc kỷ luật đình chỉ | **ĐẠT** | *"2. Cho đến thời điểm xét tốt nghiệp không bị truy cứu trách nhiệm hình sự hoặc không đang trong thời gian bị kỷ luật ở mức đình chỉ học tập."* | `qd580_v2_c074_reg_d25_p20_c0fc3fe6` (PDF p.20) | Nêu đúng điều kiện 2. |
| **Dense** | DEV06-P3 | Tích lũy đủ học phần, số tín chỉ của CTĐT | **ĐẠT** | *"3. Tích lũy đủ học phần, số tín chỉ của chương trình đào tạo..."* | `qd580_v2_c074_reg_d25_p20_c0fc3fe6` (PDF p.20) | Nêu đúng điều kiện 3. |
| **Dense** | DEV06-P4 | Hoàn thành GDQP-AN, GDTC, đạt CĐR ngoại ngữ & CNTT | **ĐẠT** | *"... và hoàn thành các học phần điều kiện gồm: Giáo dục quốc phòng - An ninh và Giáo dục thể chất, đạt chuẩn đầu ra của chương trình đào tạo (kể cả chuẩn đầu ra về ngoại ngữ và công nghệ thông tin)."* | `qd580_v2_c074_reg_d25_p20_c0fc3fe6` (PDF p.20) | Nêu đúng toàn bộ các môn điều kiện và CĐR. |
| **Dense** | DEV06-P5 | ĐTBTL toàn khóa đạt từ 5.5 trở lên | **ĐẠT** | *"4. Điểm trung bình chung tích lũy của toàn khóa học đạt từ 5.5 trở lên."* | `qd580_v2_c075_reg_d25_p21_7b66725c` (PDF p.21) | Nêu đúng ngưỡng 5.5. |
| **Hybrid** | DEV06-P1 | Có đơn đề nghị công nhận tốt nghiệp | **ĐẠT** | *"1. Có đơn đề nghị công nhận tốt nghiệp"* | `qd580_v2_c074_reg_d25_p20_c0fc3fe6` (PDF p.20) | Đạt. |
| **Hybrid** | DEV06-P2 | Không bị truy cứu TN hình sự hoặc kỷ luật đình chỉ | **ĐẠT** | *"2. Cho đến thời điểm xét tốt nghiệp không bị truy cứu trách nhiệm hình sự hoặc không đang trong thời gian bị kỷ luật ở mức đình chỉ học tập"* | `qd580_v2_c074_reg_d25_p20_c0fc3fe6` (PDF p.20) | Đạt. |
| **Hybrid** | DEV06-P3 | Tích lũy đủ học phần, số tín chỉ của CTĐT | **ĐẠT** | *"3. Tích lũy đủ học phần, số tín chỉ của chương trình đào tạo..."* | `qd580_v2_c074_reg_d25_p20_c0fc3fe6` (PDF p.20) | Đạt. |
| **Hybrid** | DEV06-P4 | Hoàn thành GDQP-AN, GDTC, đạt CĐR ngoại ngữ & CNTT | **ĐẠT** | *"... và hoàn thành các học phần điều kiện: Giáo dục quốc phòng - An ninh và Giáo dục thể chất, đạt chuẩn đầu ra của chương trình đào tạo (kể cả chuẩn đầu ra về ngoại ngữ và công nghệ thông tin)"* | `qd580_v2_c074_reg_d25_p20_c0fc3fe6` (PDF p.20) | Đạt. |
| **Hybrid** | DEV06-P5 | ĐTBTL toàn khóa đạt từ 5.5 trở lên | **ĐẠT** | *"4. Điểm trung bình chung tích lũy của toàn khóa học đạt từ 5.5 trở lên"* | `qd580_v2_c074` & `qd580_v2_c075` (PDF p.20-21) | Đạt. |

---

### DEV_07: Điểm 4.5 chữ D có qua môn không và hướng xử lý (4 ý)
- **Câu hỏi:** Kỳ rồi em thi môn Cơ sở dữ liệu bị 4.5 điểm, trên bảng điểm để chữ D. Cho em hỏi điểm này có được tính qua môn không hay em bắt buộc phải học lại?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV07-P1 | Điểm 4.5 (điểm D) xếp loại 'Không đạt' (chỉ từ 5.0 / D+ mới tích lũy) | **ĐẠT** | *"học phần có điểm đánh giá từ 5.0 trở lên (từ D+ trở lên) mới được tính là học phần tích lũy ... mức điểm 4.5 của bạn (thuộc khoảng từ 4.0 đến 4.9, điểm chữ D) được xếp loại là 'Không đạt'"* | `qd580_v2_c062_reg_d17_p15_b6de4df0` & `c061` (PDF p.15) | Khẳng định chính xác 4.5 là Không đạt. |
| **Dense** | DEV07-P2 | Sinh viên KHÔNG được tính là qua môn, không được tích lũy tín chỉ | **ĐẠT** | *"... và không được tính là học phần tích lũy"* | `qd580_v2_c062_reg_d17_p15_b6de4df0` (PDF p.15) | Trả lời trực tiếp câu hỏi qua môn. |
| **Dense** | DEV07-P3 | Có thể đăng ký thi phụ (thi lại) nếu có tổ chức (điểm giới hạn D+/C+) | **THIẾU** | *(Không nhắc đến cơ hội thi phụ / thi lại kết thúc học phần)* | Không retrieve được Điều 18 (Tổ chức kỳ thi) | Thiếu nhánh thi phụ. |
| **Dense** | DEV07-P4 | Bắt buộc học lại nếu là môn bắt buộc, hoặc học môn thay thế | **MỘT PHẦN** | *"Bạn bắt buộc phải đăng ký học lại học phần này theo quy định"* | `qd580_v2_c038_reg_d08_p09_a244c1fd` (PDF p.9, Điều 8 Khoản 3) | Khẳng định học lại một chiều mà không nêu điều kiện môn bắt buộc hay phương án thi phụ trước. |
| **Hybrid** | DEV07-P1 | Điểm 4.5 (điểm D) xếp loại 'Không đạt' (chỉ từ 5.0 / D+ mới tích lũy) | **SAI (Claim Error)** | *"học phần có điểm tổng kết đạt từ 5.0 trở lên (**từ điểm D+ trở xuống là dưới 5.0**) mới được tính là học phần tích lũy"* | Lỗi suy diễn sai từ LLM (Ngữ cảnh gốc PDF p.15 ghi D+ là 5.0 - 5.4) | **Ảo giác sai nghiêm trọng:** Điểm D+ là 5.0-5.4, không phải dưới 5.0! Việc tuyên bố "từ D+ trở xuống là dưới 5.0" là sai lệch quy chế thi đua và tính điểm. |
| **Hybrid** | DEV07-P2 | Sinh viên KHÔNG được tính là qua môn, không được tích lũy tín chỉ | **ĐẠT** | *"bạn không được tính qua môn và chưa được tính là học phần tích lũy."* | `qd580_v2_c062_reg_d17_p15_b6de4df0` (PDF p.15) | Trả lời đúng trọng tâm câu hỏi. |
| **Hybrid** | DEV07-P3 | Có thể đăng ký thi phụ (thi lại) nếu có tổ chức (điểm giới hạn D+/C+) | **THIẾU** | *(Hoàn toàn không có phương án thi phụ)* | Không retrieve được Điều 18 | Thiếu nhánh thi phụ. |
| **Hybrid** | DEV07-P4 | Bắt buộc học lại nếu là môn bắt buộc, hoặc học môn thay thế | **MỘT PHẦN** | *"sẽ phải đăng ký học lại theo quy định."* | Thiếu nhánh thi phụ và điều kiện học phần bắt buộc | Khẳng định học lại cứng nhắc, bỏ qua nhánh thi phụ. |

---

### DEV_08: Học vượt ngành CNTT hệ 4 năm được đăng ký tối đa bao nhiêu chỉ (3 ý)
- **Câu hỏi:** Mình đang học ngành Công nghệ thông tin hệ 4 năm, kỳ tới mình tính học vượt để ra trường sớm thì được đăng ký tối đa bao nhiêu chỉ một kỳ vậy?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV08-P1 | CT 4 năm (CNTT): Tối đa 15 tín chỉ/kỳ (tối thiểu 7 chỉ) | **THIẾU** | *"Ngữ cảnh chưa có thông tin cụ thể về giới hạn số tín chỉ tối đa được đăng ký cho hệ 4 năm (Cử nhân, Kỹ sư)."* | Retrieval dense chỉ lấy được `qd580_v2_c036` (PDF p.9, đoạn CT 5 năm và 6 năm), miss đoạn đầu Điều 7 ở p.8 | Dense hạ trạng thái `insufficient_evidence` do thiếu dữ kiện. |
| **Dense** | DEV08-P2 | Trường tổ chức 3 kỳ/năm, có thể học ở cả 3 kỳ | **THIẾU** | *(Không có)* | Retrieval miss | Thiếu ý. |
| **Dense** | DEV08-P3 | Tham khảo ý kiến hướng dẫn của Cố vấn học tập | **ĐẠT** | *"Em vui lòng liên hệ trực tiếp với Phòng Quản lý Đào tạo hoặc Cố vấn học tập để được hướng dẫn chính xác nhất."* | Hệ thống fallback chuẩn mực khi thiếu thông tin | Đạt ý hướng dẫn sinh viên hỏi CVHT. |
| **Hybrid** | DEV08-P1 | CT 4 năm (CNTT): Tối đa 15 tín chỉ/kỳ (tối thiểu 7 chỉ) | **ĐẠT** | *"Đối với chương trình học 04 năm: Tối thiểu 07 tín chỉ/học kỳ và tối đa 15 tín chỉ/học kỳ ... giới hạn số tín chỉ tối đa bạn được phép đăng ký trong một học kỳ là **15 tín chỉ/học kỳ**"* | `qd580_v2_c035_reg_d07_p08_811c2b53` (PDF p.8-9, [SRC-3]) | Hybrid tìm ra chunk `qd580_v2_c035` chứa quy định hệ 4 năm và trả lời đúng 15 tín chỉ. |
| **Hybrid** | DEV08-P2 | Trường tổ chức 3 kỳ/năm, có thể học ở cả 3 kỳ | **THIẾU** | *(Không đề cập đến việc trường tổ chức 3 học kỳ/năm để tận dụng học vượt)* | Bỏ sót trong khâu tổng hợp của LLM | Thiếu ý cơ chế năm 3 kỳ. |
| **Hybrid** | DEV08-P3 | Tham khảo ý kiến hướng dẫn của Cố vấn học tập | **ĐẠT** | *"mỗi sinh viên phải đăng ký học các học phần dự định theo hướng dẫn của cố vấn học tập ... Bạn nên trao đổi thêm với cố vấn học tập để được hướng dẫn chi tiết nhé!"* | `qd580_v2_c035_reg_d07_p08_811c2b53` (PDF p.8, Khoản 2) | Đạt. |

---

### DEV_09: Rút bớt học phần và hoàn tiền học phí sau đăng ký muộn (3 ý)
- **Câu hỏi:** Vậy nếu sau khi đăng ký muộn xong mà mình thấy quá tải muốn rút bớt học phần thì trong QĐ 580 có quy định điều kiện rút và việc hoàn tiền học phí thế nào?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV09-P1 | QĐ 580 chỉ có quy định đăng ký (Đ7) & tín chỉ học phí (Đ3.4) | **THIẾU** | *(Không phân tích cụ thể Điều 7 và Điều 3.4)* | Không có trong câu trả lời | Thiếu giải thích nguồn gốc văn bản. |
| **Dense** | DEV09-P2 | QĐ 580 hiện tại không có điều khoản rút học phần & hoàn học phí | **ĐẠT** | *"tài liệu hiện tại chưa có đủ dữ liệu cụ thể về điều kiện rút bớt học phần sau khi đăng ký muộn và việc hoàn tiền học phí."* | Toàn văn QĐ 580 | Xác định đúng lỗ hổng văn bản. |
| **Dense** | DEV09-P3 | Nêu rõ giới hạn tài liệu QĐ 580, khuyên liên hệ P.QLĐT / CVHT | **ĐẠT** | *"Bạn vui lòng liên hệ trực tiếp với Phòng Quản lý Đào tạo hoặc Cố vấn học tập để được hướng dẫn chi tiết về vấn đề này."* | Khuyến nghị hành động chuẩn mực | Đạt. |
| **Hybrid** | DEV09-P1 | QĐ 580 chỉ có quy định đăng ký (Đ7) & tín chỉ học phí (Đ3.4) | **THIẾU** | *(Không phân tích cụ thể Điều 7 và Điều 3.4)* | Không có trong câu trả lời | Thiếu giải thích nguồn gốc văn bản. |
| **Hybrid** | DEV09-P2 | QĐ 580 hiện tại không có điều khoản rút học phần & hoàn học phí | **ĐẠT** | *"Quyết định số 580/QĐ-ĐHNCT hiện tại chưa có đủ dữ liệu cụ thể về điều kiện rút bớt học phần sau khi đăng ký muộn cũng như quy định về việc hoàn tiền học phí trong trường hợp này."* | Toàn văn QĐ 580 | Xác định đúng lỗ hổng văn bản. |
| **Hybrid** | DEV09-P3 | Nêu rõ giới hạn tài liệu QĐ 580, khuyên liên hệ P.QLĐT / CVHT | **ĐẠT** | *"Để biết thêm thông tin chi tiết và chính xác, sinh viên vui lòng liên hệ trực tiếp với Phòng Quản lý Đào tạo hoặc Cố vấn học tập để được hướng dẫn."* | Khuyến nghị hành động chuẩn mực | Đạt. |

---

### DEV_10: Học phí CNTT 2026-2027 và cách tính điểm rèn luyện (3 ý)
- **Câu hỏi:** Theo Quyết định 580/QĐ-ĐHNCT, mức học phí cụ thể cho một tín chỉ của sinh viên ngành CNTT năm học 2026-2027 là bao nhiêu tiền và cách tính điểm rèn luyện của sinh viên như thế nào?

| Mode | Point ID | Tiêu chuẩn vàng (Gold Standard) | Kết quả | Trích đoạn Answer thực tế | Nguồn kiểm tra (Chunk / Trang / Span) | Lý do chấm |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **Dense** | DEV10-P1 | Từ chối đưa con số học phí cụ thể (do HĐT quyết định đơn giá) | **ĐẠT** | *"nằm ngoài phạm vi điều chỉnh của Quy chế đào tạo ... Đối với thông tin về mức học phí chi tiết từng ngành ... vui lòng liên hệ trực tiếp với Phòng Quản lý Đào tạo"* | Status: `out_of_scope` | Từ chối chính xác, không bịa đặt số tiền. |
| **Dense** | DEV10-P2 | Từ chối đưa cách chấm điểm rèn luyện (ngoài phạm vi QĐ 580) | **ĐẠT** | *"câu hỏi của bạn về ... cách tính điểm rèn luyện nằm ngoài phạm vi điều chỉnh của Quy chế đào tạo"* | QĐ 580 Điều 1 | Xác định đúng điểm rèn luyện thuộc quy chế công tác sinh viên riêng. |
| **Dense** | DEV10-P3 | Không võ đoán, giải thích rõ giới hạn của QĐ 580 | **ĐẠT** | *"Quy chế 580 chỉ quy định về các vấn đề học vụ chung như khái niệm tín chỉ (Điều 3) ... hay cảnh báo học tập (Điều 10)."* | `qd580_v2_c011`, `c012`, `c044` | Giải thích cặn kẽ phạm vi văn bản. |
| **Hybrid** | DEV10-P1 | Từ chối đưa con số học phí cụ thể (do HĐT quyết định đơn giá) | **ĐẠT** | *"Quy chế 580 chỉ quy định về tín chỉ học phí là đơn vị lượng hóa chi phí và cách tính bằng tổng số tín chỉ đăng ký nhân với đơn giá do Chủ tịch Hội đồng trường quy định [SRC-2], nhưng không quy định mức phí cụ thể từng ngành"* | `qd580_v2_c012_reg_d03_p04_72b38f88` (PDF p.4, Điều 3 Khoản 4) | Rất xuất sắc: Trích dẫn chính xác Điều 3 khoản 4 về thẩm quyền của Chủ tịch HĐT. |
| **Hybrid** | DEV10-P2 | Từ chối đưa cách chấm điểm rèn luyện (ngoài phạm vi QĐ 580) | **ĐẠT** | *"... hay quy chế điểm rèn luyện."* | Điều 1 QĐ 580 | Từ chối chính xác. |
| **Hybrid** | DEV10-P3 | Không võ đoán, giải thích rõ giới hạn của QĐ 580 | **ĐẠT** | *"Câu hỏi của bạn về mức học phí ... nằm ngoài phạm vi điều chỉnh của Quy chế Đào tạo trình độ đại học theo Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024 ... Vui lòng liên hệ trực tiếp với Phòng Quản lý Đào tạo hoặc Cố vấn học tập..."* | Status: `out_of_scope` | Giải thích lịch sự, khoa học, đúng chuẩn mực. |

---

## 4. KẾT LUẬN VÀ PHÂN TÍCH HỌC THUẬT

1. **Hiệu quả thực tế của Hybrid Search:**
   - **Cải thiện độ bao phủ (Recall / Evidence Coverage):** Hybrid giải quyết triệt để 2 ca thất bại nặng của Dense là **DEV_02** (Điều 3 - Cơ cấu năm học) và **DEV_08** (Điều 7 - Tín chỉ hệ 4 năm), nâng tổng số ý đạt từ 25/36 (69.4%) lên 28/36 (77.8%).
   - **Bảo toàn tính an toàn học vụ:** Ở các câu hỏi ngoài phạm vi hoặc thiếu dữ kiện (**DEV_09**, **DEV_10**), Hybrid vẫn giữ vững phản ứng an toàn (`insufficient_evidence`, `out_of_scope`), không bị từ khóa sparse làm nhiễu để sinh bậy.

2. **Bài học rút ra từ lỗi DEV_07:**
   - Tại DEV_07 (Hybrid), mô hình Gemini đã tự ý thêm một nhận định sai thực tế: *"từ điểm D+ trở xuống là dưới 5.0"*.
   - **Nguyên nhân gốc rễ:** Trong ngữ cảnh cấp cho LLM, bảng quy đổi thể hiện D+ ứng với $5.0 - 5.4$ và D ứng với $4.0 - 4.9$. Khi diễn giải văn xuôi tự nhiên, mô hình bị lúng túng giữa ngưỡng chặn dưới ($5.0$) của D+ và ngưỡng chặn trên ($4.9$) của D, dẫn tới việc phát biểu sai quy tắc logic.
   - **Hành động kiểm định liêm chính học thuật:** Rubric này ghi nhận rõ ràng mức **SAI (Claim Error)** cho ý DEV07-P1 của Hybrid. Điều này chứng minh rằng việc có đầy đủ mã nguồn [SRC-x] hợp lệ trong ngữ cảnh chưa đảm bảo 100% mọi câu khẳng định của LLM đều chuẩn xác, đòi hỏi các vòng kiểm tra groundedness chặt chẽ hơn trong tương lai.
