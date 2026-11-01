# PROJECT.md — Tổng quan và phạm vi đồ án

> **Định danh dự án:** `dnc-academic-advisor-rag` — trợ lý tra cứu quy chế học vụ DNC, môn Đồ án 2 chuyên ngành CNTT.  
> **Git root:** `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`  
> **Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.

File nhiệm vụ và báo cáo phải cùng định danh trên. Từ 01/11/2026, lượt bàn giao mới dùng tiền tố `DNC-RAG-TASK-`; giữ nguyên các mã lịch sử cũ có dẫn chiếu. Không dùng chung nội dung bàn giao/nhiệm vụ với dự án Điện toán đám mây hay checkout khác.

> Cập nhật: **31/10/2026**. Phương án đã thống nhất: giữ phạm vi dữ liệu rộng và lõi RAG; giảm phần tài khoản, quản trị và độ phức tạp hội thoại; đánh giá bằng 60–80 câu có nguồn chuẩn.
> Đây là tài liệu thiết kế và kế hoạch, không phải xác nhận các chức năng đã được lập trình. Xem `LOGIC.md` để biết luồng xử lý; xem `ROADMAP.md` để biết tiến độ và tiêu chí hoàn thành.

## 1. Thông tin cơ bản

| Thuộc tính | Nội dung |
| --- | --- |
| Tên đề tài | Xây dựng hệ thống trợ lý ảo hỗ trợ tra cứu quy chế học vụ ứng dụng kỹ thuật Retrieval-Augmented Generation (RAG) |
| Môn học | Đồ án 2 — Chuyên ngành Công nghệ Thông tin |
| Trường | Đại học Nam Cần Thơ (DNC) — Trường Công nghệ Số & Trí tuệ Nhân tạo |
| Lớp | DH23TIN — Khóa 2023 |
| Học kỳ | Học kỳ 1, năm học 2026–2027 |
| Thời gian thực hiện | 26/10/2026–03/01/2027, khoảng 10 tuần |
| Khoảng nộp bài | 04/01/2027–10/01/2027, kế thừa kế hoạch cũ; đối chiếu thông báo chính thức trước khi nộp |
| Báo cáo dự kiến | 30–50 trang không kể phụ lục; thể thức theo QĐ 309/QĐ-ĐHNCT ngày 08/12/2016 và hướng dẫn được trường cung cấp |
| Gặp giảng viên | Kế hoạch tối thiểu 4 lần; mỗi lần lưu biên bản và góp ý |

## 2. Mục tiêu và sản phẩm

Sinh viên hỏi bằng tiếng Việt tự nhiên; hệ thống tìm nội dung trong kho tài liệu của trường, giải thích ngắn gọn và đưa nguồn để kiểm chứng. Khi thiếu căn cứ hoặc thiếu thông tin áp dụng, bot từ chối kết luận hoặc hỏi lại.

Mục tiêu cụ thể:

1. Kế thừa và kiểm tra dữ liệu hiện có, giữ dấu vết về tài liệu gốc, điều khoản và trang.
2. Xây dựng pipeline nạp dữ liệu và pipeline hỏi đáp có hybrid search, reranking, viết lại câu hỏi có điều kiện.
3. Có website chat, xem nguồn và quản trị tài liệu tối giản.
4. Giảm câu trả lời không có căn cứ; không cam kết loại bỏ hoàn toàn hallucination.
5. Đánh giá truy xuất, câu trả lời, trích dẫn, hành vi hỏi lại/từ chối và tốc độ bằng thực nghiệm.

Sản phẩm bàn giao: mã nguồn và hướng dẫn chạy; kho dữ liệu có nguồn; website; bộ đánh giá 60–80 câu và kết quả so sánh; báo cáo, sơ đồ, slide và minh chứng demo.

## 3. Phạm vi dữ liệu và hiện trạng

**Giữ phạm vi dữ liệu của bản cũ**, không thu hẹp chỉ còn quy chế đào tạo:

| Nhóm | Nội dung |
| --- | --- |
| 01 | Tổng quan, danh bạ và thông tin liên hệ DNC |
| 02 | Quy chế đào tạo, đăng ký học phần, điểm, học lại, cảnh báo và thôi học |
| 03 | Công tác sinh viên, điểm rèn luyện và quy định liên quan |
| 04 | Khen thưởng, kỷ luật và nội quy lớp học |
| 05 | Học phí, miễn giảm và học bổng |
| 06 | Chuẩn đầu ra và điều kiện tốt nghiệp |

Hiện trạng kiểm tra thư mục ngày 31/10/2026:

