# Báo cáo cá nhân — CaoMinhQuang-2A202603906

## 1. Thông tin thành viên

- Họ tên: Cao Minh Quang
- MSSV: 2A202603906
- Email: cquang2k5@gmail.com

## 2. Phần việc phụ trách

Phụ trách hoàn thiện phần kỹ thuật và bằng chứng cho **3 checkpoint đầu (CP1, CP2, CP3)** rồi bàn giao code trên nhánh `main` để 2 thành viên còn lại tiếp tục CP4 và CP5:

- **CP1:** Cấu hình môi trường, kiểm tra API key các tool, khắc phục sự cố quota provider và chạy baseline `v0` kèm phân tích lỗi.
- **CP2:** Thực hiện vòng lặp tối ưu dựa trên bằng chứng qua 3 phiên bản `v1 → v2 → v3` trên `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, ghi log vào `version_log.csv` và bảng B1/B2 trong báo cáo nhóm.
- **CP3:** Xây dựng tool mới `hackernews`, đăng ký vào hệ thống, viết 3 unit test offline trong `tests/test_tools_todo.py` và giữ toàn bộ `pytest` xanh (0 failed).

## 3. Đóng góp cụ thể

- **Thiết lập & Baseline `v0` (CP1):**
  - Cấu hình `TAVILY_API_KEY`, `FIRECRAWL_API_KEY`, `RAPIDAPI_KEY` vào `starter_v0/.env` (không commit secret lên Git).
  - Khắc phục sự cố khi thử nghiệm Gemini API (`gemini-3.8-flash` lỗi `503 UNAVAILABLE` và `gemini-3.6-flash` chạm giới hạn Free Tier 20 requests/ngày `429 RESOURCE_EXHAUSTED`) bằng cách chuyển sang chạy local qua **Ollama (`qwen2.5:3b`)** để đủ điều kiện chạy nhiều vòng eval lặp lại trên cùng một model.
  - Chạy baseline `v0` (`case_accuracy = 0.40` — 8/20 PASS, `tool_routing_accuracy = 0.55`, `provider_error_cases = 0`), đọc run JSON và phân loại toàn bộ 12 case FAIL vào bảng **B2** của `report/team/group_report.md`.
- **Tối ưu Prompt & Tool Declaration `v1 → v3` (CP2):**
  - **`v1` (`system_prompt.md`):** Gỡ bỏ các chỉ dẫn bẫy của starter (ép đoán bừa handle/URL, tự ý gửi `send`, ép chọn 1 tool), bổ sung rule routing, map handle (`sama`, `elonmusk`, `karpathy`), quy tắc out-of-scope/meta và cho phép gọi tool song song → `case_accuracy` tăng từ `0.40` lên **`0.45`** (9/20), `tool_routing_accuracy` tăng lên **`0.65`**.
  - **`v2` (`tools.yaml`):** Viết lại `description` ngắn gọn theo cấu trúc *DÙNG KHI / KHÔNG DÙNG KHI* phù hợp cho model nhỏ 3B trên CPU (tránh quá tải context 4096 gây timeout), chuẩn hóa convention tham số (`lookup.query` chỉ giữ từ khóa ngắn, `topic` chỉ nhận `general|news`, `clarify` dùng tool call thay vì text suông) → `case_accuracy` nhảy lên **`0.70`** (14/20), `multiturn_accuracy` đạt **`0.8333`** (5/6).
  - **`v3` (`system_prompt.md`):** Siết rule nhận diện `http(s)://` → bắt buộc gọi `fetch`, cấm gọi `clarify` với câu hỏi coding/toán, thêm ví dụ gọi tool `clarify` và truyền `limit` → `case_accuracy` đạt **`0.80`** (16/20), `tool_routing_accuracy` đạt **`0.85`**, `argument_accuracy` đạt **`0.80`**.
