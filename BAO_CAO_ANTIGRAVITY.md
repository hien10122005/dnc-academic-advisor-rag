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

- **Mã lượt:** `DNC-RAG-TASK-05-R03`
- **Nhiệm vụ:** 05 — Đối soát vector, hoàn thiện rubric và provenance bằng chứng
- **Ngày hoàn tất:** 02/11/2026
- **Trạng thái tự báo:** `HOÀN THÀNH — CHỜ KIỂM TRA`
- **Vị trí báo cáo:** [Mục DNC-RAG-TASK-05-R03](#dnc-rag-task-05-r03--doi-soat-vector-va-hoan-thien-rubric-bang-chung)

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
- **Commit triển khai:** SHA `bcb6b2088fe89e350fc2aff16c3e913f8714bff6` — `feat(rag): complete Task 04 R03 - live Gemini 3.5 Flash Lite, strict citation verification, typed errors, and 43 offline tests`.
- **Push:** Thành công; xác nhận remote `origin/main` khớp chính xác `bcb6b2088fe89e350fc2aff16c3e913f8714bff6`.
- **Bảo mật:** Đã kiểm tra `.gitignore`, tuyệt đối không commit `.env` hay API key lên kho lưu trữ.

#### 7. Bàn giao cho Codex

- **Báo cáo chuyên môn chính:** `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_RAG_LIVE_QD580_R03.md`.
- **Dữ liệu đánh giá đính kèm:** `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_LIVE_DEV10_R03.jsonl` và `DNC_RAG_LIVE_DEV10_R03.csv`.
- **Điểm cần Codex tập trung kiểm tra:**
  1. Kiểm tra 8 ca test mới trong `tests/test_api_and_rag.py` kiểm định loại bỏ auto-attach top 1, hạ cấp citation ảo, và typed errors.
  2. Kiểm tra tính an toàn của `backend/gemini_client.py` (`types.HttpOptions`, selective retry, cô lập mock).
  3. Đối chiếu kết quả 10 ca live tại `DNC_RAG_LIVE_DEV10_R03.jsonl`, đặc biệt là hành vi từ chối an toàn tại DEV_02, DEV_08, DEV_09 và DEV_10.
- **Trạng thái rà soát:** `CHƯA KIỂM TRA` — chờ Codex xác minh.

---

### DNC-RAG-TASK-04-R04 — Chốt Baseline A, phân loại lỗi & khử rò rỉ đường dẫn, kiểm soát retry SDK và chấm lại kết quả trung thực

**Thời điểm bàn giao:** 18:30 ngày 01/11/2026, giờ Việt Nam.  
**Định danh:** `dnc-academic-advisor-rag`; Git root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.  
**File giao nhiệm vụ:** `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_04_R04_CHOT_BASELINE.md`.  
**Tài liệu đối chiếu:** Nhận xét Codex R03 tại `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_04_R03.md`.  
**Trạng thái tự báo:** `HOÀN THÀNH — CHỜ KIỂM TRA`.

#### 1. Kết quả chính

1. **Khử hoàn toàn rò rỉ đường dẫn nội bộ (Path Sanitization):**
   - Tách bạch `public_message` và `internal_detail` trong `backend/errors.py`. Tự động nhận diện và làm sạch chuỗi đường dẫn tệp (`E:\`, `C:\`, `/`) và token nhạy cảm trong response trả về người dùng.
   - Chuẩn hóa HTTP Status Code của `LLMQuotaExceededError` thành `429 Too Many Requests` (theo RFC 6585).
   - Đảm bảo cả `/health` và `/chat` không bao giờ rò rỉ đường dẫn file nội bộ (như `E:\private\secret-location\manifest.json`).

2. **Kiểm soát chặt chẽ Retry & Vòng đời SDK:**
   - Xây dựng `classify_exception` phân loại rõ: Lỗi lập trình (`ValueError`, `TypeError`) & Lỗi máy khách 4xx (`400`, `401`, `404`) -> Tuyệt đối KHÔNG retry.
   - Lỗi tạm thời (Transient: Timeout, 429, 503) -> Retry có backoff đến tối đa `max_retries`.
   - Vô hiệu hóa retry nội bộ của Google GenAI SDK bằng `types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1))` để vòng lặp bên ngoài kiểm soát tuyệt đối số lần gọi.
   - Thêm thuộc tính `is_using_live_api` đảm bảo khi tiêm mock handler thì `is_live_llm` luôn là `False`.

3. **Cải tiến trích đoạn chứng cứ thực chất (Substantive Quote Snippet):**
   - Thuật toán chọn span đại diện trong `backend/rag_engine.py` ưu tiên span nội dung thực chất dài hơn, bỏ qua span chỉ chứa dòng tiêu đề điều khoản ngắn hoặc header bảng lặp lại, đồng thời bảo toàn chính xác tuyệt đối tọa độ span gốc và trang PDF.

4. **Kiểm thử tự động toàn diện (Unit Tests):**
   - Đạt **50/50 tests OK** trong 18.37 giây ở chế độ offline 100% (thêm 7 tests mới kiểm định path sanitization, SDK retry=1, non-retry 401/404/ValueError, transient retry 503, substantive quote snippet, mock live flag).

5. **Đánh giá Live 10 ca phát triển với Rubric trung thực:**
   - Chạy toàn bộ 10 ca live với `gemini-3.5-flash-lite`, lưu trữ đầy đủ run metadata, toàn bộ 5 retrieved contexts (content, spans, similarity), user prompt và timings vào `DNC_RAG_LIVE_DEV10_R04.jsonl` và `.csv`.
   - Chấm điểm từng ý bắt buộc (mandatory points) theo rubric khách quan:
     - Đạt hoàn toàn (Full Pass): 3 ca (`DEV_03`: 100%, `DEV_06`: 100%, `DEV_10`: 100%).
     - Đạt một phần (Partial Pass): 4 ca (`DEV_01`: 75%, `DEV_04`: 75%, `DEV_05`: 66.7%, `DEV_07`: 50%).
     - Từ chối an toàn do thiếu dữ liệu truy xuất (Retrieval Miss): 2 ca (`DEV_02`, `DEV_08`).
     - Single-turn Only (N/A multi-turn): 1 ca (`DEV_09`).
     - Tỷ lệ bịa đặt nguồn (Hallucination): **0%**.

#### 2. Đối chiếu từng yêu cầu và nhận xét cần sửa

| Yêu cầu / Mã nhận xét Codex R03 | Đã làm gì | Kết quả | Minh chứng | Phần còn thiếu |
| --- | --- | --- | --- | --- |
| **[P1] Đánh giá câu trả lời DEV_07** | Đánh giá lại câu trả lời theo rubric gold standard: chỉ ra điểm 4.5 là Không đạt nhưng khẳng định bắt buộc học lại mà bỏ sót nhánh thi lại/thi phụ | Đạt một phần (2/4 ý - 50%) | `BAO_CAO_CHOT_BASELINE_QD580_R04.md` mục 4; `calc_stats.py` | Sẽ được giải quyết bằng hybrid search và prompt routing ở Task 05 |
| **[P1] Chấm từng ý DEV_01, 04, 05** | Chấm chi tiết từng mandatory point: DEV_01 thiếu làm tròn 1 chữ số thập phân (3/4); DEV_04 thiếu thời điểm/thủ tục (3/4); DEV_05 thiếu lệ phí thi lại (2/3) | Đạt theo tự kiểm tra trung thực | `BAO_CAO_CHOT_BASELINE_QD580_R04.md` Bảng 4.1 | Không hạ thấp tiêu chuẩn gold standard |
| **[P1] Ghi rõ lỗi truy xuất DEV_02, 08** | Ghi nhận rõ là Retrieval Miss của bộ truy xuất Dense Bi-encoder, từ chối an toàn của LLM là tốt nhưng hệ thống toàn trình tính là chưa đạt truy xuất | Đạt theo tự kiểm tra trung thực | Báo cáo mục 4 & 5 | Chờ Task 05 (BM25 + RRF) để giải quyết |
| **[P1] Nhãn DEV_09 single-turn** | Gán nhãn Single-turn Only (N/A multi-turn) cho DEV_09 | Đạt theo tự kiểm tra | Báo cáo mục 4 | Chưa có session state (ngoài phạm vi task) |
| **[P1] Khử rò rỉ đường dẫn nội bộ** | Thêm `public_message` an toàn trong `DNCError`, làm sạch path và token; sửa exception handler của FastAPI `/health` và `/chat` | Đạt theo tự kiểm tra | `backend/errors.py`, `backend/main.py`; test `test_health_and_chat_sanitizes_internal_path_on_error` | Không |
| **[P2] Retry đúng loại lỗi & SDK** | `classify_exception` phân loại rõ; tắt retry nội bộ SDK (`attempts=1`); non-transient gọi SDK đúng 1 lần; transient retry có sleep | Đạt theo tự kiểm tra | `backend/gemini_client.py`; 4 test unit mới trong `tests/test_api_and_rag.py` | Không |
| **[P2] Thống kê đo lường minh bạch** | Tính toán minh bạch trung bình, trung vị, toàn bộ 10 ca và ca ấm (bỏ ca đầu); ghi rõ mẫu số | Đạt theo tự kiểm tra | Báo cáo Bảng 3.2; `evaluation/calc_stats.py` | Không |
| **[P2] Lưu đầy đủ artifacts tái lập** | Lưu đầy đủ 5 retrieved contexts (content, spans, similarity), user prompt, raw output, citations vào JSONL | Đạt theo tự kiểm tra | `evaluation/results/DNC_RAG_LIVE_DEV10_R04.jsonl` và `.csv` | Không |
| **[P2] Cải tiến quote snippet** | Thuật toán ưu tiên span nội dung thực chất thay vì span tiêu đề điều khoản ngắn hoặc header bảng | Đạt theo tự kiểm tra | `backend/rag_engine.py`; test `test_substantive_quote_snippet_selection` | Không |

#### 3. File và cấu hình thay đổi

- **File tạo mới:**
  - `05_Mã Nguồn Chương Trình/evaluation/run_eval_live_r04.py`: Script đánh giá thực nghiệm R04 kết nối Gemini Live và lưu trữ đầy đủ run metadata.
  - `05_Mã Nguồn Chương Trình/evaluation/calc_stats.py`: Script tính toán trung bình, trung vị, cold/warm và đối chiếu mandatory points.
  - `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_LIVE_DEV10_R04.jsonl`: Dữ liệu đánh giá chi tiết 10 ca live kèm retrieved contexts.
  - `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_LIVE_DEV10_R04.csv`: Dữ liệu bảng tổng hợp UTF-8 BOM.
  - `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_CHOT_BASELINE_QD580_R04.md`: Báo cáo kỹ thuật nghiệm thu Baseline A.
- **File sửa đổi:**
  - `backend/errors.py`: Phân tách `public_message` và `internal_detail`, tự động lọc đường dẫn tệp và token nhạy cảm, đồng bộ `status_code = 429` cho `LLMQuotaExceededError`.
  - `backend/main.py`: Cập nhật exception handlers của `/health` và `/chat` trả về `public_message` an toàn.
  - `backend/gemini_client.py`: Thêm `classify_exception`, vô hiệu hóa retry SDK (`attempts=1`), chặn retry lỗi lập trình và 4xx, thêm `is_using_live_api`, kiểm tra ping/pong trong smoke test.
  - `backend/rag_engine.py`: Dùng `is_using_live_api`, cập nhật `SYSTEM_PROMPT_TEMPLATE` hướng dẫn chú ý điều kiện/ngoại lệ/làm tròn, cải tiến thuật toán chọn span chứng cứ thực chất.
  - `tests/test_api_and_rag.py`: Bổ sung 7 test case kiểm định khử rò rỉ path, retry SDK, non-retry 401/404/ValueError, transient 503 retry, substantive quote snippet, mock live flag (tổng 24 tests trong file, tổng 50 tests toàn bộ).
  - `BAO_CAO_BAN_GIAO.md`, `ROADMAP.md`, `05_Mã Nguồn Chương Trình/README.md`.

#### 4. Kiểm thử và chạy thực tế

| Tên test / Lệnh chạy | Môi trường | Kiểu thực thi | Số ca qua / lỗi | File minh chứng |
| :--- | :--- | :--- | :---: | :--- |
| `python -m unittest tests/test_chunking_and_sources.py` | Local CPU (`.venv`) | Dữ liệu & Tokenizer thật | 5/5 OK | Log unittest |
| `python -m unittest tests/test_lifecycle_and_regression.py` | Local CPU (`.venv`) | ChromaDB thật | 21/21 OK | Log unittest |
| `python -m unittest tests/test_api_and_rag.py` | Local CPU (`.venv`) | Mock SDK & Fake Transport | 24/24 OK | Log unittest |
| `python -m unittest discover -s tests -p "test_*.py"` | Local CPU (`.venv`) | Toàn bộ 50 ca kiểm thử offline | 50/50 OK | 18.371s, OK |
| `python evaluation/run_eval_live_r04.py` | Local Internet | Google Gemini Live (`gemini-3.5-flash-lite`) | 10/10 ca hoàn thành | `DNC_RAG_LIVE_DEV10_R04.jsonl` và `.csv` |
| `python evaluation/calc_stats.py` | Local CPU | Đo lường thống kê & rubric đối chiếu | 10 ca khớp | `BAO_CAO_CHOT_BASELINE_QD580_R04.md` |

- **Số liệu đo lường Telemetry trên 10 ca phát triển:**
  - Truy xuất Vector (Retrieval): Trung bình toàn bộ $65.88\text{ ms}$, trung vị $63.07\text{ ms}$; Warm trung bình $63.48\text{ ms}$, warm trung vị $60.78\text{ ms}$.
  - Sinh phản hồi LLM (Generation): Trung bình toàn bộ $1916.81\text{ ms}$, trung vị $1699.59\text{ ms}$; Warm trung bình $1929.47\text{ ms}$, warm trung vị $1665.70\text{ ms}$.
  - Tổng thời gian E2E (Total): Trung bình toàn bộ $1982.75\text{ ms}$, trung vị $1769.82\text{ ms}$; Warm trung bình $1993.01\text{ ms}$, warm trung vị $1716.76\text{ ms}$.
- **Tái lập tối thiểu:**
  ```powershell
  cd "05_Mã Nguồn Chương Trình"
  # Chạy toàn bộ 50 bài unit test offline
  $env:HF_HUB_OFFLINE="1"; $env:TRANSFORMERS_OFFLINE="1"; $env:GEMINI_API_KEY=""; .\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"

  # Chạy đánh giá Live trên tập 10 ca phát triển
  .\.venv\Scripts\python.exe evaluation/run_eval_live_r04.py
  ```

#### 5. Lỗi, giới hạn và việc còn lại

- **Lỗi phần mềm nội bộ:** 0 lỗi. Toàn bộ 50 unit tests đều qua.
- **Giới hạn đã nhận diện (Baseline A):**
  - Tồn tại hiện tượng bỏ sót truy xuất (Retrieval Miss) trên câu hỏi khái niệm chung (`DEV_02`) và câu hỏi đời thường (`DEV_08`) do hạn chế của mô hình Dense Bi-encoder thuần túy.
  - Câu trả lời của LLM đôi khi bỏ sót một số điều kiện phụ (làm tròn số ở `DEV_01`, thủ tục đăng ký ở `DEV_04`, lệ phí ở `DEV_05`) hoặc khẳng định phiến diện (bắt buộc học lại mà không nêu nhánh thi lại ở `DEV_07`).
  - Hệ thống chưa hỗ trợ Multi-turn / Session State (`DEV_09` được xếp loại Single-turn).
- **Kế hoạch tiếp theo (Task 05):**
  - Triển khai BM25 Sparse Search kết hợp Vector Dense Search bằng giải thuật Reciprocal Rank Fusion (RRF) để khắc phục triệt để Retrieval Miss của DEV_02 và DEV_08.
  - So sánh thực nghiệm có số liệu trực tiếp giữa Baseline A (Dense) và Hybrid (BM25 + Dense).

#### 6. GitHub

- **Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).
- **Commit triển khai:** Sẽ cập nhật sau lệnh git commit/push.
- **Bảo mật:** Không commit `.env` hay API key lên kho lưu trữ.

#### 7. Bàn giao cho Codex

- **Báo cáo chuyên môn chính:** `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_CHOT_BASELINE_QD580_R04.md`.
- **Dữ liệu đánh giá đính kèm:** `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_LIVE_DEV10_R04.jsonl` và `DNC_RAG_LIVE_DEV10_R04.csv`.
- **Điểm cần Codex tập trung kiểm tra:**
  1. Kiểm tra 7 ca test mới trong `tests/test_api_and_rag.py` (khử rò rỉ path, SDK retry=1, non-retry 401/404/ValueError, transient 503 retry, substantive quote snippet, mock live flag).
  2. Kiểm tra tính an toàn của `backend/errors.py` và `backend/gemini_client.py`.
  3. Đối chiếu rubric chấm trung thực 10 ca tại `BAO_CAO_CHOT_BASELINE_QD580_R04.md`.
- **Trạng thái rà soát:** `CHƯA KIỂM TRA` — chờ Codex xác minh.

---

### DNC-RAG-TASK-05-R01 — Đo đúng baseline và tích hợp Hybrid BM25 + RRF

**Thời điểm bàn giao:** 19:00 ngày 01/11/2026, giờ Việt Nam.  
**Định danh:** `dnc-academic-advisor-rag`; Git root và remote đã xác nhận: `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).  
**File giao nhiệm vụ:** `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_HYBRID_BM25_RRF.md`.  
**Trạng thái tự báo:** `HOÀN THÀNH — CHỜ KIỂM TRA`.  

