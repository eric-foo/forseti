# TikTok Behavioral Sync Fresh Lane Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet
scope: >
  Cold-reader reset packet for continuing the TikTok behavioral-sync lane after
  the prior lane became noisy. Carries the same IG/YT-parity goal while making
  the next bottleneck explicit: packet-grade capture of TikTok page-owned
  comment-list response bodies, not more DOM-only probing.
use_when:
  - Starting a fresh TikTok behavioral-sync lane from the current Orca repo.
  - Recovering the source pack and drift guard before any TikTok probing or implementation.
  - Preventing repeated browser/login/DOM loops from replacing the existing TikTok and IG/YT docs.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md
  - docs/workflows/tiktok_behavioral_gap_ledger_from_ig_youtube_v0.md
  - docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_receipt_v0.md
  - docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_payload_v0.json
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md
stale_if:
  - A later TikTok live probe captures packet-grade comment-list response bodies.
  - Any named TikTok spec, recon, receipt, source-capture playbook, or recon-index file changes materially.
  - A later IG/YT behavioral closeout changes the behavioral completeness target.
  - The owner redirects from TikTok source-family behavioral sync to a different lane.
```

## Load Contract

- packet_version: workflow-handoff/max/v0
- mode: max
- source_loading_mode: repo-overlay-bound
- created_at: 2026-06-30 Asia/Singapore
- created_by_lane: Codex TikTok/IG/YT behavioral sync reset lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-youtube-residual-burndown`
- handoff_path: `docs/workflows/tiktok_behavioral_sync_fresh_lane_handoff_v0.md`
- expected_branch: `codex/ig-youtube-residual-burndown-pushable`
- expected_head_before_handoff_file: `1b0fb0c875a2fd3a6462d71b44b046cdb12faab0`
- expected_dirty_state_before_handoff_file: clean relative to `origin/codex/ig-youtube-residual-burndown-pushable`
- expected_dirty_state_after_handoff_file: one untracked handoff file at this path unless a later lane stages, commits, moves, or deletes it
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: Give Orca a TikTok creator/video capture lane with behavioral completeness comparable to the existing Instagram/YouTube behavioral lanes, preserving all source-visible creator, video, text, metadata, stats, comment, provenance, access, and residual facts that can affect creator decisions while minimizing fingerprint, account, and request-cost exposure.
- anchor_goal: Start a fresh TikTok lane from the existing TikTok plus IG/YT source pack and converge on the lowest-cost sessioned TikTok packet-grade capture shape; the immediate bottleneck is page-owned `/api/comment/list` response-body capture, not further DOM-only probing.
- success_signal:
  - Core success:
    - Owner-observable: the owner can start a new lane from one packet without repeatedly repointing the agent to the TikTok, IG, or YouTube docs.
    - Output fit: the next answer or artifact makes the TikTok information contract, source pack, blockers, first material batch, and forbidden drift unambiguous.
    - Boundary: success is not DOM-only evidence, browser relaunching, direct endpoint forging, stored cookies, CAPTCHA solving, or implementation/readiness claims by themselves.
    - Drift cue: the lane starts probing browser/login/DOM surfaces before reading the existing docs, or treats Chrome `pageAssets`/DOM as packet-grade comment evidence.
  - Secondary success signals:
    - Packet-grade proof is one sanitized page-owned response body for the pinned fixture, with exact fields and no secrets.
    - A later 5-video rung runs only after the pinned response-body proof succeeds.
  - status: user_stated

## Open Decision / Fork

- decision: Which response-body capture surface should the fresh lane use for the pinned TikTok fixture?
  - options:
    - `A_existing_harness_observation`: adapt or run the existing `fetch_browser_page_observation_capture` response observer with a sessioned context and a post-load comment-panel action.
    - `B_supported_real_chrome_network_body_surface`: use a supported real-Chrome network-body capability if one is available without raw CDP/bookmarklet workarounds or cookie/token export.
    - `C_blocked_tooling_gap`: stop and report that no currently supported surface can capture page-owned XHR/fetch bodies from the entitled TikTok session without violating guardrails.
  - already constrained / off the table:
    - No more Chrome-extension DOM probing as packet proof.
    - No raw CDP, bookmarklet, JavaScript-URL, or blocked-browser workaround.
    - No Playwright/Chrome-for-Testing Google OAuth loop.
    - No direct forged `/api/comment/list` calls, signed URL replay, signature generation, or printed raw signed URLs.
    - No personal-account session export, cookie/storage/token printout, proxy endpoint printout, or secret-bearing packet.
    - No CAPTCHA solving. If a visible challenge modal has an `X`, it may be closed with human-like mouse movement; if the source remains gated, stop.
  - trade-offs:
    - Option A is source-aligned if the session can be created or reused without repeating the failed login path; it already models response predicates and body redaction boundaries.
    - Option B may be the cleanest if the current tool surface supports it, but earlier Chrome capability probing found only `pageAssets`, not XHR/fetch bodies.
    - Option C is the correct stop if neither A nor B is available; it preserves failure visibility instead of burning more browser budget.
  - owner of the call: owner decides any live run, session/account risk, or new tool surface. Harness permission prompts remain the per-operation gate.
  - recommendation and why: choose A only after an assumption gate proves the session path and response observer are available. Otherwise choose C. Do not spend another batch on DOM-only Chrome probing.

## Drift Guard

- existing docs first:
  - why it matters: the current repo already has TikTok source-family specs, recon, receipts, and IG/YT behavioral reference docs.
  - what violating it would break: the owner will have to repoint again, and the lane will rediscover stale facts instead of compounding.
- behavioral parity, not machinery parity:
  - why it matters: IG/YT define information categories and residual posture; TikTok owns acquisition mechanics.
  - what violating it would break: copying IG grid mechanics or YouTube transcript/comment mechanics into TikTok would create fake parity.
