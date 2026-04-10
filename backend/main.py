import os
from socket import socket

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.api import (
    user_api,
    upload_api,
    qa_api,
    manage_api,
    history_api,
    chat_api
)
from backend.interceptor.auth_interceptor import auth_interceptor
from backend.interceptor.exception_handler import global_exception_handler
from backend.service.auto_upload_service import start_auto_upload_scanner

from backend.config.backend_base_settings import BACKEND_CONFIG, DB_CONFIG
from backend.utils.logger import logger


# 🔥 新版 FastAPI 生命周期（替换旧的 on_event，无警告）
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    logger.info("✅ 后端服务启动完成")
    start_auto_upload_scanner(user_id=1)
    yield
    # 关闭时执行（可选）
    logger.info("🛑 后端服务已关闭")


# 初始化 FastAPI
app = FastAPI(
    title="AI 知识库后端",
    version="1.0",
    lifespan=lifespan  # 🔥 新写法，无废弃警告
)

# 全局异常捕获
app.add_exception_handler(Exception, global_exception_handler)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局登录拦截
@app.middleware("http")
async def apply_auth(request, call_next):
    return await auth_interceptor(request, call_next)


# 挂载所有路由
app.include_router(user_api.router)
app.include_router(upload_api.router)
app.include_router(qa_api.router)
app.include_router(history_api.router)
app.include_router(manage_api.router)
app.include_router(chat_api.router)


# 健康检查
@app.get("/")
def root():
    return {"message": "AI 知识库后端运行正常 ✅"}


# 启动入口（🔥🔥🔥 这里彻底修复！！！）
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",  # <-- 已修复！你的文件名是 app.py！
        host=BACKEND_CONFIG["host"],
        port=BACKEND_CONFIG["port"],
        reload=BACKEND_CONFIG.get("reload", True)
    )