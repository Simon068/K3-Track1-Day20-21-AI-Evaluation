# Human agreement — vòng độc lập

- Ngày đo: 2026-08-21
- Raters: Trần Kiên (`2A202601598`) và Nguyễn Phú Quang (`2A202602017`)
- Tập chung: 25 scenario IDs
- Đồng thuận hoàn toàn: **23/25 = 92%**
- Pairwise agreement: **92%**

Lệnh đã chạy:

```powershell
python eval/agreement.py labels-tran-kien.csv labels-nguyen-phu-quang.csv
```

## Hai case bất đồng

| scenario_id | Trần Kiên | Nguyễn Phú Quang | Trạng thái |
|---|---|---|---|
| `sc-c04-a` | fail | pass | JSON raw bị vỡ do quote không escape; một người coi đây là schema blocker |
| `sc-c13-a` | uncertain | pass | Một người chấp nhận boundary, một người giữ uncertain vì claim không source |

## Quyết định sau đồng thuận

Nhóm chốt gold labels:

- `sc-c04-a`: `fail` — `fail: schema — JSON không parse được`.
- `sc-c13-a`: `uncertain` — tutor đã từ chối giá hiện hành nhưng vẫn đưa claim
  `< $30/1M tokens` không có source.
- `sc-c20-a`: `pass`.

Gold labels được lưu tại `deliverables/evidence/labels.csv`. Hai file độc lập phía
trên vẫn được giữ nguyên để bảo toàn evidence agreement trước đồng thuận.
