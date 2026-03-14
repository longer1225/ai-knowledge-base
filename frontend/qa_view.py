import streamlit as st
from utils.api_client import qa_chat

def render():
    # 1. 渲染历史对话 (如果你没有历史记录，就会显示那句经典的提示语)
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

    # 2. 底部悬浮输入框 (这就是你丢失的那个输入框)
    prompt = st.chat_input("有问题，尽管问...")
    if prompt:
        st.session_state.qa_history.append({"question": prompt, "answer": "", "source": ""})
        st.rerun()

    # 3. 处理最新的未回答的问题
    if st.session_state.qa_history and st.session_state.qa_history[-1]["answer"] == "":
        latest_question = st.session_state.qa_history[-1]["question"]
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("思考中..."):
                # 调用后端的问答接口
                res = qa_chat(st.session_state.get("token"), latest_question)
                if res and res.get("code") == 0:
                    st.session_state.qa_history[-1]["answer"] = res["data"]["answer"]
                    st.session_state.qa_history[-1]["source"] = res["data"].get("source", "")
                    st.rerun()
                else:
                    st.error("请求失败，请检查后端服务")
                    st.session_state.qa_history.pop()