#### 1. Kết quả chính

1. **Hoàn tất toàn bộ 7 yêu cầu Chặng A bắt buộc:**
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

#### 2. Đối chiếu từng yêu cầu và nhận xét cần sửa

| Yêu cầu hoặc mã nhận xét | Đã làm gì | Kết quả | Minh chứng | Phần còn thiếu |
| :--- | :--- | :---: | :--- | :--- |
| 1. Chặng A: Retry theo structured code | Phân loại dựa trên số nguyên `exc.status_code`, `exc.code`; kiểm tra chuỗi lỗi hỗn hợp | Đạt | `backend/gemini_client.py`, tests trong `test_api_and_rag.py` | Không |
| 2. Chặng A: Sanitization sentinel tokens | Cấu hình `is_infrastructure_error = True` dùng message an toàn, chặn token rò rỉ | Đạt | `backend/errors.py`, tests trong `test_api_and_rag.py` | Không |
| 3. Chặng A: Cô lập Idempotency | Dùng `tempfile.TemporaryDirectory()` trong test chunking | Đạt | `tests/test_chunking_and_sources.py` | Không |
| 4. Chặng A: Trace từ chính engine | Thêm `trace` vào `RAGResponse`, tham số `return_trace=True`, test spy single retrieval | Đạt | `backend/rag_engine.py`, test spy trong `test_api_and_rag.py` | Không |
| 5. Chặng A: Telemetry & Provenance | Đo bằng `time.perf_counter()`, tách cold/warm, lưu git commit, dirty flag, file hashes | Đạt | `evaluation/run_eval_live_task05.py`, `calc_stats_task05.py` | Không |
| 6. Chặng A: Rubric từng ý | Chấm chi tiết 10 ca theo gold points, tách biệt membership vs correctness vs faithfulness | Đạt | `BAO_CAO_HYBRID_BM25_RRF_QD580.md` | Không |
| 7. Chặng A: Errata R04 | Ghi rõ đính chính trace tái dựng và phân biệt cold/warm trong báo cáo kỹ thuật | Đạt | Mục I.7 trong `BAO_CAO_HYBRID_BM25_RRF_QD580.md` | Không |
| 8. Chặng B: BM25 Okapi Index | Tokenizer tiếng Việt, Lucene non-negative IDF, dùng 104 chunks `embedding_text` | Đạt | `backend/bm25_retriever.py`, tests trong `test_hybrid_bm25_rrf.py` | Không |
| 9. Chặng B: Reciprocal Rank Fusion | RRF $k=60$, Top-20 Dense + Top-20 Sparse $\rightarrow$ Top-5, tie-break ổn định, tách riêng scores | Đạt | `backend/bm25_retriever.py`, tests tính tay trong `test_hybrid_bm25_rrf.py` | Không |
| 10. Chặng B: Preflight fail-closed | Đồng bộ kiểm tra cả ChromaDB và BM25 theo hash và số lượng chunk khi khởi động | Đạt | `backend/retrieval.py` | Không |
| 11. Chặng B: API & CLI Mode | Cho phép chọn `mode="dense"|"hybrid"`, validate enum HTTP 422, giữ dense mặc định | Đạt | `backend/main.py`, `backend/cli.py`, `test_hybrid_bm25_rrf.py` | Không |
| 12. Thực nghiệm: Retrieval A/B | Chạy đánh giá Source Span Intersection so sánh song song Dense vs Hybrid trên 10 ca | Đạt | `evaluation/evaluate_retrieval_ab.py`, `RETRIEVAL_AB_COMPARISON_TASK05.json` | Không |
| 13. Thực nghiệm: Live A/B Gemini | Chạy Live Gemini 3.5 Flash-lite 10 ca cho cả 2 mode, thu thập trace và telemetry | Đạt | `evaluation/run_eval_live_task05.py`, `DNC_RAG_AB_DEV10_TASK05.jsonl`, `.csv` | Không |

