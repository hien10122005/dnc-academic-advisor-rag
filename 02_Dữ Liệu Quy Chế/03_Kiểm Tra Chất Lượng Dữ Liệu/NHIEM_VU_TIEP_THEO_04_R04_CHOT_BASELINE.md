# DNC-RAG-TASK-04-R04 — Chốt baseline A và sửa lỗi còn lại

## 1. Đúng dự án và tài liệu đầu vào

- Project ID: `dnc-academic-advisor-rag`; môn Đồ án 2 — chuyên ngành CNTT; Trợ lý học vụ DNC.
- Git root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`.
- Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.
- Đây không phải dự án môn Điện toán đám mây. Kiểm tra root/remote trước khi sửa.
- Đọc PROJECT.md, LOGIC.md, ROADMAP.md, hai file BAO_CAO_ANTIGRAVITY.md / BAO_CAO_BAN_GIAO.md, nhiệm vụ R03 và `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R03.md`.

## 2. Mục tiêu và giới hạn

Chốt baseline A (dense retrieval + Gemini) trung thực, sửa đường trả lỗi và retry, cải thiện việc giữ điều kiện/ngoại lệ trong câu trả lời. Giữ QĐ580, 104 chunks và collection v2 hiện tại. Không xây UI, SQLite/admin, BM25, reranker hoặc multi-turn ở lượt này; không mở rộng kiến trúc. Không yêu cầu 10/10 đúng và không hardcode đáp án DEV.

## 3. Sửa public errors

- Tách public message/code khỏi chi tiết nội bộ. `/chat` và `/health` không trả raw exception, đường dẫn máy, SDK payload hoặc key.
- Kiểm tra các nhánh thiếu status/manifest, JSON hỏng và lỗi Chroma. Giữ preflight fail-closed.
- Test bằng dependency giả hoặc file tạm; không xóa/sửa kho thật để mô phỏng lỗi. Assert status/code và không lộ đường dẫn lẫn chuỗi bí mật giả.
- Đồng bộ mã HTTP quota trong code, tài liệu và tests; hiện report nói 429 nhưng class dùng 503. Chọn chính sách có lý do, không chỉ sửa bảng cho đẹp.

## 4. Sửa retry và timeout có kiểm thử

- Dùng mã HTTP/type của exception SDK/httpx thay vì tìm số trong str(exc). Chỉ retry transient đã định nghĩa: lỗi mạng có thể phục hồi, timeout, 429 và 5xx phù hợp. Lỗi lập trình ValueError/TypeError, schema và 400/401/403/404 không retry.
- Kiểm soát retry SDK và vòng ngoài để số lần gọi có giới hạn rõ. Có thể tắt retry SDK và dùng một vòng ngoài; ghi tổng attempts và backoff, không nhân retry hai tầng.
- Đặt giới hạn thời gian toàn yêu cầu rõ ràng hoặc mô tả đúng worst-case của nhiều attempts; không gọi timeout mỗi attempt là timeout tổng. Đảm bảo lỗi cuối được phân loại theo lỗi thực tế, tránh timeout cũ lấn lỗi sau.
- Smoke và generate dùng chính sách thống nhất, không báo CONNECTED chỉ vì parse được JSON rỗng/sai ping.
- Tests offline: timeout được truyền thật, 401/404/ValueError/schema chỉ 1 lần, transient có số lần đúng, hết retry trả typed error phù hợp. Mock sleep; tests không gọi API.
- Nếu mock handler được tiêm vào client có key, metadata response vẫn phải ghi mock, không gắn `is_live_llm=true` chỉ vì SDK đã khởi tạo.

## 5. Bám nguồn và chấm lại baseline

- Điều chỉnh prompt chung để giữ điều kiện, lựa chọn và ngoại lệ; khi context chưa đủ nhánh thì diễn đạt giới hạn, tránh biến một lựa chọn thành nghĩa vụ tuyệt đối. Không thêm nhánh theo DEV ID/từ khóa câu hỏi và không dùng gold làm context.
- Với DEV_07, đối chiếu thi lại/học lại và học phần bắt buộc/thay thế từ corpus. Nếu nguồn liên quan không vào top-k, phân loại thiếu retrieval; không nhét thủ công chunk đúng vào pipeline. Chưa cần xử lý hết lỗi recall ở lượt này.
- Quote giữ truy nguyên bằng spans/trang; ưu tiên câu chứa căn cứ hơn tiêu đề/header nếu có thể làm gọn. Không cắt offsets sau khi sửa chuỗi rồi giả định vẫn khớp nguyên văn. Ghi rõ preview không chứng minh toàn bộ answer.
- Tạo rubric có từng mandatory point: đạt/một phần/thiếu/sai, kèm trích answer và nguồn đối chiếu; có người hoặc agent chấm, ngày, cách chấm và giới hạn. Tách correctness/completeness, faithfulness, citation ID hợp lệ và đúng bằng chứng, hành vi từ chối.
- DEV_02/08 là câu có đáp án: từ chối là không đáp ứng, dù tránh đoán là an toàn. DEV_09 runner chưa dùng history: ghi single-turn và N/A multi-turn. Không tuyên bố đã có hội thoại.
- Không sửa gold gốc để nâng điểm. Nếu ý gold vượt câu hỏi, ghi tranh luận rubric riêng và báo cả kết quả theo gold hiện tại.

## 6. Minh chứng, đo lường và live

- Giữ nguyên artifact/report R03; thêm errata hoặc liên kết đính chính, không xóa lịch sử.
- Chạy offline tests trước. Key đã có trong `.env` được ignore, không yêu cầu người dùng gửi lại, không đưa vào báo cáo hay commit. Không kích hoạt billing hoặc tài nguyên trả phí mới.
- Smoke thành công mới chạy một lượt 10 ca live cho bản R04; nếu upstream lỗi thì báo một phần, không giả output. Không tự chạy lặp nhiều lần để chọn kết quả đẹp.
- Lưu `DNC_RAG_LIVE_DEV10_R04.jsonl` gồm run_id/thời gian, version code, prompt/config, corpus/chunks hash, câu hỏi/query thực dùng, top-k và đầy đủ retrieved chunk IDs/content/spans, output/status/citations/timing/lỗi; không key. Gold chỉ dùng sau sinh để chấm.
- Tạo bảng rubric từng ca, summary bằng script đọc artifacts; báo mẫu số, trung bình/trung vị và cold/warm rõ. Không suy ra hiệu năng tải nhiều người hoặc “0 hallucination” từ source ID hợp lệ. Nếu báo p95 thì nêu chỉ có 10 mẫu.
- Báo cáo mới `evaluation/results/BAO_CAO_CHOT_BASELINE_QD580_R04.md`: bảng đối chiếu từng phát hiện R03, các test thực sự tồn tại, số liệu tính được, ca sai còn lại và nguyên nhân/giới hạn. Chưa cần đạt tuyệt đối để nghiệm thu.

## 7. Hoàn thành và bàn giao

- Các lỗi public error/retry có test hồi quy; không còn chấm kết quả thiếu ý là 100%; phân biệt live/mock và đủ dữ liệu để kiểm tra quality.
- Toàn bộ tests qua; idempotency chạy trong thư mục tạm thay vì ghi artifact gốc. Chỉ chạy live có chủ đích ở evaluation/smoke riêng.
- Cập nhật README/ROADMAP theo đúng trạng thái; thêm R04 vào BAO_CAO_ANTIGRAVITY.md và BAO_CAO_BAN_GIAO.md; phần Codex giữ CHƯA KIỂM TRA.
- Kiểm tra git diff/staged, secrets bị ignore; commit/push repo đã chỉ định, không force. Ghi SHA triển khai, SHA bàn giao và xác nhận remote; phần chưa làm phải nêu rõ.
- Sau nghiệm thu, hướng tiếp theo là Task 05: thêm BM25 + RRF trên cùng chunks, so sánh dense/hybrid bằng cùng bộ dev; reranker sẽ là nhiệm vụ riêng. Không tự đánh dấu Task05 hoàn thành trong lượt này.
