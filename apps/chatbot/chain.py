from typing import Any, Dict, Iterable, List

from llama_cpp import ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage

from models.base_model import BaseModel


class Chain:
    def __init__(self, system_prompt: str, model: BaseModel) -> None:
        self._system_prompt = system_prompt
        self._chain = model.llm

    def generate(self, messages: List[ChatCompletionRequestMessage]):
        messages_with_system_prompt = [
            ChatCompletionRequestSystemMessage(
                role="system",
                content=self._system_prompt,
            ),
            *messages,
        ]

        completion = self._chain.create_chat_completion(
            messages=messages_with_system_prompt,
            stream=True,
        )

        if not isinstance(completion, Iterable):
            raise ValueError("Completion is not iterable")

        for chunk in completion:
            assert isinstance(chunk, Dict)
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                yield delta["content"]
