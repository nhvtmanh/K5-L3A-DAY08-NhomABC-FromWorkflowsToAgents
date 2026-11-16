# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: NhomABC
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`): `baa3103`

## 2. Mục tiêu và cách tiếp cận

Nhóm hiểu bài toán thế nào, chia việc ra sao, thứ tự làm bốn shape.

Nhóm triển khai cùng một quy trình xử lý claim hoàn phí vận chuyển qua bốn shape. Mục tiêu là chọn kiến trúc ít tự chủ nhất nhưng vẫn đạt đúng nghiệp vụ, đồng thời giữ approval, idempotency, crash safety và trace sạch. Nhóm làm theo thứ tự workflow, single, orchestrator; swarm có sẵn dùng làm đối chứng.

## 3. Giải pháp

Mô tả ba shape nhóm viết (workflow, single, orchestrator): mỗi shape đọc gì, quyết định gì, gọi host ra sao. Chỉ rõ ranh giới code / model (tham khảo [docs/architecture.md](../../docs/architecture.md)), cách handoff được sanitize và trace ghi những event nào.

Workflow là pipeline Python cố định: đọc claim qua `get_claim_view`, kiểm tra order bằng `lookup_order`, tính quote bằng `compute_compensation`, rồi gọi host `durability.issue_refund`. Single dùng vòng ReAct tối đa 8 bước; model chỉ chọn read tool, còn code và host quyết định số tiền và ghi refund. Orchestrator tạo handoff bằng allowlist, chạy investigator read-only, nhận order/policy/quote đã được giới hạn dữ liệu rồi mới gọi host.

Không shape nào ghi trực tiếp database. Quote truyền vào host là quote đầy đủ để host tự kiểm approval, per-order cap và idempotency. Trace chỉ ghi các event đã sanitize như claim metadata, visibility, quote và kết quả host; không ghi ticket, claim/order raw, secret, header, số điện thoại, địa chỉ, tên hàng hoặc internal note.

## 4. Kết quả

Bảng so sánh 4 shape trên bộ public (từ `src/reports/benchmark.json`): pass rate, pass^5, seed min–max, variance, cost/success, mean/p95 steps. Kèm crash safety (`src/reports/crash.json`) và, nếu có, kết quả tự kiểm trên `student_drop/`.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND) | Mean/P95 steps |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 27.857 | 4.07 / 5 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 29.121 | 7.71 / 9 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 46.429 | 5.00 / 6 |
| swarm | 0.985714 | 0.928571 | 0.928571–1.000 | 0.000816 | 49.567 | 2.80 / 3 |

Crash safety đạt `20/20` trong `src/reports/crash.json`; toàn bộ host và student test đạt `302 passed`. Nhóm chọn workflow vì cùng độ đúng public với single/orchestrator nhưng có cost/success thấp nhất và không phụ thuộc seed. Chưa có hidden self-check nên chưa khẳng định ngưỡng hidden.

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

Lỗi gặp phải (kèm lệnh, output hoặc ảnh chụp) và cách nhóm xử lý.

Khó khăn chính là phải phân biệt quote đầy đủ với số tiền net sau khi trừ refund cũ. Nhóm dùng `lookup_refund_history` chỉ cho mục đích đọc và vẫn truyền full quote vào host để tránh trừ hai lần. Crash được kiểm tra bằng `python -m lab8.crash_test --count 20 --out reports/crash.json`; benchmark được tái tạo bằng lệnh trong research card.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`. Nêu thêm giới hạn của nhóm và điều kiện làm kết luận thay đổi.

MockLLM và dữ liệu public nhỏ nên chưa phản ánh model production, latency thật hoặc claim mới. Kết luận có thể thay đổi nếu task cần điều phối linh hoạt, investigator độc lập hoặc hidden corpus làm workflow không đạt ngưỡng 0.75. Mọi shape vẫn phải giữ cổng host approval, secret và crash.

## 8. Tài liệu tham khảo

Tài liệu chính của lab: `README.md`, `docs/business_rules.md`, `docs/contracts.md`, `docs/metrics.md` và output `src/reports/benchmark.json`, `src/reports/crash.json`.
