import os
import tempfile
from fastapi import UploadFile

from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import TEXT_SPLIT_CONFIG
from backend.core.exceptions import ParamException
from backend.mapper.document_mapper import insert_document, batch_insert_chunks
from backend.models.document_chunk import DocumentChunk
from backend.utils.embedding_util import get_embedding
from backend.utils.logger import logger

# 分块器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=TEXT_SPLIT_CONFIG["chunk_size"],
    chunk_overlap=TEXT_SPLIT_CONFIG["chunk_overlap"],
    separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", "；", ";", "，", ","]
)

# ------------------------------
# 支持格式
# ------------------------------
ALLOWED_SUFFIX = [".txt", ".md", ".docx", ".pdf", ".csv", ".pptx"]


def upload_document(file: UploadFile, user_id: int):
    logger.info("[Service] 开始处理用户 %s 的文件：%s", user_id, file.filename)

    suffix = os.path.splitext(file.filename)[-1].lower()
    if suffix not in ALLOWED_SUFFIX:
        raise ParamException(f"仅支持：{', '.join(ALLOWED_SUFFIX)}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        content = ""

        # ======================
        # 解析文件
        # ======================

        if suffix in [".txt", ".md"]:
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

        elif suffix == ".docx":
            from docx import Document
            doc = Document(tmp_path)
            content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

        elif suffix == ".pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(tmp_path)
            content = "\n".join([
                page.extract_text() or "" for page in reader.pages  # ✅ 防 None
            ])

        elif suffix == ".csv":
            import csv
            rows = []
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    rows.append(" | ".join(row))
            content = "\n".join(rows)

        elif suffix == ".pptx":
            from pptx import Presentation
            prs = Presentation(tmp_path)
            texts = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        texts.append(shape.text)
            content = "\n".join(texts)

        if not content.strip():
            raise ParamException("文件内容为空或无法提取文本")

        # ======================
        # 分块
        # ======================
        chunks = text_splitter.split_text(content)
        logger.debug("[Service] 文件分块完成，共 %s 块", len(chunks))

        # ======================
        # 插入文档
        # ======================
        doc = insert_document(
            user_id=user_id,
            doc_name=file.filename,
            doc_type=suffix[1:],
            file_size=os.path.getsize(tmp_path)
        )

        # ======================
        # embedding（批量优化）
        # ======================
        embedding = get_embedding()

        # 🔥 批量算 embedding（关键优化）
        vectors = embedding.embed_documents(chunks)

        chunk_items = []
        for idx, (text, vec) in enumerate(zip(chunks, vectors)):
            chunk_items.append(DocumentChunk(
                doc_id=doc.doc_id,
                chunk_text=text,
                chunk_embedding=vec,
                chunk_index=idx
            ))

        batch_insert_chunks(chunk_items)

        logger.info("[Service] 文档处理完成，doc_id=%s", doc.doc_id)
        return doc.doc_id

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)