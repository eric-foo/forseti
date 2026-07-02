# Orca Data Lake derived_retrieval Activation Proposal v0

```yaml
retrieval_header_version: 1
artifact_role: >
  Proposed architecture decision-request (non-authorizing). Requests owner gate-closure
  to populate the already-reserved indexes/derived_retrieval slot with three object-level
  reverse-lookup views (by-creator, by-mention, undone-discovery), and to decide
  query-engine timing. Re-decides no ratified architecture; works strictly within the
  storage, derived-layout, and medallion contracts.
scope: >
  Why the derived_retrieval governance gate's named trigger ("a governed consumer needs a
  reverse lookup") is now met; the three views proposed; how incremental discovery would
  be built (the daemon full-rescan fix); the trigger/routine model for deterministic vs
  LLM/capture lanes; the engine residual (by-key scan now, SQL query-lens later); the
  bronze/silver/gold mapping; and every accepted residual under the mini-god-tier lens.
use_when:
  - Deciding whether to close the derived_retrieval population gate for object-level retrieval.
  - Scoping incremental work-discovery for the transcript/extraction runner (the O(total) rescan).
  - Checking that a creator/mention retrieval design stays object-level and non-dossier.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
authority_boundary: retrieval_only
status: >
  PROPOSED 2026-06-25. Decision-request only: not implementation authority, not a contract
  amendment, not engine selection, not validation/readiness. Becomes actionable only if the
  data-lake-spine owner adopts it and records the gate-closure in the owning contracts.
stale_if:
  - The derived-layout, storage, or medallion contract changes the derived_retrieval, by-key-discovery, or medallion boundary.
  - The owner adopts this (then it is superseded by the ratified gate-closure record).
  - Capture/silver schema or the transcript runner's discovery path is restructured before adoption.
```

## What this asks for (one screen)

```text
The architecture is already decided. This requests a GATE CLOSURE, not a new design.

Close the derived_retrieval population gate for three OBJECT-LEVEL reverse-lookup views:
  1. by_creator    : (source_family + observed public handle) -> packet/derived refs
  2. by_mention    : (brand / product line entity)            -> packet/derived refs
  3. undone         : (committed - done)                       -> packets needing work

Then decide query-engine TIMING (by-key scan now; SQL query-lens when latency warrants).

Everything stays inside the ratified contracts: raw stays opaque on the filesystem; the
views are rebuildable, non-authoritative, non-Judgment; by-key discovery stays the
authority and the backstop.
```

## Why now — the named trigger conditions are met

The derived-layout contract reserved `derived_retrieval` and gated its population behind explicit triggers. Both are now met:

- **Residual:** *"derived_retrieval population deferred (rebuildable, non-authoritative, governance-gated); trigger: a governed consumer needs a reverse lookup."*
  - **Met by three governed consumers:** (a) ideal-audience inference needs *creator → all of that creator's packets* to fuse a per-creator profile (`fuse_profile` is single-creator and consumes a pre-gathered record list — it does not find them); (b) product intelligence needs *brand/line → all videos mentioning it*, across creators; (c) the transcript/extraction runner needs *undone → packets needing extraction* to stop rescanning the whole lake every run.
- **Residual:** *"No backend/queue/scheduler/engine (by-key discovery is authority); trigger: scan/query latency proves insufficient."*
  - **Early evidence, not yet decisive:** `run_extraction` rebuilds the whole availability index and `load_raw_packet`-hashes every YouTube packet on every run (`runners/run_transcript_product_extract.py` → `rebuild_availability()` + `list_available()` + per-packet `load_raw_packet`); the completion marker stops re-*extraction*, not re-*discovery*. This is O(total) per run regardless of backlog. At low thousands it is "early, not paranoid"; the engine decision can therefore be **staged** (see below) rather than forced now.

## What is already decided (this proposal re-decides none of it)

