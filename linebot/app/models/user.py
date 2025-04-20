# use sqlite
from sqlalchemy import Column, Integer, String
from app.db.database import Base
from dataclasses import dataclass
from typing import Optional


class User(Base):
    __tablename__ = "users"

    line_id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<User line_id={self.line_id}>"


@dataclass
class UserModel:
    line_id: str
    conversation_id: Optional[str] = None
