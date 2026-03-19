from backend.llm.factory import LLMFactory
from backend.config.backend_base_settings import LLM_CONFIG

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = LLMFactory.get(**LLM_CONFIG)
    return _llm