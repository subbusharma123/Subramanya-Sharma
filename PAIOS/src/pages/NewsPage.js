import { useEffect, useMemo, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './Page.css';

function NewsPage() {
  const { category } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    axios
      .get('/api/news')
      .then((response) => {
        setData(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const categoryData = useMemo(() => {
    if (!data || !category) {
      return null;
    }

    return data[category] || null;
  }, [category, data]);

  if (loading) {
    return <div className="page-container">Loading the latest intelligence...</div>;
  }

  if (error) {
    return <div className="page-container">Error: {error}</div>;
  }

  if (!categoryData) {
    return (
      <div className="page-container">
        <p>No intelligence found for this category.</p>
        <Link to="/" className="action-pill action-pill--primary">Back to home</Link>
      </div>
    );
  }

  return (
    <div className="page-container">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">News detail</p>
          <h1>{categoryData.title}</h1>
          <p className="hero-copy">{categoryData.summary}</p>
        </div>
        <Link to="/" className="action-pill action-pill--primary">Back to briefing</Link>
      </section>

      <div className="section-grid">
        {categoryData.details.map((detail, index) => (
          <div className="card section-card" key={`${detail.headline}-${index}`}>
            <div className="section-card__header">
              <h3>{detail.headline}</h3>
              <span className="badge">{detail.impact}</span>
            </div>
            <p>{detail.body}</p>
            <p className="muted-text">Source: {detail.source}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default NewsPage;
