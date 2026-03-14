import streamlit as st


def login_guard(func):
    """
    真正的重定向拦截器 (类似 Java 的 HandlerInterceptor)
    """

    def wrapper(*args, **kwargs):
        # 如果没有登录
        if not st.session_state.get("login_user"):
            # 1. 弹出警告
            st.toast("⚠️ 访问此页面需要登录！正在跳转...", icon="⚠️")
            # 2. 强制将路由修改为登录页
            st.session_state.current_page = "登录"
            # 3. 强制刷新页面 (相当于 Java 的 response.sendRedirect)
            st.rerun()
            return None  # 拦截掉原函数的执行

        # 如果已登录，放行 (相当于 Java 的 chain.doFilter)
        return func(*args, **kwargs)

    return wrapper