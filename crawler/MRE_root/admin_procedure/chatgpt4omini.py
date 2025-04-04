import os
import requests
import json
from openai import OpenAI

client = OpenAI(api_key="api_key")


url = "https://web.ncku.edu.tw/index.php"
response = requests.get(url)
web_data = response.text

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": """你是一位喜歡整理資料的人，喜歡把所有問題整理成qa的形式，如以下這樣的json格式: 
                        [
                        {"question": "問題1", "answer": "答案1"},
                        {"question": "問題2", "answer": "答案2"},
                        ]
                    """,
        },
        {"role": "user", "content": web_data},
    ],
    model="gpt-4o-mini",
)

print(chat_completion.choices[0].message.content)
