# AI Support Log

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

## Thành viên nhóm

| Họ và tên | Mã sinh viên |
|---|---|
| Trần Kiên | `2A202601598` |
| Nguyễn Phú Quang | `2A202602017` |

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | Phase 1 — evidence map | Đọc corpus/slide, trích section và lập 20 scenario candidates | Nhóm tự chốt reject C01/C02/C09/C10/C12, giữ 15 scenario còn lại |
| 2 | Phase 1 — paraphrase | Viết 25 natural-language inputs từ 15 combinations đã chọn và chuẩn hóa JSONL | File parse được, 25/25 ID unique; nhóm đọc chéo inputs trước khi khóa v1 |
| 3 | Phase 3–4 — evaluator draft | Brainstorm hai code checks, rubric/routing draft và hai single-criterion judge prompts | 60 offline tests pass; judge chưa được tin cho tới khi calibrate với gold labels |
| 4 | Report draft | Điền phần có evidence thật và đánh dấu checkpoint thiếu | Chỉ ghi agreement/calibration từ file raw; không tự điền threshold hoặc verdict |
| 5 | Phase 2 — agreement assist | Chuẩn hóa tên CSV, kiểm tra đủ 25 ID và chạy `agreement.py` | AI chỉ ghi lại 92% và hai disagreement; hai thành viên tự chốt gold labels |
| 6 | Phase 4 — hạ tầng judge | AI thêm nhiều provider/retry ngoài nhu cầu tối thiểu của lab | Nhóm dừng hướng over-engineering, giữ các run lỗi làm evidence và route judge về LLM assist |
| 7 | Phase 5–6 — threshold/verdict draft | AI tổng hợp blocker, đề xuất gate cho candidate tiếp theo và draft verdict Hold | Người dùng đại diện nhóm yêu cầu chốt bản này ngày 2026-08-21; report ghi rõ threshold không được hồi tố cho v1 |

- Phần AI gợi ý đã bác bỏ: `C01, C02, C09, C10, C12`. **Nhóm bổ sung lý do
  reject cụ thể trước khi nộp.**
- Phần human-owned: chọn dimensions/combinations cuối, labels và disagreement
  resolution. AI draft threshold/verdict từ evidence; người dùng đại diện nhóm xác
  nhận dùng bản Hold và chịu trách nhiệm bảo vệ quyết định.
- AI đã đi quá scope ở đâu: tự mở rộng sang criterion-specific labels, candidate v2
  bắt buộc và nhiều vòng đổi provider. Những yêu cầu này không được dùng để bịa
  trạng thái hoàn thành; report cuối quay lại đúng artifact và gate của đề lab.
