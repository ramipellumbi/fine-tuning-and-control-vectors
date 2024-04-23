from typing import Optional

from enums.models import Models
from models.llama_model import LlamaModel
from models.mistral_model import MistralModel


class ModelFactory:
    @staticmethod
    def create_model(model: Models, path: Optional[str] = None):
        assert model in Models, f"Model {model} not supported"

        if model == Models.LLAMA:
            return LlamaModel(path)
        if model == Models.MISTRAL:
            return MistralModel(path)

        raise ValueError(f"Model {model} has no return path")