- packet-grade comments require response bodies:
  - why it matters: DOM comment rows lack `cid`, commenter `uid`, exact `create_time`, cursor, and `has_more`.
  - what violating it would break: the lane would claim comment completeness from lower-fidelity DOM evidence.
- sessioned does not mean secret-bearing:
  - why it matters: TikTok sessioning trades CAPTCHA risk for account/session risk.
  - what violating it would break: packets would become contaminated scratch and could leak credentials, cookies, tokens, device IDs, proxy endpoints, or exit IPs.
- lowest practical fingerprinting:
  - why it matters: the target is most decision-useful source-visible information at bounded request cost.
  - what violating it would break: deep comment pagination, forged API calls, or repeated login/browser churn would increase detectability before proving value.
- old lane is orientation only:
  - why it matters: the prior lane mixed browser control surfaces, login bootstrapping, DOM scans, and response-body goals.
  - what violating it would break: the fresh lane inherits confusion instead of source-backed state.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/decision-routing.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `.agents/workflow-overlay/retrieval-metadata.md`
  - `docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md`
  - `docs/workflows/tiktok_behavioral_gap_ledger_from_ig_youtube_v0.md`
  - `docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_receipt_v0.md`
  - `docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_payload_v0.json`
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md`
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md`
  - `orca-harness/source_capture/adapters/browser_snapshot.py`
  - `orca-harness/runners/run_source_capture_browser_session_bootstrap.py`
  - `orca-harness/runners/run_source_capture_authenticated_browser_packet.py`
  - `orca-harness/source_capture/auth_state.py`
  - `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
- already loaded (weak orientation, freshness-marked; not authority): the files above were read or targeted-searched in this sender lane on 2026-06-30.
- must load first (before strict or actionable steps): `AGENTS.md`, overlay README/source-loading/decision-routing, the TikTok handoff/gap ledger/sessioned receipt/payload, capture playbook, recon index, TikTok spec/recon/warm-probe plan, and the exact harness files if the receiver will touch or run the response observer.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: TikTok inherits IG/YT behavioral completeness targets, not IG/YT acquisition machinery.
  - decided in: `docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md`
  - compare target: SHA256 `60AE53C47CD49450626618C716A50EC81854071013AA43E5A4551A840707DF62`
  - verify before: claiming the TikTok lane objective or drift guard.
- decision, framing, profile, or convention: current TikTok next move is response-body proof, because DOM/hydration is already clean enough and Chrome `pageAssets` is not a body surface.
  - decided in: `docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_receipt_v0.md`
  - compare target: SHA256 `3C5DDDCCE261B7D254CA0912BA157400DA93AD8A3358B28333CCF5B3148CEE73`
  - verify before: deciding to run more DOM-only browser probes.
- decision, framing, profile, or convention: TikTok comments are packet-grade only when the page-owned `/api/comment/list` response body yields exact fields.
  - decided in: `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md` and `tiktok_first_slice_probe_recon_v0.md`
  - compare target: SHA256 `3171F2DA3A8E67C88C6FB587490DC932F6B50A22F5C864464CE1D95B8E63666C`; SHA256 `5D9BC9FED9865E87B8C5AAED896CC86B39860E0D9E2E1738482375D7DAE9F6CC`
  - verify before: claiming `cid`, `uid`, exact comment timestamp, cursor, or `has_more`.
- decision, framing, profile, or convention: sessioned/cookied TikTok runs require a dedicated non-personal account, human login, no secrets in packets, public content only, and stop-on-challenge.
  - decided in: `tiktok_capture_lane_spec_v0.md` and `tiktok_sessioned_capture_warm_probe_plan_v0.md`
  - compare target: SHA256 `3171F2DA3A8E67C88C6FB587490DC932F6B50A22F5C864464CE1D95B8E63666C`; SHA256 `2DFC7CD9704B530EFE480FFDABCF67EEFE3B8B1AA2A454B1A83C6F9CF252C0E7`
  - verify before: any live or sessioned action.

## Active Objective

Continue only the TikTok behavioral-sync lane. The fresh lane should re-load the named sources, confirm the current state, and batch the next material step around packet-grade response-body capture for the pinned TikTok fixture before any 5-video rung or implementation claim.

## Exact Next Authorized Action

1. Load this packet, re-read the named load-bearing sources, and return a confirm-don't-trust load outcome (`REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`, `BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`).
2. Run a compact assumption gate on the response-body surface: can a supported route observe the page-owned `/api/comment/list` response body from a sessioned public TikTok page without leaking secrets, forging signatures, or using blocked browser workarounds?
3. If the assumption gate passes and live action is current-authorized in the receiving prompt/tooling, run only the pinned fixture first: `https://www.tiktok.com/@tiktok/video/7642770753292635422`.
4. Preserve only sanitized packet proof: response-body presence, body hash, exact required fields observed, request count, source URL, retrieval time, limitation notes, and no-secret confirmation. Do not print or persist raw signed URLs, cookies, tokens, storage state, proxy endpoints, exit IPs, or device IDs.
5. If the pinned proof succeeds, then and only then plan the 5-video ceiling rung from the existing profile-grid payload. If it fails, stop with the precise body-access blocker.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Orca agent behavior and project instructions.
    - Load-bearing: yes.
    - Compare target: SHA256 `AEABE784AE4B629A05E065FD7A31292716D4E9CA7931B1BD45006DDD1503F7C7`.
    - Last checked: 2026-06-30.
    - Reuse rule: re-read before strict project or lifecycle claims.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md` - SHA256 `A136775DA51F7B1B7563292660B705673B26E1A6436A08F7566C221D3B4BCF6A`.
  - `.agents/workflow-overlay/source-loading.md` - SHA256 `8FADC263B98F08B73B68E44DE71709D4AAF7FEA5D2E0390602B93E7863E11AB3`.
  - `.agents/workflow-overlay/decision-routing.md` - SHA256 `8CA8069E20C5803A1B645921ABBD986656739C943ED0996572E26A4B9430092E`.
  - `.agents/workflow-overlay/source-of-truth.md` - SHA256 `04DAF7979FDA605A2E7CF334DBC7ECADB02F8C1F1B40A432E14B4F3503235D0C`.
  - `.agents/workflow-overlay/artifact-folders.md` - SHA256 `C53876526EA781F8800A156E7969A9E21E17154E66F219C1F953FC72EDB4CA0B`.
  - `.agents/workflow-overlay/retrieval-metadata.md` - SHA256 `7CE0444850C988A1E4C74FAA07EBC696561C3874F978F7C6C6E498092F9C83D7`.
  - Role: Orca overlay entrypoint, source loading, routing, artifact placement, and retrieval header rules.
  - Load-bearing: yes.
  - Last checked: 2026-06-30.
  - Reuse rule: re-read when strict source, routing, artifact, or lifecycle claims matter.
- User constraints:
  - The fresh lane exists because the old lane became contaminated by repeated repointing, browser/login churn, and surface confusion.
  - Use the existing TikTok, IG, and YouTube docs first.
  - TikTok must be cookied/sessioned because logged-out restrictions are strong.
  - If a CAPTCHA modal has a visible `X`, closing it is allowed; solving CAPTCHA is not.
  - Do not relaunch browsers without need; prefer the already-working session surface when a supported body-capture route exists.
- Source-read ledger:
  - `docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md`
    - Role: prior TikTok behavioral-sync handoff and original goal/drift guard.
    - Load-bearing: yes.
    - Compare target: SHA256 `60AE53C47CD49450626618C716A50EC81854071013AA43E5A4551A840707DF62`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before claiming lane objective.
  - `docs/workflows/tiktok_behavioral_gap_ledger_from_ig_youtube_v0.md`
    - Role: TikTok behavioral gap ledger and current next-move decision/addendum.
    - Load-bearing: yes.
    - Compare target: SHA256 `3E2E792650F68716749D6917A5A2B2D84FC88FFAB3017B6626A59A315125CA0E`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before claiming current blocker or next batch.
  - `docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_receipt_v0.md`
    - Role: current sessioned DOM/hydration/comment-DOM evidence and Chrome body-access blocker.
    - Load-bearing: yes.
    - Compare target: SHA256 `3C5DDDCCE261B7D254CA0912BA157400DA93AD8A3358B28333CCF5B3148CEE73`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before deciding DOM is exhausted or response-body proof is next.
  - `docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_payload_v0.json`
    - Role: structured profile-grid, video hydration, and visible-comment payload.
    - Load-bearing: yes.
    - Compare target: SHA256 `E6D2F48BE360D3A4BD8E6AAC676C71418DF336A7628BB397A3C1E000E042B59B`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before using grid anchors for a 5-video rung.
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
    - Role: source-capture method, access gate, route catalog, receipt rules.
    - Load-bearing: yes.
    - Compare target: SHA256 `0B8C169F10741ABE6574CFC18A25A0C1516B45E1B30FA11F4B2C551235F62796`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before capture/probe route decisions.
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
    - Role: current recon index, including TikTok partial social row and sessioned update.
    - Load-bearing: yes.
    - Compare target: SHA256 `D5E6BB07498C59D8C77F8DBA00954B499E8B889E4C7A492B61C4D6B3215A5E1C`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before social recon status claims.
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
    - Role: TikTok data contract, fingerprint/access/session invariants, source-text boundary.
    - Load-bearing: yes.
    - Compare target: SHA256 `3171F2DA3A8E67C88C6FB587490DC932F6B50A22F5C864464CE1D95B8E63666C`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before TikTok field, session, or non-claim statements.
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md`
    - Role: first-slice route evidence and correction that API response is the comment capture target.
    - Load-bearing: yes.
    - Compare target: SHA256 `5D9BC9FED9865E87B8C5AAED896CC86B39860E0D9E2E1738482375D7DAE9F6CC`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before route or comment-field claims.
  - `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md`
    - Role: sessioned warm-probe plan, account/session preconditions, response-body bottleneck.
    - Load-bearing: yes.
    - Compare target: SHA256 `2DFC7CD9704B530EFE480FFDABCF67EEFE3B8B1AA2A454B1A83C6F9CF252C0E7`.
    - Last checked: 2026-06-30.
    - Reuse rule: verify before live/sessioned run setup.
  - `orca-harness/source_capture/adapters/browser_snapshot.py`
    - Role: response-observation seam and body redaction behavior.
    - Load-bearing: yes if using or editing harness path.
    - Compare target: SHA256 `C7378539BF6AE8AB01ADA7AC32D837844BB9FACEE2DA8C142302040E05DBC7E6`.
    - Last checked: targeted `rg` 2026-06-30.
    - Reuse rule: re-read exact function before use or patch.
  - `orca-harness/runners/run_source_capture_browser_session_bootstrap.py`
    - Role: human-login session bootstrap.
    - Load-bearing: yes if using Playwright storage-state route.
    - Compare target: SHA256 `AEF293E18D961F03D693D5B5E4D346FF4C47375673AAF9F896DEB024F310D7CF`.
    - Last checked: targeted `rg` 2026-06-30.
    - Reuse rule: re-read before invoking.
  - `orca-harness/runners/run_source_capture_authenticated_browser_packet.py`
    - Role: authenticated browser packet runner.
    - Load-bearing: yes if using Playwright storage-state route.
    - Compare target: SHA256 `4730E12CA08A03F910FEF58F057334E51B773E0D4EDDDC3CEB8993B6D56A51A2`.
    - Last checked: targeted `rg` 2026-06-30.
    - Reuse rule: re-read before invoking.
  - `orca-harness/source_capture/auth_state.py`
    - Role: ignored auth-state path and metadata validation.
    - Load-bearing: yes if using saved session state.
    - Compare target: SHA256 `1F75F1624B0702305F524048404BD4E081776A61D9E6D98868C3DEB327468B39`.
    - Last checked: targeted `rg` 2026-06-30.
    - Reuse rule: re-read before touching any auth-state artifact.
  - `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
    - Role: response-observation tests, including post-load action before DOM and response body reads.
    - Load-bearing: yes if patching browser observation seam.
    - Compare target: SHA256 `7E0985BC4910EE149E8D75771EA66B1362BA2AF7EE2E5305E85A59954A853AEB`.
    - Last checked: targeted `rg` 2026-06-30.
    - Reuse rule: re-read and run relevant tests before patch completion claims.
- Source gaps:
  - No sessioned `/api/comment/list` response body has been captured.
  - No exact sessioned comment `cid`, `uid`, `create_time`, cursor, or `has_more` proof exists.
  - No per-account ceiling run exists.
  - No TikTok transcript, source-native caption, ASR, durable audio, or durable video proof exists.
  - The current Chrome extension surface is not a response-body surface.
- Strict-only blockers:
  - Live TikTok action needs current owner/live authorization in the receiving lane plus any harness/network permission prompts.
  - Personal account/session export is forbidden.
  - Raw signed URLs, cookies, tokens, storage state, proxy endpoints, exit IPs, and device IDs must not enter durable packets.
- Not-proven boundaries:
  - not TikTok validation/readiness
  - not implementation authorization
  - not per-account ceiling proof
  - not packet-grade comments
  - not legal advice

## Cynefin Routing

Smallest complete outcome: reset the TikTok lane into a source-backed response-body-capture batch, with a fresh-reader packet that prevents redoing stale browser/login/DOM work.

Regime: Complex.

Why: the desired information contract is clear, but the working response-body surface under a cookied TikTok session is still uncertain and can change the next technical route.

Decomposition: risk-first probe after source reload; resolve the response-body surface before any broader 5-video rung or implementation work.

Current bottleneck: supported access to the page-owned `/api/comment/list` response body without secrets, signature forging, or blocked browser workarounds.

Riskiest assumption: an available supported harness/browser route can observe page-owned XHR/fetch response bodies in the sessioned TikTok context.

Stop or pivot condition: no supported body surface, visible challenge that remains after dismissing a modal `X`, secret exposure risk, or a login path that repeats the Chrome-for-Testing OAuth failure.

Allowed next move: source reload plus assumption gate, then pinned response-body proof if authorized and supported.

Disallowed next move: more DOM-only probing, browser relaunch churn, direct signed endpoint calls, CAPTCHA solving, personal-account export, or a 5-video rung before pinned packet proof.

## Current Task State

- Completed:
  - Prior TikTok behavioral handoff and gap ledger exist.
  - Sessioned profile/grid, video hydration, and visible comment DOM were captured for the locked `@tiktok` fixture.
  - Existing Chrome follow-up confirmed clean rendering but only `pageAssets` capability, not XHR/fetch bodies.
  - TikTok source-family spec and warm-probe plan now name response-body capture as the remaining packet bottleneck.
- Partially completed:
  - Pinned fixture is ready for packet-grade response-body proof.
  - Profile payload contains enough anchors for a later 5-video rung, but that rung is premature until pinned proof succeeds.
- Broken or uncertain:
  - Old lane context mixed DOM, session bootstrap, response capture, and login mechanics.
  - The Playwright/Chrome-for-Testing login path hit Google OAuth rejection and should not be repeated as the default.
  - Saved/local auth-state artifacts, if present, are ignored local secret-adjacent artifacts and must not be printed or treated as packet evidence.

## Workspace State

- Branch: `codex/ig-youtube-residual-burndown-pushable`
- Head before writing packet: `1b0fb0c875a2fd3a6462d71b44b046cdb12faab0`
- Dirty or untracked state before handoff: clean relative to `origin/codex/ig-youtube-residual-burndown-pushable`
- Dirty or untracked state after writing the handoff file: this handoff file is newly untracked unless a later command stages, commits, moves, or deletes it
- Target files or artifacts: this handoff packet only
- Related branches: remote `origin/codex/ig-youtube-residual-burndown-pushable` already contains the previous TikTok receipt/gap-ledger updates at head `1b0fb0c875a2fd3a6462d71b44b046cdb12faab0`

## Changed / Inspected / Tested Files

- `docs/workflows/tiktok_behavioral_sync_fresh_lane_handoff_v0.md`
  - Status: newly written by this lane.
  - Role: durable cold-reader reset packet.
  - Important observations: records why the next lane must start from sources and response-body proof.
- `docs/workflows/tiktok_behavioral_gap_ledger_from_ig_youtube_v0.md`
  - Status: inspected.
  - Role: latest TikTok behavior-sync ledger and addendum.
  - Important observations: current next move is pinned response capture, not more DOM.
- `docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_receipt_v0.md`
  - Status: inspected.
  - Role: live receipt for sessioned DOM/hydration evidence and Chrome blocker.
  - Important observations: DOM is useful but lower fidelity; Chrome `pageAssets` is not a response-body route.
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
  - Status: inspected.
  - Role: TikTok capture contract.
  - Important observations: comments require page-owned `/api/comment/list` interception; forged signatures and secret persistence are forbidden.
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md`
  - Status: inspected.
  - Role: sessioned runbook and warm-probe plan.
  - Important observations: harness fit names `fetch_browser_page_observation_capture`; current receipts did not capture bodies.
- `orca-harness/source_capture/adapters/browser_snapshot.py`
  - Status: targeted search only, not full implementation review.
  - Role: candidate response-observation surface.
  - Important observations: `fetch_browser_page_observation_capture` and observed response body reading are present; re-read before use or patch.

## Frozen Decisions

- Decision: TikTok behavioral parity means same decision-useful information posture as IG/YT, not copied acquisition mechanics.
  - Evidence: prior TikTok handoff and gap ledger.
  - Consequence: TikTok owns its sessioned/cookied, page-owned request, comment-body route.
- Decision: DOM-only comment evidence is not packet-grade for TikTok comments.
  - Evidence: sessioned DOM/hydration receipt and TikTok spec/recon.
  - Consequence: exact comment IDs/timestamps/cursors require response-body capture.
- Decision: `/api/comment/list` is the page-owned web endpoint target, not a public API to call directly.
  - Evidence: sessioned receipt and first-slice recon.
  - Consequence: let the page issue the request and observe the response; do not forge or replay signatures.
- Decision: sessioned/cookied access uses a dedicated account, human login, public content only, no secrets in packets, stop-on-challenge.
  - Evidence: TikTok spec C8' and sessioned warm-probe plan.
  - Consequence: no personal account, no agent-entered credentials, no cookie/token dumps, no CAPTCHA solving.

