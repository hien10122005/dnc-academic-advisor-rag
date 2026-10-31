# BÁO CÁO CHUẨN HÓA DỮ LIỆU NGUỒN QUYẾT ĐỊNH 580/QĐ-ĐHNCT
## NGHIÊN CỨU SỐ HÓA, ĐỐI CHIẾU NGUỒN GỐC VÀ XÂY DỰNG TẬP PHÁT TRIỂN CHUẨN HỌC VỤ

> **Văn bản căn cứ:** Quyết định số 580/QĐ-ĐHNCT ngày 02 tháng 8 năm 2024 của Hiệu trưởng Trường Đại học Nam Cần Thơ về việc ban hành Quy chế tổ chức đào tạo trình độ đại học.
> **Thời gian thực hiện:** Ngày 31 tháng 10 năm 2026.
> **Người thực hiện kiểm chứng:** Antigravity Pair-Programmer (chế độ kiểm định trực quan song song).
> **Thư mục lưu trữ kết quả:** `02_Dữ Liệu Quy Chế/04_Dữ Liệu Đã Kiểm Chứng/QD580/`.

---

## 1. TỔNG QUAN VÀ MỤC TIÊU NHIỆM VỤ

Quy chuẩn hóa cơ sở tri thức trước khi đưa vào đường ống nạp dữ liệu (Ingestion Pipeline) là yêu cầu tiên quyết nhằm bảo đảm tính liêm chính và sự chính xác tuyệt đối của trợ lý học vụ AI. Nghiên cứu thực nghiệm tại bước kiểm định trước đó đã chỉ ra rằng tệp dữ liệu văn bản đã qua xử lý cũ (`02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md`) tồn tại nhiều sai lệch nghiêm trọng so với văn bản quy phạm gốc, đặc biệt là việc gán sai thang điểm đánh giá học phần (nhận định sai điểm D là tích lũy, quy ước điểm A từ 8.5 thay vì 9.0), sai lệch cơ cấu số học kỳ trong năm học (2 kỳ chính thay vì 3 kỳ), và áp đặt hạn mức đăng ký tín chỉ không có căn cứ.

Mục tiêu cốt lõi của giai đoạn này tập trung vào các nội dung sau:
1. Thực hiện số hóa và đối chiếu trực quan 100% toàn bộ 26 trang của văn bản Quyết định số 580/QĐ-ĐHNCT từ bản quét bitmap kết xuất ở tỷ lệ `scale=1.5` (~108 DPI), bảo đảm truy nguyên được số trang PDF, số trang in và vị trí điều khoản cụ thể.
2. Thiết lập cấu trúc dữ liệu thô (`raw/`) tách biệt với dữ liệu đã kiểm chứng, xây dựng định dạng Markdown theo trang (`QD580_THEO_TRANG.md`) và tệp dữ liệu cấu trúc (`QD580_PAGES.jsonl`) gắn kèm đầy đủ siêu dữ liệu (metadata) truy xuất nguồn gốc.
3. Lập bảng nhật ký theo dõi kiểm chứng từng trang (`KIEM_CHUNG_TUNG_TRANG.csv`) và nhật ký đính chính (`NHAT_KY_DINH_CHINH.csv`) phản ánh chi tiết các điểm sai lệch của tệp quy chế cũ.
4. Xây dựng bản đề xuất đính chính hoàn chỉnh (`DE_XUAT_DINH_CHINH_FILE_02.md`), trong đó bóc tách triệt để phần quy định gốc trong QĐ 580 với các thông tin bổ sung từ Sổ tay sinh viên hoặc các hướng dẫn học vụ bên ngoài.
5. Biên soạn bộ 10 ca phát triển học vụ chuẩn (`DEV_10_CAU_QD580.jsonl`) có đáp án và trích dẫn kiểm chứng 1-1 để làm bộ tiêu chuẩn vàng (Golden Evaluation Set) phục vụ việc đánh giá sau khi hoàn thiện nạp chỉ mục.

---

## 2. PHƯƠNG PHÁP VÀ QUY TRÌNH THỰC HIỆN

