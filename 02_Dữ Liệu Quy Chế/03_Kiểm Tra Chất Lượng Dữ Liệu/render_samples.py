import os
import pypdfium2 as pdfium

out_dir = r"02_Dữ Liệu Quy Chế\03_Kiểm Tra Chất Lượng Dữ Liệu\sample_renders"
os.makedirs(out_dir, exist_ok=True)

pdf_dir = r"02_Dữ Liệu Quy Chế\01_Tài Liệu Gốc (PDF)"
tasks = [
    ("01-HUONG-DAN-GIANG-VIEN-NCT.pdf", [1, 2, 6]),
    ("580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf", [1, 2, 3, 5, 10, 20, 26]),
    ("so_tay_sinh_vien_2026_2027.pdf", [1, 2, 3, 4, 5, 10, 25, 45, 49])
]

for fname, pages in tasks:
    fpath = os.path.join(pdf_dir, fname)
    pdf = pdfium.PdfDocument(fpath)
    prefix = fname.split("-")[0].replace(".pdf", "")
    for pno in pages:
        page = pdf[pno - 1]
        image = page.render(scale=1.5).to_pil()
        out_name = f"{prefix}_page_{pno:02d}.png"
        image.save(os.path.join(out_dir, out_name))
        print(f"Rendered {fname} page {pno} -> {out_name} (size: {image.size})")

print("Rendering complete.")
