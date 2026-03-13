# backend/api/user_api.py
import requests
from config import API_BASE_URL  # 复用你的全局配置


def login(username: str, password: str) -> tuple[bool, str, str]:
    """
    后端登录接口实现（前端调用版）
    返回：(是否成功, token/错误信息, 用户名/空)
    """
    try:
        # 这里是前端调用后端接口的逻辑（如果是前后端分离）
        # 如果是单体应用，直接调用service层：
        # from backend.service.user_service import user_login
        # return user_login(username, password)

        # 前后端分离版示例：
        response = requests.post(
            f"{API_BASE_URL}/api/user/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            return True, data.get("token", ""), data.get("username", "")
        return False, f"登录失败：{response.text}", ""
    except Exception as e:
        return False, f"接口调用失败：{str(e)}", ""


def register(username: str, password: str) -> tuple[bool, str]:
    """
    后端注册接口实现（前端调用版）
    """
    try:
        # 前后端分离版：
        response = requests.post(
            f"{API_BASE_URL}/api/user/register",
            json={"username": username, "password": password}
        )
        if response.status_code == 201:
            return True, ""
        return False, f"注册失败：{response.text}"
    except Exception as e:
        return False, f"接口调用失败：{str(e)}"

# 如果你需要FastAPI后端接口（供前端调用），补充：
# from fastapi import APIRouter
# router = APIRouter(prefix="/api/user", tags=["用户"])

# @router.post("/login")
# def api_login(username: str, password: str):
#     from backend.service.user_service import user_login
#     success, token, username = user_login(username, password)
#     if success:
#         return {"code": 200, "token": token, "username": username}
#     return {"code": 400, "msg": token}

# @router.post("/register")
# def api_register(username: str, password: str):
#     from backend.service.user_service import user_register
#     success, msg = user_register(username, password)
#     if success:
#         return {"code": 201, "msg": "注册成功"}
#     return {"code": 400, "msg": msg}