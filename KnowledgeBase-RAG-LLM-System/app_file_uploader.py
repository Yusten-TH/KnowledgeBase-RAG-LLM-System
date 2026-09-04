"""
基于Streamlit完成WEB网页上传服务
轻量化，不用每次运行代码
pip install streamlit

streamlit: 当web页面元素发生变化，则代码重新执行一遍
"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# session_state是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


count = 0

# file_uploader
uploader_file = st.file_uploader(
    "请上传txt文件",
    type=['txt'],
    accept_multiple_files=False,        # False表示仅接受单文件上传
)
if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # get_value()获取内容->bytes->decode('utf-8')
    text = uploader_file.getvalue().decode("utf-8")
    # st.write(text)
    with st.spinner("载入知识库中..."):               # 在spinner代码的执行过程中会有一个加载动画
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)



