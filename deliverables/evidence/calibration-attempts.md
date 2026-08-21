# Calibration attempts — 2026-08-21

## Groundedness / GPT-5-mini

- Evidence version: `judge-prompt-v1.md` + `verdicts-v1.jsonl`.
- 25/25 verdict hợp lệ.
- Matrix judge × human: pass `[22,0,1]`; fail `[1,1,0]`; uncertain `[0,0,0]`.
- Agreement: 23/25 = 92%.
- Pattern: false reject `sc-c11-b`; chỉ có một human-fail nên bad-case recall
  không có đủ sample để bảo vệ automated gate.

## Follow-up quality / Nemotron

- 24/25 output judge parse hợp lệ; `sc-c04-b` bị cắt trước JSON, không phải verdict
  uncertain.
- Trong 24 verdict thật, judge đều pass; agreement với nhãn tổng 22/24 = 91.7%.
- Pattern: judge chưa chứng minh khả năng bắt follow-up xấu; route LLM assist.
- Raw attempt đã được loại khỏi gói nộp để tránh nhầm với evaluator hợp lệ; số liệu
  trên được giữ làm log chẩn đoán, không dùng làm release evidence.

## Groundedness / Nemotron

- Chỉ 4 verdict thật; 21 row HTTP 429. Không dùng matrix 1/4 để kết luận chất lượng.
- Raw infra file đã được loại khỏi gói nộp vì không phải calibration run hợp lệ.

## Follow-up quality / Groq GPT-OSS 120B

- Evidence version: `judge-prompt-v2.md` + `verdicts-v2.jsonl`.
- 25/25 verdict hợp lệ; judge pass cả 25 rows.
- Matrix judge × human: pass `[23,1,1]`; fail `[0,0,0]`; uncertain `[0,0,0]`.
- Agreement: 23/25 = 92%.
- Pattern: evaluator quá dễ, chưa chứng minh bad-case recall; route LLM assist.

## Routing consequence

Không evaluator semantic nào được dùng làm ground truth hoặc automated release
gate. Groundedness và follow-up quality được giữ ở làn LLM assist; human quyết.

Lưu ý version: v1 và v2 là hai tiêu chí khác nhau, không phải hai lần chỉnh prompt
của cùng một tiêu chí. Do đó các file này không được dùng để tuyên bố đã đạt yêu
cầu hai vòng calibration cho từng judge.
