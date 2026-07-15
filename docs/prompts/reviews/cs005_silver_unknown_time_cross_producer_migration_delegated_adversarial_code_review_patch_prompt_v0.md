# CS-005 Silver Unknown-Time Cross-Producer Migration — Delegated Adversarial Code Review And Patch Commission

```yaml
retrieval_header_version: 1
artifact_role: Forseti delegated adversarial code-review-and-patch commission
scope: >
  Revision-bound independent review and bounded patch hardening of the CS-005
  generic Silver unknown-time validator plus the four migrated strict-write
  producer families.
use_when:
  - Couriering the owner-authorized independent review-and-patch pass for implementation commit 234b9f223949f3200945e7b4522891babe0e6bf4.
  - Adjudicating whether that commit truthfully preserves unknown source-effective time without a generic null escape hatch.
stale_if:
  - The implementation target differs from commit 234b9f223949f3200945e7b4522891babe0e6bf4.
  - The named 25-file patch scope or the generic Silver unknown-time authority changes.
authority_boundary: commission_only
```

## Forseti Prompt Preflight

- `output_mode: file-write` in a clean isolated review worktree; return findings, diff, verdict, validation, and residuals in chat.
- `edit_permission: implementation-authorized` only for the exact named target set below.
- `expected_start: exact commit 234b9f223949f3200945e7b4522891babe0e6bf4`; stop if HEAD differs or the worktree is dirty.
- `receiver_mechanism: owner-couriered Codex managed-worktree task` rooted in the app-created target worktree; verify current root, exact HEAD, write/index capability, and no concurrent writer before source loading.
- `target_kind: delegated_code_review_and_patch` under `.agents/workflow-overlay/delegated-review-patch.md`.
- `access: repo`.
- `review_method: workflow-deep-thinking, then workflow-code-review`. Do not use artifact review as the code-review method.
- `de_correlation_bar: cross-vendor discovery`. The author family is OpenAI; the owner/courier must select a delegate from a different upstream model vendor and record that fact. Unknown lineage cannot support a no-new-seam claim.
- `scope: the exact implementation diff from f1ca90577efae7b9054274e753aacd83ec76bb41 to 234b9f223949f3200945e7b4522891babe0e6bf4 and only the named patchable files`.
- `review: coverage-first and adversarial`; report every failure mode, including minor or low-confidence findings.
- `validation: focused Silver/producer/Company Surface tests, affected regressions, diff-scoped gates, and the full harness when a patch is made`. Preserve `GATE PASS` / `GATE FAIL` / `INFO` / `OUT OF SCOPE`.
- `external boundary: jb and external workflow sources are not Forseti authority`. Installed/user/plugin skills and external reference folders are read-only.

## Why This Combined Pass Is Commissioned

Ordinary read-only review is insufficient because this architecture-doctrine change couples one generic fail-closed validator to four producer migrations, version/fingerprint re-surfacing, reader behavior, and authoritative contract wording. A reviewer who finds an implementation-local defect should close it in the same bounded pass, while the commissioning Chief Architect retains authority over what is kept.

## Required Start-State Read

Before analysis or edits:

1. Run `git rev-parse --show-toplevel`, `git rev-parse HEAD`, `git status --short --branch`, and `git diff --check`.
2. Require clean HEAD exactly `234b9f223949f3200945e7b4522891babe0e6bf4`. Stop as `BLOCKED_TARGET_DRIFT_DURING_REVIEW` on any mismatch, dirty file, untracked file, or concurrent writer.
3. Verify `f1ca90577efae7b9054274e753aacd83ec76bb41` is an ancestor and inspect the real diff with:
   - `git diff --stat f1ca90577efae7b9054274e753aacd83ec76bb41..HEAD`
   - `git diff --check f1ca90577efae7b9054274e753aacd83ec76bb41..HEAD`
   - `git diff --find-renames f1ca90577efae7b9054274e753aacd83ec76bb41..HEAD -- <named target files>`
4. State `SOURCE_CONTEXT_READY` only after the required authority is loaded.

## Required Authority, In Order

