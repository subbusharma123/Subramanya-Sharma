"""
Global Politics Agent — US, China, EU, Russia, Middle East, Indo-Pacific
"""
import httpx
from typing import Any, Dict
from loguru import logger
from langchain_core.messages import HumanMessage

from agents.base import BaseAgent
from core.config import settings

try:
    import feedparser
except ImportError:
    feedparser = None

GLOBAL_FEEDS = {
    "Reuters World":    "https://feeds.reuters.com/reuters/worldNews",
    "BBC World":        "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera":       "https://www.aljazeera.com/xml/rss/all.xml",
    "The Guardian Intl":"https://www.theguardian.com/world/rss",
    "Foreign Policy":   "https://foreignpolicy.com/feed/",
}

GLOBAL_KEYWORDS = [
    "war", "conflict", "sanctions", "trade", "tariff", "diplomacy",
    "election", "military", "nuclear", "china", "usa", "russia",
    "ukraine", "middle east", "nato", "un", "g7", "g20",
    "energy", "oil", "indo-pacific", "taiwan", "israel", "iran"
]


class GlobalPoliticsAgent(BaseAgent):
    name = "global_politics"
    refresh_interval = 3600

    async def fetch_data(self) -> Dict[str, Any]:
        entries = []
        if feedparser is None:
            logger.warning("[global_politics] feedparser is not installed; RSS feed parsing is disabled.")
            return {"entries": []}

        async with httpx.AsyncClient(timeout=15.0) as client:
            for source, url in GLOBAL_FEEDS.items():
                try:
                    resp = await client.get(url)
                    feed = feedparser.parse(resp.text)
                    for e in feed.entries[:8]:
                        title = e.get("title", "")
                        summary = e.get("summary", "")[:500]
                        if any(kw in title.lower() or kw in summary.lower()
                               for kw in GLOBAL_KEYWORDS):
                            entries.append({
                                "source": source,
                                "title": title,
                                "summary": summary,
                                "link": e.get("link", ""),
                            })
                except Exception as ex:
                    logger.warning(f"[global_politics] {source}: {ex}")

        return {"entries": entries[:30]}

    async def analyze(self, data: Dict[str, Any]) -> str:
        entries = data.get("entries", [])
        if not entries:
            return "Global news temporarily unavailable."

        news_text = "\n".join([
            f"- [{e['source']}] {e['title']}: {e['summary'][:200]}"
            for e in entries[:20]
        ])

        llm = self.llm.get("primary")
        msg = HumanMessage(content=f"""
You are a global geopolitical analyst. Based on the news below, provide:

Top 10 Global Political Events Today:
For each: Headline, Region, 2-sentence summary, India relevance (if any), Market impact.

Focus on: US, China, Russia, EU, Middle East, Indo-Pacific.

News:
{news_text}
""")
        result = await llm.ainvoke([msg])
        return result.content
