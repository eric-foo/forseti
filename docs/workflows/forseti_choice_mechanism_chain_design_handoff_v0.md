# Choice-Mechanism Chain Design — Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Commissions a bounded design pass for the choice-mechanism chain pillar of
  the CI report: acquisition lenses for below-title-level customer evidence,
  the review classification method, proportionality mechanics, and the
  client-facing chain-card presentation format. The output is a design
  proposal that lands as the chain section of the CSB contract synthesis pass
  recorded in the adjudication ledger — never standalone doctrine.
use_when:
  - Dispatching the chain design lane.
  - Adjudicating the returned design proposal into the contract pass.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_ci_report_external_review_adjudication_ledger_v0.md
  - docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
stale_if:
  - The design proposal is adjudicated into the contract pass (packet consumed).
  - The owner changes any chain-pillar ruling in the adjudication ledger.
```

## Load Contract

- `packet_version`: 0
- `created_at`: 2026-07-17 Asia/Singapore
- `created_by_lane`: Tower 28 CI corrections lane (branch `claude/tower28-c1-corrections-c5-validator`); provenance only, not authority
- `load_rule`: confirm-don't-trust; the adjudication ledger's item 4 rulings are the binding design constraints — reread them from the ledger, not from this packet's paraphrase

## What the chain is

For each hero product: claim → why customers buy → what they experience →
which complaints attack the claim → where defectors go, every link resolving
to observation rows. It is the report's single best synthesis device (owner-
rated); this handoff designs how it gets fed and how it gets shown.

## Commission (four design deliverables)

### D1 — Acquisition lenses (below title level)

Design which sources and reads feed the chain's middle links (motivation and
experience), using the sanctioned routes already in use (retailer review
surfaces, sanctioned listing reads, public web). Do not add restraint language
beyond existing doctrine — owner ruling: the doctrine-stated routes are the
boundary, restated caveats are noise. Name what each lens can and cannot see.

### D2 — Review classification method

The five-way complaint classification (core-positioning threat / ordinary
defect / education gap / price-value / substantiation risk) applied to review
bodies, with the substantiveness filter as the admission rule:

- classify only substantive reviews — verified-purchase where the surface
  exposes it, non-trivial body text;
- contentless drive-by star ratings are excluded from classification
  (aggregate star distributions are collected separately and already carry
  them);
- each classified review records: product, star, class, the claim it attacks
  (if any), specificity marker (vague vs mechanism/ingredient-specific), date.

### D3 — Proportionality mechanics (binding rulings from the ledger)

- Proportions are of STATED SAMPLES only ("12 of 50 sampled substantive
  negative reviews"), never population rates.
- No background/comparator base-rate tracking — owner rejected it as
  unmaintainable; assume category background exists and say so.
- The claim-amplification principle does the base-rate's job: an explicit
  brand claim amplifies any complaint that attacks it — the stronger and more
  specific the claim, the more a claim-attacking complaint counts. Design how
  the chain card expresses this weighting honestly.

### D4 — Chain-card presentation format

One card per hero product: a mechanism sentence on top (the aggressive,
decision-bearing line), five cells beneath (claim / buy-reason / experience /
complaint class / substitute), each cell carrying its observation ids and a
confidence mark. Show how a card compresses to one 5-field front-page
conclusion row. Produce ONE worked example filled entirely from the existing
Tower 28 v1 report observations — no new scanning in this lane.

## Drift Guard

- Design pass only: no scanning, no capture, no contract edits, no new
  schema or validator fields — the output is a proposal for the contract pass.
- Claim discipline stays Forseti's: describe substitution citing and
  complaint composition; never demand capture, sell-through, or rate claims.
- Monitoring cadence is out of scope (co-movement is the future longitudinal
  seed; this design is point-in-time).

## Success signal

A design proposal the owner can adjudicate in one pass: the four deliverables
above, each with its limits named, plus the single Tower 28 worked example —
ready to slot into the contract-pass PR as the chain section.
