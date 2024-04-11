import streamlit as st
from llm_handler import create_chain

st.set_page_config(page_title="Ed")
st.header("Unlock your learning potential with Ed!")

system_prompt = st.text_area(
    label="System Prompt",
    value="",
    key="system_prompt")

@st.cache_resource
def gen_chain():
    return create_chain(system_prompt)

llm_chain = gen_chain()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Your message here", key="user_input"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    response = llm_chain.invoke({"question": user_prompt})
    print(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
