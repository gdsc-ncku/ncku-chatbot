from linebot.models import TextSendMessage, FlexSendMessage
from linebot.models.events import FollowEvent

from .handlers import (
    send_message,
    show_loading_animation,
)
from ..config.line_config import line_bot_api
from ..config.logger import get_logger
from .utils import flex_message_convert_to_json

logger = get_logger(__name__)

WELCOME_MESSAGE_1 = """歡迎使用 NCKU Chatbot！這是一款由 GDG on Campus 團隊開發的 AI 聊天機器人，能協助你解答問題、進行對話。

Welcome to NCKU Chatbot — an AI chatbot developed by GDG on Campus, here to help you with questions and conversations.

開始使用前，請先勾選同意使用條款，並建立你的個人檔案。

Before getting started, please agree to the terms of use and set up your personal profile.

Let's get started, {user_display_name} 🫶"""


class WelcomeService:
    def __init__(self):
        self.logger = logger
        self.line_bot_api = line_bot_api

    def send_welcome_message(self, event: FollowEvent):
        if event.type != "follow":
            self.logger.info(f"Not a follow event: {event}")
            return

        user_id = event.source.user_id
        user_profile = self.line_bot_api.get_profile(user_id)
        user_display_name = user_profile.display_name
        self.logger.info("Follow event received")
        self.logger.info(f"User id: {user_id}")
        self.logger.info(f"User display name: {user_display_name}")
        show_loading_animation(user_id)
        self.logger.info(f"Sending welcome message to user: {user_id}")
        flex_message_json = flex_message_convert_to_json("flex_messages/welcome/1.json")
        send_message(
            event.reply_token,
            [
                TextSendMessage(
                    text=WELCOME_MESSAGE_1.format(user_display_name=user_display_name)
                ),
                FlexSendMessage(alt_text="請閱讀服務條款", contents=flex_message_json),
            ],
        )
