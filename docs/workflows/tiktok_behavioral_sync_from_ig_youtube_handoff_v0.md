# TikTok Behavioral Sync From IG YouTube Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet
scope: >
  Cold-reader handoff for starting the TikTok behavior-sync lane after the
  Instagram/YouTube behavioral-sync closeout. Carries the desired target:
  same behavioral completeness and information-gathering posture as IG/YT,
  with most source-visible information and the lowest practical fingerprinting
  footprint, without copying IG or YouTube mechanics into TikTok.
use_when:
  - Starting a fresh TikTok capture/behavior lane after the IG/YT sync lane.
  - Checking what TikTok should inherit behaviorally from IG/YT and what must
    remain TikTok-source-family owned.
  - Preparing a TikTok source refresh, probe plan, or bounded implementation
    scoping pass.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md
  - docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
  - docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md
stale_if:
  - A later IG/YT behavioral closeout supersedes the counts or residuals named here.
  - Any TikTok source-family spec, probe recon, sessioned probe plan, capture playbook, or recon index entry changes.
  - The owner redirects from TikTok source-family behavior sync to shared-core implementation or bulk capture.
  - A live TikTok probe runs and updates the route, access, fingerprint, or data-contract evidence.
```

## Load Contract

- packet_version: workflow-handoff/max/v0
- mode: max
- created_at: 2026-06-30
- created_by_lane: Codex IG/YT behavioral residual-burndown lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-youtube-residual-burndown`
- handoff_path: `docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md`
- expected_branch: `codex/ig-youtube-residual-burndown-pushable`
- expected_head_before_handoff_file: `886769bc683d3162f3b00b35ee7acb8e9c7ade4d`
- expected_dirty_state_before_handoff_file: clean relative to `origin/codex/ig-youtube-residual-burndown`
- expected_dirty_state_after_handoff_file: one untracked handoff file at this path unless a later lane commits or moves it
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Unify Instagram Reels, YouTube videos/Shorts, TikTok, and later social-video sources around a shared behavioral completeness and information-gathering contract while preserving source-family-specific capture mechanics.
- anchor_goal: Start TikTok from the now-proven IG/YT behavioral contract and the existing TikTok recon/spec sources, aiming for maximum source-visible information with minimum practical fingerprinting surface.
- success_signal: A cold TikTok lane can state, with fresh source pointers, which TikTok profile-grid, video-detail, comment, metadata, transcript/audio, persistence, extraction, residual, and fingerprint/access behaviors can match the IG/YT contract; which TikTok-specific mechanics stay adapter-owned; and whether the next step is a probe, docs/spec patch, implementation patch, or blocker.

## Open Decision / Fork

- decision: How should TikTok enter the IG/YT behavior contract?
  - options:
    - `A_source_refresh_gap_ledger_first`: re-read the TikTok spec/recon/probe plans plus IG/YT closeout, then produce a TikTok behavioral gap ledger and exact probe/patch decision.
    - `B_owner_gated_warm_session_probe`: run the existing sessioned warm-probe plan with a dedicated account, human login, and network approval, then update the TikTok route evidence.
    - `C_implementation_now`: start building TikTok parser/runner/projection code immediately.
  - already constrained / off the table:
    - Do not build shared core or TikTok code from this packet alone.
    - Do not run live TikTok or sessioned capture without current explicit live/network authorization, human-performed login, and account-risk acceptance.
    - Do not make TikTok use IG selectors, YouTube `youtubei`, or any forged TikTok signature route.
  - trade-offs:
    - Option A is lowest lock-in and best first step because TikTok sources already exist but contain route/access changes that must be reconciled before scoping.
    - Option B measures the real per-account ceiling and may be needed before claiming reliability, but it requires live network, a dedicated account, and accepted ban/ToS risk.
    - Option C is fastest to code but wrong now: it would freeze route and access assumptions before the TikTok evidence is refreshed.
  - owner of the call: owner decides whether/when live TikTok probing and sessioned-account risk are allowed.
  - recommendation and why: choose Option A first. Then run Option B only if the refreshed ledger says the warm-session route evidence is the bottleneck for implementation. Defer Option C until an assumption gate/fused implementation pass has a source-backed target.

## Drift Guard

- behavioral parity, not machinery parity:
  - why it matters: The IG/YT lane succeeded by making behavior comparable while leaving capture mechanics platform-owned.
  - what violating it would break: Copying IG browser-grid/deep-capture or YouTube caption/youtubei mechanics into TikTok would create fake uniformity and likely miss TikTok's actual source surfaces.
