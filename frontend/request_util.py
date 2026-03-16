import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

def req_post(url, data):
    headers = {}
    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.post(API_BASE + url, json=data, headers=headers)

def req_get(url):
    headers = {}
    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(API_BASE + url, headers=headers)