import os
import pypdfium2 as pdfium

out_dir = r"02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\sample_renders"
doc_path = r"02_Dữ Liệu Quy Chế\01_Tài Liệu Gốc (PDF)\01-HUONG-DAN-GIANG-VIEN-NCT.pdf"
pdf = pdfium.PdfDocument(doc_path)

for pno in [1, 2, 3, 4, 5, 6]:
    page = pdf[pno - 1]
    img = page.render(scale=1.5).to_pil()
    img_name = f"hdgv_p{pno:02d}.png"
    img.save(os.path.join(out_dir, img_name))
    print(f"Rendered hdgv page {pno} -> {img_name}")
