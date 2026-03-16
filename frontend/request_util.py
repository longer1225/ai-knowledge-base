import streamlit as st
import requests

# ✅ 关键修复：导入统一配置的 API_BASE_URL
from settings import API_BASE_URL

# 封装请求头（自动带 token）
def get_headers():
    headers = {"Content-Type": "application/json"}
    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# GET 请求（把 API_BASE 改成 API_BASE_URL）
def req_get(url):
    return requests.get(
        API_BASE_URL + url,  # ✅ 改这里
        headers=get_headers(),
        timeout=10
    )

# POST 请求（把 API_BASE 改成 API_BASE_URL）
def req_post(url, data):
    return requests.post(
        API_BASE_URL + url,  # ✅ 改这里
        json=data,
        headers=get_headers(),
        timeout=10
    )

# DELETE 请求（把 API_BASE 改成 API_BASE_URL）
def req_delete(url):
    return requests.delete(
        API_BASE_URL + url,  # ✅ 改这里
        headers=get_headers(),
        timeout=10
    )