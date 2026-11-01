# DNC-RAG-TASK-05-R01 — Đo đúng baseline và thêm Hybrid BM25 + RRF

## 1. Nhận diện và đầu vào

- Project ID: `dnc-academic-advisor-rag`; môn Đồ án 2, Trợ lý học vụ DNC, không phải môn Điện toán đám mây.
- Root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`.
- Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`. Kiểm tra root và remote trước khi sửa.
- Đọc PROJECT.md, LOGIC.md, ROADMAP.md, BAO_CAO_ANTIGRAVITY.md, BAO_CAO_BAN_GIAO.md, nhiệm vụ R04 và nhận xét `evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R04.md` trong thư mục mã nguồn.
- Baseline code đầu vào b68811f9aac8fd0aa479e8410cbaaafafcecc656; 104 chunks QD580, collection qd580_baseline_v2. Không thay PDF, Markdown quy chế, corpus/gold hay chunk IDs để cải thiện điểm.

## 2. Chặng A bắt buộc — sửa điều kiện đánh giá trước khi so sánh

1. Phân loại retry theo code/type có cấu trúc, không tìm số HTTP trong str(exception). Test 503 có request ID chứa 404 vẫn retry, 401 có chữ quota vẫn không retry; giữ attempts SDK=1 và giới hạn vòng ngoài. Bổ sung kiểm tra timeout thực truyền và lỗi cuối sau chuỗi lỗi hỗn hợp.
2. Dùng public messages ổn định cho lỗi hạ tầng; không phản chiếu raw message/SDK payload sang API, kể cả không có dấu slash. Test fake secret sentinel qua /health và /chat; logging không ghi key/payload chứa bí mật. Giữ HTTP/code có ích cho client.
3. Cô lập idempotency trong test thật bằng TemporaryDirectory; không ghi chunks/manifest của kho dùng chung.
4. Capture trace từ **chính lần gọi engine/LLM**: retrieved contexts, source IDs, user/system prompt và generation config. Không truy xuất thêm để dựng lại log. Có thể dùng callback hoặc kết quả debug nội bộ, tránh đưa chi tiết implementation vào API sản phẩm. Test spy xác nhận prompt lưu đúng prompt gửi và retrieve chỉ một lần ở chế độ dense.
5. Ghi run_id/thời gian, code SHA + trạng thái dirty/source hash nếu chưa commit, corpus/chunks hash, model/revision, dependency/config (không key), query và mode. Dùng perf_counter cho durations; tách startup, retrieval, fusion và generation; không gọi lượt đầu đã warm-up là cold start.
6. Tạo rubric từng mandatory point (giữ gold gốc), có đạt/một phần/thiếu/sai, trích answer và nguồn; nêu agent/người chấm, ngày và hạn chế. DEV_06 theo 5 ý gold. DEV_09 single-turn thì N/A multi-turn. Citation membership, evidence correctness và faithfulness là các tiêu chí khác nhau.
7. Thêm errata vào báo cáo R04 hoặc file riêng liên kết lại để nêu trace tái dựng, cold/warm và giới hạn metadata; giữ nguyên raw R03/R04. Không tuyên bố “đã lọc mọi token” hay “0 hallucination” chỉ từ ID hợp lệ.

Hoàn tất code/tests chặng A trước khi xây phép so sánh B. Không cần toàn bộ DEV đều đúng; cần kết quả đủ kiểm chứng.

## 3. Chặng B — Hybrid nhẹ trên cùng dữ liệu

- Giữ mode `dense` làm baseline A; thêm mode `hybrid` = dense + BM25 + Reciprocal Rank Fusion. Default hiện tại vẫn dense cho tới khi có kết quả chọn cấu hình. Không triển khai reranker ở lượt này.
- BM25 dùng đúng 104 chunks đủ điều kiện, mapping chunk_id/metadata/spans từ cùng artifact. Ghi rõ dùng content hay embedding_text; cố định cấu hình và không tự bỏ decision chunks. BM25 không cần dịch vụ hay CSDL mới.
- Tokenization thống nhất cho query/corpus: chuẩn hóa Unicode, chữ thường, tách từ/số rõ; giữ tiếng Việt có dấu, số và ký hiệu có ý nghĩa. Có thể chọn cách đơn giản có mô tả, không bắt buộc mô hình tách từ lớn. Không tạo từ điển đặc chế theo DEV/gold.
- Cố định cấu hình khởi đầu ví dụ dense top-20, BM25 top-20, RRF k=60, final top-5. Công thức sum(1/(k+rank)), rank bắt đầu 1; deduplicate theo chunk_id; tie-break ổn định. Xử lý query rỗng/không khớp sparse không đưa zero-score hits vào RRF như bằng chứng; dense vẫn hoạt động nếu sparse không có hit.
- Không cộng trực tiếp cosine similarity với điểm BM25. Lưu dense_rank/score, bm25_rank/score và fusion_score riêng; fusion_score không được giả làm cosine hay confidence. Không thêm threshold từ chối theo số chưa hiệu chỉnh.
- Preflight fail-closed áp dụng cả hai mode, xác minh BM25 và vector cùng corpus hash/chunk IDs. Build/cache BM25 ở startup theo fingerprint; không build lại mỗi câu hỏi, không trả BM25 cũ sau corpus thay đổi. Không cần pipeline quản trị mới.
- RAGEngine nhận retriever có interface thống nhất; một pipeline ghép context/citation/schema dùng cho cả A/B. Cho phép chọn mode qua CLI hoặc cấu hình rõ; nếu thêm tham số API thì validate enum, giữ client cũ tương thích. Không đổi global mode theo từng request gây ảnh hưởng request khác.