1. `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Targeted overlay sections:
   - `source-of-truth.md` direction-change propagation,
   - `source-loading.md`,
   - `decision-routing.md` receiver binding and exact revision,
   - `validation-gates.md` Current Gates,
   - `safety-rules.md`,
   - `artifact-roles.md`,
   - `prompt-orchestration.md` review defaults,
   - `review-lanes.md` Current Lanes, Review Doctrine, and Rules,
   - `delegated-review-patch.md` “When it applies”, “The loop”, lifecycle hard stop, and `delegated_code_review_and_patch`.
3. The generic Silver contract and validator:
   - `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
   - `forseti-harness/data_lake/silver_record.py`
   - `forseti-harness/data_lake/silver_census.py`
4. The four producer families, their routers, contracts, and focused tests in the named target set.
5. Company Surface logical/Silver mapping contracts and mapper only as the exposing consumer; preserve its signed temporal semantics.
6. `docs/decisions/silver_vault_legacy_record_convergence_v0.md` and the current lineage/physical-reference authority.
7. The exact base-to-target diff.

## Bound Truth Rule

The implementation is fit only if all of these remain true:

- An ordinary observation with known source-effective time has a non-empty `observed_at`.
- `observed_at: null` is accepted only for an observation whose `payload.observation.effective_interval` has `start: null`, `start_precision: "unknown"`, and a non-empty `unknown_reason`, plus non-empty `recorded_at`, `evidence_refs`, and `limitations` and truthful common `captured_at`.
- Capture, seed-generation, processing, or recorded time is never substituted for source-effective `observed_at`.
- Relationships retain their existing nullable behavior.
- Company Surface signed semantics and Silver’s closed common `record_kind` set do not change.
- No producer allowlist, legacy escape hatch, second marker grammar, or arbitrary null-time path exists.
- Transcript product mentions, TikTok comment attention, Instagram creator metrics, and YouTube creator metrics use the same grammar with truthful producer-owned provenance and time.
- Version/fingerprint changes re-surface output-shape migrations where the current pickup/obligation mechanism requires it.
- Census and other materially affected consumers do not reinterpret `captured_at` as `observed_at`.
- Physical reference verification, lineage authority, source adapters, schedulers, capture, UI, and caches remain unchanged.

## Exact Patchable Target Set

The delegate may edit only these files:

