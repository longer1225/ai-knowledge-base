# backend/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.api import user_api, upload_api, qa_api, history_api

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载所有 API 路由（这一行非常关键）
app.include_router(user_api.router)


@app.get("/")
def root():
    return {"message": "AI 知识库后端运行正常"}