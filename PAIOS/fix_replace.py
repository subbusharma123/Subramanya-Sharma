from pathlib import Path
p = Path("dashboard/app.py")
text = p.read_text(encoding="utf-8")
text = text.replace('elif page == "� Projects":', 'elif page == "📁 Projects":')
text = text.replace('elif page == "�🔬 Research":', 'elif page == "🔬 Research":')
p.write_text(text, encoding="utf-8")
