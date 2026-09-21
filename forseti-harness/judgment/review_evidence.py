"""Lossless prompt rendering and bounded answer-review mechanics.

Transport references never replace source identities or confer corroboration.
Stored source/answer artifacts keep their ordinary, complete schemas.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import re


RENDERING_GUIDANCE = (
    "The JSON uses lossless review_evidence_v1 transport. Resolve {$text: ID} from texts and "
    "{$value: ID} from values (which can themselves contain references); "
    "a {$table: {defaults, columns, rows}} is a list of records: copy named defaults into each "
    "record and map row values to columns in order. {$literal: OBJECT} escapes a literal object. "
    "All fields and list order are preserved. Transport references are NOT source identities: "
    "keep each evidence ID, independent origin, support/opposition relation and source condition separate. "
    "Finding conditions/scope_conditions are the UNION of child conditions, including opposing sources; "
    "condition_lineage binds conditions to individual semantic units. Do not attribute the union to "
    "every source or delete legitimate opposing conditions. Use per-source lineage and relations to judge meaning. "
    "Read the whole source context: ordinary context-supported interpretation is permitted; absence of identical "
    "literal words is not by itself a defect. Criticism must identify an unsupported change in meaning and its "
    "concrete effect, not merely different phrasing or a more precise possible citation. "
)


def compact_evidence(value):
    """Factor repeated text and common record fields without selecting evidence."""
    counts = Counter()
    structures = Counter()

    def signature(node):
        return json.dumps(node, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    def count(node):
        if isinstance(node, (list, dict)):
            key = signature(node)
            if len(key) >= 120:
                structures[key] += 1
        if isinstance(node, str) and len(node) >= 120:
            counts[node] += 1
        elif isinstance(node, dict):
            for child in node.values():
                count(child)
        elif isinstance(node, list):
            for child in node:
                count(child)

    count(value)
    identities = {s: "t" + hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]
                  for s, n in counts.items() if n > 1}
    texts = {ref: s for s, ref in identities.items()}
    if len(texts) != len(identities):
        raise ValueError("compact evidence text identity collision")
    shared = {s: "v" + hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]
              for s, n in structures.items() if n > 1}
    if len(set(shared.values())) != len(shared):
        raise ValueError("compact evidence value identity collision")
    values = {}
    used_texts = set()

    def encode(node, *, inline=False):
        if isinstance(node, str):
            if node in identities:
                used_texts.add(identities[node])
                return {"$text": identities[node]}
            return node
        if not inline and isinstance(node, (list, dict)):
            key = signature(node)
            if key in shared:
                ref = shared[key]
                if ref not in values:
                    values[ref] = encode(node, inline=True)
                return {"$value": ref}
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

    data = encode(value)
    result = {"format": "review_evidence_v1", "texts": {r: texts[r] for r in sorted(used_texts)},
              "values": values, "data": data}
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
        if set(node) == {"$value"}:
            return decode(packet["values"][node["$value"]])
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
    material = [f for f in findings if f["status"] == "open" and f["severity"] in {"blocker", "major"}]
    if for_correction:
        # Routing a material repair still requires an explicit current question.
        return [f for f in material if f["introduced_at"] in {"current_answer", "frozen_upstream"}
                and any(r.startswith("current_answer:") for r in f["artifact_refs"])]
    # Reporting must not erase a current/uncertain defect because its locator
    # differs from the routing syntax. Inventory-only findings remain separate.
    answer_fields = {"current_answer", "corrected_answer", "corrected_affected_answers", "original_affected_answers"}
    return [f for f in material if f["introduced_at"] in {"current_answer", "uncertain"}
            or any(re.split(r"[:.\[]", r, maxsplit=1)[0] in answer_fields for r in f["artifact_refs"])]


def compose_answer_patch(original, patch, affected):
    replacements = {a["question_id"]: a for a in patch["answers"]}
    if len(replacements) != len(patch["answers"]) or set(replacements) != set(affected):
        raise ValueError("answer patch must replace exactly the affected questions")
    return {**original, "answers": [deepcopy(replacements.get(a["question_id"], a))
                                    for a in original["answers"]]}


def answer_identity(answer):
    return hashlib.sha256(json.dumps(answer, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def apply_exact_answer_repairs(original, repairs, nominations, known_refs, reference_errors=None, *, unit_sources=None,
                              allow_retained=False):
    """Apply reviewer-authored text only. Applicability is not semantic acceptance."""
    if repairs["answer_sha256"] != answer_identity(original):
        raise ValueError("exact repairs have a stale frozen answer identity")
    rows = {row["question_id"]: row for row in original["answers"]}
    reference_errors = reference_errors or {}
    unit_sources = unit_sources or {}
    def source_ids(refs):
        return {unit_sources.get(ref, ref) for ref in refs}
    scope = {}
    for finding in material_answer_findings(nominations):
        for ref in finding["artifact_refs"]:
            if ref.startswith("current_answer:"):
                scope.setdefault(ref.removeprefix("current_answer:"), set()).update(finding["source_refs"])
    if scope.keys() - rows.keys():
        raise ValueError("exact repair nomination has unknown answer scope")
    edits_by_field = {}
    added_refs = {}
    for edit in repairs["edits"]:
        question, field = edit["question_id"], edit["field"]
        if question not in rows or question not in scope.keys() | reference_errors.keys() or field not in {"answer", "limits", "evidence_refs"}:
            raise ValueError("exact repair is outside nominated answer scope")
        refs = set(edit["source_refs"])
        before, after = edit["before"], edit["after"]
        citation_repair = before in reference_errors.get(question, []) and after in known_refs and edit["source_refs"] == [after]
        nominated_sources = source_ids(scope.get(question, set()))
        original_refs = answer_source_references(rows[question], known_refs)
        repair_sources = source_ids(refs)
        # A focused repair can retain cited context without nominating that
        # unchanged context as a defect. It still needs a material repair source.
        if not refs or refs - known_refs or (not citation_repair and (
                not repair_sources & nominated_sources or repair_sources - nominated_sources - source_ids(original_refs))):
            raise ValueError("exact repair sources are outside nominated source scope")
        if field == "evidence_refs":
            if not citation_repair or rows[question][field].count(before) != 1:
                raise ValueError("exact citation repair must replace one observed invalid reference")
            start = rows[question][field].index(before)
            group = edits_by_field.setdefault((question, field), [])
            if any(old_start == start for old_start, _, _ in group):
                raise ValueError("exact repair anchors overlap")
            group.append((start, start + 1, after))
            added_refs.setdefault(question, set()).update(refs)
            continue
        text = rows[question][field]
        start = text.find(before)
        if not before or start < 0 or text.find(before, start + 1) >= 0:
            raise ValueError("exact repair anchor is missing or ambiguous")
        if before == after:
            raise ValueError("exact repair has no text change")
        introduced = answer_source_references({"answer": after, "evidence_refs": []}, known_refs)
        if introduced - original_refs - refs:
            raise ValueError("exact repair introduces a citation outside its source refs")
        end = start + len(before)
        group = edits_by_field.setdefault((question, field), [])
        if any(start < old_end and old_start < end for old_start, old_end, _ in group):
            raise ValueError("exact repair anchors overlap")
        group.append((start, end, after))
        added_refs.setdefault(question, set()).update(refs)
    expected = scope.keys() | reference_errors.keys()
    required = reference_errors.keys() if allow_retained else expected
    # A valid edit may resolve a finding spanning multiple answer sections.
    # Retention never clears a nomination: the caller must recheck all of them.
    if required - added_refs.keys() or (expected and not added_refs):
        raise ValueError("exact repairs omit a nominated answer")
    corrected = deepcopy(original)
    for row in corrected["answers"]:
        question = row["question_id"]
        for field in ("answer", "limits"):
            for start, end, after in sorted(edits_by_field.get((question, field), []), reverse=True):
                row[field] = row[field][:start] + after + row[field][end:]
        for start, _, after in edits_by_field.get((question, "evidence_refs"), []):
            row["evidence_refs"][start] = after
        row["evidence_refs"].extend(sorted(added_refs.get(question, set()) - set(row["evidence_refs"])))
    return corrected


def answer_source_references(row, known):
    """Include inline references in the supplied source namespaces, not just the index.

    Ordinary prose and URLs are not interpreted as source citations. Namespaces
    come from the actual evidence identities; no product/source-specific rules.
    """
    refs = set(row["evidence_refs"])
    namespaces = sorted({r.split(":", 1)[0] for r in known if ":" in r})
    if namespaces:
        pattern = r"(?<![\w:])(?:" + "|".join(map(re.escape, namespaces)) + r"):[\w:.-]+"
        for field in ("answer", "limits"):
            refs.update(m.rstrip(".:,") for m in re.findall(pattern, row.get(field, "")))
    return refs


def correction_selection(original, candidate, assessment, recheck, request=None):
    """Shared live/closeout decision; selection with residuals never means approval.

    Old responses retain the old clean-only selection rule. New comparison
    authority is usable only with its exact bound request and source evidence.
    """
    remaining = recheck_answer_findings(recheck)
    failed = [c for c in recheck["check_results"]
              if c["status"] in {"fail", "uncertain"} and c["scope"] != "upstream_only"]
    accepted = not remaining and not failed
    comparison = recheck.get("answer_comparison")
    if recheck.get("schema_version") == "finite_source_assessment_v4" and comparison is not None:
        verified = verified_answer_improvement(original, candidate, assessment, recheck, request)
        accepted = verified
    outside = [f for f in material_answer_findings(assessment["material_findings"], for_correction=False)
               if f not in material_answer_findings(assessment["material_findings"])]
    unresolved = remaining or failed or (outside and recheck.get("schema_version") == "finite_source_assessment_v4")
    status = ("rejected" if not accepted else "original_retained" if candidate == original
              else "selected_requires_adjudication" if unresolved else "accepted")
    result = {"answer_correction_status": status, "answer_correction_failed_checks": failed}
    result.update(correction_material_status(assessment, status, recheck))
    return result


def correction_material_status(assessment, correction_status, recheck=None):
    original = material_answer_findings(assessment["material_findings"], for_correction=False)
    selected = correction_status in {"accepted", "original_retained", "selected_requires_adjudication"}
    remaining = original
    if selected:
        nominations = material_answer_findings(assessment["material_findings"])
        remaining = [f for f in original if f not in nominations]
        if recheck is not None:
            remaining += [f for f in recheck_answer_findings(recheck)
                          if f not in remaining]
    status = ("correction_rejected_original_requires_adjudication" if correction_status == "rejected"
              else "selected_answer_requires_adjudication" if correction_status == "selected_requires_adjudication"
              else "material_defects_remain" if remaining else "no_open_material_answer_defects_reported")
    return {"remaining_material_answer_findings": remaining, "answer_material_status": status}


def recheck_answer_findings(recheck):
    findings = material_answer_findings(recheck["material_findings"], for_correction=False)
    if recheck.get("schema_version") == "finite_source_assessment_v4":
        # Historical origin is never evidence that an open answer defect vanished.
        findings = [f for f in recheck["material_findings"] if f in findings or (
            f["introduced_at"] == "historical_answer" and f["status"] == "open"
            and f["severity"] in {"major", "blocker"})]
    return findings


def verified_answer_improvement(original, candidate, assessment, recheck, request):
    """Check identity/coverage of source-backed comparison, not semantic truth by code."""
    comparison = recheck["answer_comparison"]
    if not request or not assessment or original == candidate:
        return False
    nominations = material_answer_findings(assessment["material_findings"])
    repairs = assessment.get("answer_repairs", {}).get("edits", [])
    affected = [q["id"] for q in request["affected_questions"]]
    before = {a["question_id"]: a for a in original["answers"]}
    after = {a["question_id"]: a for a in candidate["answers"]}
    if (comparison["original_answer_sha256"] != answer_identity(original)
            or comparison["candidate_answer_sha256"] != answer_identity(candidate)
            or comparison["affected_question_ids"] != affected
            or comparison["changed_claims_verdict"] != "no_new_or_worsened_material_defect"
            or request["original_affected_answers"] != [a for a in original["answers"] if a["question_id"] in affected]
            or request["corrected_affected_answers"] != [a for a in candidate["answers"] if a["question_id"] in affected]
            or request["nominations_to_verify_against_sources"] != nominations
            or request["exact_repairs"] != assessment.get("answer_repairs")
            or before.keys() != after.keys()
            or any(a != after[q] for q, a in before.items() if q not in affected)):
        return False
    sources = {r["evidence_id"]: r for r in request["complete_relevant_source_rows"]}
    units = {u["semantic_unit_ref"]: u["evidence_id"] for u in request["verified_units"]}

    def supported(row):
        refs = row["source_refs"]
        observations = row["source_observations"]
        return bool(refs and row["explanation"].strip()
                    and all(units.get(ref, ref) in sources for ref in refs)
                    and {o["source_ref"] for o in observations} == set(refs)
                    and all(o["excerpt"].strip() and o["excerpt"] in sources[units.get(o["source_ref"], o["source_ref"])].get("text", "")
                            for o in observations))

    repair_checks = comparison["repair_checks"]
    if (not repairs or sorted(r["edit_index"] for r in repair_checks) != list(range(len(repairs)))
            or any(r["verdict"] != "verified" or not supported(r)
                   or not set(repairs[r["edit_index"]]["source_refs"]).issubset(r["source_refs"])
                   for r in repair_checks)):
        return False
    residuals = recheck_answer_findings(recheck)
    expected = [i for i, f in enumerate(recheck["material_findings"]) if f in residuals]
    records = comparison["residual_checks"]
    if sorted(r["finding_index"] for r in records) != expected:
        return False
    for row in records:
        q, field = row["question_id"], row["field"]
        finding = recheck["material_findings"][row["finding_index"]]
        excerpt = row["original_excerpt"]
        if (row["verdict"] != "unchanged_preexisting" or q not in affected or not supported(row)
                or not excerpt.strip() or excerpt != row["candidate_excerpt"]
                or excerpt not in before[q][field] or excerpt not in after[q][field]
                or not set(finding["source_refs"]).issubset(row["source_refs"])
                or not set(before[q]["evidence_refs"]).issubset(after[q]["evidence_refs"])):
            return False
    nomination_checks = comparison["nomination_checks"]
    if sorted(r["nomination_index"] for r in nomination_checks) != list(range(len(nominations))):
        return False
    for row in nomination_checks:
        linked = row["remaining_finding_indices"]
        if (not supported(row) or not set(nominations[row["nomination_index"]]["source_refs"]).issubset(row["source_refs"])
                or row["disposition"] == "uncertain"
                or (row["disposition"] == "remaining" and (not linked or not set(linked).issubset(expected)))
                or (row["disposition"] != "remaining" and linked)):
            return False
    failed = [c for c in recheck["check_results"]
              if c["status"] in {"fail", "uncertain"} and c["scope"] != "upstream_only"]
    links = comparison["failed_check_links"]
    if sorted(r["check_id"] for r in links) != sorted(c["check_id"] for c in failed):
        return False
    if any(c["scope"] != "answer" or c["status"] != "fail" for c in failed):
        return False
    for link in links:
        if not link["finding_indices"] or not set(link["finding_indices"]).issubset(expected):
            return False
        check = next(c for c in failed if c["check_id"] == link["check_id"])
        findings = [recheck["material_findings"][i] for i in link["finding_indices"]]
        aliases = {r for f in findings for r in f["artifact_refs"]}
        aliases.update(f"material_findings[{i}]" for i in link["finding_indices"])
        supporting_sources = {units.get(r, r) for f in findings for r in f["source_refs"]}
        if (set(check["finding_refs"]) - aliases
                or {units.get(r, r) for r in check["source_refs"]} - supporting_sources):
            return False
    return True
