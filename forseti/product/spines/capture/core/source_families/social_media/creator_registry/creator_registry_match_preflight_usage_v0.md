# Creator Registry Match Preflight Usage v0

```yaml
retrieval_header_version: 1
artifact_role: Operator-facing usage note
scope: >
  How discovery and capture lanes use the Creator Registry match preflight
  before starting new social creator capture.
use_when:
  - A scan lane has candidate creator/account handles or profile URLs.
  - A capture lane is about to start a new social creator capture.
  - A cold agent needs to distinguish already-known creators/accounts from new candidates.
authority_boundary: usage_guidance_only
```

## Required Preflight

Before starting a new social creator capture, pass the candidate account batch
through `orca-harness/runners/run_creator_registry_match_preflight.py` against
the current `creator_profile_current_view_v0.json`.

Write or preserve the emitted receipt and cite it in the scan/capture handoff or
agent report before starting `new_capture`. A manual visual scan of the registry
or static projection is useful orientation, but it is not a substitute for the
runner receipt.

For a social creator/account capture handoff, carry the receipt row's
`intended_action`, `decision`, `action_status`, and `can_start_new_capture`
fields. Do not infer new-capture permission from `decision` or `action_status`
alone; only `can_start_new_capture: true` on an `intended_action: new_capture`
receipt row clears a new social creator/account capture.

The preflight emits a receipt for each candidate:

- `existing_match`: do not create a new creator/account capture; update or work
  against the matched registry identity.
- `new_candidate`: a new capture may proceed for candidates whose
  `intended_action` is `new_capture`.
- `ambiguous_match`: stop and resolve identity before capture.
- `invalid_candidate`: fix the candidate input before capture.

The runner exits nonzero when a requested action is blocked, including
`new_capture` on an existing or ambiguous candidate.

Command shape:

```powershell
python orca-harness/runners/run_creator_registry_match_preflight.py `
  --candidates "<candidate batch json>" `
  --output "<receipt json>"
```

## Candidate Input

Candidate rows must provide:

- `candidate_id`
- `intended_action`: `classify`, `new_capture`, or `update_existing`
- at least one matchable identity: platform handle, profile URL,
  `platform_account_id_or_none`, `profile_subject_id_or_none`, or
  `platform_public_account_id_or_none`

For handle-only candidates, provide `platform`. Profile URLs may infer platform
for known social hosts. Unsupported platforms or unknown profile URL hosts are invalid candidates.

## Checker Enforcement Note

`check_csb_scanning_artifact.py` now performs two distinct checks for scan
artifacts that carry `creator_registry_match_preflight` blocks:

- shape/self-consistency: required preflight fields are present, concrete-looking,
  and clearance-shaped for `new_capture` handoff rows;
- receipt-content verification: for detected `docs/research/` scan artifacts or
  explicit checker paths, cited repo-relative receipt JSON files must exist, use
  `creator_registry_match_preflight_receipt_v0`, have a summary consistent with
  their `results`, and contain result rows whose `candidate_id`,
  `intended_action`, `decision`, `action_status`, and `can_start_new_capture`
  match the artifact's handoff row.

The checker still does not prove fuzzy duplicate absence, cross-platform
identity, discovery quality, source adequacy, runner provenance beyond the
preserved JSON receipt content, registry mutation, or Capture execution. Treat a
green checker run as receipt-content consistency evidence, not scan validation or
Capture authorization.

## Non-Claims

This preflight is exact-match enforcement only:

- not fuzzy display-name matching
- not cross-platform creator identity proof
- not proof that discovery searched enough
- not silver metric refresh
- not registry mutation
- not live social search
- not a Source Capture packet writer

## Accepted Residuals

Fuzzy duplicates may still pass. This is accepted until exact preflight fails to
prevent repeated duplicate captures.

Cross-platform identity remains outside this runner. Use the public-handle
linkage workflow for creator-level promotion.

Metric freshness is not handled here. If the candidate already exists but stats
are stale, update the existing identity in the relevant capture/metric lane.

## Direction Change Propagation - Receipt Content Checker

