"""訊息服務模組 - 處理 LINE Bot 的各種訊息類型"""

import logging
from .handlers import (
    handle_text_message,
    handle_image_message,
    handle_audio_message,
    send_message,
    show_loading_animation,
)

logger = logging.getLogger(__name__)


# 為了保持與舊版API相容，我們可以保留這個類別作為包裝器
class MessageService:
    """處理 LINE Bot 的訊息服務 (相容性封裝)"""

    def handle_text_message(self, event):
        """處理文字訊息"""
        show_loading_animation(event.source.user_id)
        return handle_text_message(event)

    def handle_image_message(self, event):
        """處理圖片訊息"""
        show_loading_animation(event.source.user_id)
        return handle_image_message(event)

    def handle_audio_message(self, event):
        """處理音訊訊息"""
        show_loading_animation(event.source.user_id)
        return handle_audio_message(event)

    def send_message(self, reply_token, messages):
        """發送訊息到 LINE"""
        send_message(reply_token, messages)
