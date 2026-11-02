# Codex nghiệm thu DNC-RAG-TASK-05-R05

Ngày kiểm tra: **02/11/2026**, giờ Việt Nam. Project: `dnc-academic-advisor-rag`.

**Kết luận: ĐẠT CÓ ĐIỀU KIỆN — chốt baseline Task05 bằng bản evidence đã hiệu chỉnh của Codex.** Mapping/offsets/quotes của R05 đã khớp về cấu trúc; reviewer đã bổ sung phần chọn nguồn theo nội dung ngay trong lượt kiểm tra này. Không giao thêm vòng sửa tài liệu. Có thể chuyển sang Task06 reranker nhẹ, với các giới hạn baseline ở mục4.

## 1. Phiên bản và phạm vi

- HEAD/remote main kiểm tra: **`23f240f6a5d5d52ab8b67fa82e741d626f6b0bd9`**; triển khai R05: `c90a5ce2fc22fac0f4cd51ed6641cc3355466c19`.
- Remote: `https://github.com/hien10122005/dnc-academic-advisor-rag.git`; working tree sạch khi bắt đầu.
- Không có thay đổi production backend, tests, corpus/chunks/manifest/gold giữa R04 và R05. Raw20 outputs vẫn giữ hash lịch sử. Review chỉ thêm script kiểm evidence, bản hiệu chỉnh và tài liệu nghiệm thu; không sửa lời tự báo của Antigravity hoặc sinh lại output.
- Theo phạm vi R05 chỉ thay tài liệu, không lặp tests ML hoặc gọi Gemini. Kế thừa kết quả R04: **12 readiness +10 integrity +14 focused unit tests qua trong môi trường cô lập**. Chưa có kết quả full-suite80 với ML/Chroma thật; không biến36 unit tests thành xác nhận end-to-end.

## 2. R05 đã khắc phục mapping, offsets và provenance

Đã kiểm độc lập sidecar `EVIDENCE_DEV10_TASK05_R05.jsonl` trực tiếp với raw contexts, `QD580_PAGES.jsonl`, chunk source spans và gold gốc:

- **72 hàng, 72 keys duy nhất**, đủ36 ý cho mỗi mode; nguyên văn `gold_point` khớp gold theo index.
- **58 source spans**, không có lỗi source ID/chunk, page quote, bounds, span thuộc context hay nội dung quote trong chunk được gửi LLM.
- Mọi hàng không có nguồn đều có `na_reason`. Các nhãn cộng đúng Dense25 ĐẠT/1 MỘT PHẦN/10 THIẾU; Hybrid28 ĐẠT/1 MỘT PHẦN/6 THIẾU/1 SAI.
- SHA R02 đã được sửa đúng thành `9b008ecb252482c4e8ae064d3148cb5dedf0f47e`; vai trò commit R01/R02 ghi đúng và các mục báo cáo có đích liên kết.

Tuy nhiên, structural audit không đủ để khẳng định span chứng minh nội dung gold. Reviewer đọc nội dung và thấy generator `find_best_span()` có nhánh lấy span đầu tiên khi không tìm thấy keyword, hoặc chỉ lấy một trang của điều khoản nối trang. Ví dụ:

| Ý được chấm | Span R05 đã khớp ký tự nhưng chưa đủ nội dung | Hiệu chỉnh của Codex |
| --- | --- | --- |
| DEV03-P1, hai mode; DEV08-P1 Hybrid | Chỉ tiêu đề Điều7, p8 `[2274,2309)`, không có7/15 tín chỉ | Đúng dòng CT4 năm, c035 p9 **`[0,90)`** |
| DEV04-P2, hai mode | Câu mở “đáp ứng01 trong02 điều kiện”, thiếu cả hai nhánh7.0/5.5 | Thêm c044 p11 **`[619,753)`** và **`[754,884)`**, giữ câu mở điều kiện |
| DEV04-P4, hai mode | Đoạn khả năng tiếp nhận của Khoa, không có quy trình đăng ký | c045 p11 **`[961,1192)`** |
| DEV05-P2, hai mode | Chỉ p16, dừng giữa câu ở “Thực hành, học” | Ghép c070 p16 **`[2248,2483)`** và p17 **`[0,282)`** để đủ các loại học phần |
| DEV06-P4, hai mode | Chỉ phần chuẩn ngoại ngữ/CNTT p21, thiếu GDQP/GDTC ở p20 | Ghép c084 p20 **`[1901,2061)`** và p21 **`[0,89)`** |
| DEV07-P4, hai mode | c038 khoản3 nói cải thiện môn đã đạt5.0–dưới6.5; không chứng minh bắt buộc học lại cho4.5 | Tách gold c037 khoản1/2 ra khỏi context; xác nhận c037 chưa retrieve và đánh dấu claim yêu cầu học lại vô điều kiện **chưa được context hỗ trợ** |