## Mutable Questions

- Observation: TikTok grid `video_id` / `aweme_id` values appear to be Snowflake-like IDs whose high bits encode a Unix timestamp (`decoded_aweme_id_create_time_utc = int(video_id) >> 32`).
  - Evidence observed in the Funmi Monet grid probe on 2026-06-30: grid link `/@funmimonet/video/7655162561783975199` decodes to `2026-06-25T03:00:26Z`; the captured first comment for the same video had `create_time` `2026-06-25T03:27:14Z`, which is plausibly after post creation.
  - Consequence: every grid-visible TikTok video link can carry a high-confidence derived post-time candidate without opening the video page.
  - Source-strength rule: record this as `decoded_aweme_id_create_time_utc` derived from visible grid video ID until cross-checked against page-owned item/detail JSON for at least one target; do not present it as TikTok-confirmed `create_time` without that cross-check.
  - Boundary: this does not expose comments, comment cursors, likes/diggs/shares/saves, or transcript. Those still require page-owned response/hydration or video/detail surfaces.

- Observation: A sessioned Funmi Monet profile/grid response probe found stats-bearing page-owned list responses without opening individual video pages.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_grid_response_probe_20260630T145319Z\result.json`: run status `complete`; 22 sanitized response summaries; 97 unique extracted item candidates; 91 carried `playCount`, `diggCount`, `commentCount`, `shareCount`, `collectCount`, and exact `createTime`.
  - Source surface: extracted stats came from page-owned `/api/post/item_list/` and `/api/repost/item_list/` responses, with raw response bodies excluded and response/url hashes retained.
  - Consequence: for a creator grid/listing batch, likes/diggs, comment counts, shares, saves/collects, play counts, and exact post `createTime` may be captured from profile/list responses before entering each video detail page.
  - Source-strength rule: call this `profile_list_response_stats`, not rendered DOM proof; parser work must de-duplicate/reconcile post vs repost rows and discard stray non-video-looking IDs before making packet claims.
  - Boundary: this still does not expose comment bodies, `cid`, commenter `uid`, comment `create_time`, comment cursor, `has_more`, transcript, or audio. Those remain separate page-owned comment-list/video-detail/media questions.

- Observation: A sessioned Funmi Monet grid audio/comment-body probe found audio-bearing muted previews but no UI-level grid unmute control and no comment bodies in the profile/list responses.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_grid_audio_comment_probe_20260630T161553Z\result.json`: run status `complete`; 22 sanitized response summaries; 91 post items with stats; 5 hovered grid previews; all 5 were playing and muted; all 5 had positive `webkitAudioDecodedByteCount`; no visible mute/sound/volume UI controls were found or clicked.
  - Comment-body result: sanitized in-memory JSON scanning found `comment_like_object_count=0` and `comment_text_body_candidate_count=0`; observed comment-related keys were count/status/settings fields such as `commentCount`, `commentSetting`, `itemCommentStatus`, not comment text bodies.
  - Consequence: grid hover previews likely carry audio media, but the current grid UI route does not expose an obvious source-visible unmute action; transcription from grid would need a separate, explicitly scoped media/audio capture route, not just profile/list JSON.
  - Source-strength rule: record this as `grid_preview_audio_present_muted_no_ui_unmute_observed`, not as proof that TikTok never exposes grid audio controls across all layouts/accounts.
  - Boundary: this does not supersede `/api/comment/list`; actual comment bodies and packet-grade comment fields still require opening/triggering the page-owned comment-list response.