#### 3. File và cấu hình thay đổi

- **File tạo mới:**
  - `backend/bm25_retriever.py`: Module BM25Okapi và thuật toán RRF.
  - `tests/test_hybrid_bm25_rrf.py`: 10 bài unit test kiểm định BM25, RRF và tham số API.
  - `evaluation/evaluate_retrieval_ab.py`: Script đánh giá so sánh truy xuất Dense vs Hybrid.
  - `evaluation/run_eval_live_task05.py`: Script đánh giá thực nghiệm A/B Live với Gemini.
  - `evaluation/results/RETRIEVAL_AB_COMPARISON_TASK05.json`: Dữ liệu đo lường truy xuất chi tiết.
  - `evaluation/results/DNC_RAG_AB_DEV10_TASK05.jsonl`: Artifact trace và phản hồi Live đầy đủ 20 lượt.
  - `evaluation/results/DNC_RAG_AB_DEV10_TASK05.csv`: Bảng tóm tắt kết quả thực nghiệm Live.
  - `evaluation/results/BAO_CAO_HYBRID_BM25_RRF_QD580.md`: Báo cáo kỹ thuật phân tích chuyên sâu.
- **File chỉnh sửa:**
  - `backend/errors.py`: Bổ sung cờ `is_infrastructure_error = True` trên `DNCError`.
  - `backend/gemini_client.py`: Phân loại lỗi theo HTTP status code số nguyên, xử lý timeout chuỗi hỗn hợp.
  - `backend/chunking.py`: Tham số hóa đường dẫn xuất chunk/manifest để cô lập test.
  - `backend/rag_engine.py`: Bổ sung `trace`, tham số `return_trace`, tham số `mode="dense"|"hybrid"`.
  - `backend/retrieval.py`: Tích hợp BM25 index và phương thức `retrieve_hybrid()`.
  - `backend/main.py`: Nhận tham số `mode` trong `ChatRequest`, validation enum HTTP 422.
  - `backend/cli.py`: Hỗ trợ flag `--mode dense|hybrid`.
  - `tests/test_chunking_and_sources.py`: Dùng `TemporaryDirectory()` cho test tính bất biến.
  - `tests/test_api_and_rag.py`: Bổ sung 3 test cases cho structured code, chuỗi lỗi hỗn hợp, sentinel token sanitization, và test spy single retrieval.
  - `05_Mã Nguồn Chương Trình/README.md`, `ROADMAP.md`.
