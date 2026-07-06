import { useEffect, useState } from 'react';
import axios from 'axios';
import './Page.css';

function PortfolioPage() {
  const [section, setSection] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get('/api/home')
      .then((response) => {
        setSection(response.data?.sections?.portfolio || null);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="page-container">Loading portfolio brief...</div>;
  if (error) return <div className="page-container">Error: {error}</div>;

  const items = section?.items || [
    'Daily P&amp;L view',
    'Diversification score',
    'Rebalancing alerts',
  ];
  const summary = section?.summary || 'Monitor performance, unusual movements and the next sensible action for your holdings.';

  return (
    <div className="page-container">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Portfolio intelligence</p>
          <h1>Risk, rebalancing and opportunity view</h1>
          <p className="hero-copy">{summary}</p>
        </div>
        <div className="hero-stats">
          <div className="hero-pill">
            <strong>Watchlist</strong>
            <p>Ready for holdings</p>
          </div>
        </div>
      </section>

      <div className="cards-grid home-grid">
        <div className="card card--accent">
          <h3>Portfolio posture</h3>
          <ul>
            {items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3>Suggested moves</h3>
          <ul>
            <li>Check sharp market moves</li>
            <li>Review over-concentrated sectors</li>
            <li>Protect risk if volatility rises</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default PortfolioPage;
