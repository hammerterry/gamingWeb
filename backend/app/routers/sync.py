from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.rawg_client import rawg_client
from app.services.game_service import GameService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/rawg")
async def sync_from_rawg(
    page_size: int = 20,
    dates: str = None,
    db: Session = Depends(get_db)
):
    """從 RAWG API 同步遊戲資料"""
    if not rawg_client.api_key:
        raise HTTPException(status_code=400, detail="RAWG API key not configured")

    game_service = GameService(db)
    
    # 獲取遊戲列表
    rawg_data = await rawg_client.get_games(page_size=page_size, dates=dates)
    
    synced_count = 0
    for rawg_game in rawg_data.get("results", []):
        try:
            # 解析遊戲資料
            game_data = rawg_client.parse_game_data(rawg_game)
            
            # 檢查是否已存在
            existing_game = game_service.get_game_by_rawg_id(game_data["rawg_id"])
            
            if existing_game:
                # 更新現有遊戲
                game_service.update_game(existing_game.id, game_data)
            else:
                # 創建新遊戲
                game_service.create_game(game_data)
            
            synced_count += 1
        except Exception as e:
            logger.error(f"Error syncing game {rawg_game.get('name')}: {e}")
            continue

    return {
        "message": f"Successfully synced {synced_count} games",
        "synced_count": synced_count
    }


@router.post("/rawg/{game_id}/details")
async def sync_game_details(
    game_id: int,
    db: Session = Depends(get_db)
):
    """同步特定遊戲的詳細資訊（截圖、系統需求等）"""
    if not rawg_client.api_key:
        raise HTTPException(status_code=400, detail="RAWG API key not configured")

    game_service = GameService(db)
    game = game_service.get_game_by_rawg_id(game_id)
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # 獲取詳細資訊
    details = await rawg_client.get_game_details(game_id)
    
    # 獲取截圖
    screenshots_data = await rawg_client.get_game_screenshots(game_id)
    screenshots = [s.get("image") for s in screenshots_data if s.get("image")]
    
    # 更新遊戲
    update_data = {
        "system_requirements": details.get("requirements"),
        "purchase_links": details.get("stores"),
        "trailer_url": details.get("clip", {}).get("clip") if details.get("clip") else None,
        "screenshots": screenshots,
    }
    
    game_service.update_game(game.id, update_data)
    
    return {
        "message": "Game details synced successfully",
        "game_id": game.id
    }
