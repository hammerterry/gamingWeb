import httpx
from typing import List, Dict, Any, Optional
from app.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RAWGClient:
    def __init__(self):
        self.api_key = settings.RAWG_API_KEY
        self.base_url = settings.RAWG_API_URL

    async def get_games(
        self,
        page: int = 1,
        page_size: int = 20,
        dates: Optional[str] = None,
        platforms: Optional[str] = None,
        search: Optional[str] = None,
        ordering: str = "-released"
    ) -> Dict[str, Any]:
        """從 RAWG API 獲取遊戲列表"""
        params = {
            "key": self.api_key,
            "page": page,
            "page_size": page_size,
            "ordering": ordering,
        }
        
        if dates:
            params["dates"] = dates
        if platforms:
            params["platforms"] = platforms
        if search:
            params["search"] = search

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/games",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error fetching games from RAWG: {e}")
                return {"results": [], "count": 0}

    async def get_game_details(self, game_id: int) -> Dict[str, Any]:
        """獲取遊戲詳細資訊"""
        params = {"key": self.api_key}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/games/{game_id}",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error fetching game details from RAWG: {e}")
                return {}

    async def get_game_screenshots(self, game_id: int) -> List[Dict[str, Any]]:
        """獲取遊戲截圖"""
        params = {"key": self.api_key}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/games/{game_id}/screenshots",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("results", [])
            except Exception as e:
                logger.error(f"Error fetching screenshots from RAWG: {e}")
                return []

    def parse_game_data(self, rawg_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析 RAWG 遊戲資料為我們的格式"""
        # 提取平台
        platforms = []
        for platform in rawg_data.get("platforms", []):
            platform_info = platform.get("platform", {})
            if platform_info:
                platforms.append(platform_info.get("name"))

        # 提取類型
        genres = []
        for genre in rawg_data.get("genres", []):
            if genre.get("name"):
                genres.append(genre.get("name"))

        # 解析發售日期
        release_date = None
        if rawg_data.get("released"):
            try:
                release_date = datetime.fromisoformat(
                    rawg_data.get("released").replace("Z", "+00:00")
                )
            except:
                pass

        return {
            "rawg_id": rawg_data.get("id"),
            "title": rawg_data.get("name"),
            "description": rawg_data.get("description_raw"),
            "release_date": release_date,
            "cover_url": rawg_data.get("background_image"),
            "background_image": rawg_data.get("background_image_additional"),
            "developer": rawg_data.get("developers", [{}])[0].get("name") if rawg_data.get("developers") else None,
            "publisher": rawg_data.get("publishers", [{}])[0].get("name") if rawg_data.get("publishers") else None,
            "metacritic_score": rawg_data.get("metacritic"),
            "rating": rawg_data.get("rating"),
            "ratings_count": rawg_data.get("ratings_total"),
            "platforms": platforms,
            "genres": genres,
        }


rawg_client = RAWGClient()
