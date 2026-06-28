# YouTube Post-ECR Cleaning Adapter Architecture Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (Planning/Architecture handoff prompt)
scope: >
  Commission a fresh lane to define the post-ECR Cleaning adapter routing
  contract, starting with YouTube surfaces, so ECR remains generic while
  Cleaning routes by evidence mechanics and Extraction routes by question.
use_when:
  - Picking up the YouTube-first post-ECR Cleaning adapter architecture lane.
  - Checking whether a YouTube surface should be admitted to ECR, Cleaning, or a
    question-specific extractor.
  - Preparing the later IG or other-source rollout after the YouTube contract is
    source-visible.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md
  - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
```

## Orca Prompt Preflight

- preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.
- output_mode: `file-write`; durable handoff prompt at `docs/prompts/handoffs/youtube_post_ecr_cleaning_adapter_architecture_handoff_v0.md`.
- template_kind: `handoff`; no registered project-local handoff template is bound, so this uses the explicit `workflow-handoff` packet contract under the Orca prompt-orchestration file-write rule.
- authorization_basis: current owner instruction in this thread to hand off the YouTube-first post-ECR Cleaning routing architecture question.
- edit_permission: `docs-write`; this handoff authorizes a later docs/architecture pass only. It does not authorize runtime implementation, tests, live capture, or production deployment.
- target_files_or_dirs: likely output under `orca/product/spines/cleaning/contracts/`; read-only implementation references under `orca-harness/`.
- source_pack / bounded_reads: custom S3-style pack centered on Cleaning foundation, Data Capture/ECR/Cleaning boundary, ECR frame, YouTube transcript extraction spec, and the current YouTube ECR/Cleaning runner.
- dirty_state_allowance: receiver should start in a clean fresh branch or worktree off latest `origin/main`; do not reuse the sender's worktree.
- branch_or_commit_reference: sender filed from `codex/youtube-downstream-ecr-cleaning` at `aea51cf1` before this handoff file; receiver must refetch and re-read current sources.
- doctrine_change_decision: the receiving lane may recommend an architecture-doctrine change. If it changes Cleaning or prompt/workflow doctrine, it must update the controlling source and carry a `direction_change_propagation` receipt or blocker.
- isolation_decision: use a fresh branch or worktree off latest `origin/main` for any docs-write architecture pass; no runtime edit without a new bounded implementation handoff.
- validation_gates: docs/artifact hygiene and source-backed self-check only unless implementation is separately authorized; no code-test success may be claimed from this prompt.
- thread_operating_target_continuity: no active `thread_operating_target` was visible; not carried.

## Cynefin Routing

Smallest complete outcome: produce a source-backed post-ECR Cleaning adapter routing architecture note, YouTube-first, that separates ECR admission, Cleaning adapter admission, and Extraction admission without changing runtime code.

Regime: Complicated.

Why: the work needs layer-boundary judgment and source hierarchy, but the target can be reasoned through from the current Cleaning, ECR, and YouTube sources.

Decomposition: layer-based.

Current bottleneck: the system needs an explicit routing contract so source-family labels do not become "platform blobs" that mix transcripts, audio, post text, comments, and metadata.

Riskiest assumption: that the current YouTube runner's `youtube_comments` rejection is an ECR rule; it is not proven and should be treated as a transcript-cleaning adapter boundary until re-verified.

Stop or pivot condition: if current source shows an accepted Cleaning adapter registry or source-surface routing doctrine already exists, do not author a duplicate; patch or supersede the owning source instead.

Allowed next move: read the named sources, then author a narrow architecture note or plan for post-ECR Cleaning adapter routing.

Disallowed next move: changing ECR derivers, adding runtime adapter code, admitting comments into transcript extraction, or expanding into IG implementation before the YouTube routing contract is source-visible.

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-26
- created_by_lane: Codex lane `codex/youtube-downstream-ecr-cleaning` (provenance only; not authority)
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/prompts/handoffs/youtube_post_ecr_cleaning_adapter_architecture_handoff_v0.md`
- expected_branch: receiver creates a fresh docs/architecture lane off latest `origin/main`, or a fresh worktree if running parallel with active lanes
- expected_head: reread-required; sender observed `codex/youtube-downstream-ecr-cleaning` at `aea51cf1` before writing this file, but main moves fast
- expected_dirty_state_including_handoff_file: sender worktree was clean before adding this file; receiver must inspect fresh state and should not assume this file is already merged to main
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: Orca turns public social capture into usable demand-read signals through the pipeline capture -> ECR -> Cleaning -> Judgment while preserving raw traceability and layer ownership.
- anchor_goal: Define the post-ECR Cleaning routing contract so YouTube surfaces enter the correct Cleaning mechanics and question-specific extraction, while ECR remains source-family-agnostic.
- success_signal: A cold lane can point to a source-backed architecture note that says, for YouTube first, which surfaces get generic ECR receipt, which surfaces have Cleaning adapters, which surfaces are context-only or unsupported, and which extractor may consume each cleaned evidence shape. The note must name the rollout rule for later IG/other-source adoption without authorizing runtime implementation.

