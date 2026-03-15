// ---------- tiny spa router ----------
const main = document.getElementById('spa-root');

const skillDetails = {
  "LangGraph": "Building multi-agent systems and stateful applications using LangGraph and LangChain workflows.",
  "Agentic AI": "Designing and deploying autonomous AI agents that can plan, execute, and iterate on tasks.",
  "LLMs": "Leveraging Large Language Models (OpenAI, Gemini) for natural language understanding and generation.",
  "LangChain": "Building context-aware applications by chaining LLM calls and integrating external tools.",
  "RAG": "Implementing Retrieval-Augmented Generation to ground LLM responses in custom enterprise data.",
  "Prompt Engineering": "Crafting and optimizing prompts to guide model behavior and ensure output quality.",
  "Python": "Extensive experience (3+ years) in Python for data analysis, backend development, and automation.",
  "SQL": "Proficient in writing complex SQL queries for data extraction, manipulation, and analytics.",
  "Java": "Familiarity with core Java concepts and basic object-oriented application development.",
  "C++": "Knowledge of fundamental C++ arrays, structures, and basic algorithms.",
  "Elasticsearch": "Designing schemas and utilizing Elasticsearch for distributed search and analytics of large datasets.",
  "Kibana": "Creating intuitive executive visualizations and dashboards to monitor metrics.",
  "Logstash": "Configuring Logstash pipelines for data ingestion and integration into Elasticsearch.",
  "ETL Pipelines": "Designing and maintaining Extract, Transform, Load (ETL) pipelines to reduce manual processing.",
  "Data Modeling": "Structuring schemas for operational databases to ensure robust efficiency.",
  "Real-Time Streaming": "Handling streaming data in real-time for live dashboards and immediate actionable insights.",
  "Docker": "Containerizing applications using Docker and docker-compose for production-ready deployments.",
  "Kubernetes": "Orchestrating containerized services and demonstrating orchestration skills.",
  "Azure": "Deploying and managing cloud services and infrastructure on Microsoft Azure.",
  "AWS": "Utilizing AWS services for versatile scalable cloud computing solutions.",
  "CI/CD": "Familiar with continuous integration and continuous deployment pipeline concepts.",
  "SAP HANA": "Working with SAP HANA in-memory database for high-performance analytics.",
  "Oracle": "Working with Oracle databases and enterprise data management.",
  "MySQL Workbench": "Managing MySQL databases, schema design, and query optimization.",
  "ServiceNow": "Managing ITSM workflows, incident tracking, and resolution tracking within ServiceNow (SNOW).",
  "SAP": "Experience with SAP systems and modules for enterprise resource planning.",
  "SAP T-Codes": "Familiarity with SAP Transaction Codes for navigating and executing system functions.",
  "Git/GitHub": "Using Git version control systems to collaborate efficiently in team environments and manage source code.",
  "Agile/Scrum": "Participating in agile sprints to deliver executive-ready data visualizations incrementally."
};

document.addEventListener('click', e => {
  // 1. Skill Modal Open
  if (e.target.closest('.skill-interactive')) {
    const skillName = e.target.closest('.skill-interactive').getAttribute('data-skill');
    const modal = document.getElementById('skillModal');

    if (skillDetails[skillName]) {
      document.getElementById('modalTitle').textContent = skillName;
      document.getElementById('modalDesc').textContent = skillDetails[skillName];
      modal.classList.add('active');
    }
  }

  // 2. Skill Modal Close
  if (e.target.closest('#closeModal') || e.target.classList.contains('modal-overlay')) {
    document.getElementById('skillModal').classList.remove('active');
  }

  // Toggle Interactive Cards
  if (e.target.closest('.interactive-card')) {
    const card = e.target.closest('.interactive-card');
    // If clicking inside the content (e.g. a link), don't toggle if we strictly want that.
    // But here we want the whole card to toggle.

    // Close others (optional - straightforward is to just toggle current)
    // Remove 'active' from siblings? Let's keep it simple: toggle current.

    card.classList.toggle('active');

    const btn = card.querySelector('.toggle-btn');
    if (btn) {
      if (card.classList.contains('active')) {
        btn.innerHTML = '<i class="fa-solid fa-chevron-down"></i> Hide Details';
      } else {
        btn.innerHTML = '<i class="fa-solid fa-chevron-down"></i> Show Details';
      }
    }
  }

  // SPA Navigation
  const link = e.target.closest('a[data-link]');
  if (!link) return;
  e.preventDefault();
  navigate(link.href);
});

async function navigate(url) {
  main.classList.add('spa-out');
  await delay(300);
  const html = await (await fetch(url)).text();
  const newMain = new DOMParser().parseFromString(html, 'text/html').querySelector('#spa-root').innerHTML;
  main.innerHTML = newMain;
  main.classList.remove('spa-out');
  main.classList.add('spa-in');
  window.history.pushState(null, null, url);
  document.title = new DOMParser().parseFromString(html, 'text/html').title;
}
window.addEventListener('popstate', () => navigate(location.pathname));

function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

// ---------- dark-mode toggle ----------
const html = document.documentElement;
const toggle = document.createElement('i');
toggle.className = 'fa-solid fa-circle-half-stroke theme-toggle';
toggle.style.marginLeft = '1rem'; toggle.style.cursor = 'pointer';
document.querySelector('.navbar').appendChild(toggle);

toggle.addEventListener('click', () => {
  const current = html.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});
(function () {
  const saved = localStorage.getItem('theme');
  if (saved) html.setAttribute('data-theme', saved);
})();

// ---------- mobile nav ----------
const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => navLinks.classList.toggle('active'));

/*  NEW  */
document.querySelectorAll('.nav-links a[data-link]').forEach(a =>
  a.addEventListener('click', () => navLinks.classList.remove('active'))
);

// ----- footer year -----
document.getElementById('year').textContent = new Date().getFullYear();

