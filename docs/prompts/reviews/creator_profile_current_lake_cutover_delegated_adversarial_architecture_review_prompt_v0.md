# Creator Profile Current Lake Cut-Over — Delegated Adversarial Architecture Review (Commission Prompt) v0

```yaml
retrieval_header_version: 1
artifact_role: delegated adversarial architecture review commission prompt
scope: >
  Commissions a fresh cross-vendor reviewer to adversarially stress-test the proposed
  creator_profile_current lake cut-over architecture BEFORE ratification or implementation. Read-only
  design review; produce a durable adversarial review report. The home model (Anthropic CA) adjudicates
  the findings and revises the proposal. Not a code patch; there is no code to patch yet.
use_when:
  - Running the adversarial architecture review of the lake cut-over proposal.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md
  - orca-harness/capture_spine/creator_profile_current/materialize.py
  - orca-harness/capture_spine/creator_profile_current/silver_metric_reader.py
  - orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
  - orca-harness/data_lake/root.py
  - orca-harness/tests/unit/test_creator_profile_current_static_view.py
```

You are a **fresh, independent cross-vendor reviewer**. You are NOT the model that
authored this proposal (de-correlation bar: `cross_vendor_discovery` — your value
is that you reason from outside the authoring lane). Treat every claim below as a
hypothesis: **confirm-don't-trust**. Your job is to **attack** this architecture
and find where it is wrong, fragile, over/under-scoped, or quietly fails the goal
— not to rubber-stamp it. A review that finds nothing material is a failed review;
if you genuinely find nothing, prove you tried by showing the strongest attacks
you mounted and why each failed.

## orca_start_preflight (complete before reviewing)

- `agents_md_read`: read `AGENTS.md` and `.agents/workflow-overlay/README.md` in
  this repo first, then the overlay files they route to. They govern source
  loading, safety, and claim discipline.
- `repo_state`: branch `claude/creator-profile-silver-repoint` (or wherever this
  prompt and the proposal are committed); fetch fresh and read the pinned files at
  current HEAD. The worktree may carry other untracked files — rely on the **named
  files**, not on a clean tree.
