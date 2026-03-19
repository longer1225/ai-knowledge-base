from .base import BaseEmbedding
from .ollama import OllamaEmbedding
from .mock import MockEmbedding
from .qwen_embedding import QwenEmbedding  # 👈 新增


class EmbeddingFactory:
    @staticmethod
    def get(model_type: str = "mock", **kwargs) -> BaseEmbedding:

        if model_type == "ollama":
            return OllamaEmbedding(
                model=kwargs.get("model_name"),
                host=kwargs.get("host")
            )

        elif model_type == "qwen":   # 👈 核心新增
            return QwenEmbedding(
                api_key=kwargs.get("api_key"),
                model_name=kwargs.get("model_name")
            )

        elif model_type == "mock":
            return MockEmbedding(
                dimension=kwargs.get("dimension", 384)
            )

        else:
            raise ValueError(f"不支持的模型类型: {model_type}")