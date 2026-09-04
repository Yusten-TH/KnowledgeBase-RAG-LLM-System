import time
from os.path import join

import config_data as config
from rag import RagService
import streamlit as st

st.title("智能客服")
st.divider()            # 分隔符


if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好，有什么可以帮助你的?"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 下页面最下方提供用户输入栏
prompt= st.chat_input()
if prompt:
    # 在页面输出用户提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"assistant","content":prompt})

    ai_res_list = []
    with st.spinner("思考中..."):
        res_stream =  st.session_state["rag"].chain.stream({"input":prompt},config.session_config)
        # yield
        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk


        st.chat_message("assistant").write_stream(capture(res_stream,ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})
# ["a","b","c"]  “” .join(list) ->abc
# ["a","b","c"]  “,” .join(list) ->a,b,c