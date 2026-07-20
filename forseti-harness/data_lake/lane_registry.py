"""Single source of truth for Data Lake derived-lane roles.

Every derived lane a producer writes has a ROLE here. This is the map the
no-blur write-path guard reads (``.agents/hooks/check_silver_lane_registry.py``):
the guard rejects a ``silver``-named lane that is not declared, and a raw write
to a ``silver_envelope`` lane that bypasses the validating front-door.

Declarative on purpose: this module imports no producer code (it sits in the
base ``data_lake`` layer), so the guard can load it standalone without pulling
the harness or risking an import cycle. Lane string VALUES are mirrored from the
producers' own constants; the guard enforces that mirror (a written silver lane
that is absent here fails CI), so the two cannot silently drift.

Two grammars, declared honestly:

- ``silver_envelope``: the ``silver_vault_record_v0`` record envelope
  (``record_kind``/``payload_kind``/``payload.observation``). The validating
  front-door ``data_lake.silver_record.append_silver_record`` is the only
  sanctioned writer.
- ``silver_lineage``: the remaining pre-existing grammar-B capture lanes.  The
  migrated product/audience lanes are ``retired_silver_lineage``: their bytes
  remain audit-readable, but current readers and writers never select them.

``FRONT_DOOR_PENDING`` records ``silver_envelope`` lanes whose producer has not
yet been migrated onto the front-door, each with the reason. The guard permits a
raw write to a pending lane (a named, justified baseline -- not a silent
exception); a NEW envelope lane is not allowed here and must use the front-door.
"""
from __future__ import annotations

from enum import Enum


class LaneRole(str, Enum):
    SILVER_ENVELOPE = "silver_envelope"
    SILVER_LINEAGE = "silver_lineage"
    RETIRED_SILVER_LINEAGE = "retired_silver_lineage"
    RETIRED_LANE = "retired_lane"
    DECISION_EVIDENCE_RECEIPT = "decision_evidence_receipt"
    ANALYTIC_PROFILE = "analytic_profile"
    COMPLETION_MARKER = "completion_marker"
    CLEANING_AUDIT = "cleaning_audit"
    PROJECTION = "projection"
    RETIRED_CAPTURE_PROJECTION = "retired_capture_projection"
    ECR = "ecr"
    SIGNAL_CONTENT = "signal_content"
    TRANSCRIPT_CAPTURE = "transcript_capture"


# The one sanctioned writer for silver_envelope lanes (named so the guard can
# exempt it and point a violator at it).
SILVER_ENVELOPE_FRONT_DOOR_MODULE = "forseti-harness/data_lake/silver_record.py"
SILVER_ENVELOPE_FRONT_DOOR_FUNC = "append_silver_record"


LANE_ROLES: dict[str, LaneRole] = {
    # --- silver_envelope: silver_vault_record_v0; validating front-door required
    "cleaning_basenotes_silver": LaneRole.SILVER_ENVELOPE,
    "cleaning_fragrantica_silver": LaneRole.SILVER_ENVELOPE,
    "cleaning_parfumo_silver": LaneRole.SILVER_ENVELOPE,
    "creator_metric_silver": LaneRole.SILVER_ENVELOPE,
    "creator_metric_rollup_silver": LaneRole.SILVER_ENVELOPE,
    "company_surface_silver": LaneRole.SILVER_ENVELOPE,
    "social_metric_observation_set_silver": LaneRole.SILVER_ENVELOPE,
    "tiktok_comment_attention_silver": LaneRole.SILVER_ENVELOPE,
    "transcript_product_mentions_silver": LaneRole.SILVER_ENVELOPE,
    "raw_packet_tombstone_silver": LaneRole.SILVER_ENVELOPE,
    "transcript_product_mentions_completion": LaneRole.COMPLETION_MARKER,
    "retail_pdp_silver": LaneRole.SILVER_ENVELOPE,
    "silver__capture__audience_comments": LaneRole.SILVER_ENVELOPE,
    "silver__capture__reel_transcript": LaneRole.SILVER_ENVELOPE,
    "silver__capture__reel_deep_capture__set": LaneRole.COMPLETION_MARKER,
    "creator_audience_evidence_assembly_receipt": LaneRole.DECISION_EVIDENCE_RECEIPT,
    # --- retired audience inference lanes: names reserved; never current authority
    "tiktok_audience_evidence_silver": LaneRole.RETIRED_SILVER_LINEAGE,
    "tiktok_audience_evidence_completion": LaneRole.RETIRED_LANE,
    "tiktok_audience_profile_analysis": LaneRole.RETIRED_LANE,
    "tiktok_audience_profile_analysis_completion": LaneRole.RETIRED_LANE,
    # --- retired grammar-B cleaning lanes: history preserved, never current authority
    "silver__cleaning__product_mentions": LaneRole.RETIRED_SILVER_LINEAGE,
    "silver__cleaning__product_mentions__set": LaneRole.RETIRED_SILVER_LINEAGE,
    "silver__cleaning__tiktok_audience_evidence": LaneRole.RETIRED_SILVER_LINEAGE,
    "silver__cleaning__tiktok_audience_evidence__set": LaneRole.RETIRED_SILVER_LINEAGE,
    "silver__cleaning__tiktok_audience_profile": LaneRole.RETIRED_SILVER_LINEAGE,
    "silver__cleaning__tiktok_audience_profile__set": LaneRole.RETIRED_SILVER_LINEAGE,
    # --- cleaning audit pack (processing evidence; no record_kind)
    "cleaning_basenotes_audit": LaneRole.CLEANING_AUDIT,
    "cleaning_fragrantica_audit": LaneRole.CLEANING_AUDIT,
    "cleaning_parfumo_audit": LaneRole.CLEANING_AUDIT,
    # --- historical capture projections: readable, never current writer targets
    "projection_basenotes": LaneRole.RETIRED_CAPTURE_PROJECTION,
    "projection_fragrantica": LaneRole.RETIRED_CAPTURE_PROJECTION,
    "projection_parfumo": LaneRole.RETIRED_CAPTURE_PROJECTION,
    "projection_retail_pdp": LaneRole.RETIRED_CAPTURE_PROJECTION,
    "projection_fragrance_review": LaneRole.PROJECTION,
    # --- analytical projections (aggregation/observation, not capture retention)
    "projection_ig": LaneRole.PROJECTION,
    "projection_ig_reels_grid": LaneRole.PROJECTION,
    # --- ECR source-side epistemic postures (+ completion marker)
    "ecr_timing": LaneRole.ECR,
    "ecr_inspectability": LaneRole.ECR,
    "ecr_identity": LaneRole.ECR,
    "ecr_source_visibility": LaneRole.ECR,
    "ecr_set": LaneRole.ECR,
    # --- signal content records
    "signal_content": LaneRole.SIGNAL_CONTENT,
    # --- ASR transcript derived records (+ completion marker)
    "transcript_asr": LaneRole.TRANSCRIPT_CAPTURE,
    "transcript_asr__set": LaneRole.TRANSCRIPT_CAPTURE,
}


