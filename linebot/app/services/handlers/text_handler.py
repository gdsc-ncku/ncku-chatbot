"""處理文字訊息的模組"""

import json
from linebot.models import TextSendMessage, FlexSendMessage
from .common import create_quick_reply, COMMANDS
from ...api.dify import inference
from ...config.logger import get_logger

# 取得模組的日誌記錄器
logger = get_logger(__name__)


def handle_text_message(event):
    """處理文字訊息"""
    try:
        user_input = event.message.text
        user_id = event.source.user_id

        # 產生回應訊息
        quick_reply = None
        if user_input in COMMANDS:
            response_text = COMMANDS[user_input]
            quick_reply = create_quick_reply()
            return [TextSendMessage(text=response_text, quick_reply=quick_reply)]

        # 處理一般查詢
        response_text = inference(user_input, user_id)
        quick_reply = create_quick_reply()

        # 處理可能包含 Flex Message 的回應
        if "===FLEX_MESSAGE===" in response_text:
            parts = response_text.split("===FLEX_MESSAGE===")
            text_content = parts[0].strip()
            text_message = TextSendMessage(text=text_content, quick_reply=quick_reply)

            # 檢查是否有 Flex Message 部分
            if len(parts) > 1:
                flex_content = parts[1].strip().replace("```", "").replace("json", "")
                if flex_content and flex_content != "False":
                    try:
                        flex_json = json.loads(flex_content)
                        return [
                            text_message,
                            FlexSendMessage(alt_text="詳細資訊", contents=flex_json),
                        ]
                    except Exception as e:
                        logger.error(f"Flex訊息解析錯誤: {str(e)}", exc_info=True)

            return [text_message]

        # 純文字回應
        return [TextSendMessage(text=response_text, quick_reply=quick_reply)]

    except Exception as e:
        logger.error(f"處理訊息時發生錯誤: {str(e)}", exc_info=True)
        return [
            TextSendMessage(
                text="抱歉，系統發生錯誤，請稍後再試。",
                quick_reply=create_quick_reply(),
            )
        ]
