import logging
from linebot.models import MessageEvent, TextMessage, ImageMessage, AudioMessage

from ..config.line_config import handler
from ..services.message_service import MessageService
from ..config.logger import get_logger

# 取得模組的日誌記錄器
logger = get_logger(__name__)

message_service = MessageService()


# text message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_messages = message_service.handle_text_message(event)
    message_service.send_message(event.reply_token, reply_messages)


# image message
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    reply_messages = message_service.handle_image_message(event)
    logger.info(f"圖片處理回應: {reply_messages}")
    message_service.send_message(event.reply_token, reply_messages)


# audio message
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    reply_messages = message_service.handle_audio_message(event)
    message_service.send_message(event.reply_token, reply_messages)
