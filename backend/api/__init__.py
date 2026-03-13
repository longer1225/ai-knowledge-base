# backend/api/__init__.py
from fastapi import FastAPI
from ..database import engine, Base
from . import upload_api, qa_api, history_api

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建主 APP
app = FastAPI(title="AI知识库问答系统")

# 挂载所有子路由（你三个模块）
app.include_router(upload_api.router)
app.include_router(qa_api.router)
app.include_router(history_api.router)