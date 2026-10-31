# Nhiệm vụ tiếp theo cho Antigravity — Chuẩn hóa nguồn QĐ 580

Ngày giao: **31/10/2026**. Đọc `PROJECT.md`, `LOGIC.md`, `ROADMAP.md` và báo cáo kiểm tra dữ liệu trước khi thực hiện.

## 1. Kết quả rà soát đầu ra bước 1

Đã đọc báo cáo, README, ba CSV và script tạo bảng; xem mẫu ảnh render QĐ 580 trang PDF 15, sổ tay trang PDF 13 và 49. Đây là rà soát đầu ra, chưa phải đối chiếu lại toàn bộ 81 trang.

- Có 81 dòng kiểm tra trang PDF, 32 dòng đối chiếu nguồn và 7 vấn đề được ghi nhận.
- Hai đầu việc kiểm kê và kiểm tra text layer trong ROADMAP đã được đánh dấu kèm tên minh chứng. Điều này chưa có nghĩa toàn bộ dữ liệu sẵn sàng ingestion.
- SHA-256 của sáu Markdown quy chế khớp với giá trị ghi nhận trước khi giao bước 1.
- Phát hiện sai lệch thang điểm được minh họa bằng ảnh QĐ 580 trang PDF 15, trang in 14; cần đối chiếu các nội dung còn lại trước khi sửa.

### Điểm cần chỉnh trong bộ kiểm tra

1. **Sai thống kê:** CSV hiện có 17 dòng khớp, 12 dòng sai lệch, 3 dòng chưa có căn cứ; báo cáo đang ghi 18/11/3. Riêng file 02 có 3 khớp, 5 sai lệch, 1 chưa có căn cứ. Nếu thống kê riêng sáu Markdown thì có 31 mẫu: 16 khớp, 12 sai lệch, 3 chưa có căn cứ. Dòng tài liệu giảng viên phải được tách riêng. Tính tỷ lệ từ CSV, không chép lại các số này nếu CSV đã được sửa có căn cứ.
2. **Phạm vi trang:** ảnh sổ tay trang PDF 49 là bìa sau có QR, nhất quán với CSV kiểm tra trang; báo cáo không được ghi trang này là nội dung chuẩn đầu ra/trang in 46.
3. **Kết luận quá mức:** chưa đủ chứng cứ từ ba file để kết luận QĐ 580 là văn bản “cao nhất”, “mới nhất” toàn trường hoặc tài liệu giảng viên “đã hết hiệu lực/đã bị thay thế”. Chỉ mô tả nguồn hiện có, khác biệt quan sát được và quyết định chưa kích hoạt cho bản thử. Không làm thêm tra cứu pháp lý bên ngoài ở nhiệm vụ này.
4. **Cách phân loại:** `kiem_tra_trang_pdf.py` đo số ký tự/ảnh nhưng gán loại theo tên file và số trang. Phải ghi rõ phần nào là dữ liệu đo tự động, phần nào là nhãn kiểm tra thủ công. `tao_bang_doi_chieu_va_van_de.py` xuất các nhận xét đã nhập sẵn, không tự đối chiếu nội dung PDF. Chạy lại script không tự xác minh các nhận xét đó.
5. **Danh bạ:** bản scan trang PDF 13 ghi mục Khảo thí với email `phongtc-hc@nctu.edu.vn`. Không tự đổi tên đơn vị thành Tổ chức–Hành chính chỉ vì tên email; ghi đúng nguồn và đánh dấu điểm bất thường cần xác minh. Không gọi mọi số dạng 798 xxx là giả: cùng trang có những số dạng này ở các đơn vị khác.
6. **Độ bao phủ:** “0 mục chưa kiểm tra” trong mẫu không đồng nghĩa đã kiểm tra toàn bộ sáu Markdown. Nêu rõ chỉ đối chiếu 32 mẫu và phần ngoài mẫu chưa được xác minh; sửa từ ngữ “chế tạo” thành sai lệch/chưa có căn cứ nếu chưa có chứng cứ về cách hình thành nội dung.

## 2. Mục tiêu nhiệm vụ này

