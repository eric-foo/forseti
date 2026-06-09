# Case Index — Inoreader Repricing (Decide-vs-Confirm lane)

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine case index + frame-lock (facilitator-side; frame-lock only, capture pending)
scope: Frame-lock for the Inoreader 2019 repricing decide-vs-confirm backtest. Participant packet, facilitator ledger, evidence, and sealed outcome are NEEDS_CAPTURE.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/decide_vs_confirm_backtest_case_frame_template_v0.md
  - docs/research/judgment-spine/decide_vs_confirm_case_discovery_results_v0.md
  - docs/research/judgment-spine/cases/case_usage_ledger_v0.md
```

## Status

`FRAME_LOCKED_PENDING_CAPTURE`. Decide-vs-Confirm lane. Frame-lock only —
participant packet, facilitator ledger, evidence, and sealed outcome are
`NEEDS_CAPTURE` (gated capture stage / ECR rung one). Product-learning cap. Not
captured, not validated, not judgment-quality, not memorization-certified. Freezes
nothing. Untracked on the current ECR branch.

Usage: `case_usage_ledger_v0.md`, `Uses` 0.

## Case frame (spoiler-free)

- **subject:** Inoreader (Innologica), 2019 Pro-plan repricing / repackaging
- **decision_family:** pricing / repricing / packaging
- **decision_owner_context:** Founder/CEO, Innologica (bootstrapped RSS-reader co)
- **decision_question:** at the cutoff, how aggressively to gate power-user
  functionality (Rules limits) into paid tiers when repackaging — watch / hold /
  narrow / phase / commit
- **cutoff_window:** ~Jan 2019 — `NEEDS_VERIFICATION` (replay gate)
- **decide_vs_confirm_hypothesis:** does clean pre-cutoff public signal (competitor
  RSS-reader pricing/packaging + public power-user sentiment) DECIDE the gating
  calibration, or only CONFIRM it after the reaction? AR-S2: decision-grade for a
  first-time aggressive gating, or needs an observable iteration?
- **anti_cherry_pick:** drawn from the pre-declared obscure-repricing discovery
  lane, not because the outcome flatters Orca

## Run parameters (Decide-vs-Confirm lane)

- **Web search OFF** for the contestant (sealed pool only) — structural and
  recorded (`web_search_disabled` evidence), not a prompt instruction. Load-bearing:
  it is what makes a not-too-prominent case safe.
- **Memorization:** obscurity-first; **isolated** memory probe (separate session,
  no priming) as a **conservative backstop**, not a gate; a fail is a swap signal →
  prefer a lower-`Uses` case.
- **Optional flavor-anonymization at packet construction:** genericize company name
  / non-decision flavor only; **never the decision-driving numbers** (prices/limits
  stay real so the outcome remains ground truth).

## Missing pieces (NEEDS_CAPTURE — gated)

participant_packet.md (zero-spoiler, built clean at capture) · facilitator_ledger.yaml
(sealed band inputs + leakage audit + freeze hash) · evidence/*.yaml (real pre-cutoff
units, cutoff-disciplined) · sealed outcome (facilitator-only) · probes/ · runs/ · scores/

## Non-claims

Not captured, not validated, not judgment-quality, not memorization-certified, not
buyer proof. Product-learning cap. Freezes nothing.

## ═══ SEALED — FACILITATOR ONLY (outcome; skip if blind-judging) ═══

- **sealed_outcome:** founder publicly walked back a power-user limit; company
  remained operational (2019→ongoing). [existence/direction only; not interpreted]
- **post_window_exclusion:** exclude the founder's public walk-back and all
  post-cutoff pricing evolutions / user reaction from at-cutoff reasoning.

## ═══ END SEALED ═══
