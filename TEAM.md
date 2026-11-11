# Team

## Thông tin nhóm

- Tên nhóm: BLG
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-BLG-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit tích hợp gần nhất: `https://github.com/dinhnam269/K5-L3B-DAY03-BLG-ResearchAgentToolEval`, nhánh `main`, commit `f0ac9c5` (đã đồng bộ với `dev-DinhNam`)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Cao Minh Quang | 2A202603906 | cquang2k5@gmail.com | quang011105 | CP1–CP3 (Setup, Baseline v0, Tối ưu v1–v3, Tool mới `hackernews` & Unit Test) |
|   2 | Cao Phạm Tân Khải | 2A202603883 | cptkhai@gmail.com | capkhai | CP4 (thiết kế 10 eval case nhóm, chạy eval và cập nhật báo cáo/bằng chứng) |
|   3 | Nguyễn Đình Nam | 2A202603797 | dinhnam269@gmail.com | dinhnam269 | CP5 (dashboard HTML xem kết quả eval, A1/A3 và hướng dẫn chạy UI) |

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

## CaoPhamTanKhai-2A202603883

### Phần việc phụ trách

- Phụ trách **CP4 — thiết kế và chạy bộ eval nhóm**.
- Phối hợp kiểm tra contract tool, cập nhật version log và báo cáo nhóm.

### Đóng góp cụ thể

- Viết 10 eval case gồm 5 single-turn và 5 multi-turn, có case kiểm tra routing tới tool `hackernews`.
- Chạy group eval bằng Ollama `qwen2.5:3b`, tinh chỉnh phần kỳ vọng và đạt 10/10 PASS (`provider_error_cases: 0`).
- Cập nhật `version_log.csv` và các bảng B1, B3, B5a, B6 trong báo cáo nhóm.

### Bằng chứng

- Báo cáo cá nhân: `report/team/2A202603883_CaoPhamTanKhai.md`
- Eval: `starter_v0/data/eval_group.json`, `starter_v0/runs/v3_B_group_ollama_20261110T231457884672.json`
- Commit CP4: `ce5e380` (`Hoan thanh cp4: viet 10 test case, chay pass 10/10`)

## NguyenDinhNam-2A202603797

### Phần việc phụ trách

- Phụ trách **CP5 — dashboard HTML trình bày kết quả evaluation**.
- Đóng góp nội dung giới thiệu agent, câu hỏi mẫu A3 và hướng dẫn chạy dashboard trong báo cáo nhóm.

### Đóng góp cụ thể

- Tạo `starter_v0/demo_cp5.html`, cho phép tải run JSON, xem metric, lọc/tìm test case và đối chiếu expected với actual.
- Dashboard chạy cục bộ, không gọi model và không truyền file run ra mạng; đây không phải giao diện chat live.
- CP5 còn thiếu triển khai public và transcript tối thiểu 3 lượt chat live; xem trạng thái cụ thể trong báo cáo cá nhân.

### Bằng chứng

- Báo cáo cá nhân: `report/team/2A202603797_NguyenDinhNam.md`
- Dashboard: `starter_v0/demo_cp5.html`
- Commit dashboard: `64181a2` (`Add CP5 evaluation demo`)
