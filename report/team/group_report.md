# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: BLG
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: `ollama` (`qwen2.5:3b`)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

BLG Research Agent hỗ trợ tìm kiếm và tổng hợp thông tin từ web, Twitter/X, Hacker News và arXiv; đồng thời có thể đọc URL và tra cứu chính sách nội bộ. Agent có thể trình bày kết quả thành digest và chỉ gửi bản tin lên Telegram sau khi người dùng xác nhận.

**Cách chạy UI:**

- **UI Chat live với Agent (Streamlit — `starter_v0/app.py`):**
  1. Cài dependency (đã khai báo `streamlit>=1.35.0` trong `starter_v0/requirements.txt`): `pip install -r requirements.txt`.
  2. Chạy từ thư mục `starter_v0/`: `streamlit run app.py` → mở `http://localhost:8501` (chọn provider `ollama`, model `qwen2.5:3b` hoặc provider cloud có key trong `.env`). Giao diện hiển thị rõ từng tool call, tham số, kết quả và cảnh báo/lỗi tool (không che lỗi) và tự lưu transcript vào `starter_v0/transcripts/`.
- **Dashboard xem kết quả Eval (`starter_v0/demo_cp5.html`):**
  - Từ `starter_v0/`, chạy `python -m http.server 8000`, mở `http://localhost:8000/demo_cp5.html` rồi nạp file `runs/*.json` để xem metric và đối chiếu expected/actual.

**Link dùng thử (deploy):**

- Local UI: `http://localhost:8501` (khi demo/showdown chạy `cloudflared tunnel --url http://localhost:8501` để cấp URL `https://<random>.trycloudflare.com` tạm thời cho team khác truy cập; chưa deploy server public cố định vì agent dùng model local Ollama trên máy).

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin (`text`/`choice`) hoặc xin xác nhận (`yes_no`) | không |
| `timeline` | Lấy các tweet gần đây của một tài khoản Twitter/X cụ thể | không |
| `social_search` | Tìm tweet theo từ khóa/chủ đề (`Latest` hoặc `Top`) | không |
| `lookup` | Tìm kiếm thông tin và tin tức trên web qua Tavily (`general`/`news`, lọc `timeframe`) | không |
| `fetch` | Đọc và trích xuất nội dung trực tiếp từ một URL cụ thể qua Firecrawl | không |
| `format` | Trình bày danh sách kết quả đã thu thập thành markdown digest | không |
| `send` | Gửi bản tin lên kênh Telegram (chỉ thực hiện khi `confirmed=true`) | không |
| `policy` | Tra cứu tài liệu chính sách nội bộ công ty (`company_policy/*.md`) | không |
| `papers` | Tìm bài báo khoa học trên arXiv | không |
| `paper_text` | Tải PDF và trích xuất nội dung text từ bài báo arXiv | không |
| `hackernews` | Tìm bài thảo luận công nghệ trên Hacker News qua Algolia HN API (`relevance`/`date`) | **có (CP3)** |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Tìm tin tức mới nhất về AI agents trên web, rồi tóm tắt 3 điểm chính kèm nguồn.
2. Tìm các bài thảo luận về Qwen trên Hacker News và cho biết bài nào được quan tâm nhất.
3. Đọc nội dung bài viết tại https://arxiv.org/abs/1706.03762 và tóm tắt ý tưởng chính.
4. Tìm các bài đăng gần đây của Sam Altman trên Twitter/X.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **Thay đổi trong `starter_v0/artifacts/system_prompt.md` (`v1`, `v3`):**
  - Gỡ bỏ các chỉ dẫn bẫy của starter (tự đoán handle `sama`/URL khi thiếu thông tin, tự ý `send` không hỏi lại, ép chỉ chọn 1 tool).
  - Thêm quy tắc routing rõ ràng: câu hỏi meta và ngoài phạm vi (toán, lập trình) trả lời/từ chối thẳng bằng text (không gọi tool hay `clarify`); thiếu handle/URL hoặc chưa xác nhận `send` bắt buộc gọi tool `clarify`; có `http(s)://` URL bắt buộc gọi `fetch`; cho phép gọi song song `lookup` + `social_search` khi user hỏi cả web và Twitter; ưu tiên chỉ dẫn đổi nguồn ở lượt hội thoại mới nhất.
  - Bổ sung bảng map handle (`Sam Altman` → `sama`, `Elon Musk` → `elonmusk`, `Andrej Karpathy` → `karpathy`) và nhắc truyền `limit` khi user nêu số lượng tweet.
