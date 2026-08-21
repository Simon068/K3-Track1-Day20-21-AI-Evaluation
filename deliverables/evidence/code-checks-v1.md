# Code checks — results v1

Đã chạy ngày 2026-08-21 trên `results-v1.jsonl`:

```powershell
python eval/code_checks.py deliverables/evidence/results-v1.jsonl
```

| Check | Pass | Fail/skip |
|---|---:|---:|
| `schema_valid` | 24 | 1 fail |
| `citation_exists` | 24 | 0 fail, 1 skip |
| `quote_verbatim` | 7 | 17 fail, 1 skip |
| `scope_source_consistency` | 24 | 0 fail, 1 skip |
| `followup_contract` | 24 | 0 fail, 1 skip |

- Schema fail: `sc-c04-a` — raw JSON không parse được.
- Quote mismatch: `sc-c03-b`, `sc-c04-b`, `sc-c05-a`, `sc-c05-b`, `sc-c06-a`,
  `sc-c06-b`, `sc-c07-a`, `sc-c07-b`, `sc-c08-a`, `sc-c11-a`, `sc-c15-a`,
  `sc-c16-a`, `sc-c17-a`, `sc-c17-b`, `sc-c18-a`, `sc-c19-a`, `sc-c20-a`.

`quote_verbatim` so theo chuỗi token liên tiếp sau khi bỏ dấu tiếng Việt,
lowercase, dấu câu và khác biệt khoảng trắng. Vì vậy 17 mismatch này không chỉ do
format/gạch đầu dòng; human vẫn cần xác nhận contract “quote nguyên văn” có được
áp dụng như blocker ở release gate hay không.

Code check và human labels là hai evidence khác nhau. Nhóm phải đọc các mismatch để
quyết định đây là lỗi tutor hay false positive của rule; không tự động đổi nhãn người
theo kết quả code.
