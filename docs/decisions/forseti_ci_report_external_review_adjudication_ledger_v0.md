# CI Report External Review Adjudication Ledger v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Adjudicated agreements from the external (multi-vendor LLM) assessments of
  the Tower 28 Phase 1 CI report bundle, plus the owner rulings that bind them.
  This ledger is the single accumulation point for the deferred CSB
  company-profile contract synthesis upgrade: the contract pass executes only
  from items recorded here, after all external responses are adjudicated.
use_when:
  - Executing or planning the CSB company-profile contract synthesis upgrade
    (exec brief, concentration, choice-mechanism chain, readability).
  - Adjudicating a further external assessment of a CI report bundle.
  - Checking whether a proposed report-shape idea was already accepted,
    deferred, or rejected.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
  - docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md
stale_if:
  - The CSB company-profile contract lands the synthesis upgrade (this ledger
    then becomes historical input, superseded by the contract itself).
  - The owner reverses any ruling recorded here.
```

Authority: owner rulings in chat, 2026-07-17. Status: OPEN — awaiting
adjudication of 1-2 remaining external responses before the contract pass.
Next source after the contract pass lands: the CSB contract files named in
`open_next`.

## How this ledger works

External evaluators (2-3 independent ChatGPT Pro sessions) assessed the Tower
28 Phase 1 bundle (report + scan receipt + CSB board; Phase 2 excluded) for
CI-worthiness. Each batch is adjudicated confirm-don't-trust against the
artifacts; every falsifiable claim is verified by direct read before
acceptance. Batch 1's falsifiable defect claims verified 4-for-4 correct.

## Accepted — corrections (EXECUTED, this lane)

| Item | Disposition |
| --- | --- |
| Sub-scout operations arithmetic (91 vs actual 101; ~110 vs ~120) | Fixed in scan receipt; per-scout addends now stated inline |
| OBS-002 pointer cited OBS-016 (lipgloss thread) for leadership-continuity absence; correct row is OBS-015 (negative bundle) | Fixed in report |
| Scan "seven-item" SOS family listing 8 tokens | Fixed: refill-folds-into-spray convention stated in scan (report already carried it) |
| $12-$34 price range untraceable to any excerpt | Fixed: serum $34 (genuinely observed in the M01 Sephora page-state read) added to OBS-008 excerpt; CSC-002 reworded to match observed catalog states |
| Scan SOBS-027 asserted "2026-02" Pvolve placement flatly | Fixed: month is article framing, not verified event date (report already caveated) |
| Report as_of 2026-07-17 vs commission as_of 2026-07-16 | Fixed: amendment note added; no claim gains recency from the advance |
| Overreach wording ("dominate creator titles", "recurring" without volume, "claims-contradiction complaint", "owning legal entity resolves to") | Softened to literal observed strength |
| Dangling observation references possible | Validator now emits `dangling_observation_reference` for any OBS token without a ledger row (mechanical; semantic mispointing remains review work) |
| Reviews missed arithmetic/pointer/traceability defects | Review Prompt Defaults now bind a provenance-accuracy goal with observable success signals for evidence-bearing artifacts |

## Accepted — contract synthesis upgrade (DEFERRED until this ledger closes)

Owner rule: guidance-only, no new schema, ledgers, or validator fields unless
separately agreed; recurring toll must stay "write better conclusions", not
"fill more forms". Owner rule on lens-status vocabulary: do not over-restrict —
a definition line at most.

| # | Item | Owner ruling |
| --- | --- | --- |
| 1 | Organize synthesis around commercial decisions | Owner accepts the criticism at full strength (external score 3/10 on this axis); the exec layer is mandatory, not optional |
| 2 | Concentration synthesis (publicly visible concentration, never revenue concentration) | Accepted; retailer-coverage breadth noted as thin — see retailer probe below |
| 3 | Momentum classification | Vocabulary accepted for the future longitudinal product; renamed **co-movement** (owner, 2026-07-17); not adoptable now — consumes time series we deliberately do not collect. Boundary note: our current aligned-signal discipline is spatial (same theme across independent venues at one point in time); co-movement is temporal (signals moving together across snapshots) and needs at least two observation dates |
| 4 | Customer-choice mechanism chain + claims-to-complaints five-way classification | Accepted — rated the single best external item; claim discipline stays ours (describe substitution citing, never demand capture). Proportionality rule (owner, 2026-07-17): never state a complaint rate without a denominator; classify a theme by WHICH claim it attacks, not by volume; name an expected-background class (idiosyncratic/allergy-type reactions every sensitive-skin brand accrues) — a theme graduates from background to core-positioning threat only when it is ingredient-specific, repeated across independent venues, or attacks the load-bearing claim directly |
| 5 | Defensibility / attack-surface read | Accepted as a Phase 2 adjudication-layer lens, not Phase 1 substrate. Priming rule (owner, 2026-07-17): the CSB Phase 1 contract should prime collection of defensibility RAW MATERIAL — comparator claims language, substitution economics, price-gap observations, claims-parity reads — without making the defensibility judgment |
| 6 | Invalidation signals stated inside Phase 1 chronology synthesis | Accepted |
| 7 | Research priority order (retail/customer/claims first) | Accepted as-is |
| 8 | Linked-commercial-claim admission principle | Principle accepted; their typed relationship schema rejected — we use our existing observation/candidate structure |
| 9 | 5-field front-page conclusions (claim / evidence / consequence / confidence / next observable) | Accepted; owner ruling: maximum aggressiveness in decision consequence and confidence-stating — the admission fields (evidence bound + next observable) are what make aggressiveness safe; never aggressiveness via evidence overclaim |
| 10 | Central promise (where value resides, what drives it, is it strengthening, what threatens it) | Accepted as the report's front-page voice AND as the internal decision-adjudication frame; rejected as the product center (product center stays decision adjudication, owner-locked) |
| 11 | Readability | Owner requires the report be "way more readable": exec brief as h2 preamble, plain-language section leads, the two cheap matrices (SKU reception; known/inferred/unknown) as plain markdown tables; audit ledgers stay but move visually behind the narrative |
| 12 | Evidence-preservation trigger | Same deferral as the contract pass. Governing rule accepted: preserve (screenshot/HTML) what could change a conclusion, be disputed, or disappear; negatives need route+date+query only. Routed to the Capture seam as a capture-request trigger, not a data-lake build. Bloat control: conclusion-bearing observations only — for a Tower 28-scale run that is roughly 10-30 captures, not a crawl. Mechanics (owner discussion 2026-07-17): single-file HTML (MHTML/SingleFile-style) preferred — text-searchable, diffable, ~1-5 MB raw and compresses 80-90%; full-page screenshot only when layout itself is the evidence, auto-compressed to WebP; auto-compression is a one-line adapter step, worth doing, no further engineering |

## Open questions feeding the same pass

- Retailer breadth: HANDOFF WRITTEN (owner-directed, 2026-07-17) —
  `docs/workflows/forseti_capture_beauty_retailer_surface_probe_handoff_v0.md`.
  Capture spine first proposes a subject-agnostic bound-target list beyond the
  four known candidates; owner binds before any probe. Geographic default:
  US-first comparison spine + one bounded home-market read where the subject's
  home market differs (owner-overridable at binding).
- Remaining external responses: adjudicate into this ledger before the
  contract pass (owner to confirm how many are still outstanding).

## Rejected (do not resurrect without new owner word)

- CI report as the product center (product center: decision adjudication).
- Demand-leakage phrasing and any "captures customers" style demand claims
  from public proxies.
- Standing monitoring / crawler now (monitoring-eligibility gate stands).
- Their typed relationship-ledger schema (ceremony debt).
- Arithmetic-reconciliation validator checks (brittle; provenance review pass
  covers the class).

## Trigger to close this ledger

All external batches adjudicated + owner says "go" on the contract pass →
one bounded PR to the CSB company-profile contract files applies every
DEFERRED-accepted item above, then this ledger's stale_if fires.
