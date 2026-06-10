# Judgment-Spine Case — Usage Ledger v0

Purpose: a discoverable registry of **how many times** each case pack has been used
— for judgment runs, method-validation replays, or capture-armory proofs — so a
later model/agent does **not** default to the same few cases. Before selecting a
case, consult this ledger and **prefer the lowest use-count**; after using a case,
**increment its count** (and add purpose + date + run-artifact path).

## Counter

`Uses` = number of distinct times the case pack has been exercised.

Counts before 2026-06-09 are **observed-from-disk estimates** — exact historical
use-times were never recorded — and the counter is authoritative going forward.
Lower `Uses` = preferred for the next selection.

## Cases

Ordered low → high `Uses` (ties keep prior order).

| Case | Location | Uses | Observed usage | Notes |
|---|---|---|---|---|
| inoreader-repricing | `docs/research/judgment-spine/cases/inoreader-repricing/` (pending) | 0 | — | confirmed decide-vs-confirm subject (repricing); frame-lock + capture pending |
| craft-expressionengine | `docs/research/judgment-spine/cases/craft-expressionengine/` (pending) | 0 | — | confirmed decide-vs-confirm subject (displacement); frame-lock + capture pending |
| intercom→zendesk | `docs/product/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md` | 0 | method-validation replay frame only (no run) | candidate |
| stack-overflow→chatgpt | `docs/product/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md` | 0 | replay frame only (no run) | candidate |
| reddit-api-pricing | `docs/product/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md` | 0 | replay frame only (no run) | Reddit-surface; would exercise the in-progress (other-lane) Reddit/cloakbrowser adapters |
| thomson-reuters→casetext | `docs/product/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md` | 0 | replay frame only (no run) | candidate |
| daimler-carve-out | `docs/research/judgment-spine/cases/daimler-carve-out/` | 1 | judgment run (participant packet, case-02 preflight, safety receipt) | owner-confirmed done |
| milwaukee-fiscal-crossroads | `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/` | 1 | judgment run (reveal readout) | owner-confirmed done |
| canoo-walmart | `docs/research/judgment-spine/cases/canoo-walmart/` | 1 | full judgment cycle (blind judgments, reveal readout, outcome calibration, JSG receipts) | judged already; sources may never have been captured *through the armory* — confirm before reusing for a capture proof |
| unity-runtime-fee | `docs/research/judgment-spine/cases/unity-runtime-fee/` | 2 | judgment run (reveal readout) + method-validation `mv04` | owner-confirmed done |

## Selection discipline

- Prefer the **lowest `Uses`** for any new run/proof; do **not** default to the
  most-developed cases (unity, canoo-walmart, daimler, milwaukee).
- After a use, **increment `Uses`**, add the purpose + date, and link the run artifact.
- A case `Uses`-d only on the judgment axis whose sources were never captured
  through the armory (e.g. canoo-walmart) may still be a valid capture-proof
  target — note that explicitly rather than auto-excluding it.
- Lower count is a *spread-usage* signal, not a quality signal.

## Non-claims

Usage counter only. Not a judgment verdict, not a case-quality ranking, not source
completeness or capture validation. Records use counts to spread case selection,
nothing more.
