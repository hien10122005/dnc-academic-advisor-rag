# DNC RAG — Báo cáo bàn giao đồ án trợ lý học vụ

> **Project ID:** `dnc-academic-advisor-rag`  
> **Môn học:** Đồ án 2 — Chuyên ngành CNTT, Đại học Nam Cần Thơ.  
> **Git root:** `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`  
> **Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git`  
> **Nhiệm vụ 04:** RAG tra cứu QĐ 580 bằng FastAPI và Gemini. File này không phải bàn giao môn Điện toán đám mây.

**Xác định đúng dự án trước khi ghi:** kiểm tra thư mục làm việc, `PROJECT.md` và Git remote khớp định danh trên. Nếu khác, xác định lại đúng checkout trước khi sửa, chạy tác vụ ghi hoặc commit. Không lấy kết quả của một dự án khác điền vào đây.

**Mã nhiệm vụ từ nay:** dùng tiền tố `DNC-RAG`, ví dụ `DNC-RAG-TASK-04-R02`. Lượt lịch sử `TASK-04-R01` bên dưới thuộc đồ án RAG này, được giữ nguyên để bảo toàn báo cáo; các lượt mới ghi mã có tiền tố và dẫn lượt cũ nếu là bản sửa. Không tạo một lượt R01 khác cho cùng lần bàn giao.

Thiết lập ngày **01/11/2026**, theo yêu cầu của người dùng.

Đây là đầu mối để Antigravity báo cáo sau mỗi nhiệm vụ và để Codex tìm đúng đầu ra khi rà soát. File này không thay thế báo cáo chuyên môn, ROADMAP hoặc kết quả kiểm thử; phải liên kết tới các minh chứng đó.

**Bổ sung cách dùng:** Antigravity ghi báo cáo thực hiện chi tiết trong `BAO_CAO_ANTIGRAVITY.md`. File bàn giao này giữ chỉ mục, tóm tắt, liên kết tới đúng mã lượt và phần Codex rà soát. Trong mẫu mục A bên dưới, có thể thay các bảng chi tiết bằng liên kết tới báo cáo cùng mã lượt; không cần chép hai bản đầy đủ. Các quy tắc giữ lịch sử, minh chứng và phân biệt tự báo/kiểm tra vẫn áp dụng.

## 1. Quy tắc sử dụng bắt buộc

### Antigravity thực hiện

1. Đọc file này trước khi bắt đầu nhiệm vụ mới, cùng PROJECT và file giao nhiệm vụ.
2. Thêm một mục vào cuối phần **Lịch sử bàn giao**, theo mẫu bên dưới, khi kết thúc mỗi nhiệm vụ hoặc bàn giao dở vì trở ngại. Không xóa hoặc ghi đè lịch sử các nhiệm vụ trước.
3. Mỗi lần sửa theo phản biện, tạo một lượt bàn giao mới với cùng mã nhiệm vụ và số lượt tăng dần, ví dụ `DNC-RAG-TASK-04-R01`, `DNC-RAG-TASK-04-R02`. Ghi rõ nhận xét nào đã sửa và nhận xét nào còn mở; tôn trọng lượt lịch sử đã tồn tại dưới mã cũ.
4. Cập nhật bảng chỉ mục để người đọc tìm được lượt mới nhất. Nội dung báo cáo phải phản ánh phần thực sự chạy được, không chỉ kế hoạch hay code đã viết.
5. Gắn đường dẫn tương đối từ Git root tới code, test, báo cáo và kết quả; dùng tên test/lệnh cụ thể. Không dán toàn bộ log dài vào file chung.
6. Phân biệt test mock/offline với kết nối dịch vụ thật; nêu môi trường, phiên bản dữ liệu/model và số lượng ca. Không dùng tỷ lệ kiểm thử để cam kết sản phẩm đúng tuyệt đối.
7. Ghi rõ việc chưa làm, lỗi còn tồn tại, điều kiện chưa kiểm tra và trở ngại cần người dùng xử lý. Không tự ghi kết luận nghiệm thu thay cho người rà soát.
8. Không đưa API key, token, mật khẩu, `.env` thật hoặc dữ liệu nhạy cảm vào báo cáo.
9. Cập nhật ROADMAP và các báo cáo liên quan nhất quán. Trong lời nhắn cuối cho người dùng, nêu mã bàn giao và nhắc Codex đọc file này.
10. Nếu nhiệm vụ có yêu cầu Git, commit/push cả báo cáo bàn giao và tài liệu được phép chia sẻ. Ghi **SHA commit triển khai** đã tồn tại; không cần cố ghi SHA của chính commit chứa dòng báo cáo đó. Xác nhận trạng thái remote bằng kết quả thực tế, không tự nhận đã push khi chỉ commit local.

### Codex rà soát

- Đọc lượt bàn giao mới nhất, đối chiếu minh chứng và chạy kiểm tra thích hợp.
- Ghi nhận xét trong mục riêng của cùng lượt hoặc liên kết tới báo cáo phản biện; không sửa lời tự báo cáo của Antigravity thành kết quả đã được xác minh.
- Phân biệt: đã đọc báo cáo, đã kiểm tra code, đã chạy test và đã kiểm chứng tích hợp thật.
- Khi chưa rà soát, trạng thái luôn là `CHƯA KIỂM TRA`. Việc Antigravity ghi hoàn thành không tự động thành đã nghiệm thu.

File là kênh bàn giao qua thư mục chung. Việc ghi file không tự gửi thông báo tới một phiên chat khác; người dùng chỉ cần nhắn Codex đọc lượt bàn giao mới.

## 2. Quy ước trạng thái

| Người ghi | Trạng thái | Ý nghĩa |
| --- | --- | --- |
| Antigravity | `HOÀN THÀNH — CHỜ KIỂM TRA` | Tự báo đã đạt các tiêu chí, có minh chứng, chờ rà soát |
| Antigravity | `HOÀN THÀNH MỘT PHẦN` | Có đầu ra nhưng còn mục chưa thực hiện hoặc chưa kiểm chứng |
| Antigravity | `BỊ CẢN TRỞ` | Ghi chính xác điều kiện ngăn phần còn lại và việc độc lập đã hoàn thành |
| Codex | `CHƯA KIỂM TRA` | Chưa có kết luận rà soát cho lượt này |
| Codex | `ĐẠT` | Các tiêu chí trong phạm vi đã giao đã được kiểm tra phù hợp |
| Codex | `ĐẠT CÓ ĐIỀU KIỆN` | Nêu cụ thể điều kiện/giới hạn và phần được phép chuyển bước |
| Codex | `CẦN SỬA` | Có lỗi hoặc thiếu minh chứng ảnh hưởng nghiệm thu |

## 3. Chỉ mục bàn giao

| Mã lượt | Ngày bàn giao | Nhiệm vụ | Antigravity tự báo | Codex rà soát | Đường dẫn báo cáo chính |
| --- | --- | --- | --- | --- | --- |
| `TASK-04-R01` | 01/11/2026 | 04 — RAG cơ bản qua FastAPI và Gemini | `HOÀN THÀNH MỘT PHẦN` | `CHƯA KIỂM TRA` | [Báo cáo RAG cơ bản QĐ 580](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md) |
| `DNC-RAG-TASK-04-R02` | 01/11/2026 | 04 — RAG cơ bản qua FastAPI và Gemini | `HOÀN THÀNH MỘT PHẦN` | `CẦN SỬA` | [Báo cáo chi tiết BAO_CAO_ANTIGRAVITY.md](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-04-r02--rag-co-ban-qua-fastapi-va-gemini) |
| `DNC-RAG-TASK-04-R03` | 01/11/2026 | 04 — Hoàn thiện citation, cấu hình an toàn và đánh giá RAG Gemini Live | `HOÀN THÀNH — CHỜ KIỂM TRA` | `ĐẠT MỘT PHẦN — CẦN SỬA` | [Báo cáo RAG Live R03](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_RAG_LIVE_QD580_R03.md) và [BAO_CAO_ANTIGRAVITY.md](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-04-r03--hoan-thien-citation-va-gemini-live) |
| `DNC-RAG-TASK-04-R04` | 01/11/2026 | 04 — Chốt baseline A, phân loại lỗi & khử rò rỉ đường dẫn, kiểm soát retry SDK và chấm lại kết quả trung thực | `HOÀN THÀNH — CHỜ KIỂM TRA` | `ĐẠT MỘT PHẦN — TASK05 CÓ ĐIỀU KIỆN` | [Báo cáo chốt Baseline A R04](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_CHOT_BASELINE_QD580_R04.md) và [BAO_CAO_ANTIGRAVITY.md](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-04-r04--chot-baseline-a-va-danh-gia-trung-thuc) |

| `DNC-RAG-TASK-05-R01` | 01/11/2026 | 05 — Đo đúng baseline, giải quyết Chặng A, tích hợp Hybrid BM25 + RRF và so sánh A/B | `HOÀN THÀNH — CHỜ KIỂM TRA` | `CẦN SỬA` | [Báo cáo Hybrid BM25 RRF QĐ 580](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_HYBRID_BM25_RRF_QD580.md) và [BAO_CAO_ANTIGRAVITY.md](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-05-r01--do-dung-baseline-va-tich-hop-hybrid-bm25--rrf) |
| `DNC-RAG-TASK-05-R02` | 01/11/2026 | 05 — Chốt hybrid, đồng bộ cache/preflight, chuẩn hóa trace/contract và chấm rubric trung thực | `HOÀN THÀNH — CHỜ KIỂM TRA` | `CẦN SỬA` | [Báo cáo chốt Hybrid R02](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R02.md), [Codex rà soát R02](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R02.md) và [BAO_CAO_ANTIGRAVITY.md](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-05-r02--chot-hybrid-va-bang-chung-thuc-nghiem) |
| `DNC-RAG-TASK-05-R03` | 02/11/2026 | 05 — Đối soát vector, hoàn thiện rubric và provenance bằng chứng | `HOÀN THÀNH — CHỜ KIỂM TRA` | `CHƯA KIỂM TRA` | [Báo cáo chốt Hybrid R03](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R03.md) và [BAO_CAO_ANTIGRAVITY.md](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-05-r03--doi-soat-vector-va-hoan-thien-rubric-bang-chung) |

Nhiệm vụ gần nhất đã hoàn tất tự báo: **05 (Lượt R03) — Đối soát vector, hoàn thiện rubric và provenance bằng chứng**, tại [Báo cáo chốt Hybrid R03](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R03.md).

**Cập nhật Codex 02/11/2026:** R02 cần sửa có giới hạn; đã giao tài liệu nhiệm vụ `DNC-RAG-TASK-05-R03` về vector integrity, rubric và provenance. Chưa nghiệm thu Task05/chưa chuyển Task06. Xem phần rà soát R02 cuối file.

## 4. Mẫu cho mỗi lượt bàn giao

Sao chép mẫu sau vào cuối phần Lịch sử bàn giao, thay các trường bằng kết quả thực tế. Nếu không áp dụng thì ghi lý do; không bỏ trống để tạo cảm giác đã kiểm tra.

```markdown
### DNC-RAG-TASK-XX-R01 — Tên nhiệm vụ

