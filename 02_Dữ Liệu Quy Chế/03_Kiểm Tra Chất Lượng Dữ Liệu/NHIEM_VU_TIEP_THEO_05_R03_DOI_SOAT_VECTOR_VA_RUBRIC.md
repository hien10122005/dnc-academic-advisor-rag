# DNC-RAG-TASK-05-R03 — Đối soát vector và hoàn thiện rubric/bằng chứng

Project ID: `dnc-academic-advisor-rag`, Đồ án 2 — Trợ lý học vụ DNC.
Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.
Root hiện tại của bản review: `G:\Other computers\My computer\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; xác minh root/remote của phiên thực hiện, không hardcode đường dẫn E/G vào chương trình.

Đọc PROJECT, LOGIC, ROADMAP, hai file bàn giao/báo cáo Anti, nhiệm vụ R02 và `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R02.md`, kèm `KIEM_TRA_DOC_LAP_TASK05_R02.json`. Giữ nguyên nhiệm vụ, nhận xét và raw outputs lịch sử.

## 1. Phạm vi

Sửa có giới hạn để nghiệm thu Task05. Giữ corpus QĐ580 104 chunks, gold DEV10, Dense mặc định và thuật toán BM25/RRF hiện có. Chưa thêm reranker, UI, admin/SQLite, rewrite/multi-turn, nguồn mới hay claim verifier. Không tối ưu theo DEV ID và không yêu cầu mô hình trả lời hoàn hảo để nghiệm thu.

## 2. [P1] Vector integrity phải được kiểm thực tế

- `check_readiness()` kiểm số lượng và tập ID **thực tế** trong Chroma so với manifest/chunks, không chỉ so metadata. Từ chối khi empty/missing/extra ID hoặc sai ID dù count không đổi.
- Kiểm schema, ID thiếu/trùng và số lượng manifest/chunks; lỗi thiếu/hỏng hoặc lệch đều về `KnowledgeBaseNotReadyError`, không công bố READY/healthy.
- Giữ fail-closed khi thiếu chunks, BUILDING/FAILED và cache invalidation BM25 đã sửa. Không hardcode count=104 trong logic integrity; dùng manifest đã kiểm hợp lệ.
- Chính sách kiểm/cache và nạp lại phải rõ, phù hợp một tiến trình local; không cần kiến trúc phân tán. Không để cache integrity che mất thay đổi ở vector store mà metadata giữ nguyên.
- Tests dùng DB/files tạm hoặc fake có hành vi rõ. Tối thiểu: đúng ID, collection rỗng, thiếu ID, dư ID, same-count-wrong-ID, manifest/chunks lỗi và API health trả 503 khi integrity fail. Không mutate DB thật để tạo ca lỗi.

## 3. [P2] Chấm lại từ nguồn thật, giữ gold

- Tạo rubric mới `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R03.md`; dùng nguyên 20 outputs cũ, không ghi đè raw/gold.
- Mỗi mode/case/point ID có gold nguyên văn hoặc dẫn chính xác index; kết quả đạt/một phần/thiếu/sai; trích answer; source ID + chunk ID thật + PDF page + source span khi áp dụng; lý do; người/agent chấm và ngày.
- Phân biệt căn cứ gold, context thực tế gửi LLM và citations được trả. Kiểm mọi full chunk ID tồn tại; faithfulness phải dựa vào context của chính record đó. Các ý từ chối/an toàn không có nguồn trích riêng phải ghi N/A có lý do.
- Sửa ít nhất 8 full chunk IDs sai mà artifact Codex liệt kê; không chỉ thay hậu tố hash bằng đoán. DEV04 nguồn thật chính là c044/c045. Dense đã retrieve c045 nhưng bỏ sót quy trình trong answer, nên phân loại lỗi generation omission.
- DEV09-P3 giữ ý gốc về thiếu căn cứ trong QĐ580; khuyên liên hệ là nhận xét thêm. DEV06 giữ 5 ý; DEV07 giữ lỗi D+ và các thiếu nhánh thi phụ/điều kiện học lại. Không bỏ ý gold vì câu hỏi ngắn; có thể nhận xét riêng về mức phù hợp của gold.
- Tính lại tổng nhãn từ bảng mới. Không coi 25/36 và 28/36 cũ là chuẩn bắt buộc phải giữ.

## 4. [P2] Báo cáo có provenance đúng

- Báo cáo mới `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R03.md`, dẫn phát hiện R02 -> sửa/test/minh chứng/giới hạn.
- Retrieval tính trên DEV01–DEV09, DEV10 loại khỏi mẫu số; ghi DEV09 single-turn/N/A năng lực hội thoại. Hit@5 Hybrid=9/9 không có nghĩa full-case/answer accuracy=100%; full-case@5 đang là 6/9. Báo MRR giảm và quy mô tập dev nhỏ.
- Ghi tên file test/số ca đúng log thực tế. Không dùng danh sách module không tồn tại. Full suite R02 có 70 test methods về cấu trúc; số ca sau sửa phải dựa vào runner.
- Ghi Python/dependencies thật của môi trường chạy, không gán dữ liệu phiên bản hiện tại cho lượt live cũ không có metadata. Giải thích Uvicorn installed/pinned nếu khác; không tự nâng/hạ toàn bộ môi trường để làm đẹp báo cáo.
- Bỏ khẳng định seed cố định nếu không có seed trong config/artifact. Nêu raw A/B dirty HEAD và giới hạn tái lập; không sửa lịch sử để nói đã chạy ở commit sạch sau này.
- Phân biệt timing runner R04 với startup API. Không kết luận outlier do mạng/warm-up khi không có phép đo phân tách.

## 5. Kiểm thử và bàn giao

- Chạy riêng test API mode, riêng file hybrid, bộ tests integrity mới và toàn suite, offline/key rỗng, không gọi Gemini thật. Cô lập và restore globals/dependencies.
- Lưu log kết quả, phiên bản/source hash và lệnh chạy. Nếu ổ đồng bộ gây chậm import, có thể dùng môi trường local phù hợp; phân biệt lỗi môi trường với lỗi tests, không tự báo 70/70 khi runner chưa hoàn tất. Focused run có stub ML phải được ghi là unit run, không phải integration thật.
- Có thể dùng thứ hạng/source spans đã lưu để tính lại metrics; nếu rerun retrieval thì ghi artifact mới hoặc thư mục tạm. Không chạy lại 20 Gemini requests chỉ để sửa báo cáo; không cần người dùng gửi lại key.
- Cập nhật README/ROADMAP đúng hiện trạng; thêm R03 vào `BAO_CAO_ANTIGRAVITY.md` và `BAO_CAO_BAN_GIAO.md`, giữ phần Codex là CHƯA KIỂM TRA. Không sửa lời tự báo cũ thành đã nghiệm thu.
- Kiểm diff/secrets; nếu thực hiện commit/push theo quy trình bàn giao thì dùng đúng repo, không force, ghi SHA thực và trạng thái remote/file chưa commit. Không tự gán SHA chưa tồn tại.

Hoàn tất khi vector/chunks/BM25 dùng cùng tập ID đã kiểm, tests lỗi integrity có thể tái hiện và qua, rubric truy nguyên đúng raw/context/gold, báo cáo có điều kiện đo và logs đúng. Sau đó chờ Codex nghiệm thu trước Task06.
