# DNC-RAG-TASK-05-R04 — Chốt regression tests và bằng chứng

Project `dnc-academic-advisor-rag`; remote `https://github.com/hien10122005/dnc-academic-advisor-rag.git`. Xác minh root/remote thực tế của phiên. Đọc nhiệm vụ R03, nhận xét `evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R03.md`, artifact `KIEM_TRA_DOC_LAP_TASK05_R03.json` trong thư mục mã nguồn và hai file bàn giao/báo cáo Anti cùng PROJECT/LOGIC/ROADMAP.

## 1. Phạm vi cần giữ

P1 production vector integrity của R02 đã được khắc phục qua probe; giữ count/ID validation và fail-closed. Chỉ sửa fixture/test isolation và bằng chứng/provenance. Không làm lại BM25/RRF, không thêm reranker/UI/admin/multi-turn/nguồn mới, không sửa corpus/gold/raw outputs. Dense tiếp tục mặc định. Không nới guard để test cũ qua.

## 2. Cập nhật regression và cô lập test

- `TestRetrieverReadinessVerification` trong `tests/test_lifecycle_and_regression.py` phải có fixture thật sự READY: manifest có danh sách chunks hợp lệ và collection có đúng ID `c1` cùng embedding giả xác định. Mọi artifacts/DB đều ở thư mục tạm.
- Tái hiện và sửa 2 errors (valid preflight, chuyển BUILDING sau READY) và 3 assertion failures (status fingerprint, Chroma metadata fingerprint, disk hash) đã ghi trong review. Giữ assertions kiểm nguyên nhân; mỗi negative case chỉ sửa một yếu tố trên fixture hợp lệ.
- Loại cơ chế cài MagicMock Chroma/SentenceTransformer vĩnh viễn trong `sys.modules` ở đầu `test_vector_integrity.py`. Nếu cần runner cô lập để tránh imports ML, đặt stub chỉ trong tiến trình runner đó và ghi rõ unit scope; full suite và integration không được âm thầm dùng stub.
- Test duplicate IDs dùng **cùng số lượng** để chạm guard duplicate, thay vì thất bại sớm do count 105. Bổ sung các biến thể schema/chunks còn thiếu nếu báo cáo tuyên bố đã kiểm.
- Chạy riêng class readiness, vector integrity, hybrid, riêng API mode và full suite trong môi trường offline/key rỗng. Dùng cùng phiên bản/config, lưu log và phân biệt real Chroma với fake/unit scope. Nếu import quá chậm, có thể dùng môi trường local tương thích; không ghi tất cả tests qua khi chỉ đếm methods hoặc runner chưa xong.

## 3. Hoàn thiện evidence của rubric

- Tạo rubric/sidecar mới cho R04, giữ raw outputs và gold. Đối chiếu **mode/case/point -> source ID -> chunk ID -> PDF page -> offset `[start,end)`**, kèm quote answer và lý do chấm. Phần refusal dùng N/A có lý do.
- DEV08 Hybrid P1: `c035` là **SRC-3**, không phải SRC-2.
- DEV05 cả hai mode P3: context **SRC-1 c070** có lệ phí và ngoại lệ hoãn thi ở PDF p17 `[0,282)`; answer thiếu là **generation omission**. Giữ nhãn THIẾU nếu vẫn đúng nội dung.
- DEV05 giới hạn D+/C+ là **Điều 18 khoản 6**; không thi lại/lệ phí là **khoản 5**, nối trang16–17. DEV06 ngưỡng5.5 là **Điều25 khoản2**, p21 `[90,160)`; chuẩn đầu ra ngoại ngữ/CNTT có phần nối p21 `[0,89)` trong c084. Không dựng điểm/khoản không có trong nguồn.
- Giữ DEV06 đủ5 ý, gold DEV09-P3, claim error D+ của DEV07 và thiếu nhánh thi phụ/điều kiện học lại. Kiểm toàn bộ refs/mapping, không chỉ sửa vài ví dụ. Không ép tổng điểm phải giữ nguyên nếu có phát hiện cần đổi nhãn.

## 4. Bàn giao và lịch sử

- Sửa các dòng SHA `523c512...` bị chèn nhầm vào Task04-R03/R04 và Task05-R01 trong bàn giao, và Task05-R02 trong báo cáo Anti. Đối chiếu Git để khôi phục lịch sử; thêm errata, không thay hàng loạt SHA các lượt cũ. SHA này thuộc triển khai Task05-R03.
- Thêm **mục báo cáo R03 còn thiếu** trong lịch sử `BAO_CAO_ANTIGRAVITY.md`, dẫn báo cáo kỹ thuật đã có; sửa anchor cho khớp heading thực. Sau đó thêm mục R04 riêng, không ghi đè R03.
- Báo cáo mới `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R04.md`: từng phát hiện -> sửa/test/log/giới hạn; nêu test methods khác test results, actual environment và dirty/provenance thật. Không gọi lại 20 Gemini requests chỉ để sửa tài liệu.
- Cập nhật README/ROADMAP/bàn giao nhất quán; Codex R04 để CHƯA KIỂM TRA. Nếu commit/push theo quy trình thì đúng repo, không force, ghi SHA đã tồn tại và trạng thái remote/file chưa commit; không lộ secrets.

Hoàn tất khi regression và test isolation có minh chứng qua, vector guard giữ nguyên, rubric có nguồn/offset đúng và lịch sử bàn giao không còn gán nhầm commit. Chờ Codex nghiệm thu trước Task06; không cần LLM đạt100% mọi DEV.
