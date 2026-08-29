from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import get_settings


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENTS_PATH = PROJECT_ROOT / "documents"

VECTOR_STORE_PATH = PROJECT_ROOT / "data" / "chroma_db"


def get_embeddings():
    """Create the Gemini embedding model."""

    settings = get_settings()

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.google_api_key,
    )


def ingest_documents() -> None:
    """Load documents, chunk them, embed them, and store them in Chroma."""

    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8",
        )

        loaded_documents = loader.load()

        for document in loaded_documents:
            document.metadata["source_file"] = file_path.name

        documents.extend(loaded_documents)

    print(
        f"Loaded {len(documents)} documents."
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(
        f"Created {len(chunks)} chunks."
    )

    embeddings = get_embeddings()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_STORE_PATH),
        collection_name="aegis_enterprise",
    )

    print(
        "Documents successfully ingested into ChromaDB."
    )


if __name__ == "__main__":
    ingest_documents()
