from sqlalchemy.orm import Session
from ..models.user import User
from ..db.database import SessionLocal


class UserRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_user(self, line_id: str) -> User:
        """取得用戶資料，如果不存在則創建新用戶"""
        user = self.db.query(User).filter(User.line_id == line_id).first()
        if not user:
            user = User(line_id=line_id)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user

    def update_conversation_id(self, line_id: str, conversation_id: str) -> None:
        """更新用戶的對話 ID"""
        user = self.get_user(line_id)
        user.conversation_id = conversation_id
        self.db.commit()

    def __del__(self):
        """確保資料庫連接被正確關閉"""
        self.db.close()
