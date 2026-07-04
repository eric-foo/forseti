# Creator Ledger Operational Evolution Contract v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_architecture_contract
scope: >
  Operational evolution contract for the Creator Ledger: how the registry,
  public-handle linkage ledger, metric records, and current profile view evolve
  additively so future capability upgrades do not require repeated data
  remigration.
use_when:
  - Scoping Creator Registry or Creator Ledger changes that add identity, metric, audience, or product-surface capability.
  - Checking whether a proposed creator-ledger upgrade should add a layer, field, view, or resolver instead of rewriting existing records.
  - Applying a God Tier or Mini God Tier capability lens to the Creator Ledger without mistaking audit completeness for efficacy.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
stale_if:
  - The Creator Registry folder no longer owns the social creator-ledger artifacts.
  - A successor creator identity, metric, or profile-current architecture supersedes the sibling-record split.
  - God Tier or Mini God Tier doctrine changes the efficacy/non-claim boundary.
```

## Purpose

This contract makes the Creator Ledger operational target explicit: the ledger
should become useful memory for creator discovery, capture, and Creator Signal
without forcing repeated data remigration each time the capability bar rises.

The durable shape is additive evolution over stable sibling records:

- exact known-account lookup and scan/capture preflight in the Creator Registry;
- public account and public-handle linkage evidence in the linkage ledger;
- raw captures, metric observations, and metric rollups in their owning Capture
  or Silver records;
- `creator_profile_current` as a generated read model over those siblings; and
- Creator Signal as the product-facing interpretation layer over the read model.

The ledger is operational when those layers help the operator avoid duplicate
work, route known accounts correctly, carry source-backed candidate handoffs,
and expose decision-useful creator profiles while preserving visible
missingness and source limits. A more complete audit trail is useful only when
it improves those outcomes or prevents material overclaiming.

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_creator_ledger_operational_evolution
  edit_permission: docs-write
  target_scope:
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
    - docs/workflows/forseti_repo_map_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/workflows/creator_registry_operational_next_steps_handoff_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
    - docs/decisions/orca_mini_god_tier_doctrine_v0.md
```

## Operational Invariant

Future Creator Ledger changes should preserve existing records and add the
minimum new layer needed for the new capability:

```text
raw/source evidence -> normalized identity/metric/audience records
-> derived rollups or linkage review state -> current read model
-> product-facing Creator Signal surface
```

Do not move facts upward just because a downstream surface wants to show them.
Raw source material stays in Capture or lake-owned source records. Metric
observations and rollups stay in metric records. Public-handle linkage evidence
stays in the linkage ledger. `creator_profile_current` joins and points back; it
does not become the source of truth.

## Migration-Stability Rules

Stable identifiers are compatibility boundaries:

- keep `platform_account_id` stable for a public account once admitted;
- keep `creator_record_id` stable for a promoted public account cluster;
- keep metric observation and rollup ids stable for source-backed records;
- keep evidence ids stable for public-handle linkage evidence; and
- keep source pointers stable enough for drill-back or explicitly version them
  when a storage home changes.

Schema changes should prefer additive fields, sibling records, or derived views
over rewriting historical rows. A rewrite is allowed only when the old record is
wrong, forbidden, or unable to preserve the new source truth with a versioned
adapter.

Physicalization is an implementation detail, not the data contract. Static JSON,
SQLite, Data Lake records, or dashboard queries should map to the sibling-record
contract rather than changing what identity, metric, audience, or profile facts
mean. A later storage engine may replace the physical home without changing
ledger semantics if it preserves stable ids, lineage, posture/value coupling,
limitations, and non-claims.

## Upgrade Pattern

Use this default sequence for new capability:

1. Identify the layer that owns the new fact or decision.
2. Add the smallest stable field, sibling record, resolver output, or read-model
   projection that preserves the owning layer.
3. Keep missingness explicit: unavailable, not attempted, out of window, gated,
   or not applicable is not an observed zero.
