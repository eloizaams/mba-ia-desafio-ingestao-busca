import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

class PDFIngestor:
    def __init__(self, pdf_path: str, embedding_model: str, pgvector_url: str, pgvector_collection: str):
        self.pdf_path = Path(pdf_path)
        self.embedding_model = embedding_model
        self.pgvector_url = pgvector_url
        self.pgvector_collection = pgvector_collection

    def load_pdf(self) -> List[Document]:
        loader = PyPDFLoader(str(self.pdf_path))
        return loader.load()

    def split_documents(self, docs: List[Document]) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            add_start_index=False
        )
        return splitter.split_documents(docs)

    def enrich_documents(self, docs: List[Document]) -> List[Document]:
        return [
            Document(
                page_content=doc.page_content,
                metadata={k: v for k, v in doc.metadata.items() if v not in ("", None)}
            )
            for doc in docs
        ]

    def generate_ids(self, docs: List[Document]) -> List[str]:
        return [f"doc-{i}" for i in range(len(docs))]

    def store_documents(self, docs: List[Document], ids: List[str]):
        embeddings = OpenAIEmbeddings(model=self.embedding_model)
        store = PGVector(
            embeddings=embeddings,
            collection_name=self.pgvector_collection,
            connection=self.pgvector_url,
            use_jsonb=True,
        )
        store.add_documents(documents=docs, ids=ids)

    def ingest(self):
        print("Carregando PDF...")
        docs = self.load_pdf()
        print(f"{len(docs)} documentos carregados.")
        splits = self.split_documents(docs)
        if not splits:
            raise RuntimeError("No document chunks to ingest.")
        print(f"{len(splits)} chunks gerados.")
        enriched_docs = self.enrich_documents(splits)
        ids = self.generate_ids(enriched_docs)
        print("Armazenando documentos no PGVector...")
        self.store_documents(enriched_docs, ids)
        print("Ingestão finalizada com sucesso!")

def get_env_variable(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Environment variable {key} is not set")
    return value

if __name__ == "__main__":
    load_dotenv()
    print("Iniciando ingestão...")
    # Checa todas as variáveis obrigatórias
    for k in ("OPENAI_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")
           
    pdf_path = get_env_variable("PDF_PATH")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    pgvector_url = get_env_variable("DATABASE_URL")
    pgvector_collection = get_env_variable("PG_VECTOR_COLLECTION_NAME")

    ingestor = PDFIngestor(
        pdf_path=pdf_path,
        embedding_model=embedding_model,
        pgvector_url=pgvector_url,
        pgvector_collection=pgvector_collection
    )
    ingestor.ingest()