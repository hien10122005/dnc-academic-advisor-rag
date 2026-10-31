# Nhiệm vụ 03 cho Antigravity — Chunking và vector search baseline

Ngày giao: **31/10/2026**. Thư mục làm việc là thư mục gốc đồ án hiện tại. Đọc `PROJECT.md`, `LOGIC.md`, `ROADMAP.md` và bộ nguồn `02_Dữ Liệu Quy Chế/04_Dữ Liệu Đã Kiểm Chứng/QD580/` trước khi làm.

## 1. Kết quả rà soát bước vừa hoàn thành

- `QD580_PAGES.jsonl` có 26 bản ghi không rỗng, số trang duy nhất đủ 1–26; tất cả đang được gắn `source_verified=true`.
- `DEV_10_CAU_QD580.jsonl` có 10 ID duy nhất; `DEV_05` thiếu trường `history`, cần chuẩn hóa thành danh sách rỗng.
- Đã đối chiếu mẫu ảnh trang PDF 8, 10, 20, 21 với nội dung JSONL, chưa thấy sai lệch nội dung trọng yếu ở các trang này. Đây không phải lần kiểm tra độc lập toàn bộ 26 trang.
- Sáu Markdown quy chế cũ có SHA-256 giữ nguyên so với giá trị đã ghi ở bước trước. Các mục ROADMAP vừa được đánh dấu có đầu ra tương ứng.
- Có dữ liệu đủ để bắt đầu thử nghiệm kỹ thuật cục bộ. Tuy nhiên, chưa được dùng việc đủ 26 bản ghi hay cờ `source_verified` như bằng chứng tự động về độ chính xác tuyệt đối.

## 2. Mục tiêu và giới hạn

Sửa một số vấn đề còn lại trong báo cáo và metadata phát triển; xây module chia đoạn có nguồn; nạp ChromaDB cục bộ và tìm kiếm vector trên QĐ 580; báo kết quả baseline truy xuất.

**Chưa làm:** Gemini, sinh câu trả lời, FastAPI, Streamlit, admin, hybrid/BM25, reranking và viết lại câu hỏi bằng LLM. Các phần đó vẫn thuộc kế hoạch cuối, không bị bỏ khỏi phạm vi.

## 3. Bước A — Chỉnh đầu vào và báo cáo trước khi đánh giá

Sao lưu các file cần sửa; sửa cả dữ liệu gốc của script sinh file để chạy lại không tái tạo lỗi.

### A1. Hoàn thiện bằng chứng cho 10 ca phát triển

Thay trường nguồn một trang đơn lẻ bằng danh sách `evidence`, cho phép nhiều đoạn trên nhiều trang. Mỗi đoạn có `document_id`, phiên bản/checksum nguồn, `pdf_page`, `printed_page`, điều/khoản và trích dẫn nguyên văn có thể định vị trong nội dung trang. Giữ diễn giải/đáp án riêng khỏi trích dẫn nguồn.

Rà lại toàn bộ 10 ca, đặc biệt:

- `DEV_02`: ý bắt buộc về lịch tháng 6 không có trong đoạn trích hiện tại; bổ sung bằng chứng đúng vị trí hoặc bỏ khỏi ý bắt buộc nếu không chứng minh được.
- `DEV_05`: các điều kiện trải trang PDF 16–17; không chỉ gắn trang 16 cho toàn bộ đáp án. Bổ sung `history=[]`.
- `DEV_06`: Điều 25 nối từ trang PDF 20 sang 21, gồm ngưỡng điểm ở trang 21. Phải lưu đủ nguồn.
- `DEV_07`: bảng điểm, học lại và thi lại thuộc nhiều trang, không thể gắn tất cả vào trang PDF 9.
- `DEV_08`: không mặc nhiên coi đăng ký tối đa ở cả ba kỳ là đủ điều kiện tốt nghiệp sớm; chỉ để ý bắt buộc được nguồn hỗ trợ và phù hợp câu hỏi.
- `DEV_09`: bỏ yêu cầu khẳng định thời hạn rút môn nằm ở sổ tay/quy chế tài chính nếu nguồn thử chỉ có QĐ 580. Ca này có phần trả lời được và phần chưa đủ căn cứ; ghi nhãn rõ thay vì bắt bot bịa nguồn khác. Phần trích dẫn không được chứa nhận định của người soạn trong ngoặc vuông như thể là lời văn gốc.
- `DEV_10`: tách bằng chứng Điều 1 và quy tắc học phí trên các trang tương ứng; không yêu cầu nguồn đơn lẻ chứng minh một điều khoản không tồn tại. Mô tả giới hạn kho thử, không suy rộng toàn trường.

