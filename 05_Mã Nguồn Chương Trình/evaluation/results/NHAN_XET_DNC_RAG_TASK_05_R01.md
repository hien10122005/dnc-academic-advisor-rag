# Codex rà soát DNC-RAG-TASK-05-R01

- Project: `dnc-academic-advisor-rag`, Đồ án 2 — Trợ lý học vụ DNC.
- Ngày: 01/11/2026. Kết luận: **CẦN SỬA có giới hạn trước khi nghiệm thu Task05**. Có cải thiện retrieval tái lập được; không yêu cầu làm lại hybrid.
- HEAD và origin/main đã đối chiếu: `bb88f0c21c9e6a37d08abdc0732a9c73663a9a20`. Commit triển khai thật: `3c5a93d249300619791d4ba804165d97f6550193`. SHA `3c5a93d11b339ae780c1081aee3480ec8e77ce0b` trong lời tự báo bàn giao không khớp Git.

## 1. Kiểm tra đã làm

- Đọc code BM25/RRF, preflight/cache, engine trace, API, scripts đánh giá và 20 artifacts A/B. Chạy suite offline bằng Python `.venv`, key rỗng, HF/Transformers offline: **63 chạy, 0 failure/error/skip**.
- Chạy lại evaluator retrieval A/B vào **thư mục tạm**, không ghi đè artifact bàn giao. Thứ tự chunk IDs của toàn bộ 9 ca có evidence khớp ở cả hai mode; các chỉ số chất lượng khớp số liệu Anti.
- Đọc 20 JSONL: 20 cặp mode/case duy nhất; mỗi mode 10 ca; mọi record đánh dấu live, citation ID/chunk ID khớp context đã lưu. Không gọi Gemini lại trong review; đây không phải chứng thực độc lập 20 request upstream, mà là đối chiếu artifact/code cùng retrieval thật.
- Mean total engine từ artifacts: dense 3052.465ms, hybrid 1757.226ms. Mẫu nhỏ, dense có outlier; không suy ra hybrid tự làm Gemini nhanh hơn hay đã kiểm tra tải nhiều người.
- Chunks và manifest hash hiện tại khớp báo cáo: chunks `5802f176f1f603123126c49284449085bd18bdf64f3213998e081ecd01536398`, manifest `c0ceea3306e71506ceaeae17e8328423993e80967e855c6605d775a64b9c2e9b`. Python thực kiểm tra **3.14.6**, không phải 3.12 như báo cáo.
- Chặng A cải thiện: phân loại HTTP không còn dò số trong message; hạ tầng public message cố định; test idempotency cô lập; trace lấy từ luồng engine, không gọi retrieval ngoài lần sinh như R04.

## 2. Kết quả retrieval đúng cách diễn giải

| Chỉ số | Dense | Hybrid |
| --- | ---: | ---: |
| Hit@3 — ít nhất một evidence đạt coverage >=90% | 7/9 | 8/9 |
| Hit@5 — ít nhất một evidence đạt coverage >=90% | 7/9 | 9/9 |
| Mean evidence coverage@5 | 0.6368 | 0.8034 |
| Mean evidence coverage@10 | 0.8312 | 0.9143 |
| Full-case coverage@10 — mọi evidence đều >=90% | 6/9 | 7/9 |
| MRR@10 | 0.6806 | 0.6574 |

DEV02/08 được đưa nguồn cần thiết vào Top5 và artifact hybrid trả lời được; đây là tiến bộ có minh chứng. Tuy nhiên **Hit@5=9/9 không có nghĩa đủ mọi bằng chứng của 9 ca**. Evaluator dùng `any(c >= .90)`, còn mean coverage@5 chỉ 80.34%; DEV07 coverage@5 vẫn 0.25, DEV08 0.50. Các câu “độ phủ bằng chứng Top5 tuyệt đối 100%”, “bảo đảm đưa đúng dữ kiện”, “không gây ảo giác” phải đính chính. MRR giảm nhẹ phải báo là giảm, chưa có cơ sở kết luận luôn tốt hơn.

## 3. Phát hiện cần sửa

### [P1] BM25 cache chưa đối chiếu fingerprint và preflight bỏ qua chunk file bị thiếu

`VectorRetriever.bm25_index` chỉ build khi None; `indexed_fingerprint` được lưu nhưng không so với hash mới sau readiness. Khi một ingestion hoàn tất và cập nhật status/manifest/vector, cache sparse vẫn có thể giữ thế hệ cũ.

