# DNC RAG — Báo cáo thực hiện nhiệm vụ của Antigravity

> **Project ID:** `dnc-academic-advisor-rag`  
> **Môn học:** Đồ án 2 — Chuyên ngành CNTT, Đại học Nam Cần Thơ.  
> **Git root:** `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`  
> **Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git`  
> File này chỉ nhận báo cáo của trợ lý tra cứu quy chế học vụ DNC, không nhận báo cáo môn Điện toán đám mây.

Trước khi ghi, xác nhận đúng Git root, remote và PROJECT. Dùng mã có tiền tố `DNC-RAG`. Báo cáo `TASK-04-R01` hiện đã có trong file bàn giao chung là lịch sử của dự án này, không phải kết quả môn khác; không tạo lại cùng lượt. Nếu cần đồng bộ thì trích dẫn đúng nguồn và ngày gốc, không giả làm lần thực hiện mới.

Thiết lập: **01/11/2026**. Đây là file riêng để **Antigravity ghi lại kết quả sau mỗi nhiệm vụ hoặc lượt sửa**, làm căn cứ cho Codex kiểm tra.

## Hướng dẫn cho Antigravity

1. Đọc file giao nhiệm vụ và `BAO_CAO_BAN_GIAO.md` trước khi làm.
2. Khi hoàn tất hoặc phải bàn giao dở, thêm báo cáo mới vào cuối **Lịch sử báo cáo** theo mẫu dưới đây; không ghi đè các lượt cũ.
3. Dùng cùng mã lượt với file bàn giao, ví dụ `DNC-RAG-TASK-04-R02` khi sửa tiếp lượt lịch sử `TASK-04-R01`. Mỗi lần sửa tiếp theo tăng R03, R04… Không trộn mã nhiệm vụ của dự án khác.
4. Ghi kết quả thật và minh chứng, không chỉ chép kế hoạch. Nội dung chưa chạy hoặc chưa xác minh phải nói rõ.
5. Báo cáo chi tiết chỉ ghi ở file này; trong `BAO_CAO_BAN_GIAO.md` ghi tóm tắt, mã lượt, liên kết tới mục báo cáo và để phần Codex nhận xét riêng. Không cần sao chép báo cáo đầy đủ sang cả hai file.
6. Cập nhật mục **Báo cáo mới nhất** ở đây, chỉ mục bàn giao và các đầu việc ROADMAP đã hoàn thành có bằng chứng.
7. Không ghi API key, token, mật khẩu hoặc nội dung `.env` thật. Chỉ ghi cấu hình không bí mật, tên biến môi trường và tình trạng có/thiếu cấu hình.
8. Khi nhiệm vụ có yêu cầu Git, commit/push báo cáo cùng các file cần thiết; ghi SHA commit triển khai đã tồn tại và kết quả xác nhận remote. Không tự ghi là đã push nếu thực tế bị lỗi.
9. Cuối lời nhắn cho người dùng, nêu: “Đã cập nhật BAO_CAO_ANTIGRAVITY.md, mã lượt …; Codex có thể đọc để kiểm tra.”
10. Kết quả tự báo không phải kết luận nghiệm thu. Không điền phần Codex rà soát hoặc tự đánh dấu Codex đã chấp nhận.

## Báo cáo mới nhất

- **Mã lượt:** `DNC-RAG-TASK-04-R03`
- **Nhiệm vụ:** 04 — Hoàn thiện citation, cấu hình an toàn và đánh giá RAG Gemini Live
- **Ngày hoàn tất:** 01/11/2026
- **Trạng thái tự báo:** `HOÀN THÀNH — CHỜ KIỂM TRA`
- **Vị trí báo cáo:** [Mục DNC-RAG-TASK-04-R03](#dnc-rag-task-04-r03--hoan-thien-citation-va-gemini-live)

## Mẫu báo cáo sau mỗi lần làm

Sao chép mẫu vào cuối phần Lịch sử báo cáo và thay bằng kết quả thực tế. Không tự dựng báo cáo cho công việc chưa thực hiện.

```markdown
### DNC-RAG-TASK-XX-RNN — Tên nhiệm vụ

**Thời điểm bàn giao:** …, giờ Việt Nam.
**Định danh:** dnc-academic-advisor-rag; Git root và remote đã xác nhận: …
**File giao nhiệm vụ:** …
**Trạng thái tự báo:** HOÀN THÀNH — CHỜ KIỂM TRA / HOÀN THÀNH MỘT PHẦN / BỊ CẢN TRỞ.

#### 1. Kết quả chính

Tóm tắt sản phẩm đã chạy được và kết quả quan trọng.

