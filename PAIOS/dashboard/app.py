"""
PAIOS Streamlit Dashboard
"""

from __future__ import annotations

import asyncio
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from agents import PortfolioAgent, ProductivityAgent, ResearchAgent
from agents.base import AgentResult
from core.llm import LLMRouter


PAGE_OPTIONS = [
    "Home",
    "📁 Projects",
    "🔬 Research",
    "📅 Productivity",
    "📈 Portfolio",
]


@st.cache_data(ttl=300)
def get_project_insights() -> Dict[str, List[str]]:
    git_changes: List[str] = []
    recent_files: List[str] = []

    if (ROOT_DIR / ".git").exists():
        try:
            status = subprocess.check_output(
                ["git", "status", "--short"],
                cwd=ROOT_DIR,
                text=True,
                stderr=subprocess.DEVNULL,
            )
            git_changes = [line.strip() for line in status.splitlines() if line.strip()][:12]

            log_files = subprocess.check_output(
                ["git", "log", "--name-only", "--pretty=format:", "-n", "20"],
                cwd=ROOT_DIR,
                text=True,
                stderr=subprocess.DEVNULL,
            )
            candidates = [line.strip() for line in log_files.splitlines() if line.strip()]
            unique_files = []
            for item in candidates:
                if item not in unique_files:
                    unique_files.append(item)
            recent_files = unique_files[:10]
        except (subprocess.CalledProcessError, FileNotFoundError):
            git_changes = []
            recent_files = []

    if not recent_files:
        python_files = [p for p in ROOT_DIR.rglob("*.py") if p.is_file()]
        recent_files = [str(p.relative_to(ROOT_DIR)) for p in sorted(python_files, key=lambda p: p.stat().st_mtime, reverse=True)[:10]]

    return {
        "git_changes": git_changes,
        "recent_files": recent_files,
    }


def get_system_insights() -> Dict[str, Any]:
    try:
        import platform
        import psutil

        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(ROOT_DIR))
        uptime = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M")

        return {
            "hostname": platform.node(),
            "platform": f"{platform.system()} {platform.release()}",
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "memory_percent": memory.percent,
            "memory_used": f"{memory.used // (1024**2)} MB / {memory.total // (1024**3)} GB",
            "disk_percent": disk.percent,
            "disk_used": f"{disk.used // (1024**3)} GB / {disk.total // (1024**3)} GB",
            "boot_time": uptime,
        }
    except Exception:
        return {
            "hostname": "unknown",
            "platform": "unknown",
            "cpu_percent": 0,
            "memory_percent": 0,
            "memory_used": "unknown",
            "disk_percent": 0,
            "disk_used": "unknown",
            "boot_time": "unknown",
        }


def run_agent(agent_cls: Any) -> AgentResult:
    llm = LLMRouter()
    agent = agent_cls(llm)
    try:
        return asyncio.run(agent.run())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(agent.run())
    except Exception as exc:
        return AgentResult(
            agent_name=agent_cls.__name__,
            data={},
            summary=f"Agent error: {exc}",
            error=str(exc),
            success=False,
        )


def render_page_header(title: str, subtitle: str) -> None:
    st.title(title)
    st.caption(subtitle)
    st.markdown("---")


