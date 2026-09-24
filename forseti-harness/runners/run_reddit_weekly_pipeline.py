"""Run the weekly Reddit Top100 model and thread-capture stages without a supervising agent.

Stages (each resumable; every model call keeps a receipt under the run directory):

- ``adjudicate``: row-level listing adjudication of a weekly reader queue under
  ``weekly_latent_problem_gtm_discovery_v0``, one structured model call per chunk,
  then the deep-dive manifest and 10-URL capture batches (Best-sort thread URLs).
- ``capture``: drives ``run_reddit_old_http_batch.py`` batch by batch, retrying
  non-access failures once in a fresh output root; any refusal, access diagnostic
  or tripped breaker stops the run.
- ``read``: renders each captured batch in ``reddit_weekly_value_bounded_read_v1``
  attention order, asks the model for judgment fields only, fills fixed fields and
  verbatim quote text from the content record, validates every receipt with the
  weekly finalizer's own check, repairs failing threads once, and logs usage.
- ``scope``: writes the finalize directory for batches 1..N (the full set or an
  owner stop), excluding threads recorded as unavailable at capture.
- ``delta`` / ``evidence`` / ``check``: script-only consolidation aids over a
  finalized catalog (card candidates, card-ready claims and quotes, and a
  fail-loud check that the weekly read cites only yes threads and verbatim quotes).

Model transport is the Claude Code CLI in headless print mode with structured
output and no tools. Judgment stays run-scoped; nothing here writes to the lake
except the thread packets that ``capture`` commits through the existing runner.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import threading
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runners._scaffold import exit_on_failure
from runners.run_reddit_weekly_finalizer import (
    EVIDENCE_READ_RECEIPT_SCHEMA,
    READ_POLICY_ID,
    _validated_evidence_read_receipt,
)

HARNESS = Path(__file__).resolve().parents[1]
THREAD_BATCH_RUNNER = HARNESS / "runners" / "run_reddit_old_http_batch.py"
METHODOLOGY_ID = "reddit_weekly_top100_per_subreddit_v0"
DECISION_FRAME = "weekly_latent_problem_gtm_discovery_v0"
POLICY_VERSION = "reddit_listing_efficiency_v0"
BEST_SORT = "?sort=confidence"
BATCH_SIZE = 10
THREAD_ID = re.compile(r"/comments/([A-Za-z0-9]+)")
CAPTURE_QUESTION = (
    "Does this thread add material, recoverable evidence about product choice, product "
    "performance, unmet demand, customer constraints, alternatives, workarounds, or where "
    "customers go?"
)
WAVES = ("high_priority", "explicit_evidence_yes", "borderline_resolution")

CODES: dict[str, tuple[str, str, str]] = {
    "yf": ("yes", "failure_or_unmet_need", "normal"),
    "yF": ("yes", "failure_or_unmet_need", "high"),
    "yr": ("yes", "recommendation_or_specific_demand", "normal"),
    "yR": ("yes", "recommendation_or_specific_demand", "high"),
    "yc": ("yes", "comparison_substitute_or_dupe", "normal"),
    "yC": ("yes", "comparison_substitute_or_dupe", "high"),
    "yp": ("yes", "product_experience_review_or_performance", "normal"),
    "yP": ("yes", "product_experience_review_or_performance", "high"),
    "ya": ("yes", "price_access_purchase_availability_or_switching", "normal"),
    "yA": ("yes", "price_access_purchase_availability_or_switching", "high"),
    "yb": ("yes", "completed_use_abandonment_regret_or_consumption", "normal"),
    "yB": ("yes", "completed_use_abandonment_regret_or_consumption", "high"),
    "ys": ("yes", "product_compatibility_or_safety_problem", "normal"),
    "yS": ("yes", "product_compatibility_or_safety_problem", "high"),
    "bo": ("borderline", "insufficient_listing_context", "normal"),
    "ba": ("borderline", "bounded_applicability_or_safety_uncertainty", "normal"),
    "bf": ("borderline", "commercial_object_implied_by_format", "normal"),
    "na": ("no", "appearance_validation_or_showcase", "suppressed"),
    "nt": ("no", "generic_technique_without_product_implication", "suppressed"),
    "nc": ("no", "crowd_diagnosis_or_clinical_treatment", "suppressed"),
    "ng": ("no", "gossip_without_commercial_consequence", "suppressed"),
    "nw": ("no", "wts_resale_or_swap_administration", "suppressed"),
    "nr": ("no", "retailer_promotion_news_or_release_only", "suppressed"),
    "nd": ("no", "specialist_diy_formulation", "suppressed"),
    "np": ("no", "praise_or_category_favorite_problem_queue", "suppressed"),
    "nx": ("no", "insufficient_expected_current_contribution", "suppressed"),
    "ns": ("no", "professional_service_outside_commission", "suppressed"),
    "nu": ("no", "routine_collection_or_progress_without_problem_promise", "suppressed"),
}

SYSTEM_PROMPT = (
    "You are a careful evidence analyst for a beauty and personal-care challenger brand. "
    "Answer only from the supplied text, follow the rules exactly, and return the requested "
    "structured output."
)

ADJUDICATE_BRIEF = """Decide which Reddit listing rows deserve a deep read for frame weekly_latent_problem_gtm_discovery_v0: a scaling beauty or personal-care challenger looking for latent GTM problems (unvoiced, emerging, or evident). Every row already cleared the comment floor. Judge each row independently from its title, flair, post type and listing context; never from engagement alone.

Admit (yes) when the listing visibly promises: named-product performance, failure or disappointment; recommendation, comparison, substitute, dupe or discontinued-product replacement; a specific user/condition/constraint with a desired outcome; completed use, repurchase, abandonment, regret or consumption; price, access, purchase, refund, availability or switching; a product stack or compatibility problem; a verified creator/brand relationship with trust consequences. Use an uppercase code (high priority) only for the strongest, most decision-relevant rows.
Concrete evidence outranks the format: collection/routine/haul/favorite/praise/project-pan labels are weak priors, never vetoes. A weak-format title with a visible commercial object that could hide such evidence is borderline, not no. A pure showcase, generic favorites prompt, ordinary haul or routine with no concrete decision promise is no.
Borderline: bo when the title depends on "this", an image or an opaque community format; ba for bounded applicability or safety uncertainty; bf when a commercial object is implied by the format.
No: na appearance validation or showcase; nt generic technique with no product implication; nc crowd diagnosis or clinical treatment; ng gossip without commercial consequence; nw WTS/swap/resale administration; nr retailer promotion, news or release-only; nd specialist DIY formulation; np praise-only or category favorites (served by the separate leaderboard lane); ns professional services; nu routine, collection or progress with no problem promise; nx insufficient expected contribution, wrong geography (country-audience, non-US), daily/SOTD mega-threads, or anything else.
Yes codes: f failure or unmet need; r recommendation or specific demand; c comparison, substitute or dupe; p product experience or performance; a price, access, purchase or switching; b completed use, abandonment, regret or consumption; s compatibility or safety problem.

