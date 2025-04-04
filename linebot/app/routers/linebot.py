from fastapi import APIRouter, Request, HTTPException
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, AudioMessage
from ..config.line_config import handler
from ..services.message_service import MessageService

router = APIRouter(prefix="/linebot", tags=["linebot"])


# 建立 MessageService 物件
message_service = MessageService()

# 註冊訊息處理函式
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print("收到文字訊息")
    reply_message = message_service.handle_text_message(event)
    message_service.send_message(event.reply_token, [reply_message])

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print("收到圖片訊息")
    reply_message = message_service.handle_image_message(event)
    message_service.send_message(event.reply_token, [reply_message])

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    print("收到音訊訊息")
    reply_message = message_service.handle_audio_message(event)
    message_service.send_message(event.reply_token, [reply_message])


@router.post("/webhook")
async def line_webhook(request: Request):
    # 獲取 X-Line-Signature header 值
    signature = request.headers["X-Line-Signature"]

    # 獲取請求體內容
    body = await request.body()

    try:
        # 驗證簽名並處理請求
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"
