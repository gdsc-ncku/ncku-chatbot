import traceback
import base64
import os
from pydub import AudioSegment
from ..config.logger import get_logger
from .utils.openai_api import openai_api

logger = get_logger(__name__)


def transcribe_audio(audio_path: str, prompt: str = "請將以下語音內容逐字轉寫") -> str:
    """
    使用 OpenAI 相容 API (實際為 Gemini 代理) 對語音檔進行語音辨識。

    Args:
        audio_path (str): 語音檔案路徑
        prompt (str): 可選的提示語

    Returns:
        str: 辨識出來的語音內容（文字）
    """
    try:
        # 轉為單聲道 16kHz，並輸出成 .wav 格式
        sound = AudioSegment.from_file(audio_path)
        sound = sound.set_channels(1).set_frame_rate(16000)
        temp_path = "temp_audio.wav"
        sound.export(temp_path, format="wav")

        # base64 encode 音檔
        with open(temp_path, "rb") as audio_file:
            audio_data = audio_file.read()
        base64_audio = base64.b64encode(audio_data).decode("utf-8")

        # 建立 OpenAI 相容格式的 messages
        messages = [
            {
                "role": "assistant",
                "content": "你是一個專業的 AI 聊天機器人，請根據語音內容生成逐字稿",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "input_audio",
                        "input_audio": {"data": base64_audio, "format": "wav"},
                    },
                ],
            },
        ]

        # 呼叫自定義的 openai_api（實際透過 Gemini 代理）
        reply_msg = openai_api(messages)
        return reply_msg

    except Exception as e:
        error_detail = f"處理語音時發生錯誤: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_detail)
        return "處理語音時發生錯誤，請稍後再試"
