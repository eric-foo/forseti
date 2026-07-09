"""ECR (Evidence Candidate Record) source-side package.

Realizes source-side rows of the ECR field schema ratified at 387b630
(``docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md``), one pure
deriver per row:

- SP-3 (pre-decision timing/cutoff): ``EcrTimingPosture`` +
  ``derive_timing_postures`` (per-slice; M1 carry of the producer's closed
  ``cutoff_posture``).
- SP-2 (inspectability): ``EcrInspectabilityPosture`` +
  ``derive_inspectability_postures`` (per-slice; M2 derived-read over the
  M1-carried ``PreservedFile.sha256`` integrity anchor and the slice locator).
- SP-1 (source identity): ``EcrIdentityPosture`` + ``derive_identity_postures``
  (per-packet; M2 derived-read with an M3 stop over ``source_family`` /
  ``source_surface`` / ``source_locator``).
- SP-6 (source visibility): ``EcrSourceVisibilityPosture`` +
  ``derive_source_visibility_postures`` (per-packet, flat; M2 derived-read of the
  ratified residual-first table over ``archive_history_posture`` + the archive
  slice's ``cutoff_posture`` class + current-body presence). The archive-date
  class ``D`` binds to ``cutoff_posture``-as-class per the 641cf15 amendment
  (recorded inline at the boundary doc's Direction Change Propagation); the
  corroborated tier and the immutable/official ``not_applicable`` clear are
  declared-but-dormant (D2/M and the row-1 X condition are deferred).

Each subpredicate sits at its true grain (SP-1 / SP-6 per-packet; SP-2/SP-3
per-slice), performs no I/O, mutates no input, binds no ``EvidenceUnit``, and
makes no JSG-01, scoring, or readiness claim.

Authorization provenance: each slice is built under explicit owner current-turn
authorization (a ``/fused`` implementation turn; option A of the ECR-gate
decision) -- SP-3, SP-2, SP-1, and SP-6 are authorized. ECR is a separately-gated
boundary (``.agents/workflow-overlay/safety-rules.md``): any packet->EvidenceUnit
binding, the SP-5 finalizer, Cleaning, Judgment, and commits/pushes each require
their own separate authorization. JSG-01 stays FROZEN.

There is no ``cutoff_posture -> pre_decision_status`` mapping or reconciliation
layer here: SP-3 and SP-4 are distinct conductor subpredicates, so the ECR is a
parallel record the frozen conductor reads, not a projection into EvidenceUnit.
"""
from ecr.deriver import (
    derive_identity_postures,
    derive_inspectability_postures,
    derive_source_visibility_postures,
    derive_timing_postures,
)
from ecr.models import (
    EcrIdentityPosture,
    EcrInspectabilityPosture,
    EcrSourceVisibilityPosture,
    EcrTimingPosture,
    EcrTimingResidual,
    IdentityState,
    InspectabilityState,
    SourceVisibilityResidual,
    SourceVisibilityValue,
)

__all__ = [
    "EcrIdentityPosture",
    "EcrInspectabilityPosture",
    "EcrSourceVisibilityPosture",
    "EcrTimingPosture",
    "EcrTimingResidual",
    "IdentityState",
    "InspectabilityState",
    "SourceVisibilityResidual",
    "SourceVisibilityValue",
    "derive_identity_postures",
    "derive_inspectability_postures",
    "derive_source_visibility_postures",
    "derive_timing_postures",
]
