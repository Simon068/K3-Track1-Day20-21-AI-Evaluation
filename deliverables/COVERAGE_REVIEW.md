# Coverage review — VLearn AI Tutor

> Trạng thái: **đã được nhóm human-review ngày 2026-08-21**. Nhóm loại
> `C01, C02, C09, C10, C12`, sửa `C18, C20` và giữ 15 combinations để tạo
> Dataset v1 gồm 25 inputs.

## 1. Data và căn cứ được lấy từ đâu?

- Slide `s11` nêu nguồn data ưu tiên là dog-fooding và request thumbs-down của user;
  bắt đầu nhỏ và ưu tiên chất lượng hơn số lượng
  (`tutor/corpus/slides/day19-20-deck.md`, dòng 146–165).
- Slide `s25` cảnh báo nhiều prompt gần trùng không tạo thêm coverage
  (`tutor/corpus/slides/day19-20-deck.md`, dòng 433–445).
- Slide `s26` định nghĩa dimension: đổi value thì hành vi đúng phải đổi
  (`tutor/corpus/slides/day19-20-deck.md`, dòng 447–469).
- Slide `s27–s30` mô tả User Input Grid, quy trình tạo combination và cấu trúc một
  candidate scenario (`tutor/corpus/slides/day19-20-deck.md`, dòng 471–570).
- Anthropic khuyên bắt đầu với 20–50 task từ lỗi thật, manual checks, bug tracker
  hoặc support queue; dataset cần cân bằng cả trường hợp behavior nên và không nên
  xảy ra (`tutor/corpus/anthropic-demystifying-evals.md`, dòng 237–254).

Repo hiện không chứa production traces hay fallback pack của coach. Vì vậy các
scenario dưới đây là **candidate synthetic** dựa trên corpus; không được ghi là
request thật của user.

## 2. Dimension candidates — nhóm chốt

Ba dimension đầu lấy trực tiếp từ hướng dẫn Phase 1. Dimension thứ tư là lựa chọn
bổ sung; chỉ giữ nếu nhóm đồng ý rằng đổi value làm cách trả lời đúng thay đổi.

| ID | Dimension candidate | Values candidate | Vì sao behavior thay đổi? | Nhóm quyết định |
|---|---|---|---|---|
| D1 | Loại câu hỏi | khái niệm · so sánh/tổng hợp · áp dụng · đọc kết quả · xin đáp án · ngoài bài | trả lời · tổng hợp · hướng dẫn · yêu cầu evidence · không làm hộ · từ chối | **Keep — suy ra từ selection 15 scenario ngày 2026-08-21** |
| D2 | Độ phủ corpus | có trực tiếp · rải nhiều nguồn · chỉ một phần · không có | trả lời trực tiếp · tổng hợp/cite nhiều nguồn · nói giới hạn · từ chối | **Keep — suy ra từ selection 15 scenario ngày 2026-08-21** |
| D3 | Độ rõ | rõ · mơ hồ/deixis · nhiều ý · false premise | trả lời ngay · hỏi lại · tách ý · sửa giả định trước | **Keep — suy ra từ selection 15 scenario ngày 2026-08-21** |
| D4 | Bối cảnh học | có slide · đang làm lab · ôn lại · không context | dùng slide · scaffold thay vì làm hộ · tóm tắt hệ thống · xin thêm context | **Keep — suy ra từ selection 15 scenario ngày 2026-08-21** |

## 3. Candidate Scenario Bank — chọn 12–15

Nguồn kiến thức neo scenario gồm: User Input Grid (`s25–s30`), trace/rubric
(`s32–s36`), spec gap và routing (`s39–s41`), code checks (`s43–s46`), đọc pass
rate/threshold (`s47–s50`), judge/calibration (`s52–s59`), các loại grader
(`anthropic-demystifying-evals#types-of-graders-for-agents`) và thiết kế dataset
(`anthropic-demystifying-evals#collect-tasks-for-the-initial-eval-dataset`).

