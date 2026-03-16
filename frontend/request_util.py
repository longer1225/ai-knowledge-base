import streamlit as st
import requests

# 统一端口，以后只改这里
API_BASE = "http://127.0.0.1:8001"

# 封装请求头（自动带 token）
def get_headers():
    headers = {"Content-Type": "application/json"}
    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# GET 请求
def req_get(url):
    return requests.get(
        API_BASE + url,
        headers=get_headers(),
        timeout=10
    )

# POST 请求
def req_post(url, data):
    return requests.post(
        API_BASE + url,
        json=data,
        headers=get_headers(),
        timeout=10
    )

# DELETE 请求（给删除文档用）
def req_delete(url):
    return requests.delete(
        API_BASE + url,
        headers=get_headers(),
        timeout=10
    )