import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Page.css';

function HomePage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboard = () => {
    setLoading(true);
    axios
      .get('/api/home')
      .then((response) => {
        setData(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadDashboard();
    const timer = setInterval(loadDashboard, 300000);
    return () => clearInterval(timer);
  }, []);

  if (loading) {
    return <div className="page-container">Loading your executive briefing...</div>;
  }

  if (error) {
    return <div className="page-container">Error: {error}</div>;
  }

  const { header, summary, sections, notifications, system_insights, project_insights } = data;

  return (
    <div className="page-container">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">{header.greeting}, {header.user}</p>
          <h1>Personal AI command center</h1>
          <p className="hero-copy">
            Your laptop wakes up, tracks the market, monitors the news and keeps the next most important actions in sight.
          </p>
          <div className="action-row">
            <span className="action-pill action-pill--primary">Market {header.market_sentiment}</span>
            <span className="action-pill action-pill--secondary">AI {header.ai_sentiment}</span>
            <span className="action-pill">Refresh every 3-5 min</span>
          </div>
        </div>
        <div className="hero-stats">
          <div className="hero-pill">
            <strong>{header.date}</strong>
            <p>{header.time}</p>
          </div>
          <div className="hero-pill">
            <strong>{header.location}</strong>
            <p>{header.weather}</p>
          </div>
        </div>
      </section>

      <div className="cards-grid home-grid">
        <div className="card card--accent">
          <h3>Today’s summary</h3>
          <ul>
            {summary.today.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3>Priority actions</h3>
          <ul>
            {data.focus.priority_actions.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3>Live signals</h3>
          <ul>
            {data.focus.live_signals.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="cards-grid home-grid">
        <div className="card">
          <h3>Critical alerts</h3>
          <ul>
            {notifications.critical.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3>System health</h3>
          <p>CPU: {system_insights.cpu_percent}%</p>
          <p>Memory: {system_insights.memory_percent}%</p>
          <p>Disk: {system_insights.disk_percent}%</p>
          <p>Platform: {system_insights.platform}</p>
        </div>
        <div className="card">
          <h3>Workspace pulse</h3>
          <p>{project_insights.git_changes.length} local changes</p>
          <p>{project_insights.recent_files.length} recent files</p>
          <p>{notifications.informational[1]}</p>
        </div>
      </div>

      <section className="insight-row">
        <div className="card">
          <h3>Market sentiment</h3>
          <p className="metric-value">{header.market_sentiment}</p>
        </div>
        <div className="card">
          <h3>AI industry sentiment</h3>
          <p className="metric-value">{header.ai_sentiment}</p>
        </div>
        <div className="card">
          <h3>Workspace status</h3>
          <p>{project_insights.git_changes.length} pending changes</p>
          <p>{project_insights.recent_files.length} recent files</p>
        </div>
      </section>

      <div className="section-grid">
        {Object.entries(sections).map(([key, section]) => (
          <div className="card section-card" key={key}>
            <div className="section-card__header">
              <h3>{section.title}</h3>
              <span className="badge">{section.priority}</span>
            </div>
            <p>{section.summary}</p>
            <ul>
              {section.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
            <Link className="action-pill action-pill--primary" to={`/news/${key}`}>
              Open details
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
