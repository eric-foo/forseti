"""Signal Content Record (v0) -- the second derived-record kind: content.

Parallel to the ECR integrity postures (``ecr/``); see
``docs/product/core_spine_v0_signal_content_record_architecture_v0.md``.
Data model + the v0 carry-or-residualize deriver. No persistence, no
EvidenceUnit binding.
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
    SignalEventTimeStatus,
    SignalFamily,
)
from signal_content.deriver import derive_signal_content

__all__ = [
    "derive_signal_content",
    "SIGNAL_CONTENT_MANIFEST_VERSION",
    "ContentReferences",
    "DecisionRelevance",
    "Delta",
    "FamilyDetailBase",
    "Reaction",
    "SignalContentRecord",
    "SignalEventTimeField",
    "SignalEventTimeReference",
    "SignalEventTimeStatus",
    "SignalFamily",
]
