from typing import Optional

from models.base_model import BaseModel


class MistralModel(BaseModel):
    def __init__(self, model_path: Optional[str]):
        kwargs = {}

        kwargs["model_path"] = model_path
        kwargs["chat_format"] = "mistral-instruct"
        kwargs["repo_id"] = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
        kwargs["model_file_name"] = "mistral-7b-instruct-v0.1.Q4_0.gguf"
        kwargs["stop_token"] = ["[INST]"]
        super().__init__(**kwargs)

    def model_name(self) -> str:
        return "mistral"