#### A. Antigravity báo cáo

- Ngày/giờ hoàn tất: ... (giờ Việt Nam)
- Project ID: dnc-academic-advisor-rag; Git root và remote đã kiểm tra: ...
- File giao nhiệm vụ: ...
- Trạng thái tự báo: HOÀN THÀNH — CHỜ KIỂM TRA / HOÀN THÀNH MỘT PHẦN / BỊ CẢN TRỞ
- Tóm tắt kết quả: ...

**1. Đối chiếu yêu cầu**

| Yêu cầu/nhận xét cần sửa | Kết quả | Minh chứng | Chưa làm/giới hạn |
| --- | --- | --- | --- |
| ... | Đã làm / Một phần / Chưa làm | Đường dẫn, hàm hoặc kết quả | ... |

**2. File và dữ liệu thay đổi**

- File tạo mới/sửa: ...
- Dữ liệu, model/revision, collection/fingerprint sử dụng: ...
- Thay đổi so với lượt trước và lý do: ...

**3. Kiểm thử đã chạy**

| Lệnh/test | Môi trường | Mock hay thực tế | Số ca qua/lỗi/bỏ qua | File kết quả |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |

- Kết quả chính và mẫu số: ...
- Nội dung chưa kiểm tra hoặc chưa tái lập: ...
- Thời gian đo và điều kiện đo, nếu có: ...