- **Thay đổi trong `starter_v0/artifacts/tools.yaml` (`v2`):**
  - Viết lại toàn bộ `description` ngắn gọn theo mẫu **Dùng khi / Không dùng khi** để phù hợp context nhỏ của model 3B.
  - Chuẩn hóa convention tham số: `lookup.query` chỉ giữ từ khóa ngắn (không lặp `"news"`/`"today"`), `lookup.topic` chỉ nhận `general`/`news`, `social_search.search_type` phân biệt `Top`/`Latest`, `timeline.screenname` không có `@`, và `send` yêu cầu `confirmed=true` sau khi user xác nhận qua `clarify(response_type="yes_no")`.
- **Tool mới nhóm viết — `hackernews` (`starter_v0/tools/hackernews/`):**
  - Tìm các bài thảo luận công nghệ/AI trên Hacker News qua Algolia HN Search API (`hn.algolia.com`, không cần API key), hỗ trợ `sort_by` (`relevance`/`date`) và `limit` (clamp `1..20`).
  - Agent nên gọi `hackernews` khi người dùng hỏi rõ về bài viết/thảo luận trên Hacker News (không dùng thay cho `lookup` tin web chung hay `social_search` trên Twitter).

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi starter chưa tối ưu trước khi sửa (`ollama` / `qwen2.5:3b`) | — | 0.40 (8/20) | `starter_v0/runs/v0_B_base_ollama_20261110T184359142341.json` |
| v1 | `system_prompt.md` | Gỡ chỉ dẫn bẫy của starter + thêm rule routing, map handle và ranh giới out-of-scope/clarify | 0.40 (8/20) | 0.45 (9/20) | `starter_v0/runs/v1_B_base_ollama_20261110T185037706863.json` |
| v2 | `tools.yaml` | Viết lại description ngắn gọn (DÙNG KHI / KHÔNG DÙNG KHI) và quy ước tham số trong `tools.yaml` | 0.45 (9/20) | 0.70 (14/20) | `starter_v0/runs/v2_B_base_ollama_20261110T191308230206.json` |
| v3 | `system_prompt.md` | Siết rule `http(s)://` → `fetch`, cấm gọi `clarify` với coding/toán, thêm ví dụ gọi `clarify` và truyền `limit` | 0.70 (14/20) | 0.80 (16/20) | `starter_v0/runs/v3_B_base_ollama_20261110T192354388698.json` |
| v3-group | `tools.yaml` | Khai báo thêm tool mới `hackernews` trong `tools.yaml` và đo trên bộ eval nhóm 10 case (`eval_group.json`) | 0.80 (base) | 1.00 (10/10 group) | `starter_v0/runs/v3_B_group_ollama_20261110T231457884672.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON (`v0_B_base_ollama_20261110T184359142341.json`).

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R01_user_tweets_routing` | `wrong_tool` | `timeline(screenname="samaltman")` | `screenname: expected 'sama', got 'samaltman'` | Thêm bảng map tên người nổi tiếng sang handle Twitter (`Sam Altman` → `sama`, `Andrej Karpathy` → `karpathy`, `Elon Musk` → `elonmusk`) |
| `R03_web_news_routing` | `wrong_tool` | `papers(query="AI", sort_by="lastUpdatedDate", max_results=5)` | `missing tool call lookup; extra tool call papers` | Phân biệt rõ rule routing: tin tức web → `lookup(topic="news")`, chỉ dùng `papers` cho bài báo khoa học arXiv |
| `R06_timeframe_arg` | `wrong_arg_value` | `lookup(topic="tech", query="tin công nghệ trong tuần này", timeframe="week")` | `topic: expected 'news', got 'tech'` (API 400 Bad Request) | Ghi rõ enum `topic` chỉ nhận `general` hoặc `news`; `query` chỉ chứa từ khóa ngắn |
| `R08_out_of_scope` | `out_of_scope` | `clarify(question="giải giúp mình bài toán tích phân: nguyên hàm của x^2 là gì?")` | `expected no tool call` | Bổ sung rule từ chối thẳng không gọi tool với câu hỏi ngoài phạm vi research (toán, lập trình...) |
| `R10_missing_handle` | `missing_info` | `timeline(screenname="twitter")` | `missing tool call clarify; extra tool call timeline` | Gỡ chỉ dẫn ép đoán bừa trong `system_prompt.md`; bắt buộc gọi `clarify(response_type="text")` khi thiếu handle |
| `R11_missing_url` | `missing_info` | `lookup(query="bài viết", timeframe="day", topic="general")` | `missing tool call clarify; extra tool call lookup` | Gỡ chỉ dẫn ép đoán URL trong `system_prompt.md`; bắt buộc gọi `clarify(response_type="text")` khi nói "bài này" mà thiếu link |
| `R12_confirm_before_send` | `wrong_boundary` | `send(text="Đây là bản tin mới nhất từ nguồn tin cậy.", confirmed=true)` | `missing tool call clarify; extra tool call send` | Gỡ chỉ dẫn tự gửi trong `system_prompt.md`; yêu cầu gọi `clarify(response_type="yes_no")` xác nhận trước khi `send` |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `social_search(Latest, 3)` + `social_search(Top, 3)` | `missing tool call lookup; extra tool call social_search` | Gỡ chỉ dẫn ép chọn 1 tool trong `system_prompt.md`; hướng dẫn gọi song song `lookup` + `social_search` khi cần cả web và Twitter |
| `R14_out_of_scope_coding` | `out_of_scope` | `clarify(question="Viết giúp mình một hàm Python tính Fibonacci bằng recursion.")` | `expected no tool call` | Bổ sung rule từ chối thẳng không gọi tool với yêu cầu viết code ngoài phạm vi research |
| `M02_carryover_timeframe` | `wrong_arg_value` | `lookup(query="robotics today", timeframe="day")` | `query: expected 'robotics', got 'robotics today'; topic: expected 'news', got None` | Quy ước `lookup.query` chỉ giữ từ khóa chủ đề (`"robotics"`), giữ `topic="news"` khi user nói "vẫn là tin hôm nay" |
| `M03_correction_handle` | `wrong_arg_value` | `social_search(query="Andrej Karpathy", search_type="Latest", limit=3)` | `missing tool call timeline; extra tool call social_search` | Nhấn mạnh tweet *của một người cụ thể* → luôn dùng `timeline` + map handle (`Andrej Karpathy` → `karpathy`), không dùng `social_search` |
| `M06_switch_tool` | `wrong_tool` | `social_search(query="OpenAI", search_type="Latest", limit=5)` | `missing tool call lookup; extra tool call social_search` | Nhấn mạnh tuân theo chỉ dẫn đổi nguồn ở lượt mới nhất ("Bỏ Twitter, chuyển sang tìm trên web tin tức" → chuyển sang `lookup`) |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_hackernews_topic_routing` | Single-turn (`wrong_tool`): Hỏi thảo luận trên Hacker News → route tới tool mới `hackernews` (không dùng `lookup` hay `social_search`) | `hackernews(query="Rust")` | PASS |
| `G02_hackernews_latest_limit_args` | Single-turn (`wrong_arg_value`): Tìm bài "mới nhất" kèm số lượng trên Hacker News → trích đúng `sort_by="date"` và `limit=3` | `hackernews(query="LLM", sort_by="date", limit=3)` | PASS |
| `G03_web_news_month_timeframe` | Single-turn (`wrong_arg_value`): Cụm "trong tháng này" → gọi `lookup` với `topic="news"`, `timeframe="month"` (bộ base mới chỉ test `day` và `week`) | `lookup(query="AI", topic="news", timeframe="month")` | PASS |
| `G04_out_of_scope_translation` | Single-turn (`out_of_scope`): Yêu cầu dịch thuật/giải thích ngữ pháp ngoài phạm vi research → từ chối thẳng, không gọi `clarify` hay `lookup` | `no_tool: true` (`refuse`) | PASS |
| `G05_unnecessary_tool_greeting_meta` | Single-turn (`unnecessary_tool`): Câu hỏi meta về bản thân và vai trò của trợ lý → trả lời thẳng không gọi tool, tránh gọi nhầm `policy` hoặc `lookup` | `no_tool: true` (`answer_without_tool`) | PASS |
| `GM01_confirm_then_send_telegram` | Multi-turn (`wrong_boundary`): 3 turns — sau khi agent hỏi xác nhận và user đồng ý ở lượt cuối → gọi `send` với `confirmed=true` (kiểm tra subset `confirmed=true`) | `send(confirmed=true)` | PASS |
| `GM02_switch_twitter_to_hackernews` | Multi-turn (`wrong_tool`): 3 turns — đổi nguồn từ Twitter sang tool mới `hackernews` ở lượt cuối, giữ chủ đề `OpenAI` và truyền `limit=5` | `hackernews(query="OpenAI", limit=5)` | PASS |
| `GM03_correction_url_fetch` | Multi-turn (`wrong_arg_value`): 3 turns — user sửa lại URL ở lượt 2 → gọi `fetch` đúng URL mới của Anthropic, bỏ qua URL cũ ở lượt 1 | `fetch(url="https://www.anthropic.com/research")` | PASS |
| `GM04_correction_social_search_topic` | Multi-turn (`wrong_arg_value`): 3 turns — đổi chủ đề tìm kiếm trên Twitter từ `GPT-5` sang `Claude` và trích đúng `limit=5` ở lượt cuối | `social_search(query="Claude", limit=5)` | PASS |
| `GM05_clarify_then_fill_handle_sama` | Multi-turn (`missing_info`): 3 turns — lượt 1 thiếu tên người, sau khi được hỏi lại thì lượt 3 bổ sung Sam Altman và số lượng 5 → gọi `timeline(screenname="sama", limit=5)` | `timeline(screenname="sama", limit=5)` | PASS |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/v3_ollama_20261111T112155035914.transcript.json` (chạy `python chat.py --provider ollama --model qwen2.5:3b --version v3`).

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | *"Trên Hacker News đang bàn luận gì về Rust?"* | `hackernews(query="Rust", sort_by="relevance")` | `v3+p3ddd6af1ce1d+t061bc1144e3b` | Trả về 5 bài thảo luận thật từ Algolia HN kèm link, points và số comments |
| 2 | *"Tóm tắt 5 tweet mới nhất giúp mình"* (thiếu tên người) | `timeline(screenname="sama")` | `v3+p3ddd6af1ce1d+t061bc1144e3b` | Model 3B vẫn tự đoán mặc định `sama` thay vì gọi `clarify` (khớp lỗi quan sát ở `R10` trong `eval_base.json`) |
| 3 | *"Của Sam Altman nhé"* (bổ sung thông tin) | `timeline(screenname="sama")` | `v3+p3ddd6af1ce1d+t061bc1144e3b` | Lấy đúng 5 tweet mới nhất của `@sama` và tóm tắt có trích nguồn |
| 4 | *"Đăng bản tin này lên Telegram giúp mình"* | `send()` → bị guardrail trả `status="needs_confirmation"` | `v3+p3ddd6af1ce1d+t061bc1144e3b` | Guardrail code của `send` chặn không gửi và buộc model hỏi lại người dùng xác nhận trước khi gửi |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/hackernews/`) | `starter_v0/tools/hackernews/tool.py`, `TOOL.md`, `tools/__init__.py`, `artifacts/tools.yaml` | Tìm kiếm thảo luận công nghệ trên Hacker News qua Algolia API (không cần API key), hỗ trợ `sort_by=relevance|date` và `limit` | Clamp `limit` (1–20), fallback `sort_by` ngoài enum, bắt `ValueError`/`HTTPError` trả về error dict thay vì raise |
| Unit test tool mới (3 test) | `starter_v0/tests/test_tools_todo.py` (`pytest -v`: 70 passed, 14 skipped, 0 failed) | Pass cả 3 test: happy path (`search_by_date` + fallback `hn_url`), input xấu (query rỗng, enum sai, `limit` dạng chuỗi), và HTTP 503 trả error dict | Eval chỉ kiểm tra model có gọi đúng `hackernews(query=...)` hay không, không bắt được bug bên trong code tool (ví dụ quên truyền `hitsPerPage` hoặc crash khi `hit["url"]` là `None`); unit test bắt được ngay offline |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `starter_v0/requirements.txt` (`streamlit>=1.35.0`), `starter_v0/demo_cp5.html` | `streamlit run app.py` phục vụ HTTP 200 tại `http://localhost:8501`, chat live với agent qua `run_model_tool_loop` và lưu transcript | Hiển thị nguyên vẹn JSON kết quả và `st.error(...)` khi tool lỗi hoặc `st.warning` khi `needs_confirmation`, không che lỗi tool |

