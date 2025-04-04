import requests
from openai import OpenAI
import os
import json

client = OpenAI(api_key="api_key")
filename = "行政手續摘要.json"

# 預設網址
base_url = "https://adms-acad.ncku.edu.tw/?Lang=zh-tw"
prefixed_url = f"https://r.jina.ai/{base_url}"

# 爬取網站內容
response = requests.get(prefixed_url)
web_data = response.text

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": """你是一個資料整理專家，請從使用者提供的文字內容中生成：
            1. 一個適合的標題（title）。
            2. 一段適合的回應內容。
            輸出格式如下：
            {
                "question": "適當的標題",
                "answer": "詳細的回應內容"
            }
            請使用**繁體中文**回應
            請把所以資訊列點出來
            不要反斜線和空白
            可以附上連結在回應裡面""",
        },
        {"role": "user", "content": web_data},
    ],
    model="gpt-4o-mini",
)

# 解析回應並格式化 JSON
generated_content = chat_completion.choices[0].message.content.strip()

try:
    new_data = json.loads(generated_content)
except json.JSONDecodeError as e:
    print("JSON 格式錯誤：", e)
else:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                if isinstance(existing_data, list):
                    existing_data.append(new_data)
                else:
                    existing_data = [existing_data, new_data]
            except json.JSONDecodeError:
                # 如果檔案內容無效，初始化為空列表
                existing_data = [new_data]
    else:
        existing_data = [new_data]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
