from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.api import user_api, upload_api, qa_api, manage_api
# 👇 这行是你现在的正确路径
from backend.interceptor.auth_interceptor import auth_interceptor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局登录拦截（你改名后的）
@app.middleware("http")
async def apply_auth(request, call_next):
    return await auth_interceptor(request, call_next)

# 挂载路由
app.include_router(user_api.router)
app.include_router(upload_api.router)
app.include_router(qa_api.router)

app.include_router(manage_api.router)

@app.get("/")
def root():
    return {"message": "AI 知识库后端运行正常"}

import uvicorn
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )