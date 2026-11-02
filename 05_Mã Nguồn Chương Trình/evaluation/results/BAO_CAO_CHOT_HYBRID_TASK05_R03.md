# BÁO CÁO KỸ THUẬT CHỐT HYBRID SEARCH, VECTOR INTEGRITY VÀ ĐỐI SOÁT BẰNG CHỨNG (DNC-RAG-TASK-05-R03)

---

## 1. THÔNG TIN ĐỊNH DANH VÀ MÔI TRƯỜNG THỰC THI

- **Project ID:** `dnc-academic-advisor-rag`
- **Tên đề tài:** Xây dựng hệ thống trợ lý ảo hỗ trợ tra cứu quy chế học vụ ứng dụng kỹ thuật Retrieval-Augmented Generation (RAG) (QĐ 580/QĐ-ĐHNCT ngày 02/08/2024).
- **Môn học:** Đồ án 2 — Chuyên ngành Công nghệ thông tin, Trường Đại học Nam Cần Thơ.
- **Thư mục kiểm tra thực tế:** `G:\Other computers\My computer\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`
- **Git Remote Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`)
- **Mã nhiệm vụ / Ticket ID:** `DNC-RAG-TASK-05-R03`
- **Tài liệu rà soát nguồn:** `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R02.md` và `KIEM_TRA_DOC_LAP_TASK05_R02.json` (Codex rà soát ngày 02/11/2026).
- **Phiên bản Python & Thư viện thực tế trong môi trường `.venv`:**
  - Python: **3.14.5** (tags/v3.14.5:5607950, 64-bit) trên Windows.
  - Sentence-Transformers: **6.2.0**
  - ChromaDB: **1.5.9**
  - FastAPI: **0.162.0**
  - Uvicorn: **0.54.0** *(Ghi chú provenance: `requirements.txt` ghi `uvicorn==0.42.0`, nhưng bản cài đặt thực tế trong `.venv` là `0.54.0`; hệ thống giữ nguyên môi trường thực tế, không tự ý hạ/nâng thư viện để làm đẹp số liệu).*
  - PyTorch: **2.15.0**; Transformers: **5.22.1**; NumPy: **2.5.4**
  - Google GenAI SDK: **2.34.0**; Pydantic: **2.14.2**
- **Mã băm kiểm định dữ liệu (Corpus & Artifact Hashes):**
  - Chunks file (`QD580_CHUNKS.jsonl`): `5802f176f1f603123126c49284449085bd18bdf64f3213998e081ecd01536398`
  - Manifest file (`QD580_MANIFEST.json`): `c0ceea3306e71506ceaeae17e8328423993e80967e855c6605d775a64b9c2e9b`
  - Raw A/B JSONL (`DNC_RAG_AB_DEV10_TASK05.jsonl`): `c86b2310e989d3579925bda700dd26f5eadd45571f130493e25f8213d608077f`
  - Raw A/B CSV (`DNC_RAG_AB_DEV10_TASK05.csv`): `1b9733fdd681261335918aa705186fdaaed8ffd8d4f217a4a9c814b08bbf6be6`
  - Tổng số chunk quy chế: Đúng **104 chunks** (baseline v2 sẵn sàng).
  - Model nhúng: `bkai-foundation-models/vietnamese-bi-encoder` (Revision: `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`).

---

## 2. BẢNG ĐỐI CHIẾU XỬ LÝ TOÀN BỘ PHÁT HIỆN TỪ CODEX REVIEW R02

| STT | Mã phát hiện (Codex R02) | Phân loại & Mức độ | Vấn đề kỹ thuật ghi nhận | Biện pháp khắc phục đã triển khai tại R03 | Minh chứng kiểm thử & Artifact đối soát |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | **[P1] Vector Integrity chưa kiểm tra thực tế** | Toàn vẹn dữ liệu & Fail-closed | `check_readiness()` chỉ đối soát metadata collection và file hash; vẫn báo READY khi vector collection rỗng (0 ID) hoặc có cùng số lượng nhưng sai ID (`REPLACED_WRONG_ID`). | Nâng cấp toàn diện `check_readiness()` trong `backend/retrieval.py`:<br>1. Kiểm tra cấu trúc `total_chunks` và danh sách `chunks` trong manifest (bắt buộc số nguyên dương, kiểm tra thiếu/trùng `chunk_id`).<br>2. Kiểm tra đọc từng dòng trong tệp chunks đĩa: xác thực schema JSON, kiểm tra số lượng, trùng lặp và đối soát khớp 100% tập ID với manifest.<br>3. Kiểm tra thực tế trong ChromaDB collection: gọi `col.count()` và `col.get(include=[])`, đối soát số lượng, kiểm tra trùng lặp và so khớp tuyệt đối tập ID thực tế với manifest (`set(col_ids) == set(manifest_ids)`). Mọi sai lệch đều raise `KnowledgeBaseNotReadyError`. | - File mã nguồn: `backend/retrieval.py` (L146-L325).<br>- Suite kiểm thử mới: `tests/test_vector_integrity.py` gồm **10 unit tests** (đúng ID, 0 ID, thiếu ID, dư ID, same-count-wrong-ID, trùng ID, manifest lỗi, chunks lỗi, API health 503).<br>- Chạy qua 10/10 tests trong 0.45s.<br>- Probe của Codex trong `scratch/review_task05_r02_runtime.py` xác nhận: `empty-vector-same-metadata: REJECTED`, `wrong-vector-id-set-same-count: REJECTED`. |
| **2** | **[P2] Rubric sai 8 chunk ID và nhầm lỗi DEV_04** | Liêm chính học thuật & Đánh giá | - Rubric R02 có 8 chunk ID đầy đủ không tồn tại trong corpus (ví dụ `c046`, `c047`, `c067`, `c068`, `c074`, `c075`, `c011`, `c012`).<br>- DEV_04 Dense bị ghi nhận nhầm là lỗi retrieval, trong khi context thực tế đã cấp `c045` ở `SRC-2`.<br>- DEV09-P3 bị đổi nghĩa gold thành khuyên liên hệ. | - Lập file rubric mới `RUBRIC_CHAM_DIEM_DEV10_TASK05_R03.md`, giữ nguyên 20 outputs thô của `DNC_RAG_AB_DEV10_TASK05.jsonl`.<br>- Thay thế toàn bộ bằng Chunk ID thực tế trong corpus: `c044`, `c045`, `c070`, `c071`, `c084`, `c085`, `c014`, `c016`. Script tự động kiểm tra xác nhận **0 invalid chunk refs**.<br>- Sửa phân loại DEV_04 Dense: **Generation Omission** (LLM nhận được context chứa Khoản 3 nhưng bỏ sót khi tổng hợp câu trả lời).<br>- Khôi phục DEV09-P3 đúng nguyên văn gold: nêu rõ phần hỏi rút môn và hoàn phí là chưa đủ căn cứ trong QĐ 580 (khuyên liên hệ là nhận xét thêm). | `05_Mã Nguồn Chương Trình/evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R03.md`.<br>Script kiểm chứng chunk IDs: 13/13 refs hợp lệ 100%. |
| **3** | **[P2] Báo cáo nhầm mẫu số và danh sách test modules** | Tính chính xác khoa học & Provenance | - Báo cáo ghi retrieval 9 ca là DEV01-DEV08 và DEV10 (nhầm DEV09 với DEV10).<br>- Ghi sai tên các module test (`test_chunking.py`, `test_ingestion.py`...).<br>- Khẳng định "seed cố định" thiếu minh chứng.<br>- Chưa phân biệt rõ runner timing với lifespan startup. | - Mẫu số retrieval chuẩn mực là **DEV_01 đến DEV_09** (9 ca), loại trừ **DEV_10** (ngoại vi QĐ 580). DEV_09 có gold evidence để đo retrieval, tính chất multi-turn ghi nhận N/A.<br>- Liệt kê đúng 5 file test methods thực tế trong repo (tổng 80 tests).<br>- Bỏ khẳng định "seed cố định" do SDK không truyền seed parameter.<br>- Nêu rõ metadata lần chạy live: commit `b68811f9...`, dirty=True. Phân tách rõ ràng nạp weights ở startup và thời gian đo lường RAG Engine. | Mục 3, 4, 5 của báo cáo này. |

---

## 3. PHẦN ĐÍNH CHÍNH (ERRATA & PROVENANCE)

1. **Về mẫu số và phân loại ca đánh giá Retrieval:**
   - **Mẫu số đánh giá Retrieval:** Đúng **9 ca (DEV_01 đến DEV_09)**. Ca `DEV_10` được loại khỏi phép đo Retrieval vì là câu hỏi nằm ngoài phạm vi văn bản QĐ 580 (học phí chi tiết từng ngành và điểm rèn luyện).
   - **Đặc thù ca DEV_09:** Câu hỏi mang tính chất tiếp nối lịch sử. Trong đợt chạy độc lập (Single-turn), hệ thống đo lường khả năng truy xuất các căn cứ Điều 7 và Điều 3.4 (đạt độ phủ theo rubric gold). Năng lực hội thoại đa lượt (multi-turn rewrite) được ghi nhận là **N/A** do phiên bản hiện tại chưa xây dựng bộ nhớ đệm hội thoại.
2. **Về danh sách Module kiểm thử tự động:**
   - Trong báo cáo R02 trước đây, danh sách file test bị ghi theo cấu trúc phân rã dự kiến (`test_chunking.py`, `test_ingestion.py`...).
   - **Cấu trúc thực tế trong thư mục `tests/` hiện tại gồm 5 files:**
     1. `test_api_and_rag.py`: **27 test methods** (API endpoints, Lifespan, Mock LLM, Citation verification).
     2. `test_chunking_and_sources.py`: **5 test methods** (Giới hạn token, Source spans, Overlap, Tính bảo toàn cấu trúc).
     3. `test_hybrid_bm25_rrf.py`: **17 test methods** (Vietnamese tokenizer, BM25 Okapi, RRF, Contract, API mode validation).
     4. `test_lifecycle_and_regression.py`: **21 test methods** (Vòng đời ingestion, revision model, evidence whitespace mapping, regression).
     5. `test_vector_integrity.py` *(Mới ở R03)*: **10 test methods** (Vector count/ID match, empty collection, extra/missing ID, wrong ID, manifest/chunks schema, API 503).
     - **Tổng cộng:** **80 test methods**.
3. **Về thông số mô hình và siêu tham số:**
   - Bỏ khẳng định "seed cố định" trong các báo cáo cũ, vì trong cấu hình gọi API `google-genai` hiện tại (`backend/gemini_client.py`), tham số `seed` không được cấu hình trong `types.GenerateContentConfig`. Nhiệt độ (temperature) được thiết lập ở mức $0.0$.
4. **Về Metadata và giới hạn tái lập (Reproducibility):**
   - Đợt chạy thực nghiệm Live 20 requests A/B trên tập phát triển được thực thi tại commit `b68811f9aac8fd0aa479e8410cbaaafafcecc656` với trạng thái `git_dirty = True`. Dữ liệu thô được đóng băng nguyên vẹn tại `DNC_RAG_AB_DEV10_TASK05.jsonl` và `DNC_RAG_AB_DEV10_TASK05.csv` để đối soát, không sinh lại hay sửa đổi kết quả thô.
   - Việc nạp PyTorch model weights diễn ra ở sự kiện `lifespan` startup của FastAPI (hoặc ở lệnh khởi tạo retriever). Thời gian thực thi `timings` trong response chỉ bao gồm thời gian truy vấn nội bộ của hàm `engine.answer_question()`.

---

## 4. KẾT QUẢ ĐỐI SOÁT VÀ CHẤT LƯỢNG RETRIEVAL THỰC NGHIỆM

Bảng đối chiếu chỉ số đo lường độc lập tính toán lại từ thứ hạng và source spans lưu trong `RETRIEVAL_AB_COMPARISON_TASK05.json` trên 9 ca kiểm thử chuẩn mực (**DEV_01 đến DEV_09**):

| Chỉ số đánh giá Retrieval | Dense Retrieval | Hybrid (Dense + BM25 via RRF) | Chênh lệch ($\Delta$) | Ý nghĩa thực tiễn học vụ |
| :--- | :---: | :---: | :---: | :--- |
| **Hit@3** ($\ge 1$ evidence span $\ge 90\%$) | 7 / 9 (77.8%) | **8 / 9 (88.9%)** | +11.1% | Cải thiện khả năng xuất hiện căn cứ ngay ở các vị trí đầu. |
| **Hit@5** ($\ge 1$ evidence span $\ge 90\%$) | 7 / 9 (77.8%) | **9 / 9 (100.0%)** | +22.2% | Cứu vãn thành công 2 ca thất bại hoàn toàn của Dense (DEV_02 và DEV_08). |
| **Full-case Coverage@5** (Tất cả evidence $\ge 90\%$) | 5 / 9 (55.6%) | **6 / 9 (66.7%)** | +11.1% | Tăng số ca thu hồi trọn vẹn mọi mảnh bằng chứng trong Top 5. |
| **Full-case Coverage@10** (Tất cả evidence $\ge 90\%$) | 6 / 9 (66.7%) | **7 / 9 (77.8%)** | +11.1% | Thêm 1 ca bao phủ trọn vẹn toàn bộ các đoạn quy định liên quan. |
| **Mean Evidence Coverage@5** | 63.68% | **80.34%** | **+16.66%** | Tăng đáng kể tỷ lệ dữ kiện quy chế đưa vào ngữ cảnh sinh câu trả lời. |
| **Mean Evidence Coverage@10** | 83.12% | **91.43%** | +8.31% | Đạt ngưỡng bao phủ trên 90% khi mở rộng Top 10. |
| **Mean Reciprocal Rank (MRR@10)** | **0.6806** | 0.6574 | -0.0232 | **Giảm nhẹ:** Giải thuật RRF hòa trộn thứ hạng làm dịch chuyển vị trí tương đối của một số chunk đơn lẻ. |

> **Lưu ý khoa học quan trọng:**
> - Chỉ số **Hit@5 = 9/9 (100%)** của Hybrid Search phản ánh việc mọi câu hỏi đều có ít nhất 1 mảnh căn cứ đạt chuẩn $\ge 90\%$. Điều này **KHÔNG đồng nghĩa** với việc toàn bộ các câu hỏi đều đạt 100% bằng chứng (Full-case Coverage@5 là **6/9 = 66.7%**).
> - Tập phát triển có quy mô nhỏ (10 ca), được dùng để định hình kiến trúc và phát hiện điểm yếu, không đại diện cho độ chính xác suy rộng của toàn bộ hệ thống trên tập dữ liệu lớn cuối kỳ.

---

## 5. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

Toàn bộ hệ thống kiểm thử được thiết kế độc lập, cô lập, có thể chạy offline không cần Internet hay API Gemini:
1. **Bộ kiểm thử tính toàn vẹn Vector Integrity mới (`tests/test_vector_integrity.py`):**
   - Chạy độc lập: `python -m unittest tests/test_vector_integrity.py`
   - Kết quả: **10/10 tests PASS** trong **0.449 giây**.
   - Kiểm chứng đầy đủ: Valid collection, Empty collection (0 vector), Missing ID, Extra ID, Same-count-wrong-ID, Chroma duplicate ID, Manifest schema/duplicate, Chunks file duplicate/mismatch, và API `/health` trả HTTP 503 khi integrity fail.
2. **Bộ kiểm thử Focused Unit Run cô lập (`scratch/review_task05_r02_isolated.py`):**
   - Chạy độc lập với sentinels chặn gọi ML: `python scratch/review_task05_r02_isolated.py`
   - Kết quả: **14/14 tests PASS** trong **0.218 giây**.
3. **Bộ kiểm tra Runtime Probes độc lập (`scratch/review_task05_r02_runtime.py`):**
   - Kết quả: **PASS toàn diện**:
     - `valid-vector`: READY
     - `empty-vector-same-metadata`: REJECTED (KnowledgeBaseNotReadyError)
     - `wrong-vector-id-set-same-count`: REJECTED (KnowledgeBaseNotReadyError)
     - `building`: REJECTED
     - `failed`: REJECTED
     - `missing-chunks`: REJECTED
     - `cache_two_real_temporary_generations`: PASS
     - `engine_sparse_citation_trace_single_retrieval_mode_validation`: PASS
     - `cli_sparse_only_both_entrypoints`: PASS

---

## 6. PHÂN TÍCH RÀ SOÁT CHẤT LƯỢNG CÂU TRẢ LỜI VÀ LỖI HỌC VỤ

Theo bảng rubric chi tiết tại `RUBRIC_CHAM_DIEM_DEV10_TASK05_R03.md`:
1. **Tổng điểm các ý bắt buộc (Mandatory Points):**
   - **Dense:** 25/36 ý ĐẠT (69.4%), 1 ý Một phần, 10 ý Thiếu, 0 ý Sai.
   - **Hybrid:** 28/36 ý ĐẠT (77.8%), 1 ý Một phần, 6 ý Thiếu, **1 ý SAI**.
2. **Phân loại lỗi khách quan:**
   - **DEV_04 (Lỗi Generation Omission ở Dense):** Cả hai mode đều trích xuất được `qd580_v2_c045` vào ngữ cảnh context (`SRC-2`), nhưng mô hình LLM ở chế độ Dense đã bỏ sót quy trình Khoản 3 khi tổng hợp đáp án. Đây là sự thiếu sót của khâu sinh câu trả lời (LLM), không phải lỗi của khâu Retrieval.
   - **DEV_07 (Lỗi Claim Error ở Hybrid):** Mô hình Gemini tự ý nhận định: *"từ điểm D+ trở xuống là dưới 5.0"*, trong khi văn bản quy định D+ là $5.0 - 5.4$. Lỗi này được chấm thẳng thắn là **SAI**, nhấn mạnh tầm quan trọng của cơ chế đối soát trích dẫn ở các chặng tiếp theo.
