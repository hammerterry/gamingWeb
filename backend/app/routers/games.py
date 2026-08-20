from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.schemas.game import GameResponse, GameListResponse
from app.services.game_service import GameService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["games"])


class GameImport(BaseModel):
    title: str
    description: Optional[str] = None
    release_date: Optional[str] = None
    cover_url: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    metacritic_score: Optional[int] = None
    rating: Optional[float] = None
    ratings_count: Optional[int] = 0
    system_requirements: Optional[dict] = None
    purchase_links: Optional[dict] = None
    trailer_url: Optional[str] = None
    screenshots: Optional[List[str]] = []
    platforms: Optional[List[str]] = []
    genres: Optional[List[str]] = []


@router.get("/", response_model=GameListResponse)
async def get_games(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    platform: Optional[str] = None,
    genre: Optional[str] = None,
    search: Optional[str] = None,
    ordering: str = Query("release_date", regex="^(release_date|rating|metacritic)$"),
    db: Session = Depends(get_db)
):
    """獲取遊戲列表"""
    game_service = GameService(db)
    games = game_service.get_games(
        skip=skip,
        limit=limit,
        platform=platform,
        genre=genre,
        search=search,
        ordering=ordering
    )
    
    # 計算總數（簡化版，實際應該用 count query）
    total = len(games)
    
    return GameListResponse(total=total, games=games)


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    """獲取遊戲詳細資訊"""
    game_service = GameService(db)
    game = game_service.get_game_by_id(game_id)
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return game


@router.post("/import")
async def import_game(game_data: GameImport, db: Session = Depends(get_db)):
    """匯入遊戲資料"""
    game_service = GameService(db)
    game = game_service.create_game(game_data.dict())
    return {"id": game.id, "title": game.title}
