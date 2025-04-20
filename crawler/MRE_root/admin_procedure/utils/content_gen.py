def generate_content(client, web_data):
    # Generate content using OpenAI's API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """你是一個資料整理專家，請從使用者提供的文字內容中生成：
                1. 一個適合的標題（title）。
                2. 一段適合的內容。
                請使用**繁體中文**回應
                請把所有資訊列點出來
                不要反斜線和空白
                **連結請務必保留並且一定要附上，包含下載連結**""",
            },
            {"role": "user", "content": web_data},
        ],
        model="gpt-4o-mini",
    )
    return chat_completion.choices[0].message.content.strip()


def question_classifaier(client, web_data):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """請幫助分辨以下內容是否屬於校園的行政手續問題:
                如註冊、申請宿舍、學籍變更等。
                **只要輸出True或False即可。**""",
            },
            {"role": "user", "content": web_data},
        ],
        model="gpt-4o-mini",
    )
    return chat_completion.choices[0].message.content.strip()