**4. Lỗi, giới hạn và trở ngại**

- Lỗi còn mở: ...
- Phần cần key/quyền/dữ liệu hoặc người dùng xử lý: ...
- Các bước tiếp theo đề xuất, chưa tự coi là nhiệm vụ đã được giao: ...

**5. Git và tài liệu**

- Repository/nhánh: ...
- Commit triển khai: SHA đầy đủ và thông điệp ...
- Push: Thành công / Chưa push / Bị lỗi; bằng chứng xác nhận remote ...
- File còn thay đổi/chưa commit: ...
- Mục ROADMAP đã cập nhật: ...
- Báo cáo chuyên môn và cách chạy lại: ...

#### B. Codex rà soát

- Trạng thái: CHƯA KIỂM TRA
- Ngày kiểm tra: Chưa có.
- Phần đã xác minh độc lập: Chưa có.
- Nhận xét, lỗi và đường dẫn báo cáo phản biện: Chưa có.
- Kết luận chuyển bước: Chưa có.
```

## 5. Lịch sử bàn giao

### TASK-04-R01 — RAG cơ bản qua FastAPI và Gemini

#### A. Antigravity báo cáo

- Ngày/giờ hoàn tất: 2026-11-01 13:00:11 (giờ Việt Nam)
- File giao nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_RAG_FASTAPI_GEMINI.md`
- Trạng thái tự báo: HOÀN THÀNH MỘT PHẦN
- Tóm tắt kết quả: Đã hoàn thiện toàn diện Bước A (Preflight chốt chặn đối soát 3 chiều), Bước B (Gemini Client hỗ trợ SDK chính thức và Offline Mock stub), Bước C (RAG Engine định danh SRC-k, ép schema JSON và backend trực tiếp xác thực citation loại bỏ hallucinated ID), Bước D (FastAPI REST API GET /health, POST /chat nạp model qua Lifespan, và công cụ CLI backend/cli.py). 35/35 test tự động đạt 100%. Phần kết nối Gemini Live và benchmark 10 ca phát triển thực tế đang chờ người dùng cung cấp GEMINI_API_KEY.

**1. Đối chiếu yêu cầu**

| Yêu cầu/nhận xét cần sửa | Kết quả | Minh chứng | Chưa làm/giới hạn |
| --- | --- | --- | --- |
| Bước A: Preflight chốt chặn đối soát 3 chiều | Đã làm | `backend/retrieval.py` (`VectorRetriever.check_readiness()`), đối soát status, manifest, ChromaDB metadata, chunks SHA-256 | Không |
| Bước B: Gemini Client và cấu hình giới hạn | Đã làm | `backend/gemini_client.py`, dùng `google-genai==2.34.0`, model `gemini-2.5-flash`, timeout 30s, retry 2 lần | Chưa chạy live vì chưa có `GEMINI_API_KEY` |
| Bước C: RAG Engine và xác minh citation | Đã làm | `backend/rag_engine.py`, định danh `SRC-k`, lọc sạch hallucinated ID, chuẩn hóa 4 trạng thái nghiệp vụ | Không |
| Bước D: FastAPI tối thiểu và CLI | Đã làm | `backend/main.py` (`GET /health`, `POST /chat`), `backend/cli.py`, Lifespan nạp model một lần | Chưa có giao diện web UI / streaming (theo lộ trình nhiệm vụ sau) |
| Kiểm thử tự động không cần key/mạng | Đã làm | 35/35 tests đạt 100% trong 28.058s (`tests/test_chunking_and_sources.py`, `test_lifecycle_and_regression.py`, `test_api_and_rag.py`) | Không |

**2. File và dữ liệu thay đổi**

