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
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Zhang et al., 2026, [Rethinking the Evaluation of Efficiency Methods for Multi-Agent Systems](https://aclanthology.org/2026.emnlp-main.798/), EMNLP. Loại bằng chứng: nghiên cứu benchmark chẩn đoán có kiểm soát, không phải báo cáo production. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Trong các phương pháp tối ưu hiệu suất MAS được khảo sát, lợi ích đo được có thể phụ thuộc prompt và topology ban đầu; vì vậy chưa thể quy mọi cải thiện cho thay đổi cấu trúc. Đây không phải kết luận rằng mọi hệ multi-agent đều kém hiệu quả. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Nguồn nghiên cứu các phương pháp hiệu suất MAS trong benchmark chẩn đoán với backbone, agent registry và runtime chung; kết luận giới hạn trong setup được khảo sát. Áp dụng tại lab chỉ là kiểm chứng nhỏ với MockLLM, 14 public claims, năm seed, SQLite mới mỗi trial và policy snapshot `2026-11-15`; không đại diện cho model production. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Đề xuất ablation trên orchestrator: bỏ duy nhất lượt đọc `lookup_policy` riêng trong handoff, vì `compute_compensation` vẫn tự đọc policy hiện hành. Dự đoán pass rate/pass^5 không đổi, cost/success giảm khoảng 9.29 VND (65 lượt tool × 10 VND / 70 trial pass), mean tool calls giảm khoảng 0.93. Đây là giả thuyết sau khi xem baseline, chưa có kết quả ablation. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Benchmark đã có giữ cùng MockLLM, tool registry/host, seeds `11,22,33,44,55`, corpus, world/policy, pricing và evaluator; mỗi trial dùng SQLite mới. Tuy nhiên các shape khác cả logic điều phối và số lượt model/tool nên chưa cô lập topology. Ablation đề xuất giữ nguyên orchestrator và mọi yếu tố trên, chỉ bật/tắt lượt `lookup_policy` riêng trong handoff; không sửa `compute_compensation`, host hay thước đo. Chạy baseline và biến thể thành hai report riêng, lưu lệnh và commit tương ứng. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: bỏ một tool tưởng dư thừa nhưng làm mất dữ liệu cần thiết hoặc thay đổi quyết định. So sánh từng cặp claim/seed về status, proposal, ledger và audit qua evaluator; đo pass rate, pass^5, seed variance, cost/success và tool calls. Kiểm tra trace để không có leak và host không bị bypass; không coi các trường hợp đó đã được đo bằng bộ đếm riêng nếu report không xuất bộ đếm. Mean/p95 steps chỉ phản ánh số event trace, không phải latency. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `src/reports/benchmark.json`; 70 trial/shape, 4 shape, 5 seed.
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: chưa kết luận về hypothesis ablation ở trên vì mới có baseline, chưa chạy biến thể. Benchmark hiện có cho thấy workflow/single/orchestrator đều đạt pass rate và pass^5 `1.000`, variance `0.000000`; cost/success lần lượt khoảng `27.857`, `29.121`, `46.429` VND. Swarm đạt pass rate `0.985714`, pass^5 `0.928571`, variance `0.000816`, cost/success `49.567` VND. Đây là so sánh các triển khai, chưa phải ablation một biến nội bộ nên không kết luận chênh lệch chỉ do topology.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
