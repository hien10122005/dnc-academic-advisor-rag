# DNC-RAG-TASK-05-R05 — Chốt evidence trực tiếp từ trace

Project: `dnc-academic-advisor-rag`; remote `https://github.com/hien10122005/dnc-academic-advisor-rag.git`. Đọc nhận xét `evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R04.md`, `KIEM_TRA_DOC_LAP_TASK05_R04.json` và **`DOI_SOAT_EVIDENCE_TASK05_R04.json`** trong thư mục mã nguồn, cùng file bàn giao/PROJECT/ROADMAP.

## Phạm vi

Chỉ sửa tài liệu/evidence/provenance. 12 readiness +10 integrity +14 focused unit tests đã qua độc lập trong phạm vi mock; không mở lại lỗi fixture hoặc đổi guard production. Không sửa code retrieval/tests/corpus/gold/raw, không thêm tính năng, không gọi lại Gemini. Chưa triển khai Task06 trong lượt này.

## 1. Sinh evidence từ dữ liệu, không gõ lại tọa độ

- Dùng `DOI_SOAT_EVIDENCE_TASK05_R04.json`: 72 hàng có mapping source thật và nguyên văn source spans của các chunk được nhắc. Danh sách14 source mapping sai và24 ranges vượt chunk đã có sẵn. Có thể dùng script local `scratch/review_task05_r04_evidence.py` làm điểm khởi đầu cho bộ kiểm tài liệu; không dùng LLM đoán source ID/offsets.
- Tạo **`evaluation/results/EVIDENCE_DEV10_TASK05_R05.jsonl`**, mỗi mode/case/point có gold index/nguyên văn, nhãn chấm, quote answer, danh sách source ID/full chunk ID, page/start/end/quote từ đúng record. Tách căn cứ gold và context thực tế; nếu gold không retrieve được thì không gán source ID giả. N/A phải có lý do.
- Source ID phải lấy từ `retrieved_contexts` của **chính mode/case đó**. Một chunk có thể là SRC-1 ở case này và SRC-3 ở case khác. Kiểm mọi cặp mapping, không chỉ14 ví dụ cũ.
- Tọa độ phải thuộc đúng source spans của context, `quote == QD580_PAGES[page].content[start:end]`. Giữ điều kiện/exceptions và bảng nhiều hàng; có thể chọn span con phù hợp khi khớp nguyên văn. Không lấy khoảng ngoài chunk rồi gọi đó là evidence đã gửi LLM.
- Các bảng nhiều hàng/điều khoản nối trang dùng nhiều spans. Nếu dẫn toàn chunk, dùng đúng list source spans (không gộp khoảng có gaps rồi tuyên bố chính xác từng ký tự).
- Rubric mới **`RUBRIC_CHAM_DIEM_DEV10_TASK05_R05.md`** dẫn sidecar theo mode/case/point; tránh lặp gõ thủ công source ID và offsets gây sai khác. Nhãn36 ý/mode, DEV06 đủ5 ý, gold DEV09-P3 và lỗi DEV07 giữ theo outputs thật; không ép tổng điểm phải bằng bản cũ nếu phát hiện cần đổi.

## 2. Kiểm tự động và đọc nội dung

- Kiểm đủ72 hàng, key duy nhất, source ID/chunk đúng context, offsets hợp lệ, quote khớp trang/chunk, source hash và raw hash không đổi. Trả về số mismatch=0 và lưu báo cáo kiểm tra, lệnh/script có thể chạy lại.
- Đọc căn cứ với từng mandatory point để bảo đảm span có nội dung hỗ trợ; structural check qua chưa tự chứng minh faithfulness. Các ý THIẾU/SAI cần trích answer/lý do và căn cứ đối chiếu, không tự đổi thành ĐẠT.
- Nếu chỉ sửa tài liệu thì **không cần chạy lại36 tests hoặc full-suite ML**. Không ghi 80/80 khi chưa có log full suite thật; giữ giới hạn về imports trên ổ đồng bộ. Không sinh lại20 live outputs để sửa rubric.

## 3. Provenance và bàn giao

- Đính chính dòng R02 trong `BAO_CAO_ANTIGRAVITY.md`: SHA triển khai R02 đúng là **`9b008ecb252482c4e8ae064d3148cb5dedf0f47e`**. `3c5a93d249300619791d4ba804165d97f6550193` là Task05-R01. Bỏ SHA không tồn tại `9b008ecb25d19e917d057778b665fa1a4e21a201`; ghi errata có ngày, không thay toàn cục lịch sử các lượt khác.
- Báo cáo **`BAO_CAO_CHOT_EVIDENCE_TASK05_R05.md`**: đối chiếu R04 -> sửa/validation/giới hạn, source/raw hash, code/script/config dùng kiểm. Không khẳng định tuyệt đối RAG chính xác hoặc mọi evidence đã đúng chỉ từ chunk IDs tồn tại.
- Cập nhật bàn giao/Anti/ROADMAP, phần Codex R05 để CHƯA KIỂM TRA. Nếu commit/push theo quy trình thì đúng repo, không force, ghi SHA từ lệnh Git thật; không tự chép/gõ đoán SHA.

Hoàn tất khi sidecar có mapping/offsets/quotes tự kiểm khớp toàn bộ và người/agent chấm đã đọc nội dung theo gold, lịch sử SHA đúng, raw/corpus/production không đổi. Sau đó Codex chốt nghiệm thu Task05 và xét Task06.