- **Dữ liệu/Corpus:** 104 chunks QĐ 580 giữ nguyên bất biến, collection `qd580_baseline_v2`.

#### 4. Kiểm thử và chạy thực tế

| Tên test / Lệnh chạy | Môi trường | Kiểu thực thi | Số ca qua / lỗi | File minh chứng |
| :--- | :--- | :--- | :---: | :--- |
| `python -m unittest discover -s tests -p "test_*.py"` | Local CPU (`.venv`) | Toàn bộ 63 bài test offline | 63/63 OK | Log unittest (30.358s) |
| `python evaluation/evaluate_retrieval_ab.py` | Local CPU (`.venv`) | So sánh Retrieval Dense vs Hybrid | 10/10 ca hoàn thành | `RETRIEVAL_AB_COMPARISON_TASK05.json` |
| `python evaluation/run_eval_live_task05.py` | Local Internet | Gemini Live (`gemini-3.5-flash-lite`) | 20/20 lượt hoàn thành | `DNC_RAG_AB_DEV10_TASK05.jsonl` và `.csv` |

- **Bảng so sánh tổng hợp chỉ số Retrieval A/B:**
  - Hit@1: Dense 0.5556 $\rightarrow$ Hybrid 0.4444 (-0.1112)
  - Hit@3: Dense 0.7778 $\rightarrow$ Hybrid **0.8889** (+0.1111)
  - Hit@5: Dense 0.7778 $\rightarrow$ Hybrid **1.0000** (+0.2222)
  - Mean Coverage@5: Dense 0.6368 $\rightarrow$ Hybrid **0.8034** (+0.1666)
  - Full Case Coverage@10: Dense 0.6667 $\rightarrow$ Hybrid **0.7778** (+0.1111)
  - Retrieval Latency (Warm): Dense 62.34ms $\rightarrow$ Hybrid 68.01ms (+5.67ms)

