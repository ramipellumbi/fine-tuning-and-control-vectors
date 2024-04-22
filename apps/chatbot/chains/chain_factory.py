from chains.llama_chain import LlamaChain
from chains.mistral_chain import MistralChain
from enums.models import Models
from models.llama_model import LlamaModel
from models.mistral_model import MistralModel
from models.model_factory import ModelFactory


class ChainFactory:
    def __init__(self, system_prompt: str, model_factory: ModelFactory):
        self._system_prompt = system_prompt
        self._model_factory = model_factory

    def _create_llama_chain(self, model: LlamaModel):
        return LlamaChain(self._system_prompt, model)

    def _create_mistral_chain(self, model: MistralModel):
        return MistralChain(self._system_prompt, model)

    def create_chain(self, model_name: Models):
        if model_name == Models.LLAMA:
            model = self._model_factory.create_model(model_name)
            if not isinstance(model, LlamaModel):
                raise ValueError(f"Model {model} is not an instance of LlamaModel")

            return self._create_llama_chain(model)

        if model_name == Models.MISTRAL:
            model = self._model_factory.create_model(model_name)
            if not isinstance(model, MistralModel):
                raise ValueError(f"Model {model} is not an instance of MistralModel")

            return self._create_mistral_chain(model)

        raise ValueError(f"Model {model} not supported")
