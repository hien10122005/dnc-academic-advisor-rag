import os
import glob

md_dir = r"02_Dữ Liệu Quy Chế\02_Văn Bản Đã Làm Sạch (Text)"
md_files = sorted(glob.glob(os.path.join(md_dir, "*.md")))

for fpath in md_files:
    fname = os.path.basename(fpath)
    size_bytes = os.path.getsize(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    print(f"\n==========================================")
    print(f"MD FILE: {fname} | Size: {size_bytes} bytes | Lines: {len(lines)}")
    headings = [line for line in lines if line.strip().startswith("#")]
    print(f"Headings count: {len(headings)}")
    for h in headings[:10]:
        print(f"  {h}")
    if len(headings) > 10:
        print(f"  ... and {len(headings) - 10} more headings")
