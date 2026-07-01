# Repo Map Retrieval Batches 3-5 Mega Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial artifact review report
scope: Consolidated delegated adversarial review and home-model adjudication for repo-map retrieval Batches 3-5.
use_when:
  - Auditing the Batch 3-5 repo-map retrieval hardening changes.
  - Checking why the remaining missing-header backlog was accepted as residual.
  - Reviewing the Milwaukee authority-boundary patch adjudication.
open_next:
  - docs/workflows/repo_map_retrieval_batches_3_5_v0.md
  - docs/decisions/orca_repo_map_architecture_mgt_v0.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/retrieval-metadata.md
authority_boundary: retrieval_only
```

## Review Provenance

- review_type: delegated adversarial artifact review plus home-model adjudication
- reviewed_by: unrecorded
- authored_by: unrecorded
- de_correlation_bar: same_vendor_sanity
- same_vendor_rationale: Bounded documentation/header hardening review; no cross-vendor discovery or no-new-seam claim is made.
- delegated_reviewer: in-session subagent `019f1f72-0f1c-7042-8dc1-3d03a19c9f82`
- output_mode: filesystem-output
- report_path: `docs/review-outputs/adversarial-artifact-reviews/repo_map_retrieval_batches_3_5_mega_adversarial_review_v0.md`

## Commission

Review the Batch 3-5 repo-map retrieval hardening changes for correctness, bloat, source support, false authority, stale claims, and avoidable operator friction.

Reviewed targets:

- `docs/workflows/repo_map_retrieval_batches_3_5_v0.md`
- `docs/workflows/orca_bootstrap_record.md`
- `docs/workflows/turn_08_workflow_bedrock_maximization.md`
- `docs/migration/import_queue.md`
- `docs/review-inputs/repo_structure_binding_v0_delegated_review_v0/MANIFEST.md`
- `docs/decisions/consultant_loop/milwaukee_initial_judgement.md`

## Source-Read Ledger

- `AGENTS.md`: project behavior and lifecycle constraints.
- `.agents/workflow-overlay/README.md`: overlay entrypoint.
- `.agents/workflow-overlay/decision-routing.md`: Cynefin routing requirement for substantial/review-affecting work.
- `.agents/workflow-overlay/retrieval-metadata.md`: retrieval-header scope, controlled authority boundary, and no-broad-backfill rule.
- `.agents/workflow-overlay/review-lanes.md`: adversarial artifact review lane, report location, provenance fields, and same-vendor sanity bar.
- `.agents/workflow-overlay/artifact-folders.md`: accepted artifact homes.
- `.agents/workflow-overlay/source-loading.md`: source-loading and retrieval budget context.
- `docs/decisions/orca_repo_map_architecture_mgt_v0.md`: accepted repo-map god-tier architecture and residuals.
- `docs/workflows/repo_map_retrieval_probe_batch_2_v0.md`: Batch 2 probe baseline and Windows encoding defect.
- `docs/workflows/repo_map_recent_changes/README.md`: recent-change satellite contract.
- Changed target artifacts listed in the commission.

Read-only checks observed locally during review:

- `header_index.py --health --oneline`: `retrieval health: 61 missing headers, 0 orphans`.
- `check_retrieval_header.py --changed --strict`: exit 0 (no findings).
- `header_index.py --index`: changed/new targets appear in the generated index.
- `check_map_links.py --strict`: `OK (0 findings)`.
- `header_index.py --selftest`: `SELFTEST OK`.
- `git diff --check`: exit 0.

## Findings

### AR-MEGA-01 - Accepted And Patched

phase: correctness / authority hygiene

location evidence:

- `docs/workflows/repo_map_retrieval_batches_3_5_v0.md` originally said the Milwaukee body remained non-authoritative after changing its header authority boundary.
- `docs/decisions/consultant_loop/milwaukee_initial_judgement.md` originally had seal and non-claim language, but did not explicitly say the artifact was not Orca decision/source authority after the header was normalized to `authority_boundary: retrieval_only`.

strongest defense:

- `retrieval_only` is the controlled header value, and `.agents/workflow-overlay/retrieval-metadata.md` says that header value does not create or upgrade authority.

why the defense failed:

- The schema change was correct, but the Batch record's preservation claim was stronger than the Milwaukee body text. Moving the non-authority boundary out of the header required the body to carry that boundary explicitly.

impact:

- Low but real false-authority risk: future readers could treat a sealed companion note under `docs/decisions/consultant_loop/` as more authoritative than intended.

minimum_closure_condition:

- Milwaukee's body explicitly states the note is a sealed comparison artifact only and not Orca decision authority, source-of-truth authority, validation evidence, readiness evidence, or outcome calibration.

adjudication:

- Accepted.
- Patched `docs/decisions/consultant_loop/milwaukee_initial_judgement.md` to add the explicit authority-boundary sentence in the body.
- Patched `docs/workflows/repo_map_retrieval_batches_3_5_v0.md` to say the body now carries the explicit non-authority boundary instead of relying on an unsupported preservation claim.

next_authorized_action:

- Re-run retrieval/header/link gates after staging so the new review report is included in changed-file checks.

patch_queue_entry authorized:

- No. This review is decision input and home-model adjudication, not an executor-ready patch queue.

## Non-Findings

- The targeted headers do not violate the no-broad-backfill rule: Batch 3 touched a small set of foundational workflow, migration, review-input, and decision-boundary artifacts rather than sweeping historical prompts/review outputs.
- Leaving 61 missing headers is an accepted residual under the current architecture: `--health` reports advisory backlog, while `--strict` gates changed durable docs forward-only.
- Batch 4 correctly found no recent-change notes to promote; the satellite contains only `README.md`.
- Batch 5 correctly avoided a standing gardener or broad stricter gate; the evidence showed one concrete Windows encoding defect, already patched in Batch 2, not repeated stale-note or missed-promotion failures.
- No changed-file retrieval header schema, generated index, or map-link defect was found in the reviewed set.

## Strict Boundaries And Not-Proven Claims

- Not validation, readiness, approval, repo-map completeness, source-of-truth promotion, or proof that all historical docs are retrievable.
- Not a cross-vendor discovery review and not a no-new-seam claim.
- Review findings are decision input only; remediation becomes mandatory only if separately accepted or bound by an authorized lane.
- A green retrieval/header/link check is routing hygiene only.
