from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/gamingweb"
    
    # RAWG API
    RAWG_API_KEY: Optional[str] = None
    RAWG_API_URL: str = "https://api.rawg.io/api"
    
    # App
    APP_NAME: str = "GamingWeb API"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()
