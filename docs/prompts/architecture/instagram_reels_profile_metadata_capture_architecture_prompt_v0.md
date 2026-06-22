```yaml
retrieval_header_version: 1
artifact_role: Orca architecture-planning prompt
scope: >
  Architecture planning for an Instagram public creator grid capture spine: high-cadence `/reels/`
  traction plus lower-cadence static/profile-grid companion capture, joined with creator profile
  metadata, captions, timestamps, engagement, and ad-signal fields while preserving source provenance
  and conflict visibility.
use_when:
  - Commissioning a read-only architecture planning pass before implementation scoping.
  - Deciding the core/satellite boundary for IG creator profile snapshot plus reel media and static comparison records.
  - Comparing DOM-grid, passive page-load JSON, and viewport/zoom implications without executing a runner patch.
authority_boundary: prompt_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/safety-rules.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_reel_viewcount_capture_feasibility_recon_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_wind_caller_capture_feasibility_recon_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
stale_if:
  - A newer IG creator-grid/profile metadata probe supersedes the listed scratch/test-run evidence.
  - The current user redirects from architecture planning into implementation, live capture, or ad classification.
  - Source Capture Armory or IG source-family docs are patched after this prompt is written.
```

# Instagram Creator Grid Metadata Capture Architecture Prompt

## Orca Prompt Preflight

- Output mode: `file-write` for this prompt artifact; receiving architecture pass output is `chat-only` unless the operator explicitly requests a filed architecture report.
- Template kind: `none`; architecture prompt authored directly under Orca prompt contract.
- Edit permission: `read-only`; no file edits, no runner patch, no live capture, no commit, no push.
- Targets: IG-only capture-spine architecture for public creator profile snapshot plus high-cadence reel records and lower-cadence static/profile-grid comparison records.
- Branch/workspace: use the current Orca workspace supplied by the operator; verify current branch and dirty state before making strict repo claims.
- Reviews: not a review prompt; do not emit review findings or formal verdicts.
- Doctrine change: do not change doctrine. If a doctrine change appears necessary, return a blocker instead of patching sources.
- Prompt artifact path: `docs/prompts/architecture/instagram_reels_profile_metadata_capture_architecture_prompt_v0.md`.

## Executor Target

Produce a read-only target architecture for the IG public creator grid capture spine: high-cadence reels plus lower-cadence static/profile-grid companion capture.

Done looks like: a later implementation-scoping pass can implement the capture record shape, field-provenance policy, and reels/static separation without re-deciding whether the core is DOM-first, JSON-first, or hybrid.

## Mandatory Method Handling

REFERENCE-LOAD `workflow-architecture-planning` if it is available in the receiving environment. Do not APPLY it yet.

Then SOURCE-LOAD the task sources listed below. Declare exactly one:

- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

Only after that declaration, APPLY architecture planning in `standard` profile.

Use three advisory perspectives. If the environment supports subagents, launch three standard advisory subagents:

1. Directional architecture lane.
2. Adversarial architecture lane.
3. Grounding architecture lane.

If subagents are unavailable or unsafe in the environment, run the three perspectives locally and disclose the fallback. Advisory perspectives are inputs only, not verdicts.

Each advisory lane must return this terse schema, one line per field:

```text
perspective:
architecture_recommendation:
strongest_reason:
strongest_risk:
core_boundary:
satellite_boundary:
viewport_zoom_position:
provenance_conflict_position:
not_proven:
source_cites:
```

Every load-bearing source claim needs a local file/path cite when available. Use `unknown` for absent fields.

## Required Source Pack

