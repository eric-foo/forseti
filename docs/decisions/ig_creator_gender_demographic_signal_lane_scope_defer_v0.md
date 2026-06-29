# IG Reels — Creator-Gender Demographic Signal Lane — Scope + Deferral Decision (v0)

```yaml
retrieval_header_version: 1
artifact_role: Decision record (owner-scoped lane; deterministic core authorized; downstream slices deferred)
scope: >
  Captures the owner-decided scope for a SEPARATE creator-demographic signal lane over
  the IG reels social-source pipeline that tags each reel with the CREATOR's gender as a
  confidence-weighted soft lean, so product signals can be cut male-vs-female (goal:
  gender x product-stance). Records that PR 420 authorized and built the deterministic
  schema/fusion/test core only, while cleaning inference, product mapping, gender x stance
  join, capture/backfill, and calibration remain deferred behind explicit authorization.
use_when:
  - Checking what PR 420's deterministic creator-gender core slice authorizes and implements.
  - Picking up the deferred cleaning inference, product mapping, gender x stance join, capture/backfill, or calibration work.
  - Confirming that downstream creator-gender lane slices still require explicit bounded owner authorization.
authority_boundary: retrieval_only
open_next:
  - orca-harness/scoring/audience_fusion.py            # the soft-aggregation shape this lane is modeled on
  - orca-harness/scoring/product_fusion.py             # the product-STANCE lane this must NOT fold into
  - docs/decisions/product_verdict_fusion_calibration_surface_v0.md  # Pass-1<->Pass-2 calibration context the deferral waits on
  - orca-harness/cleaning/transcript_product_extractor.py  # parse_mentions: the agent-in-the-loop inference exemplar (cleaning zone)
stale_if:
  - The owner authorizes, amends, or rejects this lane scope.
  - The Pass-1 note-adjective stance fix lands and its corpus validation completes (un-defer trigger fires).
  - The deferred-Judgment / fusion calibration shape that "mixed" verdicts depend on changes materially.
```

## Status

`DETERMINISTIC_CORE_AUTHORIZED_AND_BUILT — DOWNSTREAM_SLICES_DEFERRED`. This record
started as a deferred scope capture. PR 420 now carries the owner-authorized deterministic
core slice: strict soft-lean schemas, no-LLM scoring-zone fusion, and focused tests. The
agent-in-the-loop cleaning inference, product-to-marketed-gender mapping, gender x
product-stance join, capture/backfill, repo-map registration after settlement, and real
calibration remain deferred and require separate bounded owner authorization.

## Decision

**Scope the creator-gender demographic signal lane as a SEPARATE lane (sibling to the
existing scoring fusions). PR 420 authorizes only the deterministic core slice: the soft-lean
schema contract, no-LLM scoring-zone fusion, and tests. Keep the agent-in-the-loop cleaning
inference, product-to-marketed-gender mapping, gender x product-stance join, capture/backfill,
repo-map registration after settlement, and calibration deferred until separately authorized.**

## Owner-Decided Scope (the constraints to honor when un-deferred)

Captured from the owner brief; these are owner decisions, not agent inferences.

1. **Creator gender ONLY.** Tag each reel with the *creator's* gender, inferred from
   reliable self-presentation cues (name, "as a woman…" style framing, explicit
   self-reference). **Do NOT** attempt per-commenter gender — the owner ruled it out as
   too noisy.
2. **SEPARATE lane, modeled on `scoring/audience_fusion.py`.** **Do NOT** fold this into
   `scoring/product_fusion.py`. That lane is creator product-**stance**; this is an
   **audience/creator demographic** signal. Different epistemic kind → sibling lane, not an
   extension of the stance lane. (Matches the existing one-lane-per-epistemic-kind grammar.)
3. **Confidence-weighted soft lean, never a hard label.** Gender inference is probabilistic
   and sensitive; emit a soft lean with confidence, never a categorical creator-gender
   label.