# silver_envelope lanes whose producer still writes through the raw lake writer
# rather than the validating front-door. A NAMED, justified baseline read by the
# guard -- each entry must state why, and is a migration target, not a permanent
# exception. EMPTY as of Batch 3: the IG + YouTube creator-metric producers were
# migrated onto the validating front-door (append_silver_record) once the metric
# posture-reason contract was reconciled, so no silver_envelope lane is exempt. A new
# silver_envelope lane must NOT be added here; it must use the front-door from the start.
FRONT_DOOR_PENDING: dict[str, str] = {}


# The exact, frozen set of lanes FRONT_DOOR_PENDING is allowed to contain. The guard
# fails if FRONT_DOOR_PENDING drifts from this baseline, so a NEW silver_envelope bypass
# cannot be silently grandfathered -- adding one requires a deliberate, reviewed edit
# here. Empty since the Batch-3 creator-metric migration; when a NEW migration target
# genuinely needs a temporary raw-write window, add the lane to both this baseline and
# FRONT_DOOR_PENDING together, and remove it from both when the migration lands.
FRONT_DOOR_PENDING_BASELINE: frozenset[str] = frozenset()


# Exact legacy grammar-B set accepted before the Silver/Vault envelope became the
# only route for new Silver Authority lanes. Equality is deliberate: a migration
# may shrink this set only through a reviewed edit that changes both the registry
# and this baseline; expanding it silently is forbidden.
SILVER_LINEAGE_LEGACY_BASELINE: frozenset[str] = frozenset()

RETIRED_SILVER_LINEAGE_BASELINE: frozenset[str] = frozenset(
    {
        "silver__cleaning__product_mentions",
        "silver__cleaning__product_mentions__set",
        "silver__cleaning__tiktok_audience_evidence",
        "silver__cleaning__tiktok_audience_evidence__set",
        "silver__cleaning__tiktok_audience_profile",
        "silver__cleaning__tiktok_audience_profile__set",
        "tiktok_audience_evidence_silver",
    }
)

RETIRED_LANE_BASELINE: frozenset[str] = frozenset(
    {
        "tiktok_audience_evidence_completion",
        "tiktok_audience_profile_analysis",
        "tiktok_audience_profile_analysis_completion",
    }
)

RETIRED_CAPTURE_PROJECTION_BASELINE: frozenset[str] = frozenset(
    {
        "projection_basenotes",
        "projection_fragrantica",
        "projection_parfumo",
        "projection_retail_pdp",
    }
)


