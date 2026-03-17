import numpy as np
import json
from backend.embedding.factory import EmbeddingFactory
# ✅ 改用新配置
from config.backend_base_settings import EMBEDDING_CONFIG, ENV_MODE
from backend.mapper.qa_mapper import list_all_document_chunks, insert_qa_history
from utils.logger import logger
from backend.exceptions import ParamException

embedding = EmbeddingFactory.get(**EMBEDDING_CONFIG)

def ask_question(question: str, user_id: int):
    if not question or not question.strip():
        raise ParamException("问题不能为空")

    logger.debug(f"[Service] 用户 {user_id} 提问：{question}")

    # 开发环境直接返回
    if ENV_MODE == "dev":
        answer = "⚠️【开发模式】模型未加载，仅用于接口测试"
        source = ""
        insert_qa_history(user_id, question, answer, source, "")
        return answer, source

    # 生产环境逻辑
    query_emb = embedding.embed(question)
    chunks = list_all_document_chunks()

    scored = []
    for chunk in chunks:
        vec = np.array(chunk.chunk_embedding)
        score = np.dot(vec, query_emb) / (np.linalg.norm(vec) * np.linalg.norm(query_emb))
        scored.append((chunk, round(float(score), 4)))

    scored.sort(key=lambda x: x[1], reverse=True)
    top_chunks = scored[:3]

    context = "\n---\n".join([c.chunk_text for c, s in top_chunks])
    answer = f"基于知识库：\n{context[:400]}"

    source = json.dumps([
        {"chunk_id": c.chunk_id, "text": c.chunk_text[:100]+"...", "score": s}
        for c, s in top_chunks
    ])

    insert_qa_history(
        user_id=user_id,
        question=question,
        answer=answer,
        source_chunks=source,
        similarity_scores=json.dumps([s for _, s in top_chunks])
    )

    return answer, source