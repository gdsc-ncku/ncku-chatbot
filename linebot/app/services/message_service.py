import logging

from linebot.models import (
    TextSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    SendMessage,
)

from ..config.line_config import line_bot_api
from ..api.dify import inference

logger = logging.getLogger(__name__)

COMMANDS = {
    "/help": (
        "📚 可用的指令列表：\n"
        "1. /help - 顯示此幫助訊息\n"
        "2. /setup - 設定相關功能\n\n"
        "💡 您也可以直接輸入問題，我會盡力協助您！"
    ),
    "/setup": "⚙️ 設定功能開發中，敬請期待！",
}


class MessageService:
    """處理 LINE Bot 的訊息服務"""

    def handle_text_message(self, event) -> TextSendMessage:
        """處理文字訊息"""
        try:
            user_input = event.message.text
            user_id = event.source.user_id

            # 產生回應訊息
            quick_reply = None
            if user_input in COMMANDS:
                quick_reply = self._create_quick_reply()
                response_text = COMMANDS[user_input]
            else:
                response_text = inference(user_input, user_id)

            return TextSendMessage(text=response_text, quick_reply=quick_reply)

        except Exception as e:
            logger.error(f"處理訊息時發生錯誤: {str(e)}", exc_info=True)
            return TextSendMessage(
                text="抱歉，系統發生錯誤，請稍後再試。",
                quick_reply=self._create_quick_reply(),
            )

    def handle_image_message(self, event) -> TextSendMessage:
        """處理圖片訊息"""
        return TextSendMessage(
            text="收到圖片消息", quick_reply=self._create_quick_reply()
        )

    def handle_audio_message(self, event) -> TextSendMessage:
        """處理音訊訊息"""
        return TextSendMessage(
            text="收到音訊消息", quick_reply=self._create_quick_reply()
        )

    def send_message(self, reply_token: str, messages: list[SendMessage]) -> None:
        """發送訊息到 LINE"""
        line_bot_api.reply_message(reply_token, messages)

    def _create_quick_reply(self) -> QuickReply:
        """建立快速回覆按鈕"""
        return QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="說明", text="/help")),
                QuickReplyButton(action=MessageAction(label="設定", text="/setup")),
            ]
        )
