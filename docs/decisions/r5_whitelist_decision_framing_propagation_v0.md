---
retrieval_header_version: 1
artifact_role: Decision record (direction-change propagation map for R5 decision-framing / whitelist-not-blacklist leak-safety). NOT validation/readiness.
scope: >
  Propagates the R5 leak-safety doctrine (participant packets are decision briefs
  not tests; whitelist-only meta-instruction; no enumerated forbidden/spoiler list
  on any contestant- or blind-constructor-readable surface; spoiler taxonomy
  sealed-only; reasoning-trace IS the probe; active recall dropped; contamination =
  outcome-USE not recognition) across the judgment-spine. Records controlling
  sources, the full downstream surface inventory (Sonnet fan-out 2026-06-12), and
  the routing/disposition of each. Source: conductor addendum v1 (R5/R6) + the
  Beauty Pie packet review.
use_when:
  - Enacting R5 across the construction protocol/template/schema and downstream docs.
  - Checking which surfaces carry the pre-R5 blacklist / active-recall pattern.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md
  - docs/review-outputs/adversarial-artifact-reviews/beautypie_repricing_2023_paired_packets_adversarial_artifact_review_v0.md
stale_if:
  - Conductor addendum v1 is ratified or amended (re-derive from it).
  - The case schema (case_models.py) field is migrated (update the code-routed rows).
---

# R5 Decision-Framing / Whitelist Propagation (v0)

```yaml
direction_change_propagation:
  doctrine_changed: >
    R5 (conductor addendum v1): participant packets are GENUINE DECISION BRIEFS,
    never tests. WHITELIST-only meta-instruction ("decide using only the
    information in this brief"); NO enumerated forbidden/spoiler list on any
    contestant- or blind-constructor-readable surface (an enumerated forbidden
    list is itself a leak); spoiler taxonomy lives ONLY in the sealed
    facilitator-only record. Plus: the blind judgment carries a reasoning trace
    that IS the contamination probe (JSG-08 tell-audit); active recall is DROPPED
    entirely; contamination = outcome-USE, not recognition-capacity.
  trigger: product_doctrine
  related_triggers: [review_authority]
  status: PARTIALLY ENACTED (conductor addendum v1 owner-RATIFIED 2026-06-16). The
    finder-frame operative bar + the judgement case construction protocol are
    enacted, and a default-on identity-masking-with-sealed-crosswalk rule (mask the
    target brand only; keep third-party identities, provenance, and decision numbers
    real; supply brand attributes as in-packet evidence; route out un-maskable
    cases) is layered on R5 at those same surfaces. Remaining downstream surfaces
    (claim-defense doctrine, packing interface, fixture drafts, the _scratch batch-2
    exam instruments, and the case_models.py code field) stay pending. The
    ratification + masking adoption are routed to adversarial artifact review before
    downstream lanes treat them as final.
```

## Controlling sources (change #6 — the root that mandates the blacklist field)

| Source | Locus | Change | Disposition |
| --- | --- | --- | --- |
| `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md` | :72 must-include, :255 frontmatter, :232-236 reject/quarantine | `forbidden_information_notice` -> `information_boundary` (whitelist-only rule); recognition-probe gate -> isolation screen | enact |
| `docs/research/judgment-spine/decide_vs_confirm_backtest_case_frame_template_v0.md` | :91 four-lane spec | field rename + whitelist note | enact |
| `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md` | :47 field, :131 spoiler_inventory comment | field rename + sealed-only note | enact |
| `orca-harness/schemas/case_models.py` | :42-43 field + validator, :134-138 LeakageAudit | **CODE**: rename + whitelist validator; spoiler_inventory sealing | **ROUTED to bounded code turn (spawn_task)** — required now because the Beauty Pie packets already use `information_boundary` |

## Downstream surfaces (Sonnet fan-out 2026-06-12; disposition)

- **Live case packets carrying the blacklist:** Beauty Pie (`information_boundary`, **DONE** — the R5 reference impl); Inoreader + FeedHaven (`forbidden_information_notice` :13 + "what this case tests" :55 + ledger `spoiler_inventory` enumerations — **QUARANTINED dev cases**, de-leak proposed, ledgers are freeze-hashed so packet-only); `tr_casetext` plumbing fixture :12 (must change with the schema or the test suite breaks).
- **Fixture drafts (blacklist + test-framing):** canoo_walmart, daimler (frontmatter + body + conversion plan + extraction plan), unity — all `forbidden_information_notice` enumerations + "blind judgment packet" / "what is withheld" framing. **proposed-pending**.
- **Active-recall surfaces (R3 drop):** `memorization_probe_protocol.md` (whole doc — **supersede**); daimler memorization-probe-request-prep + work-queue; canoo/unity/daimler freeze-blockers ("memorization probe passes" -> "isolation_result proven"); batch-1 ledger :104 + batch-2 routing :44-47 ("recognition check FIRST" -> isolation + tell-audit). **proposed-pending**.
- **Claim defense doctrine** (`docs/product/product_lead/orca_claim_defense_doctrine_v0.md`): :177 "model knew the outcome" receipt (recognition -> outcome-USE/trace); :195 amendment (active recall "post-seal forensic" -> dropped entirely); :187-188 **stale citation to the blocked v0 addendum -> v1**. **proposed-pending (high; my doctrine, stale pointer)**.
- **Finder frame** (`docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md`): :52-57 "swap on recognition" -> swap-on-outcome-USE + active recall dropped (already on the operative bar); anonymization bullet **enacted 2026-06-16** — replaced "optional flavor-anonymization, use sparingly" with **default-on identity-masking with sealed crosswalk** (mask target brand only; keep third-party identities / provenance / decision-numbers real; attributes-as-evidence; route-out; masking is a supplement, tell-audit unchanged); stays whitelist + R6 gate. **enacted**.
- **Packing interface v3**: :135 spoiler_inventory sealed-only reinforcement; :156 contestant-visible boundary whitelist note. **proposed-pending**.
- **Conductor operating model** `stale_if`: add the v1 addendum at ratification. **at-ratification**.

## Disposition legend / non-claims

`enact` = doc edit applied/applying in this propagation. `proposed-pending` = fan-out-proposed, exact edit captured, application is the immediate follow-up pass (or a second editing fan-out). `ROUTED` = harness code, needs bounded authorization. `QUARANTINED`/freeze-hashed = do not rewrite frozen ledgers (breaks `ledger_freeze_hash`); packet-surface fixes only. Frozen/historical probe artifacts get a SUPERSEDED banner, not deletion. Not validation, readiness, or ratification; R5 itself is pending the conductor addendum v1 re-review.
```
