# Báo cáo cá nhân — 2A202603883_CaoPhamTanKhai

## 1. Thông tin thành viên

- Họ tên: Cao Phạm Tân Khải
- MSSV: 2A202603883
- Email: cptkhai@gmail.com

## 2. Phần việc phụ trách

- Phụ trách **Checkpoint 4 (CP4) — Thiết kế và chạy bộ Eval nhóm (`data/eval_group.json`)**.
- Phối hợp kiểm tra đồng bộ schema (`test_tool_contract.py`), cập nhật `artifacts/version_log.csv` và hoàn thiện bảng B1, B3, B5a cùng phần tổng hợp trong `report/team/group_report.md`.

## 3. Đóng góp cụ thể

- Thiết kế và viết đúng **10 test cases** trong `starter_v0/data/eval_group.json` gồm **5 single-turn cases (`G01`–`G05`)** và **5 multi-turn cases (`GM01`–`GM05`)**, bao phủ đủ 6 nhóm lỗi (`wrong_tool`, `wrong_arg_value`, `wrong_boundary`, `unnecessary_tool`, `out_of_scope`, `missing_info`):
  - Kiểm tra điều hướng và trích xuất tham số cho **tool mới của nhóm (`hackernews`)** ở cả single-turn (`G01_hackernews_topic_routing`, `G02_hackernews_latest_limit_args`) và multi-turn đổi nguồn từ Twitter sang Hacker News (`GM02_switch_twitter_to_hackernews`).
  - Kiểm tra các tình huống chưa được phủ trong `eval_base.json`: mốc thời gian `timeframe="month"` (`G03`), từ chối dịch thuật/ngữ pháp ngoài phạm vi (`G04`), câu hỏi meta về vai trò trợ lý (`G05`), luồng gửi Telegram sau khi người dùng đã xác nhận `confirmed=true` (`GM01`), sửa lại URL ở lượt hội thoại sau (`GM03`), đổi chủ đề tìm kiếm Twitter kèm `limit` (`GM04`), và bổ sung tên tài khoản sau khi được hỏi lại (`GM05`).
- Thiết lập môi trường chạy local model `qwen2.5:3b` qua Ollama, chạy đánh giá `--suite group`, phân tích log lỗi từ `runs/` và tinh chỉnh tập con tham số kỳ vọng (`expect.tool_calls[].args`) đúng quy ước chấm `compare_subset` để đạt **10/10 PASS (`case_accuracy: 1.0`, `provider_error_cases: 0`)**.
- Chuẩn hóa lại định dạng CSV của `starter_v0/artifacts/version_log.csv` (bổ sung dòng `v3-group`) và cập nhật đầy đủ bảng B1, B3, B5a, B6 trong `report/team/group_report.md`.

## 4. Bằng chứng

- **File/commit/PR:**
  - Bộ test case nhóm: `starter_v0/data/eval_group.json`
  - Kết quả chạy eval nhóm (10/10 PASS): `starter_v0/runs/v3_B_group_ollama_20261110T231457884672.json`
  - Log phiên bản: `starter_v0/artifacts/version_log.csv` (`v3-group`, artifact `v3+p3ddd6af1ce1d+tacc71cc37f0f`)
  - Báo cáo nhóm: `report/team/group_report.md` (Mục B1, B3, B5a, B6)
  - Commit message: `Hoan thanh cp4: viet 10 test case, chay pass 10/10`
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Công cụ sử dụng: Antigravity AI Assistant, Ollama (`qwen2.5:3b`), `pytest`.
  - Cách tự kiểm tra kết quả:
    1. Chạy `pytest starter_v0/tests` xác nhận **70 passed, 0 failed** (đảm bảo `test_tool_contract.py` kiểm tra toàn bộ tool trong `eval_group.json` đều đã khai báo hợp lệ trong `tools.yaml` và `tools/__init__.py`).
    2. Chạy `python run_eval.py --provider ollama --model qwen2.5:3b --version v3 --suite group --eval-cases data/eval_group.json` và đối chiếu trực tiếp file log `starter_v0/runs/v3_B_group_ollama_20261110T231457884672.json`: kiểm tra `total_cases == 10`, `measured_cases == 10`, `provider_error_cases == 0`, `passed_cases == 10` (`case_accuracy == 1.0`).

## 5. Tự đánh giá

- Hoàn thành đầy đủ nhiệm vụ ở Checkpoint 4 và phần báo cáo liên quan, đảm bảo đầy đủ bằng chứng đẩy lên repo để thành viên hoàn thiện nốt CP5
- Hiểu rõ sự khác biệt giữa kiểm tra tập con tham số (`compare_subset` trong `expect.tool_calls`) và kiểm tra `no_tool: true` cho các trường hợp ngoài phạm vi hoặc câu hỏi meta.
- Phân biệt được ranh giới giữa đánh giá hành vi điều hướng của model (`run_eval.py`) và kiểm thử đơn vị cho logic bên trong code của tool (`pytest`), cũng như cách chẩn đoán và xử lý lỗi kết nối provider (`provider_error`) trên môi trường thực tế.
