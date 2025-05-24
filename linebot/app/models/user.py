# use sqlite
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
from dataclasses import dataclass
from typing import Optional


class User(Base):
    __tablename__ = "users"

    line_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    conversation_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    roles: Mapped[str] = mapped_column(String, default="role_student")
    accpted_terms: Mapped[bool] = mapped_column(default=False)
    language: Mapped[str] = mapped_column(String, default="zh-TW")

    def __repr__(self):
        return f"<User line_id={self.line_id}>"


@dataclass
class UserModel:
    line_id: str
    conversation_id: Optional[str] = None
