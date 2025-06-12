class InvoiceSystemException(Exception):
    """Base exception for Invoice Reimbursement System"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

# File-related
class FileProcessingError(InvoiceSystemException): pass
class PDFParsingError(FileProcessingError): pass
class ZipExtractionError(FileProcessingError): pass

# LLM-related
class LLMError(InvoiceSystemException): pass
class LLMConnectionError(LLMError): pass
class LLMResponseError(LLMError): pass

# VectorDB
class VectorDBError(InvoiceSystemException): pass
class VectorDBConnectionError(VectorDBError): pass

# Embeddings
class EmbeddingError(InvoiceSystemException): pass

# Config
class ConfigurationError(InvoiceSystemException): pass

# Validation/API
class ValidationError(InvoiceSystemException): pass
class APIError(InvoiceSystemException): pass
class AuthenticationError(InvoiceSystemException): pass

# Batch Processing
class BatchProcessingError(InvoiceSystemException): pass

# Error code constants
class ErrorCodes:
    FILE_NOT_FOUND = "FILE_001"
    INVALID_FILE_FORMAT = "FILE_003"
    EXTRACTION_FAILED = "FILE_004"

    LLM_CONNECTION_FAILED = "LLM_001"
    LLM_INVALID_RESPONSE = "LLM_002"

    VECTOR_DB_CONNECTION_FAILED = "VDB_001"
    VECTOR_DB_INSERT_FAILED = "VDB_003"

    EMBEDDING_FAILED = "EMB_001"
    CONFIG_FILE_NOT_FOUND = "CFG_001"

    INVALID_INPUT_FORMAT = "VAL_001"
    BATCH_PROCESSING_FAILED = "BCH_001"
    INVALID_REQUEST = "API_001"

# Decorator for safe execution with logging
from functools import wraps
from utils.logger import app_logger

def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvoiceSystemException as e:
            app_logger.error(f"[{e.error_code}] {e.message}")
            raise
        except Exception as e:
            app_logger.exception(f"Unhandled Exception in {func.__name__}")
            raise InvoiceSystemException(
                f"Unexpected error in {func.__name__}: {str(e)}",
                "UNEXPECTED_001"
            )
    return wrapper