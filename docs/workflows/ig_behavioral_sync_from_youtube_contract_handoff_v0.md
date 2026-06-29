# IG Behavioral Sync From YouTube Contract Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Cold-reader handoff for starting the Instagram/Reels behavioral-sync lane from the source-backed YouTube behavioral contract.
use_when:
  - Starting a fresh IG lane after the YouTube behavioral contract extraction and adjudication work.
  - Re-establishing what to compare, what not to copy, and which sources must be reread before IG behavior claims.
  - Preparing an IG gap ledger or bounded IG patch plan against the YouTube reference behavior.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
  - docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
branch_or_commit: codex/youtube-contract-review-adjudication parent 6e8aea65a8fd5c6ebbaa5818dbbd7e09fb48ba84 before this handoff file was added
stale_if:
  - PR #432 is closed without merge or superseded by another YouTube behavioral contract patch.
  - Any named IG or YouTube capture, transcript, projection, persistence, extraction, or focused test source changes.
  - The owner redirects from behavior parity to shared acquisition machinery.
```

## Load Contract

Packet mode: `workflow-handoff/max/v0`.

This is a state packet, not source authority. Treat it as orientation until the named sources below are freshly opened. For strict or actionable claims, confirm against the source file or live PR state first.

Current durable surface at packet creation:

- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- worktree used for this packet: `.codex/worktrees/youtube-contract-review-adjudication`
- branch: `codex/youtube-contract-review-adjudication`
- PR: `https://github.com/eric-foo/orca/pull/432`
- PR state observed on 2026-06-29: open draft, base `main`, head `codex/youtube-contract-review-adjudication`, head OID `6e8aea65a8fd5c6ebbaa5818dbbd7e09fb48ba84`
- important caveat: that head OID is the parent commit before this handoff file was added. A receiver must re-check the live PR head or merged `origin/main` before relying on it.

Orca start preflight for this packet:

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 plus target workflow/docs and targeted IG/YT source map
  edit_permission: docs-write
  target_scope: cross-thread workflow handoff for starting the IG behavioral-sync lane
  dirty_state_checked: yes
  blocked_if_missing: PR #432 state, YouTube contract source, IG source/test reread, capture playbook reread before live capture
```

Minimum required rereads for the next lane:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-loading.md`
4. `.agents/workflow-overlay/decision-routing.md`
5. `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
6. `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
7. `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
8. `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`
9. `docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md`
10. the IG implementation and focused tests listed under "Source Ledger".

## Goal Handoff

Long-term goal: unify IG/Reels, YouTube, and later TikTok capture behavior around a shared completeness contract without forcing shared acquisition machinery, runner shape, transcript priority, or persistence unit shape.

Active objective for the receiving lane: start the IG lane. Compare current IG grid, deep-capture, audio-transcript, projection, persistence, and extraction behavior against the adjudicated YouTube behavioral contract. Produce a source-backed IG gap ledger and a bounded patch decision.

Success signal: the lane can name, with source pointers, which IG behavior should match the YouTube-level completeness contract, which IG-specific shapes stay adapter-owned, which residuals are accepted, and which exact IG patch or no-patch decision is next.

## Open Decision / Fork

Decision: should the IG lane patch immediately from the existing IG back-fix spec, or first refresh the source-backed IG gap ledger?

Recommended fork: refresh the IG gap ledger first. The existing IG back-fix spec is strong planning material, but it was written before this handoff and before the PR #432 adjudication patch. It should not become implementation authority until the next lane re-reads the named IG sources/tests and verifies that the source basis still matches.

If the owner explicitly asks for implementation in the next turn, run the assumption gate and fused path against the refreshed source reads before editing.

## Drift Guard

Do not copy YouTube's acquisition method, caption-first priority, packet anchors, HTTP/youtubei shape, or runner structure into IG.

Do not average IG and YouTube into a vague abstraction. The shared target is observable behavior: identity, comments posture, transcript-source records, run receipts, deterministic persistence correlation, extraction-feed compatibility, extraction rollup semantics, residual visibility, and no hidden completeness claims.

Do not implement the shared core from this packet. This packet starts the IG behavior-sync lane only.

Do not treat PR #432 as merged until a live PR or `origin/main` check proves it. If PR #432 is not merged, use the PR branch/worktree as the YouTube reference or stop and rebase the contract patch.

Do not use the older `codex/youtube-behavioral-contract-extract` branch as the landing surface. It was superseded after PR #430 merged.

Do not use prior chat memory, this handoff, or any review output as strict source proof. Re-read the named source files.

## Inherited Context

The useful answer to the user's review question is: yes, the delegated review was narrowly worth it for this artifact, but not as routine documentation ceremony.

Why it was worth it:

- It did not uncover a deep behavioral error; the YouTube contract was materially accurate.
- It caught real durability defects before the artifact became the IG reference: an unfenced retrieval header and an unowned one-off `review_routing_status` field.
- It surfaced completeness omissions that matter in a behavior contract: single-video-id preconditions and extraction-result enrichment fields.
- It independently confirmed no critical or major behavioral inaccuracies before using the YouTube contract as the IG comparison anchor.

Why it should not expand scope:

- The review does not prove runtime readiness, live capture readiness, shared-core readiness, or IG parity.
- The review cost was high. Use it at high-lock-in fork points, not ordinary docs.

The owner clarified the target during this lane: push against the same capture/completeness machinery only where behavior needs to be comparable, but keep acquisition method, priority, shape, and platform-specific exploration open. The lane-first route is YouTube complete enough first, then use that completed YouTube behavior to back-fix IG.

## Current Task State

Completed before this handoff:

- YouTube behavioral contract was extracted from source and stored in `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`.
- Delegated review was adjudicated.
- Accepted patches were applied on fresh branch `codex/youtube-contract-review-adjudication`.
- Draft PR #432 was opened from that branch.
- Validation for the PR #432 YouTube-contract patch passed before this handoff file was added:
  - `git diff --check origin/main..HEAD`
  - `python .agents/hooks/check_retrieval_header.py --strict docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
  - `python .agents/hooks/check_retrieval_header.py --changed --strict`
  - `python .agents/hooks/header_index.py --strict --base origin/main`

