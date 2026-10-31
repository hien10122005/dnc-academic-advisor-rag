# Nhận xét kiểm tra baseline QĐ 580

Ngày kiểm tra: 31/10/2026. Phạm vi: báo cáo baseline, module chunking/ingestion/retrieval/evaluation, corpus và các kết quả đã lưu. Kiểm tra bằng môi trường `.venv` hiện có, chỉ đọc kho Chroma và truy vấn; không nạp lại, không ghi đè kết quả gốc, không sửa code ứng dụng hoặc ROADMAP.

## Kết luận

**Đã có pipeline vector chạy thực tế, nhưng chưa đủ điều kiện nghiệm thu toàn bộ nhiệm vụ 03 hoặc dùng các chỉ số hiện tại làm baseline cuối.** Cần sửa các lỗi nguồn, giới hạn token và chấm bằng chứng rồi nạp/đánh giá lại. Không cần thêm tính năng mới để giải quyết các vấn đề này.

## Phần đã xác nhận

- Tái tạo chunking trong bộ nhớ từ nguồn hiện tại sinh đúng 70 ID như file đã lưu.
- SHA-256 file chunk thực tế trùng manifest: `ba12332c8f1227c42abb16a290f56034c94721680617ff34b7e3b1fd72099ce2`.
- Collection `qd580_baseline_a` có 70 bản ghi, metadata dùng khoảng cách cosine và model ứng viên đã khai báo.
- Tải được mô hình từ cache với chế độ offline, truy vấn thật trả về top-k và điểm. Các kiểm tra này không cần Gemini hay mạng.
- Không chạy lại ingestion lần hai trong đợt rà soát này, nên chưa xác nhận độc lập thời gian nạp hoặc toàn bộ kết luận idempotency trong báo cáo.

## 1. [P1] Chunk vượt giới hạn đầu vào của embedding

Mô hình đang chạy có `max_seq_length=256`. Đếm tokenizer trên `embedding_text`, bao gồm tiêu đề ngữ cảnh, cho thấy **24/70 chunk vượt giới hạn**, lớn nhất **683 token**. Thử xử lý chunk `qd580_reg_p03_d03_e0facc1e` dài 438 token thực tế cho tensor đầu vào kích thước `[1, 256]`.

Module chia đoạn chỉ gộp các paragraph theo mốc mềm; không chia tiếp một paragraph dài. Vì thế việc cài mốc 600 ký tự chưa ngăn được cắt nội dung ở bước embedding. Các chunk lớn nhất hiện là văn bản thường, không chỉ bảng cần giữ nguyên.

**Cần sửa:** kiểm soát token thực sau khi thêm context prefix, chia tiếp văn bản dài theo cấu trúc; với bảng cần giữ quan hệ nhãn/cột và có cách chia an toàn nếu quá giới hạn. Thêm kiểm tra chứng minh mọi đoạn được đưa vào model không bị cắt ngầm. Không kết luận nguyên nhân DEV_02 chỉ là tên trường lấn át trước khi thử lại sau sửa.

## 2. [P1] Overlap bị ghi sai trang, thiếu vị trí nguồn

Ở `backend/chunking.py`, sau khi lấy overlap từ chunk trước, `cur_pages` được thay bằng trang của block hiện tại. Nguồn của phần overlap không được giữ lại.

Ví dụ thực tế: `qd580_reg_p09_d07_f5db66ee` khai báo nguồn chỉ trang PDF 9, nhưng có dòng “phải đăng ký học các học phần dự định theo hướng dẫn của cố vấn học tập với điều kiện đăng ký:” thuộc trang PDF 8. Có các trường hợp tương tự ở trang 3→4, 4→5, 5→6, 15→16, 16→17.

Toàn bộ 70 chunk hiện không có `source_spans`. Manifest cũng không có danh sách `chunks` mà retriever đang cố đọc; truy vấn thực tế trả `source_spans=[]`. `page_sources` chỉ giữ số trang, không có khoảng ký tự như nhiệm vụ yêu cầu.

**Cần sửa:** truyền vị trí nguồn xuyên suốt quá trình ghép/tách/overlap; lưu offset theo trang, phân biệt context thêm vào với nội dung gốc; kiểm tra rằng từng phần trả ra có thể trích lại từ đúng trang đã khai báo. Đồng bộ manifest và retriever.

## 3. [P1] Hàm chấm có thể nhận bằng chứng sai là đúng

`evaluation/evaluate_retrieval.py::is_evidence_in_chunk` cho phép:

- Khớp chỉ 80 ký tự đầu hoặc cuối của trích dẫn dài.
- Khớp theo tên điều khoản dù đoạn trích không nằm trong chunk.

Đã tái hiện bằng ca tối thiểu: evidence và chunk cùng trang, cùng tên điều, nhưng nội dung hoàn toàn khác nhau; hàm vẫn trả `True`. Hành vi này không phù hợp mô tả trong báo cáo rằng phải khớp cả trang, điều và trích dẫn.

