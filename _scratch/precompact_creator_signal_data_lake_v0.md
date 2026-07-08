# Pre-Compact Checkpoint

## Current objective

Define the low-regret Orca data-lake / Creator Signal read-model shape: raw lake remains packet-addressed, while buyer-facing Creator Signal shows selected Bronze evidence, Silver mechanical derived facts, and Pre-gold movement candidates without leaking Judgment meaning into storage.

## Current state

- What has been completed:
  - Loaded Orca overlay entrypoint and deep-thinking skill earlier in this turn.
  - Read Data Lake authority and workflow sources enough to bind the architecture:
    - `orca/product/spines/data_lake/README.md`
    - `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
    - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
    - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md`
    - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
    - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
    - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
    - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md`
  - Read current Silver implementation surfaces:
    - `orca-harness/source_capture/ig_projection.py`
    - `orca-harness/source_capture/ig_reels_grid_projection.py`
    - `orca-harness/ecr/models.py`
    - `orca-harness/ecr/deriver.py`
    - `orca-harness/ecr/lake.py`
    - `orca-harness/signal_content/models.py`
    - `orca-harness/signal_content/deriver.py`
    - `orca-harness/signal_content/lake.py`
    - `orca-harness/cleaning/models.py`
    - `orca-harness/cleaning/projection.py`
    - `orca-harness/cleaning/core.py`
  - Read current IG creator/capture context:
    - `orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_momentum_pipeline_architecture_v0.md`
    - `orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md`
    - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md`
    - `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md`
    - `docs/workflows/ig_reels_projection_to_ecr_consumption_handoff_v0.md`
    - `docs/workflows/ig_reels_projection_to_ecr_consumption_decision_v0.md`
- What is partially completed:
  - Conceptual decision is clear: Creator Signal should present Bronze + Silver + Pre-gold together, but only as a derived read model.
  - No durable CreatorSignalView contract has been authored yet.
  - No implementation changes have been made in this precompact turn.
- What is currently broken or uncertain:
  - Working tree is dirty on `codex/ig-reels-capture-spine`; do not assume clean state.
  - `orca-harness/source_capture/ig_reels_grid_projection.py` and its test are modified in the worktree and should be reread before any strict code claim.
  - The exact physical/read-model home for CreatorSignalView is not yet chosen; likely a new contract under data_lake authority/workflows or a capture/signal-facing workflow doc, but this needs a small placement decision.

## Important files and symbols

- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md`
  - Relevant functions/classes/components: Raw admission/key grammar contract.
  - Current role in the task: Controls why raw lake must not be `creator/<socials>/<stats>`.
  - Important changes or observations: Raw path is locked at `raw/<packet_id>/`; lake keys are addressing handles, not creator/entity identities; semantic object/event identity and cross-packet dedupe are out of scope/deferred.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
  - Relevant functions/classes/components: Core Lake owns / Lake must not own / Projection boundary.
  - Current role in the task: Controls raw-vs-derived boundary.
  - Important changes or observations: Lake preserves raw packets and by-key findability; it must not own canonical creator identity, dedupe, Cleaning transforms, or Judgment meaning.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
  - Relevant functions/classes/components: Bronze/Silver/Pre-gold/Gold-ready/Gold map.
  - Current role in the task: Controls how to show Pre-gold without overclaiming.
  - Important changes or observations: Bronze = raw packets/attachments; Silver = projection/ECR/SCR/Cleaning/mechanical derived features; Pre-gold = mechanical candidate records such as Spike Alert / Movement Alert; Gold stays Judgment-owned.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
  - Relevant functions/classes/components: `derived/<raw-anchor>/<lane-namespace>/<record-id>`, `indexes/derived_retrieval/`.
  - Current role in the task: Controls where Creator Signal can live without new raw structure.
  - Important changes or observations: Cross-object, cross-time, aggregate, and on-demand analysis should live as rebuildable derived_retrieval views or assembly receipts referencing raw + derived refs, not as new lake authority.
- `orca-harness/source_capture/ig_projection.py`
  - Relevant functions/classes/components: `IgCreatorMomentumProjectionPacket`, `IgCreatorMomentumProjectionRow`, `project_ig_creator_momentum_into_lake`, `PROJECTION_IG_LANE`.
  - Current role in the task: Existing IG Silver lane for creator momentum.
  - Important changes or observations: Writes append-only derived record at `derived/<packet_id>/projection_ig/<record>.json`; row carries raw refs/anchors, metric posture/value, entity namespace/id, username, content shortcode/url, source-visible fields, residuals. It is view-only, not cleaned or Judgment-ready.
- `orca-harness/source_capture/ig_reels_grid_projection.py`
  - Relevant functions/classes/components: `IgReelsGridProjectionPacket`, `IgReelsGridProjectionRow`, `source_surface_count_candidates`, `chosen_source_surface`, `join_status`.
  - Current role in the task: Existing IG reels-grid Silver projection; preserves cross-surface disagreement.
  - Important changes or observations: Modified in worktree. Reread before strict claims. It reconnects selected metric observations with raw capture-file surface candidates; this is valuable silver material for Creator Signal.
- `orca-harness/ecr/lake.py`
  - Relevant functions/classes/components: `derive_ecr_into_lake`, `ECR_LANES`, `ECR_COMPLETION_LANE`.
  - Current role in the task: ECR Silver integrity records.
  - Important changes or observations: Loads raw by packet id and writes four sibling ECR records as an all-or-nothing set under `derived/<packet_id>/ecr_<kind>/<record>.json`; no projection field merge.
- `orca-harness/signal_content/`
  - Relevant functions/classes/components: `SignalContentRecord`, `derive_signal_content`, `derive_signal_content_into_lake`.
  - Current role in the task: Existing SCR/Silver-ish content model, but dormant/not default.
  - Important changes or observations: Model + residual deriver + lake persistence exist, but do not revive as default route unless explicitly authorized.
- `orca-harness/cleaning/`
  - Relevant functions/classes/components: `CleaningInputHandle`, `CleaningPacket`, `cleaning_input_handles_from_projection_rows`, `derive_exact_identity_duplicate_groups`.
  - Current role in the task: Mechanical Silver normalization/ledger layer.
  - Important changes or observations: Good for raw-keyed handles, exact raw-anchor dedupe, normalized strings/domains; not for creator identity resolution or Judgment meaning.
- `docs/workflows/ig_reels_projection_to_ecr_consumption_decision_v0.md`
  - Relevant functions/classes/components: Keys-vs-handle ECR consumption decision.
  - Current role in the task: Important boundary precedent.
  - Important changes or observations: Decision recorded Option 1: packet_id/slice_id keys suffice; no projection row reference added to ECR; no projection fields merged into ECR.

## Decisions made

- Decision: Show Bronze + Silver + Pre-gold together in the Creator Signal product surface.
  - Reason: Bronze gives inspectable source truth (actual likes/counts/links/raw mechanical evidence), Silver gives legible mechanical rows and integrity/cleaning refs, and Pre-gold gives buyer-visible value by surfacing movements/candidates.
  - Consequence: Creator Signal View should be a composed derived read model, not a raw lake reorganization.
- Decision: Raw lake must not be reorganized as `creator/<socials>/<stats>`.
  - Reason: Current raw admission and core contracts forbid creator/entity identity as raw address; raw path is packet-depth only.
  - Consequence: Use `raw/<packet_id>/` for truth and `derived/` or `indexes/derived_retrieval/` for the presentable view.
- Decision: Pre-gold should be shown as mechanical attention evidence, not interpreted truth.
  - Reason: Medallion contract says Pre-gold can include Movement/Spike candidates but not credibility, virality, manipulation, demand support, or action meaning.
  - Consequence: Product labels should be `Movement Alert`, `Spike Alert`, `Follower Jump Candidate`, `Content Velocity Candidate`, `Bio Link Change Candidate`, not `viral`, `credible`, `demand signal`, or `creator score`.
- Decision: ECR stays integrity-side and should not absorb creator presentation fields.
  - Reason: ECR consumption decision already concluded packet/slice keys suffice; projection and ECR are keyed siblings over raw.
  - Consequence: CreatorSignalView may display ECR refs/statuses but should not ask ECR to copy projection fields.

## Superseded / Ignore

- Prior instruction, idea, artifact, or finding: "Arrange the lake under creator, link socials, then stats."
  - Why superseded: Good presentation shape but bad raw storage shape; would smuggle mutable creator identity into raw lake.
  - Current replacement: Derived CreatorSignalView assembled from raw + projection + ECR + cleaning + Pre-gold candidate refs.
- Prior instruction, idea, artifact, or finding: "Only show silver data."
  - Why superseded: Too weak for buyer value and hides inspectability.
  - Current replacement: Show selected Bronze evidence plus Silver mechanical rows plus Pre-gold candidates, each with refs/residuals/non-claims.
- Prior instruction, idea, artifact, or finding: "Pre-gold means Judgment-like insight."
  - Why superseded: Medallion contract forbids that; Gold stays Judgment-owned.
  - Current replacement: Pre-gold means mechanical candidate records with declared profile/version/window/baseline/threshold and explicit non-claims.
- Prior instruction, idea, artifact, or finding: "SCR should consume IG projection by default."
  - Why superseded: Current ECR handoff/decision says SCR is deprecated/dormant as default; do not revive without explicit authorization.
  - Current replacement: Default route is evidence/read-model assembly; SCR only if explicitly revived for a named need.

## Commands and results

- Command:
  ```bash
  rg --files -g '!_scratch/**' -g '!worktrees/**' | rg "projection|ecr|signal_content|cleaning|silver|lake_pilot|ig_reels_grid_projection|ig_projection|data_lake"
  ```
  Result:
  - Passed/failed/not run: ran.
  - Important output: Found current projection/ECR/signal_content/cleaning/data_lake implementation surfaces and tests.
- Command:
  ```bash
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: ran before precompact.
  - Important output: `## codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine [gone]`; modified `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md`, `orca-harness/source_capture/ig_reels_grid_projection.py`, `orca-harness/tests/unit/test_source_capture_ig_reels_projection.py`; many untracked files including `_scratch/`, several docs/workflows/hygiene files; warning opening `orca-harness/.pytest_tmp/`.
