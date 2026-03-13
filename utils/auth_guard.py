# utils/auth_guard.py（弹窗提示版）
import streamlit as st

def login_guard(func):
    """
    登录拦截器装饰器（弹窗提示版）
    """
    def wrapper(*args, **kwargs):
        if not st.session_state.get("login_user"):
            # 弹窗提示（替代原文字提示）
            st.toast("⚠️ 请先登录后再操作！", icon="⚠️")
            # 可选：强制跳转到登录页
            # st.session_state.current_page = "登录"
            # st.rerun()
            return None
        return func(*args, **kwargs)
    return wrapper

def check_login_status() -> bool:
    """简单检查登录状态"""
    return bool(st.session_state.get("login_user"))