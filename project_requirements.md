# GamingWeb — 遊戲資訊網站需求規格書

> 版本：v1.0  
> 日期：2026-08-20  
> 狀態：📋 設計階段  
> Repo：`/root/gamingWeb`

---

## 0. 專案目的

建立一個遊戲資訊網站，讓使用者可以：
- 追蹤新遊戲發售日期
- 瀏覽遊戲詳細資訊（圖片、資料、平台評分）
- 快速判斷哪些遊戲值得關注

---

## 1. 目標用戶

| 用戶 | 需求 |
|------|------|
| 遊戲玩家 | 追蹤即將發售的遊戲、查看評分決定是否購買 |
| 輕度玩家 | 快速瀏覽熱門遊戲、了解評價 |
| 遊戲收藏家 | 按平台/日期整理發售清單 |

---

## 2. 功能需求

### 2.1 首頁 — 即將發售遊戲清單

| # | 功能 | 說明 | 優先級 |
|---|------|------|:--:|
| 2.1.1 | 發售日曆 | 以時間線/日曆視圖顯示即將發售的遊戲 | 🔴 |
| 2.1.2 | 熱門遊戲卡片 | 顯示遊戲封面、名稱、發售日期、平台、評分 | 🔴 |
| 2.1.3 | 平台篩選 | 按 PC/PS5/Xbox/Switch 等平台過濾 | 🔴 |
| 2.1.4 | 日期範圍 | 本週/本月/下月/自訂日期 | 🟠 |
| 2.1.5 | 搜尋 | 遊戲名稱搜尋 | 🟠 |
| 2.1.6 | 排序選項 | 最新發售 / 最高評分 / 最多評論 | 🔴 |

### 2.2 遊戲內頁

| # | 功能 | 說明 | 優先級 |
|---|------|------|:--:|
| 2.2.1 | 遊戲封面圖 | 大尺寸遊戲封面/海報 | 🔴 |
| 2.2.2 | 基本資料 | 發售日期、開發商、發行商、平台、類型 | 🔴 |
| 2.2.3 | 遊戲截圖 | 多張遊戲畫面截圖 | 🔴 |
| 2.2.4 | 平台評分 | Metacritic、Steam、OpenCritic 等平台分數 | 🔴 |
| 2.2.5 | 遊戲簡介 | 遊戲描述/故事背景 | 🟠 |
| 2.2.6 | 官方影片 | 嵌入 YouTube 官方預告片/遊戲介紹影片 | 🔴 |
| 2.2.7 | 購買連結 | Amazon / Steam / PS Store 等購買連結 | 🔴 |
| 2.2.8 | 系統需求 | PC 最低/建議配備 | 🟡 |

### 2.3 評分展示

| # | 功能 | 說明 | 優先級 |
|---|------|------|:--:|
| 2.3.1 | 媒體評分 | Metacritic 媒體綜合分數 | 🔴 |
| 2.3.2 | 玩家評分 | Metacritic 玩家分數 / Steam 評價 | 🔴 |
| 2.3.3 | 多平台分數 | 同一遊戲在不同平台的評分（PS5 vs PC vs Xbox） | 🟠 |
| 2.3.4 | 分數趨勢 | 評分變化趨勢（可選） | 🟡 |

---

## 3. 頁面結構

### 3.1 頁面列表

| 路徑 | 頁面 | 說明 |
|------|------|------|
| `/` | 首頁 | 即將發售遊戲清單 |
| `/game/:id` | 遊戲內頁 | 遊戲詳細資訊 |
| `/calendar` | 發售日曆 | 日曆視圖 |
| `/platform/:platform` | 平台頁面 | 特定平台的遊戲清單 |
| `/search?q=` | 搜尋結果 | 搜尋結果頁 |

### 3.2 首頁佈局

```
┌──────────────────────────────────────────────┐
│  GamingWeb                    [搜尋] [平台▼]  │
├──────────────────────────────────────────────┤
│                                              │
│  🔥 本週發售                                  │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │
│  │ 封面  │ │ 封面  │ │ 封面  │ │ 封面  │        │
│  │ 遊戲A │ │ 遊戲B │ │ 遊戲C │ │ 遊戲D │        │
│  │ 8/25  │ │ 8/26  │ │ 8/27  │ │ 8/28  │        │
│  │ ⭐85  │ │ ⭐78  │ │ ⭐92  │ │ ⭐71  │        │
│  └──────┘ └──────┘ └──────┘ └──────┘        │
│                                              │
│  📅 下月發售                                   │
│  ┌──────┐ ┌──────┐ ┌──────┐                  │
│  │ ...  │ │ ...  │ │ ...  │                  │
│  └──────┘ └──────┘ └──────┘                  │
│                                              │
└──────────────────────────────────────────────┘
```

### 3.3 遊戲內頁佈局

