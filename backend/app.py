from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.api import user_api, upload_api, qa_api, manage_api, history_api
from backend.interceptor.auth_interceptor import auth_interceptor
from backend.interceptor.exception_handler import global_exception_handler
from backend.api import chat_api
from backend.service.auto_upload_service import start_auto_upload_scanner

# ✅ 统一使用新配置
from config.backend_base_settings import BACKEND_CONFIG
from utils.logger import logger

app = FastAPI(title="AI 知识库后端", version="1.0")

# 全局异常捕获（你写的全局异常处理器）
app.add_exception_handler(Exception, global_exception_handler)

# CORS 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动自动文件扫描服务 🔥
@app.on_event("startup")
def startup_event():
    logger.info("✅ 后端服务启动完成")
    start_auto_upload_scanner(user_id=1)  # 默认给1号管理员自动入库

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

# 启动
import uvicorn
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=BACKEND_CONFIG["host"],
        port=BACKEND_CONFIG["port"],
        reload=BACKEND_CONFIG.get("reload", True)  # 👈 自动兼容，不报错
    )