# DỮ LIỆU ĐÃ KIỂM CHỨNG — QUYẾT ĐỊNH 580/QĐ-ĐHNCT
## HỆ THỐNG DỮ LIỆU SỐ HÓA VÀ BỘ TEST BENCH PHÁT TRIỂN

> Thư mục này chứa toàn bộ dữ liệu số hóa, tài liệu kiểm chứng từng trang, đề xuất đính chính và bộ ca phát triển chuẩn của **Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024** của Hiệu trưởng Trường Đại học Nam Cần Thơ về Quy chế đào tạo trình độ đại học.

---

## 1. Cấu trúc thư mục

```text
04_Dữ Liệu Đã Kiểm Chứng/QD580/
├── raw/                              # Thư mục chứa 26 tệp văn bản thô theo trang
│   ├── qd580_p01_raw.txt             # Trang PDF 1 (Quyết định ban hành)
│   ├── ...
│   └── qd580_p26_raw.txt             # Trang PDF 26 (Điều khoản thi hành, ký tên)
├── QD580_THEO_TRANG.md               # Bản đọc Markdown hoàn chỉnh theo trang
├── QD580_PAGES.jsonl                 # Tệp JSON Lines có cấu trúc metadata cho từng trang
├── KIEM_CHUNG_TUNG_TRANG.csv         # Bảng kiểm soát 26 dòng theo dõi trạng thái đối chiếu
├── DE_XUAT_DINH_CHINH_FILE_02.md     # Bản đề xuất sửa File 02 (tách riêng phần QĐ 580 và sổ tay)
├── NHAT_KY_DINH_CHINH.csv            # Nhật ký chi tiết các điểm thay đổi giữa bản cũ và mới
├── DEV_10_CAU_QD580.jsonl            # Tập 10 ca phát triển có trích dẫn điều khoản và đáp án chuẩn
├── BAO_CAO_CHUAN_HOA_QD580.md        # Báo cáo học thuật chi tiết về quá trình chuẩn hóa dữ liệu
├── tao_du_lieu_qd580.py              # Script sinh các tệp raw, QD580_THEO_TRANG.md, JSONL và CSV kiểm chứng
├── tao_dinh_chinh_va_dev_cases.py    # Script sinh tệp đính chính, nhật ký thay đổi và 10 test case
└── README.md                         # Hướng dẫn tái hiện và quy chuẩn kiểm định này
```

---

## 2. Quy trình kiểm chứng và phân biệt phương pháp

### 2.1. Phân biệt xử lý tự động và đối chiếu thủ công
- **Xử lý tự động:**
  - Script `pypdfium2` kết xuất 26 trang PDF bitmap quét 300 DPI sang định dạng PNG tại thư mục `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/sample_renders/580_p01.png` - `580_p26.png`.
  - Tự động kiểm tra text layer xác nhận không có lớp ký tự số hóa (text length = 0).
  - Tự động biên dịch dữ liệu trang sang định dạng `QD580_PAGES.jsonl` và `KIEM_CHUNG_TUNG_TRANG.csv`.
- **Đối chiếu trực quan thủ công (Manual Visual Audit):**
  - Đọc và chép đối chiếu trực quan 100% từng dòng, từng dấu ngắt câu, từng điều/khoản và từng ô bảng biểu giữa bản scan phóng to và văn bản số hóa.
  - Kiểm tra đặc biệt các con số học vụ quan trọng: Ngưỡng tích lũy $\ge 5.0$ (D+), thang điểm A từ 9.0, giới hạn tín chỉ (4 năm: 7–15; 5 năm: 9–20; 6 năm: 10–23), trần điểm thi lại D+/C+.
  - Không dựa vào độ tin cậy giả định của mô hình OCR tự động khi môi trường không có gói nhận diện tiếng Việt.

---

## 3. Hướng dẫn tái chạy (Reproduction)

Mở terminal tại thư mục gốc của dự án hoặc thư mục hiện tại:

```powershell
# Chuyển vào thư mục chứa script
cd "02_Dữ Liệu Quy Chế/04_Dữ Liệu Đã Kiểm Chứng/QD580"

# 1. Tái tạo các tệp số hóa trang (raw, markdown, jsonl, csv kiểm chứng)
python tao_du_lieu_qd580.py

# 2. Tái tạo tệp đề xuất đính chính, nhật ký thay đổi và 10 test case phát triển
python tao_dinh_chinh_va_dev_cases.py
```

---

## 4. Các cam kết và giới hạn dữ liệu

1. **Bảo toàn dữ liệu cũ:** Không ghi đè 6 tệp Markdown đã làm sạch cũ trong `02_Văn Bản Đã Làm Sạch (Text)/` và không sửa đổi 3 tệp PDF gốc trong `01_Tài Liệu Gốc (PDF)/`.
2. **Không vượt phạm vi:** Không triển khai pipeline ingestion, embedding, ChromaDB hay chatbot trong nhiệm vụ này.
3. **Chuẩn mã hóa:** Tất cả các tệp văn bản đều được lưu ở định dạng UTF-8 (các tệp CSV có ký tự BOM `utf-8-sig` để hiển thị tiếng Việt chính xác trên Microsoft Excel).
