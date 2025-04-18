import requests
from openai import OpenAI
import os
import json

client = OpenAI(api_key="api_key")
filename = "行政手續摘要.json"

# 從 urls.txt 讀取 base_url
main_urls = []
with open("./web_crawler_urls.txt", "r", encoding="utf-8") as file:
    for line in file:
        url = line.strip().strip('"')
        if url.startswith("http"):
            main_urls.append(url)

# 初始化 JSON 資料
existing_data = []
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
            if not isinstance(existing_data, list):
                existing_data = [existing_data]
        except json.JSONDecodeError:
            existing_data = []

# 對每個 URL 進行爬取和處理
for base_url in main_urls:
    prefixed_url = f"https://r.jina.ai/{base_url}"

    # 爬取網站內容
    try:
        response = requests.get(prefixed_url)
        response.raise_for_status()  # 檢查請求是否成功
        web_data = response.text
    except requests.RequestException as e:
        print(f"爬取 {base_url} 失敗：{e}")
        continue

    # 呼叫 OpenAI API 處理內容
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
                請把所有資訊列點出來
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
        existing_data.append(new_data)
    except json.JSONDecodeError as e:
        print(f"JSON 格式錯誤（{base_url}）：{e}")
        continue

# 將所有結果寫入檔案
with open(filename, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)
