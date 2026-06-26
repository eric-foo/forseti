# Product-Verdict Gold-Write Lane Article (v0)

```yaml
retrieval_header_version: 1
artifact_role: Lane article (reference) — how to persist Pass-2 product verdicts to the data lake (GOLD layer)
scope: >
  The pickup point for the (currently deferred) gold-write build: take the built, deterministic
  Pass-2 product fusion (orca-harness/scoring/product_fusion.py) and persist its verdicts to the
  data lake as a GOLD derived layer, mirroring orca-harness/ecr/lake.py and
  orca-harness/cleaning/transcript_product_lake.py. Records the agreed v0 shape (per-video gold),
  the pattern to mirror, and what stays deferred (cross-creator aggregation).
use_when:
  - Starting the gold-write lake adapter for product verdicts.
  - Confirming the agreed shape and what is in vs out of v0 before building.
authority_boundary: retrieval_only
open_next:
  - orca-harness/scoring/product_fusion.py
  - orca-harness/cleaning/transcript_product_lake.py
  - orca-harness/ecr/lake.py
  - orca-harness/data_lake/root.py
stale_if:
  - The fusion's input (ProductMention) or output (ProductVerdict / ProductVerdictSet) shape changes.
  - The data lake record-set / append-only / completion-marker contract changes.
  - The owner authorizes the deferred cross-creator / cross-video aggregation (then its section is built).
status: DEFERRED — owner-deferred 2026-06-26 pending IG + YT lane structural sync; REFERENCE ONLY, this article authorizes no build.
```

## Status — why this is deferred

Pass-2 product fusion is **built, reviewed, and merged** (`scoring/product_fusion.py`, deterministic, LLM-free, source-agnostic; eric-foo/orca#394). The **gold write** (persisting its verdicts to the lake) is **deferred by the owner on 2026-06-26** so the **IG and YouTube lanes can first be synced** in structure / handling before the lake layer is wired. This article is the reference an agent opens **when gold writes resume**. It grants no build authority; resuming needs its own owner go.

## What the gold write does

Persist a Pass-2 `ProductVerdictSet` to the data lake as a **gold** derived layer, anchored to the same raw the silver mentions key to — so a reader can walk gold verdict → silver mentions → bronze transcript/audio.

## The agreed v0 shape — PER-VIDEO

The silver mentions are stored **per-transcript (per-video)**, keyed by `transcript_anchor`, with **no creator index** (`cleaning/transcript_product_lake.py`: `derived/<transcript_anchor>/silver__cleaning__product_mentions/`). The transcript specs' v0 gold layout is likewise per-video. So v0 gold is **per-video**:

1. Read one transcript's silver mentions at `derived/<transcript_anchor>/silver__cleaning__product_mentions/`.
2. Parse them into `ProductMention`s.
3. `fuse_product_verdicts(mentions, creator_id=<video owner>)` — `creator_id` is **caller-supplied** (the video's owner from capture metadata; the silver lane carries none).
4. Write the `ProductVerdictSet` to `derived/<transcript_anchor>/gold__scoring__product_verdicts/<record_id>` as an all-or-nothing record-set with a completion marker.

## The pattern to mirror

Same read/derive/append rails as the proven derivers:
- `ecr/lake.py` — `derive_ecr_into_lake` (load by key → run pure deriver → `append_record_set`).
- `cleaning/transcript_product_lake.py` — `extract_products_into_lake` (the silver sibling; same `append_record_set(subtree="derived", raw_anchor=..., record_id, members, completion_lane)` shape).

Keep the **pure fusion** (`scoring/product_fusion.py`) separate from the **I/O adapter** (a new `scoring/product_verdict_lake.py` or similar) exactly as `ecr.deriver` is separate from `ecr.lake` — so the fusion stays offline-testable and the I/O is isolated.

**Lane naming:** `gold__scoring__product_verdicts` + `gold__scoring__product_verdicts__set` (completion), mirroring the silver `silver__cleaning__product_mentions(__set)`.

## Determinism / idempotency

- Deterministic `record_id` per `(mentions content + fusion_config_version)` so re-runs check/skip (like `mentions_record_id`); write-once (re-derive = a fresh `record_id`).
- Pin `generated_at` when byte-identical re-derivation matters (the fusion defaults it to `utc_now_z()`).

## Boundaries (carry verbatim)

- The gold verdict is **observed-stance sentiment** ("what the creator said about this product"), **never** demand / credibility / independence / Action-Ceiling — those are **Judgment**.
- **No engagement/resonance input** — that is the Engagement Logic Registry's domain (`orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`), joined at Judgment, not here.
- LLM-free (`scoring/` no-LLM zone; keep the contract test green).

## Build steps (for the picking-up agent)

1. New `scoring/product_verdict_lake.py` (mirror `cleaning/transcript_product_lake.py`): `derive_product_verdicts_into_lake(*, data_root, transcript_anchor, creator_id, ...)` — load the silver mentions for `transcript_anchor`, parse to `ProductMention`s, `fuse_product_verdicts`, `append_record_set` the gold set.
2. A thin runner (mirror the transcript/ECR runners), daemon-ready, skip-if-complete via `is_record_set_complete`.
3. Offline fixture tests (mirror `test_audience_fusion` / `test_product_fusion` discipline) — no LLM, no network.
4. Delegated cross-vendor review (contract-bearing lake surface).
5. DCP: the gold layer moves from "scoped" to "shipped" in the YouTube + IG transcript specs.

## Deferred — NOT v0 (cross-creator aggregation)

"A creator's verdict for a product **across all their reels**" is a **separate Named Upgrade** (the transcript specs already defer it). It needs (a) a **creator → videos** resolution (the capture lane owns the mapping; the silver lane has no creator index) and (b) a **new cross-video anchor shape** (the lake is per-packet today). Do not fold it into the per-video v0.

## Entry pointers

- Fusion: `orca-harness/scoring/product_fusion.py` (and `schemas/product_mention_models.py` for `ProductMention` / `ProductVerdict` / `ProductVerdictSet`).
- Lake API: `orca-harness/data_lake/root.py` (`append_record_set`, `load_raw_packet`, `is_record_set_complete`).
- Silver persistence: `orca-harness/cleaning/transcript_product_lake.py`.
- Pattern template: `orca-harness/ecr/lake.py`.
- Gold-layer layout + medallion naming: the YouTube + IG transcript→product extraction specs under `orca/product/spines/capture/core/source_families/social_media/`.

## Non-claims

Reference doc only. Not validation, readiness, or acceptance; authorizes no build, capture, or lake write (each needs its own owner go). The Pass-2 fusion it builds on is merged; this gold-write layer is not yet built.
