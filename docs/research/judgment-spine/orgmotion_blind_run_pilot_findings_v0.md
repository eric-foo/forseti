---
retrieval_header_version: 1
artifact_role: Research / pilot findings record (blind org-motion paired-run). NOT validation, readiness, judgment-quality, calibration, or buyer-proof evidence. Single-vendor pilot.
scope: >
  Blind org-motion delta test on the two frozen org-motion fixtures (Beauty Pie #3, Topicals #4):
  does ADDING the org-motion evidence (augmented arm) change the best-move call vs the baseline arm?
  Measures movement of the best move given available evidence — NOT correctness against the sealed
  real-world outcome (no reveal). Single-vendor (Claude), instruction-level isolation, small-N.
use_when:
  - Reviewing whether the org-motion paired arm shifts the contestant call (anti-cherry-pick reporting).
  - Auditing the blind-run method before a fuller cross-vendor / scored run.
authority_boundary: retrieval_only
stale_if:
  - A cross-vendor or run_case.py-scored run supersedes these by-hand single-vendor numbers.
  - Either frozen fixture's ledger_freeze_hash changes (the fixture changed -> investigate).
---

# Org-Motion Blind-Run Pilot Findings (v0)

## Status & non-claims

PILOT / DISCOVERY. **Single-vendor** (Claude Opus; a Claude Sonnet pass validated the Topicals loop).
**Blind** — contestants saw only a zero-spoiler packet; no sealed outcome was revealed, so this measures
**whether org-motion moves the best-move call**, NOT whether the call was right. Not validation, not
readiness, not judgment-quality, not calibration, not a scoring-key result. Product-learning tier, N small.

## Method

- Two frozen paired fixtures, org-motion the only baseline↔augmented delta:
  - Beauty Pie `beautypie_repricing_2023_v0` (ladder: watch=1 / hold=2 / soften=3 / phase-or-grandfather=4 / commit=5).
  - Topicals `topicals_retail_expansion_2021_v0` (ladder: watch=1 / hold=2 / limited-pilot=3 / broad-expansion=4).
- Each contestant = a fresh isolated sub-agent given ONLY the packet file, instructed: no other tool, no
  web, no outside/later knowledge; decide as the brief's decision-maker; pick one ladder rung + reasoning.
- **Opus**, N=5 draws per arm per case (the runtime model, per owner direction 2026-06-14: "all judgement
  should be opus since that's the runtime one"). Topicals also has a Sonnet N=3/arm validation pass.
- Comparison: distribution + mean ladder level, baseline vs augmented. No band-key scoring (see Scoping note).

## Results — Opus, N=5/arm

### Topicals (org-motion = single 2021-03-03 careers snapshot, 1 Supply Chain Manager role)

| Arm | Calls (level) | Mean | hold-rate |
| --- | --- | --- | --- |
| Baseline | limited-pilot×4 (3), hold×1 (2) | 2.80 | 1/5 |
| Augmented | limited-pilot×5 (3) | 3.00 | 0/5 |

Delta +0.20; org-motion eliminated the lone "hold"; **modal call unchanged** (limited-pilot both arms);
ceiling held (no broad-expansion). Sonnet validation (N=3/arm) showed the same shape: baseline 2.67 (1/3
hold) -> augmented 3.00 (0/3 hold).

### Beauty Pie (org-motion = hiring trajectory: 3 Product Leads incl. Retention + demand/inventory planning)

| Arm | Calls (level) | Mean |
| --- | --- | --- |
| Baseline | phase-or-grandfather×5 (4) | 4.00 |
| Augmented | phase-or-grandfather×5 (4) | 4.00 |

Delta 0.00; **unanimous phase-or-grandfather in both arms** — zero movement.

## Finding

**Org-motion did NOT move the modal best-move call in either case (0 of 2 at the modal level).** Topicals
showed a tiny consensus-tightening (one marginal "hold" draw moved to "limited-pilot"); Beauty Pie showed
none. This matches the pre-registered blind prediction for Topicals (`org_motion_blind_prediction_v0.md`:
"weak upward at most; small / possibly nil; do not expect it to flip a passive call to an aggressive one").

Mechanism (from the augmented traces): contestants reasoned about the org-motion signal explicitly and
weighted it as **weak corroboration, not a driver** — Topicals' single supply-chain hire read as mildly
pro-action (capability being *built* -> don't sit on hold, but not proof of readiness -> cap at a bounded
pilot); Beauty Pie's richer hiring signal read as weak / **mildly cautionary** (a fresh Retention role =
retention is an *unsolved, actively-staffed* concern -> if anything argues against the aggressive move).
A single honestly-presented hiring signal did not swing a major decision — arguably the correct behavior,
and a quiet check that the augmented packets do not over-steer.

## Caveats / limitations (named, not hidden)

- **Single-vendor** (Claude). The charter panel (GPT-5.5, Grok, Gemini) was not reachable here; cross-vendor
  is an owner-run. A Claude-only result may carry Claude-family idiosyncrasy.
- **Small-N** (5/arm). Distributions are suggestive, not significant.
- **Blind by design** — measures call movement, not correctness; no reveal (calibration would need N>=K + reveal).
- **Instruction-level isolation** (no-tools/no-web by instruction), not the charter's structural web-off; no
  formal pre-judgment recognition/obscurity screen and no JSG-08 tell-audit were run (deferred). Recognition
  affects both arms, so the within-case delta remains interpretable.
- Reasoning traces were captured in-session (sub-agent returns) but are NOT yet persisted per-draw; a fuller
  run should persist each blind_judgement + trace for an auditable tell-audit.

## Scoping note — run_case.py does not fit the paired cases

The harness runtime scorer `orca-harness/runners/run_case.py` cannot score these fixtures as-is:
(1) `run_fixed_case` calls `FacilitatorLedger.model_validate`, but the frozen paired ledgers are
`model_valid = no` (the known L4 construction-vs-runtime schema-drift); and (2) it expects a single-packet
layout (`participant_packet.md`, `evidence/*.yaml`, `runs/*/*/blind_judgement.yaml`), whereas the org-motion
cases are paired (baseline + augmented, evidence inline). The org-motion DELTA (this pilot) does not need the
band-key scorer — it is a baseline-vs-augmented call comparison. Wiring paired cases into `run_case.py`
(needs L4 + a paired adapter) is a separate future harness task, logged here.
