# Team

## Thông tin nhóm

- Tên nhóm: BLG
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-BLG-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: `https://github.com/dinhnam269/K5-L3B-DAY03-BLG-ResearchAgentToolEval`, nhánh `main` (commit chốt điền sau khi hoàn tất CP4–CP5)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Cao Minh Quang | 2A202603906 | cquang2k5@gmail.com | quang011105 | CP1–CP3 (Setup, Baseline v0, Tối ưu v1–v3, Tool mới `hackernews` & Unit Test) |
|   2 |        |      |       |        |         |
|   3 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## CaoMinhQuang-2A202603906

### Phần việc phụ trách

- Phụ trách toàn bộ **CP1 (Setup & Baseline `v0`)**, **CP2 (Tối ưu `system_prompt.md` và `tools.yaml` qua `v1`–`v3`)**, và **CP3 (Xây dựng tool mới `hackernews` & viết unit test)**.

### Đóng góp cụ thể

- Cấu hình API key trong `starter_v0/.env` (không commit secret) và chuyển sang local model Ollama (`qwen2.5:3b`) để xử lý giới hạn quota 20 req/ngày của Gemini Free Tier.
- Chạy baseline `v0` (`0.40` — 8/20 PASS, `provider_error_cases: 0`), phân tích đủ 12 case FAIL vào bảng B2 của `report/team/group_report.md`.
- Thực hiện tối ưu 3 vòng có bằng chứng: `v1` (`system_prompt.md`, `0.45`), `v2` (`tools.yaml`, `0.70`), `v3` (`system_prompt.md`, `0.80` — 16/20 PASS), ghi `starter_v0/artifacts/version_log.csv` và bảng B1.
- Xây dựng tool mới `hackernews` (`starter_v0/tools/hackernews/tool.py`, `TOOL.md`), đăng ký trong `tools/__init__.py` & `artifacts/tools.yaml`, viết 3 unit test offline trong `tests/test_tools_todo.py` (`pytest` đạt `70 passed, 14 skipped, 0 failed`) và ghi bảng B5a.

### Bằng chứng

- Commit trên nhánh `main`: `ca8295d` (`Complete CP1-CP3: v0-v3 eval optimization (ollama qwen2.5:3b) and hackernews tool with tests`)
- Run JSON (`provider_error_cases == 0`): `starter_v0/runs/v0_B_base_ollama_20261110T184359142341.json`, `v1_B_base_ollama_20261110T185037706863.json`, `v2_B_base_ollama_20261110T191308230206.json`, `v3_B_base_ollama_20261110T192354388698.json`
- Báo cáo cá nhân: `report/team/2A202603906_CaoMinhQuang.md`

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
