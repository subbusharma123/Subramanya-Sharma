"""
Research Agent — ArXiv papers, HuggingFace papers, tech blogs
"""
import httpx
from typing import Any, Dict
from loguru import logger
from langchain_core.messages import HumanMessage

from agents.base import BaseAgent

try:
    import feedparser
except ImportError:  # pragma: no cover - optional dependency
    feedparser = None

RESEARCH_FEEDS = {
    "ArXiv AI":     "https://arxiv.org/rss/cs.AI",
    "ArXiv ML":     "https://arxiv.org/rss/cs.LG",
    "ArXiv CL":     "https://arxiv.org/rss/cs.CL",
    "ArXiv CV":     "https://arxiv.org/rss/cs.CV",
    "ArXiv RO":     "https://arxiv.org/rss/cs.RO",
    "HF Papers":    "https://huggingface.co/blog/feed.xml",
    "Towards DS":   "https://towardsdatascience.com/feed",
    "Sebastian R":  "https://magazine.sebastianraschka.com/feed",
}


class ResearchAgent(BaseAgent):
    name = "research"
    refresh_interval = 3600

    async def fetch_data(self) -> Dict[str, Any]:
        papers = []
        if feedparser is None:
            logger.warning("[research] feedparser is not installed; RSS feed parsing is disabled.")
            return {"papers": []}

        async with httpx.AsyncClient(timeout=15.0) as client:
            for source, url in RESEARCH_FEEDS.items():
                try:
                    resp = await client.get(url)
                    feed = feedparser.parse(resp.text)
                    for e in feed.entries[:5]:
                        papers.append({
                            "source": source,
                            "title": e.get("title", "").strip(),
                            "summary": e.get("summary", "")[:600].strip(),
                            "link": e.get("link", ""),
                        })
                except Exception as ex:
                    logger.warning(f"[research] {source}: {ex}")

        return {"papers": papers[:30]}

    async def analyze(self, data: Dict[str, Any]) -> str:
        papers = data.get("papers", [])
        if not papers:
            return "Research digest unavailable."

        paper_text = "\n".join([
            f"[{p['source']}] {p['title']}: {p['summary'][:200]}"
            for p in papers[:20]
        ])

        llm = self.llm.get("primary")
        msg = HumanMessage(content=f"""
You are an AI research analyst. Create a 5-minute research digest from these recent papers and posts.

Include:
1. 🔥 Top 3 most important papers/findings
2. 📊 Key trends observed
3. 🛠️ Practical applications
4. 🌟 Open-source highlights

Papers:
{paper_text}

Keep it digestible and practical. Under 300 words.
""")
        result = await llm.ainvoke([msg])
        return result.content
