# YouTube Shorts Creator Infrastructure Decision Path v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Source-backed placement and field-contract recommendation for planned creator-ledger infrastructure across YouTube Shorts and future social creator source families.
use_when:
  - Deciding where recurring creator-ledger infrastructure should live across Scanning, Capture, Data Lake, and projection surfaces.
  - Checking whether the 200-row fragrance creator ledger can be reused as infrastructure evidence.
  - Designing the minimum creator-observation, niche membership, stats, and non-claim boundaries for a future creator ledger.
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_video_capture_surface_findings_v0.md
  - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - .agents/workflow-overlay/artifact-folders.md
input_hashes:
  - path: docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json
    sha256: abc788fa4e6dde0d5aa189166e7176d109c0a0c82fcf29462e31c621a2ca026b
    size: 64190
  - path: docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json
    sha256: e1d74fe107d0ad416becb7df19cd115364ab69c46c7a3c66ed08a4b182837d0a
    size: 791926
branch_or_commit: codex/youtube-shorts-tone-viability-prompt @ 36b32cfa61b421dd32f4994b78c47379bfbae843; amended after owner clarification on same branch
stale_if:
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json changes.
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json changes.
  - .agents/workflow-overlay/artifact-folders.md changes accepted folder rules for docs/review-inputs, docs/workflows, or orca/product/.
  - .agents/workflow-overlay/artifact-roles.md changes review-input or workflow-record role bindings.
  - Data Lake core/storage or Capture source-family attachment boundaries change.
authority_boundary: retrieval_only
```

## Source-Loading Surface

Purpose: record the corrected placement path for a creator ledger that is intended to become real infrastructure: a ledger of creators under a niche or sub-niche, with important observed stats and source-backed residuals.

Owner clarification, 2026-06-27: this is not a one-off workflow routing helper. The durable target is creator-ledger infrastructure for niche/sub-niche coverage and creator stats. That premise supersedes the earlier lower-lock-in recommendation that treated `docs/workflows/` as the likely durable index home.

Do not use for: creator identity verification, cross-platform identity linking, creator quality ranking, buyer proof, energy/prosody claims, runtime capture, crawler design, or transcript storage.

Authority boundary: this is a workflow recommendation and routing record. `AGENTS.md` and `.agents/workflow-overlay/` control Orca project rules. The source JSON artifacts control observed pool and ledger facts. Product-spine contracts must own recurring infrastructure before runtime implementation or stronger source-of-truth claims.

Recheck recipe: re-hash the two JSON inputs in the retrieval header, re-run the count assertions in "Verified Inputs", and re-read Capture/Data Lake boundary sources before promoting, implementing, or materially changing this route.

Non-claims: not approval, not validation, not readiness, not source-of-truth promotion, not identity verification, not implementation authorization, not buyer proof.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 target deepening
  edit_permission: docs-write
  target_scope: docs-only workflow record for creator-ledger infrastructure placement and schema boundaries
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md; overlay README/source-of-truth/source-loading/artifact-folders/artifact-roles/retrieval-metadata; creator ledger md/json; expansion200 capture md/json; Capture/Data Lake boundary sources
```

## Verified Inputs

| Source | Fresh observations used here |
| --- | --- |
| `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json` | `ledger_policy.identity_posture` is "observed YouTube channel/handle evidence only"; counts are `pool_rows_total=200`, `creators_observed=31`, `creator_or_channel_observed=30`, `brand_or_platform_accounts_observed=1`; `admitted_rows_total` across creator entries sums to 200. |
| `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.md` | The human summary states the ledger records observed handles/channels, not identity verification, ranking, row relevance certification, or independent-creator proof. |
| `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json` | Counts are `prior_admitted_total=100`, `new_admitted=100`, `cumulative_admitted_total=200`, `attempts=152`; the cumulative pool has 200 objects and 200 unique video IDs. |
| `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.md` | The pool is admitted as a 200-Short capture expansion, not a labeled benchmark; transcript bodies remain outside the repo; the companion creator ledger is observed handle/channel evidence only. |
| `docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md` | Energy, pace, volume, and prosody are excluded from transcript-only labels; stable coarse tone fields are not creator-index fields. |
| `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_video_capture_surface_findings_v0.md` | YouTube creator/channel surfaces expose channel identity and recent stats from public surfaces; this is recon-grade, not packet-grade or build authorization. |
| `orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md` | New tenant/source-family typed payloads target packet/slice-keyed extension envelopes; source-family satellites own platform-specific payload schema and meaning. |
| `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md` | Data Lake owns raw packet preservation, stable by-key findability, source-payload Attachment Record rules, and logical append-only downstream result attachment; it must not own canonical creator identity, domain ontology, or downstream orchestration. |
| `.agents/workflow-overlay/artifact-folders.md` and `.agents/workflow-overlay/artifact-roles.md` | `docs/review-inputs/` is the accepted home for prepared review inputs; `docs/workflows/` is the accepted home for workflow records; `orca/product/` is the product tree for product/capture/data-lake contracts. |

## Corrected Decision

The durable creator ledger is infrastructure. The final recurring owner should not be a generic workflow index. Use this split:

1. **Scanning owns discovery and candidate frontier.** It finds which creators/channels may matter for a niche/sub-niche and emits bounded candidate or capture-request surfaces. It does not own captured stats or persistent creator rows.
2. **Capture owns the creator-observation contract.** The Capture source-family layer should define what must be preserved for a YouTube/social creator observation: platform keys, handle/display name, channel ID when available, observed stats, niche/sub-niche basis, capture time/window, source URLs, packet refs, residuals, and identity boundary.
3. **Data Lake owns raw storage and keyed attachment.** It stores raw packets and creator-observation Attachment Records by packet/slice/source-family keys. It should not decide creator identity, niche semantics, ranking, or creator quality.
4. **Projection owns the queryable ledger view.** A later projection can materialize "all creators under niche/sub-niche with important stats" from raw packets plus creator-observation attachment records and versioned niche/stat registries. That view is rebuildable, not source truth.
5. **`docs/workflows/` owns only the transition record.** This file can route the next architecture move, but it is not the durable infrastructure home.

