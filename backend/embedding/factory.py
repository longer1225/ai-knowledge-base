from .base import BaseEmbedding
from .ollama import OllamaEmbedding
from .mock import MockEmbedding  # 新增


class EmbeddingFactory:
    @staticmethod
    def get(model_type: str = "mock", **kwargs) -> BaseEmbedding:
        if model_type == "ollama":
            return OllamaEmbedding(
                model=kwargs.get("ollama_model"),
                host=kwargs.get("ollama_host")
            )

        elif model_type == "mock":  # 👈 轻量测试版
            return MockEmbedding(dimension=kwargs.get("dimension", 384))

        else:
            raise ValueError(f"不支持的模型类型: {model_type}")