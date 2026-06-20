# Consumer-Demand Candidate Pool Handoff v0 (one-shot, dated)

```yaml
retrieval_header_version: 1
artifact_role: Discovery-lane output handoff (one-shot candidate pool consolidation; NOT a maintained registry)
scope: >
  Consolidates every unconsumed screen candidate from the discovery lane's
  three screens (beauty proving screen 2; beauty subtle screen 3; ingestible
  beauty screen 1) into one read for a consuming batch: 14 candidates + 2
  resolved completions, with all flags carried (fame/recognition-check,
  non-US per the 2026-06-12 owner direction, weak-receipt, corroborated
  A-leg, boundary rulings) and the consuming-batch obligations stated. Cut
  2026-06-12; never updated in place — a later screen cuts a v1.
use_when:
  - Commissioning or running a backtest-batch admission pass (recognition
    checks, swap placement, dev/holdout, packets) over discovery output.
  - Feeding post-ratification consumer-demand work raw case material.
  - Checking what the discovery lane has produced without reading 3 ledgers.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/foundation/vertical_exploration/orca_memorization_resistant_case_finder_frame_v0.md   # operative obscurity bar + probe protocol
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md        # recognition/swap/split machinery exemplar
  - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md # claim caps for any consumer
stale_if:
  - Any batch admits or rejects candidates from this pool (that batch's ledger takes over those rows).
  - A new screen produces candidates (cut consumer_demand_candidate_pool_handoff_v1; this version becomes historical).
  - The owner retires or re-scopes the pool.
```

## What this is — and is not

The discovery lane's unconsumed output, made consumable in ONE read. It is a
dated handoff, not a registry: it is never edited after cut (the source
ledgers remain the source of truth for every row), it asserts nothing about
any candidate's current state, and admission decisions belong entirely to the
consuming batch's own ledger.

## The Pool (14 candidates + 2 completions; cut 2026-06-12)

Flags: FAME = recognition check required before any use; NON-US = treat per
owner direction 2026-06-12 (US brands/ecosystem default; consuming batch
routes inclusion to the owner or defers the row); WEAK = receipt depth below
bar, source-depth check required; CORR = admitted under the corroborated
material-change A-leg (community-comparison grade, not lab grade); BORDER =
boundary ruling recorded in the source ledger.

| # | Brand | Vertical | Decision (DecisionEvent) (one line) | Class | Flags | Source ledger |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Joah Beauty (Kiss Products) | beauty | CVS-exclusive K-beauty line killed: socials wiped June 2024, Apr 2025 closure + liquidation | newsy | — | screen 2 |
| 2 | Dear, Klairs (Wishtrend) | beauty | Suspend-and-replace: re-tested own bestseller post-Purito (SPF 28 vs 50+), suspended all sunscreen sales + refunds, relaunched verified | newsy | NON-US (KR) | screen 2 |
| 3 | Private Packs | beauty/personal care | Retail retreat from ~1,000 CVS + ~250 Target doors on velocity miss; ~$100K infra written off; DTC pivot | newsy | — | screen 2 |
| 4 | Kinder Beauty | beauty subscription | Box-economics pivot Mar 2023; shutdown Jan 2024; decay documented pre-announcement by r/BeautyBoxes | newsy | — | screen 2 |
| 5 | Bonjout Beauty | beauty | Single-SKU moratorium 2023–2025 despite demand; reversed Apr 2026 on 2,400-customer focus group | newsy | BORDER (FR-founded, US-market) | screen 2 |
| 6 | Purito | beauty | Recall-and-reformulate after independent lab SPF tests (Dec 2020); new manufacturer; verified relaunch | newsy | FAME + NON-US (KR) | screen 2 |
| 7 | Selfless by Hyram | beauty | Channel saga: Sephora exit -> Target repricing entry (Feb 2023) -> founder buyback -> Target exit (Apr 2025) | newsy | FAME (founder) | screen 2 |
| 8 | Puredistance | fragrance (beauty-adjacent) | IFRA-forced kill of original M + reformulated V2Q replacement (2022); stockpiling + secondary-market premium | subtle | NON-US (NL) | screen 3 |
| 9 | Imaginary Authors | fragrance | Quiet SKU kills: Whispered Myths + Telegrama (Aug 2024), 8 total kills on product-info page, low-sales rationale | subtle | — | screen 3 |
| 10 | Xerjoff (Irisss) | fragrance | SILENT reformulation never acknowledged; two community detection waves years apart; old-bottle premium | subtle | NON-US (IT) + CORR | screen 3 (owner-direction note) |
| 11 | Sundaily (ex-Sundots) | ingestible beauty | Full pivot: UV-protectant ingestible repositioned to skin-health gummies; Goop validation followed | newsy | — | ingestible screen 1 |
| 12 | Manifesto | ingestible beauty | Regulatory-forced reformulation (France E171 ban): 6-month delay accepted for EU access; Cult Beauty entry | newsy | NON-US (UK) | ingestible screen 1 |
| 13 | The Nue Co. | ingestible beauty | Pivot OUT of supplements to fragrance-first (fragrance 20%->65% of revenue; CAC halved; Ulta exclusive) | newsy | BORDER (exit decision; US/UK hybrid) | ingestible screen 1 |
| 14 | Kalumi BEAUTYfood | ingestible beauty | Pandemic reformulation + downward repricing (MCT added while price cut) | newsy | WEAK (snippet-grade action receipt) | ingestible screen 1 |

