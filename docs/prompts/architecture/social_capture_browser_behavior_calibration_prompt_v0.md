# Social Capture Browser-Behavior Calibration Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact - architecture/calibration commission
scope: >
  Commissions a fresh Chief Architect lane to source-load the current IG capture
  spine, evaluate browser-behavior calibration changes for durable social
  capture runs, and test whether any shared controller shape can safely extend
  to TikTok and YouTube without erasing platform-specific evidence gates.
use_when:
  - Commissioning an IG-first browser-behavior calibration architecture pass for social capture.
  - Testing the owner hypothesis that IG, TikTok, and YouTube may share behavioral primitives.
  - Asking for a small proposed change set before any implementation or live capture run.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_families/instagram/ig_at_scale_operating_envelope_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_logged_out_sustainability_probe_plan_v0.md
  - orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
branch_or_commit: codex/social-capture-browser-calibration-prompt @ 631c5e89de59848fada59d45e52668ae2dba85b5
stale_if:
  - IG rate, cooldown, viewport, logged-out reachability, or two-lane additivity evidence changes.
  - TikTok or YouTube receive durable source-family recon, recipe cards, or source-access decisions.
  - The source-access boundary, wind-caller carve-out, anti-block ladder, or capture playbook changes.
  - A later implementation lane lands browser-behavior controls for social capture.
```

Paste the body below into a fresh Chief Architect thread in this workspace.

---

You are the Chief Architect for Orca.

## Objective

Explore the current IG capture spine and recommend a small browser-behavior
calibration change set that makes durable social capture runs less likely to be
culled by predictable, bot-like run shape.

The owner hypothesis is:

> A more human-shaped browser behavior model may improve run durability for IG,
> and the same general behavior model might also apply to TikTok and YouTube.

Treat that as a hypothesis, not a fact. Your job is to decide what can be shared
as a platform-agnostic controller concept, what must remain IG-specific, and
what requires separate TikTok or YouTube recon before Orca can rely on it.

## Hard Pushback To Preserve

Do not assume IG, TikTok, and YouTube share the same culling model. They may
share high-level primitives, such as bounded sessions, human-rate pacing,
cooldowns, stop-on-wall behavior, and receipt discipline. They do not inherit
the same thresholds, substrates, viewport behavior, auth-wall semantics, policy
posture, or fallback routes without source-specific evidence.

If the source context does not support TikTok or YouTube, return a recon-first
recommendation for those platforms instead of generalizing from IG.

## Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
authorization_basis: owner request in the capture lane to branch out a prompt for IG / TikTok / YouTube browser-behavior calibration.
objective: >
  Produce an architecture recommendation and small proposed change set for
  social-capture browser-behavior calibration, IG-first, with TikTok/YouTube
  generalization explicitly gated by source evidence.
intended_decision: >
  Decide whether to recommend IG-only prompt/doc patches, a shared social
  browser-behavior controller with platform profiles, recon-first for TikTok
  and YouTube, no change, or a blocked source-context result.
target_files_or_dirs:
  - docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md
  - orca/product/spines/capture/source_families/instagram/
  - orca/product/spines/capture/source_capture_toolbox/
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
source_pack: bounded custom pack listed below.
output_mode: file-write
edit_permission: docs-write for one recommendation artifact only; no runtime edits.
dirty_state_allowance: use a clean worktree off current main; unrelated dirty files are out of scope.
controlling_source_state: reread required in receiver thread before strict claims.
branch_or_commit_reference: source prompt authored on codex/social-capture-browser-calibration-prompt @ 631c5e89de59848fada59d45e52668ae2dba85b5.
doctrine_change_decision: >
  The recommendation may propose doctrine or architecture changes, but must not
  apply them. If it recommends changing source-access posture, capture
  obligations, anti-block ladder behavior, prompt doctrine, validation language,
  or lifecycle boundaries, name the propagation surfaces and stop at proposal.
isolation_decision: worktree off main; this is cross-lane docs work on a dirty-base repo.
validation_gates: retrieval-header strict check for the written recommendation artifact; no validation/readiness claims.
thread_operating_target_continuity: not carried forward; this is a new architecture/calibration commission branching from capture-lane work.
```

## Required Reads

Authority and workflow:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

