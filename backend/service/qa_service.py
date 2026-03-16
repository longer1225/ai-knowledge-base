from sqlalchemy.orm import Session
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM

from ..models import QAHistory
# from .upload_service import get_vector_store
"""
class MockLLM(LLM):
    def _call(self, prompt: str, stop=None):
        return f"【LangChain 生成回答】\n根据知识库内容：\n{prompt[:300]}..."
    @property
    def _llm_type(self):
        return "mock"

llm = MockLLM()

def ask_question(question: str, db: Session):
    vs = get_vector_store()
    retriever = vs.as_retriever(search_kwargs={"k": 3})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

    result = qa_chain({"query": question})
    answer = result["result"]
    source_docs = result["source_documents"]

    history = QAHistory(question=question, answer=answer)
    db.add(history)
    db.commit()

    source_text = "\n\n----------------\n\n".join([d.page_content for d in source_docs])
    return answer, source_text
"""