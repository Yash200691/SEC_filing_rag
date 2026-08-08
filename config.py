"""
Application Configuration

Loads all configuration from the .env file
using Pydantic BaseSettings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    """

    # Embedding
    EMBEDDING_MODEL: str = "BAAI/bge-base-en-v1.5"

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    COLLECTION_NAME: str = "financial_rag"
    VECTOR_SIZE: int = 768
    DISTANCE: str = "COSINE"

    # Data
    CHUNK_DIRECTORY: str = "data/chunks"

    # Batch
    BATCH_SIZE: int = 64

    # Grok
    XAI_API_KEY: str
    GROK_MODEL: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()

# Backward-compatible module-level configuration values used by the app.
EMBEDDING_MODEL = settings.EMBEDDING_MODEL
QDRANT_URL = settings.QDRANT_URL
COLLECTION_NAME = settings.COLLECTION_NAME
VECTOR_SIZE = settings.VECTOR_SIZE
CHUNK_DIRECTORY = settings.CHUNK_DIRECTORY
BATCH_SIZE = settings.BATCH_SIZE