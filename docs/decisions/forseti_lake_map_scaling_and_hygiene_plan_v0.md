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

### Staging residual adjudication (2026-07-20, SLG-05)

The sole live staging residual
`.staging/01KXSP6FN5PD37NDB15VDXH5B9` was a complete anonymous
CloakBrowser capture of the Ulta ILIA Super Serum Skin Tint PDP, not disposable
scratch: rendered DOM, visible text, viewport screenshot, and metadata captured
at `2026-07-18T04:01:51Z`. No committed manifest contained its URL or any of its
four artifact hashes.

The four files were admitted through the sanctioned already-local packet runner
as `retail_pdp / cloakbrowser_snapshot` packet
`01KXXJXMRN7RCGJHCJ2ZNB2BMS`. The recovery packet preserves the original capture
time separately from its receipt-generation time and explicitly records that
the original invocation was unavailable, market pin was unconfirmed, heavy
assets were blocked despite the named profile expectation, and the configured
scroll-stop condition was not reached. Every source hash matched both the
committed manifest and the independently hashed committed body; the owning root
API loaded all four bodies and public availability was present.

A post-admission mechanical projection from committed raw produced Ulta/ILIA,
`$48.00 USD`, in-stock status, aggregate rating `4.4` over `6,587` reviews, and
five embedded review bodies. Only after those checks passed was the exact
staging directory removed. Post-delete load and projection succeeded again,
`.staging` was empty, and the final doctor closed `status=ok` in 5.55 seconds:
785 retained raw packets all verified, 3 tombstoned, 782 public, 782
availability, and zero missing, orphaned, stale, or read failures. This admits
useful observed PDP evidence; it does not upgrade the packet to confirmed Ulta
US/USD storefront evidence.

### Scheduled cadence dogfood closeout (2026-07-20)

The first full scheduled dogfood used the deliberately pinned runtime at
`ff2891a` and started from 784 public packets. Its two cycles took 2,792.929
and 2,776.070 seconds, the final pending sweep took 3,120.327 seconds, and five
late arrivals were reported. After 8,690.892 seconds it exited 1 and correctly
did not rebuild the lake map. The final sweep had observed one transient
availability-index gap for packet `01KXRFG9J60WWK6QT1QFZTXFZV`; a targeted
follow-up proved that packet remained committed, public, and not tombstoned.

PR #1172 moved cadence to one timed scoped reconcile. PR #1175 made scoped
pickup validate the whole scope and apply source-family filtering from the same
immutable public-availability snapshot, failing loudly when a scoped packet is
missing. On the first optimized scheduled attempt, reconcile still took 287.86
seconds, but the two cycles fell to 34.692 and 29.17 seconds and the final sweep
to 26.161 seconds, with zero cadence failures. An external `0xC000013A`
termination then interrupted the cold map rebuild. A direct sanctioned rebuild
subsequently published every view and cache at
`2026-07-20 03:39:41+08:00`.

The doctor then exposed three availability orphans belonging to validated
raw-packet tombstones. The sanctioned `--rebuild-availability` completed in
4.041 seconds; doctor closed `status=ok` in 22.146 seconds at 792 retained raw
packets, 789 public packets, 789 availability entries, and three tombstones. A
fully successful pre-final scheduled run over 789 packets then completed:
reconcile 390.074 seconds; cycles 25.015 and 23.128 seconds; final sweep 25.164
seconds; map rebuild 53.322 seconds; total 517.899 seconds; exit 0.

PR #1182 removed the remaining per-packet public-read/tombstone rescans:
selected availability writes stay isolated per packet and all successful writes
are validated by one public snapshot. Its delegated validation passed 28
focused and 195 broader tests, the receiver's affected tests also passed, and a
live 789-packet reconcile benchmark closed with zero failures in 10.626 seconds.

Final scheduled dogfood ran the merged, manually deployed runtime at exact
revision `d2728eb14ce63987c93352134a2f08ce1f404835`. From 790 starting packets it
derived one new ECR record, then completed reconcile in 13.550 seconds, cycle 1
in 26.916 seconds, cycle 2 in 27.798 seconds, the final sweep in 27.125 seconds,
the late-arrival check in 0.712 seconds with zero late arrivals, and the map
rebuild in 59.151 seconds. Total runtime was 155.730 seconds with exit 0. The
final log SHA-256 was
`ab27881e92681e50f2dbd61526736911a6d988eb83deb9ae35cf82a48ade9945`.
Final doctor closed `status=ok` in 6.341 seconds: all 793 retained raw packets
verified, 790 public packets, 790 availability entries, three tombstones, and
zero defects.

