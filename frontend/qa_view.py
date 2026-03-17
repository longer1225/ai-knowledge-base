import streamlit as st
from utils.request_util import req_post, req_get
from utils.logger import logger

def qa_chat(question):
    try:
        logger.info(f"[前端] 发起问答请求：{question[:20]}...")
        data = req_post("/api/qa/ask", {"question": question})
        return data.get("data", {}).get("answer", "")
    except Exception as e:
        logger.error(f"[前端] 问答接口异常：{e}")
        st.error(f"❌ 问答接口调用失败：{str(e)}")
        return ""

def load_user_qa_history():
    try:
        logger.info("[前端] 加载QA历史")
        data = req_get("/api/history/qa")
        if data.get("code") == 0:
            return data.get("data", [])
        else:
            st.warning(f"⚠️ 加载历史失败：{data.get('msg')}")
            return []
    except Exception as e:
        logger.error(f"[前端] 加载历史失败：{e}")
        return []

def save_user_qa_history(question, answer):
    try:
        logger.info("[前端] 保存QA历史")
        req_post("/api/history/qa", {
            "question": question,
            "answer": answer
        })
    except Exception as e:
        logger.error(f"[前端] 保存历史失败：{e}")

def render():
    st.title("💬 AI 知识库问答")
    token = st.session_state.get("token")
    if not token:
        st.error("❌ 请先登录！")
        return

    qa_history = load_user_qa_history()
    for chat in reversed(qa_history):
        with st.chat_message("user"):
            st.markdown(chat["question"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

    question = st.chat_input("输入你的问题...")
    if question and question.strip():
        with st.chat_message("user"):
            st.markdown(question)
        with st.spinner("🤖 思考中..."):
            answer = qa_chat(question)
            final_answer = answer or "⚠️ 未获取到有效回答"

        with st.chat_message("assistant"):
            st.markdown(final_answer)
        save_user_qa_history(question, final_answer)
        st.rerun()