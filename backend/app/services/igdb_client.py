import httpx
from typing import List, Dict, Any
from datetime import datetime
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class IGDBClient:
    def __init__(self):
        self.client_id = settings.IGDB_CLIENT_ID
        self.client_secret = settings.IGDB_CLIENT_SECRET
        self.api_url = settings.IGDB_API_URL
        self.access_token = None
        self.token_expires_at = None

    async def _get_access_token(self) -> str:
        """獲取 Twitch OAuth access token"""
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://id.twitch.tv/oauth2/token",
                params={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials"
                }
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data["access_token"]
            # Token 有效期約 60 天，但我們每次重新獲取確保安全
            self.token_expires_at = datetime.now()
            return self.access_token

    async def _make_request(self, endpoint: str, body: str) -> List[Dict]:
        """發送 IGDB API 請求"""
        token = await self._get_access_token()
        
        headers = {
            "Client-ID": str(self.client_id),
            "Authorization": f"Bearer {token}",
            "Content-Type": "text/plain"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/{endpoint}",
                headers=headers,
                content=body,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_upcoming_games(self, limit: int = 50) -> List[Dict]:
        """獲取即將發售的遊戲"""
        now = int(datetime.now().timestamp())
        future = int((datetime.now().timestamp()) + (90 * 24 * 60 * 60))  # 90 天後
        
        body = f"""
        fields name, summary, cover.url, first_release_date, platforms.name, 
               genres.name, involved_companies.company.name, involved_companies.developer,
               aggregated_rating, aggregated_rating_count, url, screenshots.url,
               videos.video_id, websites.url, websites.category;
        where first_release_date >= {now} & first_release_date <= {future};
        sort first_release_date asc;
        limit {limit};
        """
        
        try:
            games = await self._make_request("games", body)
            return games
        except Exception as e:
            logger.error(f"Error fetching upcoming games from IGDB: {e}")
            return []

    async def get_popular_games(self, limit: int = 50) -> List[Dict]:
        """獲取熱門遊戲"""
        body = f"""
        fields name, summary, cover.url, first_release_date, platforms.name,
               genres.name, involved_companies.company.name, involved_companies.developer,
               aggregated_rating, aggregated_rating_count, url, screenshots.url,
               videos.video_id, websites.url, websites.category;
        sort aggregated_rating desc;
        limit {limit};
        """
        
        try:
            games = await self._make_request("games", body)
            return games
        except Exception as e:
            logger.error(f"Error fetching popular games from IGDB: {e}")
            return []

    def parse_game_data(self, igdb_game: Dict) -> Dict:
        """解析 IGDB 遊戲資料為我們的格式"""
        # 提取開發商
        developer = None
        publisher = None
        for company in igdb_game.get("involved_companies", []):
            if company.get("developer"):
                developer = company["company"]["name"]
            else:
                publisher = company["company"]["name"]

        # 提取平台
        platforms = [p["name"] for p in igdb_game.get("platforms", [])]

        # 提取類型
        genres = [g["name"] for g in igdb_game.get("genres", [])]

        # 提取截圖
        screenshots = []
        for screenshot in igdb_game.get("screenshots", []):
            if screenshot.get("url"):
                # IGDB 返回的圖片 URL 需要轉換為高清版本
                url = screenshot["url"].replace("t_thumb", "t_screenshot_huge")
                screenshots.append(f"https:{url}")

        # 提取影片（YouTube）
        trailer_url = None
        for video in igdb_game.get("videos", []):
            if video.get("video_id"):
                trailer_url = f"https://www.youtube.com/watch?v={video['video_id']}"
                break

        # 提取購買連結
        purchase_links = {}
        for website in igdb_game.get("websites", []):
            category = website.get("category")
            url = website.get("url")
            if category == 1:  # Steam
                purchase_links["steam"] = url
            elif category == 13:  # PlayStation
                purchase_links["ps_store"] = url
            elif category == 14:  # Xbox
                purchase_links["xbox_store"] = url
            elif category == 15:  # Nintendo
                purchase_links["nintendo_eshop"] = url

        # 轉換發售日期
        release_date = None
        if igdb_game.get("first_release_date"):
            release_date = datetime.fromtimestamp(igdb_game["first_release_date"]).isoformat()

        # 提取封面圖片
        cover_url = None
        if igdb_game.get("cover", {}).get("url"):
            cover_url = f"https:{igdb_game['cover']['url']}".replace("t_thumb", "t_cover_big")

        return {
            "rawg_id": igdb_game.get("id"),  # 使用 IGDB ID 作為 rawg_id
            "title": igdb_game.get("name", "Unknown"),
            "description": igdb_game.get("summary", ""),
            "release_date": release_date,
            "cover_url": cover_url,
            "developer": developer,
            "publisher": publisher,
            "platforms": platforms,
            "genres": genres,
            "metacritic_score": None,  # IGDB 沒有 Metacritic 分數
            "rating": igdb_game.get("aggregated_rating"),
            "ratings_count": igdb_game.get("aggregated_rating_count", 0),
            "screenshots": screenshots,
            "trailer_url": trailer_url,
            "purchase_links": purchase_links,
            "system_requirements": None,  # IGDB 沒有系統需求
        }


igdb_client = IGDBClient()
