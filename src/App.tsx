import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import GameDetailPage from './pages/GameDetailPage';

function App() {
  return (
    <BrowserRouter basename="/games">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/game/:id" element={<GameDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
