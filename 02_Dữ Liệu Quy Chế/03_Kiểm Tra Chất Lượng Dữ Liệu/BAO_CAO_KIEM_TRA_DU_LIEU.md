# BÁO CÁO KIỂM TRA CHẤT LƯỢNG DỮ LIỆU ĐẦU VÀO
## DỰ ÁN: TRỢ LÝ ẢO TRA CỨU QUY CHẾ HỌC VỤ DNC ỨNG DỤNG RAG

> **Ngày thực hiện kiểm tra:** 31/10/2026  
> **Đơn vị thực hiện:** Nhóm sinh viên thực hiện Đồ án 2 — Lớp DH23TIN, Trường Công nghệ Số & Trí tuệ Nhân tạo, Trường Đại học Nam Cần Thơ (DNC)  
> **Phạm vi kiểm tra:** Toàn bộ 03 tài liệu PDF gốc và 06 file văn bản Markdown đã làm sạch tại thư mục `02_Dữ Liệu Quy Chế`  
> **Căn cứ tài liệu hệ thống:** `PROJECT.md`, `LOGIC.md`, `ROADMAP.md` (Phiên bản cập nhật ngày 31/10/2026)

---

## 1. TỔNG QUAN VÀ KIỂM KÊ DỮ LIỆU HIỆN CÓ

### 1.1. Hiện trạng thư mục dữ liệu

Thư mục dữ liệu dự án gồm hai nhánh lưu trữ chính:
1. `02_Dữ Liệu Quy Chế/01_Tài Liệu Gốc (PDF)`: Chứa 03 tệp PDF văn bản pháp quy và tài liệu hướng dẫn gốc.
2. `02_Dữ Liệu Quy Chế/02_Văn Bản Đã Làm Sạch (Text)`: Chứa 06 tệp Markdown định dạng văn bản đã được biên tập trước đó, bao phủ 06 nhóm nội dung quy chế học vụ.

Tất cả các tệp đều mở bình thường bằng các thư viện phân tích cấu trúc (`pdfplumber`, `pypdf`, `pypdfium2`), không có tệp nào bị hỏng (corrupt) về mặt vật lý lưu trữ.

### 1.2. Bảng kiểm kê chi tiết tài liệu PDF gốc

Bảng 1.1 Kiểm kê chi tiết 03 tài liệu PDF gốc trong kho dữ liệu
| STT | Tên tệp PDF | Dung lượng | Số trang | Số hiệu / Căn cứ văn bản | Ngày ban hành | Cơ quan / Người ký |
| :---: | :--- | :---: | :---: | :--- | :---: | :--- |
| 1 | `01-HUONG-DAN-GIANG-VIEN-NCT.pdf` | 2.13 MB (2.229.396 bytes) | 6 | Số: 55/HD-ĐHNCT | 28/04/2016 | KT. Hiệu trưởng — Phó Hiệu trưởng TS. Nguyễn Văn Quang |
| 2 | `580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf` | 6.33 MB (6.635.360 bytes) | 26 | Quyết định số 580/QĐ-ĐHNCT | 02/08/2024 | Hiệu trưởng TS. Nguyễn Văn Quang |
| 3 | `so_tay_sinh_vien_2026_2027.pdf` | 73.13 MB (76.682.642 bytes) | 49 | Sổ tay sinh viên năm học 2026–2027 (gồm nhiều QĐ trích yếu) | Năm học 2026–2027 | Trường Đại học Nam Cần Thơ |
*Nguồn: Tổng hợp từ kết quả kiểm định kỹ thuật ngày 31/10/2026*

### 1.3. Phân biệt mục đích và đối tượng áp dụng của tài liệu

Qua kiểm tra nội dung và thể thức văn bản:
- **Tài liệu hướng dẫn giảng viên (`01-HUONG-DAN-GIANG-VIEN-NCT.pdf`):** Ban hành từ năm 2016 (Số 55/HD-ĐHNCT). Đây là văn bản nội bộ quy định nghĩa vụ của giảng viên (thực hiện giờ giảng, ra đề thi trước 02 tuần, tổ chức coi thi, vào sổ điểm, chấm thi). Một số quy định về tỷ lệ đánh giá học phần tại văn bản này (ví dụ: thi cuối kỳ 50% tại Điều 4) có sự khác biệt so với Quyết định 580 (thi kết thúc học phần 60%). **Quyết định:** Tài liệu này là hướng dẫn nghiệp vụ dành riêng cho cán bộ, giảng viên; không phù hợp làm nguồn dữ liệu trả lời sinh viên trong hệ thống chatbot, tránh xung đột thông tin và gây hiểu lầm cho người học. Quyết định chưa kích hoạt tệp này cho bản thử nghiệm.
- **Quy chế đào tạo đại học (`580/QĐ-ĐHNCT`):** Ban hành ngày 02/08/2024, gồm 05 chương với 32 điều. Trong phạm vi 03 tệp PDF hiện có, đây là văn bản quy chế đào tạo đại học theo hệ thống tín chỉ hiện hành quy chuẩn nhất của trường, điều chỉnh các quyền lợi và nghĩa vụ học tập cốt lõi của sinh viên. Đây là nguồn chuẩn xác bắt buộc cho Nhóm 02 (Quy chế đào tạo).
- **Sổ tay sinh viên 2026–2027 (`so_tay_sinh_vien_2026_2027.pdf`):** Tài liệu cẩm nang chính thức phát hành cho sinh viên đầu khóa năm học 2026–2027, tích hợp các quyết định trích yếu quan trọng: QĐ 444 (Tầm nhìn, sứ mạng), QĐ 1358 (Khen thưởng), QĐ 1042 (Nội quy lớp học), QĐ 42B & QĐ 123 (Học phí, miễn giảm học phí), QĐ 350 (Chuẩn đầu ra). Đây là nguồn trực tiếp bao phủ cả 06 nhóm nội dung cho sinh viên.

