from typing import Optional

from langchain_core.callbacks import CallbackManager
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from huggingface_hub import hf_hub_download


class LlamaLLM:
    def __init__(self, model_path: Optional[str]):
        if model_path is None:
            repo_id, model_file_name = (
                "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
                "Meta-Llama-3-8B-Instruct-Q8_0.gguf",
            )
            model_path = hf_hub_download(
                repo_id=repo_id, filename=model_file_name, repo_type="model"
            )

        self._llm = LlamaCpp(
            model_path=model_path,
            temperature=0,
            max_tokens=2048,
            top_p=1,
            stop=["<|eot_id|>"],
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