**Cần sửa:** ánh xạ bằng chứng bằng nguồn/offset và đơn vị bằng chứng rõ ràng. Bằng chứng dài có thể chia thành các ý cần thiết hoặc được phủ bởi nhiều chunk, nhưng không được coi một đuôi câu chung là toàn bộ bằng chứng. Chấm riêng điều kiện đủ của câu nhiều nguồn. Thêm ca kiểm tra cùng điều nhưng khác khoản/nội dung phải không được tính đúng.

Các giá trị Hit Rate, MRR và coverage hiện lưu được tính từ hàm này; chưa xác nhận chúng là các chỉ số đánh giá đúng theo tiêu chí bằng chứng. Không khẳng định toàn bộ kết quả đều sai, nhưng phải chạy lại sau khi sửa.

## 4. [P1] Ngưỡng từ chối đề xuất không được dữ liệu hiện có hỗ trợ

Báo cáo ghi các ca hợp lệ có top similarity khoảng 0.55–0.78, từ đó đề xuất ngưỡng 0.45–0.48. Tuy nhiên, `top_k_results.jsonl` thực tế có:

| Ca | Top similarity lưu thực tế |
| --- | ---: |
| DEV_03 | 0.4118 |
| DEV_07 | 0.2525 |
| DEV_08 | 0.3258 |
| DEV_10 — thiếu căn cứ cho đáp án được hỏi | 0.4058 |

Ngưỡng 0.45 sẽ loại ít nhất ba ca hợp lệ nêu trên. DEV_10 còn có điểm cao hơn DEV_07/08, nên một mẫu âm không chứng minh có ranh giới phân tách an toàn.

**Cần sửa:** bỏ kết luận “chặn an toàn” và “cơ sở vững chắc” cho ngưỡng này. Chỉ xem threshold là giả thuyết cần hiệu chỉnh trên tập phát triển đa dạng hơn, đo cả từ chối nhầm và chấp nhận nhầm. Retrieval đơn thuần chưa chứng minh bot biết từ chối hoặc không hallucinate.

## 5. [P2] Báo cáo và trạng thái chưa khớp dữ liệu/code

Thống kê lại trực tiếp từ `QD580_CHUNKS.jsonl`:

| Thuộc tính | Báo cáo | Thực tế file |
| --- | ---: | ---: |
| Trung bình ký tự nội dung/chunk | 396.4 | 793.93 |
| Trung vị | 381 | 726 |
| Nhỏ nhất | 109 | 28 |
| Lớn nhất | 808 | 2371 |
| Chunk phần quyết định | 4 | 6 |

Định nghĩa phép đo ở đây là `len(content)`, không gồm context prefix. Trường `char_count` trong dữ liệu khớp cách đếm này. Báo cáo phải sinh thống kê từ artifact thực tế và ghi rõ cách đo.

Các điểm khác:

- ID hiện dựa vào hash nội dung rút gọn, phần văn bản, trang đầu và số điều; chưa chứa đầy đủ fingerprint nguồn/cấu hình như mô tả.
- Ingestion chỉ upsert ID hiện tại, chưa từ chối collection khác phiên bản/model hoặc xử lý ID cũ còn sót khi corpus thay đổi. Cùng nguồn nạp hai lần không trùng chưa chứng minh an toàn khi cập nhật phiên bản.
- `INGESTION_STATUS.json` chỉ ghi READY cuối lần chạy thành công; chưa có vòng đời build/failed và kiểm tra readiness tại retriever. Không có trường `corpus_ready: true` như ROADMAP đang dẫn.
- Báo cáo không ghi commit revision cụ thể của mô hình; “199 weights tensors” không phải revision tái lập.
- Không thấy file kiểm tra tự động cho các tiêu chí nguồn, nối trang, token và idempotency trong thư mục mã nguồn đã quét.
- Bảng tiến độ tổng quan vẫn ghi Tuần 2 chưa có minh chứng, trái phần checklist đã đánh dấu. Một số mục checklist cũng mô tả chức năng chưa hiện thực đủ.
- Không suy ra thứ hạng đúng trung bình bằng cách lấy nghịch đảo MRR. Không khẳng định hybrid chắc chắn sửa triệt để lỗi trước khi đo.

## Thứ tự xử lý đề xuất

1. Sửa chunking: giới hạn token, vị trí nguồn và overlap; bổ sung các kiểm tra thực chất.
2. Sửa ánh xạ/chấm bằng chứng; rà lại eligibility của ca có đáp án một phần như DEV_09.
3. Làm rõ fingerprint, cô lập phiên bản collection và trạng thái build/ready/failed; bảo vệ dữ liệu baseline cũ trước khi tạo phiên bản mới.
4. Tạo lại chunks, nạp lại đúng phiên bản, kiểm tra không trùng và truy vấn thực tế.
5. Chạy lại bộ phát triển, sinh thống kê/báo cáo từ artifact, sửa ROADMAP theo kết quả thật.

Hoàn thành các việc này trước khi triển khai hybrid, reranking hoặc phần sinh câu trả lời. Giữ kết quả lần cũ như bản thử có giới hạn thay vì xóa hoặc trình bày nó là baseline đã được nghiệm thu.

