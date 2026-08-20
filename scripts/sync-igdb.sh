#!/bin/bash

# GamingWeb IGDB 自動同步腳本
# 每天自動從 IGDB 同步最新遊戲資料

API_URL="http://localhost:8001"
LOG_FILE="/var/log/gamingweb-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "開始同步 IGDB 遊戲資料..."

# 同步即將發售的遊戲
log "同步即將發售的遊戲..."
UPCOMING_RESULT=$(curl -s -X POST "$API_URL/sync/igdb/upcoming?limit=100")
UPCOMING_COUNT=$(echo "$UPCOMING_RESULT" | grep -o '"synced_count":[0-9]*' | cut -d':' -f2)
log "即將發售遊戲同步完成: $UPCOMING_COUNT 款"

# 同步熱門遊戲
log "同步熱門遊戲..."
POPULAR_RESULT=$(curl -s -X POST "$API_URL/sync/igdb/popular?limit=100")
POPULAR_COUNT=$(echo "$POPULAR_RESULT" | grep -o '"synced_count":[0-9]*' | cut -d':' -f2)
log "熱門遊戲同步完成: $POPULAR_COUNT 款"

# 獲取總遊戲數量
TOTAL=$(curl -s "$API_URL/games/?limit=1" | grep -o '"total":[0-9]*' | cut -d':' -f2)
log "資料庫總計: $TOTAL 款遊戲"

log "同步完成"
