import argparse
import json
import os
import sys

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
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free", messages=messages, tools=available_functions
        )

        message = response.choices[0].message

        if response.usage is None:
            raise RuntimeError("API response missing usage metadata")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        messages.append(message)

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

if __name__ == "__main__":
    main()