Latent problems are often voiced as category-wide discussion with no product in the title. These are yes (f, a or b) even without a named product: fatigue with a trend or ingredient ("sick of gourmand", "musk in everything"), distrust of marketing, AI ads, influencers or reviews, overconsumption, regret or no-buy, regulation or availability gaps ("US sunscreen is worse", "can't get X"), and unmet needs of a segment (menopause, olive or fair skin, a climate or occupation). They are not gossip: gossip is about a person, not about how people buy or use products.

Apply the no rules next; a row that matches one is no even if it also sounds like a question or request:
- best-of, favorites, "which do you prefer", "what's your HG", "rate my" prompts about what people already love are np unless the title names a failure, disappointment, switch or problem; a request for a recommendation for a stated need, condition or constraint ("eye cream recs at 31", "sunscreen that doesn't break me out") is yes (r), not np;
- posts about a specific country or region outside the US (Canada, UK, India, Australia, Italy, Europe, ...) are nx;
- nc only when the object is a prescription drug regimen, a diagnosis-only photo request ("what is this rash?"), or a medical question; ns for injections, fillers, lasers, surgery and salon or professional services. Skin, hair and scalp problems where people want products, routines or fixes (acne, rosacea, perimenopause and menopause skin, dryness, hair loss with over-the-counter products, eczema care) stay eligible and are usually yes (f) or borderline;
- sales, discounts, gift-with-purchase, advent calendars, beauty boxes, releases and launch announcements are nr;
- items outside beauty and personal care (contact lenses, clothing, candles, home fragrance) are nx;
- daily/weekly discussion and SOTD mega-threads are nx.

Return exactly one decision per row, using the row's thread_id exactly as given.

ROWS (tab-separated: thread_id, subreddit, comments, score, flair, post_type, selection, title, context):
"""

READ_BRIEF = """Read the captured Reddit threads below for a beauty/personal-care challenger brand looking for latent GTM problems (frame weekly_latent_problem_gtm_discovery_v0) and return one judgment object per thread.

What counts: product failure, disappointment, workaround, substitution/dupe, compatibility conflict, unmet need, price/access/switching, discontinuation/reformulation, regret, trust/marketing backlash. Praise-only, showcases and generic advice are weak.

Each thread is already in policy attention order: post, COHORT, then BATCH 1, 2, ... A batch adds value only if it adds a new condition, mechanism, consequence, behavior, materially better evidence, or counter. Stop after two consecutive no-value batches (stop_reason decision_relevant_novelty_plateau, consecutive_no_value_batches 2) or at END (stop_reason corpus_exhausted, comments_reviewed = the total shown at END, consecutive_no_value_batches = trailing no-value batches 0-1). comments_reviewed = cohort + comments in every batch you read.

admission yes if the thread carries decision-relevant evidence, else no. A thread that proves empty is no, contribution_class excluded_after_read, core_problem starting "NO_SIGNAL: ".
Claims: claim_id unique kebab-case; evidence_kind individual | recurrence | map_or_shortlist | factual_or_safety | dispute; support_comment_ids 0-5 real comment IDs from the thread (never the post); counter_comment_ids must not overlap support. yes needs at least one claim. Distinct cited IDs across claims cannot exceed comments_reviewed.
recurrence: 1-5 DIRECT first-person reports of the same experience by DISTINCT authors, none by the OP, none [deleted]/[removed]; a recommendation is not a report. corroboration_status by count: 1 lead, 2 emerging, 3-4 corroborated, 5 sufficient. Every other kind uses not_applicable.
core_problem: one plain sentence a founder outside this project can read cold. commercial_signal: one sentence. named_brands: brands in their stated context. quote_comment_ids: two comment IDs whose text best shows the problem (none for no).

