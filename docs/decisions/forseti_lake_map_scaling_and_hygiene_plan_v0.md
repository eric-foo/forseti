# Forseti Lake Map Scaling And Hygiene Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Owner-ratified decision record (staged upgrade plan with triggers)
scope: >
  The staged scaling and hygiene plan for the lake map — the generated Silver
  entity read layer (by_creator / by_mention / undone views, Creator Vault
  account summaries, and the scoped lookup runner) — recording the
  owner-ratified upgrade sequence, the trigger
  that fires each stage, and the deferred identity work, so future work units
  bind to recorded decisions instead of re-deriving them.
use_when:
  - Deciding whether a lake-map performance or retrievability complaint fires a recorded trigger.
  - Scoping the incremental classification cache, view sharding, SQL query lens, retention, or identity follow-ups.
  - Checking why the lake map is flat JSON rather than SQL today.
stale_if:
  - A later accepted decision supersedes a stage, trigger, or deferral recorded here.
  - The consumption seam contract changes the built-view set or authority boundary.
authority_boundary: retrieval_only
```

## Naming

**"Lake map"** is the canonical informal name for the generated Silver entity
read layer. Formal artifacts keep their existing names; this record binds the
alias so conversation, commissions, and future records can say "lake map" and
mean exactly: the gate-opened core views and Creator Vault account summaries
built by `forseti-harness/data_lake/derived_retrieval_views.py` under
`indexes/derived_retrieval/silver_vault/`, plus the scoped read entry point
`forseti-harness/runners/run_derived_retrieval_lookup.py`, governed by
`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`.
Like the repo map, the lake map is derived, regenerable, and never authority;
by-key discovery over `derived/` stays the retrieval authority.

## Ratified Current State (2026-07-17)

All three views are built on the live lake, byte-rebuildability is proven, and
the cross-vendor delegated review of the layer was adjudicated and landed
(PR #1031; adjudication record
`docs/review-outputs/silver_entity_read_layer_delegated_code_review_adjudication_v0.md`).
by_creator is schema v2: card key `(platform namespace, asserted identity
kind, native id)`; closed platform-namespace vocabulary; unfileable
account-describing shapes are named residuals; native product-page identity
sources are a closed in-code registry (Fragrantica sole entry). Measured at
~8.5k Silver records: full rebuild ~5 minutes, prove-rebuildability ~10
minutes, lookups sub-second. On 2026-07-19, production diagnosis established
that the cache avoids classification work but still parses and fingerprints
the whole Silver corpus. Cadence freshness is therefore narrowed to Creator
Vault through a full-history scan of only `creator_metric_silver`; generic core
views remain explicit owner-rebuildable caches.

## Staged Upgrades

Stage 1 is the explicit exception to the original trigger-only sequence: on
2026-07-17 the owner pulled it forward before its wall-clock trigger fired.
Stages 2–4 remain trigger-gated.

### Stage 1 — Incremental classification cache

- **Original trigger (did not fire):** rebuild wall-clock exceeds operational
  tolerance (analysis: the whole-lake sweep breaks at roughly 100k–250k
  records, ~10–25x current).
- **Owner pull-forward (2026-07-17), narrowed 2026-07-19:** the cache remains
  useful for explicit full-map rebuilds, but it does not make a whole-lake
  cadence scan cheap: cache-key formation still parses records and fingerprints
  referenced bytes. The recurring freshness requirement is current Creator
  Vault profile metrics, not every generic reverse-lookup view. Cadence now
  scans only the full `creator_metric_silver` history; this is an owner scope
  correction, not a claim that a later-stage trigger fired.
- **Ratified design essentials:** cache authority verdicts keyed by
  `(content_hash, classifier_version, referenced-bytes fingerprint)`;
  records are immutable so an unchanged key keeps its verdict verbatim. The
  creator-metric family is the sole non-record-local case: its key also
  carries a lineage/epoch/archive-state fingerprint, and a change to that
  state rescans only the two creator-metric lanes. Full rescan triggers:
  classifier/registry code change; Bronze catalog rebuild (attachment-backed
  refs only). Classification consumes no wall-clock time, so caching is sound.
- **Fix in the same stage** (they dominate cold builds regardless of cache):
  the O(n²) list-membership dedups in the view builders, repeated
  whole-packet re-hashing per referencing record, the whole-catalog scan per
  attachment ref, and the double source-verification of the mentions lane.
- Periodic byte-integrity audit (re-hash everything) becomes a scheduled
  check decoupled from rebuilds.
- **Promoted implementation shape:** a passing
  `runners/run_seam_cadence.py --run` completes one committed starting
  packet-id snapshot, then invokes the contract-pinned rebuild runner with
  `--target creator_vault`. That target scans only the full
  `creator_metric_silver` observation-lane history, publishes per-account
  envelopes plus unfileable-account residuals, and leaves the generic core
  views unchanged. Packets committed later are next-run cadence work; the
  subsequent Creator Vault rebuild is intentionally live. Failed cadence
  performs no rebuild and a rebuild failure fails the cadence. The disposable
  classification cache remains under
  `indexes/derived_retrieval/silver_vault/core/cache/` for explicit full-map
  rebuilds. `--prove-incremental-equality` and `--audit-source-integrity`
  remain owner-operated full-map verification modes. No scheduler, queue,
  cursor, or per-cadence Git mutation is introduced.

### Stage 2 — Per-creator view sharding

- **Trigger:** by_creator file size makes lookup loads slow (analysis:
  whole-file parse degrades materially around ~50–100 MB, ~0.5–1M records).
- Shard per creator (~one small file per card), never per anchor (millions of
  files is an NTFS liability). Per-shard canonical JSON keeps the existing
  byte-compare prove-rebuildability unchanged.

### Stage 3 — SQL query lens, as a disposable projection only

- **Trigger:** an ad-hoc cross-entity or cross-time question the flat views
  cannot answer efficiently (the consumption seam contract's staged
  query-lens trigger). Entity point-lookups do NOT fire it — they are
  sub-second on the views.
- **Ratified shape:** SQLite/DuckDB built FROM the byte-proven JSON views and
  regenerated, never migrated; never a proof target, never authority.
  prove-rebuildability keeps byte-comparing the JSON (DB file bytes are not
  reproducible; a DB-only artifact would need a sorted-row content-hash
  comparison, a doctrine amendment deliberately not taken while the JSON
  remains canonical).
- **Semantic invariants any schema must carry:** per-row authority status +
  reason from the shared classifier; absence-never-zero structurally (posture
  and coverage columns; no `NOT NULL DEFAULT 0` counts; no `COALESCE(x,0)`);
  generation provenance columns; per-platform discriminated identity keys
  (namespace, identity kind, native id); exact observed strings with any
  normalization as a separate labeled column.

### Stage 4 — Governed retention

- **Trigger:** storage or handling overhead of tombstoned/duplicate material
  actually bites (it does not today).
- Physical byte removal only for material already under a tombstone receipt,
  keeping the receipt — deletion must stay loud and evidenced. Records that
  were believed and later found wrong are never physically deleted; they stay
  marked, because the fact they were believed is itself evidence. Exact
  byte-identical duplicates are prevented at the write front door instead
  (bounded lane in flight: `claude/lake-dup-rejection`).

## Deferred Identity Work (recorded, not built)

- **Within-platform alias joins:** a handle-keyed card may join an
  account-id-keyed card only on record-asserted evidence (one record naming
  both), time-scoped because handles recycle; displayed as a labeled join,
  never a silent merge. Trigger: handle-only cards accumulate enough to hurt.
- **Linked-cards overlay:** by_creator grows a cross-platform
  "linked cards" cross-reference DISPLAYING declared/probable links from the
  creator public-handle linkage ledger (first declared link landed via
  PR #1048). Cards stay per-platform truth; the link is a labeled overlay.
  Trigger: a consumer needs the cross-platform view.
- **Retail PDP as a product-identity source:** `retail_pdp_silver`
  `retailer_product` rows are a real second entry for the
  `NATIVE_PRODUCT_PAGE_SOURCES` registry (currently declared a known
  non-account subject kind only). Trigger: retail product pages need to be
  findable by product identity in the lake map.
- **Reddit/Quora onboarding:** when those lanes land, extend
  `KNOWN_PLATFORM_NAMESPACES` deliberately (exact lowercase canonical,
  matching the Reddit venue registry posture) and give authors the
  platform-account subject shape; until then any such records surface in the
  unfiled-tray residuals rather than vanishing.

## Accepted Residuals

- The lake map answers known reverse lookups; free-text and fuzzy search stay
  out of scope (exact normalized identity matching is deliberate).
- `by_mention`'s mentions section stays empty until the transcript
  product-mention producers run over real transcript inputs (0 records
  lake-wide as of this record; the ideal-audience judgment consumes
  comment-attention evidence, not product mentions).
- Creator Vault freshness is guaranteed only after a passing seam-cadence run
  (or an owner-operated scoped rebuild), not continuously between runs.
  Generic `by_creator`, `by_mention`, and `undone` freshness is guaranteed only
  after an explicit full-map rebuild. Cadence completion covers its exact
  starting packet set; the subsequent Creator Vault package may be a live
  superset if capture or derivation continued. Manifest provenance discloses
  generation time and a source-ref-set fingerprint; hash verification proves
  integrity rather than currency.

### Historical propagation evidence (2026-07-17)

The receipt below records the original Stage 1 promotion. Its whole-map cadence
scope is superseded by the 2026-07-19 owner correction above; it remains
historical provenance, not the current operating rule. Current propagation
evidence is the owning-source diff plus the PR/closeout, so no new receipt is
created.

```yaml
direction_change_propagation:
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  doctrine_changed: >
    The owner pulled Stage 1 forward before its original wall-clock trigger
    fired: every passing monitoring cadence now refreshes the lake map through
    the sanctioned rebuild runner, classification becomes incrementally cached
    disposable state, and byte-equality plus cold integrity modes preserve the
    existing proof and output model. Stages 2-4 remain trigger-gated.
  controlling_sources_updated:
    - docs/decisions/forseti_lake_map_scaling_and_hygiene_plan_v0.md
    - forseti-harness/data_lake/derived_retrieval_cache.py
    - forseti-harness/data_lake/derived_retrieval_views.py
    - forseti-harness/data_lake/catalog.py
    - forseti-harness/data_lake/product_mention_selection.py
    - forseti-harness/data_lake/silver_record.py
    - forseti-harness/runners/run_data_lake_indexes_rebuild.py
    - forseti-harness/runners/run_seam_cadence.py
    - forseti-harness/tests/test_data_lake_indexes_rebuild.py
    - forseti-harness/tests/unit/test_seam_cadence.py
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - docs/decisions/forseti_data_lake_derived_retrieval_activation_proposal_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
      reason: >
        Its view set, sanctioned writer, generated-read-model authority
        boundary, policy-pin obligation, and exact-byte proof remain unchanged;
        Stage 1 changes rebuild computation and cadence freshness only.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        All of indexes remains disposable and rebuildable from committed
        material; the cache and new proof/audit modes instantiate that existing
        boundary without changing it.
    - path: docs/decisions/forseti_data_lake_derived_retrieval_activation_proposal_v0.md
      reason: >
        The activation proposal's gate-opened view set and non-authoritative
        posture are unchanged; this later ratified scaling record owns Stage 1.
  stale_language_search: >
    rg -n "each fires on its trigger|No stage is built|freshness between
    rebuilds|incremental classification cache|prove-incremental-equality"
    docs/decisions/forseti_lake_map_scaling_and_hygiene_plan_v0.md
    forseti/product/spines/data_lake/authority
  non_claims:
    - not validation or readiness
    - not a change to view authority or the proof model
    - not a claim that Stage 2, Stage 3, or Stage 4 fired
    - not a claim that monitoring provides continuous freshness between runs
```
