# main.py（关键修改：导入utils下的api_client，而非backend/api）
import streamlit as st
from config import init_session_state, load_css, API_BASE_URL
from utils.auth_guard import login_guard
# 核心修改：从utils.api_client导入，复用你现有文件，不新增目录
from utils.api_client import login, register

# 以下所有逻辑完全不变（保留登录页面、拦截器、侧边栏等）
# ====================== 初始化 ======================
init_session_state()
load_css()


# ====================== 右上角登录/注册按钮（修复重复Key） ======================
def render_top_right_user_info():
    with st.container():
        col1, col2, col3 = st.columns([0.92, 0.04, 0.04])
        with col1:
            st.empty()

        # 未登录状态（给按钮加唯一key）
        if not st.session_state.get("login_user"):
            with col2:
                if st.button("登录", use_container_width=True, key="top_login_btn"):  # 唯一key
                    st.session_state.current_page = "登录"
                    st.rerun()
            with col3:
                if st.button("注册", use_container_width=True, key="top_register_btn"):  # 唯一key
                    st.session_state.current_page = "注册"
                    st.rerun()
        # 已登录状态（给按钮加唯一key）
        else:
            col1, col2 = st.columns([0.92, 0.08])
            with col1:
                st.empty()
            with col2:
                st.markdown(f"<span style='color:black; font-weight:bold;'>👤 {st.session_state.login_user}</span>",
                            unsafe_allow_html=True)
                if st.button("退出", use_container_width=True, key="top_logout_btn"):  # 唯一key
                    st.session_state.login_user = None
                    st.session_state.token = None
                    st.rerun()


# ====================== 登录/注册页面（修复重复Key + 优化样式） ======================
def render_login_page():
    """GPT风格登录页面"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">登录</div>', unsafe_allow_html=True)

    # 登录表单
    username = st.text_input("用户名", placeholder="请输入用户名", label_visibility="collapsed", key="login_username")
    password = st.text_input("密码", placeholder="请输入密码", type="password", label_visibility="collapsed",
                             key="login_pwd")

    # 登录按钮加唯一key
    if st.button("登录", use_container_width=True, key="do_login_btn"):
        success, token, username = login(username, password)
        if success:
            st.session_state.login_user = username
            st.session_state.token = token
            st.success("登录成功！正在返回首页...")
            st.session_state.current_page = "智能问答"
            st.rerun()
        else:
            st.error(token)

    # 注册跳转按钮加唯一key
    if st.button("还没有账号？立即注册", use_container_width=True, type="secondary", key="goto_reg_btn"):
        st.session_state.current_page = "注册"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_register_page():
    """GPT风格注册页面"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">注册</div>', unsafe_allow_html=True)

    # 注册表单（加唯一key）
    username = st.text_input("用户名", placeholder="请设置用户名", label_visibility="collapsed", key="reg_username")
    password = st.text_input("密码", placeholder="请设置密码", type="password", label_visibility="collapsed",
                             key="reg_pwd")
    repassword = st.text_input("确认密码", placeholder="请再次输入密码", type="password", label_visibility="collapsed",
                               key="reg_repwd")

    # 注册按钮加唯一key
    if st.button("OK", use_container_width=True, key="do_reg_btn"):
        if password != repassword:
            st.error("两次密码不一致！")
        else:
            success, msg = register(username, password)
            if success:
                st.success("注册成功！跳转到登录页...")
                st.session_state.current_page = "登录"
                st.rerun()
            else:
                st.error(msg)
    st.markdown('</div>', unsafe_allow_html=True)


# ====================== 侧边栏（保留原有逻辑） ======================
def render_sidebar():
    with st.sidebar:
        st.markdown(
            "<h3 style='color: white; margin-bottom: 20px; padding-left: 10px;'>知识库问答系统</h3>",
            unsafe_allow_html=True)

        st.markdown('<div class="sidebar-btn-container">', unsafe_allow_html=True)
        # 侧边栏按钮加唯一key
        if st.button("💬 新聊天", use_container_width=True, key="sidebar_qa_btn"):
            st.session_state.current_page = "智能问答"
            st.rerun()
        if st.button("📤 文档上传", use_container_width=True, key="sidebar_upload_btn"):
            st.session_state.current_page = "文档上传"
            st.rerun()
        if st.button("📖 知识库管理", use_container_width=True, key="sidebar_manage_btn"):
            st.session_state.current_page = "知识库管理"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
        st.markdown(
            f"<p style='color: #888; font-size: 12px; padding-left:10px;'>当前文档数: {len(st.session_state.docs)}</p>",
            unsafe_allow_html=True)


# ====================== 业务页面（弹窗提示版拦截器） ======================
@login_guard  # 登录拦截：未登录显示弹窗提示
def render_qa_page():
    """智能问答页面"""
    from frontend.qa_view import render
    render()


@login_guard
def render_upload_page():
    """文档上传页面"""
    from frontend.upload_view import render
    render()


@login_guard
def render_manage_page():
    """知识库管理页面"""
    from frontend.manage_view import render
    render()


# ====================== 路由分发 ======================
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