import requests

from backend.service.user_service import login_user, register_user
from config import API_BASE_URL

# 登录接口调用
from backend.database import get_db


def login(username: str, password: str):
    db = next(get_db())
    return login_user(db, username, password)

def register(username: str, password: str):
    db = next(get_db())
    return register_user(db, username, password)

# 保留你原有业务接口（upload_document/qa_chat等）
def upload_document(token: str, file_path: str):
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_BASE_URL}/api/upload", headers=headers, files=files)
    return response.json()

def qa_chat(token: str, question: str):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"question": question}
    response = requests.post(f"{API_BASE_URL}/api/qa", headers=headers, json=data)
    return response.json()