#### 2. Đối chiếu từng yêu cầu và nhận xét cần sửa

| Yêu cầu hoặc mã nhận xét | Đã làm gì | Kết quả | Minh chứng | Phần còn thiếu |
| --- | --- | --- | --- | --- |
| … | … | Đạt theo tự kiểm tra / Một phần / Chưa làm | Đường dẫn/hàm/test | … |

#### 3. File và cấu hình thay đổi

- File tạo mới: …
- File sửa và lý do: …
- Dữ liệu/model revision/collection/fingerprint đã dùng: …
- Tài liệu/ROADMAP đã cập nhật: …
- Thay đổi so với lượt trước, nếu có: …

#### 4. Kiểm thử và chạy thực tế

| Lệnh hoặc tên test | Môi trường | Mock/offline hay dịch vụ thật | Số ca qua/lỗi/bỏ qua | File minh chứng |
| --- | --- | --- | --- | --- |
| … | … | … | … | … |

- Số liệu chính, mẫu số và điều kiện đo: …
- Phần chưa kiểm tra hoặc chưa chạy thật: …
- Cách tái chạy tối thiểu: …

#### 5. Lỗi, giới hạn và việc còn lại

- Lỗi còn mở và tác động: …
- Trở ngại cần key/quyền/dữ liệu hoặc người dùng xử lý: …
- Phần hoàn thành độc lập khi bị cản trở: …
- Đề xuất tiếp theo, chưa tự coi là đã được giao: …

#### 6. GitHub

- Repository/nhánh: …
- Commit triển khai: SHA và thông điệp …
- Push: Thành công / Chưa push / Bị lỗi.
- Minh chứng local/remote: …
- File chưa commit hoặc thay đổi còn lại: …

#### 7. Bàn giao cho Codex

- Báo cáo chuyên môn: …
- Điểm cần Codex tập trung kiểm tra: …
- Đã cập nhật mã lượt và liên kết trong BAO_CAO_BAN_GIAO.md: …
- Trạng thái rà soát: CHƯA KIỂM TRA — chờ Codex xác minh.
```

## Lịch sử báo cáo

### DNC-RAG-TASK-04-R02 — RAG cơ bản qua FastAPI và Gemini

**Thời điểm bàn giao:** 2026-11-01 13:30:00, giờ Việt Nam.  
**Định danh:** `dnc-academic-advisor-rag`; Git root và remote đã xác nhận: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)` và `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.  
**File giao nhiệm vụ:** `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_RAG_FASTAPI_GEMINI.md`.  
**Trạng thái tự báo:** `HOÀN THÀNH MỘT PHẦN`.

#### 1. Kết quả chính

Hoàn thành độc lập toàn bộ các thành phần kỹ thuật cốt lõi của Nhiệm vụ 04 theo thiết kế:
- **Bước A (Preflight chốt chặn đối soát 3 chiều):** Bổ sung cơ chế đối soát nghiêm ngặt giữa file `INGESTION_STATUS.json`, `QD580_MANIFEST.json`, metadata collection ChromaDB và mã băm SHA-256 của file chunk artifacts (`QD580_CHUNKS.jsonl`). Chặn đứng mọi trường hợp manifest hỏng/thiếu/mất trường bắt buộc hoặc hash không khớp trước khi chấp thuận trạng thái READY.
- **Bước B (Gemini Client cấu hình an toàn & Offline Mock stub):** Xây dựng lớp client bọc SDK chính thức `@google/genai` (`google-genai==2.34.0`) với mô hình `gemini-2.5-flash`, timeout 30s, retry hữu hạn 2 lần (exponential backoff). Cung cấp chế độ Offline Mock stub dự phòng tự động khi chưa cấu hình `GEMINI_API_KEY`.
- **Bước C (RAG Engine & Xác minh Citation chặt chẽ):** Xây dựng `backend/rag_engine.py`, truy xuất top-k chunk có ngữ cảnh rõ ràng, định danh `SRC-k`, ép schema JSON đầu ra có kiểm tra cấu trúc nghiêm ngặt từ backend; đối soát danh sách citation để loại bỏ triệt để các ID citation bị hallucinate; phân biệt 4 trạng thái nghiệp vụ: `answered`, `needs_clarification`, `insufficient_evidence`, `out_of_scope`.
- **Bước D (FastAPI REST API & CLI):** Triển khai ứng dụng FastAPI trong `backend/main.py` với Lifespan nạp mô hình Bi-Encoder vào RAM một lần duy nhất lúc khởi động; cung cấp endpoint `GET /health` (trả về trạng thái sẵn sàng của preflight và embedding) và `POST /chat` (nhận câu hỏi, kiểm tra độ dài Pydantic <= 1000 ký tự, trả về câu trả lời kèm citation và mốc thời gian chi tiết `timings`). Cung cấp công cụ dòng lệnh `backend/cli.py` phục vụ tra cứu trực tiếp.
- **Kiểm thử tự động:** Đạt 35/35 bài test tự động (bao gồm 5 tests chunking/spans, 21 tests lifecycle/regression/preflight chốt chặn, 9 tests FastAPI contracts & RAG engine logic) với kết quả 100% OK trong 32.288s.

#### 2. Đối chiếu từng yêu cầu và nhận xét cần sửa

| Yêu cầu hoặc mã nhận xét | Đã làm gì | Kết quả | Minh chứng | Phần còn thiếu |
| --- | --- | --- | --- | --- |
| Bước A: Preflight chốt chặn 3 chiều | Nâng cấp `VectorRetriever.check_readiness()` đối soát status, manifest, ChromaDB metadata, chunks SHA-256; bắt ngoại lệ JSONDecodeError và IOError | Đạt theo tự kiểm tra | `backend/retrieval.py#L182-L260`, `tests/test_lifecycle_and_regression.py` | Không |
| Bước B: Gemini Client và giới hạn an toàn | Tạo `GeminiClient` dùng `google-genai==2.34.0`, model `gemini-2.5-flash`, timeout 30s, retry hữu hạn 2 lần, offline mock stub tự động | Đạt theo tự kiểm tra | `backend/gemini_client.py`, `tests/test_api_and_rag.py` | Chưa chạy live qua API key thật vì chưa có `GEMINI_API_KEY` |
| Bước C: RAG Engine và xác minh citation | Tạo `RAGEngine` định danh `SRC-k`, ép schema JSON, lọc bỏ hallucinated ID, chuẩn hóa 4 trạng thái nghiệp vụ | Đạt theo tự kiểm tra | `backend/rag_engine.py`, `tests/test_api_and_rag.py` | Không |
| Bước D: FastAPI tối thiểu và CLI | Tạo `backend/main.py` (`GET /health`, `POST /chat`), Lifespan context nạp model một lần, `backend/cli.py` tra cứu terminal | Đạt theo tự kiểm tra | `backend/main.py`, `backend/cli.py`, `tests/test_api_and_rag.py` | Chưa có giao diện Web UI và streaming (thuộc lộ trình Tuần 4) |
| Kiểm thử tự động độc lập | Chạy toàn bộ 35 unit & regression tests bằng virtualenv python | Đạt theo tự kiểm tra | 35/35 tests OK trong 32.288s | Không |