- most information, least fingerprinting:
  - why it matters: TikTok's spec prioritizes lowest bot detectability and scale, so the lane should ride page-owned requests and cap per-target requests.
  - what violating it would break: Deep pagination, synthetic signed API calls, high-rate scanning, or full comment census would increase detection surface before proving value.
- sessioned TikTok is not a free upgrade:
  - why it matters: Existing TikTok spec pivots to a dedicated authenticated session because logged-out was brittle, but that trades captcha/throttle for account-ban risk.
  - what violating it would break: Using a personal account, agent-entered credentials, or storing session material would contaminate packets and violate the secret/access boundary.
- no secret or fingerprint leakage:
  - why it matters: TikTok route evidence includes cookies, device/session tokens, `msToken`, `X-Bogus`, `X-Gnarly`, proxy and browser-fingerprint sensitivities.
  - what violating it would break: Durable packets would become contaminated scratch and unusable as source-capture records.
- no downstream meaning in Capture:
  - why it matters: Capture may preserve source-visible counts, comments, handles, hashtags, sounds, stats, and timestamps, but does not decide bots, sponsorship, credibility, demand, or action support.
  - what violating it would break: Capture would leak into Judgment/Cleaning claims and overstate source facts.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md`
  - `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md`
  - `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`
  - `docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md`
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md`
- already loaded (weak orientation, freshness-marked; not authority): the files above were read in this handoff lane on 2026-06-30, plus targeted searches for TikTok/social source-family artifacts.
- must load first (before strict or actionable steps): `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/decision-routing.md`, source-capture playbook, recon index, current TikTok spec/recon/probe plans, and the IG/YT closeout receipt.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: IG/YT are behaviorally comparable enough to hand off; not globally platform-complete.
  - decided in: `docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md`
  - compare target: SHA256 `A3621D5AAF067AEFE122322C560E0F7968288422D275D242A5FFD7FB29DD35A8`
  - verify before: claiming IG/YT phase closure or using IG/YT as TikTok reference.
- decision, framing, profile, or convention: YouTube caption-route corpus is measurable and observed complete for 31 caption-ready videos; platform-wide ASR/no-caption remains residual.
  - decided in: `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md`
  - compare target: SHA256 `B26F6DE6E62A383E82DAA0E737BEB4707F1BDB1126D1C514C339757033853D0D`
  - verify before: using YouTube as a completed behavior reference.
- decision, framing, profile, or convention: shared target is thin behavioral core, not shared acquisition machinery.
  - decided in: `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`
  - compare target: SHA256 `8C2A62390E386DC8EBECA517D4F0518F5C053FF43CD69D97B9CC9D3FC380E8AD`
  - verify before: proposing any shared-core or cross-platform abstraction.
- decision, framing, profile, or convention: TikTok has source-family spec/recon evidence, but detection ceiling and scale reliability remain unmeasured.
  - decided in: `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`, `tiktok_first_slice_probe_recon_v0.md`, and `tiktok_sessioned_capture_warm_probe_plan_v0.md`
  - compare target: SHA256 `6ABF594A667A269FE9D35E67D72069C9B3D9190DF029E07839414C9DB6448F1C`; `F77A29723F1A2E462BD0555F113829DA7288798B4FF1D34810EBD964B1795BD3`; `013BA33A459CFDE072E6C5FCD929E2E6B1627312E5287FED8B28CCE80286F88D`
  - verify before: claiming TikTok route, access, data contract, reliability, or capture readiness.

## Active Objective

Start the TikTok behavior-sync lane. Compare TikTok's existing source-family spec, first-slice recon, and sessioned warm-probe plan against the IG/YT behavioral contract, then produce a source-backed TikTok gap ledger and next-action decision.

## Exact Next Authorized Action

