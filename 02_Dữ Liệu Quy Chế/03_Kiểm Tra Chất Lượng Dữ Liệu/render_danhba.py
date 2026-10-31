import os
import pypdfium2 as pdfium

out_dir = r"02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\sample_renders"
pdf_path = r"02_Dữ Liệu Quy Chế\01_Tài Liệu Gốc (PDF)\so_tay_sinh_vien_2026_2027.pdf"

pdf = pdfium.PdfDocument(pdf_path)

# Let's render pages 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
# Note: In PDF, page index is 0-based.
# PDF page 12 is index 11 (printed page 9: Danh bạ các phòng/ban/viện/trung tâm)
for pno in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]:
    page = pdf[pno - 1]
    img = page.render(scale=1.5).to_pil()
    img_name = f"so_tay_p{pno:02d}.png"
    img.save(os.path.join(out_dir, img_name))
    print(f"Rendered so_tay page {pno} -> {img_name}")
