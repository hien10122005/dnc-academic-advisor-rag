# Codex rà soát DNC-RAG-TASK-04-R04

- Dự án: `dnc-academic-advisor-rag` — Đồ án 2, Trợ lý học vụ DNC.
- Ngày: 01/11/2026. Commit triển khai và remote main: `b68811f9aac8fd0aa479e8410cbaaafafcecc656`.
- Kết luận: **ĐẠT MỘT PHẦN; cho phép chuyển Task 05 theo hai chặng, sửa các điều kiện đo/robustness trước khi so sánh hybrid.** Baseline dense chạy được; chưa coi toàn bộ yêu cầu R04 đã hoàn tất.

## 1. Kết quả độc lập

- Chạy unittest discovery bằng Python của `.venv`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, key rỗng: **50 test, 0 failure, 0 error, 0 skip**. Riêng idempotency được reviewer chuyển output sang TemporaryDirectory bằng patch để không ghi chunks/manifest gốc; test trong repo vẫn chưa tự cô lập phần này.
- Git sạch trước rà soát, remote main khớp SHA trên; không thay application code hay artifact live trong lần review.
- Xác minh code: public_message được dùng ở API, đường dẫn Windows/POSIX đã có chốt chặn; SDK retry_options attempts=1 ở client/request; ValueError dừng sau một lượt theo test; quota class đã thống nhất HTTP 429; mock handler có is_using_live_api=False; quote ưu tiên span có nội dung.
- Đọc đủ 10 dòng R04: 6 answered, 3 insufficient_evidence, 1 out_of_scope, mỗi dòng lưu 5 retrieved contexts. Toàn bộ citation IDs/chunk IDs khớp context trong artifact. Đây là kiểm tra định danh, không phải chứng minh mọi khẳng định được nguồn hỗ trợ.
- Số liệu R04 tính lại khớp báo cáo: retrieval mean 65.876ms; LLM mean 1916.805ms; total mean 1982.748ms; total median 1769.820ms; bỏ ca đầu total mean 1993.012ms. Không chạy lại live trong lần review này; đánh giá dựa trên artifacts Anti lưu và code thực tế.
- Rubric đã thừa nhận DEV_07 trả lời thiếu/sai nhánh xử lý và DEV_02/08 retrieval miss; tốt hơn R03. DEV_06 có 5 mandatory points trong gold, bảng lại gộp thành 4/4: không đổi kết luận nội dung đủ nhưng cần sửa mẫu số theo gold.

## 2. Phần còn mở đã tái hiện

### [P2] Mã HTTP chuẩn vẫn bị chuỗi message ghi đè

Probe exception có `code=503`, message `upstream unavailable request id 404123`: classify_exception trả `(False, client_error, 503)`. Nhánh dò “404” trong str(exc) chạy trước server branch nên tắt retry nhầm dù mã đã biết. Cần ưu tiên hoàn toàn code/type, bỏ dò số trong message; test thêm code và nội dung mâu thuẫn (401 chứa quota, 503 chứa 404...). Không cần viết lại toàn client.

### [P2] Trace đánh giá chưa phải đầu vào thật của lần sinh

`run_eval_live_r04.py` gọi retriever một lần để lưu contexts, tự dựng user_prompt, rồi engine.answer_question gọi retriever lần nữa và tự dựng prompt lần nữa. Engine thêm `(Trang in: ...)`, prompt lưu trong artifact không có phần này. Vì vậy chưa thể gọi user_prompt lưu là prompt chính xác đã gửi; hai truy xuất giống nhau trên kho ổn định không thay thế được trace từ chính lần generate.

Lần truy xuất ngoài cũng đã nạp model trước lúc engine đo retrieval_ms. Ca đầu 87.48ms không đo cold startup của model. Tổng 1982.748ms là thời gian engine, chưa bao gồm truy xuất ghi log bên ngoài; chưa phải toàn wall-clock runner/API. Cần capture contexts/prompt một lần từ luồng engine, đo bằng monotonic/perf_counter, phân biệt thời gian khởi động, engine và evaluation. Giữ R04 làm kết quả lịch sử có giới hạn, không sửa artifact để giả vờ là trace thật.

Metadata chỉ lưu HEAD a72369d cũ trong khi code R04 chưa commit; chưa có dirty flag/source hash, corpus/chunks hash hoặc runtime generation config đầy đủ. HEAD trước thay đổi là hợp lệ để ghi nhưng chưa đủ tái lập. Lần chạy mới cần định danh code thực chạy và cấu hình.

### [P2] Chưa có chấm từng ý bằng chứng và chính sách public message còn theo heuristic

Báo cáo đã có nhận xét theo ca, chưa có file chấm từng mandatory point với câu trả lời/nguồn và người/agent chấm. DEV_07 nói phải học lại nhưng nguồn được cite chỉ hỗ trợ điểm không đạt/tích lũy; phải ghi lỗi faithfulness riêng, không chỉ thiếu ý. “0% citation IDs ngoài context” không đồng nghĩa “0% nguồn dẫn sai nội dung” hoặc 0 hallucination.

DNCError hiện cho phép message không chứa slash/file extension đi thẳng ra public. Probe `KnowledgeBaseNotReadyError('provider error token=FAKE_SECRET_SENTINEL')` trả nguyên sentinel qua public_message. Không dùng secret thật trong probe. Do đó chưa có căn cứ tuyên bố đã lọc token bí mật. Ưu tiên public message ổn định theo code/class cho lỗi hạ tầng, chi tiết chẩn đoán ở internal_detail; log dùng thông tin có kiểm soát, không dump payload/key. Đây là sửa gọn của đường lỗi, không yêu cầu xây hệ thống bảo mật mới.

## 3. Quyết định chuyển bước

Không yêu cầu tối ưu hết 10 câu để chốt dense. Cho phép Task05 **chặng A** sửa các điểm nhỏ trên và đóng băng baseline/trace đúng; sau đó **chặng B** bổ sung BM25 + RRF và so sánh công bằng dense/hybrid trên cùng corpus, prompt và cấu hình. Giữ lỗi DEV_02/07/08 làm phân tích đối chứng, không hardcode nguồn/gold. Chưa triển khai UI, admin, multi-turn hay reranker trong nhiệm vụ này.

Nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_HYBRID_BM25_RRF.md`.
