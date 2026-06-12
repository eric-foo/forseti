"""Append-only persistence for the Layer-2a observation log (company-aggregate, EDGAR).

The thin durable home for ``EdgarHeadcountObservation`` rows: a single append-only YAML-document
stream (one ``---`` document per observation) outside any packet directory. No DB, no overwrite --
re-captures and re-extractions are APPENDED as new rows; the projection (Layer 2b) collapses /
conflicts them on read. This is the persisted truth the computed-on-read projection folds; it is
NOT itself a canonical company record.

Reuses ``append_yaml_document`` / ``load_yaml_documents`` (the canonical dumper quotes date-like
scalars, so ISO dates round-trip as ``str``, not ``date``). The reader re-validates every row
against the current ``EdgarHeadcountObservation`` schema -- a corrupt or off-schema row fails
visibly rather than silently dropping.
"""
from __future__ import annotations

from pathlib import Path

from harness_utils import append_yaml_document, load_yaml_documents
from source_capture.company_aggregate.observation import EdgarHeadcountObservation


def append_observation(observation: EdgarHeadcountObservation, *, log_path: Path) -> None:
    """Append one observation as a new YAML document (append-only; never overwrites)."""
    append_yaml_document(log_path, observation.model_dump(mode="json"))


def read_observation_log(log_path: Path) -> list[EdgarHeadcountObservation]:
    """Read + re-validate every observation row. Missing file -> empty log."""
    documents = load_yaml_documents(log_path)
    return [EdgarHeadcountObservation.model_validate(document) for document in documents]
