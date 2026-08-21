# REPORT — Eval loop A→Z: VLearn AI Tutor

Report A→Z của eval loop — mỗi mục ứng một phase của bài lab. Mọi số liệu và quyết
định trong đây phải dẫn được xuống file data thô trong `evidence/` (dataset-v1.jsonl,
results-vN.jsonl, labels.csv, judge-prompt-vN.md, verdicts-vN.jsonl, braintrust-link.md).

### Thành viên nhóm

| Họ và tên | Mã sinh viên |
|---|---|
| Trần Kiên | `2A202601598` |
| Nguyễn Phú Quang | `2A202602017` |


---

## 1. Input Grid

> Lưới input = trục "ai hỏi" × "hỏi kiểu gì". LLM giúp sinh input, con người kiểm soát
> coverage. Trả lời các câu hỏi sau rồi vẽ lưới của bạn.

- User được phủ: học viên đang làm lab, học viên đang xem slide, học viên ôn lại và
  user không cung cấp context/adversarial.
- Intent được phủ: hỏi khái niệm, so sánh, áp dụng, đọc kết quả, xin đáp án và hỏi
  ngoài corpus.
- Nhóm đã human-select ngày 2026-08-21: reject `C01, C02, C09, C10, C12`; keep 15
  combinations còn lại. File quyết định: `deliverables/COVERAGE_REVIEW.md`.
- High-risk: kết luận ship từ overall pass rate (`C07`), thay human bằng judge chưa
  calibrate (`C08`), xin/bịa verdict (`C11`), dữ liệu hiện hành ngoài corpus (`C13`),
  prompt injection + citation giả (`C14`) và overfit judge (`C20`).
- Chưa có production traces nên **không tuyên bố frequency distribution**. Các
  representative case chỉ là giả thuyết cần đối chiếu sau launch/dog-fooding.

### Dimensions đã khóa

| Dimension | Values trong Dataset v1 | Behavior đúng thay đổi |
|---|---|---|
| Loại câu hỏi | khái niệm · so sánh · áp dụng · đọc kết quả · xin đáp án · ngoài bài | trả lời · tổng hợp · scaffold · yêu cầu evidence · không làm hộ · từ chối |
| Độ phủ corpus | trực tiếp · rải nhiều nguồn · chỉ một phần · không có | trả lời/cite · tổng hợp · nói giới hạn · từ chối |
| Độ rõ | rõ · mơ hồ/deixis · nhiều ý · false premise | trả lời · hỏi lại · tách ý · sửa giả định trước |
| Bối cảnh học | có slide · đang làm lab · ôn lại · không context | dùng slide · scaffold · hệ thống hóa · xin thêm context/giữ boundary |

### Lưới của bạn

| Bối cảnh \ Intent | Khái niệm/so sánh | Áp dụng | Đọc kết quả | Xin đáp án / ngoài bài |
|---|---|---|---|---|
| Đang làm lab | — | C03, C06, C19 | C16 | C11 |
| Có slide | C05, C18 | — | C04, C07, C20 | — |
| Ôn lại | C08, C15 | — | — | — |
| Không context | — | C17 | — | C13, C14 |

---

## 2. Dataset v1

> Dataset là "bộ đề thi" của tutor. Nêu rõ nó phủ những ô nào trong input-grid.

- Dataset có **25 rows / 15 combinations**, ID duy nhất, parse JSONL hợp lệ.
- Scope: 19 in-scope (76%) và 6 out-of-scope (24%). Ambiguous/deixis: 6 rows
  (24%, C04/C05/C17). High-risk: 11 rows (44%). Challenge: 9 (36%);
  representative: 5 (20%).
- Hai paraphrase của cùng combination là biến thể ngôn ngữ, **không được tính là
  coverage mới**. Coverage được báo theo 15 combinations.
- Tất cả input hiện là synthetic AI paraphrase từ combination do human chọn; repo
  không có production trace/fallback pack. Không row nào được ghi là user trace thật.
- Human review: nhóm loại 5 scenario candidates và giữ 15; sau yêu cầu “triển khai
  toàn bộ”, 25 paraphrase được ghi `keep_human_2026-08-21`. Cần hai thành viên đọc
  lại trước live run nếu đây chưa phản ánh quyết định chung của cả nhóm.
- Blind spots: chưa có production distribution, hội thoại nhiều lượt, lỗi retrieval
  từ trace thật, input tiếng Anh/mixed-language và case source conflict/stale corpus.
- **Checkpoint human còn thiếu:** nếu chỉ giữ 10 rows, nhóm phải tự chọn và ghi lý do;
  AI không quyết định thay mục này.

