"""Bounded, complete-inventory consumption of an already verified normal view.

This is a provider-free continuation, not extraction or reconciliation. Requests
and accepted responses are immutable and addressed by their actual dependencies.
"""
from collections import Counter, defaultdict
import hashlib
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from judgment.review_evidence import render_evidence


METHOD = """Consume the supplied verified evidence for the commissioned questions.
Verification establishes extraction, not downstream relevance or correct judgment.
Preserve native finding IDs and relation ownership across slices. A slice is not a
complete finding or a representative sample. Preserve source roles, opposition,
conditions, uncertainty, intent versus observed action, mitigation, residuals,
and evidenced no-action. Never infer prevalence or causation from counts.
Source review: use original context to judge answer relevance and meaning, without
redoing extraction or consolidation. Account for EVERY supplied unit exactly once
in findings or unused. A finding can cite several units; do not collapse their
roles or transfer a source's conditions to another. Unused needs a concrete reason
why it cannot affect these questions; uncertain relevance belongs in a finding
with its limits, not unused. Preserve potentially material uncited observations.
Assembly: compare ALL supplied findings across batches for conflict, complement,
scope, and important omissions. Use unused reasons to challenge exclusions. Answer
from checked findings and limits; a pile of independent summaries is insufficient.
Answer review: independently test each answer and commissioned check against the
complete checked set, including contrary evidence and unused reasons. Upstream
verification is no proof of materiality. If a conflict, exclusion, or missing
context cannot be resolved from these records, request exact finding/unused handles in
reopen_refs. Do not pass unresolved meaning. Reopened originals supplement, never
replace, the complete checked set. Return only the required JSON.
"""


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(compact(value).encode()).hexdigest()


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique)


def retain(path, value):
    from runners.run_semantic_evidence_integration import _retain_advance_artifact
    path = Path(path)
    data = (compact(value) + "\n").encode()
    _retain_advance_artifact(path, data, raw=True)
    if path.read_bytes() != data:
        raise ValueError(f"consumer readback differs: {path}")


def obj(fields):
    return {"type": "object", "additionalProperties": False,
            "required": list(fields), "properties": fields}


TEXT = {"type": "string"}


def strings(choices=None):
    # Provider structured-output schemas reject uniqueItems and cap enum size.
    # Exact identity and uniqueness are enforced by the local consumer instead.
    return {"type": "array", "items": TEXT}


def response_schema(phase, payload):
    ids = payload["unit_ids"]
    qids = [q["id"] for q in payload["commission"]["questions"]]
    if phase in {"source_review", "reopen"}:
        finding = obj({"statement": TEXT, "question_ids": strings(qids),
            "supporting_refs": strings(ids), "opposing_refs": strings(ids),
            "context_refs": strings(ids), "limits": TEXT})
        return obj({"findings": {"type": "array", "items": finding},
            "unused": {"type": "array", "items": obj({"unit_ref": TEXT, "reason": TEXT})}})
    if phase == "assembly":
        return obj({"answers": {"type": "array", "items": obj({
            "question_id": {"type": "string", "enum": qids}, "answer": TEXT,
            "evidence_refs": strings(ids), "limits": TEXT})}})
    schema = obj({"answers": {"type": "array", "items": obj({
        "question_id": {"type": "string", "enum": qids},
        "status": {"type": "string", "enum": ["pass", "defect", "unresolved"]}, "reason": TEXT})},
        "checks": {"type": "array", "minItems": len(payload["checks"]), "maxItems": len(payload["checks"]),
            "items": obj({"check_id": TEXT if not payload["checks"] else {"type": "string", "enum": [c["id"] for c in payload["checks"]]},
            "status": {"type": "string", "enum": ["pass", "defect", "unresolved"]}, "reason": TEXT})},
        "material_findings": {"type": "array", "items": obj({"question_ids": strings(qids),
            "reason": TEXT, "evidence_refs": strings(ids)})},
        "reopen_refs": strings(ids)})
    if payload.get("correction_policy") == "exact_review_repairs_v1":
        from runners.run_finite_semantic_consolidation import assessment_schema
        shared = assessment_schema(scoped_checks=True, exact_repairs=True,
                                   answer=payload["answer"], known_refs=set(ids))["properties"]
        schema["properties"].update(material_findings=shared["material_findings"],
                                    answer_repairs=shared["answer_repairs"])
        schema["required"].append("answer_repairs")
        check = schema["properties"]["checks"]["items"]
        check["properties"]["scope"] = shared["check_results"]["items"]["properties"]["scope"]
        check["required"].append("scope")
    return schema