## Open Decision / Fork

- decision: Should the next work be an architecture pass or a runtime implementation pass?
  - options:
    - Architecture/scoping pass first: define the source-surface -> Cleaning adapter -> Extraction routing contract, using YouTube as the first concrete surface set.
    - Runtime implementation first: refactor the current runner into an adapter registry immediately.
    - Broad platform rollout: apply the rule to YouTube, IG, Reddit, retail, and future surfaces in one pass.
  - already constrained / off the table:
    - Do not change ECR derivers; ECR remains generic and source-side.
    - Do not treat YouTube comments as transcript input without a comment/thread adapter and extractor.
    - Do not expand into IG runtime changes before the YouTube contract exists.
    - Do not build gold/Judgment, live LLM transport, derived retrieval, or projection changes from this handoff.
  - trade-offs:
    - Architecture first is slower than a quick refactor, but prevents a platform-specific blob and creates a reusable rollout rule.
    - Runtime first may look efficient but risks freezing the current smoke-runner coupling as doctrine.
    - Broad rollout would maximize apparent coverage but increases lock-in before the surface-routing rule is settled.
  - owner of the call: receiving architecture lane may recommend the contract; the human owner owns any doctrine ratification and any later implementation expansion.
  - recommendation and why: run the architecture/scoping pass first. The real boundary is post-ECR Cleaning mechanics, not the YouTube platform label.

## Drift Guard

- invariant: ECR is generic receipt/derive.
  - why it matters: ECR answers integrity questions about source identity, inspectability, timing, and visibility.
  - what violating it would break: platform-specific ECR overrides would fork the source-side integrity layer.
- invariant: Cleaning routes by evidence mechanics.
  - why it matters: captions, ASR audio, post text, comments, metadata, and retail pages need different preparation while sharing traceability obligations.
  - what violating it would break: a platform bucket can accidentally treat comments as transcripts, metadata as evidence text, or raw audio as cleaned text.
- invariant: Extraction routes by question and cleaned evidence shape.
  - why it matters: product mention extraction, audience inference, and comment-demand extraction are different contracts.
  - what violating it would break: question-specific extractors would consume the wrong material and create false semantic claims.
- non-goal: no runtime implementation in this handoff.
  - why it matters: the owner asked whether this is architecture and post-ECR Cleaning; this file commissions that answer, not a code patch.
  - what violating it would break: it would bypass the architecture decision and widen an already active implementation PR.