## 4. Kiểm thử và thực nghiệm

- Tests có ý nghĩa: BM25 deterministic và token query/corpus đồng nhất; RRF đúng số từ ví dụ nhỏ tính tay, tie/dedup, sparse không hit; corpus mismatch bị chặn; cả modes giữ source spans/pages; trace đúng nguồn/prompt gửi; API/CLI mode hợp lệ và không làm hỏng dense.
- Suite offline tuyệt đối không phụ thuộc Gemini. Mock transport và sleep khi kiểm retry; không xóa/sửa kho thật.
- Chạy retrieval-only A/B trước trên cùng DEV10, top-k và gold: Hit@3, MRR@10 và evidence coverage theo định nghĩa evaluator hiện tại; nêu mẫu số và ngưỡng nếu dùng. Tách câu không có evidence khỏi denominator, không chấm chỉ bằng tên Điều. Lưu rank/chunk IDs/content từng mode.
- Sau tests và smoke live qua, chạy một lượt A/B live (10 ca mỗi mode) với cùng model/prompt/generation config/final top-k và corpus; tránh lặp để chọn đáp án đẹp. Không đổi prompt riêng cho mode để tăng điểm. Ghi thứ tự chạy và hạn chế biến động mạng/LLM. `.env` đã có key; không yêu cầu gửi lại, không ghi key vào artifact/commit, không tự bật billing.
- Chấm từng ý và faithfulness có nguồn; đánh dấu từ chối nhầm của ca có đáp án, single-turn/multi-turn riêng. Phân tích DEV02/07/08 dựa trên rank và context thật, không cam kết hybrid chắc chắn khắc phục.
- So sánh độ đúng, độ phủ bằng chứng và chi phí thời gian; báo mẫu số, mean/median, warm-up, lỗi/timeouts. Không kết luận thống kê lớn từ 10 ca dev; chưa mở tập test cuối.
- Nếu upstream bị cản trở: bàn giao retrieval/tests đã làm + trạng thái một phần, không giả live và không che lỗi.

## 5. Sản phẩm và bàn giao

- Code/tests, cấu hình và README chạy dense/hybrid.
- Artifact A/B có trace thật và provenance; đặt tên mới theo Task05, không ghi đè lịch sử R04.
- `evaluation/results/BAO_CAO_HYBRID_BM25_RRF_QD580.md`: đối chiếu chặng A, cấu hình/công thức/tokenizer, retrieval A/B, rubric từng ý, latency, lỗi/giới hạn và lựa chọn cấu hình có căn cứ. Cho phép kết quả hybrid không cải thiện.
- Cập nhật ROADMAP đúng phần làm được; không đánh dấu UI/reranker/multi-turn/admin hoàn tất.
- Append DNC-RAG-TASK-05-R01 vào BAO_CAO_ANTIGRAVITY.md và BAO_CAO_BAN_GIAO.md; Codex CHƯA KIỂM TRA. Nêu riêng phần còn mở từ R04.
- Kiểm tra staged diff/secrets; commit/push repo đúng, không force. Báo SHA code chạy đánh giá, SHA bàn giao, remote và file chưa commit. Không sửa PROJECT/LOGIC để nới tiêu chí nghiệm thu.

## 6. Tiêu chí nghiệm thu

Chặng A có tests và minh chứng khắc phục; dense còn chạy như đối chứng; hybrid dùng cùng corpus và preflight, RRF có thể kiểm chứng; A/B có trace đúng và đánh giá trung thực. **Không yêu cầu chất lượng phải 100% hoặc hybrid bắt buộc tốt hơn.** Chưa thêm UI, SQLite/admin, hội thoại, reranker hoặc phạm vi dữ liệu mới trong nhiệm vụ này.