## 3. Bản evidence cuối đã được Codex hoàn thiện

**Dùng [EVIDENCE_DEV10_TASK05_CODEX_VERIFIED.jsonl](EVIDENCE_DEV10_TASK05_CODEX_VERIFIED.jsonl) làm bản evidence tham chiếu hiện hành**, cùng các nhãn R05; giữ sidecar/rubric R05 nguyên bản để truy lại lịch sử.

Reviewer đã hiệu chỉnh cách chọn/ghép spans hoặc bỏ nguồn trùng/không phù hợp trên **21 hàng**; con số này là số hàng thay đổi nguồn, không phải21 lỗi đáp án mới. Bản hiệu chỉnh:

- Giữ đủ72 hàng, nguyên gold và nhãn chấm cũ; bổ sung nguyên văn `raw_answer`, lý do kiểm tra và `claim_support` riêng để không nhầm điểm đủ ý với faithfulness.
- Tách `gold_sources` (căn cứ chuẩn, có thể chưa retrieve) khỏi `sources` (thực sự trong context record). Không gán source ID cho căn cứ vắng trong context.
- Có **62 source spans**; audit độc lập không có lỗi về keys, gold, source mapping, page/context quote hoặc source spans.
- DEV07-P4 vẫn giữ nhãn MỘT PHẦN về nội dung trả lời theo rubric cũ, nhưng cả hai mode được gắn `unsupported_unconditional_retake_claim`. Không dùng nhãn này để kết luận claim đúng nguồn. DEV07 Hybrid P1 vẫn là SAI do phát ngôn D+ trái bảng điểm.

Script chạy lại bằng Python chuẩn, không import ML hoặc gọi mạng:

```powershell
# Từ thư mục mã nguồn
python evaluation/review_task05_r05.py
```

Script kiểm sidecar R05, sinh bản hiệu chỉnh từ các anchors đã đọc và kiểm tra lại. Nếu anchor không tồn tại phải lỗi, không fallback về tiêu đề/đoạn đầu. Artifact audit/hashes: [KIEM_TRA_DOC_LAP_TASK05_R05.json](KIEM_TRA_DOC_LAP_TASK05_R05.json). Script và các artifacts reviewer chưa commit/push trong lượt này.

## 4. Điều kiện và giới hạn khi chuyển Task06

Task05 được chốt **trong phạm vi baseline QĐ580/104 chunks và tập phát triển10 ca**, không chứng nhận toàn bộ sản phẩm cuối hoặc độ chính xác tổng quát.

- Tài liệu đánh giá tiếp theo dùng bản evidence Codex đã hiệu chỉnh; số25/36 và28/36 là nhãn đủ ý lịch sử, **không phải accuracy/faithfulness tuyệt đối**. Tách rõ hai claim học lại chưa được hỗ trợ, một claim D+ sai, các omission và retrieval misses.
- Giữ sự thật rằng full-suite80/ML integration chưa tái lập trên môi trường hiện tại. Với thay đổi code Task06, kiểm thử thật trong môi trường ổn định và ghi phiên bản/log; không dùng mock để thay kết quả integration.
- Reranker phải được so với Dense/Hybrid trên cùng corpus và cấu hình đo có provenance; không hứa reranker sẽ chữa mọi lỗi generation, không tối ưu theo từng DEV ID. Mở rộng60–80 ca vẫn là kế hoạch đánh giá cuối kỳ.
- Chưa triển khai reranker/UI/admin/multi-turn trong lượt nghiệm thu này. Không cần thêm vòng sửa R05; các hiệu chỉnh evidence đã được reviewer thực hiện và ghi vào bàn giao/ROADMAP.
