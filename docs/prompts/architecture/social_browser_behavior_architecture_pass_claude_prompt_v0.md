# Social Browser Behavior Architecture Pass Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact - architecture pass
scope: >
  Claude-ready prompt for a proper architecture pass over the social browser
  behavior calibration recommendation. The pass should attack whether the
  proposed IG doc patch + recon-first shared-controller direction is the right
  architecture, not merely verify the recommendation.
use_when:
  - Running a fresh architecture pass on the social browser behavior calibration lane.
  - Stress-testing whether the shared social browser controller abstraction is premature.
  - Deciding the next routing object after the recon-first recommendation artifact.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_capture_toolbox/social_browser_behavior_recon_first_calibration_note_v0.md
  - docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_logged_out_sustainability_probe_plan_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
branch_or_commit: codex/social-capture-browser-calibration-core-port @ 036d304d876020ead7345cfd730e4a1574668dcf plus this prompt
stale_if:
  - The recommendation artifact changes.
  - TikTok or YouTube receive durable Capture recipe cards or source-family recon.
  - IG cadence, viewport, cooldown, source-access, or browser-route evidence changes.
  - The receiver cannot access the repo/filesystem and no source capsule is provided.
```

Paste the body below into Claude.

---

You are the Chief Architect for Orca.

## Objective

Run a proper architecture pass on the current social browser behavior
calibration recommendation. Do not merely verify the recommendation. Treat the
recommendation as a candidate architecture and attack it.

The candidate recommendation is:

- Patch IG docs now around browser session shape, stop/cooldown, viewport
  interpretation, stable egress lanes, and receipt evidence.
- Keep a shared social browser controller only as a conceptual profile
  interface.
- Require TikTok/YouTube recon before inheriting any IG thresholds, routes,
  viewport behavior, cooldowns, or source-access posture.

Your task is to decide whether that is actually the right architecture, whether
the shared-controller abstraction should be accepted, deferred, narrowed, or
rejected, and what the next routing object should be.

## Required Pushback

Push hard against weak architecture. In particular, attack these failure modes:

- The recommendation may be too close to "IG patch now" and not architecture
  enough.
- The "shared controller" may be premature naming that creates implementation
  gravity before a second platform exists.
- The recon-first answer may be true but operationally unhelpful unless it says
  exactly what a TikTok/YouTube recon must fill.
- The IG patch set may be fragmented across too many docs instead of producing
  one stable boundary.
- The next move may not be another artifact; it may be owner acceptance,
  rejection, or a narrower doc patch.

Do not give comfort if the architecture is weak. Return the strongest usable
answer.

## Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
authorization_basis: owner asked to prompt out for a proper Claude architecture pass after a low-signal zero-finding check.
objective: >
  Decide whether the current social browser behavior calibration recommendation
  has the right target architecture and next routing object.
intended_decision: >
  Select, narrow, defer, or reject the candidate IG-patch-now / shared-interface
  / TikTok-YouTube-recon-first architecture.
output_mode: chat-only architecture pass; do not write files unless the owner explicitly redirects.
template_kind: architecture pass; no runtime-model routing implication.
edit_permission: read-only.
target_files_or_dirs:
  - orca/product/spines/capture/core/source_capture_toolbox/social_browser_behavior_recon_first_calibration_note_v0.md
  - docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/
  - orca/product/spines/capture/core/source_capture_toolbox/
  - orca/product/spines/capture/core/contracts/source_access_boundary/
source_pack: bounded custom pack listed below.
dirty_state_allowance: read-only; report dirty-state conflicts if they affect source authority.
controlling_source_state: reread required in receiver thread before strict claims.
branch_or_commit_reference: codex/social-capture-browser-calibration-core-port; verify live branch/head before source claims.
doctrine_change_decision: proposal only; do not apply doctrine changes.
validation_gates: none; this is architecture planning, not validation/readiness.
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: not_applicable
```

## Required Reads

First read:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

Then read the candidate and source pack:

- `orca/product/spines/capture/core/source_capture_toolbox/social_browser_behavior_recon_first_calibration_note_v0.md`
- `docs/prompts/architecture/social_capture_browser_behavior_calibration_prompt_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
- `orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md`
- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_r_probe_results_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_rate_findings_report_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_logged_out_sustainability_probe_plan_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_sustained_cadence_r_probe_design_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md`

