import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TalentMind AI"
    
    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@db:5432/talentmind"
    )
    
    # Chroma Vector Database path
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    
    # Embedding Model Configuration
    # We default to all-MiniLM-L6-v2 for speed/efficiency, but support swapping to BAAI/bge-large-en-v1.5
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    class Config:
        case_sensitive = True

settings = Settings()