### 2.1. Phân tích đặc tính tài liệu gốc và giới hạn công nghệ OCR
Tệp tài liệu gốc `580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf` có dung lượng chính xác là **6.635.360 bytes** (xấp xỉ $6.33\text{ MB}$), bao gồm 26 trang. Kiểm tra kỹ thuật lớp văn bản (text layer) xác nhận toàn bộ 26 trang đều là ảnh quét bitmap không có lớp ký tự số hóa (text length = 0).

Trong điều kiện môi trường cục bộ Windows không có gói ngôn ngữ tiếng Việt của Windows Media OCR và hệ thống không cài đặt sẵn công cụ Tesseract OCR tiếng Việt trong biến môi trường PATH, việc sử dụng các mô hình OCR tự động không được huấn luyện riêng biệt trên phông chữ hành chính tiếng Việt dễ dẫn đến hiện tượng đọc sai dấu thanh, nhầm lẫn số học và sai lệch ký hiệu toán học nguy hiểm. Do đó, quy trình thực hiện đã chuyển đổi sang **phương pháp đối chiếu trực quan thủ công có sự hỗ trợ của kết xuất ảnh độ phân giải scale=1.5 (~108 DPI từ chuẩn 72 DPI của PDF) qua thư viện pypdfium2 (Manual Visual Transcription from Rendered Images)**. Lưu ý rằng thư mục `raw/` và tệp đọc `QD580_THEO_TRANG.md` được kết xuất từ cùng tập dữ liệu chép tay chuẩn hóa `PAGES_DATA`, đóng vai trò là bản chép đầu vào để theo dõi theo trang, không đại diện cho lịch sử chạy của hai công cụ OCR độc lập. Đồng thời, việc đối chiếu được thực hiện trực tiếp bởi agent trong phiên làm việc, không giả định có người kiểm tra độc lập thứ hai.

### 2.2. Quy trình kiểm định 4 bước
Quá trình chuẩn hóa được triển khai theo chu trình khép kín:
- **Bước 1: Kết xuất ảnh trung gian:** Sử dụng thư viện `pypdfium2` với tham số `scale=1.5` (~108 DPI từ gốc 72 DPI) để kết xuất toàn bộ 26 trang sang định dạng PNG tại thư mục `sample_renders/580_p01.png` đến `580_p26.png`.
- **Bước 2: Thử nghiệm số hóa 4 trang trọng yếu (Part B):** Tiến hành kiểm tra chi tiết 4 trang trọng điểm:
  - Trang PDF 3 (Trang in 2): Kiểm tra bảng tín chỉ tối thiểu theo bằng cấp và quy định Điều 3 về 3 học kỳ trong năm.
  - Trang PDF 9 (Trang in 8): Kiểm tra Điều 7 và Điều 8 về định mức tín chỉ tối thiểu/tối đa và quy tắc học cải thiện lấy điểm thi sau cùng.
  - Trang PDF 15 (Trang in 14): Kiểm tra từng ô trong bảng quy đổi điểm học phần Điều 17, đối chiếu kỹ lưỡng ngưỡng đạt môn $\ge 5.0$ (D+) và các mức không đạt D (4.0–4.9), F (<4.0).
  - Trang PDF 17 (Trang in 16): Kiểm tra Điều 18 và Điều 19 về giới hạn trần điểm thi lại ở mức D+ hoặc C+, lưu trữ bảng điểm vĩnh viễn và trần chuyển đổi tín chỉ tối đa 50%.
- **Bước 3: Mở rộng kiểm chứng toàn diện 26 trang (Part C):** Thực hiện chép thô, đối chiếu từng câu từ, dấu ngắt câu, định dạng bảng và điều khoản chuyển tiếp giữa các trang từ trang 1 đến trang 26.
- **Bước 4: Đóng gói và kiểm định đối xứng:** Biên soạn các tệp JSONL, CSV và Markdown với mã hóa UTF-8 (CSV sử dụng UTF-8 with BOM để hỗ trợ hiển thị tiếng Việt trên Microsoft Excel).

---

## 3. KẾT QUẢ SỐ HÓA VÀ ĐỐI CHIẾU 26 TRANG

Toàn bộ 26 trang của văn bản đã được số hóa và kiểm chứng thành công với tỷ lệ hoàn thành 100%. Không có trang nào bị bỏ sót hay mang trạng thái chưa xác minh.

