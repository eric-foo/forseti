# Creator Registry Cold Creator Discovery Scan Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Filed reusable prompt shell for launching a cold creator discovery scan that
  uses the Creator Registry match preflight before any new social creator/account
  capture request.
use_when:
  - Commissioning a fresh scan lane to find additional social creators/accounts in an owner-supplied niche or platform lane.
  - A cold agent must distinguish already-known registry accounts from new candidates before capture handoff.
  - Preserving the scan-to-capture boundary after Creator Registry preflight enforcement and rehearsal landed.
authority_boundary: retrieval_only
branch_or_commit: origin/main@ef2bcf184992c7c29d631190b2deb9487bc265b6
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/validation-gates.md
  - forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md
  - orca-harness/runners/run_creator_registry_match_preflight.py
stale_if:
  - The Creator Registry match preflight usage note or runner changes receipt fields or exit behavior.
  - The scanning MGT operating model changes the capture_request block or social creator route boundary.
  - The live creator_profile_current view moves away from the current exact-match registry shape.
  - The owner supplies a concrete target whose source family has narrower rules than this prompt shell names.
```

## Prompt Authoring Preflight

```yaml
orchestrator_mode: workflow-prompt-orchestrator
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
forseti_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes - .agents/workflow-overlay/README.md read in current task context
  source_pack: custom_creator_registry_cold_scan_handoff
  edit_permission: docs-write for this prompt artifact only
  target_scope:
    - docs/prompts/handoffs/creator_registry_cold_creator_discovery_scan_handoff_prompt_v0.md
  dirty_state_checked: yes - isolated worktree codex/creator-registry-cold-scan-handoff from origin/main@ef2bcf18
  blocked_if_missing:
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
    - forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
    - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
    - docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md
output_mode: file-write
downstream_launch_mode: paste-ready-chat after the dispatcher fills target variables
template_kind: handoff
template_source: direct Orca handoff prompt under prompt-orchestration contract; no project-local handoff template is registered beyond the folder/role binding.
prompt_artifact_path: docs/prompts/handoffs/creator_registry_cold_creator_discovery_scan_handoff_prompt_v0.md
downstream_output_artifact_path: "<FILL_BEFORE_LAUNCH: docs/research/creator_discovery_scan_<target_slug>_v0.md or owner-supplied path>"
edit_permission: docs-write for this prompt artifact; downstream scan lane is docs-write only unless separately authorized.
dirty_state_allowance: this prompt branch must be clean at closeout; downstream receiver must use a clean branch/worktree.
controlling_source_state: clean at authoring start; receiver must fresh-read current sources before running.
repo_map_decision: loaded
repo_map_reason: required to confirm current live paths after the Forseti product-root migration and to avoid stale pre-migration product-root paths.
doctrine_change_decision: no doctrine change; this files a reusable launch prompt that consumes existing scan/capture registry rules.
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
workflow_sequence_policy: overlay_owned
workflow_sequence_source: active_overlay plus current owner direction after PR #667 merged
workflow_sequence_status: bound
model_lane: unbound; prompt is model-neutral and must not prescribe runtime model choice
non_claims:
  - not a scan authorization by itself
  - not capture authorization
  - not validation
  - not readiness
  - not fuzzy duplicate detection
  - not cross-platform identity proof
  - not source-access permission