def exact(actual, expected, boundary):
    if Counter(actual) != Counter(expected) or len(set(expected)) != len(expected):
        raise ValueError(f"{boundary}: missing, duplicate, or foreign result identity")


def validate_response(request, response, count):
    try:
        Draft202012Validator(request["schema"]).validate(response)
    except ValidationError as exc:
        # Callers report ValueError as a preserved failure, never a crash.
        raise ValueError(f"consumer response schema violation: {exc.message}") from exc
    def text_and_array_rules(value, *, exact_after=False):
        if isinstance(value, str) and not value.strip() and not exact_after:
            raise ValueError("consumer response contains empty text")
        if isinstance(value, list):
            if all(isinstance(v, str) for v in value) and len(value) != len(set(value)):
                raise ValueError("consumer duplicate reference coverage")
            for child in value:
                text_and_array_rules(child)
        if isinstance(value, dict):
            for key, child in value.items():
                text_and_array_rules(child, exact_after=key == "after")
    text_and_array_rules(response)
    if count(compact(response)) > request["capacity"]["output_reserve_tokens"]:
        raise ValueError("consumer output exceeds reserved capacity")
    payload, phase = request["payload"], request["phase"]
    if phase in {"source_review", "reopen"}:
        used = []
        if len({digest(f) for f in response["findings"]}) != len(response["findings"]):
            raise ValueError("consumer duplicate finding coverage")
        for finding in response["findings"]:
            refs = sum((finding[k] for k in ("supporting_refs", "opposing_refs", "context_refs")), [])
            if not refs or not finding["question_ids"]:
                raise ValueError("consumer finding requires evidence and commissioned relevance")
            if set(finding["question_ids"]) - {q["id"] for q in payload["commission"]["questions"]}:
                raise ValueError("consumer finding has foreign question identity")
            used.extend(refs)
        unused = [r["unit_ref"] for r in response["unused"]]
        if set(used).intersection(unused):
            raise ValueError("consumer unit cannot be used and unused")
        exact(sorted(set(used)) + unused, payload["unit_ids"], "consumer unit coverage")
    else:
        exact([a["question_id"] for a in response["answers"]],
              [q["id"] for q in payload["commission"]["questions"]], "consumer question coverage")
        if phase != "assembly":
            if set(response["reopen_refs"]) - set(payload["unit_ids"]):
                raise ValueError("consumer review has foreign original-source handle")
            exact([c["check_id"] for c in response["checks"]],
                  [c["id"] for c in payload["checks"]], "consumer check coverage")
            if response["reopen_refs"] and all(a["status"] == "pass" for a in response["answers"] + response["checks"]):
                raise ValueError("consumer unresolved originals cannot pass")
            qids = {q["id"] for q in payload["commission"]["questions"]}
            for finding in ([] if payload.get("correction_policy") else response["material_findings"]):
                if (not finding["question_ids"] or set(finding["question_ids"]) - qids
                        or set(finding["evidence_refs"]) - set(payload["unit_ids"])):
                    raise ValueError("consumer review finding identity differs")
                if all(a["status"] == "pass" for a in response["answers"] if a["question_id"] in finding["question_ids"]):
                    raise ValueError("consumer material finding cannot coexist with passed affected answers")
        elif any(set(a["evidence_refs"]) - set(payload["unit_ids"]) for a in response["answers"]):
            raise ValueError("consumer answer has foreign evidence coverage")

    if payload.get("correction_policy") == "exact_review_repairs_v1":
        from judgment.review_evidence import answer_identity
        if response["answer_repairs"]["answer_sha256"] != answer_identity(payload["answer"]):
            raise ValueError("consumer repair answer identity mismatch")
        qids = {q["id"] for q in payload["commission"]["questions"]}
        for finding in response["material_findings"]:
            if set(finding["source_refs"]) - set(payload["unit_ids"]):
                raise ValueError("consumer repair has foreign evidence handle")
            for ref in finding["artifact_refs"]:
                if ref.startswith("current_answer:") and ref.removeprefix("current_answer:") not in qids:
                    raise ValueError("consumer repair has foreign answer identity")
            if finding["status"] == "open" and finding["severity"] in {"major", "blocker"}:
                if all(row["status"] == "pass" for row in response["answers"] + response["checks"]):
                    raise ValueError("consumer open material finding cannot pass review")
        if request["phase"] == "correction_recheck" and response["answer_repairs"]["edits"]:
            raise ValueError("consumer correction permits one exact repair, not a retry loop")


