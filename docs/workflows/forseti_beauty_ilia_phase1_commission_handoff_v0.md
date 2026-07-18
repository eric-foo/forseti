# ILIA Beauty Phase 1 — Commission Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Commissions the Phase 1 company competitive-intelligence run for ILIA
  Beauty — pool company #2, the first run under the ratified (round-2
  guarded) CSB company-profile contract on a subject other than Tower 28,
  and the first parent-owned subject. Fresh scan; the contract files are the
  only synthesis authority.
use_when:
  - Dispatching the ILIA Phase 1 lane.
  - Adjudicating the returned ILIA bundle (one-by-one cadence gate).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - docs/research/forseti_beauty_us_company_eligibility_pool_v0.md
stale_if:
  - The ILIA bundle lands validator-PASS and is adjudicated (packet consumed).
  - The owner re-sequences the pool or supersedes the CSB contract.
```

## Load Contract

- `packet_version`: 0
- `created_at`: 2026-07-18 Asia/Singapore
- `created_by_lane`: Tower 28 CI/GTM lane; provenance only, not authority
- `load_rule`: confirm-don't-trust. Dispatch-critical reads first: this
  packet, the playbook's operating sequence, the capture recon index rows
  you will use, and the runner command shapes. Read the full contract
  synthesis sections and the validator while acquisition workers run, not
  before dispatching them (adopted run habit; escape hatch: if you genuinely
  need early worker output to design the rest, take it).

## Subject

- **ILIA Beauty** — pool row USBEAUTY-021 (scaling stratum, makeup),
  `docs/research/forseti_beauty_us_company_eligibility_pool_v0.md`.
- **Resolved parent: Famille C** (the pool's parent resolution). This is the
  deliberate new contract stressor: the first parent-owned subject. Entity,
  trademark, and identity checks now have a parent dimension Tower 28
  (independent) never exercised. Where the contract's identity/entity
  handling is ambiguous for a parent-owned Brand, run the defensible
  default, and return the friction as typed feedback — no contract edits
  from this lane.
- `mode: forward`, `time_posture: recency_first`, `as_of` set at dispatch;
  `commission_profile: company_competitive_intelligence`.

## Evidence base: fresh scan

Full fresh scan — no prior typed rows exist for ILIA; nothing is reused.
All acquisition routes through the capture spine under its own authority;
sanctioned routes only; bot walls are typed gaps; no login walls, no cart
interaction.

Run knowledge to reuse (recon index rows; do not rediscover):

- Sephora PDP review sampling: substantive per-review text with the
  verified-purchase marker; classification rows carry verified substantive
  reviews only; existence never stated as concentration or rate.
- US-pinned Amazon vantage for seller-of-record and diversion state. Known
  live bug: the `amazon_pdp_distribution` capture profile's sufficiency
  literals reference an unrelated LANEIGE product (fix in flight) — until it
  merges, profiled Amazon captures may exit non-zero while writing real
  packets; read content from the raw packets as the Tower 28 v2 lane did,
  and record the workaround in the scan receipt.
- Certifier seal directories: endpoint recipes are in the recon index
  (WP REST / Drupal Views / Gatsby page-data patterns) — applicable only if
  ILIA's packs or PDPs actually carry certifier seals; absence of seals is
  simply no check, not a typed gap.

## Report requirements

- The ratified contract governs, including the Executive Intelligence Brief
  directness guards: inference worded as inference even at full directness;
  small or uncorroborated samples support existence, never concentration,
  rates, or comparatives without a cited comparator base.
- Validator PASS (`.agents/hooks/check_commission_signal_board_output.py`)
  before the bundle is presented.
- Three-component bundle: sealed commission board, scan receipt (typed
  access outcomes and capture receipts), completed report.

## Drift Guard

- **Subject independence:** do NOT load the Tower 28 report synthesis
  (either version) or its board. The contract alone shapes this report.
  This run doubles as the first Tower 28 peer for later comparison, and the
  peer value depends on the two reports being independently produced under
  the same contract — no comparison-to-Tower-28 content inside the report.
- Decision-neutral throughout: no pain, buyer, ICP, urgency, wedge, or GTM
  content; the report is also the Company Surface feed for ILIA.
- One-by-one cadence: after this bundle lands, owner adjudication happens
  before any next pool company dispatches.
- No standing monitoring, no schedulers; one bounded run.

## Success signal

A validator-PASS ILIA bundle (board + scan receipt + report with exec
brief), produced under the ratified contract with typed parent-dimension
friction feedback if any — ready for owner adjudication and, downstream,
for first peer use against Tower 28.
