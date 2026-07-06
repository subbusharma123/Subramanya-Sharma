import { useEffect, useState } from 'react';
import axios from 'axios';
import './Page.css';

function ProjectsPage() {
  const [insights, setInsights] = useState({ git_changes: [], recent_files: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get('/api/projects')
      .then((response) => {
        setInsights(response.data || { git_changes: [], recent_files: [] });
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="page-container">Loading project insights...</div>;
  if (error) return <div className="page-container">Error: {error}</div>;

  const recentFiles = insights.recent_files || [];
  const pendingChanges = insights.git_changes || [];

  return (
    <div className="page-container">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Workspace intelligence</p>
          <h1>Projects & execution pulse</h1>
          <p className="hero-copy">Track what moved, what needs attention, and what deserves your focus next.</p>
        </div>
        <div className="hero-stats">
          <div className="hero-pill">
            <strong>{pendingChanges.length}</strong>
            <p>Pending changes</p>
          </div>
          <div className="hero-pill">
            <strong>{recentFiles.length}</strong>
            <p>Recent files</p>
          </div>
        </div>
      </section>

      <div className="cards-grid home-grid">
        <div className="card card--accent">
          <h3>Action queue</h3>
          <ul>
            {pendingChanges.length > 0 ? (
              <li>Review the pending git changes and commit the highest-value work.</li>
            ) : (
              <li>Your workspace looks clean. Start a focused coding session.</li>
            )}
            <li>Revisit the most recently touched files to keep momentum.</li>
          </ul>
        </div>
        <div className="card">
          <h3>Pending changes</h3>
          <ul>
            {pendingChanges.length > 0 ? (
              pendingChanges.slice(0, 6).map((change) => <li key={change}>{change}</li>)
            ) : (
              <li>No uncommitted git changes detected.</li>
            )}
          </ul>
        </div>
      </div>

      <section className="card">
        <h3>Recent files</h3>
        <div className="chip-list">
          {recentFiles.slice(0, 10).map((file) => (
            <span className="chip" key={file}>{file}</span>
          ))}
        </div>
      </section>
    </div>
  );
}

export default ProjectsPage;