Nếu cần dùng câu hỏi độc lập cho ca nối tiếp để đo riêng truy xuất, thêm `retrieval_query` do người soạn biên tập và ghi rõ đánh giá đang dùng câu hỏi đã làm rõ sẵn. Không đưa đáp án hoặc nguồn chuẩn vào query và không coi đây là đánh giá module viết lại hội thoại.

### A2. Chỉnh mô tả phương pháp và số liệu

- PDF QĐ 580 hiện có **6.635.360 bytes**, không phải 11.7 MB như báo cáo chuẩn hóa đang ghi. Ghi bytes và đơn vị quy đổi rõ ràng.
- Script render được kiểm tra dùng `scale=1.5`; chưa có căn cứ gọi ảnh `580_pXX.png` là render 300 DPI. Kiểm tra script/ảnh thực tế và ghi đúng phương pháp, không chỉ sửa bằng một con số phỏng đoán khác.
- Script `tao_du_lieu_qd580.py` hiện sinh `raw/` và bản cuối từ cùng `PAGES_DATA`, đồng thời đặt cờ xác minh cho mọi trang. Sau chuẩn hóa xuống dòng, 26 bản raw trùng nội dung bản cuối. Phải mô tả đây là bản chép đầu vào được xuất từ cùng dữ liệu, không phải bằng chứng độc lập về lịch sử OCR/hiệu chỉnh. Không tạo bản raw giả để mô phỏng lịch sử trước đó.
- Giữ bản chép thủ công có đối chiếu là phương pháp hợp lệ, nhưng tách kết quả đọc nguồn của agent khỏi kiểm tra độc lập bởi người khác. Không gọi là “kiểm tra chéo độc lập” nếu chưa có.
- Rà báo cáo kiểm tra bước 1: bổ sung nhật ký đính chính không thay cho sửa nội dung sai còn trong thân báo cáo, ví dụ “song bằng ở Điều 14” hoặc tài liệu cũ “đã hết hiệu lực”. Sửa theo nguồn hiện có hoặc ghi chưa xác minh.
- Chỉ số faithfulness cần câu trả lời sinh ra, nên chưa đo ở bước vector search. Bước này đo truy xuất, không báo điểm chất lượng câu trả lời.

## 4. Bước B — Môi trường tối thiểu và kiểm tra đầu vào

Làm việc trong `05_Mã Nguồn Chương Trình/`, tạo môi trường riêng phù hợp với embedding/Chroma. Không thay Python toàn máy; kiểm tra phiên bản tương thích thay vì dùng Python 3.14 của môi trường kiểm tra theo mặc định.

- Tạo `requirements.txt` với phiên bản đã thử thành công, `.gitignore`, `.env.example` không có bí mật, README hướng dẫn chạy.
- Chỉ cài thư viện cần cho chia đoạn/embedding/vector search và kiểm tra; chưa cài toàn bộ stack tương lai.
- Có thể tải mô hình công khai từ nguồn chính thức; không cần API key hay dịch vụ trả phí. Ghi model ID/revision và thư viện sử dụng, thử kích thước nhỏ trước khi nạp toàn bộ.
- Kiểm tra JSONL có 26 trang duy nhất, nội dung không rỗng, kiểu boolean xác minh đúng; đối chiếu với CSV kiểm chứng. Từ chối dữ liệu lỗi, trùng hoặc thiếu nguồn bằng thông báo rõ ràng.
- Tính checksum PDF và bộ trang đầu vào để xác định phiên bản corpus. Không gắn version tùy ý không truy về được snapshot.
- Không chạy lại các script sinh nguồn ở mỗi lần ingestion và không đọc sáu Markdown cũ vào kho thử.

