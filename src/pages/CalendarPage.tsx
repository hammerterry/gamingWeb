import { useState, useMemo, useEffect } from 'react';
import { Link } from 'react-router-dom';
import type { Game } from '../types/game';
import { fetchGames } from '../api/games';

export default function CalendarPage() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);

  // 從 API 載入遊戲資料
  useEffect(() => {
    const loadGames = async () => {
      try {
        setLoading(true);
        const data = await fetchGames({ limit: 500 });
        setGames(data.games);
      } catch (error) {
        console.error('Failed to load games:', error);
      } finally {
        setLoading(false);
      }
    };
    loadGames();
  }, []);

  const calendarData = useMemo(() => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const firstDayOfWeek = firstDay.getDay(); // 0 = Sunday
    
    const days: Array<{ date: Date; games: Game[] }> = [];
    
    for (let i = 0; i < firstDayOfWeek; i++) {
      days.push({ date: new Date(year, month, -firstDayOfWeek + i + 1), games: [] });
    }
    
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day);
      const dayGames = games.filter(game => {
        if (!game.release_date) return false;
        const gameDate = new Date(game.release_date);
        return gameDate.getFullYear() === year &&
               gameDate.getMonth() === month &&
               gameDate.getDate() === day;
      });
      days.push({ date, games: dayGames });
    }
    
    const remainingDays = 7 - (days.length % 7);
    if (remainingDays < 7) {
      for (let i = 1; i <= remainingDays; i++) {
        days.push({ date: new Date(year, month + 1, i), games: [] });
      }
    }
    
    return days;
  }, [currentDate, games]);

  const monthNames = ['一月', '二月', '三月', '四月', '五月', '六月', 
                      '七月', '八月', '九月', '十月', '十一月', '十二月'];
  const weekDays = ['日', '一', '二', '三', '四', '五', '六'];

  const goToPrevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const isToday = (date: Date) => {
    const today = new Date();
    return date.getDate() === today.getDate() &&
           date.getMonth() === today.getMonth() &&
           date.getFullYear() === today.getFullYear();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">載入中...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <Link to="/" className="text-blue-400 hover:text-blue-300 mb-4 inline-block">
            ← 返回首頁
          </Link>
          <h1 className="text-3xl font-bold">發售日曆</h1>
          <p className="text-gray-400 mt-2">共 {games.length} 款遊戲</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Month Navigation */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={goToPrevMonth}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
          >
            ← 上個月
          </button>
          <h2 className="text-2xl font-bold">
            {currentDate.getFullYear()} 年 {monthNames[currentDate.getMonth()]}
          </h2>
          <button
            onClick={goToNextMonth}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
          >
            下個月 →
          </button>
        </div>

        {/* Calendar Grid */}
        <div className="bg-gray-800 rounded-lg overflow-hidden">
          {/* Weekday Headers */}
          <div className="grid grid-cols-7 bg-gray-700">
            {weekDays.map(day => (
              <div key={day} className="p-3 text-center font-semibold text-gray-300">
                {day}
              </div>
            ))}
          </div>

          {/* Calendar Days */}
          <div className="grid grid-cols-7">
            {calendarData.map((day, index) => {
              const isCurrentMonth = day.date.getMonth() === currentDate.getMonth();
              const hasGames = day.games.length > 0;
              
              return (
                <div
                  key={index}
                  className={`min-h-[100px] p-2 border-t border-r border-gray-700 ${
                    !isCurrentMonth ? 'bg-gray-850 opacity-50' : 'bg-gray-800'
                  } ${isToday(day.date) ? 'ring-2 ring-blue-500' : ''}`}
                >
                  <div className={`text-sm font-semibold mb-1 ${
                    isToday(day.date) ? 'text-blue-400' : 'text-gray-300'
                  }`}>
                    {day.date.getDate()}
                  </div>
                  
                  {hasGames && (
                    <div className="space-y-1">
                      {day.games.map(game => (
                        <Link
                          key={game.id}
                          to={`/game/${game.id}`}
                          className="block text-xs bg-blue-600 hover:bg-blue-500 rounded px-1 py-0.5 truncate transition-colors"
                          title={game.title}
                        >
                          {game.title}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Legend */}
        <div className="mt-6 flex items-center gap-4 text-sm text-gray-400">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-600 rounded"></div>
            <span>遊戲發售日</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 ring-2 ring-blue-500 rounded"></div>
            <span>今天</span>
          </div>
        </div>
      </main>
    </div>
  );
}