- Observation: A known Funmi Monet paid-partnership video was detectable from the profile/grid page-owned list response, even though the rendered grid card did not visibly show the paid label.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_paid_partnership_probe_20260630T162414Z\result.json` for video `7629774409762442526`: target appeared in profile phase `/api/post/item_list/` with body hash/byte count retained; the target item carried `isAd=True` and `adLabelVersion=2`; target node keys also included ad/branded-adjacent fields such as `adAuthorization` and `BAInfo`.
  - Cross-check: direct video-detail DOM scan showed visible `Paid partnership` / `sponsored-tag` labels for the same target, while profile-grid DOM scans had `target_card_contains_paid_terms=False`.
  - Consequence: paid-partnership/ad disclosure can be captured from grid/list response metadata before opening each video, if the target item is present in the profile/list batch.
  - Source-strength rule: call this `profile_list_response_ad_disclosure_candidate` until parser fixtures define the exact normalized field contract; prefer `isAd=True` plus response provenance over hashtag-only inference.
  - Boundary: this does not mean every sponsorship/FTC disclosure is reliably encoded as `isAd`; hashtags like `#partner` remain separate source-text signals and should not be collapsed into the platform ad-disclosure flag.

- Observation: Sponsor/partner hashtag source-text signals are also available from the profile/grid page-owned list response when the target item is present.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_paid_partnership_probe_20260630T162414Z\result.json` for video `7629774409762442526`: the profile phase `/api/post/item_list/` target item exposed `challenges[].title=burberrypartner` and `textExtra[].hashtagName=burberrypartner`; direct video-detail DOM cross-check showed visible `#BurberryPartner`.
  - Consequence: `#partner`-style hashtag/source-text signals can be collected at grid/list-response stage before opening each video, alongside `desc`/`textExtra`/music metadata, if the profile/list item is in the fetched batch.
  - Source-strength rule: keep hashtag disclosure signals separate from platform ad-disclosure fields. A hashtag such as `#partner` or `#BurberryPartner` is source text; `isAd=True` / `adLabelVersion` is a platform disclosure candidate.
  - Boundary: hashtags are creator-authored or source-visible text signals and are not proof that TikTok rendered a paid-partnership label; do not collapse hashtag-only evidence into `isAd`.

