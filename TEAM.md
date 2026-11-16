# Team

## Thông tin nhóm

- Tên nhóm: NhomABC
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-NhomABC-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/nhvtmanh/K5-L3A-DAY08-NhomABC-FromWorkflowsToAgents

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lê Hoàng Anh | 2A202603691 | lehoaganh2910@gmail.com | hoanganh2910 | Benchmark và phân tích kết quả |
|   2 | Điền họ tên | Điền MSSV | Điền email | Điền GitHub | Kiểm thử độ bền, bảo mật và submission |
|   3 | Phan Văn Cường | 2A202603669 | 26ai.cuongpv2@vinuni.edu.vn | pcuongggg333 | Nghiên cứu, ablation và báo cáo |

### Phân công công việc

| Người | Phạm vi và việc cụ thể | Đầu ra / điều kiện hoàn thành |
| --- | --- | --- |
| Thành viên 1 — Benchmark và phân tích | Từ `src/`, chạy benchmark 4 shape × 5 seed trên public claims. Đọc `reports/benchmark.json`; so sánh pass rate, pass^5, seed min–max/variance, cost per success, mean/p95 steps. Dựa trên số liệu và kiểm thử của Thành viên 2, chọn shape và giải thích điều kiện có thể làm đổi quyết định. Không sửa `lab8/metrics.py`. | Tạo `src/reports/benchmark.json`; điền các dòng số liệu trong `report/team/decision_adr.md` gồm shape chọn, commit hash, run ID, metrics, crash safety và bằng chứng secret/approval. Ghi một test regression liên quan benchmark/đầu ra nếu phát hiện thiếu coverage. |
| Thành viên 2 — Độ bền, bảo mật và submission | Kiểm tra T11 retry cùng claim và T12 crash/resume trên cả ba shape nhóm viết; kiểm tra approval đúng claim, handoff chỉ có tool allowlist, trace/stdout không chứa secret hoặc dữ liệu thô. Chạy student tests, host tests, crash suite; nếu giảng viên đã phát `student_drop/`, chạy lệnh self-check trong `src/README.md`. Sau khi các báo cáo hoàn tất, chạy `lab8.check_submission` và chuyển lại mọi FAIL cho người phụ trách. | Xác nhận `python -m pytest -q -m student -o addopts=`, `python -m pytest -q` và `python -m lab8.crash_test --count 20 --out reports/crash.json`; crash phải `20/20`. Ghi lại kết quả hidden self-check nếu có. Thêm/sửa test hồi quy phù hợp với crash, retry hoặc handoff nếu coverage còn thiếu. |
| Thành viên 3 — Nghiên cứu, ablation và báo cáo | Chọn một câu R1–R4 trong research card; tra nguồn, ghi claim và giới hạn nguồn. Đề xuất một hypothesis, cố định model/tools/seed/corpus/giá/evaluator, chỉ thay đổi một biến và chạy một ablation. Tổng hợp cách tiếp cận ba shape, kết quả từ hai thành viên còn lại, khó khăn, giới hạn và tài liệu tham khảo. | Hoàn thiện `report/team/research_card.md`, biên tập `report/team/group_report.md` (tối đa 5 trang ngoài phụ lục), tạo báo cáo cá nhân cho từng người theo mẫu `report/team/MSSV_HoTen.md`. Thêm/sửa test regression liên quan trace hoặc contract nếu coverage còn thiếu. |

### Thứ tự phối hợp và bàn giao

1. Cả nhóm đồng bộ nhánh `main`; mỗi người xác nhận `python -m pytest -q` chạy được trong `src/`.
2. Thành viên 2 xác nhận kết quả test/crash và chuyển số liệu, lỗi (nếu có) cho Thành viên 1 và 3.
3. Thành viên 1 chạy benchmark public, hoàn thiện ADR và gửi run ID/số liệu cho cả nhóm.
4. Thành viên 3 hoàn thiện research card/ablation và báo cáo nhóm dựa trên bằng chứng đã chạy, không tự điền số liệu ước đoán.
5. Thành viên 2 chạy `python -m lab8.check_submission` sau khi báo cáo hoàn tất; cả nhóm xử lý mọi `[FAIL]`.
6. Mỗi người tự cập nhật dòng đóng góp của mình bằng commit thật và test đã thêm/sửa; không ghi thay đóng góp hoặc kết quả của người khác.

Không sửa `src/lab8/metrics.py`, `src/lab8/durability.py`, `src/lab8/policy.py`, `src/config/` hoặc `src/data/`. Các báo cáo và lệnh cuối buổi phải bám theo [CHECKPOINTS.md](CHECKPOINTS.md) và [src/README.md](src/README.md).

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Thành viên 1 — điền tên | Benchmark và phân tích kết quả | | |
| Thành viên 2 — điền tên | Kiểm thử độ bền, bảo mật và submission | | |
| Thành viên 3 — Phan Văn Cường | Nghiên cứu, ablation và báo cáo | | |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
