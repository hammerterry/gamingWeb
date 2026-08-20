import type { Game } from '../types/game';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/games';

export interface GameListResponse {
  total: number;
  games: Game[];
}

export async function fetchGames(params: {
  skip?: number;
  limit?: number;
  platform?: string;
  genre?: string;
  search?: string;
  ordering?: string;
} = {}): Promise<GameListResponse> {
  const searchParams = new URLSearchParams();
  
  if (params.skip) searchParams.append('skip', params.skip.toString());
  if (params.limit) searchParams.append('limit', params.limit.toString());
  if (params.platform) searchParams.append('platform', params.platform);
  if (params.genre) searchParams.append('genre', params.genre);
  if (params.search) searchParams.append('search', params.search);
  if (params.ordering) searchParams.append('ordering', params.ordering);

  const url = `${API_BASE_URL}/?${searchParams.toString()}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch games: ${response.statusText}`);
  }
  
  const data = await response.json();
  
  // 轉換 API 資料格式為前端格式
  const games: Game[] = data.games.map((g: any) => ({
    id: g.id.toString(),
    title: g.title,
    cover_url: g.cover_url || '',
    screenshots: g.screenshots || [],
    description: g.description || '',
    release_date: g.release_date || '',
    platforms: Array.isArray(g.platforms) && g.platforms.length > 0 && typeof g.platforms[0] === 'object'
      ? g.platforms.map((p: any) => p.name)
      : (g.platforms || []),
    developer: g.developer || '',
    publisher: g.publisher || '',
    genres: Array.isArray(g.genres) && g.genres.length > 0 && typeof g.genres[0] === 'object'
      ? g.genres.map((gen: any) => gen.name)
      : (g.genres || []),
    trailer_url: g.trailer_url,
    purchase_links: g.purchase_links,
    system_requirements: g.system_requirements,
    ratings: g.metacritic_score ? [{ source: 'metacritic', score: g.metacritic_score, max_score: 100 }] : [],
    created_at: g.created_at,
    updated_at: g.updated_at,
  }));
  
  return { total: data.total, games };
}

export async function fetchGameById(id: string): Promise<Game> {
  const url = `${API_BASE_URL}/${id}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch game: ${response.statusText}`);
  }
  
  const g = await response.json();
  
  // 轉換 API 資料格式為前端格式
  return {
    id: g.id.toString(),
    title: g.title,
    cover_url: g.cover_url || '',
    screenshots: g.screenshots || [],
    description: g.description || '',
    release_date: g.release_date || '',
    platforms: Array.isArray(g.platforms) && g.platforms.length > 0 && typeof g.platforms[0] === 'object'
      ? g.platforms.map((p: any) => p.name)
      : (g.platforms || []),
    developer: g.developer || '',
    publisher: g.publisher || '',
    genres: Array.isArray(g.genres) && g.genres.length > 0 && typeof g.genres[0] === 'object'
      ? g.genres.map((gen: any) => gen.name)
      : (g.genres || []),
    trailer_url: g.trailer_url,
    purchase_links: g.purchase_links,
    system_requirements: g.system_requirements,
    ratings: g.metacritic_score ? [{ source: 'metacritic', score: g.metacritic_score, max_score: 100 }] : [],
    created_at: g.created_at,
    updated_at: g.updated_at,
  };
}
