import streamlit as st

def render():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<h2 style='color: white;'>📖 知识库管理</h2>", unsafe_allow_html=True)
    with col2:
        if st.button("🗑️ 清空所有对话历史", use_container_width=True):
            st.session_state.qa_history = []
            st.toast("对话历史已清空")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.docs:
        for doc in st.session_state.docs:
            st.markdown(f"""
                <div class="dark-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin:0; color:#ECECEC;">📄 {doc['name']}</h4>
                            <p style="margin:5px 0 0 0; color:#888; font-size:14px;">
                                大小: {doc['size']} B &nbsp;|&nbsp; 上传时间: {doc['time']}
                            </p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("删除此文档", key=f"del_{doc['id']}"):
                st.session_state.docs.remove(doc)
                st.rerun() # 刷新页面
    else:
        st.info("当前知识库为空，请前往「文档上传」页面添加文档。")