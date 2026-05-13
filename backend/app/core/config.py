from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Transport Company System"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    DATABASE_URL: str = "postgresql://transport_user:transport_pass@localhost:5432/transport_db"
    
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()