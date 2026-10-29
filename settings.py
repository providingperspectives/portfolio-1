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

    # 4. Contact form email delivery
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False
    SMTP_SENDER_EMAIL: str = ""
    CONTACT_RECIPIENT_EMAIL: str = "juliusrlnd@gmail.com"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings():
    return Settings()