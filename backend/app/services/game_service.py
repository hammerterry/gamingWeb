from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.game import Game, Platform, Genre
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GameService:
    def __init__(self, db: Session):
        self.db = db

    def get_games(
        self,
        skip: int = 0,
        limit: int = 20,
        platform: Optional[str] = None,
        genre: Optional[str] = None,
        search: Optional[str] = None,
        ordering: str = "release_date"
    ) -> List[Game]:
        """獲取遊戲列表"""
        query = self.db.query(Game)

        if platform:
            # JSON array 查詢
            query = query.filter(Game.platforms.contains([platform]))
        
        if genre:
            query = query.filter(Game.genres.contains([genre]))
        
        if search:
            query = query.filter(Game.title.ilike(f"%{search}%"))

        # 排序
        if ordering == "release_date":
            query = query.order_by(Game.release_date.desc())
        elif ordering == "rating":
            query = query.order_by(Game.rating.desc())
        elif ordering == "metacritic":
            query = query.order_by(Game.metacritic_score.desc())

        return query.offset(skip).limit(limit).all()

    def get_game_by_id(self, game_id: int) -> Optional[Game]:
        """根據 ID 獲取遊戲"""
        return self.db.query(Game).filter(Game.id == game_id).first()

    def get_game_by_rawg_id(self, rawg_id: int) -> Optional[Game]:
        """根據 RAWG ID 獲取遊戲"""
        return self.db.query(Game).filter(Game.rawg_id == rawg_id).first()

    def get_game_by_title(self, title: str) -> Optional[Game]:
        """根據標題獲取遊戲"""
        return self.db.query(Game).filter(Game.title == title).first()

    def create_game(self, game_data: dict) -> Game:
        """創建遊戲"""
        game = Game(
            rawg_id=game_data.get("rawg_id"),
            title=game_data.get("title"),
            description=game_data.get("description"),
            release_date=game_data.get("release_date"),
            cover_url=game_data.get("cover_url"),
            background_image=game_data.get("background_image"),
            developer=game_data.get("developer"),
            publisher=game_data.get("publisher"),
            metacritic_score=game_data.get("metacritic_score"),
            rating=game_data.get("rating"),
            ratings_count=game_data.get("ratings_count", 0),
            system_requirements=game_data.get("system_requirements"),
            purchase_links=game_data.get("purchase_links"),
            trailer_url=game_data.get("trailer_url"),
            screenshots=game_data.get("screenshots", []),
            platforms=game_data.get("platforms", []),
            genres=game_data.get("genres", []),
        )

        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def update_game(self, game_id: int, game_data: dict) -> Optional[Game]:
        """更新遊戲"""
        game = self.get_game_by_id(game_id)
        if not game:
            return None

        for key, value in game_data.items():
            if hasattr(game, key):
                setattr(game, key, value)

        game.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(game)
        return game
