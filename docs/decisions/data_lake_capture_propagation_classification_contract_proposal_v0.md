# Data Lake Capture Propagation Classification Contract Proposal v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision proposal
scope: >
  Prepare-only proposal for a narrow Data Lake / Capture propagation
  classification contract: which changes propagate as generic lake/storage or
  packet-runner checks, which propagate as platform behavioral parity checks,
  and which stay source-family-local.
use_when:
  - Deciding whether a Data Lake, capture runner, YouTube, Instagram, TikTok, or downstream residual change requires same-class checks elsewhere.
  - Selecting the controlling home before patching propagation doctrine.
  - Preventing platform-specific acquisition routes from becoming generic Data Lake doctrine.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
  - orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
  - orca-harness/youtube_capture/behavioral_projection.py
  - orca-harness/source_capture/ig_reels_behavioral_projection.py
  - orca-harness/source_capture/ig_reels_grid_projection.py
stale_if:
  - Data Lake raw/derived/medallion semantics change.
  - SourceCapturePacket runner lake-seam enforcement changes.
  - YouTube, Instagram, TikTok, or another social capture behavioral projection contract changes.
  - A later accepted propagation contract or decision supersedes this proposal.
authority_boundary: retrieval_only
```

## Status

`PROPOSAL_READY_FOR_OWNER_STEERING_V0`.

This is a prepare-only proposal and classification artifact. It does not edit
the controlling Data Lake, Capture, projection, ECR, Cleaning, Judgment, overlay,
or harness authority files. It is not accepted doctrine, validation, readiness,
implementation authorization, source-access authorization, runtime authority, or
proof that any platform lane is complete.

Because this artifact classifies and recommends a future controlling home without
changing that home, no `direction_change_propagation` receipt is owed by this
proposal. If the owner accepts the proposal and a later patch edits controlling
source, that patch must carry the relevant `direction_change_propagation` receipt
or blocker.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 Data Lake / Capture propagation
  edit_permission: docs-write
  target_scope:
    - docs/decisions/data_lake_capture_propagation_classification_contract_proposal_v0.md
    - docs/workflows/orca_repo_map_v0.md
  dirty_state_checked: yes
  isolation: worktree branch codex/data-lake-capture-propagation-proposal from origin/main at 32e2d888f07ce345abadd521dca0dff9db93e264
  blocked_if_missing: owner acceptance before patching controlling doctrine
```

## Recommendation

Create the future accepted rule as a narrow Data Lake / Capture propagation
classification contract, not as broad overlay workflow doctrine and not as a
platform acquisition rule.

Recommended future controlling home:

`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md`

That home fits because the classification is about product architecture at the
lake/capture boundary: raw packet preservation, lake seams, derived records,
behavioral projection parity, and downstream residual semantics. Like the Data
Lake medallion contract (which maps Silver/Gold epistemic boundaries across the
projection, ECR/SCR, Cleaning, and Judgment lanes without owning them), this
contract classifies and routes propagation to each owning lane; it does not
transfer behavioral-projection, acquisition-route, ECR, Cleaning, or Judgment
ownership into Data Lake. The Orca overlay should only be edited if the owner
wants to change agent workflow behavior, gate behavior, or source-loading
mechanics. The current problem is narrower than that.

## Architecture Planning Triage

Full `workflow-architecture-planning` is not required before this proposal. The
smallest complete architecture move is the classification below.

Run a full architecture-planning lane only if the owner chooses one of these
broader paths:

- make this an overlay-wide propagation doctrine for all agents and all lanes;
- introduce a cross-source behavioral record ontology beyond the current
  projection parity checks;
- add physical Data Lake write/storage boundaries or runtime behavior;
- force platform acquisition route convergence across YouTube, Instagram, TikTok,
  or future source families.

## Mini God Tier Fit

This structure is Mini God Tier compatible. It names the residuals, keeps the
scope small, and prevents a narrow discovery from becoming a universal claim.

It is not a Mini God Tier achievement claim. It asserts no validation, readiness,
platform coverage, or implementation completeness.

Accepted residuals in this proposal (per
`docs/decisions/forseti_mini_god_tier_doctrine_v0.md`, each names what is foregone,
why it is acceptable now, the remaining risk, and the upgrade trigger):

- **No universal output/seam rule for non-packet runners.** Foregone: a single
  lake-routing rule covering every runner. Acceptable now: only raw
  `SourceCapturePacket` producers carry raw lake truth, and the seam coverage
  test already scopes to them; offline projections, materializers, and
  audit/report runners write no raw truth. Risk: a future non-packet runner that
  should route into the lake is not caught by the packet-producer seam. Upgrade
  trigger: a non-packet entrypoint needs lake routing, scoping its own seam
  rather than widening this bucket.
