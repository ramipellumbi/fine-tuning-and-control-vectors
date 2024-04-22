from typing import Dict, List


class Conversation:
    def __init__(self, context_length: int = 2):
        self._messages: List[Dict[str, str]] = []
        self._context_length = context_length

    def add_message(self, message: Dict[str, str]):
        assert "role" in message, "Message must have a role."
        assert "content" in message, "Message must have content."
        assert message["role"] in [
            "user",
            "assistant",
        ], "Message role must be 'user' or 'assistant'."
        assert isinstance(message["content"], str), "Message content must be a string."

        self._messages.append(message)

        print(f"Added message: {message}")
        print(f"Current messages in history: {self._messages[-self._context_length:]}")

    def generate_prompt(
        self,
    ):
        # generate a prompt that includes the current message history
        # and then append the user's message with context

        # get the current message history
        message_history = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in self._messages[-self._context_length :]
            ]
        )

        return message_history


conversation = Conversation()