### Danh sách scenario (bảng tóm tắt)

| scenario_id | ô trong lưới | expected | nguồn câu hỏi |
|---|---|---|---|
| sc-c03-a/b | áp dụng · rõ · lab | hướng dẫn grid, không chọn coverage thay nhóm | AI paraphrase / human-kept C03 |
| sc-c04-a/b | đọc kết quả · mơ hồ · slide | hỏi thêm threshold/slice/evidence | AI paraphrase / human-kept C04 |
| sc-c05-a/b | khái niệm · deixis · slide | dùng context để giải thích matrix | AI paraphrase / human-kept C05 |
| sc-c06-a/b | áp dụng · multi-intent · lab | tách code và semantic judge | AI paraphrase / human-kept C06 |
| sc-c07-a/b | đọc kết quả · false premise | không ship từ headline metric | AI paraphrase / human-kept C07 |
| sc-c08-a/b | judge · false premise · ôn lại | giữ human baseline/calibration | AI paraphrase / human-kept C08 |
| sc-c11-a/b | xin đáp án · lab | không bịa/viết hộ verdict | AI paraphrase / human-kept C11 |
| sc-c13-a/b | ngoài corpus · dữ liệu động | từ chối giá hiện hành không có nguồn | AI paraphrase / human-kept C13 |
| sc-c14-a/b | adversarial · không corpus | chống injection/citation giả | AI paraphrase / human-kept C14 |
| sc-c15-a | so sánh · multi-intent | route code/judge/human | AI paraphrase / human-kept C15 |
| sc-c16-a | đọc calibration · partial | không áp ngưỡng agreement phổ quát | AI paraphrase / human-kept C16 |
| sc-c17-a/b | lấy data · mơ hồ | hỏi context, nêu nguồn data hợp lệ | AI paraphrase / human-kept C17 |
| sc-c18-a | trace · typo · slide | hiểu input tự nhiên, giải thích trace | AI paraphrase / human-kept C18 |
| sc-c19-a | code + judge · multi-intent | code trước, mỗi judge một tiêu chí | AI paraphrase / human-kept C19 |
| sc-c20-a | judge ceiling · false premise | đổi ít một/chuyển lane khi chạm trần | AI paraphrase / human-kept C20 |

---

## 3. Rubric v1

> Rubric = định nghĩa "đủ tốt" mà cả team chấm giống nhau. Thu hẹp scope trước khi
> viết tiêu chí.

> **Trạng thái: draft v0.9 trước human baseline.** Chưa được gọi là rubric v1 đã
> calibrate cho tới khi hai người chấm độc lập và xử lý disagreement.

Một câu in-scope “đủ tốt” khi trả đúng intent bằng thông tin được quote trong corpus,
không mạnh hơn bằng chứng, tuân thủ JSON contract và đưa ba hướng học tiếp có giá trị.
Một câu out-of-scope pass khi từ chối khéo, không bịa nguồn/nội dung và dẫn người học
về chủ đề eval có trong corpus.

### Rubric của bạn

| Tiêu chí | Pass khi | Fail khi | Blocker? (draft) |
|---|---|---|---|
| Schema contract | Parse được JSON; đủ `scope/answer/sources/followup_questions`, đúng kiểu | JSON vỡ, thiếu/sai kiểu field | Có |
| Citation integrity | Mỗi source có doc/section tồn tại và quote nguyên văn không rỗng trong đúng section | ID giả, quote rỗng/lệch section | Có |
| Groundedness | Mọi claim quan trọng được ít nhất một quote hỗ trợ trực tiếp; không mạnh hơn nguồn | Có unsupported/contradictory claim hoặc biến ví dụ thành luật | Có |
| Scope handling | In-scope trả lời từ corpus; out-of-scope từ chối và không gắn nguồn giả | Từ chối oan, trả lời ngoài corpus, hoặc scope/source mâu thuẫn | Có |
| Follow-up contract | Đúng 3 chuỗi không rỗng, không trùng | Thiếu/thừa/rỗng/trùng | Có |
| Follow-up quality | Ba câu cụ thể, đúng chủ đề, mở các hướng đào sâu khác nhau | Xã giao, lặp, lệch scope hoặc tiếp tục chủ đề ngoài corpus | **Nhóm xác nhận sau disagreement** |

Boundary examples dùng cho judge draft nằm tại
`eval/judge_prompts/groundedness-v1.md` và
`eval/judge_prompts/followup-quality-v1.md`.

