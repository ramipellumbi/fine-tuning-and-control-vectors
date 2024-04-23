from abc import ABC, abstractmethod
from typing import Dict, Iterable, List

from llama_cpp import (
    ChatCompletionRequestMessage,
    ChatCompletionRequestSystemMessage,
    Llama,
)
from huggingface_hub import hf_hub_download


class BaseModel(ABC):
    def __init__(self, **kwargs):
        assert "model_path" in kwargs, "model_path is required"
        assert "chat_format" in kwargs, "chat_format is required"
        assert "repo_id" in kwargs, "repo_id is required"
        assert "model_file_name" in kwargs, "model_file_name is required"
        assert "stop_token" in kwargs, "stop_token is required"

        stop_token = kwargs["stop_token"]
        assert isinstance(stop_token, List), "stop_token must be a list of strings"

        chat_format = kwargs["chat_format"]
        assert chat_format in [
            "mistral-instruct",
            "llama-3",
        ], "chat_format must be one of 'mistral-instruct' or 'llama-3'"

        model_path = kwargs["model_path"]
        if model_path is None:
            repo_id = kwargs["repo_id"]
            model_file_name = kwargs["model_file_name"]

            assert isinstance(
                repo_id, str
            ), "repo_id must be a string and is required if no model_path is provided"
            assert isinstance(
                model_file_name, str
            ), "model_file_name must be a string and is required if no model_path is provided"

            model_path = hf_hub_download(
                repo_id=repo_id, filename=model_file_name, repo_type="model"
            )

        self._llm = Llama(
            model_path=model_path,
            chat_format=chat_format,
            stream=True,
            n_gpu_layers=-1,
            n_ctx=4096,
            verbose=False,
            temperature=0.9,
            skip_special_tokens=True,
            stop=stop_token,
        )

    @abstractmethod
    def model_name(self) -> str:
        """
        Returns the model name
        """

    def generate(
        self, system_prompt: str, messages: List[ChatCompletionRequestMessage]
    ):
        messages_with_system_prompt = [
            ChatCompletionRequestSystemMessage(
                role="system",
                content=system_prompt,
            ),
            *messages,
        ]

        completion = self._llm.create_chat_completion(
            messages=messages_with_system_prompt,
            stream=True,
        )
        assert isinstance(completion, Iterable), "Completion is not iterable"

        for chunk in completion:
            assert isinstance(chunk, Dict)
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                yield delta["content"]