THREADS:
"""


class PipelineError(RuntimeError):
    """A stage refused to continue; the run directory keeps every receipt so far."""


# ---------------------------------------------------------------- model transport


ModelCall = Callable[[str, dict], dict]


def claude_structured_call_factory(
    *, model: str, effort: str, timeout: float, executable: str | None, bare: bool, cwd: Path
) -> ModelCall:
    """Headless Claude Code call with no tools, no settings and no project memory.

    ``--setting-sources ""`` plus a neutral working directory keep CLAUDE.md and
    user settings out of every call (measured ~6k fixed tokens per call). ``--bare``
    additionally skips hooks but also skips the logged-in account, so it is only
    for API-key environments.
    """
    cli = executable or shutil.which("claude")
    if not cli:
        raise PipelineError("claude CLI not found; install @anthropic-ai/claude-code or pass --claude-executable")

    def call(prompt: str, schema: dict) -> dict:
        command = [cli, "-p"]
        if bare:
            command.append("--bare")
        command += [
            "--output-format", "json", "--json-schema", json.dumps(schema, separators=(",", ":")),
            "--model", model, "--effort", effort, "--tools", "", "--no-session-persistence",
            "--setting-sources", "", "--system-prompt", SYSTEM_PROMPT,
        ]
        try:
            process = subprocess.run(
                command, input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=timeout, cwd=cwd,
            )
        except subprocess.TimeoutExpired as exc:
            raise PipelineError(f"model call timed out after {timeout}s") from exc
        lines = [line for line in process.stdout.splitlines() if line.strip().startswith("{")]
        if not lines:
            raise PipelineError(f"model call returned no JSON (exit {process.returncode}): {process.stderr.strip()[:300]}")
        payload = json.loads(lines[-1])
        if process.returncode != 0 or payload.get("is_error") or not isinstance(payload.get("structured_output"), dict):
            raise PipelineError(f"model call failed: {str(payload.get('result'))[:300]}")
        usage = payload.get("usage") or {}
        return {
            "output": payload["structured_output"],
            "usage": {
                "input_tokens": usage.get("input_tokens"),
                "output_tokens": usage.get("output_tokens"),
                "cache_read_input_tokens": usage.get("cache_read_input_tokens"),
                "cache_creation_input_tokens": usage.get("cache_creation_input_tokens"),
                "total_cost_usd": payload.get("total_cost_usd"),
                "duration_ms": payload.get("duration_ms"),
                "model": model,
                "effort": effort,
            },
        }

    call.receipt_identity = {"model": model, "effort": effort, "system_prompt": SYSTEM_PROMPT, "bare": bare}
    return call


def receipted_call(call: ModelCall, receipt_path: Path, prompt: str, schema: dict) -> dict:
    """Reuse a stored response for an identical prompt; otherwise call and store it."""
    identity = getattr(call, "receipt_identity", None)
    digest = hashlib.sha256(json.dumps(
        {"prompt": prompt, "schema": schema, "identity": identity}, sort_keys=True
    ).encode("utf-8")).hexdigest()
    if receipt_path.is_file():
        stored = json.loads(receipt_path.read_text(encoding="utf-8"))
        if stored.get("prompt_sha256") == digest:
            return {**stored, "reused": True}
    response = call(prompt, schema)
    receipt = {"prompt_sha256": digest, "called_at": dt.datetime.now(dt.timezone.utc).isoformat(), **response}
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


_USAGE_LOCK = threading.Lock()


def _append_usage(run_dir: Path, row: dict) -> None:
    """Log each receipt once, including one persisted before an interrupted append.

    A reused receipt reproduces its logged row exactly; a deliberate fresh call with the
    same prompt carries different usage, so it is still logged as real spend.
    """
    path = run_dir / "model_usage_log.jsonl"
    with _USAGE_LOCK:
        if path.is_file():
            if any(json.loads(line) == row for line in path.read_text(encoding="utf-8").splitlines()):
                return
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _flat(value: object) -> str:
    return " ".join(str(value or "").split())


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- adjudicate

ADJUDICATE_SCHEMA = {
    "type": "object",
    "properties": {
        "decisions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"thread_id": {"type": "string"}, "code": {"type": "string", "enum": sorted(CODES)}},
                "required": ["thread_id", "code"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["decisions"],
    "additionalProperties": False,
}


def _review_rows(reader: dict) -> list[dict]:
    rows = []
    for cand in reader["candidates"]:
        match = THREAD_ID.search(cand["thread_url"])
        if not match:
            raise PipelineError(f"no thread id in {cand['thread_url']}")
        title = _flat(cand.get("title_or_none"))
        alt = re.sub(r"^r/\S+ - ", "", _flat(cand.get("listing_preview_alt_text_or_none")))
        context = [] if not alt or alt.lower() == title.lower() else [f"alt={alt}"]
        domain = _flat(cand.get("listing_content_domain_or_none"))
        if domain and not domain.startswith("self.") and domain not in {"reddit.com", "i.redd.it", "v.redd.it"}:
            context.append(f"domain={domain}")
        rows.append({
            "thread_id": match.group(1), "cand": cand, "subreddit": cand["subreddit"],
            "rank": cand.get("subreddit_rank_by_comments") or 0,
            "line": "\t".join(str(x) for x in (
                match.group(1), cand["subreddit"], cand.get("comments"), cand.get("score"),
                _flat(cand.get("flair_or_none")) or "-", _flat(cand.get("listing_post_type_or_none")) or "-",
                cand.get("selection_reason", ""), title, " | ".join(context) or "-",
            )),
        })
    ids = [r["thread_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise PipelineError("duplicate thread ids in reader candidates")
    rows.sort(key=lambda r: (r["subreddit"], r["rank"]))
    return rows


def _chunks(rows: list[dict], size: int) -> list[list[dict]]:
    chunks: list[list[dict]] = []
    current: list[dict] = []
    for row in rows:
        if current and len(current) >= size and row["subreddit"] != current[-1]["subreddit"]:
            chunks.append(current)
            current = []
        current.append(row)
    if current:
        chunks.append(current)
    return chunks


def _dedupe(decisions: list[dict]) -> list[dict]:
    """Collapse exact repeats; conflicting codes for one thread stay visible to the check."""
    seen: set[tuple[str, str]] = set()
    unique = []
    for d in decisions:
        key = (d.get("thread_id"), d.get("code"))
        if key not in seen:
            seen.add(key)
            unique.append(d)
    return unique


def _check_chunk(chunk: list[dict], decisions: list[dict]) -> list[str]:
    expected = {r["thread_id"] for r in chunk}
    seen = Counter(d.get("thread_id") for d in decisions)
    problems = [f"missing {sorted(expected - set(seen))}"] if expected - set(seen) else []
    if set(seen) - expected:
        problems.append(f"unexpected {sorted(set(seen) - expected)}")
    dupes = sorted(t for t, n in seen.items() if n > 1)
    if dupes:
        problems.append(f"duplicated {dupes}")
    return problems


def adjudicate(run_dir: Path, reader_path: Path, call: ModelCall, *, chunk_rows: int, workers: int) -> dict:
    raw = reader_path.read_bytes()
    reader = json.loads(raw)
    rows = _review_rows(reader)
    chunks = _chunks(rows, chunk_rows)

    def run_chunk(index: int, chunk: list[dict]) -> list[dict]:
        prompt = ADJUDICATE_BRIEF + "\n".join(r["line"] for r in chunk) + "\n"
        receipt = receipted_call(call, run_dir / "calls" / "adjudicate" / f"chunk_{index:03d}.json", prompt, ADJUDICATE_SCHEMA)
        _append_usage(run_dir, {"stage": "adjudicate", "unit": f"chunk_{index:03d}", "rows": len(chunk),
                                "prompt_sha256": receipt["prompt_sha256"], **receipt["usage"]})
        decisions = _dedupe(receipt["output"]["decisions"])
        problems = _check_chunk(chunk, decisions)
        if problems:
            repair_prompt = prompt + "\nYour previous answer was rejected: " + "; ".join(problems) + ". Return exactly one decision for every row above.\n"
            receipt = receipted_call(call, run_dir / "calls" / "adjudicate" / f"chunk_{index:03d}_repair.json", repair_prompt, ADJUDICATE_SCHEMA)
            _append_usage(run_dir, {"stage": "adjudicate", "unit": f"chunk_{index:03d}_repair", "rows": len(chunk),
                                    "prompt_sha256": receipt["prompt_sha256"], **receipt["usage"]})
            decisions = _dedupe(receipt["output"]["decisions"])
            problems = _check_chunk(chunk, decisions)
            if problems:
                raise PipelineError(f"adjudication chunk {index} still invalid: {'; '.join(problems)}")
        return decisions

    decided: dict[str, str] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for decisions in pool.map(lambda pair: run_chunk(*pair), enumerate(chunks, start=1)):
            decided.update({d["thread_id"]: d["code"] for d in decisions})
    if set(decided) != {r["thread_id"] for r in rows}:
        raise PipelineError("adjudication does not cover the reader queue exactly")

    records = []
    for row in rows:
        admission, reason, band = CODES[decided[row["thread_id"]]]
        cand = row["cand"]
        records.append({
            "policy_version": POLICY_VERSION, "decision_frame": DECISION_FRAME, "methodology_id": METHODOLOGY_ID,
            "thread_id": row["thread_id"], "thread_url": cand["thread_url"], "subreddit": cand["subreddit"],
            "listing_snapshot": {"captured_at": cand.get("timestamp_utc_ms_or_none") or "missing",
                                 "score": cand.get("score"), "comments": cand.get("comments")},
            "title_or_none": cand.get("title_or_none"), "selection_reason": cand.get("selection_reason"),
            "admission": admission, "reason_codes": [reason], "priority_band": band,
            "adjudication_basis": "model_row_adjudication",
        })
    counts = Counter(r["admission"] for r in records)
    adjudication = {
        "schema": "forseti.reddit.weekly_problem_adjudication.v1",
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "run_name": reader.get("run_name"), "read_policy_id": READ_POLICY_ID,
        "method": "row-level model adjudication of every reader candidate via run_reddit_weekly_pipeline",
        "reader_path": str(reader_path), "reader_sha256": hashlib.sha256(raw).hexdigest(),
        "coverage": {"review_pool": len(rows), "rows_adjudicated": len(records)},
        "admission_counts": dict(counts), "pass_count": counts["yes"] + counts["borderline"],
        "decisions": records,
    }
    adjudication_path = run_dir / "problem_adjudication_v1.json"
    _write_json(adjudication_path, adjudication)
    manifest = build_manifest(run_dir, adjudication_path)
    return {"rows": len(records), "counts": dict(counts), "admitted": manifest["coverage"]["admitted"],
            "batches": math.ceil(manifest["coverage"]["admitted"] / BATCH_SIZE)}


def _wave(record: dict) -> str:
    if record["admission"] == "yes":
        return "high_priority" if record["priority_band"] == "high" else "explicit_evidence_yes"
    return "borderline_resolution"


def build_manifest(run_dir: Path, adjudication_path: Path) -> dict:
    raw = adjudication_path.read_bytes()
    decisions = json.loads(raw)["decisions"]
    admitted = [r for r in decisions if r["admission"] in {"yes", "borderline"}]
    admitted.sort(key=lambda r: (WAVES.index(_wave(r)), -(r["listing_snapshot"]["comments"] or 0), r["thread_url"]))
    pending = [{**r, "deep_dive_order": i, "capture_wave": _wave(r)} for i, r in enumerate(admitted, start=1)]
    counts = Counter(r["admission"] for r in decisions)
    manifest = {
        "schema": "forseti.reddit.weekly_deep_dive_manifest.v1",
        "source_adjudication": str(adjudication_path),
        "source_adjudication_sha256": hashlib.sha256(raw).hexdigest(),
        "methodology_id": METHODOLOGY_ID, "decision_frame": DECISION_FRAME, "read_policy_id": READ_POLICY_ID,
        "coverage": {"adjudicated": len(decisions), "admitted": len(pending), "yes": counts["yes"],
                     "borderline": counts["borderline"], "suppressed_no": counts["no"],
                     "already_captured_admitted": 0, "pending_capture": len(pending)},
        "ordering": list(WAVES), "existing_admitted_captures": [], "pending": pending,
    }
    _write_json(run_dir / "deep_dive_manifest_v1.json", manifest)
    for start in range(0, len(pending), BATCH_SIZE):
        slots = [{"slot_id": f"deep_{r['deep_dive_order']:04d}", "url": r["thread_url"].split("?")[0] + BEST_SORT}
                 for r in pending[start:start + BATCH_SIZE]]
        _write_json(run_dir / "capture-batches" / f"batch_{start // BATCH_SIZE + 1:03d}.json", slots)
    return manifest


# ---------------------------------------------------------------- capture


def _batch_numbers(run_dir: Path, first: int | None, last: int | None) -> list[int]:
    numbers = sorted(int(p.stem.split("_")[1]) for p in (run_dir / "capture-batches").glob("batch_*.json"))
    return [n for n in numbers if (first is None or n >= first) and (last is None or n <= last)]


def _summary(output_root: Path) -> dict | None:
    path = output_root / "batch_summary.json"
    return _read_json(path) if path.is_file() else None


def _successes(summary: dict) -> dict[str, str]:
    return {r["slot_id"]: r["packet_dir"] for r in summary.get("results", [])
            if r.get("capture_exit") == 0 and r.get("content_record_preserved") and r.get("packet_dir")}


def _refused(summary: dict) -> bool:
    return (bool(summary.get("circuit_breaker", {}).get("tripped"))
            or bool(summary.get("access_diagnostic_count"))
            or bool(summary.get("access_diagnostic_failure_count"))
            or any(r.get("navigation_http_status") is not None
                   or r.get("access_diagnostic_status") in {"preserved", "failed"}
                   for r in summary.get("results", [])))


RunBatch = Callable[[Path, Path, bool], None]
# Reddit's own notice on a thread page whose post is gone. A block or challenge page never carries it.
SOURCE_UNAVAILABLE = re.compile(r"Sorry, this post (?:was|has been) (?:deleted|removed)[^.\n]*")
UNAVAILABLE_SLOTS = "unavailable_slots.json"


def _source_unavailable(summary: dict) -> dict[str, dict]:
    """Failed slots whose preserved page text is Reddit's deleted/removed-post notice."""
    out = {}
    for r in summary.get("results", []):
        if r.get("capture_exit") == 0 or not r.get("packet_dir"):
            continue
        for path in Path(r["packet_dir"]).glob("raw/*visible_text.txt"):
            if match := SOURCE_UNAVAILABLE.search(path.read_text(encoding="utf-8", errors="replace")):
                out[r["slot_id"]] = {"slot_id": r["slot_id"], "url": r.get("url"), "status": "source_deleted_or_removed",
                                     "evidence": match.group(0), "packet_dir": r["packet_dir"]}
    return out


