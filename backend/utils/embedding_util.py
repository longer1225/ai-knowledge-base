from backend.config import EMBEDDING_CONFIG
from backend.embedding.factory import EmbeddingFactory

_embedding = None

def get_embedding():
    global _embedding
    if _embedding is None:
        _embedding = EmbeddingFactory.get(**EMBEDDING_CONFIG)
    return _embedding