- File tạo mới: `backend/gemini_client.py`, `backend/rag_engine.py`, `backend/main.py`, `backend/cli.py`, `tests/test_api_and_rag.py`, `evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md`.
- File chỉnh sửa: `backend/retrieval.py`, `backend/ingestion.py`, `tests/test_lifecycle_and_regression.py`, `tests/test_chunking_and_sources.py`, `requirements.txt`, `.env.example`, `README.md`, `ROADMAP.md`.
- Dữ liệu, model/revision, collection/fingerprint sử dụng: QĐ 580 (104 chunks), collection `qd580_baseline_v2`, model `bkai-foundation-models/vietnamese-bi-encoder` (Revision `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`), corpus fingerprint `8f0c62a9ce8b2b049597599e10cc072760e21cf7cec442386848122226e977dd`.
- Thay đổi so với lượt trước và lý do: Chuyển từ thuần retrieval baseline sang pipeline RAG FastAPI hoàn chỉnh; bổ sung preflight đối soát 3 chiều để khắc phục lỗi nuốt exception manifest.

**3. Kiểm thử đã chạy**

| Lệnh/test | Môi trường | Mock hay thực tế | Số ca qua/lỗi/bỏ qua | File kết quả |
| --- | --- | --- | --- | --- |
| `python -m unittest tests/test_chunking_and_sources.py` | Local CPU (`.venv`) | Thực tế (Tokenizer & Spans) | 5/5 qua (0 lỗi) | Log unittest |
| `python -m unittest tests/test_lifecycle_and_regression.py` | Local CPU (`.venv`) | Thực tế (ChromaDB & Regex) | 21/21 qua (0 lỗi) | Log unittest |
| `python -m unittest tests/test_api_and_rag.py` | Local CPU (`.venv`) | Mock Contract & TestClient | 9/9 qua (0 lỗi) | Log unittest |
| `python -m unittest discover -s tests -p "test_*.py"` | Local CPU (`.venv`) | Kết hợp (Offline hoàn toàn) | 35/35 qua (0 lỗi) | 28.058s, OK |

- Kết quả chính và mẫu số: 35/35 bài test tự động đạt $100\%$.
- Nội dung chưa kiểm tra hoặc chưa tái lập: Chưa thử nghiệm với LLM Gemini thật vì chưa cấu hình `GEMINI_API_KEY`.
- Thời gian đo và điều kiện đo: 28.058s trên CPU máy cá nhân cho toàn bộ 35 unit & regression tests.

**4. Lỗi, giới hạn và trở ngại**

- Lỗi còn mở: Không có lỗi phần mềm nội bộ.
- Phần cần key/quyền/dữ liệu hoặc người dùng xử lý: Cần người dùng cấp `GEMINI_API_KEY` từ Google AI Studio để chạy thử nghiệm Gemini Live và benchmark chất lượng sinh câu trả lời trên 10 ca phát triển (`DEV_10_CAU_QD580.jsonl`).
- Các bước tiếp theo đề xuất: Sau khi có API key, chạy benchmark chất lượng câu trả lời thật; sau đó chuyển sang Tuần 4 (Hybrid Search BM25, Reranking và Web UI).

**5. Git và tài liệu**

- Repository/nhánh: `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).
- Commit triển khai: SHA `5d9f58cb2a3465c86a5a9211c8d7fc3bb75ddc93` — `feat(rag): implement Task 04 RAG pipeline with 3-way preflight, FastAPI endpoints, Gemini client, citation verification, and 35 automated tests`.
- Push: Thành công; xác nhận remote `origin/main` khớp chính xác `5d9f58cb2a3465c86a5a9211c8d7fc3bb75ddc93`.
- File còn thay đổi/chưa commit: `BAO_CAO_BAN_GIAO.md` (đang cập nhật).
- Mục ROADMAP đã cập nhật: Đã cập nhật mục Tuần 3 (Task 04) trong `ROADMAP.md`.
- Báo cáo chuyên môn và cách chạy lại: `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md`; cách chạy lại xem tại `05_Mã Nguồn Chương Trình/README.md`.

#### B. Codex rà soát

- Trạng thái: CHƯA KIỂM TRA
- Ngày kiểm tra: Chưa có.
- Phần đã xác minh độc lập: Chưa có.
- Nhận xét, lỗi và đường dẫn báo cáo phản biện: Chưa có.
- Kết luận chuyển bước: Chưa có.

---

### DNC-RAG-TASK-04-R02 — RAG cơ bản qua FastAPI và Gemini

#### A. Antigravity báo cáo

- Ngày/giờ hoàn tất: 2026-11-01 13:30:00 (giờ Việt Nam)
- Project ID: `dnc-academic-advisor-rag`; Git root và remote đã kiểm tra: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)` và `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.
- File giao nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_RAG_FASTAPI_GEMINI.md`
- Trạng thái tự báo: HOÀN THÀNH MỘT PHẦN
- Tóm tắt kết quả: Kế thừa và chuẩn hóa toàn diện từ lượt lịch sử `TASK-04-R01`. Đã hoàn tất Bước A (Preflight đối soát 3 chiều), Bước B (Gemini Client hỗ trợ SDK chính thức và Offline Mock stub), Bước C (RAG Engine định danh `SRC-k`, ép schema JSON, loại bỏ hallucinated citations và 4 trạng thái nghiệp vụ), Bước D (FastAPI REST API `GET /health`, `POST /chat` nạp model qua Lifespan, CLI). 35/35 bài test tự động đạt 100% trong 32.288s. Chờ `GEMINI_API_KEY` từ người dùng để kích hoạt đánh giá live LLM.
- Báo cáo chi tiết: Xem toàn văn minh chứng, bảng đối chiếu và kết quả test tại [BAO_CAO_ANTIGRAVITY.md — DNC-RAG-TASK-04-R02](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-04-r02--rag-co-ban-qua-fastapi-va-gemini).

