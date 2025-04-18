"""處理圖片訊息的模組"""

import os
import logging
from linebot.models import TextSendMessage
from .common import create_quick_reply
from ...api.vision import process_image
from ...config.line_config import line_bot_api

logger = logging.getLogger(__name__)


def handle_image_message(event):
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
        return [TextSendMessage(text=response, quick_reply=create_quick_reply())]
    except Exception as e:
        logger.error(f"處理圖片訊息時發生錯誤: {str(e)}", exc_info=True)
        return [
            TextSendMessage(
                text="抱歉，處理圖片時發生錯誤，請稍後再試。",
                quick_reply=create_quick_reply(),
            )
        ]
