from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/gamingweb"
    
    # RAWG API
    RAWG_API_KEY: Optional[str] = None
    RAWG_API_URL: str = "https://api.rawg.io/api"
    
    # IGDB API (Twitch)
    IGDB_CLIENT_ID: Optional[str] = None
    IGDB_CLIENT_SECRET: Optional[str] = None
    IGDB_API_URL: str = "https://api.igdb.com/v4"
    
    # App
    APP_NAME: str = "GamingWeb API"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()
