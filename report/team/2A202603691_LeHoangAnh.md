# Báo cáo cá nhân — Lê Hoàng Anh

## 1. Thông tin thành viên

- Họ tên: Lê Hoàng Anh
- MSSV: 2A202603691
- Email: Chưa điền
- GitHub: Chưa điền

## 2. Phần việc phụ trách

- CP1: thiết lập môi trường Python 3.13.3, chạy smoke test và đọc contract của lab.
- CP2: triển khai ba shape nhóm viết: workflow, single và orchestrator.
- Tích hợp: xử lý merge conflict giữa `main` và `origin/main` ở `single.py` và `workflow.py`.
- CP4: chạy crash suite 20 điểm.
- Vai trò được phân công cho phần còn lại theo `TEAM.md`: benchmark và phân tích kết quả. Phần benchmark CP5 chưa hoàn thành tại thời điểm viết báo cáo này.

## 3. Đóng góp cụ thể

- Triển khai luồng xử lý claim cho ba shape, giữ việc tính quote và ghi refund ở host; truyền quote đầy đủ vào `issue_refund`.
- Với single, giới hạn ReAct ở 8 bước và bật `worker=True` để worker chỉ gọi được công cụ đọc.
- Giữ trace theo hướng không ghi raw claim/order; truyền `crash_at` xuống `issue_refund` để lỗi crash được kiểm tra và không bị nuốt.
- Giải quyết xung đột merge bằng cách ghép logic CP2 với thay đổi read-only từ nhánh remote, sau đó chạy lại test.
- Commit liên quan: `5f381dd` (Completed CP1 and CP2); merge commit: `0070554` (Merge origin/main into main).

## 4. Bằng chứng

- Student matrix: `python -m pytest -q -m student -o addopts=` — **248 passed, 54 deselected**.
- Host tests: `python -m pytest -q` — **54 passed, 248 deselected**.
- Crash suite: `python -m lab8.crash_test --count 20 --out reports/crash.json` — **crash_safety 20/20**.
- Các file shape liên quan: `src/lab8/shapes/workflow.py`, `src/lab8/shapes/single.py`, `src/lab8/shapes/orchestrator.py`.
- Các kết quả trên là bằng chứng kiểm thử, không có run ID được in ra bởi những lệnh đã chạy.
- Chưa thêm hoặc sửa test trong các đóng góp được ghi nhận ở trên; cần bổ sung một test hồi quy có ý nghĩa và cập nhật bảng đóng góp trước khi nộp nếu yêu cầu của nhóm/grader vẫn áp dụng.

## 5. Công cụ AI đã dùng

- Dùng Copilot trong VS Code để hỗ trợ đọc cấu trúc project, giải thích contract, triển khai và rà soát code shape, phân tích conflict và soạn báo cáo.
- Tự kiểm tra kết quả bằng student tests, host tests và crash suite; không dùng AI để tạo số liệu benchmark. Benchmark CP5 chưa chạy.

## 6. Tự đánh giá

Đã hoàn thành phần triển khai CP2 và tích hợp merge; các kiểm thử hiện có cùng crash suite đều đạt. Qua phần này, tôi hiểu rõ hơn vì sao refund phải được host kiểm soát, vì sao cần truyền quote đầy đủ và vì sao trace phải được sanitize. Phần cần hoàn tất tiếp theo là chạy benchmark CP5, dùng số liệu thực để điền ADR và báo cáo, đồng thời bổ sung test hồi quy phù hợp với đóng góp của mình.
