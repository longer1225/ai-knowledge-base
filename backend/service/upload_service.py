import os
import tempfile
from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..models import DocumentChunk
from backend.embedding.factory import EmbeddingFactory
from config.backend_base_settings import TEXT_SPLIT_CONFIG, EMBEDDING_CONFIG
from backend.mapper.document_mapper import insert_document, batch_insert_chunks
from utils.logger import logger
from backend.exceptions import ParamException

# 分块器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=TEXT_SPLIT_CONFIG["chunk_size"],
    chunk_overlap=TEXT_SPLIT_CONFIG["chunk_overlap"],
    separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?"]
)

# 向量模型
embedding = EmbeddingFactory.get(**EMBEDDING_CONFIG)

# ------------------------------
# 支持格式：txt、md、docx、pdf、csv、pptx
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
        # ==========================================
        # 【核心：不同文件 → 不同读取 → 最终都是文本】
        # ==========================================
        content = ""

        # 1. TXT
        if suffix == ".txt":
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

        # 2. MD
        elif suffix == ".md":
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

        # 3. DOCX
        elif suffix == ".docx":
            from docx import Document
            doc = Document(tmp_path)
            content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

        # 4. PDF
        elif suffix == ".pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(tmp_path)
            content = "\n".join([page.extract_text() for page in reader.pages])

        # 5. CSV
        elif suffix == ".csv":
            import csv
            rows = []
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    rows.append(" | ".join(row))
            content = "\n".join(rows)

        # 6. PPTX
        elif suffix == ".pptx":
            from pptx import Presentation
            prs = Presentation(tmp_path)
            content = ""
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        content += shape.text + "\n"

        if not content.strip():
            raise ParamException("文件内容为空或无法提取文本")

        # ==========================================
        # 以下逻辑：分块、向量、入库 → 全部统一！
        # ==========================================
        chunks = text_splitter.split_text(content)
        logger.debug("[Service] 文件分块完成，共 %s 块", len(chunks))

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
        logger.info("[Service] 文档处理完成，doc_id=%s", doc.doc_id)
        return doc.doc_id

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)