4. **No-LLM constraint holds in scoring/capture zones.** Any LLM-ish inference uses the
   **agent-in-the-loop** pattern (subscription, no API key), like
   `cleaning/transcript_product_extractor.py`'s `parse_mentions` — not a programmatic LLM
   SDK call.
5. **Goal: gender × product-stance.** The payoff is cutting product signals male-vs-female
   — e.g. "is product X praised more by male vs female creators." Must be testable at scale
   (the capture infra is being scaled broadly).

## Why a SEPARATE lane, and the design shape the constraints imply

This is the lane-level shape. PR 420 locks only the deterministic core record/fusion/test
surface; downstream cleaning inference, data persistence, and join behavior remain deferred
and are not designed here.

- **The no-LLM guard splits the work across two zones.** `tests/contract/test_no_llm_imports.py`
  forbids `openai/anthropic/litellm/langchain` imports in `scoring/`, `reports/`,
  `runners/`, `schemas/`, and `harness_utils.py`. So a `scoring/` gender-lean fusion
  (modeled on `audience_fusion.py`) is hard-bound to be **pure/deterministic** — it cannot
  do the inference itself.
- **Inference belongs in the cleaning/extraction zone.** `cleaning/transcript_product_extractor.py`
  (where `parse_mentions` lives, line 162) is **outside** the guarded set. So the creator-
  gender inference — the LLM-ish step — runs there via the agent-in-the-loop pattern and
  persists a deterministic per-reel creator-gender soft-lean signal as a silver-lane
  artifact. This mirrors the existing Pass-1 (extract, agent-in-the-loop, cleaning) ->
  Pass-2 (fuse, deterministic, scoring) split that `product_fusion`/`audience_fusion`
  already use.
- **The new `scoring/` lane is a deterministic soft-aggregation fusion** over that
  persisted per-reel signal (shape borrowed from `audience_fusion.py`: confidence-weighted,
  soft, abstaining), emitting a creator-gender lean + confidence per creator — never a hard label.
- **The payoff is a join, not a new capture.** Gender x product-stance is a deterministic
  join of this lane's per-reel creator-gender lean against the existing product-stance
  verdict (`product_fusion`), aggregated across the corpus. That join remains deferred.

## Hypothesis / hook (why "mixed" verdicts may already encode this)

Owner-stated, recorded as a hypothesis to test once the lane exists — not an established
finding:

> In couple-review reels, the love/hate "mixed" product verdict often **is** the gender
> split — e.g. Louis Vuitton Ombre Nomade in perfumesiren's reel `DZ5C6vRTKMW`, where one
> partner loved it and the other didn't.

Mechanically this is plausible: `product_fusion`'s verdict map yields **mixed** when *both*
a support side and an oppose side clear `material_min`. If a couple-review reel's
support/oppose split tracks the partners' gender split, then existing **mixed** verdicts
already carry latent gender-preference signal that this lane could surface. (The
perfumesiren reel and the per-reel silver-lane persistence are owner-stated; confirm at
scoping — not verified in this record.)

## What Remains Deferred (substantive, not bureaucratic)

The downstream lane remains deferred because the eventual gender x stance signal
**piggybacks on exactly what the in-flight calibration is changing**:

- The creator-gender x stance payoff and the "mixed-verdict encodes gender" hook both sit
  downstream of Pass-1 stance extraction and Pass-2 mixed-verdict formation.
- `product_verdict_fusion_calibration_surface_v0.md` records that the Pass-2 fusion
  constants only mean something relative to how the Pass-1 extractor distributes
  `stance_vote` / `extractor_confidence` ("entanglement with Pass-1"). The in-flight
  Pass-1 note-adjective stance fix changes that distribution, which shifts which reels
  come out mixed.
- Building the downstream cleaning inference, product mapping, gender x stance join, or
  calibration on top of a moving Pass-1 would bake in a calibration that is about to shift.
  Waiting remains the smallest-complete move for those slices: let Pass-1 settle, then read
  gender against a stable stance substrate.
- The PR 420 deterministic core is allowed because it defines the minimized soft-lean
  contract and deterministic combiner only; it does not run cleaning inference, read runtime
  data, join against product stance, or claim calibration.

