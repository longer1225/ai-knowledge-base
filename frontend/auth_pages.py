import streamlit as st
import requests
from config.backend_base_settings import API_BASE_URL

def render_login_page():
    _, center_col, _ = st.columns([1, 1.5, 1])

    with center_col:
        st.markdown('<h2 style="text-align:center; color:white; margin-top:15vh;">欢迎登录</h2>', unsafe_allow_html=True)

        username = st.text_input("用户名", placeholder="请输入用户名", label_visibility="collapsed", key="login_username")
        password = st.text_input("密码", placeholder="请输入密码", type="password", label_visibility="collapsed", key="login_pwd")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("登录", use_container_width=True, type="primary", key="login_btn"):
            if not username or not password:
                st.warning("请输入用户名和密码")
                return

            try:
                res = requests.post(f"{API_BASE_URL}/api/user/login", json={"username": username, "password": password})
                data = res.json()

                if data.get("code") == 0:
                    st.session_state.login_user = data["data"]["username"]
                    st.session_state.token = data["data"]["access_token"]
                    st.toast("✅ 登录成功！")
                    st.session_state.current_page = "智能问答"
                    st.rerun()
                else:
                    st.error(data.get("msg", "登录失败"))
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

        if st.button("还没有账号？立即注册", use_container_width=True, key="goto_register"):
            st.session_state.current_page = "注册"
            st.rerun()

def render_register_page():
    _, center_col, _ = st.columns([1, 1.5, 1])

    with center_col:
        st.markdown('<h2 style="text-align:center; color:white; margin-top:15vh;">创建新账号</h2>', unsafe_allow_html=True)

        username = st.text_input("用户名", placeholder="请设置用户名", label_visibility="collapsed", key="reg_username")
        password = st.text_input("密码", placeholder="请设置密码", type="password", label_visibility="collapsed", key="reg_pwd")
        repassword = st.text_input("确认密码", placeholder="请再次输入密码", type="password", label_visibility="collapsed", key="reg_repwd")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("注册", use_container_width=True, type="primary", key="register_btn"):
            if not username or not password:
                st.warning("请输入完整信息")
                return
            if password != repassword:
                st.error("两次密码不一致")
                return

            try:
                res = requests.post(f"{API_BASE_URL}/api/user/register", json={"username": username, "password": password})
                data = res.json()

                if data.get("code") == 0:
                    st.success("✅ 注册成功！请登录")
                    st.session_state.current_page = "登录"
                    st.rerun()
                else:
                    st.error(data.get("msg", "注册失败"))
            except Exception as e:
                st.error(f"请求失败: {str(e)}")

        if st.button("返回登录", use_container_width=True, key="goto_login"):
            st.session_state.current_page = "登录"
            st.rerun()