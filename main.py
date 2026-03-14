import json
from datetime import datetime

from openai import OpenAI

def get_client():
    return OpenAI()

def get_current_time() -> str:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[tool] get_current_time -> {current_time}")
    return current_time

TOOLS = {
    "get_current_time": get_current_time,
}

MODEL = "gpt-4.1-mini"

SYSTEM_PROMPT = """
Ты — консольный чат-бот.
Если пользователь спрашивает текущее время, используй инструмент get_current_time.
Если инструмент не нужен, отвечай обычным текстом.
""".strip()

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Возвращает текущее локальное время на компьютере, где запущен скрипт.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    }
]

def ask_model(user_message: str):
    response = get_client().responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=user_message,
        tools=TOOL_DEFINITIONS,
    )
    return response

def build_function_outputs(response):
    input_items = []

    for item in response.output:
        if item.type != "function_call":
            continue

        function_name = item.name
        arguments = json.loads(item.arguments)

        if function_name not in TOOLS:
            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": f"Unknown function: {function_name}",
                }
            )
            continue

        result = TOOLS[function_name](**arguments)

        input_items.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": result,
            }
        )

    return input_items

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
        user_message = input("Ты: ").strip()

        if user_message.lower() == "exit":
            print("Выход из чата.")
            break

        if not user_message:
            continue

        try:
            answer = run_single_turn(user_message)
            print(f"Бот: {answer}")
        except Exception as error:
            print(f"Ошибка: {error}")

if __name__ == "__main__":
    main()