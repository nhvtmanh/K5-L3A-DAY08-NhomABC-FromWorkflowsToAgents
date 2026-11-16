# Decision record

Quyết định dựa trên benchmark public của bốn shape, cùng 14 claim và năm seed `11,22,33,44,55` (70 trial mỗi shape). Shape chọn dưới đây được dùng cho cổng hidden; kết quả public chưa xác nhận ngưỡng hidden.

- Shape chọn: workflow
- Commit hash: 1fba04b9825b00a46b356b7fa6d58eb9a4db9352
- Run id dẫn chứng: R-workflow-C-001-s11
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000
- Cost per success (mô phỏng, VND): ~ 27.86 VND
- Crash safety: 20/20, xem [crash.json](/src/reports/crash.json)
- Secret leak / approval bypass: không ghi nhận trong 70 trial public của workflow (70/70 có reason=ok và qua evaluator kiểm trace/ledger); benchmark không xuất hai bộ đếm riêng, chưa có số liệu hidden.

## Vì sao shape này

Nhóm chọn workflow vì đây là kiến trúc ít tự chủ nhất đáp ứng toàn bộ bộ public trong thí nghiệm. Workflow, single và orchestrator cùng đạt pass rate 1.000, pass^5 1.000 và seed variance 0, nhưng workflow có cost/success thấp nhất: 27.8571 VND so với 29.1214 VND của single và 46.4286 VND của orchestrator. Workflow không gọi model, tính tiền bằng `compute_compensation` từ order và policy hiện hành, không dùng số ngày trễ trong ticket. Quote đầy đủ được truyền vào `durability.issue_refund`; host kiểm approval, trần theo đơn và idempotency. Số liệu tổng hợp lấy từ `by_shape.workflow` của [benchmark.json](../../src/reports/benchmark.json), không suy ra từ trial dẫn chứng riêng lẻ.

## Có đáng đổi lấy multi-agent không

Trên cùng corpus, seed, MockLLM, bảng giá, mốc policy `2026-11-15` và cơ chế SQLite mới cho từng trial, chưa có lợi ích độ đúng để bù chi phí thêm của single hoặc orchestrator. Swarm có cost/success 49.5670 VND, pass rate 69/70 (0.985714), pass^5 13/14 (0.928571), seed min–max 0.928571–1.000 và variance 0.0008163265. Trial `R-swarm-C-002-s55` trả `resolved` thay vì `denied`, phù hợp điểm yếu tham chiếu tin số ngày trễ trong ticket. Nhóm giữ workflow cho task hiện tại.

Nhóm sẽ cân nhắc đổi kiến trúc nếu corpus đại diện mới có nghiệp vụ cần điều phối linh hoạt hoặc điều tra độc lập, và phép đo cùng điều kiện cho thấy kiến trúc khác cải thiện độ đúng đủ để chấp nhận chi phí tăng. Mọi lựa chọn vẫn phải qua cổng approval, secret và crash; shape chọn phải đạt hidden pass rate ít nhất 0.75. Bảng benchmark so sánh các triển khai hiện tại, chưa tách riêng tác động topology khỏi số lượt gọi model/tool và logic điều phối; cần ablation để kết luận quan hệ nhân quả.

## Trace và bằng chứng

Workflow ghi các event theo nhánh chạy:

- `claim`: chỉ `found` và `has_order_id`.
- `lookup_order`: chỉ `visible` và `reason`.
- `quote`: số tiền, lý do, clause và các phần tính do code trả về.
- `refund_request`: quote đầy đủ gửi host; trace được ghi trước lời gọi host để còn bằng chứng nếu crash.
- `refund_result`: `ok`, `reason`, `conflict` từ host.

Không ghi ticket, nguyên claim/order, `parent_secret`, raw headers, số điện thoại, địa chỉ, tên hàng, ghi chú nội bộ hoặc principal vào trace. Việc chọn field trong code giúp tránh chuyển dữ liệu nhạy cảm vào log. `finish()` ghi trace cho mọi nhánh trả kết quả bình thường, đồng thời lấy refund và số audit committed từ ledger. `crash_at` được truyền vào host và `InjectedCrash` được phép truyền ra; kết nối vẫn đóng trong `finally`.

Trace tuân contract v1: file JSON của lần chạy hiện tại có `run_id` khớp `RunResult` và `events` là list. Evaluator quét trace cùng các file có tiền tố `run_id` trong cùng thư mục. Workflow không tạo debug dump riêng hay in dữ liệu claim/order ra stdout. Nếu bổ sung log ngoài phạm vi scanner, nhóm phải rà soát nơi ghi và quét các log đó bằng dữ liệu canary/PII kiểm thử; scanner hiện tại không đủ để chứng minh các đầu ra ngoài phạm vi của nó an toàn.

Bằng chứng hiện có là 70/70 trial workflow được evaluator đánh giá `ok`, toàn bộ test host và student đã chạy đạt 302/302, cùng crash report 20/20. Crash report chủ yếu kiểm host và một kịch bản swarm; test T11/T12 trong ma trận student kiểm retry và crash/resume trực tiếp trên từng shape nhóm viết. Không diễn giải crash report là 20 điểm crash riêng cho workflow.

## Giới hạn

MockLLM là bộ mô phỏng, không phải model sản xuất. Chi phí là VND mô phỏng theo cấu hình, không phải hóa đơn API; latency là `unavailable`. Mean steps đếm event trace, phụ thuộc cách ghi log của từng shape, nên không dùng riêng số steps để kết luận kiến trúc nào nhanh hơn.

Public benchmark chỉ gồm 14 claim và năm seed. Workflow không gọi model nên variance bằng 0 trong phép đo này không chứng minh khả năng xử lý mọi claim mới. Chưa có kết quả hidden 40 claim × 5 seed; chưa xác nhận ngưỡng pass rate 0.75 hoặc hai bộ đếm leak/bypass trên hidden. Không sửa tay JSON kết quả.
