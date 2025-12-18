from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Unified Cyber Defense Platform"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "cyber_defense_db"
    DATABASE_URL: str = "sqlite+aiosqlite:///./local_dev.db"
    
    SECRET_KEY: str = "local_dev_secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    REDIS_URL: str = "redis://localhost:6379/0" # Will fail if no redis, but we can try
    
    class Config:
        case_sensitive = True
        # In docker, these are env vars. Local fallback can be .env
        env_file = ".env"

settings = Settings()
