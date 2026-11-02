# BÁO CÁO KỸ THUẬT: CHỐT BẰNG CHỨNG HỌC VỤ TRỰC TIẾP TỪ TRACE VÀ KHÔI PHỤC PROVENANCE
## NHIỆM VỤ DNC-RAG-TASK-05 (LƯỢT R05)

- **Dự án:** `dnc-academic-advisor-rag` (Hệ thống Trợ lý học vụ hỗ trợ sinh viên dựa trên Quy chế Đào tạo ĐHNCT).
- **Văn bản pháp quy cơ sở:** Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024 của Hiệu trưởng Trường Đại học Nam Cần Thơ.
- **Thời điểm thực hiện:** Ngày 02 tháng 11 năm 2026 (Giờ Việt Nam).
- **Đơn vị thực hiện:** Antigravity AI Agent (Pair Programming).
- **Đối tác rà soát độc lập:** Codex.
- **Tài liệu nhiệm vụ:** `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R05_CHOT_EVIDENCE_TU_TRACE.md`.
- **Tài liệu rà soát R04 của Codex:** `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R04.md` và `DOI_SOAT_EVIDENCE_TASK05_R04.json`.
- **Sidecar bằng chứng chuẩn hóa:** `05_Mã Nguồn Chương Trình/evaluation/results/EVIDENCE_DEV10_TASK05_R05.jsonl` (72 hàng máy đọc được).
- **Rubric R05 chi tiết:** `05_Mã Nguồn Chương Trình/evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R05.md`.

---

## 1. TỔNG QUAN VÀ MỤC TIÊU LƯỢT R05

Trong đợt rà soát R04, Codex đã kiểm tra độc lập và ghi nhận:
1. **Phần kiểm thử đã hoàn tất:**
   - 12/12 regression test cases của `TestRetrieverReadinessVerification` PASS (0.508s).
   - 10/10 integrity unit tests PASS (0.424s).
   - 14/14 focused BM25/RRF unit tests PASS (0.202s).
   - Đã gỡ bỏ hoàn toàn việc ô nhiễm `sys.modules` trong `test_vector_integrity.py`.
   - Giữ nguyên production code `backend/retrieval.py` và 104 chunks corpus QĐ 580.
2. **Các tồn tại về rubric và provenance cần chốt ở R05:**
   - **Source ID Mismatches:** Có 14 cặp source ID bị ghi nhầm do đặt source ID cố định thay vì lấy từ context của chính record đó (ví dụ c062 là SRC-5 ở Dense DEV01 và SRC-3 ở Hybrid DEV01).
   - **Range Failures:** Có 24 khoảng offset vượt khỏi envelope của chunk được dẫn do gõ thủ công khoảng rộng thay vì dùng đúng tọa độ source span thực tế.
   - **Lịch sử Git SHA:** Dòng SHA Task05-R02 trong `BAO_CAO_ANTIGRAVITY.md` ghi nhầm hash dài không tồn tại; SHA chuẩn xác của `9b008ec` là `9b008ecb252482c4e8ae064d3148cb5dedf0f47e`.

Lượt R05 giải quyết triệt để toàn bộ các tồn tại trên bằng phương pháp **sinh bằng chứng tự động (Data-driven Evidence Generation)** từ trace bất biến của 20 raw outputs và 104 chunks corpus.

---

## 2. KẾT QUẢ KHẮC PHỤC CHI TIẾT

### 2.1. Thiết lập Sidecar Bằng chứng Chuẩn hóa (`EVIDENCE_DEV10_TASK05_R05.jsonl`)

Đã xây dựng tập tin sidecar máy đọc được gồm 72 hàng tương ứng với 36 ý bắt buộc cho cả hai chế độ Dense và Hybrid. Mỗi hàng chứa:
- `mode`: Chế độ truy xuất (`dense` hoặc `hybrid`).
- `case_id` và `point_id`: Mã câu hỏi và mã ý bắt buộc (`DEV_01` -> `DEV_10`, `DEV01-P1` -> `DEV10-P3`).
- `gold_point`: Nguyên văn tiêu chuẩn vàng.
- `grade`: Kết quả đánh giá (`ĐẠT`, `MỘT PHẦN`, `THIẾU`, `SAI`).
- `answer_excerpt`: Trích đoạn câu trả lời thực tế từ raw record.
- `sources`: Danh sách căn cứ trích dẫn thực tế được lấy từ `retrieved_contexts` của chính record đó:
  - `source_id`: Mã trích dẫn thực tế (`SRC-1` .. `SRC-5`).
  - `chunk_id`: Full chunk ID trong corpus.
  - `pdf_page`: Trang PDF chứa quy định.
  - `start`, `end`: Tọa độ chính xác của source span.
  - `quote`: Nguyên văn trích đoạn văn bản quy chế khớp 100% với `QD580_PAGES[pdf_page][start:end]`.
