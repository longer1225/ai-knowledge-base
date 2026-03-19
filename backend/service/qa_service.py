import json
from typing import AsyncGenerator

# 适配器
from backend.adapter.langchain.embedding_adapter import LangChainEmbeddingAdapter
from backend.adapter.langchain.llm_adapter import LangChainLLMAdapter

# 配置 & 工具
from backend.config.backend_base_settings import ENV_MODE, TOP_K
from backend.mapper.qa_mapper import list_all_document_chunks, insert_qa_history
from backend.utils.logger import logger
from backend.core.exceptions import ParamException

# 模型工具
from backend.utils.embedding_util import get_embedding
from backend.utils.llm_util import get_llm

# LangChain
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


# 函数签名变成异步生成器（支持流式）
async def ask_question_stream(question: str, user_id: int) -> AsyncGenerator[str, None]:
    if not question or not question.strip():
        raise ParamException("问题不能为空")

    logger.debug(f"[Service] 用户 {user_id} 提问：{question}")

    # 开发模式
    if ENV_MODE == "dev":
        yield "⚠️【开发模式】模型未加载，仅用于接口测试"
        insert_qa_history(user_id, question, "开发模式回复", "", "")
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

        # ====================== 从配置读取 TOP_K ======================
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

        # ====================== 流式输出 ======================
        full_answer = ""
        for token in qa_chain.stream({"query": question}):
            if "result" in token:
                content = token["result"]
                full_answer += content
                yield content

        # ====================== 最后保存历史（不变） ======================
        source_docs = retriever.get_relevant_documents(question)
        source = json.dumps([
            {
                "chunk_id": doc.metadata["chunk_id"],
                "text": doc.page_content[:100] + "...",
                "score": 0.0
            } for doc in source_docs
        ], ensure_ascii=False)

        similarity_scores = json.dumps([0.0] * len(source_docs))

        insert_qa_history(
            user_id=user_id,
            question=question,
            answer=full_answer,
            source_chunks=source,
            similarity_scores=similarity_scores
        )

    except Exception as e:
        logger.error(f"[Service] 流式问答失败：{e}", exc_info=True)
        yield "【服务出错】"