from typing import Dict, List, Optional

from llama_cpp import ChatCompletionRequestMessage


class Conversation:
    def __init__(self, context_length: Optional[int] = None):
        self._messages: List[ChatCompletionRequestMessage] = []
        self._context_length = context_length

    def add_message(self, message: ChatCompletionRequestMessage):
        assert "role" in message, "Message must have a role."
        assert "content" in message, "Message must have content."
        assert message["role"] in [
            "user",
            "assistant",
        ], "Message role must be 'user' or 'assistant'."
        assert isinstance(message["content"], str), "Message content must be a string."

        self._messages.append(message)

        print(f"Added message: {message}")
        print(f"Current messages in history: {self.get_messages()}")

    def get_messages(self):
        if self._context_length is None:
            return self._messages

        return self._messages[-self._context_length :]


conversation = Conversation()
