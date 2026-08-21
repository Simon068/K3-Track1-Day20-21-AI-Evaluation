# REPORT — VLearn AI Tutor Evaluation

## Thành viên

| Họ và tên | Mã sinh viên |
|---|---|
| Trần Kiên | `2A202601598` |
| Nguyễn Phú Quang | `2A202602017` |

## 1. Input Grid

Nhóm khóa bốn dimensions trước khi dùng AI paraphrase: loại câu hỏi, độ phủ
corpus, độ rõ của input và bối cảnh học. Nhóm human-review 20 candidate
combinations, loại `C01, C02, C09, C10, C12`, sửa `C18, C20` và giữ 15
combinations. Quyết định và lý do nằm trong `deliverables/COVERAGE_REVIEW.md`.

| Bối cảnh \ Intent | Khái niệm/so sánh | Áp dụng | Đọc kết quả | Xin đáp án / ngoài bài |
|---|---|---|---|---|
| Đang làm lab | — | C03, C06, C19 | C16 | C11 |
| Có slide | C05, C18 | — | C04, C07, C20 | — |
| Ôn lại | C08, C15 | — | — | — |
| Không context | — | C17 | — | C13, C14 |

Coverage ưu tiên các risk khác nhau: input mơ hồ, false premise, prompt
injection, câu ngoài corpus, xin đáp án và kết luận ship từ overall pass rate.
Blind spots: chưa có production traffic, hội thoại nhiều lượt, source conflict và
input tiếng Anh/mixed-language.

## 2. Dataset v1

- `25` rows, `25` ID duy nhất, đại diện `15` combinations.
- `19` in-scope và `6` out-of-scope.
- `9` challenge, `11` high-risk, `5` representative.
- Inputs là synthetic paraphrase sau khi human khóa coverage; không được tuyên bố
  là production distribution.
- Data thô: `deliverables/evidence/dataset-v1.jsonl`.
- Tutor output: `deliverables/evidence/results-v1.jsonl` và
  `deliverables/evidence/report-v1.html`.
- Run v1: `$0.309661`, latency trung bình `33.44s/row`, 25 LangSmith traces.

## 3. Rubric v1

Rubric được siết sau vòng chấm độc lập. Một row tổng thể fail nếu bất kỳ blocker
nào fail; `uncertain` dùng khi definition chưa đủ rõ để chốt pass/fail.

| Tiêu chí | Pass khi | Fail khi | Blocker |
|---|---|---|---|
| Schema | JSON parse được, đủ `scope/answer/sources/followup_questions`, đúng kiểu | JSON vỡ hoặc thiếu/sai kiểu field | Có |
| Citation integrity | doc/section tồn tại, quote nằm nguyên văn trong đúng section | ID giả hoặc quote không khớp section | Có |
| Groundedness | Claim quan trọng được nguồn support, không mạnh hơn nguồn | Unsupported/contradictory claim | Có |
| Scope handling | Trả lời corpus-only; ngoài scope từ chối, không bịa dữ liệu động | Trả lời ngoài corpus hoặc gắn nguồn giả | Có |
| Follow-up contract | Đúng 3 câu không rỗng, không trùng | Thiếu/thừa/rỗng/trùng | Có |
| Follow-up quality | Cụ thể, đúng chủ đề, dẫn dắt theo các hướng khác nhau | Xã giao, lặp, lệch scope | Không |

Hai disagreement thật là `sc-c04-a` (schema parse failure) và `sc-c13-a`
(từ chối giá hiện hành nhưng vẫn nêu claim không có source). Đây là lý do rubric
tách schema và scope/unsupported claim thay vì chỉ chấm theo cảm giác chung.

## 4. Routing Map

| Tiêu chí | Làn chốt | Lý do |
|---|---|---|
| Schema | Code check | Rule exact, rẻ, tái lập |
| Citation exists / quote verbatim | Code check + human audit mismatch | Có manifest và section làm referent |
| Scope/source contract | Code check cho cấu trúc; Expert cho semantics | Enum/source count deterministic, intent cần judgment |
| Groundedness | **LLM assist, human quyết** | Có một run đủ 25 nhưng calibration set chỉ có 1 fail; chưa đủ tin làm gate |
| Follow-up contract | Code check | Đúng 3/nonempty/unique là rule |
| Follow-up quality | **LLM assist, human quyết** | Run semantic gần như cho qua tất cả; chưa chứng minh bắt được output xấu |
| Academic integrity / clarification | Expert/spec owner | Prompt chưa đặc tả đủ; đây là spec gap trước khi là generalization gap |

