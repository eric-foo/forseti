"""Lossless prompt rendering and bounded answer-review mechanics.

Transport references never replace source identities or confer corroboration.
Stored source/answer artifacts keep their ordinary, complete schemas.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import json


RENDERING_GUIDANCE = (
    "The JSON uses lossless review_evidence_v1 transport. Resolve {$text: ID} from texts; "
    "a {$table: {defaults, columns, rows}} is a list of records: copy named defaults into each "
    "record and map row values to columns in order. {$literal: OBJECT} escapes a literal object. "
    "All fields and list order are preserved. Transport references are NOT source identities: "
    "keep each evidence ID, independent origin, support/opposition relation and source condition separate. "
    "Finding conditions/scope_conditions are the UNION of child conditions, including opposing sources; "
    "condition_lineage binds conditions to individual semantic units. Do not attribute the union to "
    "every source or delete legitimate opposing conditions. Use per-source lineage and relations to judge meaning. "
)


def compact_evidence(value):
    """Factor repeated text and common record fields without selecting evidence."""
    counts = Counter()

    def count(node):
        if isinstance(node, str) and len(node) >= 120:
            counts[node] += 1
        elif isinstance(node, dict):
            for child in node.values():
                count(child)
        elif isinstance(node, list):
            for child in node:
                count(child)

    count(value)
    identities = {s: "t" + hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]
                  for s, n in counts.items() if n > 1}
    texts = {ref: s for s, ref in identities.items()}
    if len(texts) != len(identities):
        raise ValueError("compact evidence text identity collision")

    def encode(node):
        if isinstance(node, str):
            return {"$text": identities[node]} if node in identities else node
        if isinstance(node, dict):
            result = {k: encode(v) for k, v in node.items()}
            return {"$literal": result} if any(k.startswith("$") for k in node) else result
        if isinstance(node, list):
            # Identical field sets avoid conflating a missing field with JSON null.
            if len(node) > 1 and all(isinstance(r, dict) for r in node) and all(
                    set(r) == set(node[0]) for r in node):
                defaults = {k: v for k, v in node[0].items() if all(
                    json.dumps(r[k], sort_keys=True) == json.dumps(v, sort_keys=True) for r in node[1:])}
                columns = sorted(set(node[0]) - set(defaults))
                return {"$table": {"defaults": {k: encode(v) for k, v in defaults.items()},
                    "columns": columns, "rows": [[encode(r[k]) for k in columns] for r in node]}}
            return [encode(v) for v in node]
        return node

    result = {"format": "review_evidence_v1", "texts": texts, "data": encode(value)}
    if json.dumps(expand_evidence(result), sort_keys=True) != json.dumps(value, sort_keys=True):
        raise ValueError("compact evidence failed complete field preservation")
    return result


def expand_evidence(packet):
    """Reconstruct the original JSON for verification and downstream consumers."""
    if packet["format"] != "review_evidence_v1":
        raise ValueError("unknown evidence rendering")

    def decode(node):
        if isinstance(node, list):
            return [decode(v) for v in node]
        if not isinstance(node, dict):
            return node
        if set(node) == {"$text"}:
            return packet["texts"][node["$text"]]
        if set(node) == {"$literal"}:
            return {k: decode(v) for k, v in node["$literal"].items()}
        if set(node) == {"$table"}:
            table = node["$table"]
            defaults = {k: decode(v) for k, v in table["defaults"].items()}
            return [{**deepcopy(defaults), **dict(zip(table["columns"], map(decode, row), strict=True))}
                    for row in table["rows"]]
        return {k: decode(v) for k, v in node.items()}

    return decode(packet["data"])


def render_evidence(value):
    return RENDERING_GUIDANCE + "\n\n" + json.dumps(
        compact_evidence(value), ensure_ascii=False, separators=(",", ":")) + "\n"


def material_answer_findings(findings, *, for_correction=True):
    """Consume existing reviewer judgments; do not introduce another triage call."""
    return [f for f in findings if f["status"] == "open" and f["severity"] in {"blocker", "major"}
            and (not for_correction or f["introduced_at"] in {"current_answer", "frozen_upstream"})
            and any(r.startswith("current_answer:") or (not for_correction and r.startswith("corrected_answer:"))
                    for r in f["artifact_refs"])]


def compose_answer_patch(original, patch, affected):
    replacements = {a["question_id"]: a for a in patch["answers"]}
    if len(replacements) != len(patch["answers"]) or set(replacements) != set(affected):
        raise ValueError("answer patch must replace exactly the affected questions")
    return {**original, "answers": [deepcopy(replacements.get(a["question_id"], a))
                                    for a in original["answers"]]}