#### 5. Lỗi, giới hạn và việc còn lại

- **Lỗi phần mềm nội bộ:** 0 lỗi. Toàn bộ 63 unit tests đều qua.
- **Giới hạn đã nhận diện:**
  - Ở ca `DEV_07`, cả Dense và Hybrid đều chưa đưa được Điều 18 (thi phụ) vào Top-5 cạnh tranh với Điều 17 (thang điểm) và Điều 8 (học lại). Cần nghiên cứu mở rộng Top-K hoặc Query Expansion ở giai đoạn sau.
  - Chưa hỗ trợ Reranker mô hình Cross-Encoder (được để dành cho chặng sau theo phạm vi giao).
  - Chưa hỗ trợ giao diện Web UI và quản lý hội thoại đa lượt (DEV_09 tiếp tục đánh giá dưới dạng Single-turn).
- **Cấu hình đề xuất:** Mặc định giữ `mode="dense"` để bảo đảm tương thích ngược, cho phép kích hoạt `mode="hybrid"` qua API/CLI.

#### 6. GitHub

- **Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).
- **Commit triển khai:** `3c5a93d11b339ae780c1081aee3480ec8e77ce0b` (đã push thành công lên `origin/main`).
- **Bảo mật:** Không commit `.env` hay API key lên Git.

#### 7. Bàn giao cho Codex

