#!/usr/bin/env python3
"""Score an external-arm blind run from a pasted model reply.

PURPOSE
  Turn one external contestant's pasted exam reply into a scored Batch 2 run with
  no hand-assembly of metadata. You paste the model's answer into a file; this
  wraps it with the required blind_judgement metadata, validates it, writes it to
  the case's runs/<contestant_id>/run_001/blind_judgement.yaml, and scores it via
  the pinned key (run_case.run_fixed_case). Built for the GPT-5.5 and Grok 4 arms.

WHAT YOU DO
  1. Run the case's *_EXAM.txt through the model (fresh session, web/tools OFF).
  2. Save the model's WHOLE reply (the ```yaml block + the RECOGNITION line) to a file.
  3. Run this:
       python forseti-harness/runners/score_external_run.py \
         --model gpt55 --case nueco --reply path/to/reply.txt
     Add --dry-run first to preview without writing/scoring.

WHAT IT DOES NOT DO
  It never invents a contestant answer. It only ingests a reply you provide. The
  reply must be a genuine run of the named model; this tool does not fabricate runs.

NOTES
  - case_id is read from the case's facilitator_ledger (nueco -> b2_holdout_h7_v0).
  - prompt_hash = SHA-256 (uppercase) of the exam text (default: the assembled
    *_EXAM.txt under _scratch/batch2_external_exams/, override with --exam, or pass
    --prompt-hash directly).
  - The RECOGNITION SELF-REPORT line is captured into advisory_phase_1_fields for
    the JSG-08 tell-audit and printed so you can add it to the case findings.
  - A distinct contestant_id per model avoids the duplicate-score guard. Re-scoring
    the same (case, model, run_001) is refused unless you pass --allow-duplicate-score.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml

from harness_utils import load_yaml_file, write_yaml_file
from schemas.case_models import FacilitatorLedger
from schemas.judgement_models import BlindJudgement
from scoring.mapping_table import derive_action_band

# --- model registry (extend here for more arms) ---------------------------------
MODELS = {
    "gpt55": {"contestant_id": "gpt55_isolated_v0", "model_id": "gpt-5.5", "model_family": "openai_gpt"},
    "grok4": {"contestant_id": "grok4_isolated_v0", "model_id": "grok-4", "model_family": "xai_grok"},
    "gemini": {"contestant_id": "gemini_isolated_v0", "model_id": "gemini", "model_family": "google_gemini"},
    "qwen": {"contestant_id": "qwen_isolated_v0", "model_id": "qwen", "model_family": "alibaba_qwen"},
}

# --- case aliases -> (case_dir, exam_filename) ----------------------------------
EXAM_DIRNAME = "_scratch/batch2_external_exams"
CASES = {
    "kinderbeauty": ("kinderbeauty_box_pivot_2023_v0", "kinderbeauty_box_pivot_2023_v0__EXAM.txt"),
    "joahbeauty": ("joahbeauty_cvs_kill_2024_v0", "joahbeauty_cvs_kill_2024_v0__EXAM.txt"),
    "privatepacks": ("privatepacks_retail_retreat_v0", "privatepacks_retail_retreat_v0__EXAM.txt"),
    "selflessbyhyram": ("selflessbyhyram_target_entry_2023_v0", "selflessbyhyram_target_entry_2023_v0__EXAM.txt"),
    "sundaily": ("sundaily_gummy_pivot_v0", "sundaily_gummy_pivot_v0__EXAM.txt"),
    "imaginaryauthors": ("imaginaryauthors_sku_kills_2024_v0", "imaginaryauthors_sku_kills_2024_v0__EXAM.txt"),
    "nueco": ("nueco_fragrance_pivot_v0", "nueco_b2_holdout_h7_v0__EXAM.txt"),
    "cocokind": ("cocokind_holdprice_2025_v0", "cocokind_holdprice_2025_v0__EXAM.txt"),
    "saie": ("saie_price_increase_2025_v0", "saie_price_increase_2025_v0__EXAM.txt"),
}
# short aliases
CASES["selfless"] = CASES["selflessbyhyram"]
CASES["ia"] = CASES["imaginaryauthors"]

CONTENT_FIELDS = [
    "judgement_class",
    "decision_shape",
    "recommended_action",
    "contestant_band_claim",
    "evidence_used",
    "must_address_items_covered",
    "load_bearing_assumption",
]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _resolve_case(case_arg: str) -> tuple[str, str]:
    """Return (case_dir, exam_filename). Accept an alias or a full case_dir."""
    key = case_arg.strip().lower()
    if key in CASES:
        return CASES[key]
    for cdir, exam in CASES.values():
        if case_arg == cdir:
            return cdir, exam
    raise SystemExit(
        f"Unknown case '{case_arg}'. Use one of: {', '.join(sorted(CASES))} (or a full case dir)."
    )


def _extract_yaml_block(reply_text: str) -> dict:
    """Extract the first fenced code block from the reply and parse it as YAML."""
    m = re.search(r"```(?:ya?ml)?\s*\n(.*?)```", reply_text, re.DOTALL | re.IGNORECASE)
    raw = m.group(1) if m else reply_text  # fall back to the whole text if no fence
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise SystemExit(f"Could not parse the reply's YAML block: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("The reply's YAML block did not parse to a mapping/object.")
    return data


def _extract_recognition(reply_text: str) -> str | None:
    m = re.search(r"RECOGNITION SELF-REPORT:\s*(.+)", reply_text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def _compute_prompt_hash(exam_path: Path | None, prompt_hash: str | None) -> str:
    if prompt_hash:
        return prompt_hash.upper()
    if exam_path is None:
        raise SystemExit("Provide --exam <exam.txt> or --prompt-hash <sha256>.")
    if not exam_path.exists():
        raise SystemExit(
            f"Exam file not found: {exam_path}\n"
            "Pass --exam to point at the *_EXAM.txt you pasted, or --prompt-hash directly."
        )
    return hashlib.sha256(exam_path.read_bytes()).hexdigest().upper()


def build_blind_judgement(
    *, case_dir: Path, model_key: str, reply_text: str, prompt_hash: str, temperature: float
) -> tuple[dict, str, str | None]:
    ledger = FacilitatorLedger.model_validate(load_yaml_file(case_dir / "facilitator_ledger.yaml"))
    model = MODELS[model_key]
    reply = _extract_yaml_block(reply_text)
    recognition = _extract_recognition(reply_text)

    missing = [f for f in ("judgement_class", "decision_shape", "recommended_action") if f not in reply]
    if missing:
        raise SystemExit(f"Reply is missing required field(s): {', '.join(missing)}")

    bj: dict = {
        "case_id": ledger.case_id,
        "contestant_id": model["contestant_id"],
        "run_id": "run_001",
        "model_id": model["model_id"],
        "model_family": model["model_family"],
        "model_snapshot_if_available": None,
        "prompt_hash": prompt_hash,
        "temperature": float(temperature),
        "seed_if_supported": None,
        "harness_version": "v0_14",
    }
    for f in CONTENT_FIELDS:
        if f in reply and reply[f] is not None:
            bj[f] = reply[f]
    bj.setdefault("must_address_items_covered", [])
    bj["advisory_phase_1_fields"] = {"recognition_self_report": recognition} if recognition else {}

    BlindJudgement.model_validate(bj)  # raises on any schema problem
    return bj, ledger.case_id, recognition


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Score an external-arm blind run from a pasted model reply.")
    p.add_argument("--model", required=True, choices=sorted(MODELS), help="external contestant model")
    p.add_argument("--case", required=True, help="case alias (e.g. nueco) or full case dir")
    p.add_argument("--reply", required=True, type=Path, help="file with the model's pasted reply")
    p.add_argument("--exam", type=Path, default=None, help="exam .txt for prompt_hash (default: assembled _scratch exam)")
    p.add_argument("--prompt-hash", default=None, help="supply prompt_hash directly instead of --exam")
    p.add_argument("--temperature", type=float, default=1.0)
    p.add_argument("--dry-run", action="store_true", help="validate + preview; do not write or score")
    p.add_argument("--allow-duplicate-score", action="store_true")
    args = p.parse_args(argv)

    root = _project_root()
    case_dir_name, exam_filename = _resolve_case(args.case)
    case_dir = root / "cases" / "product_learning" / case_dir_name
    if not case_dir.exists():
        raise SystemExit(f"Case dir not found on disk: {case_dir} (run from a checkout of origin/main).")

    exam_path = args.exam if args.exam is not None else (root.parent / EXAM_DIRNAME / exam_filename)
    if not args.reply.exists():
        raise SystemExit(f"Reply file not found: {args.reply}")
    reply_text = args.reply.read_text(encoding="utf-8")
    prompt_hash = _compute_prompt_hash(None if args.prompt_hash else exam_path, args.prompt_hash)

    bj, case_id, recognition = build_blind_judgement(
        case_dir=case_dir, model_key=args.model, reply_text=reply_text,
        prompt_hash=prompt_hash, temperature=args.temperature,
    )

    band = derive_action_band(FacilitatorLedger.model_validate(load_yaml_file(case_dir / "facilitator_ledger.yaml")).frozen_band_inputs)
    level = bj["recommended_action"]["ladder_level"]
    over = max(0, level - band.action_ceiling)
    under = max(0, band.action_floor - level)
    verdict = "in-band" if (over == 0 and under == 0) else (f"OVER by {over}" if over else f"UNDER by {under}")

    print(f"case_id            : {case_id}")
    print(f"contestant_id      : {bj['contestant_id']} ({bj['model_id']})")
    print(f"prompt_hash        : {prompt_hash[:16]}...")
    print(f"recommended level  : {level}")
    print(f"band               : [{band.action_floor},{band.action_ceiling}] {band.band_status.value}  ->  {verdict}")
    print(f"recognition        : {recognition or '(none captured)'}")

    if args.dry_run:
        print("\n--- DRY RUN: assembled blind_judgement.yaml (not written) ---")
        print(yaml.safe_dump(bj, sort_keys=False, allow_unicode=True))
        print("DRY RUN ok -- re-run without --dry-run to write + score.")
        return 0

    from runners.run_case import run_fixed_case  # local import: only needed for real scoring

    run_dir = case_dir / "runs" / bj["contestant_id"] / "run_001"
    bj_path = run_dir / "blind_judgement.yaml"
    if bj_path.exists() and not args.allow_duplicate_score:
        raise SystemExit(
            f"Refusing to overwrite existing run: {bj_path}\n"
            "This (case, model, run_001) already has a judgement. Use --allow-duplicate-score to override."
        )
    write_yaml_file(bj_path, bj)
    art = run_fixed_case(case_dir, allow_duplicate_score=args.allow_duplicate_score)
    sb = art.scoring_bundle.scoring_result
    print("\n--- SCORED ---")
    print(f"in_band={sb.in_band} over_band={sb.over_band} under_band={sb.under_band} "
          f"(floor {sb.action_band_result.action_floor}, ceiling {sb.action_band_result.action_ceiling})")
    print(f"checks: ev_presence={sb.evidence_id_check_result.evidence_id_presence_pass} "
          f"pre_decision={sb.evidence_id_check_result.pre_decision_status_pass} "
          f"lb_citation={sb.evidence_id_check_result.load_bearing_claim_citation_pass} "
          f"must_address={sb.must_address_coverage_result.pass_}")
    print(f"failure_events: {[(e.failure_type, e.severity) for e in art.scoring_bundle.failure_events] or 'none'}")
    print(f"blind_judgement: {bj_path}")
    print(f"case_report    : {art.report_path}")
    print(f"score_id       : {sb.scoring_result_id} (score file is gitignored)")
    print("\nNext: add this arm's row to the case's cross_vendor_blind_run_findings_v0.md, then land via PR.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
