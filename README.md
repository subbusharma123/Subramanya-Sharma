# Subramanya Sharma Portfolio + AI Agent

This repository supports two deployment modes:

1. Native single-URL mode (recommended): Flask portfolio + built-in AI API and widget
2. Dual-service mode: Flask portfolio + external Streamlit AI service embedded via iframe

## Architecture

User opens portfolio website (Flask)
-> clicks floating AI chat button
-> native widget calls /api/ai-chat
-> agent routes requests to:

- Local portfolio retriever (TXT/PDF/DOCX/CSV under static)
- Live web search tool (Google Programmable Search)
- Gemini model for reasoning and response generation

## Important Files

- app.py: Flask app, AI API endpoint, and chat config injection
- ai_agent_app.py: Optional external Streamlit AI agent (dual-service mode)
- static/portfolio_info.txt: structured profile knowledge base
- static/project_data.csv: structured project metrics
- templates/base.html: floating chat widget markup
- static/css/gallery.css: chat widget styling
- render.yaml: Render Blueprint for both web services

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables.

Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY="your_gemini_api_key"
$env:GOOGLE_CSE_ID="your_google_cse_id"
$env:USE_NATIVE_AI_CHAT="1"
```

4. Run Flask portfolio:

```bash
python app.py
```

Portfolio URL (with native chat): http://127.0.0.1:5000

Optional external mode:

```powershell
$env:AI_CHAT_URL="http://localhost:8501"
$env:USE_NATIVE_AI_CHAT="0"
streamlit run ai_agent_app.py
```

## Render Hosting (Free Tier)

For same URL hosting, deploy only the Flask service. The AI runs inside Flask at /api/ai-chat.

### Option 1: Single Service (same URL, lowest cost)

Create one Render Web Service:

- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Environment Variables:
   - GOOGLE_API_KEY=your_gemini_api_key
   - GOOGLE_CSE_ID=your_google_cse_id (optional but required for live web news)
   - USE_NATIVE_AI_CHAT=1

### Option 2: Blueprint Deploy (dual service)

1. Push this repository to GitHub.
2. In Render, click New + -> Blueprint.
3. Select this repository.
4. Render reads render.yaml and creates both services:
   - subramanya-portfolio-web
   - subramanya-portfolio-ai-agent
5. After first deploy, open the AI service URL and copy it.
6. In portfolio service environment variables, set:
   - AI_CHAT_URL = https://<your-ai-service>.onrender.com
7. In AI service environment variables, set:
   - GOOGLE_API_KEY = your Gemini API key
   - GOOGLE_CSE_ID = your Google Programmable Search Engine ID
8. Redeploy portfolio service after setting AI_CHAT_URL.

### Option 2: Manual Two-Service Setup

Create two Render Web Services from the same repo:

Service A (Portfolio):
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Env Var: AI_CHAT_URL=https://<agent-service-url>.onrender.com

Service B (AI Agent):
- Build Command: pip install -r requirements.txt
- Start Command: streamlit run ai_agent_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
- Env Vars:
  - GOOGLE_API_KEY=...
  - GOOGLE_CSE_ID=...

## Google Programmable Search Setup

1. Create a search engine at https://programmablesearchengine.google.com/
2. Configure it to search the entire web.
3. Copy the Search Engine ID to GOOGLE_CSE_ID.
4. Ensure your API key can access Custom Search API.

## Notes

- In native mode, everything runs on the same URL and chat calls /api/ai-chat.
- If GOOGLE_CSE_ID is missing, the assistant still works for portfolio and general questions but web search tool replies with a setup hint.
- In external mode, set AI_CHAT_URL and optionally disable native mode with USE_NATIVE_AI_CHAT=0.
