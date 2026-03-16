import os
import tempfile
from fastapi import UploadFile, HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..models import DocumentChunk
from ..embedding.factory import EmbeddingFactory
from settings import TEXT_SPLIT_CONFIG, EMBEDDING_CONFIG
from backend.mapper.document_mapper import insert_document, batch_insert_chunks

# 分块器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=TEXT_SPLIT_CONFIG["chunk_size"],
    chunk_overlap=TEXT_SPLIT_CONFIG["chunk_overlap"],
    separators=["\n\n", "\n", "。", "！", "？"]
)

# 向量模型
embedding = EmbeddingFactory.get(**EMBEDDING_CONFIG)

# ============================
# ✅ 修复：改成同步函数！！！（最重要的一行）
# ============================
def upload_document(file: UploadFile, user_id: int):
    suffix = os.path.splitext(file.filename)[-1].lower()

    if suffix not in [".txt", ".docx"]:
        raise HTTPException(status_code=400, detail="仅支持 .txt 或 .docx 文件")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        # 同步读取文件
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        # 读取文件
        if suffix == ".txt":
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            from docx import Document as DocxDocument
            doc = DocxDocument(tmp_path)
            content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

        if not content.strip():
            raise HTTPException(status_code=400, detail="文件内容不能为空")

        # 文本分块
        chunks = text_splitter.split_text(content)

        # 插入文档
        doc = insert_document(
            user_id=user_id,
            doc_name=file.filename,
            doc_type=suffix[1:],
            file_size=os.path.getsize(tmp_path)
        )

        chunk_items = []
        for idx, text in enumerate(chunks):
            vec = embedding.embed(text)
            chunk_items.append(DocumentChunk(
                doc_id=doc.doc_id,
                chunk_text=text,
                chunk_embedding=vec,
                chunk_index=idx
            ))

        batch_insert_chunks(chunk_items)

        return doc.doc_id

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)