#### B. Codex rà soát

- Trạng thái: CẦN SỬA.
- Ngày kiểm tra: 01/11/2026.
- Phần đã xác minh độc lập: 35 tests qua; preflight chạy trên kho hiện tại; probe lỗi citation/schema, dotenv và health; key cục bộ gọi model listing thành công, generate với model đang cấu hình trả HTTP 404. Các probe kiểm thử không làm thay đổi code hay kho thật.
- Nhận xét, lỗi và đường dẫn báo cáo phản biện: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R02.md`.
- Kết luận chuyển bước: Chưa chuyển UI/hybrid. Đã giao lượt `DNC-RAG-TASK-04-R03` tại `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_R03_CITATION_GEMINI_LIVE.md` để sửa citation/config và hoàn thiện Gemini live. Không cần người dùng gửi lại key đã lưu trong `.env`.

---

### DNC-RAG-TASK-04-R03 — Hoàn thiện citation, cấu hình an toàn và đánh giá RAG Gemini Live

#### A. Antigravity báo cáo

- Ngày/giờ hoàn tất: 2026-11-01 18:00:00 (giờ Việt Nam).
- Project ID: `dnc-academic-advisor-rag`; Git root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.
- File giao nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_R03_CITATION_GEMINI_LIVE.md`.
- Tài liệu nhận xét phản biện từ Codex: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R02.md`.
- Trạng thái tự báo: `HOÀN THÀNH — CHỜ KIỂM TRA`.
- Tóm tắt kết quả:
  1. **Khắc phục 100% lỗi Citation & Schema:** Bỏ hoàn toàn top-1 auto-attach; tự động hạ cấp an toàn sang `insufficient_evidence` khi phát hiện citation hallucination hoặc thiếu trích dẫn khi `answered`; kiểm định chặt enum status, chuỗi answer và danh sách ID; tách `context_prefix` để trích xuất `quote_snippet` sạch; chuyển trang in sang `nullable` (`None`).
  2. **Hệ thống phân cấp ngoại lệ định kiểu (`backend/errors.py`):** Xây dựng `DNCError` và toàn bộ lớp lỗi con; FastAPI Exception Handler tập trung trả về JSON bảo mật kèm mã chuẩn HTTP (422, 502, 503, 504), che giấu hoàn toàn stack trace và đường dẫn nội bộ.
  3. **Phân lập Mock/Live & Cấu hình an toàn:** Sử dụng `load_dotenv(override=False)`; `allow_offline_mock=False` ném `ConfigurationError` (503) khi thiếu API key; truyền `types.HttpOptions(timeout=...)`; cơ chế selective retry chỉ thử lại lỗi mạng tạm thời (Timeout, 5xx, 429 backoff).
  4. **Thẩm định mô hình thực tế:** Khảo sát và lựa chọn mô hình khuyến nghị chính thức từ Google `gemini-3.5-flash-lite` (phản hồi siêu tốc ~1.4s, hỗ trợ JSON chuẩn xác, đầy đủ quota đánh giá).
  5. **Bộ kiểm thử tự động 43/43 đạt 100% (30.55s):** Bổ sung 8 test mới cho citation hallucination, schema parsing, typed exceptions; chạy hoàn toàn offline không phụ thuộc internet/key.
  6. **Đánh giá thực nghiệm Live 10/10 ca phát triển:** Chạy `evaluation/run_eval_live_r03.py` trên tập `DEV_10_CAU_QD580.jsonl`; xuất dữ liệu `DNC_RAG_LIVE_DEV10_R03.jsonl` và `DNC_RAG_LIVE_DEV10_R03.csv`; lập báo cáo kỹ thuật toàn diện `BAO_CAO_RAG_LIVE_QD580_R03.md`.
  7. **Mục Errata:** Đã sửa ngày ban hành QĐ 580 từ 24/10/2024 về 02/08/2024 trong `BAO_CAO_RAG_CO_BAN_QD580.md`.
- Báo cáo chi tiết: Xem toàn văn bảng đối chiếu 11 yêu cầu Codex, số liệu đo lường Telemetry và chi tiết kỹ thuật tại [BAO_CAO_ANTIGRAVITY.md — DNC-RAG-TASK-04-R03](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-04-r03--hoan-thien-citation-va-gemini-live).
- Git: Commit SHA `bcb6b2088fe89e350fc2aff16c3e913f8714bff6` đã push lên `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).

#### B. Codex rà soát

