from core.dashboard_data import build_executive_dashboard, build_news_catalog


def test_build_executive_dashboard_includes_required_sections():
    payload = build_executive_dashboard()

    assert payload["header"]["greeting"]
    assert payload["header"]["location"]
    assert payload["summary"]["today"]
    assert "ai_intelligence" in payload["sections"]
    assert "india_politics" in payload["sections"]
    assert "financial" in payload["sections"]
    assert "portfolio" in payload["sections"]
    assert payload["notifications"]["critical"]


def test_build_news_catalog_returns_category_details():
    news = build_news_catalog()

    assert "ai_intelligence" in news
    assert news["ai_intelligence"]["details"]


def test_build_executive_dashboard_includes_actionable_focus_cards():
    payload = build_executive_dashboard()

    assert "focus" in payload
    assert payload["focus"]["priority_actions"]
    assert payload["focus"]["live_signals"]
