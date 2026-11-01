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

- **Mã lượt:** `DNC-RAG-TASK-04-R02`
- **Nhiệm vụ:** 04 — RAG cơ bản qua FastAPI và Gemini
- **Ngày hoàn tất:** 01/11/2026
- **Trạng thái tự báo:** `HOÀN THÀNH MỘT PHẦN`
- **Vị trí báo cáo:** [Mục DNC-RAG-TASK-04-R02](#dnc-rag-task-04-r02--rag-co-ban-qua-fastapi-va-gemini)

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