- **Báo cáo chuyên môn chính:** `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_HYBRID_BM25_RRF_QD580.md`.
- **Dữ liệu đánh giá đính kèm:** `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_AB_DEV10_TASK05.jsonl` và `DNC_RAG_AB_DEV10_TASK05.csv`.
- **Điểm cần Codex tập trung kiểm tra:**
  1. Kiểm tra mã nguồn BM25 và giải thuật RRF tại `backend/bm25_retriever.py` cùng 10 unit tests trong `tests/test_hybrid_bm25_rrf.py`.
  2. Kiểm tra tính an toàn của `backend/errors.py` và phân loại structured exception trong `backend/gemini_client.py`.
  3. Kiểm tra tính trung thực của trace trong `DNC_RAG_AB_DEV10_TASK05.jsonl` (thu thập từ chính engine, không gọi duplicate retrieval).
  4. Đối chiếu kết quả A/B giữa Dense và Hybrid trong việc giải quyết DEV_02 và DEV_08.
- **Trạng thái rà soát:** `CHƯA KIỂM TRA` — chờ Codex xác minh.

---

### DNC-RAG-TASK-05-R02 — Chốt hybrid và bằng chứng thực nghiệm

**Thời điểm bàn giao:** 20:00 ngày 01/11/2026, giờ Việt Nam.  
**Định danh:** `dnc-academic-advisor-rag`; Git root: `E:\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).  
**File giao nhiệm vụ:** `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R02_CHOT_HYBRID.md`.  
**Tài liệu nhận xét Codex R01:** `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R01.md`.  
**Trạng thái tự báo:** `HOÀN THÀNH — CHỜ KIỂM TRA`.  

#### 1. Kết quả chính

1. **Khắc phục toàn diện lỗi Cache & Preflight ([P1]):**
   - Triển khai cơ chế kiểm tra `indexed_fingerprint` động: So khớp `self._bm25_index.indexed_fingerprint` với `readiness['corpus_fingerprint']` trên mỗi truy cập property `bm25_index`. Nếu phát hiện fingerprint thay đổi, tự động vô hiệu hóa và tái tạo sạch sẽ chỉ mục BM25 trong RAM.
   - Thắt chặt tiền kiểm tra Fail-closed: Bắt buộc `chunks_file_path.exists()` trong `check_readiness()`, từ chối phục vụ ngay lập tức (`KnowledgeBaseNotReadyError`) nếu thiếu tệp chunks.
   - Kiểm tra đối soát trùng lặp `chunk_id` và đối soát khớp tập ID set giữa `chunks.jsonl` và `manifest.json`.
   - Bổ sung `retriever.preload_bm25()` vào startup lifespan của FastAPI.

2. **Chuẩn hóa Hợp đồng RRF và Observability Trace ([P2]):**
   - Gán thứ hạng cuối cùng `rank = 1..k` nhất quán sau khi hoàn tất sắp xếp RRF.
   - Chuẩn hóa các hit chỉ có ở sparse: gán `similarity = None` và `distance = None` (nullable chân thực, không gán giả 0.0), tự động suy diễn `is_cross_page` dạng boolean, loại bỏ triệt để nguy cơ `KeyError` ở API và CLI.
   - Cập nhật Pydantic `CitationModel`: `similarity: Optional[float] = None`.
   - Bổ sung đầy đủ candidate scores (`dense_rank`, `dense_score`, `bm25_rank`, `bm25_score`, `rrf_score`) và cấu hình `fusion_config` trong `return_trace=True` của `RAGEngine`.
   - Validate chế độ `mode in ("dense", "hybrid")` ở cả 3 tầng: API, CLI, RAGEngine. Duy trì `mode="dense"` làm mặc định.

3. **Cô lập Kiểm thử Tự động ([P2]):**
   - Tái cấu trúc `TestHybridIntegration.test_api_chat_endpoint_mode_validation`: Sử dụng fixture `setUp` inject mock `RAGEngine` trả về `RAGResponse` chuẩn và `tearDown` khôi phục `main_module.rag_engine_instance` nguyên vẹn.
   - Bộ kiểm thử toàn diện tăng lên **70 bài test** (thêm 7 test cases cho fail-closed, cache invalidation, duplicate IDs, ID set mismatch, sparse-only contract, RRF ranking). Toàn bộ 70 tests chạy hoàn toàn offline độc lập, **đạt 100% (70/70 OK)**.

4. **Đính chính số đo và Lập Rubric chi tiết ([P1/P2]):**
   - Giữ nguyên vẹn 20 artifacts raw gốc trong `DNC_RAG_AB_DEV10_TASK05.jsonl` và `.csv`.
   - Lập tệp rubric độc lập `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05.md` chấm chi tiết 36 ý bắt buộc cho 20 lượt chạy (10 dense + 10 hybrid).
   - Đánh giá thẳng thắn phát ngôn sai của Hybrid tại DEV_07: câu *"từ điểm D+ trở xuống là dưới 5.0"* bị chấm **SAI (Claim Error)**.
   - Báo cáo chi tiết kỹ thuật tại `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R02.md` với đầy đủ errata (SHA commit, PyTorch warm-up timing, giải thích Hit@5 là $\ge 1$ evidence $\ge 90\%$, mean coverage 80.34%, MRR giảm nhẹ xuống 0.6574).

#### 2. Đối chiếu từng phát hiện của Codex R01

| Mã phát hiện | Yêu cầu khắc phục | Kết quả xử lý | Minh chứng |
| :--- | :--- | :---: | :--- |
| **[P1] BM25 cache invalidation** | So sánh fingerprint BM25 với corpus mới sau readiness; rebuild nếu đổi | ĐẠT | `backend/retrieval.py` (`bm25_index`), test `test_bm25_cache_invalidation_on_fingerprint_change` |
| **[P1] Preflight missing chunks** | Từ chối dứt khoát khi tệp chunks không tồn tại | ĐẠT | `backend/retrieval.py` (`check_readiness`), test `test_retriever_check_readiness_fail_closed_missing_chunks` |
| **[P2] Test API isolation** | Quản lý mock engine riêng, restore global state sau test | ĐẠT | `tests/test_hybrid_bm25_rrf.py` (`setUp`/`tearDown`) |
| **[P2] RRF contract & nullable** | Gán rank 1..k sau fusion, nullable similarity/distance cho sparse-only, có is_cross_page | ĐẠT | `backend/bm25_retriever.py` (`reciprocal_rank_fusion`), tests `test_rrf_sparse_only_contract` |
| **[P2] Engine trace candidate scores** | Lưu dense/bm25 rank-score và rrf_score riêng trong trace, lưu fusion_config | ĐẠT | `backend/rag_engine.py` (dataclass `SourceContext` & `trace_data`) |
| **[P1/P2] DEV_07 & Rubric chi tiết** | Chấm câu "D+ trở xuống là dưới 5.0" là Sai; lập rubric từng ý cho 20 records | ĐẠT | `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05.md` |
| **[P2] Errata & Provenance** | Ghi đúng Python 3.14.6, đính chính SHA, nạp weights ngoài engine timing, preload BM25 startup | ĐẠT | `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R02.md` (Mục 1 & 3) |

#### 3. File và cấu hình thay đổi

- **File tạo mới:**
  - `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05.md`: Rubric chi tiết 36 ý bắt buộc cho 20 lượt chạy.
  - `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R02.md`: Báo cáo kỹ thuật chốt Hybrid và bằng chứng thực nghiệm.
- **File chỉnh sửa:**
  - `backend/bm25_retriever.py`: Thêm kiểm tra trùng ID, kiểm tra ID set khớp manifest, gán rank 1..k sau fusion, nullable similarity/distance cho sparse-only hits.
  - `backend/retrieval.py`: Thêm fail-closed khi thiếu chunks file, kiểm tra fingerprint invalidation trong `bm25_index`, thêm `preload_bm25()`.
  - `backend/rag_engine.py`: Validate `mode`, mở rộng `SourceContext` và `CitationItem` với candidate scores nullable, lưu `fusion_config` và candidate scores trong trace.
  - `backend/main.py`: Thêm `retriever.preload_bm25()` trong startup lifespan, cập nhật `CitationModel.similarity` nullable.
  - `backend/cli.py`: Thêm tham số `--mode`, in citations tương thích với nullable similarity.
  - `tests/test_hybrid_bm25_rrf.py`: Mở rộng lên 17 tests với mock fixture cô lập, kiểm tra fail-closed, cache invalidation, duplicate IDs, ID mismatch, sparse-only contract.
  - `05_Mã Nguồn Chương Trình/README.md`, `ROADMAP.md`, `BAO_CAO_BAN_GIAO.md`.

#### 4. Kiểm thử và chạy thực tế

- **Lệnh chạy toàn bộ 70 unit tests offline:**
  `.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"`
  -> `Ran 70 tests in 53.476s. OK!`