## Downstream Un-Defer Trigger

Condition-triggered, not date-based:

- The **Pass-1 note-adjective stance fix** is landed, **and**
- its **corpus validation** is complete (the stance substrate is stable).

On observing the trigger, the owner authorizes the next bounded build in-turn; then run
implementation scoping for only the newly authorized downstream slice (cleaning inference,
product mapping, gender x stance join, calibration, or backfill) on its own lane.

## Authorization Gate

Per `AGENTS.md`: implementation/runtime work requires **explicit bounded authorization** in
the authorizing turn. The current authorized scope is PR 420's deterministic core only:
`orca-harness/schemas/creator_gender_models.py`, `orca-harness/scoring/creator_gender_fusion.py`,
and focused unit/no-LLM tests. It does **not** authorize editing `cleaning/`, capture runners,
data-lake persistence, product-stance joins, product mapping, backfill/capture execution, or
runtime data reads.

## Owner-Pending Decisions (surfaced, not resolved)

1. **Downstream minimization / obligation posture.** PR 420 resolves the deterministic-core
   minimization posture (soft signed lean, confidence, cue kind, bounded basis, typed
   provenance, no categorical label). Storage obligations for the future cleaning-produced
   signal and any data-lake persistence remain pending.
2. **Calibration with the existing fusions.** PR 420 uses an uncalibrated v0 deterministic
   floor/gain for the core. Real corpus calibration and any decision to share or diverge
   from the audience/product prior remain pending.
3. **Downstream confidence / abstain policy.** PR 420 enforces the deterministic core's
   decisive/abstained output invariants. Future cleaning reliability thresholds and join-time
   aggregation policy remain pending.
4. **Inference reliability bar.** Which cues count as reliable creator self-presentation,
   and how the agent-in-the-loop step records its basis (so the soft lean is auditable).

## Touch-points / anchors (existence confirmed 2026-06-27; internals NOT designed here)

- `orca-harness/scoring/audience_fusion.py` — soft-aggregation shape to model the new lane on. ✓ exists
- `orca-harness/scoring/product_fusion.py` — product-STANCE lane; do NOT fold into it; the join's stance source. ✓ exists
- `orca-harness/cleaning/transcript_product_extractor.py` — `parse_mentions` (line 162) agent-in-the-loop exemplar, in the non-guarded cleaning zone. ✓ exists
- `orca-harness/tests/contract/test_no_llm_imports.py` — the no-LLM guard; confirms `scoring/` is hard-bound deterministic. ✓ exists
- `orca-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py` — the deep-capture runner the owner names as the persistence source. ✓ exists
- `docs/decisions/product_verdict_fusion_calibration_surface_v0.md` — Pass-1<->Pass-2 calibration context the deferral waits on.

Owner-stated and **to confirm at scoping** (not verified here): the per-reel persistence of
creator transcript + top ~15 audience comments as silver lanes under
`F:/orca-data-lake/derived/*/<shortcode>/`; the perfumesiren `DZ5C6vRTKMW` example.

## Non-Claims

This record authorizes and describes only PR 420's deterministic core. It is **not** validation,
readiness, buyer-proof, capture/backfill authorization, cleaning inference authorization,
product mapping authorization, gender x product-stance join authorization, data-lake storage
authorization, real calibration, or repo-map registration. It does not assert the owner-stated
F:/ persistence layout or the perfumesiren example — those are to-confirm in downstream scoping.
It does not modify `product_fusion`, `audience_fusion`, or the no-LLM guard.

## Provenance

