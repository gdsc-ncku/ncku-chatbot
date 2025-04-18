"""處理音訊訊息的模組"""

import logging
from linebot.models import TextSendMessage
from .common import create_quick_reply

logger = logging.getLogger(__name__)


def handle_audio_message(event):
    """處理音訊訊息"""
    return [TextSendMessage(text="收到音訊消息", quick_reply=create_quick_reply())]
