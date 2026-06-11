---
retrieval_header_version: 1
artifact_role: Decision-adjacent routing record (batch-2 candidate routing, beauty-prioritized; PENDING owner admission). NOT an admission, not a batch declaration.
scope: >
  Routes the consumer-demand candidate pool handoff (14 candidates + 2 completions,
  cut 2026-06-12) into the judgment-spine batch pipeline as a prioritized,
  beauty-first queue for a batch-2 admission pass. Carries the pool's obligations
  and surfaces the owner-gated admission decisions. Admission itself belongs to a
  batch-2 ledger on owner sign-off (batch-1 is the machinery exemplar).
use_when:
  - Running the batch-2 admission pass (recognition checks, dev/holdout, packets).
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
stale_if:
  - A batch-2 ledger admits/rejects these candidates (it takes over those rows).
  - The pool cuts a v1 (re-route from the new pool).
---

# Judgment-Spine Batch-2 Candidate Routing (beauty-first; PENDING owner admission)

Routes `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md` into
the batch pipeline, **beauty prioritized per owner direction (2026-06-12)**. This
records ordering + obligations only; ADMISSION (which cases, dev/holdout, packets)
belongs to a batch-2 ledger on owner sign-off.

## Priority order (beauty first)

**Priority 1 - pure beauty (the wedge).** Clean (US-default) first: row 4 **Kinder
Beauty** (beauty *subscription* - closest to the Beauty Pie #3 family), row 1 Joah,
row 3 Private Packs, row 7 Selfless by Hyram (FAME-founder). Then owner-routed:
row 2 Dear, Klairs (NON-US), row 5 Bonjout (BORDER), row 6 Purito (FAME + NON-US).

**Priority 2 - ingestible beauty.** Row 11 Sundaily, row 13 The Nue Co. (BORDER),
row 14 Kalumi (WEAK - source-depth check), row 12 Manifesto (NON-US).

**Priority 3 - fragrance (beauty-adjacent).** Row 9 Imaginary Authors; then
NON-US: row 8 Puredistance, row 10 Xerjoff (NON-US + CORR).

**Completions** (resolved; optional ready-outcome cases at owner discretion):
C1 cocokind (held), C2 Saie (persisted).

## Obligations carried (bind on admission)

- **Recognition check FIRST** per case-and-model (isolated, web-off, recorded); a
  fail = SWAP signal, not a verdict. FAME rows (6, 7) cannot be used without it.
- **NON-US rows (2, 6, 8, 10, 12) + BORDER (5, 13) route to the owner** (US-default,
  owner direction 2026-06-12).
- Row 14 (Kalumi): source-depth check before admission. Row 10 (Xerjoff): community-
  comparison grade; the decision-grade screen still applies.
- Product-learning cap; nothing here is buyer-proof or judgment-quality evidence.

## Owner decisions (gate admission)

1. Which Priority-1 beauty rows enter batch-2, and how many?
2. NON-US / BORDER inclusion calls (per row).
3. Dev/holdout split + panel (batch-1 pattern).
4. Sign-off to declare the batch-2 ledger.

## Non-claims

Routes and prioritizes only. Admits no candidate, runs no recognition check,
declares no batch, authorizes no capture. The pool and its source ledgers stay
source-of-truth.
