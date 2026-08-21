# AI Support Log

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | Phase 1 — evidence map | Đọc corpus/slide, trích section và lập 20 scenario candidates | Human reject C01/C02/C09/C10/C12, keep 15 scenario ngày 2026-08-21 |
| 2 | Phase 1 — paraphrase | Viết 25 natural-language inputs từ 15 combinations đã chọn và chuẩn hóa JSONL | Human yêu cầu triển khai tiếp; file được parse, 25/25 ID unique; nhóm vẫn cần đọc chéo |
| 3 | Phase 3–4 — evaluator draft | Brainstorm hai code checks, rubric/routing draft và hai single-criterion judge prompts | 48 offline tests pass; judge chưa được tin cho tới khi calibrate với gold labels |
| 4 | Report draft | Điền phần có evidence thật và đánh dấu checkpoint thiếu | Không điền agreement, threshold, calibration result hoặc verdict khi chưa có số liệu |

- Phần AI gợi ý đã bác bỏ: `C01, C02, C09, C10, C12`. **Nhóm bổ sung lý do
  reject cụ thể trước khi nộp.**
- Phần human-owned: chọn dimensions/combinations cuối, labels, disagreement
  resolution, threshold và verdict.