## Yêu cầu bổ sung của người dùng — Đưa dự án lên GitHub

Sau khi sửa các vấn đề và chạy kiểm tra lại, Antigravity thực hiện commit và push dự án vào repository người dùng đã chỉ định:

**https://github.com/hien10122005/dnc-academic-advisor-rag.git**

Đây là yêu cầu thực hiện trong nhiệm vụ, không chỉ viết hướng dẫn. Chỉ báo đã push khi có kết quả thành công và xác nhận được commit trên remote. Nếu gặp trở ngại xác thực hoặc quyền repository, báo chính xác trở ngại và giữ nguyên phần việc đã hoàn thành.

### 1. Phạm vi repository và chuẩn bị

- Đặt Git root tại thư mục gốc đồ án đang chứa `PROJECT.md`, `LOGIC.md`, `ROADMAP.md` và thư mục `05_Mã Nguồn Chương Trình`, để giữ cấu trúc đường dẫn tương đối của chương trình.
- Trước khi khởi tạo, kiểm tra repository hiện có bằng `git rev-parse --show-toplevel`, `git status`, remote và nhánh. Không tạo repository lồng bên trong thư mục mã nguồn; nếu phát hiện cấu trúc Git khác dự kiến thì kiểm tra trước khi thao tác, không xóa `.git`.
- Tạo hoặc cập nhật README ở Git root với tiêu đề `# dnc-academic-advisor-rag`; giữ nội dung có ích đã có, không lặp tiêu đề bằng cách chạy `echo >> README.md` nhiều lần.
- README mô tả đề tài, phạm vi, cấu trúc, môi trường, cách cài/chạy chunking, ingestion và đánh giá, dữ liệu cần chuẩn bị, số liệu sau sửa và giới hạn hiện tại. Chưa mô tả chatbot/giao diện như tính năng đã có.
- Commit mã nguồn, kiểm tra tự động, tài liệu dự án, dữ liệu văn bản nguồn đã chuẩn bị cho bản thử và các kết quả/báo cáo nhỏ cần thiết để tái hiện. Chỉ đưa lên các tài liệu được phép chia sẻ.
- Tạo `.gitignore` ở Git root trước khi stage. Loại môi trường ảo, cache Python/mô hình, trọng số tải về, ChromaDB/SQLite được sinh khi chạy, log, `.env` và các biến thể chứa bí mật, ảnh render trung gian, `scratch/`, bản ZIP sao lưu và thư mục `backup_b*`. Giữ `.env.example` không có bí mật.
- PDF gốc và các file nhị phân lớn không tự động đưa vào commit đầu; ghi cách chuẩn bị đúng vị trí trong README. Không chuyển sang hosting/dịch vụ lưu trữ khác để tải những file này lên trong nhiệm vụ.
- Kiểm tra staged diff và danh sách file trước commit, tránh lộ API key, token, mật khẩu quản trị hoặc thông tin xác thực. Không in bí mật ra terminal/báo cáo. Không dùng `git add .` khi chưa kiểm tra phạm vi file và ignore.

### 2. Commit và push

Áp dụng chuỗi người dùng cung cấp theo trạng thái thực tế:

```powershell
# Chạy tại Git root; chỉ init nếu chưa có repository đúng phạm vi.
git init
# Stage các đường dẫn đã kiểm tra, gồm README, .gitignore, code và tài liệu cần thiết.
git add README.md .gitignore
# Thêm các đường dẫn còn lại sau khi kiểm tra, không chỉ commit README.
git diff --cached --stat
git diff --cached --check
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/hien10122005/dnc-academic-advisor-rag.git
git push -u origin main
```

- Đây là khung lệnh cho repository mới. Nếu đã có commit thì dùng thông điệp phản ánh thay đổi thật, không giả làm lần khởi tạo đầu.
- Nếu đã có `origin` đúng URL thì giữ và không chạy lại `remote add`; nếu khác URL, không tự ghi đè một remote không liên quan.
- Kiểm tra remote đã có lịch sử hay chưa trước push. Không force-push, xóa nhánh hoặc ghi đè lịch sử để vượt lỗi; giữ lịch sử hiện có và xử lý khác biệt có kiểm soát.
- Dùng phiên đăng nhập Git/GitHub đã có. Không ghi token trong URL remote, README hoặc code; không tự đổi danh tính Git toàn máy.

### 3. Minh chứng hoàn thành

- Ghi URL repository, nhánh được push, commit SHA và thông điệp commit.
- Kiểm tra `origin/main` khớp commit dự định push, đối chiếu với remote bằng `git ls-remote origin refs/heads/main` và kiểm tra trạng thái working tree.
- Báo rõ file còn thay đổi hoặc chưa được push nếu có; không sửa thêm file rồi tuyên bố tất cả đã lên remote.
- Cập nhật đầu việc Git tương ứng trong ROADMAP trước commit nếu đã đủ minh chứng local; chỉ ghi xác nhận push sau khi remote thực sự nhận commit. Nếu cần ghi xác nhận vào file sau push thì commit/push bổ sung và báo SHA cuối cùng.
