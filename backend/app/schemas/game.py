from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PlatformBase(BaseModel):
    name: str


class GenreBase(BaseModel):
    name: str


class GameBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_date: Optional[datetime] = None
    cover_url: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    metacritic_score: Optional[int] = None
    rating: Optional[float] = None


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass


class GameResponse(GameBase):
    id: int
    rawg_id: Optional[int] = None
    background_image: Optional[str] = None
    ratings_count: int = 0
    system_requirements: Optional[dict] = None
    purchase_links: Optional[dict] = None
    trailer_url: Optional[str] = None
    screenshots: List[str] = []
    platforms: List[str] = []
    genres: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GameListResponse(BaseModel):
    total: int
    games: List[GameResponse]
