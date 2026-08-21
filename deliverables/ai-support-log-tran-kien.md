# AI Support Log — Trần Kiên (`2A202601598`)

**AI đã giúp tôi ở đâu?**

AI hỗ trợ paraphrase inputs sau khi nhóm khóa coverage, draft code checks/judge
prompt, kiểm tra cấu trúc artifact và tổng hợp số liệu thật vào report.

**AI sai, hời hợt hoặc làm mất coverage ở đâu?**

AI đã đi quá scope khi biến criterion-specific labels/candidate thành yêu cầu
bắt buộc và dành quá nhiều thời gian đổi provider/retry thay vì chốt deliverables.

**Tôi đã tự sửa hoặc quyết định lại điều gì?**

Tôi tự chấm labels, cùng nhóm xử lý disagreement và chốt gold. Tôi giữ các judge
chưa đủ calibration ở vai trò LLM assist, xác nhận verdict Hold và ưu tiên sửa JSON
escaping/quote extraction trước lần chạy tiếp theo.
