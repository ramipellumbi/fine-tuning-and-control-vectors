from llama_cpp import Llama
from huggingface_hub import hf_hub_download


class BaseModel:
    def __init__(self, **kwargs):
        if "model_path" not in kwargs:
            raise ValueError("model_path is required")
        if "repo_id" not in kwargs:
            raise ValueError("repo_id is required")
        if "model_file_name" not in kwargs:
            raise ValueError("model_file_name is required")
        if "stop_token" not in kwargs:
            raise ValueError("stop_token is required")
        if "chat_format" not in kwargs:
            raise ValueError("chat_format is required")

        chat_format = kwargs["chat_format"]
        assert chat_format in [
            "mistral-instruct",
            "llama-3",
        ], "chat_format must be one of 'mistral-instruct' or 'llama-3'"

        model_path = kwargs["model_path"]

        if model_path is None:
            repo_id = kwargs["repo_id"]
            model_file_name = kwargs["model_file_name"]

            assert isinstance(
                repo_id, str
            ), "repo_id must be a string and is required if no model_path is provided"
            assert isinstance(
                model_file_name, str
            ), "model_file_name must be a string and is required if no model_path is provided"

            model_path = hf_hub_download(
                repo_id=repo_id, filename=model_file_name, repo_type="model"
            )

        stop_token = kwargs["stop_token"]

        self._llm = Llama(
            model_path=model_path,
            chat_format=chat_format,
            stream=True,
            n_gpu_layers=-1,
            n_ctx=4096,
            verbose=False,
            temperature=0.9,
            skip_special_tokens=True,
            stop=stop_token,
        )

    @property
    def llm(self):
        return self._llm
