import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI

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
    args = parser.parse_args()

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ]
    )

    if response.usage is None:
        raise RuntimeError("API response has failed")

    prompt_tokens = response.usage.prompt_tokens 
    response_tokens = response.usage.completion_tokens

    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