Not completed:

- No fresh full IG lane analysis was performed in this handoff step.
- No IG source edits were made.
- No shared-core implementation or refactor was started.
- No live capture was run in this handoff step.

## Source Ledger

Hashes below were observed in `.codex/worktrees/youtube-contract-review-adjudication` on 2026-06-29. Use them as compare targets, not as a substitute for rereading.

Workflow/docs:

- `E0D1FCD55052AD0C300DBF596241C2EB5A5A33C1BC99F602A8A63951331BD2C3`  `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
- `8C2A62390E386DC8EBECA517D4F0518F5C053FF43CD69D97B9CC9D3FC380E8AD`  `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`
- `DB7E592AEE7184D1D6F667B2E3D70C8A14B9CCE5631019F850FC5EDB1868F5AA`  `docs/workflows/shared_capture_behavioral_contract_extraction_spec_v0.md`
- `60BB5ABAEFDFD5C45BF021323DC83F0776E0CBCBA41C84AA82D4A46E368FFAA3`  `docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md`

YouTube source and tests:

- `D9F760EF4BDD28C4946EB73111F77A7A0254E2C5DE3EE11AAD729787B8C673B3`  `orca-harness/youtube_capture/behavioral_projection.py`
- `D55180AD50287F52569A1D6F4462E5071534A7DDE8689E4EF06968A8769748A4`  `orca-harness/tests/unit/test_youtube_behavioral_projection.py`
- `D39086E33666859DD1C8F949CCB4B6051C5DEE19CBADFF0A0E7438A887C52ED5`  `orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py`
- `EA78BCEF550E35A69A7A495FA76D067C1069469C821CCC5A21D1FFA84971AE6D`  `orca-harness/data_lake/root.py`

IG source and tests to reread before claims:

- `4685309F1C4D8DA97B007823CE7F50F84C6F1C52CA10F52E22599150E90B67E1`  `orca-harness/source_capture/ig_reels_grid_projection.py`
- `39EBE775B97EEA248B492BD810A1F851BC9EEB7792E58041C7D3E863434A660D`  `orca-harness/source_capture/transcript/ig_reels_audio_packet.py`
- `903ED3E4A5BB542F56CA96872BFA56BC509A2D219BDC084EF2E588B85BED52B8`  `orca-harness/source_capture/ig_reels_deep_capture.py`
- `8DBD6C909AC4B2769ED65F03D11B5F70B8D99132EC91B1D7A36BC9685A477DDE`  `orca-harness/source_capture/ig_reels_deep_capture_lake.py`
- `2D3FEB08EE2E53B98D79366A453784C562146D77E17E05AB416153675500DF56`  `orca-harness/source_capture/ig_projection.py`
- `86F1D0652A3BE2AE2D1084D054953147436FDB7BE3B5852B7AF3341B4DC65994`  `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py`
- `334BD3822157BC2785649D6D1EB342D6F8D648C9659EEFB685683FD6AFAB8D66`  `orca-harness/runners/run_source_capture_ig_reels_audio_packet.py`
- `9D2E446B5A3A740D020C06BADDF9800A7D152E32D3F9BF8C74EEC3A16D2AFBF9`  `orca-harness/tests/unit/test_source_capture_ig_reels_projection.py`
- `430842712E4132604765FB443D39835E8A3B05D9561E182551EF23393D07F336`  `orca-harness/tests/unit/test_ig_reels_audio_packet.py`
- `984ADF91A29F4FAEF7E009FCCF7BB59715F381F38AD5E61676C59AD587C86B7F`  `orca-harness/tests/unit/test_ig_reels_deep_capture.py`
- `52F9CB45176DCC60BB5230307D7D816DFA1C6583CA3D899C310522F8DA76E071`  `orca-harness/tests/unit/test_ig_reels_deep_capture_lake.py`

Additional likely IG sources to search if the first pass exposes a gap:

- `orca-harness/source_capture/ig_reels_grid.py`
- `orca-harness/source_capture/ig_reels_comments.py`
- `orca-harness/runners/run_source_capture_ig_reels_deep_capture.py`
- `orca-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py`
- `orca-harness/runners/run_ig_reels_product_extract.py`
- `orca-harness/tests/unit/test_ig_reels_product_extract.py`

## Behavioral Anchors To Compare

Use the YouTube contract as a reference contract, not an implementation recipe.

YouTube reference behavior to compare:

- `project_youtube_behavioral_item(...)` exposes metadata, comments, transcript sources, extraction statuses, canonical transcript source, and `behavioral_completeness`.
- `behavioral_completeness.complete` is true only when the transcript extraction rollup status is exactly `complete`.
- Extraction rollup statuses include `no_extraction_eligible_sources`, `complete`, `complete_with_residuals`, `partial_failed`, `partial`, `failed`, `source_problem`, and `not_attempted`.
- Runtime acquisition and LLM imports are forbidden in the YouTube behavioral projection module.
- Transfer note: the shared discussion should reuse behavior/completeness projection and residual vocabulary, not YouTube acquisition machinery.

IG behavior that must be checked fresh:

- Grid projection behavior: shortcode identity, ranking basis, metric limitations, surface disagreement, and non-authoritative fields.
- Deep capture behavior: rendered reel pass, comments, transient media handle, ASR route, and redaction/non-persistence posture.
- Deep-capture lake behavior: shortcode-anchored derived record set, comments/transcript members, and completion marker.
- Standalone audio behavior: `ig_reels_audio` SourceCapturePacket, `transcript_asr` derived record, posture, cues, model/tool metadata, and failure visibility.
- Extraction behavior: whether only standalone audio packets feed the shared extractor today, and whether deep-capture transcript records are currently outside the shared extraction feed.

## MGT / SCI Lens

MGT target: the lane should be complete enough to make failures, partials, skipped work, residuals, weak evidence, and transcript/extraction gaps visible without pretending the platforms are uniform.

Accepted residuals can remain if named, discoverable, and upgrade-triggered:

- IG can remain ASR-only in v0.
- IG can keep separate grid, deep-capture, and standalone audio runners if receipts and correlation stay coherent.
- Physical persistence can remain uneven if deterministic lookup prevents human-convention joins.
- Deep-capture transcript extraction can remain residual only if it is explicitly named and does not let a whole-item extraction status claim hidden completeness.

SCI boundary: the smallest complete next move is an IG gap ledger and patch decision, not a shared-core build. A larger patch is justified only if the gap ledger shows that hidden completeness or non-deterministic correlation would otherwise survive.

## Exact Next Move

1. Confirm PR #432 or merged `origin/main` state. If PR #432 is still open, start from or fetch the PR branch; if it merged, start fresh from `origin/main` after verifying the YouTube contract includes the adjudication patch.
2. Re-read the capture playbook and recon index before any live capture, because live IG capture remains source-capture activity.
3. Re-read the IG sources/tests in the Source Ledger and the existing IG back-fix spec.
4. Produce an `IG vs YouTube behavioral gap ledger` with rows for identity, candidate/ranking limits, comments posture, transcript source records, run receipts, persistence correlation, extraction feed, extraction statuses, residuals, and tests.
5. Decide one of:
   - no patch yet: old IG spec is stale or source evidence conflicts;
   - docs patch: update the IG back-fix spec/gap ledger only;
   - implementation patch: owner authorized source-changing IG parity work and assumption gate/fused passes.

## Review Checkpoint

Adversarial review is not required before the first IG source refresh. It becomes worth considering again after the IG gap ledger and a concrete IG patch plan exist, because that is the next high-lock-in fork.

If the patch plan only changes docs and keeps behavior/no-authority boundaries clear, a small source-backed review may be enough. If it changes runtime projection or persistence semantics, run a code review plus source-backed artifact review before shared-core extraction.

## Non-Claims

This packet does not claim:

- PR #432 is merged;
- IG parity is implemented;
- IG live capture was run or validated;
- YouTube runtime acquisition coverage is complete;
- shared capture core implementation is authorized;
- TikTok behavior, route, access posture, or adapter shape is known;
- production readiness, legal/access approval, or live-scale validation.
