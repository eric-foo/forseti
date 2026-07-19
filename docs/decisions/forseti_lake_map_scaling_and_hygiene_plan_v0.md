# Forseti Lake Map Scaling And Hygiene Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Owner-ratified decision record (staged upgrade plan with triggers)
scope: >
  The staged scaling and hygiene plan for the lake map — the generated Silver
  entity read layer (by_creator / by_mention / undone views plus the scoped
  lookup runner) — recording the owner-ratified upgrade sequence, the trigger
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
mean exactly: the gate-opened views built by
`forseti-harness/data_lake/derived_retrieval_views.py` under
`indexes/derived_retrieval/silver_vault/core/`, plus the scoped read entry
point `forseti-harness/runners/run_derived_retrieval_lookup.py`, governed by
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
minutes, lookups sub-second.

### Operational freshness verification (2026-07-19, SLG-03)

The live lake was reconciled through the sanctioned runners after stable-storage
confirmation. The pre-state was 644 Bronze catalog packets versus 781
availability entries. Rebuilding Bronze found 778 committed public packets; the
three remaining availability entries were valid raw containers excluded by
validated raw-packet tombstones. The sanctioned availability rebuild removed
those stale generated entries, yielding 778/778 with no manual deletion.

A legitimate `retail_pdp / cloakbrowser_snapshot` packet then arrived while the
first read-only Silver rebuildability proof was running. That proof reported
`by_creator` and `by_mention` rebuildable and `undone` drifted; the arrival
explains the exact split because `undone` includes every available anchor. A
final Bronze then Silver convergence included the arrival and closed at:

- Bronze strict inspect: `status=ok`, expected/indexed packets `779/779`, 2,485
  indexed Attachment Records, and zero missing, orphaned, stale, or read-failure
  entries;
- availability entries: 779;
- Silver generation `88a2516067a54077ac4660eb664b7a90`, generated at
  `2026-07-19T23:25:49.069077+08:00`, with all three manifest `view_sha256`
  values matching their query-table bytes;
- `by_creator`: 22,383 source refs, high-watermark
  `c43d24a408ce9fa7eb573973d6e005c128dc533119a95ee1eb47df9cb8c847fe`;
- `by_mention`: 12 source refs, high-watermark
  `ab506805dce7c135bc28f48939dd2e8915b49df24ec6d174807561a5d5f44b4b`;
- `undone`: 2,787 source refs; targeted regeneration under the stored final
  generation stamp matched both the query table and manifest byte-for-byte.

The first two views retained the exact source high-watermarks and view hashes
that passed the full proof before the raw-only late arrival; the targeted final
proof therefore re-ran only the affected `undone` view. This is a point-in-time
freshness receipt, not continuous freshness or hardware-health proof. The
measured silent whole-lake runtime remains owned by SLG-04.

### Whole-lake assurance verification (2026-07-20, SLG-04)

The existing doctor and Silver census now stream structured, flushed phase
progress to stderr while retaining their single machine-readable JSON result on
stdout. The doctor reports discovery, availability, validated tombstone
resolution, and verified-read progress every 100 packets. The census reports raw
manifest and creator-lineage phases, every registered Silver lane, 1,000-record
lane milestones, deep-capture markers, and final reconciliation. No scan,
source-authority check, or error was removed to make these commands look fast.

Live dogfood established the actual runtime shape:

- doctor closeout: 6.218 seconds; 784 retained raw packets all verified, 3
  validated tombstones, 781 public packets, 781 availability entries, and zero
  missing, orphaned, stale, or read-failure entries;
- full Silver census: 898.361 seconds for 22,515 Silver records; 22,064 current
  source-backed, 319 historical-compatible, zero unclassified, and zero errors;
- `cleaning_fragrantica_silver` is the measured bottleneck: 17,695 records in
  868.06 seconds. The next slowest lane was
  `tiktok_comment_attention_silver`: 3,087 records in 16.503 seconds;
- cadence `--check` emitted its snapshot in 0.478 seconds, then visibly named
  `run_ecr_catchup.py` as the active pending-check entrypoint for 107.1 seconds
  before the bounded read-only dogfood process was stopped. The production
  scheduled task remained `Ready`.

The doctor also corrected one dogfood-discovered false positive: validated
raw-packet tombstones retain raw bytes but intentionally remove public
availability. The doctor now verifies those retained bytes, excludes their IDs
from the public availability expectation, and reports them explicitly. Two new
packets arrived during the long census, explaining its 782-capture snapshot
versus the final 784-retained/781-public doctor snapshot. These are operational
progress and point-in-time integrity receipts, not a claim that the population
census is fast or that the lake is continuously quiescent.

## Staged Upgrades

Stage 1 is the explicit exception to the original trigger-only sequence: on
2026-07-17 the owner pulled it forward before its wall-clock trigger fired.
Stages 2–4 remain trigger-gated.

### Stage 1 — Incremental classification cache

- **Original trigger (did not fire):** rebuild wall-clock exceeds operational
  tolerance (analysis: the whole-lake sweep breaks at roughly 100k–250k
  records, ~10–25x current).
- **Owner pull-forward (2026-07-17):** near-zero lake-map staleness after every
  passing monitoring round is wanted at every scale, and the incremental/full
  byte-equality proof is cheap while a cold comparison still costs minutes
  rather than hours. This declaration promotes Stage 1 now; it does not
  fabricate a fired wall-clock trigger.
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
  packet-id snapshot, then invokes the contract-pinned
  `run_data_lake_indexes_rebuild.py` path at cadence tail. Packets committed
  later are next-run cadence work; the subsequent map rebuild is intentionally
  live and may include their newer derived material. Failed cadence performs
  no rebuild and a rebuild failure fails the cadence. The disposable cache lives under
  `indexes/derived_retrieval/silver_vault/core/cache/`; deleting it produces a
  cold rebuild. `--prove-incremental-equality` byte-compares incremental and
  full-cold generated files, while `--audit-source-integrity` performs the
  owner-scheduled cold source re-hash independently of rebuilds. View and
  manifest schemas and canonical output bytes are unchanged.

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
- Freshness is guaranteed only after a passing seam-cadence run (or an
  owner-operated fallback rebuild), not continuously between runs. Cadence
  completion covers its exact starting packet set; the map built afterward is
  a current non-authoritative rebuild and may be a superset if capture or
  derivation continued. Manifest provenance discloses the generation, while
  hash verification proves integrity rather than currency.
- Automation boundary: a successful `run_seam_cadence.py --run` rebuilds the
  map automatically; `--check` does not rebuild, and no background scheduler
  is selected. A fresh root uses one explicit
  `--bootstrap-active-product-mention-policy` cadence run, which pins the
  checkout's exact active policy and refuses an existing manifest. Later runs
  reuse those stored pins.

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
