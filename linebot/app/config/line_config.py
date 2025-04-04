from linebot import LineBotApi, WebhookHandler
from dotenv import load_dotenv
import os

load_dotenv()

# 初始化 LINE Bot API 和 WebhookHandler
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
