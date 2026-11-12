import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    print("Hello from secret-asian!")
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("No api key found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt", nargs="?")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    memory_file = Path("conversation.json")
    if memory_file.exists():
        with open(memory_file, "r") as f:
            messages = json.load(f)
    else:
        messages = [
            {"role": "system", "content": system_prompt},
        ]

    while True:
        if args.user_prompt:
            user_prompt = args.user_prompt
            args.user_prompt = None
        else:
            user_prompt = input("You: ")

        if user_prompt.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_prompt})

        for _ in range(20):
            response = client.chat.completions.create(
                model="openrouter/free", messages=messages, tools=available_functions
            )

            message = response.choices[0].message

            if response.usage is None:
                raise RuntimeError("API response missing usage metadata")

            if args.verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")

            messages.append(message.model_dump())

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_result = call_function(tool_call, verbose=args.verbose)
                    messages.append(tool_result)
                    print(tool_result["content"])
            elif message.content:
                print(message.content)
                break
            else:
                raise RuntimeError("No content or tool call returned by the model")

        else:
            print("agent did not finish its task within the iteration limit")
            sys.exit(1)

        with open(memory_file, "w") as f:
            json.dump(messages, f)

if __name__ == "__main__":
    main()
