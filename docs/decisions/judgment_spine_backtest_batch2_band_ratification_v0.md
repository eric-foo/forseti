# Judgment Spine — Backtest Batch 2 Band Ratification v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Owner ratification of the facilitator-set scoring bands (frozen_band_inputs)
  for all 9 Batch 2 product-learning cases. Records the owner's acceptance of
  each case's frozen band as the answer key against which the Claude-Sonnet arm
  (and the forthcoming external arms) are scored. This is an external owner
  sign-off that references each frozen facilitator_ledger by its freeze hash; it
  does NOT mutate the frozen ledgers, change any band, alter any score, or touch
  the pinned scoring key. Caps at product-learning.
use_when:
  - Confirming whether a Batch 2 case's band is owner-ratified before relying on its result.
  - Auditing the owner sign-off chain for the Batch 2 scoring key.
authority_boundary: retrieval_only
authored_by: judgment-spine batch-2 coordination lane (Opus 4.8), owner-directed 2026-06-16 (Eric)
open_next:
  - docs/decisions/judgment_spine_backtest_batch2_ledger_declaration_v0.md
  - forseti-harness/cases/product_learning/nueco_fragrance_pivot_v0/cross_vendor_blind_run_findings_v0.md
  - forseti-harness/cases/product_learning/cocokind_holdprice_2025_v0/cross_vendor_blind_run_findings_v0.md
  - forseti-harness/cases/product_learning/saie_price_increase_2025_v0/cross_vendor_blind_run_findings_v0.md
input_hashes:
  orca-harness/scoring/band_scorer.py: D54DCD2CB34A8158232E1A428F70A1F3F182052529D7BC8E5293D5F21A67E1E3
  orca-harness/scoring/mapping_table.py: 8BFD4830A2E3C8FEFEE631B4CE69AF6241BDBDDE585AFAAB09A7791A356AC9E9
branch_or_commit: batch2-panel-continuation @ origin/main 31829fcb
stale_if:
  - The owner revises a ratified band (revise by dated note; a band change is a scoring-key change and stops/rolls the batch).
  - A facilitator_ledger's frozen_band_inputs or freeze hash changes from the value ratified below.
```

## Status

`BATCH2_BANDS_OWNER_RATIFIED` — a batch-local label, not an evidence-ladder
closeout_state or claim tier. The owner **ratified these bands in-thread
2026-06-16 (Eric)**, directing ratification of the slice-2 cases and accepting
extension to the full 9-case set (see Scope note).

## What this ratifies

The owner accepts each case's facilitator-set `frozen_band_inputs` — and the
deterministic band the pinned key derives from them — as the **scoring key** for
that case. This removes the `owner ratification pending` caveat carried in the
per-case findings. It applies to the already-scored Claude-Sonnet arm and to the
forthcoming external arms (GPT-5.5 / Grok 4 / Gemini), which score against the
same frozen bands.

## Ratified bands (all 9 cases)

| case_id (dir) | role | ledger case_id | band | status | facilitator_ledger freeze hash |
|---|---|---|---|---|---|
| kinderbeauty_box_pivot_2023_v0 | holdout | kinderbeauty_box_pivot_2023_v0 | [3,4] | normal | `a337fc7095ed15e520e09837d6a77be71986ba5d7a6bbb8881d16a18ad869ffc` |
| joahbeauty_cvs_kill_2024_v0 | holdout | joahbeauty_cvs_kill_2024_v0 | [6,6] | conflict_escalate | `b969d7acc3a8d35ef7efe411c07cf4785261895fa19f37c35cfa6e1b66b41ba8` |
| privatepacks_retail_retreat_v0 | holdout | privatepacks_retail_retreat_v0 | [6,6] | conflict_escalate | `f3e2daf5989eb4565583eca893ce10baf2cf263116a0af6b944792dd41ac09a4` |
| selflessbyhyram_target_entry_2023_v0 | holdout | selflessbyhyram_target_entry_2023_v0 | [3,4] | normal | `8d0c8f00931bc532c2c03c60700f55d2b69ce56456e3c07f238982d91dee9815` |
| sundaily_gummy_pivot_v0 | holdout | sundaily_gummy_pivot_v0 | [6,6] | conflict_escalate | `1ac2c3591a6a0676a8399c5a626b5d5b136233577ed48e20e9f8bddabc5361c5` |
| imaginaryauthors_sku_kills_2024_v0 | holdout | imaginaryauthors_sku_kills_2024_v0 | [3,5] | normal | `238d4c82135dd729f5116655fbf6177a70c94e54f507f7ed54c0daaf34b9cb02` |
| nueco_fragrance_pivot_v0 | holdout | b2_holdout_h7_v0 (neutralized) | [3,5] | normal | `a9150d51b5150a4b2e69f93b335494cc1fce1058cf5bae9cf885be609e6a54c4` |
| cocokind_holdprice_2025_v0 | dev | cocokind_holdprice_2025_v0 | [1,4] | normal | `71093da84ee9c15a86878e8d698704f8056d99d3dc38b6d9fbb10a1d5900a814` |
| saie_price_increase_2025_v0 | dev | saie_price_increase_2025_v0 | [3,4] | normal | `b1f21470303ac1e26b27248c168ad503d0e2e3579546ef0d952e70f1880829ef` |

7 holdouts + 2 dev = 9. Bands are the deterministic output of the pinned key
(`band_scorer.py` / `mapping_table.py`, `input_hashes` above, unchanged) applied
to each ledger's `frozen_band_inputs`; this record ratifies the band inputs, not
a hand-set band.

## Scope note (owner-directed, with disclosed extension)

The owner explicitly directed ratification of the three slice-2 cases (nueco,
cocokind, saie). The other six slice-1 holdout bands were **equally
facilitator-set and equally `owner (pending)`**; a partial 3-of-9 ratification
would leave the batch scoring key half-signed and the findings caveats
inconsistent. The full 9-case set is therefore ratified here under owner
authority for batch-key coherence. The owner may scope this back to the three
slice-2 cases by dated note.

## Mechanism (why the frozen ledgers are not edited)

Each `facilitator_ledger.yaml` is a frozen artifact: its `ledger_freeze_hash` and
`ledger_authors.second_labeler: owner (pending)` reflect its state **at freeze
time**, and the committed scores / case_reports bind those exact hashes. Editing
the ledgers to flip `second_labeler` would change every freeze hash and strand
the committed score references. Ratification is therefore recorded **externally**
here, referencing each ledger by its frozen hash. The ledgers retain
`owner (pending)` as their accurate frozen-time state; **this record is the
durable, authoritative owner sign-off** that supersedes that caveat.

## What this does NOT change

- No `frozen_band_inputs`, derived band, blind judgement, or score changes.
- The pinned scoring key (`band_scorer.py` / `mapping_table.py`) is unchanged
  (`input_hashes` above match the Batch 1/2 pin). Ratifying bands is **not** a
  key change and does not stop or roll the batch.
- No new claim tier. Results remain **product-learning** signal — not validation,
  readiness, or buyer-proof. Ratification means the owner accepts the answer key,
  not that any result is validated.

## Non-claims

Not validation, not readiness, not buyer-proof, not a claim-tier advance. The
external arms (GPT-5.5 / Grok 4 / Gemini) are owner-run and not yet recorded.
JSG-08 caveats in the per-case findings (notably the saie recognition/outcome
alignment) stand independent of band ratification.
