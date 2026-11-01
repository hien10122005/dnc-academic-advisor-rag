# BÁO CÁO KỸ THUẬT CHỐT HYBRID SEARCH VÀ BẰNG CHỨNG THỰC NGHIỆM (DNC-RAG-TASK-05-R02)

---

## 1. THÔNG TIN ĐỊNH DANH VÀ MÔI TRƯỜNG THỰC THI

- **Project ID:** `dnc-academic-advisor-rag`
- **Tên đề tài:** Trợ lý tra cứu quy chế học vụ Đại học Nam Cần Thơ ứng dụng RAG (QĐ 580/QĐ-ĐHNCT ngày 02/08/2024).
- **Môn học:** Đồ án 2 — Chuyên ngành Công nghệ thông tin, Trường Đại học Nam Cần Thơ.
- **Thư mục gốc (Root):** `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`
- **Git Remote Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git`
- **Mã nhiệm vụ / Ticket ID:** `DNC-RAG-TASK-05-R02`
- **Phiên bản Python & Thư viện thực tế:**
  - Python: **3.14.6 (64-bit)** trên hệ điều hành Windows.
  - Sentence-Transformers: 5.1.2.
  - ChromaDB: 1.5.0.
  - FastAPI: 0.128.0; Uvicorn: 0.40.0.
- **Mã băm kiểm định dữ liệu (Corpus Hashes):**
  - Chunks file (`chunks.jsonl`): `5802f176f1f603123126c49284449085bd18bdf64f3213998e081ecd01536398`
  - Manifest file (`manifest.json`): `c0ceea3306e71506ceaeae17e8328423993e80967e855c6605d775a64b9c2e9b`
  - Tổng số chunk quy chế: Đúng **104 chunks** (baseline v2 sẵn sàng).
  - Model nhúng: `bkai-foundation-models/vietnamese-bi-encoder` (Revision: `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`).

---

## 2. BẢNG ĐỐI CHIẾU XỬ LÝ TOÀN BỘ PHÁT HIỆN TỪ CODEX REVIEW R01

| STT | Mã phát hiện (Codex) | Phân loại & Mức độ | Vấn đề kỹ thuật ghi nhận | Biện pháp khắc phục đã triển khai | Minh chứng kiểm thử & Artifact đối soát |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | **[P1] BM25 cache & preflight missing chunks** | An toàn dữ liệu & Fail-closed | - Cache BM25 không so sánh fingerprint mới sau readiness.<br>- `check_readiness` bỏ qua kiểm tra hash khi file chunks không tồn tại. | - Thêm bước đối chiếu `self._bm25_index.indexed_fingerprint != readiness['corpus_fingerprint']` trên mỗi lượt truy cập property `bm25_index`. Nếu khác, tự động hủy cache và tái tạo sạch sẽ.<br>- Bổ sung tiền kiểm tra `chunks_file_path.exists()` trong `check_readiness()`: nếu thiếu, raise `KnowledgeBaseNotReadyError` ngay lập tức (fail-closed tuyệt đối). | - `test_retriever_check_readiness_fail_closed_missing_chunks`<br>- `test_bm25_cache_invalidation_on_fingerprint_change`<br>- `test_missing_chunks_file_raises_error`<br>- `test_duplicate_chunk_ids_raises_error`<br>- `test_manifest_id_set_mismatch_raises_error` |
| **2** | **[P2] Test API isolation** | Kiểm thử & Độ độc lập | `test_api_chat_endpoint_mode_validation` chạy đơn lẻ bị HTTP 503 do `rag_engine_instance` chưa được khởi tạo qua lifespan. | Thiết lập fixture `setUp` inject mock `RAGEngine` trả về `RAGResponse` chuẩn và `tearDown` khôi phục `main_module.rag_engine_instance` nguyên vẹn sau mỗi test case. | `test_api_chat_endpoint_mode_validation` chạy độc lập thành công 100%, không phụ thuộc thứ tự chạy test suite. |
| **3** | **[P2] RRF Contract & Nullable scores** | Chuẩn hóa API & CLI | - Hit chỉ xuất hiện ở sparse bị thiếu `rank` sau fusion (phải là 1..k).<br>- `similarity` bị gán giả 0.0 thay vì nullable.<br>- Thiếu trường `distance` và `is_cross_page` làm CLI có nguy cơ KeyError. | - Sau khi xếp hạng RRF, gán lại `item["rank"] = 1..k` cho danh sách kết quả.<br>- Với sparse-only hits: `similarity = None`, `distance = None` (nullable chân thực).<br>- Tự động suy diễn `is_cross_page = (start_pdf != end_pdf)` nếu thiếu.<br>- Cập nhật schema Pydantic `CitationModel`: `similarity: Optional[float] = None`. | - `test_rrf_sparse_only_contract`<br>- `test_rrf_hand_calculated_example`<br>- `test_rrf_sparse_only_can_rank_before_dense_only` |
| **4** | **[P2] Engine trace thiếu candidate scores** | Khả năng quan sát (Observability) | `return_trace=True` trong RAGEngine bỏ sót điểm số từng luồng (`dense_rank`, `dense_score`, `bm25_rank`, `bm25_score`, `rrf_score`) và cấu hình fusion. | - Mở rộng dataclass `SourceContext` hỗ trợ đầy đủ các trường điểm số.<br>- Bổ sung trường `fusion_config: {"dense_top_k": 20, "bm25_top_k": 20, "rrf_k": 60, "final_k": k}` khi `mode == "hybrid"` trong trace.<br>- Lưu trữ tách bạch điểm từng luồng trong `retrieved_contexts`. | File mã nguồn `backend/rag_engine.py` (L62-L100, L375-L405). |
| **5** | **[P1/P2] Đánh giá sai sót DEV_07 & Lập Rubric** | Liêm chính học thuật & Đánh giá | - Hybrid ở DEV_07 sinh nhận định sai: *"từ điểm D+ trở xuống là dưới 5.0"* (trong khi D+ là 5.0 - 5.4).<br>- Báo cáo cũ chưa lập bảng rubric từng ý bắt buộc cho 20 records. | - Không sửa dữ liệu thô `DNC_RAG_AB_DEV10_TASK05.jsonl` (giữ nguyên tính khách quan).<br>- Lập file rubric độc lập `RUBRIC_CHAM_DIEM_DEV10_TASK05.md` chấm chi tiết từng ý của 20 lượt chạy.<br>- Chấm thẳng thắn ý DEV07-P1 của Hybrid là **SAI (Claim Error)**. | `05_Mã Nguồn Chương Trình/evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05.md`. |
| **6** | **[P2] Đính chính Errata & Provenance** | Tính chính xác khoa học | - Đính chính SHA bàn giao bị gõ nhầm.<br>- Sửa giải thích R04: nạp PyTorch weights diễn ra ở khởi tạo retrieval, ngoài engine timing.<br>- Mô tả đúng cơ chế nạp BM25 (đã bổ sung `preload_bm25()` ở startup).<br>- Diễn giải đúng Hit@5: $\ge 1$ evidence $\ge 90\%$, không phải 100% mọi evidence. | Ghi nhận chi tiết trong Mục 3 và Mục 4 của báo cáo này. | Mục 3 & 4 dưới đây. |

---

## 3. PHẦN ĐÍNH CHÍNH (ERRATA)

1. **Đính chính Commit SHA bàn giao ở Task05-R01:**
   - *Báo cáo tự ghi:* `3c5a93d11b339ae780c1081aee3480ec8e77ce0b`
   - *Commit SHA thực tế trên Git repo:* `3c5a93d249300619791d4ba804165d97f6550193`
   - *Nguyên nhân:* Nhầm lẫn ký tự khi sao chép chuỗi băm trong lời nhắn bàn giao.
2. **Đính chính giải thích độ trễ khởi động PyTorch (Errata R04 & Task05):**
   - Trong báo cáo R04/Task05 trước đây có đoạn nhận định độ trễ lượt đầu tăng cao là do engine nạp weights PyTorch.
   - *Đính chính chuẩn xác:* Việc nạp weights mô hình Sentence-Transformers diễn ra ở tầng `VectorRetriever` trong quá trình khởi tạo ứng dụng (lifespan startup). Khoảng thời gian đo lường của RAG Engine chỉ tính từ lúc tiếp nhận câu hỏi; do đó, sự biến thiên thời gian ở lượt đầu là do cơ chế warm-up tính toán vector nội bộ của PyTorch/CPU và độ trễ kết nối mạng lần đầu tới máy chủ Gemini, không phải do nạp weights trong hàm engine.
3. **Đính chính cơ chế nạp BM25 Index:**
   - Ở Task05-R01, BM25 Index thực tế được nạp lazy tại request đầu tiên truy vấn hybrid.
   - Ở Task05-R02, hệ thống đã chính thức bổ sung phương thức `retriever.preload_bm25()` vào sự kiện `lifespan` startup của FastAPI (`backend/main.py`), bảo đảm cả mô hình Vector và chỉ mục BM25 đều được nạp sẵn sàng 100% vào bộ nhớ RAM trước khi tiếp nhận request.
4. **Đính chính cách hiểu về chỉ số Hit@5 và MRR:**
   - Chỉ số **Hit@5 = 9/9 (100%)** của Hybrid Search có nghĩa là: **100% trong số 9 ca kiểm thử có ít nhất một đoạn trích dẫn (evidence span) đạt độ phủ $\ge 90\%$ trong Top 5**.
   - Chỉ số này **KHÔNG đồng nghĩa** với việc toàn bộ các bằng chứng của 9 ca đều được tìm thấy đầy đủ 100%, và **KHÔNG đồng nghĩa** với độ chính xác tuyệt đối của câu trả lời.
   - Độ phủ trung bình thực tế (Mean evidence coverage@5) đạt **80.34%** (so với 63.68% của Dense).
   - Chỉ số **MRR@10 giảm nhẹ** từ $0.6806$ (Dense) xuống $0.6574$ (Hybrid), do việc dung hợp RRF giữa hai danh sách thứ hạng làm dịch chuyển vị trí tương đối của một số chunk đơn lẻ.

---

## 4. KẾT QUẢ ĐỐI SOÁT VÀ CHẤT LƯỢNG RETRIEVAL THỰC NGHIỆM

Bảng đối chiếu chỉ số đo lường độc lập trên 9 ca phát triển có căn cứ (DEV_01 đến DEV_08 và DEV_10; DEV_09 là câu hỏi thiếu căn cứ kiểm tra fallback):

| Chỉ số đánh giá Retrieval | Dense Retrieval | Hybrid (Dense + BM25 via RRF) | Chênh lệch ($\Delta$) | Ý nghĩa thực tiễn học vụ |
| :--- | :---: | :---: | :---: | :--- |
| **Hit@3** ($\ge 1$ evidence span $\ge 90\%$) | 7 / 9 (77.8%) | **8 / 9 (88.9%)** | +11.1% | Cải thiện khả năng xuất hiện căn cứ ngay ở các vị trí đầu. |
| **Hit@5** ($\ge 1$ evidence span $\ge 90\%$) | 7 / 9 (77.8%) | **9 / 9 (100.0%)** | +22.2% | Cứu vãn thành công 2 ca thất bại hoàn toàn của Dense (DEV_02 và DEV_08). |
| **Mean Evidence Coverage@5** | 63.68% | **80.34%** | **+16.66%** | Tăng đáng kể tỷ lệ dữ kiện quy chế đưa vào ngữ cảnh sinh câu trả lời. |
| **Mean Evidence Coverage@10** | 83.12% | **91.43%** | +8.31% | Đạt ngưỡng bao phủ trên 90% khi mở rộng Top 10. |
| **Full-case Coverage@10** (100% evidence $\ge 90\%$) | 6 / 9 (66.7%) | **7 / 9 (77.8%)** | +11.1% | Thêm 1 ca bao phủ trọn vẹn toàn bộ các đoạn quy định liên quan. |
| **Mean Reciprocal Rank (MRR@10)** | **0.6806** | 0.6574 | -0.0232 | Giảm nhẹ do giải thuật RRF làm cân bằng lại vị trí các chunk đồng hạng. |

---

## 5. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

Toàn bộ hệ thống được kiểm thử hoàn toàn độc lập, môi trường cô lập, offline, không phụ thuộc kết nối Internet hay API Gemini:
- **Lệnh thực thi kiểm thử toàn diện:**
  `.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"`
