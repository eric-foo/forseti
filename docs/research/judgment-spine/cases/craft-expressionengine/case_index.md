# Case Index — Craft/ExpressionEngine (Decide-vs-Confirm lane)

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine case index + frame-lock (facilitator-side; frame-lock only, capture pending)
scope: Frame-lock for the Pixel & Tonic / ExpressionEngine 2012-2013 competitor-displacement decide-vs-confirm backtest. Participant packet, facilitator ledger, evidence, and sealed outcome are NEEDS_CAPTURE.
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

- **subject:** Pixel & Tonic (Brandon Kelly), 2012-2013 decision re: ExpressionEngine
  community departure
- **decision_family:** competitor-displacement (clean non-review substrate)
- **decision_owner_context:** Founder Brandon Kelly, Pixel & Tonic — ExpressionEngine's
  leading add-on maker (ecosystem insider)
- **decision_question:** at the cutoff, should P&T respond to EE community discontent
  + beginning departures by building / backing a competing CMS, or stay loyal to EE —
  watch / probe / test / hold / build / move
- **cutoff_window:** ~2012-2013 — `NEEDS_VERIFICATION` (replay gate)
- **decide_vs_confirm_hypothesis:** can clean non-review public signal (EE
  community/forum discontent + agency sentiment, not reviews) DECIDE the build-the-rival
  move, or only CONFIRM it after the rival's adoption was known?
- **anti_cherry_pick:** drawn from the pre-declared obscure-displacement discovery
  lane, not because the outcome flatters Orca

## Run parameters (Decide-vs-Confirm lane)

- **Web search OFF** for the contestant (sealed pool only) — structural and
  recorded (`web_search_disabled` evidence), not a prompt instruction. Load-bearing:
  it is what makes a not-too-prominent case safe.
- **Memorization:** obscurity-first; **isolated** memory probe (separate session,
  no priming) as a **conservative backstop**, not a gate; a fail is a swap signal →
  prefer a lower-`Uses` case.
- **Optional flavor-anonymization at packet construction:** genericize company name
  / non-decision flavor only; **never the decision-driving numbers** (the levers the
  decision turns on stay real so the outcome remains ground truth).

## Missing pieces (NEEDS_CAPTURE — gated)

participant_packet.md (zero-spoiler, built clean at capture) · facilitator_ledger.yaml
(sealed band inputs + leakage audit + freeze hash) · evidence/*.yaml (real pre-cutoff
units, cutoff-disciplined) · sealed outcome (facilitator-only) · probes/ · runs/ · scores/

## Non-claims

Not captured, not validated, not judgment-quality, not memorization-certified, not
buyer proof. Product-learning cap. Freezes nothing.

## ═══ SEALED — FACILITATOR ONLY (outcome; skip if blind-judging) ═══

- **sealed_outcome:** Pixel & Tonic built the rival (Craft CMS launched 2013) and
  later divested its ExpressionEngine plugins. [existence/direction only; not interpreted]
- **post_window_exclusion:** exclude the rival's launch (2013), its adoption, and the
  EE-plugin divestiture from at-cutoff reasoning.

## ═══ END SEALED ═══