```

## Authorization Basis

The owner reported PR #667 merged and said to proceed. Local verification observed
PR #667 as merged into `origin/main` at merge commit `ef2bcf18`, adding the cold
preflight rehearsal record. The prior closeout named the next material step:
use the behavior in the next cold scan/capture handoff.

This artifact prepares that handoff. It does not run a scan and is not launch-ready
until an owner or dispatcher fills the target variables in the paste-ready prompt.

## Fitness Reference

Goal: make cold creator discovery lanes use the Creator Registry as the first
anti-duplicate checkpoint before asking Capture to start new social creator/account
work.

Done looks like: a future scan output can list already-known registry matches,
new exact-unmatched candidates, and any capture_request rows with the required
preflight receipt fields, so Capture does not recapture an account already present
in the registry.

This goal and signal are executor orientation and review axes to attack, not a
claim that any future scan is complete, high quality, or capture-authorized.

## Current Path Note

Current `origin/main` uses `forseti/product/...` for the product spine paths.
Some recently merged historical receipts still quote older pre-migration product-root
paths. A receiving lane must use the current live `forseti/product/...` paths or
resolve old paths through `docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`
before making strict source claims.

## Paste-Ready Launch Prompt

````markdown
# Creator Registry Cold Creator Discovery Scan Commission

You are opening a fresh Orca scan lane to find additional social creators/accounts
for an owner-supplied lane.

This prompt is not valid until the dispatcher fills these launch variables:

```yaml
launch_variables_required:
  scan_target: "<owner-supplied niche / lane / creator type>"
  platforms_in_scope: ["<youtube|instagram|tiktok|other owner-supplied>"]
  geography_or_market_scope: "<owner-supplied or not_applicable>"
  source_access_boundary: "<public/no-login only unless owner explicitly authorizes more>"
  run_cap:
    max_exact_queries: "<number>"
    max_creator_candidate_rows: "<number>"
    max_source_reads: "<number>"
  output_artifact_path: "docs/research/creator_discovery_scan_<target_slug>_v0.md"
  capture_request_policy: "scan_may_emit_capture_requests | scan_only_no_capture_requests"
```

If any launch variable is missing, return `BLOCKED_MISSING_OWNER_SCAN_TARGET`
and do not scan.

## Access Gate

If you have repo/filesystem access, open the required files and re-read their
load-bearing sections before making strict or actionable claims.

If you do not have repo/filesystem access, stop and request a source capsule or
no-repo handoff. Do not scan from memory, chat summaries, or stale path claims.

Current live product-spine paths are under `forseti/product/...`. If a cited
source in an older artifact uses a pre-migration product-root path, resolve the current path
through `docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`
or by `rg --files` before relying on it.

## Required Source Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read `.agents/workflow-overlay/source-loading.md`,
   `.agents/workflow-overlay/artifact-roles.md`,
   `.agents/workflow-overlay/retrieval-metadata.md`, and
   `.agents/workflow-overlay/validation-gates.md` only as needed to bind the
   output artifact and validation gates.
3. SOURCE-LOAD the scan/registry pack below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, run the scan.

No workflow method is required by this prompt. If you choose to use a workflow
method, follow the Source-Gated Method Contract: REFERENCE-LOAD the method first,
do not APPLY it before task sources are loaded, declare source readiness, then
APPLY it.

## Required Sources

Scan and capture-boundary sources:

- `forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
- `docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md`
- `orca-harness/runners/run_creator_registry_match_preflight.py`
- `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
- `forseti/product/spines/creator_signal/creator_signal_multi_creator_library_static_projection_v0.md` for orientation only, if present
- `orca-harness/docs/source_capture_agent_runbook.md` targeted to the Creator Registry preflight and Source Capture boundary sections

Optional only if the scan target needs broader scanning method context:

- `forseti/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md`
- `forseti/product/spines/scanning/README.md`

## Hard Boundaries

- This is a scanning lane, not Capture execution.
- Do not run live capture, packet writers, data-lake writes, ECR, Cleaning,
  Judgment, outreach, contact finding, follower graph work, comment scraping,
  channel/person dossiers, or standing monitoring.
- Do not edit the Creator Registry, identity ledger, metric rollups, source data,
  or static projection.
- A visual registry/projection scan is orientation only. It never replaces the
  Creator Registry match preflight runner receipt.
- Exact-match preflight is not fuzzy duplicate detection and not cross-platform
  identity proof.
- A `new_candidate` result from `intended_action: classify` does not clear new
  capture. New social creator/account capture requires `intended_action:
  new_capture` and `can_start_new_capture: true` on the receipt row.
- If a candidate is `existing_match`, route to the matched registry identity or
  an update-existing lane; do not create a new capture target.
- If a candidate is `ambiguous_match` or `invalid_candidate`, stop and resolve
  identity/input before any capture handoff.

## Objective

Create a dated scan artifact at:

```text
<FILL_BEFORE_LAUNCH: output_artifact_path>
```

The artifact should answer:

> For the owner-supplied target, which public social creator/account candidates
> look worth carrying forward, which are already present in the Creator Registry,
> and which exact-unmatched rows may be handed to Capture as new social
> creator/account candidates only if the registry preflight receipt clears them?

## Required Operating Steps

1. Confirm launch variables and write them at the top of the scan artifact.
2. Read the current registry view counts and platform mix from
   `creator_profile_current_view_v0.json`; do not hardcode old counts.
3. Use the static projection, if present, only for human-readable orientation.
4. Run the bounded public scan under the supplied run cap.
5. Build a candidate batch JSON for every social creator/account row that might
   become a capture request or future registry candidate.
6. For any row that may ask Capture to start a new social creator/account capture,
   set `intended_action: new_capture` before running the preflight.
7. Run:

```powershell
python orca-harness/runners/run_creator_registry_match_preflight.py `
  --candidates "<candidate batch json>" `
  --output "<local receipt json>"