def _unavailable(run_dir: Path) -> list[dict]:
    path = run_dir / "captures" / UNAVAILABLE_SLOTS
    return _read_json(path) if path.is_file() else []


def capture(run_dir: Path, run_batch: RunBatch, *, first: int | None, last: int | None) -> dict:
    captured = 0
    for n in _batch_numbers(run_dir, first, last):
        tag = f"{n:03d}"
        index_path = run_dir / "captures" / f"batch_{tag}_index.json"
        if index_path.is_file():
            continue
        slots = _read_json(run_dir / "capture-batches" / f"batch_{tag}.json")
        surface = run_dir / "captures" / f"batch_{tag}_surface"
        summary = _summary(surface)
        if summary is None:
            run_batch(run_dir / "capture-batches" / f"batch_{tag}.json", surface, (surface / "batch_progress.jsonl").is_file())
            summary = _summary(surface)
        if summary is None or _refused(summary):
            raise PipelineError(f"capture batch {tag} refused or produced no summary; stop and inspect {surface}")
        found = _successes(summary)
        gone = {k: v for k, v in _source_unavailable(summary).items() if k not in found}
        missing = [s for s in slots if s["slot_id"] not in found and s["slot_id"] not in gone]
        if missing:
            retry_root = run_dir / "captures" / f"batch_{tag}_retry"
            retry_list = run_dir / "captures" / f"batch_{tag}_retry_urls.json"
            _write_json(retry_list, missing)
            run_batch(retry_list, retry_root, (retry_root / "batch_progress.jsonl").is_file())
            retry = _summary(retry_root)
            if retry is None or _refused(retry):
                raise PipelineError(f"capture batch {tag} retry refused; stop and inspect {retry_root}")
            found.update(_successes(retry))
            gone.update({k: v for k, v in _source_unavailable(retry).items() if k not in found})
        still = [s["slot_id"] for s in slots if s["slot_id"] not in found and s["slot_id"] not in gone]
        if still:
            raise PipelineError(f"capture batch {tag} still missing {still} after one retry")
        if gone:
            known = {u["slot_id"] for u in _unavailable(run_dir)}
            _write_json(run_dir / "captures" / UNAVAILABLE_SLOTS,
                        _unavailable(run_dir) + [{**u, "batch": tag} for k, u in gone.items() if k not in known])
        _write_json(index_path, {s["slot_id"]: found[s["slot_id"]] for s in slots if s["slot_id"] in found})
        captured += 1
    return {"batches_captured": captured}


