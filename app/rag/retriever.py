from pathlib import Path

from langchain_chroma import Chroma

from app.rag.ingest import get_embeddings


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_STORE_PATH = PROJECT_ROOT / "data" / "chroma_db"


def get_vector_store() -> Chroma:
    """Load the persistent Aegis Chroma vector store."""

    embeddings = get_embeddings()

    return Chroma(
        collection_name="aegis_enterprise",
        persist_directory=str(VECTOR_STORE_PATH),
        embedding_function=embeddings,
    )


def retrieve_documents(
    query: str,
    k: int = 4,
) -> list[dict]:
    """Retrieve relevant enterprise document chunks."""

    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        query,
        k=k,
    )

    results = []

    for document in documents:
        results.append(
            {
                "content": document.page_content,
                "source": document.metadata.get(
                    "source_file",
                    "unknown",
                ),
            }
        )

    return results
