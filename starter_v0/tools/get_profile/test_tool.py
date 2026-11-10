from unittest.mock import Mock

import requests

from tools.tool import get_profile


def test_happy_path_returns_profile(monkeypatch):
    response = Mock(status_code=200)
    response.json.return_value = {"profile": {"handle": "openai", "name": "OpenAI"}}
    request = Mock(return_value=response)
    monkeypatch.setattr(requests, "get", request)

    result = get_profile(screenname="@OpenAI", detail="metrics")

    assert result == {"ok": True, "profile": {"handle": "openai", "name": "OpenAI"}}
    assert request.call_args.args[0].endswith("/users/openai")
    assert request.call_args.kwargs["params"] == {"detail": "metrics"}


def test_bad_model_inputs_return_error_dict():
    assert get_profile(screenname="") ["ok"] is False
    assert get_profile(screenname=123)["error"]["code"] == "invalid_input"
    assert get_profile(screenname="OpenAI", detail="private")["error"]["code"] == "invalid_input"


def test_missing_key_and_http_429_return_error_dict(monkeypatch):
    missing = get_profile()
    assert missing["ok"] is False
    assert missing["error"]["code"] == "missing_key"

    response = Mock(status_code=429)
    monkeypatch.setattr(requests, "get", Mock(return_value=response))
    rate_limited = get_profile(screenname="OpenAI")
    assert rate_limited["ok"] is False
    assert rate_limited["error"] == {
        "code": "rate_limited",
        "message": "Profile service rate limit reached.",
        "status": 429,
    }
