from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = "gemini-2.0-flash-001"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def openai_api(messages):
    client = OpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
    )
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0.7
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print(openai_api("你知道王建民嗎？"))
