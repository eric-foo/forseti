# Judgment Spine — Backtest Batch 2 Ledger Declaration v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Pre-declared ledger for product-learning backtest batch 2 (beauty-vertical
  consumer-demand decisions): the 9 pre-cutoff Wayback Source Capture candidate
  cases (~75 INV-1 units, merged to main) admitted as ONE pre-committed set,
  with dev/holdout marking, the Batch-1 frozen scoring key inherited unchanged,
  the Batch-1 contestant panel, execution rules, anti-cherry-pick
  pre-commitment, all-results reporting commitment, and screen provenance.
  Caps at product-learning; covers by-hand runs only.
use_when:
  - Running, swapping, scoring, or reporting any batch-2 backtest case.
  - Checking what batch 2 may claim and what its results bind.
  - Auditing batch-2 case selection against the anti-cherry-pick rule.
authority_boundary: retrieval_only
open_next:
  - docs/product/foundation/consumer_demand_candidate_pool_handoff_v0.md
  - docs/decisions/judgment_spine_backtest_batch2_candidate_routing_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
  - orca-harness/cases/product_learning/inoreader_repricing_2019_v0/cross_vendor_blind_run_findings_v0.md
input_hashes:
  orca-harness/scoring/band_scorer.py: D54DCD2CB34A8158232E1A428F70A1F3F182052529D7BC8E5293D5F21A67E1E3
  orca-harness/scoring/mapping_table.py: 8BFD4830A2E3C8FEFEE631B4CE69AF6241BDBDDE585AFAAB09A7791A356AC9E9
branch_or_commit: judgment-spine-batch2-ledger @ origin/main 8147e30d (worktree clean except this declaration)
stale_if:
  - The owner amends the case list, split, or panel (amend by dated note, not silent rewrite).
  - An owner-accepted scoring-key change lands (the batch stops; see Key Pin).
  - The batch closes with its distillation record (this ledger becomes historical).