4. Preserve source drill-back and recipe/version fields when a derived value is
   emitted.
5. Update product-facing interpretation only after the source layer can support
   the claim.

Examples:

- A fuzzy duplicate helper should emit review candidates or resolver evidence;
  it must not overwrite exact-match preflight rows or silently merge accounts.
- Cross-platform creator rollups should require promoted public-handle linkage
  and recompute from compatible source observations or accepted rollup records;
  they must not sum account-level read-model values as raw truth.
- Cadence or velocity should populate the already-declared fields only after
  Silver-side history can emit recipe-backed values with lineage.
- A dashboard should consume `creator_profile_current` and source drill-back; it
  should not mutate identity, metric, or linkage records.

## Additive Upgrade Intake

Before a future Creator Ledger capability change is treated as ready to build,
route, or hand off, record a compact additive-upgrade intake in the changed
artifact, checkpoint, PR body, or handoff. The intake is lightweight, but it must
force the migration-stability question before data shape changes start.

A sufficient intake answers:

- efficacy target: which primary efficacy test the change improves;
- owning layer: registry index, linkage ledger, metric observation/rollup,
  current read model, or Creator Signal surface;
- additive record path: the field, sibling record, resolver output, generated
  view, or presentation rule to add;
- stable-id posture: which existing ids remain untouched and which new ids, if
  any, are introduced;
- source and lineage posture: where source truth stays and how drill-back or
  recipe/version fields remain visible;
- missingness posture: which unavailable, gated, out-of-window, or not-attempted
  values remain explicit;
- proof checkpoint: the smallest later checkpoint that would show efficacy
  without claiming validation or readiness; and
- forbidden move check: whether the proposed route rewrites historical rows,
  promotes `creator_profile_current` into source truth, or collapses sibling
  records into a convenience blob.

If the forbidden move check is not clean, do not proceed by normalizing the risk
away. Either choose an additive sibling/resolver/view route, or write the
exception explicitly with the old record that is wrong, forbidden, or unable to
preserve source truth through a versioned adapter.

## Efficacy-First God Tier Lens

For the Creator Ledger, "God Tier" should mean operational efficacy before audit
completeness. The ledger improves when it lets Orca make better creator-memory
decisions with less duplicate work and less overclaiming.

Primary efficacy tests:

- duplicate-work prevention: known exact accounts block duplicate new-capture
  requests, and repeated observations attach to the right existing account;
- candidate recall: scan lanes can surface plausible new creator accounts without
  losing known-account orientation;
- handoff usefulness: candidate and capture-request rows carry the preflight
  receipt fields needed by the next lane;
- identity decision support: soft links, rejected links, and promoted links make
  account-cluster review easier without claiming real-world identity; and
- product usefulness: Creator Signal can show source-backed influence,
  freshness, missingness, and limitations in a way an operator can act on.

Audit completeness is a support function. Add stricter receipts, hashes,
review records, and checker coverage when they protect these efficacy outcomes
or prevent unsafe claims. Do not treat more audit surface by itself as God Tier
progress.

### Operational Proof Loop

Every future Creator Ledger capability upgrade should leave one small efficacy
checkpoint before it is treated as operational. The checkpoint is not a broad
audit packet; it is the minimum evidence that the new capability made the ledger
work better without remigrating existing data.

A conforming checkpoint names:

- owning layer: registry index, linkage ledger, metric observation/rollup,
  current read model, or Creator Signal surface;
- additive path: the new field, sibling record, resolver output, generated view,
  or presentation rule added without rewriting historical source truth;
- migration-stability evidence: stable ids, source pointers, posture/value
  coupling, and limitations remain intact for existing records;
- efficacy outcome: at least one primary efficacy test above improves or becomes
  easier to verify; and
- accepted residuals: the specific fuzzy identity, source freshness, metric
  breadth, storage physicalization, or product-surface limits still left out.

