import time
import streamlit as st
from backend.utils.logger import logger
from frontend.request_util import req_post, req_get, req_stream_post

# ==================== API 函数 ====================
def create_chat():
    try:
        logger.info("[前端] 调用新建对话接口")
        res = req_post("/api/chat/new", {})
        if res and res.get("code") == 0:
            return res["data"]["chat_id"]
    except Exception as e:
        logger.error(f"[前端] 新建对话失败：{e}")
        st.error("新建对话出错啦～")
    return None

def qa_ask(question):
    try:
        chat_id = st.session_state.get("chat_id")
        logger.info(f"[前端QA] 用户问题：{question}")
        return req_stream_post("/api/qa/ask", {"question": question, "chat_id": chat_id})
    except Exception as e:
        logger.error(f"[前端QA] 请求异常：{str(e)}")
        return ["⚠️ 网络异常或服务未启动"]

def load_chat_history(chat_id):
    try:
        logger.info(f"[前端] 加载聊天记录：{chat_id}")
        res = req_get(f"/api/history/chat/{chat_id}")
        if res and res.get("code") == 0:
            return res["data"]
    except Exception as e:
        logger.error(f"[前端] 加载历史失败：{e}")
    return []

def save_chat_msg(question, answer, chat_id):
    try:
        logger.info("[前端] 保存消息到历史")
        req_post("/api/history/qa", {"question": question, "answer": answer, "chat_id": chat_id})
    except Exception as e:
        logger.error(f"[前端] 保存消息失败：{e}")


# ==================== 主渲染函数 ====================
def render():
    # 🔥🔥🔥 核心修复：将所有的初始化放进 render 函数内部！
    # 这样每次页面刷新，都会确保这些变量100%存在，绝对不会报 KeyError
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = None
    if "chat_history_cache" not in st.session_state:
        st.session_state.chat_history_cache = []
    if "history_rendered" not in st.session_state:
        st.session_state.history_rendered = False
    if "current_loaded_chat_id" not in st.session_state:
        st.session_state.current_loaded_chat_id = None

    # 1. 登录拦截校验
    if not st.session_state.get("token"):
        st.error("❌ 请先登录再使用问答功能")
        return

    current_chat_id = st.session_state.get("chat_id")
    st.title("💬 AI 知识库问答")

    # 2. 空状态提示
    if not current_chat_id:
        st.info("👈 点击左侧「新聊天」开始对话")
        return

    # 3. 动态切换历史记录
    if st.session_state.current_loaded_chat_id != current_chat_id:
        history = load_chat_history(current_chat_id)
        st.session_state.chat_history_cache = history if history else []
        st.session_state.current_loaded_chat_id = current_chat_id

    # 4. 渲染所有的历史记录（从缓存中读取）
    for msg in st.session_state.chat_history_cache:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg.get("question", ""))
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg.get("answer", ""))

    # 5. 监听用户底部输入框
    question = st.chat_input("输入你的问题...")

    if question and question.strip():
        # 立刻在页面上渲染用户的提问
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(question)

        # 准备渲染 AI 的回答
        with st.chat_message("assistant", avatar="🤖"):
            answer_container = st.empty()
            full_answer = ""

            answer_container.markdown("🪐Thinking...")

            # 调用流式请求
            response = qa_ask(question)
            for chunk in response:
                if chunk:
                    full_answer += chunk
                    # 加上闪烁光标效果
                    answer_container.markdown(full_answer + " ▌")
                    # 强行逼出真实的打字机停顿感
                    time.sleep(0.03)

            # 流式传输结束后，去掉闪烁的光标，渲染最终纯净的文本
            answer_container.markdown(full_answer)


        # 7. 追加到前端缓存中
        st.session_state.chat_history_cache.append({
            "question": question,
            "answer": full_answer
        })

        # 8. 强制刷新页面
        st.rerun()