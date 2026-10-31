"""
Script tạo file Word chuẩn trường ĐH Nam Cần Thơ (QĐ 309/QĐ-ĐHNCT)
Chạy: python tao_tai_lieu_du_an.py
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

# ──────────────────────────────────────────────
#  HÀM TIỆN ÍCH
# ──────────────────────────────────────────────

def set_page_margins(doc):
    """Chuẩn lề theo QĐ 309: Trái 3.5cm, Phải 2cm, Trên 2.5cm, Dưới 2.5cm."""
    for section in doc.sections:
        section.left_margin   = Cm(3.5)
        section.right_margin  = Cm(2.0)
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.header_distance = Cm(1.0)
        section.footer_distance = Cm(1.0)

def fmt_paragraph(para, font_size=13, bold=False, italic=False,
                  align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=0,
                  line_spacing=1.2, first_line_indent=None):
    """Áp định dạng chuẩn cho một đoạn văn."""
    para.alignment = align
    pf = para.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after  = Pt(space_after)
    pf.line_spacing = Pt(font_size * line_spacing)
    if first_line_indent is not None:
        pf.first_line_indent = Cm(first_line_indent)
    for run in para.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        run.font.bold   = bold
        run.font.italic = italic

def add_heading(doc, text, level=1, font_size=13, bold=True,
                align=WD_ALIGN_PARAGRAPH.LEFT, uppercase=False, page_break=False):
    """Thêm đề mục chuẩn."""
    if page_break:
        para = doc.add_page_break()
    para = doc.add_paragraph()
    para.alignment = align
    para.paragraph_format.space_before = Pt(6)
    para.paragraph_format.space_after  = Pt(0)
    para.paragraph_format.line_spacing = Pt(font_size * 1.2)
    run = para.add_run(text.upper() if uppercase else text)
    run.font.name  = "Times New Roman"
    run.font.size  = Pt(font_size)
    run.font.bold  = bold
    return para

def add_body(doc, text, indent=1.0):
    """Thêm đoạn thân bài chuẩn."""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para.paragraph_format.space_before      = Pt(6)
    para.paragraph_format.space_after       = Pt(0)
    para.paragraph_format.line_spacing      = Pt(13 * 1.2)
    para.paragraph_format.first_line_indent = Cm(indent)
    run = para.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    return para

def add_table(doc, headers, rows, caption, source):
    """Thêm bảng chuẩn: tên bảng phía trên căn trái, nguồn phía dưới căn giữa nghiêng."""
    # Tên bảng (phía trên, căn trái)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    cap.paragraph_format.space_before = Pt(6)
    cap.paragraph_format.space_after  = Pt(2)
    cap.paragraph_format.line_spacing = Pt(13 * 1.2)
    run_cap = cap.add_run(caption)
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(13)
    run_cap.font.bold = False

    # Bảng
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = hdr_cells[i].paragraphs[0].runs[0]
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.bold = True
        # Màu nền tiêu đề
        tc = hdr_cells[i]._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "D9D9D9")
        tcPr.append(shd)

    # Data rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, cell_text in enumerate(row_data):
            row_cells[c_idx].text = str(cell_text)
            row_cells[c_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in row_cells[c_idx].paragraphs[0].runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)

    # Nguồn (phía dưới, căn giữa, nghiêng, cỡ 11)
    src = doc.add_paragraph()
    src.alignment = WD_ALIGN_PARAGRAPH.CENTER
    src.paragraph_format.space_before = Pt(2)
    src.paragraph_format.space_after  = Pt(6)
    src.paragraph_format.line_spacing = Pt(11)
    run_src = src.add_run(source)
    run_src.font.name   = "Times New Roman"
    run_src.font.size   = Pt(11)
    run_src.font.italic = True

    return table

# ──────────────────────────────────────────────
#  XÂY DỰNG TÀI LIỆU
# ──────────────────────────────────────────────

def build_document():
    doc = Document()
    set_page_margins(doc)

    # ── TRANG TIÊU ĐỀ ──────────────────────────────────────────────────────
    header = doc.add_paragraph()
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header.paragraph_format.space_before = Pt(0)
    header.paragraph_format.space_after  = Pt(0)
    run_h = header.add_run(
        "TRƯỜNG ĐẠI HỌC NAM CẦN THƠ\n"
        "TRƯỜNG CÔNG NGHỆ SỐ & TRÍ TUỆ NHÂN TẠO"
    )
    run_h.font.name = "Times New Roman"
    run_h.font.size = Pt(13)
    run_h.font.bold = True

    doc.add_paragraph()  # khoảng trắng

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(12)
    title.paragraph_format.space_after  = Pt(6)
    run_t = title.add_run("TÀI LIỆU MÔ TẢ DỰ ÁN\nĐỒ ÁN 2 — CHUYÊN NGÀNH CÔNG NGHỆ THÔNG TIN")
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(16)
    run_t.font.bold = True

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_before = Pt(6)
    subtitle.paragraph_format.space_after  = Pt(0)
    run_s = subtitle.add_run(
        "Tên đề tài:\n"
        "Xây dựng hệ thống trợ lý ảo hỗ trợ tra cứu quy chế học vụ\n"
        "ứng dụng kỹ thuật Retrieval-Augmented Generation (RAG)"
    )
    run_s.font.name   = "Times New Roman"
    run_s.font.size   = Pt(14)
    run_s.font.bold   = True
    run_s.font.italic = False

    doc.add_paragraph()
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.paragraph_format.space_before = Pt(24)
    run_i = info.add_run(
        f"Học kỳ 1 — Năm học 2026 – 2027\n"
        f"Ngày lập: {datetime.date.today().strftime('%d/%m/%Y')}"
    )
    run_i.font.name = "Times New Roman"
    run_i.font.size = Pt(13)

    doc.add_page_break()

    # ── PHẦN 1: THÔNG TIN CƠ BẢN ───────────────────────────────────────────
    add_heading(doc, "I. THÔNG TIN CHUNG VỀ ĐỀ TÀI", level=1, font_size=14,
                align=WD_ALIGN_PARAGRAPH.CENTER, uppercase=False)

    info_headers = ["Thuộc tính", "Chi tiết"]
    info_rows = [
        ["Tên đề tài",          "Xây dựng hệ thống trợ lý ảo hỗ trợ tra cứu quy chế học vụ ứng dụng kỹ thuật Retrieval-Augmented Generation (RAG)"],
        ["Môn học",             "Đồ án 2 – Chuyên ngành Công nghệ Thông tin (CNTT)"],
        ["Học kỳ",              "Học kỳ 1 – Năm học 2026 – 2027"],
        ["Trường",              "Đại học Nam Cần Thơ (DNC) — Trường Công nghệ Số & Trí tuệ Nhân tạo"],
        ["Lớp",                 "DH23TIN (Khóa 2023)"],
        ["Thời gian thực hiện", "26/10/2026 – 03/01/2027 (~10 tuần)"],
        ["Hạn nộp bài",         "04/01/2027 – 10/01/2027"],
        ["Thể thức trình bày",  "Quyết định 309/QĐ-ĐHNCT ngày 08/12/2016"],
        ["Độ dài báo cáo",      "30 – 50 trang (không kể phụ lục)"],
    ]
    add_table(doc, info_headers, info_rows,
              "Bảng 1.1 Thông tin tổng quan đề tài",
              "Nguồn: Kế hoạch số 112/KH-CNS&TTNT ngày 19/10/2026")

    # ── PHẦN 2: MỤC TIÊU ───────────────────────────────────────────────────
    add_heading(doc, "II. MỤC TIÊU NGHIÊN CỨU", level=1, font_size=14,
                align=WD_ALIGN_PARAGRAPH.CENTER, page_break=True)

    add_heading(doc, "2.1 Mục tiêu tổng quát", font_size=13)
    add_body(doc,
        "Xây dựng hệ thống trợ lý ảo thông minh có khả năng giải đáp tự động các câu "
        "hỏi liên quan đến quy chế học vụ, quy định đào tạo, học bổng và thủ tục hành "
        "chính của Trường Đại học Nam Cần Thơ. Hệ thống ứng dụng kỹ thuật RAG "
        "(Retrieval-Augmented Generation) kết hợp cơ sở dữ liệu Vector để đảm bảo câu "
        "trả lời luôn chính xác, có căn cứ pháp lý rõ ràng và không xảy ra hiện tượng "
        "ảo giác (Hallucination) thông tin.")

    add_heading(doc, "2.2 Mục tiêu cụ thể", font_size=13)
    goals = [
        "Số hóa và chuẩn hóa toàn bộ kho văn bản quy chế đào tạo của trường DNC thành dạng Vector Embedding có thể tra cứu ngữ nghĩa.",
        "Xây dựng pipeline RAG hoàn chỉnh: Tiếp nhận câu hỏi → Tìm kiếm ngữ cảnh tương quan → Sinh câu trả lời kèm trích dẫn văn bản gốc.",
        "Triển khai giao diện Web Chatbot thân thiện để sinh viên sử dụng trực tiếp không cần cài đặt.",
        "Đảm bảo hệ thống kiểm soát hiện tượng ảo giác thông qua System Prompt nghiêm ngặt và tham số Temperature thấp.",
        "Đánh giá định lượng chất lượng hệ thống thông qua các độ đo: Hit Rate, MRR, Faithfulness và Answer Relevance.",
    ]
    for i, g in enumerate(goals, 1):
        p = doc.add_paragraph(style="List Number")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after  = Pt(0)
        p.paragraph_format.line_spacing = Pt(13 * 1.2)
        p.paragraph_format.left_indent  = Cm(1.0)
        run = p.add_run(g)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)

    # ── PHẦN 3: KIẾN TRÚC HỆ THỐNG ─────────────────────────────────────────
    add_heading(doc, "III. KIẾN TRÚC HỆ THỐNG", level=1, font_size=14,
                align=WD_ALIGN_PARAGRAPH.CENTER, page_break=True)

    add_heading(doc, "3.1 Tổng quan kiến trúc 3 lớp", font_size=13)
    add_body(doc,
        "Hệ thống được thiết kế theo mô hình kiến trúc 3 lớp (3-Tier Architecture) "
        "tách biệt rõ ràng giữa giao diện người dùng, dịch vụ xử lý AI và lớp lưu "
        "trữ dữ liệu, đảm bảo khả năng mở rộng và bảo trì dễ dàng.")

    arch_headers = ["Lớp", "Thành phần", "Công nghệ", "Vai trò"]
    arch_rows = [
        ["Tầng 1 – Giao diện", "Web Chatbot",           "Streamlit",              "Giao diện hội thoại cho sinh viên"],
        ["Tầng 1 – Giao diện", "Admin Panel",            "Streamlit",              "Tải lên & quản lý tài liệu quy chế"],
        ["Tầng 2 – Dịch vụ AI","RAG Pipeline",           "LangChain",              "Điều phối toàn bộ luồng xử lý"],
        ["Tầng 2 – Dịch vụ AI","Embedding Model",        "Vietnamese Bi-Encoder",  "Biến văn bản thành vector số học"],
        ["Tầng 2 – Dịch vụ AI","LLM – Sinh câu trả lời","Gemini 1.5 Flash API",   "Tổng hợp câu trả lời từ ngữ cảnh"],
        ["Tầng 2 – Dịch vụ AI","REST API",               "FastAPI",                "Kết nối Frontend và AI Engine"],
        ["Tầng 3 – Dữ liệu",   "Vector Database",        "ChromaDB",               "Lưu trữ chunks và vector embeddings"],
    ]
    add_table(doc, arch_headers, arch_rows,
              "Bảng 3.1 Mô tả kiến trúc 3 lớp của hệ thống",
              "Nguồn: Tác giả đề xuất thiết kế (2026)")

    # ── PHẦN 4: TECH STACK ──────────────────────────────────────────────────
    add_heading(doc, "IV. CÔNG NGHỆ SỬ DỤNG (TECH STACK)", level=1, font_size=14,
                align=WD_ALIGN_PARAGRAPH.CENTER, page_break=True)

    add_body(doc,
        "Toàn bộ hệ thống được xây dựng bằng ngôn ngữ Python 3.11 và các thư viện "
        "mã nguồn mở hiện đại. Tiêu chí lựa chọn công nghệ ưu tiên: miễn phí 100%, "
        "không yêu cầu phần cứng GPU đắt tiền, được cộng đồng AI toàn cầu sử dụng "
        "rộng rãi và có tài liệu phong phú.")

    tech_headers = ["Thành phần", "Công nghệ / Thư viện", "Phiên bản", "Lý do lựa chọn"]
    tech_rows = [
        ["Ngôn ngữ lập trình",   "Python",                          "3.11",  "Ngôn ngữ số 1 về AI/ML, hệ sinh thái thư viện phong phú"],
        ["Đọc & xử lý PDF",      "pdfplumber / PyMuPDF",            "Latest","Trích xuất text tiếng Việt chuẩn xác, không bị lỗi font"],
        ["RAG Framework",         "LangChain",                       "Latest","Tiêu chuẩn công nghiệp để xây dựng ứng dụng RAG"],
        ["Mô hình Embedding",    "vietnamese-bi-encoder (BKAI)",    "v1",    "Chuyên sâu tiếng Việt, chạy CPU, miễn phí"],
        ["Vector Database",       "ChromaDB",                        "Latest","Mã nguồn mở, lưu cục bộ SQLite, không cần server"],
        ["LLM – Sinh câu trả lời","Google Gemini 1.5 Flash API",    "API",   "Miễn phí cho học tập, tốc độ nhanh, hỗ trợ tiếng Việt tốt"],
        ["Backend API",           "FastAPI",                         "Latest","Hiệu năng cao, tự động tạo tài liệu API (Swagger)"],
        ["Giao diện Web",         "Streamlit",                       "Latest","Tạo Web Chat trong 1 ngày bằng Python thuần, không cần JS"],
    ]
    add_table(doc, tech_headers, tech_rows,
              "Bảng 4.1 Bảng tổng hợp công nghệ sử dụng trong dự án",
              "Nguồn: Tác giả tổng hợp và lựa chọn (2026)")

    # ── PHẦN 5: KẾ HOẠCH TIẾN ĐỘ ───────────────────────────────────────────
    add_heading(doc, "V. KẾ HOẠCH TIẾN ĐỘ THỰC HIỆN (10 TUẦN)", level=1, font_size=14,
                align=WD_ALIGN_PARAGRAPH.CENTER, page_break=True)

    plan_headers = ["Tuần", "Thời gian", "Công việc cụ thể", "Kết quả cần đạt"]
    plan_rows = [
        ["1",  "26/10–01/11", "Thu thập PDF quy chế · Gặp Thầy lần 1 · Viết đề cương",       "Có đủ tài liệu quy chế · Đề cương được duyệt"],
        ["2",  "02/11–08/11", "Xây dựng ingestion.py · Tạo ChromaDB · Test Embedding",         "ChromaDB chứa đủ chunks quy chế DNC"],
        ["3",  "09/11–15/11", "Xây dựng rag_engine.py · Kết nối Gemini API · Test Terminal",   "Hỏi đáp cơ bản chạy được trên Terminal"],
        ["4",  "16/11–22/11", "Xây dựng Streamlit Chat UI · Gặp Thầy lần 2",                  "Demo Web Chatbot cơ bản hoàn chỉnh"],
        ["5",  "23/11–29/11", "Tinh chỉnh Prompt · Thêm trích dẫn nguồn · Test 30 câu hỏi",   "Độ chính xác >85% trên tập test"],
        ["6",  "30/11–06/12", "Vẽ sơ đồ hệ thống · Chụp màn hình demo · Gặp Thầy lần 3",     "Hoàn chỉnh bộ sơ đồ cho báo cáo"],
        ["7",  "07/12–13/12", "Viết Chương 1 & Chương 2 báo cáo",                              "Hoàn thành 2 chương đầu"],
        ["8",  "14/12–20/12", "Viết Chương 3 & Chương 4 báo cáo",                              "Hoàn thành toàn bộ 4 chương"],
        ["9",  "21/12–27/12", "Hoàn chỉnh báo cáo · Gặp Thầy lần 4 · Chỉnh theo góp ý",      "Báo cáo hoàn chỉnh được Thầy chấp thuận"],
        ["10", "28/12–03/01", "Làm slide · Demo lần cuối · In đóng cuốn · Nộp bài đúng hạn",  "Nộp đầy đủ: báo cáo in + file CD"],
    ]
    add_table(doc, plan_headers, plan_rows,
              "Bảng 5.1 Kế hoạch tiến độ thực hiện đề tài 10 tuần",
              "Nguồn: Tác giả lập kế hoạch căn cứ Kế hoạch số 112/KH-CNS&TTNT")

    # ── PHẦN 6: CẤU TRÚC BÁO CÁO ───────────────────────────────────────────
    add_heading(doc, "VI. CẤU TRÚC QUYỂN BÁO CÁO (30 – 50 TRANG)", level=1, font_size=14,
                align=WD_ALIGN_PARAGRAPH.CENTER, page_break=True)

    chapters = [
        ("CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI",
         ["1.1  Đặt vấn đề và bối cảnh thực tế",
          "1.2  Các hệ thống liên quan đã được nghiên cứu",
          "1.3  Mục tiêu nghiên cứu",
          "1.4  Đối tượng và phạm vi nghiên cứu",
          "1.5  Phương pháp nghiên cứu và bố cục báo cáo"]),
        ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT",
         ["2.1  Mô hình ngôn ngữ lớn (Large Language Models – LLMs)",
          "2.2  Kiến trúc Retrieval-Augmented Generation (RAG)",
          "2.3  Kỹ thuật Vector Embedding và độ đo Cosine Similarity",
          "2.4  Cơ sở dữ liệu Vector (Vector Database – ChromaDB)",
          "2.5  Mô hình nhúng tiếng Việt (Vietnamese Bi-Encoder)",
          "2.6  Kỹ thuật Prompt Engineering và kiểm soát Hallucination"]),
        ("CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG",
         ["3.1  Phân tích yêu cầu chức năng và phi chức năng",
          "3.2  Sơ đồ ca sử dụng (Use Case Diagram)",
          "3.3  Đặc tả chi tiết các ca sử dụng cốt lõi",
          "3.4  Thiết kế kiến trúc hệ thống 3 lớp",
          "3.5  Thiết kế luồng xử lý RAG (Sequence Diagram)",
          "3.6  Thiết kế cơ sở dữ liệu Vector (Cấu trúc Chunk & Metadata)",
          "3.7  Thiết kế giao diện người dùng (UI Wireframe)"]),
        ("CHƯƠNG 4: HIỆN THỰC HÓA VÀ ĐÁNH GIÁ KẾT QUẢ",
         ["4.1  Môi trường phát triển và cài đặt thư viện",
          "4.2  Cấu trúc tổ chức mã nguồn dự án",
          "4.3  Hiện thực pipeline Ingestion (Nạp dữ liệu quy chế)",
          "4.4  Hiện thực pipeline Query (Truy vấn và sinh câu trả lời)",
          "4.5  Giao diện hệ thống (Màn hình demo thực tế)",
          "4.6  Đánh giá chất lượng hệ thống (Hit Rate, Faithfulness, Relevance)",
          "4.7  Kiểm thử hệ thống (Test Cases Matrix)"]),
    ]

    for ch_title, sections in chapters:
        add_heading(doc, ch_title, font_size=13, bold=True)
        for sec in sections:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after  = Pt(0)
            p.paragraph_format.line_spacing = Pt(13 * 1.2)
            p.paragraph_format.left_indent  = Cm(1.0)
            run = p.add_run(sec)
            run.font.name = "Times New Roman"
            run.font.size = Pt(13)

    # ── PHẦN 7: CẤU TRÚC THỰ MỤC ───────────────────────────────────────────
    add_heading(doc, "VII. CẤU TRÚC THƯ MỤC DỰ ÁN", level=1, font_size=14,
                align=WD_ALIGN_PARAGRAPH.CENTER, page_break=True)

    folder_headers = ["Thư mục", "Nội dung lưu trữ"]
    folder_rows = [
        ["01_Kế Hoạch & Hướng Dẫn/",              "File kế hoạch môn học, quy định lịch nộp bài và tiêu chí chấm điểm của Khoa"],
        ["02_Dữ Liệu Quy Chế/01_Tài Liệu Gốc (PDF)/", "Các file PDF quy chế đào tạo gốc chưa xử lý"],
        ["02_Dữ Liệu Quy Chế/02_Văn Bản Đã Làm Sạch (Text)/","File text sạch sau khi chạy script trích xuất và chuẩn hóa"],
        ["03_Đề Cương & Báo Cáo/01_Đề Cương Chi Tiết/", "File Word đề cương gửi Thầy hướng dẫn duyệt"],
        ["03_Đề Cương & Báo Cáo/02_Bản Thảo Báo Cáo (Drafts)/","Các bản nháp từng chương trong quá trình viết"],
        ["03_Đề Cương & Báo Cáo/03_Bản In Chính Thức (Final)/","File Word/PDF hoàn chỉnh chuẩn QĐ 309 để in đóng cuốn nộp trường"],
        ["04_Slide Thuyết Trình/",                "File PowerPoint báo cáo bảo vệ trước Hội đồng chấm đồ án"],
        ["05_Mã Nguồn Chương Trình/backend/",     "Code Python xử lý AI: config.py, ingestion.py, rag_engine.py, main.py"],
        ["05_Mã Nguồn Chương Trình/frontend/",    "Code giao diện Streamlit: app.py (Web Chatbot sinh viên)"],
        ["05_Mã Nguồn Chương Trình/chroma_db/",   "Cơ sở dữ liệu Vector ChromaDB (tự động tạo khi chạy ingestion.py)"],
        ["05_Mã Nguồn Chương Trình/notebooks/",   "File Jupyter Notebook thử nghiệm từng module AI riêng lẻ"],
        ["06_Tài Liệu Tham Khảo/",               "Bài báo khoa học, sách, tài liệu về RAG, LLM dùng để trích dẫn báo cáo"],
        ["07_Hình Ảnh & Sơ Đồ Hệ Thống/",        "Sơ đồ kiến trúc, Use Case, Sequence Diagram và ảnh chụp màn hình demo"],
        ["08_Biên Bản & Nhật Ký Gặp Thầy/",      "Biên bản ghi lại nội dung ít nhất 4 lần gặp Thầy hướng dẫn theo quy định"],
    ]
    add_table(doc, folder_headers, folder_rows,
              "Bảng 7.1 Mô tả cấu trúc thư mục quản lý dự án",
              "Nguồn: Tác giả tự tổ chức (2026)")

    # ── PHẦN 8: LƯU Ý QUAN TRỌNG ───────────────────────────────────────────
    add_heading(doc, "VIII. LƯU Ý QUAN TRỌNG", level=1, font_size=14,
                align=WD_ALIGN_PARAGRAPH.CENTER, page_break=True)

    notes = [
        ("⚠️  Dữ liệu quy chế:",
         "File so_tay_sinh_vien_2026_2027.pdf hiện là file ảnh scan (76 MB, không có lớp text). "
         "Cần bổ sung thêm các file quy chế đào tạo dạng text từ cổng thông tin trường tại dnc.edu.vn "
         "để hệ thống RAG đọc và trích xuất chính xác."),
        ("⚠️  API Key Gemini:",
         "Tạo miễn phí tại aistudio.google.com. Lưu vào file backend/config.py. "
         "TUYỆT ĐỐI KHÔNG đưa API key vào code khi đẩy lên GitHub."),
        ("⚠️  Deadline:",
         "Hạn nộp báo cáo: 04/01/2027 – 10/01/2027. Cần hoàn thành toàn bộ code và báo cáo "
         "trước ngày 28/12/2026 để có thời gian in đóng cuốn."),
        ("⚠️  Yêu cầu gặp Thầy:",
         "Phải gặp Giảng viên hướng dẫn ít nhất 4 lần trong suốt quá trình thực hiện. "
         "Ghi biên bản đầy đủ và lưu vào thư mục '08_Biên Bản & Nhật Ký Gặp Thầy'."),
        ("✅  Chi phí thực hiện:",
         "Gần như 0 đồng. ChromaDB miễn phí, Mô hình nhúng tiếng Việt miễn phí, "
         "Gemini API miễn phí cho tài khoản cá nhân (hạn mức 15 RPM, 1 triệu token/tháng)."),
    ]

    for title, content in notes:
        add_heading(doc, title, font_size=13, bold=True)
        add_body(doc, content)

    # ── FOOTER ──────────────────────────────────────────────────────────────
    footer_para = doc.add_paragraph()
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_para.paragraph_format.space_before = Pt(24)
    run_f = footer_para.add_run(
        f"─────────────────────────────────────────────\n"
        f"Tài liệu được tạo tự động ngày {datetime.date.today().strftime('%d/%m/%Y')}\n"
        f"Trường Đại học Nam Cần Thơ – Đồ án 2 – Học kỳ 1 năm học 2026 – 2027"
    )
    run_f.font.name   = "Times New Roman"
    run_f.font.size   = Pt(11)
    run_f.font.italic = True

    # ── LƯU FILE ────────────────────────────────────────────────────────────
    output_path = r"03_Đề Cương & Báo Cáo\01_Đề Cương Chi Tiết\TÀI LIỆU DỰ ÁN.docx"
    doc.save(output_path)
    print(f"✅ Đã tạo file Word thành công: {output_path}")
    return output_path

if __name__ == "__main__":
    build_document()