Probe dùng 104 chunks bản sao trong TemporaryDirectory: khởi tạo index, sửa một chunk thêm sentinel và cập nhật hash manifest; giả lập check_readiness thành công của thế hệ vector/status mới (không sửa DB thật). Getter vẫn trả cùng index cũ, fingerprint không khớp, search sentinel 0 hit; index mới cùng file có 1 hit. Đây là kiểm tra có dependency giả cho preflight, không phải cập nhật corpus thật. Cần so fingerprint và rebuild có kiểm soát hoặc fail-closed; kiểm tra ID set/duplicates thực sự, không chỉ hardcode số lượng 104.

Probe riêng `VectorRetriever(chunks_file_path=<đường dẫn tạm không tồn tại>).check_readiness()` với status/manifest/DB thật trả **READY**, vì bước 9 chỉ hash khi exists. Cần từ chối khi file bắt buộc bị thiếu.

### [P2] Test API hybrid phụ thuộc thứ tự chạy

Riêng `TestHybridIntegration.test_api_chat_endpoint_mode_validation` chạy độc lập: **1 fail**, dense hợp lệ nhận 503 thay vì 200. TestClient không enter lifespan, không tự inject engine; khi suite đầy đủ pass là do global engine/mock còn lại từ module trước. Cần fixture riêng và restore state, kiểm chứng nhóm hybrid chạy riêng lẫn suite đầy đủ, không cần key. Không sử dụng thông số 63/63 để kết luận độc lập các nhóm hiện tại.

### [P2] Rank/metadata hybrid và trace chưa thống nhất

RRF thay thứ tự nhưng giữ `rank` của base dense item hoặc không có rank ở item chỉ BM25. CLI retrieval in res['rank'], res['distance'], res['is_cross_page'] nên không có hợp đồng đầy đủ cho sparse-only; cần rank sau fusion đúng 1..k và metadata thống nhất, cosine nullable rõ khi không có dense score.

Engine trace chỉ giữ subset trong SourceContext; dense_rank/score, bm25_rank/score và rrf_score bị bỏ. Artifact retrieval-only có các trường này nhưng 20 trace sinh câu trả lời thì không. Thêm trường này vào debug trace để kiểm tra candidate selection/fusion của chính lần sinh, không biến fusion score thành similarity.

### [P1 về kết luận chất lượng; P2 về hoàn thiện rubric] DEV07 còn sai câu chữ/điều kiện

Hybrid answer lưu: **“từ điểm D+ trở xuống là dưới 5.0”** — sai vì D+ là 5.0–5.4. Answer đồng thời kết luận phải học lại mà không có nhánh thi lại/điều kiện môn học. Báo cáo chưa ghi lỗi ngưỡng D+ này, và mô tả “cả hai trả lời đúng ... phải học lại” quá rộng. Source ID hợp lệ không xác nhận mọi claim đúng. Chấm nội dung sai/không được hỗ trợ riêng với thiếu ý; không sửa raw output lịch sử.

`grade_ab_rubric.py` chỉ in gold/answers, không tạo bảng chấm từng ý. Báo cáo có tóm tắt điểm theo ca nhưng còn thiếu trích answer và evidence từng ý, người/agent chấm và ngày. Cần file rubric có thể kiểm tra, giữ DEV09 N/A multi-turn. Không cần LLM đạt 100% để nghiệm thu.

### [P2] Đính chính điều kiện đo và provenance

- Errata Task05 nói lượt đầu R04 đo PyTorch weights là sai: runner R04 truy xuất trước khi engine đo, nên phần nạp weights nằm ngoài engine timing; ghi đúng như review R04. Hybrid hiện tại build BM25 lazy ở request đầu, không preload startup như báo cáo mô tả.
- Metadata A/B có dirty=True và HEAD trước triển khai; chưa source hash/runtime dependency đầy đủ. Ghi giới hạn tái lập, không giả artifact đã chạy ở commit sau. Lượt mới nếu cần ghi source hash hoặc code commit sạch trước chạy.
- Không kết luận outlier DEV07 do mạng nếu không có telemetry phân biệt upstream/retry/mạng.
- Không sửa nhiệm vụ gốc/nhận xét Codex để nới tiêu chí; thêm báo cáo/errata ở file mới.

## 4. Quyết định tiếp theo

Giao Task05-R02 sửa cache/preflight, hợp đồng output/trace, cô lập tests và đính chính/chấm lại artifacts đang có. Không chạy lại mặc định 20 câu live chỉ để đổi báo cáo; dùng offline artifacts và retrieval. Nếu sửa prompt/engine ảnh hưởng generation, chạy smoke + ca cần kiểm tra, lưu lượt mới và mô tả giới hạn. Chưa giao reranker/UI/admin/multi-turn. Nhiệm vụ tiếp theo sau nghiệm thu dự kiến là reranker nhẹ, không mặc định mô hình hay hứa sẽ sửa hết DEV07.