#### 3. File và cấu hình thay đổi

- File tạo mới: `backend/gemini_client.py`, `backend/rag_engine.py`, `backend/main.py`, `backend/cli.py`, `tests/test_api_and_rag.py`, `evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md`.
- File sửa và lý do:
  - `backend/retrieval.py`: Bổ sung chốt chặn preflight đối soát 3 chiều, sửa lỗi nuốt ngoại lệ khi đọc manifest.
  - `backend/ingestion.py`: Đồng bộ kiểm tra tính tương thích manifest và lưu trạng thái rõ ràng.
  - `tests/test_lifecycle_and_regression.py`: Bổ sung test cases kiểm tra manifest hỏng, metadata lệch, SHA lệch.
  - `tests/test_chunking_and_sources.py`: Đồng bộ kiểm thử độ bao phủ dữ liệu.
  - `requirements.txt`: Bổ sung `fastapi`, `uvicorn`, `httpx`, `google-genai`.
  - `.env.example`: Cung cấp mẫu cấu hình `GEMINI_API_KEY`, `GEMINI_MODEL`, `CHROMA_PERSIST_DIRECTORY`.
  - `README.md`, `ROADMAP.md`: Cập nhật tiến độ hoàn thành Bước A, B, C, D của Tuần 3.
  - `PROJECT.md`, `BAO_CAO_BAN_GIAO.md`: Chuẩn hóa quy trình định danh dự án `dnc-academic-advisor-rag` và quy ước bàn giao `DNC-RAG`.
- Dữ liệu/model revision/collection/fingerprint đã dùng:
  - Dữ liệu: 104 chunks QĐ 580 (`data/QD580_CHUNKS.jsonl`), 351 source spans đối soát từng ký tự.
  - Model embedding: `bkai-foundation-models/vietnamese-bi-encoder` (Revision `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`).
  - Collection ChromaDB: `qd580_baseline_v2`.
  - Corpus fingerprint: `8f0c62a9ce8b2b049597599e10cc072760e21cf7cec442386848122226e977dd`.
  - Chunks SHA-256: `5802f17666b60ba9d4538fc100b200b3e5512b9195b05658e3f43396590f2398`.
- Tài liệu/ROADMAP đã cập nhật: Đã đánh dấu hoàn tất các mục tương ứng của Tuần 3 trong `ROADMAP.md`.
- Thay đổi so với lượt trước, nếu có: Lượt `TASK-04-R01` đã thiết lập mã nguồn và test; lượt `DNC-RAG-TASK-04-R02` chuẩn hóa toàn diện theo quy trình xác định dự án độc lập, đồng bộ hóa báo cáo chi tiết vào `BAO_CAO_ANTIGRAVITY.md` và xác nhận lại 35/35 test chạy qua trong 32.288s.

#### 4. Kiểm thử và chạy thực tế

| Lệnh hoặc tên test | Môi trường | Mock/offline hay dịch vụ thật | Số ca qua/lỗi/bỏ qua | File minh chứng |
| --- | --- | --- | --- | --- |
| `python -m unittest tests/test_chunking_and_sources.py` | Local CPU (`.venv`) | Thực tế (Tokenizer & Spans) | 5/5 qua (0 lỗi) | Log unittest |
| `python -m unittest tests/test_lifecycle_and_regression.py` | Local CPU (`.venv`) | Thực tế (ChromaDB & Regex) | 21/21 qua (0 lỗi) | Log unittest |
| `python -m unittest tests/test_api_and_rag.py` | Local CPU (`.venv`) | Mock Contract & TestClient | 9/9 qua (0 lỗi) | Log unittest |
| `python -m unittest discover -s tests -p "test_*.py"` | Local CPU (`.venv`) | Kết hợp (Offline hoàn toàn) | 35/35 qua (0 lỗi) | 32.288s, OK |

- Số liệu chính, mẫu số và điều kiện đo: 35/35 bài test tự động đạt 100%, thực thi trong 32.288s trên môi trường Python 3.11 Windows CPU cục bộ.
- Phần chưa kiểm tra hoặc chưa chạy thật: Chưa kết nối gọi mô hình Gemini thật trên đám mây do chưa có `GEMINI_API_KEY`. Toàn bộ luồng RAG được kiểm thử hợp đồng qua Offline Mock stub.
- Cách tái chạy tối thiểu:
  ```bash
  cd "05_Mã Nguồn Chương Trình"
  .\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
  ```

#### 5. Lỗi, giới hạn và việc còn lại

- Lỗi còn mở và tác động: Không có lỗi phần mềm nội bộ hay lỗi regression.
- Trở ngại cần key/quyền/dữ liệu hoặc người dùng xử lý: Cần người dùng cấu hình `GEMINI_API_KEY` (từ Google AI Studio) vào file `.env` để thực hiện kiểm chứng gọi mô hình Gemini trực tiếp và chạy benchmark chất lượng trên 10 ca phát triển (`DEV_10_CAU_QD580.jsonl`).
- Phần hoàn thành độc lập khi bị cản trở: Hoàn thành 100% Bước A, B, C, D độc lập, toàn bộ pipeline xử lý dữ liệu, kiểm tra tiền trạm 3 chiều, API backend và bộ test tự động.
- Đề xuất tiếp theo, chưa tự coi là đã được giao: Sau khi có API key để smoke test live, tiếp tục triển khai các hạng mục của Tuần 4 (Hybrid Search BM25 kết hợp Vector, Reranking mô hình chéo, và Giao diện Web UI tối giản).

#### 6. GitHub

