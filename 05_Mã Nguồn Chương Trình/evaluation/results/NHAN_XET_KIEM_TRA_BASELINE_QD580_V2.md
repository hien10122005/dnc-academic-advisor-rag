# Rà soát độc lập baseline QĐ 580 v2

Ngày kiểm tra: **01/11/2026**. Commit được kiểm tra: `33efe91af7532eab05fa3e1d2144f6927864d64b`.

## Kết luận

Bản v2 có tiến bộ thực chất: đã sửa lỗi cắt ngầm ở corpus hiện tại, bổ sung nguồn theo khoảng ký tự và chạy được đánh giá truy xuất. Tuy nhiên, **chưa hoàn thành toàn bộ tiêu chí nghiệm thu**: vòng đời/chặn phiên bản chỉ mục còn lỗi, revision chưa được ép khi tải mô hình, bộ chấm có lỗi định vị khi chuẩn hóa khoảng trắng và báo cáo còn số liệu không khớp artifact.

Không cần làm lại từ đầu. Sửa các mục dưới đây, thêm kiểm thử hồi quy rồi mới chuyển sang tính năng tiếp theo.

## Phạm vi và phương pháp kiểm tra

- Đọc chunking, ingestion, retrieval, bộ chấm, kiểm thử, manifest, dữ liệu, báo cáo, README và cấu hình Git.
- Chạy cả 5 kiểm thử của Antigravity. Riêng phép thử sinh lại chunk/manifest được chuyển sang thư mục tạm, không ghi đè đầu ra đang đánh giá.
- Kiểm tra độc lập giới hạn offset và độ phủ ký tự nguồn.
- Chạy lại `evaluate_collection` cho v2 trong bộ nhớ; không ghi đè hai file kết quả benchmark.
- Dùng file trạng thái tạm và mock collection/model để thử các tình huống lỗi. Không sửa/xóa/nạp lại collection thật trong các phép thử này.
- Kiểm tra remote bằng `git ls-remote origin refs/heads/main`. Không push hoặc thay đổi lịch sử Git trong đợt rà soát.

## Những phần đã đạt trên dữ liệu hiện tại

| Nội dung | Kết quả xác nhận |
| --- | --- |
| Số chunk | 104 |
| Giới hạn đầu vào | Đếm lại bằng tokenizer: tối đa 246 token, không chunk nào vượt 256 |
| Source spans | 351 khoảng khớp từng ký tự giữa trang nguồn và nội dung chunk |
| Giới hạn offset | Không phát hiện khoảng rỗng, đảo ngược hoặc vượt chuỗi |
| Overlap | 27 khoảng có nhãn và khớp nguồn |
| Bộ kiểm thử hiện có | 5/5 bài qua |
| Sinh lại chunk/manifest | Mã băm giữ nguyên khi ghi vào thư mục tạm |
| Tập ca phát triển | Snapshot trong thư mục mã nguồn khớp mã băm file nguồn |
| Kết quả truy xuất v2 | Chạy lại cho đúng các chỉ số đã lưu |
| GitHub | `main` trên remote trùng commit local `33efe91af7532eab05fa3e1d2144f6927864d64b` |

Độ phủ nguồn độc lập: phần chưa được đưa vào spans gồm đoạn đầu trang PDF 2 (tiêu đề quy chế, dòng ban hành và tên Chương I), tổng 149 ký tự không phải khoảng trắng. Không phát hiện khoảng nội dung quy chế khác bị bỏ trong phép kiểm tra hợp các spans hiện tại. Cần ghi đây là phần bỏ qua có chủ đích, thay vì khẳng định mọi ký tự nguồn đều nằm trong chunks.

Các chỉ số chạy lại theo rubric hiện tại:

| Chỉ số | Kết quả |
| --- | ---: |
| Hit@1 | 0.5556 |
| Hit@3 | 0.7778 |
| Hit@5 | 0.7778 |
| Hit@10 | 1.0000 |
| MRR@10 | 0.6806 |
| Độ phủ bằng chứng trung bình@10 | 0.8312 |
| Tỷ lệ ca mọi bằng chứng đạt ngưỡng >=90%@10 | 0.6667 |

Đây là kết quả trên 9 ca được bộ chấm gắn nhãn grounded trong tập phát triển, không phải chất lượng tổng quát của chatbot hoặc kết quả kiểm thử cuối.

## 1. [P1] Ingestion chưa chặn phiên bản không tương thích và vẫn báo READY khi số lượng sai

