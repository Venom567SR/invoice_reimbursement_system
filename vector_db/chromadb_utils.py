from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings

from utils.config import get_config
from utils.exceptions import VectorDBConnectionError, VectorDBError, handle_exception

config = get_config()

@handle_exception
def get_chroma_db(embedding: Embeddings):
    try:
        return Chroma(
            collection_name=config["vector_db"]["collection_name"],
            embedding_function=embedding,
            persist_directory=config["vector_db"]["persist_directory"]
        )
    except Exception as e:
        raise VectorDBConnectionError(f"Could not connect to ChromaDB: {str(e)}")

@handle_exception
def add_invoice_to_vector_store(db: Chroma, text: str, metadata: dict):
    try:
        db.add_texts([text], metadatas=[metadata])
        db.persist()
    except Exception as e:
        raise VectorDBError(f"Failed to add document to vector store: {str(e)}")

@handle_exception
def search_documents(db: Chroma, query: str, k: int = 5):
    try:
        return db.similarity_search(query, k=k)
    except Exception as e:
        raise VectorDBError(f"Failed to search vector store: {str(e)}")