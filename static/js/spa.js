// ---------- tiny spa router ----------
const main = document.getElementById('spa-root');

// Projects reference with detailed descriptions
const projectsMap = {
  "AI-Powered Agents for AIOps": {
    description: "Six AI-powered agents for change risk assessment, SLA breach prediction, incident correlation, and intelligent ticket routing using LangGraph and LangChain. Reduced manual triage by 60%, shortened resolution time by 35%, and saved $150K+ annually.",
    skills: ["LangGraph", "Agentic AI", "LLMs", "LangChain", "Prompt Engineering", "Python", "Docker", "Kubernetes", "Azure", "AWS"]
  },
  "Analytical Dashboards & Executive Reporting": {
    description: "Built and maintained dashboards for POS, inventory, resiliency, and customer satisfaction using Elasticsearch, Kibana, and SQL. Eliminated 15+ hours per week of manual reporting and achieved 100% data consistency.",
    skills: ["Elasticsearch", "Kibana", "Logstash", "ETL Pipelines", "Data Modeling", "SQL", "Python", "Real-Time Streaming"]
  },
  "Service Management Enablement": {
    description: "Resolved 150+ ServiceNow incidents and RITM requests. Streamlined onboarding/offboarding workflows and reduced cycle time by 30% through process automation and improved escalation paths.",
    skills: ["ServiceNow", "Agile/Scrum", "Python", "Git/GitHub"]
  }
};

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

// Helper function to get projects using a specific skill
function getProjectsForSkill(skillName) {
  const projects = [];
  for (const [projectName, projectData] of Object.entries(projectsMap)) {
    if (projectData.skills.includes(skillName)) {
      projects.push({ name: projectName, description: projectData.description });
    }
  }
  return projects;
}

document.addEventListener('click', e => {
  // 1. Skill Modal Open
  if (e.target.closest('.skill-interactive')) {
    const skillName = e.target.closest('.skill-interactive').getAttribute('data-skill');
    const modal = document.getElementById('skillModal');

    if (skillDetails[skillName]) {
      document.getElementById('modalTitle').textContent = skillName;
      
      let modalHTML = '<p style="margin-bottom: 1rem;">' + skillDetails[skillName] + '</p>';
      
      const projects = getProjectsForSkill(skillName);
      if (projects.length > 0) {
        modalHTML += '<h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--gold);">Projects using this skill:</h4>';
        projects.forEach(project => {
          modalHTML += '<div style="background: var(--card-bg); padding: 0.8rem; border-radius: 0.5rem; margin-bottom: 0.8rem; border-left: 3px solid var(--gold);">';
          modalHTML += '<h5 style="margin: 0 0 0.5rem 0;">' + project.name + '</h5>';
          modalHTML += '<p style="margin: 0; font-size: 0.9rem; color: var(--fg-dim);">' + project.description + '</p>';
          modalHTML += '</div>';
        });
      } else {
        modalHTML += '<p style="margin-top: 1rem; font-size: 0.9rem; color: var(--fg-dim);">This skill is foundational and supports multiple projects.</p>';
      }
      
      document.getElementById('modalDesc').innerHTML = modalHTML;
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

// ----- Modal handling -----
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add('active');
}
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('active');
}

const contactBtn = document.getElementById('contact-float');
if (contactBtn) {
  contactBtn.addEventListener('click', () => openModal('contact-modal'));
}
const contactClose = document.getElementById('contact-close');
if (contactClose) {
  contactClose.addEventListener('click', () => closeModal('contact-modal'));
}

const resumeBtn = document.getElementById('resume-btn');
if (resumeBtn) {
  resumeBtn.addEventListener('click', () => openModal('resume-modal'));
}
const resumeClose = document.getElementById('resume-close');
if (resumeClose) {
  resumeClose.addEventListener('click', () => closeModal('resume-modal'));
}

const resumeViewBtn = document.getElementById('resume-view-btn');
const resumeDownloadBtn = document.getElementById('resume-download-btn');
const resumeViewPanel = document.getElementById('resume-view-panel');
const resumeDownloadPanel = document.getElementById('resume-download-panel');

function setResumeMode(mode) {
  if (!resumeViewBtn || !resumeDownloadBtn || !resumeViewPanel || !resumeDownloadPanel) return;
  const isView = mode === 'view';
  resumeViewBtn.classList.toggle('active', isView);
  resumeDownloadBtn.classList.toggle('active', !isView);
  resumeViewPanel.classList.toggle('active', isView);
  resumeDownloadPanel.classList.toggle('active', !isView);
}

if (resumeViewBtn) resumeViewBtn.addEventListener('click', () => setResumeMode('view'));
if (resumeDownloadBtn) resumeDownloadBtn.addEventListener('click', () => setResumeMode('download'));

function triggerResumeDownload() {
  const link = document.createElement('a');
  link.href = window.resumeUrl || '/static/docs/SubramanyaResume.pdf';
  link.download = window.resumeFilename || 'SubramanyaResume.pdf';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

const resumeDownloadDirect = document.getElementById('resume-download-direct');
if (resumeDownloadDirect) {
  resumeDownloadDirect.addEventListener('click', triggerResumeDownload);
}
const resumeDownload = document.getElementById('resume-download');
if (resumeDownload) {
  resumeDownload.addEventListener('click', triggerResumeDownload);
}

// Close modals when clicking overlay
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      overlay.classList.remove('active');
    }
  });
});


