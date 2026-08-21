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
| `sc-c13-a` | uncertain | fail | Chờ hai thành viên thảo luận và ghi lý do mỗi phía |
| `sc-c20-a` | pass | fail | Chờ hai thành viên thảo luận và ghi lý do mỗi phía |

`labels-consensus-draft.csv` chỉ chép 23 nhãn hai người đã đồng thuận và để trống
hai case trên. Không được đổi tên thành `labels.csv` hoặc dùng calibrate judge trước
khi hai thành viên tự chốt nhãn vàng và note.