Bảng 3.1 tổng hợp thông số số hóa và phạm vi điều khoản của từng trang:

| Trang PDF | Trang in | Chương | Điều khoản bao hàm | Trạng thái | Ghi chú đối chiếu |
| :---: | :---: | :---: | :--- | :---: | :--- |
| **01** | Không số | Quyết định | Căn cứ pháp lý, Điều 1 – Điều 3 Quyết định | ĐÃ KIỂM CHỨNG | Ban hành quy chế 5 chương 32 điều; ký bởi TS. Nguyễn Văn Quang |
| **02** | 1 | Chương I | Điều 1; Điều 2 (khoản 1–4, bảng phần 1) | ĐÃ KIỂM CHỨNG | Khối lượng tín chỉ VB2 (60), Liên thông CĐ (60), TC (70) |
| **03** | 2 | Chương I | Điều 2 (khoản 4 bảng phần 2, khoản 5); Điều 3 (khoản 1–3) | ĐÃ KIỂM CHỨNG | Tín chỉ Cử nhân (120), Kỹ sư/Dược sĩ (150), Bác sĩ (180); 03 học kỳ/năm |
| **04** | 3 | Chương I | Điều 3 (khoản 3–5) | ĐÃ KIỂM CHỨNG | Tín chỉ 15 tiết LT, chuẩn bị 30 giờ; Tín chỉ học phí do HĐT định giá |
| **05** | 4 | Chương I | Điều 3 (khoản 5–6, bảng quy mô mở lớp) | ĐÃ KIỂM CHỨNG | Mở lớp LT $\ge 60$ SV, TH $\ge 40$, TT/TT $\ge 20$, ĐA môn 15, KLTN 05 |
| **06** | 5 | Chương I | Điều 3 (khoản 6–8); Điều 4 | ĐÃ KIỂM CHỨNG | Hủy lớp thiếu sĩ số; Lớp sinh viên; Sổ tay SV; Quyền/nghĩa vụ SV |
| **07** | 6 | Chương II | Điều 5 (khoản 1–6, bảng thời gian học); Điều 6 | ĐÃ KIỂM CHỨNG | Thời gian đào tạo chuẩn; Thời gian tối đa gấp 2 lần; VLVH dài hơn 20% |
| **08** | 7 | Chương II | Điều 6 (khoản 1–6); Điều 7 (khoản 1–2) | ĐÃ KIỂM CHỨNG | TKB $\le 15$ giờ/tuần, 4 giờ/ngày; Trực tuyến $\le 30$%; ĐK học trước 4 tuần |
| **09** | 8 | Chương II | Điều 7 (khoản 2–3); Điều 8; Điều 9 (khoản 1a) | ĐÃ KIỂM CHỨNG | Hạn mức tín chỉ 4 năm (7–15), 5 năm (9–20), 6 năm (10–23); Cải thiện lấy thi sau cùng |
| **10** | 9 | Chương II | Điều 9 (khoản 1a–d, khoản 2); Điều 10 (khoản 1–3) | ĐÃ KIỂM CHỨNG | Cảnh báo học tập ĐTB kỳ < 4.7 hoặc < 5.0; Nợ > 24 tín chỉ; Cảnh báo 2 lần liên tiếp buộc thôi học |
| **11** | 10 | Chương II | Điều 10 (khoản 3); Điều 11 (khoản 1–8) | ĐÃ KIỂM CHỨNG | Song bằng: năm thứ 2, ĐTB $\ge 7.0$ (ĐBCL) hoặc $\ge 5.5$ (trúng tuyển); CT1 < 5.5 dừng học CT2 |
| **12** | 11 | Chương II | Điều 11 (khoản 9–10); Điều 12; Điều 13 (khoản 1–2) | ĐÃ KIỂM CHỨNG | Chuyển ngành sau năm 1 trước năm cuối, duy nhất 1 lần; Chuyển trường |
| **13** | 12 | Chương II | Điều 13 (khoản 3–4); Điều 14 (khoản 1–5b) | ĐÃ KIỂM CHỨNG | Chuyển sang VLVH/từ xa; Liên kết đào tạo VLVH (giảng viên cơ hữu $\ge 70$%) |
| **14** | 13 | Chương II | Điều 14 (khoản 5c–d); Điều 15; Điều 16 (bảng xếp năm) | ĐÃ KIỂM CHỨNG | Xếp năm học: Năm 1 (<31 TC), Năm 2 (31–64), Năm 3 (65–96), Năm 4 (97–128), Năm 5 (129–160), Năm 6 ($\ge 161$) |
| **15** | 14 | Chương III | Điều 17 (khoản 1, bảng quy đổi điểm học phần, khoản 1a–c) | ĐÃ KIỂM CHỨNG | Điểm $\ge 5.0$ (D+) tích lũy; D (4.0–4.9) không đạt; Trọng số LT 10%-30%-60% |
| **16** | 15 | Chương III | Điều 17 (khoản 2–3); Điều 18 (khoản 1–5) | ĐÃ KIỂM CHỨNG | Điểm M; Cấm thi khi vắng > 50% tiết hoặc vắng > 50% kỳ kiểm tra; Thi lại cho điểm < 5.0 |
| **17** | 16 | Chương III | Điều 18 (khoản 5–11); Điều 19; Điều 20 (khoản 1–2) | ĐÃ KIỂM CHỨNG | Điểm thi lại giới hạn D+ hoặc C+; Miễn trừ tín chỉ $\le 50$%; Lưu bài thi 2 năm, bảng điểm vĩnh viễn |
| **18** | 17 | Chương III | Điều 20 (khoản 2–4, bảng xếp loại học lực); Điều 21 (khoản 1) | ĐÃ KIỂM CHỨNG | Công thức bình quân gia quyền; Bảng xếp loại học lực (Xuất sắc $\ge 9.00$, Giỏi $\ge 8.00$) |
| **19** | 18 | Chương III | Điều 21 (khoản 2–3); Điều 22 (khoản 1–4) | ĐÃ KIỂM CHỨNG | Phúc khảo bài thi kết thúc tại Phòng Khảo thí & ĐBCLGD; Phụ lục văn bằng |
| **20** | 19 | Chương IV | Điều 23; Điều 24; Điều 25 (khoản 1) | ĐÃ KIỂM CHỨNG | Thực tập cuối khóa, ĐA/KLTN chấm thang 10; Điều kiện tốt nghiệp |
| **21** | 20 | Chương IV | Điều 25 (khoản 2–3); Điều 26; Điều 27 (khoản 1) | ĐÃ KIỂM CHỨNG | ĐTB tích lũy tốt nghiệp $\ge 5.5$; Thi lại > 5% tín chỉ bị giảm 1 bậc tốt nghiệp (Xuất sắc/Giỏi); Gia hạn 03 năm |
| **22** | 21 | Chương IV | Điều 27 (khoản 2–4) | ĐÃ KIỂM CHỨNG | Giấy chứng nhận tốt nghiệp tạm thời; Bằng chỉ cấp một lần (mất/hỏng cấp bản sao) |
| **23** | 22 | Chương V | Điều 28 (khoản 1–4, bảng kỷ luật thi cử) | ĐÃ KIỂM CHỨNG | Bảng xử lý vi phạm thi cử: Khiển trách (-25%), Cảnh cáo (-50%), Đình chỉ (-100%) |
| **24** | 23 | Chương V | Điều 28 (khoản 5–12); Điều 29 (khoản 1–2b) | ĐÃ KIỂM CHỨNG | Thi hộ: lần 1 đình chỉ 1 năm, lần 2 buộc thôi học; Tiêu chuẩn và trách nhiệm GVCN |
| **25** | 24 | Chương V | Điều 29 (khoản 2c, 3); Điều 30; Điều 31 | ĐÃ KIỂM CHỨNG | Quyền lợi GVCN; Khảo sát ý kiến SV lưu 2 năm; Trách nhiệm các đơn vị |
| **26** | 25 | Chương V | Điều 32 (khoản 1–3) | ĐÃ KIỂM CHỨNG | Hiệu lực thi hành cho sinh viên chính quy tín chỉ; Ký và đóng dấu Hiệu trưởng |

