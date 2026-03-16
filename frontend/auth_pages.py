import streamlit as st
import requests

from settings import API_BASE_URL


# =========================
# 登录页面
# =========================
def render_login_page():
    _, center_col, _ = st.columns([1, 1.5, 1])

    with center_col:
        st.markdown(
            '<h2 style="text-align:center; color:white; margin-top:15vh;">欢迎登录</h2>',
            unsafe_allow_html=True
        )

        username = st.text_input(
            "用户名",
            placeholder="请输入用户名",
            label_visibility="collapsed",
            key="login_username"
        )

        password = st.text_input(
            "密码",
            placeholder="请输入密码",
            type="password",
            label_visibility="collapsed",
            key="login_pwd"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 登录按钮
        if st.button("登录", use_container_width=True, type="primary", key="login_btn"):

            st.write("登录按钮被点击")

            if not username or not password:
                st.warning("请输入用户名和密码")
                return

            try:
                st.write("准备发送登录请求")

                response = requests.post(
                    f"{API_BASE_URL}/api/user/login",
                    json={
                        "username": username,
                        "password": password
                    }
                )

                st.write("请求发送完成")
                st.write("状态码:", response.status_code)
                st.write("返回:", response.text)

                data = response.json()

                if data["code"] == 200:

                    st.session_state.login_user = data["username"]
                    st.session_state.token = data["access_token"]

                    st.toast("登录成功！", icon="✅")

                    st.session_state.current_page = "智能问答"
                    st.rerun()

                else:
                    st.error(data["msg"])

            except Exception as e:
                st.error(f"请求失败: {str(e)}")

        # 跳转注册
        if st.button("还没有账号？立即注册", use_container_width=True, key="goto_register"):
            st.session_state.current_page = "注册"
            st.rerun()


# =========================
# 注册页面
# =========================
def render_register_page():
    _, center_col, _ = st.columns([1, 1.5, 1])

    with center_col:
        st.markdown(
            '<h2 style="text-align:center; color:white; margin-top:15vh;">创建新账号</h2>',
            unsafe_allow_html=True
        )

        username = st.text_input(
            "用户名",
            placeholder="请设置用户名",
            label_visibility="collapsed",
            key="reg_username"
        )

        password = st.text_input(
            "密码",
            placeholder="请设置密码",
            type="password",
            label_visibility="collapsed",
            key="reg_pwd"
        )

        repassword = st.text_input(
            "确认密码",
            placeholder="请再次输入密码",
            type="password",
            label_visibility="collapsed",
            key="reg_repwd"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 注册按钮
        if st.button("注册", use_container_width=True, type="primary", key="register_btn"):

            st.write("注册按钮被点击")

            if not username or not password:
                st.warning("请输入完整信息")
                return

            if password != repassword:
                st.error("两次密码不一致")
                return

            try:

                st.write("准备发送注册请求")

                response = requests.post(
                    f"{API_BASE_URL}/api/user/register",
                    json={
                        "username": username,
                        "password": password
                    }
                )

                st.write("请求发送完成")
                st.write("状态码:", response.status_code)
                st.write("返回:", response.text)

                data = response.json()

                if data["code"] == 200:
                    st.success("注册成功！请登录")

                    st.session_state.current_page = "登录"
                    st.rerun()

                else:
                    st.error(data["msg"])

            except requests.exceptions.ConnectionError:
                st.error("连接后端失败，请确认 FastAPI 在 8000 端口运行")

            except Exception as e:
                st.error(f"请求失败: {str(e)}")

        # 返回登录
        if st.button("返回登录", use_container_width=True, key="goto_login"):
            st.session_state.current_page = "登录"
            st.rerun()