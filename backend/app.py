from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.api import user_api, upload_api, qa_api, manage_api, history_api
from backend.interceptor.auth_interceptor import auth_interceptor
# ✅ 导入settings配置
from settings import BACKEND_CONFIG

app = FastAPI()

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

# 挂载路由
app.include_router(user_api.router)
app.include_router(upload_api.router)
app.include_router(qa_api.router)
app.include_router(history_api.router)
app.include_router(manage_api.router)

@app.get("/")
def root():
    return {"message": "AI 知识库后端运行正常"}

import uvicorn
if __name__ == '__main__':
    # ✅ 从配置文件读取，不再硬编码
    uvicorn.run(
        "main:app",
        host=BACKEND_CONFIG["host"],
        port=BACKEND_CONFIG["port"],
        reload=BACKEND_CONFIG["reload"]
    )