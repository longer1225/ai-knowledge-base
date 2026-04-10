from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY, BIGINT, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = "documents"

    doc_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    doc_name = Column(String(255), nullable=False)
    doc_type = Column(String(50), nullable=False)
    upload_time = Column(DateTime, default=func.current_timestamp())
    file_size = Column(BIGINT)
    status = Column(String(20), default="processed")

