import streamlit as st
import requests
from datetime import datetime

def render():
    st.markdown("<h2 style='color: white; margin-bottom: 20px;'>📤 文档上传</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #aaa;'>支持 docx / txt 格式，单次限传1个</p>", unsafe_allow_html=True)

    file = st.file_uploader("选择文件", type=["docx", "txt"], label_visibility="collapsed")

    if file:
        if file.size == 0:
            st.warning("你上传的是空文件，请选择非空的txt/docx文件！")
        else:
            if st.button("开始上传与处理", type="primary"):
                with st.spinner("上传中..."):
                    token = st.session_state.get("token", "")
                    headers = {"Authorization": f"Bearer {token}"}
                    files = {"file": (file.name, file, file.type)}

                    try:
                        res = requests.post(
                            url="http://localhost:8001/api/upload",
                            headers=headers,
                            files=files
                        )

                        data = res.json()
                        if res.status_code == 200 and data.get("code") == 0:
                            st.session_state.docs.append({
                                "id": data["data"]["doc_id"],
                                "name": file.name,
                                "size": file.size,
                                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            st.success(f"✅ {file.name} 上传成功！")
                        else:
                            st.error(f"❌ {data.get('msg', '上传失败')}")

                    except Exception as e:
                        st.error(f"连接后端失败：{str(e)}")