```

8. Preserve the emitted receipt locally and cite its path in the scan artifact.
9. Inspect row-level results. Mixed batches may exit nonzero when one row is
   blocked while another clears; never treat the whole batch as all allowed or
   all blocked.
10. Emit candidate rows and capture_request rows only within the output contract
    below.

## Output Artifact Contract

The scan artifact must include these sections:

```markdown
# <Target> Creator Discovery Scan v0

## Retrieval Header
## Launch Variables
## Source Context
## Registry Orientation
## Scan Moves And Queries
## Candidate Batch
## Creator Registry Match Preflight Receipt
## Existing Registry Matches
## New Exact-Unmatched Candidates
## Blocked Or Ambiguous Candidates
## Capture Requests
## Non-Claims And Residuals
## Validation
## Next Step
```

For each candidate row, include:

```yaml
candidate_id:
platform:
handle_or_url:
public_profile_url_or_none:
public_handle_or_none:
source_url_or_none:
why_candidate_was_collected:
preflight:
  receipt_path:
  intended_action:
  decision:
  action_status:
  can_start_new_capture:
  matched_registry_profiles_summary:
status:
  existing_registry_match | new_exact_unmatched | ambiguous_or_invalid | not_capture_candidate
next_step:
  update_existing | eligible_for_capture_request | resolve_identity | no_capture_request
```

For each `capture_request`, use the scanning MGT block shape and include:

```yaml
creator_registry_match_preflight:
  required_when: new_social_creator_account_capture | not_applicable
  receipt_path: null_or_path
  intended_action: new_capture | classify | update_existing | not_applicable
  decision: existing_match | new_candidate | ambiguous_match | invalid_candidate | not_applicable
  action_status: allowed | blocked | not_applicable
  can_start_new_capture: true | false | not_applicable
```

A new social creator/account capture request is allowed only when:

```yaml
required_when: new_social_creator_account_capture
intended_action: new_capture
decision: new_candidate
action_status: allowed
can_start_new_capture: true
```

For non-social or scan-only rows, use `required_when: not_applicable` and do not
carry clearance-shaped fields.

## Required Validation

Before reporting completion, run or explicitly mark not-run with reason:

```powershell
git diff --check
python .agents/hooks/check_retrieval_header.py --changed --strict
python .agents/hooks/header_index.py --strict --base origin/main
python .agents/hooks/check_handoff_pointers.py --strict --base origin/main
python .agents/hooks/check_dcp_receipt.py --strict --base origin/main
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_full_gt_claims.py --changed --strict
python .agents/hooks/check_csb_scanning_artifact.py --changed --strict
```

If your scan artifact is not CSB-first and `check_csb_scanning_artifact.py` does
not apply, state that explicitly; do not treat the skipped check as a pass.

## Closeout

Report:

- output artifact path;
- registry view counts observed from the current JSON;
- candidate count;
- preflight receipt path;
- counts by preflight decision;
- which rows, if any, are eligible for capture request;
- validation commands and observed outcomes;
- residuals: exact-match only, no fuzzy identity, no cross-platform identity,
  no metric refresh, no capture run.

Do not claim validation, readiness, source completeness, creator quality,
commercial fit, buyer proof, capture authorization, or registry mutation.
````

## Dispatcher Notes

Use this prompt by filling the launch variables in the paste-ready block or by
wrapping it in a lane PR/comment that supplies them. Without those variables, the
receiver must block instead of inventing a target.

For a simple first live use, choose a small run cap and a single platform. The
point is to prove the cold-run flow on real candidate rows before expanding to
multi-platform or fuzzy/cross-platform identity work.
