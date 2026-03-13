# utils/api_client.py（完整修改版，保留你原有业务逻辑）
import requests
from config import API_BASE_URL

# ========== 保留你原有的业务接口（如下示例，根据你的实际代码调整） ==========
def upload_document(token: str, file_path: str):
    """上传文档接口（你的原有逻辑）"""
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_BASE_URL}/api/upload", headers=headers, files=files)
    return response.json()

def qa_chat(token: str, question: str):
    """智能问答接口（你的原有逻辑）"""
    headers = {"Authorization": f"Bearer {token}"}
    data = {"question": question}
    response = requests.post(f"{API_BASE_URL}/api/qa", headers=headers, json=data)
    return response.json()

# ========== 新增登录/注册接口（只发HTTP请求，无FastAPI依赖） ==========
def login(username: str, password: str) -> tuple[bool, str, str]:
    """前端登录接口调用（纯HTTP请求，不导入后端代码）"""
    try:
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
    """前端注册接口调用（纯HTTP请求）"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/user/register",
            json={"username": username, "password": password}
        )
        if response.status_code == 201:
            return True, ""
        return False, f"注册失败：{response.text}"
    except Exception as e:
        return False, f"接口调用失败：{str(e)}"