Completions (resolved, recorded-not-promoted by their screen; available as
candidates at the consumer's discretion):

| C | Brand | Resolution | Source |
| --- | --- | --- | --- |
| C1 | cocokind | Tariff hold-price decision (June 2025) HELD through at least June 2026 (soft O-leg: absence-of-increase evidence + stable site prices + absent from raiser lists) | screen 3 ledger, completions |
| C2 | Saie | +$1–4 increase (June 2025) PERSISTED into 2026 (BeautyMatter raiser list; brand community posts as action receipts) | screen 3 ledger, completions |

Full receipts per row live in the source ledgers:
`docs/decisions/venue_procedure_proving_screen_beauty_ledger_v0.md` (screen 2),
`docs/decisions/beauty_subtle_decision_screen3_ledger_v0.md` (screen 3),
`docs/decisions/ingestible_beauty_screen1_ledger_v0.md` (ingestible screen 1).
This packet deliberately does not duplicate URL sets.

## Consuming-Batch Obligations (bind on any consumer)

1. RECOGNITION CHECKS FIRST, per the finder frame's operative bar: isolated
   probe session per case-and-model pair; contestant web search OFF
   (structural, recorded); a probe fail is a SWAP signal, not a verdict.
   FAME rows (6, 7) cannot be used without this; running it on every used row
   is the conservative default.
2. NON-US rows (2, 6, 8, 10, 12) follow the owner direction of 2026-06-12:
   US brands/ecosystem is the default — route inclusion to the owner or defer
   the row. BORDER rows (5, 13) get an explicit call.
3. Row 14 (Kalumi) requires a source-depth check before admission (its action
   receipt is snippet-grade).
4. Row 10 (Xerjoff) was admitted under the corroborated material-change A-leg
   — its evidence is community-comparison grade, not lab grade; the
   decision-grade screen still applies.
5. Admission, swap placement, dev/holdout split, packet construction, and all
   results reporting belong to the CONSUMER's own ledger (batch-1 ledger is
   the machinery exemplar). This packet records none of it.
6. Claim caps per the evidence ladder: product-learning tier; nothing here is
   buyer proof or judgment-quality evidence.

## Non-Claims

Not validation, readiness, buyer proof, or judgment-quality evidence; no
candidate is admitted, recognized-checked, or packet-ready. Not a registry:
one-shot, dated, never updated in place; the source ledgers stay the source
of truth. Authorizes no batch, no capture, no screen.

## Lane Note

Cut by the pre-capture discovery CA lane under owner in-thread authorization
(2026-06-12, "let's continue with recommended move"), gated by
workflow-assumption-gate (READY_WITH_VERIFIED_LEDGER, in-thread). Uncommitted
at cut; commit on owner word.
