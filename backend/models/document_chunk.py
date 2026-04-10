from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY, BIGINT, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc_id = Column(Integer, ForeignKey("documents.doc_id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_embedding = Column(ARRAY(Float), nullable=False)
    chunk_index = Column(Integer)
    create_time = Column(DateTime, default=func.current_timestamp())