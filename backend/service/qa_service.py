import json
from typing import AsyncGenerator

from backend.config.backend_base_settings import ENV_MODE, TOP_K
from backend.mapper.history_mapper import insert_history, get_history_by_chat_id
from backend.utils.logger import logger
from backend.core.exceptions import ParamException
from backend.utils.embedding_util import get_embedding
from backend.utils.llm_util import get_llm
from backend.utils.llm_prompt_util import generate_chat_title
from backend.service.chat_service import update_chat_title_service


async def ask_question_stream(
    question: str,
    user_id: int,
    chat_id: int
) -> AsyncGenerator[str, None]:

    if not question or not question.strip():
        raise ParamException("问题不能为空")

    logger.debug(f"[Service] 用户 {user_id} 提问：{question}")

    # ======================
    # 自动生成标题
    # ======================
    try:
        msg_list = get_history_by_chat_id(user_id, chat_id)
        if len(msg_list) == 0:
            title = generate_chat_title(question)
            update_chat_title_service(chat_id, user_id, title)
    except Exception as e:
        logger.error(f"生成标题失败: {e}")

    # ======================
    # 开发模式
    # ======================
    if ENV_MODE == "dev":
        yield "⚠️【开发模式】模型未加载，仅用于接口测试"
        insert_history(
            user_id=user_id,
            question=question,
            answer="开发模式回复",
            chat_id=chat_id
        )
        return

    try:
        embedding = get_embedding()
        llm = get_llm()
        from backend.utils.redis_cache import redis_cache

        # ======================
        # 加载文档块
        # ======================
        chunks = []
        from backend.mapper.document_mapper import list_user_documents
        docs = list_user_documents(user_id)

        for d in docs:
            doc_id = d["doc_id"]
            cache_key = f"rag:doc:{doc_id}:chunks"
            cache_data = redis_cache.get(cache_key)
            if cache_data:
                chunks.extend(json.loads(cache_data))

        # ======================
        # 向量检索
        # ======================
        context = ""
        top_chunks = []
        if chunks:
            query_vec = embedding.embed_documents([question])[0]
            def cosine_sim(a, b):
                import math
                dot = sum(i * j for i, j in zip(a, b))
                norm_a = math.sqrt(sum(i*i for i in a))
                norm_b = math.sqrt(sum(i*i for i in b))
                return dot / (norm_a * norm_b + 1e-8)

            scored_chunks = []
            for c in chunks:
                sim = cosine_sim(query_vec, c["chunk_embedding"])
                scored_chunks.append((sim, c))

            scored_chunks.sort(key=lambda x: x[0], reverse=True)
            top_chunks = scored_chunks[:TOP_K]
            context = "\n\n".join([c["chunk_text"] for _, c in top_chunks])

        # ======================
        # 🔥🔥🔥 【真正的上下文】加载历史对话
        # ======================
        history = get_history_by_chat_id(user_id, chat_id)
        messages = []

        # 有知识库 → 加上系统提示
        if context.strip():
            messages.append({
                "role": "system",
                "content": f"你是基于文档的智能助手，必须根据文档内容回答，不要编造。\n文档内容：\n{context}"
            })

        # 把历史聊天记录加入上下文
        for msg in history:
            messages.append({"role": "user", "content": msg["question"]})
            messages.append({"role": "assistant", "content": msg["answer"]})

        # 加入当前问题
        messages.append({"role": "user", "content": question})

        # ======================
        # 🔥 构建带上下文的 prompt
        # ======================
        prompt = ""
        for m in messages:
            role = m["role"]
            content = m["content"]
            if role == "system":
                prompt += f"系统：{content}\n"
            elif role == "user":
                prompt += f"用户：{content}\n"
            elif role == "assistant":
                prompt += f"助手：{content}\n"
        prompt += "助手："

        # ======================
        # 流式输出
        # ======================
        full_answer = ""
        result = llm.generate(prompt)
        for ch in result:
            full_answer += ch
            yield ch

        # ======================
        # 保存历史
        # ======================
        source = json.dumps([
            {
                "chunk_id": c.get("chunk_id", 0),
                "text": c.get("chunk_text", "")[:100] + "...",
                "score": float(sim)
            }
            for sim, c in top_chunks
        ], ensure_ascii=False)

        similarity_scores = json.dumps([float(sim) for sim, _ in top_chunks])

        insert_history(
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