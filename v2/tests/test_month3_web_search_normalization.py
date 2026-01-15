from v2.engine_adapter import EngineInput, run_engine_via_v1

def test_bare_search_the_web_triggers_followup():
    out = run_engine_via_v1(EngineInput(raw_text="search the web", awake=True))
    assert out.route_kind == "WEB_LOOKUP_FOLLOWUP"
    assert "search the web for" in out.speak_text.lower() or "what would you like" in out.speak_text.lower()
    assert out.actions == []

def test_search_the_web_for_normalizes_to_web_lookup_action():
    out = run_engine_via_v1(EngineInput(raw_text="search the web for pizza near me", awake=True))
    types = [a.get("type") for a in (out.actions or [])]
    assert "WEB_LOOKUP_QUERY" in types
