from langchain_core.embeddings import Embeddings
from backend.embedding.base import BaseEmbedding


class LangChainEmbeddingAdapter(Embeddings):
    def __init__(self, embedding: BaseEmbedding):
        self.embedding = embedding

    def embed_query(self, text: str) -> list[float]:
        return self.embedding.embed(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # ✅ 批量调用（性能关键）
        return self.embedding.embed_documents(texts)