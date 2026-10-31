import os
import sys
import pypdf
import pdfplumber

pdf_dir = r"02_Dữ Liệu Quy Chế\01_Tài Liệu Gốc (PDF)"
files = [
    "01-HUONG-DAN-GIANG-VIEN-NCT.pdf",
    "580-QD-DHNCT-quy-che-dao-tao-trinh-do-dai-hoc-so-580-ngay-02-08-2024.pdf",
    "so_tay_sinh_vien_2026_2027.pdf"
]

for fname in files:
    fpath = os.path.join(pdf_dir, fname)
    size_bytes = os.path.getsize(fpath)
    print(f"\n==========================================")
    print(f"FILE: {fname}")
    print(f"SIZE: {size_bytes} bytes ({size_bytes / (1024*1024):.2f} MB)")
    
    with pdfplumber.open(fpath) as pdf:
        num_pages = len(pdf.pages)
        print(f"PAGES: {num_pages}")
        
        zero_text_pages = []
        low_text_pages = [] # < 100 chars
        normal_text_pages = [] # >= 100 chars
        
        for idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            text_len = len(text.strip())
            images = page.images
            
            if text_len == 0:
                zero_text_pages.append((idx, len(images)))
            elif text_len < 100:
                low_text_pages.append((idx, text_len, len(images), text.strip()[:60].replace('\n', ' ')))
            else:
                normal_text_pages.append((idx, text_len))
        
        print(f"Total pages: {num_pages}")
        print(f"Zero text pages: {len(zero_text_pages)} -> {zero_text_pages[:20]}")
        print(f"Low text pages (<100 chars): {len(low_text_pages)} -> {low_text_pages[:20]}")
        print(f"Normal text pages (>=100 chars): {len(normal_text_pages)}")
        
        # Sample first 3 pages and last 2 pages text
        print("\n--- SAMPLE PAGE 1 TEXT ---")
        p1 = pdf.pages[0].extract_text()
        print((p1[:300] if p1 else "[NO TEXT EXTRACTED]"))
        
        if num_pages > 1:
            print("\n--- SAMPLE PAGE 2 TEXT ---")
            p2 = pdf.pages[1].extract_text()
            print((p2[:300] if p2 else "[NO TEXT EXTRACTED]"))
