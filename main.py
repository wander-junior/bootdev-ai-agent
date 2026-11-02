import os

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

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ]
)

def main():
    if response.usage is None:
        raise RuntimeError("API response has failed")

    prompt_tokens = response.usage.prompt_tokens 
    response_tokens = response.usage.completion_tokens

    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