- **Tool mới `hackernews` & Unit Test (CP3):**
  - Tự xây dựng tool `hackernews` (`starter_v0/tools/hackernews/tool.py` + `TOOL.md`) tìm kiếm bài thảo luận trên Hacker News qua Algolia HN Search API (`hn.algolia.com`, không cần API key), hỗ trợ `sort_by=relevance|date`, chuẩn hóa/clamp `limit` (`1..20`), fallback URL sang thread HN khi `url` gốc bị `None`, và bắt ngoại lệ trả về error dict qua `_shared.err`.
  - Đăng ký vào `starter_v0/tools/__init__.py` (`TOOL_FUNCTIONS`) và `starter_v0/artifacts/tools.yaml`.
  - Viết 3 unit test offline (mock HTTP bằng `fake_http`) trong `starter_v0/tests/test_tools_todo.py`: test happy path (`search_by_date` & fallback `hn_url`), test input xấu từ model (`query` rỗng, `sort_by` ngoài enum, `limit` dạng chuỗi `"3"`), và test nhánh lỗi HTTP 503 trả về error dict.

## 4. Bằng chứng

- **File/commit/PR:**
  - Commit trên nhánh `main` của repo `K5-L3B-DAY03-BLG-ResearchAgentToolEval`: `ca8295d` (`Complete CP1-CP3: v0-v3 eval optimization (ollama qwen2.5:3b) and hackernews tool with tests`).
  - Các file run hợp lệ (`provider_error_cases == 0`, `measured_cases == 20`):
    - `starter_v0/runs/v0_B_base_ollama_20261110T184359142341.json` (`0.40`)
    - `starter_v0/runs/v1_B_base_ollama_20261110T185037706863.json` (`0.45`)
    - `starter_v0/runs/v2_B_base_ollama_20261110T191308230206.json` (`0.70`)
    - `starter_v0/runs/v3_B_base_ollama_20261110T192354388698.json` (`0.80`)
  - Artifacts & Code: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/artifacts/version_log.csv`, `starter_v0/tools/hackernews/tool.py`, `starter_v0/tools/hackernews/TOOL.md`, `starter_v0/tools/__init__.py`, `starter_v0/tests/test_tools_todo.py`, `report/team/group_report.md`.
  - Kết quả kiểm thử: `pytest` chạy từ `starter_v0/` đạt **`70 passed, 14 skipped, 0 failed`** (gồm 60 contract tests, 7 example tests, và 3 unit tests của `hackernews`).
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Sử dụng trợ lý AI coding (Antigravity) hỗ trợ tra cứu hướng dẫn, đọc và phân tích log lỗi trong `runs/*.json`, đề xuất giả thuyết cho từng vòng `v1`–`v3` phù hợp với model 3B, viết khung code tool `hackernews` và các unit test.
  - Cách tự kiểm tra kết quả: tự chạy `scripts/preflight_provider.py`, smoke test từng tool với dữ liệu thật (`lookup`, `fetch`, `timeline`, `hackernews`), chạy `run_eval.py` kiểm tra `provider_error_cases == 0`, đối chiếu `prompt_hash`/`tools_hash` giữa `version_log.csv` và run JSON, chạy `pytest` xác nhận `0 failed`, và rà soát `git diff --cached` trước khi push để đảm bảo không lộ `.env`/API key.

## 5. Tự đánh giá

- Đã hoàn thành đầy đủ, đúng chuẩn 3 checkpoint đầu (CP1–CP3) với bằng chứng thật và đẩy sạch lên nhánh `main` để các thành viên khác kế thừa làm CP4–CP5.
- Nắm rõ cơ chế hoạt động và lý do cải thiện từ `0.40` lên `0.80` qua `v0–v3`, phân biệt được lỗi routing/args của model (eval) với lỗi xử lý biên trong code tool (unit test), đồng thời nhận diện rõ giới hạn của model nhỏ 3B ở 4 case còn sót (`R10`, `R11`, `R12`, `M03`).