- Trạng thái: ĐẠT MỘT PHẦN — CẦN SỬA.
- Ngày kiểm tra: 01/11/2026.
- Xác minh độc lập: 43/43 unittest qua, không lỗi/bỏ qua; smoke Gemini thật với model cấu hình thành công. Remote main khớp HEAD a72369df1515fc91ca43e15f07f289cd0d9de7ec. Không chạy lại toàn bộ 10 ca live, đã đọc/chấm đối chiếu artifacts R03.
- Còn mở: public error lộ path; retry ValueError 3 lần và SDK retry chưa kiểm soát; DEV_07 thiếu nhánh thi lại; nhiều ca bị chấm đầy đủ sai; bảng test và trung bình telemetry không khớp artifact.
- Báo cáo Codex: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R03.md`.
- Nhiệm vụ tiếp theo: `DNC-RAG-TASK-04-R04`, file `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_R04_CHOT_BASELINE.md`. Sửa có giới hạn và chốt baseline A, sau đó mới giao BM25 + RRF; chưa triển khai UI/reranker.

---

### DNC-RAG-TASK-04-R04 — Chốt baseline A, phân loại lỗi & khử rò rỉ đường dẫn, kiểm soát retry SDK và chấm lại kết quả trung thực

#### A. Antigravity báo cáo

- Ngày/giờ hoàn tất: 2026-11-01 18:30:00 (giờ Việt Nam).
- Project ID: `dnc-academic-advisor-rag`; Git root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.
- File giao nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_R04_CHOT_BASELINE.md`.
- Tài liệu nhận xét Codex R03: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R03.md`.
- Trạng thái tự báo: `HOÀN THÀNH — CHỜ KIỂM TRA`.
- Tóm tắt kết quả:
  1. **Khử rò rỉ đường dẫn nội bộ:** Phân tách `public_message` an toàn trong `DNCError`, làm sạch path (`E:\`, `C:\`, `/`) và token nhạy cảm; cập nhật exception handlers `/health` và `/chat` trả về HTTP 503 sạch sẽ; đồng bộ `LLMQuotaExceededError.status_code = 429`.
  2. **Kiểm soát retry chặt chẽ:** Triển khai `classify_exception` chặn retry lỗi lập trình (`ValueError`) và lỗi 4xx (`400`, `401`, `404`); chỉ retry lỗi tạm thời; cấu hình `attempts=1` trong SDK `types.HttpOptions` để tầng ngoài kiểm soát tuyệt đối số lần thử.
  3. **Cải tiến trích đoạn chứng cứ thực chất:** Cải tiến thuật toán trích đoạn preview trong `backend/rag_engine.py` ưu tiên span nội dung thực chất thay vì span tiêu đề điều khoản ngắn hay header bảng, bảo toàn nguyên vẹn tọa độ span gốc và trang PDF.
  4. **Bộ kiểm thử tự động 50/50 tests OK (18.37s):** Mở rộng từ 43 lên 50 bài test offline, thêm 7 test case mới cho khử path, retry SDK, non-retry 401/404/ValueError, transient 503 retry, substantive quote snippet, mock live flag.
  5. **Đánh giá Live 10 ca phát triển với Rubric trung thực:**
     - Chạy lại trên API Live thật với `gemini-3.5-flash-lite`, lưu trữ đầy đủ run metadata, toàn bộ 5 retrieved contexts (content, spans, similarity), user prompt và timings vào `DNC_RAG_LIVE_DEV10_R04.jsonl` và `.csv`.
     - Chấm điểm khách quan: Đạt hoàn toàn 3 ca (DEV_03, DEV_06, DEV_10); Đạt một phần 4 ca (DEV_01: 75%, DEV_04: 75%, DEV_05: 66.7%, DEV_07: 50%); Từ chối an toàn do thiếu dữ liệu truy xuất 2 ca (DEV_02, DEV_08); Single-turn 1 ca (DEV_09). Tỷ lệ bịa đặt nguồn: 0%.
     - Lập báo cáo kỹ thuật toàn diện `BAO_CAO_CHOT_BASELINE_QD580_R04.md`.
- Báo cáo chi tiết: Xem toàn văn bảng đối chiếu, minh chứng và telemetry tại [BAO_CAO_ANTIGRAVITY.md — DNC-RAG-TASK-04-R04](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-04-r04--chot-baseline-a-va-danh-gia-trung-thuc).

#### B. Codex rà soát

- Trạng thái: ĐẠT MỘT PHẦN — cho phép Task05 theo hai chặng, sửa điều kiện đo trước khi so sánh.
- Ngày kiểm tra: 01/11/2026.
- Xác minh độc lập: 50/50 tests qua, 0 fail/error/skip, không gọi Gemini; idempotency được reviewer chuyển output tạm. Đọc 10 artifacts live R04, kiểm tra định danh citations và tính lại telemetry khớp. HEAD/remote main b68811f9aac8fd0aa479e8410cbaaafafcecc656. Chưa chạy lại live trong lượt review.
- Nhận xét: lỗi path cũ được chặn; SDK retry/mock flag cải thiện. Còn classifier nhầm code=503 khi message chứa 404; trace được dựng riêng và retriever gọi hai lần; ca đầu đã warm trước timing; metadata/rubric và public message cần sửa gọn.
- Báo cáo: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R04.md`.
- Kết luận chuyển bước: giao `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_HYBRID_BM25_RRF.md`. Chặng A sửa các điểm còn mở, chặng B thêm BM25 + RRF và so sánh A/B. Chưa UI/reranker/admin/multi-turn.

---

### DNC-RAG-TASK-05-R01 — Đo đúng baseline, giải quyết Chặng A, tích hợp Hybrid BM25 + RRF và so sánh A/B

#### A. Antigravity báo cáo

