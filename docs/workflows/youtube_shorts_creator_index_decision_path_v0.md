# YouTube Shorts Creator Index Decision Path v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Source-backed placement and field-contract recommendation for YouTube Shorts creator ledger/index artifacts.
use_when:
  - Deciding where future YouTube Shorts creator-analysis lanes should route observed handle/channel evidence.
  - Checking whether the 200-row fragrance creator ledger can be reused as a cross-lane creator index.
  - Designing the minimum fields and non-claims for a cross-lane creator index.
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.md
  - .agents/workflow-overlay/artifact-folders.md
input_hashes:
  - path: docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json
    sha256: abc788fa4e6dde0d5aa189166e7176d109c0a0c82fcf29462e31c621a2ca026b
    size: 64190
  - path: docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json
    sha256: e1d74fe107d0ad416becb7df19cd115364ab69c46c7a3c66ed08a4b182837d0a
    size: 791926
branch_or_commit: codex/youtube-shorts-tone-viability-prompt @ 36b32cfa61b421dd32f4994b78c47379bfbae843
stale_if:
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json changes.
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json changes.
  - .agents/workflow-overlay/artifact-folders.md changes accepted folder rules for docs/review-inputs, docs/workflows, or orca/product/.
  - .agents/workflow-overlay/artifact-roles.md changes review-input or workflow-record role bindings.
authority_boundary: retrieval_only
```

## Source-Loading Surface

Purpose: record the smallest source-backed path for deciding creator-ledger/index placement before creator-analysis lanes cite the current pool ledger as a stable cross-lane creator substrate.

Do not use for: creator identity verification, cross-platform identity linking, creator quality ranking, buyer proof, energy/prosody claims, runtime capture, crawler design, or transcript storage.

Authority boundary: this is a workflow recommendation and routing record. `AGENTS.md` and `.agents/workflow-overlay/` control Orca project rules. The source JSON artifacts control observed pool and ledger facts. Owner acceptance is still required before treating a cross-lane index placement as final product or capture-spine authority.

Recheck recipe: re-hash the two JSON inputs in the retrieval header, re-run the count assertions in "Verified Inputs", and re-read `.agents/workflow-overlay/artifact-folders.md` plus `.agents/workflow-overlay/artifact-roles.md` before promoting or materially changing this route.

Non-claims: not approval, not validation, not readiness, not source-of-truth promotion, not identity verification, not implementation authorization, not buyer proof.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 target deepening
  edit_permission: docs-write
  target_scope: docs-only workflow record for YouTube Shorts creator ledger/index placement and schema boundaries
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md; overlay README/source-of-truth/source-loading/artifact-folders/artifact-roles/retrieval-metadata; creator ledger md/json; expansion200 capture md/json
```

## Verified Inputs

| Source | Fresh observations used here |
| --- | --- |
| `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json` | `ledger_policy.identity_posture` is "observed YouTube channel/handle evidence only"; counts are `pool_rows_total=200`, `creators_observed=31`, `creator_or_channel_observed=30`, `brand_or_platform_accounts_observed=1`; `admitted_rows_total` across creator entries sums to 200. |
| `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.md` | The human summary states the ledger records observed handles/channels, not identity verification, ranking, row relevance certification, or independent-creator proof. |
| `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json` | Counts are `prior_admitted_total=100`, `new_admitted=100`, `cumulative_admitted_total=200`, `attempts=152`; the cumulative pool has 200 objects and 200 unique video IDs. |
| `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.md` | The pool is admitted as a 200-Short capture expansion, not a labeled benchmark; transcript bodies remain outside the repo; the companion creator ledger is observed handle/channel evidence only. |
| `docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md` | Energy, pace, volume, and prosody are excluded from transcript-only labels; stable coarse tone fields are not creator-index fields. |
| `.agents/workflow-overlay/artifact-folders.md` and `.agents/workflow-overlay/artifact-roles.md` | `docs/review-inputs/` is the accepted home for prepared review inputs; `docs/workflows/` is the accepted home for workflow records, operational notes, and repo maps; `orca/product/` is the product tree with stronger governance expectations. |

## Placement Comparison

| Placement | Fit | Cost / risk | Recommendation |
| --- | --- | --- | --- |
| Keep only `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.*` | Correct for the 200-row fragrance pool evidence ledger. It preserves the observed source facts beside the capture review input. | Weak cross-lane reuse. Future creator lanes could overread a corpus-specific ledger as universal creator coverage. | Keep it as the source evidence ledger only. Do not rename it into the cross-lane index. |
| Add a cross-lane index under `docs/workflows/` | Best fit for a non-authoritative routing/index object that points to one or more pool ledgers, records lifecycle rules, and carries non-claims. | Requires one more durable artifact and disciplined source-hash refresh when ledgers change. It must not become a hidden source of truth. | Recommended next durable object if creator lanes need a stable join surface. Call it an index, not a ledger, because it routes evidence ledgers rather than becoming evidence itself. |
| Promote now into `orca/product/spines/capture/...` or another product/capture spine | Could become appropriate if recurring creator-ledger operations become part of the accepted capture operating model. | Highest lock-in. Product/capture placement implies stronger governance expectations, source-quality gates, and possible confusion with identity/linking authority. | Defer. Promote only after the owner accepts a recurring creator-ledger operating contract and identity/linking gates. |
| Split evidence ledger plus workflow index | Preserves the current corpus-local evidence while giving future lanes a stable non-authoritative routing surface. | Requires clear lifecycle and non-claim language in both artifacts. | Preferred architecture. |

