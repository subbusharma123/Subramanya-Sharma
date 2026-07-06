"""
Base Agent — All PAIOS agents inherit from this.
"""
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from loguru import logger
from core.llm import LLMRouter


@dataclass
class AgentResult:
    agent_name: str
    data: Dict[str, Any]
    summary: str
    timestamp: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None
    success: bool = True


class BaseAgent(ABC):
    name: str = "base"
    refresh_interval: int = 300  # seconds

    def __init__(self, llm: LLMRouter):
        self.llm = llm
        self._last_result: Optional[AgentResult] = None
        self._last_run: Optional[datetime] = None

    async def run(self) -> AgentResult:
        logger.info(f"[{self.name}] Starting run...")
        data: Dict[str, Any] = {}
        summary: str = ""
        fetch_error: Optional[str] = None
        llm_error: Optional[str] = None

        # Step 1: Fetch data — independently handled
        try:
            data = await self.fetch_data()
        except Exception as e:
            fetch_error = str(e)
            logger.error(f"[{self.name}] fetch_data failed: {e}")

        # Step 2: LLM analysis — falls back to raw summary if LLM unavailable
        if data:
            try:
                summary = await self.analyze(data)
            except Exception as e:
                llm_error = str(e)
                logger.warning(f"[{self.name}] LLM analyze failed (showing raw data): {e}")
                summary = self.raw_summary(data)
        elif fetch_error:
            summary = f"⚠️ Could not fetch data: {fetch_error}"
        else:
            summary = "No data available."

        result = AgentResult(
            agent_name=self.name,
            data=data,
            summary=summary,
            error=fetch_error or llm_error,
            success=fetch_error is None,
        )
        self._last_result = result
        self._last_run = datetime.now()
        logger.success(f"[{self.name}] Completed (data={'ok' if data else 'empty'}, llm={'ok' if not llm_error else 'fallback'}).")
        return result

    @abstractmethod
    async def fetch_data(self) -> Dict[str, Any]:
        """Fetch raw data from APIs/web."""
        ...

    @abstractmethod
    async def analyze(self, data: Dict[str, Any]) -> str:
        """Use LLM to analyze and summarize."""
        ...

    def raw_summary(self, data: Dict[str, Any]) -> str:
        """
        Fallback when LLM is unavailable.
        Agents can override this for better raw formatting.
        By default renders the first few keys of data.
        """
        lines = ["📡 **Live data (AI analysis unavailable — start Ollama to enable)**\n"]
        for k, v in list(data.items())[:5]:
            if isinstance(v, list) and v:
                lines.append(f"**{k.replace('_',' ').title()}:** {len(v)} items fetched")
            elif isinstance(v, dict):
                lines.append(f"**{k.replace('_',' ').title()}:** {len(v)} entries")
            elif v:
                lines.append(f"**{k.replace('_',' ').title()}:** {v}")
        return "\n".join(lines)

    def get_last_result(self) -> Optional[AgentResult]:
        return self._last_result