- non-goal: no IG rollout yet.
  - why it matters: the owner direction is YouTube first, then release the pattern into IG and others.
  - what violating it would break: cross-source rollout would happen before the source-surface contract is explicit.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  - `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`
  - `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md`
  - `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
  - `orca-harness/runners/run_transcript_product_extract.py`
  - `orca-harness/cleaning/models.py`
  - `orca-harness/cleaning/audience_post_input.py`
  - `orca-harness/source_capture/transcript/caption_packet.py`
  - `orca-harness/source_capture/transcript/asr_packet.py`
  - `orca-harness/source_capture/audience_post_packet.py`
- already loaded (weak orientation, freshness-marked; not authority): the sender read the files above on 2026-06-26 in the `codex/youtube-downstream-ecr-cleaning` worktree. Re-read before strict or actionable use.
- must load first (before strict or actionable steps): `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/decision-routing.md`, the Cleaning foundation, the boundary contract, and the current runner/source-surface code.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- ECR generic: ECR is receipt/derive over source-side packet facts, not Cleaning or Judgment.
  - decided in: `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` and `orca-harness/ecr/__init__.py`
  - compare target: reread-required
  - verify before: any claim that ECR should or should not admit a surface
- Cleaning post-ECR: Cleaning uses raw-keyed input handles with optional projection/ECR refs, and source-family adapters feed the generic core.
  - decided in: `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md` and `orca-harness/cleaning/models.py`
  - compare target: reread-required
  - verify before: any adapter-routing recommendation
- YouTube transcript extraction is transcript-shaped: captions and ASR produce transcript cues; Pass-1 product extraction consumes transcripts.
  - decided in: `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md` and `orca-harness/runners/run_transcript_product_extract.py`
  - compare target: reread-required
  - verify before: any extraction routing claim
- ASR is allowed for the YouTube transcript path.
  - decided in: current owner instruction and implemented in the active YouTube ECR/Cleaning branch
  - compare target: reread-required against `run_capture_ecr_cleaning_smoke.py`, tests, and user instruction carried by this handoff
  - verify before: narrowing any transcript route to captions only
- YouTube comments are not globally rejected by ECR.
  - decided in: current layer-boundary reasoning; not yet installed as a source-of-truth architecture record
  - compare target: not proven until the receiving architecture note records it from sources
  - verify before: using this as doctrine outside this handoff

## Active Objective

Run a YouTube-first post-ECR Cleaning architecture pass. The receiver should define how source surfaces route from generic ECR receipt into mechanic-specific Cleaning adapters and then into question-specific extractors, with explicit unsupported/context-only states.

## Exact Next Authorized Action

1. Create a fresh docs/architecture branch or worktree off latest `origin/main`; state branch, HEAD, and dirty state before editing.
2. Re-read the named load-bearing sources under the confirm-don't-trust contract.
3. Author a narrow architecture note, likely under `orca/product/spines/cleaning/contracts/`, that defines a source-surface routing table for YouTube first:
   - `youtube_captions` -> transcript mechanics -> transcript product extraction where the question is product mentions.
   - `youtube_audio` -> audio/ASR route -> transcript mechanics -> transcript product extraction where the question is product mentions.
   - `youtube_post_text` -> written post/audience-post mechanics -> audience/post extraction where the question fits.
   - `youtube_comments` -> comment/thread mechanics, unsupported until a comment/thread adapter and extractor exist.
   - metadata-only files -> context/receipt material unless a specific adapter names them as semantic input.
4. The note must state the reusable rollout rule for IG and later sources: platform/source family is not the Cleaning unit; evidence mechanics and extraction question are.
5. Stop after the architecture/scoping artifact unless the current user explicitly authorizes implementation. If implementation is later authorized, prepare a separate implementation handoff or scoped patch plan.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` supplied in current task context; load-bearing yes; compare target `reread-required`.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint and binding rule.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: load before Orca project work.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading budgets and read-pack rules.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: receiver re-runs progressive source loading.
  - `.agents/workflow-overlay/decision-routing.md`
    - Role: Cynefin routing for architecture/cross-thread handoff work.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: run before planning or delegation.
  - `.agents/workflow-overlay/prompt-orchestration.md`
    - Role: durable handoff/file-write prompt contract.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: apply for any new durable prompt/handoff artifact.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: accepted destination folders.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: use `docs/prompts/handoffs/` for this handoff and `orca/product/spines/cleaning/contracts/` for a Cleaning architecture note if still appropriate.
  - `.agents/workflow-overlay/retrieval-metadata.md`
    - Role: retrieval header contract.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: use retrieval headers for new durable artifacts.
- User constraints:
  - Owner wants YouTube first, then release the pattern into IG and other sources.
  - Owner confirmed ASR is allowed.
  - Owner asked whether this is architecture and whether it is post-ECR Cleaning; answer carried here: yes, it is a post-ECR Cleaning architecture/scoping pass.
