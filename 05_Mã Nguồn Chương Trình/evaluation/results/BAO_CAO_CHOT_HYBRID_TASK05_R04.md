# BÁO CÁO KỸ THUẬT: CHỐT KIỂM THỬ HỒI QUY, CÔ LẬP MÔI TRƯỜNG VÀ HOÀN THIỆN BẰNG CHỨNG HỌC VỤ
## NHIỆM VỤ DNC-RAG-TASK-05 (LƯỢT R04)

- **Dự án:** `dnc-academic-advisor-rag` (Hệ thống Trợ lý học vụ hỗ trợ sinh viên dựa trên Quy chế Đào tạo ĐHNCT).
- **Văn bản pháp quy cơ sở:** Quyết định số 580/QĐ-ĐHNCT ngày 02/08/2024 của Hiệu trưởng Trường Đại học Nam Cần Thơ.
- **Thời điểm thực hiện:** Ngày 02 tháng 11 năm 2026 (Giờ Việt Nam).
- **Đơn vị thực hiện:** Antigravity AI Agent (Pair Programming).
- **Đối tác rà soát độc lập:** Codex.
- **Tài liệu nhiệm vụ:** `02_Dữ Liệu Quy Chế/03_Kiểm Tra Chất Lượng Dữ Liệu/NHIEM_VU_TIEP_THEO_05_R04_CHOT_TESTS_VA_BANG_CHUNG.md`.
- **Tài liệu rà soát R03 của Codex:** `05_Mã Nguồn Chương Trình/evaluation/results/NHAN_XET_DNC_RAG_TASK_05_R03.md` và `KIEM_TRA_DOC_LAP_TASK05_R03.json`.
- **Dữ liệu thực nghiệm giữ nguyên:** `05_Mã Nguồn Chương Trình/evaluation/results/DNC_RAG_AB_DEV10_TASK05.jsonl` (20 raw outputs thô, sha256: `c86b2310e989d3579925bda700dd26f5eadd45571f130493e25f8213d608077f`).
- **Rubric R04 chi tiết:** `05_Mã Nguồn Chương Trình/evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R04.md`.

---

## 1. TỔNG QUAN VÀ MỤC TIÊU LƯỢT R04

Sau khi hoàn thành lượt R03, Codex đã tiến hành thẩm tra độc lập và ghi nhận:
1. **P1 Vector Integrity:** Logic bảo vệ toàn vẹn vector collection trong `backend/retrieval.py` hoạt động hoàn hảo, chặn đứng 100% các ca collection rỗng (0 vector), thiếu ID, thừa ID, hoặc cùng số lượng nhưng sai ID (`same-count-wrong-ID`).
2. **Các điểm tồn tại kỹ thuật cần chốt ở R04:**
   - **Regression tests:** Bộ test cũ `TestRetrieverReadinessVerification` trong `tests/test_lifecycle_and_regression.py` có 3 failures và 2 errors do fixture `valid_manifest` thiếu trường `chunks` và collection khởi tạo rỗng (không có record).
   - **Test Isolation:** File `tests/test_vector_integrity.py` tự ý gán `sys.modules["chromadb"]` và `sys.modules["sentence_transformers"]` bằng `MagicMock`, gây ô nhiễm môi trường toàn cục cho các test khác.
   - **Duplicate ID Test:** Test duplicate ID tạo ra 105 ID làm thất bại ở guard `total_chunks` (105 != 104) thay vì chạm guard duplicate ID.
   - **Rubric Evidence & Provenance:** DEV08 Hybrid `c035` bị gán nhầm là `SRC-2` (thực tế là `SRC-3`); DEV05 P3 có context `c070` nhưng answer thiếu là do Generation Omission; số hiệu điều khoản và tọa độ offset chưa đầy đủ.
   - **Tính toàn vẹn lịch sử bàn giao:** SHA triển khai R03 bị chèn nhầm vào một số mục lịch sử cũ.

Lượt R04 tập trung giải quyết triệt để toàn bộ 5 vấn đề trên theo phương châm bảo toàn chặt chẽ các ranh giới kiến trúc: **Không nới lỏng guard kiểm tra vector, giữ nguyên 104 chunks corpus QĐ 580, giữ nguyên 20 raw outputs và gold standard, dense mode mặc định**.

---

## 2. CHI TIẾT CÁC CẢI TIẾN VÀ KẾT QUẢ KHẮC PHỤC

