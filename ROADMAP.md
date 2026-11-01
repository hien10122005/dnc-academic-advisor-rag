# ROADMAP.md — Kế hoạch thực hiện và nhật ký tiến độ

> Cập nhật: **31/10/2026**. Đọc `PROJECT.md` để biết phạm vi đã thống nhất; `LOGIC.md` để biết đặc tả xử lý và đánh giá.
> Checklist đánh dấu hoàn thành chỉ khi có sản phẩm hoặc minh chứng. Lịch dưới đây là kế hoạch, không phải xác nhận tiến độ. Không suy ra phần trăm hoàn thành từ việc đã có thư mục.

## 1. Trạng thái hiện tại và kế thừa lịch sử

### Đã quan sát trực tiếp trong thư mục

- [x] Có 3 tài liệu PDF gốc trong thư mục dữ liệu.
- [x] Có 6 file Markdown đã chuẩn bị, bao phủ 6 nhóm nội dung.
- [x] Có 3 tài liệu mô tả, logic và roadmap; đã cập nhật theo phương án giảm tải ngày 31/10/2026.
- [x] Có cấu trúc thư mục backend, frontend, chroma_db và notebooks.
- [x] Có mã nguồn chạy được: Đã thiết lập môi trường phân lập `.venv` (Python 3.14.6) và hoàn thiện các module cốt lõi `backend/config.py`, `backend/chunking.py`, `backend/ingestion.py`, `backend/retrieval.py`, `evaluation/evaluate_retrieval.py` ngày 31/10/2026.
- [x] Có kết quả ingestion, benchmark hoặc demo thực tế: Đã nạp thành công 70 chunks QĐ 580 vào ChromaDB collection `qd580_baseline_a`, chạy thử nghiệm và xuất báo cáo tại `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_BASELINE_VECTOR_QD580.md` ngày 31/10/2026.

### Thông tin kế thừa từ roadmap cũ

Bản cũ đánh dấu đã liên hệ giảng viên, ghi phản hồi và thu thập/làm sạch dữ liệu; nhật ký ghi ngày 25/10/2026. Các trường ngày gặp, phản hồi và tên đề tài được duyệt còn để trống. Trong thư mục biên bản được kiểm tra chưa thấy file, vì vậy không tự xác nhận việc gặp hoặc duyệt đề tài đã hoàn tất; giữ là thông tin cần bổ sung minh chứng, không kết luận chưa từng liên hệ.

Bản cũ ghi giai đoạn chuẩn bị 65% và dữ liệu chính xác 100%. Bản hiện tại thay bằng đầu ra kiểm tra được: đã có file dữ liệu, còn phải đối chiếu nguồn và ánh xạ trang. Bản gốc đầy đủ được lưu trong ZIP tại `scratch/document_backups/` trước khi cập nhật.

Bản Word `03_Đề Cương & Báo Cáo/01_Đề Cương Chi Tiết/TÀI LIỆU DỰ ÁN.docx` là tài liệu đã có; nội dung chưa được đồng bộ trong lần sửa Markdown này.

## 2. Bảng tiến độ tổng quan