---

## 4. PHÂN TÍCH SAI LỆCH VÀ ĐỀ XUẤT ĐÍNH CHÍNH FILE 02

Qua quá trình đối chiếu đối xứng giữa tệp văn bản cũ `02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md` và 26 trang scan gốc QĐ 580, tác giả ghi nhận 10 điểm khác biệt cốt lõi đã được ghi vào `NHAT_KY_DINH_CHINH.csv`. Các sai lệch trọng yếu gồm:

1. **Khái niệm và ngưỡng tích lũy điểm học phần:**
   - *Văn bản cũ:* Ghi nhận điểm D (4.0 – 4.9) là đạt môn và được tính tích lũy; mức điểm A bắt đầu từ 8.5.
   - *QĐ 580 gốc (Điều 17 khoản 1):* Quy định dứt khoát chỉ những học phần có điểm đánh giá từ **5.0 trở lên (D+)** mới được công nhận là học phần tích lũy. Mức điểm 4.0 – 4.9 (D) và dưới 4.0 (F) đều bị phân loại vào nhóm **"Không đạt"**. Điểm A bắt đầu từ 9.0 trở lên.
2. **Quy định học cải thiện và nguyên tắc tính điểm:**
   - *Văn bản cũ:* Cho phép cải thiện điểm D và D+, đồng thời lấy điểm cao nhất giữa các lần học để tính GPA.
   - *QĐ 580 gốc (Điều 8 khoản 3):* Chỉ cho phép học cải thiện đối với các học phần có điểm đạt từ **5.0 đến dưới 6.5**. Kết quả của **lần thi sau cùng** được dùng để tính vào điểm trung bình tích lũy (không lấy điểm cao nhất). Vì điểm D thuộc diện không đạt nên sinh viên bắt buộc phải học lại chứ không phải học cải thiện.
