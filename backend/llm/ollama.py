import requests
from .base import BaseLLM

class OllamaLLM(BaseLLM):
    """Ollama本地大模型实现"""
    def __init__(self, model: str = "qwen2:7b", host: str = "http://localhost:11434"):
        self.url = f"{host}/api/generate"
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            r = requests.post(
                self.url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=60
            )
            return r.json()["response"]
        except Exception as e:
            raise Exception(f"Ollama LLM调用失败: {str(e)}")