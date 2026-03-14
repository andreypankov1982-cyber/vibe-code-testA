# Terminal Chat Bot with Function Calling

Test assignment solution for **Variant A**.

## Overview

This project is a terminal-based chat bot built with Python and the OpenAI API.

It can:

- read user messages in a loop
- send them to OpenAI
- use a simple tool named `get_current_time`
- call that tool when the user asks for the current time

The implementation follows the assignment requirement to support basic function calling in a console chat flow.

## Features

- terminal chat loop
- OpenAI Responses API integration
- function calling with `get_current_time`
- second request after tool execution
- `.env` support via `python-dotenv`
- automated tests with `pytest` for tool-call handling scenarios

## Project Structure

- `main.py` — main chat bot application
- `tests/test_main.py` — automated tests for tool-call handling scenarios
- `requirements.txt` — project dependencies
- `.env.example` — example environment configuration
- `.gitignore` — ignored local files

## Setup

1. Clone the repository:

```bash
git clone https://github.com/andreypankov1982-cyber/vibe-code-testA.git
cd vibe-code-testA
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_real_openai_api_key_here
```

You can copy `.env.example` and rename it to `.env`.

## Run

```powershell
python main.py
```

## Run Tests

```powershell
pytest
```

## Error Handling

- the application shows a clear error message if `OPENAI_API_KEY` is missing
- the chat can be stopped with `exit`, `quit`, `q`, `Ctrl+C`, or `Ctrl+D`

## Example Dialogue

```text
Чат запущен. Напиши сообщение.
Для выхода введи: exit

Ты: Сколько будет 2+2?
Бот: 2 + 2 = 4.

Ты: Какое сейчас время?
[tool] get_current_time -> 2026-03-14 17:28:03
Бот: Сейчас 17:28. Чем могу помочь?

Ты: exit
Выход из чата.
```

## How Function Calling Works

1. The user message is sent to OpenAI.
2. If the model decides to call `get_current_time`, the script detects the function call.
3. The tool is executed locally in Python.
4. The tool result is sent back to OpenAI.
5. The final assistant response is printed in the terminal.

## Assignment Checklist

Implemented requirements from Variant A:

1. A script that continuously reads user input and sends it to OpenAI
2. A function `get_current_time` that returns the current time
3. A prompt that tells the model to use the tool when the user asks for time
4. Parsing the model response and executing the function when needed

## AI Usage

**AI-assisted contribution: approximately 65%.**

AI was used to help with project scaffolding, drafting parts of the function-calling flow, refining the test, and preparing documentation.

Final integration, environment setup, debugging, validation, and manual refinements were completed by the author.