from linebot.models import (
    TextSendMessage,
    FlexSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
)
from ...config.logger import get_logger
from ..utils import flex_message_convert_to_json
from ...repositories.user_repository import UserRepository

logger = get_logger(__name__)
user_repository = UserRepository()

WELCOME_MESSAGE_AFTER_SETTING = """👋 嗨！歡迎使用「成大 Linebot」🌳✨
無論是校園資訊、活動查詢、選課資訊還是校內生活大小事，我都可以為你服務！
你可以試試點選下方泡泡來問我
或者直接傳訊息給我吧！我會盡快幫你找到答案喔～😉
有問題也隨時告訴我，讓你的校園生活更便利！"""

TERMS_MESSAGE = """📜 服務條款
    NCKU Chatbot 的回覆基於現有資料與自然語言處理技術，可能存在誤差或未能即時更新的情況。使用者應自行判斷回覆內容的準確性，並以學校官方公告與相關單位提供的資訊為準。本服務不對因使用 NCKU Chatbot 所產生的任何後果負責。

    我們的資料涵蓋到「宿舍」「社團」「學校活動」「課程」「常見行政手續」「成大法規彙編」等七大主題。請注意，本服務僅提供輔助資訊，具體內容仍應以學校官方公告為準。使用者在使用本服務時，應遵守學校相關規定與法律法規，並對自己的行為負責。"""


def create_quickreply():
    return QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label="說明", text="/help")),
            QuickReplyButton(action=MessageAction(label="設定", text="/setup")),
        ]
    )


def handle_postback_event(event):
    data = event.postback.data
    user_id = event.source.user_id
    if data == "read_terms":
        logger.info(f"User {user_id} requested to read terms.")
        return [
            TextSendMessage(text=f"{TERMS_MESSAGE}"),
            FlexSendMessage(
                alt_text="請閱讀服務條款",
                contents=flex_message_convert_to_json(
                    "flex_messages/welcome/terms.json"
                ),
            ),
        ]
    elif data == "accept_terms":
        logger.info(f"User {user_id} accepted terms.")
        user_repository.update_accpted_terms(user_id, True)
        return [
            TextSendMessage(text="感謝您的回覆，接下來我們來設定您的個人資料吧！"),
            FlexSendMessage(
                alt_text="請選擇語言",
                contents=flex_message_convert_to_json(
                    "flex_messages/welcome/language.json"
                ),
            ),
        ]
    elif data == "reject_terms":
        logger.info(f"User {user_id} rejected terms.")
        user_repository.update_accpted_terms(user_id, False)
        return [TextSendMessage(text="感謝您的回覆，如果有需要隨時可以點擊同意歐")]
    elif data == "zh-TW":
        user_repository.update_language(user_id, "zh-TW")
        return [
            TextSendMessage(text="感謝您的回覆，接下來我們來設定您的個人資料吧！"),
            FlexSendMessage(
                alt_text="請選擇您的身份",
                contents=flex_message_convert_to_json(
                    "flex_messages/welcome/role.json"
                ),
            ),
        ]
    elif data == "en":
        logger.info(f"User {user_id} selected English language.")
        user_repository.update_language(user_id, "en")
        return [
            TextSendMessage(
                text="Thank you for your reply, let's set up your profile next!"
            ),
            FlexSendMessage(
                alt_text="Please select your identity",
                contents=flex_message_convert_to_json(
                    "flex_messages/welcome/role.json"
                ),
            ),
        ]
    elif data == "role_faculty":
        logger.info(f"User {user_id} selected faculty role.")
        user_repository.update_roles(user_id, "faculty")
        return [
            TextSendMessage(text="您已經設定為教職員身份，鵝子歡迎您！"),
            TextSendMessage(
                text=WELCOME_MESSAGE_AFTER_SETTING, quick_reply=create_quickreply()
            ),
        ]
    elif data == "role_student":
        logger.info(f"User {user_id} selected student role.")
        user_repository.update_roles(user_id, "student")
        return [
            TextSendMessage(text="您已經設定為學生身份，鵝子歡迎您！"),
            TextSendMessage(
                text=WELCOME_MESSAGE_AFTER_SETTING, quick_reply=create_quickreply()
            ),
        ]
    elif data == "role_visitor":
        logger.info(f"User {user_id} selected visitor role.")
        user_repository.update_roles(user_id, "visitor")
        return [
            TextSendMessage(text="您已經設定為校外人士身份"),
            TextSendMessage(
                text=WELCOME_MESSAGE_AFTER_SETTING, quick_reply=create_quickreply()
            ),
        ]
    else:
        logger.warning(f"Unknown postback data: {data} from user {user_id}")
