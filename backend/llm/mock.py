from .base import BaseLLM

class MockLLM(BaseLLM):
    """模拟LLM，开发环境用"""
    def generate(self, prompt: str) -> str:
        return "⚠️【开发模式】LLM测试回复"