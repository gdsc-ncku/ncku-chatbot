from fastapi import APIRouter, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix="/linebot",
    tags=["linebot"]
)

# 初始化 LINE Bot API 和 WebhookHandler
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@router.post("/webhook")
async def line_webhook(request: Request):
    # 獲取 X-Line-Signature header 值
    signature = request.headers.get('X-Line-Signature', '')
    
    # 獲取請求體內容
    body = await request.body()
    body = body.decode('utf-8')
    
    try:
        # 驗證簽名並處理 webhook 事件
        handler.handle(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    return {'message': 'OK'}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當收到文字訊息時的處理邏輯
    message = TextSendMessage(text=f"NCKU Chatbot 收到訊息: {event.message.text}")
    line_bot_api.reply_message(event.reply_token, message) 