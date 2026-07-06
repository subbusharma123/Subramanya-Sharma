"""
Stub agents — Portfolio, AI Investment, Productivity, Email, Notification
These provide working stubs that can be expanded with real API integrations.
"""
from agents.base import BaseAgent
from typing import Any, Dict
from langchain_core.messages import HumanMessage


class PortfolioAgent(BaseAgent):
    name = "portfolio"
    refresh_interval = 900

    async def fetch_data(self) -> Dict[str, Any]:
        # TODO: Integrate Zerodha API, Groww API, or manual CSV
        return {
            "note": "Portfolio data — connect Zerodha/Groww API or add manual holdings in config/portfolio.json",
            "portfolio": []
        }

    async def analyze(self, data: Dict[str, Any]) -> str:
        return "📊 Portfolio Agent: Add your holdings in config/portfolio.json to activate tracking."


class AIInvestmentAgent(BaseAgent):
    name = "ai_investment"
    refresh_interval = 3600

    AI_SECTOR_TICKERS = {
        "NVIDIA": "NVDA", "Microsoft": "MSFT", "Alphabet": "GOOGL",
        "Meta": "META", "AMD": "AMD", "Intel": "INTC",
        "Palantir": "PLTR", "C3.ai": "AI",
    }

    async def fetch_data(self) -> Dict[str, Any]:
        import yfinance as yf
        data = {}
        for name, sym in self.AI_SECTOR_TICKERS.items():
            try:
                t = yf.Ticker(sym)
                hist = t.history(period="2d")
                if not hist.empty:
                    latest = hist["Close"].iloc[-1]
                    prev = hist["Close"].iloc[-2] if len(hist) > 1 else latest
                    change_pct = ((latest - prev) / prev) * 100
                    data[name] = {"symbol": sym, "price": round(latest, 2), "change": round(change_pct, 2)}
            except Exception:
                pass
        return {"ai_stocks": data}

    async def analyze(self, data: Dict[str, Any]) -> str:
        stocks = data.get("ai_stocks", {})
        if not stocks:
            return "AI investment data unavailable."

        lines = "\n".join([f"{k} ({v['symbol']}): ${v['price']} ({'+' if v['change']>=0 else ''}{v['change']}%)"
                           for k, v in stocks.items()])
        llm = self.llm.get("fast")
        msg = HumanMessage(content=f"""
Analyze these AI sector stocks and provide:
1. Best opportunity today
2. Highest risk today  
3. Sector trend observation

Stocks:
{lines}

Under 150 words.
""")
        result = await llm.ainvoke([msg])
        return result.content


class ProductivityAgent(BaseAgent):
    name = "productivity"
    refresh_interval = 1800

    async def fetch_data(self) -> Dict[str, Any]:
        # TODO: Integrate Google Calendar API
        return {
            "note": "Connect Google Calendar via OAuth — see docs/setup_google.md",
            "events": [],
            "tasks": []
        }

    async def analyze(self, data: Dict[str, Any]) -> str:
        return "📅 Productivity Agent: Connect Google Calendar in config to see your schedule here."


class NotificationAgent(BaseAgent):
    name = "notification"
    refresh_interval = 60

    async def fetch_data(self) -> Dict[str, Any]:
        return {}

    async def analyze(self, data: Dict[str, Any]) -> str:
        return "Notification agent active."

    async def send_morning_digest(self):
        try:
            from plyer import notification
            notification.notify(
                title="🧠 PAIOS — Good Morning Subramanya!",
                message="Your daily briefing is ready. Open the dashboard.",
                timeout=10
            )
        except Exception:
            pass


class EmailAgent(BaseAgent):
    name = "email"
    refresh_interval = 600

    async def fetch_data(self) -> Dict[str, Any]:
        # TODO: Integrate Gmail API with OAuth
        return {"note": "Connect Gmail via Google OAuth — see docs/setup_google.md"}

    async def analyze(self, data: Dict[str, Any]) -> str:
        return "📧 Email Agent: Connect Gmail API via OAuth to enable email intelligence."
