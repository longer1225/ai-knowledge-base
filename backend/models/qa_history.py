from backend.core.database import Base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY, BIGINT, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship


class QAHistory(Base):
    __tablename__ = "qa_history"

    qa_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    source_chunks = Column(Text)
    similarity_scores = Column(Text)
    create_time = Column(DateTime, default=func.current_timestamp())
    chat_id = Column(Integer, nullable=True)  # 加这行