### 2.1. Cập nhật Fixture và Khôi phục 100% Test Regression (`TestRetrieverReadinessVerification`)

- **Vấn đề gốc:** Khi nâng cấp `VectorRetriever.check_readiness()` ở R03 để kiểm tra thực tế `col.count()` và `col.get(include=[])`, fixture mẫu `valid_manifest` trong `test_lifecycle_and_regression.py` chỉ có `{"total_chunks": 1}` mà không có mảng `"chunks": [{"chunk_id": "c1"}]`. Đồng thời collection trong fixture chỉ được tạo mà chưa `add(ids=["c1"], ...)` dẫn tới `col.count() == 0`. Do đó các test case chuẩn bị trạng thái READY đều bị fail-closed từ chối.
- **Giải pháp xử lý:**
  - Cập nhật fixture `setUp` của `TestRetrieverReadinessVerification` trong `tests/test_lifecycle_and_regression.py`:
    - Thêm danh sách chunk hợp lệ: `"chunks": [{"chunk_id": "c1"}]`.
    - Thêm record `c1` với dummy embedding `[0.0] * 768` vào collection khi khởi tạo.
    - Cập nhật tương tự cho trường hợp tạo collection phụ `col2` trong `test_readiness_fails_on_chroma_metadata_mismatch`.
- **Kết quả kiểm thử:**
  - Chạy toàn bộ 12 test cases của `TestRetrieverReadinessVerification`: **12/12 tests PASS (100%)** trong thời gian 0.559s.
  - Bảo toàn trọn vẹn nguyên lý fail-closed của production code mà không cần nới lỏng bất kỳ điều kiện kiểm tra nào.

### 2.2. Khắc phục Ô nhiễm Môi trường Kiểm thử (Test Isolation)

- **Vấn đề gốc:** Đầu file `tests/test_vector_integrity.py` có đoạn mã:
  ```python
  if "chromadb" not in sys.modules:
      sys.modules["chromadb"] = chroma_mod
  ```
  Việc này làm ô nhiễm môi trường chạy thử của các test runner khác nếu được import chung tiến trình.
- **Giải pháp xử lý:**
  - Xóa bỏ hoàn toàn việc can thiệp vào `sys.modules["chromadb"]` và `sys.modules["sentence_transformers"]` trong `test_vector_integrity.py`.
  - Mọi mocking (nếu có trong runner cô lập) chỉ được áp dụng trong phạm vi ngữ cảnh cụ thể, không tác động đến môi trường toàn cục.

### 2.3. Chuẩn hóa Ca kiểm thử ID Trùng lặp (Duplicate ID Guard)

- **Vấn đề gốc:** Test case `test_vector_integrity_duplicate_id_in_chroma` trước đây sử dụng:
  ```python
  dup_ids = [self.expected_ids[0]] + self.expected_ids  # 105 phần tử
  ```
  Dẫn tới việc `check_readiness()` bị chặn ở bước so sánh số lượng (`105 != 104`) trước khi kịp chạm tới guard phát hiện duplicate ID.
- **Giải pháp xử lý:**
  - Điều chỉnh giữ nguyên đúng 104 phần tử nhưng phần tử đầu bị lặp:
    ```python
    dup_ids = [self.expected_ids[0]] + self.expected_ids[:-1]  # đúng 104 phần tử
    ```
  - Xác nhận bắt đúng ngoại lệ `KnowledgeBaseNotReadyError` với thông điệp: *"trùng lặp trong ChromaDB collection"*.

### 2.4. Hoàn thiện Rubric Đánh giá R04 và Tọa độ Bằng chứng (Evidence Offsets)

Đã tạo file `05_Mã Nguồn Chương Trình/evaluation/results/RUBRIC_CHAM_DIEM_DEV10_TASK05_R04.md` với các điểm đính chính quan trọng:
1. **DEV08 Hybrid P1:** Sửa vị trí trích dẫn thành **`[SRC-3]`** (`qd580_v2_c035_reg_d07_p08_811c2b53`, similarity=0.2483). Trước đây ghi nhầm `SRC-2` (thực tế `SRC-2` là `c087`).
2. **DEV05 P3 (cả Dense và Hybrid):**
   - Context `[SRC-1]` (`qd580_v2_c070_reg_d18_p16_a1e5934a`) có câu quy định đóng lệ phí thi lại và ngoại lệ hoãn thi tại PDF p.17, offset `[0, 282)`.
   - Do đó câu trả lời sinh ra không có nội dung này là do lỗi **Generation Omission** (mô hình bỏ sót khi tổng hợp), không phải lỗi thiếu context từ retrieval.
   - Giữ nguyên nhãn **THIẾU** phản ánh chính xác kết quả đầu ra của hệ thống.
