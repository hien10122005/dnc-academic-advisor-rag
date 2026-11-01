# DNC-RAG-TASK-05-R02 — Chốt hybrid và bằng chứng thực nghiệm

## Nhận diện

Project ID `dnc-academic-advisor-rag`, Đồ án 2 — Trợ lý học vụ DNC; không phải dự án Điện toán đám mây.
Root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`.
Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.

Đọc PROJECT.md, LOGIC.md, ROADMAP.md, hai file bàn giao/báo cáo Anti, nhiệm vụ Task05-R01 và `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R01.md`. Xác nhận root/remote. Giữ nguyên nội dung nhiệm vụ và nhận xét gốc; nếu khác ý thì ghi phản hồi đối chiếu ở báo cáo mới.

## Mục tiêu

Sửa các lỗi có phạm vi hẹp để nghiệm thu dense/hybrid. Không thêm UI, SQLite/admin, rewrite/multi-turn, cross-encoder, corpus mới hay dịch vụ mới. Không tối ưu theo từng DEV ID, không sửa gold/PDF/chunks để tăng điểm. Giữ mặc định dense trong lượt này.

## 1. Cache và readiness phải đồng bộ

- Thiếu chunk file, manifest/status lỗi hoặc hash/ID set không khớp phải từ chối. Không bỏ qua disk hash chỉ vì file không tồn tại.
- So indexed_fingerprint BM25 với thế hệ corpus đã qua preflight trên mỗi luồng lấy cache; nếu đổi thì rebuild an toàn hoặc fail-closed có hướng dẫn rõ. Không trả BM25 cũ sau khi vector/status/manifest mới đã READY.
- Xác minh duplicate IDs và ID set của BM25 so với vector/chunks; kiểm tra số lượng theo manifest, không chỉ `len==104`. Việc hiện tại có 104 chunks vẫn là dữ liệu baseline, không được thay corpus.
- Tests dùng thư mục/DB tạm hoặc dependency giả rõ ràng: thiếu chunks, cached generation cũ nhưng preflight generation mới hợp lệ, duplicate/mismatch, BUILDING/FAILED. Không mutate DB thật. Nêu rebuild/cache concurrency policy đơn giản, không thêm kiến trúc phân tán.

## 2. Hợp đồng kết quả và trace

- Kết quả fusion có rank cuối đúng 1..k; giữ dense_rank và bm25_rank riêng. Item chỉ sparse vẫn có metadata cần cho CLI/API/citation, cosine/distance thiếu thì biểu diễn rõ nullable thay vì giả độ tin cậy.
- Kiểm thử item sparse-only đứng trước dense-only, rank sau fusion, tie/dedup và CLI hybrid không KeyError. Trace của chính lần generate lưu dense/bm25 rank-score và rrf_score riêng, cấu hình top20/top20/k60/final5.
- Validate mode ở engine/CLI/API; không âm thầm fallback mode lạ hoặc hybrid không được hỗ trợ thành dense rồi log hybrid.
- Nếu muốn preload BM25 ở startup thì làm gọn và test; nếu giữ lazy thì sửa mô tả/timing đúng lazy. Không bắt buộc đổi kiểu startup chỉ để đẹp báo cáo.

## 3. Kiểm thử phải tự đứng độc lập

- Test API hybrid tự quản engine/mock hoặc lifespan và restore mọi global/dependency sau test. Không dựa vào model/mock của module trước.
- Chạy riêng file hybrid, riêng test mode và toàn suite, đều offline, key rỗng, không request Gemini thật. Không viết test chỉ kiểm chuỗi báo cáo; tập trung lỗi đã tái hiện.

## 4. Đính chính số đo và chấm chất lượng

- Giữ nguyên 20 outputs Task05-R01. Tạo errata và báo cáo mới, không ghi đè raw artifacts để giấu lỗi.
- Diễn giải Hit@5 là ít nhất một evidence >=90% span, không phải mọi evidence, không phải accuracy. Nêu mean coverage@5 0.8034; tính full-case coverage@5 nếu cần từ nguồn trace thật và gold, không suy ra từ Hit@5. Báo cả MRR giảm.
- Chấm lại DEV07: câu “D+ trở xuống là dưới 5.0” sai; phân biệt claim sai, thiếu nhánh thi lại và nhánh học lại thiếu điều kiện. Ghi faithfulness theo context thực sự được gửi, không chỉ ID membership. Có thể sửa prompt chung để tránh suy diễn, không regex đáp án hay chèn gold/correct chunk theo DEV.
- Tạo file rubric từng mandatory point cho 20 bản ghi: mode/case/point ID, gold, đạt/một phần/thiếu/sai, trích answer, nguồn kiểm tra (chunk/page/span), lý do và agent/người chấm/ngày. DEV06 giữ 5 ý, DEV09 single-turn/N/A multi-turn. Nếu ý gold vượt câu hỏi, ghi nhận xét riêng và vẫn báo điểm theo gold hiện tại.
- Ghi đúng Python/dependencies thực tế; sửa SHA triển khai sai ở handover bằng errata. Ghi rõ artifacts dirty HEAD giới hạn tái lập, không giả chạy ở commit chưa tồn tại. Mọi lần chạy mới lưu source hash/code version/config không bí mật.
- Sửa errata R04: nạp weights nằm ở retrieval ngoài engine timing; không mô tả ngược. Giới hạn mẫu 10 dev, sequential A/B và outlier phải nêu; không khẳng định outlier do mạng khi không có log đo phân biệt.

## 5. Chạy lại vừa đủ và bàn giao

- Ưu tiên offline tests, tái chạy retrieval vào artifact phiên bản mới/thư mục tạm và regrade dữ liệu live có sẵn. Không mặc định gọi lại 20 Gemini requests để chỉ sửa báo cáo.
- Nếu đổi prompt/logic sinh thì smoke trước rồi chạy ca có liên quan, lưu run mới riêng, giữ kết quả cũ. Nếu muốn kết luận A/B mới toàn bộ thì phải có lượt paired tương ứng; không trộn hai prompt/version rồi báo so sánh công bằng. Không cần đạt 100% mọi DEV để nghiệm thu.
- Key đã có `.env` bị ignore; không yêu cầu gửi lại, không log/commit key và không tự bật billing.
- Báo cáo mới: `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R02.md`, kèm rubric/errata và bảng từng phát hiện Codex -> sửa/test/artifact/giới hạn.
- Cập nhật README/ROADMAP đúng mức; append DNC-RAG-TASK-05-R02 vào BAO_CAO_ANTIGRAVITY.md và BAO_CAO_BAN_GIAO.md; phần Codex để CHƯA KIỂM TRA. Không tự nghiệm thu.
- Kiểm tra diff/staged/secrets, commit/push repo đúng không force; nêu SHA thực `git rev-parse`, remote, code chạy đánh giá và file còn chưa commit. Không sửa các nhận xét lịch sử của Codex.

Hoàn thành khi cache/readiness và output có tests tái hiện rồi qua, nhóm tests độc lập qua, rubric/báo cáo phản ánh đúng lỗi và độ đo, artifact nguồn giữ nguyên. Sau đó mới xét Task06 reranker nhẹ; chưa tự triển khai ở lượt này.
