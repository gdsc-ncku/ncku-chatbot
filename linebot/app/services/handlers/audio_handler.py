"""處理語音訊息的模組"""

import os
import tempfile
from linebot.models import TextSendMessage
from .common import create_quick_reply
from ...api.speech import transcribe_audio
from ...config.line_config import line_bot_api
from ...config.logger import get_logger

# 取得模組的日誌記錄器
logger = get_logger(__name__)


def handle_audio_message(event):
    """處理語音訊息"""
    try:
        # 取得語音內容
        message_id = event.message.id
        message_content = line_bot_api.get_message_content(message_id)

        # 建立臨時檔案保存語音
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".m4a"
        ) as temp_audio_file:
            for chunk in message_content.iter_content():
                temp_audio_file.write(chunk)
            temp_file_path = temp_audio_file.name

        response = transcribe_audio(temp_file_path)

        # 刪除臨時檔案
        os.remove(temp_file_path)

        return [
            TextSendMessage(
                text=f"語音辨識結果：{response}", quick_reply=create_quick_reply()
            )
        ]
    except Exception as e:
        logger.error(f"處理語音訊息時發生錯誤: {str(e)}", exc_info=True)
        return [
            TextSendMessage(
                text="抱歉，處理語音時發生錯誤，請稍後再試。",
                quick_reply=create_quick_reply(),
            )
        ]
