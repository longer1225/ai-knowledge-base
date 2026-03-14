import os
import tempfile
from sqlalchemy.orm import Session
from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector

from ..models import Document
from settings import GAUSSDB_CONFIG, EMBEDDING_MODEL, TEXT_SPLIT_CONFIG

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=TEXT_SPLIT_CONFIG["chunk_size"],
    chunk_overlap=TEXT_SPLIT_CONFIG["chunk_overlap"],
)

CONNECTION_STRING = f"postgresql+psycopg2://{GAUSSDB_CONFIG['user']}:{GAUSSDB_CONFIG['password']}@{GAUSSDB_CONFIG['host']}:{GAUSSDB_CONFIG['port']}/{GAUSSDB_CONFIG['database']}"

def get_vector_store():
    return PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        collection_name="document_chunks",
    )

async def upload_document(file: UploadFile, db: Session):
    suffix = os.path.splitext(file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        if tmp_path.endswith(".txt"):
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
        elif tmp_path.endswith(".docx"):
            from docx import Document
            doc = Document(tmp_path)
            content = "\n".join([p.text for p in doc.paragraphs])
        else:
            content = ""
    except:
        content = ""

    chunks = text_splitter.split_text(content)
    vs = get_vector_store()
    vs.add_texts(chunks)

    doc = Document(name=file.filename, size=os.path.getsize(tmp_path))
    db.add(doc)
    db.commit()
    os.unlink(tmp_path)
    return doc.id