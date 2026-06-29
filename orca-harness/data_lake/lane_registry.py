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
- ``silver_lineage``: the SECOND, pre-existing silver grammar -- the
  ``silver_lineage`` kit plus a freeform payload (transcript/IG product mentions
  and the ``silver__capture__*`` set lanes). Batch 1 DECLARES it; it does not
  reshape those records onto the envelope. Reconciling the envelope and
  lineage-kit grammars is a high-lock-in fork deferred to a later batch,
  coordinated with PR #456.

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
    CLEANING_AUDIT = "cleaning_audit"
    PROJECTION = "projection"
    ECR = "ecr"
    SIGNAL_CONTENT = "signal_content"
    TRANSCRIPT_CAPTURE = "transcript_capture"


# The one sanctioned writer for silver_envelope lanes (named so the guard can
# exempt it and point a violator at it).
SILVER_ENVELOPE_FRONT_DOOR_MODULE = "orca-harness/data_lake/silver_record.py"
SILVER_ENVELOPE_FRONT_DOOR_FUNC = "append_silver_record"


LANE_ROLES: dict[str, LaneRole] = {
    # --- silver_envelope: silver_vault_record_v0; validating front-door required
    "cleaning_fragrantica_silver": LaneRole.SILVER_ENVELOPE,
    "creator_metric_silver": LaneRole.SILVER_ENVELOPE,
    "creator_metric_rollup_silver": LaneRole.SILVER_ENVELOPE,
    # --- silver_lineage: grammar B (lineage kit + freeform payload); declared,
    #     not reshaped. Reconcile with the envelope grammar later (see PR #456).
    "silver__cleaning__product_mentions": LaneRole.SILVER_LINEAGE,
    "silver__cleaning__product_mentions__set": LaneRole.SILVER_LINEAGE,
    "silver__capture__audience_comments": LaneRole.SILVER_LINEAGE,
    "silver__capture__reel_transcript": LaneRole.SILVER_LINEAGE,
    "silver__capture__reel_deep_capture__set": LaneRole.SILVER_LINEAGE,
    # --- cleaning audit pack (processing evidence; no record_kind)
    "cleaning_fragrantica_audit": LaneRole.CLEANING_AUDIT,
    # --- mechanical projections (explicitly not_cleaned / not_judgment_ready)
    "projection_fragrantica": LaneRole.PROJECTION,
    "projection_ig": LaneRole.PROJECTION,
    "projection_ig_reels_grid": LaneRole.PROJECTION,
    "projection_retail_pdp": LaneRole.PROJECTION,
    "projection_fragrance_review": LaneRole.PROJECTION,
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
# exception. A new silver_envelope lane must NOT be added here; it must use the
# front-door from the start.
FRONT_DOOR_PENDING: dict[str, str] = {
    "creator_metric_silver": (
        "the IG and YouTube creator-metric producers (silver_metric_producer.py, "
        "youtube_silver_metric_producer.py) write this lane raw; their non-observed "
        "MetricObservation encodes the reason in reason_detail, which the envelope front-door "
        "validator does not yet accept (it requires reason_code). Reconcile the posture-reason "
        "contract before migrating both onto the front-door (Batch 3; coordinate PR #456)."
    ),
    "creator_metric_rollup_silver": (
        "same two producers; migrate alongside creator_metric_silver once the posture-reason "
        "contract is reconciled (Batch 3)."
    ),
}


SILVER_ENVELOPE_LANES = frozenset(
    lane for lane, role in LANE_ROLES.items() if role is LaneRole.SILVER_ENVELOPE
)
SILVER_LANES = frozenset(
    lane
    for lane, role in LANE_ROLES.items()
    if role in (LaneRole.SILVER_ENVELOPE, LaneRole.SILVER_LINEAGE)
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
    "SILVER_ENVELOPE_LANES",
    "SILVER_LANES",
    "SILVER_ENVELOPE_FRONT_DOOR_MODULE",
    "SILVER_ENVELOPE_FRONT_DOOR_FUNC",
    "role_of",
    "is_silver_named",
]