- Working model: TikTok now looks similar to IG only at the high-level capture shape: profile/list grid first, then per-video/reel capture for deep fields.
  - Grid/list response stage can carry `video_id`, decoded ID time, exact `createTime`, counts/stats, caption/description source text, hashtags/textExtra, music, and platform ad-disclosure candidates.
  - Per-video/reel stage is still required for comment bodies and packet-grade comment fields via page-owned `/api/comment/list`: `cid`, `text`, comment `create_time`, `digg_count`, `reply_comment_total`, `user.uid`, `user.unique_id`, cursor, `has_more`, and total.
  - Transcript/source-native caption status is not yet proven. The paid-partnership target's item node showed a `video.subtitleInfos` key, but no subtitle payload or transcript route has been validated; this should be probed in the per-video capture pass without persisting raw media URLs or subtitle URLs.
  - Source-strength rule: call the next step `per_video_comment_and_subtitle_probe`, not an IG-equivalent transcript implementation. TikTok owns selectors, request triggers, subtitle fields, audio/media boundaries, and residuals.
  - Boundary: do not use grid hover audio/media as the transcript route unless a separate owner-approved media/audio capture decision is made; comments remain response-body proof, not rendered DOM proof.

- Observation: The first N=1 per-video Funmi proof captured packet-grade comment bodies from the page-owned comment-list response.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_per_video_comment_subtitle_probe_20260630T163312Z\result.json` for video `7629774409762442526`: response listener attached before navigation; UI clicked `[data-e2e='comment-icon']`; one `/api/comment/list` response was observed; status `complete`; body present with SHA256 `81ac7038b3f91bc5327ed1b3840eeb1ac940e45bf219faf884de834b9a661bec`; `body_byte_count=122119`; JSON parse succeeded.
  - Comment contract observed: 20 comments; `cursor=20`; `has_more=1`; `total=304`; all 20 stored comments carried `cid`, exact `text`, `create_time`, `digg_count`, `reply_comment_total`, `user.uid`, `user.unique_id`, and `user.nickname` in source order.
  - Consequence: the per-video/reel comment route is packet-grade for this fixture using page-owned response interception, and can now be shaped into a small batch runner after parser/receipt fixtures are defined.
  - Source-strength rule: call this `per_video_comment_list_body_proof_n1`; it proves the route for this session/fixture, not per-account ceiling or all-video reliability.
  - Boundary: raw comment response bodies and raw signed endpoint URLs were not persisted; exact public comment texts were stored as parsed fields in the staging artifact because `text` is part of the TikTok comment packet contract.

- Observation: The same per-video proof found a source-native subtitle candidate but did not capture transcript/subtitle body text through UI-owned page requests.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_per_video_comment_subtitle_probe_20260630T163312Z\result.json`: hydration found `video.subtitleInfos` with one item: `Format=webvtt`, `LanguageCodeName=eng-US`, `Source=ASR`, `Size=1106`, `Version=1:whisper_lid`, and a sanitized subtitle `Url` hash only. A follow-up UI caption probe in `F:\orca-data-lake\.staging\tiktok_funmi_caption_ui_probe_20260630T163533Z\result.json` found no visible caption/subtitle/settings controls, no visible caption text, no `textTracks`, and no page-owned WebVTT response body.
  - Consequence: TikTok can expose ASR/WebVTT subtitle metadata in the video item, but the validated route has not yet captured the transcript body without directly fetching the subtitle URL.
  - Source-strength rule: call this `subtitle_metadata_candidate_no_body_capture`; do not claim transcript capture until a page-owned subtitle response body or an explicitly approved subtitle-file fetch route is validated.
  - Boundary: no raw subtitle URL, raw media URL, raw subtitle body, cookies, or tokens were persisted.

- Transcript acquisition ladder for the next probe:
  - Tier 1: `source_native_subtitle_webvtt`. Use the already observed `video.subtitleInfos` metadata from page hydration. Admit the WebVTT body only through a bounded subtitle-file route that records source video id, subtitle metadata fields, subtitle URL hash, body byte count, body SHA256, parsed cue text, cue timings if present, retrieval time, and no-secret confirmation. Do not persist raw subtitle URL, raw signed media URL, cookies, tokens, or request headers.
  - Tier 1 success signal: parsed WebVTT/body text exists for the target video, with body hash and subtitle metadata tying it back to TikTok hydration. Label provenance as TikTok source-native subtitle metadata with `Source=ASR` when that is the source field; do not label it as owner-generated ASR.
  - Tier 1 blocker: subtitle metadata absent, URL expired/inaccessible, direct subtitle fetch judged outside the current guardrail, response body unavailable, or subtitle body is empty/unparseable.
  - Tier 2: `visible_caption_overlay`. If Tier 1 cannot be admitted, try to observe rendered caption overlay during playback through UI/DOM/screenshot timing. This is confirmation or fallback extraction only; it is viewport/layout brittle and should preserve cue text/timing confidence separately from source-native subtitle files.
  - Tier 2 success signal: visible caption text is captured across playback windows with timestamps/frame offsets and enough coverage to reconstruct spoken text, labeled as rendered-overlay capture.
  - Tier 2 blocker: no visible caption controls/overlay in the browser layout, inconsistent timed rendering, or extraction requires raw media beyond the approved route.
  - Tier 3: `derived_asr_transcript`. If source-native subtitle and rendered-overlay routes fail or are absent, perform owner-approved ASR from media/audio bytes. This is the highest-cost fallback and must be labeled as derived, not TikTok-native.
  - Tier 3 success signal: transcript text with ASR engine/version, media/audio provenance, confidence/residuals, and explicit label `derived_asr_transcript`.
  - Tier 3 blocker: media/audio capture not approved, media bytes inaccessible, account/fingerprint risk too high, or storage/provenance rules are not defined.
  - Smallest next test: run Tier 1 only on video `7629774409762442526`, because hydration already exposed `subtitleInfos`. If Tier 1 succeeds, do not run Tier 2/3 for that fixture. If Tier 1 fails, record the exact blocker before escalating.

