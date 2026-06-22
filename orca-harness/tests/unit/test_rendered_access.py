from __future__ import annotations

from source_capture.rendered_access import RenderedAccessClass, classify_rendered_access


def test_classify_rendered_access_flags_cloudflare_interstitial() -> None:
    result = classify_rendered_access(
        title="Just a moment...",
        visible_text="Enable JavaScript and cookies to continue",
        rendered_dom="<html><script>window.__cf_chl_tk='token'</script></html>",
    )

    assert result.classification == RenderedAccessClass.ACCESS_BLOCKED
    assert result.signal == "cloudflare_interstitial"


def test_classify_rendered_access_keeps_residual_cloudflare_marker_separate() -> None:
    result = classify_rendered_access(
        title="Mojave Ghost by Byredo",
        visible_text="Reviews 1 2 3 Basenotes source content",
        rendered_dom=(
            "<html><body>Reviews 1 2 3 Basenotes source content"
            "<script src='/cdn-cgi/challenge-platform/scripts/jsd/main.js'></script>"
            "</body></html>"
        ),
    )

    assert result.classification == RenderedAccessClass.RESIDUAL_CHALLENGE_MARKER
    assert result.signal == "residual_cloudflare_challenge_marker"


def test_classify_rendered_access_keeps_hidden_residual_cloudflare_text_separate() -> None:
    result = classify_rendered_access(
        title="Just a moment...",
        visible_text="Reviews 1 2 3 Basenotes source content and comments remain visible",
        rendered_dom=(
            "<html><body>Reviews 1 2 3 Basenotes source content"
            "<template>Enable JavaScript and cookies to continue</template>"
            "<script src='/cdn-cgi/challenge-platform/scripts/jsd/main.js'></script>"
            "</body></html>"
        ),
    )

    assert result.classification == RenderedAccessClass.RESIDUAL_CHALLENGE_MARKER
    assert result.signal == "residual_cloudflare_challenge_marker"


def test_classify_rendered_access_reports_no_block_marker_for_source_content() -> None:
    result = classify_rendered_access(
        title="Rendered Source",
        visible_text="Visible source language",
        rendered_dom="<html><body>Visible source language</body></html>",
    )

    assert result.classification == RenderedAccessClass.NO_BLOCK_MARKER
    assert result.signal is None