## 5. Bước C — Chunking theo cấu trúc và truy nguyên nguồn

Tạo `backend/config.py`, `backend/chunking.py`, `backend/ingestion.py`; tách chức năng đọc nguồn, chia đoạn và lưu chỉ mục. Có thể thêm `storage.py` nhỏ cho manifest/trạng thái nếu cần; chưa xây cơ sở dữ liệu nghiệp vụ hoàn chỉnh.

- Nhận `QD580_PAGES.jsonl` làm đầu vào; chỉ dùng phần đủ điều kiện kiểm chứng.
- Phân biệt `decision` (quyết định ban hành, Điều 1–3) với `regulation` (quy chế kèm theo, Điều 1–32). Không gộp hai Điều 1 vào cùng mục.
- Ghép phần điều/khoản nối qua trang trước khi chia tiếp. Giữ điều kiện, phủ định và ngoại lệ; không lấy danh sách `articles` cấp trang để gán tất cả điều đó cho mọi chunk.
- Mốc thử là 600 ký tự, overlap 100; đây là tham số khởi đầu. Bảng hoặc cấu trúc không thể chia an toàn được phép vượt mốc mềm, nhưng phải kiểm tra giới hạn token thực của embedding và ghi lý do. Không để mô hình âm thầm cắt phần cuối chunk.
- Bảng điểm phải giữ tiêu đề, hàng, cột và nhãn tích lũy/không đạt; nếu tách bảng thì lặp tiêu đề cần thiết và giữ quan hệ giữa hàng và nhãn.
- Chunk có ID ổn định từ phiên bản nguồn, vị trí và cấu hình. Cùng dữ liệu/cấu hình chạy hai lần sinh cùng ID; đổi nguồn hoặc cấu hình nhận biết được phiên bản mới.
- Metadata gồm tài liệu, phiên bản, phần văn bản, điều/khoản, trang bắt đầu/kết thúc, các đoạn nguồn cụ thể và trạng thái xác minh. Lưu vị trí/khoảng ký tự theo từng trang để kiểm chứng nội dung; nếu thêm tiêu đề cha vào chunk thì đánh dấu đó là ngữ cảnh bổ sung.
- Phần overlap cũng phải có nguồn chính xác. Không chỉ dùng trang đầu đại diện cho toàn bộ chunk nhiều trang.
- Xuất `QD580_CHUNKS.jsonl` để xem trước; có bảng đối chiếu đoạn nối trang và các trường hợp bảng. Kiểm tra không bỏ mất nội dung quy chế; phần bỏ qua như header/footer phải được liệt kê, không xóa nhầm điều khoản hoặc quyết định ban hành.

## 6. Bước D — Nạp vector và chạy truy xuất baseline A