## Recommended Architecture

Use a split architecture:

1. Keep `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.md` and `.json` as the pool-specific evidence ledger for the 200-row fragrance Shorts pool.
2. If downstream creator-analysis lanes need a stable cross-lane surface, create a separate workflow index under `docs/workflows/`, for example `docs/workflows/youtube_shorts_creator_index_v0.md`.
3. The cross-lane object should be an index, not a ledger. A ledger records observed evidence for one corpus or pool. An index routes across ledgers, carries join keys and lifecycle rules, and repeats only the minimum observed-handle facts needed for routing.
4. Product/capture-spine promotion stays deferred until a later accepted operating contract defines recurring source quality, update cadence, identity verification gates, and cross-platform linking boundaries.

This recommendation intentionally chooses the lower-lock-in complete path. It gives creator lanes a durable routing surface without prematurely promoting corpus-specific observations into product/capture authority.

## Field Contract

Minimum field inclusion test: every field must support joining, provenance, lifecycle, or residual visibility. Exclude fields whose main purpose is ranking, scoring, creator quality assessment, inferred identity, tone generalization, or engagement prediction.

Required fields for a future cross-lane creator index:

| Field | Purpose | Boundary |
| --- | --- | --- |
| `index_entry_id` | Stable row key for the index entry. | Must be deterministic from observed platform keys; not a person ID. |
| `platform` | Source platform, initially `youtube_shorts` or `youtube`. | Not cross-platform linking. |
| `observed_handle` | Handle/query string as observed in source artifacts. | Not legal identity or ownership. |
| `observed_author_names` | Author/channel names seen in source artifacts. | May be aliases or display names; not verified person names. |
| `observed_channel_ids` | Channel IDs when retained by source artifacts. | `UNKNOWN` remains valid when prior fixtures lack the field. |
| `creator_classification` | `creator_or_channel_observed`, `brand_or_platform_account_observed`, or a future explicit residual value. | Classification is observation posture, not creator quality. |
| `identity_verification_status` | Default `not_verified`; future stronger values require accepted gates. | Must not be self-certified by the index. |
| `evidence_ledgers` | Paths, hashes, and counts for source ledgers that support the entry. | Points to evidence; does not copy transcript bodies. |
| `corpus_memberships` | Pool IDs, row IDs, video IDs, counts, and relevance residuals by corpus. | Corpus coverage is not creator coverage. |
| `join_keys` | Video IDs, pool IDs, channel IDs, handles, and source URLs needed for joins. | No transcript text bodies. |
| `residual_flags` | Unknown channel IDs, brand/platform account, abstain/off-topic residuals, low-evidence rows, or source gaps. | Residuals travel with the row instead of being smoothed away. |
| `lifecycle` | Created/updated timestamps, source hashes, supersedes/superseded-by, stale conditions. | Lifecycle metadata is routing support, not validation. |
| `non_claims` | Identity, independence, ranking, buyer proof, energy/prosody, and benchmark boundaries. | Must stay visible in every durable index artifact. |

Pool-specific creator ledgers should keep richer evidence-local fields such as `pool_ids`, `video_ids`, `sample_shorts_urls`, word-count ranges, source artifact counts, and known label-status counts. The cross-lane index may point to those fields but should not duplicate every row-level detail unless a future join requires it.

Forbidden index fields without a new accepted source gate:

- transcript bodies or transcript excerpts;
- audio energy, pace, volume, prosody, or excitement;
- creator quality scores, trust scores, rankings, or "best creator" labels;
- person identity, ownership, independence, agency representation, or cross-platform same-entity assertions;
- buyer-proof, validation, benchmark-readiness, or judgment-quality status.

## Lifecycle Boundary

- Create or update the cross-lane index only when a source evidence ledger is created, materially changed, or intentionally admitted into the index.
- Each update must re-hash source ledger and pool JSON files, re-derive row counts, and carry changed residuals forward.
- Index updates are docs-only unless a later accepted handoff explicitly authorizes bounded implementation.
- If source artifacts drift, prefer updating the evidence ledger first and then refreshing the index from that ledger; do not silently patch the index as the only copy of evidence.
- Retire or supersede this workflow-level route only after an owner-accepted product/capture operating contract defines stronger placement.

## Next Authorized Actions

- Current lane: close after this recommendation is written, source-checked, and the consumed handoff checkpoint is retired.
- If owner accepts this route: create `docs/workflows/youtube_shorts_creator_index_v0.md` as a retrieval-only cross-lane index that points to the fragrance creator ledger and any future source ledgers.
- If owner wants stronger authority now: first author an operating contract for creator-ledger lifecycle, identity verification gates, and source-quality requirements; do not promote by moving the current pool ledger alone.
- Tone-labeling continuation may use this record as routing context, but it must still cite the source pool and ledger directly for observed facts.