- Có 3 PDF: sổ tay sinh viên 2026–2027; QĐ 580 về quy chế đào tạo; tài liệu hướng dẫn giảng viên.
- Có 6 file Markdown trong `02_Dữ Liệu Quy Chế/02_Văn Bản Đã Làm Sạch (Text)`.
- Thư mục `05_Mã Nguồn Chương Trình` có các thư mục con nhưng chưa có file chương trình.
- Roadmap cũ ghi nhận đã thu thập và làm sạch dữ liệu. Kế thừa kết quả này, nhưng việc đối chiếu đầy đủ với PDF, ánh xạ số trang và phạm vi áp dụng chưa được xác nhận trong lần cập nhật này.
- Sổ tay từng được ghi nhận là PDF scan; cần kiểm tra text layer và xử lý OCR/trích xuất đã có trước khi nạp. Chưa có kết quả kiểm tra PDF mới trong lần cập nhật này.

Đưa dữ liệu vào lần lượt: kiểm chứng một nhóm để chạy thử toàn luồng, sau đó mở rộng đủ 6 nhóm. Mỗi đoạn dùng để trả lời phải truy về được nguồn; nội dung chưa đối chiếu được không đưa vào kho đang phục vụ hỏi đáp. Không tự dựng số quyết định, trang, ngưỡng điểm hoặc thông tin liên hệ.

## 4. Đối tượng sử dụng và chức năng

| Đối tượng | Quyền và chức năng |
| --- | --- |
| Người tra cứu, chủ yếu là sinh viên | Không cần đăng nhập; hỏi đáp; xem đoạn nguồn và PDF; hỏi nối tiếp trong phiên; xóa hội thoại hiện tại; gửi phản hồi đơn giản |
| Quản trị viên (`admin`) | Đăng nhập; tải tài liệu; cập nhật thông tin nguồn; xem trạng thái xử lý/lỗi; kích hoạt hoặc ngừng sử dụng tài liệu đã lập chỉ mục; xem phản hồi và thống kê kỹ thuật tối thiểu |

Người tra cứu là đối tượng nghiệp vụ, không cần tài khoản `student` trong cơ sở dữ liệu. Admin được cấp sẵn cho bản đồ án, không có đăng ký công khai. Backend kiểm tra quyền của mọi thao tác quản trị, không chỉ ẩn nút ở giao diện.

### Chức năng bắt buộc

- Hỏi đáp có trích dẫn gắn với đoạn tài liệu thực sự truy xuất được.
- Hybrid search: vector + BM25; reranking có bật/tắt phục vụ thực nghiệm.
- Viết lại khi câu nối tiếp phụ thuộc ngữ cảnh; câu rõ ràng được truy xuất trực tiếp.
- Dùng tối đa **3 lượt hỏi–đáp hoàn chỉnh gần nhất** làm ngữ cảnh hội thoại; thêm giới hạn độ dài đầu vào.
- Lịch sử hiển thị và ngữ cảnh chỉ tồn tại trong phiên; không khôi phục lịch sử theo tài khoản.
- Hỏi lại nếu thiếu dữ kiện ảnh hưởng đáp án; từ chối kết luận khi không đủ căn cứ.
- Admin quản lý tài liệu tối giản, đồng bộ trạng thái sử dụng giữa vector search và BM25.
- Đo thời gian, lưu cấu hình và kết quả đánh giá.

### Ngoài phạm vi bản bàn giao

Đăng ký sinh viên, quên/đổi mật khẩu tự phục vụ, quản lý nhiều cấp nhân sự, lịch sử liên thiết bị, bộ nhớ hội thoại dài hạn, quy trình duyệt nhiều cấp, kết nối portal/điểm cá nhân, tự động giải quyết mọi mâu thuẫn văn bản, ứng dụng di động riêng và kiến trúc microservices.

## 5. Kiến trúc và công nghệ

```text
Trình duyệt → Streamlit (chat / quản trị)
                    ↓ HTTP API
              Một backend FastAPI
              ├── Xác thực admin và quản lý tài liệu
              ├── Ingestion: trích xuất → kiểm tra nguồn → chia đoạn → lập chỉ mục
              ├── Query: viết lại có điều kiện → hybrid → rerank → sinh câu trả lời
              └── Phản hồi và đo lường
                    ├── ChromaDB: vector, đoạn văn, metadata
                    ├── BM25: chỉ mục từ khóa trên cùng tập đoạn hợp lệ
                    ├── SQLite: admin, tài liệu, trạng thái, phản hồi, số đo tối thiểu
                    ├── Thư mục PDF và dữ liệu đã chuẩn hóa
                    └── Gemini API
```

