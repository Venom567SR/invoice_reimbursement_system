from langchain_community.embeddings import HuggingFaceEmbeddings
from utils.exceptions import EmbeddingError, handle_exception
from utils.config import get_config

config = get_config()

@handle_exception
def get_embedding_model():
    try:
        return HuggingFaceEmbeddings(model_name=config["embedding"]["model_name"])
    except Exception as e:
        raise EmbeddingError(f"Failed to load embedding model: {str(e)}")