### 1.4. Bảng kiểm kê chi tiết 06 tệp Markdown đã làm sạch

Bảng 1.2 Kiểm kê cấu trúc 06 tệp Markdown trong thư mục văn bản đã làm sạch
| Tên tệp Markdown | Nhóm nội dung | Dung lượng | Số dòng | Số đề mục (#) | Chủ đề bao phủ chính |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `01_Tong_Quan_Va_Danh_Ba_DNC.md` | Nhóm 01 | 11.117 bytes | 91 | 9 | Thông tin chung, sứ mạng, tầm nhìn, danh bạ phòng ban/khoa, hệ sinh thái DNC |
| `02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md` | Nhóm 02 | 14.915 bytes | 159 | 25 | Tổ chức tín chỉ, đăng ký môn, thang điểm đánh giá, thi lại, GPA, cảnh báo học vụ, tốt nghiệp |
| `03_Cong_Tac_Sinh_Vien_Va_Diem_Ren_Luyen.md` | Nhóm 03 | 14.199 bytes | 120 | 12 | Quyền/nghĩa vụ sinh viên, nội/ngoại trú, 5 tiêu chí ĐRL (100đ), khung kỷ luật 29 hành vi |
| `04_Quy_Che_Khen_Thuong_Va_Ky_Luat_Sinh_Vien.md` | Nhóm 04 | 11.378 bytes | 93 | 19 | Danh hiệu thi đua (QĐ 1358/QĐ-ĐHNCT), 12 điều nội quy phòng học (QĐ 1042/QĐ-ĐHNCT) |
| `05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md` | Nhóm 05 | 8.995 bytes | 85 | 16 | Quy định học phí (QĐ 42B), miễn giảm học phí (QĐ 123), học bổng khuyến khích & doanh nghiệp |
| `06_Quy_Dinh_Chuan_Dau_Ra_Tot_Nghiep.md` | Nhóm 06 | 9.515 bytes | 79 | 11 | Chuẩn đầu ra Ngoại ngữ (QĐ 350), Tin học, Kỹ năng mềm, Chứng chỉ AI, Kỹ năng nghề |
*Nguồn: Tổng hợp từ kết quả kiểm định kỹ thuật ngày 31/10/2026*

---

## 2. KIỂM TRA KHẢ NĂNG TRÍCH XUẤT VĂN BẢN TỪ PDF

### 2.1. Phương pháp và tiêu chí phân loại từng trang

Toàn bộ 81 trang của 03 tài liệu PDF được rà soát kết hợp giữa đo lường kỹ thuật tự động và đối chiếu thủ công:
- **Đo lường kỹ thuật tự động (bằng script `kiem_tra_trang_pdf.py`):** Sử dụng `pdfplumber` để đo chính xác số lượng ký tự văn bản trích xuất được (`extract_text()`) và đếm số lượng đối tượng hình ảnh (`len(page.images)`) trên từng trang.
- **Nhãn phân loại và kiểm định nội dung thủ công:** Sau khi script đo số ký tự, người kiểm tra trực tiếp đối chiếu hình ảnh trang được render qua `pypdfium2` (scale 1.5) để gán nhãn phân loại chính xác, đảm bảo không kết luận phiến diện chỉ dựa trên số ký tự trích xuất.

Các trang được phân loại chính xác thành 4 nhóm theo quy chuẩn:
1. **Có text và trích xuất đọc được:** Trang có text layer chuẩn UTF-8, đọc được tiếng Việt có dấu đầy đủ, cấu trúc rõ ràng.
2. **Trang ảnh/scan có nội dung nhưng cần OCR:** Trang chứa nội dung chữ nhưng ở định dạng hình ảnh raster (scan hoặc đồ họa vector không nhúng text), lệnh trích xuất text trả về 0 ký tự hoặc khoảng trắng.
3. **Có text nhưng lỗi font, thứ tự đọc, bảng hoặc mất dấu:** Trang có text layer nhưng font bị mã hóa sai bảng mã tiếng Việt (mất dấu thanh, ký tự lạ), bảng biểu bị vỡ dòng hoặc xáo trộn thứ tự từ ngữ.
4. **Trang trắng hoặc chỉ có hình minh họa:** Trang bìa không chứa điều khoản quy chế, trang trắng phân cách chương, hoặc trang chỉ có hình ảnh nghệ thuật/quảng cáo.

### 2.2. Bảng thống kê phân loại khả năng trích xuất

Bảng 2.1 Thống kê phân loại khả năng trích xuất trên 81 trang PDF
| Tên tệp PDF | Tổng số trang | Nhóm 1: Text tốt | Nhóm 2: Ảnh scan cần OCR | Nhóm 3: Lỗi font / mất dấu | Nhóm 4: Bìa / chỉ có ảnh |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `01-HUONG-DAN-GIANG-VIEN-NCT.pdf` | 6 | 0 (0%) | 0 (0%) | 6 (100%) | 0 (0%) |
| `580-QD-DHNCT-quy-che-dao-tao...` | 26 | 0 (0%) | 26 (100%) | 0 (0%) | 0 (0%) |
| `so_tay_sinh_vien_2026_2027.pdf` | 49 | 0 (0%) | 47 (95.9%) | 0 (0%) | 2 (4.1%) |
| **Tổng cộng toàn bộ kho dữ liệu** | **81** | **0 (0.0%)** | **73 (90.1%)** | **6 (7.4%)** | **2 (2.5%)** |
*Nguồn: Trích xuất từ tệp `KIEM_TRA_TRANG_PDF.csv` ngày 31/10/2026*

> [!WARNING]
> **Phát hiện cốt lõi về chất lượng dữ liệu trích xuất:**
> Trong toàn bộ 81 trang PDF hiện có trong kho dữ liệu gốc, **0% trang đạt điều kiện Nhóm 1 (có text sạch đọc được trực tiếp)**. Cụ thể:
> - Tệp `QĐ 580` (26 trang) và `Sổ tay sinh viên` (49 trang) hoàn toàn không có text layer (extract ra 0 ký tự). Toàn bộ nội dung nằm trong lớp ảnh scan và đồ họa xuất bản.
> - Tệp `Hướng dẫn giảng viên` (6 trang) có text layer nhưng bị hỏng bảng mã tiếng Việt nặng (ví dụ: `BOorAo DT)C vA DAo TAO CONG HoA xA HOI CHiT NGHiA VI¥T NAM`, `Di~u 1:Thuc hi~n gift giang`).
> - Do đó, **không thể nạp trực tiếp PDF gốc vào bộ chia đoạn (chunker) hoặc embedding model hiện tại nếu chưa qua xử lý OCR tiếng Việt chất lượng cao**.

### 2.3. Đánh giá thử nghiệm công cụ OCR cục bộ và giới hạn kỹ thuật

Nhóm nghiên cứu đã tiến hành rà soát các công cụ OCR cục bộ sẵn có trên môi trường máy chủ phát triển (Windows 11, Python 3.14.6):
- Thư viện `tesseract` chưa được cài đặt trong biến môi trường PATH hệ thống.
- Giao diện lập trình Windows Runtime `Windows.Media.Ocr.OcrEngine` có sẵn trong hệ điều hành nhưng hiện tại chỉ cài đặt gói ngôn ngữ tiếng Anh (`en-US`, `en-GB`), không có gói nhận dạng tiếng Việt (`vi-VN`).
- Khi chạy thử nghiệm nhận dạng trên trang 1 của QĐ 580 với engine tiếng Anh, kết quả trả về văn bản không nhận diện được dấu thanh tiếng Việt và cấu trúc câu bị đứt đoạn.
- **Giới hạn kết luận:** Việc thực hiện OCR toàn bộ tài liệu cần được chuẩn bị bằng công cụ chuyên dụng cho tiếng Việt (như VietOCR, PaddleOCR hoặc Tesseract có bổ sung dữ liệu huấn luyện `vie.traineddata`) trong tuần triển khai Ingestion (Tuần 2).

---

## 3. ĐỐI CHIẾU NỘI DUNG MARKDOWN VỚI NGUỒN GỐC

Quá trình đối chiếu được thực hiện bằng cách render trực quan từng trang tài liệu PDF scan và so sánh song song với các đoạn văn bản tương ứng trong 06 tệp Markdown đã làm sạch.

Tất cả các đoạn kiểm tra đều được phân loại nghiêm ngặt vào một trong 4 nhóm:
1. **Đã đối chiếu và khớp:** Nội dung, số liệu, căn cứ và thuật ngữ đồng nhất hoàn toàn với tài liệu gốc.
2. **Có sai lệch:** Có sự khác biệt về số liệu, tỷ lệ, điều kiện áp dụng, hoặc có sự thêm bớt diễn giải làm thay đổi bản chất quy chế.
3. **Chưa kiểm tra:** Các đoạn văn bản nằm ngoài mẫu khảo sát đợt 1.
4. **Chưa tìm thấy căn cứ trong các nguồn hiện có:** Nội dung trong Markdown không tìm thấy dấu vết trong 03 tài liệu PDF hiện có.

### 3.1. Phân tích chi tiết từng tệp Markdown

#### File 1: `01_Tong_Quan_Va_Danh_Ba_DNC.md`
- **Nguồn đối chiếu:** Sổ tay sinh viên 2026–2027 (Trang bìa, Trang in 01–17; tương ứng Trang PDF 1, 4–20).
- **Mục đã đối chiếu và khớp:** Thông tin chung, địa chỉ (168 Nguyễn Văn Cừ nối dài), hotline tuyển sinh (0939 257 838), website; Sứ mạng, tầm nhìn chiến lược theo QĐ 444/QĐ-CTHĐT-ĐHNCT; Hệ sinh thái doanh nghiệp DNC (Bệnh viện ĐHNCT 300 giường, Showroom ô tô, Trung tâm Phần mềm DNC...).
- **Sai lệch thông tin được phát hiện:** Toàn bộ bảng danh bạ liên hệ các phòng ban (Mục 3) chứa số điện thoại và địa chỉ email có sự sai lệch so với bản scan Sổ tay sinh viên:
  - *Phòng Quản lý Đào tạo:* SĐT trong Sổ tay là `02923 798 999` (Zalo `0907668874`), Email `phongdaotao@nctu.edu.vn` (Markdown ghi là 798 168 và daotao@...).
  - *Phòng Tổ chức - Hành chính:* SĐT trong Sổ tay là `02923 798 668`, Email `phongtc-hc@nctu.edu.vn` (Markdown ghi là 798 666 và tchc@...).
  - *Phòng Quản lý HSSV:* SĐT trong Sổ tay là `02923 798 444`, Email `phongqlhssv@nctu.edu.vn` (Markdown ghi là 798 333 và ctsv@...).
  - *Phòng Tài chính - Kế hoạch:* SĐT trong Sổ tay là `02923 751 668`, Email `phongtc-kh@nctu.edu.vn` (Markdown ghi là 798 444 và taichinh@...).
  - *Phòng Khảo thí & ĐBCLGD:* SĐT trong Sổ tay là `02923 798 668`, Zalo `0392972799`. Về email, bản scan trang in 10 ghi `phongtc-hc@nctu.edu.vn` (đây là điểm bất thường cần xác minh lại với trường vì trùng tên viết tắt Phòng Tổ chức - Hành chính; Markdown ghi `khaothi@nctu.edu.vn` chưa có căn cứ trong bản in).

#### File 2: `02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md`
- **Nguồn đối chiếu:** Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024 (Trang in 1–25, PDF 2–26) và Sổ tay sinh viên (Trang in 18–24, PDF 21–27).
- **Mục đã đối chiếu và khớp:** Tỷ trọng điểm học phần 10% chuyên cần - 30% giữa kỳ - 60% thi kết thúc học phần (Điều 17 Khoản 1.a QĐ 580 & Trang in 20 Sổ tay); Điều kiện học cùng lúc 2 chương trình (Điều 11 QĐ 580); Các trường hợp buộc thôi học (Trang in 22 Sổ tay); Điều kiện xét tốt nghiệp (Điều 25 QĐ 580).
- **Sai lệch nghiêm trọng được phát hiện:**
  - *Thang điểm đánh giá và điều kiện tích lũy học phần (Điều 17 QĐ 580):* Markdown chép thang điểm chung của trường khác (Điểm A từ 8.5–10.0; B+ từ 8.0–8.4; D từ 4.0–4.9 là Đạt/Tích lũy). **Thực tế tại DNC (QĐ 580 và Sổ tay trang 20):** Điểm A là `9.0 – 10.0`; Điểm B+ là `8.0 – 8.9`; Điểm D+ là `5.0 – 5.4`; và **Điểm D (4.0 – 4.9) là KHÔNG ĐẠT (KHÔNG ĐƯỢC TÍCH LŨY)**. Quy chế DNC nêu rõ: chỉ học phần có điểm đánh giá từ 5.0 trở lên (D+) mới được tính là học phần tích lũy. Việc Markdown ghi điểm D là tích lũy là sai lệch bản chất học vụ rất nghiêm trọng.
  - *Tổ chức năm học (Điều 3 Khoản 2.b QĐ 580):* DNC tổ chức mỗi năm gồm **03 học kỳ** (mỗi kỳ 10–12 tuần học + 2 tuần đánh giá). Markdown ghi sai thành mô hình 02 học kỳ chính (15 tuần) + 01 học kỳ phụ hè (5 tuần).
  - *Khối lượng tín chỉ đăng ký (Điều 7 Khoản 2 QĐ 580):* CT 4 năm đăng ký tối thiểu 7 và tối đa 15 tín chỉ/kỳ; CT 5 năm là 9–20; CT 6 năm là 10–23. Markdown ghi sai thành 14–25 tín chỉ.
  - *Quy định học cải thiện (Điều 8 Khoản 3 QĐ 580):* QĐ 580 quy định lấy *kết quả của lần thi sau cùng* để tính vào điểm trung bình tích lũy, không phải lấy *điểm cao nhất giữa các lần học* như Markdown nêu.
  - *Khống chế điểm thi lại (Điều 18 Khoản 6 QĐ 580):* Điểm học phần sau khi thi lại chỉ được giới hạn ở mức điểm `D+` hoặc `C+`. Markdown bỏ sót quy định khống chế này.
- **Chưa tìm thấy căn cứ trong nguồn hiện có:** Mục 6.1 về các ngưỡng điểm cảnh báo học tập số thập phân chi tiết (0.80, 1.00, 1.20, 1.40, 1.60, 1.80) không xuất hiện trong văn bản QĐ 580 hay Sổ tay sinh viên.

#### File 3: `03_Cong_Tac_Sinh_Vien_Va_Diem_Ren_Luyen.md`
- **Nguồn đối chiếu:** Sổ tay sinh viên 2026–2027 (Trang in 25–35, PDF 28–38).
- **Mục đã đối chiếu và khớp:** Quyền lợi và nghĩa vụ sinh viên (Trang in 25–27); Quy chế nội trú, ngoại trú (Trang in 34–35); 5 Tiêu chí đánh giá điểm rèn luyện theo thang điểm 100 với cơ cấu 20 – 25 – 20 – 25 – 10 (Trang in 31–33); Khung phân loại kết quả rèn luyện (Xuất sắc ≥90, Tốt 80–89, Khá 65–79, TB 50–64, Yếu 35–49, Kém <35).
- **Chưa tìm thấy căn cứ trong nguồn hiện có:** Mục 4 về "Khung xử lý kỷ luật sinh viên vi phạm (29 hành vi điển hình)". Trong Sổ tay sinh viên Trang in 35 chỉ có một đoạn ngắn quy định về kiểm tra, xử lý vi phạm nội trú KTX. Bảng 29 hành vi này nhiều khả năng được lấy từ Thông tư 10/2016/TT-BGDĐT của Bộ GD&ĐT nhưng chưa tìm thấy văn bản quy định riêng tương ứng của DNC trong 03 tệp PDF hiện có.

#### File 4: `04_Quy_Che_Khen_Thuong_Va_Ky_Luat_Sinh_Vien.md`
- **Nguồn đối chiếu:** Sổ tay sinh viên 2026–2027 (Trang in 36–40, PDF 39–43).
- **Mục đã đối chiếu và khớp:**
  - Quyết định ban hành Quy chế khen thưởng sinh viên: Số `1358/QĐ-ĐHNCT` ngày `09/10/2025` của Hiệu trưởng DNC (Trang in 36).
  - 4 danh hiệu thi đua: Sinh viên Xuất sắc, Sinh viên Giỏi, Thủ khoa toàn khóa học, Thủ khoa đầu vào (Điều 3).
  - Quyết định ban hành Nội quy phòng học: Số `1042/QĐ-ĐHNCT` ngày `12/08/2025` của Hiệu trưởng DNC (Trang in 40).
  - 12 quy định nội quy phòng học (vào lớp đúng giờ, đeo thẻ SV, cấm livestream/TikTok, đi trễ quá 15 phút, giảng viên trễ quá 15 phút báo phòng QLĐT...).
- **Ghi chú thể thức:** Bản scan gốc trình bày 12 điểm gạch đầu dòng, Markdown đã tự động đánh số thành Điều 1 đến Điều 12.

#### File 5: `05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md`
- **Nguồn đối chiếu:** Sổ tay sinh viên 2026–2027 (Trang in 41–44, PDF 44–47).
- **Mục đã đối chiếu và khớp:** Quyết định số `42B/QĐ-ĐHNCT` ngày `16/07/2015` về nộp học phí và chế tài (cấm thi HK1, cấm thi lần 2, lưu ban/thôi học); Quyết định số `123/QĐ-CTHĐT-ĐHNCT` ngày `21/04/2026` của Chủ tịch HĐT về giảm học phí.
- **Sai lệch nội dung được phát hiện:**
  - *Tỷ lệ miễn giảm sinh viên khuyết tật:* Sổ tay quy định sinh viên khuyết tật nặng giảm `20%` học phí/kỳ (Trang in 43). Markdown xếp nhầm vào mức `50%`.
  - *Bỏ sót các diện ưu đãi đặc thù DNC:* Sổ tay quy định các chính sách rất đặc thù của DNC: Thân nhân cán bộ, giảng viên cơ hữu DNC giảm `20%`; Con Hiệu trưởng/Hiệu phó các trường THPT giảm `10%`; Thí sinh hộ khẩu thường trú TP. Đà Nẵng giảm `15%`; Thí sinh hộ khẩu các xã Đại Lộc, Hà Nha, Thượng Đức, Phú Nhuận, Vu Gia giảm `20%` và miễn tiền ký túc xá. Markdown bỏ sót hoàn toàn các nhóm này.
  - *Học bổng khuyến khích học tập:* Markdown tự tạo ra tỷ lệ 100% học phí (GPA ≥3.60, ĐRL ≥90) và 50–70% (GPA 3.20–3.59, ĐRL ≥80). Trong văn bản gốc (Trang in 42 Sổ tay), nhà trường chỉ quy định xét điểm trung bình năm học từ cao xuống thấp và rèn luyện từ tốt trở lên, kinh phí do Chủ tịch HĐT và Hiệu trưởng quyết định theo quy mô quỹ học bổng hàng năm.

#### File 6: `06_Quy_Dinh_Chuan_Dau_Ra_Tot_Nghiep.md`
- **Nguồn đối chiếu:** Sổ tay sinh viên 2026–2027 (Trang in 45, tương ứng Trang PDF 48; lưu ý: Trang PDF 49 là bìa sau chứa mã QR, không phải nội dung chuẩn đầu ra hay trang in 46).
- **Mục đã đối chiếu và khớp:**
  - Căn cứ pháp lý chuẩn đầu ra Ngoại ngữ: Quyết định số `350/QĐ-ĐHNCT` ngày `07/04/2026`.
  - 5 Chuẩn đầu ra bắt buộc: Ngoại ngữ (Tiếng Anh B1 / Bậc 3 VSTEP; Ngôn ngữ Anh đạt C1 + B1 Pháp văn; Y khoa/Răng hàm mặt đạt Bậc 4; Du lịch/Dược học đạt Bậc 3); Tin học (Cơ bản và Nâng cao cho ngành không chuyên CNTT); Kỹ năng mềm; Kỹ năng Trí tuệ nhân tạo (AI Skills Certificate — bắt buộc cho SV chính quy tốt nghiệp từ năm học 2026–2027); Kỹ năng nghề nghiệp.
- **Chưa tìm thấy căn cứ trong nguồn hiện có:** Mục 3 trong Markdown về "Lộ trình khuyến nghị 4 năm và thủ tục nộp chứng chỉ trước 45 ngày" là phần hướng dẫn do người soạn thảo tự thêm vào, không có trong văn bản scan Sổ tay sinh viên.

---

## 4. TỔNG HỢP KẾT QUẢ ĐỐI CHIẾU VÀ ÁNH XẠ NGUỒN

Quá trình đối chiếu mẫu được thực hiện trên 32 vị trí đại diện có chọn lọc qua 06 tệp Markdown và 01 tài liệu hướng dẫn giảng viên. Toàn bộ các đoạn kiểm chứng chi tiết được lưu trữ tại tệp `DOI_CHIEU_NGUON.csv`.

> [!NOTE]
> **Về phương pháp và độ bao phủ của mẫu khảo sát:**
> - Bảng `DOI_CHIEU_NGUON.csv` được tạo từ các nhận xét đã kiểm tra và ghi nhận sau khi so sánh trực quan từng trang tài liệu; script `tao_bang_doi_chieu_va_van_de.py` dùng để xuất bảng dữ liệu cấu trúc chuẩn hóa, không tự động nhận diện AI.
> - Cột "Chưa kiểm tra: 0" trong Bảng 4.1 phản ánh rằng trong phạm vi **32 mục được chọn vào mẫu khảo sát đợt 1**, nhóm kiểm tra đã đối chiếu đủ 32 mục, không bỏ dở mục nào. Điều này **hoàn toàn không đồng nghĩa với việc đã kiểm tra toàn bộ 100% nội dung của 06 tệp Markdown**. Mọi phần văn bản nằm ngoài 32 mục khảo sát vẫn ở trạng thái **Chưa xác minh** và cần tiếp tục đối chiếu.

Bảng 4.1 Bảng tổng hợp mức độ bao phủ và kết quả đối chiếu trên mẫu khảo sát
| Tệp Markdown / Nguồn khảo sát | Tổng số mục khảo sát | Đã đối chiếu & khớp | Có sai lệch | Chưa kiểm tra | Chưa tìm thấy căn cứ | Tỷ lệ khớp trên mẫu |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `01_Tong_Quan_Va_Danh_Ba_DNC.md` | 7 | 3 | 4 | 0 | 0 | 42.9% |
| `02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md` | 9 | 3 | 5 | 0 | 1 | 33.3% |
| `03_Cong_Tac_Sinh_Vien_Va_Diem_Ren_Luyen.md` | 4 | 3 | 0 | 0 | 1 | 75.0% |
| `04_Quy_Che_Khen_Thuong_Va_Ky_Luat_Sinh_Vien.md` | 3 | 3 | 0 | 0 | 0 | 100.0% |
| `05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md` | 5 | 2 | 3 | 0 | 0 | 40.0% |
| `06_Quy_Dinh_Chuan_Dau_Ra_Tot_Nghiep.md` | 3 | 2 | 0 | 0 | 1 | 66.7% |
| **Tổng cộng 06 tệp Markdown** | **31** | **16 (51.6%)** | **12 (38.7%)** | **0 (0.0%)** | **3 (9.7%)** | **51.6%** |
| `[Tài liệu riêng: 01-HUONG-DAN-GIANG-VIEN-NCT.pdf]` | 1 | 1 | 0 | 0 | 0 | (Tài liệu nghiệp vụ GV) |
| **Tổng toàn bộ khảo sát (kể cả tài liệu GV)** | **32** | **17 (53.1%)** | **12 (37.5%)** | **0 (0.0%)** | **3 (9.4%)** | **53.1%** |
*Nguồn: Tính toán động từ tệp `DOI_CHIEU_NGUON.csv` ngày 31/10/2026*

> [!IMPORTANT]
> **Nhận định quan trọng về tính sẵn sàng của dữ liệu Markdown:**
> Mặc dù 06 tệp Markdown đã được tổ chức công phu và bao quát đủ 06 nhóm nội dung, kết quả đối chiếu mẫu cho thấy tỷ lệ sai lệch số liệu và thông tin chưa có căn cứ chiếm tới 48.4% số mục đối chiếu của 06 Markdown (12 sai lệch + 3 chưa có căn cứ trên 31 mẫu).
> Do đó, **06 tệp Markdown hiện tại CHƯA SẴN SÀNG để nạp ngay vào pipeline RAG nếu chưa được đính chính các lỗi sai lệch này**.

---

## 5. DANH SÁCH CÁC VẤN ĐỀ CHẤT LƯỢNG VÀ HƯỚNG XỬ LÝ

Toàn bộ 07 vấn đề chất lượng dữ liệu được theo dõi tại `DANH_SACH_VAN_DE.csv`. Dưới đây là tóm tắt các vấn đề trọng yếu cần giải quyết:

Bảng 5.1 Bảng tổng hợp các vấn đề chất lượng dữ liệu đầu vào
| Mã vấn đề | Nhóm vấn đề | Mức độ | Mô tả tóm tắt | Hướng xử lý đề xuất | Trạng thái |
| :---: | :--- | :---: | :--- | :--- | :---: |
| `ISSUE-DATA-01` | Trích xuất PDF & OCR | **Nghiêm trọng** | 100% trang của QĐ 580 (26 trang) và Sổ tay sinh viên (49 trang) là ảnh scan không có text layer. File hướng dẫn GV bị hỏng font. | Triển khai OCR offline tiếng Việt chuyên dụng hoặc số hóa có kiểm chứng trước khi chunking; không nạp trực tiếp PDF rỗng. | Chờ xử lý |
| `ISSUE-DATA-02` | Quy chế điểm số | **Nghiêm trọng** | File 02 sai thang điểm (A: 9.0–10.0, B+: 8.0–8.9); đặc biệt ghi điểm D (4.0–4.9) là tích lũy trong khi DNC quy định điểm D là KHÔNG ĐẠT. | Hiệu chỉnh ngay bảng quy đổi thang điểm và điều kiện học lại trong File 02 theo Điều 17 QĐ 580. | Chờ xử lý |
| `ISSUE-DATA-03` | Cấu trúc năm học | **Nghiêm trọng** | File 02 ghi 2 kỳ chính (15 tuần) + 1 hè (5 tuần), trái ngược quy chế DNC là 03 học kỳ/năm (10–12 tuần học + 2 tuần thi) và mức tín chỉ 7–15, 9–20, 10–23. | Sửa lại mô tả năm học và giới hạn tín chỉ theo đúng Điều 3 và Điều 7 QĐ 580. | Chờ xử lý |
| `ISSUE-DATA-04` | Danh bạ liên hệ | **Nghiêm trọng** | File 01 bị chế tạo số điện thoại hàng loạt (798 168, 798 333, 798 444, 798 555...) và email không khớp thực tế. | Thay thế toàn bộ bằng bảng danh bạ chuẩn tại Trang in 09–10 Sổ tay sinh viên (kèm số Zalo và phòng trực). | Chờ xử lý |
| `ISSUE-DATA-05` | Miễn giảm & Học bổng | **Nghiêm trọng** | File 05 phân sai nhóm khuyết tật (20% thành 50%), bỏ sót các chính sách đặc thù của DNC (Đà Nẵng, Quảng Nam, con CB-GV), tự chế tạo tỷ lệ học bổng. | Cập nhật lại các tỷ lệ phần trăm theo QĐ 123 (Trang 43 Sổ tay) và bỏ các ngưỡng điểm học bổng tự chế tạo. | Chờ xử lý |
| `ISSUE-DATA-06` | Căn cứ chưa xác minh | **Trung bình** | Bảng 29 hành vi kỷ luật (File 03), ngưỡng cảnh báo học tập số thập phân (File 02), lộ trình 4 năm chuẩn đầu ra (File 06) chưa có căn cứ trong 3 PDF. | Đánh dấu metadata `source_verified = False`, tạm thời chưa kích hoạt các đoạn này trong kho phục vụ hỏi đáp. | Chờ xử lý |
| `ISSUE-DATA-07` | Phân loại tài liệu GV | **Trung bình** | Tệp `01-HUONG-DAN-GIANG-VIEN-NCT.pdf` (năm 2016) là văn bản nội bộ dành cho giảng viên, có tỷ lệ điểm cũ (50% KTHP) khác biệt với QĐ 580 (60% KTHP), chưa có căn cứ hiệu lực hiện hành. | Đưa vào nhóm tài liệu nghiệp vụ giảng viên, không kích hoạt làm nguồn tri thức trong chatbot sinh viên bản thử. | Đã ghi nhận |
*Nguồn: Trích xuất từ tệp `DANH_SACH_VAN_DE.csv` ngày 31/10/2026*

---

## 6. ĐÁNH GIÁ KHẢ NĂNG SỬ DỤNG QUYẾT ĐỊNH 580 CHO BẢN THỬ ĐẦU TIÊN (BASELINE)

Theo định hướng trong `PROJECT.md` và `ROADMAP.md`, việc lựa chọn một nhóm tài liệu hạt nhân chuẩn xác để chạy thông suốt toàn bộ luồng pipeline từ trích xuất, chia đoạn, lập chỉ mục đến truy xuất và sinh câu trả lời trong Tuần 2 là ưu tiên hàng đầu.

### 6.1. Đánh giá ưu điểm của Quyết định 580/QĐ-ĐHNCT
1. **Căn cứ pháp lý rõ ràng:** Quyết định 580 ban hành ngày 02/08/2024 bởi Hiệu trưởng TS. Nguyễn Văn Quang, là văn bản quy chế đào tạo đại học chính quy theo hệ thống tín chỉ hoàn chỉnh nhất trong 03 tệp PDF hiện có của kho dữ liệu.
2. **Cấu trúc văn bản quy phạm chặt chẽ:** Toàn văn gồm 05 chương với 32 điều rõ ràng, dễ dàng phân đoạn tự nhiên theo ranh giới Điều/Khoản (`Chương I -> Điều 1 -> Khoản 1, 2...`), hạn chế tối đa hiện tượng phân mảnh ngữ nghĩa (semantic fragmentation).
3. **Độ bao phủ trực tiếp các câu hỏi thường gặp nhất của sinh viên:** Quy chế chứa đựng câu trả lời cho các vấn đề cốt lõi: tín chỉ, học kỳ, đăng ký môn học, thi lại, hoãn thi, cách tính GPA, điều kiện tích lũy học phần (điểm từ 5.0 trở lên), học song bằng và điều kiện tốt nghiệp.

### 6.2. Thách thức kỹ thuật và điều kiện tiên quyết
- Quyết định 580 là **tệp scan ảnh 100% (26 trang, 0 ký tự text layer)**.
- Do đó, để sử dụng Quyết định 580 làm nguồn cho bản thử đầu tiên (Baseline / Prototype trong Tuần 2), điều kiện bắt buộc là: **Phải thực hiện OCR tiếng Việt chất lượng cao hoặc chuyển đổi văn bản có đối chiếu 1-1 cho 26 trang này**, gắn metadata số trang PDF (từ 1 đến 26) và số trang in (từ trang Quyết định đến trang in 1–25).

---

## 7. KẾT LUẬN VÀ KẾ HOẠCH HÀNH ĐỘNG TIẾP THEO

### 7.1. Kết luận kiểm tra chất lượng dữ liệu
1. **Về dữ liệu PDF gốc:** Cả 03 tệp PDF đều toàn vẹn về mặt lưu trữ nhưng không tệp nào có text layer sạch dùng được ngay. QĐ 580 và Sổ tay sinh viên là ảnh scan; Hướng dẫn giảng viên bị lỗi mã hóa font. Tệp Hướng dẫn giảng viên (2016) là văn bản nội bộ dành cho giảng viên có điểm thi cũ nên chưa kích hoạt trong kho hỏi đáp của sinh viên.
2. **Về 06 tệp Markdown:** Đã bao phủ cấu trúc 06 nhóm nội dung nhưng chứa nhiều sai lệch số liệu trọng yếu (thang điểm, số kỳ học, khối lượng tín chỉ, thông tin liên hệ danh bạ, tỷ lệ miễn giảm học phí).
3. **Tính sẵn sàng:** Dữ liệu hiện tại **chưa sẵn sàng cho việc nạp tự động hàng loạt**. Cần một bước tiền xử lý chuẩn hóa trước khi bước vào giai đoạn nạp kho (Ingestion).

### 7.2. Ba việc ưu tiên hàng đầu tiếp theo (Tuần 2)
1. **Ưu tiên 1 — Chuẩn hóa và làm sạch văn bản lõi cho Quyết định 580 (Quy chế đào tạo):** Thực hiện số hóa/OCR có kiểm chứng 26 trang của QĐ 580, sửa toàn bộ các sai lệch điểm số trong File 02 Markdown để làm nguồn dữ liệu sạch đầu tiên cho bản thử nghiệm Baseline.
2. **Ưu tiên 2 — Đính chính danh bạ liên hệ và chính sách miễn giảm trong File 01 và File 05:** Cập nhật số điện thoại, Zalo, email chuẩn của các phòng ban từ Sổ tay trang 9–10 và các tỷ lệ miễn giảm học phí chuẩn từ QĐ 123 (Sổ tay trang 43).
3. **Ưu tiên 3 — Xây dựng Pipeline Ingestion có gắn Metadata và kiểm tra nguồn (Source Verification):** Hiện thực hóa module nạp dữ liệu tại `ingestion.py` hỗ trợ các trường metadata bắt buộc: `source_file`, `pdf_page_start`, `pdf_page_end`, `printed_page`, `article`, `decision_number`, `source_verified` theo đúng đặc tả của `LOGIC.md`.

---

## 8. NHẬT KÝ ĐÍNH CHÍNH BỘ BÁO CÁO (ĐỢT 2 — 31/10/2026)

Thực hiện rà soát theo chỉ đạo tại `NHIEM_VU_TIEP_THEO_02_CHUAN_HOA_QD580.md`, báo cáo đã được hiệu chỉnh các điểm sau:
1. **Đính chính số liệu thống kê Bảng 4.1:** Cập nhật chính xác số liệu tính toán động từ `DOI_CHIEU_NGUON.csv`: Khảo sát 06 Markdown gồm 31 mẫu (16 khớp, 12 sai lệch, 3 chưa tìm thấy căn cứ); riêng File 02 có 3 khớp, 5 sai lệch, 1 chưa có căn cứ; tách riêng 01 dòng cho tài liệu hướng dẫn giảng viên (1 khớp).
2. **Hiệu chỉnh phạm vi trang Sổ tay sinh viên:** Sửa ghi chú về Trang PDF 49 là trang bìa sau chứa mã QR, không phải nội dung chuẩn đầu ra hay trang in 46.
3. **Chuẩn hóa phương pháp luận trích xuất:** Ghi rõ `kiem_tra_trang_pdf.py` đo lường số ký tự/ảnh tự động, còn nhãn phân loại là kết quả đánh giá thủ công có kiểm chứng trực quan; `tao_bang_doi_chieu_va_van_de.py` xuất bảng dữ liệu từ các nhận xét đã ghi nhận, không tự động nhận diện AI.
4. **Chuẩn hóa ngôn từ khoa học:** Điều chỉnh các kết luận khẳng định tuyệt đối ("cao nhất/mới nhất toàn trường", "đã hết hiệu lực") về đúng phạm vi mô tả tài liệu hiện có; sửa cách dùng từ "chế tạo" thành "sai lệch so với nguồn PDF" hoặc "chưa tìm thấy căn cứ".
5. **Ghi nhận điểm bất thường danh bạ:** Ghi nhận email Phòng Khảo thí trên bản in trang 10 là `phongtc-hc@nctu.edu.vn` (trùng ký hiệu TC-HC) là điểm bất thường cần nhà trường xác minh, không tự suy đoán.
6. **Lưu trữ sao lưu:** Toàn bộ phiên bản báo cáo và script trước khi hiệu chỉnh đã được sao lưu an toàn tại thư mục `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/backup_b1/`.

---
*Báo cáo được lưu trữ chính thức tại thư mục `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/BAO_CAO_KIEM_TRA_DU_LIEU.md` kèm theo các tệp dữ liệu kiểm định `KIEM_TRA_TRANG_PDF.csv`, `DOI_CHIEU_NGUON.csv` và `DANH_SACH_VAN_DE.csv`.*
