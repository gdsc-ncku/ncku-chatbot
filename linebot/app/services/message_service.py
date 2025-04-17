import logging
import json

from linebot.models import (
    TextSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    SendMessage,
    FlexSendMessage,
)
from ..api.vision import process_image
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
                response_text = COMMANDS[user_input]
                quick_reply = self._create_quick_reply()
                return [TextSendMessage(text=response_text, quick_reply=quick_reply)]

            # 處理一般查詢
            response_text = inference(user_input, user_id)
            quick_reply = self._create_quick_reply()

            # 處理可能包含 Flex Message 的回應
            if "===FLEX_MESSAGE===" in response_text:
                parts = response_text.split("===FLEX_MESSAGE===")
                text_content = parts[0].strip()
                text_message = TextSendMessage(
                    text=text_content, quick_reply=quick_reply
                )

                # 檢查是否有 Flex Message 部分
                if len(parts) > 1:
                    flex_content = (
                        parts[1].strip().replace("```", "").replace("json", "")
                    )
                    if flex_content and flex_content != "False":
                        try:
                            flex_json = json.loads(flex_content)
                            return [
                                text_message,
                                FlexSendMessage(
                                    alt_text="詳細資訊", contents=flex_json
                                ),
                            ]
                        except Exception as e:
                            logger.error(f"Flex訊息解析錯誤: {str(e)}", exc_info=True)

                return [text_message]

            # 純文字回應
            return [TextSendMessage(text=response_text, quick_reply=quick_reply)]

        except Exception as e:
            logger.error(f"處理訊息時發生錯誤: {str(e)}", exc_info=True)
            return TextSendMessage(
                text="抱歉，系統發生錯誤，請稍後再試。",
                quick_reply=self._create_quick_reply(),
            )

    def handle_image_message(self, event) -> TextSendMessage:
        """處理圖片訊息"""
        try:
            # 取得圖片內容
            message_id = event.message.id
            message_content = line_bot_api.get_message_content(message_id)

            # 建立臨時檔案保存圖片
            temp_file_path = f"{message_id}.jpg"
            with open(temp_file_path, "wb") as temp_image_file:
                for chunk in message_content.iter_content():
                    temp_image_file.write(chunk)

            # 使用 vision 函式處理圖片
            response = process_image(
                temp_file_path, "圖片內容有什麼?"
            )  # TODO: 設定圖片處理的 prompt

            # 刪除臨時檔案
            os.remove(temp_file_path)

            return TextSendMessage(
                text=response, quick_reply=self._create_quick_reply()
            )
        except Exception as e:
            logger.error(f"處理圖片訊息時發生錯誤: {str(e)}", exc_info=True)
            return TextSendMessage(
                text="抱歉，處理圖片時發生錯誤，請稍後再試。",
                quick_reply=self._create_quick_reply(),
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