Hard rule: do not make creator or handle the Data Lake placement key. Handles are mutable, channel IDs can be missing in prior fixtures, and creator identity is not verified. Lake placement should stay stable-keyed by source family, packet/slice/file refs, hashes, and attachment records. Creator becomes an observed payload and projected query view, not the lake root.

## Placement Comparison

| Placement | Fit | Cost / risk | Recommendation |
| --- | --- | --- | --- |
| `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.*` | Correct for the 200-row fragrance pool evidence ledger. | Corpus-specific; cannot be the universal creator infrastructure. | Keep as source evidence only. |
| `docs/workflows/` | Good for this decision path and interim routing while the infrastructure contract is being authored. | Too weak as final home for recurring creator ledger infrastructure. | Keep this record here, but do not make the future creator ledger a workflow-only artifact. |
| Capture source-family spine under `orca/product/spines/capture/core/source_families/social_media/...` | Best owner for creator-observation capture contract, source-family field semantics, metric posture, source access, and packet attachment requirements. | Higher governance burden than workflow docs; requires a real product architecture contract before implementation. | Primary recommended next durable home for the infrastructure contract. Start YouTube/social first, generalize only after another platform proves the shared fields. |
| Data Lake spine under `orca/product/spines/data_lake/` | Owns raw packet preservation, keyed findability, Attachment Records, and storage/physicalization boundaries. | Wrong owner for creator semantics, identity, niche taxonomy, or ledger ranking. A Data Lake-first creator table would overfit storage around unstable identity. | Use for storage/attachment contract updates only after the Capture contract defines the creator-observation payload. Do not make Data Lake the semantic owner. |
| Scanning spine under `orca/product/spines/scanning/` | Owns niche/sub-niche discovery, candidate route, frontier, and capture-request generation. | Not the place to preserve captured stats or raw evidence. | Use for creator discovery and candidate frontier, not as the ledger store. |
| Domain satellite, e.g. fragrance | Can own niche/sub-niche taxonomy, domain-specific inclusion criteria, and domain-specific stat relevance. | Domain-specific; should not become social creator infrastructure core. | Use for fragrance-specific taxonomy and downstream interpretation, not for shared creator-ledger mechanics. |
| Projection / projected view contract | Best fit for queryable "all creators under X niche/sub-niche with stats" views derived from raw packet keys. | Must stay rebuildable and non-authoritative; needs capture and lake inputs first. | Define after the Capture creator-observation contract. |

## Field Contract Direction

Minimum field inclusion test: every field must support discovery, joining, provenance, lifecycle, residual visibility, or stats interpretation. Exclude fields whose main purpose is creator quality ranking, inferred identity, buyer proof, or engagement prediction without a source-backed metric contract.

A future Capture creator-observation contract should define at least:

| Field group | Purpose | Boundary |
| --- | --- | --- |
| Stable observed subject key | Platform, platform subject key type, platform subject key, channel ID or equivalent when available. | Prefer stable platform IDs over handles; never a verified person ID. |
| Mutable visible labels | Handle, display name, channel title, observed URL, observed-at timestamp. | Mutable labels are observations, not identity truth. |
| Niche/sub-niche membership | Niche ID, sub-niche ID, assignment source, assignment basis, assignment time/window, residuals. | Membership is routing/classification posture, not proof of creator identity or quality. |
| Observed stats | Metric name, value, unit, posture, source surface, capture time/window, metric registry version. | Absence/hidden/blocked/not-attempted must not be stored as observed zero. |
| Source refs | Packet ID, slice ID, video IDs, source URLs, preserved file refs, hashes. | No transcript bodies in the ledger/index. |
| Lifecycle and policies | Source hashes, schema version, identity/conflict policy version, metric registry version, supersession/stale rules. | Required before recurring capture or projection. |
| Non-claims and residuals | Identity not verified, brand/platform accounts, unknown channel IDs, off-topic/abstain residuals, low-evidence flags. | Residuals travel with rows; they are not smoothed into clean creator truth. |

The current pool-specific creator ledger can seed the first evidence set. It should not be treated as the recurring schema itself.

## Lifecycle Boundary

- Author a Capture source-family creator-observation infrastructure contract before creating runtime capture or a permanent cross-lane creator ledger table.
- Use the current 200-row fragrance creator ledger as evidence input to that contract, not as the canonical infrastructure surface.
- After the Capture contract is accepted, decide Data Lake attachment representation: manifest child, immutable sidecar, or another hash-pinned Attachment Record form.
- After Data Lake attachment is decided, define a rebuildable projection view for niche/sub-niche creator lookup and stat queries.
- Do not promote creator identity, niche membership, or creator ranking into Data Lake core.
- Do not build scheduler/crawler/runtime capture from this decision-path artifact.

## Next Authorized Actions

- Patch complete: this record now reflects the owner-stated premise that creator ledger is real infrastructure.
- Next architecture artifact: author a Capture source-family creator-observation contract, likely under `orca/product/spines/capture/core/source_families/social_media/youtube/` for the YouTube-first version, or a sibling `social_media/` contract if the owner wants platform-shared infrastructure from the start.
- After that contract: author the Data Lake attachment/physicalization decision for creator-observation records.
- After that: author the projection/view contract for the queryable creator ledger by niche/sub-niche and observed stats.
