from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY
from sqlalchemy.sql import func
from .database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    file_type = Column(String(50))
    upload_time = Column(DateTime, default=func.now())

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
    chunk_index = Column(Integer)

class QAHistory(Base):
    __tablename__ = "qa_history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    source_chunks = Column(Text)  # 补上这个字段！
    create_time = Column(DateTime, default=func.now())