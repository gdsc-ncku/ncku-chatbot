from linebot.models import TextSendMessage
from ...config.logger import get_logger

logger = get_logger(__name__)


def handle_postback_event(event):
    data = event.postback.data
    if data == "read_terms":
        return [TextSendMessage(text="以下是服務條款 (TODO: 用 flex message 呈現)")]
    elif data == "accept_terms":
        return [TextSendMessage(text="感謝您的回覆")]
    elif data == "reject_terms":
        return [TextSendMessage(text="感謝您的回覆")]
    else:
        return [TextSendMessage(text="請選擇一個選項")]
