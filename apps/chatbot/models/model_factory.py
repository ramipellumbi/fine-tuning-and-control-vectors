from typing import Optional

from enums.models import Models
from models.llama_model import LlamaModel
from models.mistral_model import MistralModel


class ModelFactory:
    def __init__(self, model_path: Optional[str] = None):
        self._model_path = model_path

    def _create_llama_model(self):
        return LlamaModel(self._model_path)

    def _create_mistral_model(self):
        return MistralModel(self._model_path)

    def create_model(self, model: Models):
        if model == Models.LLAMA:
            return self._create_llama_model()
        if model == Models.MISTRAL:
            return self._create_mistral_model()

        raise ValueError(f"Model {model} not supported")
