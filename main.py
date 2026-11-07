import os
import argparse
import json

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import call_function, available_functions

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

if api_key is None:
    raise Exception("Cannot find API Key")


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable Verbosse Output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for i in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions
        )

        if response.usage is None:
            raise RuntimeError("API response has failed")

        prompt_tokens = response.usage.prompt_tokens 
        response_tokens = response.usage.completion_tokens

        if args.verbose:
            print(f"Prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls is None or len(message.tool_calls) == 0:
            print(f"Final response: \n {message.content}")
            break
        else:
            if i == 19:
                print("Error: Maximum iterations reached")
                exit(1)

            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)

                if result_message == "":
                    raise ValueError("Function returned an empty string")

                if args.verbose:
                    print(f"-> {result_message['content']}")


if __name__ == "__main__":
    main()
