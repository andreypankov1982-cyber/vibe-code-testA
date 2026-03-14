import json

import main


class FakeFunctionCall:
    type = "function_call"
    name = "get_current_time"
    arguments = json.dumps({})
    call_id = "call_123"


class FakeResponse:
    output = [FakeFunctionCall()]


def test_build_function_outputs_returns_function_result(monkeypatch):
    monkeypatch.setitem(main.TOOLS, "get_current_time", lambda: "2026-03-14 17:28:03")

    result = main.build_function_outputs(FakeResponse())

    assert result == [
        {
            "type": "function_call_output",
            "call_id": "call_123",
            "output": "2026-03-14 17:28:03",
        }
    ]