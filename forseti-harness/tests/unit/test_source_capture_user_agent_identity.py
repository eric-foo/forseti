from __future__ import annotations

from source_capture.adapters import (
    direct_http,
    fragrance_discovery_fetch,
    fragrance_widget_fallback,
    publisher_history,
    reddit_api,
)


def test_default_source_capture_user_agents_use_forseti_identity() -> None:
    user_agents = [
        direct_http.DEFAULT_USER_AGENT,
        fragrance_discovery_fetch._USER_AGENT,
        fragrance_widget_fallback.DEFAULT_WIDGET_FALLBACK_USER_AGENT,
        publisher_history.DEFAULT_PUBLISHER_HISTORY_USER_AGENT,
        reddit_api.DEFAULT_USER_AGENT,
    ]

    assert all("ForsetiSourceCapture" in user_agent for user_agent in user_agents)
    assert all("OrcaSourceCapture" not in user_agent for user_agent in user_agents)