- `na_reason`: Diễn giải minh bạch đối với các trường hợp không có trích dẫn riêng (Retrieval miss, Out-of-scope, hoặc Lỗ hổng văn bản).

### 2.2. Khắc phục 100% Lỗi Ánh xạ Source ID và Envelope Offsets

- **Source ID Mismatches:** Đã điều chỉnh toàn bộ 14 trường hợp ghi nhận sai trong R04:
  - DEV01 (Dense): c062 được ánh xạ đúng vào `[SRC-5]`.
  - DEV01 (Hybrid): c062 được ánh xạ đúng vào `[SRC-3]`.
  - DEV06 (Hybrid): c084 được ánh xạ đúng vào `[SRC-3]`.
  - DEV07 (Dense): c038 được ánh xạ đúng vào `[SRC-1]`.
- **Envelope Offsets:** Toàn bộ các khoảng offset trong rubric và sidecar đều nằm chính xác trong envelope của chunk được dẫn. Ví dụ:
  - c062 (Bảng quy đổi điểm, trang 15): Offset chuẩn là `[436, 858)` (trước đây ghi nhầm `[462, 1149)`).
  - c014 (Cơ cấu năm học, trang 3): Offset chuẩn là `[1350, 1661)` cho Khoản 1 Điểm a (trước đây ghi nhầm `[1143, 1421)`).
  - c038 (Quy định học lại, trang 9): Offset chuẩn là `[1307, 1682)` cho Khoản 3 (trước đây ghi nhầm `[1148, 1485)`).

### 2.3. Kết quả Kiểm tra Tự động Độc lập (Independent Audit Summary)

Đã chạy công cụ kiểm tra tự động theo đúng tiêu chuẩn của Codex trên tập tin `RUBRIC_CHAM_DIEM_DEV10_TASK05_R05.md`:
```json
{
  "rows": 72,
  "claimed_ranges": 58,
  "ranges_outside_cited_chunk_envelope": 0,
  "rows_with_range_failures": 0,
  "source_id_mismatches": 0,
  "invalid_full_ids": 0
}
```
**Kết quả: 0 source ID mismatches, 0 range failures, 0 invalid chunk IDs trên toàn bộ 72 hàng (100% PASS).**

### 2.4. Đính chính Lịch sử Provenance

- Đã đính chính dòng 631 trong `BAO_CAO_ANTIGRAVITY.md`: SHA triển khai Task05-R02 là `9b008ecb252482c4e8ae064d3148cb5dedf0f47e` (loại bỏ chuỗi hash không tồn tại `9b008ecb25d19e917d057778b665fa1a4e21a201`).
- Bổ sung đầy đủ các mục báo cáo `DNC-RAG-TASK-05-R03`, `DNC-RAG-TASK-05-R04` và `DNC-RAG-TASK-05-R05`.

---

## 3. TỔNG KẾT VÀ BÀN GIAO

| Hạng mục kiểm tra | Trạng thái R04 | Trạng thái R05 | Minh chứng kỹ thuật |
| :--- | :---: | :---: | :--- |
| **Source ID Mapping** | 14 mismatches | **0 mismatch (100% khớp)** | Ánh xạ trực tiếp từ `retrieved_contexts` của từng record. |
| **Offset Boundaries** | 24 range failures | **0 failure (100% trong envelope)** | Dùng chính xác tọa độ source span và quote text từ `QD580_PAGES`. |
| **Full Chunk ID Integrity** | 100% hợp lệ | **100% hợp lệ (0 invalid)** | Toàn bộ chunk IDs thuộc 104 chunks corpus QĐ 580. |
| **Machine-readable Sidecar** | Chưa có | **Hoàn thành** | `EVIDENCE_DEV10_TASK05_R05.jsonl` (72 hàng đầy đủ). |
| **Rubric Đánh giá R05** | Thủ công | **Data-driven chuẩn hóa** | `RUBRIC_CHAM_DIEM_DEV10_TASK05_R05.md` dẫn chiếu sidecar. |
| **Lịch sử Provenance Git** | Hash R02 gõ nhầm | **ĐÃ ĐÍNH CHÍNH** | Khôi phục chính xác `9b008ecb252482c4e8ae064d3148cb5dedf0f47e`. |

Nhiệm vụ Task 05 (Lượt R05) đã hoàn tất trọn vẹn, sẵn sàng để Codex tiến hành rà soát nghiệm thu.