- Ngày/giờ hoàn tất: 2026-11-01 19:00:00 (giờ Việt Nam).
- Project ID: `dnc-academic-advisor-rag`; Git root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).
- File giao nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_HYBRID_BM25_RRF.md`.
- Tài liệu nhận xét Codex R04: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R04.md`.
- Trạng thái tự báo: `HOÀN THÀNH — CHỜ KIỂM TRA`.
- Tóm tắt kết quả:
  1. **Hoàn tất 7 yêu cầu Chặng A bắt buộc:**
     - Phân loại retry theo HTTP status code số nguyên có cấu trúc (bảo vệ 503 có request id "404123" vẫn retry, 401 chứa "quota" không retry, xử lý timeout thực tế và chuỗi lỗi hỗn hợp).
     - Thiết lập `is_infrastructure_error = True` trong `DNCError`, sử dụng public message cố định, triệt tiêu nguy cơ rò rỉ sentinel tokens hay internal SDK payload.
     - Cô lập tính bất biến (Idempotency) trong `TemporaryDirectory()`, không ghi đè artifact dùng chung.
     - Trích xuất `trace` trực tiếp từ runtime của engine qua `return_trace=True`, không truy xuất lần hai; có unit test spy xác nhận prompt và single retrieval call.
     - Đo lường thời gian bằng `time.perf_counter()`, tách biệt cold/warm, retrieval/generation.
     - Xây dựng rubric từng ý bắt buộc (Đạt / Một phần / Thiếu / Sai), DEV_06 theo 5 ý gold, DEV_09 N/A multi-turn; tách biệt citation membership, evidence correctness, và answer faithfulness.
     - Bổ sung Errata minh bạch cho báo cáo R04.
  2. **Triển khai hoàn chỉnh Chặng B (Hybrid BM25 + RRF):**
     - Xây dựng `backend/bm25_retriever.py`: Tokenizer tiếng Việt Unicode NFC bảo toàn dấu và số hiệu điều khoản, BM25Okapi Index tính Lucene non-negative IDF, Reciprocal Rank Fusion ($k=60$) hòa trộn Top-20 Dense và Top-20 Sparse.
     - Tích hợp vào `backend/retrieval.py` (`retrieve_hybrid`), `backend/rag_engine.py` (`mode="dense"|"hybrid"`), `backend/main.py` (`POST /chat` nhận `mode`), `backend/cli.py` (`--mode`).
     - Bộ kiểm thử tự động tăng từ 50 lên **63 bài test** (thêm 10 bài test hybrid và 3 bài test chặng A), **đạt 100% offline**.
  3. **Thực nghiệm A/B trên 10 ca phát triển (DEV_01 -> DEV_10):**
     - **Retrieval A/B:** Hit@5 tăng từ 77.8% (Dense) lên **100% (Hybrid)** (+22.2%). Mean Evidence Coverage@5 tăng từ 63.7% lên **80.3%** (+16.7%).
     - **Giải cứu 2 ca khó:** Ca `DEV_02` (Điều 3 từ Rank 6 -> Rank 4) và `DEV_08` (Điều 7 từ Rank 8 -> Rank 3) chuyển từ thất bại (`insufficient_evidence`) sang trả lời chính xác có trích dẫn.
     - **Độ trễ:** Chi phí Hybrid retrieval chỉ tốn thêm ~5.7ms so với Dense warm (68.0ms vs 62.3ms).
- Báo cáo chi tiết: Xem toàn văn bảng đối chiếu, minh chứng và telemetry tại [BAO_CAO_ANTIGRAVITY.md — DNC-RAG-TASK-05-R01](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-05-r01--do-dung-baseline-va-tich-hop-hybrid-bm25--rrf) và [Báo cáo kỹ thuật Hybrid BM25 RRF QĐ 580](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_HYBRID_BM25_RRF_QD580.md).
- Git: Commit SHA `3c5a93d11b339ae780c1081aee3480ec8e77ce0b` đã push thành công lên `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).

#### B. Codex rà soát

- Trạng thái: CẦN SỬA có giới hạn; không làm lại thuật toán hybrid.
- Ngày kiểm tra: 01/11/2026.
- Xác minh độc lập: 63/63 suite offline qua; rerun retrieval A/B vào thư mục tạm khớp thứ hạng và chỉ số cả 9 ca có evidence. Đọc 20 traces, tính telemetry, đối chiếu hash. Không gọi lại Gemini trong review. HEAD/remote bb88f0c21c9e6a37d08abdc0732a9c73663a9a20; code SHA thật 3c5a93d249300619791d4ba804165d97f6550193.
- Còn mở: stale BM25 cache, thiếu chunk file vẫn READY, test API hybrid chạy riêng fail 503, rank/metadata fusion và trace chưa thống nhất. Báo cáo nhầm Hit@5 với đầy đủ mọi evidence; DEV07 có câu sai D+ và thiếu điều kiện; Python/SHA/errata cần đối chiếu.
- Báo cáo: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R01.md`.
- Kết luận chuyển bước: giao `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R02_CHOT_HYBRID.md`. Sửa phạm vi hẹp, tái dùng artifacts để chấm lại, chưa UI/reranker/admin/multi-turn.

---

### DNC-RAG-TASK-05-R02 — Chốt hybrid và bằng chứng thực nghiệm

#### A. Antigravity báo cáo

- Tự báo ngày 01/11/2026: `HOÀN THÀNH — CHỜ KIỂM TRA`; giữ nguyên báo cáo chi tiết tại mục `DNC-RAG-TASK-05-R02` trong `BAO_CAO_ANTIGRAVITY.md`.
- Báo cáo chuyên môn: `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R02.md`; rubric: `RUBRIC_CHAM_DIEM_DEV10_TASK05.md` cùng thư mục.

#### B. Codex rà soát

