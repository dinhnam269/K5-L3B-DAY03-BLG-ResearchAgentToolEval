from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"

load_lab_env(ROOT)

st.set_page_config(page_title="BLG Research Agent", page_icon="🔎", layout="wide")
st.title("🔎 BLG Research Agent")
st.caption("Live Research Agent UI — hiển thị đầy đủ tool calls, tham số và kết quả/lỗi tool theo từng lượt.")


def _init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "turn_index" not in st.session_state:
        st.session_state.turn_index = 0
    if "transcript" not in st.session_state:
        st.session_state.transcript = None
    if "transcript_path" not in st.session_state:
        st.session_state.transcript_path = None


def _render_tool_events(tool_events: list[dict[str, Any]]) -> None:
    if not tool_events:
        return
    with st.expander(f"Chi tiết Tool Calls ({len(tool_events)})", expanded=False):
        for idx, event in enumerate(tool_events, start=1):
            tool_name = event.get("tool", "unknown")
            args = event.get("args", {})
            result = event.get("result", {})
            st.markdown(f"**{idx}. `{tool_name}`** `{json.dumps(args, ensure_ascii=False)}`")
            if isinstance(result, dict) and result.get("error"):
                st.error(f"Tool error ({result.get('error')}): {result.get('message', '')}")
            elif isinstance(result, dict) and result.get("status") == "needs_confirmation":
                st.warning(result.get("message", "Cần xác nhận từ người dùng trước khi gửi."))
            st.json(result)


_init_session()

with st.sidebar:
    st.header("Cấu hình Agent")
    provider_name = st.selectbox("Provider", ["ollama", "openrouter", "gemini", "openai", "anthropic"], index=0)
    default_model = "qwen2.5:3b" if provider_name == "ollama" else ""
    model_input = st.text_input("Model (để trống nếu dùng mặc định)", value=default_model)
    version_label = st.text_input("Version label", value="v3")
    history_window = st.slider("History window (turns)", min_value=1, max_value=10, value=5)
    max_tool_rounds = st.slider("Max tool rounds / turn", min_value=1, max_value=6, value=4)

    if st.button("Bắt đầu phiên chat mới", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.turn_index = 0
        st.session_state.transcript = None
        st.session_state.transcript_path = None
        st.rerun()

    st.divider()
    st.markdown("**Câu hỏi gợi ý:**")
    st.markdown("- *Tin tức AI hôm nay có gì nổi bật?*")
    st.markdown("- *Trên Hacker News đang bàn luận gì về Rust?*")
    st.markdown("- *Tóm tắt 5 tweet mới nhất giúp mình* → sau đó bổ sung *của Sam Altman*")
    st.markdown("- *Đăng bản tin này lên Telegram giúp mình*")

system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_path = ARTIFACTS_DIR / "tools.yaml"
system_prompt = system_prompt_path.read_text(encoding="utf-8")
tool_declarations = load_tool_declarations(tools_path)
openai_tools = to_openai_tools(tool_declarations)
artifact_version = build_artifact_version(version_label or "v3", system_prompt_path, tools_path)

with st.sidebar:
    st.caption(f"Artifact: `{artifact_version.artifact_version}`")
    st.caption(f"Tools loaded: `{len(tool_declarations)}`")
    if st.session_state.transcript_path:
        st.caption(f"Transcript: `{Path(st.session_state.transcript_path).name}`")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            _render_tool_events(msg.get("tool_events", []))

user_text = st.chat_input("Nhập yêu cầu nghiên cứu của bạn...")
if user_text:
    user_text = user_text.strip()
    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        provider = make_provider(provider_name)
        model_name = model_input.strip() or None
        selected_model = model_name or getattr(provider, "default_model", None)

        if st.session_state.transcript is None:
            timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
            transcript_id = "_".join([safe_slug(version_label or "v3"), safe_slug(provider_name), timestamp])
            st.session_state.transcript_path = str(TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json")
            st.session_state.transcript = {
                "transcript_id": transcript_id,
                **artifact_version_dict(artifact_version),
                "provider": provider_name,
                "model": selected_model,
                "system_prompt": str(system_prompt_path),
                "tools": str(tools_path),
                "history_window": history_window,
                "max_tool_rounds": max_tool_rounds,
                "created_at": now_iso(),
                "updated_at": now_iso(),
                "turns": [],
            }

        st.session_state.turn_index += 1
        messages = [
            {"role": "system", "content": system_prompt},
            *trim_history(st.session_state.history, history_window),
            {"role": "user", "content": user_text},
        ]
        turn_record: dict[str, Any] = {
            "turn_index": st.session_state.turn_index,
            "started_at": now_iso(),
            "user": user_text,
            "status": "started",
            "assistant_text": None,
            "rounds": [],
            "tool_events": [],
        }

        with st.chat_message("assistant"):
            with st.spinner("Agent đang xử lý..."):
                try:
                    result = run_model_tool_loop(
                        provider=provider,
                        messages=messages,
                        tools=openai_tools,
                        model=model_name,
                        max_tool_rounds=max_tool_rounds,
                    )
                    turn_record.update(result)
                    assistant_text = result.get("assistant_text") or ""
                    st.markdown(assistant_text)
                    _render_tool_events(result.get("tool_events", []))
                    st.session_state.history.append({"role": "user", "content": user_text})
                    st.session_state.history.append({"role": "assistant", "content": assistant_text})
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_text,
                        "tool_events": result.get("tool_events", []),
                    })
                except Exception as exc:
                    err_text = f"{type(exc).__name__}: {exc}"
                    turn_record.update({"status": "provider_error", "error": err_text})
                    st.error(f"Provider error: {err_text}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"⚠️ Provider error: `{err_text}`",
                        "tool_events": [],
                    })

        turn_record["ended_at"] = now_iso()
        st.session_state.transcript["turns"].append(turn_record)
        write_transcript(Path(st.session_state.transcript_path), st.session_state.transcript)

