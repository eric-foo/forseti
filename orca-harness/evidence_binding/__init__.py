"""JSG-01-scoped EvidenceUnit binding package (slice B of the bounded unfreeze build).

The minimal composition layer above the ECR source-side spine: binds, by key
(reference-never-merge), exactly what the JSG-01 predicate reads — the four
derived source-side postures (SP-1/2/3/6) and the current ``FinalizationReceipt``
read — onto one case-packet evidence unit.

Authorization provenance: built under the owner-ratified JSG-01-scoped
EvidenceUnit binding contract (boundary doc, dated 2026-06-12; design basis
``docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md``)
inside the bounded ECR CA unfreeze-build commission. The full ECR/Evidence Unit
field architecture, the canonical object name, D2, SP-4 value policing, and the
JSG-01 unfreeze remain reserved. JSG-01 stays FROZEN; this package computes no
aggregate verdict and clears no case.
"""
from evidence_binding.composer import Jsg01BindingError, compose_jsg01_evidence_record
from evidence_binding.models import (
    Jsg01EvidenceBinding,
    Jsg01EvidenceRecord,
    Jsg01FinalizationRead,
)

__all__ = [
    "Jsg01BindingError",
    "Jsg01EvidenceBinding",
    "Jsg01EvidenceRecord",
    "Jsg01FinalizationRead",
    "compose_jsg01_evidence_record",
]
