# DNC-RAG-TASK-04-R03 — Hoàn thiện citation và Gemini live

Ngày giao: **01/11/2026**.

> **Project ID:** `dnc-academic-advisor-rag`  
> **Git root:** `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`  
> **Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git`  
> Đây là đồ án RAG học vụ DNC, không phải dự án Điện toán đám mây.

## 1. Đọc trước khi làm

- PROJECT, LOGIC, ROADMAP và hai file báo cáo/bàn giao ở Git root.
- Nhiệm vụ 04 gốc và `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R02.md`.
- Kiểm tra đúng Git root và remote; giữ lịch sử R01/R02. Lượt này dùng mã `DNC-RAG-TASK-04-R03`.

## 2. Mục tiêu

Khắc phục lỗi citation/schema, phân biệt mock/live rõ ràng, kết nối Gemini thật và đánh giá bản RAG QĐ 580 qua FastAPI. Chưa làm hybrid, reranking, UI, hội thoại nhiều lượt, tài khoản hoặc bổ sung dữ liệu khác.

Bản R02 đã qua 35 kiểm thử nhưng còn lỗi được tái hiện trong nhận xét. Không coi số test qua là bằng chứng đã hoàn thiện tất cả yêu cầu.

## 3. Citation và schema — sửa trước mọi đánh giá chất lượng

- Bỏ hoàn toàn việc tự gắn nguồn top-1 dựa vào similarity khi model không cung cấp citation hợp lệ.
- Không tự chuyển status sai, thiếu trường hoặc answer rỗng thành `answered`. Dùng schema chặt chẽ và kiểu lỗi rõ ràng.
- `answered` phải có citation hợp lệ; chỉ ID bịa hoặc không có citation thì không trả như thành công. Không tạo câu thay thế có vẻ đã được giải đáp khi schema lỗi.
- Nếu model trả cả nguồn thật và nguồn bịa, nêu chính sách rõ: reject cả phản hồi hoặc hạ trạng thái an toàn; không lặng lẽ lọc ID rồi giữ nguyên mọi khẳng định chưa kiểm chứng. Không thêm vòng sửa LLM vô hạn.
- ID phải thuộc đúng tập ngữ cảnh của request. Không nhận tên file/trang do model tự tạo thay metadata nguồn.
- Tách `embedding_text` và nội dung gốc. Dùng `source_spans` để dựng quote và trang; không lấy context prefix hoặc 120 ký tự đầu tùy ý làm trích dẫn PDF.
- Citation có thể chứa danh sách các đoạn nguồn/trang; không giả định chỉ một trang đầu là đủ. Đối chiếu từng quote với chuỗi trang nguồn và giữ offset theo định nghĩa đã có.
- Trang in chưa xác định phải null/không hiển thị, không dùng -1 hoặc giá trị suy đoán.
- Kiểm tra đúng source ID/quote chỉ là kiểm tra cấu trúc và truy nguyên; đánh giá nội dung câu trả lời bám nguồn vẫn phải làm riêng.

## 4. Cấu hình và chế độ mock/live

- Key người dùng đã cung cấp được lưu cục bộ trong `05_Mã Nguồn Chương Trình/.env` dưới biến `GEMINI_API_KEY`. **Không yêu cầu người dùng gửi lại key trong chat, không in/chép key vào file tracked.**
- Nạp `.env` bằng đường dẫn xác định theo vị trí mã nguồn; giữ ưu tiên biến môi trường đã được đặt (`override=False` hoặc cơ chế tương đương). Đọc được khi chạy từ Git root hoặc thư mục mã nguồn.
- Mock chỉ bật qua dependency injection/test flag rõ ràng, mặc định tắt ở chế độ phục vụ thật. Không có key/model/SDK hợp lệ phải trả 503 hoặc trạng thái unavailable, không tự tạo câu trả lời mock.
- `/health` phân biệt retrieval sẵn sàng, cấu hình LLM và trạng thái tích hợp. Không gọi mạng ở mọi health check. Không gọi có SDK client là chứng minh kết nối live đã thành công.
- Các test API phải dùng stub được inject rõ, không dựa vào việc máy đang không có key. Chạy full suite không được phát sinh request Gemini thật ngoài ý muốn.

## 5. Kết nối Gemini đúng model/API thực tế

Thông tin đã kiểm tra, không chứa bí mật:

- Key cục bộ gọi model listing thành công.
- Hai probe sinh nội dung ngắn với `gemini-2.5-flash` qua `models.generate_content` trả HTTP 404. Provider thông báo model này không còn được cung cấp cho người dùng mới.
- Hướng dẫn chính thức được đọc ngày 01/11/2026 có ví dụ Interactions API và `gemini-3.8-flash`: [Gemini Getting started](https://ai.google.dev/gemini-api/docs/get-started).

Yêu cầu:

1. Đọc lại tài liệu chính thức và khả năng SDK hiện cài, chọn model/API tài khoản thực sự gọi được. Không đổi sang một model ngẫu nhiên chỉ vì có tên trong danh sách; không bật thanh toán, nâng cấp tài khoản hoặc tạo tài nguyên trả phí trong nhiệm vụ này.
2. Giữ model và lựa chọn API cấu hình được; cập nhật SDK tối thiểu nếu cần, ghi phiên bản đã chạy. Không nâng cấp toàn bộ môi trường không liên quan.
3. Timeout phải được gắn thật vào HTTP/request SDK. Retry chỉ lỗi tạm thời, hữu hạn; không retry 400/401/403/404 hoặc lỗi schema như lỗi mạng. Kiểm soát cả retry mặc định của SDK.
4. Smoke test một yêu cầu nhỏ trước; không chạy 10 ca khi model/auth còn lỗi. Giới hạn output và số lần gọi, ghi chi phí/token nếu SDK cung cấp; không tự suy ra dịch vụ miễn phí.
5. Nếu dùng Interactions, cập nhật cách truyền system instruction, JSON/structured output và đọc text theo docs/SDK đang dùng. Không mang tham số GenerateContent sang API khác khi chưa kiểm tra. Chưa bật memory phía server hay multi-turn; ưu tiên request độc lập và không lưu hội thoại khi API hỗ trợ cấu hình tương ứng.
6. Nếu smoke test lỗi quota/quyền/model, báo mã lỗi đã che bí mật và dừng các lần gọi chất lượng phụ thuộc; hoàn thành phần code/test độc lập, không giả kết quả live.

## 6. API và lỗi

- Dùng lỗi có kiểu/mã cho readiness, cấu hình, timeout, quota, upstream và schema; không phân loại bằng tìm từ trong thông báo exception.
- Lỗi kho/cấu hình trả 503; lỗi upstream/schema có mã phù hợp đã tài liệu hóa, timeout có phân biệt. Đầu vào sai trả 422.
- Response công khai không lộ đường dẫn ổ đĩa, exception SDK thô hay key; trả request ID để đối chiếu log nội bộ đã che bí mật.
- Câu ngoài phạm vi, thiếu căn cứ, cần hỏi lại là trạng thái nghiệp vụ; phân biệt lỗi dịch vụ với giới hạn dữ liệu.
- Đảm bảo câu thiếu dữ liệu học vụ không bị gọi là ngoài phạm vi toàn bộ dự án chỉ vì QĐ 580 chưa có biểu phí.
- Không coi chỉ thị trong câu hỏi/đoạn nguồn là chỉ thị thay thế system prompt.

## 7. Kiểm thử hồi quy và chạy thật

Giữ các test cũ phù hợp, cập nhật các test đã vô tình chấp nhận hành vi sai. Thêm ít nhất các nhóm kiểm tra sau:

- Model chỉ trả ID bịa; `answered` không citation ở cả similarity cao/thấp; status sai; JSON không phải object; answer rỗng; kiểu cited IDs sai.
- Citation dựng từ spans của đoạn qua nhiều trang, đoạn overlap và context prefix; quote phải tìm lại được nguyên văn ở trang được dẫn.
- Thiếu `.env`, key trống, SDK khởi tạo lỗi: không trả câu mock như câu live. Có `.env` chỉ là test đọc cấu hình, không tự gửi mạng.
- Timeout thực truyền vào SDK; lỗi không retry và lỗi được retry đúng số lần; không lộ bí mật/đường dẫn trong response/log đã kiểm tra.
- `/health` và `/chat` có status HTTP/nghiệp vụ đúng; test suite không phụ thuộc Gemini thật hoặc khóa trên máy.

Sau khi offline tests qua và smoke live thành công:

- Chạy bộ 10 ca phát triển trên bản trả lời thật. Ca nối tiếp chưa hỗ trợ thì dùng câu độc lập có nhãn rõ hoặc ghi N/A; không báo đã hỗ trợ hội thoại.
- Lưu câu hỏi/query dùng, ID và nội dung nguồn thật, cấu hình model/API, câu trả lời, citation, trạng thái, lỗi và thời gian từng bước. Không lưu key.
- Đối chiếu thủ công các ý bắt buộc, số liệu/ngoại lệ, bám nguồn, đúng quote/trang và hành vi hỏi lại/từ chối. Ghi người chấm, ngày, rubric và mẫu số; không gọi kết quả mock là chất lượng LLM.
- Khi sai, phân biệt thiếu nguồn do retrieval với sinh sai khi đã có đủ nguồn. Không đổi câu hỏi/đáp án chuẩn để tăng điểm; nếu đính chính nguồn thật, ghi phiên bản và lý do.
- Không đặt yêu cầu phải đạt điểm hoàn hảo; báo lỗi còn lại trung thực. Tập 10 ca vẫn là tập phát triển, không phải đánh giá cuối 60–80 ca.

## 8. Đầu ra và bàn giao

- Code client/engine/API/config và test đã sửa; `.env.example` không có bí mật.
- `evaluation/results/BAO_CAO_RAG_LIVE_QD580_R03.md` và kết quả từng ca dạng JSONL/CSV; smoke test live có trạng thái thật. Không ghi đè/xóa báo cáo R02 để làm mất lịch sử.
- Sửa báo cáo cũ theo nhật ký đính chính: ngày QĐ 580 là 02/08/2024 theo nguồn dự án; Python/version thực tế, hash tự tính, timeout thực và mức nghiệm thu đúng.
- Cập nhật README và ROADMAP: chỉ đánh dấu live đã làm khi có minh chứng; chưa đưa UI/hybrid/reranking thành đã hoàn thành.
- Thêm lượt `DNC-RAG-TASK-04-R03` vào `BAO_CAO_ANTIGRAVITY.md`, cập nhật chỉ mục/liên kết ở `BAO_CAO_BAN_GIAO.md`; để phần Codex là CHƯA KIỂM TRA.
- Commit/push repository đã chỉ định sau khi kiểm tra staged diff, giữ `.env` bị ignore, không force-push. Báo SHA local/remote và phần còn chưa push nếu có.

## 9. Điều kiện hoàn thành

Được nghiệm thu RAG live khi: không còn tự gắn citation để hợp thức hóa câu trả lời; mock tách biệt; cấu hình đọc được an toàn; timeout/error handling có kiểm thử; smoke Gemini thật thành công; API trả câu có nguồn kiểm tra được; báo kết quả phát triển và giới hạn thực tế.

Nếu upstream còn cản trở thì bàn giao HOÀN THÀNH MỘT PHẦN với minh chứng; chưa chuyển sang UI/hybrid cho tới khi có quyết định rà soát. Tiếp tục tự làm các phần độc lập trong phạm vi, không cần xin xác nhận lại chỉ để bắt đầu sửa.
