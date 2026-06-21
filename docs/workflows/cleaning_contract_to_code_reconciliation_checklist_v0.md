# Cleaning Contract-To-Code Reconciliation Checklist v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: >
  Contract-to-code checklist for reconciling the bounded Cleaning Spine v0
  substrate in orca-harness/cleaning/ against the current Cleaning README,
  foundation, boundary, projection, and corroboration/amplification sources.
use_when:
  - Checking whether the bounded Cleaning code stays inside the current source-invariant Cleaning contract.
  - Planning a narrow patch to orca-harness/cleaning/ or its focused unit tests.
  - Separating Cleaning substrate evidence from validation, readiness, or Judgment claims.
authority_boundary: retrieval_only
branch_or_commit: codex/cleaning-spine-continuation @ bc950cdfeeb3a02f33bf52217d71e049aa9093f2 plus uncommitted Cleaning hardening patch in this worktree
open_next:
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - orca-harness/cleaning/models.py
  - orca-harness/cleaning/core.py
  - orca-harness/cleaning/projection.py
  - orca-harness/tests/unit/test_cleaning_core.py
  - orca-harness/tests/unit/test_cleaning_projection_integration.py
stale_if:
  - Cleaning README or foundation changes the layer boundary, allowed transforms, OD-1, OD-4, OD-7, or build boundary.
  - The Data Capture / ECR / Cleaning / Judgment boundary or Projection Doctrine changes relevant ownership.
  - orca-harness/cleaning/ or the focused Cleaning tests are patched.
  - This branch is rebased past the commit named above without refreshing this checklist.
```

## Purpose

This checklist is a working reconciliation aid for the bounded Cleaning substrate
already present in `orca-harness/cleaning/`. It maps current contract obligations
to current code and tests so the next patch can target real drift instead of
re-litigating the Cleaning layer.

Do not use this artifact as validation, readiness, owner ratification, product
proof, production-Cleaning authorization, or authority to widen Cleaning into
near-match dedupe, clustering, ECR, Judgment, persistence, APIs, runners, or
source acquisition.

## Recheck Recipe

Before acting from this checklist:

1. Re-read the `open_next` sources above and check current `git status --short --branch`.
2. Confirm this file is still branch-current, or refresh it after code or contract changes.
3. Re-run the focused Cleaning tests before claiming the code still matches the checklist.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_cleaning_contract_to_code
  edit_permission: docs-write
  target_scope: docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md plus repo-map route
  dirty_state_checked: yes
  blocked_if_missing:
    - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md
    - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    - orca-harness/cleaning/models.py
    - orca-harness/cleaning/core.py
    - orca-harness/cleaning/projection.py
```

## Source Surface Read

Source anchors re-read for this reconciliation:

