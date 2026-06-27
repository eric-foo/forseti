# IG Reels — Creator-Gender Demographic Signal Lane — Scope + Deferral Decision (v0)

```yaml
retrieval_header_version: 1
artifact_role: Decision record (owner-scoped lane; DEFERRED; not a build authorization)
scope: >
  Captures the owner-decided scope for a SEPARATE creator-demographic signal lane over
  the IG reels social-source pipeline that tags each reel with the CREATOR's gender as a
  confidence-weighted soft lean, so product signals can be cut male-vs-female (goal:
  gender x product-stance). Records the explicit deferral, the un-defer trigger (the
  in-flight Pass-1 note-adjective stance calibration + its corpus validation), and the
  per-AGENTS.md authorization gate. Scope/intent capture only.
use_when:
  - Picking up the creator-gender demographic lane after the Pass-1 stance calibration finishes.
  - Checking what the owner decided (and ruled out) for creator-gender tagging before scoping a build.
  - Confirming whether this lane is authorized yet (it is not) and what must happen first.
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

`SCOPE_CAPTURED — DEFERRED — NOT_AUTHORIZED`. This record captures an owner-decided lane
scope and an explicit owner deferral. It is **not** a build authorization, **not**
implementation scoping, **not** validation, readiness, or buyer-proof, and it locks **no**
implementation design. It records intent durably so the lane can be picked up cleanly when
the un-defer trigger fires and the owner grants bounded authorization. Authored on a lane
branch (`claude/hopeful-spence-ae22f2`), not merged to `main`.

## Decision

**Scope the creator-gender demographic signal lane as a SEPARATE lane (sibling to the
existing scoring fusions), and DEFER any build until the in-flight Pass-1 note-adjective
stance calibration and its corpus validation are finished. Implementation requires explicit
bounded owner authorization in the authorizing turn (per `AGENTS.md`); this record is not
that authorization.**

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

This is scope-level shape (what the constraints force), **not** a locked implementation
design and **not** authorization. Detailed scoping (record schema, function surface,
`STEP-*` route) is deferred to the post-authorization scoping pass.

- **The no-LLM guard splits the work across two zones.** `tests/contract/test_no_llm_imports.py`
  forbids `openai/anthropic/litellm/langchain` imports in `scoring/`, `reports/`,
  `runners/`, `schemas/`, and `harness_utils.py`. So a `scoring/` gender-lean fusion
  (modeled on `audience_fusion.py`) is hard-bound to be **pure/deterministic** — it cannot
  do the inference itself.
- **Inference belongs in the cleaning/extraction zone.** `cleaning/transcript_product_extractor.py`
  (where `parse_mentions` lives, line 162) is **outside** the guarded set. So the creator-
  gender inference — the LLM-ish step — runs there via the agent-in-the-loop pattern and
  **persists a deterministic per-reel creator-gender soft-lean signal** as a silver-lane
  artifact. This mirrors the existing **Pass-1 (extract, agent-in-the-loop, cleaning) →
  Pass-2 (fuse, deterministic, scoring)** split that `product_fusion`/`audience_fusion`
  already use.
- **The new `scoring/` lane is then a deterministic soft-aggregation fusion** over that
  persisted per-reel signal (shape borrowed from `audience_fusion.py`: confidence-weighted,
  soft, abstaining), emitting a creator-gender **lean + confidence** per reel/creator —
  never a hard label.
- **The payoff is a join, not a new capture.** "Gender × product-stance" is a deterministic
  join of this lane's per-reel creator-gender lean against the existing product-stance
  verdict (`product_fusion`), aggregated across the (broadly-scaled) corpus. The data is
  already captured (owner: creator transcript + top ~15 audience comments persisted per
  reel under the IG reels deep-capture silver lanes); this lane adds a creator-gender read
  over it, not a new capture surface.

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

## Why DEFER (substantive, not bureaucratic)

The deferral is not just sequencing hygiene — the gender signal **piggybacks on exactly
what the in-flight calibration is changing**:

- The creator-gender × stance payoff and the "mixed-verdict encodes gender" hook both sit
  **downstream of Pass-1 stance extraction and Pass-2 mixed-verdict formation**.
- `product_verdict_fusion_calibration_surface_v0.md` records that the Pass-2 fusion
  constants only mean something **relative to how the Pass-1 extractor distributes
  `stance_vote` / `extractor_confidence`** ("entanglement with Pass-1"). The in-flight
  Pass-1 note-adjective stance fix changes that distribution, which shifts **which reels
  come out "mixed"** — i.e. the precise signal this lane would build on.
- Building the gender lane on top of a moving Pass-1 would bake in a calibration that is
  about to shift. Waiting is the smallest-complete move: let Pass-1 settle, then read
  gender against a stable stance substrate.

## Un-Defer Trigger

Condition-triggered, not date-based:

- The **Pass-1 note-adjective stance fix** is landed, **and**
- its **corpus validation** is complete (the stance substrate is stable).

On observing the trigger, the owner authorizes the bounded build in-turn; then run
implementation scoping (record schema, inference touch-point in `cleaning/`, the `scoring/`
fusion surface, the gender×stance join, validation) → spec → build, on its own lane.

## Authorization Gate

Per `AGENTS.md`: implementation/runtime work requires **explicit bounded authorization** in
the authorizing turn. This record is documentation of an owner-scoped, owner-deferred lane;
it does **not** authorize editing `cleaning/`, `scoring/`, runners, schemas, or any runtime
surface, and does not authorize a capture or backfill run.

## Owner-Pending Decisions (surfaced, not resolved)

1. **Sensitivity / minimization posture for an inferred-demographic signal.** Inferring a
   person's gender is probabilistic and sensitive (owner's framing). Before build, decide
   how the per-reel creator-gender lean is stored, labeled, and minimized, and whether it
   carries a minimization/obligation posture analogous to other capture lanes. Surfaced as
   a prerequisite; not resolved here.
2. **Shared vs independent calibration with the existing fusions.** `audience_fusion` and
   `product_fusion` already share a v0 prior (gain 2.0, abstain floor 0.40, 1.0/0.6/0.3
   multipliers — see `product_verdict_fusion_calibration_surface_v0.md`). Decide whether the
   gender-lean fusion shares that surface or diverges (a recorded decision, not copy-paste
   drift).
3. **Confidence floor / abstain policy for the soft lean.** Where the lean abstains vs.
   emits — the "never a hard label" constraint plus an explicit abstain bar for low-signal
   reels (no name cue, no self-reference).
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

Scope/intent capture only. **Not** a build authorization, **not** implementation scoping or
a route, **not** a schema/field/record design, **not** validation, readiness, or buyer-proof,
**not** a capture/backfill authorization, **not** a calibration claim, **not** an obligation/
minimization-contract amendment (the sensitivity posture is surfaced, not closed), **not**
owner-locked. Does not assert the owner-stated F:/ persistence layout or the perfumesiren
example — those are to-confirm at scoping. Does not modify `product_fusion`, `audience_fusion`,
or the no-LLM guard.

## Provenance

Authored from the owner brief (2026-06-27). Read-only verification this turn: confirmed the
five named code anchors exist at the paths above; read `test_no_llm_imports.py` (guard covers
`scoring/reports/runners/schemas` + `harness_utils.py`); confirmed `parse_mentions` at
`transcript_product_extractor.py:162` sits in the non-guarded `cleaning` zone; read
`product_verdict_fusion_calibration_surface_v0.md` for the Pass-1<->Pass-2 entanglement that
justifies the deferral trigger. No runtime data (F:/ data lake) read; no implementation
designed.

## Direction Change Propagation

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