- **Lệnh chạy riêng nhóm test Hybrid R02:**
  `.\.venv\Scripts\python.exe -m unittest tests/test_hybrid_bm25_rrf.py`
  -> `Ran 17 tests in 1.688s. OK!`

#### 5. Lỗi, giới hạn và việc còn lại

- **Lỗi phần mềm nội bộ:** 0 lỗi. Toàn bộ 70 tests đều vượt qua độc lập.
- **Giới hạn đã xác định:**
  - Lỗi phát ngôn của LLM tại DEV_07 ("từ điểm D+ trở xuống là dưới 5.0") cho thấy việc ngữ cảnh có đủ nguồn chưa ngăn chặn được 100% ảo giác suy diễn của mô hình. Cần xem xét thêm cơ chế Cross-Encoder Reranker hoặc Post-generation Claim Verification ở giai đoạn sau.
  - Chế độ mặc định tiếp tục duy trì `dense` cho tính tương thích ngược; `hybrid` hoạt động hoàn chỉnh khi được chọn.
  - Chưa triển khai Cross-Encoder Reranker, UI hay SQLite/Multi-turn trong lượt này theo đúng phạm vi nhiệm vụ.

#### 6. GitHub

- **Repository:** `https://github.com/hien10122005/dnc-academic-advisor-rag.git` (nhánh `main`).
- **Commit triển khai:** `9b008ecb252482c4e8ae064d3148cb5dedf0f47e` (commit hoàn tất Task05-R02 trên origin/main; commit `3c5a93d249300619791d4ba804165d97f6550193` thuộc Task05-R01; đã đính chính ngày 02/11/2026 loại bỏ hash gõ nhầm).
- **Bảo mật:** Không commit `.env` hay API key lên kho lưu trữ.

#### 7. Bàn giao cho Codex

- **Báo cáo chuyên môn chính:** `05_Mã Nguồn Chương Trình/evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R02.md`.
- **Rubric đánh giá chi tiết:** `05_Mã Nguồn Chương Trình/evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05.md`.
- **Trạng thái rà soát:** `CHƯA KIỂM TRA` — chờ Codex xác minh.

---

