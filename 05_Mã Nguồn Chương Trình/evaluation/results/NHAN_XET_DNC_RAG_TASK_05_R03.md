# Codex rà soát DNC-RAG-TASK-05-R03

Ngày kiểm tra: **02/11/2026**, giờ Việt Nam. Project: `dnc-academic-advisor-rag`.

**Kết luận: CẦN SỬA có giới hạn, tập trung tests và bằng chứng.** Lỗi production P1 về vector integrity của R02 đã được khắc phục trong các probe độc lập. Chưa nghiệm thu Task05 vì fixture readiness cũ không còn hợp lệ, rubric còn sai vị trí nguồn/nguyên nhân và lịch sử bàn giao bị gán nhầm commit. Không cần làm lại BM25/RRF hoặc nới guard production.

## 1. Phiên bản và phạm vi

- HEAD/remote main được kiểm tra: **`a372d5b9df3146c788533e11fe71095418dd8eb7`**; commit triển khai R03: `523c5126d65749574fc21f79978b58932ff80e1a`.
- Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`. Checkout ở `G:\Other computers\My computer\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`.
- Khi bắt đầu, báo cáo kỹ thuật và rubric R03 đã có thay đổi local: mỗi file thêm một dòng trống cuối file. Giữ nguyên các thay đổi này; không quy chúng cho lượt review.
- Đọc code/diff/nhiệm vụ R03 và toàn bộ rubric, đối chiếu 20 raw records và source spans. Không sửa code, tests, corpus/gold/raw outputs hay `.env`; không gọi Gemini, không ghi DB thật, không commit/push.

## 2. Xác minh độc lập

| Kiểm tra | Kết quả |
| --- | --- |
| File mới `tests.test_vector_integrity` | **10/10 qua**, 0.466 giây. Chính module test dùng ML imports giả toàn tiến trình; kết quả là unit tests với fake collection, không phải Chroma/ML integration thật. |
| Focused BM25/RRF/API | **14/14 qua**, 0.190 giây, dùng runner R02 với fail-on-use ML sentinels. |
| Probe runtime R02 chạy lại trên R03 | Valid vector READY; empty/same-count-wrong-ID **REJECTED**, có gọi `count/get`; BUILDING/FAILED/missing chunks đều REJECTED. Cache hai thế hệ, engine trace/single retrieval và hai CLI sparse-only tiếp tục qua. |
| Readiness regression cũ | Chạy nguyên class `TestRetrieverReadinessVerification` (giữ nguyên AST bodies) với production retriever import bình thường, fake Chroma có semantics collection tạo mới rỗng và mock embedding setup: **12 tests, 7 qua, 3 failures, 2 errors**. Đây là probe cô lập, không phải kết quả toàn suite 80 tests. |
| Full-suite attempt | Khởi chạy discover offline/key rỗng và traceback định kỳ; vẫn ở dependency imports trên ổ đồng bộ, dừng lúc **16:05:20**. **Chưa có kết quả toàn suite 80 tests**; không tính số methods là số tests qua. |
| Corpus/raw outputs | SHA-256 chunks, manifest, raw JSONL và CSV giữ nguyên so với review R02. Không chạy lại LLM/embedding A/B. |
| Rubric references | 72 hàng (36/mode); không còn full chunk ID không tồn tại; các full refs nằm trong context của đúng record. Vẫn có một source-ID mapping sai và mô tả điều/khoản/thiếu nguồn không đúng, xem dưới. |

Artifact: [KIEM_TRA_DOC_LAP_TASK05_R03.json](KIEM_TRA_DOC_LAP_TASK05_R03.json). Logs local được Git ignore: `scratch/review_task05_r03_integrity.log`, `review_task05_r03_focused.log`, `review_task05_r03_runtime.log`, `review_task05_r03_regression.log`, `review_task05_r03_suite.log`. Probe regression tái chạy từ thư mục mã nguồn:

```powershell
.\.venv\Scripts\python.exe -u -X utf8 ..\scratch\review_task05_r03_regression.py
```

Probe này thay Chroma và embedding setup để bỏ bước import ML; không sửa thân setUp/test gốc và không thay logic retriever. File integrity chạy riêng bằng `python -m unittest tests.test_vector_integrity -v`. Phiên bản Python thực tế lượt này là **3.14.5**, khớp báo cáo R03; khác interpreter ghi ở review R02, không sửa dữ liệu môi trường lịch sử thành số của lượt hiện tại.

## 3. Các điểm cần sửa

### [P2] Fixture regression chưa theo hợp đồng integrity mới; có 5 ca hỏng

Vị trí: `tests/test_lifecycle_and_regression.py:254–278` và các tests của `TestRetrieverReadinessVerification`.

`valid_manifest` cũ không có `chunks`, trong khi R03 bắt buộc danh sách ID hợp lệ. Collection mẫu được `create_collection()` nhưng không nạp `c1`; một kho hợp lệ phải có đúng ID đó. Với guard mới, cả hai fixture đều không thể là trạng thái READY hợp lệ.

Probe 12 ca ghi nhận:

- **2 errors:** `test_valid_preflight_passes`, `test_cache_invalidation_when_status_changes_to_building` — lỗi ngay từ lần READY ban đầu với thông báo `Danh sách 'chunks' ... (0 vs 1)`.
- **3 failures:** `test_reject_mismatched_fingerprint`, `test_reject_chroma_metadata_mismatch`, `test_reject_disk_chunk_hash_mismatch` — bị chặn bởi manifest thiếu danh sách chunks trước khi tới lỗi mà test định kiểm.
- Một số negative tests vẫn qua nhưng có thể qua nhờ guard sớm khác nguyên nhân dự định; cần bảo đảm mỗi ca chỉ gây lỗi mục tiêu trên nền fixture hợp lệ.

**Sửa fixture, giữ guard:** bổ sung danh sách manifest đúng, tạo record `c1` với embedding giả xác định trong DB tạm hoặc fake tương ứng; chạy riêng class và full suite. Không đổi test thành chấp nhận bất kỳ exception nào để che sai nguyên nhân.

Ngoài ra, `tests/test_vector_integrity.py:36–49` tự cài `chromadb` và `sentence_transformers` giả vào `sys.modules` nếu chưa import và không restore; thứ tự nạp test có thể quyết định module thật/giả được dùng ở các nhóm khác. Chuyển việc cô lập ML sang runner riêng hoặc dùng cơ chế dependency injection/cleanup rõ ràng. Không để full-suite integration vô tình dùng MagicMock toàn cục.

### [P2] Rubric còn sai source ID, vị trí điều khoản và phân loại omission

Vị trí: `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R03.md`, các mục DEV05, DEV06 và DEV08.

- **DEV08 Hybrid P1:** ghi `c035` là **SRC-2**, nhưng raw record có **SRC-3 = c035**; SRC-2 là `qd580_v2_c087_reg_d26_p21_6790bf08`. Chunk ID tồn tại chưa đủ để xác nhận source mapping đúng.
- **DEV05 P3 của cả hai mode:** rubric nói phí thi lại không nằm trong context. Thực tế cả hai có **SRC-1 = `qd580_v2_c070_reg_d18_p16_a1e5934a`**, chứa đầy đủ nghĩa vụ đóng lệ phí và ngoại lệ hoãn thi; span **PDF p17 `[0,282)`**. Answer bỏ sót ý này nên nhãn THIẾU có thể giữ, nhưng nguyên nhân là **generation omission**, không phải retrieval miss.
- **DEV05 P1/P2:** c071 chứa giới hạn D+/C+ tại **Điều 18 khoản 6**, c070 chứa nhóm không tổ chức thi lại/lệ phí tại **khoản 5** (không phải khoản 4/3 như rubric ghi). c070 nối trang 16–17, không chỉ trang 16.
- **DEV06 P5:** ngưỡng 5.5 nằm tại **Điều 25 khoản 2**, PDF p21 `[90,160)`; không phải “khoản 1 điểm d”. **DEV06 P4:** c084 chứa nội dung nối trang, phần chuẩn đầu ra ngoại ngữ/CNTT nằm ở PDF p21 `[0,89)`, nên dẫn riêng p20 không đầy đủ. Điểm ĐẠT nội dung không tự động bị đổi vì lỗi định vị, nhưng phải sửa evidence đúng.
- Rubric R03 chưa cung cấp offsets cụ thể cho từng căn cứ dù mục đích đầu file ghi có source spans. Bổ sung bảng evidence/sidecar liên kết mode/case/point -> source ID/chunk/page/offset, hoặc ghi span trực tiếp; N/A có lý do cho hành vi từ chối.

DEV04 generation omission và DEV09-P3 đã sửa đúng. DEV06 giữ 5 ý; DEV07 giữ nhận định D+ sai và thiếu nhánh thi phụ/điều kiện học lại. Các tổng 25/36 và 28/36 khớp số nhãn, nhưng không dùng chúng để tuyên bố evidence đã được kiểm hoàn chỉnh khi còn các lỗi trên.

### [P2] Bàn giao gán commit R03 cho lượt lịch sử và thiếu mục báo cáo R03

Vị trí: `BAO_CAO_BAN_GIAO.md:228,260,292`; `BAO_CAO_ANTIGRAVITY.md:631` và liên kết “Báo cáo mới nhất”.

- Diff từ `9b008ec` cho thấy SHA **523c512...** được chèn vào các lượt Task04-R03, Task04-R04, Task05-R01 trong bàn giao; file Antigravity còn ghi SHA này vào mục Task05-R02. Đây là commit triển khai **Task05-R03**, không phải commit thực hiện các lượt cũ. Các mục cũ giờ có thể chứa cả SHA mới lẫn SHA lịch sử, gây sai provenance.
- File Antigravity đổi “Báo cáo mới nhất” thành R03 nhưng **không thêm heading/mục R03** ở lịch sử; anchor `#dnc-rag-task-05-r03--doi-soat-vector-va-hoan-thien-rubric-bang-chung` không có đích. Báo cáo kỹ thuật R03 tồn tại, nhưng link bàn giao vào file này đang hỏng.

Khôi phục các thay đổi SHA bị gán sai bằng đối chiếu Git, giữ các SHA lịch sử đã có; thêm mục R03 riêng và errata có ngày. Không dùng replace toàn cục trường “Commit triển khai”. Reviewer không sửa lời tự báo lịch sử trong lượt này.

## 4. Quyết định tiếp theo

Giao **DNC-RAG-TASK-05-R04** tại `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R04_CHOT_TESTS_VA_BANG_CHUNG.md`.

Phạm vi còn lại là fixture/test isolation và sửa bằng chứng/bàn giao; không yêu cầu thay thuật toán retrieval hoặc sinh lại 20 outputs. Sau khi regression qua và tài liệu truy nguyên đúng mới nghiệm thu Task05 để xét Task06. Lỗi production P1 đã đóng trong probe kiểm tra, không mở lại chỉ vì fixture cũ hỏng.