Authored from the owner brief (2026-06-27). Read-only verification in the original turn:
confirmed the five named code anchors exist at the paths above; read `test_no_llm_imports.py`
(guard covers `scoring/reports/runners/schemas` + `harness_utils.py`); confirmed
`parse_mentions` at `transcript_product_extractor.py:162` sits in the non-guarded `cleaning`
zone; read `product_verdict_fusion_calibration_surface_v0.md` for the Pass-1<->Pass-2
entanglement that justifies downstream deferral. Updated 2026-06-29 during PR 420 closeout
from owner instruction to proceed after patching; no runtime data (F:/ data lake) read.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    PR 420 authorizes and lands only the deterministic creator-gender core slice (strict
    soft-lean schemas, no-LLM scoring fusion, and tests), while downstream cleaning
    inference, product mapping, gender x product-stance join, capture/backfill, repo-map
    registration after settlement, and calibration remain separately deferred.
  trigger: lifecycle_boundary
  related_triggers:
    - architecture_doctrine
  controlling_sources_updated:
    - docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md
    - orca-harness/schemas/creator_gender_models.py
    - orca-harness/scoring/creator_gender_fusion.py
    - orca-harness/tests/unit/test_creator_gender_fusion.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/product_verdict_fusion_calibration_surface_v0.md
    - orca-harness/tests/contract/test_no_llm_imports.py
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Repo-map registration remains deferred until the PR lands and the lane is settled;
        adding a routing row before merge would route agents to an in-flight branch.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Known-source registration remains deferred until the lane lands; this branch-local
        deterministic core does not need top-level source registration before merge.
  stale_language_search: >
    rg -n "DEFERRED|NOT_AUTHORIZED|not a build authorization|0\.3|17/17|product_marketed_gender"
    docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md
    orca-harness/schemas/creator_gender_models.py orca-harness/scoring/creator_gender_fusion.py
    orca-harness/tests/unit/test_creator_gender_fusion.py
  stale_language_search_result: >
    Executed 2026-06-29 during PR 420 closeout. Current-body hits are expected:
    the status and scope text name downstream deferral, and the code keeps
    `product_marketed_gender` as an auditable zero-weight cue kind. No live current
    text retains `NOT_AUTHORIZED`, `0.3`, or `17/17` as active claims. Hits in the
    older 2026-06-27 direction_change_propagation receipt preserve historical
    deferred/unbuilt language and are superseded by this receipt, not active routing.
  non_claims:
    - not validation
    - not readiness
    - not buyer-proof
    - not capture/backfill authorization
    - not cleaning inference authorization
    - not product mapping or gender x product-stance join authorization
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Records a NEW, DEFERRED, not-yet-authorized creator-gender demographic signal lane
    scope for the IG reels pipeline: a SEPARATE sibling lane (not folded into
    product_fusion's stance lane) emitting a confidence-weighted creator-gender soft lean,
    with inference in the agent-in-the-loop cleaning zone and a deterministic scoring-zone
    fusion, to enable a gender x product-stance cut. No existing rule, contract, or lane is
    changed; the build is deferred behind the Pass-1 stance-calibration un-defer trigger and
    the AGENTS.md authorization gate.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md
  downstream_surfaces_checked:
    - docs/decisions/product_verdict_fusion_calibration_surface_v0.md
    - orca-harness/scoring/audience_fusion.py
    - orca-harness/scoring/product_fusion.py
    - orca-harness/tests/contract/test_no_llm_imports.py
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Routing-surface registration DEFERRED. The lane is unauthorized and unbuilt and this
        record sits on a lane branch not merged to main; registering it now would route
        agents to a non-existent lane. Registration belongs to the owner's authorize+build+
        propagation pass when the lane is actually built.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Known-source registration DEFERRED for the same reason — the lane is deferred and
        unbuilt; it registers when built, not before.
    - path: docs/decisions/orca_doctrine_index_v0.md
      reason: >
        Index registration DEFERRED until the lane is authorized/built and this record is
        merged to main; indexing a deferred, branch-only scope record would advertise an
        unbuilt lane as live.
  stale_language_search: >
    not_run — additive new decision record on a lane branch; no existing routing surface
    references this lane yet, so there is no stale routing language to sweep. The sweep
    belongs to the owner's authorize+build+propagation pass.
  non_claims:
    - not validation
    - not readiness
    - not a build authorization
    - not implementation scoping
    - not a capture/backfill authorization
    - not a calibration claim
    - not an obligation/minimization-contract amendment
    - not owner-lock
```