Tạo bản số hóa QĐ 580 có nguồn theo trang, đủ làm đầu vào thử ingestion; đồng thời đính chính phần báo cáo kiểm tra còn sai và chuẩn bị 10 ca phát triển có đáp án nguồn. Chưa làm chatbot, tài khoản, giao diện, embedding, ChromaDB hoặc Gemini.

Thư mục dự án:

```text
E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)
```

## 3. Công việc thực hiện theo thứ tự

### A. Hiệu chỉnh bộ báo cáo kiểm tra

- Sao lưu các đầu ra và script liên quan trước khi sửa.
- Sửa báo cáo, CSV hoặc script ở những điểm nêu trên theo bằng chứng, bảo đảm chạy script không tạo lại phiên bản đã biết sai.
- Tính bảng tổng hợp từ CSV bằng script nhỏ; tách sáu Markdown khỏi dòng tài liệu giảng viên.
- Bổ sung ghi chú phương pháp, phạm vi mẫu và nhật ký đính chính; giữ lại vấn đề còn chưa xác minh.
- Không tự chuyển cả bảy vấn đề sang “đã xử lý” chỉ vì đã sửa báo cáo.

### B. Thử số hóa bốn trang QĐ 580

Nguồn: `02_Dữ Liệu Quy Chế/01_Tài Liệu Gốc (PDF)/580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf`.

- Làm thử trang PDF **3, 9, 15, 17** để kiểm tra văn bản, số liệu, bảng điểm và điều kiện học vụ.
- Ưu tiên OCR cục bộ có hỗ trợ tiếng Việt. Chỉ dùng môi trường riêng; ghi công cụ, phiên bản và cách chạy. Không đổi Python toàn máy hay nâng cấp hàng loạt thư viện của dự án.
- Có thể dùng bản chép thủ công đối chiếu trực quan nếu công cụ OCR chưa phù hợp; ghi đúng phương pháp, không gọi là OCR tự động.
- Lưu bản thô riêng với bản đã đối chiếu. Kiểm tra trực quan số liệu, dấu so sánh, phủ định, điều kiện, ngoại lệ và từng ô bảng; điểm confidence OCR không thay thế đối chiếu.
- Nếu chưa đọc chắc được, đánh dấu đoạn chưa xác minh, nêu trở ngại; không tự điền nội dung từ Markdown cũ hoặc từ báo cáo kiểm tra.
- Không tải PDF lên dịch vụ bên ngoài hay dùng OCR trả phí trong nhiệm vụ này.

### C. Mở rộng bản có kiểm chứng tới 26 trang

Nếu mẫu thử đạt yêu cầu và công cụ làm được, tiếp tục toàn bộ QĐ 580. Không cần hỏi lại đối với việc số hóa cục bộ trong phạm vi này. Nếu gặp trở ngại thực tế, hoàn thành phần có thể kiểm chứng và báo rõ phần còn thiếu.

- Bao gồm trang quyết định và quy chế kèm theo; giữ đúng tiêu đề, điều/khoản, bảng và nội dung tiếp nối giữa trang.
- Mỗi trang có `document_id`, tên file nguồn, `pdf_page` tính từ 1, `printed_page` nếu nhìn thấy, phương pháp trích xuất, nội dung và trạng thái đối chiếu.
- Không suy ra trang in hoàn toàn bằng công thức; ghi theo ảnh gốc. Không nhầm Điều 1–3 của quyết định ban hành với Điều 1–32 của quy chế kèm theo.
- Giữ nguyên điều kiện và ngoại lệ, không rút gọn thành kết luận áp dụng cho mọi khóa/ngành.
- Tạo bản đọc Markdown theo trang và JSONL chứa nội dung có cấu trúc. Đoạn chưa kiểm tra có `source_verified=false`, không đủ điều kiện làm dữ liệu trả lời.
- Tạo bản đề xuất đính chính file 02 và bảng thay đổi đối chiếu theo nguồn. Không ghi đè sáu Markdown cũ trong nhiệm vụ này; phần lấy từ sổ tay phải được tách rõ, không gắn nhầm nguồn QĐ 580.

