# ==============================================
# 👇 这四行必须放在最最最顶部！修复路径问题
# ==============================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from config.frontend_config import init_session_state, load_css
from utils.auth_guard import login_guard

# 页面导入（全部拆出去了）
from frontend.auth_pages import render_login_page, render_register_page

init_session_state()
load_css()

# ====================== 右上角用户栏 ======================
def render_top_right_user_info():
    with st.container():
        col1, col2, col3 = st.columns([8, 1, 1])
        if not st.session_state.get("login_user"):
            with col2:
                if st.button("登录", use_container_width=True, key="top_login_btn"):
                    st.session_state.current_page = "登录"
                    st.rerun()
            with col3:
                if st.button("注册", use_container_width=True, key="top_register_btn"):
                    st.session_state.current_page = "注册"
                    st.rerun()
        else:
            col_empty, col_name, col_logout = st.columns([8, 1.5, 0.5])
            with col_name:
                st.markdown(f"<div style='text-align:right; padding-top:10px; color:#ECECEC;'>👤 {st.session_state.login_user}</div>", unsafe_allow_html=True)
            with col_logout:
                if st.button("退出", use_container_width=True, key="top_logout_btn"):
                    st.session_state.login_user = None
                    st.session_state.token = None
                    st.rerun()

# ====================== 侧边栏 ======================
def render_sidebar():
    with st.sidebar:
        st.markdown("<h3 style='color:white;'>知识库问答系统</h3>", unsafe_allow_html=True)
        if st.button("💬 新聊天", use_container_width=True):
            st.session_state.current_page = "智能问答"
            st.rerun()
        if st.button("📤 文档上传", use_container_width=True):
            st.session_state.current_page = "文档上传"
            st.rerun()
        if st.button("📖 知识库管理", use_container_width=True):
            st.session_state.current_page = "知识库管理"
            st.rerun()

# ====================== 业务页面 ======================
@login_guard
def render_qa_page():
    from frontend.qa_view import render
    render()

@login_guard
def render_upload_page():
    from frontend.upload_view import render
    render()

@login_guard
def render_manage_page():
    from frontend.manage_view import render
    render()

# ====================== 路由 ======================
def main():
    render_top_right_user_info()
    render_sidebar()
    page = st.session_state.current_page

    if page == "智能问答":
        render_qa_page()
    elif page == "文档上传":
        render_upload_page()
    elif page == "知识库管理":
        render_manage_page()
    elif page == "登录":
        render_login_page()
    elif page == "注册":
        render_register_page()

if __name__ == "__main__":
    main()