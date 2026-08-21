# Human checkpoints còn thiếu

Không điền giả các mục dưới đây. Đây là phần hai thành viên phải tự thực hiện:

| Họ và tên | Mã sinh viên | File nhãn độc lập |
|---|---|---|
| Trần Kiên | `2A202601598` | `labels-tran-kien.csv` |
| Nguyễn Phú Quang | `2A202602017` | `labels-nguyen-phu-quang.csv` |

## A. Trước live run

- [x] Có `OPENROUTER_API_KEY` tương thích với model trong `.env`.
- [x] Tutor `openrouter/deepseek/deepseek-v4-flash`; judge dự kiến
  `openrouter/openai/gpt-5-mini` — khác họ model, ghi nhận ngày 2026-08-21.
- [x] Có `LANGSMITH_API_KEY`; project `ai-evaluation`.
- [ ] Ghi trace project link vào `deliverables/evidence/braintrust-link.md`.

Live run đã log 25 traces lên LangSmith. Không ghi giá trị API key vào evidence hoặc
commit; chỉ còn thiếu URL project/run để làm minh chứng có thể mở được.

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
- [x] Agreement trước đồng thuận: 23/25 = 92%; disagreement: `sc-c13-a`, `sc-c20-a`.
- [ ] Đồng thuận `labels.csv`; không để AI gắn nhãn.
- [ ] Nếu calibrate judge theo từng tiêu chí, tạo gold files tương ứng
  `labels-groundedness.csv` và `labels-followup.csv` từ quyết định human.

## C. Calibration

```powershell
python eval/code_checks.py
python eval/judge.py --prompt eval/judge_prompts/groundedness-v1.md --output verdicts-groundedness-v1.jsonl --labels labels-groundedness.csv
python eval/judge.py --prompt eval/judge_prompts/followup-quality-v1.md --output verdicts-followup-v1.jsonl --labels labels-followup.csv
```

- [x] Đã chạy code checks trên `results-v1.jsonl`: schema 24/25; citation ID 24/24;
  quote-verbatim 7/24; scope/source contract 24/24; follow-up contract 24/24.
- [ ] Hai thành viên xác nhận 17 quote mismatches là lỗi tutor hay false positive của
  rule; human labels không được tự động sửa theo code check.
- [ ] Lưu confusion matrix, TPR/TNR và disagreement pattern judge vòng 1.
- [ ] Mỗi lần chỉ sửa một yếu tố prompt; lưu prompt/verdicts trước khi chạy lại.
- [ ] Chạy tối thiểu hai vòng mỗi judge.
- [ ] So kết quả judge với human–human agreement ceiling.

## D. Threshold và verdict

- [ ] Nhóm viết threshold theo từng critical criterion **trước** khi xem candidate.
- [ ] Ghi timestamp và người đồng thuận threshold.
- [ ] Đọc kết quả theo slice; đọc tay ba trace fail quan trọng nhất.
- [ ] Nhóm tự quyết Ship / Ship with conditions / Hold.
- [ ] Hoàn thiện monitoring plan hoặc đòn bẩy tiếp theo bằng evidence thật.