```
┌──────────────────────────────────────────────┐
│  ← 返回                                       │
│                                              │
│  ┌────────────┐  遊戲名稱                      │
│  │            │  發售日期: 2026-09-15          │
│  │  遊戲封面   │  平台: PC, PS5, Xbox Series X  │
│  │            │  開發商: CD Projekt Red         │
│  │            │  類型: RPG, Action             │
│  └────────────┘                               │
│                                              │
│  ⭐ 評分                                      │
│  ┌──────────┬──────────┬──────────┐           │
│  │Metacritic│  Steam   │OpenCritic│           │
│  │   92     │  90% 👍  │   91     │           │
│  └──────────┴──────────┴──────────┘           │
│                                              │
│  📸 截圖                                      │
│  [圖1] [圖2] [圖3] [圖4]                      │
│                                              │
│  📝 遊戲簡介                                   │
│  這是一款開放世界 RPG...                        │
│                                              │
│  🎬 官方影片                                  │
│  ┌─────────────────────────────────────┐      │
│  │        YouTube 預告片嵌入             │      │
│  └─────────────────────────────────────┘      │
│                                              │
│  🛒 購買                                      │
│  [Steam $59.99] [Amazon $54.99] [PS Store]   │
│                                              │
│  💻 系統需求 (PC)                              │
│  最低: i5-10400, GTX 1060, 16GB RAM          │
│  建議: i7-12700, RTX 3070, 32GB RAM          │
└──────────────────────────────────────────────┘
```

---

## 4. 資料模型

### 4.1 Game（遊戲）

```typescript
interface Game {
  id: string;                    // 唯一識別碼
  title: string;                 // 遊戲名稱
  cover_url: string;             // 封面圖片 URL
  screenshots: string[];         // 截圖 URL 列表
  description: string;           // 遊戲簡介
  release_date: string;          // 發售日期 (ISO)
  platforms: Platform[];         // 發售平台
  developer: string;             // 開發商
  publisher: string;             // 發行商
  genres: string[];              // 遊戲類型
  trailer_url?: string;          // YouTube 官方預告片/介紹影片
  purchase_links?: {             // 購買連結
    steam?: string;
    amazon?: string;
    ps_store?: string;
    xbox_store?: string;
    nintendo_eshop?: string;
  };
  system_requirements?: {        // PC 系統需求
    minimum: string;
    recommended: string;
  };
  ratings: GameRating[];         // 各平台評分
  created_at: string;
  updated_at: string;
}
```

### 4.2 Platform（平台）

```typescript
type Platform = 'PC' | 'PS5' | 'PS4' | 'Xbox Series X' | 'Xbox One' | 'Nintendo Switch' | 'Mobile';
```

### 4.3 GameRating（評分）

```typescript
interface GameRating {
  source: 'metacritic' | 'steam' | 'opencritic' | 'ign' | 'gamespot';
  score: number;                 // 0-100
  max_score: number;             // 預設 100
  count?: number;                // 評分人數
  url?: string;                  // 評分來源連結
}
```

### 4.4 User（使用者）— Phase 4

```typescript
interface User {
  id: string;
  email: string;
  username: string;
  avatar_url?: string;
  role: 'user' | 'developer' | 'admin';
  created_at: string;
}
```

### 4.5 UserRating（使用者評分）— Phase 4

```typescript
interface UserRating {
  id: string;
  user_id: string;
  game_id: string;
  score: number;                 // 1-10
  comment: string;               // 文字評論
  rating_type: 'normal' | 'completed';  // 普通評分 / 通關後評分
  completion_proof?: string;     // 通關證明截圖 URL
  proof_status?: 'pending' | 'approved' | 'rejected';
  weight: number;                // 評分權重（普通=1, 通關=2）
  created_at: string;
  updated_at: string;
}
```

### 4.6 IndieGame（獨立遊戲）— Phase 5

```typescript
interface IndieGame extends Game {
  developer_id: string;
  status: 'concept' | 'in_development' | 'alpha' | 'beta' | 'released' | 'early_access';
  updates: DevUpdate[];
  followers: number;
  wishlist_count: number;
}

interface DevUpdate {
  id: string;
  game_id: string;
  title: string;
  content: string;               // Markdown
  media_urls: string[];
  created_at: string;
}
```

### 4.7 評分計算邏輯

```
加權平均分 = (普通評分總和 × 1 + 通關評分總和 × 2) / (普通評分數 × 1 + 通關評分數 × 2)
```

通關評分的權重是普通評分的 2 倍，因為通關玩家對遊戲的理解更全面。


---

## 5. 技術棧建議

| 層 | Phase 1-3（MVP） | Phase 4+（社群） |
|------|------|------|
| 前端 | React + Vite + TypeScript + Tailwind CSS | 同左 |
| 後端 | 無（靜態 JSON） | FastAPI + PostgreSQL |
| 認證 | 無 | JWT + bcrypt |
| 圖片儲存 | 外部 URL | S3 / Cloudflare R2（通關證明截圖） |
| 部署 | Vercel / GitHub Pages | VPS（Docker Compose） |

### MVP 階段：純前端 + JSON 資料