def build_request(phase, payload, capacity, context, count):
    schema = response_schema(phase, payload)
    repair_guidance = ""
    if payload.get("correction_policy") == "exact_review_repairs_v1":
        from judgment.review_evidence import answer_identity
        repair_guidance = (
            "\nClassify each repair nomination explicitly with severity, introduced_at, status, "
            "source_refs (checked handles), and artifact_refs (current_answer:QUESTION_ID only "
            "when the current answer is affected). Never convert an upstream-only issue into "
            "an answer defect. An uncertain origin remains uncertain. For admissible exact "
            "answer repairs supply unique before/after anchors and supporting checked handles; "
            "otherwise leave edits empty and preserve failure. Bind answer_repairs.answer_sha256="
            + answer_identity(payload["answer"]) + ". Check scope is answer, upstream_only, or unknown. "
            "During correction_recheck independently check all nominations, edits, changed claims "
            "and retained answers against the complete checked set. Do not propose another repair.\n")
    # Membership is already exposed by source-group IDs or checked handles.
    # Keep its exact local validation copy without duplicating it in actor text.
    actor_payload = payload if phase in {"source_review", "reopen"} else {k: v for k, v in payload.items() if k != "unit_ids"}
    prompt = context + "\n" + METHOD + "\nPHASE: " + phase + repair_guidance + "\n" + render_evidence(json.loads(compact(actor_payload)))
    measured = count(compact({"prompt": prompt, "response_schema": schema}))
    total = measured + capacity["output_reserve_tokens"] + capacity["other_overhead_reserve_tokens"]
    if total > capacity["effective_context_tokens"]:
        raise ValueError(f"consumer capacity exceeded at {phase}: {total} > {capacity['effective_context_tokens']}; no truncation")
    body = {"version": "complete_case_consumer_request_v1", "phase": phase,
            "payload": payload, "prompt": prompt, "schema": schema, "capacity": capacity,
            "measurement": {"input_and_schema_tokens": measured, "total_reserved_tokens": total,
                            "tokenizer_model_equivalence": "not_attested"}}
    return {**body, "request_sha256": digest(body)}


def source_groups(source, verified, view):
    """Lossless row atoms: all verified meanings, all relations, all residuals."""
    rows = source["captured_items"]
    exact([r["evidence_id"] for r in rows], list({r["evidence_id"]: None for r in rows}), "source identity")
    by_row = defaultdict(list)
    units = {u["semantic_unit_ref"]: u for u in verified["semantic_units"]}
    exact([u["semantic_unit_ref"] for u in verified["semantic_units"]], list(units), "verified identity")
    for unit in units.values():
        by_row[unit["evidence_id"]].append(unit)
    if set(by_row) - {r["evidence_id"] for r in rows}:
        raise ValueError("verified evidence has foreign source rows")
    related = defaultdict(list)
    attached = set()
    for finding in view["propositions"]:
        relations = finding["semantic_relations"]
        refs = {ref for values in relations.values() for ref in values}
        if refs - units.keys():
            raise ValueError("native finding has unknown unit")
        attached |= refs
        for row_id in {units[ref]["evidence_id"] for ref in refs}:
            owned = {u["semantic_unit_ref"] for u in by_row[row_id]}
            local = {**finding, "semantic_relations": {k: [r for r in v if r in owned] for k, v in relations.items()}}
            if "condition_lineage" in local:
                lineage = local["condition_lineage"]
                local["condition_lineage"] = ({k: v for k, v in lineage.items() if k in owned}
                    if isinstance(lineage, dict) else [r for r in lineage if r["semantic_unit_ref"] in owned])
            related[row_id].append(local)
    residuals = {u["semantic_unit_ref"]: u for u in view["unmerged_semantic_units"]}
    exact(list(attached) + list(residuals), list(units), "native finding/residual partition")
    artifacts = {a["artifact_id"]: a for a in source["source_artifacts"]}
    containers = {c["container_id"]: c for c in source.get("containers", [])}
    dispositions = defaultdict(list)
    for disposition in verified["evidence_dispositions"]:
        dispositions[disposition["evidence_id"]].append(disposition)
    result = []
    for row in rows:
        row_id = row["evidence_id"]
        if row["source_artifact_id"] not in artifacts:
            raise ValueError("source locator missing")
        owned = by_row[row_id]
        ids = [u["semantic_unit_ref"] for u in owned] or ["source:" + row_id]
        result.append({"unit_ids": ids, "source_row": row,
            "source_artifact": artifacts[row["source_artifact_id"]], "verified_units": owned,
            "container": containers.get(row.get("container_id")),
            "native_findings": related[row_id], "dispositions": dispositions[row_id],
            "residuals": [residuals[i] for i in ids if i in residuals]})
    return result


