import streamlit as st
from llm_handler import create_chain

st.set_page_config(page_title="Ed")
st.header("Unlock your learning potential with Ed!")

system_prompt = st.text_area(
    label="System Prompt",
    value="",
    key="system_prompt")

llm_chain = create_chain(system_prompt, st)

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "How may I help you today?"
    }]

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Your message here", key="user_input"):
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        stream = llm_chain.stream({"question": user_prompt})
        response = st.write_stream(stream)
    st.session_state.messages.append({
        "role": "assistant",
        "content": str(response)
    })