- Dùng embedding ứng viên đã nêu trong PROJECT sau khi thử trên máy; nếu không chạy được, ghi lỗi và lý do chọn phương án thay thế, không tự tải nhiều mô hình lớn để dò ngẫu nhiên.
- Lưu ChromaDB cục bộ với metadata đúng kiểu dữ liệu thư viện hỗ trợ; thông tin nguồn phức hợp có thể lưu riêng trong manifest và liên kết bằng chunk ID.
- Dùng cùng mô hình, tiền xử lý và chiều vector lúc nạp và lúc tìm. Ghi cách tính khoảng cách và chiều tốt/xấu của điểm API, không mặc định mọi score là cosine similarity.
- Nạp hai lần cùng đầu vào không làm tăng số chunk; không trộn phiên bản embedding/chunking khác nhau trong một collection.
- Có trạng thái build và ready/failed tối thiểu cho corpus thử; chưa công bố chỉ mục chưa hoàn tất. Không yêu cầu làm toàn bộ upload/admin trong bước này.
- Tạo `backend/retrieval.py` hoặc CLI tìm kiếm; nhận query, in top 10 kèm ID, điểm, điều/khoản, trang và đoạn trích.
- Chạy bộ phát triển trên tập ca được gắn nhãn có bằng chứng phù hợp. Với ca không có đáp án đầy đủ, xuất kết quả để phân tích nhưng không gộp vào mẫu số truy xuất như một câu có đáp án chuẩn.
- Đo Hit Rate@3, MRR@10, và độ phủ bằng chứng cho câu nhiều nguồn. Ánh xạ bằng chứng chuẩn sang chunk bằng khoảng nguồn đã kiểm tra, không chỉ coi mọi đoạn cùng trang là đáp án đúng.
- Báo số ca hợp lệ, số ca lỗi/không áp dụng, kết quả từng ca và thời gian truy xuất sau khởi động. Tách tải mô hình, embedding corpus và embedding query; không gọi thời gian tìm vector là thời gian trả lời hoàn chỉnh của chatbot.
- Không bắt buộc đạt tỷ lệ nhất định bằng cách đưa đáp án vào query hay chỉnh nguồn chuẩn theo kết quả tìm kiếm. Nêu lỗi và giới hạn thực tế; 10 ca chỉ là tập phát triển.

## 7. Đầu ra và tiêu chí nghiệm thu

Trong thư mục mã nguồn:

- Các module, cấu hình môi trường tối thiểu và hướng dẫn cài/chạy.
- `evaluation/` có script đánh giá retrieval và snapshot bộ phát triển đã chỉnh nguồn.
- `evaluation/results/` có chunks/manifest, top-k từng ca, số đo và `BAO_CAO_BASELINE_VECTOR_QD580.md`; có thể đặt file dữ liệu trung gian ở `data/` nếu README chỉ rõ đường dẫn.
- Kiểm tra thiết yếu cho bảo toàn nguồn khi nối trang, bảng điểm, ID ổn định, đầu vào không hợp lệ và nạp lại không trùng. Kiểm tra trên dữ liệu thật ngoài các kiểm tra module nhỏ.
- Lệnh tái chạy thực tế, model/revision, dependencies, cấu hình máy và lỗi/giới hạn được ghi rõ. Không tạo kết quả giả nếu bước tải mô hình hoặc lập chỉ mục thất bại.

Được nghiệm thu bước kỹ thuật khi tạo được chunks truy nguyên nguồn, nạp/tìm kiếm thực tế, nạp lại không trùng và xuất kết quả phát triển tái chạy được. Nếu có lỗi nội dung nguồn, ghi nhận và sửa có căn cứ trước khi gọi tập đó là ready.

Giữ nguyên `PROJECT.md`, `LOGIC.md`, PDF gốc và sáu Markdown cũ. Được sửa bộ QĐ 580 và báo cáo kiểm tra để xử lý các vấn đề nêu trên nhưng phải sao lưu, ghi thay đổi và cập nhật script sinh dữ liệu. Không đánh dấu vấn đề của các nhóm dữ liệu khác đã xử lý.

Chỉ cập nhật ROADMAP cho phần thực sự hoàn thành, ghi đường dẫn minh chứng đầy đủ; trạng thái tổng quan mã nguồn cũng phải phản ánh đã có module nếu chạy được. Chưa đánh dấu FastAPI, Gemini, hybrid, reranking hoặc demo giao diện hoàn thành.

Cuối nhiệm vụ báo: file thay đổi; vấn đề dữ liệu đã sửa/còn mở; số trang/chunk; số ca truy xuất hợp lệ; kết quả và thời gian; bằng chứng nạp lại; lệnh tái hiện; việc tiếp theo. Nếu blocked, hoàn thành phần độc lập và nêu chính xác trở ngại, không tiếp tục tạo báo cáo thành công.