**Chưa hoàn thành:** 2-way independent cross-label, human–human agreement và disagreement cases.
Những dữ kiện đó phải được thêm sau Phase 2; AI không được tự tạo.

---

## 4. Routing Map

> Cái gì kiểm bằng code, cái gì cần LLM judge, cái gì phải đến tay expert. Không phải
> tiêu chí nào cũng cần LLM.

- Code lane hiện có 5 checks: `schema_valid`, `citation_exists`, `quote_verbatim`,
  `scope_source_consistency`, `followup_contract`. Hai check cuối là rule nhóm thêm.
- Groundedness và follow-up quality cần đọc ngữ nghĩa nên có judge riêng. Cho tới khi
  calibrate đạt gần human–human ceiling, verdict judge chỉ là **LLM assist**.
- Judge dùng `temperature=0`; model chưa khóa vì `.env` chưa có provider key tương
  thích cho default tutor/judge. Khi chọn phải dùng model khác họ tutor và ghi lại.
- Spec-gap backlog: system prompt hiện chưa nói rõ “không viết hộ capstone verdict”
  và chưa quy định rõ khi nào phải hỏi lại input mơ hồ. `C11` và phần clarify của
  `C04/C05/C17` chưa nên được gọi là generalization failure trước khi spec được sửa.
- Các contract đã có rõ trong system prompt (schema, corpus-only, citation, đúng ba
  follow-up) mà model lúc làm được lúc không là generalization-gap candidates.

### Bảng routing

| Tiêu chí | Code | LLM judge | Con người | Lý do |
|---|---|---|---|---|
| Schema contract | Chính | Không | Audit lỗi parser | Rule exact, rẻ và tái lập |
| Citation integrity | Chính | Không | Audit false positive của token match | Manifest/section/quote là referent deterministic |
| Scope/source consistency | Chính cho cấu trúc | Chưa | Quyết định semantic scope | Code bắt enum/empty sources; intent cần judgment |
| Groundedness | Code đã loại citation hỏng trước | Assist → Judge nếu calibrated | Gold labels + audit | Cần đối chiếu nghĩa claim với quote |
| Follow-up contract | Chính | Không | Không cần thường xuyên | Đúng 3/nonempty/unique là rule |
| Follow-up quality | Không | Assist → Judge nếu calibrated | Gold labels + audit | Tính dẫn dắt/liên quan phụ thuộc ngữ nghĩa |
| Academic-integrity/clarification | Không | Không ở v1 | Expert/spec owner | Prompt chưa đặc tả đủ; sửa spec trước eval |

Lệnh chạy hai judge sau khi có gold labels:

```powershell
python eval/judge.py --prompt eval/judge_prompts/groundedness-v1.md --output verdicts-groundedness-v1.jsonl --labels labels-groundedness.csv
python eval/judge.py --prompt eval/judge_prompts/followup-quality-v1.md --output verdicts-followup-v1.jsonl --labels labels-followup.csv
```

---

## 5. Calibration Report

> Judge chỉ đáng tin khi đã calibrate với chuẩn vàng của con người. Đây là minh chứng
> cho việc đó.

- Trần Kiên đã **gán nhãn tay 25/25 row**: 23 pass, 1 fail, 1 uncertain. Đây mới là
  một rater độc lập. Nguyễn Phú Quang đã chấm cùng 25 row: 22 pass, 3 fail.
- Human–human agreement trước đồng thuận: **23/25 = 92%**. Hai disagreement là
  `sc-c13-a` (uncertain/fail) và `sc-c20-a` (pass/fail). Evidence:
  `deliverables/evidence/human-agreement-v1.md`.
- Chưa được gọi là gold labels cho tới khi hai thành viên tự thảo luận hai case trên
  và ghi quyết định vào `labels.csv`.
- Chạy `python3 eval/judge.py`: **agreement** giữa judge và nhãn người là bao nhiêu %? Dán
  confusion matrix vào đây.
- Judge **sai ở đâu**? (chặt quá / lỏng quá / lệch ở nhóm câu nào — in-scope hay
  out-of-scope?)
- Bạn đã sửa `eval/judge_prompt.md` thế nào sau vòng calibrate đầu? Agreement sau sửa?
- Kết luận: judge của bạn **đủ tin để chấm tự động tiêu chí nào**, và tiêu chí nào vẫn
  phải giữ cho người?

### Confusion matrix (dán output judge.py)

```
CHƯA CHẠY — không có gold labels, không được dùng judge làm ground truth.
```

Checkpoint bắt buộc trước khi điền mục này:

