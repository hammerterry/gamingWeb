from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.igdb_client import igdb_client
from app.services.game_service import GameService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/igdb/upcoming")
async def sync_upcoming_games(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """從 IGDB 同步即將發售的遊戲"""
    if not igdb_client.client_id or not igdb_client.client_secret:
        raise HTTPException(status_code=400, detail="IGDB credentials not configured")

    game_service = GameService(db)
    
    # 獲取即將發售的遊戲
    igdb_games = await igdb_client.get_upcoming_games(limit=limit)
    
    synced_count = 0
    for igdb_game in igdb_games:
        try:
            game_data = igdb_client.parse_game_data(igdb_game)
            
            # 檢查是否已存在
            existing = game_service.get_game_by_title(game_data["title"])
            
            if existing:
                # 更新現有遊戲
                game_service.update_game(existing.id, game_data)
            else:
                # 創建新遊戲
                game_service.create_game(game_data)
            
            synced_count += 1
        except Exception as e:
            logger.error(f"Error syncing game {igdb_game.get('name')}: {e}")
            continue

    return {
        "message": f"Successfully synced {synced_count} upcoming games",
        "synced_count": synced_count
    }


@router.post("/igdb/popular")
async def sync_popular_games(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """從 IGDB 同步熱門遊戲"""
    if not igdb_client.client_id or not igdb_client.client_secret:
        raise HTTPException(status_code=400, detail="IGDB credentials not configured")

    game_service = GameService(db)
    
    # 獲取熱門遊戲
    igdb_games = await igdb_client.get_popular_games(limit=limit)
    
    synced_count = 0
    for igdb_game in igdb_games:
        try:
            game_data = igdb_client.parse_game_data(igdb_game)
            
            # 檢查是否已存在
            existing = game_service.get_game_by_title(game_data["title"])
            
            if existing:
                # 更新現有遊戲
                game_service.update_game(existing.id, game_data)
            else:
                # 創建新遊戲
                game_service.create_game(game_data)
            
            synced_count += 1
        except Exception as e:
            logger.error(f"Error syncing game {igdb_game.get('name')}: {e}")
            continue

    return {
        "message": f"Successfully synced {synced_count} popular games",
        "synced_count": synced_count
    }