- Observation: Tier 1 source-native subtitle admission succeeded for the Funmi paid-partnership fixture.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_tier1_subtitle_webvtt_probe_20260630T164813Z\result.json` for video `7629774409762442526`: status `complete`; fetch method `page_fetch`; fetch status `200`; subtitle URL SHA256 `b8024596878db98375ad33d9cd4972f7330685302f2d41ba2da73db83b215cad`; body byte count `1106`; body SHA256 `06bebc49bd509289d11418848e4e7641c475dc3df158fce0de6087e3e6c223fe`; parsed as WebVTT with 15 cues and transcript text SHA256 `93d47995271478e2fa427ca691fca1624e9cbe6a99f483111c32a9720ebdf14a`.
  - Subtitle metadata: hydration exposed one `subtitleInfos` item with `Format=webvtt`, `LanguageCodeName=eng-US`, `LanguageID=2`, `Size=1106`, `Source=ASR`, and `Version=1:whisper_lid`; raw subtitle URL was not persisted.
  - Consequence: for this fixture, the lowest-cost transcript route is validated as `source_native_subtitle_webvtt`; Tier 2 visible-caption overlay and Tier 3 derived ASR are unnecessary for this video.
  - Source-strength rule: label transcript provenance as TikTok source-native subtitle metadata with source field `ASR`, not as owner-generated ASR. Parsed cue text/timing is admissible; raw subtitle body and raw URL remain excluded.
  - Boundary: response header reported content type `video/mp4` while the body parsed as WebVTT, so implementation should validate subtitle body shape and hydration metadata instead of relying on content-type alone. This N=1 proof does not establish all-video subtitle coverage or expiry behavior.

- Observation: A conservative N=5 Funmi per-video cadence pilot succeeded for both comment bodies and source-native subtitles.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_n5_comment_subtitle_cadence_probe_20260630T165301Z\result.json`: 5 attempted, 5 completed, 0 challenges, no stop reason, cadence sleep range `45-75` seconds between videos.
  - Comment route rate: `5/5` videos produced one page-owned `/api/comment/list` response with parsed comment bodies and packet fields. Comment response body hashes were retained per video; raw response bodies and raw endpoint URLs were not persisted.
  - Subtitle route rate: `5/5` videos had source-native subtitle metadata and successful WebVTT body admission through the Tier 1 route. Cue counts observed across the five videos were `23`, `64`, `34`, `23`, and `77`.
  - Consequence: the current Funmi/session path supports the intended workflow shape at N=5: grid/list response for candidate metadata, then per-video comment-list body plus source-native WebVTT transcript capture.
  - Source-strength rule: call this `n5_cadence_pilot_clean`, not a 30-video rate estimate or account ceiling. Use it to justify the next rung, not to claim stable scale.
  - Boundary: this was one account/session, one creator, one short run, and no challenge; it does not establish N=30 survivability, cross-creator coverage, subtitle coverage for all TikToks, or long-run account safety.

- Observation: The N=25 remaining Funmi per-video cadence rung completed cleanly and turned the N=5 pilot into a 30-video rate estimate.
  - Evidence observed in `F:\orca-data-lake\.staging\tiktok_funmi_n25_remaining_comment_subtitle_cadence_probe_20260630T170246Z\result.json`: offset `5`; requested `25`; attempted `25`; completed `25`; failed `0`; challenges `0`; stop reason empty; cadence sleep range `75-120` seconds.
  - N=25 comment route rate: `25/25` videos produced one page-owned `/api/comment/list` response with parsed comment bodies and packet fields. Raw comment response bodies and raw endpoint URLs were not persisted.
  - N=25 subtitle route rate: `21/25` videos had Tier 1 source-native WebVTT subtitle success. The 4 misses had `item_found=True` but `subtitle_info_count=0`, while comments still succeeded; they are best classified as `no_subtitleInfos_present`, not subtitle fetch failures.
  - Combined N=30 rate from the N=5 pilot plus N=25 remaining rung: comments `30/30`; source-native subtitles `26/30`; challenges `0/30`; run scope one creator/session/account and one short time window.
  - Consequence: for Funmi under this session, the workflow shape is now measured at 30 videos: grid/list metadata first, then per-video comment body capture plus Tier 1 subtitle capture where `subtitleInfos` exists.
  - Source-strength rule: call this `n30_funmi_cadence_rate_estimate`, not a general TikTok guarantee or account ceiling. The subtitle denominator should separate `subtitleInfos` presence (`26/30`) from WebVTT fetch success when present (`26/26`).
  - Boundary: this does not prove cross-creator subtitle coverage, long-run account safety, or higher-volume survivability. Next scale rung should only proceed with an explicit stop-on-challenge guard and a reason to spend account/session budget.

- Question: Which supported response-body surface is available to the fresh lane?
  - Why still mutable: Chrome extension probing found only assets; harness route exists but must be re-read and fit to the available session path.
  - What would resolve it: assumption gate plus a pinned fixture run or a precise tooling blocker.
- Question: Can the sessioned route be used without repeating failed login/browser-launch loops?
  - Why still mutable: Chrome-for-Testing Google OAuth failed; existing Chrome rendered cleanly but did not expose bodies.
  - What would resolve it: a supported session reuse/bootstrap path that does not export secrets or hit OAuth rejection.
