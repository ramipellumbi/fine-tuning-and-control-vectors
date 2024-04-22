from typing import Optional

from models.base_model import BaseModel


class LlamaModel(BaseModel):
    def __init__(self, model_path: Optional[str]):
        kwargs = {}

        kwargs["model_path"] = model_path
        kwargs["repo_id"] = "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"
        kwargs["model_file_name"] = "Meta-Llama-3-8B-Instruct-Q8_0.gguf"
        kwargs["stop_token"] = ["<|eot_id|>"]
        super().__init__(**kwargs)