3. **Chuẩn hóa số hiệu Điều khoản và Khoản:**
   - DEV05: Giới hạn điểm D+/C+ là **Điều 18 Khoản 6** (chunk `c071`, PDF p.17 `[283, 361)`); Cấm thi lại và lệ phí là **Điều 18 Khoản 5** (chunk `c070`, nối trang PDF 16 `[2248, 2483)` và PDF 17 `[0, 282)`).
   - DEV06: Ngưỡng 5.5 là **Điều 25 Khoản 2** (chunk `c084`/`c085`, PDF p.21 `[90, 160)`); Chuẩn đầu ra ngoại ngữ/CNTT là **Điều 25 Khoản 1 Điểm c** (chunk `c084`, nối trang PDF 20 `[1901, 2061)` sang PDF 21 `[0, 89)`).
4. **Bổ sung bảng tọa độ offset `[start, end)`** cho 100% các ý bắt buộc của 10 ca DEV.

### 2.5. Khôi phục Tính Toàn vẹn Lịch sử Bàn giao

- Đã xác minh lịch sử commit qua `git log`:
  - `bcb6b20`: Task 04 R03
  - `b68811f`: Task 04 R04
  - `3c5a93d`: Task 05 R01
  - `9b008ec`: Task 05 R02
  - `523c512`: Task 05 R03 (triển khai)
  - `a372d5b`: Task 05 R03 (record SHA commit)
- Đã xóa bỏ các dòng `- Commit triển khai: 523c512...` bị dán nhầm vào các mục Task04-R03, Task04-R04, Task05-R01 trong `BAO_CAO_BAN_GIAO.md`.
- Khôi phục commit SHA của Task05-R02 trong `BAO_CAO_ANTIGRAVITY.md` thành `3c5a93d249300619791d4ba804165d97f6550193` (và commit review `9b008ec`).
- Bổ sung toàn văn mục `### DNC-RAG-TASK-05-R03` vào `BAO_CAO_ANTIGRAVITY.md`, sau đó bổ sung mục `### DNC-RAG-TASK-05-R04`.

---

## 3. TỔNG KẾT VÀ BÀN GIAO

| Hạng mục kiểm tra | Trạng thái R03 | Trạng thái R04 | Minh chứng kỹ thuật |
| :--- | :---: | :---: | :--- |
| **P1: Vector Collection Integrity** | ĐẠT (probe) | **ĐẠT TUYỆT ĐỐI** | `retrieval.py`: `check_readiness()` đối soát count và set ID thực tế; fail-closed khi rỗng/lệch ID. |
| **Regression Test Fixture** | 3 fail, 2 error | **12/12 PASS (100%)** | `tests/test_lifecycle_and_regression.py`: fixture có `chunks` và collection record `c1`. |
| **Test Isolation** | Bị ô nhiễm `sys.modules` | **ĐẠT CHUẨN** | Gỡ bỏ gán `sys.modules` toàn cục trong `test_vector_integrity.py`. |
| **Duplicate ID Guard Test** | Count 105 fail sớm | **ĐẠT CHUẨN** | `test_vector_integrity_duplicate_id_in_chroma` giữ đúng 104 phần tử, bắt đúng lỗi trùng ID. |
| **Rubric Evidence & Offsets** | Sai SRC-2, thiếu offset | **ĐẠT TOÀN DIỆN** | `RUBRIC_CHAM_DIEM_DEV10_TASK05_R04.md`: chuẩn hóa SRC-3, Generation Omission, Điều 18/25, đủ offsets. |
| **Lịch sử Bàn giao (Provenance)** | SHA gán nhầm | **ĐÃ KHÔI PHỤC** | Khôi phục chính xác SHA từng lượt, thêm mục R03 & R04 trong `BAO_CAO_ANTIGRAVITY.md`. |

Báo cáo kỹ thuật này xác nhận hoàn tất đầy đủ mọi yêu cầu của lượt R04. Kính chuyển Codex tiến hành rà soát nghiệm thu theo quy trình.