| Tuần | Thời gian | Đầu ra chính | Trạng thái ngày 31/10 |
| --- | --- | --- | --- |
| 1 | 26/10–01/11/2026 | Chốt phạm vi, đề cương, môi trường và kế hoạch kiểm chứng dữ liệu | Đã chuẩn bị; hoàn thành kiểm chứng dữ liệu QĐ 580 và thiết lập môi trường |
| 2 | 02/11–08/11 | Ingestion có nguồn, vector search chạy thử; lập bộ đánh giá nháp | Đã có minh chứng thực tế: Pipeline chunking v2.0 (104 chunks), collection qd580_baseline_v2, 5 bài test tự động đạt 100%, bộ đánh giá nghiêm ngặt (Hit@10 100%, MRR 0.6806) |
| 3 | 09/11–15/11 | RAG cơ bản qua FastAPI, citation và luồng thiếu căn cứ | Đã hoàn thành nghiệm thu Nhiệm vụ 04 (01/11/2026): FastAPI /health & /chat, Preflight đối soát 3 chiều, Gemini Client đa chế độ, RAG Engine lọc hallucinated citation, CLI tra cứu, 35/35 test đạt 100%. Phần đánh giá chất lượng LLM thực tế chờ cấu hình GEMINI_API_KEY |
| 4 | 16/11–22/11 | Giao diện, hybrid search, reranking và hội thoại giới hạn | Chưa có minh chứng thực hiện |
| 5 | 23/11–29/11 | Admin tối giản, đủ dữ liệu đã kiểm chứng, chốt bộ đánh giá | Chưa có minh chứng thực hiện |
| 6 | 30/11–06/12 | So sánh A/B/C, phân tích lỗi, sơ đồ và minh chứng demo | Chưa có minh chứng thực hiện |
| 7 | 07/12–13/12 | Hoàn thiện Chương 1–2 từ ghi chép và nguồn tham khảo | Chưa có minh chứng thực hiện |
| 8 | 14/12–20/12 | Hoàn thiện Chương 3–4, kết quả và kiểm thử | Chưa có minh chứng thực hiện |
| 9 | 21/12–27/12 | Hoàn chỉnh báo cáo, nhận góp ý và đóng băng bản bàn giao | Chưa có minh chứng thực hiện |
| 10 | 28/12/2026–03/01/2027 | Slide, diễn tập, kiểm tra cài đặt, đóng gói và in | Chưa có minh chứng thực hiện |
| Nộp | 04/01–10/01/2027 | Nộp theo thông báo chính thức và xác nhận đã nhận | Kế thừa lịch cũ; cần đối chiếu |

Ưu tiên phần mềm và minh chứng trong 6 tuần đầu, nhưng ghi chép báo cáo ngay khi làm. Mỗi tuần dành thời gian xử lý lỗi và tổng kết; nếu chậm, giảm phần trang trí/hosting trước, không bỏ kiểm chứng nguồn và thực nghiệm.

## 3. Tuần 1 — Chốt phạm vi và nền tảng

