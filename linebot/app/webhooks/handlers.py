from linebot.models import MessageEvent, TextMessage, ImageMessage, AudioMessage

from ..config.line_config import handler
from ..services.message_service import MessageService

message_service = MessageService()

# text message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_message = message_service.handle_text_message(event)
    message_service.send_message(event.reply_token, [reply_message])

# image message
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    reply_message = message_service.handle_image_message(event)
    message_service.send_message(event.reply_token, [reply_message])

# audio message
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    reply_message = message_service.handle_audio_message(event)
    message_service.send_message(event.reply_token, [reply_message])