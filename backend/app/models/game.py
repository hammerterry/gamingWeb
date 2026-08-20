from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    rawg_id = Column(Integer, unique=True, index=True, nullable=True)
    
    # 基本資訊
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    release_date = Column(DateTime, nullable=True)
    
    # 圖片
    cover_url = Column(String, nullable=True)
    background_image = Column(String, nullable=True)
    
    # 開發商/發行商
    developer = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    
    # 評分
    metacritic_score = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    ratings_count = Column(Integer, default=0)
    
    # 系統需求 (JSON)
    system_requirements = Column(JSON, nullable=True)
    
    # 購買連結 (JSON)
    purchase_links = Column(JSON, nullable=True)
    
    # 預告片
    trailer_url = Column(String, nullable=True)
    
    # 截圖 (JSON array)
    screenshots = Column(JSON, default=list)
    
    # 平台和類型 (JSON arrays)
    platforms = Column(JSON, default=list)
    genres = Column(JSON, default=list)
    
    # 時間戳
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
