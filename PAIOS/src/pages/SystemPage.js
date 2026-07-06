import { useEffect, useState } from 'react';
import axios from 'axios';
import './Page.css';

function SystemPage() {
  const [system, setSystem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    axios
      .get('/api/system')
      .then((response) => {
        setSystem(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="page-container">Loading system status...</div>;
  }

  if (error) {
    return <div className="page-container">Error: {error}</div>;
  }

  return (
    <div className="page-container">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">System control center</p>
          <h1>Laptop health at a glance</h1>
          <p className="hero-copy">See the machine state, performance load and any maintenance actions that matter today.</p>
        </div>
        <div className="hero-stats">
          <div className="hero-pill">
            <strong>{system.cpu_percent}%</strong>
            <p>CPU load</p>
          </div>
        </div>
      </section>

      <div className="cards-grid home-grid">
        <div className="card card--accent">
          <h3>CPU</h3>
          <p className="metric-value">{system.cpu_percent}%</p>
          <p>{system.platform}</p>
        </div>
        <div className="card">
          <h3>Memory</h3>
          <p className="metric-value">{system.memory_percent}%</p>
          <p>{system.memory_used}</p>
        </div>
        <div className="card">
          <h3>Disk</h3>
          <p className="metric-value">{system.disk_percent}%</p>
          <p>{system.disk_used}</p>
        </div>
      </div>

      <section className="card">
        <h3>Device details</h3>
        <div className="chip-list">
          <span className="chip">Hostname: {system.hostname}</span>
          <span className="chip">Platform: {system.platform}</span>
          <span className="chip">Boot time: {system.boot_time}</span>
        </div>
      </section>
    </div>
  );
}

export default SystemPage;
