import streamlit as st
from utils.api_client import request_api

def render():
    # 渲染历史对话
    if not st.session_state.qa_history:
        st.markdown('<div class="welcome-title">有什么可以帮忙的？</div>', unsafe_allow_html=True)
    else:
        for item in st.session_state.qa_history:
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(item["question"])
            with st.chat_message("assistant", avatar="🤖"):
                st.write(item["answer"])
                if "source" in item and item["source"]:
                    with st.expander("🔍 参考切片来源", expanded=False):
                        st.write(item["source"])

    # 底部悬浮输入框
    prompt = st.chat_input("有问题，尽管问...")
    if prompt:
        st.session_state.qa_history.append({"question": prompt, "answer": "", "source": ""})
        st.rerun() # 刷新页面显示用户提问

    # 调用后端接口获取AI回答
    if st.session_state.qa_history and st.session_state.qa_history[-1]["answer"] == "":
        latest_question = st.session_state.qa_history[-1]["question"]
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("思考中..."):
                res = request_api("/api/qa", "POST", {"question": latest_question})
                if res and res.get("code") == 0:
                    st.session_state.qa_history[-1]["answer"] = res["data"]["answer"]
                    st.session_state.qa_history[-1]["source"] = res["data"].get("source", "")
                    st.rerun()
                else:
                    st.error("请求失败，请检查后端")
                    st.session_state.qa_history.pop()