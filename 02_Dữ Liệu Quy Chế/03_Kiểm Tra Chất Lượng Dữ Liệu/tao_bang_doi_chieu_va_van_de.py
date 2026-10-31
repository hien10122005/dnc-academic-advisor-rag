import csv
import os

out_dir = r"02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu"
os.makedirs(out_dir, exist_ok=True)

# 1. DOI_CHIEU_NGUON.csv
doi_chieu_file = os.path.join(out_dir, "DOI_CHIEU_NGUON.csv")
doi_chieu_data = [
    # --- File 01: Tong quan & Danh ba ---
    {
        "file_markdown": "01_Tong_Quan_Va_Danh_Ba_DNC.md",
        "tieu_de_muc": "1. THÔNG TIN CHUNG VỀ TRƯỜNG ĐẠI HỌC NAM CẦN THƠ",
        "trich_doan_vi_tri": "Số 168, Đường Nguyễn Văn Cừ nối dài... Hotline: 0939 257 838; Website: www.nctu.edu.vn",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 1,
        "trang_in": "Bìa trước",
        "dieu_muc_so_qd": "",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp địa chỉ, hotline tuyển sinh và website chính thức ở bìa sổ tay",
        "pham_vi_ap_dung": "Toàn trường, năm học 2026-2027"
    },
    {
        "file_markdown": "01_Tong_Quan_Va_Danh_Ba_DNC.md",
        "tieu_de_muc": "2. TẦM NHÌN, SỨ MẠNG VÀ GIÁ TRỊ CỐT LÕI",
        "trich_doan_vi_tri": "Sứ mạng đào tạo nguồn nhân lực chất lượng cao; Tầm nhìn đến 2030 Top 140-150 Đông Nam Á, 2045 Top 100 Châu Á; Giá trị cốt lõi: Trí tuệ - Năng động - Sáng tạo - Hội nhập",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 4,
        "trang_in": "01",
        "dieu_muc_so_qd": "444/QĐ-CTHĐT-ĐHNCT (09/05/2025)",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp nội dung sứ mạng, tầm nhìn chiến lược và số hiệu QĐ 444",
        "pham_vi_ap_dung": "Toàn trường"
    },
    {
        "file_markdown": "01_Tong_Quan_Va_Danh_Ba_DNC.md",
        "tieu_de_muc": "3. DANH BẠ LIÊN HỆ CÁC PHÒNG BAN - Phòng Quản lý Đào tạo",
        "trich_doan_vi_tri": "C2-12; SĐT: (02923) 798 168 / 798 222; Email: daotao@nctu.edu.vn",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 12,
        "trang_in": "09",
        "dieu_muc_so_qd": "Phần 2, Mục 1",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai lệch SĐT và Email: PDF gốc ghi SĐT 02923 798 999, Zalo 0907668874, Email phongdaotao@nctu.edu.vn",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "01_Tong_Quan_Va_Danh_Ba_DNC.md",
        "tieu_de_muc": "3. DANH BẠ LIÊN HỆ CÁC PHÒNG BAN - Phòng CT&QLSV",
        "trich_doan_vi_tri": "C2-03; SĐT: (02923) 798 333; Email: ctsv@nctu.edu.vn",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 12,
        "trang_in": "09",
        "dieu_muc_so_qd": "Phần 2, Mục 1",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai lệch SĐT và Email: PDF gốc ghi SĐT 02923 798 444, Email phongqlhssv@nctu.edu.vn",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "01_Tong_Quan_Va_Danh_Ba_DNC.md",
        "tieu_de_muc": "3. DANH BẠ LIÊN HỆ CÁC PHÒNG BAN - Phòng Tài chính - Kế hoạch",
        "trich_doan_vi_tri": "C2-04; SĐT: (02923) 798 444; Email: taichinh@nctu.edu.vn",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 12,
        "trang_in": "09",
        "dieu_muc_so_qd": "Phần 2, Mục 1",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai lệch SĐT và Email: PDF gốc ghi SĐT 02923 751 668, Email phongtc-kh@nctu.edu.vn",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "01_Tong_Quan_Va_Danh_Ba_DNC.md",
        "tieu_de_muc": "3. DANH BẠ LIÊN HỆ CÁC PHÒNG BAN - Phòng Khảo thí & ĐBCLGD",
        "trich_doan_vi_tri": "C2-04; SĐT: (02923) 798 555; Email: khaothi@nctu.edu.vn",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 13,
        "trang_in": "10",
        "dieu_muc_so_qd": "Phần 2, Mục 1",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai lệch SĐT: PDF gốc ghi SĐT 02923 798 668, Zalo 0392972799. Về Email, bản scan ghi phongtc-hc@nctu.edu.vn (điểm bất thường cần xác minh vì trùng ký hiệu TC-HC)",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "01_Tong_Quan_Va_Danh_Ba_DNC.md",
        "tieu_de_muc": "5. HỆ SINH THÁI DOANH NGHIỆP TRỰC THUỘC",
        "trich_doan_vi_tri": "Bệnh viện ĐHNCT 300 giường bệnh; Showroom Ô tô Nam Cần Thơ & TT Đăng kiểm xe; TT Phát triển Phần mềm DNC",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 10,
        "trang_in": "07",
        "dieu_muc_so_qd": "Phần 1, Mục 9",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp các đơn vị doanh nghiệp trực thuộc trong hệ sinh thái DNC",
        "pham_vi_ap_dung": "Toàn trường"
    },

    # --- File 02: Quy che dao tao ---
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "1.2. Tổ chức năm học và học kỳ",
        "trich_doan_vi_tri": "Một năm học thông thường gồm 02 học kỳ chính (Học kỳ 1 và Học kỳ 2) và 01 học kỳ phụ (Học kỳ hè): Học kỳ chính kéo dài tối thiểu 15 tuần học...",
        "pdf_nguon": "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
        "trang_pdf": 3,
        "trang_in": "2",
        "dieu_muc_so_qd": "Điều 3, Khoản 2.b",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai lệch mô hình năm học: QĐ 580 quy định mỗi năm gồm 03 học kỳ, mỗi kỳ từ 10 đến 12 tuần giảng dạy + 2 tuần đánh giá; MD diễn giải thành 2 kỳ chính 15 tuần + hè 5 tuần",
        "pham_vi_ap_dung": "Đại học chính quy tín chỉ"
    },
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "1.3. Khối lượng học tập đăng ký mỗi học kỳ",
        "trich_doan_vi_tri": "Trong mỗi học kỳ chính, sinh viên phải đăng ký khối lượng học tập tối thiểu là 14 tín chỉ... tối đa không quá 25 tín chỉ...",
        "pdf_nguon": "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
        "trang_pdf": 9,
        "trang_in": "8",
        "dieu_muc_so_qd": "Điều 7, Khoản 2",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai lệch số tín chỉ: QĐ 580 quy định CT 4 năm tối thiểu 7 và tối đa 15 tín chỉ/kỳ; CT 5 năm tối thiểu 9 tối đa 20; CT 6 năm tối thiểu 10 tối đa 23. MD ghi 14-25 tín chỉ",
        "pham_vi_ap_dung": "Đại học chính quy theo chương trình 4, 5, 6 năm"
    },
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "3.1. Cơ cấu tỷ trọng điểm đánh giá học phần",
        "trich_doan_vi_tri": "Chuyên cần 10% (0.10); Giữa kỳ 30% (0.30); Thi kết thúc học phần 60% (0.60)",
        "pdf_nguon": "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
        "trang_pdf": 15,
        "trang_in": "14",
        "dieu_muc_so_qd": "Điều 17, Khoản 1.a",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp hoàn toàn tỷ lệ 10% - 30% - 60% với QĐ 580 và Sổ tay sinh viên trang 20",
        "pham_vi_ap_dung": "Đại học chính quy tín chỉ"
    },
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "3.2. Bảng quy đổi thang điểm",
        "trich_doan_vi_tri": "8.5 – 10.0: Điểm A; 8.0 – 8.4: Điểm B+; 4.0 – 4.9: Điểm D (Tích lũy)",
        "pdf_nguon": "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
        "trang_pdf": 15,
        "trang_in": "14",
        "dieu_muc_so_qd": "Điều 17, Khoản 1",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai lệch nghiêm trọng: DNC quy định A là 9.0-10.0 (không phải 8.5-10.0); B+ là 8.0-8.9 (không phải 8.0-8.4); chỉ từ 5.0 trở lên (D+) mới đạt/tích lũy; điểm D (4.0-4.9) là KHÔNG ĐẠT/KHÔNG TÍCH LŨY (MD ghi là Đạt/Tích lũy)",
        "pham_vi_ap_dung": "Đại học chính quy tín chỉ"
    },
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "4.2. Quy định thi lại (Thi phụ)",
        "trich_doan_vi_tri": "Điểm tổng kết sau khi thi lại được ghi nhận vào bảng điểm theo đúng kết quả tính toán",
        "pdf_nguon": "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
        "trang_pdf": 17,
        "trang_in": "16",
        "dieu_muc_so_qd": "Điều 18, Khoản 6",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Thiếu quy định khống chế: QĐ 580 quy định điểm học phần sau khi thi lại chỉ được giới hạn ở mức điểm D+ hoặc C+",
        "pham_vi_ap_dung": "Sinh viên thi lại học phần"
    },
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "2.2. Đăng ký học lại và học cải thiện điểm",
        "trich_doan_vi_tri": "Điểm học phần cao nhất giữa các lần học sẽ được ghi nhận vào bảng điểm tích lũy chung",
        "pdf_nguon": "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
        "trang_pdf": 9,
        "trang_in": "8",
        "dieu_muc_so_qd": "Điều 8, Khoản 3",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai quy tắc tính: QĐ 580 quy định 'Kết quả của lần thi sau cùng được chọn để tính vào điểm trung bình tích lũy' chứ không lấy điểm cao nhất",
        "pham_vi_ap_dung": "Sinh viên học cải thiện (điểm từ 5.0 đến dưới 6.5)"
    },
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "6.1. Cảnh báo học tập",
        "trich_doan_vi_tri": "ĐTB học kỳ dưới 0.80 kỳ đầu, dưới 1.00 các kỳ tiếp theo; CPA dưới 1.20 năm 1, 1.40 năm 2, 1.60 năm 3, 1.80 các năm tiếp theo",
        "pdf_nguon": "",
        "trang_pdf": "",
        "trang_in": "",
        "dieu_muc_so_qd": "",
        "ket_qua_doi_chieu": "Chưa tìm thấy căn cứ trong các nguồn hiện có",
        "ghi_chu_sai_lech": "Các ngưỡng điểm số 0.80/1.00/1.20/1.40/1.60/1.80 chưa tìm thấy trong QĐ 580 hay Sổ tay sinh viên",
        "pham_vi_ap_dung": ""
    },
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "6.2. 6 Điều kiện dẫn đến Buộc thôi học",
        "trich_doan_vi_tri": "Bị cảnh báo học vụ 2 lần liên tiếp; Vượt quá thời gian đào tạo tối đa; Tự ý bỏ học không phép; Không đóng học phí đúng hạn; Vi phạm kỷ luật nghiêm trọng/thi hộ; Bị truy cứu TNHS",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 25,
        "trang_in": "22",
        "dieu_muc_so_qd": "Phần 3, Mục 6",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp các trường hợp buộc thôi học nêu tại Sổ tay sinh viên trang 22",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md",
        "tieu_de_muc": "7. HỌC CÙNG LÚC HAI CHƯƠNG TRÌNH (SONG BẰNG)",
        "trich_doan_vi_tri": "Hoàn thành tối thiểu HK1 năm 1; CPA chương trình 1 đạt từ 2.50 trở lên...",
        "pdf_nguon": "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
        "trang_pdf": 12,
        "trang_in": "11",
        "dieu_muc_so_qd": "Điều 14",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp điều kiện học song bằng với QĐ 580 và Sổ tay sinh viên trang 23",
        "pham_vi_ap_dung": "Sinh viên chính quy"
    },

    # --- File 03: Cong tac sinh vien & Diem ren luyen ---
    {
        "file_markdown": "03_Cong_Tac_Sinh_Vien_Va_Diem_Ren_Luyen.md",
        "tieu_de_muc": "1.1. Quyền lợi của sinh viên",
        "trich_doan_vi_tri": "Được tôn trọng, bình đẳng; sử dụng cơ sở vật chất; tham gia NCKH; xét học bổng; thực tập hệ sinh thái DNC; khiếu nại...",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 28,
        "trang_in": "25",
        "dieu_muc_so_qd": "Phần 3, Mục 1.1",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp 7 nhóm quyền lợi sinh viên trong Sổ tay",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "03_Cong_Tac_Sinh_Vien_Va_Diem_Ren_Luyen.md",
        "tieu_de_muc": "3.2. Cấu trúc 5 Tiêu chí Đánh giá Điểm rèn luyện",
        "trich_doan_vi_tri": "Tiêu chí 1: Ý thức học tập (20đ); Tiêu chí 2: Nội quy quy chế (25đ); Tiêu chí 3: Hoạt động CT-XH (20đ); Tiêu chí 4: Ý thức công dân (25đ); Tiêu chí 5: Phụ trách lớp/đoàn thể (10đ)",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 35,
        "trang_in": "32",
        "dieu_muc_so_qd": "Phần 3, Mục 2.2; TT 16/2015/TT-BGDĐT",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp hoàn toàn 5 tiêu chí và khung điểm (20 - 25 - 20 - 25 - 10) tổng 100 điểm",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "03_Cong_Tac_Sinh_Vien_Va_Diem_Ren_Luyen.md",
        "tieu_de_muc": "3.3. Phân loại kết quả rèn luyện",
        "trich_doan_vi_tri": "Xuất sắc: 90-100; Tốt: 80-89; Khá: 65-79; Trung bình: 50-64; Yếu: 35-49; Kém: <35",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 36,
        "trang_in": "33",
        "dieu_muc_so_qd": "Phần 3, Mục 2.3",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp khung điểm phân loại rèn luyện trong Sổ tay",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "03_Cong_Tac_Sinh_Vien_Va_Diem_Ren_Luyen.md",
        "tieu_de_muc": "4. KHUNG XỬ LÝ KỶ LUẬT SINH VIÊN VI PHẠM (29 HÀNH VI)",
        "trich_doan_vi_tri": "Bảng 29 hành vi vi phạm kỷ luật và hình thức xử lý 4 lần vi phạm",
        "pdf_nguon": "",
        "trang_pdf": "",
        "trang_in": "",
        "dieu_muc_so_qd": "",
        "ket_qua_doi_chieu": "Chưa tìm thấy căn cứ trong các nguồn hiện có",
        "ghi_chu_sai_lech": "Bảng 29 hành vi chưa tìm thấy trong Sổ tay sinh viên (trang 35 chỉ có đoạn ngắn về vi phạm nội trú) hay QĐ 580; có khả năng bắt nguồn từ TT 10/2016/TT-BGDĐT",
        "pham_vi_ap_dung": ""
    },

    # --- File 04: Khen thuong & Noi quy ---
    {
        "file_markdown": "04_Quy_Che_Khen_Thuong_Va_Ky_Luat_Sinh_Vien.md",
        "tieu_de_muc": "1. QUY CHẾ KHEN THƯỞNG SINH VIÊN",
        "trich_doan_vi_tri": "Ban hành kèm theo Quyết định số 1358/QĐ-ĐHNCT ngày 9 tháng 10 năm 2025 của Hiệu trưởng",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 39,
        "trang_in": "36",
        "dieu_muc_so_qd": "1358/QĐ-ĐHNCT (09/10/2025)",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp số Quyết định 1358/QĐ-ĐHNCT và ngày ban hành 09/10/2025",
        "pham_vi_ap_dung": "Sinh viên đại học hệ chính quy"
    },
    {
        "file_markdown": "04_Quy_Che_Khen_Thuong_Va_Ky_Luat_Sinh_Vien.md",
        "tieu_de_muc": "1.2. Danh hiệu thi đua cá nhân hàng năm",
        "trich_doan_vi_tri": "Sinh viên Xuất sắc; Sinh viên Giỏi; Thủ khoa toàn khóa học; Thủ khoa đầu vào",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 39,
        "trang_in": "36",
        "dieu_muc_so_qd": "Điều 3",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp danh mục 4 danh hiệu thi đua",
        "pham_vi_ap_dung": "Sinh viên chính quy"
    },
    {
        "file_markdown": "04_Quy_Che_Khen_Thuong_Va_Ky_Luat_Sinh_Vien.md",
        "tieu_de_muc": "2. NỘI QUY PHÒNG HỌC VÀ GIẢNG ĐƯỜNG",
        "trich_doan_vi_tri": "Quyết định số 1042/QĐ-ĐHNCT ngày 12/8/2025 của Hiệu trưởng; 12 nội quy phòng học",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 43,
        "trang_in": "40",
        "dieu_muc_so_qd": "1042/QĐ-ĐHNCT (12/08/2025)",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp số QĐ 1042 và 12 nội dung quy định phòng học (đi trễ quá 15 phút, giảng viên trễ quá 15 phút, không livestream/TikTok...)",
        "pham_vi_ap_dung": "Sinh viên, học viên toàn trường"
    },

    # --- File 05: Hoc phi & Hoc bong ---
    {
        "file_markdown": "05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md",
        "tieu_de_muc": "1. NGUYÊN TẮC THU VÀ NỘP HỌC PHÍ",
        "trich_doan_vi_tri": "Quyết định số 42B/QĐ-ĐHNCT ngày 16/7/2015 của Hiệu trưởng; Chế tài xử lý vi phạm học phí",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 44,
        "trang_in": "41",
        "dieu_muc_so_qd": "42B/QĐ-ĐHNCT (16/07/2015)",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp số QĐ 42B và chế tài vi phạm (cấm thi HK1, cấm thi lần 2, lưu ban/buộc thôi học)",
        "pham_vi_ap_dung": "Sinh viên toàn trường"
    },
    {
        "file_markdown": "05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md",
        "tieu_de_muc": "2. CHÍNH SÁCH MIỄN, GIẢM HỌC PHÍ - Căn cứ pháp lý",
        "trich_doan_vi_tri": "Quyết định số 123/QĐ-CTHĐT-ĐHNCT ngày 21/4/2026",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 46,
        "trang_in": "43",
        "dieu_muc_so_qd": "123/QĐ-CTHĐT-ĐHNCT (21/04/2026)",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp số quyết định của Chủ tịch HĐT DNC",
        "pham_vi_ap_dung": "Sinh viên ĐH chính quy trúng tuyển và đang theo học"
    },
    {
        "file_markdown": "05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md",
        "tieu_de_muc": "2.1. Mức giảm 50% học phí - Sinh viên khuyết tật nặng",
        "trich_doan_vi_tri": "Sinh viên là người khuyết tật nặng theo quy định của pháp luật...",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 46,
        "trang_in": "43",
        "dieu_muc_so_qd": "Phần 3, Mục Giảm học phí",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai tỷ lệ miễn giảm: Sổ tay quy định sinh viên khuyết tật nặng giảm 20% học phí/HK (MD xếp nhầm vào mức 50%)",
        "pham_vi_ap_dung": "Sinh viên ĐH chính quy"
    },
    {
        "file_markdown": "05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md",
        "tieu_de_muc": "2. CHÍNH SÁCH MIỄN, GIẢM HỌC PHÍ - Các diện giảm đặc thù của DNC",
        "trich_doan_vi_tri": "Người thân cán bộ GV (20%), con Hiệu trưởng/phó THPT (10%), hộ khẩu Đà Nẵng (15%), các xã Đại Lộc/Hà Nha/Thượng Đức (20% + KTX)",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 46,
        "trang_in": "43",
        "dieu_muc_so_qd": "Phần 3, Mục Giảm học phí",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Thiếu nội dung: MD chưa ghi 4 nhóm đối tượng đặc thù được hưởng chính sách giảm học phí của DNC",
        "pham_vi_ap_dung": "Sinh viên ĐH chính quy"
    },
    {
        "file_markdown": "05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md",
        "tieu_de_muc": "3.1. Học bổng Khuyến khích học tập",
        "trich_doan_vi_tri": "Học bổng Xuất sắc 100% học phí, GPA >= 3.60, ĐRL >= 90; Học bổng Giỏi 50-70% học phí, GPA 3.20-3.59, ĐRL >= 80",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 45,
        "trang_in": "42",
        "dieu_muc_so_qd": "Phần 3, Mục Tài chính 2",
        "ket_qua_doi_chieu": "Có sai lệch",
        "ghi_chu_sai_lech": "Sai lệch nội dung: Sổ tay chỉ quy định 'xét điểm trung bình năm học từ cao xuống thấp, rèn luyện từ tốt trở lên, do Chủ tịch HĐT và Hiệu trưởng quyết định theo quỹ', không có số 100% hay GPA cố định",
        "pham_vi_ap_dung": "Sinh viên chính quy"
    },

    # --- File 06: Chuan dau ra ---
    {
        "file_markdown": "06_Quy_Dinh_Chuan_Dau_Ra_Tot_Nghiep.md",
        "tieu_de_muc": "2.1. Chuẩn đầu ra 1: Ngoại ngữ (Tiếng Anh)",
        "trich_doan_vi_tri": "Tiếng Anh B1 / Bậc 3 VSTEP; QĐ 350/QĐ-ĐHNCT ngày 07/04/2026; Ngôn ngữ Anh: C1 + B1 Pháp văn; Y khoa/Răng hàm mặt: Bậc 4; Du lịch/Dược: Bậc 3",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 48,
        "trang_in": "45",
        "dieu_muc_so_qd": "350/QĐ-ĐHNCT (07/04/2026)",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp các chuẩn ngoại ngữ chung và từng ngành đặc thù, cùng số hiệu QĐ 350",
        "pham_vi_ap_dung": "Sinh viên tốt nghiệp từ năm học 2026-2027"
    },
    {
        "file_markdown": "06_Quy_Dinh_Chuan_Dau_Ra_Tot_Nghiep.md",
        "tieu_de_muc": "2.2. Chuẩn đầu ra 2: Tin học & 2.4. Kỹ năng Trí tuệ nhân tạo (AI)",
        "trich_doan_vi_tri": "Tin học nâng cao cho ngành không chuyên CNTT; Chứng chỉ Kỹ năng Trí tuệ nhân tạo tạo sinh bắt buộc tốt nghiệp từ 2026-2027",
        "pdf_nguon": "so_tay_sinh_vien_2026_2027.pdf",
        "trang_pdf": 48,
        "trang_in": "45",
        "dieu_muc_so_qd": "Phần 4, Mục I.2 & I.4",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp chuẩn tin học và chuẩn AI bắt buộc áp dụng từ năm học 2026-2027",
        "pham_vi_ap_dung": "Sinh viên ĐH chính quy tốt nghiệp từ năm 2026-2027"
    },
    {
        "file_markdown": "06_Quy_Dinh_Chuan_Dau_Ra_Tot_Nghiep.md",
        "tieu_de_muc": "3. LỘ TRÌNH VÀ THỦ TỤC XÉT CÔNG NHẬN CHUẨN ĐẦU RA",
        "trich_doan_vi_tri": "Lộ trình khuyến nghị năm 1 đến năm 4; thủ tục nộp hồ sơ trước 45 ngày",
        "pdf_nguon": "",
        "trang_pdf": "",
        "trang_in": "",
        "dieu_muc_so_qd": "",
        "ket_qua_doi_chieu": "Chưa tìm thấy căn cứ trong các nguồn hiện có",
        "ghi_chu_sai_lech": "Sổ tay sinh viên trang 45 chỉ liệt kê 5 chuẩn đầu ra bắt buộc, chưa tìm thấy văn bản hướng dẫn lộ trình 4 năm và thủ tục nộp hồ sơ này",
        "pham_vi_ap_dung": ""
    },

    # --- Tai lieu huong dan giang vien (Tach rieng) ---
    {
        "file_markdown": "[Tài liệu riêng]",
        "tieu_de_muc": "Quy định giảng dạy và đánh giá giảng viên",
        "trich_doan_vi_tri": "Hướng dẫn thực hiện nội quy giảng dạy, đánh giá học phần; Ra đề thi, phân công coi thi, nộp đề thi trước 02 tuần",
        "pdf_nguon": "01-HUONG-DAN-GIANG-VIEN-NCT.pdf",
        "trang_pdf": 1,
        "trang_in": "1",
        "dieu_muc_so_qd": "55/HD-ĐHNCT (28/04/2016)",
        "ket_qua_doi_chieu": "Đã đối chiếu và khớp",
        "ghi_chu_sai_lech": "Khớp văn bản hướng dẫn giảng viên năm 2016; đây là tài liệu nội bộ dành cho giảng viên, có khác biệt về tỷ lệ KTHP (50% so với 60% ở QĐ 580)",
        "pham_vi_ap_dung": "Cán bộ, giảng viên cơ hữu và thỉnh giảng DNC (năm 2016)"
    }
]