Capture spine and source-access sources:

- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/capture/source_capture_toolbox/capture_recon_index_v0.md`
- `orca/product/spines/capture/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md`
- `orca/product/spines/capture/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md`
- `docs/decisions/wind_caller_calibration_carveout_v0.md`

IG current spine:

- `orca/product/spines/capture/source_families/instagram/ig_capture_findings_consolidated_v0.md`
- `orca/product/spines/capture/source_families/instagram/ig_r_probe_results_v0.md`
- `orca/product/spines/capture/source_families/instagram/ig_capture_rate_findings_report_v0.md`
- `orca/product/spines/capture/source_families/instagram/ig_at_scale_operating_envelope_v0.md`
- `orca/product/spines/capture/source_families/instagram/ig_logged_out_sustainability_probe_plan_v0.md`
- `orca/product/spines/capture/source_families/instagram/ig_sustained_cadence_r_probe_design_v0.md`
- `orca/product/spines/capture/source_families/instagram/ig_capture_shape_contract_spec_v0.md`
- `orca/product/spines/capture/source_families/instagram/orca_creator_monitoring_policy_architecture_v0.md`
- `orca-harness/runners/run_source_capture_ig_calls_packet.py`

TikTok and YouTube source discovery:

- Search the repo for durable TikTok, TT, YouTube, and YT capture artifacts.
- If no durable source-family recon or recipe card exists, say so as a source
  gap. Do not substitute general platform memory for Orca source context.
- If you discuss current platform policy or access posture for TikTok or
  YouTube, verify current official sources in that thread and cite dates. If you
  do not verify them, mark the policy posture `UNKNOWN - requires source check`.

## Source-Gated Method

1. Run Orca Cynefin routing before planning. Include the allowed next move and
   the disallowed next move.
2. REFERENCE-LOAD `workflow-deep-thinking` and
   `workflow-architecture-planning` if available.
3. SOURCE-LOAD the required local sources above.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with material
   gaps.
5. Only after source readiness, APPLY the methods to analyze the source context.
6. You may use up to three advisory subagents after source readiness only. If
   used, assign them narrow roles:
   - IG spine mapper: what browser-behavior assumptions already exist?
   - Generalization skeptic: what breaks if IG behavior is generalized to TikTok/YouTube?
   - Harness/receipt mapper: what would have to change in docs or future implementation scoping?

## Boundaries

This pass is planning only.

Do not:

- Run live IG, TikTok, or YouTube capture.
- Use credentials, cookies, sessions, stored browser profiles, or login automation.
- Bypass access-control gates, private content gates, paywalls, CAPTCHAs, or
  non-entitled surfaces.
- Install, configure, or invoke browser automation, anti-detect tooling,
  proxies, scraper APIs, schedulers, queues, databases, or production workers.
- Provide a turnkey stealth recipe, fingerprint-spoofing implementation,
  CAPTCHA-solving path, per-request rotation plan, or code patch.
- Convert a blocked or culled run into fake success. Culling, blocks, redirects,
  empty payloads, and missing substrates must stay visible in receipts.
- Treat TikTok or YouTube as authorized, reachable, or equivalent to IG unless
  current Orca sources prove it.

You may recommend future implementation scoping, future probe design, or
specific doc patches. Those recommendations must remain non-executing and
owner-gated where live source access or runtime work is involved.

## Questions To Answer

1. What does the current IG spine already require for human-rate behavior,
   pacing, cooldowns, viewport selection, stop-on-wall, and receipt discipline?
2. Where is IG still under-specified? Look especially for vague `bounded_jitter`
   language, missing session-shape defaults, missing long-quiet cooldown rules,
   missing block taxonomy, missing asset/media policy, missing viewport
   discipline, missing lane separation, or missing run receipts.
3. What are the smallest useful proposed changes? Prefer three to seven
   concrete changes, each tied to a source-backed failure mode.
4. Which proposed changes belong in product docs now, and which belong in a
   later implementation-scoping prompt?
5. What, if anything, can be shared across IG, TikTok, and YouTube as a generic
   browser-behavior controller concept?
6. What must be platform-profile-specific?
7. What recon must happen before TikTok or YouTube inherit any IG-derived
   settings?
8. What evidence would prove the changes helped without creating fake success
   or hiding block/culling events?

## Candidate Change Areas To Evaluate

Do not copy these blindly. Attack them and keep only what survives source
loading.

| Candidate area | What to evaluate |
| --- | --- |
| Session-shape profile | Warm-up reads, clusters, idle gaps, long quiet windows, session ceilings, and abort posture. |
| Cooldown model | Stop after wall, avoid periodic probing that may sustain throttle, record quiet-window duration. |
| Viewport and route profile | IG already has viewport-sensitive profile enumeration; decide whether this needs a named profile. |
| Asset/media policy | Balance bandwidth savings against suspicious all-assets-blocked signatures; keep fidelity obligations visible. |
| Block taxonomy | Separate login redirect, auth gate, anti-bot challenge, 429-like rate limit, missing signal, and viewport/content-shape failure. |
| Lane separation | Stable egress lanes rather than per-request rotation; do not treat multiple accounts on one IP as throughput. |
| Receipt fields | Require enough run-shape evidence to distinguish durable capture, partial fidelity, and culling/blocking. |
| Shared controller vs platform profile | Generic primitives may be shared; thresholds and routes must be platform-specific. |

## Required Recommendation Labels

Choose one primary label:

- `RECOMMEND_IG_ONLY_DOC_PATCH_SET`
- `RECOMMEND_SHARED_SOCIAL_BROWSER_CONTROLLER_WITH_PLATFORM_PROFILES`
- `RECOMMEND_RECON_FIRST_FOR_TIKTOK_YOUTUBE`
- `RECOMMEND_NO_CHANGE`
- `BLOCKED_SOURCE_CONTEXT`

You may include a secondary label if the answer is mixed, such as
`IG_PATCH_NOW__TT_YT_RECON_FIRST`.

## Required Output Artifact

Write exactly one durable recommendation artifact. Choose the path based on the
recommendation:

- If the recommendation is IG-only:
  `orca/product/spines/capture/source_families/instagram/ig_browser_behavior_calibration_change_set_v0.md`
- If the recommendation is a shared controller with platform profiles:
  `orca/product/spines/capture/source_capture_toolbox/social_browser_behavior_calibration_architecture_v0.md`
- If the recommendation is recon-first for TikTok/YouTube with only an IG
  patch sketch:
  `orca/product/spines/capture/source_capture_toolbox/social_browser_behavior_recon_first_calibration_note_v0.md`

Use a retrieval header. Mark the artifact non-authorizing. Include source
readiness, source gaps, recommendation label, proposed changes, platform
generalization decision, owner gates, non-claims, and next authorized step.

## Output Structure

The written artifact should include:

1. Title and retrieval header.
2. Status and non-authorizing boundary.
3. Source readiness and missing sources.
4. Cynefin routing result.
5. Current IG behavior model summary.
6. Failure modes the current model does not cover well enough.
7. Proposed change set, preferably three to seven items.
8. For each proposed change:
   - target artifact or future implementation-scope surface;
   - source-backed rationale;
   - expected durability benefit;
   - risk or tradeoff;
   - evidence needed to close it;
   - owner gate if any.
9. IG / TikTok / YouTube comparison table with `known`, `unknown`, and
   `do_not_generalize` cells.
10. Recommendation label.
11. Required propagation surfaces if accepted.
12. Open owner questions.
13. Next authorized step.
14. Non-claims.

## Success Bar

The output succeeds if a future owner or CA can decide whether to:

- patch the IG operating-envelope/probe-plan docs;
- commission implementation scoping for browser-behavior controls;
- commission TikTok and YouTube recon before generalizing;
- reject the shared-controller idea as premature.

The output fails if it:

- assumes one IG-derived timing model works across TikTok and YouTube;
- proposes stealth implementation instead of architecture/scoping;
- hides culling/blocking evidence;
- claims validation, readiness, platform permission, legal sufficiency, or
  commercial authorization;
- edits runtime code or performs live source access.

## Non-Claims

This commission is not validation, readiness, legal advice, platform permission,
source-access boundary amendment, implementation authorization, live-run
authorization, proxy/session approval, anti-detect approval, scraper API
approval, production runtime, scheduler authorization, ECR, Cleaning, Judgment,
buyer proof, or commercial evidence.
