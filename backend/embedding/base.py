from abc import ABC, abstractmethod

class BaseEmbedding(ABC):
    """
    嵌入模型抽象基类
    所有模型都必须实现这个接口
    切换模型不影响上层业务
    """
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass