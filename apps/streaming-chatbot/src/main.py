import streamlit as st
from llm_chain import LlmChain, MistralLlm

st.set_page_config(page_title="Ed")
st.header("Unlock your learning potential with Ed!")

# Use containers and columns to better organize the layout
with st.container():
    st.subheader("Configuration")
    col1, col2 = st.columns(2)

    with col1:
        system_prompt = st.text_area(
            label="System Prompt",
            value="",
            key="system_prompt",
            height=150,
            help="This is the initial text that sets up the context for the model."
        )

    with col2:
        model_opt = st.radio(
           label="Model Selection",
           options=["Base", "Fine Tuned"],
           help="Select the model to use.")

model_path = None if model_opt == "Base" else model_opt  # TODO: replace with real path heree
model = MistralLlm(model_path)
chain = LlmChain(system_prompt, model)

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
        stream = chain.generate(user_prompt)
        response = st.write_stream(stream)
    st.session_state.messages.append({
        "role": "assistant",
        "content": str(response)
    })