1. `docs/decisions/silver_vault_legacy_record_convergence_v0.md`
2. `forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
3. `forseti-harness/capture_spine/creator_profile_current/tiktok_comment_attention_producer.py`
4. `forseti-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py`
5. `forseti-harness/cleaning/transcript_product_lake.py`
6. `forseti-harness/data_lake/silver_census.py`
7. `forseti-harness/data_lake/silver_record.py`
8. `forseti-harness/runners/run_transcript_product_extract.py`
9. `forseti-harness/tests/contract/test_policy_module_version_pins.py`
10. `forseti-harness/tests/test_data_lake_indexes_rebuild.py`
11. `forseti-harness/tests/test_data_lake_sov_readout.py`
12. `forseti-harness/tests/test_sov_extraction_quality_eval.py`
13. `forseti-harness/tests/unit/test_company_surface.py`
14. `forseti-harness/tests/unit/test_creator_metric_silver_producer.py`
15. `forseti-harness/tests/unit/test_ig_reels_behavioral_lake.py`
16. `forseti-harness/tests/unit/test_silver_census_behavior.py`
17. `forseti-harness/tests/unit/test_silver_record.py`
18. `forseti-harness/tests/unit/test_tiktok_comment_attention_producer.py`
19. `forseti-harness/tests/unit/test_transcript_product_lake.py`
20. `forseti-harness/tests/unit/test_youtube_creator_metric_silver_producer.py`
21. `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`
22. `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_metric_silver_record_contract_v0.md`
23. `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md`
24. `forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md`
25. `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`

Everything else is read-only and flag-only. Do not silently widen scope. If a material fix requires another file, return the exact blocker and proposed re-commission instead of editing it.

## Adversarial Review Focus

Run `workflow-deep-thinking`, then `workflow-code-review` against the bound truth rule. In addition to normal correctness, regression, security, and test analysis, actively attack:

- partial-marker acceptance and truthy/empty edge cases;
- known-time records that incorrectly declare an unknown interval;
- null-time records that smuggle capture/record time into `observed_at`;
- producer evidence refs that are non-empty but not truthful provenance;
- missing truthful `recorded_at`/`captured_at` on any real router path;
- schema/fingerprint bumps that fail to re-surface prior acknowledgements or cause deterministic identity collisions;
- legacy fixtures or consumers that become silently excluded rather than explicitly invalid or unknown;
- census/window/readout paths that still use capture time as effective time;
- relationship regressions;
- Company Surface semantic drift;
- contract/validator/test disagreement;
- DCP receipt shape, rotation limit, and materially affected router/consumer coverage.

Report every discovered failure mode. Each finding must include severity (`critical` / `major` / `minor`), confidence (`high` / `medium` / `low`), exact file/line evidence, why it violates the bound rule, `minimum_closure_condition`, and `next_authorized_action`. List defeated candidate findings under `considered_and_defended`.

## Patch Discipline

- Patch only findings that are real, inside the named target set, and resolvable without changing the architecture decision.
- Use the smallest complete patch. Every changed line must trace to a finding or required validation.
- Preserve failure visibility; do not weaken the validator, add allowlists, or make tests bypass the strict front door.
- Do not fabricate timestamps, evidence, provenance, or limitations.
- If the defect requires a new unknown-time grammar, a new producer family, Company Surface semantic change, common `record_kind` change, or another architecture decision, return `NEEDS_ARCHITECTURE_PASS` and stop patching that issue.
- Fresh-read the final diff and verify the patchable-file boundary.

## Validation

At minimum, after any patch run:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q --basetemp pytest_cs005_review_focus `
  forseti-harness/tests/unit/test_silver_record.py `
  forseti-harness/tests/unit/test_silver_census_behavior.py `
  forseti-harness/tests/unit/test_company_surface.py `
  forseti-harness/tests/unit/test_transcript_product_lake.py `
  forseti-harness/tests/unit/test_tiktok_comment_attention_producer.py `
  forseti-harness/tests/unit/test_creator_metric_silver_producer.py `
  forseti-harness/tests/unit/test_youtube_creator_metric_silver_producer.py `
  forseti-harness/tests/contract/test_policy_module_version_pins.py
```

Also run the directly affected regression files, `git diff --check`, all Current Gates with `FORSETI_DIFF_BASE=f1ca90577efae7b9054274e753aacd83ec76bb41`, and the full harness when feasible. Clean only the named review basetemp and `_scratch/` artifacts after confirming provenance. A timeout is `INFO`, not a pass; report the last observed progress and any lingering worker cleanup.

## Delegate Lifecycle Hard Stop

You may edit only the commissioned target set. Do not commit, push, open or update a PR, merge, stash, reset, clean the worktree, run repository hygiene, or advance any lifecycle state. The commissioning Chief Architect owns every keep/land decision after adjudication.

## Required Return

Return, in this order:

1. A concise findings-first summary.
2. Detailed findings and `considered_and_defended`.
3. Exact changed-file list and unified diff summary.
4. Validation table using `GATE PASS` / `GATE FAIL` / `INFO` / `OUT OF SCOPE`.
5. Verdict: `CLEAN`, `PATCHED_CLEAN`, `PATCHED_WITH_RESIDUALS`, `BLOCKED`, or `NEEDS_ARCHITECTURE_PASS`.
6. Residual risks and any requested re-commission.
7. A paste-ready courier block for the commissioning Chief Architect.

End the courier block by instructing the Chief Architect to apply `.agents/workflow-overlay/communication-style.md` → `Review Adjudication Next Step`: adjudicate findings, diff, verdict, and residuals as claims; close self-closable material issues in the same turn; route only genuinely external closures; once clean, batch lifecycle follow-ups into exactly one land step; then inspect the visible active goal for 1–5 material next moves or record `no_visible_active_goal`.

Review findings are decision input only. They are not approval, validation, mandatory remediation, or authority to keep or land the delegate’s patch.
