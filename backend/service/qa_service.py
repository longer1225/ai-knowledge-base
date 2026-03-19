# backend/service/qa_service.py
import json
from typing import AsyncGenerator

from backend.config.backend_base_settings import ENV_MODE, TOP_K
from backend.mapper.qa_mapper import (
    list_all_document_chunks,
    insert_qa_history,
    get_history_by_chat_id
)
from backend.utils.logger import logger
from backend.core.exceptions import ParamException
from backend.utils.embedding_util import get_embedding
from backend.utils.llm_util import get_llm

# 自动标题
from backend.utils.llm_prompt_util import generate_chat_title
from backend.service.chat_service import update_chat_title_service


# ======================
# 主函数
# ======================
async def ask_question_stream(
    question: str,
    user_id: int,
    chat_id: int
) -> AsyncGenerator[str, None]:

    if not question or not question.strip():
        raise ParamException("问题不能为空")

    logger.debug(f"[Service] 用户 {user_id} 提问：{question}")

    # ======================
    # 自动生成标题（第一次对话）
    # ======================
    try:
        msg_list = get_history_by_chat_id(user_id, chat_id)
        logger.info(f"【自动标题】当前消息数量 = {len(msg_list)}")

        if len(msg_list) == 0:
            title = generate_chat_title(question)
            update_chat_title_service(chat_id, user_id, title)
            logger.info(f"✅ 自动生成标题: {title}")

    except Exception as e:
        logger.error(f"❌ 生成标题失败: {e}")

    # ======================
    # 开发模式
    # ======================
    if ENV_MODE == "dev":
        yield "⚠️【开发模式】模型未加载，仅用于接口测试"
        insert_qa_history(user_id, question, "开发模式回复", "", "", chat_id=chat_id)
        return

    try:
        embedding = get_embedding()
        llm = get_llm()

        # ======================
        # 1️⃣ 获取所有文档 chunk
        # ======================
        chunks = list_all_document_chunks()

        if not chunks:
            yield "当前知识库为空，请先上传文档。"
            return

        # ======================
        # 2️⃣ 手写向量检索（简单版）
        # ======================
        query_vec = embedding.embed_documents([question])[0]

        def cosine_sim(a, b):
            import math
            dot = sum(i * j for i, j in zip(a, b))
            norm_a = math.sqrt(sum(i * i for i in a))
            norm_b = math.sqrt(sum(i * i for i in b))
            return dot / (norm_a * norm_b + 1e-8)

        scored_chunks = []
        for c in chunks:
            sim = cosine_sim(query_vec, c.chunk_embedding)
            scored_chunks.append((sim, c))

        # TopK
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_chunks = scored_chunks[:TOP_K]

        # ======================
        # 3️⃣ 构造上下文
        # ======================
        context = "\n\n".join([c.chunk_text for _, c in top_chunks])

        # ======================
        # 4️⃣ 构造 Prompt
        # ======================
        prompt = f"""根据提供的上下文回答问题，不要编造内容。

上下文：
{context}

用户问题：
{question}

请给出准确、简洁的回答："""

        # ======================
        # 5️⃣ 调用 LLM（伪流式）
        # ======================
        full_answer = ""
        result = llm.generate(prompt)

        for ch in result:
            full_answer += ch
            yield ch

        # ======================
        # 6️⃣ 构造来源信息
        # ======================
        source = json.dumps([
            {
                "chunk_id": c.chunk_id,
                "text": c.chunk_text[:100] + "...",
                "score": float(sim)
            }
            for sim, c in top_chunks
        ], ensure_ascii=False)

        similarity_scores = json.dumps(
            [float(sim) for sim, _ in top_chunks]
        )

        # ======================
        # 7️⃣ 保存记录
        # ======================
        insert_qa_history(
            user_id=user_id,
            question=question,
            answer=full_answer,
            source_chunks=source,
            similarity_scores=similarity_scores,
            chat_id=chat_id
        )

    except Exception as e:
        logger.error(f"[Service] 流式问答失败：{e}", exc_info=True)
        yield "【服务出错】"