- Source-read ledger:
  - `docs/prompts/handoffs/youtube_downstream_ecr_cleaning_lane_handoff_v0.md`
    - Role: prior implementation handoff for YouTube capture -> ECR -> Cleaning smoke and transcript validation.
    - Load-bearing: yes for current PR context; no for new doctrine.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: use as orientation; do not inherit its implementation scope into this architecture pass.
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
    - Role: controlling Data Capture / ECR / Cleaning / Judgment responsibility boundary.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: preserve ECR vs Cleaning vs Judgment split.
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
    - Role: Cleaning purpose and source-family adaptation entrypoint.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: use as Cleaning orientation; foundation carries detailed rules.
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
    - Role: Cleaning layer contract, input handle, allowed transforms, source-family adaptation boundary.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: any adapter-routing contract must preserve its layer rules.
  - `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`
    - Role: ECR receipt/derive frame and generic source-side posture design.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: no YouTube-specific ECR override.
  - `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md`
    - Role: YouTube transcript -> product mention extraction spec and transcript-shaped Pass-1 context.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: transcript extraction consumes transcript cues, not comments or metadata.
  - `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
    - Role: current capture -> ECR -> Cleaning smoke runner; has YouTube captions/audio guard on active branch.
    - Load-bearing: yes for current implementation context.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: treat as implementation evidence, not architecture doctrine.
  - `orca-harness/runners/run_transcript_product_extract.py`
    - Role: transcript product extraction runner; maps `youtube_captions` and `youtube_audio` to transcript inputs.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: use to verify transcript extraction boundary.
  - `orca-harness/cleaning/models.py`
    - Role: runtime Cleaning core models; `CleaningInputHandle` includes `source_family`, `source_surface`, raw anchor, optional projection/ECR refs.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: use to ground adapter contract in existing substrate.
  - `orca-harness/cleaning/audience_post_input.py`
    - Role: existing evidence-mechanic-specific Cleaning adapter for audience-post packets.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: use as precedent for adapter-specific surface admission.
  - `orca-harness/source_capture/transcript/caption_packet.py`, `orca-harness/source_capture/transcript/asr_packet.py`, `orca-harness/source_capture/audience_post_packet.py`
    - Role: current source surfaces and packet shape examples for captions, audio, and written post text.
    - Load-bearing: yes.
    - Compare target: `reread-required`.
    - Last checked: 2026-06-26.
    - Reuse rule: verify current `source_surface` names before drafting the routing table.
- Source gaps:
  - No source-visible YouTube comments packet/adapter was verified in this turn.
  - No accepted generic Cleaning adapter registry doctrine was found in this turn.
- Strict-only blockers:
  - Cannot claim final architecture doctrine until a controlling Cleaning/source artifact is written and, if doctrine-changing, propagated.
  - Cannot claim implementation readiness or validation from this handoff.
- Not-proven boundaries:
  - That the current active branch has landed to main.
  - That IG rollout is ready.
  - That comments have an accepted packet shape or adapter.

## Current Task State

- Completed:
  - YouTube captions and ASR are conceptually separated from comments/post text in the current owner discussion.
  - Active YouTube ECR/Cleaning implementation branch allows `youtube_captions` and `youtube_audio` in the smoke runner and rejects unsupported surfaces such as `youtube_comments`.
  - Cleaning foundation already states the core-vs-adapter boundary: generic handle/ledger core, source-family adaptation at the edge.
- Partially completed:
  - The current runner has a hardcoded YouTube surface allowlist. It is implementation-local, not an accepted architecture registry.
  - Transcript product extraction already handles caption and ASR transcript shapes, but the cross-surface routing doctrine is not filed.
- Broken or uncertain:
  - Without an explicit architecture note, future lanes may misread `youtube_comments` rejection as an ECR rejection.
  - There is no verified comment/thread Cleaning adapter for YouTube comments in the current loaded set.

## Workspace State

- Branch: sender observed `codex/youtube-downstream-ecr-cleaning`.
- Head: sender observed `aea51cf1` before writing this handoff.
- Dirty or untracked state before handoff: clean, observed by `git status --short --branch`.
- Dirty or untracked state after writing the handoff file: this handoff file is newly added until committed by the sender; receiver must verify current state.
- Target files or artifacts:
  - This handoff: `docs/prompts/handoffs/youtube_post_ecr_cleaning_adapter_architecture_handoff_v0.md`.
  - Likely receiver output: a new architecture note under `orca/product/spines/cleaning/contracts/`.
- Related worktrees or branches:
  - Existing implementation branch: `codex/youtube-downstream-ecr-cleaning`.
  - Receiver should branch fresh from latest `origin/main`; do not reuse active worktrees with unrelated dirty state.

## Changed / Inspected / Tested Files

- `docs/prompts/handoffs/youtube_post_ecr_cleaning_adapter_architecture_handoff_v0.md`
  - Status: newly added by this handoff turn.
  - Role: durable cross-lane handoff packet.
  - Important observations: commissions architecture/scoping only, not runtime implementation.
  - Symbols or sections: Load Contract, Goal Handoff, Open Decision, Drift Guard, Exact Next Authorized Action.
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - Status: inspected.
  - Role: Cleaning layer contract.
  - Important observations: Cleaning uses raw-keyed handles, optional projection/ECR refs, and source-family adaptation at the edge.
  - Symbols or sections: Layer Boundary, Inputs Cleaning May Receive, Source-Family Adaptation Boundary.
- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
  - Status: inspected.
  - Role: current implementation template.
  - Important observations: active branch has `YOUTUBE_SOURCE_SURFACES = {"youtube_captions", "youtube_audio"}` and `_process_youtube_entry` builds Cleaning handles from packet `source_slices`.
  - Symbols or sections: `YOUTUBE_SOURCE_SURFACES`, `_process_youtube_entry`.
- `orca-harness/runners/run_transcript_product_extract.py`
  - Status: inspected.
  - Role: transcript product extraction runner.
  - Important observations: maps `youtube_captions` and `youtube_audio` into `TranscriptInput`; does not claim comments are transcript input.
  - Symbols or sections: `_transcripts_for_packet`.
- `orca-harness/cleaning/audience_post_input.py`
  - Status: inspected.
  - Role: existing Cleaning adapter precedent.
  - Important observations: accepts only known audience-post surfaces and fails closed on mismatches.
  - Symbols or sections: `ALLOWED_SURFACES`, `post_input_from_packet`.

## Frozen Decisions

- Decision: ECR remains generic and source-family-agnostic.
  - Evidence: ECR frame and deriver sources; prior handoff Drift Guard.
  - Consequence: do not make YouTube-specific ECR derivers or ECR overrides.
- Decision: Cleaning is post-ECR and mechanic-specific at the adapter edge.
  - Evidence: Cleaning README and foundation; current owner direction in this thread.
  - Consequence: route by transcript/audio/post/comment/page mechanics, not by platform label alone.
- Decision: Extraction is question-specific.
  - Evidence: YouTube transcript product extraction spec and current transcript runner.
  - Consequence: product mention extraction should consume transcript-shaped input only unless another extractor is explicitly designed.
- Decision: ASR is allowed.
  - Evidence: current owner instruction and active branch tests.
  - Consequence: do not regress to caption-only transcript routing.

## Mutable Questions

- Question: What exact artifact should become the long-term home for the routing contract?
  - Why still mutable: the receiver may choose a Cleaning contract note, an architecture plan, or a patch to the existing Cleaning foundation depending on source freshness.
  - What would resolve it: read current `orca/product/spines/cleaning/contracts/` and choose the smallest complete source-visible home.
- Question: Should the later runtime shape be a registry, adapter protocol, or a simpler table in the smoke runner?
  - Why still mutable: this handoff commissions architecture, not runtime design.
  - What would resolve it: architecture note plus implementation scoping after owner authorization.
- Question: What is the exact YouTube comments packet shape?
  - Why still mutable: no current comments packet/adapter was loaded and verified in this turn.
  - What would resolve it: source-read or design a comments capture packet in a separate capture/adapter lane.

## Superseded / Dangerous-To-Reuse Context

- Stale idea: "Cleaning/ECR all for YouTube."
  - Why stale or dangerous: it mixes platform label with evidence mechanics and can route comments/audio/metadata into the wrong Cleaning or Extraction path.
  - Current replacement: ECR generic; Cleaning mechanic-specific; Extraction question-specific.
- Stale inference: "The current runner rejects `youtube_comments`, so ECR rejects comments."
  - Why stale or dangerous: the current runner couples ECR and Cleaning handle construction for a transcript-first smoke path.
  - Current replacement: treat `youtube_comments` as unsupported by the current Cleaning adapter, not globally non-receiptable by ECR.
- Stale scope: "Implement registry now."
  - Why stale or dangerous: implementation would freeze architecture before the contract is source-visible.
  - Current replacement: architecture/scoping pass first; implementation needs separate authorization.

## Commands And Verification Evidence

- Command:
  ```bash
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `## codex/youtube-downstream-ecr-cleaning...origin/codex/youtube-downstream-ecr-cleaning`.
  - Re-run target so the receiver can confirm rather than trust: receiver runs the same command in its own fresh worktree and expects a clean state before editing.