def thread_batch_runner(*, cdp_endpoint: str, data_root: str, seed_prefix: str) -> RunBatch:
    def run(url_list: Path, output_root: Path, resume: bool) -> None:
        command = [
            sys.executable, str(THREAD_BATCH_RUNNER), "--url-list", str(url_list), "--output-root", str(output_root),
            "--transport", "www_realchrome", "--cdp-endpoint", cdp_endpoint, "--data-root", data_root,
            "--decision-question", CAPTURE_QUESTION, "--max-urls", str(BATCH_SIZE), "--timeout-seconds", "60",
            "--cadence-mode", "bounded_jitter", "--cadence-basis", "cycle", "--cadence-window-seconds", "414",
            "--cadence-min-gap-seconds", "31", "--cadence-max-gap-seconds", "46",
            "--cadence-random-seed", str(int(seed_prefix + (re.sub(r"\D", "", url_list.stem) or "0"))),
            "--refusal-circuit-breaker", "3",
            "--retention-mode", "content",
        ]
        if resume:
            command.append("--resume")
        subprocess.run(command, cwd=HARNESS, check=False)

    return run


# ---------------------------------------------------------------- read


def _score(comment: dict) -> int | None:
    try:
        return int(str(comment.get("score_state")).strip())
    except (TypeError, ValueError):
        return None


def render_thread(slot_id: str, row: dict, record: dict) -> str:
    post = record.get("post", {})
    comments = [c for c in record.get("comments", []) if isinstance(c, dict)]
    n = len(comments)
    size = min(n, max(10, min(50, math.ceil(n * 0.10)))) if n else 0
    indexed = list(enumerate(comments))
    scored = sorted((p for p in indexed if _score(p[1]) is not None), key=lambda p: (-_score(p[1]), p[0]))
    cohort = (scored + [p for p in indexed if _score(p[1]) is None])[:size]
    in_cohort = {i for i, _ in cohort}
    remainder = [c for i, c in indexed if i not in in_cohort]

    def line(c: dict) -> str:
        extra = "" if c.get("comment_posture") == "present" else f" [{c.get('comment_posture')}]"
        return f"[{c.get('comment_id')}] u/{c.get('author_state')} s={c.get('score_state')} d={c.get('depth')}{extra} | {_flat(c.get('body_text'))}"

    out = [
        "#" * 60,
        f"THREAD {row['thread_id']} | {slot_id} | r/{row['subreddit']} | listing={row['admission']}",
        f"title: {_flat(record.get('thread', {}).get('title'))}",
        f"OP u/{post.get('author_state')} s={post.get('score_state')}",
        f"post: {_flat(post.get('body_text')) or '(no text body)'}",
        f"captured {n} of {record.get('comment_completeness', {}).get('declared_total_comments')} declared comments",
        f"--- COHORT ({len(cohort)}) ---", *[line(c) for _, c in cohort],
    ]
    for start in range(0, len(remainder), 25):
        chunk = remainder[start:start + 25]
        out.append(f"--- BATCH {start // 25 + 1} ({len(chunk)}) ---")
        out += [line(c) for c in chunk]
    out.append(f"--- END {row['thread_id']}: cohort={len(cohort)} remainder={len(remainder)} total={n} ---")
    return "\n".join(out)


_STR = {"type": "string"}
_STRS = {"type": "array", "items": _STR}
READ_SCHEMA = {
    "type": "object",
    "properties": {"threads": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "thread_id": _STR,
            "admission": {"type": "string", "enum": ["yes", "no"]},
            "core_problem": _STR, "commercial_signal": _STR,
            "evidence_strength": {"type": "string", "enum": ["low", "medium", "high"]},
            "contribution_class": {"type": "string", "enum": ["excluded_after_read", "usable_only", "ordinary_corroboration", "material_addition"]},
            "caveats": _STRS,
            "named_brands": {"type": "array", "items": {"type": "object", "properties": {
                "brand": _STR, "product": {"type": ["string", "null"]},
                "context": {"type": "string", "enum": ["failure", "praise", "comparison", "substitution", "switching", "price", "access", "purchase", "recommendation", "alleged_problem", "proposed_solution", "neutral_mention"]},
            }, "required": ["brand", "product", "context"], "additionalProperties": False}},
            "where_customers_go": _STRS, "workarounds_or_substitutions": _STRS,
            "quote_comment_ids": {"type": "array", "items": _STR, "maxItems": 2},
            "reason_codes": _STRS,
            "priority": {"type": "string", "enum": ["high", "normal", "low"]},
            "comments_reviewed": {"type": "integer", "minimum": 0},
            "stop_reason": {"type": "string", "enum": ["corpus_exhausted", "decision_relevant_novelty_plateau"]},
            "consecutive_no_value_batches": {"type": "integer", "minimum": 0},
            "claims": {"type": "array", "items": {"type": "object", "properties": {
                "claim_id": _STR, "statement": _STR,
                "evidence_kind": {"type": "string", "enum": ["individual", "recurrence", "map_or_shortlist", "factual_or_safety", "dispute"]},
                "corroboration_status": {"type": "string", "enum": ["lead", "emerging", "corroborated", "sufficient", "not_applicable"]},
                "support_comment_ids": {"type": "array", "items": _STR, "maxItems": 5},
                "counter_comment_ids": _STRS,
            }, "required": ["claim_id", "statement", "evidence_kind", "corroboration_status", "support_comment_ids", "counter_comment_ids"], "additionalProperties": False}},
        },
        "required": ["thread_id", "admission", "core_problem", "commercial_signal", "evidence_strength", "contribution_class",
                     "caveats", "named_brands", "where_customers_go", "workarounds_or_substitutions", "quote_comment_ids",
                     "reason_codes", "priority", "comments_reviewed", "stop_reason", "consecutive_no_value_batches", "claims"],
        "additionalProperties": False,
    }}},
    "required": ["threads"],
    "additionalProperties": False,
}


