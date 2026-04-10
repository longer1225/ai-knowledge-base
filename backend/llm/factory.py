from .base import BaseLLM
from .mock import MockLLM
from .ollama import OllamaLLM
from .qwen import AliyunQwenLLM


class LLMFactory:
    @staticmethod
    def get(model_type: str = "mock", **kwargs) -> BaseLLM:
        model_type = (model_type or "mock").lower()

        if model_type == "ollama":
            return OllamaLLM(
                model=kwargs.get("ollama_model", "llama3"),
                host=kwargs.get("ollama_host", "http://localhost:11434")
            )

        elif model_type == "qwen":
            api_key = kwargs.get("api_key")
            if not api_key:
                raise ValueError("使用 qwen 必须提供 api_key")

            return AliyunQwenLLM(
                api_key=api_key,
                model_name=kwargs.get("model_name", "qwen-turbo"),
                temperature=kwargs.get("temperature", 0.1)
            )

        elif model_type == "mock":
            return MockLLM()

        else:
            raise ValueError(f"不支持的LLM类型: {model_type}")