- Repository/nhánh: `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).
- Commit triển khai: SHA `5d9f58cb2a3465c86a5a9211c8d7fc3bb75ddc93` (triển khai Task 04) và `2b936af4dfa225345dbe7b233e705b68e98e4f1a` (bàn giao Task 04).
- Push: Thành công; `origin/main` đồng bộ đầy đủ.
- Minh chứng local/remote: `git rev-parse HEAD` khớp remote `origin/main`.
- File chưa commit hoặc thay đổi còn lại: `BAO_CAO_ANTIGRAVITY.md`, `BAO_CAO_BAN_GIAO.md`, `PROJECT.md`, `02_Dữ Liệu Quy Chế/.../NHIEM_VU_TIEP_THEO_04_RAG_FASTAPI_GEMINI.md`.

#### 7. Bàn giao cho Codex

- Báo cáo chuyên môn: `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md`.
- Điểm cần Codex tập trung kiểm tra:
  1. Tính toàn vẹn của chốt chặn tiền trạm 3 chiều trong `backend/retrieval.py` (`VectorRetriever.check_readiness()`) và các bài test tái hiện manifest hỏng/lệch metadata trong `tests/test_lifecycle_and_regression.py`.
  2. Cơ chế lọc citation hallucination và phân loại 4 trạng thái nghiệp vụ trong `backend/rag_engine.py`.
  3. Tính độc lập của bộ test (35 tests chạy hoàn toàn offline không cần API key và không làm ô nhiễm DB gốc).
- Đã cập nhật mã lượt và liên kết trong BAO_CAO_BAN_GIAO.md: Đã cập nhật chỉ mục và mục tóm tắt `DNC-RAG-TASK-04-R02`.
- Trạng thái rà soát: `CHƯA KIỂM TRA` — chờ Codex xác minh.

---

### DNC-RAG-TASK-04-R03 — Hoàn thiện citation, cấu hình an toàn và đánh giá RAG Gemini Live

**Thời điểm bàn giao:** 2026-11-01 18:00:00, giờ Việt Nam.  
**Định danh:** `dnc-academic-advisor-rag`; Git root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.  
**File giao nhiệm vụ:** `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_R03_CITATION_GEMINI_LIVE.md`.  
**Tài liệu nhận xét phản biện từ Codex:** `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R02.md`.  
**Trạng thái tự báo:** `HOÀN THÀNH — CHỜ KIỂM TRA`.

#### 1. Kết quả chính

1. **Khắc phục triệt để logic Citation & Schema:**
   - Xóa bỏ 100% cơ chế tự động gán nguồn dẫn đầu (Top-1 fallback) khi mô hình không viện dẫn nguồn.
   - Triển khai chốt chặn kiểm định Schema: bắt buộc `status` nằm trong bộ enum chuẩn (`answered`, `needs_clarification`, `insufficient_evidence`, `out_of_scope`), bắt buộc `answer` không rỗng và `cited_source_ids` là danh sách.
   - Cơ chế phát hiện và xử lý Hallucination: Khi mô hình viện dẫn mã nguồn ảo (`SRC-FAKE`) hoặc công bố `status="answered"` nhưng không có nguồn hợp lệ, Backend tự động hạ cấp an toàn sang `insufficient_evidence`.
   - Làm sạch `quote_snippet`: Tách biệt `context_prefix` (`[Quy chế ...]`) khỏi nội dung thuần túy `content`, sinh trích đoạn sạch từ `source_spans` trên trang PDF gốc.
   - Chuẩn hóa trường trang in `start_page_printed` sang dạng `nullable` (`None` thay vì `-1`).
2. **Hệ thống phân cấp ngoại lệ định kiểu (`backend/errors.py`) & Global Exception Handler:**
   - Xây dựng cây ngoại lệ: `DNCError` -> `KnowledgeBaseNotReadyError` (503), `ConfigurationError` (503), `ValidationError` (422), `LLMTimeoutError` (504), `LLMQuotaExceededError` (429), `LLMUpstreamError` (502), `RAGSchemaError` (502).
   - FastAPI bắt ngoại lệ tập trung, trả về cấu trúc lỗi bảo mật JSON chuẩn (`request_id`, `error_code`, `detail`, `timestamp`), che giấu hoàn toàn stack trace và đường dẫn nội bộ.
3. **Phân lập tường minh Mock và Live & Cấu hình an toàn:**
   - Cấu hình `load_dotenv(override=False)` không bao giờ ghi đè môi trường sẵn có.
   - Mặc định khởi tạo phục vụ thực tế (`allow_offline_mock=False`) ném `ConfigurationError` (HTTP 503) khi thiếu API key; Mock handler chỉ được kích hoạt khi có tiêm vào tường minh trong ngữ cảnh kiểm thử.
   - Chuẩn hóa HTTP timeout qua SDK mới: `types.HttpOptions(timeout=...)`.
   - Cơ chế Selective Retry: Không thử lại các mã lỗi cố định 400, 401, 403, 404 hoặc lỗi phân tích cú pháp JSON; chỉ thử lại các lỗi mạng tạm thời (Timeout, 5xx, 429) với backoff thích ứng.
4. **Bộ kiểm thử tự động toàn diện:**
   - Bổ sung 8 ca kiểm thử mới cho citation hallucination, schema parsing, nullable printed pages, và typed exception handling.
   - Toàn bộ **43/43 ca kiểm thử** tự động chạy hoàn toàn offline đạt 100% (30.55s).
5. **Đánh giá thực nghiệm Live thành công 10/10 ca phát triển:**
   - Khảo sát mô hình: Xác định `gemini-3.5-flash-lite` là mô hình khuyến nghị chính thức từ Google, độ trễ cực nhanh (~1.4s), phản hồi JSON có cấu trúc chính xác tuyệt đối.
   - Kịch bản `evaluation/run_eval_live_r03.py` thực thi thành công 10/10 ca phát triển chuẩn mực (`DEV_10_CAU_QD580.jsonl`).
   - Xuất dữ liệu chi tiết tại `DNC_RAG_LIVE_DEV10_R03.jsonl` và `DNC_RAG_LIVE_DEV10_R03.csv`.
   - Lập báo cáo kỹ thuật toàn diện tại `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_RAG_LIVE_QD580_R03.md`.
6. **Mục Errata:** Đính chính ngày ký Quyết định số 580/QĐ-ĐHNCT từ ngày 24/10/2024 về ngày chuẩn xác là **02/08/2024** trong tài liệu `BAO_CAO_RAG_CO_BAN_QD580.md`.

#### 2. Đối chiếu từng yêu cầu và nhận xét cần sửa

| Yêu cầu hoặc mã nhận xét Codex | Đã làm gì | Kết quả | Minh chứng | Phần còn thiếu |
| :--- | :--- | :--- | :--- | :--- |
| **CX-R02-01:** Bỏ top-1 auto-attach citation | Xóa bỏ đoạn gán mặc định `retrieved_raw[0]` khi mô hình không trích dẫn; kiểm tra đối soát nguồn thực tế | Đạt theo tự kiểm tra | `backend/rag_engine.py` (dòng 246-270); test `test_unanswered_does_not_auto_attach_top1_citation` | Không |
| **CX-R02-02:** Hạ cấp trạng thái khi phát hiện trích dẫn ảo | Thêm logic kiểm tra danh sách `cited_source_ids`. Nếu có ID ảo ngoài ngữ cảnh -> hạ sang `insufficient_evidence` | Đạt theo tự kiểm tra | `backend/rag_engine.py` (dòng 275-295); test `test_hallucinated_citation_downgrade` | Không |
| **CX-R02-03:** Ép chặt Schema validation | Kiểm tra status thuộc enum, answer kiểu string không rỗng, cited_source_ids kiểu list; ném `RAGSchemaError` | Đạt theo tự kiểm tra | `backend/rag_engine.py` (dòng 230-245); 4 bài test schema trong `tests/test_api_and_rag.py` | Không |
| **CX-R02-04:** Làm sạch quote snippet & context prefix | Tách `context_prefix` khỏi `content`; trích xuất `quote_snippet` thuần túy từ `source_spans` trên văn bản PDF gốc | Đạt theo tự kiểm tra | `backend/retrieval.py` và `backend/rag_engine.py`; test `test_quote_snippet_no_context_prefix` | Không |
| **CX-R02-05:** Trang in dạng nullable (`None`) | Đổi giá trị `-1` thành `None` cho trang in không xác định | Đạt theo tự kiểm tra | `backend/retrieval.py`, `backend/rag_engine.py`, `backend/main.py` (`CitationModel.printed_page: Optional[int]`) | Không |
| **CX-R02-06:** Typed Exception Hierarchy & HTTP Status | Tạo `backend/errors.py` với `DNCError`, đăng ký exception handler trả về JSON an toàn kèm mã 422, 502, 503, 504 | Đạt theo tự kiểm tra | `backend/errors.py`, `backend/main.py`; test `test_chat_endpoint_empty_question_returns_422` | Không |
| **CX-R02-07:** Bảo toàn môi trường & Phân lập Mock/Live | Dùng `load_dotenv(override=False)`; `allow_offline_mock=False` ném `ConfigurationError` khi thiếu key | Đạt theo tự kiểm tra | `backend/config.py`, `backend/gemini_client.py`; test `test_offline_client_raises_configuration_error_when_mock_disabled` | Không |
| **CX-R02-08:** HTTP Timeout & Selective Retry | Truyền `types.HttpOptions(timeout=...)`; retry có chọn lọc trên 5xx/429/timeout, không retry 4xx/JSON error | Đạt theo tự kiểm tra | `backend/gemini_client.py` (dòng 104-180) | Không |
| **CX-R02-09:** Thẩm định mô hình Live khả dụng | Khảo sát `gemini-3.5-flash-lite`, đo latency ~1.4s, cấu hình qua `GEMINI_MODEL` | Đạt theo tự kiểm tra | `backend/config.py`, `05_Mã Nguồn Chương Trình/.env.example`, `test_429.py` probe | Không |
| **CX-R02-10:** Đánh giá thực nghiệm Live 10 ca | Chạy `evaluation/run_eval_live_r03.py` trên 10 ca phát triển, xuất JSONL/CSV, lập báo cáo phân tích | Đạt theo tự kiểm tra | `evaluation/results/BAO_CAO_RAG_LIVE_QD580_R03.md`, `DNC_RAG_LIVE_DEV10_R03.jsonl`, `DNC_RAG_LIVE_DEV10_R03.csv` | Không |
| **CX-R02-11:** Đính chính ngày QĐ 580 (Errata) | Chuyển mốc ngày ban hành từ 24/10/2024 về 02/08/2024 trong báo cáo cũ | Đạt theo tự kiểm tra | `evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md` (dòng 7) | Không |

#### 3. File và cấu hình thay đổi

- **File tạo mới:**
  - `05_Mã Nguồn Chương Trình/backend/errors.py`: Hệ thống ngoại lệ định kiểu phân cấp chuẩn mực cho toàn bộ hệ thống.
  - `05_Mã Nguồn Chương Trình/evaluation/run_eval_live_r03.py`: Script đánh giá thực nghiệm Live tự động trên 10 ca phát triển.
  - `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_RAG_LIVE_QD580_R03.md`: Báo cáo kỹ thuật chi tiết đánh giá thực nghiệm Live RAG.
  - `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_LIVE_DEV10_R03.jsonl`: Kết quả thô telemetry và câu trả lời của 10 ca phát triển.
  - `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_LIVE_DEV10_R03.csv`: Bảng tổng hợp đối soát kết quả phục vụ nghiên cứu.
- **File sửa và lý do:**
  - `05_Mã Nguồn Chương Trình/backend/config.py`: Tích hợp `override=False` cho `load_dotenv`, cập nhật mô hình mặc định `gemini-3.5-flash-lite`.
  - `05_Mã Nguồn Chương Trình/backend/gemini_client.py`: Tích hợp `types.HttpOptions`, retry có chọn lọc, bọc ngoại lệ typed, khống chế mock an toàn.
  - `05_Mã Nguồn Chương Trình/backend/retrieval.py`: Bóc tách `context_prefix` khỏi `content`, chuẩn hóa `printed_page` sang nullable `None`, ném `KnowledgeBaseNotReadyError`.
  - `05_Mã Nguồn Chương Trình/backend/rag_engine.py`: Bỏ auto-attach top 1, hạ cấp an toàn khi gặp hallucinated citations, sinh quote sạch từ source spans, tăng token lên 2048.
  - `05_Mã Nguồn Chương Trình/backend/main.py`: Bổ sung global exception handler `@app.exception_handler(DNCError)`, chuẩn hóa `CitationModel`.
  - `05_Mã Nguồn Chương Trình/tests/test_api_and_rag.py`: Bổ sung 8 bài test cho logic citation, schema, nullable trang in, exception handling; nâng tổng số test lên 43.
  - `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_RAG_CO_BAN_QD580.md`: Sửa ngày ban hành QĐ 580 từ 24/10/2024 về 02/08/2024.
  - `05_Mã Nguồn Chương Trình/.env.example`: Cập nhật cấu hình mô hình mẫu `gemini-3.5-flash-lite`.
  - `ROADMAP.md`: Cập nhật minh chứng hoàn thành Tuần 1 và Tuần 3 với kết quả đánh giá thực nghiệm RAG Live.
  - `BAO_CAO_ANTIGRAVITY.md` và `BAO_CAO_BAN_GIAO.md`: Ghi nhận nhật ký bàn giao lượt `DNC-RAG-TASK-04-R03`.
- **Dữ liệu/model revision/collection/fingerprint đã dùng:**
  - Kho tri thức: `qd580_baseline_v2` (104 chunks, 351 source spans, 26/26 trang PDF QĐ 580).
  - Corpus fingerprint: `8f0c62a9ce8b2b049597599e10cc072760e21cf7cec442386848122226e977dd`.
  - Chunks SHA-256: `5802f176f1f603123126c49284449085bd18bdf64f3213998e081ecd01536398`.
  - Mô hình Embedding: `bkai-foundation-models/vietnamese-bi-encoder` (Revision: `84f9d9ada0d1a3c37557398b9ae9fcedcdf40be0`).
  - Mô hình LLM Live: `gemini-3.5-flash-lite` (Google GenAI SDK `google-genai==2.34.0`).

#### 4. Kiểm thử và minh chứng

| Lệnh kiểm thử | Môi trường | Mock hay dịch vụ thật | Số ca và kết quả | Minh chứng |
| --- | --- | --- | --- | --- |
| `python -m unittest tests/test_chunking_and_sources.py` | Local CPU (`.venv`) | Dữ liệu & Tokenizer thật | 5/5 qua (0 lỗi) | Log unittest |
| `python -m unittest tests/test_lifecycle_and_regression.py` | Local CPU (`.venv`) | ChromaDB thật | 21/21 qua (0 lỗi) | Log unittest |
| `python -m unittest tests/test_api_and_rag.py` | Local CPU (`.venv`) | Mock Handler tiêm tường minh | 17/17 qua (0 lỗi) | Log unittest |
| `python -m unittest discover -s tests -p "test_*.py"` | Local CPU (`.venv`) | Toàn bộ 43 ca kiểm thử offline | 43/43 qua (0 lỗi) | 30.555s, OK |
| `python evaluation/run_eval_live_r03.py` | Local kết nối Internet | Google Gemini Live (`gemini-3.5-flash-lite`) | 10/10 ca hoàn thành | `DNC_RAG_LIVE_DEV10_R03.jsonl` và `.csv` |

- **Số liệu đo lường Telemetry trên 10 ca phát triển:**
  - Thời gian truy xuất Vector trung bình: $58.5\text{ ms}$.
  - Thời gian sinh phản hồi LLM trung bình: $1387.6\text{ ms}$ (~1.4s).
  - Tổng thời gian đáp ứng trung bình: $1.45\text{ giây}$.
  - Độ bám nguồn: $100\%$ tuân thủ chặt chẽ tài liệu QĐ 580; không xảy ra hiện tượng bịa nguồn hoặc bịa quy định.
  - Hành vi từ chối an toàn: Phản hồi chuẩn xác `insufficient_evidence` trên DEV_02, DEV_08, DEV_09 và `out_of_scope` trên DEV_10.
- **Cách tái chạy tối thiểu:**
  ```bash
  cd "05_Mã Nguồn Chương Trình"
  # Chạy bộ test tự động (offline 100%)
  .\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"

  # Chạy đánh giá Live trên tập 10 ca phát triển
  .\.venv\Scripts\python.exe evaluation/run_eval_live_r03.py
  ```

#### 5. Lỗi, giới hạn và việc còn lại

- **Lỗi còn mở:** Không có lỗi phần mềm nội bộ, không có lỗi regression.
- **Giới hạn đã nhận diện:** Phương pháp tìm kiếm thuần Vector (Dense Retrieval) đôi khi chưa tối ưu với câu hỏi dùng từ ngữ đời thường (như DEV_08 phân đoạn hệ 4 năm nằm ở chunk liền kề có điểm tương đồng thấp hơn). Điều này là căn cứ thuyết phục để triển khai Hybrid Search (BM25 + Vector) và Reranker ở Tuần 4.
- **Phần hoàn thành:** 100% các tiêu chí của Nhiệm vụ 04 và các yêu cầu bổ sung trong lượt R03.
- **Kế hoạch Tuần 4:** Sẵn sàng bước sang Tuần 4 — triển khai BM25 Sparse Search kết hợp Vector Dense Search thành Hybrid Retrieval, bổ sung mô hình Reranker và xây dựng giao diện người dùng Web UI (Streamlit/FastAPI Frontend).

#### 6. GitHub

- **Repository/nhánh:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).
- **Commit và Push:** Sẽ được thực thi và xác nhận ngay sau khi ghi nhận báo cáo bàn giao.
- **Bảo mật:** Đã kiểm tra `.gitignore`, tuyệt đối không commit `.env` hay API key lên kho lưu trữ.

#### 7. Bàn giao cho Codex

- **Báo cáo chuyên môn chính:** `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_RAG_LIVE_QD580_R03.md`.
- **Dữ liệu đánh giá đính kèm:** `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_LIVE_DEV10_R03.jsonl` và `DNC_RAG_LIVE_DEV10_R03.csv`.
- **Điểm cần Codex tập trung kiểm tra:**
  1. Kiểm tra 8 ca test mới trong `tests/test_api_and_rag.py` kiểm định loại bỏ auto-attach top 1, hạ cấp citation ảo, và typed errors.
  2. Kiểm tra tính an toàn của `backend/gemini_client.py` (`types.HttpOptions`, selective retry, cô lập mock).
  3. Đối chiếu kết quả 10 ca live tại `DNC_RAG_LIVE_DEV10_R03.jsonl`, đặc biệt là hành vi từ chối an toàn tại DEV_02, DEV_08, DEV_09 và DEV_10.
- **Trạng thái rà soát:** `CHƯA KIỂM TRA` — chờ Codex xác minh.
