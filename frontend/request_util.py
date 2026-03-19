import streamlit as st
import requests
from backend.config.backend_base_settings import API_BASE_URL

# 封装请求头
def get_headers():
    headers = {"Content-Type": "application/json"}
    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# 统一解析 JSON（你原来的，不动）
def parse_response(res):
    data = res.json()
    code = data.get("code")
    msg = data.get("msg")
    if code != 0:
        st.toast(f"❌ {msg}")
        return None
    return data

# GET（不动）
def req_get(url):
    res = requests.get(API_BASE_URL + url, headers=get_headers(), timeout=10)
    return parse_response(res)

# POST（不动）
def req_post(url, data):
    res = requests.post(API_BASE_URL + url, json=data, headers=get_headers(), timeout=10)
    return parse_response(res)

# DELETE（不动）
def req_delete(url):
    res = requests.delete(API_BASE_URL + url, headers=get_headers(), timeout=10)
    return parse_response(res)

# ==============================================
# 🔥 🔥 🔥 【新增】流式 POST 请求（专门给 AI 用）
# ==============================================
def req_stream_post(url, data):
    url = API_BASE_URL + url
    headers = get_headers()

    # 发起流式请求
    response = requests.post(
        url,
        json=data,
        headers=headers,
        stream=True,  # 关键：开启流式
        timeout=30
    )

    answer = ""
    placeholder = st.empty()  # 流式打字机效果

    for chunk in response.iter_lines():
        if chunk:
            # 解析 SSE 格式
            chunk_str = chunk.decode("utf-8").replace("data:", "").strip()
            answer += chunk_str
            placeholder.markdown(answer)  # 实时更新

    return answer