def prepare_source_requests(groups, commission, capacity, context, count, *, phase="source_review", extra=None):
    """Pack whole source rows; never split a row or silently drop overflow."""
    requests, pending = [], []

    def build(items):
        return build_request(phase, {"commission": commission,
            "unit_ids": [i for g in items for i in g["unit_ids"]], "source_groups": items,
            **(extra or {})}, capacity, context, count)

    for group in groups:
        candidate = pending + [group]
        try:
            request = build(candidate)
            if len(candidate) > capacity["max_rows_per_slice"]:
                raise ValueError("row packing limit")
        except ValueError:
            if not pending:
                raise
            requests.append(build(pending))
            pending = [group]
            build(pending)  # indivisible overflow fails before dispatch
        else:
            pending = candidate
    if pending:
        requests.append(build(pending))
    return requests


def validate_capacity(capacity):
    if not isinstance(capacity, dict) or not isinstance(capacity.get("encoding"), str) or not capacity["encoding"].strip():
        raise ValueError("consumer requires explicit nonempty encoding")
    for key in ("effective_context_tokens", "output_reserve_tokens", "max_rows_per_slice"):
        if type(capacity.get(key)) is not int or capacity[key] <= 0:
            raise ValueError(f"consumer requires positive {key}")
    if type(capacity.get("other_overhead_reserve_tokens")) is not int or capacity["other_overhead_reserve_tokens"] < 0:
        raise ValueError("consumer requires explicit overhead reserve")


def checked_projection(results):
    """Keep meanings/unused reasons; source membership stays in immutable receipts.

    Counts are inventory facts, never votes or prevalence. Final actors reopen
    exact handles when compression leaves a material question unresolved.
    """
    records, membership = [], {}
    for request, response in results:
        for index, finding in enumerate(response["findings"]):
            handle = f"f{len(records)}"
            roles = {key: finding[key] for key in ("supporting_refs", "opposing_refs", "context_refs")}
            membership[handle] = sorted(set(sum(roles.values(), [])))
            records.append({"handle": handle, **{k: v for k, v in finding.items() if k not in roles},
                            "relation_counts": {k: len(v) for k, v in roles.items()}})
        # Equal reasons can share transport, without erasing any distinct reason.
        unused = defaultdict(list)
        for row in response["unused"]:
            unused[row["reason"]].append(row["unit_ref"])
        for index, (reason, refs) in enumerate(sorted(unused.items())):
            handle = f"u{len(records)}"
            membership[handle] = refs
            records.append({"handle": handle, "unused_reason": reason, "unit_count": len(refs)})
    return records, membership


def origin_projection(results, membership):
    """Preserve equal/distinct source identities and relation-owned source roles.

    Origin aliases denote source identity, never inferred independence. Unknown
    identity is shared as unknown, not minted into a new person per source row.
    """
    units = {}
    for request, _ in results:
        for group in request["payload"]["source_groups"]:
            for ref in group["unit_ids"]:
                units[ref] = group["source_row"]
    identity_handles, original_identities = {}, {}
    attribution = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    finding_index = 0
    for _, response in results:
        for finding in response["findings"]:
            for relation in ("supporting_refs", "opposing_refs", "context_refs"):
                for ref in finding[relation]:
                    row = units[ref]
                    identity = row.get("independence_key") or row.get("public_identity_key")
                    origin = "unknown"
                    if identity and identity not in {"unavailable", "unknown"}:
                        identity_key = compact(identity)
                        if identity_key not in identity_handles:
                            identity_handles[identity_key] = len(identity_handles)
                        origin = identity_handles[identity_key]
                        original_identities[str(origin)] = identity
                    role = row.get("source_role", "unavailable")
                    posture = row.get("independence_posture", "unavailable")
                    attribution[(role, posture)][origin][relation].add(finding_index)
            finding_index += 1
    groups = []
    for (role, posture), origins in sorted(attribution.items()):
        groups.append({"source_role": role, "independence_posture": posture,
            "origins": [{"origin": origin, **{relation.replace("_refs", "_finding_indices"): sorted(relations.get(relation, set()))
                for relation in ("supporting_refs", "opposing_refs", "context_refs")}}
                for origin, relations in sorted(origins.items(), key=lambda item: str(item[0]))]})
    return groups, original_identities


def partition_checked_records(records):
    """Separate shapes so the existing lossless renderer can factor defaults."""
    result = {"findings": [], "unused": [], "reused_dispositions": []}
    for record in records:
        key = "findings" if "statement" in record else "unused" if "unused_reason" in record else "reused_dispositions"
        result[key].append(record)
    if Counter(compact(r) for rows in result.values() for r in rows) != Counter(compact(r) for r in records):
        raise ValueError("checked transport partition lost a record")
    return result