- **Kết quả kiểm thử:**
  `Ran 70 tests in 53.476s. OK!`
  - `test_chunking.py`: 12 tests PASS.
  - `test_ingestion.py`: 11 tests PASS.
  - `test_retrieval.py`: 15 tests PASS.
  - `test_rag_engine.py`: 15 tests PASS.
  - `test_hybrid_bm25_rrf.py`: **17 tests PASS** (bổ sung đầy đủ 7 test cases mới cho R02).

---

## 6. PHÂN TÍCH RÀ SOÁT CHẤT LƯỢNG CÂU TRẢ LỜI VÀ LỖI DEV_07

Theo bảng rubric chi tiết tại `RUBRIC_CHAM_DIEM_DEV10_TASK05.md`:
1. **Tổng điểm các ý bắt buộc (Mandatory Points):**
   - **Dense:** 25/36 ý ĐẠT (69.4%), 1 ý Một phần, 10 ý Thiếu, 0 ý Sai.
   - **Hybrid:** 28/36 ý ĐẠT (77.8%), 1 ý Một phần, 6 ý Thiếu, **1 ý SAI**.
2. **Nguyên nhân và bài học từ lỗi DEV_07 ở Hybrid:**
   - *Phát ngôn sai của mô hình:* `"học phần có điểm tổng kết đạt từ 5.0 trở lên (từ điểm D+ trở xuống là dưới 5.0) mới được tính là học phần tích lũy"`.
   - *Bản chất lỗi:* Mặc dù bảng quy đổi trích xuất được thể hiện đúng $D+ = 5.0 - 5.4$, LLM đã nhầm lẫn khi tự diễn giải câu chữ, gộp D+ vào nhóm dưới 5.0.
   - *Xử lý liêm chính:* Hệ thống ghi nhận đây là lỗi **SAI** của LLM, không lấp liếm bằng việc câu kết luận sau vẫn khuyên sinh viên học lại. Điều này khẳng định sự cần thiết của các kỹ thuật xác thực câu chữ (claim validation) và cơ chế Reranker tái cấu trúc ngữ cảnh trong các bước phát triển tiếp theo.

---

## 7. KẾT LUẬN VÀ KIẾN NGHỊ BÀN GIAO

- **Chế độ mặc định của hệ thống:** Tiếp tục duy trì `mode="dense"` làm mặc định cho API và CLI để bảo đảm tính tương thích ngược tuyệt đối; kích hoạt `mode="hybrid"` khi client hoặc người dùng yêu cầu rõ ràng.
- **Tính khả thi của Hybrid Search:** Hybrid Search chứng minh sự vượt trội rõ rệt về độ phủ dữ kiện quy chế (tăng từ 63.68% lên 80.34%), giải quyết các truy vấn mang nặng từ khóa điều khoản như DEV_02 và DEV_08.
- **Giới hạn phạm vi nhiệm vụ:** Nhiệm vụ 05-R02 hoàn thành toàn diện việc chốt hạ kỹ thuật Hybrid và kiểm định thực nghiệm, bảo đảm mã nguồn sạch, fail-closed an toàn, tests độc lập. Chưa triển khai Cross-Encoder Reranker, UI, SQLite, hay Multi-turn trong lượt này.
