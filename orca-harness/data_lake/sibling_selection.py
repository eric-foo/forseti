"""Fail-closed sibling selection -- the shared read-side rule that names the CURRENT
derived record for a subject when the write-once lake holds N sibling records.

The seam's S3 behavior multiplies derived siblings by design: every policy bump or
catch-up re-derivation appends a fresh record next to its predecessor, and
``DataLakeRoot.append_record`` is write-once with no append sequence. Readers that
invent their own selection have picked STALE siblings via lexical accidents
(F-IGRC-001). This module is the general rule such readers bind to instead:

- ordering inputs are EXPLICIT. A candidate carries its subject, raw anchor,
  content hash, an optional parsed capture instant, and a caller-declared
  derivation rank (declared by the lane that mints the record ids -- this module
  never re-derives rank from record-id strings). Lexical paths and raw timestamp
  strings never order the choice.
- selection FAILS CLOSED: when "current" is not well-defined the rule raises
  ``SiblingSelectionError`` rather than silently keeping either sibling --
  mirroring the fail-closed contract of the creator-metric rollup selection
  (``select_latest_rollup_per_account``), which solved the same shape with a
  stamped run order.

Selection per subject, in order:

1. Candidates with identical ``content_hash`` collapse to one. Identical bytes
   cannot disagree, so the representative (lexically smallest ``record_ref``) is
   pure determinism, not a content choice.
2. Within one ``raw_anchor``, the highest ``derivation_rank`` supersedes lower
   ranks (e.g. a declared catch-up re-derivation supersedes the record it
   re-derives). Distinct-content candidates tying on the top rank raise
   ``ambiguous_sibling_derivation``.
3. Across anchors, the newest ``capture_instant_or_none`` wins. A candidate that
   must be ordered but carries no instant, or distinct-content candidates tying
   on the same instant, raise ``unorderable_capture_recency``. A single
   surviving candidate needs no ordering and no instant.

This is the pure rule: no lake discovery, no I/O, no producer imports. Discovery
stays lane-side; the caller maps its records into ``SiblingCandidate`` rows and
surfaces the bypassed set as named residuals instead of silently absorbing it.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable


class SiblingSelectionError(ValueError):
    """Raised when the current record for a subject is not well-defined.

    Subclasses ``ValueError`` so existing fail-closed ``except ValueError`` paths
    still catch it. ``reason`` is the machine-readable code
    (``ambiguous_sibling_derivation`` or ``unorderable_capture_recency``) and
    ``subject_key`` is the subject selection failed on.
    """

    def __init__(self, reason: str, subject_key: str, detail: str) -> None:
        self.reason = reason
        self.subject_key = subject_key
        super().__init__(f"{reason} for subject {subject_key!r}: {detail}")


@dataclass(frozen=True)
class SiblingCandidate:
    """One derived record as offered to selection for one subject.

    ``derivation_rank`` is the caller-declared within-anchor supersession rank,
    owned by the lane that mints the record ids (higher supersedes lower;
    baseline 0). ``capture_instant_or_none`` is a parsed aware instant (use
    ``parse_capture_instant``), never a raw string. ``payload`` is an opaque
    carry-through for the caller.
    """

    subject_key: str
    raw_anchor: str
    record_ref: str
    content_hash: str
    capture_instant_or_none: datetime | None = None
    derivation_rank: int = 0
    payload: Any = None


@dataclass(frozen=True)
class SelectedSibling:
    """The current record chosen for one subject, plus every distinct-content
    candidate the rule bypassed (superseded within its anchor, or older across
    anchors) so the caller can surface residuals."""

    selected: SiblingCandidate
    bypassed: tuple[SiblingCandidate, ...]


def parse_capture_instant(value: str | None) -> datetime | None:
    """Parse an ISO-8601 capture time into an aware instant for ordering, mirroring
    the harness-wide ``fromisoformat`` idiom: a trailing ``Z`` is normalized and a
    naive value is treated as UTC. Empty or None -> None -- absence stays
    unorderable; it is never coerced to an epoch."""
    if value is None or not str(value).strip():
        return None
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def select_current_record_per_subject(
    candidates: Iterable[SiblingCandidate],
) -> dict[str, SelectedSibling]:
    """Select the single current record per subject, failing closed when
    "current" is not well-defined. Returns ``{subject_key: SelectedSibling}``."""
    grouped: dict[str, list[SiblingCandidate]] = {}
    for candidate in candidates:
        grouped.setdefault(candidate.subject_key, []).append(candidate)
    return {
        subject_key: _select_one_subject(subject_key, group)
        for subject_key, group in grouped.items()
    }


def _select_one_subject(subject_key: str, group: list[SiblingCandidate]) -> SelectedSibling:
    collapsed = _collapse_identical_content(group)
    by_anchor: dict[str, list[SiblingCandidate]] = {}
    for candidate in collapsed:
        by_anchor.setdefault(candidate.raw_anchor, []).append(candidate)

    anchor_winners: list[SiblingCandidate] = []
    bypassed: list[SiblingCandidate] = []
    for anchor in sorted(by_anchor):
        winner, superseded = _apply_anchor_rank(subject_key, anchor, by_anchor[anchor])
        anchor_winners.append(winner)
        bypassed.extend(superseded)

    selected, older = _apply_capture_recency(subject_key, anchor_winners)
    bypassed.extend(older)
    return SelectedSibling(selected=selected, bypassed=tuple(bypassed))


def _collapse_identical_content(group: list[SiblingCandidate]) -> list[SiblingCandidate]:
    by_hash: dict[str, SiblingCandidate] = {}
    for candidate in group:
        current = by_hash.get(candidate.content_hash)
        if current is None or candidate.record_ref < current.record_ref:
            by_hash[candidate.content_hash] = candidate
    return sorted(by_hash.values(), key=lambda item: item.record_ref)


def _apply_anchor_rank(
    subject_key: str, anchor: str, candidates: list[SiblingCandidate]
) -> tuple[SiblingCandidate, list[SiblingCandidate]]:
    top_rank = max(candidate.derivation_rank for candidate in candidates)
    winners = [c for c in candidates if c.derivation_rank == top_rank]
    superseded = [c for c in candidates if c.derivation_rank != top_rank]
    if len(winners) > 1:
        refs = ", ".join(sorted(winner.record_ref for winner in winners))
        raise SiblingSelectionError(
            "ambiguous_sibling_derivation",
            subject_key,
            f"distinct records tie on derivation_rank {top_rank} within anchor {anchor!r}: {refs}",
        )
    return winners[0], superseded


def _apply_capture_recency(
    subject_key: str, winners: list[SiblingCandidate]
) -> tuple[SiblingCandidate, list[SiblingCandidate]]:
    if len(winners) == 1:
        return winners[0], []
    missing = sorted(w.record_ref for w in winners if w.capture_instant_or_none is None)
    if missing:
        raise SiblingSelectionError(
            "unorderable_capture_recency",
            subject_key,
            f"{len(winners)} candidates need capture-recency ordering but these carry "
            f"no capture instant: {missing}",
        )
    newest = max(w.capture_instant_or_none for w in winners)
    at_newest = [w for w in winners if w.capture_instant_or_none == newest]
    if len(at_newest) > 1:
        refs = ", ".join(sorted(candidate.record_ref for candidate in at_newest))
        raise SiblingSelectionError(
            "unorderable_capture_recency",
            subject_key,
            f"distinct records tie on capture instant {newest.isoformat()}: {refs}",
        )
    selected = at_newest[0]
    return selected, [w for w in winners if w is not selected]


__all__ = [
    "SelectedSibling",
    "SiblingCandidate",
    "SiblingSelectionError",
    "parse_capture_instant",
    "select_current_record_per_subject",
]
