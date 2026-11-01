# DNC RAG — Rà soát bàn giao TASK-04-R02

Ngày: **01/11/2026**. Project ID: `dnc-academic-advisor-rag`. Commit local và remote đã đối chiếu: `9da083287a66019ecef64f325b4c6d21784e073c`.

## Kết luận: CẦN SỬA trước khi nghiệm thu RAG live

Phần API và khung RAG đã có, preflight được cải thiện, các kiểm thử hiện có chạy qua. Tuy nhiên chưa chứng minh RAG live hoạt động đúng; có lỗi gắn nguồn tự động, quản lý mock/config và timeout. Tiếp tục nhiệm vụ 04 bằng lượt R03, chưa chuyển sang hybrid/reranking/UI.

## Kết quả kiểm tra độc lập

- Chạy bộ discovery hiện có: **35 tests, 0 failures, 0 errors, 0 skipped**. Trong tiến trình kiểm thử đã bỏ biến key khỏi môi trường; không gọi Gemini thật trong bộ test.
- Phép thử idempotency được cô lập ở thư mục tạm bằng cách điều hướng biến đường dẫn trong module kiểm thử; không ghi đè baseline.
- Preflight thực tế chạy qua với kho 104 chunks tại `qd580_baseline_v2`.
- Dùng mock xác định để thử lỗi citation và schema, không coi đó là kết quả chất lượng LLM.
- Thử TestClient với môi trường không có key nhưng có `.env` cục bộ: `/health` trả 200 `healthy`, `llm_live=false`.
- Có key trong `.env` đã được lưu theo yêu cầu người dùng. Code chưa có `load_dotenv` hoặc bước nạp file cấu hình tương đương; client mặc định không đọc được key này.
- Probe riêng dùng `dotenv_values`, không sửa cấu hình ứng dụng: gọi model listing bằng key cục bộ thành công. Hai yêu cầu sinh nội dung ngắn với model đang cấu hình `gemini-2.5-flash` đều trả HTTP 404. Lần thứ hai bỏ các tùy chọn thinking để kiểm tra tối thiểu.
- Thông báo provider, đã loại thông tin bí mật, cho biết model 2.5 Flash không còn được cung cấp cho người dùng mới và đề nghị cập nhật model/API. Điều này không chứng minh key hỏng. Không chạy bộ RAG 10 câu live trong trạng thái này.
- Đã đối chiếu hướng dẫn chính thức hiện tại: [Gemini API — Getting started](https://ai.google.dev/gemini-api/docs/get-started), trong đó ví dụ Python dùng Interactions API và model `gemini-3.8-flash`. Cần triển khai theo API/model thực sự được tài khoản hỗ trợ và xác nhận bằng smoke test, không chỉ đổi nhãn model trong báo cáo.

## 1. [P1] Engine tự gắn citation dù mô hình không cung cấp bằng chứng hợp lệ

`backend/rag_engine.py` có nhánh: `answered` nhưng không còn citation hợp lệ thì lấy nguồn đầu nếu similarity >=0.40.

Probe thực tế:

| Đầu ra mock | Kết quả hiện tại |
| --- | --- |
| `answered`, nội dung không được nguồn hỗ trợ, chỉ dẫn `SRC-999`; nguồn đầu similarity 0.65 | Vẫn `answered`, backend tự gắn `SRC-1` |
| `answered`, không có citation; similarity 0.30 | Vẫn `answered`, citations rỗng |
| status không hợp lệ `WRONG`, có `SRC-1` | Tự đổi thành `answered` |

Đây là lỗi kiểm chứng nguồn, không phải chỉ vấn đề trình bày. Backend biến nguồn tìm thấy thành căn cứ cho một câu mà mô hình chưa chứng minh sử dụng nguồn đó. Ngưỡng similarity 0.40 cũng không xác minh nội dung.

**Cần sửa:** bỏ nhánh tự gắn nguồn. Đầu ra sai schema/trạng thái hoặc `answered` không có citation hợp lệ phải bị xử lý bằng trạng thái/lỗi rõ ràng, không được nâng thành thành công. Nguồn hợp lệ về ID vẫn cần được đánh giá bám nguồn riêng.

## 2. [P1] Chế độ không có key vẫn phục vụ câu trả lời mock và báo healthy

`GeminiClient.generate_json` tự chuyển sang `_default_offline_mock` khi không live. Nếu prompt có nguồn, mock mặc định luôn trả một câu chung với `SRC-1`. FastAPI khởi động bình thường và `/health` vẫn 200 khi không có LLM thật.

Trường `is_live_llm=false` là thông tin có ích nhưng không thay thế việc phân biệt rõ dịch vụ thật với chế độ test. Báo cáo nói chỉ chờ key, trong khi key đã có cục bộ nhưng chưa được chương trình nạp.

**Cần sửa:** nạp `.env` đúng thư mục, không ghi đè biến môi trường do người dùng đã đặt; mặc định phục vụ thật phải báo thiếu cấu hình bằng 503. Mock chỉ bật rõ ràng trong test hoặc chế độ demo được gắn nhãn; không fallback âm thầm khi khởi tạo SDK lỗi. Test offline phải inject stub hoặc bật flag test riêng, không phụ thuộc vào việc máy không có key.

## 3. [P1] Citation chưa được dựng từ spans và có thể trích context giả làm lời văn nguồn

Retriever trả `content` là document đã lưu để embedding, gồm `context_prefix` do hệ thống thêm. Engine lấy 120 ký tự đầu làm `quote_snippet` và dùng trang bắt đầu của chunk, không dùng `source_spans`.

Probe trên artifact thực: snippet bắt đầu bằng dấu `[` của context prefix, không phải trích dẫn nguyên văn PDF. Với chunk nhiều trang hoặc overlap, một trang bắt đầu cũng không đại diện cho mọi phần được dùng.

**Cần sửa:** phân biệt văn bản embedding, nội dung gốc và vị trí spans. Dựng trích đoạn kiểm tra được theo trang nguồn; hỗ trợ nhiều trang/đoạn khi cần. Trang in chưa biết phải nullable, không hiện -1 như số trang thật. Không gọi nguồn đã được xác minh chỉ từ ID tồn tại.

## 4. [P2] Timeout/retry và phân loại lỗi chưa đúng như báo cáo

- `self.timeout` chỉ được gán trong client, chưa truyền vào cấu hình HTTP/request của SDK.
- Retry hiện bắt tất cả exception, gồm lỗi xác thực, model không có và JSON sai, thay vì chỉ lỗi tạm thời.
- FastAPI phân loại RuntimeError bằng chuỗi chứa “không tồn tại/chưa sẵn sàng”, khiến lỗi kho hoặc upstream dễ bị gán sai mã HTTP.
- Chi tiết exception được trả thẳng ở một số nhánh `/health`, `/chat`, có thể chứa đường dẫn máy hoặc thông báo SDK không cần công bố.

**Cần sửa:** timeout thật tại tầng SDK, retry hữu hạn theo loại lỗi và tính cả retry nội bộ SDK; lỗi có kiểu/mã riêng; response công khai chỉ có thông báo an toàn và request ID. Log nội bộ cũng phải che bí mật.

## 5. [P2] Báo cáo cần cập nhật đúng minh chứng

- Ngày QĐ 580 trong báo cáo RAG bị ghi 24/10/2024, khác nguồn dự án 02/08/2024.
- Báo cáo nói timeout 30 giây đã được cấu hình nhưng code chưa truyền timeout tới HTTP.
- Cụm “lọc triệt để hallucination/citation” không được các test hiện có chứng minh; chỉ test một ca trộn ID đúng với ID sai, chưa test mọi ID đều sai hoặc không có ID.
- Ghi đúng Python/version thực tế dùng chạy test; không trộn môi trường 3.11 và 3.14 trong cùng kết luận.
- Hash chunks trong báo cáo bàn giao phải lấy tự động từ artifact, không gõ lại giá trị khác.
- 35 tests qua không chứng minh không còn lỗi phần mềm; ghi đúng phạm vi test/mock và phần tích hợp còn thiếu.

## Nhiệm vụ tiếp theo

Xem `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_R03_CITATION_GEMINI_LIVE.md`. Giữ phạm vi QĐ 580, sửa luồng trả lời/config trước, rồi smoke test và đánh giá live có giới hạn. Báo cáo mới dùng mã `DNC-RAG-TASK-04-R03`, giữ nguyên lịch sử R01/R02.
