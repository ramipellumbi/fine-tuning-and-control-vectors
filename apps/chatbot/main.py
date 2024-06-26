import os
import sys
from enum import Enum
from typing import List, Optional

from llama_cpp import ChatCompletionRequestMessage
import streamlit as st

from conversation import conversation
from enums import Models, ModelTypes
from setup import get_model_from_options

# Add the parent directory to the sys path to import from packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Ed")
st.header("Unlock your learning potential with Ed!")


# Use containers and columns to better organize the layout
with st.container():
    st.subheader("Configuration")
    col1, col2, col3 = st.columns(3)

    with col1:
        system_prompt = st.text_area(
            label="System Prompt",
            value="",
            key="system_prompt",
            height=100,
            help="This is the initial text that sets up the context for the model.",
        )

    with col2:
        model_name = st.radio(
            label="Model Selection",
            options=[opt.name for opt in Models],
            format_func=lambda x: Models[x].value,
            help="Select the model to use.",
        )
        assert (
            model_name is not None and model_name in Models.__members__
        ), f"Model {model_name} not supported."
        model = Models[model_name]

    model_type = None
    if model != Models.LLAMA:
        with col3:
            model_type_name = st.radio(
                label="Model Type",
                options=[opt.name for opt in ModelTypes],
                format_func=lambda x: ModelTypes[x].value,
                help="Select the model type to use.",
            )
            assert (
                model_type_name is not None
                and model_type_name in ModelTypes.__members__
            )
            model_type = ModelTypes[model_type_name]

model = get_model_from_options(model, model_type)

if "messages" not in st.session_state.keys():
    initial_messages: List[ChatCompletionRequestMessage] = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]
    st.session_state.messages = initial_messages

if prompt := st.chat_input("Your query", key="user_input"):
    new_user_msg: ChatCompletionRequestMessage = {"role": "user", "content": prompt}
    st.session_state.messages.append(new_user_msg)
    conversation.add_message(new_user_msg)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    messages = conversation.get_messages()
    with st.chat_message("assistant"):
        st.write(f"({model.model_name()})")

        stream = model.generate(system_prompt, messages)
        response = st.write_stream(stream)
        new_assistant_message: ChatCompletionRequestMessage = {
            "role": "assistant",
            "content": str(response),
        }
        st.session_state.messages.append(new_assistant_message)
        conversation.add_message(new_assistant_message)
