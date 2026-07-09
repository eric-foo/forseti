# Data Lake Actor-Retrieval Governance Recommendation v0

```yaml
retrieval_header_version: 1
artifact_role: Owner-adopted actor-retrieval governance decision (authored as a recommendation; adopted 2026-06-21)
scope: >
  Recommended access, audit, retention, and identifier-scope guardrails for on-demand
  actor/commenter/reviewer timing retrieval in the Data Lake indexes/derived_retrieval
  lane, keeping it non-dossier per the medallion gold-readiness contract.
  Recommendation only; the owner (with legal/privacy review) adjudicates; the
  derived_retrieval lane stays blocked until adoption.
use_when:
  - Owner adjudication of actor-retrieval guardrails before any derived_retrieval build.
  - Checking whether a proposed retrieval surface stays non-dossier.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
stale_if:
  - The owner adopts, amends, or rejects this recommendation.
  - The medallion gold-readiness contract changes the actor-timing-retrieval boundary.
authority_boundary: retrieval_only
```

## Status

`OWNER_ADOPTED_V0`. Resolves Physicality Location Contract blocker 6 (actor-related
access/audit/retention + identifier scopes). Owner-adopted 2026-06-21.

Owner-recorded posture at adoption:

- **Lawful-basis position (owner's call, owner-recorded, not externally validated):**
  the owner reviewed PDPA and judged that logging public-platform comment/review timing
  plus the observed public username — explicitly NOT building a person dossier — does
  not require additional clearance. This is the owner's recorded position, not a legal
  validation by this artifact.
- **Takedown commitment:** on a request with reasonable-effort proof of ownership, the
  data is removed promptly. Verification is reasonable-effort, not a high bar.
- **Knobs set:** result-cache TTL = 7 days; access = internal decision-workflows only.
- **Adopted guardrail set:** the full guardrail set below (MGT), not the SCI floor.

Still NOT legal advice and NOT validation/readiness. The non-dossier guardrails below
are what keep the owner's public-data/non-dossier basis true; they are binding on any
build. The `indexes/derived_retrieval` lane is governance-unblocked but remains
build-deferred (TTL automation, query-layer enforcement, and audit tooling are built
when the lane is built). Produced by an external blocker-resolution lane and
adjudicated as faithful to the medallion contract's Actor Timing Retrieval boundary.

## Recommended Guardrails (for owner adjudication)

- **Access:** internal decision workflows only; every invocation carries a bound,
  registered decision question (from an owner-approved enumeration); no freeform "show
  everything"; one exact identifier per call; no public/anonymous path.
- **Audit:** write-before-return (a failed audit write blocks the retrieval); log
  caller, decision question, identifier scope, time window, profile/version, result
  row count, cache-hit, timestamp, and an elevated-volume flag; append-only,
  immutable, retained beyond result caches.
- **Retention:** result caches expire at a short owner-set TTL (recommended <= 30
  days, 7 preferred), measured from derivation (not last access); on-demand deletion
  required; no migration/export into any durable actor store; audit logs outlive
  caches. Underlying raw stays intact and rebuildable — reconstruction on demand is
  not "retention" of an actor history.
- **Identifier scope:** exact public identifier + single source-family namespace +
  bounded observation window only; no cross-namespace/cross-platform join; explicit
  rejections — cross-platform identity merge, canonical/legal person identity, device
  fingerprint, retrieval anchored on a risk score or prior label. New namespaces
  require an explicit owner decision.
- **Dossier hard stops (no override):** (1) no bound decision question -> fail; (2)
  scope beyond single-namespace exact-identifier -> fail; (3) no write path from
  results to a profile store, actor database, or adverse-action/outreach surface; (4)
  no unbounded-TTL cache; (5) no build on the derived_retrieval path before owner
  adoption.
- **Forbidden outputs (per medallion):** persistent all-history actor profile; "show
  everything this person did"; cross-platform identity merge; actor risk score;
  bot/fake/paid/coordinated label; credibility/exclusion recommendation;
  adverse-action/outreach surface.

## Owner Decisions (status at adoption 2026-06-21)

1. Legal/privacy posture — **DECIDED** (owner-recorded PDPA position: public data,
   comment/review timing + username, non-dossier; see Status). Not externally validated.
2. Permitted decision-question enumeration — **RESIDUAL** (defined when the lane is built).
3. Result-cache TTL — **DECIDED** (7 days); audit-log retention — **RESIDUAL**
   (default ~1 year, set at build).
4. Elevated-volume threshold for flagging — **RESIDUAL** (set at build).
5. MGT vs SCI floor — **DECIDED** (full MGT guardrail set adopted).
6. Formal adoption of guardrail wording — **DECIDED** (this adoption).

The remaining residuals (2, audit-log retention, 4) are build-time settings, not
adoption blockers; they do not re-block the lane.

## Accepted Residuals (recommendation-level, MGT)

- Automated TTL deletion not yet built (no caches exist until the lane is built;
  trigger: lane build makes automated TTL mandatory).
- Anomaly detection procedural, not automated (trigger: volume exceeds owner threshold).
- Cross-namespace enforcement procedural until a query layer exists (trigger:
  query-layer design makes it a structural pre-execution check).
- New-namespace onboarding process not yet formalized (trigger: before a second namespace).

## Non-Claims

Records the owner's adopted governance posture and binding guardrails. Not legal
advice, not validation/readiness, not implementation authorization. Does not externally
validate PDPA/GDPR compliance — the lawful-basis position is the owner's recorded call.
Does not authorize a build; the `derived_retrieval` lane is governance-unblocked but
build-deferred. Governs only actor timing retrieval in the `derived_retrieval` lane;
not the full statement of Orca data governance.
