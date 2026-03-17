import streamlit as st
import requests

# ✅ 关键修复：导入统一配置的 API_BASE_URL
from config.backend_base_settings import API_BASE_URL

# 封装请求头（自动带 token）
def get_headers():
    headers = {"Content-Type": "application/json"}
    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# ==============================
# 👇 只在这里加统一解析
# ==============================
def parse_response(res):
    data = res.json()
    code = data.get("code")
    msg = data.get("msg")

    # 后端抛出的业务异常
    if code != 0:
        st.toast(f"❌ {msg}")
        return None  # 告诉前端失败了

    # 正常返回
    return data

# GET 请求
def req_get(url):
    res = requests.get(
        API_BASE_URL + url,
        headers=get_headers(),
        timeout=10
    )
    return parse_response(res)  # 👈 只加这一句

# POST 请求
def req_post(url, data):
    res = requests.post(
        API_BASE_URL + url,
        json=data,
        headers=get_headers(),
        timeout=10
    )
    return parse_response(res)  # 👈 只加这一句

# DELETE 请求
def req_delete(url):
    res = requests.delete(
        API_BASE_URL + url,
        headers=get_headers(),
        timeout=10
    )
    return parse_response(res)  # 👈 只加这一句