def build_extract(judgment: dict, row: dict, packet_dir: str, content_record: Path, record: dict) -> dict:
    """Combine model judgments with script-owned fields and validate with the finalizer's check."""
    tid = row["thread_id"]
    by_id = {c.get("comment_id"): c for c in record.get("comments", []) if isinstance(c, dict)}
    quotes = []
    for cid in judgment["quote_comment_ids"]:
        if cid not in by_id:
            raise PipelineError(f"quote comment {cid} is not in the content record")
        body = str(by_id[cid].get("body_text") or "")
        words = list(re.finditer(r"\S+", body))
        end = words[min(len(words), 30) - 1].end() if words else 0
        quotes.append({"comment_id": cid, "text": body[:end] + (" …" if len(words) > 30 else "")})
    completeness = record.get("comment_completeness", {})
    caveats = list(judgment["caveats"])
    caveats.append(f"surface capture: {completeness.get('comments_captured')} of {completeness.get('declared_total_comments')} comments")
    extract = {
        "thread_id": tid, "url": row["thread_url"], "subreddit": row["subreddit"],
        "packet_dir": packet_dir, "content_record": str(content_record), "comment_completeness": completeness,
        "admission": judgment["admission"], "core_problem": judgment["core_problem"],
        "commercial_signal": judgment["commercial_signal"], "evidence_strength": judgment["evidence_strength"],
        "contribution_class": judgment["contribution_class"], "caveats": caveats,
        "named_brands": judgment["named_brands"], "where_customers_go": judgment["where_customers_go"],
        "workarounds_or_substitutions": judgment["workarounds_or_substitutions"], "quotes": quotes,
        "reason_codes": judgment["reason_codes"], "priority": judgment["priority"],
        "evidence_read_receipt": {
            "schema": EVIDENCE_READ_RECEIPT_SCHEMA, "policy_id": READ_POLICY_ID,
            "comments_reviewed": judgment["comments_reviewed"], "stop_reason": judgment["stop_reason"],
            "consecutive_no_value_batches": judgment["consecutive_no_value_batches"], "claims": judgment["claims"],
        },
    }
    if not extract["core_problem"].strip():
        raise PipelineError("core_problem is empty")
    try:
        _validated_evidence_read_receipt(extract=extract, content_record=record, thread_id=tid,
                                         admission=extract["admission"], manifest_read_policy_id=READ_POLICY_ID)
    except ValueError as exc:
        raise PipelineError(str(exc)) from exc
    return extract


