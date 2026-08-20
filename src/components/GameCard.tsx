import { Link } from 'react-router-dom';
import type { Game } from '../types/game';

interface GameCardProps {
  game: Game;
}

export default function GameCard({ game }: GameCardProps) {
  const releaseDate = new Date(game.release_date).toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });

  const metacriticScore = game.ratings.find(r => r.source === 'metacritic')?.score;

  return (
    <Link to={`/game/${game.id}`} className="block group">
      <div className="bg-gray-800 rounded-lg overflow-hidden transition-transform hover:scale-105">
        <div className="relative aspect-[2/3] overflow-hidden">
          <img 
            src={game.cover_url} 
            alt={game.title}
            className="w-full h-full object-cover"
          />
          {metacriticScore && (
            <div className={`absolute top-2 right-2 px-2 py-1 rounded font-bold text-sm ${
              metacriticScore >= 80 ? 'bg-green-600' :
              metacriticScore >= 60 ? 'bg-yellow-600' :
              'bg-red-600'
            }`}>
              {metacriticScore}
            </div>
          )}
        </div>
        
        <div className="p-3">
          <h3 className="font-bold text-sm mb-1 line-clamp-2 group-hover:text-blue-400">
            {game.title}
          </h3>
          
          <p className="text-xs text-gray-400 mb-2">{releaseDate}</p>
          
          <div className="flex flex-wrap gap-1">
            {game.platforms.slice(0, 3).map(platform => (
              <span 
                key={platform}
                className="text-xs bg-gray-700 px-2 py-0.5 rounded"
              >
                {platform}
              </span>
            ))}
            {game.platforms.length > 3 && (
              <span className="text-xs text-gray-400">+{game.platforms.length - 3}</span>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}
