import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ProjectsPage from './pages/ProjectsPage';
import ResearchPage from './pages/ResearchPage';
import ProductivityPage from './pages/ProductivityPage';
import PortfolioPage from './pages/PortfolioPage';
import SystemPage from './pages/SystemPage';
import NewsPage from './pages/NewsPage';
import './App.css';

const navItems = [
  { to: '/', label: 'Home', end: true },
  { to: '/projects', label: 'Projects' },
  { to: '/research', label: 'Research' },
  { to: '/productivity', label: 'Productivity' },
  { to: '/portfolio', label: 'Portfolio' },
  { to: '/system', label: 'System' },
];

const themeOptions = [
  { value: 'midnight', label: 'Midnight' },
  { value: 'aurora', label: 'Aurora' },
  { value: 'sunset', label: 'Sunset' },
  { value: 'forest', label: 'Forest' },
];

function App() {
  const [theme, setTheme] = useState(() => {
    if (typeof window === 'undefined') {
      return 'midnight';
    }
    return window.localStorage.getItem('paios-theme') || 'midnight';
  });

  useEffect(() => {
    window.localStorage.setItem('paios-theme', theme);
  }, [theme]);

  return (
    <Router>
      <div className={`app-shell theme-${theme}`}>
        <aside className="sidebar">
          <div className="sidebar__brand">PAIOS Command Center</div>
          <label className="theme-picker" htmlFor="theme-select">
            <span>Theme</span>
            <select id="theme-select" value={theme} onChange={(event) => setTheme(event.target.value)}>
              {themeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <nav className="sidebar__nav">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  isActive ? 'sidebar__link active' : 'sidebar__link'
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </aside>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/research" element={<ResearchPage />} />
            <Route path="/productivity" element={<ProductivityPage />} />
            <Route path="/portfolio" element={<PortfolioPage />} />
            <Route path="/system" element={<SystemPage />} />
            <Route path="/news/:category" element={<NewsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