Search narrowly for TikTok/YouTube Capture artifacts:

```text
rg -n -i "youtube|tiktok|tik tok|tik-tok" orca/product/spines/capture docs/workflows/data_capture_spine_consolidation_map_v0.md docs/decisions/orca_spine_first_target_structure_binding_v0.md
rg --files orca/product/spines/capture | rg -i "youtube|tiktok|tik_tok|tik-tok|\\byt_|_yt|\\btt_|_tt"
```

If no durable TikTok/YouTube recipe card or source-family recon exists, say so.
Do not use general platform memory to fill platform thresholds or routes.

## Method

1. Run Orca Cynefin routing before planning. Include allowed and disallowed next
   moves.
2. REFERENCE-LOAD architecture-planning/deep-thinking method instructions only
   if available. Do not apply them before source readiness.
3. SOURCE-LOAD the required sources.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Run three local architecture perspectives:
   - Directional: strongest case for the candidate recommendation.
   - Adversarial: strongest case against the candidate, especially premature
     shared-controller abstraction and weak next-routing.
   - Grounding: smallest complete Orca-native architecture with no fake success
     and no runtime drift.
6. Synthesize the architecture result.

Do not launch subagents unless the owner explicitly authorizes them.

## Architecture Options To Compare

Compare only real options. At minimum test these:

- `AO-1 IG-only doc patch`: no shared controller language now.
- `AO-2 Shared conceptual profile interface`: accept a controller-shaped
  vocabulary but no runtime or cross-platform defaults.
- `AO-3 Recon template first`: do not patch IG further until a TikTok/YouTube
  recon-card template defines exactly what second-platform evidence must fill.
- `AO-4 Reject abstraction`: treat browser behavior as source-family-specific
  until two platforms prove commonality.
- `AO-5 Hybrid`: IG patch now plus a minimal recon-card field list, but defer a
  named controller until the second platform exists.

## Required Questions

Answer these directly:

1. What is the actual architecture decision here?
2. Is "shared social browser behavior controller" a useful core abstraction, a
   premature name, or a future seam only?
3. What belongs in IG source-family docs versus `source_capture_toolbox/`?
4. What exact invariants should survive future TikTok/YouTube recon?
5. What exact fields must a TikTok/YouTube recon card fill before inheriting
   anything from IG?
6. Is the current recommendation artifact strong enough to act on, or should it
   be patched before use?
7. What is the smallest complete next routing object?

## Output Contract

Return chat only, with this structure:

```text
Architecture Result:
TARGET_RECOMMENDED | OPTIONS_COMPARED_NO_SELECTION | NEEDS_SOURCE_CONTEXT | DEFER_OR_REJECT

Decision:
One paragraph.

Source Context:
SOURCE_CONTEXT_READY or SOURCE_CONTEXT_INCOMPLETE, with source gaps.

Option Comparison:
Compact table. Include why each option wins/loses.

Target Architecture:
Core:
IG source-family:
Shared toolbox:
TikTok/YouTube recon:
Deferred:

Hard Pushback:
The strongest objection to the chosen answer, and why it does or does not defeat it.

Patch Or Use As-Is:
Say whether `social_browser_behavior_recon_first_calibration_note_v0.md` is usable as-is, should be patched, or should be superseded.

Smallest Complete Next Routing Object:
One object only.

Non-Claims:
No validation/readiness/runtime/live-capture/source-access authorization claims.
```

## Boundaries

Do not:

- Run live IG, TikTok, or YouTube capture.
- Edit files.
- Install or invoke browser automation, anti-detect tooling, proxies, APIs,
  schedulers, queues, databases, or workers.
- Provide a stealth recipe, fingerprint-spoofing implementation, CAPTCHA path,
  per-request rotation plan, or code patch.
- Treat TikTok or YouTube as equivalent to IG without source-family evidence.
- Convert blocks, empty payloads, redirects, or culling into success.
- Claim validation, readiness, legal sufficiency, platform permission, buyer
  proof, commercial authorization, or implementation authorization.

This is architecture planning only.