- `source_pack`: the `open_next` files above are the bounded pack. Read the
  proposal in full; read the code files enough to verify the proposal's claims
  about them (do not trust the proposal's paraphrase of the code).
- `output_mode`: durable review report (see Output). No source edits.

## Objective & intended decision

Stress-test the proposed cut-over architecture so the owner can decide whether to
implement it as-is, revise it, or rework it. Your report is a **decision input**,
not a decision. Intended decision vocabulary the owner will use:
`accept` | `revise_before_acceptance` | `needs_architecture_rework`.

## What is being proposed (summary — verify against the proposal doc)

Cut the committed `creator_profile_current` registry over to lake-sourced metrics
via a **committed, operator-regenerated rollup snapshot** that `materialize.py`
reads in place of the hand-kept `seed["metric_rollups"]`. Two gates: an
**equivalence gate** (CI, lake-free: producer→reader in a `for_test` temp lake ==
committed seed rollups == committed snapshot) and a **live-lake reconciliation
gate** (operator-local, `pytest.skip` when `ORCA_DATA_ROOT` unset). Latest rollup
per account selected by max `computed_at`, tie-break `record_id` desc, fail-closed
on ambiguous. Synthesized from a three-architect pass; the rejected alternatives
were **certify-only** (don't re-point materialize) and **full Creator Vault
envelopes now**.

## Fitness reference (what "good" means here)

- **Smallest *complete* intervention / lowest lock-in:** the narrowest change that
  *durably* makes the registry lake-sourced; not a thin slice that defers the real
  capability, not over-built structure that locks in prematurely.
- **CI determinism with no lake present** is mandatory and must be real, not
  apparent.
- **No fake success paths; real failure visibility.** `missing != zero`; posture/
  value coupling preserved.
- **Actually retires manual staleness** — or names precisely where it does not.

## Adversarial tasks — attack at least these, hardest-first

1. **Does CI-determinism actually hold, or can it be fooled?** Can the committed
   snapshot, the committed view, and the seed all pass CI while being collectively
   wrong (e.g., a stale snapshot that is internally consistent)? Is the
   equivalence gate proving what it claims, given the producer recomputes from the
   *same committed fixtures* the seed uses (is that circular — proving the lake
   path against the very inputs that define the seed)?
2. **The latest-rollup-per-account rule.** Is `max(computed_at)` + `record_id`
   tie-break + fail-closed-on-ambiguous correct and deterministic against the
   real append-only lake? Attack the same-second and same-millisecond cases, clock
   skew/non-monotonic `generated_at_utc`, and whether `record_id` (ULID) ordering
   is a safe tie-break. Is the "accepted residual" actually safe?
3. **Does this retire manual staleness, or relocate it?** The proposal admits CI
   cannot detect lake drift and pushes that to an operator/scheduled gate. Is
   "lake-verified + operator-regenerated" a real fix, or staleness wearing a
   different hat? Is the `pytest.skip`-when-no-lake gate a genuine guard or
   green-by-default theater that will never run?
4. **Is the v0 scope right?** Argue the strongest case that the recommended
   snapshot is the *wrong* cut: either certify-only is sufficient (so re-pointing
   materialize is needless risk) OR the full Creator Vault layer is warranted now
   (so the snapshot is throwaway lock-in). Which is most defensible and why?
5. **Provenance soundness.** Does binding each snapshot rollup to a Silver
   `content_hash` give real tamper-evidence and drill-back, or a false sense of
   it? Can the chain (view → snapshot → rollup record → observations → raw) break
   silently?
6. **Seed dual-maintenance residual.** During the transition both the seed and the
   snapshot claim the same numbers. Is the drift-witness enough, or does this
   create a divergence trap (especially once YouTube has no seed)?
7. **Reversibility & lock-in.** Is the claimed "one input swap to revert" real?
   What becomes a one-way door, and is it named?
8. **YouTube fold-in assumptions.** Is "purely additive, zero registry changes"
   true given YT's non-observed engagement posture and the 30/3 asymmetry?
9. **Missed failure modes / unstated assumptions.** Anything the three architects
   and the synthesis all missed (they shared inputs — look for shared blind spots).

## Output — durable adversarial review report

Write your report to
`docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_lake_cutover_architecture_adversarial_review_v0.md`
with a valid retrieval header (`retrieval_header_version: 1`,
`artifact_role: adversarial architecture review`, `authority_boundary: retrieval_only`).

- **Findings first.** Each finding: a short title, severity
  (`blocker` | `major` | `minor` | `nit`), the precise claim it attacks, the
  evidence (file:line or proposal section), and a concrete recommended design
  change (NOT code — this is a design review).
- Then an overall **verdict**: `accept` | `revise_before_acceptance` |
  `needs_architecture_rework`, with the load-bearing reason.
- Then a **review_summary** YAML block: `reviewed_by`, `de_correlation_bar:
  cross_vendor_discovery`, `verdict`, `blocker_count`, `major_count`,
  `biggest_single_risk`, `scope_fork_opinion` (your independent call on task 4).
- Read-only: do not edit source, do not write code, do not implement.

## Adjudicator next-moves (for the Anthropic home model, after the review)

The home model will adjudicate each finding as claims, not premises: verify each
against the proposal + code, accept/revise/reject with reason, and revise the
proposal doc accordingly (or escalate the scope fork to the owner). The review
does not mutate the proposal; the home model does.

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  anchor_goal: >
    Make the creator registry source-backed and lake-aware — metrics derive from Silver/data-lake
    records so the registry stops going manually stale; identity ledger stays identity-only.
  output_fit: >
    The review makes the cut-over architecture safer to ratify/implement by surfacing real design
    defects, scope-fork misjudgments, and staleness-retirement gaps before any code is written.
  drift_guard: >
    Review the DESIGN, not an imagined implementation; do not propose code patches; do not rubber-stamp;
    ground every finding in the actual code/constraints, not the proposal's self-description.
```