1. Re-read the load-bearing sources named in this packet and return a confirm-don't-trust load outcome.
2. Produce a TikTok behavioral gap ledger with rows for profile/listing grid, video detail, stable identity, metadata/stats, comments sample/posture, exact timestamps, transcript/audio/source-text posture, run receipt, persistence/correlation anchors, extraction-feed readiness, residual visibility, and fingerprint/access posture.
3. Split each row into `code-enforceable`, `behavioral/doctrine`, `requires_live_probe`, or `blocked/unproven`.
4. Decide the next move: no-patch docs/spec update, owner-gated warm-session probe, assumption-gate/fused implementation scoping, or blocker. Do not perform live capture or code edits unless explicitly redirected.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md`, supplied in current task context; load-bearing yes for project behavior and edit rules; compare target `reread-required`.
- Overlay authority:
  - `.agents/workflow-overlay/README.md`
    - Role: Orca overlay entrypoint.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-30 in this handoff lane.
    - Reuse rule: reread before strict or actionable claims.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading policy and capture playbook auto-load rule.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-30 in this handoff lane.
    - Reuse rule: reread before strict or actionable claims.
  - `.agents/workflow-overlay/decision-routing.md`
    - Role: Cynefin routing before planning, delegation, prompt execution, review, patching, or infrastructure work.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-30 in this handoff lane.
    - Reuse rule: rerun router before TikTok planning or implementation.
- Source-read ledger:
  - `docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md`
    - Role: current IG/YT behavioral closeout and non-claims.
    - Load-bearing: yes.
    - Compare target: SHA256 `A3621D5AAF067AEFE122322C560E0F7968288422D275D242A5FFD7FB29DD35A8`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify hash or reread before closure claims.
  - `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md`
    - Role: expanded YouTube caption-route corpus evidence.
    - Load-bearing: yes.
    - Compare target: SHA256 `B26F6DE6E62A383E82DAA0E737BEB4707F1BDB1126D1C514C339757033853D0D`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify hash or reread before YouTube corpus claims.
  - `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`
    - Role: thin shared behavioral-core planning boundary.
    - Load-bearing: yes.
    - Compare target: SHA256 `8C2A62390E386DC8EBECA517D4F0518F5C053FF43CD69D97B9CC9D3FC380E8AD`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before shared-core or machinery-parity claims.
  - `docs/workflows/youtube_first_behavioral_completion_spec_v0.md`
    - Role: behavior parity spec and TikTok-deferred boundary.
    - Load-bearing: yes.
    - Compare target: SHA256 `D10F373E47FED44CB99511DE460C94995B9F08EA14EE22CAA870ACBE65F786A8`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before using YouTube as behavior template.
  - `docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md`
    - Role: generic social DOM/passive-JSON lessons and code-enforceable split.
    - Load-bearing: yes.
    - Compare target: SHA256 `B9856FDDE5CD3EEB6B7B57EBB5A2363F55E67C670B4115F97D38C67D0D093401`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before carrying generic DOM/JSON lessons into TikTok.
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
    - Role: capture method, access gate, route catalog, receipt rules.
    - Load-bearing: yes.
    - Compare target: SHA256 `0B8C169F10741ABE6574CFC18A25A0C1516B45E1B30FA11F4B2C551235F62796`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before any capture/probe/live route decision.
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
    - Role: source-family recon index and social-source state.
    - Load-bearing: yes.
    - Compare target: SHA256 `E5A583DBBF910BEFC9372D470EEA88038C0FA92B3C92A1D23634C08F11CF679B`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before claiming TikTok recon status.
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
    - Role: TikTok capture behavior/data/access/fingerprint spec.
    - Load-bearing: yes.
    - Compare target: SHA256 `6ABF594A667A269FE9D35E67D72069C9B3D9190DF029E07839414C9DB6448F1C`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before TikTok spec or implementation claims.
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md`
    - Role: first TikTok technical recon and detection addendum.
    - Load-bearing: yes.
    - Compare target: SHA256 `F77A29723F1A2E462BD0555F113829DA7288798B4FF1D34810EBD964B1795BD3`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before TikTok route/access evidence claims.
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md`
    - Role: sessioned warm-probe measurement plan.
    - Load-bearing: yes.
    - Compare target: SHA256 `013BA33A459CFDE072E6C5FCD929E2E6B1627312E5287FED8B28CCE80286F88D`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before live warm-probe planning.
- Source gaps:
  - No fresh TikTok live run was performed in this handoff lane.
  - No current TikTok implementation source was found or inspected because this packet is not an implementation turn.
  - Detection ceiling and platform-scale reliability are unmeasured.
  - Transcript/audio behavior for TikTok is not proven by the loaded spec; the next lane must decide whether source-native captions/audio/transcript are visible, require ASR, or remain out of scope.
- Strict-only blockers:
  - Live TikTok probing requires explicit current live/network authorization and, for sessioned mode, human login to a dedicated account plus account-ban risk acceptance.
  - Implementation requires a separate bounded implementation authorization and assumption-gate/fused scoping.
- Not-proven boundaries:
  - not TikTok validation/readiness
  - not live-scale reliability
  - not legal advice
  - not source-access approval beyond the existing owner-risk posture
  - not a shared-core implementation authorization

## Current Task State

- Completed:
  - IG/YT behavior-sync phase has a current closeout receipt with explicit residuals and non-claims.
  - YouTube caption-route behavioral corpus is measurable and observed complete for 31 caption-ready videos.
  - Delegated review residual for the YouTube leading-dash CLI edge was patched, tested, committed, pushed, and remote-readback verified before this handoff.
  - Existing TikTok source-family spec, recon, and warm-probe plans were identified and read for this packet.
- Partially completed:
  - TikTok has source-family planning and recon evidence, but not a refreshed IG/YT behavioral gap ledger.
  - TikTok has a sessioned capture/warm-probe plan, but no measured detection ceiling in this handoff.
- Broken or uncertain:
  - TikTok's best "least fingerprinting" posture is not simply logged-out. Current spec says logged-out is brittle and sessioned/cookied may reduce challenges, with account-ban risk.
  - TikTok transcript/audio/source-text behavior is not established by this packet.

## Workspace State

- Branch: `codex/ig-youtube-residual-burndown-pushable`
- Head before writing packet: `886769bc683d3162f3b00b35ee7acb8e9c7ade4d`
- Dirty or untracked state before handoff: clean relative to `origin/codex/ig-youtube-residual-burndown`
- Dirty or untracked state after writing the handoff file: this handoff file is newly untracked unless a later command stages, commits, or moves it
- Target files or artifacts: this handoff packet only
- Related worktrees or branches: root workspace branch may have unrelated dirty/untracked files; do not use it as the strict state source for this handoff without its own status read.

## Changed / Inspected / Tested Files

- `docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md`
  - Status: newly written by this lane.
  - Role: durable cold-reader handoff packet.
  - Important observations: no implementation authority; routes receiver to source refresh and gap ledger.
- `docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md`
  - Status: inspected.
  - Role: IG/YT closeout and claim boundary.
  - Important observations: IG/YT globally platform-complete remains not proven; IG residuals and YouTube ASR/no-caption residuals remain named.
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
  - Status: inspected.
  - Role: TikTok behavior/data/access/fingerprint spec.
  - Important observations: sessioned/cookied dedicated account posture supersedes logged-out-primary; synthetic signatures forbidden; page-owned requests and hard request caps matter.
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md`
  - Status: inspected.
  - Role: first TikTok technical recon.
  - Important observations: real cookied browser exposed profile/video metadata and comments via page-emitted API; detection ceiling remains unknown.
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md`
  - Status: inspected.
  - Role: live measurement plan.
  - Important observations: requires dedicated non-personal account, human login, no concurrent TikTok tabs, warm session, and stop-on-challenge.

## Frozen Decisions

- Decision: TikTok should inherit IG/YT behavioral completeness targets, not their acquisition mechanics.
  - Evidence: `shared_capture_core_ig_youtube_tiktok_planning_v0.md` and `youtube_first_behavioral_completion_spec_v0.md`.
  - Consequence: TikTok adapter owns listing route, video-detail route, page-owned request capture, access mode, session/fingerprint posture, and field semantics.
- Decision: "Most information, least fingerprinting" means page-owned, source-native, bounded capture first.
  - Evidence: TikTok spec C1-C8' and first-slice recon.
  - Consequence: read embedded page blob, intercept page-issued comment/list responses, cap comment pagination, avoid forged signatures and deep census.
- Decision: TikTok sessioned mode is allowed only under dedicated-account constraints.
  - Evidence: TikTok spec direction update and sessioned warm-probe plan.
  - Consequence: no personal account, no agent-entered credentials, no stored secrets in packets, public content only, stop on challenge.

## Mutable Questions

- Question: Is TikTok's sessioned/cookied route reliable enough for the intended volume?
  - Why still mutable: detection ceiling is explicitly unmeasured.
  - What would resolve it: owner-gated warm-session probe with a dedicated account and measured per-account ceiling.
- Question: What is TikTok's transcript/audio/source-text posture?
  - Why still mutable: loaded TikTok spec covers metadata/comments and music/textExtra, not a proven transcript or ASR lane.
  - What would resolve it: TikTok source refresh checking whether captions, speech text, audio handles, or ASR-compatible media are public and worth capturing under least-fingerprinting constraints.
- Question: Should TikTok implement now or update docs/spec first?
  - Why still mutable: existing TikTok spec may already be implementation-facing, but it predates the completed IG/YT behavioral closeout.
  - What would resolve it: TikTok behavioral gap ledger with code-enforceable vs live-probe vs doctrine-only split.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "TikTok has no technical recon at all" in older social handoffs or recon summaries.
  - Why stale or dangerous: current tree includes TikTok first-slice recon and sessioned spec/plan.
  - Current replacement: re-read `tiktok_first_slice_probe_recon_v0.md`, `tiktok_capture_lane_spec_v0.md`, and `tiktok_sessioned_capture_warm_probe_plan_v0.md`.
- Stale instruction, idea, artifact, or finding: "logged-out only is the lowest fingerprinting path."
  - Why stale or dangerous: loaded TikTok spec says logged-out is brittle and sessioned/cookied may challenge less, while adding account-ban risk.
  - Current replacement: "lowest practical fingerprinting" means bounded page-owned requests under the current source-backed access posture, not necessarily logged-out.
- Stale instruction, idea, artifact, or finding: "30/60-minute comment window is required."
  - Why stale or dangerous: TikTok lane spec drops the requirement for bot-detection purpose and uses top/relevant comment sample.
  - Current replacement: exact timestamps are useful information; chronological census is not required unless a future downstream need reintroduces it.
- Stale instruction, idea, artifact, or finding: "shared core next."
  - Why stale or dangerous: TikTok still needs source-family refresh and behavior mapping first.
  - Current replacement: TikTok source-family lane first, shared core only after IG/YT/TikTok behaviors are stable enough to extract.

## Commands And Verification Evidence

- Command:
  `git status --short --branch; git rev-parse HEAD; git branch --show-current`
  Result:
  - Passed.
  - Important output: branch `codex/ig-youtube-residual-burndown-pushable`, HEAD `886769bc683d3162f3b00b35ee7acb8e9c7ade4d`, clean before this file.
  - Re-run target: receiver should rerun before acting.
- Command:
  `rg --files | rg -i "tiktok|social_media|youtube_first|shared_capture_core|source_capture_playbook|capture_recon_index"`
  Result:
  - Passed.
  - Important output: found TikTok spec/recon/probe files and prior social handoffs.
  - Re-run target: receiver should rerun if TikTok source inventory matters.
- Command:
  `Get-Content` on the IG/YT closeout, shared planning, capture playbook, recon index, and TikTok spec/recon/probe files.
  Result:
  - Passed.
  - Important output: source basis summarized above.
  - Re-run target: receiver must reread load-bearing sources.
- Command:
  `Get-FileHash -Algorithm SHA256` on load-bearing files.
  Result:
  - Passed.
  - Important output: hashes recorded in Authority And Source Ledger.
  - Re-run target: receiver may hash-compare or simply reread current sources and treat drift as `STALE_REREAD_REQUIRED`.

## Blockers And Risks

- Blocker or risk: TikTok live probing is not authorized by this packet.
  - Evidence: handoff and TikTok plans are retrieval/planning only; live/network action requires explicit current approval.
  - Likely next action: produce source-backed gap ledger first; ask for live-probe authorization only if it becomes the bottleneck.
- Blocker or risk: sessioned capture can burn an account.
  - Evidence: TikTok spec and sessioned warm-probe plan name account-ban risk.
  - Likely next action: if probing, use only dedicated non-personal account with human login and no secret persistence.
- Blocker or risk: "most information" can conflict with "least fingerprinting."
  - Evidence: full comment census/deep pagination increases requests; TikTok spec caps comment pagination.
  - Likely next action: capture high-value page-native metadata and top/relevant comments first; make deeper capture an explicit downstream tradeoff.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - workspace branch/head/dirty state
  - IG/YT closeout current status and residuals
  - YouTube caption-route corpus status
  - capture playbook Step 0/access/receipt rules
  - recon index TikTok/social rows
  - TikTok spec direction update and C1-C8' invariants
  - TikTok first-slice recon bottom line and detection addendum
  - TikTok sessioned warm-probe preconditions and stop conditions
- Compare target for each:
  - hashes in Authority And Source Ledger, or fresh reread if hashes drift
  - fresh `git status --short --branch`
  - fresh `git rev-parse HEAD`
- Load outcomes and what each means:
  - `REUSE`: all required load-bearing facts re-verified; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional or non-load-bearing facts drifted; reuse verified parts and rederive the rest.
  - `STALE_REREAD_REQUIRED`: material source drifted but can be reread and re-derived before work.
  - `BLOCKED_DRIFT`: drift conflicts with target path, dirty-state safety, user constraints, or authority.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim has no compare target and cannot be re-derived.
- Sources that must be reread if drift is detected:
  - source-loading overlay, capture playbook, recon index, TikTok spec/recon/probe plans, and IG/YT closeout.

## Do Not Forget

TikTok should start from profile/listing grid into video detail into page-owned comment responses, preserving source-native metadata, stats, comments, timestamps, route/fingerprint/access posture, and residuals. It should not start by forging API signatures, deep-paginating comments, storing session secrets, or extracting shared core.
