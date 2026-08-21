# evidence/ — data thô của từng bước eval loop

Thư mục này chứa **data thô** minh chứng cho mọi quyết định trong các file
`deliverables/REPORT.md`. File làm việc sinh ra ở **root repo**
(`dataset.jsonl`, `results.jsonl`, `verdicts.jsonl`, `labels.csv`) — chốt một vòng
là copy vào đây ngay, đặt tên theo version, KHÔNG ghi đè vòng cũ.

Cần có đủ:

| File | Lấy từ đâu | Là gì |
|---|---|---|
| `dataset-v1.jsonl` | `dataset.jsonl` (root) | Dataset nhóm chốt — đầu vào mọi lần chạy |
| `results-v1.jsonl` (v2, v3...) | `results.jsonl` (root) | Output tutor thật: input, output JSON, `tool_calls`, tokens, cost từng câu |
| `labels.csv` | Export từ `report.html` | Nhãn người của các thành viên (vòng chấm độc lập) |
| `judge-prompt-v1.md` (v2...) | `eval/judge_prompt.md` | Prompt judge TỪNG VÒNG — copy trước mỗi lần sửa |
| `verdicts-v1.jsonl` (v2...) | `verdicts.jsonl` (root) | Output judge từng vòng calibration |
| `braintrust-link.md` | tự tạo | Link project Braintrust/LangSmith — trace mọi run |

## Mapping của gói evidence hiện tại

Gói này dùng đúng tên version cố định của bài nộp, nhưng hai version là hai
evaluator theo hai tiêu chí khác nhau:

| Version | Tiêu chí | Judge model | File prompt | File verdict |
|---|---|---|---|---|
| v1 | Groundedness | `openrouter/openai/gpt-5-mini` | `judge-prompt-v1.md` | `verdicts-v1.jsonl` |
| v2 | Follow-up quality | `groq/openai/gpt-oss-120b` | `judge-prompt-v2.md` | `verdicts-v2.jsonl` |

`v2` không phải vòng sửa prompt của groundedness. Vì mỗi tiêu chí mới chỉ có một
run sạch, nhóm không tuyên bố đã hoàn thành hai vòng calibration cho từng judge;
hai evaluator semantic được route về **LLM assist**. Chi tiết các run hợp lệ và
attempt lỗi hạ tầng nằm trong `calibration-attempts.md`.

Các file bổ sung `labels-<tên>.csv`, `human-agreement-v1.md`,
`code-checks-v1.md` và `report-v1.html` giữ lại để chứng minh vòng chấm độc lập,
agreement, code lane và việc đọc output. Chúng không thay thế các file bắt buộc
trong bảng trên.

Số liệu trong mục 5 (Calibration Report) của `deliverables/REPORT.md` phải đối chiếu được với các
file ở đây (confusion matrix, % agreement in ra từ `eval/judge.py`).

Nhớ: chạy xong một vòng là copy ngay — cuối buổi mới gom là mất dấu các vòng trước.