| Thành phần | Lựa chọn dự kiến |
| --- | --- |
| Ngôn ngữ và môi trường | Python, pip + venv; Python 3.11 là mốc dự kiến, kiểm tra tương thích khi cài |
| Giao diện / backend | Streamlit / FastAPI + Uvicorn |
| Điều phối | LangChain; dùng module nhỏ, không thêm lớp trừu tượng khi chưa cần |
| Đọc PDF | PyMuPDF hoặc pdfplumber; OCR bổ sung khi cần |
| Embedding | Sentence Transformers; `bkai-foundation-models/vietnamese-bi-encoder` là ứng viên ban đầu |
| Truy xuất | ChromaDB + BM25; hợp nhất thứ hạng và loại trùng |
| Reranker | Cross-Encoder phù hợp tiếng Việt; chọn sau khi thử trên máy thực tế |
| Sinh câu trả lời / viết lại | Gemini API; tên mô hình cấu hình qua biến môi trường, chốt sau thử nghiệm |
| Lưu dữ liệu ứng dụng | SQLite riêng; không sửa trực tiếp các file nội bộ ChromaDB |
| Thực nghiệm | Script Python và dữ liệu CSV/JSONL; notebook tùy nhu cầu |

Ghi rõ phiên bản thư viện đã chạy được trong `requirements.txt`; không dùng nhãn “Latest” làm cấu hình tái lập. Không chốt lại Gemini 1.5 Flash hay SDK trong code mẫu cũ nếu chưa kiểm tra khả dụng. Khóa API và thông tin đăng nhập đọc từ môi trường hoặc `.env`, không ghi cứng trong code và không nộp kèm bí mật thật.

Frontend gọi backend qua API, không import mô hình hay gọi `rag_engine` trực tiếp. Tải embedding/reranker một lần khi backend khởi động. Một máy chạy giao diện, backend và kho dữ liệu là cấu hình demo ban đầu; gọi Gemini cần mạng. Hosting công khai chọn sau khi bản local ổn định.

## 6. Quy tắc chất lượng và hiệu năng

- Trích dẫn chỉ hiển thị trường đã xác minh. Phân biệt trang PDF với số trang in trên tài liệu; không suy ra số trang từ thứ tự đoạn Markdown.
- Metadata và prompt giúp kiểm soát nhưng không chứng minh câu trả lời đúng. Cần đối chiếu nội dung trả lời với đoạn nguồn.
- Không có căn cứ: “Mình chưa tìm thấy đủ thông tin trong các tài liệu hiện có để trả lời chắc chắn câu hỏi này.”
- Khi có nguồn khác nhau, trình bày căn cứ và giới hạn; không tự suy ra văn bản ưu tiên chỉ từ tên file hoặc ngày mới hơn.
- Không tự xưng là trợ lý chính thức của trường khi chưa được công nhận; đây là sản phẩm đồ án hỗ trợ tra cứu.
- Mục tiêu trải nghiệm ban đầu: bắt đầu thấy nội dung sau khoảng 2–4 giây, hoàn tất câu thông thường khoảng 4–8 giây. Đây là **mục tiêu chưa đo**, không phải cam kết; báo cáo cả trung vị và p95, tách khởi động lạnh.
- Streaming chuyển tiếp nội dung khi mô hình sinh; không tạo hiệu ứng gõ sau khi đã nhận toàn bộ câu trả lời rồi coi là giảm thời gian xử lý.

## 7. Đánh giá thực nghiệm

Dự kiến **75 ca đánh giá**, được phép điều chỉnh trong khoảng **60–80** trước khi chốt bộ kiểm thử. Có câu hỏi trực tiếp, diễn đạt đời thường, tổng hợp nhiều đoạn, nối tiếp, thiếu dữ kiện và ngoài phạm vi/không có đáp án. Đặc tả chia nhóm, nguồn chuẩn, cách chấm và cách tách tập xem `LOGIC.md`, mục 7.

So sánh 3 cấu hình: **A — vector**, **B — vector + BM25**, **C — hybrid + reranking**. Giữ cùng dữ liệu, câu hỏi, mô hình sinh và các tham số ngoài phần được so sánh. Reranking là chức năng phải triển khai để thực nghiệm; cấu hình mặc định cuối cùng chọn dựa trên chất lượng và thời gian đo được.

Đo Hit Rate@3, MRR trên nhóm có bằng chứng chuẩn; độ bám nguồn, đúng đáp án, mức liên quan, chất lượng trích dẫn trên nhóm phù hợp; hành vi hỏi lại/từ chối trên nhóm riêng. Không gộp câu ngoài phạm vi vào mẫu số truy xuất. Chưa có kết quả thực nghiệm.

