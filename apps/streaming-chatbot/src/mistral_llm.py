from typing import Optional

from langchain_core.callbacks import CallbackManager
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from huggingface_hub import hf_hub_download


class MistralLLM:
    def __init__(self, model_path: Optional[str]):
        if model_path is None:
            repo_id, model_file_name = (
                "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
                "mistral-7b-instruct-v0.1.Q4_0.gguf",
            )
            model_path = hf_hub_download(
                repo_id=repo_id, filename=model_file_name, repo_type="model"
            )

        self._llm = LlamaCpp(
            model_path=model_path,
            temperature=0,
            max_tokens=2048,
            top_p=1,
            stop=["[INST]"],
            n_gqa=8,
            streaming=True,
            n_gpu_layers=1,
            n_batch=512,
            f16_kv=True,
            verbose=True,
        )

    @property
    def llm(self):
        return self._llm