1. Có `results-v1.jsonl` kèm trace link.
2. Hai file `labels-tran-kien.csv` và `labels-nguyen-phu-quang.csv` được chấm độc lập.
3. Chạy `agreement.py`, lưu agreement trước đồng thuận và disagreement cases.
4. Đồng thuận gold label theo từng tiêu chí mà judge sẽ chấm.
5. Mỗi judge chạy ít nhất hai vòng; mỗi vòng chỉ đổi một yếu tố prompt và lưu
   confusion matrix/TPR/TNR cùng pattern lệch.

---

## 6. Scorecard & Gate

> Tổng hợp điểm theo rubric trên dataset v1, rồi ra quyết định gate như một PM thật.

- Kết quả chạy `eval/run_eval.py` + `eval/judge.py` trên dataset v1: **pass rate** theo từng tiêu
  chí là bao nhiêu? (kèm link/chỉ đường tới results.jsonl, verdicts.jsonl, report.html)
- Chi phí 1 vòng eval là bao nhiêu ($, token)? Latency trung bình 1 câu?
- **Gate**: ngưỡng nào thì ship? Ví dụ: groundedness pass ≥ 90%, không có fail nào ở
  nhóm blocker... — định nghĩa ngưỡng của bạn và giải thích vì sao.
- Kết quả hiện tại: **SHIP hay CHƯA SHIP**? Căn cứ vào gate ở trên.
- Nếu chưa ship: 3 lỗi lớn nhất cần fix ở tutor (prompt, retrieval, corpus)?

### Scorecard

Tutor run v1 đã có 25 traces trong `deliverables/evidence/results-v1.jsonl`:
24 output parse được, 1 parse error; tổng chi phí `$0.309661`; latency trung bình
`33.44s/row`. Đây là số liệu vận hành, chưa phải scorecard chất lượng vì còn thiếu
gold labels và judge calibration.

| Tiêu chí | Pass | Fail | Uncertain | Pass rate |
|---|---|---|---|---|
| | | | | |

### Quyết định gate

**CHƯA ĐƯỢC PHÉP QUYẾT ĐỊNH** — đã có live results v1, nhưng chưa có gold labels,
threshold được khóa trước candidate tiếp theo hoặc calibration evidence. Nhóm cần
đặt threshold trước khi chạy candidate v2; không được hồi tố threshold cho v1.

---

## 7. Verdict + Report cuối

> Kết luận cuối cùng của bạn với tư cách PM chịu trách nhiệm chất lượng tutor.
> Verdict đi kèm report 1 trang đủ 5 phần — viết bằng ngôn ngữ PM, không dán log thô.

### Report

#### 1. Dataset đã đánh giá

(tập nào, bao nhiêu traces, coverage chính là gì, blind spot nào còn lại)

#### 2. Quá trình đồng thuận của con người

- Agreement vòng độc lập (nhãn tổng): **92% (23/25)**.
- Mâu thuẫn cần xử lý: `sc-c13-a` (uncertain/fail) và `sc-c20-a` (pass/fail).
- Nhóm xử lý bằng cách nào: (siết định nghĩa / đổi thang / bỏ tiêu chí...)

#### 3. LLM judge

- Model judge: ________________
- Số vòng calibration: ___ — sau đó judge nhận đúng ___% output tốt và bắt đúng ___% output xấu
- Judge nào không calibrate nổi, vì sao: ________________

#### 4. Bảng quyết định routing (kèm lý giải)

| Tiêu chí | Ngưỡng pass | Giao cho | Vì sao (dựa trên số liệu) |
|---|---|---|---|
| vd: groundedness | ≥90% | LLM judge + audit 10%/tuần | bắt đúng 91% output xấu sau 2 vòng near-miss |
|  |  |  |  |
|  |  |  |  |

#### 5. Verdict + bước tiếp theo

**Ship / Ship with conditions / Hold** — vì: ________________

- Nếu Ship: monitoring tuần đầu xem gì, sample bao nhiêu %, alert ở ngưỡng nào?
- Nếu Hold: đòn bẩy tiếp theo (prompt → model → architecture) và metric chứng minh đã sẵn sàng?

### Câu hỏi tự soi

- Tin cậy nhất ở đâu, đáng lo nhất ở đâu? (dẫn scenario_id cụ thể)
- Nếu chỉ được fix **một thứ** trước khi cho học viên thật dùng, đó là gì?
- Eval loop này sẽ chạy lại **khi nào** (mỗi lần đổi prompt? mỗi tuần? khi corpus đổi?) và ai nhìn kết quả?
- Điều gì trong bài này bạn sẽ **mang về áp dụng** vào sản phẩm thật của mình?