def validate_registry() -> list[str]:
    """Registry invariants the no-blur guard enforces before scanning: the
    FRONT_DOOR_PENDING allowlist has not drifted from its named baseline, and
    every pending lane is a real silver_envelope lane carrying a migration
    reason. Returns a list of human-readable violation messages (empty = valid)."""
    errors: list[str] = []
    pending = set(FRONT_DOOR_PENDING)
    baseline = set(FRONT_DOOR_PENDING_BASELINE)
    if pending != baseline:
        errors.append(
            "FRONT_DOOR_PENDING drifted from FRONT_DOOR_PENDING_BASELINE "
            f"(added={sorted(pending - baseline)!r}, removed={sorted(baseline - pending)!r}); "
            "a new silver_envelope lane must use the front-door, not be grandfathered here. "
            "Update the baseline deliberately only when a migration genuinely lands."
        )
    for lane, reason in FRONT_DOOR_PENDING.items():
        if LANE_ROLES.get(lane) is not LaneRole.SILVER_ENVELOPE:
            errors.append(f"FRONT_DOOR_PENDING lane {lane!r} is not declared as silver_envelope.")
        if not reason.strip():
            errors.append(f"FRONT_DOOR_PENDING lane {lane!r} has no migration reason.")
    lineage_lanes = {
        lane for lane, role in LANE_ROLES.items() if role is LaneRole.SILVER_LINEAGE
    }
    lineage_baseline = set(SILVER_LINEAGE_LEGACY_BASELINE)
    if lineage_lanes != lineage_baseline:
        errors.append(
            "SILVER_LINEAGE lanes drifted from SILVER_LINEAGE_LEGACY_BASELINE "
            f"(added={sorted(lineage_lanes - lineage_baseline)!r}, "
            f"removed={sorted(lineage_baseline - lineage_lanes)!r}); new Silver Authority "
            "lanes must use the silver_vault_record_v0 envelope front door. A deliberate "
            "legacy migration may shrink the baseline only with its migration evidence."
        )
    retired_lanes = {
        lane for lane, role in LANE_ROLES.items() if role is LaneRole.RETIRED_SILVER_LINEAGE
    }
    if retired_lanes != set(RETIRED_SILVER_LINEAGE_BASELINE):
        errors.append(
            "RETIRED_SILVER_LINEAGE lanes drifted from their historical baseline "
            f"(added={sorted(retired_lanes - set(RETIRED_SILVER_LINEAGE_BASELINE))!r}, "
            f"removed={sorted(set(RETIRED_SILVER_LINEAGE_BASELINE) - retired_lanes)!r}); "
            "historical lanes remain audit-readable but must never regain current-reader authority."
        )
    retired_general = {
        lane for lane, role in LANE_ROLES.items() if role is LaneRole.RETIRED_LANE
    }
    if retired_general != set(RETIRED_LANE_BASELINE):
        errors.append(
            "RETIRED_LANE entries drifted from their historical baseline "
            f"(added={sorted(retired_general - set(RETIRED_LANE_BASELINE))!r}, "
            f"removed={sorted(set(RETIRED_LANE_BASELINE) - retired_general)!r}); "
            "retired lane names remain reserved and must not regain current-reader authority."
        )
    retired_capture_projection = {
        lane
        for lane, role in LANE_ROLES.items()
        if role is LaneRole.RETIRED_CAPTURE_PROJECTION
    }
    if retired_capture_projection != set(RETIRED_CAPTURE_PROJECTION_BASELINE):
        errors.append(
            "RETIRED_CAPTURE_PROJECTION entries drifted from their historical baseline "
            f"(added={sorted(retired_capture_projection - set(RETIRED_CAPTURE_PROJECTION_BASELINE))!r}, "
            f"removed={sorted(set(RETIRED_CAPTURE_PROJECTION_BASELINE) - retired_capture_projection)!r}); "
            "historical capture Projection lanes remain readable but never regain writer authority."
        )
    return errors


SILVER_ENVELOPE_LANES = frozenset(
    lane for lane, role in LANE_ROLES.items() if role is LaneRole.SILVER_ENVELOPE
)
SILVER_LINEAGE_LANES = frozenset(
    lane for lane, role in LANE_ROLES.items() if role is LaneRole.SILVER_LINEAGE
)
SILVER_LANES = frozenset(
    lane
    for lane, role in LANE_ROLES.items()
    if role in (LaneRole.SILVER_ENVELOPE, LaneRole.SILVER_LINEAGE, LaneRole.RETIRED_SILVER_LINEAGE)
)


def role_of(lane: str) -> LaneRole | None:
    """Return the declared role of ``lane``, or ``None`` if undeclared."""
    return LANE_ROLES.get(lane)


def is_silver_named(lane: str) -> bool:
    """The naming convention every silver lane follows (``*_silver`` /
    ``silver__*``). The guard uses this to decide an undeclared lane is a silver
    lane that should have been registered, without resolving its role first."""
    return "silver" in lane


__all__ = [
    "LaneRole",
    "LANE_ROLES",
    "FRONT_DOOR_PENDING",
    "FRONT_DOOR_PENDING_BASELINE",
    "SILVER_LINEAGE_LEGACY_BASELINE",
    "RETIRED_SILVER_LINEAGE_BASELINE",
    "RETIRED_CAPTURE_PROJECTION_BASELINE",
    "SILVER_ENVELOPE_LANES",
    "SILVER_LINEAGE_LANES",
    "SILVER_LANES",
    "SILVER_ENVELOPE_FRONT_DOOR_MODULE",
    "SILVER_ENVELOPE_FRONT_DOOR_FUNC",
    "validate_registry",
    "role_of",
    "is_silver_named",
]
