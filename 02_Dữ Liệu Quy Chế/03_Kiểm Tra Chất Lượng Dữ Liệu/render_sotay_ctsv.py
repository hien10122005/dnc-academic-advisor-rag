import os
import pypdfium2 as pdfium

out_dir = r"02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\sample_renders"
pdf_path = r"02_Dữ Liệu Quy Chế\01_Tài Liệu Gốc (PDF)\so_tay_sinh_vien_2026_2027.pdf"
pdf = pdfium.PdfDocument(pdf_path)

# PDF pages 28 to 38 (index 27 to 37) correspond to printed pages 25 to 35
for pno in range(28, 39):
    page = pdf[pno - 1]
    img = page.render(scale=1.5).to_pil()
    img_name = f"sotay_p{pno:02d}.png"
    img.save(os.path.join(out_dir, img_name))
    print(f"Rendered so_tay page {pno} -> {img_name}")