- **No forced acquisition-route uniformity across YouTube, Instagram, TikTok, or
  future source families.** Foregone: a shared cross-platform acquisition
  primitive now. Acceptable now: acquisition routes are platform-specific
  (YouTube caption/watch/ASR vs Instagram grid/audio/deep-capture) and forcing
  uniformity would copy non-transferable mechanics. Risk: a genuine
  platform-independent primitive stays source-family-local longer than strictly
  necessary. Upgrade trigger: two non-overlapping source families prove the same
  primitive and the owner accepts promotion (see the source-family-local bucket).
- **No enforced behavioral-parity guarantee for every platform.** Foregone: a
  hard cross-platform projection-parity invariant. Acceptable now: parity is a
  review obligation over shared projection shape, and only the YouTube and
  Instagram behavioral projections exist today. Risk: a new platform's projection
  could drift from the shared shape without a gate catching it. Upgrade trigger:
  the owner authorizes an enforced cross-source projection-parity check (the
  cross-source behavioral-record ontology path named in Architecture Planning
  Triage).

Preserved hard boundaries (correctness/process limits, not Pareto give-ups, so
they carry no upgrade trigger): Gold/Judgment interpretation stays in
Judgment-owned sources and never enters this lane; and this proposal patches no
controlling source until the owner accepts the controlling home (the prepare-only
process gate in Status).

## Before / After

Before this proposal:

- propagation decisions were implicit and ad hoc after Data Lake, runner,
  platform, or residual changes;
- a packet-runner lake seam could be mistaken for a rule about every runner;
- YouTube and Instagram behavioral projection similarities could be mistaken for
  shared acquisition machinery;
- Data Lake medallion boundaries, projection doctrine, ECR residual discipline,
  and platform-specific capture code had to be reconciled manually each time.

After the proposed contract is accepted and patched:

- changes classify into one of five propagation buckets before implementation;
- raw packet-runner seam changes check all raw `SourceCapturePacket` producers,
  but not unrelated runners;
- platform behavior changes trigger parity review for behavioral projections,
  not route-copying of platform acquisition machinery;
- acquisition-route discoveries remain source-family-local unless the owner
  separately promotes a platform-independent primitive;
- downstream consumer changes preserve residual/completeness visibility and the
  Gold/Judgment boundary.

## Proposed Classification Contract

| Change class | Propagation class | Required same-class check | Explicit non-propagation |
| --- | --- | --- | --- |
| Data Lake raw, by-key, derived, or medallion semantics | Generic Data Lake / downstream boundary propagation | Check Data Lake core, medallion, Silver Vault, projection doctrine, ECR submap, and Data/Cleaning boundary for raw preservation, append-only derived records, residual visibility, and Gold leakage. | Do not infer platform capture routes, Cleaning transforms, Judgment outputs, or runtime readiness from lake storage semantics. |
| Raw `SourceCapturePacket` runner output seam | Generic packet-runner lake-seam propagation | Check raw packet-producing capture runners and `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` for `--data-root`, `ORCA_DATA_ROOT` fallback only when output is omitted, `DataLakeRoot.resolve`, exclusive local/lake output modes, and `data_root=` forwarding into packet writers. | Do not apply this to every runner. Offline projections, materializers, smoke/audit runners, report builders, and other non-packet entrypoints are not covered by this seam merely because they live in `orca-harness/runners/`. |
| Platform behavioral projection shape | Platform behavioral parity check | Check source-family behavioral projections for projection-only/no-acquisition boundary, platform object key, canonical source selection, transcript source rollup, extraction/completeness status, residual naming, persistence/correlation anchors, and metric posture/count-candidate visibility where applicable. | Do not copy YouTube caption/watch/youtubei/ASR route mechanics into Instagram/TikTok, or copy Instagram grid/audio/deep-capture mechanics into YouTube/TikTok. |
| Platform acquisition route or source-surface discovery | Source-family-local | Keep the route in the owning source-family Capture lane and its runner/source docs. Promote only if two non-overlapping source families prove the same platform-independent primitive and the owner accepts promotion. | Do not generalize YouTube watch metadata, captions, `youtubei`, or ASR fallback into IG/TikTok. Do not generalize Instagram reels grid DOM/passive JSON, standalone audio, deep-capture render, source-surface disagreement, or static-post view-count handling into YouTube/TikTok. |
| Downstream consumer residual/completeness semantics | Downstream boundary propagation | Check projection doctrine, ECR, Cleaning boundary, Data Lake medallion, and any consumer read model for named residuals, missingness/posture visibility, raw-pull flags, raw/derived refs, and Gold/Judgment containment. | Do not convert residuals into prose-only warnings, success booleans, priority signals, hidden filters, or Judgment-like labels outside Judgment. |

