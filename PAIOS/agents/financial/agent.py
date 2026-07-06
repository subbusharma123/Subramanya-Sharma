"""
Financial Markets Agent
Fetches Indian & US market data, crypto, forex and commodities.
Uses yfinance (free) + CoinGecko (free) + Alpha Vantage.
"""
import yfinance as yf
from pycoingecko import CoinGeckoAPI
from typing import Any, Dict
from loguru import logger
from langchain_core.messages import HumanMessage

from agents.base import BaseAgent

INDIAN_INDICES = {
    "NIFTY 50":   "^NSEI",
    "SENSEX":     "^BSESN",
    "Bank Nifty": "^NSEBANK",
    "Nifty Midcap": "NIFTYMIDCAP150.NS",
}

US_INDICES = {
    "S&P 500":   "^GSPC",
    "NASDAQ":    "^IXIC",
    "Dow Jones": "^DJI",
}

COMMODITIES = {
    "Gold":        "GC=F",
    "Silver":      "SI=F",
    "Crude Oil":   "CL=F",
    "Natural Gas": "NG=F",
}

FOREX = {
    "USD/INR": "USDINR=X",
    "EUR/INR": "EURINR=X",
    "GBP/INR": "GBPINR=X",
    "EUR/USD": "EURUSD=X",
}

CRYPTO_IDS = [
    "bitcoin", "ethereum", "tether", "binancecoin", "solana",
    "ripple", "dogecoin", "cardano", "avalanche-2", "polkadot"
]


class FinancialAgent(BaseAgent):
    name = "financial"
    refresh_interval = 300  # 5 min

    async def fetch_data(self) -> Dict[str, Any]:
        result = {}

        # Fetch all ticker groups
        all_tickers = {**INDIAN_INDICES, **US_INDICES, **COMMODITIES, **FOREX}
        ticker_data = {}
        for name, symbol in all_tickers.items():
            try:
                t = yf.Ticker(symbol)
                hist = t.history(period="2d")
                if not hist.empty:
                    latest = hist["Close"].iloc[-1]
                    prev = hist["Close"].iloc[-2] if len(hist) > 1 else latest
                    change_pct = ((latest - prev) / prev) * 100
                    ticker_data[name] = {
                        "price": round(latest, 2),
                        "change_pct": round(change_pct, 2),
                    }
            except Exception as e:
                logger.warning(f"[financial] {name}: {e}")

        result["markets"] = ticker_data

        # Crypto via CoinGecko (free, no key needed for basic)
        try:
            cg = CoinGeckoAPI()
            crypto_data = cg.get_coins_markets(
                vs_currency="usd",
                ids=",".join(CRYPTO_IDS),
                order="market_cap_desc",
                per_page=10,
            )
            result["crypto"] = [
                {
                    "name": c["name"],
                    "symbol": c["symbol"].upper(),
                    "price": c["current_price"],
                    "change_24h": round(c["price_change_percentage_24h"] or 0, 2),
                }
                for c in crypto_data
            ]
        except Exception as e:
            logger.warning(f"[financial] Crypto fetch failed: {e}")
            result["crypto"] = []

        return result

    def raw_summary(self, data: Dict[str, Any]) -> str:
        markets = data.get("markets", {})
        crypto = data.get("crypto", [])
        lines = ["📡 **Live Market Data** *(AI analysis unavailable — install Ollama)*\n"]
        if markets:
            lines.append("**📊 Markets:**")
            for name, v in markets.items():
                sign = "+" if v["change_pct"] >= 0 else ""
                color_icon = "🟢" if v["change_pct"] >= 0 else "🔴"
                lines.append(f"  {color_icon} {name}: **{v['price']}** ({sign}{v['change_pct']}%)")
        if crypto:
            lines.append("\n**₿ Crypto:**")
            for c in crypto[:5]:
                sign = "+" if c["change_24h"] >= 0 else ""
                icon = "🟢" if c["change_24h"] >= 0 else "🔴"
                lines.append(f"  {icon} {c['name']} ({c['symbol']}): **${c['price']:,}** ({sign}{c['change_24h']}%)")
        return "\n".join(lines)

    async def analyze(self, data: Dict[str, Any]) -> str:
        markets = data.get("markets", {})
        crypto = data.get("crypto", [])

        market_lines = "\n".join([
            f"  {name}: {v['price']} ({'+' if v['change_pct'] >= 0 else ''}{v['change_pct']}%)"
            for name, v in markets.items()
        ])
        crypto_lines = "\n".join([
            f"  {c['name']} ({c['symbol']}): ${c['price']:,} ({'+' if c['change_24h'] >= 0 else ''}{c['change_24h']}%)"
            for c in crypto[:5]
        ])

        llm = self.llm.get("fast")
        msg = HumanMessage(content=f"""
You are a financial analyst. Given today's market data, provide a concise summary:
1. Overall market sentiment (Bearish/Neutral/Bullish)
2. Top movers (biggest gains & losses)
3. Key observations
4. India-specific market outlook

Market Data:
{market_lines}

Top Crypto:
{crypto_lines}

Keep response under 200 words.
""")
        result = await llm.ainvoke([msg])
        return result.content
