# AI Support Log — Nguyễn Phú Quang (`2A202602017`)

**AI đã giúp tôi ở đâu?**

AI hỗ trợ paraphrase inputs sau khi nhóm khóa coverage, draft code checks/judge
prompt, kiểm tra cấu trúc artifact và tổng hợp số liệu thật vào report.

**AI sai, hời hợt hoặc làm mất coverage ở đâu?**

AI đã đi quá scope khi biến criterion-specific labels/candidate thành yêu cầu bắt
buộc và dành quá nhiều thời gian đổi provider/retry thay vì chốt deliverables.

**Tôi đã tự sửa hoặc quyết định lại điều gì?**

Tôi chấm độc lập 25 outputs để đo human agreement, cùng nhóm xử lý disagreement và
chốt gold. Nhóm không dùng judge chưa calibrate làm ground truth, giữ chúng ở vai
trò LLM assist và chốt Hold dựa trên schema/quote blockers.