def render_summary_card(title: str, value: str, description: str) -> None:
    st.markdown(
        f"""
        <div style='padding:18px; border-radius:14px; border:1px solid #e6e6e6; background:#fbfbfb;'>
            <h3 style='margin:0 0 10px 0;'>{title}</h3>
            <div style='font-size:28px; font-weight:700; margin-bottom:8px;'>{value}</div>
            <div style='color:#555; line-height:1.5;'>{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_agent_summary(title: str, result: AgentResult, show_data: bool = True) -> None:
    st.subheader(title)

    if not result.success:
        st.warning(result.summary)
        return

    st.write(result.summary)
    if show_data and result.data:
        with st.expander("Show raw agent data"):
            st.json(result.data)


def build_home_page() -> None:
    render_page_header("PAIOS Home", "Your personal intelligence dashboard for work, research, and productivity.")

    metrics = get_project_insights()
    system_metrics = get_system_insights()
    last_updated = datetime.now().strftime("%I:%M %p, %b %d %Y")

    st.markdown(f"**Last refresh:** {last_updated}")

    col1, col2, col3 = st.columns(3)
    with col1:
        render_summary_card(
            "Workspace status",
            str(len(metrics["git_changes"])),
            "Pending git changes waiting for your review.",
        )
    with col2:
        render_summary_card(
            "Recent files",
            str(len(metrics["recent_files"])),
            "Files edited in the last project session.",
        )
    with col3:
        render_summary_card(
            "Laptop load",
            f"{system_metrics['cpu_percent']}% CPU",
            f"Memory: {system_metrics['memory_percent']}% · Disk: {system_metrics['disk_percent']}%",
        )

    st.markdown("### Snapshot: Project productivity")
    if metrics["git_changes"]:
        st.write("#### Pending git changes")
        for change in metrics["git_changes"]:
            st.code(change)
    else:
        st.info("No pending git changes were detected. Your workspace is clean or git is unavailable.")

    st.markdown("### Recent files")
    if metrics["recent_files"]:
        for file_path in metrics["recent_files"][:8]:
            st.write(f"- `{file_path}`")
    else:
        st.write("No recent project files found.")

    st.markdown("### Quick actions")
    if metrics["git_changes"]:
        st.write("- Commit or stash the pending changes before moving to the next task.")
    st.write("- Open the sidebar and select a page to continue: Projects, Research, or Productivity.")
    st.write("- Use the Research page to review fresh AI research and the Productivity page to track your next work items.")


def build_projects_page() -> None:
    render_page_header("📁 Projects", "Workspace activity, code changes, and project focus.")
    insights = get_project_insights()

    st.write("#### Project Intelligence")
    if insights["git_changes"]:
        st.write("**Pending changes:**")
        for row in insights["git_changes"]:
            st.code(row)
    else:
        st.success("No uncommitted git changes detected.")

    st.write("#### Recent files")
    if insights["recent_files"]:
        st.write(", ".join(insights["recent_files"][:10]))
    else:
        st.write("No project file history available.")

    st.markdown("#### Actionable next steps")
    if insights["git_changes"]:
        st.write("- Review or commit the listed git changes.")
    else:
        st.write("- Your workspace looks clean. Start a focused coding session.")
    if insights["recent_files"]:
        st.write(f"- Continue working on: {', '.join(insights['recent_files'][:3])}.")
    else:
        st.write("- Open a project file to begin your next session.")


def build_research_page() -> None:
    render_page_header("🔬 Research", "Recent technical research, AI papers, and curated summaries.")
    with st.spinner("Refreshing research digest..."):
        result = run_agent(ResearchAgent)

    render_agent_summary("Research Digest", result, show_data=False)

    papers = result.data.get("papers", []) if result and result.data else []
    if papers:
        st.markdown("#### Latest research items")
        for paper in papers[:8]:
            with st.expander(f"[{paper.get('source', 'source')}] {paper.get('title', 'untitled')}"):
                st.write(paper.get("summary", "No summary available."))
                if paper.get("link"):
                    st.markdown(f"[Read more]({paper['link']})")


def build_productivity_page() -> None:
    render_page_header("📅 Productivity", "Calendar, tasks, and local productivity signals.")
    with st.spinner("Loading productivity snapshot..."):
        result = run_agent(ProductivityAgent)

    render_agent_summary("Productivity Overview", result, show_data=False)

    if result and result.summary:
        st.markdown("#### Notes")
        st.write(result.summary)


def build_portfolio_page() -> None:
    render_page_header("📈 Portfolio", "Your portfolio placeholder and investment briefing.")
    with st.spinner("Loading portfolio insights..."):
        result = run_agent(PortfolioAgent)

    render_agent_summary("Portfolio Summary", result, show_data=False)
    st.markdown("---")
    st.write("**Note:** Connect your portfolio data source in `agents/stubs.py` or add a real portfolio agent to replace this placeholder.")


def main() -> None:
    st.set_page_config(
        page_title="PAIOS Dashboard",
        page_icon="🧠",
        layout="wide",
    )

    st.sidebar.title("PAIOS Navigation")
    page = st.sidebar.radio("Select a page", PAGE_OPTIONS)
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "Use this dashboard to monitor your projects, research, productivity, and portfolio placeholders."
    )

    if page == "Home":
        build_home_page()
    elif page == "📁 Projects":
        build_projects_page()
    elif page == "🔬 Research":
        build_research_page()
    elif page == "📅 Productivity":
        build_productivity_page()
    elif page == "📈 Portfolio":
        build_portfolio_page()
    else:
        st.error("Selected page is not available.")


if __name__ == "__main__":
    main()
