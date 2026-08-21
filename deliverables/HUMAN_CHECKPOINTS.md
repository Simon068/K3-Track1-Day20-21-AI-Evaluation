# Human checkpoints còn thiếu

Không điền giả các mục dưới đây. Đây là phần hai thành viên phải tự thực hiện:

| Họ và tên | Mã sinh viên | File nhãn độc lập |
|---|---|---|
| Trần Kiên | `2A202601598` | `labels-tran-kien.csv` |
| Nguyễn Phú Quang | `2A202602017` | `labels-nguyen-phu-quang.csv` |

## A. Trước live run

- [ ] Điền ít nhất một provider key tương thích với `EVAL_MODEL` trong `.env`.
- [ ] Chọn tutor model và judge model khác họ; ghi model/version/ngày.
- [ ] Điền `BRAINTRUST_API_KEY` hoặc `LANGSMITH_API_KEY` thật.
- [ ] Ghi trace project link vào `deliverables/evidence/braintrust-link.md`.

Hiện trạng được kiểm tra ngày 2026-08-21: `.env` có OpenRouter key nhưng model mặc
định vẫn cần DeepSeek/OpenAI key; chưa có tracing key. Không chạy live trước khi sửa.

## B. Human baseline

```powershell
python eval/run_eval.py
Copy-Item results.jsonl deliverables/evidence/results-v1.jsonl
python eval/report.py
```

- [ ] Hai người chấm độc lập cùng 15–20 row, không xem nhãn nhau.
- [ ] Lưu `labels-tran-kien.csv` và `labels-nguyen-phu-quang.csv`.
- [ ] Chạy `python eval/agreement.py labels-tran-kien.csv labels-nguyen-phu-quang.csv`.
- [ ] Ghi agreement trước đồng thuận và từng disagreement case.
- [ ] Đồng thuận `labels.csv`; không để AI gắn nhãn.
- [ ] Nếu calibrate judge theo từng tiêu chí, tạo gold files tương ứng
  `labels-groundedness.csv` và `labels-followup.csv` từ quyết định human.

## C. Calibration

```powershell
python eval/code_checks.py
python eval/judge.py --prompt eval/judge_prompts/groundedness-v1.md --output verdicts-groundedness-v1.jsonl --labels labels-groundedness.csv
python eval/judge.py --prompt eval/judge_prompts/followup-quality-v1.md --output verdicts-followup-v1.jsonl --labels labels-followup.csv
```

- [ ] Lưu confusion matrix, TPR/TNR và disagreement pattern vòng 1.
- [ ] Mỗi lần chỉ sửa một yếu tố prompt; lưu prompt/verdicts trước khi chạy lại.
- [ ] Chạy tối thiểu hai vòng mỗi judge.
- [ ] So kết quả judge với human–human agreement ceiling.

## D. Threshold và verdict

- [ ] Nhóm viết threshold theo từng critical criterion **trước** khi xem candidate.
- [ ] Ghi timestamp và người đồng thuận threshold.
- [ ] Đọc kết quả theo slice; đọc tay ba trace fail quan trọng nhất.
- [ ] Nhóm tự quyết Ship / Ship with conditions / Hold.
- [ ] Hoàn thiện monitoring plan hoặc đòn bẩy tiếp theo bằng evidence thật.
