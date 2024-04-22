import os
import sys
from enum import Enum
from typing import Optional

import streamlit as st

from chains import ChainFactory
from enums import Models, ModelTypes
from models import ModelFactory

# Add the parent directory to the sys path to import from packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_model_path_from_option(option: ModelTypes) -> Optional[str]:
    if option == ModelTypes.BASE:
        return None

    if option == ModelTypes.FINE_TUNED:
        # TODO
        return None

    if option == ModelTypes.FINE_TUNED_AND_CV:
        # TODO
        return None


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

model_path = get_model_path_from_option(model_type)
model_factory = ModelFactory(model_path)
chain = ChainFactory(system_prompt, model_factory).create_chain(model)

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
