# Core Spine v0 Data Lake Capture Propagation Classification Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Accepted Data Lake / Capture propagation classification contract: which
  source-changing changes propagate as generic lake/storage or packet-runner
  checks, which propagate as platform behavioral parity checks, which stay
  source-family-local, and which preserve downstream residual/gold-boundary
  visibility.
use_when:
  - Deciding whether a Data Lake, raw packet runner, YouTube, Instagram, TikTok, projection, ECR, Cleaning, or downstream consumer change requires same-class checks elsewhere.
  - Preventing packet-runner lake-seam enforcement from becoming a rule about every runner, or platform-specific acquisition routes from becoming generic Data Lake doctrine.
  - Preserving residual/completeness visibility and Judgment-owned gold semantics when lake/capture-facing surfaces change.
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
  - forseti-harness/youtube_capture/behavioral_projection.py
  - forseti-harness/source_capture/ig_reels_behavioral_projection.py
  - forseti-harness/source_capture/ig_reels_grid_projection.py
downstream_consumers:
  - Data Lake storage, raw admission, write-boundary, derived-layout, and Silver Vault lanes
  - Data Capture source-family capture/projection lanes
  - Packet-runner lake-seam test maintenance
  - ECR/SCR, Cleaning, and Judgment-bound evidence assembly lanes
stale_if:
  - Data Lake raw/derived/medallion semantics change.
  - SourceCapturePacket runner lake-seam enforcement changes.
  - YouTube, Instagram, TikTok, or another social capture behavioral projection contract changes.
  - Projection, ECR/SCR, Cleaning, or Judgment ownership changes in a later accepted source.
  - A later accepted propagation contract or owner decision supersedes this contract.
