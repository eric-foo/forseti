# Tower 28 Rerun Under Upgraded Contract — Commission Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Commissions the Tower 28 v2 company competitive-intelligence run under the
  upgraded CSB company-profile contract, as the rerun arm of the ledger-bound
  comparison loop: v1 bundle (old contract) vs v2 bundle (upgraded contract),
  both presented to a fresh external session under the same assessment lens.
  Encodes the blindness rule that makes the comparison attributable.
use_when:
  - Dispatching the Tower 28 v2 rerun lane.
  - Preparing the external comparison session after v2 lands.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
stale_if:
  - The v2 bundle lands and the external comparison is adjudicated (consumed).
  - The owner changes the comparison design (blindness, evidence base, lens).
```

## Load Contract

- `packet_version`: 0
- `created_at`: 2026-07-18 Asia/Singapore
- `created_by_lane`: Tower 28 CI/GTM lane; provenance only, not authority
- `load_rule`: confirm-don't-trust; the contract files in `open_next` are the
  only synthesis authority for the run

## Why a rerun (comparison design)

Same subject, upgraded contract: differences between v1 and v2 bundles then
measure the contract change, not company variance. The owner presents BOTH
bundles to a fresh external session under the same CI-worthiness lens used in
round 1 and adjudicates the comparison.

## Blindness rule (what the rerun lane may and may not load)

- MAY load: the upgraded contract files (`open_next`); raw evidence rows in
  the lake (observation/scan ledger rows, capture receipts), including v1's
  typed observation rows and any retailer-probe or add-on-task observations
  landed by dispatch time. Evidence is evidence.
- MUST NOT load: v1's report synthesis (Sections 5-8 narrative, company
  surface candidates, any conclusions), the external assessments of v1, or
  `docs/decisions/forseti_ci_report_external_review_adjudication_ledger_v0.md`.
  The contract already encodes every adjudicated improvement; reading the
  defect list directly would prime the lane to patch v1's specific flaws
  instead of demonstrating that the contract alone produces the better
  report. A fresh lane session runs this — not a session that carries v1 or
  ledger context.

## Dispatch decision (owner picks at dispatch): evidence base A or B+

- **A — full fresh scan.** New commission-sealed board, fresh intelligent
  walk (~v1-scale web operations), fresh observations. Tests the whole
  pipeline under the new contract, including its scan-stage guidance.
  Costlier; evidence differences (a moved world) mix into the comparison.
- **B+ — reuse + targeted supplement (recommended).** Reuse v1's typed
  observation rows as the evidence base; acquire fresh evidence ONLY where
  the upgraded contract demands classes v1 never collected: substantive
  review sampling for the Section 7 six-field classification rows and chain
  cards; preservation captures for conclusion-bearing rows (CR mechanism);
  and any add-on-task observations (price ladder, certification directories,
  diversion read) not already landed by the retailer-probe lane. Cheaper,
  attribution-clean (same base evidence, new synthesis), and exercises the
  new machinery exactly where it requires new evidence. Declare every
  supplement in the run receipt.

Either way: `mode: forward`, `time_posture: recency_first`, new as_of/cutoff
set at dispatch; no claim inherits recency it did not earn; the completed
report carries the Executive Intelligence Brief; the validator must PASS
before the bundle is presented.

## Run receipt must declare the deltas

For honest comparison attribution, the v2 bundle states, in its scan/run
receipt: which contract version it ran under; evidence base (A or B+ with
supplements enumerated); retailer surface set vs v1's (v1 was Sephora-deep
only — name whatever retailer-probe targets were bound and read by dispatch
time); and dates. The external session receives this delta declaration with
the bundles so contract-shape gains are separable from evidence-breadth
gains.

## Comparison protocol (after v2 lands; owner executes)

One fresh external session (no prior context), given: v1 bundle, v2 bundle,
the delta declaration, and the SAME round-1 lens: assess CI-worthiness,
decision-usefulness, credibility/provenance, and readability; identify
defects; then state which bundle is stronger per axis and why. The paste
prompt is drafted when v2 lands. Round-1 external findings stay withheld
from that session (fresh eyes, same lens — not a diff review of round 1).

## Drift Guard

- The report stays decision-neutral per the contract; comparison intent must
  not leak into synthesis ("beat v1" is not a synthesis instruction — the
  lane simply runs the contract).
- Sanctioned routes only; bot-blocks are typed gaps; no login walls, no cart
  interaction.
- No contract edits from this lane; contract friction returns as typed
  feedback for the next ledger round.

## Success signal

A validator-PASS v2 bundle (board + scan receipt + report with exec brief)
with the delta declaration, produced blind to v1 synthesis — ready for the
owner's same-lens external comparison in one paste.
