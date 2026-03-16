import random
from .base import BaseEmbedding

class MockEmbedding(BaseEmbedding):
    """
    🧪 超级轻量模拟嵌入
    不占内存、不联网、不跑模型、0 资源消耗
    生成固定维度假向量，用于测试上传/入库/分块
    """
    def __init__(self, dimension: int = 384):
        self.dimension = dimension  # 向量维度（和真实模型保持一致）

    def embed(self, text: str) -> list[float]:
        # 固定种子：相同文本生成相同向量，方便测试
        random.seed(len(text) + hash(text[:10]))
        return [round(random.uniform(-0.1, 0.1), 6) for _ in range(self.dimension)]