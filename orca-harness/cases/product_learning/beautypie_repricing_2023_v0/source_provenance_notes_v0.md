---
retrieval_header_version: 1
artifact_role: Facilitator-side source-provenance record (NOT contestant-visible; not a band input)
scope: >
  Per-evidence-unit provenance for case beautypie_repricing_2023_v0 after Phase-4 capture: what is
  archive-captured, what is a case-stated construction premise, and what is a general base rate. Records
  the honest sourcing limits behind the participant packets' source_manifest before freeze.
use_when:
  - Auditing what each E-unit (E1-E9) is actually sourced from before/after the fixture freeze.
  - Checking the E2 membership-structure provenance limitation and the org-motion trajectory correction.
authority_boundary: retrieval_only
open_next:
  - docs/research/orgmotion_beautypie_capture_feasibility_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
---

# Source Provenance Notes — beautypie_repricing_2023_v0 (v0)

Facilitator-side record. This is **not** part of the contestant-visible packet and is **not** a band
input. It documents, honestly, what each evidence unit is sourced from after the Phase-4 capture, so the
fixture is not frozen asserting provenance it does not have. All captures are Wayback archive snapshots
retrieved via the `archive_org` adapter (`select_snapshot ≤ cutoff`), each verified pre-cutoff with the
served body equal to the selected snapshot (no availability≠body redirect).

## Captured evidence (real SourceCapturePackets, body-verified)

| E | what it sources | snapshot | sha256 (body) | packet |
| --- | --- | --- | --- | --- |
| E1 | factory-direct / at-cost membership model (no middlemen/markups; members buy near making-cost; ~10× less than retail) | 2023-02-25 | `1dad75a2…0c03745d` | `source_captures/e1_homepage_20230225/` |
| E2 | **£10/mo monthly membership** + the factory-direct/at-cost model (how-it-works page) | 2022-12-01 | `07aab083…415ef425` | `source_captures/e2_howitworks_20221201/` |
| E3 | UK cost-of-living / elevated-inflation context (ONS CPI bulletin) | 2023-02-16 | `cd358676…64af5f3fe` | `source_captures/e3_ons_cpi_20230216/` |
| E6 | org-motion arm — Greenhouse board, cutoff-proximate, **8 open roles** | 2023-01-31 | `31e77e7f…e427e13e38d` | `source_captures/e6_greenhouse_20230131/` |
| E7 | org-motion arm — Greenhouse board trajectory point, **7 open roles** | 2022-10-02 | `69487a06…79f2c8757` | `source_captures/e7_greenhouse_20221002/` |
| E8 | org-motion arm — Greenhouse board trajectory point, **7 open roles** | 2022-06-29 | `7dae8856…93dc7920e` | `source_captures/e8_greenhouse_20220629/` |
| E9 | org-motion arm — Greenhouse board trajectory point, **11 open roles** | 2022-01-23 | `096e5f11…3c864c7ef` | `source_captures/e9_greenhouse_20220123/` |

## E2 — case-stated construction premise (the load-bearing limitation)

The decision question turns on the **£5/mo entry tier**, the **£59/yr "Beauty Pie Plus" annual**, and the
**per-tier monthly spending limits**. These are **not archive-sourced**. Verified absent across both the
E1 and E2 captured bodies, including the Next.js embedded JSON, under every field-name variant
(`£59`×0; `spend`/`allowance`/`spendLimit`/`monthlyAllowance`/`cap`×0; `Little Pie`/`Big Pie`×0; the only
membership price in any body is "£10 MONTHLY MEMBERSHIP"; `£5` occurrences are product prices).

These facts are therefore treated as a **case-stated construction premise** — real-in-the-world,
asserted as the scenario's ground truth per the packet's `permitted_assumptions` ("Treat the prices,
tiers, and monthly spending limits in the evidence as real"), and **corroborated** by the captured £10/mo
membership + factory-direct model, but **not independently archive-sourced**. This is the honest N=1
limitation, **owner-accepted this session (option B)**. The contestant-visible `source_manifest` is kept
neutral (it claims only what E2's capture evidences); this note carries the full scope so the freeze does
not encode a false sourcing claim. A bounded archive probe to source the tier structure (FAQ / near-cutoff
membership snapshot) was deferred rather than chased (disproportionate to one product-learning point).

## E4 / E5 — general base rates (asserted priors)

Not retrieved documents. `source_type: general_base_rate` — standing analytic priors, true at and before
the cutoff by construction; `retrieval_timestamp` and `hash` carry the sentinel `not_applicable_base_rate`.
Freeze-integrity of their asserted text is carried by `ledger_freeze_hash` over the whole ledger.

## Org-motion trajectory correction (E6–E9)

The gate-0 by-hand feasibility probe
(`docs/research/orgmotion_beautypie_capture_feasibility_v0.md`) stated the open-role count "grew over the
window" (inferred from body size). The Phase-4 adapter captures **contradict** that: the actual open-role
count is **11 → 7 → 7 → 8** (highest at the start, not monotonic growth). Per the ledger amendment's
anti-steering rule (raw counts/departments/trajectory, never an editorialized "expanding"), the augmented
packet's org-motion block was corrected to the captured per-snapshot record. The 8 cutoff-proximate roles
match the prior wording verbatim. Org-motion is the **only** arm-delta between the baseline and augmented
packets (E6–E9 manifest entries + the org-motion prose block).

## Non-claims

Not validation, not readiness, not a band input, not contestant-visible, not a scoring-key change. JSG-01
remains frozen (ECR derives integrity context; binds no `EvidenceUnit`). Product-learning tier, N=1.
