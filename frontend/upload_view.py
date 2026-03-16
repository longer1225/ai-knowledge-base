import streamlit as st
import requests
from datetime import datetime

from settings import API_BASE_URL


def render():
    st.markdown("<h2 style='color: white; margin-bottom: 20px;'>📤 文档上传</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #aaa;'>支持 docx / txt 格式，单次限传1个</p>", unsafe_allow_html=True)

    file = st.file_uploader("选择文件", type=["docx", "txt"], label_visibility="collapsed")

    if file:
        # 空文件判断
        if file.size == 0:
            st.warning("⚠️ 你上传的是空文件，请选择非空的 txt/docx 文件！")
        else:
            if st.button("开始上传与处理", type="primary"):
                with st.spinner("⏳ 文件上传与处理中..."):
                    # 身份验证
                    token = st.session_state.get("token", "")
                    if not token:
                        st.error("❌ 未登录，请先登录！")
                        return

                    headers = {"Authorization": f"Bearer {token}"}
                    files = {"file": (file.name, file, file.type)}

                    try:
                        # 发送上传请求
                        res = requests.post(
                            url=f"{API_BASE_URL}/api/upload",
                            headers=headers,
                            files=files,
                            timeout=60  # 大文件超时时间
                        )

                        # 解析响应
                        data = res.json()
                        if res.status_code == 200 and data.get("code") == 0:
                            # 更新文档列表
                            st.session_state.docs.append({
                                "id": data["data"]["doc_id"],
                                "name": file.name,
                                "size": file.size,
                                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            st.success(f"✅ {file.name} 上传并处理成功！")
                        else:
                            st.error(f"❌ 上传失败：{data.get('msg', '未知错误')}")

                    except requests.exceptions.Timeout:
                        st.error("⏱️ 请求超时，请检查后端服务或文件大小！")
                    except requests.exceptions.ConnectionError:
                        st.error(f"🔌 连接后端失败：{API_BASE_URL} 服务未启动！")
                    except Exception as e:
                        st.error(f"❌ 未知错误：{str(e)}")