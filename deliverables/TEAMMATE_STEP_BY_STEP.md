# Teammate Step-by-Step — Human Labeling VLearn AI Tutor

Tài liệu này dành cho thành viên thứ hai. Mục tiêu của bạn là **chấm độc lập output
của tutor và gửi lại một file CSV**. Bạn không cần API key, không cần chạy tutor và
không được xem nhãn của thành viên còn lại trước khi export.

## 0. Branch và repository đang dùng

| Vai trò | Repository / branch |
|---|---|
| Repo gốc của lớp | `VinUni-AI20k/K3-Track1-Day20-21-AI-Evaluation` · `master` |
| Fork của nhóm | `Simon068/K3-Track1-Day20-21-AI-Evaluation` |
| Branch chứa bài đang làm | `codex/eval-capstone` |
| Branch nhãn tùy chọn | `codex/human-labels-<tên>` |

Link branch chính của nhóm:

<https://github.com/Simon068/K3-Track1-Day20-21-AI-Evaluation/tree/codex/eval-capstone>

**Không chấm từ `master`**, vì Dataset v1, live results và report review hiện nằm ở
`codex/eval-capstone`.

## 1. Cách nhanh nhất — không cần clone repo

1. Mở file trên GitHub:
   <https://github.com/Simon068/K3-Track1-Day20-21-AI-Evaluation/blob/codex/eval-capstone/deliverables/evidence/report-v1.html>
2. Bấm **Download raw**.
3. Mở file `report-v1.html` vừa tải bằng Chrome hoặc Edge.
4. Chuyển sang mục [3. Cách chấm](#3-cách-chấm).

File HTML là self-contained: đã nhúng 25 inputs, outputs, citations và raw content.
Không cần cài Python và không cần `.env`.

## 2. Cách đầy đủ — clone đúng branch về máy

### Clone lần đầu

```powershell
git clone --branch codex/eval-capstone --single-branch `
  https://github.com/Simon068/K3-Track1-Day20-21-AI-Evaluation.git

cd K3-Track1-Day20-21-AI-Evaluation
git branch --show-current
```

Expected output:

```text
codex/eval-capstone
```

Mở report trên Windows:

```powershell
Invoke-Item .\deliverables\evidence\report-v1.html
```

### Nếu đã clone fork trước đó

```powershell
git fetch origin
git switch codex/eval-capstone
git pull --ff-only origin codex/eval-capstone
```

Nếu `git switch` báo branch chưa tồn tại ở local:

```powershell
git switch --track origin/codex/eval-capstone
```

## 3. Cách chấm

Trước khi bắt đầu, hai thành viên phải chấm **cùng một tập scenario IDs**. Hỏi chủ
nhóm xác nhận tập 15–20 rows. Nếu chưa thống nhất tập con, chấm cả 25 để chắc chắn có
đủ rows chung khi đo agreement.

Với từng card, đọc theo thứ tự:

1. Input của học viên và slide context.
2. Answer của tutor.
3. Sources: `doc_id`, `section_id`, quote.
4. Ba `followup_questions`.
5. Bấm **xem raw** khi UI báo không parse được hoặc cần kiểm tra output gốc.

### Chọn nhãn tổng

- `pass`: tất cả tiêu chí bên dưới đều đạt.
- `fail`: chỉ cần một tiêu chí fail.
- `uncertain`: rubric chưa đủ rõ để quyết định sau khi đã đọc kỹ; ghi lý do cụ thể.

### Năm tiêu chí cần soi

| Tiêu chí | Pass khi | Note khi fail |
|---|---|---|
| Schema | JSON parse được, đủ `scope/answer/sources/followup_questions` | `fail: schema` |
| Groundedness | Mọi claim quan trọng được quote hỗ trợ; không mạnh hơn nguồn | `fail: groundedness` |
| Citation | Doc/section/quote khớp và quote hỗ trợ đúng claim | `fail: citation` |
| Scope | In-scope trả từ corpus; out-of-scope từ chối, không bịa | `fail: scope` |
| Follow-up | Đúng 3 câu, cụ thể, không lặp, dẫn sâu đúng chủ đề | `fail: followup` |

Ví dụ note tốt:

```text
fail: schema — raw content đọc được nhưng JSON không parse được
fail: citation — quote ở s47 không support claim threshold 90%
uncertain: groundedness — chưa rõ câu này là diễn giải hay claim mới
```

Không dùng note chung chung như `cảm giác chưa ổn`.

## 4. Export labels

1. Chấm xong, bấm **Export labels.csv** ở đầu trang.
2. Đổi tên file thành `labels-<tên>.csv`, ví dụ:

```text
labels-binh.csv
```

3. Mở nhanh file và xác nhận có ba cột:

```csv
scenario_id,label,note
sc-c03-a,pass,
sc-c04-a,fail,fail: schema
```

4. Gửi file CSV trực tiếp cho chủ nhóm qua Drive/Zalo/Slack. Đây là cách đơn giản
   nhất và không cần quyền push GitHub.

Nhãn được lưu trong browser local storage. Không xóa browser data hoặc đổi profile
trước khi export.

## 5. Tùy chọn — gửi labels bằng GitHub branch

Chỉ dùng cách này nếu `Simon068` đã mời bạn làm collaborator của fork.

Root repo ignore `labels-*.csv`, nên phải đặt file trong `deliverables/evidence/`:

```powershell
Copy-Item "$env:USERPROFILE\Downloads\labels.csv" `
  ".\deliverables\evidence\labels-<tên>.csv"

git switch -c codex/human-labels-<tên>
git add -- deliverables/evidence/labels-<tên>.csv
git commit -m "Add independent human labels from <tên>"
git push -u origin codex/human-labels-<tên>
```

Gửi lại tên branch cho chủ nhóm. Không sửa `REPORT.md`, rubric hoặc labels của người
khác trên branch này.

## 6. Những việc teammate không làm ở bước này

- Không chạy `eval/judge.py` trước khi nhóm có gold labels.
- Không xem labels của người kia trước khi export.
- Không thay dataset, tutor prompt hoặc definition of quality giữa lúc chấm.
- Không tạo/bịa output mới để thay row fail.
- Không commit `.env`, API key, hoặc file chứa secrets.

## 7. Chủ nhóm làm gì sau khi nhận hai CSV?

Đặt hai file cạnh `README.md`, ví dụ:

```text
labels-an.csv
labels-binh.csv
```

Chạy agreement:

```powershell
python eval/agreement.py labels-an.csv labels-binh.csv
```

Expected output:

- Pairwise agreement tổng.
- Số rows chung được so sánh.
- Danh sách scenario bất đồng.

Hai thành viên đọc lại từng disagreement, siết rubric và chốt `labels.csv` làm gold
labels. Không dùng AI làm người tie-break.

## 8. Definition of done của teammate

- [ ] Đang xem đúng branch `codex/eval-capstone`.
- [ ] Chấm độc lập cùng tập scenario IDs với thành viên còn lại.
- [ ] Mọi `fail/uncertain` có note nêu tiêu chí và lý do.
- [ ] Export thành `labels-<tên>.csv` đúng ba cột.
- [ ] Gửi CSV cho chủ nhóm mà chưa xem labels của người kia.
