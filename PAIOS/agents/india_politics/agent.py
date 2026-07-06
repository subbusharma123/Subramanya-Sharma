"""
India Politics Agent — Fetches Indian political and economic news.
"""
import httpx
from typing import Any, Dict
from loguru import logger
from langchain_core.messages import HumanMessage

from agents.base import BaseAgent
from core.config import settings

try:
    import feedparser
except ImportError:  # pragma: no cover - optional dependency
    feedparser = None

INDIA_NEWS_FEEDS = [
    "https://feeds.feedburner.com/ndtvnews-india-news",
    "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://economictimes.indiatimes.com/nation/rssfeeds/1081479906.cms",
    "https://www.livemint.com/rss/politics",
]

INDIA_KEYWORDS = [
    "parliament", "lok sabha", "rajya sabha", "modi", "cabinet",
    "rbi", "budget", "tax", "gst", "policy", "defense", "military",
    "election", "bjp", "congress", "infrastructure", "gdp", "inflation",
    "rupee", "trade", "agreement", "diplomacy", "supreme court"
]


class IndiaPoliticsAgent(BaseAgent):
    name = "india_politics"
    refresh_interval = 3600

    async def fetch_data(self) -> Dict[str, Any]:
        entries = []
        if feedparser is None:
            logger.warning("[india_politics] feedparser is not installed; RSS feed parsing is disabled.")
            return {"entries": []}

        async with httpx.AsyncClient(timeout=15.0) as client:
            for url in INDIA_NEWS_FEEDS:
                try:
                    resp = await client.get(url)
                    feed = feedparser.parse(resp.text)
                    for e in feed.entries[:10]:
                        title = e.get("title", "")
                        summary = e.get("summary", "")[:600]
                        if any(kw in title.lower() or kw in summary.lower()
                               for kw in INDIA_KEYWORDS):
                            entries.append({
                                "title": title,
                                "summary": summary,
                                "link": e.get("link", ""),
                                "published": e.get("published", ""),
                            })
                except Exception as ex:
                    logger.warning(f"[india_politics] Feed {url}: {ex}")

        # Also use NewsAPI if key is available
        if settings.NEWS_API_KEY:
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.get(
                        "https://newsapi.org/v2/top-headlines",
                        params={
                            "country": "in",
                            "category": "politics",
                            "pageSize": 20,
                            "apiKey": settings.NEWS_API_KEY,
                        }
                    )
                    if resp.status_code == 200:
                        for a in resp.json().get("articles", []):
                            entries.append({
                                "title": a.get("title", ""),
                                "summary": a.get("description", ""),
                                "link": a.get("url", ""),
                                "published": a.get("publishedAt", ""),
                            })
            except Exception as e:
                logger.warning(f"[india_politics] NewsAPI: {e}")

        return {"entries": entries[:25]}

    async def analyze(self, data: Dict[str, Any]) -> str:
        entries = data.get("entries", [])
        if not entries:
            return "India political news temporarily unavailable."

        news_text = "\n".join([
            f"- {e['title']}: {e['summary'][:200]}"
            for e in entries[:20]
        ])

        llm = self.llm.get("primary")
        msg = HumanMessage(content=f"""
You are a senior Indian political analyst. Based on the news below, provide:

Top 10 India Political/Economic Developments Today:
For each item include:
- Headline
- 2-sentence summary
- Impact Level (Low/Medium/High)
- Economic Impact
- Investment Impact

News:
{news_text}

Format clearly with numbering.
""")
        result = await llm.ainvoke([msg])
        return result.content
