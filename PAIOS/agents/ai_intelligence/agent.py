"""
AI Intelligence Agent
Tracks model releases, research papers, and AI industry news.
Sources: RSS feeds, Hugging Face, ArXiv, company blogs
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

AI_RSS_FEEDS = {
    "OpenAI Blog":       "https://openai.com/blog/rss.xml",
    "Anthropic News":    "https://www.anthropic.com/rss.xml",
    "DeepMind Blog":     "https://deepmind.google/blog/rss.xml",
    "Meta AI Blog":      "https://ai.meta.com/blog/rss/",
    "Mistral AI":        "https://mistral.ai/news/rss.xml",
    "HuggingFace Blog":  "https://huggingface.co/blog/feed.xml",
    "ArXiv AI":          "https://arxiv.org/rss/cs.AI",
    "ArXiv LG":          "https://arxiv.org/rss/cs.LG",
}

KEYWORDS = [
    "model release", "benchmark", "llm", "gpt", "claude", "gemini",
    "llama", "mistral", "open source", "multimodal", "agent", "reasoning",
    "robotics", "foundation model", "fine-tuning", "rlhf", "rag"
]


class AIIntelligenceAgent(BaseAgent):
    name = "ai_intelligence"
    refresh_interval = 900  # 15 min

    async def fetch_data(self) -> Dict[str, Any]:
        entries = []
        if feedparser is None:
            logger.warning("[ai_intelligence] feedparser is not installed; RSS feed parsing is disabled.")
            return {"entries": [], "total_fetched": 0}

        async with httpx.AsyncClient(timeout=15.0) as client:
            for source, url in AI_RSS_FEEDS.items():
                try:
                    response = await client.get(url)
                    feed = feedparser.parse(response.text)
                    for entry in feed.entries[:5]:
                        entries.append({
                            "source": source,
                            "title": entry.get("title", ""),
                            "summary": entry.get("summary", "")[:500],
                            "link": entry.get("link", ""),
                            "published": entry.get("published", ""),
                        })
                except Exception as e:
                    logger.warning(f"[ai_intelligence] Feed {source} failed: {e}")

        # Filter by keywords
        relevant = [
            e for e in entries
            if any(kw in e["title"].lower() or kw in e["summary"].lower()
                   for kw in KEYWORDS)
        ]
        return {"entries": relevant[:20], "total_fetched": len(entries)}

    def raw_summary(self, data: Dict[str, Any]) -> str:
        entries = data.get("entries", [])
        if not entries:
            return "No AI news fetched (check network)."
        lines = [f"📡 **{len(entries)} AI updates fetched** *(AI summary unavailable — install Ollama)*\n"]
        for e in entries[:10]:
            lines.append(f"- **[{e['source']}]** {e['title']}")
        return "\n".join(lines)

    async def analyze(self, data: Dict[str, Any]) -> str:
        if not data.get("entries"):
            return "No AI news available at this time."

        entries_text = "\n".join([
            f"- [{e['source']}] {e['title']}: {e['summary'][:200]}"
            for e in data["entries"][:15]
        ])

        llm = self.llm.get("fast")
        msg = HumanMessage(content=f"""
You are an AI industry analyst. Analyze these recent AI news items and provide:
1. Top 5 most important AI developments today
2. Any new model releases
3. Notable research breakthroughs
4. Overall AI industry sentiment (Quiet/Active/Highly Active)

News items:
{entries_text}

Format your response clearly with sections.
""")
        result = await llm.ainvoke([msg])
        return result.content