- **Tool unit tests (số test đã viết và ví dụ lỗi unit test bắt được nhưng eval không bắt được):**
  - **Số test đã viết cho tool mới (`hackernews`):** **3 unit tests** trong `starter_v0/tests/test_tools_todo.py` (kết hợp cùng **60 contract tests** trong `test_tool_contract.py` và **7 example tests** → tổng cộng **70 passed, 0 failed**):
    1. `test_hackernews_happy_path_maps_hits_and_sort_by_date`: kiểm tra `sort_by="date"` gọi đúng endpoint `https://hn.algolia.com/api/v1/search_by_date`, truyền đúng `params={"query": "agents", "tags": "story", "hitsPerPage": 2}` và ánh xạ dữ liệu trả về.
    2. `test_hackernews_bad_input_handles_empty_query_and_invalid_args`: kiểm tra input xấu từ model như `query="   "` (trả về `{"error": "ValueError"}` mà không gọi mạng), `sort_by="invalid_enum"` (tự fallback về `"relevance"`), và `limit="3"` dạng chuỗi (ép kiểu sang `int` `3`).
    3. `test_hackernews_http_error_returns_error_dict`: kiểm tra khi Algolia API trả về HTTP `503`, hàm bắt ngoại lệ và trả về `{"tool": "hackernews", "error": "HTTPError", ...}` thay vì làm crash vòng lặp agent.
  - **Ví dụ lỗi thực tế mà Unit Test bắt được nhưng Eval (`run_eval.py`) không bắt được:**
    - Trên Hacker News, các bài dạng *Ask HN* hoặc *Show HN* chỉ có nội dung thảo luận nội bộ nên trường `hit["url"]` từ Algolia API trả về giá trị `None`. Nếu trong `search_hackernews()` viết `hit.get("url", "").strip()`, khi gặp `url: null` (`None`) Python sẽ văng lỗi `AttributeError: 'NoneType' object has no attribute 'strip'`, hoặc nếu quên đổi endpoint sang `search_by_date` khi `sort_by="date"` thì kết quả trả về cho người dùng sẽ bị sắp xếp sai.
    - Trong khi đó, `run_eval.py` chỉ chấm trên `response.tool_calls` do model sinh ra (ví dụ thấy model gọi `hackernews(query="LLM", sort_by="date", limit=3)` là chấm **PASS** ngay) mà không kiểm tra `tool_results` có bị lỗi hay gọi sai URL API hay không. Unit test `test_hackernews_happy_path_maps_hits_and_sort_by_date` dùng `fake_http` giả lập `hit["url"] = None` và assert trực tiếp cả `calls[0]["url"]` lẫn fallback `result["items"][1]["url"] == "https://news.ycombinator.com/item?id=42002"`, nên bắt được lỗi này ngay lập tức.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

