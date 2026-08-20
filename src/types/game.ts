export type Platform = 'PC' | 'PS5' | 'PS4' | 'Xbox Series X' | 'Xbox One' | 'Nintendo Switch' | 'Mobile';

export interface GameRating {
  source: 'metacritic' | 'steam' | 'opencritic' | 'ign' | 'gamespot';
  score: number;
  max_score: number;
  count?: number;
  url?: string;
}

export interface Game {
  id: string;
  title: string;
  cover_url: string;
  screenshots: string[];
  description: string;
  release_date: string;
  platforms: Platform[];
  developer: string;
  publisher: string;
  genres: string[];
  trailer_url?: string;
  purchase_links?: {
    steam?: string;
    amazon?: string;
    ps_store?: string;
    xbox_store?: string;
    nintendo_eshop?: string;
  };
  system_requirements?: {
    minimum: string;
    recommended: string;
  };
  ratings: GameRating[];
  created_at: string;
  updated_at: string;
}
