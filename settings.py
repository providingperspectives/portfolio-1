from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # 1. Base LLM / Chat Model Configuration
    AZURE_OPENAI_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"
    
    # 2. Embedding Configuration
    AZURE_OPENAI_EMBEDDING_KEY: str
    AZURE_OPENAI_EMBEDDING_ENDPOINT: str
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME: str
    AZURE_OPENAI_EMBEDDING_API_VERSION: str = "2024-02-01"
    
    # 3. Vector Database Configuration
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings():
    return Settings()