- [ ] Xác nhận tên đề tài/phạm vi với giảng viên; bổ sung nội dung liên hệ đã được roadmap cũ đánh dấu.
- [ ] Viết hoặc sửa đề cương ngắn: bài toán, mục tiêu, 6 nhóm dữ liệu, chức năng giảm tải, phương pháp đánh giá, đầu ra và lịch.
- [ ] Ghi rõ người tra cứu không đăng nhập, chỉ admin có tài khoản; không lưu hội thoại lâu dài.
- [x] Kiểm tra Python và chọn phiên bản tương thích; tạo venv trong thư mục mã nguồn (minh chứng: môi trường ảo `.venv` phân lập tại `05_Mã Nguồn Chương Trình/.venv` ngày 31/10/2026).
- [x] Chọn phiên bản thư viện chạy được và tạo `requirements.txt`, `.gitignore`, `.env.example` không chứa bí mật (minh chứng: `requirements.txt`, `.gitignore`, `.env.example`, `README.md` tại `05_Mã Nguồn Chương Trình/` ngày 31/10/2026).
- [x] Thử kết nối Gemini; chọn tên mô hình/SDK còn dùng được và ghi vào cấu hình, chưa mặc định model cũ (minh chứng: SDK `google-genai` mới, mô hình `gemini-3.5-flash-lite` phản hồi nhanh ~1.4s, cấu hình qua `GEMINI_MODEL` ngày 01/11/2026).
- [x] Lập danh mục 3 PDF và 6 Markdown: nguồn, trạng thái đối chiếu, trang, điều/mục, phạm vi áp dụng và vấn đề cần xử lý (minh chứng: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/DOI_CHIEU_NGUON.csv`, `DANH_SACH_VAN_DE.csv` ngày 31/10/2026).
- [x] Kiểm tra text layer của PDF và lên phương án OCR cho trang scan; chưa cần tự động hóa toàn bộ OCR (minh chứng: `KIEM_TRA_TRANG_PDF.csv` và `BAO_CAO_KIEM_TRA_DU_LIEU.md` ngày 31/10/2026).
- [ ] Tạo danh sách ca đánh giá nháp trên cả 6 nhóm dữ liệu; chưa dùng làm kết quả benchmark.

**Điều kiện hoàn thành:** đề cương phù hợp phạm vi; môi trường thử được; biết dữ liệu nào sẵn sàng và dữ liệu nào còn cần xác minh.

**Gặp giảng viên lần 1 dự kiến:** tuần 1; lưu ngày, ý kiến và đầu việc vào thư mục biên bản. Nếu đã liên hệ trước đó, bổ sung minh chứng thay vì tạo một lần gặp giả.

## 4. Tuần 2 — Nạp dữ liệu có nguồn và tìm kiếm vector

- [x] Tạo `config.py`, `storage.py`, `ingestion.py` theo thiết kế (minh chứng: `backend/config.py`, `backend/chunking.py`, `backend/ingestion.py`, `backend/retrieval.py` ngày 31/10/2026).
- [x] Trích xuất một nhóm tài liệu đã đối chiếu; giữ số trang PDF, điều/mục và văn bản gốc (minh chứng: 26/26 trang QĐ 580 số hóa có kiểm chứng tại `02_Dữ Liệu Quy Chế/04_Dữ Liệu Đã Kiểm Chứng/QD580/QD580_THEO_TRANG.md`, `QD580_PAGES.jsonl` và `KIEM_CHUNG_TUNG_TRANG.csv` ngày 31/10/2026).
- [x] Ánh xạ nội dung Markdown về nguồn; ghi rõ phần chưa xác minh (minh chứng: `DE_XUAT_DINH_CHINH_FILE_02.md` và `NHAT_KY_DINH_CHINH.csv` ngày 31/10/2026 bóc tách phần ngoài QĐ 580).
- [x] Thử chia theo cấu trúc với mốc 600 ký tự/overlap 100; kiểm tra không cắt mất điều kiện hoặc ngoại lệ (minh chứng: Pipeline chunking v2.0 sinh 104 chunks tại `05_Mã Nguồn Chương Trình/data/QD580_CHUNKS.jsonl` và `data/QD580_MANIFEST.json`, bảo toàn nguyên vẹn 51 hàng bảng biểu và 142 điều khoản, 100% chunks <= 256 tokens).
- [x] Tạo chunk ID và metadata; không điền số trang, quyết định hay điều khoản bằng suy đoán (minh chứng: deterministic ID v2, lưu 351 source spans đối soát từng ký tự, mã băm SHA-256 `5802f176...398`).
- [x] Chọn embedding sau chạy thử trên máy; tạo ChromaDB và truy xuất top-k (minh chứng: mô hình `bkai-foundation-models/vietnamese-bi-encoder` 768 chiều, revision `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`, collection ChromaDB `qd580_baseline_v2` chứa 104 vectors ngày 31/10/2026).
- [x] Kiểm tra nạp lại không nhân đôi; nạp lỗi/trang scan không âm thầm bị bỏ qua (minh chứng: kiểm tra tính Idempotent nạp lại lần 2 giữ nguyên đúng 104 chunks, ghi nhận tại `05_Mã Nguồn Chương Trình/data/INGESTION_STATUS.json` ngày 31/10/2026).
- [x] Xây nền trạng thái `uploaded`, `processing`, `needs_review`, `ready`, `failed`; chỉ kích hoạt nguồn đủ điều kiện (minh chứng: vòng đời `BUILDING` -> `READY`, `corpus_ready: true` trong `INGESTION_STATUS.json` và manifest).
- [x] Tạo danh sách câu hỏi, đáp án/ý bắt buộc và nguồn chuẩn cho tập phát triển (minh chứng: `02_Dữ Liệu Quy Chế/04_Dữ Liệu Đã Kiểm Chứng/QD580/DEV_10_CAU_QD580.jsonl` gồm 10 ca phát triển học vụ QĐ 580 ngày 31/10/2026).
- [x] Ghi cấu hình máy, số trang/đoạn và ví dụ truy xuất đúng/sai (minh chứng: Báo cáo thực nghiệm `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_BASELINE_VECTOR_QD580.md` đo lường Hit@1 55.6%, Hit@3 77.8%, Hit@10 100%, MRR@10 0.6806, độ phủ 83.1%, phân tích chi tiết DEV_02 đưa vào Top 6 và bác bỏ ngưỡng tĩnh 0.45 ở DEV_10 ngày 31/10/2026).

**Điều kiện hoàn thành:** một nhóm nguồn chạy xuyên suốt từ PDF/Markdown đã xác minh đến kết quả tìm kiếm có thể mở đúng trang. Các nhóm còn lại tiếp tục được đối chiếu đến tuần 5.

## 5. Tuần 3 — RAG cơ bản và backend

- [x] Tạo `rag_engine.py`, `main.py`; triển khai `/health` và `/chat` (minh chứng: `backend/rag_engine.py`, `backend/main.py` với Lifespan nạp model một lần, GET `/health` HTTP 200/503, POST `/chat` với business status `answered`, `needs_clarification`, `insufficient_evidence`, `out_of_scope` ngày 01/11/2026).
- [x] Câu hỏi → vector search → ngữ cảnh có source ID → Gemini → câu trả lời và citations (minh chứng: Pipeline RAG qua GeminiClient `google-genai` SDK / Offline Mock stub với model `gemini-2.5-flash`, gán nhãn ngữ cảnh `SRC-k` ngày 01/11/2026).
- [x] Nguồn do backend dựng từ metadata, không để mô hình tự tạo trang hoặc số quyết định (minh chứng: Backend Citation Verification trong `RAGEngine.answer_question()` lọc bỏ triệt để hallucinated source IDs, ánh xạ chính xác về metadata QĐ 580 ngày 01/11/2026).
- [x] Kiểm tra câu không có căn cứ; tách `insufficient_evidence` khỏi lỗi mạng/API (minh chứng: Xử lý phân biệt rõ ràng câu hỏi ngoài phạm vi, câu hỏi thiếu căn cứ và lỗi upstream 502/503 trong `rag_engine.py` và `test_api_and_rag.py` ngày 01/11/2026).
- [x] Thêm hành vi hỏi lại khi thiếu dữ kiện và thông báo phạm vi sản phẩm đồ án (minh chứng: System prompt quy định rõ ràng vai trò hỗ trợ học vụ phi chính thức, yêu cầu làm rõ khi thiếu dữ kiện ngày 01/11/2026).
- [ ] Thử trường hợp nguồn mâu thuẫn; không tự động chọn văn bản ưu tiên thiếu căn cứ (để ngỏ cho giai đoạn tích hợp thêm quy chế mới ở Tuần 4-5).
- [x] Giới hạn đầu vào, số đoạn và độ dài đầu ra; timeout và thử lại có giới hạn (minh chứng: Pydantic validation 1000 ký tự trả về HTTP 422, `max_output_tokens=1024`, retry hữu hạn 2 lần với backoff trong `gemini_client.py` ngày 01/11/2026).
- [x] Ghi số đo từng bước; tải mô hình một lần khi backend khởi động (minh chứng: `timings` trả lời chi tiết `retrieval_ms`, `llm_ms`, `total_ms`; FastAPI Lifespan nạp model Bi-Encoder vào RAM một lần duy nhất ngày 01/11/2026).
- [x] Chạy baseline A trên tập phát triển, ghi lỗi và hướng sửa (minh chứng: Hoàn tất chốt Baseline A lượt R04, đánh giá thực nghiệm Live 10 ca phát triển với Gemini 3.5 Flash Lite và chấm rubric trung thực tại `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_CHOT_BASELINE_QD580_R04.md`, `DNC_RAG_LIVE_DEV10_R04.jsonl` và `DNC_RAG_LIVE_DEV10_R04.csv` ngày 01/11/2026).
- [ ] Tiếp tục hoàn thiện đáp án chuẩn và đối chiếu các nhóm dữ liệu khác.

**Điều kiện hoàn thành:** gọi API nhận được câu trả lời có nguồn; có ví dụ thành công, thiếu căn cứ và lỗi dịch vụ được phân biệt đúng. Hoàn tất toàn bộ bước A, B, C, D độc lập, 50/50 bài test tự động đạt 100%, khử rò rỉ path, kiểm soát retry SDK và đánh giá thực nghiệm Live chốt Baseline A với `gemini-3.5-flash-lite`.

**Gặp giảng viên lần 2 dự kiến:** cuối tuần 3; trình bày demo baseline, dữ liệu và cách đánh giá, ghi góp ý thật.

## 6. Tuần 4 — Giao diện, hybrid, reranking và hội thoại

- [x] Tạo `retrieval.py` và `bm25_retriever.py`: BM25 trên cùng tập 104 đoạn với vector; tokenizer tiếng Việt bảo tồn dấu và số hiệu điều khoản, hợp nhất thứ hạng Reciprocal Rank Fusion ($k=60$) và loại trùng (minh chứng: `backend/bm25_retriever.py`, `backend/retrieval.py`, 10 bài test `tests/test_hybrid_bm25_rrf.py` ngày 01/11/2026).
- [x] Hỗ trợ cấu hình chế độ truy xuất linh hoạt: A — dense vector; B — hybrid (dense + BM25 + RRF); cấu hình qua CLI `--mode` và tham số `POST /chat` API `mode="dense"|"hybrid"` (minh chứng: `backend/main.py`, `backend/rag_engine.py`, `backend/cli.py` ngày 01/11/2026).
- [x] Đánh giá so sánh thực nghiệm A/B Retrieval và Live LLM trên tập 10 ca phát triển (minh chứng: Báo cáo `evaluation/results/BAO_CAO_HYBRID_BM25_RRF_QD580.md`, `RETRIEVAL_AB_COMPARISON_TASK05.json`, `DNC_RAG_AB_DEV10_TASK05.jsonl` và `.csv` ngày 01/11/2026; Hit@5 đạt 100%, giải quyết thành công DEV_02 và DEV_08).
- [ ] Thử reranker trên tập phát triển; ghi chất lượng, thời gian và lựa chọn mô hình (Chưa triển khai trong Nhiệm vụ 05).
- [ ] Tạo `frontend/app.py`, `api_client.py`; giao diện chỉ gọi FastAPI, không import backend AI trực tiếp (Chưa triển khai trong Nhiệm vụ 05).
- [ ] Hiển thị câu trả lời, đoạn nguồn, thông tin đã xác minh và liên kết PDF/trang khi có (Chưa triển khai trong Nhiệm vụ 05).
- [ ] Giữ lịch sử trong phiên; chỉ gửi tối đa 3 lượt hỏi–đáp gần nhất, có giới hạn độ dài (Chưa triển khai trong Nhiệm vụ 05).
- [ ] Viết lại có điều kiện với câu nối tiếp; câu độc lập không cần gọi LLM viết lại (Chưa triển khai trong Nhiệm vụ 05).
- [ ] Thử đổi chủ đề, thiếu ngữ cảnh, viết tắt, câu phủ định và con số; không được sửa sai ý hỏi (Chưa triển khai trong Nhiệm vụ 05).
- [ ] Có nút xóa chat; kiểm tra hai phiên độc lập và xóa cả ngữ cảnh.
- [ ] Hiển thị tiến trình/trạng thái; triển khai streaming thực nếu API/SDK hỗ trợ, không thay bằng hiệu ứng gõ giả.

**Điều kiện hoàn thành:** chat qua API; các chế độ A/B/C chạy được; câu nối tiếp rõ được xử lý, câu mơ hồ được hỏi lại và nguồn kiểm chứng được.

## 7. Tuần 5 — Admin tối giản và chốt dữ liệu đánh giá

- [ ] Cấp tài khoản admin, băm mật khẩu, xác thực phiên/token và đăng xuất.
- [ ] Bảo vệ endpoint quản trị tại backend; kiểm tra khách gọi trực tiếp bị từ chối.
- [ ] Giao diện admin: tải PDF/metadata, xem trạng thái/lỗi, nạp lại, kích hoạt/ngừng dùng.
- [ ] Giới hạn một tác vụ ingestion tại một thời điểm, không xây hàng đợi phân tán.
- [ ] Đồng bộ nguồn đang kích hoạt ở vector và BM25; nguồn mới chỉ dùng khi xử lý đầy đủ.
- [ ] Kiểm tra file trùng, lỗi trích xuất, dừng dùng nguồn, cập nhật metadata và phiên bản.
- [ ] Hoàn tất kiểm chứng nội dung dự định công bố trên cả 6 nhóm; lập danh sách phần chưa đủ căn cứ, không tự đánh dấu hoàn tất toàn bộ.
- [ ] Thêm phản hồi đơn giản và số đo tối thiểu; không thu thập bản chép toàn bộ hội thoại mặc định.
- [ ] Hoàn thiện **75 ca dự kiến, trong khoảng 60–80**, có nhãn và nguồn chuẩn theo `LOGIC.md`, mục 7.
- [ ] Chia 25 ca phát triển / 50 ca kiểm thử cuối, giữ các câu biến thể cùng kịch bản trong cùng tập.
- [ ] Hoàn tất tinh chỉnh trên tập phát triển; đóng băng kho dữ liệu, prompt và cấu hình trước khi mở tập kiểm thử cuối.

**Điều kiện hoàn thành:** admin thao tác được, khách không có quyền quản trị, hai nhánh chỉ mục đồng nhất, bộ đánh giá có nguồn và phiên bản rõ ràng.

**Gặp giảng viên lần 3 dự kiến:** cuối tuần 5; demo giao diện/admin, trình bày bộ đánh giá và phạm vi còn giới hạn.

## 8. Tuần 6 — Thực nghiệm, kiểm thử và minh chứng

- [ ] Chạy A/B/C trên cùng tập kiểm thử cuối và cùng phiên bản dữ liệu; lưu cấu hình, đầu ra và nguồn từng ca.
- [ ] Chấm Hit Rate@3, MRR@10 trên ca có nguồn chuẩn; đo độ phủ bằng chứng cho câu nhiều nguồn.
- [ ] Chấm đúng đáp án, faithfulness, relevance, trích dẫn; ghi rubric và người chấm.
- [ ] Chấm riêng câu cần hỏi lại, nguồn mâu thuẫn và từ chối; báo từ chối nhầm trên ca có đáp án.
- [ ] Đo nội dung đầu/tổng thời gian; báo trung vị, p95, khởi động lạnh, lỗi/timeouts và điều kiện đo.
- [ ] Không gọi mục tiêu 2–4 giây/4–8 giây là số đã đo; điền kết quả thực tế.
- [ ] Phân tích lỗi theo nguyên nhân: nguồn, chia đoạn, truy xuất, rerank, viết lại, sinh và citation.
- [ ] Chọn cấu hình mặc định bằng chất lượng và tốc độ; không mặc định C tốt nhất.
- [ ] Nếu sửa sau khi xem tập cuối, ghi rõ lần chạy mới và giới hạn đánh giá.
- [ ] Kiểm thử quyền admin, phiên độc lập, xóa chat, nạp trùng, ngừng dùng tài liệu và lỗi API.
- [ ] Vẽ Use Case, kiến trúc, ingestion/query, sequence, dữ liệu; số hình theo chương báo cáo thực tế.
- [ ] Chụp ảnh demo và lưu minh chứng; chuẩn bị dữ liệu demo dự phòng ghi rõ là kết quả đã lưu, không giả làm phản hồi trực tiếp.

**Điều kiện hoàn thành:** có bảng so sánh kèm số mẫu, số liệu tái chạy được, danh sách lỗi/giới hạn và minh chứng sử dụng. Không yêu cầu “đúng 100%” mới được viết báo cáo.

## 9. Tuần 7–9 — Hoàn thiện báo cáo

Ghi chép đã bắt đầu từ tuần 1; giai đoạn này tập trung tổng hợp và trình bày.

### Tuần 7: Chương 1–2

- [ ] Chương 1: bài toán, hệ thống liên quan, mục tiêu, phạm vi đã chốt và phương pháp.
- [ ] Chương 2: RAG, embedding, vector/BM25, hợp nhất, reranking, hội thoại ngắn, kiểm soát câu trả lời và độ đo.
- [ ] Kiểm tra nguồn tham khảo gốc, thông tin xuất bản và định dạng trích dẫn; không chép các so sánh thiếu căn cứ từ tài liệu cũ.

### Tuần 8: Chương 3–4

- [ ] Chương 3: hai đối tượng sử dụng, quyền, phiên chat, một backend, mô hình dữ liệu, luồng và giao diện.
- [ ] Chương 4: môi trường thật, hiện thực, demo, bộ 60–80 ca, tách tập, A/B/C, số đo, lỗi và giới hạn.
- [ ] Bảng biểu nêu mẫu số và phiên bản cấu hình; các số liệu chưa đo không được điền bằng mục tiêu.

### Tuần 9: Hoàn chỉnh và góp ý

- [ ] Viết kết luận dựa trên thực nghiệm, nêu giới hạn và hướng mở rộng.
- [ ] Hoàn thiện tham khảo, phụ lục, chú thích hình/bảng, danh mục và mục lục.
- [ ] Kiểm tra độ dài dự kiến 30–50 trang và thể thức theo tài liệu trường/giảng viên cung cấp.
- [ ] Đồng bộ tên đề tài, phạm vi, công nghệ, chức năng và kết quả giữa code, báo cáo, slide và các Markdown.
- [ ] Gặp giảng viên lần 4, lưu biên bản và sửa theo góp ý.
- [ ] Đóng băng bản bàn giao trước 28/12; chỉ sửa lỗi cần thiết và ghi lại thay đổi.

**Điều kiện hoàn thành:** báo cáo phản ánh đúng phần mềm thực tế, có số liệu và minh chứng, không mô tả chức năng chưa làm như đã hoàn thành.

## 10. Tuần 10 và nộp bài

- [ ] Làm slide theo thời lượng bảo vệ được thông báo: bài toán, giải pháp, thiết kế, demo, thực nghiệm, giới hạn và kết luận.
- [ ] Diễn tập câu hỏi về hybrid/reranking, nguồn, hội thoại, ngưỡng, từ chối và độ tin cậy đánh giá.
- [ ] Chạy lại từ môi trường sạch theo README; kiểm tra đường dẫn, dependencies và dữ liệu cần thiết.
- [ ] Kiểm tra API key, cấu hình admin, hạn mức dịch vụ và phương án mạng trước demo.
- [ ] Loại bí mật thật khỏi gói nộp; cung cấp `.env.example` và hướng dẫn cấu hình.
- [ ] Đóng gói source, dữ liệu được phép bàn giao, bộ đánh giá, kết quả, báo cáo PDF/Word và slide.
- [ ] Kiểm tra thông báo nộp chính thức: lịch, hình thức in/đóng quyển, file điện tử, CD/USB hoặc kênh nộp theo yêu cầu thật.
- [ ] In/đóng quyển nếu được yêu cầu; xác nhận đã nộp trong khoảng 04–10/01/2027 theo lịch kế thừa sau khi đối chiếu.

## 11. Quy tắc giữ khối lượng vừa sức

**Phải giữ:** 6 nhóm dữ liệu theo nguồn đủ điều kiện; RAG có trích dẫn; A/B/C; hội thoại ngắn; admin tối giản; đánh giá có nguồn chuẩn.

**Không bổ sung trong đợt này:** tài khoản sinh viên, quên mật khẩu tự phục vụ, lịch sử đa thiết bị, nhiều cấp phê duyệt, dashboard phức tạp, bộ nhớ dài hạn, portal cá nhân, mobile app, microservices.

Nếu chậm tiến độ: ưu tiên chạy local ổn định, giảm trang trí và hoãn hosting công khai. Việc thay đổi chức năng bắt buộc cần trao đổi lại với người dùng và ghi vào cả ba tài liệu; không tự bỏ hybrid/reranking chỉ vì baseline đã chạy được.

## 12. Mẫu nhật ký sau mỗi buổi làm

| Trường | Nội dung cần ghi |
| --- | --- |
| Ngày và người thực hiện | Ngày thực tế, không tự điền ngày kế hoạch là ngày hoàn thành |
| Đầu việc | Checklist đang xử lý |
| Kết quả | File, lệnh chạy, ảnh, cấu hình hoặc bảng số đo làm minh chứng |
| Vấn đề và giới hạn | Lỗi, dữ liệu chưa xác minh, mục chưa làm |
| Quyết định | Thay đổi gì, lý do và tác động |
| Bước tiếp theo | Việc cụ thể cho lần sau |

Nhật ký gặp giảng viên thêm: ngày gặp, nội dung trình bày, góp ý nguyên văn/tóm tắt chính xác, điều chỉnh cần làm và trạng thái thực hiện. Không đánh dấu gặp thầy hay được duyệt chỉ từ ngày đã lên lịch.

## 13. Nhật ký cập nhật tài liệu

**31/10/2026:** Đồng bộ `PROJECT.md`, `LOGIC.md`, `ROADMAP.md` theo phương án giảm tải đã được người dùng đồng ý. Giữ lõi RAG, thu gọn quản trị/tài khoản, thay code mẫu cũ bằng đặc tả và tiêu chí nghiệm thu; bổ sung kế hoạch 75 ca A/B/C. Giữ bản gốc trong ZIP, không sửa các Markdown quy chế và chưa thay đổi báo cáo Word hay tạo mã nguồn ứng dụng.