## Controlling-Home Patch Shape If Accepted

If the owner accepts the recommendation, the next patch should:

1. Add the narrow accepted contract under Data Lake authority, or an
   owner-selected equivalent home.
2. Add retrieval/map pointers from the Data Lake authority index/README or
   mechanics map, the Data Capture submap, and this repo map.
3. Add a `direction_change_propagation` receipt in the controlling source patch.
4. Keep platform acquisition examples illustrative and source-family-local.
5. Avoid adding implementation, storage, scheduler, dashboard, crawler, API,
   live capture, or validation/readiness claims.

## Owner Decision Needed

Choose one:

1. Accept the narrow Data Lake / Capture contract home and authorize a follow-up
   source patch.
2. Keep this as a non-binding proposal and continue handling propagation
   manually.
3. Escalate to broad overlay/workflow doctrine. This should trigger explicit
   architecture planning first because it changes agent workflow authority, not
   only Data Lake / Capture product architecture.

## Source Basis Ledger

Fresh-read base: `origin/main` at
`32e2d888f07ce345abadd521dca0dff9db93e264`.

Load-bearing source blobs read or checked for this proposal:

| Source | Blob checked from `origin/main` |
| --- | --- |
| `.agents/workflow-overlay/artifact-folders.md` | `2725131a3b7381838b902d4e8b6e0f1228d14c1e` |
| `.agents/workflow-overlay/retrieval-metadata.md` | `f675c5dd9357d4c53000ff8beb040839b3e06343` |
| `.agents/workflow-overlay/source-loading.md` | `6b02b3487ff27147e357df01470d31308fa5da12` |
| `.agents/workflow-overlay/source-of-truth.md` | `fd42a38eb206327ff474fa83a2a5c90165c12a59` |
| `.agents/workflow-overlay/validation-gates.md` | `890b5afa04308ae0e610dfb750afaf0d0ad87114` |
| `.agents/workflow-overlay/safety-rules.md` | `541c073bb96247387f13d5e3d1aa01793148ee17` |
| `docs/workflows/orca_repo_map_v0.md` | `aeec2ab32aff1d5b8b2c56765f94830533835987` |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | `34f8347b611715a0a9318e71d1c89e1b2a2d3ab3` |
| `docs/workflows/ecr_spine_submap_v0.md` | `66cb77c7db59ec90a2b18159e24e09799eeb555f` |
| `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md` | `e33cdab1bf37693775730e712c3562999690230d` |
| `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md` | `a3f60ee173961f58dc49740611ce54c213222787` |
| `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` | `6551b3d675a80d821173497a84bf8319e2c1418f` |
| `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | `914a56ada24c37bb5fca5f33280d0cde22d1a37a` |
| `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` | `3733e05d8a75ac599c75a485eefa758ac49efa03` |
| `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` | `a16fe86583c821ba23af952648df1b00a440fe99` |
| `orca-harness/youtube_capture/behavioral_projection.py` | `349549f945d22a3d4686bc6b477c32c0a52ab2b5` |
| `orca-harness/source_capture/ig_reels_behavioral_projection.py` | `5f08c6202616408816d548087c7112c43ec9ac32` |
| `orca-harness/source_capture/ig_reels_grid_projection.py` | `c113a7d33b06650e7bb57539225a0d990262f11d` |
| `orca-harness/source_capture/ig_reels_behavioral_lake.py` | `d8dac1a3f5bfcade3d087cc0c2da02b491497e81` |

Key checked observations:

- Data Lake core owns raw packet preservation, stable by-key findability, passive
  availability, and append-only downstream attachment while excluding Cleaning,
  ECR/SCR interpretation, Judgment, orchestration, queue authority, and physical
  runtime claims.
- Data Lake medallion semantics keep Gold interpretation in Judgment. Bronze,
  Silver, Pre-gold, and Gold-ready remain epistemic boundaries, not mere storage
  convenience labels.
- Silver Vault records are append-only derived records keyed to raw anchors,
  with posture/value coupling, raw refs, derived refs, metric missingness, and no
  Gold/Judgment output.
- Projection doctrine allows core promotion for obvious invariants, and for a
  family-specific rule only once it survives at least two non-overlapping source
  families or the owner explicitly accepts it as core; and it forbids projection
  from emitting interpretation.
- The packet-runner lake-seam test is scoped to runners that write
  `SourceCapturePacket` material and enforces data-root forwarding plus exclusive
  output modes.
- YouTube and Instagram behavioral projections both project already-captured
  surfaces and expose extraction/completeness residuals, but each explicitly does
  not acquire data and does not claim shared capture machinery.
