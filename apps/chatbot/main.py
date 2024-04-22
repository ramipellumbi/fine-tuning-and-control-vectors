import os
import sys
from enum import Enum
from typing import Optional

import streamlit as st

from conversation import conversation
from enums import Models, ModelTypes
from setup import get_chain_from_option

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
        if not model_name:
            raise ValueError("Model option must be provided.")
        model = Models[model_name]

    with col3:
        model_type_name = st.radio(
            label="Model Type",
            options=[opt.name for opt in ModelTypes],
            format_func=lambda x: ModelTypes[x].value,
            help="Select the model type to use.",
        )
        if not model_type_name:
            raise ValueError("Model type must be provided.")
        model_type = ModelTypes[model_type_name]

chain = get_chain_from_option(system_prompt, model, model_type)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

if prompt := st.chat_input("Your query", key="user_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    conversation.add_message({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    full_prompt = conversation.get_messages()
    with st.chat_message("assistant"):
        stream = chain.generate(full_prompt)
        response = st.write_stream(stream)
        st.session_state.messages.append(
            {"role": "assistant", "content": str(response)}
        )
        conversation.add_message({"role": "assistant", "content": str(response)})