Vị trí: `backend/ingestion.py`, hàm `ingest_corpus`, phần `get_or_create_collection` và trước khi đặt trạng thái READY.

Mặc dù đã ghi `corpus_fingerprint`, `model_revision` và `chunks_sha256`, code không so sánh các giá trị này với metadata collection đã tồn tại. Upsert không xóa ID cũ khi bộ dữ liệu thay đổi. Sau đó code đặt READY vô điều kiện sau khi đọc `collection.count()`, không kiểm tra đủ và đúng tập ID.

Đã tái hiện qua mock, không tác động DB thật:

- Collection hiện có fingerprint `OLD`, đầu vào fingerprint `NEW`.
- Đầu vào có 1 chunk, collection trả 2 bản ghi sau upsert.
- Code vẫn trả `status=READY`, `corpus_ready=true`.

**Yêu cầu sửa:** kiểm tra tương thích trước khi ghi; cô lập phiên bản bằng collection/snapshot khác hoặc từ chối rõ ràng. Trước READY phải xác nhận đúng tập ID, số lượng, hash và cấu hình. Không chỉ kiểm tra bằng số lượng vì tập ID sai có thể có cùng kích thước. Thêm kiểm thử cùng phiên bản, đổi nguồn/cấu hình, ID cũ còn sót và nạp lỗi giữa chừng. Không xóa collection baseline cũ để vượt lỗi.

## 2. [P1] Readiness đang cho qua trạng thái thiếu/hỏng/khác collection và bị bỏ qua khi cache

Vị trí: `backend/retrieval.py::check_readiness` và property `collection`.

Kết quả thử trực tiếp hàm với đường dẫn trạng thái tạm:

| Trạng thái thử | Kết quả hiện tại |
| --- | --- |
| File không tồn tại | Chấp nhận |
| File có JSON hỏng | Chấp nhận do exception bị nuốt |
| READY của collection khác và fingerprint khác | Chấp nhận |
| FAILED | Từ chối |

Ngoài ra, readiness chỉ được kiểm tra khi `_collection is None`. Một retriever đã cache collection có thể tiếp tục truy vấn sau khi lần nạp khác chuyển trạng thái sang BUILDING/FAILED. Trạng thái cũng là một file chung, chưa gắn an toàn với collection đang hỏi.

**Yêu cầu sửa:** thiếu/hỏng/trạng thái sai phải chặn với lỗi rõ ràng; đối chiếu đúng collection, fingerprint, model và manifest trước truy vấn. Kiểm tra mỗi request hoặc quản lý snapshot đã công bố bất biến một cách rõ ràng; không dùng việc đã cache object như chứng cứ còn READY. Thêm các ca thử nêu trên và READY→BUILDING sau lần truy vấn đầu.

## 3. [P2] Revision mới được ghi trong metadata, chưa được ép khi tải model/tokenizer

Các lời gọi thực tế vẫn là:

- `AutoTokenizer.from_pretrained(EMBEDDING_MODEL_CANDIDATE)` trong chunking và test token.
- `SentenceTransformer(model_name)` trong ingestion.
- `SentenceTransformer(self.model_name)` trong retrieval.

Không lời gọi nào truyền `revision=MODEL_REVISION`. Vì vậy cache hiện tại có thể cho kết quả đúng, nhưng máy khác hoặc lần tải sau có thể lấy revision khác trong khi manifest vẫn ghi cùng commit hash.

**Yêu cầu sửa:** dùng revision nhất quán tại mọi chỗ tải và kiểm tra revision thực tế đã resolve. Cách tiền xử lý/normalize, model ID/revision, chiều vector và distance phải tương thích giữa build/query. Bổ sung kiểm tra để không có trường hợp ghi revision A nhưng thực tế tải B.

## 4. [P2] Chuẩn hóa khoảng trắng làm định vị evidence về sai đầu trang

Vị trí: `evaluation/evaluate_retrieval.py::find_evidence_span_on_page`, nhánh trả `0, len(clean_quote)` khi chỉ khớp chuỗi đã chuẩn hóa.

Đã tái hiện với nguồn:

```text
HEADER LONG ENOUGH

TARGET  alpha
 beta END
```

Trích dẫn `TARGET alpha beta END` nằm sau tiêu đề, nhưng hàm trả `[0, 21]`. Khi đưa một chunk chỉ chứa vùng đầu trang vào hàm coverage, kết quả bị chấm 1.0 dù không có bằng chứng đích.

