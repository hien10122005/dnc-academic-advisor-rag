# Codex rà soát DNC-RAG-TASK-04-R03

- Project: `dnc-academic-advisor-rag` — Đồ án 2, Trợ lý học vụ DNC.
- Ngày: 01/11/2026. Kết luận: **ĐẠT MỘT PHẦN — CẦN SỬA trước khi chốt baseline**.
- Bản kiểm tra: HEAD `a72369df1515fc91ca43e15f07f289cd0d9de7ec`, triển khai `bcb6b2088fe89e350fc2aff16c3e913f8714bff6`; remote main đã đối chiếu khớp HEAD.

## 1. Đã xác minh độc lập

- Chạy unittest discovery bằng `.venv/Scripts/python.exe`, HF/Transformers offline, đặt GEMINI_API_KEY rỗng để không gọi Gemini: **43 chạy, 0 fail, 0 error, 0 skip**.
- Phân bố thực: `test_chunking_and_sources` 5, `test_lifecycle_and_regression` 21, `test_api_and_rag` 17; tổng 3 file. Bảng 4.2 của báo cáo R03 ghi tên file/nhóm khác thực tế.
- Code đã bỏ auto-attach top-1, chặn status/schema sai và hạ trạng thái nếu có ID bịa hoặc answered không nguồn. Cấu hình nạp dotenv với override=False; mock không còn mặc định bật.
- **Một smoke độc lập tới Gemini thật thành công**, model `gemini-3.5-flash-lite`, JSON ping/pong; timeout HTTP 10 giây, SDK attempts=1. Không chạy lại 10 câu live, không lưu/in key, không sửa `.env`.
- Artifact R03 có 10 dòng: 6 answered, 3 insufficient_evidence, 1 out_of_scope. Đây là 10 ca thực thi có đầu ra, không phải 10 câu đúng.
- Không thay application code, PDF, Markdown quy chế hoặc kết quả live R03. Test idempotency có chạy lại generator; sau test Git không ghi nhận thay đổi artifact.

## 2. Lỗi cần sửa

### [P1] Chất lượng câu trả lời DEV_07 chưa được đánh giá đúng

Đầu ra R03 khẳng định điểm D không đạt nên “bắt buộc phải đăng ký học lại”. Gold mandatory_points yêu cầu xét lựa chọn thi phụ/thi lại nếu học phần có tổ chức; chỉ sau nhánh không thi lại/không đạt mới xét học lại môn bắt buộc hoặc thay thế/tương đương. Câu trả lời thiếu các điều kiện này, nhưng báo cáo lại chấm “xuất sắc”. Không thể suy ra đúng ngữ nghĩa chỉ vì source ID tồn tại.

DEV_01 thiếu ý làm tròn 1 chữ số thập phân nhưng báo 4/4. DEV_04 thiếu ý thời điểm và thủ tục đăng ký nhưng báo 4/4. DEV_05 thiếu ý lệ phí/ngoại lệ hoãn thi trong gold nhưng báo 100%. Cần chấm từng ý, và nếu gold có ý vượt phạm vi câu hỏi thì ghi nhận xét rubric minh bạch; không lặng lẽ sửa gold để tăng điểm.

DEV_02, DEV_08 là ca có đáp án trong corpus nhưng hệ thống không tìm đủ nguồn: ghi **từ chối nhầm/thiếu truy xuất**, đồng thời có thể ghi hành vi không đoán là an toàn. Không tính cả ca là đúng chỉ vì đã từ chối. DEV_09 được runner gọi bằng riêng question, bỏ history: chưa chứng minh hội thoại nhiều lượt, phải gắn nhãn single-turn hoặc N/A cho tiêu chí multi-turn.

### [P1] Typed errors vẫn làm lộ đường dẫn nội bộ

`retrieval.py` đưa self.status_file_path/self.manifest_path và exception gốc vào KnowledgeBaseNotReadyError.message. Handler của `/chat` trả nguyên exc.message, `/health` trả knr.message. Probe TestClient không lifespan với lỗi giả lập chứa `E:\private\secret-location\manifest.json` nhận HTTP 503 và đường dẫn nguyên vẹn. Chỉ đổi lớp exception chưa đủ để bảo đảm response an toàn. Dùng public message ổn định, chi tiết nội bộ chỉ dành cho log đã che bí mật.

### [P2] Retry chưa giới hạn đúng loại lỗi và chưa kiểm soát retry SDK

Probe fake SDK ném ValueError lỗi lập trình: `generate_json` gọi SDK **3 lần** khi max_retries=2, rồi mới LLMUpstreamError. Nhánh else retry mọi exception, trái yêu cầu chỉ transient. Phân loại vẫn dựa trên chuỗi str(exc), dễ nhầm mã/timeout. HttpOptions chưa chỉ định retry_options nên chưa chứng minh giới hạn retry tổng khi kết hợp SDK và vòng ngoài. Chưa có test thật cho timeout/retry trong 17 test API mặc dù docstring mô tả đã có. Cần test bằng fake transport/SDK và sleep mock, không dùng mạng.

### [P2] Số liệu và kết luận báo cáo không tái lập

Tính trực tiếp 10 dòng JSONL R03:

| Chỉ số | Giá trị thực |
| --- | ---: |
| Tổng thời gian trung bình, cả 10 | 1600.153 ms |
| Tổng thời gian trung bình, bỏ ca đầu | 1465.451 ms |
| LLM trung bình, cả 10 | 1408.123 ms |
| Retrieval trung bình, bỏ ca đầu | 62.009 ms |

Báo cáo ghi LLM 1387.6ms, retrieval 58.5ms và E2E 1.45s không ghi rõ mẫu số. Đây là mẫu rất nhỏ, không phải cam kết tốc độ sản phẩm. Không suy ra “không xảy ra ảo giác” từ việc IDs hợp lệ hoặc 10 đầu ra.

Chưa có bảng chấm từng mandatory point, người chấm, ngày, rubric; JSONL chưa lưu đầy đủ 5 retrieved contexts/query/version/prompt để tái lập đánh giá faithfulness. Quote của DEV_01 SRC-1 chỉ là tiêu đề Điều 17; SRC-5 bắt đầu header bảng, chưa trực tiếp minh họa ý được trả lời. Đây là giới hạn hữu ích của đoạn preview, không tự chứng minh sai trang; ưu tiên quote chứa bằng chứng và bảo toàn offsets khi cải thiện.

## 3. Quyết định

Đã có RAG live vận hành và tests hồi quy qua; không cần làm lại chunking/ingestion hoặc đổi model chỉ vì báo cáo thiếu sót. Giao **DNC-RAG-TASK-04-R04** sửa lỗi có giới hạn, chấm lại trung thực và chốt baseline A. Sau nghiệm thu mới giao Task 05: BM25 + RRF so sánh dense/hybrid; reranker làm ở lượt sau để giữ khối lượng vừa sức. Không yêu cầu toàn bộ 10 câu phải đúng mới được chuyển bước; lỗi retrieval còn lại được lưu làm baseline.
