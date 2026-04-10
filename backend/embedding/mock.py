from .base import BaseEmbedding
import random


class MockEmbedding(BaseEmbedding):
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def embed(self, text: str) -> list[float]:
        # 随机向量（测试用）
        return [random.random() for _ in range(self.dimension)]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # ✅ 批量调用（核心修复点）
        return [self.embed(t) for t in texts]