authority_boundary: retrieval_only
```

## Status

`ACCEPTED_CLASSIFICATION_CONTRACT_V0`.

This contract is product architecture doctrine at the Data Lake / Capture
boundary. It classifies propagation obligations for future source-changing
work. It does not authorize implementation, source access, runtime behavior,
storage selection, scheduler/dashboard/API work, validation, readiness, proof, or
platform completeness.

## Purpose

Data Lake and Capture changes were previously easy to over-generalize:

- a raw packet-runner seam could be mistaken for a rule about every runner;
- shared YouTube/Instagram behavioral projection shape could be mistaken for
  shared acquisition machinery;
- downstream residual/completeness changes could silently leak into Gold or
  Judgment semantics;
- Data Lake authority could be misread as owning Projection, ECR/SCR, Cleaning,
  or Judgment.

This contract fixes the classification step before a future patch changes
source. It routes propagation to the owning lane without transferring ownership
into Data Lake.

## Enforcement Model

This structure is doctrine-led and code-backed where the invariant is concrete.

1. **Doctrine layer.** A future source-changing patch that touches one of the
   change classes below must classify the change before implementation and must
   record a `direction_change_propagation` receipt or blocker when it changes
   durable doctrine.
2. **Code-backed layer.** Existing packet-runner lake-seam enforcement remains
   scoped to raw `SourceCapturePacket` producers and explicit raw-packet
   orchestrators via
   `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`.
   That test checks the concrete runner seam: `--data-root`, `FORSETI_DATA_ROOT`
   primary / legacy `ORCA_DATA_ROOT` fallback only when local output is omitted, `DataLakeRoot.resolve`,
   exclusive local/lake output modes, and `data_root=` forwarding into packet
   writers. It discovers source-capture packet writers by behavior, not name
   alone, so ASR-style writers such as `write_asr_transcript` stay covered, and
   it pins the current Bronze-writer runner surface so additions/removals are
   explicit.
3. **Review layer.** Platform behavioral parity, source-family-local promotion,
   and downstream residual/gold-boundary semantics remain source-backed review
   obligations until a later owner-authorized source makes a narrower invariant
   concrete enough to test.

Do not add a generic bucket-inference hook from this contract alone. A broad
checker would over-claim semantic judgment the current code cannot safely infer.

## Classification Procedure

Before patching a Data Lake / Capture propagation-relevant source:

1. Classify the change using the table below. If one patch spans multiple
   classes, apply every relevant same-class check.
2. Open the owner sources named by the same-class check. Do not rely on this
   contract as a substitute for the owning source.
3. Preserve the explicit non-propagation boundary. A same-class check is not
   permission to copy unrelated mechanics into another lane.
4. If the patch changes durable doctrine, record DCP evidence in the controlling
   source patch. If propagation cannot be completed, return a DCP blocker.
5. Escalate to architecture planning only when the architecture gate below is
   tripped.

## Classification Table

| Change class | Propagation class | Required same-class check | Explicit non-propagation |
| --- | --- | --- | --- |
| Data Lake raw, by-key, derived, or medallion semantics | Generic Data Lake / downstream boundary propagation | Check Data Lake core, medallion, Silver Vault, projection doctrine, ECR submap, and Data/Cleaning boundary for raw preservation, append-only derived records, residual visibility, and Gold leakage. | Do not infer platform capture routes, Cleaning transforms, Judgment outputs, or runtime readiness from lake storage semantics. |
| Raw `SourceCapturePacket` runner output seam | Generic packet-runner lake-seam propagation | Check raw packet-producing capture runners, explicit raw-packet orchestrators, and `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` for the current Bronze-writer surface, behavior-discovered source-capture packet writers, `--data-root`, `FORSETI_DATA_ROOT` primary / legacy `ORCA_DATA_ROOT` fallback only when output is omitted, `DataLakeRoot.resolve`, exclusive local/lake output modes, and `data_root=` forwarding into packet writers/sub-runners. | Do not apply this to every runner. Offline projections, materializers, smoke/audit runners, report builders, derived-only Silver writers, and other non-packet entrypoints are not covered by this seam merely because they live in `forseti-harness/runners/` or touch `--data-root`. |
| Platform behavioral projection shape | Platform behavioral parity check | Check source-family behavioral projections for projection-only/no-acquisition boundary, platform object key, canonical source selection, transcript source rollup, extraction/completeness status, residual naming, persistence/correlation anchors, and metric posture/count-candidate visibility where applicable. | Do not copy YouTube caption/watch/youtubei/ASR route mechanics into Instagram/TikTok, or copy Instagram grid/audio/deep-capture mechanics into YouTube/TikTok. |
| Platform acquisition route or source-surface discovery | Source-family-local | Keep the route in the owning source-family Capture lane and its runner/source docs. Promote only if two non-overlapping source families prove the same platform-independent primitive and the owner accepts promotion. | Do not generalize YouTube watch metadata, captions, `youtubei`, or ASR fallback into IG/TikTok. Do not generalize Instagram reels grid DOM/passive JSON, standalone audio, deep-capture render, source-surface disagreement, or static-post view-count handling into YouTube/TikTok. |
| Downstream consumer residual/completeness semantics | Downstream boundary propagation | Check projection doctrine, ECR, Cleaning boundary, Data Lake medallion, and any consumer read model for named residuals, missingness/posture visibility, raw-pull flags, raw/derived refs, and Gold/Judgment containment. | Do not convert residuals into prose-only warnings, success booleans, priority signals, hidden filters, or Judgment-like labels outside Judgment. |

## Architecture Planning Gate

Full architecture planning is not required for the classification contract above.
The smallest complete architecture move is this bounded classification.

Run a separate architecture-planning lane before patching if the owner chooses
one of these broader paths:

- make this an overlay-wide propagation doctrine for all agents and all lanes;
- introduce a cross-source behavioral record ontology beyond current projection
  parity checks;
- add physical Data Lake write/storage boundaries or runtime behavior;
- force platform acquisition route convergence across YouTube, Instagram,
  TikTok, or future source families.

## Mini God Tier Fit

The owner invoked the Mini God Tier lens for this fused turn. This contract uses
that lens only to constrain the target: most of the value is captured by a small
classification contract plus explicit residuals, not by standing runtime
infrastructure.

This is not a Mini God Tier achievement claim. It asserts no validation,
readiness, platform coverage, proof, or implementation completeness.

Accepted residuals:

- **No universal output/seam rule for non-packet runners.** Foregone: a single
  lake-routing rule covering every runner. Acceptable now: only raw
  `SourceCapturePacket` producers carry raw lake truth, and the seam coverage
  test already scopes to them. Offline projections, materializers, and
  audit/report runners write no raw truth. Remaining risk: current or future
  non-packet lake writers, such as IG Reels deep-capture records, need their own
  seam if the owner wants them enforced; they are not caught by the packet-producer
  seam. Upgrade trigger: a non-packet entrypoint needs lake routing, scoping its
  own seam rather than widening this bucket.
- **Manual raw-packet orchestrator enumeration.** Foregone: static discovery of
  every orchestrator through injected runner callables, aliases, or lane wrappers.
  Acceptable now: current lake-wired raw-packet orchestrators are explicitly
  listed in `BRONZE_PACKET_ORCHESTRATORS`, including Fragrantica MGT and the IG
  Reels lane orchestrator, and the test enforces `data_root=` forwarding into
  listed raw-packet subrunners. Remaining risk: a future orchestrator can be
  missed until manually added. Upgrade trigger: another hidden orchestrator class
  appears or the owner authorizes a stronger orchestrator discovery rule.
- **No forced acquisition-route uniformity across YouTube, Instagram, TikTok, or
  future source families.** Foregone: a shared cross-platform acquisition
  primitive now. Acceptable now: acquisition routes are platform-specific
  (YouTube caption/watch/ASR vs. Instagram grid/audio/deep-capture), and forcing
  uniformity would copy non-transferable mechanics. Remaining risk: a genuine
  platform-independent primitive stays source-family-local longer than strictly
  necessary. Upgrade trigger: two non-overlapping source families prove the same
  primitive and the owner accepts promotion.
- **No enforced behavioral-parity guarantee for every platform.** Foregone: a
  hard cross-platform projection-parity invariant. Acceptable now: parity is a
  review obligation over shared projection shape, and only the YouTube and
  Instagram behavioral projections exist today. Remaining risk: a new platform's
  projection could drift from the shared shape without a gate catching it.
  Upgrade trigger: the owner authorizes an enforced cross-source
  projection-parity check, which is the cross-source behavioral-record ontology
  path named in the Architecture Planning Gate.

Preserved hard boundaries, not accepted residuals:

- Gold/Judgment interpretation stays in Judgment-owned sources and never enters
  this lane.
- Data Lake classifies and routes propagation across owning lanes; it does not own
  behavioral projection, acquisition routes, ECR/SCR, Cleaning, or Judgment.

## Smallest Complete Intervention Boundary

The complete v0 structure is this accepted contract plus navigation pointers.
The following are intentionally out of scope:

- no runtime code, source-access, capture-runner, projection, ECR, Cleaning, or
  Judgment implementation;
- no new bucket-inference hook;
- no storage, schema, queue, scheduler, dashboard, deployment, or production
  runtime authorization;
- no broad overlay workflow doctrine;
- no platform acquisition-route convergence;
- no validation/readiness/proof claim.

## Before / After

Before this contract:

- propagation decisions were implicit and patch-local after Data Lake, runner,
  platform, or residual changes;
- the packet-runner lake seam could be mistaken for a rule about every runner;
- behavioral projection shape and acquisition machinery were easy to blur;
- residual/completeness visibility and Gold/Judgment containment had to be
  manually reconciled each time.

After this contract:

- changes classify into five buckets before implementation;
- raw packet-runner seam changes check raw `SourceCapturePacket` producers, not
  unrelated runners;
- platform behavior changes trigger parity review for behavioral projections,
  not route-copying of platform acquisition machinery;
- acquisition-route discoveries remain source-family-local unless owner-promoted
  after cross-family evidence;
- downstream consumer changes preserve named residuals, raw pull, and
  Judgment-owned Gold interpretation.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake / Capture propagation now has an accepted five-bucket
    classification contract: lake/raw/medallion semantics, packet-runner lake
    seams, platform behavioral projection shape, platform acquisition routes,
    and downstream residual/completeness semantics each route to their owning
    same-class checks, with Mini God Tier residuals and no runtime or
    overlay-wide enforcement claim.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - workflow_authority
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
    - docs/decisions/data_lake_capture_propagation_classification_contract_proposal_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/data_lake_capture_propagation_classification_delegated_adversarial_review_patch_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
    - forseti-harness/youtube_capture/behavioral_projection.py
    - forseti-harness/source_capture/ig_reels_behavioral_projection.py
    - forseti-harness/source_capture/ig_reels_grid_projection.py
  intentionally_not_updated:
    - path: docs/workflows/data_capture_spine_consolidation_map_v0.md
      reason: >
        The Data Capture submap already routes lake/capture mechanics questions
        through the Data Lake mechanics map, and this patch updates that map.
        Adding a duplicate direct row would require unrelated cleanup of the
        submap's pre-existing historical inline DCP receipts, which is outside
        the smallest complete intervention.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        No overlay read pack changes. Repo-map and Data Lake mechanics pointers
        are enough to retrieve the accepted contract.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: >
        The core contract already owns raw preservation, by-key findability, and
        lake-owned boundaries; this contract classifies propagation without
        reopening those lake duties.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: >
        The medallion contract already keeps Gold/Judgment interpretation out of
        non-Judgment layers; this contract routes downstream residual/gold-boundary
        checks to it.
    - path: forseti-harness/
      reason: >
        Existing packet-runner lake-seam tests are the only concrete code-backed
        enforcement needed for v0. Behavioral parity and residual semantics stay
        doctrine/review-backed until a later owner-authorized invariant is narrow
        enough for code.
  stale_language_search: >
    not_run: additive accepted contract and pointer patch; no prior controlling
    propagation contract language was replaced, and the historical proposal
    remains explicitly proposal-only.
  non_claims:
    - not validation
    - not readiness
    - not proof
    - not implementation authorization
    - not source-access authorization
    - not runtime authority
    - not storage selection
    - not platform completeness
```