- Command:
  ```bash
  git rev-parse --short HEAD
  ```
  Result:
  - Passed/failed/not run: ran before precompact.
  - Important output: `056ef74b`.
- Command:
  ```bash
  python -m pytest ...
  ```
  Result:
  - Passed/failed/not run: not run in this conceptual/precompact step.
  - Important output: None. Do not claim validation.

## Known issues and risks

- Issue: Creator Signal read model could accidentally become a second source of truth.
  - Evidence: User wants presentable creator/social/stat organization; raw lake contracts forbid semantic identity in raw path.
  - Likely next action: Contractually mark CreatorSignalView as rebuildable/read-only from raw + derived refs, not authoritative storage.
- Issue: Pre-gold labels could overclaim.
  - Evidence: Medallion contract forbids Pre-gold from implying viral/suspicious/paid/credible/demand-supporting.
  - Likely next action: Use strict labels and non-claims; require profile/version/window/baseline/threshold/raw refs/residuals on each candidate.
- Issue: Current Silver is split and not yet buyer-presentable.
  - Evidence: Projection/ECR/SCR/Cleaning exist as separate implementation surfaces; no `CreatorSignalView` contract exists.
  - Likely next action: Author a narrow CreatorSignalView contract/spec as the first durable artifact.
- Issue: Dirty worktree and modified IG projection files.
  - Evidence: `git status --short --branch`.
  - Likely next action: Before edits, decide isolation and reread modified files; do not stage unrelated user/other-lane changes.

## Constraints and user preferences

- Constraint/preference: Push back hard when an idea is structurally wrong.
  - Source or reason: User AGENTS instruction.
- Constraint/preference: Smallest complete intervention; no speculative broad migration.
  - Source or reason: AGENTS.md.
- Constraint/preference: Show product value, not just internal lake neatness.
  - Source or reason: User said showing Pre-gold gives more value and asked to include Bronze actual likes/mechanical facts.
- Constraint/preference: Derived read model is accepted direction.
  - Source or reason: User: "derived read makes sense."
- Constraint/preference: Default allowed work is docs/decisions/prompts/reviews/migration/overlay; runtime work requires explicit bounded authorization.
  - Source or reason: AGENTS.md.

## Next steps

1. Answer the user directly: yes, Creator Signal should display selected Bronze, Silver, and Pre-gold together, with clear layer labels and non-claims.
2. If continuing after compact, propose/author the smallest durable `CreatorSignalView v0` contract that defines fields, sources, layer labels, rebuildability, and forbidden claims.
3. Validation step for doc-only contract: `git diff --check`; if touching repo-map/headers, run relevant map/header checks. If later code is changed, rerun focused projection/ECR/cleaning tests.

## Do not forget

- Bronze in the UI means selected raw/mechanical source-visible evidence, not the whole raw packet dump.
- Silver means projection/ECR/cleaning mechanical records, not Judgment.
- Pre-gold means candidate movement/attention records, not viral/credible/demand/action meaning.
- Keep raw lake packet-keyed; Creator Signal is a derived read/view assembled by refs.