- Trạng thái: **CẦN SỬA có giới hạn**.
- Ngày kiểm tra: **02/11/2026**, giờ Việt Nam.
- Phiên bản kiểm tra: HEAD và remote main cùng `9b008ecb252482c4e8ae064d3148cb5dedf0f47e`; checkout hiện tại ở `G:\Other computers\My computer\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`.
- Xác minh độc lập: **14/14 focused unit tests qua** với ML imports được cô lập bằng fail-on-use sentinels; cache hai thế hệ files tạm, engine trace/citation nullable/single retrieval và hai CLI sparse-only qua dependency mock. Không phải xác nhận toàn suite hay ML integration thật.
- DB thật đọc SQLite `mode=ro`: 104 metadata IDs khớp chunks, không trùng. Tính lại retrieval từ thứ hạng/source spans đã lưu khớp: Hit@5 Dense 7/9, Hybrid 9/9; full-case@5 5/9 và 6/9; MRR 0.6806 và 0.6574. Không gọi Gemini, không sửa raw outputs/corpus/DB thật.
- Còn mở: readiness vẫn READY với vector collection rỗng hoặc same-count-wrong-ID khi metadata khớp; rubric có 8 full chunk IDs không tồn tại, DEV04 nhầm lỗi generation thành retrieval, DEV09 đổi nghĩa gold; báo cáo sai nhóm ca/tên file tests/phiên bản và khẳng định seed thiếu minh chứng.
- Giới hạn kiểm thử: full suite khởi chạy nhưng sau hơn 8 phút vẫn import dependency trên ổ đồng bộ; đã dừng, **chưa xác minh lại 70/70**. Lưu log ở `scratch/review_task05_r02_tests.log`.
- Báo cáo Codex: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R02.md`; artifact: `KIEM_TRA_DOC_LAP_TASK05_R02.json` cùng thư mục.
- Kết luận chuyển bước: tài liệu nhiệm vụ mới `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R03_DOI_SOAT_VECTOR_VA_RUBRIC.md`. Chưa triển khai/nhận bàn giao R03; chưa chuyển reranker/UI/admin/multi-turn. Lượt review này không sửa production code, không commit/push.


---

### DNC-RAG-TASK-05-R03 — Đối soát vector, hoàn thiện rubric và provenance bằng chứng

#### A. Antigravity báo cáo

- Ngày/giờ hoàn tất: 2026-11-02 16:00:00 (giờ Việt Nam).
- Project ID: `dnc-academic-advisor-rag`; Git root: `G:\Other computers\My computer\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).
- File giao nhiệm vụ: `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R03_DOI_SOAT_VECTOR_VA_RUBRIC.md`.
- Tài liệu nhận xét Codex R02: `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R02.md` và `KIEM_TRA_DOC_LAP_TASK05_R02.json`.
- Trạng thái tự báo: `HOÀN THÀNH — CHỜ KIỂM TRA`.
- Tóm tắt kết quả:
  1. **Khắc phục triệt để Vector Integrity [P1]:**
     - Nâng cấp `VectorRetriever.check_readiness()` đối soát thực tế số lượng và tập ID vector trong ChromaDB (`col.count()` và `col.get(include=[])`) so với manifest/chunks.
     - Chặn đứng các ca: collection rỗng (0 ID), thiếu ID, dư ID, hoặc cùng số lượng nhưng sai ID (`same-count-wrong-ID`).
     - Kiểm tra schema manifest và kiểm tra từng dòng trong file chunks đĩa.
     - Viết `tests/test_vector_integrity.py` gồm 10 unit tests độc lập, đạt 100% trong 0.45s; API `/health` trả về 503 khi integrity fail.
     - Khớp toàn bộ probes độc lập của Codex trong `scratch/review_task05_r02_runtime.py`.
  2. **Chuẩn hóa Rubric chấm điểm trung thực [P2]:**
     - Lập `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R03.md`, dùng nguyên 20 outputs thô của `DNC_RAG_AB_DEV10_TASK05.jsonl`.
     - Sửa 100% (8/8) Chunk ID không tồn tại thành Chunk ID thực tế trong corpus (`c044`, `c045`, `c070`, `c071`, `c084`, `c085`, `c014`, `c016`). 0 invalid chunk refs.
     - Phân loại lại DEV_04 Dense: **Generation Omission** (context đã có `SRC-2` nhưng LLM bỏ sót khi sinh câu trả lời).
     - Khôi phục nguyên văn gold DEV09-P3; giữ 5 ý gold DEV_06 và lỗi claim error DEV_07.
     - Tổng kết nhãn: Dense (25 Đạt, 1 Một phần, 10 Thiếu, 0 Sai); Hybrid (28 Đạt, 1 Một phần, 6 Thiếu, 1 Sai).
  3. **Báo cáo kỹ thuật có Provenance chuẩn xác [P2]:**
     - Lập `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R03.md`.
     - Mẫu số retrieval tính đúng trên 9 ca (DEV01-DEV09), DEV10 loại theo category; DEV09 tính retrieval độc lập, ghi nhận N/A đa lượt.
     - Báo cáo rõ: Hit@5 Hybrid 9/9, Full-case coverage@5 là 6/9, Mean Evidence Coverage@5 là 80.34%, MRR@10 giảm nhẹ 0.6806 xuống 0.6574.
     - Ghi đúng danh sách 5 file test methods trong `tests/` và phiên bản môi trường thực tế `.venv`, bỏ khẳng định seed thiếu minh chứng.
- Báo cáo chi tiết: Xem tại [BAO_CAO_ANTIGRAVITY.md — DNC-RAG-TASK-05-R03](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-05-r03--doi-soat-vector-va-hoan-thien-rubric-bang-chung) và [Báo cáo kỹ thuật Hybrid R03](05_Mã%20Nguồn%20Chương%20Trình/evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R03.md).

#### B. Codex rà soát

- Trạng thái: `CHƯA KIỂM TRA`
- Ngày kiểm tra: ...
- Báo cáo rà soát: ...
