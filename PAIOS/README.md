# 🧠 PAIOS — Personal AI Operating System

> Your personal AI-powered executive assistant that boots with your laptop, understands the world, understands the markets, and presents only the most important information in an actionable format.

---

## 🚀 Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install backend dependencies
pip install -r requirements.txt

# 3. Install frontend dependencies
npm install

# 4. Copy env template and fill in keys
copy .env.example .env

# 5. Initialize database
python scripts/init_db.py

# 6. Start all agents
python main.py

# 7. Start the backend API
python -m uvicorn core.api:app --reload --port 8000

# 8. Start the React dashboard
npm start
```

If you want to keep using Streamlit, the old dashboard is still available in `dashboard/app.py`, but the new React frontend is the recommended path.

---

## 📁 Project Structure

```
PAIOS/
├── agents/               # All AI agent modules
│   ├── ai_intelligence/  # AI & LLM tracking agent
│   ├── india_politics/   # India political news agent
│   ├── global_politics/  # Global political news agent
│   ├── financial/        # Financial markets agent
│   ├── portfolio/        # Personal portfolio agent
│   ├── ai_investment/    # AI sector investment agent
│   ├── research/         # Research paper aggregator
│   ├── productivity/     # Calendar & tasks agent
│   ├── email/            # Email intelligence agent
│   ├── web_monitor/      # Web keyword monitor agent
│   ├── system/           # Local system health agent
│   └── notification/     # Notification routing agent
├── dashboard/            # Streamlit dashboard
├── core/                 # Shared utilities & orchestration
├── config/               # Configuration files
├── scripts/              # Setup & maintenance scripts
├── data/                 # Local data cache
├── logs/                 # Log files
├── models/               # Local LLM config
└── docs/                 # Documentation
```

---

## 🤖 LLM Strategy

| Use Case | Model | Provider |
|---|---|---|
| Summarization, news digest | `llama3.2:3b` | Local (Ollama) |
| Deep analysis, investment | `llama3.1:8b` | Local (Ollama) |
| Complex reasoning | `deepseek-r1:8b` | Local (Ollama) |
| Fallback / best quality | `gpt-4o-mini` | OpenAI API |
| Embeddings | `nomic-embed-text` | Local (Ollama) |

---

## 📊 Dashboard Sections

1. **Header** — Date, weather, sentiment, day summary
2. **AI Intelligence** — Model releases, research papers
3. **India Politics** — Top 10 developments
4. **Global Politics** — Top 10 global events
5. **Markets** — Indian + US + Crypto + Forex
6. **Portfolio** — P&L, alerts, rebalancing
7. **AI Investment** — Sector opportunities
8. **Research** — 5-min digest
9. **Productivity** — Calendar, tasks
10. **System** — Health metrics

---

## ⚙️ Startup Automation

See `scripts/setup_startup.ps1` to register PAIOS as a Windows startup task.
