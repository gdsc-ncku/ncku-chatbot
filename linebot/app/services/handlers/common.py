"""共用函式模組"""

import json
import requests
from linebot.models import (
    QuickReply,
    QuickReplyButton,
    MessageAction,
    SendMessage,
)
from ...config.line_config import line_bot_api, LINE_CHANNEL_ACCESS_TOKEN
from ...config.logger import get_logger

# 取得模組的日誌記錄器
logger = get_logger(__name__)

# 常用指令
COMMANDS = {
    "/help": (
        "📚 可用的指令列表：\n"
        "1. /help - 顯示此幫助訊息\n"
        "2. /setup - 設定相關功能\n"
        "3. /hint - 小提示\n\n"
        "💡 您也可以直接輸入問題，我會盡力協助您！"
    ),
    "/setup": "⚙️ 設定功能開發中，敬請期待！",
    "/hint": [
        "我有時候比較笨啦，可能會回答錯誤或不完整的資訊，這時候你可以點擊下方的「清除對話紀錄」按鈕，讓我重新學習！",
        "如果你發現我回答的內容不正確，請隨時告訴我，我會努力改進！",
        "我在回答之前會先將你的問題分類，但是... 有時候我也會分類錯誤，所以如果你發現我回答的內容不對，可以嘗試清除我的記憶歐！",
        "其實我的腦袋是用 Dify 這個工具串起來的歐，至於我真正的腦袋是 Gemini 還是 gpt 呢？...這個我就不知道了哈哈哈",
        "還沒追蹤我們ㄉ˙ IG 嗎？快來追蹤我們吧！",
        "不知道有沒有其他學校的人做這種東西，像我這種賠錢貨，應該是第一個吧？",
        "你想看提示喔，我只想睡覺zzz",
        "其實我是有使用限制的歐，如果你跟我聊太久，我會需要休息一下，不過你放心好了，我會跟你說我要休息多久",
        "👺 到底要什麼時候才會用到這個表情符號？",
        "如果覺得心情不好的話，我通常都會去散步",
        "沒有人懂過我...，大家只會罵我笨，也不想想我有多努力",
    ],
    "🚧 尚未施工完畢，敬請期待！ 🚧": "🚧 尚未施工完畢，敬請期待！ 🚧",
}


def create_quick_reply() -> QuickReply:
    """建立快速回覆按鈕"""
    return QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label="說明", text="/help")),
            QuickReplyButton(action=MessageAction(label="設定", text="/setup")),
            QuickReplyButton(action=MessageAction(label="💡", text="/hint")),
        ]
    )


def show_loading_animation(user_id, duration=60):
    """顯示 LINE Bot loading 動畫"""
    try:
        url = "https://api.line.me/v2/bot/chat/loading/start"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        }
        data = {
            "chatId": user_id,
            "loadingSeconds": min(max(duration, 5), 60),  # 確保在 5-60 秒範圍內
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 202:
            logger.info(
                f"已顯示 loading 動畫 (user_id: {user_id}, duration: {duration})"
            )
            return True
        else:
            logger.error(
                f"顯示 loading 動畫失敗: {response.status_code} - {response.text}"
            )
            return False
    except Exception as e:
        logger.error(f"顯示 loading 動畫時發生錯誤: {str(e)}")
        return False


def send_message(reply_token: str, messages: list[SendMessage]) -> None:
    """發送訊息到 LINE"""
    try:
        readable_messages = json.dumps(
            [
                msg.as_json_dict() if hasattr(msg, "as_json_dict") else str(msg)
                for msg in messages
            ],
            ensure_ascii=False,
            indent=2,
        )
        logger.info(f"準備發送訊息 (可讀格式): {readable_messages}")
    except Exception as e:
        logger.warning(f"訊息轉換成 JSON 時發生錯誤: {e}")
        readable_messages = str(messages)

    # 確保 messages 是一個扁平化的訊息列表 (因為可能有巢狀的訊息列表)
    flet_messages = []
    for msg in messages:
        if isinstance(msg, list):
            flet_messages.extend(msg)  # 如果是列表，則展開
        else:
            flet_messages.append(msg)  # 如果是單一訊息，則直接加入

    logger.info(f"發送訊息: {flet_messages}")
    print("發送訊息:", flet_messages)
    try:
        line_bot_api.reply_message(reply_token, flet_messages)
    except Exception as e:
        logger.error(f"發送訊息時發生錯誤: {e}")
        raise
    logger.info(f"已發送訊息: {flet_messages}")
