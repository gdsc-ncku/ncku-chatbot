"""處理音訊訊息的模組"""

from linebot.models import TextSendMessage
from .common import create_quick_reply
from ...config.logger import get_logger

# 取得模組的日誌記錄器
logger = get_logger(__name__)


def handle_audio_message(event):
    """處理音訊訊息"""
    return [TextSendMessage(text="收到音訊消息", quick_reply=create_quick_reply())]
