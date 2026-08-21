# Human checkpoints còn thiếu

Không điền giả các mục dưới đây. Đây là phần hai thành viên phải tự thực hiện:

| Họ và tên | Mã sinh viên | File nhãn độc lập |
|---|---|---|
| Trần Kiên | `2A202601598` | `labels-tran-kien.csv` |
| Nguyễn Phú Quang | `2A202602017` | `labels-nguyen-phu-quang.csv` |

## A. Trước live run

- [x] Có `OPENROUTER_API_KEY` tương thích với model trong `.env`.
- [x] Tutor `openrouter/deepseek/deepseek-v4-flash`; các judge model/attempt được
  ghi đúng theo file raw trong `calibration-attempts.md`.
- [x] Có `LANGSMITH_API_KEY`; project `ai-evaluation`.
- [x] Đã ghi trace project link vào `deliverables/evidence/braintrust-link.md`.

Live run đã log 25 traces lên LangSmith và URL project đã được lưu trong
`deliverables/evidence/braintrust-link.md`. Không ghi giá trị API key vào evidence
hoặc commit.

## B. Human baseline

```powershell
python eval/run_eval.py
Copy-Item results.jsonl deliverables/evidence/results-v1.jsonl
python eval/report.py
```

- [x] Trần Kiên đã chấm độc lập 25/25 row; file `labels-tran-kien.csv` hợp lệ.
- [x] Nguyễn Phú Quang đã chấm độc lập cùng 25 row.
- [x] Đã nhận và chuẩn hóa tên file `labels-nguyen-phu-quang.csv`.
- [x] Đã chạy `python eval/agreement.py labels-tran-kien.csv labels-nguyen-phu-quang.csv`.
- [x] Agreement trước đồng thuận: 23/25 = 92%; disagreement: `sc-c04-a`, `sc-c13-a`.
- [x] Nhóm đã tự chốt `labels.csv`: `sc-c04-a` fail, `sc-c13-a` uncertain, các row
  còn lại pass; AI chỉ ghi lại quyết định.
- [x] Dùng `labels.csv` là human baseline theo đúng workflow của lab; không tự thêm
  criterion-specific labels như một yêu cầu bắt buộc.

## C. Calibration

```powershell
python eval/code_checks.py
python eval/judge.py --prompt eval/judge_prompts/groundedness-v1.md --output verdicts-groundedness-v1.jsonl --labels labels.csv
python eval/judge.py --prompt eval/judge_prompts/followup-quality-v1.md --output verdicts-followup-v1.jsonl --labels labels.csv
```

- [x] Đã chạy code checks trên `results-v1.jsonl`: schema 24/25; citation ID 24/24;
  quote-verbatim 7/24; scope/source contract 24/24; follow-up contract 24/24.
- [x] Nhóm chốt 17 quote mismatches là lỗi contract của tutor cho release gate;
  human labels vòng độc lập vẫn được giữ nguyên, không sửa hồi tố theo code check.
- [x] Đã lưu matrix/pattern các attempt hợp lệ và loại infra error khỏi kết luận.
- [x] Đã so groundedness run đủ 25 với human ceiling 92%.
- [x] Vì không có hai vòng sạch và bad-case sample quá nhỏ, route cả hai semantic
  judge về `LLM assist`; không dùng làm automated gate hoặc ground truth.

## D. Threshold và verdict

- [x] Không hồi tố threshold cho v1; đã khóa threshold cho candidate v2 trở đi.
- [x] Timestamp: `2026-08-21 18:13:18 +07:00`; xác nhận trong task nhóm.
- [x] Đã đọc theo slice và audit `sc-c04-a`, `sc-c13-a`, `sc-c03-b`.
- [x] Verdict: **Hold**.
- [x] Đòn bẩy tiếp theo: sửa JSON escaping và exact quote extraction, chạy lại cùng
  Dataset v1; exit criteria là gate ở mục 6 của `REPORT.md`.