### D. Chuẩn bị 10 ca phát triển

- Chỉ dùng nguồn QĐ 580 đã xác minh; đây là tập phát triển, không phải tập kiểm thử cuối.
- Dự kiến 6 câu trực tiếp, 2 câu diễn đạt đời thường, 1 câu nối tiếp có lịch sử cho sẵn, 1 câu thiếu dữ kiện hoặc không có đủ căn cứ trong kho thử.
- Mỗi ca có ID, nhóm, câu hỏi, lịch sử nếu có, hành vi mong đợi, đáp án/các ý bắt buộc, đoạn dẫn chứng, điều/khoản, trang PDF và trang in.
- Ca không đủ căn cứ phải giải thích vì sao mong đợi hỏi lại/từ chối; không kết luận trường không có quy định chỉ vì bản thử thiếu tài liệu.
- Nếu chưa đủ nguồn cho 10 ca thì ghi số ca hoàn thành và phần còn thiếu, không dựng đáp án để đủ số lượng.

## 4. Đầu ra

Tạo thư mục `02_Dữ Liệu Quy Chế/04_Dữ Liệu Đã Kiểm Chứng/QD580/` gồm:

| Đầu ra | Nội dung |
| --- | --- |
| `raw/` | Văn bản thô theo trang hoặc kết quả OCR thử, không gắn nhãn đã xác minh |
| `QD580_THEO_TRANG.md` | Bản đọc có mốc nguồn/trang rõ ràng |
| `QD580_PAGES.jsonl` | Nội dung từng trang, metadata và trạng thái kiểm chứng |
| `KIEM_CHUNG_TUNG_TRANG.csv` | 26 dòng kiểm soát, kể cả trang chưa hoàn thành |
| `DE_XUAT_DINH_CHINH_FILE_02.md` | Đề xuất bản sửa theo nguồn, tách phần ngoài QĐ 580 |
| `NHAT_KY_DINH_CHINH.csv` | Nội dung cũ, đề xuất sửa, nguồn, trang và trạng thái |
| `DEV_10_CAU_QD580.jsonl` | Các ca phát triển đã hoàn thành và nguồn chuẩn |
| `BAO_CAO_CHUAN_HOA_QD580.md` | Kết quả, cách làm, giới hạn, trang còn thiếu và mức sẵn sàng |
| `README.md` và script nếu có | Cách tái chạy; phân biệt xử lý tự động với thao tác đối chiếu |

Nếu chỉ hoàn thành một phần, tên file có thể giữ như trên nhưng báo cáo và metadata phải nói rõ trạng thái từng trang; không đánh dấu cả tài liệu đã xác minh. Mã hóa UTF-8; dữ liệu thô không bị script ghi đè bằng bản hiệu chỉnh.

## 5. Điều kiện nghiệm thu và giới hạn

- Các điểm sai thống kê/phạm vi đã được sửa nhất quán hoặc ghi rõ chưa giải quyết.
- Nội dung đầu vào bản thử truy về được nguồn và trang; bảng điểm được kiểm tra từng ô.
- Mọi trang có trạng thái, người/công cụ đối chiếu và ngày; không tự điền một người kiểm tra thứ hai nếu không có.
- Chỉ đánh dấu `source_verified=true` cho phần đã thực sự đối chiếu; đoạn chưa kiểm tra phải loại khỏi tập dùng thử.
- Bộ phát triển có đáp án nguồn, không chép từ sáu Markdown chưa hiệu chỉnh.
- Giữ nguyên PDF gốc, sáu Markdown cũ, phạm vi `PROJECT.md` và `LOGIC.md`. Chỉ cập nhật đầu việc ROADMAP đã hoàn thành với đường dẫn minh chứng đầy đủ, không đánh dấu ingestion/embedding/RAG đã xong.
- Lần báo cáo cuối nêu số trang đã số hóa, đã đối chiếu, còn thiếu; số ca phát triển; các thay đổi và bước tiếp theo. Chỉ chuyển sang lập chỉ mục sau khi xác định rõ tập dữ liệu đủ điều kiện.
