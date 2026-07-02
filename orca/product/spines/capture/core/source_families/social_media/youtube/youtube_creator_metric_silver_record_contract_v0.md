# YouTube Creator Metric Silver Record Contract v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_architecture_contract
scope: >
  Producer-owned Silver Vault record contract for YouTube creator metrics: the
  MetricObservation and MetricRollupObservation derived records emitted by the
  YouTube creator-metric Silver producer from the committed YouTube Shorts
  fragrance creator-metric seed. A sibling to the Instagram creator-metric
  contract; it restates only the YouTube-specific deltas (number source,
  anchoring, view-only posture surface) and inherits the shared Silver envelope
  and rollup posture rules from the contracts in open_next.
use_when:
  - Scoping or reviewing the YouTube creator-metric Silver producer.
  - Checking how a YouTube MetricObservation/MetricRollupObservation is anchored and provenance-stamped.
  - Deciding how a YouTube per-account rollup anchors when its observations span multiple raw packets.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json
  - orca-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py
  - orca-harness/tests/unit/test_youtube_creator_metric_silver_producer.py
stale_if:
  - The Silver Vault record contract changes the record header, MetricObservation, posture, or content_hash semantics.
  - The Instagram creator-metric contract changes the shared MetricRollupObservation payload shape or derivation marker.
  - The committed youtube_shorts_fragrance_creator_metric_seed_v0.json observation/rollup shape changes.
  - A YouTube seed builder is introduced and the producer recomputes instead of wrapping the committed seed.
```

## Status

`YOUTUBE_CREATOR_METRIC_SILVER_RECORD_CONTRACT_V0`.

Producer-owned record contract for the YouTube creator-metric Silver producer
(`orca-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py`).
It is the YouTube sibling of the Instagram
`creator_metric_silver_record_contract_v0`, built to the same Silver Vault
record contract. Retrieval-only: not validation, readiness, backend selection,
dashboard, live capture, or cross-platform identity. It does not re-state the
shared Silver envelope or the rollup posture/derivation rule — those live in the
two contracts in `open_next` and are inherited verbatim. This doc fixes only
what is YouTube-specific.

## What the producer emits

The producer makes YouTube creator metrics lake-native. Number source (resolved
in implementation scoping — **Option 2, "wrap the committed seed"**): it reads
the committed
`youtube_shorts_fragrance_creator_metric_seed_v0.json` and re-emits, with **no
recompute**:

- one **MetricObservation** Silver Vault record per committed seed observation
  (per-Short `view_count`, 196 records across 30 accounts); and
- one **MetricRollupObservation** Silver Vault record per platform account (30
  records).

Both are `record_kind: observation` records carrying the Silver Vault common
header with `content_hash` on the `canonical_json_excluding_content_hash` basis,
shared `payload_kind` values (`MetricObservation` / `MetricRollupObservation`),
and the mandatory rollup `payload.observation.derivation` marker — all exactly as
the Instagram contract defines them. These records share the platform-agnostic
`creator_metric_silver` / `creator_metric_rollup_silver` lanes with the Instagram
producer; YouTube vs Instagram records stay distinguishable by `source_family`
(`social_media`), `source_surface` (`youtube_shorts`), `producer_id`, and the
subject `namespace` (`youtube`).

## YouTube-specific anchoring (the reviewable delta)

The Instagram observation carries a `raw_anchor` dict
(file_id/relative_packet_path/sha256/hash_basis) and a single shared source
packet per rollup. **YouTube is different, and the producer is honest about it:**

- **Observation `raw_anchor`** is the observation's own
  `source_packet_id_or_none` — a real Crockford-26 lake raw-packet handle that
  every committed YouTube observation carries (verified: 196/196 populated). This
  mirrors Instagram anchoring (derived record tied to the raw packet it derives
  from). The local-only `source_packet_pointer_or_none` (an absolute capture-host
  path) is **not** used — the seed itself marks it non-portable.
- **Rollup `raw_anchor`** is the rollup's `platform_account_id` (for example
  `acct_yt_fragrance_001`), **not** a single packet id. A per-account rollup
  aggregates observations that span **multiple distinct per-Short packets** (28
  of 30 accounts), so there is no single source packet to anchor it to. An
  account-scoped raw anchor is the honest choice for a multi-packet aggregate.
- **`raw_refs`** are rebuilt from the fields the YouTube seed actually declares
  as portable provenance (`source_pointer`, `source_field`, `source_file`,
  `source_packet_id_or_none`), with `sha256` + `hash_basis` set from the captured
  watch-page HTML hash (`source_watch_html_sha256_or_none`) — the hash-checkable
  source material per the Silver Vault `raw_refs` rule — and the shorts-page HTML
  hash preserved alongside. The producer does **not** fabricate an
  Instagram-style `raw_anchor` dict that the YouTube seed does not carry.

## Posture surface (view-only)

YouTube observes only `view_count`, so every observation is `observed` with a
numeric value. At the rollup level only `average_views` and `median_views` are
`observed`; `engagement_rate`, `average_like_count`, and `average_comment_count`
are `unavailable_with_reason`, and `posting_cadence` / `recent_velocity` are
`not_attempted` — all with `metric_value: null` and a reason. The producer
enforces the Silver posture/value coupling on every metric (observed ⇔ numeric
value and no reason; non-observed ⇔ null value and a reason) and fails closed on
a violation. **Missing is never zero**; there is no engagement number computed
from view-only data.

## Conformance and no-drift

- Every emitted record obeys the Silver posture/value coupling and fails closed
  on a violation, a blank/absent subject `native_id`, or a missing source packet
  anchor (never emits a fake-shaped record).
- The producer does not compute metrics. Under Option 2 the emitted numbers ARE
  the committed, already-tested seed numbers, so no-drift holds by construction;
  the producer test additionally asserts numeric equality against the committed
  seed for all 196 observations and 30 rollups.

## Accepted residuals (named, not hidden)

- **Derives from the committed proof seed**, not a live recompute from source
  review-inputs — the doctrinal difference from Instagram (which reuses a live
  builder). YouTube has no such builder. Upgrade trigger: if the YouTube seed
  needs live recompute, extract a `youtube_metric_seed.py` builder (handoff
  Option 1) and have the producer reuse it; equality with the committed seed
  stays mandatory.
- **Account-scoped rollup anchor** (vs Instagram's packet-scoped rollup anchor),
  because YouTube rollups span multiple per-Short packets. Upgrade trigger: a
  YouTube projection that yields one packet per account.
- **Silver-envelope helpers are duplicated** from the Instagram producer to keep
  the merged Instagram module untouched. Upgrade trigger: a clean shared
  silver-envelope core is extracted and both producers import it.
- **Shared platform-agnostic lanes** with the Instagram producer. Upgrade
  trigger: the owner/reader prefers per-platform lanes (a constant change while
  records remain test-only; no real-lake migration).
- v0 emits MetricObservation + MetricRollupObservation only — no
  entity/relationship records, no cross-platform creator identity, and no
  re-point of the `creator_profile_current` read model (the separate reader
  lane).

## Non-Claims

- not validation
- not readiness
- not buyer proof
- not a representative creator average
- not channel-wide creator influence
- not cross-platform identity linkage
- not a follower graph or audience estimate
- not an engagement-rate, like, or comment metric
- not SQLite or backend selection
- not dashboard implementation
- not live capture authorization
- not a re-point of the creator_profile_current read model