def read_batch(run_dir: Path, tag: str, call: ModelCall) -> dict:
    manifest = _read_json(run_dir / "deep_dive_manifest_v1.json")
    by_slot = {f"deep_{int(r['deep_dive_order']):04d}": r for r in manifest["pending"]}
    index = _read_json(run_dir / "captures" / f"batch_{tag}_index.json")
    items = []
    for slot_id, packet_dir in index.items():
        row = by_slot[slot_id]
        content_record = Path(packet_dir) / "raw" / "01_content_record.json"
        record = _read_json(content_record)
        if record.get("thread", {}).get("thread_id") != row["thread_id"]:
            raise PipelineError(f"{slot_id} content record thread mismatch")
        items.append((slot_id, row, packet_dir, content_record, record))

    if not items:
        (run_dir / f"batch_{tag}_extracts_v1.jsonl").write_text("", encoding="utf-8")
        return {"batch": tag, "yes": 0, "no": 0, "repaired_threads": 0}

    def ask(subset: list[tuple], name: str, note: str = "") -> tuple[dict[str, dict], str | None]:
        prompt = READ_BRIEF + "\n\n".join(render_thread(s, r, rec) for s, r, _, _, rec in subset) + "\n" + note
        receipt = receipted_call(call, run_dir / "calls" / "read" / f"batch_{tag}{name}.json", prompt, READ_SCHEMA)
        _append_usage(run_dir, {"stage": "read", "unit": f"batch_{tag}{name}", "threads": len(subset),
                                "prompt_sha256": receipt["prompt_sha256"], **receipt["usage"]})
        returned = receipt["output"]["threads"]
        ids = [j["thread_id"] for j in returned]
        expected = {r["thread_id"] for _, r, _, _, _ in subset}
        coverage_error = ("model judgments do not cover threads exactly"
                          if len(ids) != len(set(ids)) or set(ids) != expected else None)
        return {j["thread_id"]: j for j in returned}, coverage_error

    judgments, coverage_error = ask(items, "")
    extracts: dict[str, dict] = {}
    errors: dict[str, str] = ({row["thread_id"]: coverage_error for _, row, _, _, _ in items}
                              if coverage_error else {})
    for slot_id, row, packet_dir, content_record, record in items:
        judgment = judgments.get(row["thread_id"])
        try:
            if judgment is None:
                raise PipelineError("no judgment returned for this thread")
            extracts[row["thread_id"]] = build_extract(judgment, row, packet_dir, content_record, record)
        except PipelineError as exc:
            errors[row["thread_id"]] = str(exc)
    if errors:
        retry_items = [item for item in items if item[1]["thread_id"] in errors]
        note = "\nYour previous answer for these threads was rejected:\n" + "\n".join(f"- {t}: {e}" for t, e in errors.items()) + "\nFix exactly these problems.\n"
        judgments, coverage_error = ask(retry_items, "_repair", note)
        if coverage_error:
            raise PipelineError(f"batch {tag} repair {coverage_error}")
        for slot_id, row, packet_dir, content_record, record in retry_items:
            judgment = judgments.get(row["thread_id"])
            if judgment is None:
                raise PipelineError(f"batch {tag} thread {row['thread_id']} missing after repair")
            extracts[row["thread_id"]] = build_extract(judgment, row, packet_dir, content_record, record)
    lines = [json.dumps(extracts[item[1]["thread_id"]], ensure_ascii=False) for item in items]
    (run_dir / f"batch_{tag}_extracts_v1.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    counts = Counter(e["admission"] for e in extracts.values())
    return {"batch": tag, "yes": counts["yes"], "no": counts["no"], "repaired_threads": len(errors)}


def read(run_dir: Path, call: ModelCall, *, first: int | None, last: int | None, workers: int) -> dict:
    todo = [f"{n:03d}" for n in _batch_numbers(run_dir, first, last)
            if (run_dir / "captures" / f"batch_{n:03d}_index.json").is_file()
            and not (run_dir / f"batch_{n:03d}_extracts_v1.jsonl").is_file()]
    results, failures = [], {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(read_batch, run_dir, tag, call): tag for tag in todo}
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except PipelineError as exc:
                failures[futures[future]] = str(exc)
    if failures:
        raise PipelineError(f"read failed for batches {failures}; completed {len(results)}")
    return {"batches_read": len(results), "yes": sum(r["yes"] for r in results), "no": sum(r["no"] for r in results),
            "repaired_threads": sum(r["repaired_threads"] for r in results)}


# ---------------------------------------------------------------- scope


def scope(run_dir: Path, last_batch: int) -> dict:
    manifest = _read_json(run_dir / "deep_dive_manifest_v1.json")
    slots = set()
    for n in range(1, last_batch + 1):
        slots.update(s["slot_id"] for s in _read_json(run_dir / "capture-batches" / f"batch_{n:03d}.json"))
        if not (run_dir / f"batch_{n:03d}_extracts_v1.jsonl").is_file():
            raise PipelineError(f"batch {n:03d} has no extracts")
    gone = [u for u in _unavailable(run_dir) if u["slot_id"] in slots]
    slots -= {u["slot_id"] for u in gone}
    pending = [r for r in manifest["pending"] if f"deep_{int(r['deep_dive_order']):04d}" in slots]
    out = run_dir / f"finalize-{len(pending)}"
    narrowed = {**manifest, "pending": pending, "coverage": {
        **manifest["coverage"], "admitted": len(pending), "pending_capture": len(pending),
        "full_admitted_before_scope_reduction": manifest["coverage"]["admitted"],
        "owner_dive_scope": f"owner scope: batches 1-{last_batch} ({len(pending)} threads) in manifest order",
        "source_unavailable_at_capture": [{k: u[k] for k in ("slot_id", "url", "status", "evidence")} for u in gone],
    }}
    _write_json(out / "deep_dive_manifest_v1.json", narrowed)
    for n in range(1, last_batch + 1):
        shutil.copy2(run_dir / f"batch_{n:03d}_extracts_v1.jsonl", out / f"batch_{n:03d}_extracts_v1.jsonl")
    return {"finalize_dir": str(out), "threads": len(pending)}


# ---------------------------------------------------------------- consolidate
# Script-only aids for writing the weekly read from a finalized catalog: no model call, no lake write.

PROBLEM_CONTEXTS = {"failure", "alleged_problem", "switching", "substitution", "price", "access"}


def _catalog(finalize_dir: Path) -> list[dict]:
    paths = sorted(finalize_dir.glob("reddit_top100_*_threads.jsonl"))
    if len(paths) != 1:
        raise PipelineError(f"expected one finalized catalog in {finalize_dir}, found {len(paths)}")
    return [json.loads(line) for line in paths[0].read_text(encoding="utf-8").splitlines() if line.strip()]


def _reporters(row: dict) -> int:
    """Best finalizer-derived independent-reporter count over the row's recurrence claims."""
    return max((c["independent_reporters"]["count"] for c in row.get("evidence_read_receipt", {}).get("claims", [])
                if c["evidence_kind"] == "recurrence"), default=0)


def delta(finalize_dir: Path, previous: Path | None = None) -> str:
    """Card candidates a catalog adds over an earlier one (all of it without one); old threads by ID only."""
    rows = _catalog(finalize_dir)
    old_ids = {r["thread_id"] for r in _catalog(previous)} if previous else set()
    new_yes = [r for r in rows if r["thread_id"] not in old_ids and r["admission"] == "yes"]
    out = [json.dumps({"threads": len(rows), "new": sum(r["thread_id"] not in old_ids for r in rows), "new_yes": len(new_yes),
                       "new_contribution": dict(Counter(r.get("contribution_class") for r in new_yes))})]
    brands: dict[str, dict[str, list[dict]]] = defaultdict(lambda: {"old": [], "new": []})
    for r in rows:
        if r["admission"] != "yes":
            continue
        names = {str(b.get("brand", "")).strip().lower() for b in r.get("named_brands") or [] if b.get("context") in PROBLEM_CONTEXTS}
        for name in names - {""}:
            brands[name]["old" if r["thread_id"] in old_ids else "new"].append(r)
    out.append("\n== brands where new threads add >=2 threads or a >=3-reporter thread")
    for name, hits in sorted(brands.items(), key=lambda kv: (-len(kv[1]["new"]), kv[0])):
        if len(hits["new"]) >= 2 or any(_reporters(r) >= 3 for r in hits["new"]):
            out.append(f"-- {name}: new {len(hits['new'])}, old {len(hits['old'])} [{' '.join(r['thread_id'] for r in hits['old'][:8])}]")
            out += [f"   {r['thread_id']} r/{r['subreddit']} n={_reporters(r)} :: {r['core_problem'][:110]}" for r in hits["new"]]
    shown = [r for r in new_yes if _reporters(r) >= 2 or r.get("contribution_class") == "material_addition"]
    out.append(f"\n== new yes threads with n>=2 or material_addition ({len(shown)} of {len(new_yes)})")
    out += [f"{r['thread_id']} r/{r['subreddit']} n={_reporters(r)} {r.get('contribution_class')} :: {r['core_problem'][:130]}"
            for r in sorted(shown, key=lambda r: (r["subreddit"].lower(), -_reporters(r)))]
    return "\n".join(out) + "\n"


def evidence(finalize_dir: Path, thread_ids: Sequence[str]) -> str:
    """Card-ready evidence per thread: claims with reporter handles, verbatim quotes, caveats."""
    rows = {r["thread_id"]: r for r in _catalog(finalize_dir)}
    out = []
    for tid in thread_ids:
        r = rows.get(tid)
        if r is None:
            out.append(f"== {tid}: NOT IN CATALOG")
            continue
        listing, completeness = r["listing"], r.get("comment_completeness", {})
        out.append(f"== {tid} r/{listing['subreddit']} [{r['admission']}] comments={listing['comments']} "
                   f"captured={completeness.get('comments_captured')} :: {listing['title'][:90]}")
        out.append(f"  problem: {r['core_problem']}")
        out.append(f"  go: {r.get('where_customers_go')}")
        for c in r.get("evidence_read_receipt", {}).get("claims", []):
            reporters = c["independent_reporters"]
            if c["evidence_kind"] in {"recurrence", "factual_or_safety", "dispute"} or reporters["count"] >= 2:
                out.append(f"  claim[{c['evidence_kind']}/{c['corroboration_status']}] n={reporters['count']} "
                           f"{reporters['handles']}: {c['statement']}")
        out += [f"  quote {q['comment_id']}: \"{q['text']}\"" for q in r.get("quotes", [])[:2]]
        caveats = [c for c in r.get("caveats", []) if "surface capture" not in c.lower()][:2]
        if caveats:
            out.append(f"  caveats: {caveats}")
    return "\n".join(out) + "\n"


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("’", "'").replace("…", "...")).strip()