- Command:
  ```bash
  git rev-parse --short HEAD
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `aea51cf1`.
  - Re-run target so the receiver can confirm rather than trust: receiver records its own branch HEAD after refetching latest `origin/main`.
- Command:
  ```bash
  rg --files orca/product/spines/cleaning docs/prompts/templates/shared orca-harness/cleaning orca-harness/runners | rg 'cleaning|transcript|audience|run_capture_ecr|product'
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: found Cleaning contracts, Cleaning models/adapters, `run_capture_ecr_cleaning_smoke.py`, `run_transcript_product_extract.py`, and `run_ig_reels_product_extract.py`.
  - Re-run target so the receiver can confirm rather than trust: same or narrower source discovery in the receiving worktree.
- Validation:
  - Code tests not run for this handoff authoring turn because it is docs-only and no runtime code was changed.
  - Receiver must not infer implementation validation from this packet.

## Blockers And Risks

- Risk: architecture note accidentally changes doctrine without propagation.
  - Evidence: this work may affect Cleaning layer behavior and rollout sequencing.
  - Likely next action: if the receiving artifact changes durable doctrine, update the controlling source and carry a DCP receipt or blocker.
- Risk: comments are treated as transcript evidence.
  - Evidence: current transcript extractor handles captions and ASR transcript cues, not comment/thread structures.
  - Likely next action: require a comment/thread adapter and extractor before admitting comments into semantic Cleaning/Extraction.