- **Hết quota & lỗi quá tải của Gemini API Free Tier:** Khi chạy thử với provider `gemini`, model mặc định `gemini-3.8-flash` gặp `503 UNAVAILABLE` (high demand), còn `gemini-3.6-flash` bị giới hạn Free Tier **20 requests/ngày** theo project (`429 RESOURCE_EXHAUSTED`, làm lần chạy `eval_base.json` thứ hai chỉ đo được 3/20 case). Nhóm xử lý bằng cách cài model local **Ollama (`qwen2.5:3b`)** để chạy toàn bộ `v0–v3` ổn định với `provider_error_cases == 0`.
- **Timeout trên CPU khi schema tool quá dài (`v2`):** Khi viết mô tả ở `tools.yaml` quá dài khiến `qwen2.5:3b` (context `4096` trên CPU) bị `ReadTimeout` tại case `R08_out_of_scope`. Nhóm rút gọn lại mô tả trong `tools.yaml` ngắn, súc tích (`55 passed` contract tests) thì chạy thông suốt toàn bộ 20 cases (`case_accuracy` tăng lên `0.70`, rồi `0.80` ở `v3`).
- **Giới hạn của model nhỏ 3B:** Ở `v3` vẫn còn 4/20 case chưa đạt (`R10` tự đoán `techcrunch`, `R11`/`R12` biết hỏi lại bằng text nhưng không phát tool call `clarify`, `M03` thiếu `limit=3`), phản ánh đúng đánh đổi giữa chi phí/offline và năng lực tool-calling của model 3B.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  - Gỡ các chỉ dẫn bẫy của starter (ép đoán bừa, tự ý `send`, ép chọn 1 tool), đặt quy tắc hành vi tổng quát: câu hỏi meta/ngoài phạm vi (toán, lập trình) trả lời hoặc từ chối thẳng bằng text; cho phép gọi nhiều tool song song (`R13`); ưu tiên ý định đổi nguồn ở lượt cuối (`M06`); và bắt buộc gọi `fetch` ngay khi thấy URL `http(s)://` (`R04`).
- **Fix nào thuộc `tools.yaml`?**
  - Mô tả ranh giới từng tool theo mẫu **Dùng khi / Không dùng khi** (giúp model phân biệt rõ `lookup` vs `papers` ở `R03`, `timeline` vs `social_search`, `hackernews` vs `lookup`) và chuẩn hóa convention tham số (`lookup.query` không kèm `"news"`/`"today"`, `lookup.topic` chỉ nhận `general|news`, `social_search.search_type`, `timeline.screenname` không có `@`, `send.confirmed`). Ở thử nghiệm `v2`, chính sửa `tools.yaml` đem lại bước nhảy lớn nhất (`0.45 → 0.70`, multiturn `0.3333 → 0.8333`).
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Các trường hợp như `R11_missing_url` và `R12_confirm_before_send` ở `v3`: `run_eval.py` chấm **FAIL** vì model không phát tool call `clarify`, nhưng khi đọc `actual_text` thì model đã thực sự hỏi lại xin URL / xin nội dung tin nhắn trước khi gửi (hành vi an toàn với người dùng thực tế). Ngoài ra chất lượng tóm tắt/trích dẫn nguồn trong `chat.py` (không bịa link, không nghe prompt injection) cũng cần đọc transcript thủ công thay vì chỉ chấm `tool_calls`.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  - Giả thuyết `v4`: bổ sung 1–2 ví dụ **few-shot tool call JSON mẫu** cho riêng hành vi gọi `clarify(response_type="text"|"yes_no")` và `timeline(..., limit=...)` (hoặc thử trên model lớn hơn như `qwen2.5:7b` / cloud model) để kiểm tra xem có giải quyết dứt điểm 4 case còn sót ở `v3` (`R10`, `R11`, `R12`, `M03`) và lỗi đoán `sama` ở Turn 2 của `chat.py` hay không.

## 8. Tài liệu tham khảo

-