```yaml
direction_change_propagation:
  doctrine_changed: >
    Tightens the code-backed packet-runner lake-seam enforcement description to match the live
    contract test: Bronze writer coverage now includes behavior-discovered source-capture packet
    writer functions (including ASR-style writers whose names do not end in _packet), an explicit
    current Bronze-writer runner surface, explicit raw-packet orchestrator forwarding including
    the current IG Reels lane orchestrator, and an accepted residual for manual orchestrator
    enumeration. The non-propagation boundary is unchanged: this does not become a universal rule
    for every lake-touching runner, derived-only Silver writer, audit/report runner, materializer,
    or projection entrypoint.
  trigger: validation_philosophy
  related_triggers:
    - architecture_doctrine
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md
    - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
  downstream_surfaces_checked:
    - forseti-harness/runners/run_fragrantica_mgt_capture.py
    - forseti-harness/runners/run_ig_reels_lane_orchestrator.py
    - forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py
    - forseti-harness/runners/run_source_capture_ig_reels_audio_packet.py
    - forseti-harness/runners/run_source_capture_youtube_asr_packet.py
    - forseti-harness/source_capture/transcript/asr_packet.py
    - forseti-harness/source_capture/transcript/ig_reels_audio_packet.py
    - forseti-harness/source_capture/transcript/caption_packet.py
    - forseti-harness/source_capture/youtube_watch_packet.py
  intentionally_not_updated:
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        The map already routes packet-runner lake-seam questions through this contract and the
        test path; no new source family, top-level route, or artifact home is introduced.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: >
        Raw preservation and by-key findability are unchanged. This patch tightens runner-seam
        coverage only.
  verification: >
    `python -m pytest -q forseti-harness\tests\contract\test_capture_runner_lake_seam_coverage.py`
    passed with 9 tests after the enforcement change.
  non_claims:
    - not validation of live source access
    - not proof every lake-touching runner is a Bronze writer
    - not a universal runner-output rule
    - not Silver, projection, ECR, Cleaning, or Judgment readiness
```

Older receipts, when cycled out, belong in `docs/decisions/dcp_receipts_archive_v0.md`.
