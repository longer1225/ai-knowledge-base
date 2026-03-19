from abc import ABC, abstractmethod
from typing import List


class BaseEmbedding(ABC):
    """
    嵌入模型抽象基类
    """

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """
        单条文本 embedding
        """
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        批量文本 embedding（非常重要）
        """
        pass