```yaml
direction_change_propagation:
  doctrine_changed: >
    The scan-artifact checker now verifies Creator Registry match-preflight
    receipt content for scan artifacts that carry creator_registry_match_preflight
    blocks: cited repo-relative receipt JSON files must exist, use the expected
    receipt schema, have summary counts consistent with results, and contain
    result rows whose candidate_id and clearance fields match the artifact's
    handoff rows. This closes the prior shape-only checker residual for the
    first real receipt-bearing scan artifact, without expanding into fuzzy
    duplicate detection, source adequacy, runner-provenance proof, registry
    mutation, or Capture authorization.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - ".agents/hooks/check_csb_scanning_artifact.py"
    - "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md"
    - "docs/workflows/forseti_repo_map_v0.md"
    - "orca-harness/tests/fixtures/csb_scanning_artifacts/valid_creator_registry_preflight_scan.md"
    - "orca-harness/tests/fixtures/csb_scanning_artifacts/valid_creator_registry_preflight_receipt.json"
    - "orca-harness/tests/fixtures/csb_scanning_artifacts/bad_creator_registry_preflight_mismatch.md"
    - "orca-harness/tests/fixtures/csb_scanning_artifacts/bad_creator_registry_preflight_mismatch_receipt.json"
  downstream_surfaces_checked:
    - path: ".agents/workflow-overlay/validation-gates.md"
      note: >
        Existing receipt-field provenance and review-routing gates cover the
        governing validation philosophy; no overlay edit required for this
        source-family checker extension.
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      note: >
        Runbook routes to this usage note for Creator Registry match-preflight
        details and carries no stale checker-scope claim.
    - path: "forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md"
      note: >
        Scan core routes to this usage note for the exact-match receipt; no
        stale checker-scope claim found.
    - path: "forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md"
      note: >
        MGT operating model carries the preflight block shape but no stale
        checker-scope claim.
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/validation-gates.md"
      reason: >
        This is a concrete source-family checker implementation of the existing
        receipt-field provenance principle, not a new global validation gate.
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: >
        The runbook intentionally delegates detailed Creator Registry preflight
        semantics to this usage note.
  stale_language_search: >
    rg -n "Checker Scope Note|receipt-authenticity|receipt authenticity|content-verification|check_csb_scanning_artifact|creator_registry_match_preflight"
    forseti/product/spines/capture/core/source_families/social_media/creator_registry
    orca-harness/docs/source_capture_agent_runbook.md
    forseti/product/spines/scanning
    docs/workflows/forseti_repo_map_v0.md
    .agents/workflow-overlay/validation-gates.md
  stale_language_search_result: >
    Executed 2026-07-04. Hits are the updated usage note, runbook/spec/model
    pointers to the usage note or preflight block, the updated repo-map checker
    entry, the existing scanning README checker references, and the overlay's
    generic receipt-field provenance gate. No live surface still says the
    Creator Registry preflight checker is shape-only for receipt content.
  non_claims:
    - "not scan validation"
    - "not Capture authorization"
    - "not fuzzy duplicate detection"
    - "not cross-platform identity proof"
    - "not source adequacy proof"
    - "not runner-provenance proof beyond preserved JSON content"
    - "not registry mutation"
```

## Direction Change Propagation - Scan/Capture Receipt Handoff

```yaml
direction_change_propagation:
  doctrine_changed: >
    Scan-to-capture handoffs for social creator/account capture must carry the
    Creator Registry match preflight receipt fields, including the authoritative
    `can_start_new_capture` boolean, before a new social creator/account capture
    can start.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - "orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md"
    - "orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/prompt-orchestration.md"
    - ".agents/workflow-overlay/template-registry.md"
    - "docs/prompts/templates/shared/orca_preflight_defaults_v0.md"
    - "docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "Root agent instructions do not enumerate source-family receipt fields."
    - path: ".agents/workflow-overlay/prompt-orchestration.md"
      reason: "Prompt mechanics did not change; future scan/capture prompts inherit this through the changed scan and capture sources."
    - path: ".agents/workflow-overlay/template-registry.md"
      reason: "No template path, output mode, or template kind changed."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo-map routing is unchanged: scanning tasks route through the scanning spine and capture tasks route through the source-capture runbook."
  stale_language_search: "rg -n \"creator_registry_match_preflight|Creator Registry match preflight|can_start_new_capture|new social creator/account|new social creator|projection scan|visual registry\" orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md orca-harness/docs/source_capture_agent_runbook.md orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md docs/workflows/orca_repo_map_v0.md docs/prompts/templates/shared/orca_preflight_defaults_v0.md docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md .agents/workflow-overlay/prompt-orchestration.md .agents/workflow-overlay/template-registry.md"
  stale_language_search_result: >
    Executed 2026-07-04 after edits. Hits are the changed usage note, runbook
    report skeleton, scan-core/MGT capture-request bindings, the existing
    repo-map runner index, and the prior source-capture runbook receipt. The
    shared prompt templates and prompt-orchestration/template-registry surfaces
    carry no stale alternate handoff rule; they continue to route through the
    changed scan/capture sources.
  non_claims:
    - "not validation"
    - "not readiness"
    - "not fuzzy duplicate detection"
    - "not cross-platform identity proof"
    - "not silver metric refresh"
    - "not registry mutation"
    - "not live social search"
    - "not scan authorization"
    - "not capture authorization"
```