- `docs/hygiene/cleaning_spine_lane_handoff_v0.md` from the original workspace path; it is not present in this worktree and is orientation only.
- `AGENTS.md` from current task context.
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/workflows/orca_repo_map_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`
- `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md`
- `orca-harness/cleaning/models.py`
- `orca-harness/cleaning/core.py`
- `orca-harness/cleaning/projection.py`
- `orca-harness/tests/unit/test_cleaning_core.py`
- `orca-harness/tests/unit/test_cleaning_projection_integration.py`

At hardening time, HEAD remained `bc950cdfeeb3a02f33bf52217d71e049aa9093f2`; the branch status reported it behind local `origin/main` and dirty with this lane's modified/untracked artifacts. This checklist is tied to the current working tree patch, not a committed SHA.

## Contract-To-Code Checklist

| Contract obligation | Source anchor | Current code anchor | Current test/evidence anchor | Fit | Patch rule |
| --- | --- | --- | --- | --- | --- |
| Cleaning input handle is keyed to raw, with projection and ECR as optional keyed siblings over raw. | Cleaning foundation OD-1; Projection Doctrine OD-1; boundary note layer rules. | `CleaningInputHandle.raw_anchor`, optional `projection_ref` / `ecr_ref`, and `relation = keyed_siblings_over_raw` in `models.py`; projection adapter returns handles keyed to projection-row raw refs. | Projection integration tests assert Reddit and retail projection rows become raw-keyed Cleaning handles; core tests assert projection refs remain distinct from raw; ECR-ref tests assert valid refs share the raw packet key and mismatched refs reject. | Covered for current substrate. | Keep projection/ECR refs keyed siblings over raw; do not add ECR behavior beyond packet-id coupling without source authority. |
| Projection references must not become Cleaning, raw, or Judgment authority. | Cleaning README short mental model; Projection Doctrine non-claims and certification rules. | `CleaningProjectionRef` requires certification to show not cleaned and not Judgment-ready; projection adapter carries projection row data as secondary traceability. | `test_projection_ref_must_not_claim_cleaned_or_judgment_ready`; integration tests keep projection certification from Reddit and retail projections. | Covered for current substrate. | Keep projection refs secondary; do not add projection-derived canonical IDs or Cleaning/Judgment certification. |
| ECR reference remains pre-cleaning receipt material, not ECR implementation or Judgment claim. | Cleaning foundation inputs and OD-1; boundary note ECR row. | `CleaningEcrRef` carries `packet_id`, `ref_id`, optional `posture_kind`, optional `status`; `CleaningInputHandle` requires ECR packet to match raw packet. | `test_ecr_ref_may_share_raw_packet_key`; `test_ecr_ref_must_stay_keyed_to_raw_packet`. | Covered for current substrate packet-id coupling; ECR semantics beyond this remain out of scope. | Future ECR behavior must start from the ECR contract; do not infer it from Cleaning. |
| Non-destructive transform ledger must preserve originals, source identity, timing, hierarchy, semantic binding, and counts. | Cleaning README "What Is Generic"; foundation Non-Destructive Ledger Contract and Traceability rules. | `CleaningTransformLedgerEntry` binds a `CleaningTransform` to `CleaningPreservationCheck`; preservation validator rejects any failed required field. | `test_transform_ledger_requires_preservation_and_non_claims`; `test_preservation_check_rejects_hidden_loss`; `test_packet_rejects_unknown_transform_handle`. | Covered for current in-memory substrate. | Do not add destructive collapse, deletion, or hidden-loss success paths. |
| Dedupe core v0 is exact-identity only; near-match, copied-language grouping, and clustering are deferred unless separately owner-authorized. | Cleaning foundation OD-4; corroboration/amplification discipline; Projection Doctrine OD-4. | `CleaningTransform.validate_transform_contract` requires `method_or_rule = exact_identity` for `dedupe_mechanics` and rejects near-match / copied-language / clustering tokens; `derive_exact_identity_duplicate_groups` groups only full raw-anchor identity. | `test_core_v0_rejects_deferred_near_match_and_clustering_mechanics`; `test_exact_identity_dedupe_groups_only_full_raw_anchor_matches`. | Covered. | Any near-match, similarity, copied-language, or clustering request must stop for owner authorization or stay explicitly candidate/deferred outside core v0. |
| Cleaning may record mechanics but must not make Judgment claims or effects. | Cleaning README "What Is Not Generic"; foundation Layer Boundary, Non-Claims, and raw-pull rules; boundary note layer rules. | Required non-claims; Judgment-token validators now include the foundation-enumerated `artificial_amplification`, `discounted`, and `discounting` variants and apply to transform methods plus omissions/warnings/residuals/raw-pull triggers; `core.py` docstring says no Judgment effect. | `test_transform_rejects_judgment_vocabulary_in_method`; `test_transform_rejects_foundation_enumerated_judgment_reason_variants`; `test_transform_ledger_rejects_judgment_vocabulary_in_warnings`; `test_transform_ledger_rejects_foundation_judgment_vocabulary_in_text_fields`. | Covered for the current foundation-enumerated regression set; still a lexical guard, not proof against every equivalent Judgment-use label. | If adding new text-bearing fields or newly enumerated forbidden reasons, route them through the same no-Judgment vocabulary discipline and add focused regression tests. |
| Raw-pull/halt/escalate obligations must stay visible without pretending this bounded substrate implements trigger logic. | Cleaning foundation Traceability And Raw-Pull Rules; Projection Doctrine raw pull-in trigger table. | `CleaningTransformLedgerEntry.raw_pull_triggers` carries trigger text and uses the same no-Judgment validator; no Cleaning runner or trigger engine exists in the package. | `test_transform_ledger_allows_mechanical_raw_pull_trigger`; text-field rejection parametrization covers `raw_pull_triggers`. | Field covered; triggering logic classified out-of-substrate/deferred for `bounded_substrate_v0`. | Do not claim runtime raw-pull behavior until a separately authorized runner/trigger implementation exists. |
| Source-family adaptation stays at the edge; source-invariant core must not parse source families. | Cleaning README Source-Family Adaptation and Scalable Build Shape; foundation Source-Family Adaptation Boundary. | `models.py` docstring says adapters can feed models, core does not parse sources; `projection.py` adapts projection rows without source-family-specific model fields; `core.py` only groups raw-anchor identity. | Projection integration covers two source families: Reddit and retail/PDP projection rows. | Covered for current scope. | Keep new family parsing outside `cleaning/core.py`; only source-invariant handle, ledger, preservation, and exact-identity mechanics belong in core. |
| Runtime boundary is bounded substrate only: in-memory Pydantic models plus exact-identity deriver, not persisted storage/API/production Cleaning. | Cleaning README implementation/runtime authorization; foundation implementation/runtime authorization; repo map `orca-harness/cleaning/` row. | `orca-harness/cleaning/` contains `__init__.py`, `models.py`, `core.py`, `projection.py`; no Cleaning runner was observed under the package. | `rg --files orca-harness | rg "cleaning"` shows only the package and two focused tests. | Covered as navigation/code-shape evidence, not readiness. | Do not add persistence, runners, APIs, schedulers, dashboards, or production Cleaning behavior in this lane. |

## Candidate Patch Queue

The current hardening patch addresses the previously named ECR-ref test gap and the cross-vendor AR-01 token-guard gap. No additional code patch is queued from this checklist alone.

Before any end-to-end run:

1. Re-run focused Cleaning tests and markdown/diff hygiene.
2. If the owner authorizes a smoke path, scope a bounded non-proof smoke spec from existing capture/projection fixture into `CleaningPacket`; do not build a production runner from this checklist.

## Non-Claims

- Not validation, readiness, owner ratification, buyer proof, product proof, or implementation acceptance.
- Not authority to widen Cleaning beyond bounded substrate v0.
- Not authority to build ECR, Judgment, persistence, APIs, runners, dashboards, source acquisition, near-match dedupe, copied-language grouping, or clustering.
- Passing focused tests would show only that this bounded substrate still satisfies the exercised checks.
