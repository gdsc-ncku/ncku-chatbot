"""共用函式模組"""

import logging
from linebot.models import (
    QuickReply,
    QuickReplyButton,
    MessageAction,
    SendMessage,
)
from ...config.line_config import line_bot_api

logger = logging.getLogger(__name__)

# 常用指令
COMMANDS = {
    "/help": (
        "📚 可用的指令列表：\n"
        "1. /help - 顯示此幫助訊息\n"
        "2. /setup - 設定相關功能\n\n"
        "💡 您也可以直接輸入問題，我會盡力協助您！"
    ),
    "/setup": "⚙️ 設定功能開發中，敬請期待！",
}


def create_quick_reply() -> QuickReply:
    """建立快速回覆按鈕"""
    return QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label="說明", text="/help")),
            QuickReplyButton(action=MessageAction(label="設定", text="/setup")),
        ]
    )


def send_message(reply_token: str, messages: list[SendMessage]) -> None:
    """發送訊息到 LINE"""
    readable_messages = str(messages).encode("utf-8").decode("unicode_escape")
    logger.info(f"準備發送訊息 (使用可讀字串): {readable_messages}")

    # 確保 messages 是一個扁平化的訊息列表 (因為可能有巢狀的訊息列表)
    flat_messages = []
    for msg in messages:
        if isinstance(msg, list):
            flat_messages.extend(msg)  # 如果是列表，則展開
        else:
            flat_messages.append(msg)  # 如果是單一訊息，則直接加入

    line_bot_api.reply_message(reply_token, flat_messages)
    logger.info(f"已發送訊息: {flat_messages}")
