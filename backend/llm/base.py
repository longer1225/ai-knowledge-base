from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """LLM大模型抽象基类"""
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass