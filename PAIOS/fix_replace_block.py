from pathlib import Path
p = Path("dashboard/app.py")
text = p.read_text(encoding="utf-8")
start = text.index('elif page == "📈 Portfolio":')
end = text.index('elif page == "📅 Productivity":', start)
replacement = '''elif page == "📈 Portfolio":
    render_page_header("📈 Portfolio", "Your personal portfolio overview and suggestions.")
    result = run_agent(PortfolioAgent)
    render_agent_summary("Portfolio Summary", result, show_data=False)
    st.markdown("**Note:** This is a placeholder until your portfolio data is connected.")

elif page == "📁 Projects":
    render_page_header("📁 Projects", "Workspace activity, code changes, and project focus.")
    insights = get_project_insights()
    render_project_insights(insights)
    st.markdown("#### Actionable next steps")
    if insights["git_changes"]:
        st.write("- Review or commit the listed Git changes.")
    else:
        st.write("- No uncommitted changes found. Consider narrowing your next task.")
    if insights["recent_files"]:
        st.write("- Continue working on: " + ", ".join(insights["recent_files"][:3]))
    else:
        st.write("- Open a project file to begin your next session.")

elif page == "🔬 Research":
    render_page_header("🔬 Research", "Recent papers and technical research highlights.")
    with st.spinner("Compiling research digest..."):
        result = run_agent(ResearchAgent)
    render_agent_summary("Research Digest", result, show_data=False)
    if result.data.get("papers"):
        for p in result.data["papers"][:10]:
            with st.expander(f"[{p['source']}] {p['title']}"):
                st.write(p["summary"])
                if p.get("link"):
                    st.markdown(f"[Read more]({p['link']})")
'''
text = text[:start] + replacement + text[end:]
p.write_text(text, encoding="utf-8")
print("updated")
