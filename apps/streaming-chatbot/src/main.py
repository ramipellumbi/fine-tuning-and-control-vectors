from typing import Optional

import streamlit as st

from llm_chain import LlmChain
from llama_llm import LlamaLLM
from mistral_llm import MistralLLM


st.set_page_config(page_title="Ed")
st.header("Unlock your learning potential with Ed!")


def get_model_path_from_option(option: Optional[str]) -> Optional[str]:
    if not option or option == "Base":
        return None

    if option == "Fine Tuned":
        # TODO
        return None

    if option == "Control Vector":
        # TODO
        return None


def get_model_from_option(model_path: Optional[str], model_option: Optional[str]):
    if not model_option:
        raise ValueError("Model option must be provided.")

    if model_option == "Llama":
        return LlamaLLM(model_path)

    if model_option == "Mistral":
        return MistralLLM(model_path)

    raise ValueError("Invalid model option.")


# Use containers and columns to better organize the layout
with st.container():
    st.subheader("Configuration")
    col1, col2, col3 = st.columns(3)

    with col1:
        system_prompt = st.text_area(
            label="System Prompt",
            value="",
            key="system_prompt",
            height=150,
            help="This is the initial text that sets up the context for the model.",
        )

    with col2:
        model_opt = st.radio(
            label="Model Selection",
            options=["Base", "Fine Tuned", "Fine Tuned & Control Vector"],
            help="Select the model to use.",
        )

    with col3:
        model_type = st.radio(
            label="Model Type",
            options=["Llama", "Mistral"],
            help="Select the model type to use.",
        )


model_path = get_model_path_from_option(model_opt)
model = get_model_from_option(model_path, model_type)
chain = LlmChain(system_prompt, model)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you today?"}
    ]

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Your message here", key="user_input"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        stream = chain.generate(user_prompt)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": str(response)})
