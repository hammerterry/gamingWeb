import { useState, useMemo } from 'react';
import gamesData from '../data/games.json';
import type { Game, Platform } from '../types/game';
import GameCard from '../components/GameCard';

export default function HomePage() {
  const [selectedPlatform, setSelectedPlatform] = useState<Platform | 'all'>('all');
  const [sortBy, setSortBy] = useState<'release_date' | 'rating'>('release_date');
  const [searchQuery, setSearchQuery] = useState('');

  const platforms: Platform[] = ['PC', 'PS5', 'PS4', 'Xbox Series X', 'Xbox One', 'Nintendo Switch'];

  const filteredAndSortedGames = useMemo(() => {
    let filtered = gamesData as Game[];

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(game => 
        game.title.toLowerCase().includes(query) ||
        game.developer.toLowerCase().includes(query) ||
        game.genres.some(g => g.toLowerCase().includes(query))
      );
    }

    // Filter by platform
    if (selectedPlatform !== 'all') {
      filtered = filtered.filter(game => game.platforms.includes(selectedPlatform));
    }

    // Sort
    const sorted = [...filtered].sort((a, b) => {
      if (sortBy === 'release_date') {
        return new Date(a.release_date).getTime() - new Date(b.release_date).getTime();
      } else {
        const aScore = a.ratings.find(r => r.source === 'metacritic')?.score || 0;
        const bScore = b.ratings.find(r => r.source === 'metacritic')?.score || 0;
        return bScore - aScore;
      }
    });

    return sorted;
  }, [selectedPlatform, sortBy, searchQuery]);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold mb-6">GamingWeb</h1>
          
          {/* Search */}
          <div className="mb-4">
            <input
              type="text"
              placeholder="搜尋遊戲名稱、開發商或類型..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full md:w-96 px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          {/* Filters */}
          <div className="flex flex-wrap gap-4 items-center">
            {/* Platform Filter */}
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setSelectedPlatform('all')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  selectedPlatform === 'all'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                全部平台
              </button>
              {platforms.map(platform => (
                <button
                  key={platform}
                  onClick={() => setSelectedPlatform(platform)}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    selectedPlatform === platform
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  {platform}
                </button>
              ))}
            </div>

            {/* Sort */}
            <div className="ml-auto">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'release_date' | 'rating')}
                className="bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="release_date">依發售日期排序</option>
                <option value="rating">依評分排序</option>
              </select>
            </div>
          </div>
        </div>
      </header>

      {/* Games Grid */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-4 text-gray-400">
          顯示 {filteredAndSortedGames.length} 款遊戲
        </div>
        
        {filteredAndSortedGames.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-xl text-gray-400">沒有找到符合條件的遊戲</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
            {filteredAndSortedGames.map(game => (
              <GameCard key={game.id} game={game} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
