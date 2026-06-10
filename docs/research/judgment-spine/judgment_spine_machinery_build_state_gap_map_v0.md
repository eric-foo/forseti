# Judgment Spine — Machinery Build-State & Run-Executability Gap Map v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: >
  Verified built-vs-gap inventory of the Judgment Spine machinery as of
  2026-06-09, grounded by reading orca-harness/ directly (not the orientation
  docs, which understated some of it). Serves as the design-completion predicate
  for the re-framed judgment-lane anchor and as the owner handoff for the
  invest-vs-bank / authorize-a-run decision. Capped at product-learning; mints
  no tier and authorizes no run.
use_when:
  - Checking what judgment machinery is actually built vs a named gap before planning a build.
  - Deciding whether the design-completion anchor is met (no row left undefined).
  - Framing the authorize-a-real-run / invest-vs-bank owner decision.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
  - docs/research/judgment-spine/ideal_judgment_quality_run_and_current_position_v0.md
  - docs/product/judgment_quality_promotion_operating_model_v0.md
branch_or_commit: ecr-sp3-timing-deriver-slice1 (working tree dirty — concurrent lanes; build-state read directly from orca-harness/ on 2026-06-09)
stale_if:
  - A contestant-execution / authorized live-run record, SP-5 finalizer, JSG-01 EvidenceUnit binding, or case-finder is built (then update the affected row).
  - orca-harness/ scoring, runners, schemas, or ecr modules are materially restructured.
```

## What this is

A build-state inventory verified by **reading `orca-harness/` directly** on
2026-06-09, not by trusting the orientation docs (which had understated parts of
it). It is the **design-completion predicate** for the re-framed anchor: the
anchor is met when every row below is either *built + verified* or a *named build
gap with its authorization owner*, and the orientation docs match this. It caps
at **product-learning**; it authorizes no run and mints no tier.

## Built vs gap (verified against the code)

| Component | State | Evidence |
| --- | --- | --- |
| Scoring (JSG-07) | **Built + tested** | `scoring/band_scorer.py`, `mapping_table.py`, `evidence_id_checker.py`; `runners/run_case.py` (the "fixed Step A case scorer") |
| Memorization probe | **Built** | `runners/run_memorization_probe.py` (+ `_raw_api`), `schemas/probe_models.py` |
| No-tools isolation | **Built as a recording schema** (records evidence; does not enforce) | `ContestantExecutionIsolation` etc.; `contestant_no_tools_execution_contract_v0.md` is docs-only |
| Schemas / reports / tests | **Built** | `schemas/{case,scoring,probe,judgement}_models.py`, `reports/case_report.py`, unit + integration + contract tests |
| ECR derivers (SP-1/2/3/6) | **Built; bind no `EvidenceUnit`** | `ecr/deriver.py` — four posture derivers off the `SourceCapturePacket` |
| SP-5 finalizer | **Partial — finalizer half built** | `schemas/finalization_models.py` (committed `a37f896`): the `FinalizationReceipt` model + a validate-only, block-don't-repair consumer (binding_hash via `canonical_yaml_hash`; current-designation via per-receipt ULID + `supersedes`); 23 tests; cross-family-reviewed. **Remaining gap:** the `EvidenceUnit` binding + a case packet carrying a `FinalizationReceipt` (+ D2). JSG-01 stays FROZEN |
| JSG-01 `EvidenceUnit` binding | **Gap** | derivers bind no `EvidenceUnit`; no case packet yet carries the derived fields → JSG-01 stays FROZEN |
| Blind-judgment contestant execution under proven isolation | **Gap (by-hand; no live runner for the blind judgment)** | the probe has a raw-API live runner (`run_memorization_probe_raw_api.py`); the blind judgment has none — needs an authorized live-execution surface + isolation-receipt binding |
| An authorized real (non-synthetic) run | **None** | the 50+ `_test_runs/` are `cases/plumbing/...` with a `fixed_contestant` (canned `blind_judgement.yaml`) — synthetic smoke tests |
| Case-finder (post-cutoff / prospective sourcing) | **Gap** | only a frame doc (`docs/product/orca_memorization_resistant_case_finder_frame_v0.md`) |

## The corrected gap (what actually lifts the cap)

The harness keeps its **scoring and dry paths model-free**: `tests/contract/test_no_llm_imports.py`
bars the LLM **SDK import packages** (`openai`/`anthropic`/`litellm`/`langchain`) across
`scoring/`, `reports/`, `runners/`, `schemas/`. That bars *imports*, not raw HTTP —
`runners/run_memorization_probe_raw_api.py` makes opt-in live calls to the OpenAI/Anthropic
endpoints via raw `urllib` (guarded by `--allow-live-provider-call`). So a guarded live-API
path **already exists for the memorization probe**. What is still missing is the equivalent
for the **blind judgment**: a live-execution surface (raw API is the accepted one) that
produces the sealed blind judgment under proven isolation, **bound to an auditable
live-execution record** (today it is by-hand) — *plus* the JSG-01
`EvidenceUnit` binding and a case-finder. (The **SP-5 finalizer half is now built** —
`schemas/finalization_models.py`, `a37f896` — but no case packet yet carries a
`FinalizationReceipt`, so it does not lift the cap on its own.) No authorized real-case run exists today.

This corrects an earlier framing (in the ideal-JQ reference) that named the
memorization-probe runner and scoring as gaps; both are built.

## Completion predicate (for the anchor)

Design-complete = every row above is either *built + verified* or a *named gap
with its authorization owner*, and the orientation docs (consolidation map,
ideal-JQ, conductor JSG-01 row) match this inventory. It does **not** mean a run
has happened or that the tier is lifted.

## Non-Claims

- Not validation, readiness, buyer-proof, or judgment-quality evidence; caps at product-learning.
- Mints no claim tier; authorizes no model run, live execution, fixture admission, or build.
- Build-state verified by reading the code at the stated worktree; reread if the harness changes.
- A map of build-state; each component is owned by its code module / owner doc, which wins on any conflict.