- Risk: implementation runs before architecture.
  - Evidence: current code has an easy hardcoded allowlist that could be generalized prematurely.
  - Likely next action: stop at architecture/scoping unless a new bounded implementation handoff is explicit.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - ECR derivers remain source-family-agnostic.
  - Cleaning foundation still says generic core plus source-family adaptation edge.
  - Current YouTube runner's surface guard still admits captions/audio and rejects unsupported surfaces.
  - Transcript product extractor still consumes `youtube_captions` and `youtube_audio` transcript shapes.
  - Audience-post adapter remains a fail-closed adapter precedent for source-surface admission.
  - No existing accepted adapter-routing architecture already supersedes this handoff.
- Compare target for each:
  - `reread-required` for all source files named in Authority And Source Ledger.
- Load outcomes and what each means:
  - `REUSE`: all load-bearing sources re-read and no material drift; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional context drifted; reuse only verified sections and re-derive the rest.
  - `STALE_REREAD_REQUIRED`: material sources drifted but can be safely re-read; re-run source loading before drafting.
  - `BLOCKED_DRIFT`: source drift conflicts with the layer boundary, owner instruction, or target path.
  - `BLOCKED_MISSING_PACKET`: this handoff path is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be verified from available sources; do not proceed on sender say-so.
- Sources that must be reread if drift is detected:
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  - `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`
  - `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
  - `orca-harness/runners/run_transcript_product_extract.py`

## Do Not Forget

- This is post-ECR and specifically Cleaning architecture/scoping.
- The rule to preserve is: source family/platform for acquisition, ECR for generic receipt, Cleaning for evidence mechanics, Extraction for question-specific use.
- YouTube first means use YouTube surfaces as concrete examples; it does not mean build a permanent YouTube blob.
- ASR is allowed and should remain part of the transcript route.
- Comments are not globally rejected by ECR; they are unsupported by the current transcript-cleaning path until a comment/thread adapter exists.
- Do not implement the registry or broaden to IG until the YouTube-first routing contract is source-visible and owner-accepted.