3. **Trần điểm thi lại kết thúc học phần:**
   - *Văn bản cũ:* Không nêu khống chế trần điểm thi lại.
   - *QĐ 580 gốc (Điều 18 khoản 6):* Khống chế trần điểm sau khi thi lại chỉ được giới hạn ở mức **điểm D+ hoặc điểm C+**.
4. **Cơ cấu tổ chức năm học và khối lượng tín chỉ đăng ký:**
   - *Văn bản cũ:* Nêu trường đào tạo 2 học kỳ chính (15 tuần) và 1 học kỳ phụ; định mức đăng ký từ 14 đến 25 tín chỉ.
   - *QĐ 580 gốc (Điều 3 khoản 2, Điều 7 khoản 2):* Trường tổ chức đào tạo mỗi năm gồm **03 học kỳ** chính thức (10–12 tuần học + 2 tuần đánh giá). Hạn mức tín chỉ được phân hóa theo chương trình: 4 năm (7–15 TC/kỳ), 5 năm (9–20 TC/kỳ), 6 năm (10–23 TC/kỳ).
5. **Điều kiện công nhận tốt nghiệp:**
   - *Văn bản cũ:* Nêu CPA tích lũy từ 2.00 (thang 4), bổ sung 05 chuẩn đầu ra (chứng chỉ AI), điểm rèn luyện và trả sách thư viện.
   - *QĐ 580 gốc (Điều 25 khoản 2, Điều 26 khoản 2):* Điểm trung bình tích lũy toàn khóa yêu cầu từ **5.5 trở lên (thang điểm 10)**. Sinh viên thi lại quá 5% tổng số tín chỉ sẽ bị hạ một bậc xếp loại tốt nghiệp (đối với loại Xuất sắc và Giỏi). Các nội dung về điểm rèn luyện và chuẩn đầu ra bổ sung được tách thành mục riêng vì thuộc phạm vi điều chỉnh của các văn bản khác.

---

## 5. TẬP PHÁT TRIỂN 10 CA HỌC VỤ CHUẨN (DEV_10_CAU_QD580)

Nhằm phục vụ công tác kiểm định chất lượng phản hồi của mô hình ngôn ngữ sau khi nạp văn bản QĐ 580, tập dữ liệu `DEV_10_CAU_QD580.jsonl` được thiết kế chặt chẽ theo 4 phân nhóm tình huống thực tế:

1. **Nhóm 1: Câu hỏi trực tiếp (Direct Regulatory Questions - 6 ca):**
   - `DEV_01`: Thang điểm học phần và ngưỡng tích lũy $\ge 5.0$ (Điều 17 khoản 1).
   - `DEV_02`: Quy định tổ chức 03 học kỳ/năm học và thời lượng 10–12 tuần (Điều 3 khoản 2).
   - `DEV_03`: Khối lượng tín chỉ tối thiểu và tối đa theo hệ 4, 5, 6 năm (Điều 7 khoản 2).
   - `DEV_04`: Tiêu chuẩn đăng ký học cùng lúc hai chương trình song bằng (Điều 11 khoản 2).
   - `DEV_05`: Trần điểm thi lại giới hạn D+/C+ và các môn không thi lại (Điều 18 khoản 5, 6).
   - `DEV_06`: 5 tiêu chuẩn xét và công nhận tốt nghiệp đại học (Điều 25 khoản 1, 2).
2. **Nhóm 2: Tình huống đời thường (Colloquial Queries - 2 ca):**
   - `DEV_07`: Sinh viên bị 4.5 điểm (điểm D) hỏi về việc tích lũy và học lại (Điều 17 khoản 1, Điều 8 khoản 1).
   - `DEV_08`: Sinh viên hỏi về số tín chỉ tối đa được đăng ký để học vượt ra trường sớm (Điều 7 khoản 2).
3. **Nhóm 3: Hội thoại nối tiếp có ngữ cảnh (Contextual Multi-turn - 1 ca):**
   - `DEV_09`: Nối tiếp câu hỏi về hạn đăng ký muộn sang câu hỏi về điều kiện rút môn và hoàn phí. Hệ thống phải phân định rõ QĐ 580 không quy định biểu phí hoàn mà chỉ nêu nguyên tắc tính tín chỉ học phí.
4. **Nhóm 4: Ngoài phạm vi / Thiếu căn cứ (Out-of-Scope / Insufficient Grounding - 1 ca):**
   - `DEV_10`: Hỏi về mức tiền học phí cụ thể của 1 tín chỉ năm học 2026-2027 và cách tính điểm rèn luyện. Hệ thống từ chối đưa ra số tiền và cách chấm điểm rèn luyện dựa trên QĐ 580 vì văn bản này không công bố biểu giá tài chính chi tiết hay quy chế rèn luyện.

---

## 6. ĐÁNH GIÁ MỨC ĐỘ SẴN SÀNG VÀ HƯỚNG TRIỂN KHAI TIẾP THEO

### 6.1. Mức độ sẵn sàng của dữ liệu
- **Về tính đầy đủ:** $26/26$ trang ($100\%$) của Quyết định số 580/QĐ-ĐHNCT đã được chuyển đổi thành công sang văn bản số hóa có mốc định vị rõ ràng.
- **Về tính tin cậy:** Toàn bộ các bảng biểu (thời gian đào tạo, định mức mở lớp, định mức tín chỉ, bảng thang điểm, bảng xếp năm đào tạo, bảng kỷ luật thi cử) đã được kiểm tra chéo từng dòng và từng ô số liệu.
- **Về tính sẵn sàng ingestion:** Bộ tệp `QD580_THEO_TRANG.md` và `QD580_PAGES.jsonl` đáp ứng hoàn toàn các tiêu chuẩn kỹ thuật để làm đầu vào cho mô-đun cắt đoạn (chunking), đánh chỉ mục và tạo vector embedding trong Tuần 2.

### 6.2. Kế hoạch bước tiếp theo
1. Duy trì tính bất biến của các tệp nguồn gốc trong `01_Tài Liệu Gốc (PDF)/` và 6 tệp Markdown cũ trong `02_Văn Bản Đã Làm Sạch (Text)/` để phục vụ công tác đối sánh thực nghiệm.
2. Sử dụng `QD580_PAGES.jsonl` làm tập dữ liệu chuẩn mực để chạy thử nghiệm các chiến lược phân đoạn văn bản (Article-level chunking vs Page-level chunking).
3. Sử dụng `DEV_10_CAU_QD580.jsonl` để đánh giá độ chính xác (Precision/Recall và RAG Faithfulness) ngay sau khi thiết lập xong cơ sở dữ liệu vector ChromaDB.
