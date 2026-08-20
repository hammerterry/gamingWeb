#!/usr/bin/env python3
"""從靜態 JSON 匯入遊戲資料到資料庫"""
import json
import sys
from pathlib import Path
import httpx

# 讀取靜態遊戲資料
games_file = Path(__file__).parent.parent.parent / 'src' / 'data' / 'games.json'
with open(games_file, 'r', encoding='utf-8') as f:
    games = json.load(f)

API_URL = "http://localhost:8001/games/import"

def import_game(game):
    """匯入單個遊戲"""
    payload = {
        "title": game['title'],
        "description": game.get('description', ''),
        "release_date": game.get('release_date'),
        "cover_url": game.get('cover_url'),
        "developer": game.get('developer'),
        "publisher": game.get('publisher'),
        "platforms": game.get('platforms', []),
        "genres": game.get('genres', []),
        "metacritic_score": next((r['score'] for r in game.get('ratings', []) if r['source'] == 'metacritic'), None),
        "rating": next((r['score'] for r in game.get('ratings', []) if r['source'] == 'steam'), None),
        "ratings_count": next((r.get('count', 0) for r in game.get('ratings', []) if r['source'] == 'steam'), 0),
        "screenshots": game.get('screenshots', []),
        "trailer_url": game.get('trailer_url'),
        "purchase_links": game.get('purchase_links'),
        "system_requirements": game.get('system_requirements'),
    }
    
    response = httpx.post(API_URL, json=payload, timeout=10)
    if response.status_code == 200:
        result = response.json()
        print(f"✓ 已匯入: {game['title']} (ID: {result['id']})")
        return True
    else:
        print(f"✗ 匯入失敗: {game['title']} - {response.text}")
        return False

def main():
    print(f"開始匯入 {len(games)} 款遊戲...")
    success = 0
    for game in games:
        if import_game(game):
            success += 1
    
    print(f"\n匯入完成: {success}/{len(games)} 款遊戲")

if __name__ == "__main__":
    main()
