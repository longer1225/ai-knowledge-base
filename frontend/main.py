# ==============================================
# 👇 这四行必须放在最最最顶部！修复路径问题
# ==============================================
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from config.frontend_config import init_session_state, load_css
from utils.auth_guard import login_guard
from utils.logger import logger

# 页面导入
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
                st.markdown(
                    f"<div style='text-align:right; padding-top:10px; color:#ECECEC;'> ⚪{st.session_state.login_user}</div>",
                    unsafe_allow_html=True)
            with col_logout:
                if st.button("退出", use_container_width=True, key="top_logout_btn"):
                    st.session_state.login_user = None
                    st.session_state.token = None
                    st.rerun()


# ====================== 【核心】侧边栏（现在包含对话列表） ======================
def render_sidebar():
    with st.sidebar:
        st.markdown("<h3 style='color:white;'>知识库问答系统</h3>", unsafe_allow_html=True)

        # 新聊天
        if st.button("💬 新聊天", key="sidebar_new_chat", use_container_width=True):
            from utils.request_util import req_post
            try:
                res = req_post("/api/chat/new", {})
                if res and res.get("code") == 0:
                    st.session_state.chat_id = res["data"]["chat_id"]
            except Exception as e:
                logger.error(f"新建窗口失败: {e}")

            st.session_state.current_page = "智能问答"
            st.rerun()

        # 功能按钮
        if st.button("📤 文档上传", key="sidebar_upload", use_container_width=True):
            st.session_state.current_page = "文档上传"
            st.rerun()
        if st.button("📖 知识库管理", key="sidebar_manage", use_container_width=True):
            st.session_state.current_page = "知识库管理"
            st.rerun()

        st.divider()
        st.subheader("📂 历史对话")

        if st.session_state.get("token"):
            try:
                from utils.request_util import req_get, req_post
                res = req_get("/api/chat/list")
                if res and res.get("code") == 0:
                    chat_list = res["data"]["chats"]

                    if not chat_list:
                        st.info("暂无对话，点击「新聊天」开始吧～")
                    else:
                        for chat in chat_list:
                            cid = chat["chat_id"]
                            title = chat.get("title", f"对话 {cid}")

                            col1, col2, col3 = st.columns([7,1,1])
                            with col1:
                                if st.button(f"📝 {title}", key=f"chat_{cid}", use_container_width=True):
                                    st.session_state.chat_id = cid
                                    st.session_state.current_page = "智能问答"
                                    st.rerun()
                            with col2:
                                # 触发编辑
                                if st.button("✏️", key=f"edit_btn_{cid}", use_container_width=True):
                                    st.session_state["editing_id"] = cid

                            # 真正能修改成功的输入框（关键在这里！）
                            if st.session_state.get("editing_id") == cid:
                                new_name = st.text_input("新标题", key=f"new_name_{cid}")
                                # 用 form 确保值能提交！！！
                                with st.form(key=f"form_{cid}"):
                                    submit = st.form_submit_button("✅ 保存")
                                    if submit and new_name:
                                        # 🔥 这里才是真正能发成功的！
                                        req_post(f"/api/chat/rename/{cid}", {"title": new_name})
                                        st.session_state["editing_id"] = None
                                        st.rerun()

                            with col3:
                                if st.button("🗑️", key=f"del_{cid}", use_container_width=True):
                                    from utils.request_util import req_delete
                                    res_del = req_delete(f"/api/chat/delete/{cid}")
                                    if res_del and res_del.get("code") == 0:
                                        if st.session_state.chat_id == cid:
                                            st.session_state.chat_id = None
                                        st.rerun()
                else:
                    st.info("加载对话失败")
            except Exception as e:
                logger.error(f"获取对话列表异常: {e}")
                st.info("加载对话失败")
        else:
            st.info("请登录后查看对话")


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
    render_sidebar()  # 侧边栏只在这里跑一次
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