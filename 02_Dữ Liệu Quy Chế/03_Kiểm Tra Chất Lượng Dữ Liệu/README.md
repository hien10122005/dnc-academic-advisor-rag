# HƯỚNG DẪN TÁI HIỆN QUY TRÌNH KIỂM TRA CHẤT LƯỢNG DỮ LIỆU

Thư mục này chứa toàn bộ báo cáo, dữ liệu kiểm toán và các script Python/PowerShell được sử dụng để kiểm tra độc lập chất lượng 03 tài liệu PDF và 06 file Markdown quy chế của Trường Đại học Nam Cần Thơ (DNC).

---

## 1. CÁC TỆP ĐẦU RA CHÍNH

1. **`BAO_CAO_KIEM_TRA_DU_LIEU.md`**: Báo cáo tổng hợp chi tiết về kiểm kê, phương pháp, kết quả đối chiếu, phân tích sai lệch và kết luận về tính sẵn sàng của dữ liệu.
2. **`KIEM_TRA_TRANG_PDF.csv`**: Bảng phân loại từng trang trên tổng số 81 trang của 03 file PDF (số ký tự trích xuất, số lượng ảnh, phân loại khả năng đọc, mô tả nội dung và vấn đề trích xuất). Định dạng UTF-8 có BOM.
3. **`DOI_CHIEU_NGUON.csv`**: Bảng ánh xạ nguồn bước đầu cho 32 đoạn đại diện qua 06 file Markdown và tài liệu hướng dẫn giảng viên, chỉ rõ trang PDF, trang in, số quyết định, phạm vi áp dụng và 4 trạng thái đối chiếu. Định dạng UTF-8 có BOM.
4. **`DANH_SACH_VAN_DE.csv`**: Danh mục 07 vấn đề chất lượng dữ liệu phát hiện được, phân cấp mức độ ảnh hưởng, bằng chứng cụ thể, hướng xử lý và trạng thái theo dõi. Định dạng UTF-8 có BOM.

---

## 2. CÁCH CHẠY LẠI CÁC SCRIPT ĐỂ TÁI KIỂM ĐỊNH (REPRODUCE)

Môi trường yêu cầu:
- Python 3.10+ (đã kiểm thử thành công trên Python 3.14.6)
- Các thư viện: `pypdf`, `pdfplumber`, `pypdfium2`, `pillow`

### Bước 1: Kiểm tra cấu trúc văn bản Markdown
```powershell
python "02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\kiem_tra_md.py"
```

### Bước 2: Quét toàn bộ 81 trang PDF và tái tạo tệp KIEM_TRA_TRANG_PDF.csv
```powershell
python "02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\kiem_tra_trang_pdf.py"
```

### Bước 3: Tái tạo bảng đối chiếu nguồn và danh sách vấn đề chất lượng
```powershell
python "02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\tao_bang_doi_chieu_va_van_de.py"
```

### Bước 4: (Tùy chọn) Render mẫu các trang PDF để kiểm tra trực quan
```powershell
# Render mẫu đại diện các văn bản:
python "02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\render_samples.py"

# Render toàn bộ 26 trang của QĐ 580:
python "02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\render_580_all.py"

# Render toàn bộ 6 trang hướng dẫn giảng viên:
python "02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\render_hdgv.py"
```
Ảnh xuất ra được lưu tại thư mục con `sample_renders/`.
