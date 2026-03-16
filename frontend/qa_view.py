import streamlit as st
# 保留你的 req_post 导入，删掉多余的 requests
from frontend.request_util import  req_post


def qa_chat(token, question):
    """原函数保留，仅修复取值逻辑"""
    res = req_post("/api/qa/ask", {
        "question": question
    }).json()
    # 修复 KeyError：先取 data 层
    return res.get("data", {})


def render():
    st.title("💬 AI 知识库问答")

    # 初始化历史（保留你的原有逻辑）
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    # 展示历史对话（保留你的原有逻辑）
    for chat in st.session_state.qa_history:
        with st.chat_message("user"):
            st.markdown(chat["question"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

    # 输入框（保留你的原有逻辑）
    question = st.chat_input("请输入你的问题...")

    if question:
        # 显示用户问题（保留你的原有逻辑）
        with st.chat_message("user"):
            st.markdown(question)

        # 调用后端接口（保留你的原有逻辑，仅加模型判断）
        token = st.session_state.get("token")
        res = qa_chat(token, question)

        # ✅ 核心需求：无模型时显示「模型未加载」，有模型时显示真实回答
        answer = res.get("answer")
        if not answer:  # 后端未返回answer → 判定为模型未加载
            final_answer = "⚠️ 模型未加载，请先加载大模型后再提问！"
        else:
            final_answer = answer

        # 显示助手回答（保留你的原有逻辑）
        with st.chat_message("assistant"):
            st.markdown(final_answer)

        # 保存历史（保留你的原有逻辑）
        st.session_state.qa_history.append({
            "question": question,
            "answer": final_answer
        })