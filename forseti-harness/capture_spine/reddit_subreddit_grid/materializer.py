"""Read-only Reddit Subreddit Registry materializer over committed grid packets.

Capture runners never flip registry state (creator-registry rule); this
materializer is the one writer. It scans explicitly supplied, already
committed ``reddit_subreddit_grid`` Source Capture Packets and applies the
registry spec's two-speed rule:

- observations APPEND (one per packet per subreddit, deduped by provenance
  pointer so a re-run over the same packet cannot double-append);
- descriptive facts UPDATE-ON-CHANGE. This materializer touches only
  ``status`` (a grid capture proves liveness); it deliberately does not
  touch ``public_description_or_none``, because the grid sidebar text and
  the ``about.json`` public description are different source surfaces and
  diffing across surfaces would append spurious change records.

Unknown subreddits (packet target not present in the registry) are reported,
never silently added: grid passes are expected to start FROM a registry
filter, so an unknown target is an operator signal, not new-row authority.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from harness_utils import hash_file
from capture_spine.reddit_subreddit_grid.grid_projection import (
    GridView,
    project_old_reddit_grid_html,
)
from source_capture.models import SOURCE_CAPTURE_MANIFEST_VERSION
from source_capture.packet_inspection import read_packet_leniently
from source_capture.source_quality import resolve_manifest_path

GRID_SOURCE_FAMILY = "reddit_subreddit_grid"
GRID_OBSERVATION_SOURCE_SURFACE = "old_reddit_grid_packet"


class RegistryRefreshError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class PacketGridRead:
    manifest_path: str
    subreddit: str
    observed_at: str
    grid_view: GridView


@dataclass
class RegistryRefreshOutcome:
    registry_path: str
    refreshed_subreddits: list[str] = field(default_factory=list)
    duplicate_observation_skips: list[str] = field(default_factory=list)
    unknown_subreddits: list[str] = field(default_factory=list)
    status_changes: list[str] = field(default_factory=list)
    registry_written: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "registry_path": self.registry_path,
            "refreshed_subreddits": self.refreshed_subreddits,
            "duplicate_observation_skips": self.duplicate_observation_skips,
            "unknown_subreddits": self.unknown_subreddits,
            "status_changes": self.status_changes,
            "registry_written": self.registry_written,
            "non_claims": [
                "not metric authority",
                "not demand proof",
                "not venue quality or fit scoring",
                "not capture authorization",
            ],
        }


def refresh_registry_from_grid_packets(
    *,
    registry_path: Path,
    packet_paths: list[Path],
    dry_run: bool = False,
) -> RegistryRefreshOutcome:
    if not packet_paths:
        raise RegistryRefreshError("no_packets", "at least one grid packet path is required")

    reads = [read_grid_packet(packet_or_manifest_path=path) for path in packet_paths]

    document = json.loads(registry_path.read_text(encoding="utf-8"))
    registry = document.get("reddit_subreddit_registry")
    if not isinstance(registry, dict) or not isinstance(registry.get("subreddits"), list):
        raise RegistryRefreshError("registry_shape", f"not a reddit_subreddit_registry document: {registry_path}")
    rows_by_name = {row["subreddit"]: row for row in registry["subreddits"]}

    outcome = RegistryRefreshOutcome(registry_path=str(registry_path))
    changed = False
    for read in reads:
        row = rows_by_name.get(read.subreddit)
        if row is None:
            outcome.unknown_subreddits.append(read.subreddit)
            continue
        if _apply_two_speed_refresh(row=row, read=read, outcome=outcome):
            changed = True
            outcome.refreshed_subreddits.append(read.subreddit)

    if changed and not dry_run:
        counts = registry.setdefault("counts", {})
        counts["subreddits_total"] = len(registry["subreddits"])
        by_status: dict[str, int] = {}
        for row in registry["subreddits"]:
            by_status[row["status"]] = by_status.get(row["status"], 0) + 1
        counts["by_status"] = dict(sorted(by_status.items()))
        with registry_path.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(document, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        outcome.registry_written = True
    return outcome


def read_grid_packet(*, packet_or_manifest_path: Path) -> PacketGridRead:
    manifest_path = resolve_manifest_path(packet_or_manifest_path)
    try:
        report = read_packet_leniently(manifest_path)
    except Exception as exc:
        raise RegistryRefreshError("manifest_read_failure", f"manifest could not be read: {exc}") from exc
    if not report.conforms_to_current_schema or not report.declares_current_manifest_version:
        raise RegistryRefreshError(
            "manifest_nonconforming",
            f"manifest is not a current {SOURCE_CAPTURE_MANIFEST_VERSION!r} packet: {manifest_path}",
        )
    packet = report.packet
    if packet is None:
        raise RegistryRefreshError("packet_unavailable", "no validated packet was available")
    if packet.source_family != GRID_SOURCE_FAMILY:
        raise RegistryRefreshError(
            "ineligible_source_family",
            f"packet source_family is {packet.source_family!r}, not {GRID_SOURCE_FAMILY!r}",
        )

    locator = packet.source_locator.value or ""
    subreddit = _subreddit_from_listing_url(locator)
    if subreddit is None:
        raise RegistryRefreshError("locator_unparseable", f"cannot parse subreddit from locator: {locator!r}")

    raw_file = _resolve_raw_body_file(packet)
    raw_path = manifest_path.parent / raw_file["relative_packet_path"]
    actual_hash = hash_file(raw_path)
    if actual_hash != raw_file["sha256"]:
        raise RegistryRefreshError(
            "raw_file_hash_mismatch",
            f"stored bytes hash mismatch for {raw_path.name}: manifest={raw_file['sha256']} actual={actual_hash}",
        )

    html = raw_path.read_text(encoding="utf-8", errors="replace")
    grid_view = project_old_reddit_grid_html(
        html_text=html,
        subreddit=subreddit,
        listing_url=locator,
    )
    observed_at = _observed_date(packet)
    return PacketGridRead(
        manifest_path=str(manifest_path),
        subreddit=subreddit,
        observed_at=observed_at,
        grid_view=grid_view,
    )


def _apply_two_speed_refresh(
    *,
    row: dict[str, object],
    read: PacketGridRead,
    outcome: RegistryRefreshOutcome,
) -> bool:
    observations = row.setdefault("observations", [])
    assert isinstance(observations, list)
    if any(obs.get("provenance_pointer") == read.manifest_path for obs in observations):
        outcome.duplicate_observation_skips.append(read.subreddit)
        return False

    view = read.grid_view
    observations.append(
        {
            "observed_at": read.observed_at,
            "subscriber_count_or_none": _normalized_count(view.visible_subscriber_count_or_none),
            "active_user_count_or_none": _normalized_count(view.visible_active_user_count_or_none),
            "source_surface": GRID_OBSERVATION_SOURCE_SURFACE,
            "provenance_pointer": read.manifest_path,
            "absent_reason_or_none": view.visible_volume_signal_absent_reason_or_none,
        }
    )

    if row.get("status") != "active":
        row.setdefault("descriptive_changes", []).append(
            {"field": "status", "changed_at": read.observed_at, "previous_value": row.get("status")}
        )
        row["status"] = "active"
        outcome.status_changes.append(read.subreddit)
    row["status_observed_at"] = read.observed_at

    if row.get("capture_state") == "no_packet_recorded":
        row["capture_state"] = "grid_packets_recorded"

    register_pointers = row.setdefault("register_pointers", [])
    assert isinstance(register_pointers, list)
    if read.manifest_path not in register_pointers:
        register_pointers.append(read.manifest_path)
    return True


def _resolve_raw_body_file(packet) -> dict[str, str]:
    body_files = [
        {"relative_packet_path": item.relative_packet_path, "sha256": item.sha256}
        for item in packet.preserved_files
        if item.relative_packet_path.endswith("http_response_body.bin")
    ]
    if len(body_files) != 1:
        raise RegistryRefreshError(
            "raw_body_unresolved",
            f"expected exactly one preserved http_response_body.bin, found {len(body_files)}",
        )
    return body_files[0]


def _subreddit_from_listing_url(url: str) -> str | None:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) >= 2 and parts[0] == "r" and parts[1].replace("_", "").isalnum():
        return parts[1].lower()
    return None


def _observed_date(packet) -> str:
    for source_slice in packet.source_slices:
        capture_time = source_slice.timing.capture_time.value
        if capture_time:
            return str(capture_time)[:10]
    raise RegistryRefreshError("capture_time_missing", "packet carries no slice capture_time")


def _normalized_count(value: str | None) -> str | None:
    if value is None:
        return None
    digits = value.replace(",", "").strip()
    if digits.isdigit():
        return digits
    return value
