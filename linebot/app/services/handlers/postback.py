from linebot.models import (
    TextSendMessage,
    FlexSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
)
from ...config.logger import get_logger
from ...config.line_config import line_bot_api
from ..utils import flex_message_convert_to_json
from ...repositories.user_repository import UserRepository

logger = get_logger(__name__)
user_repository = UserRepository()

WELCOME_MESSAGE_AFTER_SETTING = """👋 嗨！歡迎使用「成大 Linebot」🌳✨
無論是校園資訊、活動查詢、選課資訊還是校內生活大小事，我都可以為你服務！
你可以試試點選下方泡泡來問我
或者直接傳訊息給我吧！我會盡快幫你找到答案喔～😉
有問題也隨時告訴我，讓你的校園生活更便利！
(小提示：如果你發現我變笨了，可以試著點選「清除對話紀錄」來重置我，這樣我就能重新學習了！)"""

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


def create_example_question_quickreply(questions: list[str]):
    return QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label=question, text=f"{question}"))
            for question in questions
        ]
    )


def handle_postback_event(event):
    data = event.postback.data
    user_id = event.source.user_id
    user_profile = line_bot_api.get_profile(user_id)
    user_display_name = user_profile.display_name
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
    elif data == "clear_conversation_id":
        logger.info(f"User {user_id} requested to clear conversation ID.")
        return_value = user_repository.update_conversation_id(user_id, "")
        logger.info(f"Conversation ID cleared for user {user_id}: {return_value}")
        return [
            TextSendMessage(
                text=f"逼..嗶茲..！＠清除對話紀錄成功，雖然我忘了這段時間和{user_display_name}的點點滴滴，不過我還是期待和你重新開始吧！"
            )
        ]
    elif data == "reset_user":
        logger.info(f"User {user_id} requested to reset user data.")
        user_repository.update_conversation_id(user_id, "")
        user_repository.update_accpted_terms(user_id, False)
        user_repository.update_language(user_id, "zh-TW")
        user_repository.update_roles(user_id, "visitor")
        return [
            TextSendMessage(text=f"已清空{user_display_name}的資料，請開始設定吧"),
            FlexSendMessage(
                alt_text="請閱讀服務條款",
                contents=flex_message_convert_to_json(
                    "flex_messages/welcome/terms.json"
                ),
            ),
        ]
    ### Example Questions using quick reply
    elif data == "example_question_law":
        logger.info(f"User {user_id} requested example question for law.")
        return [
            TextSendMessage(
                text="以下是一些關於成大法規的問題範例，您可以點選其中一個來詢問我：",
                quick_reply=create_example_question_quickreply(
                    [
                        "請告訴我成大流浪動物相關法規",
                        "宿舍違規審議小組是什麼",
                        "查詢圖書館室內空間使用規定",
                    ]
                ),
            )
        ]
    elif data == "example_question_housing":
        logger.info(f"User {user_id} requested example question for housing.")
        return [
            TextSendMessage(
                text="以下是一些關於宿舍的問題範例，您可以點選其中一個來詢問我：",
                quick_reply=create_example_question_quickreply(
                    ["光二宿舍熱水時間", "住宿服務組在哪裡？", "宿舍收費標準？"]
                ),
            )
        ]
    elif data == "example_question_club":
        logger.info(f"User {user_id} requested example question for club.")
        return [
            TextSendMessage(
                text="以下是一些關於社團的問題範例，您可以點選其中一個來詢問我：",
                quick_reply=create_example_question_quickreply(
                    [
                        "有沒有推薦的戶外社團？",
                        "學校有熱舞社嗎？",
                        "成大服務性質的社團有哪些？",
                    ]
                ),
            )
        ]
    elif data == "example_question_activity":
        logger.info(f"User {user_id} requested example question for activity.")
        return [
            TextSendMessage(
                text="以下是一些關於學校活動的問題範例，您可以點選其中一個來詢問我：",
                quick_reply=create_example_question_quickreply(
                    [
                        "成大的活動如何報名?",
                        "我可以取消報名嗎？",
                        "下星期成大的活動有哪些?",
                        "有什麼通識講座可以參加?",
                    ]
                ),
            )
        ]
    elif data == "example_question_course":
        logger.info(f"User {user_id} requested example question for course.")
        return [
            TextSendMessage(
                text="以下是一些關於課程的問題範例，您可以點選其中一個來詢問我：",
                quick_reply=create_example_question_quickreply(
                    [
                        "有又甜又涼的通識嗎？",
                        "有推薦的國文課嗎？",
                        "成大有開設AI相關的課程嗎？",
                    ]
                ),
            )
        ]
    elif data == "example_question_admin_procedure":
        logger.info(f"User {user_id} requested example question for admin procedure.")
        return [
            TextSendMessage(
                text="以下是一些關於常見行政手續的問題範例，您可以點選其中一個來詢問我：",
                quick_reply=create_example_question_quickreply(
                    ["機車證申請方式?", "學費申請流程?", "新生資料表填寫?"]
                ),
            )
        ]
    else:
        logger.warning(f"Unknown postback data: {data} from user {user_id}")
