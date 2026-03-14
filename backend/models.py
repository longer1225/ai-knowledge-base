from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY, BIGINT
from sqlalchemy.sql import func
from .database import Base

# 用户表（对应users）
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    create_time = Column(DateTime, default=func.current_timestamp())
    update_time = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

# 文档表（对应documents）
class Document(Base):
    __tablename__ = "documents"

    doc_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # 关联用户ID（必填）
    doc_name = Column(String(255), nullable=False)  # 对应原name
    doc_type = Column(String(50), nullable=False)  # 对应原file_type
    upload_time = Column(DateTime, default=func.current_timestamp())
    file_size = Column(BIGINT)  # 对应原size（文件大小用BIGINT更合理）
    status = Column(String(20), default="processed")  # 文档状态

# 文档分块表（对应document_chunks）
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc_id = Column(Integer, nullable=False)  # 关联文档ID
    chunk_text = Column(Text, nullable=False)  # 对应原content
    chunk_embedding = Column(ARRAY(Float), nullable=False)  # 对应原embedding
    chunk_index = Column(Integer)  # 分块索引
    create_time = Column(DateTime, default=func.current_timestamp())

# 问答历史表（对应qa_history）
class QAHistory(Base):
    __tablename__ = "qa_history"

    qa_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # 关联用户ID（必填）
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    source_chunks = Column(Text)  # 来源分块
    similarity_scores = Column(Text)  # 相似度分数（补充缺失字段）
    create_time = Column(DateTime, default=func.current_timestamp())