- **Cross-object analysis already has its home, with no new lake structure.** Derived-layout contract: cross-object/aggregate/on-demand analysis *"lives as a rebuildable `indexes/derived_retrieval/` view ... never forced into the single-anchor `derived/` grammar and never becomes lake authority."* by-creator and by-mention **are** cross-object analysis. (This is also why a physical `social_media/creator/platform/` tree is the wrong mechanism — a packet has one physical home but must be findable by multiple axes; the ratified answer is index views, not folders.)
- **Raw stays opaque + filesystem.** Storage contract is *non-selecting* — `packet_id` is an opaque handle; raw is write-once; SQL is wrong for blob preservation. No change proposed to raw.
- **Indexes are rebuildable-or-not-an-index.** derived-layout `prove-rebuildability` check; `derived_retrieval` rebuilds only from committed `derived/` + raw refs.
- **Medallion boundary.** Silver = *"mechanical derived features over raw"*; gold = Judgment only ("gold does not leak out of Judgment"). The views are **silver-tier retrieval**; never pre-gold (no Spike/Movement Alert semantics) and never gold.

## The three views

All three are rebuildable `derived_retrieval` views: non-authoritative, regenerated from committed `derived/`/silver + raw refs, never a source of truth.

| View | Key | Maps to | Rebuilt from |
| --- | --- | --- | --- |
| `by_creator` | `source_family` + observed public handle/id (per-platform, object-level) | packet + silver-record refs | creator field already on silver records (e.g. `EvidenceRecord.creator_id`; channel_id in caption `capture_metadata.json`) |
| `by_mention` | brand / product-line entity (object-level) | packet + silver-record refs | source-backed-complete `silver__cleaning__product_mentions` records (brand/line/stance already extracted) |
| `undone` | extraction status (`committed − done`) | packets needing extraction | availability (committed raw) minus completion markers (`is_record_set_complete`) |

Note `by_mention` needs **no new capture** — the mention data already lands in silver; this only indexes it. The evidence view must still apply the read-side Silver lineage gate: records whose `silver_record_source_backed_status` is missing, incomplete, invalid, or limitations-only may be counted as explicit residuals or cleanup inputs, but must not enter the source-backed mention evidence index.

## How best to build it (the deep-think)

### Incremental discovery (the daemon fix)

The earliest-biting problem is discovery, not query. Fix it by computing the undone set without a full rescan:

- Maintain availability **incrementally** (record a packet at commit) instead of `rebuild_availability()`-ing the whole index each run.
- Find work as the cheap diff `committed − done` (the `undone` view), and `load_raw_packet` **only the delta** — which also retires the "re-hash every packet every run" cost (done packets are never touched).
- **Keep by-key reconcile as the authoritative backstop.** Per storage-contract blocker 4, by-key discovery must still find committed work *"even if an event message is missed"* — the incremental view is an optimization layered over by-key, never a replacement.

### Trigger / routine model

The need for a *routine* comes from **cost + nondeterminism + external side-effects** — i.e. network capture and LLM extraction. Those are genuine scheduled jobs. The **deterministic lanes (ECR, SCR, deterministic cleaning) need no routine**: they are pure, re-runnable functions that can run **on-demand as a deterministic continuation** the moment their input exists, and being deterministic they may be recomputed rather than guarded for staleness (re-derive-never-migrate already permits this). Determinism removes the *correctness* reason for scheduling, not the *performance* one — so deterministic outputs may still be materialized/cached, and that cache is itself a rebuildable `derived_retrieval` view. Net: routine shrinks to capture + LLM; the deterministic spine is lazy pure functions.

