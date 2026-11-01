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
| `DNC-RAG-TASK-04-R02` | 01/11/2026 | 04 — RAG cơ bản qua FastAPI và Gemini | `HOÀN THÀNH MỘT PHẦN` | `CHƯA KIỂM TRA` | [Báo cáo chi tiết BAO_CAO_ANTIGRAVITY.md](BAO_CAO_ANTIGRAVITY.md#dnc-rag-task-04-r02--rag-co-ban-qua-fastapi-va-gemini) |

Nhiệm vụ gần nhất đã giao: **04 — RAG cơ bản qua FastAPI và Gemini**, tại [file nhiệm vụ 04](02_Dữ%20Liệu%20Quy%20Chế/03_Kiểm%20Tra%20Chất%20Lượng%20Dữ%20Liệu/NHIEM_VU_TIEP_THEO_04_RAG_FASTAPI_GEMINI.md).

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

- Trạng thái: CHƯA KIỂM TRA
- Ngày kiểm tra: Chưa có.
- Phần đã xác minh độc lập: Chưa có.
- Nhận xét, lỗi và đường dẫn báo cáo phản biện: Chưa có.
- Kết luận chuyển bước: Chưa có.
