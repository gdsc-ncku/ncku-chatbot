"""訊息服務模組 - 處理 LINE Bot 的各種訊息類型"""

from .handlers import (
    handle_postback_event,
    show_loading_animation,
    send_message,
)
from ..config.logger import get_logger

logger = get_logger(__name__)


class PostbackService:
    """處理 LINE Bot 的按鈕事件"""

    def handle_postback_event(self, event):
        """處理按鈕事件"""
        result = handle_postback_event(event)
        if not result:
            logger.warning(f"未處理的按鈕事件: {event.postback.data}")
            return None
        show_loading_animation(event.source.user_id)
        return result

    def send_message(self, reply_token, messages):
        """發送訊息到 LINE"""
        logger.info(f"發送訊息到 LINE: {messages}")
        send_message(reply_token, messages)