```
gamingWeb/
├── index.html
├── src/
│   ├── App.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── GameDetailPage.tsx
│   │   └── CalendarPage.tsx
│   ├── components/
│   │   ├── GameCard.tsx
│   │   ├── RatingBadge.tsx
│   │   ├── PlatformFilter.tsx
│   │   └── SearchBar.tsx
│   └── data/
│       └── games.json          # 遊戲資料
└── package.json
```

---

## 6. 工作項目

### Phase 1：MVP（P0）

| # | 工作項 | 說明 | 狀態 |
|---|--------|------|:--:|
| 6.1 | 初始化 React + Vite 專案 | 設定 Tailwind CSS | ⬜ |
| 6.2 | 建立 `games.json` 資料檔 | 手動填入 10-20 款熱門遊戲 | ⬜ |
| 6.3 | 首頁 — 遊戲卡片列表 | 顯示封面、名稱、發售日、平台、評分 | ⬜ |
| 6.4 | 遊戲內頁 | 封面、資料、評分、截圖、簡介 | ⬜ |
| 6.5 | 平台篩選 | 按 PC/PS5/Xbox/Switch 過濾 | ⬜ |
| 6.6 | 響應式設計 | 手機/平板/桌面 | ⬜ |

### Phase 2：增強（P1）

| # | 工作項 | 說明 | 狀態 |
|---|--------|------|:--:|
| 6.7 | 發售日曆視圖 | 月曆形式顯示發售日 | ⬜ |
| 6.8 | 搜尋功能 | 遊戲名稱搜尋 | ⬜ |
| 6.9 | 預告片嵌入 | YouTube 嵌入 | ⬜ |
| 6.10 | 系統需求展示 | PC 最低/建議配備 | ⬜ |

### Phase 3：自動化（P2）

| # | 工作項 | 說明 | 狀態 |
|---|--------|------|:--:|
| 6.11 | 自動爬蟲 | 從 Metacritic/Steam 自動更新資料 | ⬜ |
| 6.12 | 後端 API | 用 FastAPI 提供資料 API | ⬜ |
| 6.13 | 資料庫 | PostgreSQL 儲存遊戲資料 | ⬜ |

### Phase 4：社群功能（P2）

| # | 工作項 | 說明 | 狀態 |
|---|--------|------|:--:|
| 6.14 | 登入/註冊 | Email + 密碼註冊，JWT 登入 | ⬜ |
| 6.15 | 使用者資料頁 | 頭像、暱稱、遊戲收藏、評分歷史 | ⬜ |
| 6.16 | 普通評分 | 1-10 分 + 文字評論，可編輯/刪除 | ⬜ |
| 6.17 | 通關後評分 | 需上傳通關證明（截圖）才能評分 | ⬜ |
| 6.18 | 通關證明審核 | 管理員審核通關證明（通過/拒絕） | ⬜ |
| 6.19 | 評分權重 | 通關後評分權重 > 普通評分（如 2:1） | ⬜ |
| 6.20 | 評分排序 | 可按「通關評分優先」排序 | ⬜ |

### Phase 5：獨立遊戲專區（P2）

| # | 工作項 | 說明 | 狀態 |
|---|--------|------|:--:|
| 6.21 | 獨立遊戲列表 | 獨立遊戲專區頁面，與商業遊戲分開 | ⬜ |
| 6.22 | 開發者註冊 | 獨立開發者身分申請（需審核） | ⬜ |
| 6.23 | 開發進度更新 | 開發者發布開發日誌/進度更新 | ⬜ |
| 6.24 | 進度時間線 | 視覺化顯示開發歷程 | ⬜ |
| 6.25 | 願望清單/追蹤 | 玩家可追蹤獨立遊戲，發售時通知 | ⬜ |
| 6.26 | 開發者互動 | 玩家留言/問題，開發者回覆 | ⬜ |

---

## 7. 資料來源

| 來源 | 用途 | 需要 API？ |
|------|------|:--:|
| IGDB (Twitch) | 遊戲資料、封面、截圖 | ✅ 免費 tier |
| RAWG.io | 遊戲資料、評分 | ✅ 免費 20,000 calls/月 |
| Metacritic | 評分 | ❌ 需爬蟲 |
| Steam | PC 評分、價格 | ❌ 需爬蟲 |
| 手動 JSON | MVP 階段 | ❌ |

### MVP 建議：手動維護 JSON

先用 10-20 款熱門遊戲的手動資料建立 MVP，後續再整合 API。

---

## 8. 驗收標準

| # | 驗收項目 | 標準 |
|---|----------|------|
| V1 | 首頁載入 | 顯示遊戲卡片列表，每個卡片有封面、名稱、日期、評分 |
| V2 | 平台篩選 | 選擇 PS5 只顯示 PS5 遊戲 |
| V3 | 遊戲內頁 | 點擊遊戲卡片進入內頁，顯示完整資訊 |
| V4 | 評分展示 | Metacritic/Steam/OpenCritic 分數正確顯示 |
| V5 | 響應式 | 手機上卡片排列正確（1-2 列） |
| V6 | 發售日排序 | 遊戲按發售日由近到遠排列 |

---

*本規格書由 stocktrading-strategist skill 驅動。*