from typing import Optional, Union

from langchain.prompts import PromptTemplate

from llama_llm import LlamaLLM
from mistral_llm import MistralLLM


class LlmChain:
    def __init__(self, system_prompt: str, model: Union[LlamaLLM, MistralLLM]) -> None:
        prompt_template = None
        if isinstance(model, LlamaLLM):
            prompt_template = self._create_prompt_llama(system_prompt)
        if isinstance(model, MistralLLM):
            prompt_template = self._create_prompt_mistral(system_prompt)

        if prompt_template is None:
            raise ValueError("Model must be an instance of LlamaLLM or MistralLLM")

        self._chain = prompt_template | model.llm

    def _create_prompt_mistral(self, system_prompt: str):
        template = """
        <s>[INST]{}[/INST]</s>
        [INST]{}[/INST]
        """.format(
            system_prompt, "{question}"
        )

        prompt = PromptTemplate(template=template, input_variables=["question"])

        return prompt

    def _create_prompt_llama(self, system_prompt: str):
        template = """
        <|start_header_id|>system<|end_header_id|>
        {}<|eot_id|>\n\n<|start_header_id|>user<|end_header_id|>
        {}<|eot_id|>\n\n<|start_header_id|>assistant<|end_header_id|>
        """.format(
            system_prompt, "{question}"
        )

        prompt = PromptTemplate(template=template, input_variables=["question"])

        return prompt

    def generate(self, prompt: str):
        return self._chain.stream({"question": prompt})
