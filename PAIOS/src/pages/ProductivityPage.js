import { useEffect, useState } from 'react';
import axios from 'axios';
import './Page.css';

function ProductivityPage() {
  const [section, setSection] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get('/api/home')
      .then((response) => {
        setSection(response.data?.sections?.productivity || null);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="page-container">Loading productivity brief...</div>;
  if (error) return <div className="page-container">Error: {error}</div>;

  const items = section?.items || [
    'High-value deep work',
    'Important meetings',
    'Deadline protection',
  ];
  const summary = section?.summary || 'Use the dashboard to see priorities, focus blocks and the best next actions.';

  return (
    <div className="page-container">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Productivity OS</p>
          <h1>Your day, structured</h1>
          <p className="hero-copy">{summary}</p>
        </div>
        <div className="hero-stats">
          <div className="hero-pill">
            <strong>Ready</strong>
            <p>Calendar & tasks</p>
          </div>
        </div>
      </section>

      <div className="cards-grid home-grid">
        <div className="card card--accent">
          <h3>Today’s focus</h3>
          <ul>
            {items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3>Suggested actions</h3>
          <ul>
            <li>Prepare for meetings in advance</li>
            <li>Block uninterrupted focus slots</li>
            <li>Review deadlines before noon</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ProductivityPage;
