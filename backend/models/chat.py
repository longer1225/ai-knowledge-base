from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY, BIGINT, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

class Chat(Base):
    __tablename__ = "chat"

    chat_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    create_time = Column(TIMESTAMP, server_default=func.now())

    # 关系
    user = relationship("User", back_populates="chats")