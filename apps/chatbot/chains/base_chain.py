from abc import ABC, abstractmethod
from typing import Any

from langchain.prompts import PromptTemplate

from models.base_model import BaseModel


class BaseChain(ABC):
    def __init__(self, system_prompt: str, model: BaseModel) -> None:
        prompt_template = self.create_prompt(system_prompt)
        self._chain = prompt_template | model.llm

    @abstractmethod
    def create_prompt(self, system_prompt: str) -> PromptTemplate:
        """Create a prompt template for the model"""

    def generate(self, prompt: str):
        return self._chain.stream({"question": prompt})