def reused_nonclaims(groups):
    """Reuse verified no-unit decisions; keep their full reasons and exact membership."""
    grouped = defaultdict(list)
    for group in groups:
        row = group["source_row"]
        dispositions = group["dispositions"]
        if not dispositions:
            if row.get("accounting_disposition") == "assess":
                raise ValueError("assessed source without verified disposition")
            reason = {"mechanical_source_disposition": {k: v for k, v in row.items()
                if k.startswith("accounting_")}, "scope": "not semantically assessed"}
            if not reason["mechanical_source_disposition"]:
                raise ValueError("source row lacks verified or mechanical disposition")
        else:
            reason = {"verified_dispositions": [{k: v for k, v in r.items() if k != "evidence_id"}
                       for r in dispositions], "scope": "reused verification; downstream materiality not proven"}
        grouped[compact(reason)].extend(group["unit_ids"])
    records, membership = [], {}
    for reason, refs in sorted(grouped.items()):
        handle = "n" + str(len(records))
        membership[handle] = refs
        records.append({"handle": handle, **json.loads(reason), "unit_count": len(refs)})
    return records, membership


def context_prefix_identity(prefix):
    """Compare exact authority bytes while allowing only checkout header relocation."""
    from runners.run_finite_semantic_consolidation import CONTEXT, REPO
    logical_paths = {p.relative_to(REPO).as_posix() for p in CONTEXT}
    header = re.compile(r"^SOURCE ([^\r\n]+)\nSHA256 ([0-9a-f]{64})\n", re.MULTILINE)
    ending = "\nEND SOURCE\n"
    parts, cursor = [], 0
    while match := header.search(prefix, cursor):
        end = prefix.find(ending, match.end())
        # A literal END SOURCE in a supplied file is content, not a delimiter.
        while end >= 0 and hashlib.sha256(prefix[match.end():end].encode("utf-8")).hexdigest() != match[2]:
            end = prefix.find(ending, end + 1)
        if end < 0:
            raise ValueError("preloaded context source hash differs")
        label = match[1].replace("\\", "/")
        names = [name for name in logical_paths if label.endswith("/" + name)]
        identity = names[0] if len(names) == 1 else match[1]
        stop = end + len(ending)
        parts.extend((prefix[cursor:match.start(1)], identity, prefix[match.end(1):stop]))
        cursor = stop
    return "".join(parts) + prefix[cursor:]


