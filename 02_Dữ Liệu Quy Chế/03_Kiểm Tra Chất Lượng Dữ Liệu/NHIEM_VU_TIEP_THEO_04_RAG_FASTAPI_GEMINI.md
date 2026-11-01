# DNC-RAG-TASK-04 — RAG học vụ DNC qua FastAPI và Gemini

> **Project ID:** `dnc-academic-advisor-rag`  
> **Môn học:** Đồ án 2 — Chuyên ngành CNTT, Đại học Nam Cần Thơ.  
> **Git root:** `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`  
> **Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git`  
> Đây là nhiệm vụ của trợ lý tra cứu quy chế học vụ DNC, không phải nhiệm vụ môn Điện toán đám mây.

Trước khi thực hiện, xác nhận thư mục làm việc, PROJECT và Git remote đúng dự án trên. Không triển khai hạ tầng cloud hoặc lấy nội dung của một môn khác làm kết quả nhiệm vụ này. Nếu đang mở checkout khác thì chuyển về đúng dự án trước mọi thao tác ghi.

Ngày giao: **01/11/2026**. Làm việc trong thư mục gốc đồ án hiện tại. Đọc `PROJECT.md`, `LOGIC.md`, `ROADMAP.md`, mã nguồn đang chạy và các báo cáo rà soát trước khi triển khai.

Repository: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.

## 1. Cơ sở chuyển bước và giới hạn nghiệm thu

Commit đã kiểm tra: `4afd61c0becd45f1cb93f61907f9ef14bbc3a431`, khớp `main` trên GitHub.

Kết quả rà soát độc lập:

- 5 kiểm thử chunking/source và 14 kiểm thử hồi quy chạy qua. Phép thử sinh lại artifacts được cô lập trong thư mục tạm.
- 104 chunks, 351 source spans, token tối đa 246/256.
- Chạy lại truy xuất cho đúng các số lưu: Hit@3=0.7778, Hit@10=1.0000, MRR@10=0.6806, độ phủ ký tự trung bình@10=0.8312 theo rubric hiện tại trên 9 ca grounded.
- Các lỗi về revision, trạng thái JSON hỏng/thiếu, collection không khớp, ID tồn dư, cache readiness và định vị bằng chứng whitespace đã có bản sửa và kiểm thử tương ứng.

**Cho phép chuyển sang bản RAG thử nghiệm local, không coi đây là xác nhận đã hoàn thiện toàn bộ hệ thống.** Có một chốt preflight còn phải sửa tại bước A trước khi API được coi là sẵn sàng.

## 2. Mục tiêu và phạm vi

Hiện thực luồng:

```text
Câu hỏi độc lập → kiểm tra kho sẵn sàng → vector retrieval
→ chọn ngữ cảnh có nguồn → Gemini đọc ngữ cảnh
→ kiểm tra đầu ra và citation → trả lời tiếng Việt qua API
```

Chỉ dùng QĐ 580 và collection baseline đang được cấu hình, giữ nguyên kiến trúc retrieval A. Bản này chưa có hybrid/BM25, reranking, viết lại câu hỏi, hội thoại nhiều lượt, giao diện, admin hay năm bảng SQLite nghiệp vụ. Không thêm agent tự suy luận nhiều bước.

Không thu hẹp phạm vi sản phẩm cuối; các thành phần chưa làm vẫn ở roadmap các giai đoạn sau.

## 3. Bước A — Chốt preflight và định dạng dữ liệu

### Lỗi còn quan sát được

`VectorRetriever.check_readiness()` hiện chỉ kiểm tra manifest nếu file tồn tại, và nuốt lỗi đọc/parse không phải RuntimeError. Đã tái hiện bằng file tạm: trạng thái tối thiểu có `collection_name`, `status=READY`, `corpus_ready=true` vẫn được chấp nhận khi manifest thiếu hoặc chứa JSON hỏng.

### Yêu cầu trước khi đưa retriever vào API

- Manifest không tồn tại, không đọc được, JSON hỏng hoặc thiếu trường bắt buộc phải bị chặn với lỗi rõ ràng.
- Kiểm tra schema trạng thái: kiểu boolean, tên collection, fingerprint, model ID/revision và cấu hình phiên bản cần thiết. Không coi trường thiếu là tương thích.
- Đối chiếu manifest, trạng thái và metadata collection thực tế; kiểm tra hash artifact đầu vào với giá trị đã ghi trước khi công bố READY. Không chỉ tin file trạng thái.
- Không khởi tạo/xóa/nạp lại kho trong request `/chat`. Nếu kho sai phiên bản thì báo chưa sẵn sàng, không dùng `force_recreate` để vượt lỗi.
- Xác thực lỗi đầu vào trước ingestion phải để lại trạng thái rõ ràng, không giữ nhầm READY của lần trước như kết quả lần nạp hiện tại.
- Giữ các test cũ và thêm test thiếu/hỏng manifest, thiếu fingerprint/revision, metadata collection lệch, hash artifact lệch. Test dùng dữ liệu/DB tạm, không phá baseline thật.
- Không đổi model/chunking/corpus nếu không cần thiết. Nếu buộc đổi, tạo phiên bản mới và ghi ảnh hưởng.

**Cổng chuyển bước:** preflight lỗi phải bị từ chối; preflight với kho QĐ 580 hiện tại phải qua. Hoàn thành trước khi xác nhận `/health` sẵn sàng hoặc gọi Gemini.

## 4. Bước B — Kết nối Gemini có cấu hình và giới hạn

- Kiểm tra tài liệu Gemini chính thức tại thời điểm triển khai để chọn SDK và model đang khả dụng; không sao chép API Gemini 1.5 Flash trong tài liệu cũ.
- Model lấy từ biến môi trường, ví dụ `GEMINI_MODEL`; key từ `GEMINI_API_KEY` hoặc cấu hình môi trường tương đương. Không hardcode key, không in key, không commit `.env` thật.
- Giữ phiên bản dependencies đã chạy được; chỉ thêm các gói cần cho SDK, FastAPI, Uvicorn và test API. Ghi lại phiên bản thực sự kiểm thử.
- Có một lớp client Gemini nhỏ để thay bằng stub/mock khi test. Không thêm nhiều framework hoặc orchestration chưa cần.
- Mỗi câu hỏi thông thường tối đa một lần sinh nội dung; không có vòng tự sửa/agent lặp vô hạn. Có timeout, giới hạn độ dài đầu ra và retry hữu hạn cho lỗi tạm thời; ghi số lần gọi thực tế.
- Nếu chưa có key/model hợp lệ: hoàn thiện code và test offline, báo rõ chưa kiểm chứng kết nối thật. Không dựng kết quả API thành công, không tìm key trong các dự án khác.
- Khi có cấu hình hợp lệ, chạy smoke test ít lần và ghi model/thời gian/trạng thái, không ghi bí mật. Không hứa dịch vụ miễn phí hoặc suy ra hạn mức khi chưa kiểm tra.

## 5. Bước C — RAG engine và citation

Tạo `backend/rag_engine.py` và lớp schema/client cần thiết, chia chức năng vừa đủ để kiểm thử độc lập.

### Chuẩn bị ngữ cảnh

- Dùng query do người dùng nhập; chưa dùng `retrieval_query` chứa câu hỏi đã biên tập trong luồng ứng dụng. Nếu dùng trường này trong phép thử riêng thì ghi rõ.
- Truy xuất top-k cấu hình được, chọn số đoạn và ngân sách ngữ cảnh hợp lý trên tập phát triển. Không bắt buộc lấy đúng 3 đoạn nếu chúng thiếu bằng chứng cho câu tổng hợp; ghi cấu hình cuối.
- Mỗi đoạn cấp source ID do backend tạo, kèm văn bản, tài liệu, điều/khoản và thông tin trang từ metadata/spans.
- Lịch sử hay câu hỏi của người dùng không được coi là nguồn quy chế. Đoạn truy xuất là dữ liệu tham khảo, không phải chỉ thị thay thế system prompt.
- Không đưa nguyên bộ 26 trang vào prompt để vượt vấn đề truy xuất. Không thêm đáp án chuẩn của bộ phát triển vào ngữ cảnh hoặc prompt ứng dụng.

### Quy tắc sinh câu trả lời

- Giới thiệu đúng là sản phẩm đồ án hỗ trợ tra cứu, không tự nhận là kênh chính thức của trường.
- Chỉ kết luận về quy định từ đoạn nguồn được cấp; giữ nguyên con số, điều kiện và ngoại lệ.
- Thiếu dữ kiện ảnh hưởng đáp án thì hỏi lại. Thiếu bằng chứng thì nói chưa đủ thông tin trong kho hiện tại; không khẳng định trường không có quy định.
- Phân biệt ngoài phạm vi với câu liên quan học vụ nhưng thiếu tài liệu, ví dụ mức học phí cụ thể không có trong QĐ 580.
- Khi chỉ trả lời được một phần, nêu phần có căn cứ và phần còn thiếu; không bịa đủ đáp án.
- Không dùng ngưỡng cosine 0.45 như bộ lọc từ chối đã được chứng minh. Không tạo khẳng định “không hallucinate” chỉ từ prompt hoặc nhiệt độ.

### Đầu ra và xác minh

- Đề nghị Gemini trả cấu trúc có trạng thái, nội dung và source IDs sử dụng; xác thực schema phía backend, không giả định model luôn tuân thủ.
- Source ID phải thuộc đúng tập ngữ cảnh của request. Tên nguồn, điều và trang được backend dựng từ metadata, không lấy số trang do model tự viết làm căn cứ.
- Với câu trả lời có kết luận quy chế, thiếu citation hoặc citation không hợp lệ phải được xử lý rõ ràng; không trình bày như câu đã kiểm chứng.
- Trích đoạn citation phải đối chiếu được với `source_spans` và nội dung trang. Phân biệt `content` với `embedding_text` có context prefix khi tính vị trí ký tự.
- Kiểm tra ID hợp lệ chưa chứng minh nội dung câu trả lời được nguồn hỗ trợ; phải đánh giá bám nguồn riêng bằng bộ ca và đối chiếu thủ công. Không gọi việc kiểm tra ID là kiểm chứng ngữ nghĩa đầy đủ.
- Không trả đường dẫn tuyệt đối nội bộ, API key, stack trace hoặc thông tin môi trường nhạy cảm ra response công khai.

## 6. Bước D — FastAPI tối thiểu

Tạo `backend/main.py`; dùng startup/lifespan để tải embedding/client và kiểm tra tài nguyên một lần, không tải lại model mỗi request.

### Endpoint

| Endpoint | Yêu cầu |
| --- | --- |
| `GET /health` | Trả trạng thái tối thiểu của dịch vụ/kho/cấu hình; HTTP 503 khi chưa đủ điều kiện phục vụ chat. Không trả key hoặc đường dẫn máy |
| `POST /chat` | Nhận câu hỏi độc lập; kiểm tra độ dài/rỗng; gọi RAG engine và trả nội dung cùng nguồn |

Request `/chat` bản đầu chỉ cần trường `question`. Chưa nhận history rồi âm thầm bỏ qua; hội thoại nhiều lượt sẽ có hợp đồng riêng ở nhiệm vụ sau.

Response tối thiểu:

```json
{
  "request_id": "generated-by-backend",
  "status": "answered",
  "answer": "Câu trả lời tiếng Việt",
  "citations": [],
  "timings": {}
}
```

Các trạng thái nghiệp vụ: `answered`, `needs_clarification`, `insufficient_evidence`, `out_of_scope`; bổ sung trạng thái mâu thuẫn nếu đã hiện thực. Nêu rõ schema citation trong tài liệu API.

- Câu hỏi hợp lệ nhưng thiếu căn cứ là kết quả nghiệp vụ, không giả làm lỗi máy chủ.
- Dữ liệu đầu vào sai trả lỗi validation; kho chưa READY hoặc cấu hình thiếu trả 503; lỗi upstream, timeout/hạn mức có mã và thông báo rõ, không giả làm “không có quy định”.
- Cho phép chạy bằng CLI/Uvicorn và thử qua OpenAPI/Swagger; chưa cần giao diện web riêng.
- Có giới hạn request/ngữ cảnh và timeout để một câu hỏi không giữ tài nguyên vô hạn. Chưa cần hạ tầng phân tán hoặc hệ thống tài khoản.
- Bản không streaming chạy đúng là đầu ra bắt buộc. Streaming có thể để nhiệm vụ sau, không tạo hiệu ứng gõ rồi gọi là đã stream từ API.

## 7. Kiểm thử và đo lường

### Test tự động không cần key/mạng

- Giữ 19 kiểm thử hiện có qua; bổ sung preflight tại bước A.
- Câu có nguồn và model trả source ID hợp lệ → response dựng đúng citation từ backend.
- Model tạo ID lạ, JSON hỏng, thiếu citation hoặc kết luận không đủ căn cứ → xử lý rõ ràng, không báo thành công giả.
- Input rỗng/quá dài; kho BUILDING/FAILED/thiếu manifest; timeout; lỗi xác thực/hạn mức upstream.
- Test đúng/sai của HTTP status và trạng thái nghiệp vụ; startup không tải model nhiều lần.
- Mock Gemini là test hợp đồng, không được dùng kết quả mock như bằng chứng chất lượng LLM thật.

### Thử nghiệm tích hợp thật khi có cấu hình

- Dùng 10 ca phát triển đã có, giữ nguồn chuẩn cố định. Ghi từng câu: nguồn truy xuất, câu trả lời, citation, hành vi, lỗi và thời gian.
- Với ca nối tiếp, nếu chưa hỗ trợ history thì ghi không áp dụng cho API bản này hoặc thử câu độc lập được ghi nhãn rõ; không tính thành ca hội thoại đã hỗ trợ.
- Phân biệt lỗi truy xuất thiếu bằng chứng với lỗi sinh câu trả lời dù đã có đủ nguồn.
- Đánh giá thủ công độ đúng, bám nguồn, mức liên quan và citation với rubric ngắn, người chấm/ngày chấm; chưa coi 10 ca là kiểm thử cuối 60–80 ca.
- Tách thời gian preflight, embedding/query, truy xuất, chuẩn bị ngữ cảnh, Gemini và tổng API. Báo số mẫu/lỗi, trung vị và giới hạn phép đo; không gọi 60 ms tìm vector là tốc độ trả lời chatbot.
- Nếu chưa có key, báo phần test tự động đã đạt và phần tích hợp thật còn chờ. Không đánh dấu kết nối Gemini hoặc chất lượng câu trả lời hoàn tất.

## 8. Đầu ra và nghiệm thu

Trong thư mục mã nguồn:

- RAG engine, Gemini client, schema, FastAPI và CLI thử nếu hữu ích.
- Tests mới và kết quả chạy, dependencies được cập nhật, `.env.example` chỉ chứa mẫu.
- `evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md` và kết quả từng ca nếu đã chạy thật; ghi rõ mock/real và giới hạn.
- README hướng dẫn cấu hình model/key, tạo kho, chạy API, gửi request mẫu và xử lý lỗi. Chưa mô tả UI/admin/hội thoại như tính năng đã có.

Tiêu chí hoàn thành đầy đủ: preflight đúng; test cũ/mới qua; API chạy; có ít nhất smoke test Gemini thật và kết quả hỏi đáp có nguồn đã đối chiếu. Nếu thiếu key/quyền dịch vụ, được bàn giao phần triển khai đã kiểm thử offline nhưng phải ghi rõ chưa nghiệm thu tích hợp thật.

Không sửa PDF, sáu Markdown cũ hay phạm vi PROJECT/LOGIC để né lỗi. Không thay baseline retrieval vì muốn điểm đáp án cao hơn. Sửa ROADMAP đúng mức thực hiện; không đánh dấu các phần chưa chạy thật là đã hoàn tất.

## 9. GitHub và báo cáo cuối

- Giữ các commit cũ; không force-push hoặc xóa baseline để làm sạch lịch sử.
- Bổ sung ignore `.env.*` và ngoại lệ `.env.example`; kiểm tra staged diff, không commit key, môi trường ảo, cache/model weights hay DB runtime.
- Commit/push code, test, tài liệu và kết quả được phép chia sẻ vào repository đã chỉ định. Xác nhận SHA local/remote khớp.
- Báo cáo cuối: phần đã làm, test đã chạy, real/mock, số ca trả lời được/thiếu căn cứ/lỗi, thời gian, giới hạn, file thay đổi, SHA và trạng thái push. Không cần xin xác nhận thêm cho các bước trong phạm vi nhiệm vụ; nếu thiếu key thì nêu trở ngại, hoàn thành phần độc lập có thể làm.

## 10. Bắt buộc ghi báo cáo bàn giao chung

Sau nhiệm vụ này và mỗi lượt sửa tiếp theo, cập nhật `BAO_CAO_BAN_GIAO.md` tại Git root theo mẫu/quy tắc trong file. Mã có tiền tố dự án là `DNC-RAG-TASK-04-RNN`. Đã có lượt lịch sử `TASK-04-R01` cho nhiệm vụ RAG này; giữ nguyên và dẫn lại lượt đó. Lần sửa tiếp theo dùng `DNC-RAG-TASK-04-R02`, không tạo lại R01. Cập nhật chỉ mục, ghi minh chứng và trạng thái thật. Phần Codex rà soát để `CHƯA KIỂM TRA` cho đến khi có kết luận độc lập. Đưa file bàn giao vào commit/push theo yêu cầu Git và nhắc người dùng gửi Codex đọc mã lượt mới nhất.

Ghi báo cáo thực hiện chi tiết vào file riêng `BAO_CAO_ANTIGRAVITY.md`, rồi dẫn đúng mục/mã lượt từ file bàn giao chung. Giữ lịch sử từng lượt và không tự điền kết luận rà soát của Codex. Áp dụng từ nhiệm vụ hiện tại, không chỉ cho các nhiệm vụ tương lai.
