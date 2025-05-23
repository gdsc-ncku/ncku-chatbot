import traceback
from typing import Optional, Dict, Any, List

# Import OpenAI API and image processing utilities
from .utils.openai_api import openai_api
from .utils.image_processing import encode_image
from ..config.logger import get_logger

# 取得模組的日誌記錄器
logger = get_logger(__name__)


def process_image(image_path: str, prompt: str = "圖片內容有什麼?") -> str:
    """
    Process image input using OpenAI API

    Args:
        image_path: Path to the image file
        prompt: Text prompt to accompany the image

    Returns:
        str: The response from the OpenAI API
    """
    try:
        # Encode the image to base64
        base64_image = encode_image(image_path)

        # Create prompt for OpenAI API
        messages = [
            {
                "role": "assistant",
                "content": "你是一個專業的 AI 聊天機器人，請根據圖片內容使用相對應的回覆",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            },
        ]

        # Get response from OpenAI API
        reply_msg = openai_api(messages)
        return reply_msg
    except Exception as e:
        error_detail = f"未預期的錯誤: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_detail)
        return "處理圖片時發生錯誤，請稍後再試"