**Yêu cầu sửa:** ánh xạ các ký tự chuỗi chuẩn hóa trở lại offset gốc chính xác hoặc dùng evidence offsets đã kiểm chứng. Không có ánh xạ chắc chắn thì báo evidence không hợp lệ, không đoán offset 0. Thêm ca kiểm tra whitespace/newline, ký tự Unicode và nguồn lặp lại nhiều lần.

**Giới hạn ảnh hưởng hiện tại:** tất cả trích dẫn của bộ phát triển hiện tại khớp nguyên văn, nên nhánh lỗi này không được dùng trong lần chạy lại. Không vì lỗi tiềm ẩn này mà kết luận các số truy xuất hiện tại không tái lập được; chúng đã được tái lập, nhưng hàm chưa an toàn với trường hợp đã nêu.

## 5. [P2] Thống kê và cách gọi kết quả trong báo cáo vẫn sai

Tính trực tiếp từ nội dung artifact hiện tại:

| Thuộc tính | Báo cáo v2 | File thực tế |
| --- | ---: | ---: |
| Ký tự trung bình/chunk | 514.8 | 544.10 |
| Trung vị ký tự | 527.5 | 600.5 |
| Ký tự nhỏ nhất | 109 | 58 |
| Ký tự lớn nhất | 836 | 839 |
| Chunk phần quyết định | 4 | 6 |
| Chunk nối trang | 6 | 19 |

Code cũng còn có 1 chunk 246 token, dù báo cáo gọi 240 là giới hạn cứng. Điều này không vi phạm giới hạn 256 của model trên corpus hiện tại, nhưng cần thống nhất mốc mục tiêu và giới hạn thực sự được kiểm tra.

Các điểm phương pháp cần sửa:

- “Mọi bằng chứng đạt ngưỡng 90%” không có nghĩa thu hồi đầy đủ 100% mọi ý. Có thể mất một từ phủ định hay con số quan trọng trong phần còn thiếu. Ghi chính xác là tỷ lệ phủ ký tự theo ngưỡng, và kiểm tra các ý bắt buộc/số liệu riêng khi đánh giá câu trả lời.
- Không lấy nghịch đảo MRR để gọi là thứ hạng đúng trung bình.
- Hit@10=100% nghĩa mọi ca có ít nhất một bằng chứng đạt ngưỡng, không phải trả lời đúng hoàn toàn cả 9 ca.
- Chưa có p95, số liệu môi trường/phép đo và số lần lặp đầy đủ như kế hoạch; 10 query chỉ là phép thử phát triển nhỏ, không đủ để gọi hệ thống phản hồi siêu tốc trong mọi tình huống.
- Sinh bảng thống kê tự động từ artifact để tránh lặp lỗi chép số liệu.

## Git và tính tái lập

- Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.
- Xác nhận commit local và remote `main` cùng là `33efe91af7532eab05fa3e1d2144f6927864d64b`.
- Working tree sạch trước khi tạo file nhận xét này. Quét mẫu token phổ biến trên file tracked không phát hiện chuỗi khớp; đây không phải chứng nhận không thể còn bí mật.
- `.gitignore` có loại `.env` nhưng chưa bao phủ `.env.local`, `.env.production` bằng mẫu `.env.*`; nên bổ sung ngoại lệ giữ `.env.example`.
- Chưa thử cài lại toàn bộ dependencies trên máy sạch. Việc chạy được trong `.venv` hiện có không tự chứng minh hướng dẫn cài đặt hoạt động trên mọi phiên bản Python/OS.

## Việc Antigravity cần làm tiếp

1. Sửa kiểm tra tương thích và readiness trước khi thêm thành phần AI mới.
2. Ép revision thực khi tải model/tokenizer; sửa ánh xạ offset khi chuẩn hóa whitespace.
3. Bổ sung kiểm thử hồi quy cho các lỗi đã tái hiện, dùng thư mục/collection tạm để không làm hỏng baseline.
4. Chạy lại test và retrieval; giữ các kết quả đo cũ có nhãn phiên bản, không giả định số mới phải tăng.
5. Sinh lại bảng báo cáo từ dữ liệu thật, điều chỉnh các kết luận quá mức và đồng bộ README/ROADMAP.
6. Commit/push bản sửa theo yêu cầu GitHub đã có; báo SHA cuối và kết quả xác nhận remote. File nhận xét này mới được tạo tại local, chưa nằm trong commit đã kiểm tra.
