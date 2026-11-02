# Codex rà soát DNC-RAG-TASK-05-R02

Ngày kiểm tra: **02/11/2026**, giờ Việt Nam. Project: `dnc-academic-advisor-rag`.

**Kết luận: CẦN SỬA có giới hạn.** Các sửa đổi cache, fusion, nullable và test API đã có hiệu quả. Chưa nghiệm thu Task05 vì readiness chưa kiểm chứng tập ID vector thực tế và rubric/báo cáo còn sai bằng chứng. Chưa chuyển sang reranker/UI/admin/multi-turn.

## 1. Phạm vi và phiên bản

- Checkout thực tế: `G:\Other computers\My computer\Đám Mây\Năm 4\Học kỳ 1 - Năm học 2026-2027\Đồ án 2 - chuyên ngành (CNTT)`; đường dẫn `E:\...` trong lịch sử là đường dẫn cũ.
- HEAD được kiểm tra: `9b008ecb252482c4e8ae064d3148cb5dedf0f47e`, nhánh `main`.
- `git ls-remote origin refs/heads/main` trả cùng SHA; remote `https://github.com/hien10122005/dnc-academic-advisor-rag.git`.
- Trước review: `git --no-optional-locks status --short --untracked-files=no` không ghi nhận thay đổi tracked. Review chỉ thêm/cập nhật tài liệu, artifact kiểm tra và scripts/log trong `scratch/`; không sửa chương trình, corpus, gold, raw output, `.env` hay DB thật. Không commit/push trong lượt review này.
- Đã đọc nhiệm vụ R02, nhận xét R01, báo cáo và rubric R02, mã nguồn liên quan, tests và 20 outputs A/B đã lưu. Không gọi lại Gemini.

## 2. Kết quả xác minh độc lập

| Hạng mục | Kết quả và giới hạn |
| --- | --- |
| Tests tập trung | **14/14 qua**, 0 fail/error, 7.961 giây trong test runner: tokenizer 3, BM25 6, RRF 4, API mode 1. Dùng nguyên test hiện có, thay imports Chroma/SentenceTransformer bằng sentinel ném lỗi nếu được gọi. Đây là unit run cô lập, không phải kiểm thử ML/Chroma tích hợp. |
| API mode chạy riêng | **1/1 qua**, 0.131 giây, tiến trình mới với cùng ML import sentinels; xác nhận fixture không phụ thuộc các module test khác. Log: `scratch/review_task05_r02_mode_only.log`. |
| Cache hai thế hệ | Qua với **hai thế hệ files thật trong thư mục tạm**: thay fingerprint/hash/ID, BM25 tạo object mới, ID cũ biến mất, ID mới có mặt. Vector client được mock. |
| Sparse-only và trace | Engine tạo citation `similarity=None`, giữ đủ dense/BM25 rank-score và RRF score; prompt trong trace khớp prompt gửi mock LLM; chỉ gọi hybrid một lần, không gọi dense dự phòng; mode lạ bị từ chối. |
| Hai CLI | `backend.cli.main` và `backend.retrieval.main` đều in được kết quả sparse-only qua dependency mock, không KeyError/format lỗi. |
| Readiness | Chặn được missing chunks, BUILDING và FAILED. **Vẫn READY khi vector client báo collection rỗng hoặc sai một ID nhưng giữ đủ 104 phần tử**; không gọi `count()`/`get()` trong các probe. |
| DB cục bộ hiện tại | Đọc SQLite bằng `mode=ro`: metadata segment của `qd580_baseline_v2` có 104 ID, không trùng, tập ID khớp chunks. Đây không phải kiểm tra HNSW/embedding hay thực thi truy vấn Chroma. Không kết luận DB hiện tại đang hỏng từ lỗi readiness. |
| Toàn suite 70 tests | **Chưa xác minh lại được.** Lệnh discover chạy từ khoảng 15:19:55 đến 15:28:12 vẫn ở bước import dependency trên ổ đồng bộ, chưa có kết quả tests. Dừng tiến trình; stack dumps ghi nhận đọc file/importlib.metadata/importlib loader, sau đó imports Chroma. Không tính lần bị dừng là 70 tests qua hoặc thất bại của sản phẩm. |
| Raw A/B | Có đủ 20 records; JSONL/CSV không thay đổi giữa `bb88f0c` và HEAD. Không sinh lại hoặc sửa output để chấm điểm. |

