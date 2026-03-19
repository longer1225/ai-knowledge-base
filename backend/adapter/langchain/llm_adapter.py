from langchain.llms.base import LLM
from backend.llm.base import BaseLLM
from typing import Optional

class LangChainLLMAdapter(LLM):
    llm: BaseLLM

    def _call(self, prompt: str, stop: Optional[list] = None) -> str:
        return self.llm.generate(prompt)

    @property
    def _llm_type(self) -> str:
        return "custom_llm"