def advance(source, verified, view, commission, capacity, root, *, context, count):
    """Return all ready bounded jobs, or immutable checked answers / real blockers."""
    validate_capacity(capacity)
    questions = commission["questions"]
    if not questions or any(not q.get("question", "").strip() for q in questions):
        raise ValueError("consumer requires nonempty commissioned questions")
    exact([q["id"] for q in questions], list({q["id"] for q in questions}), "commission question identity")
    checks = commission.get("assessment_only", {}).get("checks", [])
    exact([c["id"] for c in checks], list({c["id"] for c in checks}), "commission check identity")
    base = {k: v for k, v in commission.items() if k != "assessment_only"}
    root = Path(root)
    groups = source_groups(source, verified, view)
    all_ids = [i for g in groups for i in g["unit_ids"]]
    context_source = {k: v for k, v in source.items()
                      if k not in {"captured_items", "source_artifacts", "containers", "source_sha256"}}

    stored_requests = None
    binding_fields = ("version", "phase", "payload", "schema", "capacity")

    def saved_request(request):
        """Reuse ordering/checkout variants only after proving equal complete delivery."""
        nonlocal stored_requests
        from judgment.review_evidence import RENDERING_GUIDANCE, expand_evidence
        # In-memory lookup only; each existing request is read at most once per
        # advance. No persisted alias registry or alternate source of authority.
        if stored_requests is None:
            stored_requests = defaultdict(list)
            for path in sorted((root / "requests").glob("*/request.json")):
                saved = read(path)
                key = digest({k: saved.get(k) for k in binding_fields})
                stored_requests[key].append((path, saved))
        key = digest({k: request.get(k) for k in binding_fields})
        marker = RENDERING_GUIDANCE + "\n\n"
        prefix, envelope = request["prompt"].rsplit(marker, 1)
        prefix_identity = context_prefix_identity(prefix)
        expected = expand_evidence(json.loads(envelope))
        matches, accepted = [], set()
        for path, saved in stored_requests[key]:
            validate_request(saved, path.parent.name)
            if marker not in saved["prompt"]:
                continue
            old_prefix, old_envelope = saved["prompt"].rsplit(marker, 1)
            if context_prefix_identity(old_prefix) != prefix_identity or expand_evidence(json.loads(old_envelope)) != expected:
                continue
            measured = count(compact({"prompt": saved["prompt"], "response_schema": saved["schema"]}))
            total = measured + capacity["output_reserve_tokens"] + capacity["other_overhead_reserve_tokens"]
            if (saved["measurement"]["input_and_schema_tokens"] != measured
                    or saved["measurement"]["total_reserved_tokens"] != total
                    or total > capacity["effective_context_tokens"]):
                raise ValueError("saved consumer delivery measurement differs")
            target = path.with_name("response.json")
            if not target.exists() and path.with_name("response.receipt.json").exists():
                raise ValueError("accepted consumer response missing; restore its bound bytes, do not rejudge")
            if target.exists():
                accepted.add(digest(read(target)))
            matches.append((not target.exists(), path, saved))
        if len(accepted) > 1:
            raise ValueError("equivalent consumer transports have conflicting saved judgments")
        return min(matches, key=lambda row: (row[0], str(row[1])))[2] if matches else request

    def consume(requests):
        missing, responses = [], []
        for request in requests:
            request = saved_request(request)
            key = request["request_sha256"]
            directory = root / "requests" / key
            retain(directory / "request.json", request)
            actor_input = directory / "actor-input.json"
            retain(actor_input, {"prompt": request["prompt"], "response_schema": request["schema"]})
            target = directory / "response.json"
            if not target.exists() and (directory / "response.receipt.json").exists():
                raise ValueError("accepted consumer response missing; restore its bound bytes, do not rejudge")
            if target.with_name("response.json.tmp").exists():
                raise ValueError("staged consumer response requires explicit recovery; do not rejudge")
            if target.exists():
                response = read(target)
                if not (directory / "response.receipt.json").exists():
                    submit(directory / "request.json", key, target, count)
                receipt = read(directory / "response.receipt.json")
                if receipt != {"request_sha256": key, "response_sha256": digest(response)}:
                    raise ValueError("accepted consumer response binding changed")
                validate_response(request, response, count)
                responses.append((request, response))
            else:
                from runners.run_semantic_evidence_integration import judgment_worker_prompt, intake_judgment_job
                job_path = directory / "request.json"
                intake = intake_judgment_job(job_path=job_path, expected_sha256=key)
                from runners.run_semantic_evidence_integration import JUDGMENT_SINGLE_RETURN_BYTE_LIMIT
                intake_bytes = len((json.dumps(intake, indent=2) + "\n").encode("utf-8"))
                worker_prompt = judgment_worker_prompt(job_path, key, intake_utf8_bytes=intake_bytes)
                from runners.run_semantic_evidence_integration import _judgment_content_chunk
                framing = []
                chunked = intake_bytes > JUDGMENT_SINGLE_RETURN_BYTE_LIMIT
                for name, content in intake["content"].items():
                    raw = content.encode("utf-8" if chunked else "utf-16-le")
                    total = len(raw) if chunked else len(raw) // 2
                    offset = 0
                    while offset < total:
                        if chunked:
                            end = offset + len(_judgment_content_chunk(raw, offset))
                            metadata = {"section": name, "from_byte": offset, "to_byte": end, "total_bytes": total}
                        else:
                            end = min(offset + 8000, total)
                            if end < total and 0xD800 <= int.from_bytes(raw[2*(end-1):2*end], "little") <= 0xDBFF:
                                end -= 1
                            metadata = {"section": name, "from_character": offset, "to_character": end, "total_characters": total}
                        framing.append({**metadata, "end_marker": f"END_SECTION_BLOCK {name} {end}"})
                        offset = end
                delivery_hashes = ({name: hashlib.sha256(content.encode()).hexdigest()
                    for name, content in intake["content"].items()} if chunked else {})
                handoff_tokens = count(compact({"worker_prompt": worker_prompt,
                    "intake_metadata": {k: v for k, v in intake.items() if k != "content"},
                    "section_framing": framing, "content_sha256": delivery_hashes}))
                total = request["measurement"]["total_reserved_tokens"] + handoff_tokens
                if total > capacity["effective_context_tokens"]:
                    raise ValueError(f"consumer capacity exceeded at {request['phase']} worker handoff: {total} > {capacity['effective_context_tokens']}; no truncation")
                missing.append({"phase": request["phase"], "job_path": str(job_path),
                    "job_sha256": key, "response_path": str(target), "worker_context": "fresh_per_request",
                    "intake_command": "intake-judgment-job", "submit_command": "submit-judgment-job",
                    "max_concurrent_workers": 3,
                    "worker_prompt": worker_prompt,
                    "measurement": {**request["measurement"], "handoff_instruction_tokens": handoff_tokens,
                                    "intake_transport_utf8_bytes": intake_bytes,
                                    "intake_transport_mode": ("bounded_sections_v1" if intake_bytes > JUDGMENT_SINGLE_RETURN_BYTE_LIMIT else "single_return"),
                                    "total_reserved_tokens": total}})
        return missing, responses

    def waiting(missing):
        return {"status": "SEMANTIC_JUDGMENT_REQUIRED", "phase": "consumer",
                "judgment_requests": missing, "model_api_calls": 0}

    anchors = {r for check in checks for r in check.get("source_rows", [])}
    if anchors - {g["source_row"]["evidence_id"] for g in groups}:
        raise ValueError("consumer check has unknown source anchor")
    active = [g for g in groups if g["verified_units"] or g["source_row"]["evidence_id"] in anchors]
    inactive = [g for g in groups if not g["verified_units"] and g["source_row"]["evidence_id"] not in anchors]
    requests = prepare_source_requests(active, base, capacity, context, count, extra={"source_context": context_source})
    missing, results = consume(requests)
    if missing:
        return waiting(missing)
    checked, membership = checked_projection(results)
    origins, original_identities = origin_projection(results, membership)
    reused, reused_membership = reused_nonclaims(inactive)
    checked.extend(reused)
    membership.update(reused_membership)
    exact(sorted({ref for refs in membership.values() for ref in refs}), all_ids, "consumer compiled membership")
    manifest = {"membership": membership, "original_origin_identities": original_identities, "source_responses": [
        {"request_sha256": request["request_sha256"], "response_sha256": digest(response)}
        for request, response in results], "reused_dispositions": reused}
    manifest_hash = digest(manifest)
    retain(root / "membership" / (manifest_hash + ".json"), manifest)
    payload = {"commission": base, "unit_ids": list(membership), "membership_sha256": manifest_hash,
               "checked_findings_and_unused": partition_checked_records(checked),
               "source_origin_attribution": origins,
               "origin_indexing": "Finding indices are zero-based positions in checked_findings_and_unused.findings. "
               "Numeric origins preserve equal/distinct source identity, not independent corroboration; unknown remains unknown."}
    assembly = build_request("assembly", payload, capacity, context, count)
    missing, answers = consume([assembly])
    if missing:
        return waiting(missing)
    assembly, answer = answers[0]
    review_payload = {**payload, "answer": answer, "checks": checks}
    def review_request(phase, value):
        legacy = build_request(phase, value, capacity, context, count)
        saved = saved_request(legacy)
        if (root / "requests" / saved["request_sha256"] / "request.json").exists():
            return saved
        return build_request(phase, {**value, "correction_policy": "exact_review_repairs_v1"}, capacity, context, count)

    review = review_request("answer_review", review_payload)
    missing, reviews = consume([review])
    if missing:
        return waiting(missing)
    review, assessment = reviews[0]
    if assessment["reopen_refs"]:
        selected = {ref for handle in assessment["reopen_refs"] for ref in membership[handle]}
        reopened = [g for g in groups if selected.intersection(g["unit_ids"])]
        requests = prepare_source_requests(reopened, base, capacity, context, count, phase="reopen",
            extra={"answer": answer, "review": assessment, "source_context": context_source})
        missing, reopened_results = consume(requests)
        if missing:
            return waiting(missing)
        review = review_request("answer_review_after_reopen", {**review_payload,
            "reopened_original_judgments": [response for _, response in reopened_results]})
        missing, reviews = consume([review])
        if missing:
            return waiting(missing)
        review, assessment = reviews[0]
    status = "COMPLETE_CASE_ANSWER_CHECKED" if not assessment["reopen_refs"] and all(
        r["status"] == "pass" for r in assessment["answers"] + assessment["checks"]) else "COMPLETE_CASE_ANSWER_REQUIRES_REVISION"
    correction = {}
    if status != "COMPLETE_CASE_ANSWER_CHECKED" and not assessment["reopen_refs"] and assessment.get("answer_repairs", {}).get("edits"):
        from judgment.review_evidence import (apply_exact_answer_repairs, material_answer_findings,
                                              compose_answer_patch, correction_selection)
        nominations = assessment["material_findings"]
        # No inferred scope: unclassified or upstream-only failed checks/answers
        # retain failure. Existing helper decides which nominations are eligible.
        eligible = material_answer_findings(nominations)
        affected = {r.removeprefix("current_answer:") for f in eligible
                    for r in f["artifact_refs"] if r.startswith("current_answer:")}
        failing = {r["question_id"] for r in assessment["answers"] if r["status"] != "pass"}
        classified = all(c["status"] == "pass" or c.get("scope") == "answer" for c in assessment["checks"])
        if eligible and failing <= affected and classified:
            try:
                candidate = apply_exact_answer_repairs(answer, assessment["answer_repairs"], nominations, set(membership))
                candidate = compose_answer_patch(answer, {"answers": [r for r in candidate["answers"]
                    if r["question_id"] in affected]}, affected)
                validate_response(assembly, candidate, count)
            except (ValueError, ValidationError) as exc:
                correction = {"status": "inadmissible", "error": str(exc), "original_answer": answer}
            else:
                correction = {"status": "pending_recheck", "original_answer": answer,
                              "candidate_answer": candidate, "original_assessment": assessment}
                correction_path = root / "corrections" / (digest(correction) + ".json")
                retain(correction_path, correction)
                recheck = build_request("correction_recheck", {**review["payload"], "answer": candidate,
                    "original_answer": answer, "repair_nominations": nominations,
                    "exact_repairs": assessment["answer_repairs"]}, capacity, context, count)
                missing, responses = consume([recheck])
                if missing:
                    return {**waiting(missing), "correction_path": str(correction_path)}
                recheck, checked = responses[0]
                def shared_assessment(value):
                    return {"material_findings": value["material_findings"], "check_results": [
                        {"check_id": "answer:" + row["question_id"], "scope": "answer",
                         "status": {"pass": "pass", "defect": "fail", "unresolved": "uncertain"}[row["status"]]}
                        for row in value["answers"]] + [
                        {**row, "status": {"pass": "pass", "defect": "fail", "unresolved": "uncertain"}[row["status"]]}
                        for row in value["checks"]]}
                selected = correction_selection(answer, candidate, shared_assessment(assessment), shared_assessment(checked))
                clean = not checked["reopen_refs"] and all(r["status"] == "pass" for r in checked["answers"] + checked["checks"])
                # Clean-only consumer route: no invented source-observation comparison.
                accepted = (clean and selected["answer_correction_status"] == "accepted"
                            and not selected["remaining_material_answer_findings"])
                correction.update(selection=selected, status="accepted" if accepted else "rejected",
                                  recheck_request=recheck["request_sha256"], recheck=checked)
                if accepted:
                    answer, assessment, review = candidate, checked, recheck
                    status = "COMPLETE_CASE_ANSWER_CHECKED"
    result = {"schema_version": "complete_case_answer_v1", "status": status,
        "source_sha256": digest(source), "verified_sha256": digest(verified), "view_sha256": digest(view),
        **({"correction": correction} if correction else {}),
        "commission_sha256": digest(commission), "source_review_requests": [r["request_sha256"] for r, _ in results],
        "assembly_request": assembly["request_sha256"], "review_request": review["request_sha256"],
        "answer": {"answers": [{**row, "checked_finding_refs": row["evidence_refs"],
            "evidence_refs": sorted({ref for handle in row["evidence_refs"] for ref in membership[handle]})}
            for row in answer["answers"]]}, "assessment": assessment,
        "coverage": {"source_rows": len(groups), "verified_units": len(verified["semantic_units"]),
                     "consumer_units": len(all_ids), "source_review_rows": len(active),
                     "reused_nonclaim_rows": len(inactive), "mode": "complete_bound_inventory_not_sample"}}
    target = root / "results" / (digest(result) + ".json")
    retain(target, result)
    return {"status": status, "phase": "consumer", "answer_path": str(target),
            "answer_sha256": digest(result), "judgment_requests": [], "model_api_calls": 0}


def validate_request(request, expected_sha256):
    body = {k: v for k, v in request.items() if k != "request_sha256"}
    if digest(body) != expected_sha256 or request["request_sha256"] != expected_sha256:
        raise ValueError("consumer request identity mismatch")
    validate_capacity(request.get("capacity"))
    return request


def submit(request_path, expected_sha256, response_path, count):
    request = validate_request(read(request_path), expected_sha256)
    response = read(response_path)
    validate_response(request, response, count)
    target = Path(request_path).parent / "response.json"
    if not target.exists() and target.with_name("response.receipt.json").exists():
        raise ValueError("accepted consumer response missing; restore its bound bytes, do not rejudge")
    retain(target, response)
    retain(target.with_name("response.receipt.json"), {"request_sha256": expected_sha256, "response_sha256": digest(response)})
    return {"status": "CONSUMER_RESPONSE_ACCEPTED", "response_path": str(target), "response_sha256": digest(read(target))}