The enabled Windows task is exactly `Forseti Daily Lake Cadence`: daily
`09:00 +08:00`, `StartWhenAvailable`, `IgnoreNew`, six-hour execution cap,
last result 0, and next run `2026-07-20 09:00 +08:00`. A successful daily run
automatically maintains the lake and rebuilds the map; runtime code deployment
remains a deliberate manual pin. A fresh root still requires one explicit
`--bootstrap-active-product-mention-policy` run and later runs reuse its stored
pins. Stages 2–4 remain trigger-gated, and SLG-06/product-mention population
remains deferred until a named consumer and real transcript inputs exist.
These receipts establish bounded operational behavior, not readiness or
continuous freshness between passing runs.

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

### Stage 1B — Generation-published incremental source reuse

Owner-pulled forward 2026-07-20 after the daily dogfood showed that 22,526
classification-cache hits still required a 59.151-second whole-lake file walk
and readers could observe the delete-then-rewrite publication window.

- A disposable SQLite source inventory under the existing map cache home
  remembers every relevant derived source path, immutable content hash, body,
  and reusable classification key. Normal refresh still enumerates paths to
  reconcile against the lake, but it reopens no unchanged source body. A
  changed or disappeared write-once source fails loudly.
- The complete canonical JSON output is written under a new immutable
  generation directory. `core/CURRENT` changes atomically only after all six
  files exist. No generation cleanup is installed: the current output is small,
  and cleanup would add a reader race before a real storage trigger exists.
- A same-input refresh returns `current` without publishing another edition.
  A cold run deletes or ignores all updater state and must reproduce the same
  canonical JSON and manifests. SQLite file bytes are not proof; canonical
  published bytes are.
- Readers use one shared pointer/pair/hash verifier. The lookup and TikTok
  comment-coordination runners are the two sanctioned map consumers observed
  in the implementation census; pickup remains map-independent.
- This private SQLite notebook is not the deferred Stage 3 SQL query lens. No
  agent or vendor queries it, and it carries no authority.

## Operator Maintenance And Recovery

Routine maintenance is automatic at the successful tail of
`run_seam_cadence.py --run`; the enabled `Forseti Daily Lake Cadence` Windows
task remains the current daily trigger. The fast no-change path makes a shorter
future schedule cheap, but this work unit does not silently change the live
task's frequency or runtime checkout.

Fresh-root bootstrap, exactly once:

```powershell
python forseti-harness/runners/run_data_lake_indexes_rebuild.py --root <FORSETI_DATA_ROOT> --target derived_retrieval --bootstrap-active-product-mention-policy
```

Immediate refresh before same-day analysis:

```powershell
python forseti-harness/runners/run_data_lake_indexes_rebuild.py --root <FORSETI_DATA_ROOT> --target derived_retrieval --use-stored-product-mention-policy
```

Independent proof and periodic deep audit:

```powershell
python forseti-harness/runners/run_data_lake_indexes_rebuild.py --root <FORSETI_DATA_ROOT> --target derived_retrieval --prove-incremental-equality --use-stored-product-mention-policy
python forseti-harness/runners/run_data_lake_indexes_rebuild.py --root <FORSETI_DATA_ROOT> --target derived_retrieval --audit-source-integrity
```

Agent/operator response table:

| Observed result | What it means | What the agent should tell the owner to do |
| --- | --- | --- |
| `status=current` | The current edition already covers the reconciled inputs. | Nothing. Do not force another edition. |
| `status=rebuilt` | New inputs were incorporated and a complete edition was published. | Nothing unless a requested lookup still misses. |
| `another updater is active` / database locked | One writer already owns the disposable notebook. | Let the current run finish and retry once or wait for the next scheduled run. If repeated, inspect the running process/task; do not delete the database underneath it. |
| SQLite inventory has a supported schema but needs a clean refresh | Disposable updater state is stale; published map and evidence remain separate. | Run the same refresh with `--full-rebuild --use-stored-product-mention-policy`; reset occurs only after the updater holds the single-writer lock. |
| SQLite inventory unreadable/corrupt or has an unsupported schema, with source audit otherwise clean | Disposable updater state failed; published map and evidence remain separate. | Stop the scheduled updater, confirm no refresh process is running, remove only `core/cache/source_inventory.sqlite3`, then run the full-rebuild command. Never remove `raw/`, `derived/`, `generations/`, or `CURRENT` as part of this repair. |
| `append-only lake source changed` or `disappeared` | Possible evidence corruption or an out-of-contract rewrite, not a cache problem. | Stop. Preserve the failing path, run the lake doctor and `--audit-source-integrity`, and diagnose the source before resetting updater state. |
| `CURRENT` unreadable or names an absent generation | Publication pointer damage; existing generation directories may still be complete. | Do not hand-edit the pointer. Inspect retained generations and recover using exact stored policy pins or perform a cold rebuild; report that retrieval is unavailable, not that evidence is lost. |
| incremental/cold equality or rebuildability fails | The fast map and authoritative reconstruction disagree. | Preserve the current generation and reports, stop using the map as current, and investigate before rebuilding away the mismatch. |
| lake root unavailable | The evidence drive cannot be verified. | Reconnect the expected root and run the lake doctor. Never create or fall back to another root. |
| scheduled task fails once | Automatic maintenance did not complete. | Run the documented immediate-refresh command once. Repeated failure requires checking the task log, pinned runtime checkout, and root health. |

