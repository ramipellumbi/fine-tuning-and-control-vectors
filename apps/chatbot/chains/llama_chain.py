from typing import Optional, Union

from langchain.prompts import PromptTemplate

from chains.base_chain import BaseChain


class LlamaChain(BaseChain):
    def __init__(self, system_prompt: str, model) -> None:
        super().__init__(system_prompt, model)

    def create_prompt(self, system_prompt: str):
        template = """
        <|start_header_id|>system<|end_header_id|>
        {}<|eot_id|>\n\n<|start_header_id|>user<|end_header_id|>
        {}<|eot_id|>\n\n<|start_header_id|>assistant<|end_header_id|>
        """.format(
            system_prompt, "{question}"
        )

        prompt = PromptTemplate(template=template, input_variables=["question"])

        return prompt
