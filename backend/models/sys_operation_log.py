# backend/models/sys_log.py
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from datetime import datetime
from backend.core.database import Base


class SysOperationLog(Base):
    __tablename__ = "sys_operation_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=True)
    operation = Column(String(50), nullable=False)    # 操作名称：用户登录、文档上传、AI提问
    module = Column(String(50), nullable=False)         # 所属模块：用户管理、文档知识库、对话问答
    content = Column(Text, nullable=True)              # 操作详细描述
    ip = Column(String(50), nullable=True)             # 客户端IP
    create_time = Column(DateTime, default=datetime.now)