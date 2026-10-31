import os
import pypdfium2 as pdfium

out_dir = r"02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\sample_renders"
os.makedirs(out_dir, exist_ok=True)

# 580: render pages 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25
doc_580_path = r"02_Dữ Liệu Quy Chế\01_Tài Liệu Gốc (PDF)\580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf"
pdf_580 = pdfium.PdfDocument(doc_580_path)

# Render key pages of 580:
# Let's render all pages of 580 or key ones to inspect articles
for pno in range(1, 27):
    page = pdf_580[pno - 1]
    img = page.render(scale=1.5).to_pil()
    img.save(os.path.join(out_dir, f"580_p{pno:02d}.png"))

print("Rendered all 26 pages of QĐ 580.")

# Sổ tay: render pages 21 to 30 (which correspond to printed pages 18 to 27)
so_tay_path = r"02_Dữ Liệu Quy Chế\01_Tài Liệu Gốc (PDF)\so_tay_sinh_vien_2026_2027.pdf"
pdf_sotay = pdfium.PdfDocument(so_tay_path)
for pno in range(21, 31):
    page = pdf_sotay[pno - 1]
    img = page.render(scale=1.5).to_pil()
    img.save(os.path.join(out_dir, f"sotay_p{pno:02d}.png"))

print("Rendered pages 21-30 of Sổ tay sinh viên.")
