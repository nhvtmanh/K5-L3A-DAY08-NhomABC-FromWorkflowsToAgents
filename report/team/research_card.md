# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R4 — Evaluation confounders |
| SOURCE | Agent evaluation literature, 2026; bằng chứng benchmark có kiểm soát trong lab và hướng dẫn R4 của đề bài |
| CLAIM | Muốn so sánh topology, cần giữ model, tools, seed, corpus, pricing và evaluator cố định; nếu không, chênh lệch metric có thể đến từ biến gây nhiễu thay vì kiến trúc. |
| BOUNDARY | Kết luận chỉ áp dụng cho MockLLM, 14 public claims, 5 seed, SQLite fresh-per-trial và policy snapshot `2026-11-15`; không suy rộng thành model production. |
| HYPOTHESIS | Khi giữ nguyên corpus, seed, giá và evaluator, workflow sẽ có pass rate tương đương single/orchestrator nhưng cost/success thấp hơn; swarm có thể có variance cao hơn do phụ thuộc seed. |
| METHOD | Giữ cố định MockLLM, read/write tools, seeds `11,22,33,44,55`, 14 claims, world/policy, pricing, fresh SQLite và evaluator. Biến thay đổi duy nhất trong benchmark là shape/topology. |
| FAILURE / METRIC | Nhiễu dự kiến: model call hoặc topology làm tăng cost và seed variance; đo pass rate, pass^5, seed variance, cost/success, mean/p95 steps, crash safety và trace leak/bypass. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `src/reports/benchmark.json`; 70 trial/shape, 4 shape, 5 seed.
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: đúng trên benchmark public. Workflow/single/orchestrator đều đạt pass rate và pass^5 `1.000`, variance `0.000000`; cost/success lần lượt khoảng `27.857`, `29.121`, `46.429` VND. Swarm đạt pass rate `0.985714`, pass^5 `0.928571`, variance `0.000816`, cost/success `49.567` VND. Đây là controlled comparison giữa shape, chưa phải ablation một biến nội bộ nên không kết luận quan hệ nhân quả chi tiết.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