## 8. Tổ chức tài liệu và mã nguồn dự kiến

Giữ nguyên 8 thư mục hiện có: kế hoạch; dữ liệu; đề cương/báo cáo; slide; mã nguồn; tham khảo; hình/sơ đồ; biên bản. Bản Word hiện có nằm trong `03_Đề Cương & Báo Cáo/01_Đề Cương Chi Tiết`; chưa được cập nhật tự động theo các file Markdown.

```text
05_Mã Nguồn Chương Trình/
  backend/
    main.py, config.py       # API, cấu hình
    auth.py, storage.py      # admin, SQLite
    ingestion.py            # trích xuất, nguồn, chia đoạn, lập chỉ mục
    retrieval.py            # vector, BM25, hợp nhất, rerank
    rag_engine.py           # viết lại có điều kiện, prompt, trả lời, citations
  frontend/
    app.py, api_client.py    # giao diện, gọi API
  evaluation/               # bộ câu hỏi, script, cấu hình và kết quả
  data/                     # SQLite và chỉ mục BM25 được tạo khi chạy
  chroma_db/                # dữ liệu vector được tạo khi chạy
  notebooks/                # thử nghiệm tùy chọn
  requirements.txt, .env.example, .gitignore, README.md
```

Đây là cấu trúc dự kiến, không phải các file đã tồn tại. Chi tiết đầu việc theo tuần và trạng thái thật ở `ROADMAP.md`.

## 9. Báo cáo và tiến độ tổng quan

Đề xuất 4 chương nội dung: (1) Tổng quan; (2) Cơ sở lý thuyết; (3) Phân tích và thiết kế; (4) Hiện thực và đánh giá; sau đó kết luận, tham khảo và phụ lục. Chương thiết kế phải phản ánh hai đối tượng sử dụng, phiên chat ngắn hạn và một backend. Chương đánh giá trình bày ba cấu hình, số liệu thật, lỗi và giới hạn.

Ghi chép thiết kế và thí nghiệm từ đầu; tuần 7–9 tập trung hoàn thiện báo cáo. Kiểm tra lại thể thức và yêu cầu bàn giao theo tài liệu chính thức trước khi định dạng bản cuối.

## 10. Nhật ký thay đổi phạm vi — 31/10/2026

- Giữ 6 nhóm dữ liệu, hybrid search, reranking và hội thoại có viết lại câu hỏi.
- Chỉ admin đăng nhập; người tra cứu không có tài khoản hay lịch sử lâu dài.
- Giới hạn 3 lượt ngữ cảnh, viết lại có điều kiện, quản trị tải lên/trạng thái/kích hoạt đơn giản.
- Đánh giá 60–80 ca có nguồn chuẩn và so sánh A/B/C; bỏ kế hoạch chỉ 30 câu.
- Thay khẳng định tuyệt đối và số đo chưa thực hiện bằng yêu cầu kiểm chứng, mục tiêu và tiêu chí nghiệm thu.
- Bản gốc ba file được lưu trong ZIP tại `scratch/document_backups/` trước khi sửa; các file dữ liệu quy chế không thay đổi.

## 11. Báo cáo bàn giao sau mỗi nhiệm vụ — áp dụng từ 01/11/2026

Theo yêu cầu người dùng, Antigravity phải đọc và cập nhật `BAO_CAO_BAN_GIAO.md` tại Git root sau mỗi nhiệm vụ hoặc mỗi lượt sửa theo phản biện. Thêm lượt mới, giữ lịch sử, báo đầu ra, file thay đổi, lệnh/kết quả test, mock/thật, lỗi còn mở, báo cáo chuyên môn và commit/push thực tế. Cập nhật ROADMAP nhất quán và dẫn mã lượt bàn giao trong lời nhắn cuối.

Codex dùng file này làm đầu mối rà soát. Phần tự báo của Antigravity và kết luận kiểm tra của Codex được ghi riêng; chưa kiểm tra thì không tự đánh dấu đã nghiệm thu. Quy tắc này chỉ bổ sung cách phối hợp, không thay đổi phạm vi sản phẩm đã chốt.

Báo cáo thực hiện chi tiết của Antigravity được ghi riêng, theo từng mã lượt, trong `BAO_CAO_ANTIGRAVITY.md`. `BAO_CAO_BAN_GIAO.md` chỉ giữ tóm tắt/liên kết và phần rà soát, không yêu cầu sao chép toàn bộ báo cáo hai lần. Sau mỗi nhiệm vụ phải cập nhật cả báo cáo chi tiết và chỉ mục bàn giao.
