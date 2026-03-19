from .base import BaseEmbedding
from openai import OpenAI


class QwenEmbedding(BaseEmbedding):
    def __init__(self, api_key: str, model_name: str = "text-embedding-v1"):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model_name = model_name

    def embed(self, text: str) -> list[float]:
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Qwen 嵌入失败: {str(e)}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise Exception(f"Qwen 批量嵌入失败: {str(e)}")