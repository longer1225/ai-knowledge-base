import requests
from .base import BaseEmbedding


class OllamaEmbedding(BaseEmbedding):
    def __init__(self, model: str = "mxbai-embed-large", host: str = "http://localhost:11434"):
        self.url = f"{host}/api/embeddings"
        self.model = model

    def embed(self, text: str) -> list[float]:
        try:
            r = requests.post(self.url, json={
                "model": self.model,
                "prompt": text
            }, timeout=30)

            return r.json()["embedding"]

        except Exception as e:
            raise Exception(f"Ollama 嵌入失败: {str(e)}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # ⚠️ Ollama目前不支持真正批量 → 只能循环
        return [self.embed(t) for t in texts]