Audit checks, validators, review reports, hashes, and receipt verification may
support the checkpoint, but they do not replace the efficacy outcome. A change
with perfect audit shape and no better duplicate prevention, handoff usefulness,
identity decision support, or product usefulness is not God Tier progress for
this ledger.

## Mini God Tier Fit For This Ledger

When the owner invokes Mini God Tier for the Creator Ledger, the target is a
high-coverage, low-lock-in operating shape: most practical value from exact
preflight, stable ids, source drill-back, explicit missingness, and generated
current views before full runtime infrastructure or migration tooling.

Accepted residuals for a Mini God Tier ledger slice:

- exact-match preflight is not fuzzy display-name duplicate detection;
- public-handle linkage is not a person identity graph;
- no standing crawler or live social search is implied;
- no automatic registry mutation is allowed from scan rows alone;
- no automatic quality, commercial-fit, or buyer-proof score is implied;
- cross-platform rollups wait for promoted linkage and compatible observations;
- metric freshness remains visible and may be stale; and
- storage physicalization, replay tooling, and broad migration automation remain
  upgrade triggers, not prerequisites for the bounded operating shape.

## Current Operating State

Current sources support this state:

- the Creator Registry folder already separates known-account lookup, public
  handle linkage, current profile view, profile record contract, and metric
  Silver contract;
- the match preflight is exact-match only and emits row-level clearance fields
  for scan/capture handoff;
- the first public YouTube fragrance scan produced ten `new_capture` candidate
  rows and a preserved receipt, but did not execute capture or mutate the
  registry;
- the receipt-content checker now verifies cited Creator Registry preflight
  receipt content for detected scan artifacts; and
- `creator_profile_current` is still a generated/static read model, not a
  database, dashboard, or source of truth.

## Non-Claims

- not validation
- not readiness
- not buyer proof
- not capture authorization
- not registry mutation
- not Silver write authorization
- not fuzzy duplicate detection
- not cross-platform identity proof
- not dashboard implementation
- not storage-engine adoption
- not a claim that the current ledger has achieved God Tier

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Creator Ledger evolution is now bound to a migration-stable additive model:
    preserve stable sibling records and generated views, add future capability
    by fields/layers/resolvers instead of remigrating data, require a compact
    additive-upgrade intake before future capability changes, and judge God Tier
    progress primarily by operational efficacy rather than audit completeness.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - workflow_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
    - docs/workflows/forseti_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
    - docs/decisions/orca_mini_god_tier_doctrine_v0.md
    - docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The kernel already binds Mini God Tier and project source-loading rules;
        this patch adds a source-family contract, not a root behavior rule.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading mechanics are unchanged; the new contract is reached
        through the Creator Registry README and repo map.
    - path: docs/decisions/orca_mini_god_tier_doctrine_v0.md
      reason: >
        The global Mini God Tier doctrine remains correct. This contract applies
        its accepted-residuals and non-claim boundaries to the Creator Ledger.
    - path: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
      reason: >
        The scan is a historical first-run artifact. Its now-stale checker
        residual is superseded by the current usage note and checker reviews,
        but changing the scan record is not required to bind ledger evolution.
  stale_language_search: >
    rg -n "creator ledger|Creator Ledger|God Tier|Mini God Tier|mini god tier|remigration|remigrate|migration-stable|additive-upgrade|upgrade intake|audit completeness|efficacy"
    AGENTS.md
    .agents/workflow-overlay
    docs/workflows/forseti_repo_map_v0.md
    docs/decisions/orca_mini_god_tier_doctrine_v0.md
    forseti/product/spines/capture/core/source_families/social_media/creator_registry
    forseti/product/spines/creator_signal
  non_claims:
    - not validation
    - not readiness
    - not capture authorization
    - not registry mutation
    - not storage-engine adoption
    - not proof that the current ledger has achieved God Tier
```

Older receipts for this source-family contract live in
`docs/decisions/dcp_receipts_archive_v0.md` when cycled out by a future edit.