**Owner preference — auto over daemon.** For the capture + LLM jobs that do need triggering, the owner prefers an **automatic** trigger over manual/attended runs, but **not a persistent daemon unless that is the only way to get auto.** Auto is achievable without a daemon: **event-triggered** (capture committing a packet fires that packet's extraction) or a **scheduled one-shot** (cron / Task Scheduler runs the pull-and-process and exits — a transient process, not an always-on loop). A persistent daemon is warranted only if *continuous low-latency* reactivity is required, which the per-creator capture cadence does not need. Two invariants hold for any of these: the trigger lives **outside the lake** (the storage + derived-layout contracts forbid the lake from scheduling, routing, retrying, or orchestrating — the wrapper *pulls* by key; the lake never pushes), and auto cadence makes **incremental discovery non-optional** (the more often it auto-fires, the less acceptable an O(total) rescan per run becomes).

### Engine (staged; an owner decision, not selected here)

Two contract invariants bound any engine: **raw truth is never replaced**, and **indexes must be rebuildable**. That sorts the options:

- **Recommended shape — SQL as a rebuildable query-lens, not a system of record.** Either DuckDB querying the silver files *in place* (files stay authoritative, the query *is* the index, zero separate artifact, rebuildable by definition) or a rebuildable SQLite index DB. With a query-lens, all three views collapse to `WHERE`/`JOIN` and no hand-built index tree is maintained — discovery is `committed − done`; retrieval is `WHERE creator =` / `WHERE mention =`.
- **Staging:** by-key + scan is what the contracts sanction *today* and is fine at current scale; adopt the query-lens when the contract's *"scan/query latency proves insufficient"* trigger actually fires. Do not select a backend pre-emptively.
- **Trap to avoid:** "SQL replaces the index" must not drift into "SQL replaces the lake" — the DB stays a disposable projection over filesystem-authoritative raw/silver.

## Bronze / silver / gold mapping

- **Bronze:** unchanged — opaque, write-once, by-key archive. Creator identity stays *captured* in content (e.g. caption `capture_metadata.json` `channel_id`), not a key.
- **Silver:** where the views + queries live (retrieval over mechanical derived features). The proposal adds nothing to gold.
- **Object-level, not actor.** by_creator (the content producer's public handle) and by_mention (a product/brand) are object-level cross-comparison, which the derived-layout contract explicitly allows. This is **not** the actor/commenter timing retrieval governed (tightly) by the medallion contract — that lane is out of scope here.

## Accepted residuals (mini-god-tier lens — named, not closed)

- **Cross-platform creator identity unification is given up.** `by_creator` is per-platform handle only; unifying one creator across yt/ig/tt is explicitly a medallion-contract *Visible Limitation* and would need separate owner authorization (it appears in that contract's `stale_if`). Audience profiles therefore remain per-(creator, platform) until that is authorized.
- **Flat `raw/` sharding deferred (scalability-last).** Fine to ~100k packets; sharding (`raw/<prefix>/<id>`) is a core-lake change triggered by real volume, not this proposal.
- **Re-hash-on-read remains** (integrity feature); incremental discovery neutralizes its per-run cost by touching only undone packets.
- **Engine selection staged** (by-key now; query-lens at the latency trigger) — not selected here.
- **Actor/commenter timing retrieval out of scope** (separate, tighter medallion governance).
- **Capture-completeness is the real limit, not lake structure** — what was not captured cannot be derived; coverage limits/residuals/raw-pull flags travel with outputs.

## Owner decisions requested

1. **Close the `derived_retrieval` population gate** for the three object-level views above (records that the "governed consumer needs a reverse lookup" trigger is met).
2. **Confirm per-platform-only creator scope** (no cross-platform identity unification yet).
3. **Decide engine timing:** ratify the staged path (by-key scan now → SQL query-lens at the latency trigger), or call the latency trigger already met and authorize the query-lens now.

## Non-claims

Not validation, readiness, or implementation authorization. Not a contract amendment (works within the ratified storage/derived-layout/medallion contracts). Not backend/engine selection. Not cross-platform identity resolution. Not actor-retrieval design. Not Judgment/gold semantics. A green `check_placement` run is placement shape, not authority.

## On adoption (not performed by this proposal)

If the owner adopts this, the gate-closure belongs in the owning contracts — the derived-layout contract's `derived_retrieval` residual and (if the engine is authorized) the storage contract's engine residual — so the source of truth moves with the decision, rather than living only in chat. Implementation would then be a separate data-lake-spine work unit (its own branch), not bolted onto any in-flight lane.
