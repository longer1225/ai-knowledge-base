import os
import tempfile
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..models import Document, DocumentChunk
from ..embedding.factory import EmbeddingFactory
from settings import TEXT_SPLIT_CONFIG, EMBEDDING_CONFIG

# 分块器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=TEXT_SPLIT_CONFIG["chunk_size"],
    chunk_overlap=TEXT_SPLIT_CONFIG["chunk_overlap"],
    separators=["\n\n", "\n", "。", "！", "？"]
)

# 模型（mock 轻量版，不占内存）
embedding = EmbeddingFactory.get(**EMBEDDING_CONFIG)

async def upload_document(file: UploadFile, user_id: int, db: Session):
    suffix = os.path.splitext(file.filename)[-1].lower()

    # ↓↓↓ 这里会导致 400，必须严格校验
    if suffix not in [".txt", ".docx"]:
        raise HTTPException(status_code=400, detail="仅支持 .txt 或 .docx 文件")

    # 临时文件（修复笔误）
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
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

        # 空内容直接报 400
        if not content or len(content.strip()) == 0:
            raise HTTPException(status_code=400, detail="文件内容不能为空")

        # 分块
        chunks = text_splitter.split_text(content)

        # 存文档
        doc = Document(
            user_id=user_id,
            doc_name=file.filename,
            doc_type=suffix[1:],
            file_size=os.path.getsize(tmp_path),
            status="processed"
        )
        db.add(doc)
        db.flush()
        doc_id = doc.doc_id

        # 存分块 + 向量
        chunk_items = []
        for idx, text in enumerate(chunks):
            vec = embedding.embed(text)
            chunk_items.append(DocumentChunk(
                doc_id=doc_id,
                chunk_text=text,
                chunk_embedding=vec,
                chunk_index=idx
            ))

        db.add_all(chunk_items)
        db.commit()
        return doc_id

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)