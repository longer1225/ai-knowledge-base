# backend/llm/qwen.py
from .base import BaseLLM
from langchain_openai import ChatOpenAI


class AliyunQwenLLM(BaseLLM):
    def __init__(
        self,
        api_key: str,
        model_name: str = "qwen-turbo",
        temperature: float = 0.1
    ):
        self.llm = ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=temperature,
            max_tokens=2048
        )

    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content