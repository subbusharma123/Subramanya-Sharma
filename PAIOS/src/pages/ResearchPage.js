import { useEffect, useState } from 'react';
import axios from 'axios';
import './Page.css';

function ResearchPage() {
  const [section, setSection] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get('/api/home')
      .then((response) => {
        setSection(response.data?.sections?.research || null);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="page-container">Loading research digest...</div>;
  if (error) return <div className="page-container">Error: {error}</div>;

  const items = section?.items || [
    'Open-source model releases',
    'Reasoning and multimodal progress',
    'Benchmark changes and robotics updates',
  ];
  const summary = section?.summary || 'Stay ahead of model launches, benchmark gains, open-source breakthroughs and practical takeaways.';

  return (
    <div className="page-container">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Research radar</p>
          <h1>5-minute research digest</h1>
          <p className="hero-copy">{summary}</p>
        </div>
        <div className="hero-stats">
          <div className="hero-pill">
            <strong>Live</strong>
            <p>AI papers & reports</p>
          </div>
        </div>
      </section>

      <div className="cards-grid home-grid">
        <div className="card card--accent">
          <h3>Priority reads</h3>
          <ul>
            {items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3>Signal board</h3>
          <ul>
            <li>Track architecture shifts</li>
            <li>Spot high-impact releases</li>
            <li>Capture practical implications fast</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ResearchPage;