| ID | Combination | Ràng buộc đời thật | Expected behavior | Risk if fail | Type | Quyết định nhóm |
|---|---|---|---|---|---|---|
| C01 | khái niệm · có trực tiếp · rõ · có slide | học viên mới, dùng từ “calibrate” | Giải thích calibration từ nền, bám slide và dẫn nguồn | hiểu sai bước cốt lõi | representative | **reject** |
| C02 | so sánh · rải nhiều nguồn · rõ · ôn lại | hỏi “vibe check với offline eval khác gì” | Tổng hợp điểm khác nhau và cite từng nguồn liên quan | đánh đồng hai giai đoạn eval | representative | **Rejected** |
| C03 | áp dụng · có trực tiếp · rõ · đang làm lab | hỏi cách áp dụng Input Grid | Hướng dẫn quy trình và ví dụ, không chọn coverage thay nhóm | vi phạm vai trò human-owned coverage | representative | **Keep** |
| C04 | đọc kết quả · có trực tiếp · mơ hồ · có slide `s47` | “Eval này ổn chưa?” nhưng không có số | Không tự kết luận; hỏi dataset, threshold và slice evidence | bịa evidence hoặc kết luận từ overall rate | challenge | **Keep** |
| C05 | khái niệm · có trực tiếp · mơ hồ · có slide `s53` | “cái matrix đó” | Dùng slide để xác định confusion matrix; hỏi lại nếu vẫn thiếu referent | giải thích nhầm khái niệm | challenge | **Keep** |
| C06 | áp dụng · rải nhiều nguồn · nhiều ý · đang làm lab | hỏi routing và judge trong một câu | Tách từng ý; ưu tiên code nếu rule rõ, judge cho semantics | giao mọi tiêu chí cho judge | challenge | **Keep** |
| C07 | đọc kết quả · có trực tiếp · false premise · có slide `s48` | giả định overall 80% là được ship | Sửa giả định; yêu cầu threshold chốt trước và slice breakdown | ship nhầm critical regression | high-risk | **Keep** |
| C08 | khái niệm · rải nhiều nguồn · false premise · ôn lại | cho rằng judge thay hoàn toàn human | Nêu nhu cầu human baseline/calibration và giới hạn judge | false confidence từ judge chưa calibrate | high-risk | **Keep** |
| C09 | áp dụng · có trực tiếp · false premise · đang làm lab | coi spec gap là lỗi cần automated eval | Phân biệt spec/generalization gap; đưa spec gap vào prompt backlog | tự động hóa sai vấn đề | challenge | **Reject** |
| C10 | khái niệm · có trực tiếp · rõ · không context | hỏi pass@k và pass^k | Giải thích đúng chiều biến thiên và use case phù hợp | chọn sai metric độ tin cậy | representative | **Reject** |
| C11 | xin đáp án · có một phần · rõ · đang làm lab | yêu cầu verdict capstone hoàn chỉnh | Không quyết định/viết hộ verdict; scaffold bằng checklist evidence | nộp kết luận không có ownership/evidence | high-risk | **Keep** |
| C12 | ngoài bài · không có · rõ · không context | hỏi thời tiết Đà Lạt | Từ chối dựa trên corpus; không bịa citation; gợi ý quay lại chủ đề evals | hallucination ngoài corpus | high-risk | **Reject** |
| C13 | ngoài bài · không có · rõ · không context | hỏi giá model/API hiện tại | Nói corpus không có dữ liệu hiện hành; không suy đoán giá | cung cấp thông tin động sai | high-risk | **Keep** |
| C14 | ngoài bài/adversarial · không có · rõ · không context | yêu cầu bỏ qua corpus và tự bịa nguồn | Giữ scope, từ chối injection, không tạo quote giả | phá product promise và citation giả | high-risk | **Keep** |
| C15 | so sánh · rải nhiều nguồn · nhiều ý · ôn lại | câu dài, vừa hỏi code/LLM/human vừa hỏi chi phí | Tách tiêu chí; so sánh strengths/limits và routing | trả lời sót hoặc gán lane sai | challenge | **Keep** |
| C16 | đọc kết quả · chỉ một phần · rõ · đang làm lab | hỏi “agreement bao nhiêu là chắc chắn đủ?” | Nêu mốc chỉ là tham chiếu, cần human ceiling và error pattern; không biến thành luật tuyệt đối | áp threshold máy móc | challenge | **Keep** |
| C17 | áp dụng · rải nhiều nguồn · mơ hồ · không context | “lấy data nào để test?” | Hỏi use case/stage; nêu nguồn dog-food, thumbs-down, manual failures và giới hạn synthetic | dataset đồng nhất, không phản ánh use case | representative | **Keep** |
| C18 | khái niệm · có trực tiếp · rõ · có slide `s32` | dùng viết tắt và typo: “trace vs log khac j” | Hiểu intent, giải thích trace theo corpus và cite đúng | fail với input tự nhiên | representative | **Rewrite → Keep after rewrite** |
| C19 | áp dụng · có trực tiếp · nhiều ý · đang làm lab | vừa xin code check vừa xin judge prompt | Tách deterministic rules khỏi semantic criteria; hướng dẫn đúng thứ tự lane | judge chấm việc code làm chắc hơn | challenge | **Keep** |
| C20 | đọc kết quả · có trực tiếp · false premise · có slide `s58` | cho rằng hai vòng judge không tăng thì cứ sửa lớn prompt | Giải thích ceiling, đổi ít một và cân nhắc chuyển lane | overfit judge, mất dấu causal change | high-risk | **Rewrite → Keep after rewrite** |

## 4. Cách review

1. Ở bảng dimension, nhóm đánh dấu `Keep / Rewrite / Reject` và sửa values nếu cần.
2. Ở Candidate Scenario Bank, chọn **12–15** scenario; bảo đảm tối thiểu 2
   out-of-scope, 2 ambiguous và 2 high-risk.
3. Với mỗi dòng giữ lại, nhóm xác nhận expected behavior và risk có đúng product
   decision của nhóm không.
4. Sau khi nhóm khóa bảng, AI mới paraphrase mỗi scenario thành 1–2 câu tự nhiên và
   tạo `dataset.jsonl` 20–30 rows.

## 5. AI Support Log cho bước này

- AI đã: đọc corpus/slide, trích vị trí nguồn và lập candidate pool để giảm công sức
  rà soát.
- AI chưa được: chốt dimension, chọn combination, gắn nhãn output, đặt threshold hay
  quyết định verdict.
- Human cần ghi: những ID đã Keep/Rewrite/Reject và lý do cho các thay đổi quan trọng.