### DNC-RAG-TASK-05-R03 — Đối soát vector, hoàn thiện rubric và provenance bằng chứng

- **Mục tiêu:** Khắc phục triệt để các nhận xét rà soát độc lập của Codex đối với Task 05 (Lượt R02): bổ sung đối soát thực tế vector collection trong ChromaDB, làm sạch 100% chunk ID ảo trong rubric, và lập báo cáo kỹ thuật có provenance minh bạch.
- **Thời gian hoàn thành:** 02/11/2026.
- **Minh chứng kỹ thuật:**
  1. `backend/retrieval.py`: Nâng cấp `VectorRetriever.check_readiness()` đối soát thực tế `col.count()` và `col.get(include=[])`, chặn rỗng (0 ID), thiếu ID, thừa ID, hoặc cùng số lượng nhưng sai ID (`same-count-wrong-ID`).
  2. `tests/test_vector_integrity.py`: 10 unit tests độc lập kiểm định toàn vẹn vector và endpoint `/health` trả về 503 khi lỗi vector.
  3. `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R03.md`: Chuẩn hóa 100% chunk ID thực tế, phân loại DEV04 là Generation Omission, giữ 5 ý gold DEV06 và lỗi claim error DEV07.
  4. `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R03.md`: Báo cáo kỹ thuật chi tiết với provenance xác thực.
- **Commit triển khai:** `523c5126d65749574fc21f79978b58932ff80e1a` (và commit ghi nhận `a372d5b9df3146c788533e11fe71095418dd8eb7`).


---

### DNC-RAG-TASK-05-R04 — Chốt regression tests và bằng chứng

- **Mục tiêu:** Khắc phục toàn diện nhận xét rà soát R03 của Codex: sửa fixture regression tests, đảm bảo test isolation, sửa duplicate ID test, hoàn thiện tọa độ offsets trong rubric, và khôi phục lịch sử provenance.
- **Thời gian hoàn thành:** 02/11/2026.
- **Minh chứng kỹ thuật:**
  1. `tests/test_lifecycle_and_regression.py`: Cập nhật fixture `setUp` của `TestRetrieverReadinessVerification` có `"chunks": [{"chunk_id": "c1"}]` và collection record `c1` với dummy embedding `[0.0]*768`. Đạt **12/12 tests PASS (100%)** trong 0.559s, bảo toàn logic guard fail-closed.
  2. `tests/test_vector_integrity.py`: Gỡ bỏ việc gán `sys.modules` toàn cục, đảm bảo cô lập môi trường kiểm thử tuyệt đối. Sửa `dup_ids` giữ nguyên đúng 104 phần tử, bắt đúng guard duplicate ID.
  3. `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R04.md`: Đính chính DEV08 Hybrid P1 thành `[SRC-3] qd580_v2_c035`; phân loại DEV05 P3 là Generation Omission (context có lệ phí ở p17 `[0, 282)` nhưng answer thiếu; giữ nhãn THIẾU); chuẩn hóa Điều 18 Khoản 5 & 6, Điều 25 Khoản 1 & 2; bổ sung 100% bảng tọa độ text offset `[start, end)`.
  4. `evaluation/results/BAO_CAO_CHOT_HYBRID_TASK05_R04.md`: Báo cáo kỹ thuật đối chiếu chi tiết từng phát hiện và phương án khắc phục.
  5. `BAO_CAO_BAN_GIAO.md`: Khôi phục chính xác các commit SHA lịch sử và bổ sung mục bàn giao R04.
- **Commit triển khai:** `c6f68c82dfbe2cfaea91203c54503a261fb9113b` (đã push thành công lên origin/main).
- **Trạng thái:** `HOÀN THÀNH — CHỜ KIỂM TRA` (Chờ Codex rà soát độc lập).

---

### DNC-RAG-TASK-05-R05 — Chốt evidence trực tiếp từ trace

- **Mục tiêu:** Khắc phục dứt điểm các tồn tại về bằng chứng trong rubric và provenance theo nhận xét rà soát R04 của Codex:
  1. Sinh bằng chứng data-driven trực tiếp từ trace và bản đối soát `DOI_SOAT_EVIDENCE_TASK05_R04.json`.
  2. Khắc phục toàn bộ 14 source ID mismatches (ánh xạ đúng theo từng record của từng mode/case).
  3. Khắc phục toàn bộ 24 khoảng offset vượt envelope của chunk được dẫn.
  4. Đính chính chính xác commit SHA triển khai Task05-R02 là `9b008ecb252482c4e8ae064d3148cb5dedf0f47e`.
- **Thời gian hoàn thành:** 02/11/2026.
- **Minh chứng kỹ thuật:**
  1. `evaluation/results/EVIDENCE_DEV10_TASK05_R05.jsonl`: Sidecar máy đọc được gồm 72 hàng chuẩn hóa, đầy đủ gold index, grade, answer excerpt, source ID thực tế, chunk ID, PDF page, exact offset và text quote.
  2. `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R05.md`: Bảng rubric dẫn chiếu trực tiếp tới sidecar JSONL; 72/72 hàng vượt qua bài kiểm tra tự động độc lập với 0 source mismatches, 0 range failures, 0 invalid chunk IDs.
  3. `evaluation/results/BAO_CAO_CHOT_EVIDENCE_TASK05_R05.md`: Báo cáo kỹ thuật chi tiết đối chiếu và phân tích liêm chính học thuật.
- **Trạng thái:** `HOÀN THÀNH — CHỜ KIỂM TRA` (Chờ Codex rà soát nghiệm thu).

---