Read:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_reel_viewcount_capture_feasibility_recon_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_wind_caller_capture_feasibility_recon_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md`

Use these local diagnostic artifacts as evidence-only, not validation:

- `orca-harness/_test_runs/ig_vanzz_reels_json_ad_metadata_20260622_1/summary.json`
- `orca-harness/_test_runs/ig_cloakbrowser_jeremyfragrance_reels_20260622_1/summary.json`
- `orca-harness/_test_runs/ig_cloakbrowser_jeremyfragrance_reels_20260622_1/1920x4000/joined_rows.json`
- `orca-harness/_test_runs/ig_jeremyfragrance_reels_zoom_matrix_20260622_1/summary.json`

Do not bulk-read unrelated `_test_runs/`. Do not read cookies, storage-state JSON, proxy endpoints, raw media bytes, or raw third-party response bodies.

If `ig_profile_grid_dom_engagement_recon_and_spec_v0.md` or any listed `_test_runs/` artifact is absent in the receiving worktree, do not substitute the older merged IG docs as proof of the 2026-06-22 observations. Declare `SOURCE_CONTEXT_INCOMPLETE` for the missing raw evidence, then use the capsule below as operator-supplied directional context for a bounded architecture amendment recommendation only. The capsule is enough to avoid a greenfield re-litigation; it is not validation or production readiness evidence.

## Cross-Worktree Evidence Capsule

This prompt may be run outside the originating workspace where the 2026-06-22 scratch artifacts were produced. In that case, carry these observations as the net-new delta to compare against the merged IG baseline sources:

- Public creator `/reels/` page, logged-out proxy, no hover/click: Vanzz at `768x1024` and `1080x1920` yielded 12 DOM reel anchors and 12 parsed grid rows with visible view counts plus hidden like/comment numeric leaves. The first 12 shortcodes matched across both viewports. A very large `5204x4728` viewport redirected to login and yielded 0 anchors.
- Vanzz `/api/v1/clips/user/` page-load JSON returned the same 12 target shortcodes with exact timestamps, engagement counts, and ad-signal-capable fields. Example timestamps included `DZz48C2hkI5` at `2026-06-20T14:19:02Z`, `DZx0y8jBw-q` at `2026-06-19T19:05:19Z`, and `DZXDTz5BuIW` at `2026-06-09T09:31:46Z`. The pinned/older-looking `C7dGMB_hY3n` dated to `2024-05-27T02:10:12Z`.
- Jeremy Fragrance CloakBrowser probe: `1080x1920` produced 12 DOM anchors, 12 parsed rows, 12 network media records, and 10 joined metadata records. `1920x4000` still produced only 12 DOM anchors and 12 parsed rows, but passive network media records increased to 30 and joined metadata to 12.
- In the Jeremy probe, `/api/v1/clips/user/` matched grid-visible reel views for sampled rows, while `/api/v1/users/web_profile_info/` sometimes carried lower video/play counts for the same shortcode. Therefore source provenance and conflict policy are core requirements; do not collapse all "view" fields into one unqualified value.
- Passive JSON/network records can carry shortcode, permalink path, timestamp, caption text, product type, like/comment/view counts, `is_paid_partnership`, `is_affiliate`, and sponsor-user candidates. Preserve these as ad-signal fields only; do not classify ads.
- Browser zoom is not proven as a steady-state route. Playwright keyboard zoom and CDP page-scale checks did not reproduce manual Chrome zoom-out behavior cleanly, so zoom remains excluded unless a later real-browser/manual-control probe proves it.
- The architecture decision should be an amendment to the existing shortcode-keyed hybrid capture spine, not a fresh identity/provenance/record-shape architecture. Add creator profile snapshot fields such as follower count, bio, display name, external URL, and capture URL/timestamp when present in DOM or passive JSON.

## Current Working Facts To Verify, Not Trust

Treat these as hypotheses until confirmed from the sources above:

- The useful core join key is Instagram media shortcode, present in both permalink paths and page-load JSON records.
- DOM grid rows can expose visible views and hidden likes/comments in the observed shape, but code must preserve raw hidden numeric leaves and mark parse status.
- Passive page-load JSON can expose timestamp, caption, view/play count, like count, comment count, product type, and ad-signal fields.
- `/api/v1/clips/user/` matched grid-visible views in the Jeremy CloakBrowser run; `/api/v1/users/web_profile_info/` sometimes carried lower video/play counts, so field-source provenance matters.
- Zoom is not currently a stable automation route: Playwright keyboard zoom did not reproduce manual Chrome zoom, and the zoom-matrix diagnostic was not a clean positive result.
- Larger viewport may increase passive JSON/media records in some runs, but it did not reliably increase rendered DOM rows and should not be treated as a core invariant unless the source evidence proves it.
- Follower count, bio, display name, external URL, and creator-level metadata should be considered part of the creator profile snapshot if visible in DOM or passive JSON.

## Architecture Questions

Answer these directly:

1. What is the core architecture: JSON-first, DOM-first, or hybrid?
2. What is the canonical identity model for creator and media records?
3. Which fields belong in the creator profile snapshot?
4. Which fields belong in reel media records and lower-cadence static/profile-grid comparison records?
5. What is the field-provenance and conflict policy for views, likes, comments, captions, dates, and ad-signal fields?
6. How should the architecture handle `/clips/user/` versus `web_profile_info` count semantics?
7. Should viewport be a core invariant, a route parameter, or a probe-only tuning variable?
8. Should zoom remain excluded from steady-state unless a real-browser/manual-control route proves it?
9. What stays satellite or deferred: ad classification, comments text capture, media/video sampling, profile discovery, scaling cadence, and official API integration?
10. What is the smallest complete next routing object after this architecture pass?

## Expected Architecture Output

Return:

```text
Human Summary:
Decision:
Target Architecture:
Why This Wins:
Core / Satellite Boundary:
Creator Profile Snapshot:
Media Records (Reels And Static Companion):
Field Provenance / Conflict Policy:
Viewport / Zoom Position:
Deferred Implementation Implications:
What We Are Not Doing:
Blockers / Not-Proven Boundaries:
Next:

Agent Detail:
Profile / Evidence Mode / Source Mode:
Subagents Launched:
Source-Read Ledger:
Questions Answered:
Architecture Option Comparison:
Target Architecture Detail:
Validation / Failure Implications:
Bloat-Cut Queue:
What Would Change The Recommendation:
```

## Hard Constraints

- Read-only architecture planning only.
- Do not execute live IG capture.
- Do not patch code or docs.
- Do not use raw cookies, raw storage-state paths, Chrome profile paths, password automation, CAPTCHA solving, proxy endpoint disclosure, exit-IP recording, or media-byte capture.
- Do not provide stealth, bypass, fingerprint-evasion, or anti-detect implementation guidance.
- Do not classify a post as an ad. Preserve ad-signal fields as candidate evidence only.
- Do not treat diagnostic `_test_runs/` as validation, readiness, or source completeness proof.
- Do not convert implementation implications into an executor-ready patch queue.

## Result Vocabulary

Use exactly one architecture result:

- `TARGET_RECOMMENDED`
- `OPTIONS_COMPARED_NO_SELECTION`
- `NEEDS_SOURCE_CONTEXT`
- `NEEDS_FEATURE_PLANNING`
- `DEFER_OR_REJECT`
- `AUTHORITY_BLOCKED`

These are planning results only. They are not validation, readiness, approval, implementation authority, or production clearance.
