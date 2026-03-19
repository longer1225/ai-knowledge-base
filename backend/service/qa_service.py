# backend/service/qa_service.py
import json
from typing import AsyncGenerator

from backend.adapter.langchain.embedding_adapter import LangChainEmbeddingAdapter
from backend.adapter.langchain.llm_adapter import LangChainLLMAdapter
from backend.config.backend_base_settings import ENV_MODE, TOP_K
from backend.mapper.qa_mapper import list_all_document_chunks, insert_qa_history, get_history_by_chat_id
from backend.utils.logger import logger
from backend.core.exceptions import ParamException
from backend.utils.embedding_util import get_embedding
from backend.utils.llm_util import get_llm

# 👇 👇 👇 新增：自动标题生成
from backend.utils.llm_prompt_util import generate_chat_title
from backend.service.chat_service import update_chat_title_service

from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


# ======================
# 增加 chat_id 参数
# ======================
async def ask_question_stream(question: str, user_id: int, chat_id: int) -> AsyncGenerator[str, None]:
    if not question or not question.strip():
        raise ParamException("问题不能为空")

    logger.debug(f"[Service] 用户 {user_id} 提问：{question}")

    # ======================
    # ✅ 先判断！！！在保存之前！！！
    # ======================
    try:
        msg_list = get_history_by_chat_id(user_id, chat_id)
        logger.info(f"【自动标题】当前消息数量 = {len(msg_list)}")  # 日志

        if len(msg_list) == 0:
            title = generate_chat_title(question)
            update_chat_title_service(chat_id, user_id, title)
            logger.info(f"✅ 自动生成标题: {title}")
    except Exception as e:
        logger.error(f"❌ 生成标题失败: {e}")

    # 下面你原来的代码完全不动
    if ENV_MODE == "dev":
        yield "⚠️【开发模式】模型未加载，仅用于接口测试"
        insert_qa_history(user_id, question, "开发模式回复", "", "", chat_id=chat_id)
        return

    try:
        embedding = get_embedding()
        llm = get_llm()

        lc_embedding = LangChainEmbeddingAdapter(embedding)
        lc_llm = LangChainLLMAdapter(llm=llm)

        chunks = list_all_document_chunks()
        documents = [
            Document(page_content=c.chunk_text, metadata={"chunk_id": c.chunk_id})
            for c in chunks
        ]

        db = FAISS.from_documents(documents, lc_embedding)
        retriever = db.as_retriever(search_kwargs={"k": TOP_K})

        prompt = PromptTemplate(
            template="""根据上下文回答问题，不要编造答案。
                上下文：
                {context}
                
                用户问题：{question}
                回答：""",
            input_variables=["context", "question"]
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=lc_llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )

        full_answer = ""
        for token in qa_chain.stream({"query": question}):
            if "result" in token:
                content = token["result"]
                full_answer += content
                yield content

        source_docs = retriever.get_relevant_documents(question)
        source = json.dumps([
            {
                "chunk_id": doc.metadata["chunk_id"],
                "text": doc.page_content[:100] + "...",
                "score": 0.0
            } for doc in source_docs
        ], ensure_ascii=False)

        similarity_scores = json.dumps([0.0] * len(source_docs))

        # ======================
        # 保存时带上 chat_id
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