- Question: What is the sessioned per-account ceiling?
  - Why still mutable: no 5/20/50/100 rung has run.
  - What would resolve it: after pinned packet proof, run the owner-gated 5-video rung first, then escalate only if clean.

## Superseded / Dangerous-To-Reuse Context

- Stale or dangerous context: "We need a full new TikTok probe from scratch."
  - Why stale or dangerous: current repo already has TikTok handoff, gap ledger, spec, recon, warm-probe plan, sessioned receipt, and payload.
  - Current replacement: re-read the named docs first; strict claims require source confirmation.
- Stale or dangerous context: "DOM did not expose fields, so keep probing DOM/React objects."
  - Why stale or dangerous: the docs already say DOM is lower fidelity and missing `cid`, `uid`, exact `create_time`, cursor, and `has_more`.
  - Current replacement: move to response-body capture or stop with body-access blocker.
- Stale or dangerous context: "Chrome pageAssets might be enough."
  - Why stale or dangerous: the receipt says `pageAssets` inventories scripts/images/styles/fonts/video assets, not XHR/fetch response bodies.
  - Current replacement: use a supported response-body surface only.
- Stale or dangerous context: "Try another Playwright login."
  - Why stale or dangerous: Chrome-for-Testing Google OAuth was rejected as insecure, and repeated relaunches wasted budget.
  - Current replacement: avoid login loops; use existing session surfaces only if supported and non-secret-bearing.
- Stale or dangerous context: "Call `/api/comment/list` directly."
  - Why stale or dangerous: the TikTok target is the page-owned signed request body, not a forged direct API call.
  - Current replacement: observe the browser page's request/response.
- Stale or dangerous context: old chat memory as authority.
  - Why stale or dangerous: the prior lane was noisy enough that the owner had to repoint repeatedly.
  - Current replacement: packet plus confirm-don't-trust source reload.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed.
  - Important output before writing: `## codex/ig-youtube-residual-burndown-pushable...origin/codex/ig-youtube-residual-burndown-pushable`
  - Re-run target: receiver should rerun before acting.
- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed.
  - Important output: `1b0fb0c875a2fd3a6462d71b44b046cdb12faab0`
  - Re-run target: receiver should rerun before strict workspace claims.
- Command:
  ```powershell
  rg --files | rg "(ig|instagram|youtube|tiktok).*behavior|behavior.*(ig|youtube|tiktok)|source_capture_playbook|capture_recon_index|tiktok_.*(capture|probe|receipt|payload|handoff|ledger)"
  ```
  Result:
  - Passed.
  - Important output: found the TikTok handoff, gap ledger, sessioned receipts/payload, IG/YT behavioral docs, source-capture playbook, recon index, and TikTok source-family specs.
  - Re-run target: receiver should rerun if source inventory matters.
- Command:
  ```powershell
  Get-Content -Raw <named source files>
  ```
  Result:
  - Passed for the main overlay, TikTok, capture-method, and selected harness sources named in the ledger.
  - Important output: current blocker is response-body capture, not DOM/hydration.
  - Re-run target: receiver must reread load-bearing sources.
- Command:
  ```powershell
  Get-FileHash -Algorithm SHA256 <named source files>
  ```
  Result:
  - Passed.
  - Important output: hashes recorded in the Authority And Source Ledger.
  - Re-run target: receiver may hash-compare or reread current source and treat material drift as `STALE_REREAD_REQUIRED`.

## Blockers And Risks

- Blocker or risk: no supported response-body surface may be available against the current session.
  - Evidence: Chrome extension surface exposed only `pageAssets`; page eval lacked usable resource timing.
  - Likely next action: assumption gate; use harness body observer only if it can run without violating auth/session guardrails.
- Blocker or risk: sessioned capture can burn an account.
  - Evidence: TikTok spec and warm-probe plan.
  - Likely next action: only dedicated non-personal public-content session; stop on challenge.
- Blocker or risk: response-body proof can leak secrets if handled carelessly.
  - Evidence: TikTok signed request surfaces include token/signature/fingerprint-sensitive query/header/session material.
  - Likely next action: preserve sanitized proof only; no raw signed URLs or secrets.
- Blocker or risk: the fresh lane may overcorrect into planning-only.
  - Evidence: the owner wants big steps, disciplined batches, and same goal.
  - Likely next action: after source reload and assumption gate, execute the pinned proof if current authorization and tool support exist.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - branch, head, and dirty state
  - this packet path and readability
  - TikTok goal/drift guard in the prior handoff
  - current next-move addendum in the gap ledger
  - sessioned DOM/hydration receipt and payload
  - TikTok spec field contract and C8' session rules
  - first-slice recon explanation of `/api/comment/list`
  - warm-probe plan harness fit and stop conditions
  - harness response-observation functions if using or editing code
- Compare target for each:
  - hashes in the Authority And Source Ledger, fresh file reads, fresh `git status --short --branch`, and fresh `git rev-parse HEAD`
- Load outcomes and what each means:
  - `REUSE`: all required load-bearing facts reverified; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional or non-load-bearing facts drifted; reuse verified parts and rederive the rest.
  - `STALE_REREAD_REQUIRED`: material source drifted but can be reread and re-derived before work.
  - `BLOCKED_DRIFT`: drift conflicts with target path, dirty-state safety, user constraints, or authority.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim has no compare target and cannot be re-derived.
- Sources that must be reread if drift is detected:
  - overlay source-loading and decision-routing
  - prior TikTok handoff, gap ledger, sessioned receipt, payload
  - capture playbook, recon index, TikTok spec/recon/warm-probe plan
  - harness response-observation/session files if using code

## Do Not Forget

The next compounding proof is narrow: one pinned TikTok video, one page-owned comment-list response-body proof, sanitized fields and body hash, no secrets. A 5-video rung, implementation patch, or broader capture only comes after that proof or an explicit blocker.
