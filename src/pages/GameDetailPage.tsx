import { useParams, Link } from 'react-router-dom';
import gamesData from '../data/games.json';
import type { Game } from '../types/game';
import { extractYouTubeId } from '../utils/youtube';

export default function GameDetailPage() {
  const { id } = useParams<{ id: string }>();
  const game = gamesData.find(g => g.id === id) as Game | undefined;

  if (!game) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">遊戲不存在</h1>
          <Link to="/" className="text-blue-400 hover:text-blue-300">
            返回首頁
          </Link>
        </div>
      </div>
    );
  }

  const releaseDate = new Date(game.release_date).toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  const metacriticScore = game.ratings.find(r => r.source === 'metacritic')?.score;
  const steamScore = game.ratings.find(r => r.source === 'steam');
  const opencriticScore = game.ratings.find(r => r.source === 'opencritic')?.score;

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gradient-to-b from-gray-800 to-gray-900 py-8">
        <div className="container mx-auto px-4">
          <Link to="/" className="text-blue-400 hover:text-blue-300 mb-4 inline-block">
            ← 返回首頁
          </Link>
          
          <div className="flex flex-col md:flex-row gap-8 mt-4">
            {/* Cover Image */}
            <div className="w-full md:w-1/3">
              <img 
                src={game.cover_url} 
                alt={game.title}
                className="w-full rounded-lg shadow-2xl"
              />
            </div>
            
            {/* Game Info */}
            <div className="w-full md:w-2/3">
              <h1 className="text-4xl font-bold mb-4">{game.title}</h1>
              
              <div className="space-y-2 mb-6">
                <p className="text-gray-300">
                  <span className="font-semibold">發售日期：</span> {releaseDate}
                </p>
                <p className="text-gray-300">
                  <span className="font-semibold">開發商：</span> {game.developer}
                </p>
                <p className="text-gray-300">
                  <span className="font-semibold">發行商：</span> {game.publisher}
                </p>
                <p className="text-gray-300">
                  <span className="font-semibold">類型：</span> {game.genres.join(', ')}
                </p>
                <div className="flex flex-wrap gap-2 mt-2">
                  {game.platforms.map(platform => (
                    <span 
                      key={platform}
                      className="bg-blue-600 px-3 py-1 rounded-full text-sm"
                    >
                      {platform}
                    </span>
                  ))}
                </div>
              </div>
              
              {/* Ratings */}
              <div className="grid grid-cols-3 gap-4 mb-6">
                {metacriticScore && (
                  <div className="bg-gray-800 p-4 rounded-lg text-center">
                    <div className="text-3xl font-bold text-green-400">{metacriticScore}</div>
                    <div className="text-sm text-gray-400">Metacritic</div>
                  </div>
                )}
                {steamScore && (
                  <div className="bg-gray-800 p-4 rounded-lg text-center">
                    <div className="text-3xl font-bold text-blue-400">{steamScore.score}%</div>
                    <div className="text-sm text-gray-400">Steam</div>
                    {steamScore.count && (
                      <div className="text-xs text-gray-500">{steamScore.count.toLocaleString()} 評價</div>
                    )}
                  </div>
                )}
                {opencriticScore && (
                  <div className="bg-gray-800 p-4 rounded-lg text-center">
                    <div className="text-3xl font-bold text-purple-400">{opencriticScore}</div>
                    <div className="text-sm text-gray-400">OpenCritic</div>
                  </div>
                )}
              </div>
              
              {/* Purchase Links */}
              {game.purchase_links && (
                <div className="flex flex-wrap gap-3">
                  {game.purchase_links.steam && (
                    <a 
                      href={game.purchase_links.steam}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg font-semibold transition-colors"
                    >
                      Steam
                    </a>
                  )}
                  {game.purchase_links.ps_store && (
                    <a 
                      href={game.purchase_links.ps_store}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-blue-800 hover:bg-blue-900 px-6 py-2 rounded-lg font-semibold transition-colors"
                    >
                      PlayStation Store
                    </a>
                  )}
                  {game.purchase_links.xbox_store && (
                    <a 
                      href={game.purchase_links.xbox_store}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded-lg font-semibold transition-colors"
                    >
                      Xbox Store
                    </a>
                  )}
                  {game.purchase_links.nintendo_eshop && (
                    <a 
                      href={game.purchase_links.nintendo_eshop}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-red-600 hover:bg-red-700 px-6 py-2 rounded-lg font-semibold transition-colors"
                    >
                      Nintendo eShop
                    </a>
                  )}
                  {game.purchase_links.amazon && (
                    <a 
                      href={game.purchase_links.amazon}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-yellow-600 hover:bg-yellow-700 px-6 py-2 rounded-lg font-semibold transition-colors"
                    >
                      Amazon
                    </a>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      
      {/* Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Description */}
        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">遊戲簡介</h2>
          <p className="text-gray-300 leading-relaxed">{game.description}</p>
        </section>
        
        {/* Screenshots */}
        {game.screenshots && game.screenshots.length > 0 && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">遊戲截圖</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {game.screenshots.map((screenshot, index) => (
                <img 
                  key={index}
                  src={screenshot}
                  alt={`${game.title} screenshot ${index + 1}`}
                  className="w-full rounded-lg"
                />
              ))}
            </div>
          </section>
        )}
        
        {/* Trailer */}
        {game.trailer_url && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">官方預告片</h2>
            <div className="aspect-video bg-gray-800 rounded-lg overflow-hidden">
              <iframe
                width="100%"
                height="100%"
                src={`https://www.youtube.com/embed/${extractYouTubeId(game.trailer_url)}`}
                title={`${game.title} trailer`}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          </section>
        )}
        
        {/* System Requirements */}
        {game.system_requirements && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">系統需求 (PC)</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-800 p-6 rounded-lg">
                <h3 className="text-xl font-bold mb-3 text-yellow-400">最低需求</h3>
                <p className="text-gray-300">{game.system_requirements.minimum}</p>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg">
                <h3 className="text-xl font-bold mb-3 text-green-400">建議需求</h3>
                <p className="text-gray-300">{game.system_requirements.recommended}</p>
              </div>
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
