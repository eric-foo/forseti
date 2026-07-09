"""Coverage flag: a packet-producing capture runner must either carry the Data
Lake seam (``--data-root`` / ``data_root`` -> commit into the lake) or be
explicitly acknowledged as not-yet-synced.

This is the enforced version of the manual "which runners route into the lake?"
survey. Adding a NEW packet runner without the seam -- and without an entry in
``KNOWN_UNSYNCED`` -- fails this test on purpose. That is the nudge: wire the
seam (mirror ``run_source_capture_http_packet.py``) or acknowledge the gap with a
reason. The test also fails if a runner gains the seam but is left in the
allowlist, so the allowlist cannot rot.
"""
from __future__ import annotations

from pathlib import Path

_RUNNERS_DIR = Path(__file__).resolve().parents[2] / "runners"

# A runner is a raw-packet PRODUCER if it writes a SourceCapturePacket.
_PRODUCER_TOKENS = ("write_local_source_capture_packet", "stage_and_write_packet")
# The lake seam: the runner can commit into the lake by key.
_SEAM_TOKEN = "data_root"

# Packet-producing runners that intentionally do NOT route into the lake yet.
# Each MUST carry a reason. Remove an entry when you wire its seam. Adding a new
# packet runner without the seam and without an entry here fails the test below.
KNOWN_UNSYNCED: dict[str, str] = {
    "run_source_capture_browser_packet.py": "browser-snapshot surface not yet captured live into the lake",
    "run_source_capture_authenticated_browser_packet.py": "authenticated-browser surface not yet captured live",
    "run_source_capture_cloakbrowser_packet.py": "anti-detect browser surface not yet captured live",
    "run_source_capture_antiblock_http_packet.py": "anti-blocking HTTP surface not yet captured live",
    "run_source_capture_archive_packet.py": "archive.org / archive.today surface not yet captured live",
    "run_source_capture_historical_packet.py": "multi-archive historical surface not yet captured live",
    "run_source_capture_media_packet.py": "media-asset surface not yet captured live",
    "run_source_capture_price_payload_packet.py": "vendor-pricing payload surface not yet captured live",
    "run_source_capture_ig_calls_packet.py": "instagram creator-momentum surface not yet captured live",
}


def _packet_producers() -> dict[str, bool]:
    """Map each packet-producing runner filename -> whether it carries the seam."""
    producers: dict[str, bool] = {}
    for path in sorted(_RUNNERS_DIR.glob("run_*.py")):
        src = path.read_text(encoding="utf-8")
        if any(token in src for token in _PRODUCER_TOKENS):
            producers[path.name] = _SEAM_TOKEN in src
    return producers


def test_every_packet_runner_is_lake_wired_or_acknowledged() -> None:
    producers = _packet_producers()
    assert producers, "no packet-producing runners detected -- detection tokens are stale"

    unsynced = {name for name, has_seam in producers.items() if not has_seam}

    new_unsynced = unsynced - set(KNOWN_UNSYNCED)
    assert not new_unsynced, (
        "Packet-producing runner(s) missing the lake seam (no `data_root` / `--data-root`).\n"
        "Wire the seam (mirror run_source_capture_http_packet.py) OR add to KNOWN_UNSYNCED with a reason:\n"
        f"  {sorted(new_unsynced)}"
    )

    stale_ack = set(KNOWN_UNSYNCED) - unsynced
    assert not stale_ack, (
        "KNOWN_UNSYNCED lists runner(s) that now carry the seam (or are no longer packet producers).\n"
        "Remove them from KNOWN_UNSYNCED:\n"
        f"  {sorted(stale_ack)}"
    )


def test_known_unsynced_entries_have_reasons() -> None:
    missing = [name for name, reason in KNOWN_UNSYNCED.items() if not reason.strip()]
    assert not missing, f"KNOWN_UNSYNCED entries need a reason: {missing}"
