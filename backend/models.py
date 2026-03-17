from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY, BIGINT, ForeignKey
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

# 多对话窗口表
class Chat(Base):
    __tablename__ = "chat"

    chat_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    create_time = Column(TIMESTAMP, server_default=func.now())

    # 关系
    user = relationship("User", back_populates="chats")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    create_time = Column(DateTime, default=func.current_timestamp())
    update_time = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    chats = relationship("Chat", back_populates="user", cascade="all, delete")  # 加这行


class Document(Base):
    __tablename__ = "documents"

    doc_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    doc_name = Column(String(255), nullable=False)
    doc_type = Column(String(50), nullable=False)
    upload_time = Column(DateTime, default=func.current_timestamp())
    file_size = Column(BIGINT)
    status = Column(String(20), default="processed")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc_id = Column(Integer, ForeignKey("documents.doc_id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_embedding = Column(ARRAY(Float), nullable=False)
    chunk_index = Column(Integer)
    create_time = Column(DateTime, default=func.current_timestamp())


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