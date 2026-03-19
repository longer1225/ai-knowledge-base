from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY, BIGINT, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    create_time = Column(DateTime, default=func.current_timestamp())
    update_time = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    chats = relationship("Chat", back_populates="user", cascade="all, delete")  # 加这行