Map failure never implies evidence loss. Evidence durability remains a separate
deployment obligation: independently back up `raw/` and `derived/`; the map,
its generations, and its SQLite notebook need no backup.

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
- Automation boundary: the enabled `Forseti Daily Lake Cadence` task runs
  daily at `09:00 +08:00`; a successful `run_seam_cadence.py --run`
  maintains the lake and rebuilds the map automatically, while `--check` does
  not rebuild. Runtime code is deliberately pinned and deployed manually rather
  than self-updating. A fresh root uses one explicit
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

```yaml
direction_change_propagation:
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
    - output_authority
  doctrine_changed: >
    Stage 1 now reuses a complete disposable source inventory rather than
    reopening every unchanged derived record, publishes complete immutable map
    generations through one atomic CURRENT pointer, and binds sanctioned
    readers plus operator recovery to that generation contract. The canonical
    JSON views remain the cross-vendor proof surface; the private SQLite
    notebook is neither authority nor the deferred Stage 3 query lens.
  controlling_sources_updated:
    - docs/decisions/forseti_lake_map_scaling_and_hygiene_plan_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
    - forseti-harness/data_lake/derived_retrieval_state.py
    - forseti-harness/data_lake/derived_retrieval_cache.py
    - forseti-harness/data_lake/derived_retrieval_views.py
    - forseti-harness/data_lake/product_mention_selection.py
    - forseti-harness/runners/run_data_lake_indexes_rebuild.py
    - forseti-harness/runners/run_derived_retrieval_lookup.py
    - forseti-harness/runners/run_tiktok_comment_coordination.py
  downstream_surfaces_checked:
    - forseti-harness/data_lake/root.py
    - forseti-harness/runners/run_seam_cadence.py
    - forseti-harness/tests/test_data_lake_indexes_rebuild.py
    - forseti-harness/tests/test_data_lake_rebuild_proof.py
    - forseti-harness/tests/unit/test_tiktok_comment_coordination.py
    - forseti-harness/tests/unit/test_seam_cadence.py
  intentionally_not_updated:
    - path: forseti-harness/data_lake/root.py
      reason: >
        The root still creates the fixed query_tables/manifests directories as
        the pre-pointer migration fallback. Dynamic generation directories are
        builder-owned and need no new authoritative root write surface.
    - path: forseti-harness/runners/run_seam_cadence.py
      reason: >
        It already invokes the sole sanctioned updater only after a passing
        cadence. The updater's new current/rebuilt distinction does not change
        cadence success or failure semantics.
    - path: live Windows Task Scheduler configuration
      reason: >
        The enabled daily task remains the observed automatic trigger. This
        repository work does not silently change its frequency or pinned
        runtime checkout.
  stale_language_search: >
    rg -n "core/(query_tables|manifests)|core\\\\(query_tables|manifests)|
    derived_retrieval/silver_vault/core/query_tables|wipes and rewrites|
    delete-then" forseti-harness forseti/product/spines/data_lake
    docs/decisions/forseti_lake_map_scaling_and_hygiene_plan_v0.md
  stale_language_search_result: >
    Executed 2026-07-20. Remaining fixed-path hits are the root's deliberate
    empty migration directories and the consumption contract's explicit
    pre-CURRENT fallback. The lookup-runner stale docstring and contract
    one-screen summary were updated. Historical 59.151-second and
    delete-then-rewrite wording remains only as the observed reason Stage 1B
    was pulled forward.
  non_claims:
    - not live deployment or a change to the current scheduled-task frequency
    - not evidence backup or drive-failure recovery
    - not Stage 2 sharding or the Stage 3 SQL query lens
    - not continuous freshness between updater reconciliations
```