def check(finalize_dir: Path, read_path: Path) -> dict:
    """Fail unless every cited thread is a yes row and every card quote is verbatim source text."""
    rows = {r["thread_id"]: r for r in _catalog(finalize_dir)}
    text = read_path.read_text(encoding="utf-8")
    id_lengths = {len(t) for t in rows}
    cited = sorted({t for t in re.findall(r"`([a-z0-9]+)`", text)
                    if t in rows or (len(t) in id_lengths and any(ch.isdigit() for ch in t))})
    problems = [f"cited thread {t} is not in the catalog" for t in cited if t not in rows]
    problems += [f"cited thread {t} is admission={rows[t]['admission']}, not yes"
                 for t in cited if t in rows and rows[t]["admission"] != "yes"]
    corpus = []
    for r in rows.values():
        corpus += [_normalized(q["text"]) for q in r.get("quotes", [])]
        record = Path(r.get("content_record") or "")
        if record.is_file():
            corpus += [_normalized(c.get("body_text") or "") for c in _read_json(record).get("comments", [])]
    quotes = [q for line in text.splitlines() if "**Quotes:**" in line
              for q in re.findall(r"\"(.+?)\"(?: ·|$)", line.split("**Quotes:**", 1)[1])]
    problems += [f"quote is not verbatim source text: {q[:80]}" for q in quotes
                 if not any(_normalized(q).rstrip(".").rstrip("…") in c for c in corpus)]
    if problems:
        raise PipelineError("weekly read check failed: " + "; ".join(problems))
    yes = [r for r in rows.values() if r["admission"] == "yes"]
    return {"cited_threads": len(cited), "quotes": len(quotes), "yes": len(yes), "no": len(rows) - len(yes),
            "contribution": dict(Counter(r.get("contribution_class") for r in yes))}


# ---------------------------------------------------------------- CLI


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    def model_args(p: argparse.ArgumentParser, effort: str) -> None:
        p.add_argument("--model", default="sonnet")
        p.add_argument("--effort", default=effort)
        p.add_argument("--timeout-seconds", type=float, default=900)
        p.add_argument("--workers", type=int, default=4)
        p.add_argument("--claude-executable")
        p.add_argument("--bare", action="store_true", help="Pass --bare (API-key environments only; skips the logged-in account).")

    a = sub.add_parser("adjudicate")
    a.add_argument("--run-dir", type=Path, required=True)
    a.add_argument("--reader-json", type=Path, required=True)
    a.add_argument("--chunk-rows", type=int, default=150)
    model_args(a, "medium")
    c = sub.add_parser("capture")
    c.add_argument("--run-dir", type=Path, required=True)
    c.add_argument("--cdp-endpoint", required=True)
    c.add_argument("--data-root", required=True)
    c.add_argument("--first", type=int)
    c.add_argument("--last", type=int)
    r = sub.add_parser("read")
    r.add_argument("--run-dir", type=Path, required=True)
    r.add_argument("--first", type=int)
    r.add_argument("--last", type=int)
    model_args(r, "medium")
    s = sub.add_parser("scope")
    s.add_argument("--run-dir", type=Path, required=True)
    s.add_argument("--last-batch", type=int, required=True)
    d = sub.add_parser("delta", help="Print card candidates from a finalized catalog (script only).")
    d.add_argument("--finalize-dir", type=Path, required=True)
    d.add_argument("--previous", type=Path, help="An earlier finalize dir of the same run; its threads are cited by ID only.")
    e = sub.add_parser("evidence", help="Print card-ready claims, reporter handles and quotes for thread IDs.")
    e.add_argument("--finalize-dir", type=Path, required=True)
    e.add_argument("thread_ids", nargs="+")
    k = sub.add_parser("check", help="Fail unless the weekly read cites only yes threads and verbatim quotes.")
    k.add_argument("--finalize-dir", type=Path, required=True)
    k.add_argument("--read", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    with exit_on_failure(parser, runner_name="reddit weekly pipeline",
                         expected=(PipelineError, OSError, ValueError, json.JSONDecodeError)):
        if args.command in {"delta", "evidence"}:
            sys.stdout.reconfigure(encoding="utf-8")
            print(delta(args.finalize_dir, args.previous) if args.command == "delta"
                  else evidence(args.finalize_dir, args.thread_ids), end="")
            return 0
        if args.command == "check":
            print(json.dumps(check(args.finalize_dir, args.read), indent=2))
            return 0
        run_dir = args.run_dir.resolve()
        run_dir.mkdir(parents=True, exist_ok=True)
        if args.command in {"adjudicate", "read"}:
            call = claude_structured_call_factory(model=args.model, effort=args.effort, timeout=args.timeout_seconds,
                                                  executable=args.claude_executable, bare=args.bare, cwd=run_dir)
        if args.command == "adjudicate":
            result = adjudicate(run_dir, args.reader_json, call, chunk_rows=args.chunk_rows, workers=args.workers)
        elif args.command == "capture":
            result = capture(run_dir, thread_batch_runner(cdp_endpoint=args.cdp_endpoint, data_root=args.data_root,
                                                          seed_prefix=re.sub(r"\D", "", run_dir.name)[-6:] or "1"),
                             first=args.first, last=args.last)
        elif args.command == "read":
            result = read(run_dir, call, first=args.first, last=args.last, workers=args.workers)
        else:
            result = scope(run_dir, args.last_batch)
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