Minh chứng máy đọc được: [KIEM_TRA_DOC_LAP_TASK05_R02.json](KIEM_TRA_DOC_LAP_TASK05_R02.json), gồm probes, hashes corpus/raw/code, thông tin phiên bản và phạm vi mock. Scripts/log local: `scratch/review_task05_r02_isolated.py`, `scratch/review_task05_r02_isolated.log`, `scratch/review_task05_r02_runtime.py`, `scratch/review_task05_r02_static.py`, `scratch/review_task05_r02_tests.log`. Các file scratch được Git ignore.

Lệnh focused run từ thư mục mã nguồn:

```powershell
.\.venv\Scripts\python.exe -u -X utf8 ..\scratch\review_task05_r02_isolated.py
.\.venv\Scripts\python.exe -u -X utf8 ..\scratch\review_task05_r02_runtime.py
```

Full-suite attempt đặt key rỗng, `ALLOW_OFFLINE_MOCK=true`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `ANONYMIZED_TELEMETRY=False`, bật import timing và traceback mỗi 45 giây. Focused runners còn tắt discovery plugin Pydantic để tránh quét metadata không liên quan. Không thay đổi `.env` của người dùng.

## 3. Các phát hiện cần sửa

### [P1] Readiness chưa đối soát vector ID/count thực tế

Vị trí: `backend/retrieval.py:177–234`, đặc biệt bước 8 và giá trị `total_chunks` trả về từ manifest. `BM25OkapiIndex` đã kiểm ID giữa JSONL và manifest, nhưng không đối chiếu được Chroma; `check_readiness()` chỉ xem collection metadata và disk hash.

Tái hiện bằng **VectorRetriever import bình thường**, fake client/collection, status + manifest + chunks thật sao chép vào thư mục tạm:

| Vector collection giả | Metadata/hash | Kỳ vọng | Thực tế |
| --- | --- | --- | --- |
| Đúng 104 ID | Khớp | READY | READY |
| 0 ID | Vẫn khớp | Từ chối | **READY** |
| 104 ID, thay một ID bằng `REPLACED_WRONG_ID` | Vẫn khớp | Từ chối | **READY** |

Khi vector collection mất/thừa/thay ID nhưng metadata còn nguyên, health vẫn có thể công bố kho sẵn sàng và hybrid hợp nhất hai tập khác nhau. Đây là yêu cầu còn thiếu của mục 1 nhiệm vụ R02, không phải yêu cầu mở rộng corpus.

Sửa: kiểm schema/số lượng/ID duy nhất trong chunks và manifest, lấy ID thực tế từ Chroma và so tập ID cùng số lượng; mọi sai lệch phải thành `KnowledgeBaseNotReadyError`. Với baseline 104 chunks, cách kiểm trực tiếp đơn giản là đủ. Nếu cache kết quả integrity, phải có chính sách vô hiệu hóa rõ, không chỉ tin metadata do chính bên ghi lưu lại. Thêm tests temporary Chroma hoặc fake có semantics rõ cho empty/missing/extra/same-count-wrong-ID và test health từ chối.

### [P2] Rubric chưa truy nguyên đúng nguồn, có sửa nghĩa gold và nhầm lỗi retrieval với generation

Vị trí: `evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05.md`, các phần DEV02/04/05/06/09/10.

- Có **8 chuỗi chunk ID đầy đủ không tồn tại** trong corpus 104 chunks hiện tại; danh sách chính xác nằm trong artifact kiểm tra. Ví dụ DEV04-P1/P2/P3 dùng `qd580_v2_c046_reg_d11_p11_40c06ba1`; trace thực tế dùng `qd580_v2_c044_reg_d11_p11_b8f7da1b`. Hybrid DEV04-P4 phải kiểm `SRC-2 = qd580_v2_c045_reg_d11_p11_546fe1b1`, không phải `qd580_v2_c047_reg_d11_p11_545cf0fe` như rubric ghi.
- Dense DEV04-P4 ghi không lấy được đoạn quy trình. Thực tế trace có `c045` ở SRC-2; LLM đã không đưa ý này vào answer. `c047` thực tế cũng có trong Top-5 Dense. Điểm **THIẾU** có thể giữ, nhưng phải sửa nguyên nhân và nguồn đối chiếu.
- DEV09-P3 trong gold là **nêu rõ thiếu căn cứ trong kho QĐ 580**. Rubric đổi thành thêm điều kiện khuyên liên hệ P.QLĐT/CVHT. Việc hướng dẫn liên hệ có thể chấm bổ sung, không được thay mandatory point gốc. DEV06 vẫn giữ đúng 5 ý; tổng 36 hàng mỗi mode là đúng về đếm.
- Nhiều nguồn ghi chỉ `c074`, `Toàn văn QĐ580` hoặc mô tả chung, chưa có tọa độ page/span đối chiếu cụ thể; phải lấy từ đúng context được gửi khi chấm faithfulness. Phân biệt nguồn trong gold, nguồn retrieved và nguồn được cite.
- Việc chấm **SAI** cho câu “D+ trở xuống là dưới 5.0” của Hybrid DEV07 là đúng. Hai mode vẫn thiếu nhánh thi phụ và thiếu điều kiện khi kết luận học lại. Không dùng source-ID membership để chứng nhận mọi claim đúng.

