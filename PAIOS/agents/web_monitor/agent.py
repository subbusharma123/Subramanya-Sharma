"""
Web Monitor Agent — Tracks custom keywords, alerts on major news
"""
import httpx
from typing import Any, Dict, List
from loguru import logger
from langchain_core.messages import HumanMessage

from agents.base import BaseAgent
from core.config import settings

try:
    import feedparser
except ImportError:
    feedparser = None

WATCH_KEYWORDS = [
    "AI Agents", "LLM", "NVIDIA", "Semiconductor", "Kyndryl",
    "Elasticsearch", "Kubernetes", "OpenAI", "Gemini", "Claude",
    "Anthropic", "LangChain", "LangGraph", "CrewAI", "RAG"
]

TECH_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://venturebeat.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://news.ycombinator.com/rss",
]


class WebMonitorAgent(BaseAgent):
    name = "web_monitor"
    refresh_interval = 900

    async def fetch_data(self) -> Dict[str, Any]:
        alerts = []
        if feedparser is None:
            logger.warning("[web_monitor] feedparser is not installed; RSS feed parsing is disabled.")
            return {"alerts": [], "keywords_watched": WATCH_KEYWORDS}

        async with httpx.AsyncClient(timeout=15.0) as client:
            for url in TECH_FEEDS:
                try:
                    resp = await client.get(url)
                    feed = feedparser.parse(resp.text)
                    for e in feed.entries[:15]:
                        title = e.get("title", "")
                        summary = e.get("summary", "")[:400]
                        matched_kws = [
                            kw for kw in WATCH_KEYWORDS
                            if kw.lower() in title.lower() or kw.lower() in summary.lower()
                        ]
                        if matched_kws:
                            alerts.append({
                                "title": title,
                                "summary": summary,
                                "link": e.get("link", ""),
                                "matched_keywords": matched_kws,
                            })
                except Exception as ex:
                    logger.warning(f"[web_monitor] {url}: {ex}")

        # Deduplicate by title
        seen = set()
        unique = []
        for a in alerts:
            if a["title"] not in seen:
                seen.add(a["title"])
                unique.append(a)

        return {"alerts": unique[:20], "keywords_watched": WATCH_KEYWORDS}

    async def analyze(self, data: Dict[str, Any]) -> str:
        alerts = data.get("alerts", [])
        if not alerts:
            return f"No alerts for watched keywords: {', '.join(WATCH_KEYWORDS[:5])}..."

        alert_text = "\n".join([
            f"- {a['title']} [Keywords: {', '.join(a['matched_keywords'])}]"
            for a in alerts[:15]
        ])

        llm = self.llm.get("fast")
        msg = HumanMessage(content=f"""
Summarize these keyword alerts in a brief, actionable format.
Group by keyword/topic. Highlight any urgent news.

Alerts:
{alert_text}
""")
        result = await llm.ainvoke([msg])
        return result.content