```

## Status

`BATCH2_ACTIVE_OWNER_SIGNED` — a batch-local label, not an evidence-ladder
closeout_state or claim tier. This declaration pre-commits the admitted set and
discipline; the owner **signed it in-thread 2026-06-16 (Eric)**, advancing it
from `BATCH2_DECLARED_PENDING_OWNER_SIGNOFF` to `BATCH2_ACTIVE_OWNER_SIGNED`.

The owner selected these parameters in-thread 2026-06-15 and signed the
declaration 2026-06-16: (a) a **new Batch 2** (not a
Batch-1 amendment); (b) **all 9** captured candidate cases admitted as the
pre-committed set; (c) **The Nue Co.** (border US/UK) included by explicit owner
call and **fragrance confirmed in-family**; (d) the **Batch-1 contestant panel**
reused; (e) the **Batch-1 frozen scoring key inherited unchanged**; (f) the
dev/holdout split below. Later changes are dated-amendment-only.

## Authorization Basis And Cap

- Owner, in-thread, 2026-06-15: "new batch 2"; "include both" (Nue Co border +
  fragrance in-family); "same panel"; pinned key confirmed; the proposed
  dev/holdout split accepted.
- Covers: by-hand contestant runs (fresh chat-surface or sub-agent sessions)
  plus deterministic scoring via `orca-harness/runners/run_case.py`, at
  product-learning tier.
- Does NOT cover: live raw-API provider calls (each needs its own authorization
  record), scoring-key changes, JQ-lane builds (D5 propagation, tooled runner,
  sealed pool), fixture admission, buyer contact, or a JSG-01 unfreeze.
- Claim cap: product-learning per
  `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`;
  the chat/manual execution surface is permanently non-gate-clearing per
  `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md`.

## Source Pool Provenance

The admitted cases are the **L1 capture corpus**: 9 cases / ~75 INV-1 units of
pre-cutoff Wayback Source Capture evidence, built byte-faithful and merged to
`origin/main`. They were drawn from the consumer-demand candidate roster
(`docs/product/foundation/consumer_demand_candidate_pool_handoff_v0.md`, blob
`b26fb9c1`) and routed into the batch pipeline, beauty-first, by
`docs/decisions/judgment_spine_backtest_batch2_candidate_routing_v0.md` (blob
`748b6285`). The roster's consuming-batch obligations (isolation screen first;
NON-US/BORDER owner routing; product-learning cap) bind here. The captures are
evidence inputs only — admission to backtest status is this ledger's act.

## Ledger (pre-declared; every result will be reported)

| # | Case (harness dir under `orca-harness/cases/product_learning/`) | Roster row | Sector / decision family | Type | Split | Entry basis |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `kinderbeauty_box_pivot_2023_v0` | #4 Kinder Beauty | beauty subscription — box-economics pivot (Mar 2023) | decide | holdout | captured pool, owner-admitted 2026-06-15 |
| 2 | `joahbeauty_cvs_kill_2024_v0` | #1 Joah Beauty (Kiss) | beauty — CVS-exclusive line kill (2024) | decide | holdout | captured pool, owner-admitted 2026-06-15 |
| 3 | `privatepacks_retail_retreat_v0` | #3 Private Packs | beauty/personal-care — retail retreat + DTC pivot | decide | holdout | captured pool, owner-admitted 2026-06-15 |
| 4 | `selflessbyhyram_target_entry_2023_v0` | #7 Selfless by Hyram | beauty — channel saga / Target repricing entry (Feb 2023) | decide | holdout | captured pool, owner-admitted 2026-06-15; FAME-founder → isolation screen required |
| 5 | `sundaily_gummy_pivot_v0` | #11 Sundaily (ex-Sundots) | ingestible beauty — UV→skin-health repositioning | decide | holdout | captured pool, owner-admitted 2026-06-15 |
| 6 | `nueco_fragrance_pivot_v0` | #13 The Nue Co. | ingestible→fragrance-first pivot | decide | holdout | captured pool, owner-admitted 2026-06-15; BORDER (US/UK) included by owner call |
| 7 | `imaginaryauthors_sku_kills_2024_v0` | #9 Imaginary Authors | fragrance — quiet SKU kills (2024) | decide | holdout | captured pool, owner-admitted 2026-06-15 |
| 8 | `cocokind_holdprice_2025_v0` | C1 cocokind | beauty — tariff hold-price (June 2025, HELD) | confirm | dev | captured pool, owner-admitted 2026-06-15 |
| 9 | `saie_price_increase_2025_v0` | C2 Saie | beauty — +$1–4 increase (June 2025, PERSISTED) | confirm | dev | captured pool, owner-admitted 2026-06-15 |

Dev/holdout meaning (batch-local vocabulary, same as Batch 1): dev cases may
inform key/harness critique and proposed changes; holdout cases are run once
under the pinned key and only reported — no key or harness iteration may
condition on them. **Dev = the two confirm-type completions (#8 cocokind, #9
Saie)** — held/persisted outcomes, lower-stakes, used to shake out packet shape
and the decide-vs-confirm read. **Holdout = the seven decide-type cases (#1–#7)**
— genuine pivot/kill/channel decisions reserved as untainted test signal.
Harness case IDs are assigned at packet construction.

## Anti-Cherry-Pick Pre-Commitment (load-bearing)

The 9 captures were selected **outcome-aware** (each case dir encodes the
decision and its later outcome). To preserve the batch's anti-cherry-pick
property, this declaration fixes — **now, before any outcome-blind packet is
built, any contestant run, or any gate/reveal**:

- **The full admitted set is all 9 cases, and every case is run and reported.**
  Inclusion cannot correlate with favorability because the set is closed here,
  before the outcome-aware step. Report **all** results — in-band / over / under,
  failures, exclusions, swaps, and contaminated arms (recorded-as-data).
  Selective admission or selective reporting voids the anti-cherry-pick property.
- **The selection rule is feasibility-based, not outcome-based:** "every
  currently-captured (pre-cutoff, byte-faithful, merged) US-default or
  border-US beauty-vertical consumer-demand case." The roster rows **excluded**
  from this set were excluded for capture-feasibility / flag reasons recorded in
  the roster — pure NON-US (Dear Klairs, Purito, Manifesto, Puredistance,
  Xerjoff), WEAK receipt (Kalumi), FR-founded border (Bonjout) — **not** for
  outcome. The two border-US rows that WERE captured (Selfless, Nue Co) are
  admitted, not dropped.
- **Honest claim this enables:** "the demand-read called K of 9 in-band across 9
  pre-committed cases," not "here is a case where it worked." This mirrors the
  Batch-1 Org-Motion Batch Pre-Commitment precedent (fix the run-on-all set
  before the reveal so inclusion cannot track favorability).

## Recognition / Isolation Discipline (inherited)

Per the Batch-1 amendment of 2026-06-12 (active recall dropped):

- A **non-inducing pre-judgment isolation screen** (structural web-off /
  `isolation_result == proven`, recorded) precedes any judgment. Active
  "name the case" recall is **dropped** (it manufactures recognition).
- **Recognition capacity alone is not contamination and not a swap signal.**
  Contamination is **outcome-USE**, caught after the fact by tell-auditing the
  required reasoning trace at JSG-08; a confirmed outcome-use tell routes the
  arm to contaminated / **quarantine = recorded-as-data, not discarded**.
- **#4 Selfless by Hyram** carries a famous founder — the highest
  recognition/leakage risk in the set. The isolation screen is **mandatory**,
  and it is the **first swap candidate only if isolation cannot be proven**. A
  fame/obscurity screen may inform that swap selection but is not a gate.

## Swap Behavior (pre-commitment-preserving)

Because the set is pre-committed and the remaining roster rows are not yet
captured, a case that **cannot clear the isolation screen** is recorded as
**contaminated / quarantine (recorded-as-data, not discarded)** — it is not
silently dropped. Admitting a replacement case requires a **dated owner-signed
amendment** plus a captured, byte-faithful same-family alternate; the swap event
is itself recorded as a batch finding. There is no silent post-hoc swap.

## Key Pin

The scoring key is frozen for the entire batch as implemented at the
`input_hashes` above. This is the **same frozen key as Batch 1** —
`orca-harness/scoring/band_scorer.py` and `orca-harness/scoring/mapping_table.py`
SHA-256 verified **byte-identical** to the Batch-1 pin on `origin/main`
(2026-06-15). The `option_value: high` → action-floor-4 rule stands **AS-IS**
(Batch 2 measures that rule, it does not change it). An owner-accepted key change
stops the batch; unrun cases roll into a new ledger under the new pin. Proposed
key changes belong only in the closing distillation record.

## Execution Rules

- Contestant runs happen only in fresh isolated sessions (chat surface or
  sub-agent), web search OFF (structural where the surface allows; recorded),
  against zero-spoiler packets.
- The planning thread that authored this ledger is outcome-aware for every case;
  no contestant run may be primed from it.
- A non-inducing isolation screen per case-and-model precedes any judgment (see
  Recognition / Isolation Discipline).
- Default panel (owner-confirmed 2026-06-15, = the Batch-1 panel): Claude
  Sonnet-class, GPT-5.5, Grok 4, plus Gemini subject to the isolation screen.
  Per-case isolation decides clean vs contaminated arms; contaminated arms are
  recorded as data, not discarded.
- Scoring: `orca-harness/runners/run_case.py` against the pinned key; one
  findings record per case (the Inoreader cross-vendor findings record is the
  exemplar shape).
- All results reported: in-band / over / under, failures, exclusions, swaps,
  quarantines. Selective reporting voids the batch's anti-cherry-pick property.

## Outcome-Blind Packet Construction

Contestant packets are **zero-spoiler**: a DERIVED, stripped artifact, not the
raw outcome-labelled case dir, built by an actor **not holding the sealed
outcome**. The merged capture packets are **INV-1** — observed facts + limits
only; reused AS source evidence, never edited to add scores/weights/ranks/
verdicts. Per-unit **pre-cutoff** compliance and **byte-faithfulness** (body-sha
vs manifest) are re-verified at packet construction, before any run.

## Closing Artifact

The batch closes with one distillation record: the K-of-9 in-band tally across
the pre-committed set; the decide-vs-confirm read (the 2 dev completions vs the 7
holdout decisions); the recognition/isolation-to-call map; proposed-not-applied
key changes (owner-gated); and venues-used provenance.

## Non-Claims

- Not validation, readiness, buyer proof, or judgment-quality evidence; the
  product-learning cap holds for every batch-2 result.
- Not live-API authorization; not a scoring-key change; not fixture admission;
  not a JSG-01 unfreeze; not case-finder-frame sign-off; not D5 propagation.
- **Org-motion is NOT part of this batch.** Batch 2 is the consumer-demand
  Wayback capture corpus; the Batch-1 org-motion probe was Batch-1-scoped and is
  not promoted or carried here.
- Mints no ladder vocabulary: dev/holdout and the Status label are batch-local.
- This ledger's existence proves selection discipline only — it proves nothing
  about result quality.

## Owner Signature (recorded)

This declaration is `BATCH2_ACTIVE_OWNER_SIGNED` — owner signed in-thread
2026-06-16 (Eric); parameters selected 2026-06-15. The pre-committed set, split,
panel, and frozen-key pin above are now locked; later changes are
dated-amendment-only. The standard batch flow is hereby authorized: outcome-blind
packet construction (by an actor not holding the outcomes) → blind/isolated
contestant runs → `run_case.py` scoring against the pinned key → one findings
record per case, all reported. The runs remain owner-cap-bound (product-learning;
no live-API; no scoring-key change).