Vì vậy các tổng **25/36** và **28/36** hiện mới được xác nhận là tổng số nhãn trong rubric, chưa được nghiệm thu là điểm chất lượng đã chấm đúng toàn bộ. Không sửa raw outputs hoặc gold để khớp rubric.

### [P2] Báo cáo tái lập còn sai nhóm ca, danh sách tests và cấu hình

Vị trí: `BAO_CAO_CHOT_HYBRID_TASK05_R02.md:13–17,47,61,81–85`; `RUBRIC_CHAM_DIEM_DEV10_TASK05.md:8`.

- Mẫu số retrieval 9 ca là **DEV01–DEV09**, loại DEV10 theo category; báo cáo R02 lại ghi DEV01–DEV08 và DEV10. DEV09 có gold evidence để đo retrieval, còn năng lực multi-turn chưa được đánh giá; hai điều này không mâu thuẫn.
- Bảng module tests R02 ghi `test_chunking.py`, `test_ingestion.py`, `test_retrieval.py`, `test_rag_engine.py` nhưng các file này không có. Các module thật có số test methods: `test_api_and_rag.py` **27**, `test_chunking_and_sources.py` **5**, `test_hybrid_bm25_rrf.py` **17**, `test_lifecycle_and_regression.py` **21**. Tổng 70 là đúng về cấu trúc, không thay thế log chạy.
- Phiên bản môi trường đọc từ distribution metadata hiện tại: Python **3.14.6**, SentenceTransformers **6.2.0**, Chroma **1.5.9**, FastAPI **0.162.0**, Uvicorn **0.54.0**. Khác các số 5.1.2/1.5.0/0.128.0/0.40.0 trong báo cáo. `requirements.txt` còn pin Uvicorn 0.42.0. Cần chỉ rõ môi trường của lần đo lịch sử và môi trường hiện tại; không gán phiên bản đoán vào lượt chạy cũ, không tự nâng/hạ thư viện chỉ để khớp báo cáo.
- Không tìm thấy seed được gửi trong `GenerateContentConfig` hoặc artifact, nên bỏ khẳng định “seed cố định” nếu không có minh chứng.
- Raw A/B ghi `git_commit=b68811f...`, `git_dirty=true`. Giữ và nêu rõ giới hạn tái lập, không nói outputs được chạy ở commit R02 sạch. Không suy nguyên nhân độ trễ thành mạng/warm-up từ timings tổng. R04 gọi retrieval trước engine nên việc nạp weights nằm ngoài engine timing; phân biệt luồng runner R04 với lifespan FastAPI.

## 4. Độ đo đã tính lại

Tính lại từ thứ hạng lưu trong `RETRIEVAL_AB_COMPARISON_TASK05.json`, chunks/source spans và gold nguyên bản; không chạy lại embedding hoặc LLM.

| Chỉ số (9 ca DEV01–DEV09) | Dense | Hybrid |
| --- | --- | --- |
| Hit@5: ít nhất một evidence có coverage >=90% | 7/9 (77.78%) | 9/9 (100%) |
| Mean evidence coverage@5 | 63.6761% | 80.3428% |
| Full-case coverage@5: mọi evidence >=90% | 5/9 (55.56%) | 6/9 (66.67%) |
| Full-case coverage@10 | 6/9 (66.67%) | 7/9 (77.78%) |
| MRR@10 | 0.680556 | 0.657407 |

Các số retrieval chính khớp artifacts. Đây là tập **phát triển 10 ca**, không phải độ chính xác tổng quát hay bộ test độc lập cuối kỳ. A/B live lịch sử chạy tuần tự; không kết luận thời gian/độ ổn định tốt hơn từ mẫu nhỏ và outlier.

## 5. Quyết định tiếp theo

Giao **DNC-RAG-TASK-05-R03** tại `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R03_DOI_SOAT_VECTOR_VA_RUBRIC.md`. Chỉ hoàn thiện vector integrity, sửa rubric/provenance và bổ sung minh chứng tests đúng môi trường. Không làm lại hybrid, không yêu cầu LLM đạt 100%, không tự chạy lại 20 Gemini requests, chưa thêm reranker/UI/admin/multi-turn. Sau R03 đạt mới xét Task06 reranker nhẹ.
