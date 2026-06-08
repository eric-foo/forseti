"""Signal Content Record (v0) -- the second derived-record kind: content.

Parallel to the ECR integrity postures (``ecr/``); see
``docs/product/core_spine_v0_signal_content_record_architecture_v0.md``.
Data model only -- no deriver, no persistence, no EvidenceUnit binding.
"""
from __future__ import annotations

from signal_content.models import (
    SIGNAL_CONTENT_MANIFEST_VERSION,
    ContentReferences,
    DecisionRelevance,
    Delta,
    FamilyDetailBase,
    Reaction,
    SignalContentRecord,
    SignalEventTimeField,
    SignalEventTimeReference,
    SignalFamily,
)

__all__ = [
    "SIGNAL_CONTENT_MANIFEST_VERSION",
    "ContentReferences",
    "DecisionRelevance",
    "Delta",
    "FamilyDetailBase",
    "Reaction",
    "SignalContentRecord",
    "SignalEventTimeField",
    "SignalEventTimeReference",
    "SignalFamily",
]
