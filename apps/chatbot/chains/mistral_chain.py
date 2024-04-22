from typing import Optional, Union

from langchain.prompts import PromptTemplate

from chains.base_chain import BaseChain


class MistralChain(BaseChain):
    def __init__(self, system_prompt: str, model) -> None:
        super().__init__(system_prompt, model)

    def create_prompt(self, system_prompt: str):
        template = """
        <s>[INST]{}[/INST]</s>
        [INST]{}[/INST]
        """.format(
            system_prompt, "{question}"
        )

        prompt = PromptTemplate(template=template, input_variables=["question"])

        return prompt