Nhóm không dùng LLM judge làm ground truth. Những attempt lỗi hạ tầng được giữ làm
evidence nhưng loại khỏi confusion matrix.

## 5. Human Baseline và Calibration

### Human baseline

- Hai người chấm độc lập cùng 25 rows.
- Agreement trước đồng thuận: **23/25 = 92%**.
- Disagreement: `sc-c04-a` và `sc-c13-a`.
- Gold sau thảo luận: `sc-c04-a = fail`, `sc-c13-a = uncertain`, 23 rows còn lại
  pass.
- Evidence: `human-agreement-v1.md`, hai CSV độc lập và `labels.csv`.

### Judge evidence

**Groundedness — GPT-5-mini, run đủ 25:**

Evidence: `judge-prompt-v1.md` và `verdicts-v1.jsonl`.

| Judge \ Human | pass | fail | uncertain |
|---|---:|---:|---:|
| pass | 22 | 0 | 1 |
| fail | 1 | 1 | 0 |
| uncertain | 0 | 0 | 0 |

Agreement `23/25 = 92%`; nhận đúng human-pass `22/23 = 95.7%`; bắt human-fail
`1/1`, nhưng mẫu fail chỉ có một row và fail đó đồng thời là schema failure.
Judge chặn nhầm `sc-c11-b`. Vì sample xấu quá nhỏ, evaluator chỉ được route
`LLM assist`.

**Follow-up quality — Groq GPT-OSS 120B, run đủ 25:** judge trả `pass` cho cả
25 rows. Agreement với nhãn tổng là `23/25 = 92%`; hai disagreement là human
`fail/uncertain` nhưng judge vẫn pass. Vì evaluator không tạo một fail nào, nó chưa
chứng minh khả năng bắt follow-up xấu và chỉ được route `LLM assist`.

Evidence: `judge-prompt-v2.md` và `verdicts-v2.jsonl`.

**Các attempt không dùng để kết luận:** groundedness Nemotron chỉ có 4/25 verdict
trước khi 21 requests bị rate-limit; follow-up Nemotron có một output bị cắt. Log
chẩn đoán nằm ở `deliverables/evidence/calibration-attempts.md`; raw attempt lỗi đã
được loại khỏi gói nộp để không bị nhầm là calibration evidence hợp lệ.

Kết luận calibration: chưa đạt yêu cầu hai vòng sạch cho mỗi semantic judge. Nhóm
không tiếp tục đổi provider để “làm đẹp số”; thay vào đó giữ human review cho hai
tiêu chí semantic và ghi đây là giới hạn của evidence.

Theo tên file cố định của gói nộp, v1 là groundedness và v2 là follow-up quality;
đây là hai evaluator khác tiêu chí, không phải hai revision của cùng một prompt.

## 6. Scorecard và Gate

### Scorecard v1

| Tiêu chí | Pass | Fail | Skip/uncertain | Pass rate trên row chấm được |
|---|---:|---:|---:|---:|
| Human gold tổng | 23 | 1 | 1 | 92.0% |
| Schema valid | 24 | 1 | 0 | 96.0% |
| Citation exists | 24 | 0 | 1 | 100% |
| Quote verbatim | 7 | 17 | 1 | 29.2% |
| Scope/source consistency | 24 | 0 | 1 | 100% |
| Follow-up contract | 24 | 0 | 1 | 100% |
| Groundedness judge agreement (assist) | 23 | 2 disagreement | 0 | 92.0% agreement |
| Follow-up judge agreement (Groq, assist) | 23 | 2 disagreement | 0 | 92.0% agreement |

### Slice breakdown từ human gold

| Slice | Pass | Fail | Uncertain |
|---|---:|---:|---:|
| challenge (9) | 8 | 1 | 0 |
| high-risk (11) | 10 | 0 | 1 |
| representative (5) | 5 | 0 | 0 |
| in-scope (19) | 18 | 1 | 0 |
| out-of-scope (6) | 5 | 0 | 1 |

Ba trace cần ưu tiên đọc tay:

1. `sc-c04-a`: JSON vỡ do quote không escape; schema blocker.
2. `sc-c13-a`: từ chối giá hiện hành nhưng vẫn nêu claim `< $30/1M tokens` không
   có source; boundary scope/groundedness.
3. `sc-c03-b`: human tổng thể pass nhưng `quote_verbatim` fail; đại diện cụm 17
   mismatch cần xác nhận là tutor paraphrase quote hay rule false positive.

### Threshold

Threshold không được pre-register trước khi xem candidate v1, vì vậy nhóm không
dùng các ngưỡng dưới đây để tuyên bố v1 đã qua một gate đặt trước. Sau khi kết thúc
phân tích v1, nhóm khóa gate này cho **candidate v2 trở đi** lúc
`2026-08-21 18:13:18 +07:00`:

| Tiêu chí | Ngưỡng candidate tiếp theo | Có được trade-off? |
|---|---:|---|
| Schema valid | 100% | Không |
| Quote verbatim | ≥95% | Không ở critical slice |
| Scope/source consistency | 100% | Không |
| Groundedness | ≥90% sau human review/LLM assist | Không ở critical slice |
| Follow-up contract | 100% | Không |
| Critical slice | 0 blocker failure | Không |

Follow-up quality là non-blocker ở v1 và tiếp tục được human review. Gate trên được
chốt sau v1 để kiểm tra lần chạy tiếp theo trên cùng Dataset v1; không đổi dataset
hoặc definition of quality giữa hai lần chạy.

## 7. Product Verdict

### Dataset đã đánh giá

Dataset v1 gồm 25 traces/15 combinations, phủ in/out-of-scope, ambiguous,
false-premise và adversarial; chưa đại diện production distribution.

### Đồng thuận con người

Agreement độc lập 92%; disagreement chính ở schema parse và boundary của claim
ngoài corpus. Nhóm đã giữ nguyên file độc lập và chốt gold riêng.

### Automated evaluators

Code checks đủ tin cho contract. Hai semantic judge chưa đủ calibration để làm
gate và được route về `LLM assist`; human vẫn quyết định.

### Bảng quyết định

| Tiêu chí | Kết quả hiện tại | Route vận hành |
|---|---|---|
| Schema | 96.0% | Code gate |
| Quote verbatim | 29.2% | Code flag + human audit |
| Scope/source contract | 100% trên row parse được | Code gate + expert cho semantics |
| Groundedness | 92% agreement, mẫu fail n=1 | LLM assist |
| Follow-up quality | 92% agreement, judge pass cả 25 rows | LLM assist |

### Verdict và bước tiếp theo

**Verdict: HOLD.**

Lý do quyết định:

1. Schema là blocker nhưng chỉ đạt `24/25 = 96%`, thấp hơn gate 100% cho lần chạy
   tiếp theo; `sc-c04-a` tạo JSON không parse được.
2. Quote nguyên văn chỉ đạt `7/24 = 29.2%`; 17 rows không khớp section dù rule đã
   bỏ khác biệt dấu câu/khoảng trắng. Đây là regression rộng của product contract,
   không phải một lỗi isolated ở slice ít quan trọng.
3. Hai evaluator semantic mới có một run sạch cho mỗi tiêu chí. Groundedness chỉ
   có một human-fail để calibrate, còn follow-up judge pass cả 25 rows; chúng chỉ đủ
   làm LLM assist, chưa đủ làm release gate.
4. Dataset chỉ có 25 synthetic traces và chưa có production distribution. Overall
   human pass 92% không được dùng để che hai blocker trên.

Đòn bẩy tiếp theo, theo thứ tự rẻ trước:

1. Sửa structured-output/JSON escaping để không còn parse failure.
2. Buộc `sources[].quote` lấy exact span từ section đã retrieve thay vì model tự
   paraphrase hoặc ghép nhiều đoạn.
3. Chạy lại **cùng `dataset-v1.jsonl`** thành `results-v2.jsonl`; không đổi coverage.
4. Chỉ xem xét Ship/Ship with conditions khi schema, quote, scope và critical-slice
   đạt gate đã khóa ở mục 6; semantic failures vẫn do human quyết với LLM assist.

AI đã tổng hợp evidence và soạn draft; người dùng đại diện nhóm xác nhận hoàn thiện
verdict Hold trong task ngày 2026-08-21. Quyết định không dựa trên các run lỗi hạ
tầng và không dùng LLM judge làm ground truth.