with open(doi_chieu_file, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "file_markdown", "tieu_de_muc", "trich_doan_vi_tri", "pdf_nguon",
        "trang_pdf", "trang_in", "dieu_muc_so_qd", "ket_qua_doi_chieu",
        "ghi_chu_sai_lech", "pham_vi_ap_dung"
    ])
    writer.writeheader()
    writer.writerows(doi_chieu_data)

# 2. DANH_SACH_VAN_DE.csv
van_de_file = os.path.join(out_dir, "DANH_SACH_VAN_DE.csv")
van_de_data = [
    {
        "ma_van_de": "ISSUE-DATA-01",
        "nhom_van_de": "Khả năng trích xuất PDF (OCR)",
        "muc_do_anh_huong": "Nghiêm trọng",
        "mo_ta_van_de": "Toàn bộ 26 trang của QĐ 580 và 49 trang của Sổ tay sinh viên là ảnh scan/đồ họa không có text layer (0 ký tự trích xuất qua PyMuPDF/pdfplumber). File hướng dẫn giảng viên có text layer nhưng bị lỗi mã hóa font tiếng Việt nặng.",
        "bang_chung_cu_the": "pdfplumber extract_text() trả về rỗng cho 100% trang của QĐ 580 (26/26) và Sổ tay sinh viên (49/49). File 01-HUONG-DAN... trích xuất ra 'BOorAo DT)C vA DAo TAO CONG HoA xA HOI...'",
        "huong_xu_ly": "Thực hiện OCR offline cục bộ có hỗ trợ tiếng Việt hoặc số hóa có đối chiếu từng trang trước khi chia đoạn; tuyệt đối không nạp file PDF rỗng text vào pipeline.",
        "trang_thai": "Chờ xử lý"
    },
    {
        "ma_van_de": "ISSUE-DATA-02",
        "nhom_van_de": "Sai lệch nội dung quy chế điểm số",
        "muc_do_anh_huong": "Nghiêm trọng",
        "mo_ta_van_de": "File 02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md sai lệch về thang điểm quy đổi và điều kiện đạt/tích lũy học phần so với QĐ 580 và Sổ tay sinh viên.",
        "bang_chung_cu_the": "MD ghi điểm A là 8.5-10.0 (thực tế DNC là 9.0-10.0); B+ là 8.0-8.4 (thực tế DNC là 8.0-8.9); MD ghi điểm D (4.0-4.9) là Đạt/Tích lũy (thực tế DNC Điều 17 QĐ 580 quy định điểm D là KHÔNG ĐẠT/KHÔNG TÍCH LŨY, chỉ từ 5.0 trở lên - D+ mới được tích lũy).",
        "huong_xu_ly": "Hiệu chỉnh bảng quy đổi thang điểm và điều kiện học lại/học cải thiện trong bản đề xuất sửa File 02 theo Điều 17 QĐ 580.",
        "trang_thai": "Chờ xử lý"
    },
    {
        "ma_van_de": "ISSUE-DATA-03",
        "nhom_van_de": "Sai lệch cơ cấu năm học và số tín chỉ",
        "muc_do_anh_huong": "Nghiêm trọng",
        "mo_ta_van_de": "File 02_Quy_Che_Dao_Tao_Va_Hoc_Tap.md mô tả cấu trúc năm học 2 học kỳ chính + 1 hè và mức tín chỉ 14-25, khác với quy định 3 học kỳ/năm của DNC.",
        "bang_chung_cu_the": "Điều 3 Khoản 2.b QĐ 580: DNC tổ chức mỗi năm 03 học kỳ (10-12 tuần học + 2 tuần thi). Điều 7 Khoản 2: Đăng ký 7-15 tín chỉ/kỳ (CT 4 năm), 9-20 (CT 5 năm), 10-23 (CT 6 năm). MD ghi 2 kỳ chính 15 tuần và 14-25 tín chỉ.",
        "huong_xu_ly": "Đề xuất sửa lại mô tả năm học và giới hạn tín chỉ đăng ký theo đúng Điều 3 và Điều 7 của QĐ 580.",
        "trang_thai": "Chờ xử lý"
    },
    {
        "ma_van_de": "ISSUE-DATA-04",
        "nhom_van_de": "Thông tin liên hệ danh bạ có sai lệch",
        "muc_do_anh_huong": "Nghiêm trọng",
        "mo_ta_van_de": "File 01_Tong_Quan_Va_Danh_Ba_DNC.md có nhiều số điện thoại và email phòng ban không khớp với thông tin in trên Sổ tay sinh viên.",
        "bang_chung_cu_the": "Phòng QLĐT trong PDF là 02923 798 999 (Zalo 0907668874, phongdaotao@nctu.edu.vn); Phòng QL HSSV là 02923 798 444 (phongqlhssv@nctu.edu.vn); Phòng TC-KH là 02923 751 668 (phongtc-kh@nctu.edu.vn); Phòng Khảo thí là 02923 798 668.",
        "huong_xu_ly": "Thay thế các số điện thoại, Zalo và email phòng ban theo đúng Bảng danh bạ trang 9-10 Sổ tay sinh viên 2026-2027.",
        "trang_thai": "Chờ xử lý"
    },
    {
        "ma_van_de": "ISSUE-DATA-05",
        "nhom_van_de": "Sai lệch tỷ lệ miễn giảm và thông tin học bổng",
        "muc_do_anh_huong": "Nghiêm trọng",
        "mo_ta_van_de": "File 05_Hoc_Phi_Mien_Giam_Va_Hoc_Bong.md phân sai nhóm sinh viên khuyết tật nặng (20% thành 50%), thiếu các chính sách ưu đãi địa phương và cán bộ của DNC, tự đưa vào mức học bổng 100% và 50-70% kèm ngưỡng điểm GPA cố định.",
        "bang_chung_cu_the": "QĐ 123 tại trang 43 Sổ tay: Khuyết tật nặng giảm 20% (MD ghi 50%); có giảm cho thân nhân cán bộ GV (20%), Đà Nẵng (15%), các xã Đại Lộc/Hà Nha... (20% + KTX). Mục học bổng trang 42 Sổ tay không có số 100% hay GPA 3.60.",
        "huong_xu_ly": "Cập nhật các mức phần trăm miễn giảm và ghi rõ điều kiện học bổng xét từ trên xuống dưới theo quỹ hàng năm của trường.",
        "trang_thai": "Chờ xử lý"
    },
    {
        "ma_van_de": "ISSUE-DATA-06",
        "nhom_van_de": "Nội dung chưa tìm thấy căn cứ trong nguồn PDF",
        "muc_do_anh_huong": "Trung bình",
        "mo_ta_van_de": "Một số mục trong Markdown chưa tìm thấy căn cứ trong 3 PDF: Bảng 29 hành vi kỷ luật (file 03), ngưỡng điểm cảnh báo học tập 0.80/1.00/1.20 (file 02), lộ trình khuyến nghị 4 năm chuẩn đầu ra (file 06).",
        "bang_chung_cu_the": "Sổ tay trang 35 chỉ có đoạn ngắn về nội trú; Sổ tay trang 22 chỉ có 6 điều kiện buộc thôi học; Sổ tay trang 45 chỉ có danh mục 5 chuẩn đầu ra.",
        "huong_xu_ly": "Gắn nhãn metadata 'source_verified = False' hoặc tạm thời chưa đưa các mục này vào kho truy vấn chính thức cho đến khi đối chiếu được với văn bản quyết định riêng của trường.",
        "trang_thai": "Chờ xử lý"
    },
    {
        "ma_van_de": "ISSUE-DATA-07",
        "nhom_van_de": "Phân loại tài liệu giảng viên",
        "muc_do_anh_huong": "Trung bình",
        "mo_ta_van_de": "File 01-HUONG-DAN-GIANG-VIEN-NCT.pdf ban hành năm 2016 (Số 55/HD-ĐHNCT) là văn bản nội bộ dành cho giảng viên và có tỷ lệ đánh giá cũ (50% KTHP) khác biệt với QĐ 580.",
        "bang_chung_cu_the": "Văn bản ghi rõ 'HƯỚNG DẪN THỰC HIỆN NỘI QUY GIẢNG DẠY', ký năm 2016. Tỷ lệ thi KTHP 50% khác biệt với QĐ 580 (2024) quy định 60%.",
        "huong_xu_ly": "Phân loại file này vào nhóm 'Tài liệu nghiệp vụ giảng viên - Quyết định chưa kích hoạt trong chatbot sinh viên' để tránh xung đột dữ liệu.",
        "trang_thai": "Đã ghi nhận"
    }
]

with open(van_de_file, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "ma_van_de", "nhom_van_de", "muc_do_anh_huong", "mo_ta_van_de",
        "bang_chung_cu_the", "huong_xu_ly", "trang_thai"
    ])
    writer.writeheader()
    writer.writerows(van_de_data)

print(f"Updated {doi_chieu_file} ({len(doi_chieu_data)} rows) and {van_de_file} ({len(van_de_data)} rows).")
