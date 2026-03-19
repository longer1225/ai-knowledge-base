from .base import BaseLLM
from .mock import MockLLM
from .ollama import OllamaLLM

class LLMFactory:
    @staticmethod
    def get(model_type: str = "mock", **kwargs) -> BaseLLM:
        if model_type == "ollama":
            return OllamaLLM(
                model=kwargs.get("ollama_model"),
                host=kwargs.get("ollama_host")
            )
        elif model_type == "mock":
            return MockLLM()
        else:
            raise ValueError(f"不支持的LLM类型: {model_type}")