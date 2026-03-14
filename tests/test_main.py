import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main


class FakeFunctionCall:
    type = "function_call"
    name = "get_current_time"
    arguments = json.dumps({})
    call_id = "call_123"


class FakeUnknownFunctionCall:
    type = "function_call"
    name = "unknown_function"
    arguments = json.dumps({})
    call_id = "call_999"


class FakeMessage:
    type = "message"


class FakeResponse:
    output = [FakeFunctionCall()]


class FakeUnknownResponse:
    output = [FakeUnknownFunctionCall()]


class FakeNoFunctionResponse:
    output = [FakeMessage()]


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


def test_build_function_outputs_returns_unknown_function_message():
    result = main.build_function_outputs(FakeUnknownResponse())

    assert result == [
        {
            "type": "function_call_output",
            "call_id": "call_999",
            "output": "Unknown function: unknown_function",
        }
    ]


def test_build_function_outputs_returns_empty_list_when_no_function_call():
    result = main.build_function_outputs(FakeNoFunctionResponse())

    assert result == []
