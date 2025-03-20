from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
import traceback  # 用於輸出錯誤堆疊

from utils.openai_api import openai_api
from utils.image_processing import encode_image


app = Flask(__name__)

channel_access_token = 'your access token'
channel_secret = 'your secret'

@app.route("/", methods=['POST'])
def linebot():

    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        line_bot_api = LineBotApi(channel_access_token)
        handler = WebhookHandler(channel_secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg_type = json_data['events'][0]['message']['type']

        # text processing
        if msg_type == 'text':
            msg = json_data['events'][0]['message']['text']
            prompt = [
                {"role": "assistant", 
                 "content": "你是一個專業的 AI 聊天機器人，請根據問題使用相對應語言回覆"},
                {"role": "user", "content": msg}
            ]
            reply_msg = openai_api(prompt)

        # image processing
        elif msg_type == 'image':
            msgID = json_data['events'][0]['message']['id']
            message_content = line_bot_api.get_message_content(msgID)

            with open(f'{msgID}.jpg', 'wb') as fd:
                fd.write(message_content.content)
            base64_image = encode_image(f'{msgID}.jpg') # image processing                
            prompt=[
                {"role": "assistant", 
                 "content": "你是一個專業的 AI 聊天機器人，請根據圖片內容使用相對應的回覆"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "圖片內容有什麼?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ]
            reply_msg = openai_api(prompt)
        else:
            reply_msg = '你傳的不是文字或圖片呦～'

        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk,text_message)
    except Exception as e:
        print(f"未預期的錯誤: {str(e)}\n{traceback.format_exc()}")
    return 'OK'

if __name__ == "__main__":
    app.run(debug=True)  # 使用環境變數中的 port，如果未設置則預設為 8000