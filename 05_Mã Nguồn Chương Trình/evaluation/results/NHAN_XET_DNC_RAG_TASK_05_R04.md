# Codex rà soát DNC-RAG-TASK-05-R04

Ngày kiểm tra: **02/11/2026**, giờ Việt Nam. Project: `dnc-academic-advisor-rag`.

**Kết luận: phần sửa tests đã đạt trong phạm vi kiểm tra cô lập; còn CẦN SỬA bằng chứng rubric.** Không yêu cầu sửa lại production retrieval hoặc fixture đã qua. Chưa chốt rubric/Task05 vì có nhiều offsets và source-ID mapping không đúng với raw contexts.

## 1. Phiên bản và kiểm thử

- HEAD/remote main: **`28f97d54d41edb25e041c80cb42709fce40094a0`**; triển khai R04: `c6f68c82dfbe2cfaea91203c54503a261fb9113b`. Remote `https://github.com/hien10122005/dnc-academic-advisor-rag.git`; working tree sạch khi bắt đầu.
- Production `backend/retrieval.py` giữ nguyên so với R03; SHA chunks/manifest/raw JSONL/raw CSV giữ nguyên. Không sửa code/tests/corpus/gold/raw, không gọi Gemini, không ghi DB thật, không commit/push trong review.

| Kiểm tra độc lập | Kết quả | Phạm vi |
| --- | --- | --- |
| Class readiness regression | **12/12 qua**, 0.508s | Nguyên class test hiện tại qua AST, fake Chroma/embedding setup, retriever import bình thường. Năm lỗi R03 đã hết trong probe này. |
| Vector integrity | **10/10 qua**, 0.424s | Nguyên module test, ML import sentinels trong runner riêng; duplicate-ID có count104 và chạm đúng guard. |
| Focused BM25/RRF/API | **14/14 qua**, 0.202s | Unit tests với fail-on-use ML import sentinels. |
| Runtime probes | Qua | Empty/wrong-ID bị chặn; cache hai thế hệ, trace single retrieval và hai CLI sparse-only tiếp tục qua dependency mocks. |
| Test isolation | Đã sửa qua đọc diff | Module `test_vector_integrity.py` không còn cài mock Chroma/SentenceTransformer vào `sys.modules`. |
| Toàn suite80 | **Chưa có kết quả** | Đã thử discover offline/key rỗng; dừng khi vẫn import dependencies trên ổ đồng bộ. Không xem 36 tests cô lập là 80 tests hay end-to-end integration thật. |

Artifact: [KIEM_TRA_DOC_LAP_TASK05_R04.json](KIEM_TRA_DOC_LAP_TASK05_R04.json). Logs local được Git ignore: `scratch/review_task05_r04_regression.log`, `review_task05_r04_integrity.log`, `review_task05_r04_focused.log`, `review_task05_r04_runtime.log`, `review_task05_r04_suite.log`.

## 2. [P2] Rubric có offsets/source-ID mapping sai dù full chunk IDs hợp lệ

File: `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R04.md`.

Đã chạy script đối chiếu **72 hàng** với đúng `retrieved_contexts` của 20 raw records và `source_spans` của corpus. Kết quả:

- Không có full chunk ID không tồn tại.
- Có **14 cặp source ID–chunk sai** (không đồng nghĩa 14 ca).
- Trong **57 khoảng offsets** ghi tường minh trong cột evidence, có **24 khoảng trên24 hàng vượt phạm vi chunk được dẫn**. Đây là kiểm tra cấu trúc theo envelope trang của các source spans; còn cần đọc nội dung để xác nhận mỗi span hỗ trợ ý gold. Không suy “33 khoảng còn lại đúng ngữ nghĩa” chỉ vì chúng nằm trong phạm vi.

Ví dụ xác minh trực tiếp:

| Ý rubric | Ghi trong R04 | Thực tế từ raw/context/source spans |
| --- | --- | --- |
| DEV01 P2/P3, cả hai mode | `SRC-2 = c062`, p15 `[462,1149)` | `SRC-2` là c065; tìm source ID của c062 trong đúng record. Source span bảng c062 là p15 **`[436,858)`**, không kết thúc tại1149. |
| DEV02 Hybrid P1–P3 | c014 p3 `[1143,1421)` | Source spans c014: **`[1350,1661)`, `[1662,1908)`, `[1909,1927)`**. Khoảng được ghi bắt đầu trước chunk và không bao phủ đầy đủ quy định năm3 kỳ. |
| DEV06 Hybrid P1–P4 | `SRC-1 = c084` | Raw: **`SRC-3 = c084`**, SRC-1 là c085. |
| DEV07 Dense P4 | `SRC-4 = c038`, p9 `[1148,1485)` | Raw: **`SRC-1 = c038`**; source span c038 là **p9 `[1307,1682)`**. |

Các sửa DEV08 SRC-3, DEV05 generation omission, số khoản DEV05/DEV06 đã có. Tuy nhiên các source IDs mới ở những hàng khác dường như được dùng chung theo vị trí của mode/case khác; phải ánh xạ theo **từng record**, không đặt source ID cố định cho một chunk trên cả bộ dữ liệu.

Để sửa bằng dữ liệu thật, reviewer đã tạo [DOI_SOAT_EVIDENCE_TASK05_R04.json](DOI_SOAT_EVIDENCE_TASK05_R04.json), chứa:

- Danh sách đầy đủ14 mismatches và24 khoảng sai, kèm mode/case/point/line.
- Với từng chunk được nhắc trong mỗi hàng: full chunk ID, **source ID thực tế trong record**, PDF page, offsets và nguyên văn source spans lấy từ trang chuẩn.
- Các hàng không có nguồn được khai báo vẫn được giữ để người chấm bổ sung căn cứ gold hoặc N/A có lý do. Đây là bản đối soát nguồn, **không tự cấp lại điểm hoặc tự chứng nhận faithfulness**.

Script tạo bản đối soát nằm ở `scratch/review_task05_r04_evidence.py`; chạy bằng Python chuẩn, không import ML hay gọi API. Không điền offsets bằng ước lượng hoặc sửa corpus/raw để khớp rubric. Nên sinh một sidecar evidence chuẩn rồi để rubric dẫn tới thay vì gõ lại từng tọa độ.

## 3. [P2] Còn một SHA bị ghi sai trong lịch sử R02

`BAO_CAO_ANTIGRAVITY.md:631` ghi `9b008ecb25d19e917d057778b665fa1a4e21a201`; `git cat-file -t` không tìm được object này. SHA thật của `9b008ec` là **`9b008ecb252482c4e8ae064d3148cb5dedf0f47e`**, mang thay đổi triển khai Task05-R02. `3c5a93d249300619791d4ba804165d97f6550193` là triển khai Task05-R01; không gọi SHA R02 là commit “cập nhật rà soát” nếu nội dung commit là sửa R02.

Các dòng523c512 bị gán sai vào Task04-R03/R04 và Task05-R01 đã được gỡ; mục R03/R04 trong file Antigravity đã thêm, anchors có đích. Chỉ cần đính chính chính xác dòng R02 và diễn giải vai trò các commit.

## 4. Bước tiếp theo

Tài liệu nhiệm vụ **DNC-RAG-TASK-05-R05**: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R05_CHOT_EVIDENCE_TU_TRACE.md`.

**Chỉ còn chốt evidence/provenance**, không yêu cầu viết lại tests hoặc chạy lại Gemini. Dùng bản đối soát máy đọc được để sửa một lần cho toàn bộ mapping/offsets và kiểm tự động. Nếu chỉ thay tài liệu, không cần lặp lại các tests ML vừa kiểm; giữ rõ giới hạn chưa có kết quả full-suite thật. Không dùng ngôn ngữ “đạt tuyệt đối” cho chất lượng RAG; lỗi claim/omission của outputs cũ vẫn là kết quả thực nghiệm phải giữ.
