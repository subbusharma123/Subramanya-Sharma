"""
PAIOS — Main Entry Point
Orchestrates all agents and starts the scheduler.
"""
import asyncio
import signal
from loguru import logger
from rich.console import Console
from rich.panel import Panel

from core.orchestrator import PAIOSOrchestrator
from core.config import settings

console = Console()

def print_banner():
    console.print(Panel.fit(
        "[bold cyan]🧠 PAIOS — Personal AI Operating System[/bold cyan]\n"
        "[dim]Your Personal AI Executive Assistant[/dim]\n\n"
        f"[green]User:[/green] {settings.USER_NAME}\n"
        f"[green]Location:[/green] {settings.USER_LOCATION}\n"
        f"[green]LLM:[/green] {settings.OLLAMA_PRIMARY_MODEL} (local) + {settings.OPENAI_MODEL} (cloud fallback)",
        border_style="cyan"
    ))

async def main():
    print_banner()
    orchestrator = PAIOSOrchestrator()

    # Handle graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, orchestrator.shutdown)

    try:
        logger.info("Starting PAIOS orchestrator...")
        await orchestrator.start()
    except KeyboardInterrupt:
        logger.info("Shutting down PAIOS...")
    finally:
        await orchestrator.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
