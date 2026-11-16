# Báo cáo cá nhân — Phan Văn Cường

## 1. Thông tin thành viên

- Họ tên: Phan Văn Cường
- MSSV: 2A202603669
- Email: 26ai.cuongpv2@vinuni.edu.vn
- GitHub: pcuongggg333

## 2. Phần việc phụ trách

- Phụ trách nghiên cứu, ablation và tổng hợp báo cáo theo phân công trong `TEAM.md`.
- Chọn câu hỏi R4 — Evaluation confounders trong research card.
- Xác định các biến cần cố định khi so sánh topology: MockLLM, tools, seed, corpus, pricing, world/policy, SQLite fresh-per-trial và evaluator.
- Tổng hợp kết quả benchmark của workflow, single, orchestrator và swarm; biên tập research card và group report.
- Nêu giới hạn của kết quả, đặc biệt là giới hạn của MockLLM, public corpus và việc chưa có hidden self-check.

## 3. Đóng góp cụ thể

- Hoàn thiện `report/team/research_card.md` với claim rằng chênh lệch metric chỉ có thể quy cho topology khi các biến model, tools, seed, corpus, giá và evaluator được giữ cố định.
- Ghi hypothesis: workflow có thể đạt độ đúng tương đương single/orchestrator nhưng có cost/success thấp hơn; swarm có thể có variance cao hơn do phụ thuộc seed.
- Chuẩn hóa phương pháp benchmark với 14 public claims, năm seed `11,22,33,44,55`, bốn shape và SQLite fresh-per-trial.
- Phân tích kết quả: workflow, single và orchestrator đều đạt pass rate/pass^5 `1.000/1.000` và variance `0.000000`; swarm đạt pass rate `0.985714`, pass^5 `0.928571` và variance `0.000816`.
- Đối chiếu cost/success và hỗ trợ quyết định chọn workflow: workflow khoảng `27.857` VND, thấp hơn single `29.121`, orchestrator `46.429` và swarm `49.567`.
- Tổng hợp giới hạn: kết quả chỉ áp dụng cho MockLLM, 14 public claims và policy snapshot `2026-11-15`; latency chưa có số đo và chưa thể suy rộng thành model production.
- Biên tập các phần mục tiêu, kết quả, khó khăn, hạn chế và tài liệu tham khảo trong `report/team/group_report.md`.

## 4. Bằng chứng

- Lệnh benchmark được ghi trong research card:
  `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`.
- Kết quả benchmark được lấy từ `src/reports/benchmark.json`, gồm 70 trial cho mỗi shape.
- Crash safety của nhóm đạt `20/20` trong `src/reports/crash.json`.
- Student và host test đạt tổng cộng `302 passed` theo group report.
- Các artifact báo cáo đã cập nhật: `report/team/research_card.md` và `report/team/group_report.md`.

## 5. Công cụ AI đã dùng

- Dùng Copilot trong VS Code để hỗ trợ đọc cấu trúc repo, đối chiếu phần việc trong `TEAM.md`, tổng hợp số liệu benchmark và biên tập báo cáo.
- Các số liệu trong báo cáo được đối chiếu từ các file kết quả và báo cáo đã có trong repo, không tự tạo số liệu benchmark.
- Kết luận được giới hạn theo corpus, seed, model và evaluator đã nêu trong research card.

## 6. Tự đánh giá

Tôi đã hoàn thành phần nghiên cứu R4, mô tả phương pháp controlled comparison và tổng hợp bằng chứng cho quyết định chọn workflow. Qua việc đối chiếu các shape, tôi hiểu rõ rằng việc so sánh multi-agent cần kiểm soát các biến gây nhiễu; nếu không, chênh lệch cost hoặc pass rate chưa đủ để kết luận nguyên nhân là topology. Hạn chế còn lại là ablation hiện mới so sánh các shape triển khai trong cùng benchmark, chưa tách được hoàn toàn tác động của topology khỏi số lượt gọi model/tool và logic điều phối. Kết quả cũng chưa thay thế cho hidden evaluation hoặc kiểm chứng trên model production.
