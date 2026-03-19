from langchain_core.language_models.llms import LLM
from backend.llm.base import BaseLLM
from typing import Optional


class LangChainLLMAdapter(LLM):
    def __init__(self, llm: BaseLLM):
        super().__init__()
        self.llm = llm

    def _call(self, prompt: str, stop: Optional[list] = None) -> str:
        return self.llm.generate(prompt)

    @property
    def _llm_type(self) -> str:
        return "custom_llm"