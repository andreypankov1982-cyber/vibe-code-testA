import json
import os
from datetime import datetime
from typing import Callable

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-4.1-mini"
EXIT_COMMANDS = {"exit", "quit", "q"}

SYSTEM_PROMPT = """
Ты — консольный чат-бот.
Если пользователь спрашивает текущее время, используй инструмент get_current_time.
Если инструмент не нужен, отвечай обычным текстом.
""".strip()


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not found. Add it to the .env file in the project root."
        )
    return OpenAI(api_key=api_key)


def get_current_time() -> str:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[tool] get_current_time -> {current_time}")
    return current_time


TOOLS: dict[str, Callable[..., str]] = {
    "get_current_time": get_current_time,
}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Returns the current local time on the machine where the script is running.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    }
]


def ask_model(user_message: str):
    return get_client().responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=user_message,
        tools=TOOL_DEFINITIONS,
    )


def build_function_outputs(response) -> list[dict[str, str]]:
    function_outputs = []

    for item in response.output:
        if item.type != "function_call":
            continue

        function_name = item.name
        arguments = json.loads(item.arguments or "{}")

        if function_name not in TOOLS:
            function_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": f"Unknown function: {function_name}",
                }
            )
            continue

        result = TOOLS[function_name](**arguments)
        function_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": result,
            }
        )

    return function_outputs


def run_single_turn(user_message: str) -> str:
    first_response = ask_model(user_message)
    function_outputs = build_function_outputs(first_response)

    if not function_outputs:
        return first_response.output_text

    second_response = get_client().responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        previous_response_id=first_response.id,
        input=function_outputs,
        tools=TOOL_DEFINITIONS,
    )
    return second_response.output_text


def main():
    print("Чат запущен. Напиши сообщение.")
    print("Для выхода введи: exit")

    while True:
        try:
            user_message = input("Ты: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из чата.")
            break

        if not user_message:
            continue

        if user_message.lower() in EXIT_COMMANDS:
            print("Выход из чата.")
            break

        try:
            answer = run_single_turn(user_message)
            print(f"Бот: {answer}")
        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()