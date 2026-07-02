# Bronze Catalog v0 Delegated Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: Read-only de-correlated adversarial code review prompt for Bronze Catalog v0 in PR #485.
use_when:
  - Commissioning an independent review of the Bronze Catalog v0 implementation patch.
  - Checking whether the generated Bronze catalog remains non-authoritative, deterministic, and rebuildable from verified raw packets.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/source-loading.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
branch_or_commit: codex/bronze-catalog-v0 at b2a9c8f6cd4f74c11bb71a8a9794e174e2f76714
stale_if:
  - PR #485 changes after commit b2a9c8f6cd4f74c11bb71a8a9794e174e2f76714.
  - The base branch changes away from codex/bronze-v41-clean-verify.
  - Any target file listed below is renamed or replaced.
```

## Commission

Perform a read-only, de-correlated adversarial implementation/code review of
Bronze Catalog v0 in Orca PR #485:

`https://github.com/eric-foo/orca/pull/485`

The review target is the implementation patch at:

```text
base: codex/bronze-v41-clean-verify
head: b2a9c8f6cd4f74c11bb71a8a9794e174e2f76714
compare: codex/bronze-v41-clean-verify..b2a9c8f6cd4f74c11bb71a8a9794e174e2f76714
```

This prompt file may appear in a later branch commit for routing. It is not part
of the review target. Review the four target files named below and the diff
between the base and implementation commit.

This is decision input only. Do not patch files, commit, stage, push, retarget
the PR, create generated catalog output, run live capture, access external
services, or broaden into product planning.

## Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
authorization_basis: current owner request, "prompt - delegate patch review"
objective: commission an independent adversarial code review of Bronze Catalog v0 before CA adjudication
intended_decision: whether PR #485 has blocker/major correctness or false-traceability defects before merge consideration
output_mode: review-report
prompt_artifact_path: docs/prompts/reviews/bronze_catalog_v0_delegated_adversarial_code_review_prompt_v0.md
required_review_report_path: docs/review-outputs/bronze_catalog_v0_delegated_adversarial_code_review_v0.md
template_kind: review
template_source: workflow-prompt-orchestrator + workflow-code-review contract; no repo-code-review template is bound in Orca's template registry
edit_permission: read-only review; report-write only to required_review_report_path
target_files_or_dirs:
  - docs/workflows/orca_repo_map_v0.md
  - orca-harness/data_lake/catalog.py
  - orca-harness/runners/run_data_lake_catalog.py
  - orca-harness/tests/test_data_lake_catalog.py
source_pack: custom S1 plus target implementation diff and validation evidence
dirty_state_allowance: target implementation commit is clean; this prompt file, if present after b2a9c8f6, is out of review scope
controlling_source_state: prompt author read AGENTS.md from current context, overlay README, prompt-orchestration, delegated-review-patch, review-lanes, source-loading, artifact-folders, retrieval-metadata, template-registry, workflow-code-review, and workflow-deep-thinking
branch_or_commit_reference: codex/bronze-catalog-v0 at b2a9c8f6cd4f74c11bb71a8a9794e174e2f76714
doctrine_change_decision: no doctrine change intended; this is review setup for a generated implementation index
isolation_decision: existing clean worktree C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-catalog-v0 on codex/bronze-catalog-v0; root checkout is dirty and not the review target
validation_gates: reviewer inspects supplied validation evidence and may rerun local tests; no validation/readiness claim is created by this review prompt
thread_operating_target_continuity: carried_forward=no; no visible active thread_operating_target was bound for this prompt artifact
```

## Receiving Actor / De-Correlation Receipt

- author / CA / home model family: OpenAI GPT-family Codex home model.
- required reviewer/controller family: different vendor or model lineage from
  the author/home family when this is used as a cross-vendor discovery pass.
- de-correlation is a who-constraint, not a model recommendation. This prompt
  does not prescribe, rank, or recommend a runtime model.
- current receiving actor role: controller, if this prompt is pasted directly
  to the independent reviewer; otherwise the home dispatcher must courier it to
  a de-correlated controller.
- if the receiving reviewer cannot satisfy the different-family requirement,
  state `BLOCKED_CONTROLLER_NOT_DECORRELATED` or record
  `de_correlation_bar: same_vendor_sanity` with rationale. Do not claim
  cross-vendor discovery / no-new-seam.
- reviewer output is decision input for CA adjudication only; it is not approval,
  validation, readiness, or auto-keep authority.

## Required Method Sequence

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/review-lanes.md`.
4. Read `.agents/workflow-overlay/prompt-orchestration.md`.
5. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
6. REFERENCE-LOAD `workflow-code-review`. Do not APPLY it yet.
7. SOURCE-LOAD the target files, support files, diff, and validation evidence
   listed below.
8. Declare `SOURCE_CONTEXT_READY` only after the required sources and target
   diff are loaded. If any required source is missing, declare
   `SOURCE_CONTEXT_INCOMPLETE` and name the missing source.
9. Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame
   failure modes, then APPLY `workflow-code-review` in adversarial posture.
10. Write the full durable report to
    `docs/review-outputs/bronze_catalog_v0_delegated_adversarial_code_review_v0.md`.
11. After the report is written, return only a compact human summary plus a
    fenced `review_summary` YAML block in chat.

If `workflow-code-review` is unavailable or unresolved after source readiness,
return a blocked or advisory-only result and do not emit formal verdicts,
readiness claims, mandatory remediation, patch queues, executor-ready handoffs,
or validation claims.

## Required Source Basis

Read these authority and prompt-policy files:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`

Read these implementation/source files fully:

- `orca-harness/data_lake/root.py`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/writer.py`
- `orca-harness/data_lake/catalog.py`
- `orca-harness/runners/run_data_lake_catalog.py`
- `orca-harness/tests/test_data_lake_catalog.py`
- `docs/workflows/orca_repo_map_v0.md`

Inspect this diff exactly:

```powershell
git diff codex/bronze-v41-clean-verify..b2a9c8f6cd4f74c11bb71a8a9794e174e2f76714 -- docs/workflows/orca_repo_map_v0.md orca-harness/data_lake/catalog.py orca-harness/runners/run_data_lake_catalog.py orca-harness/tests/test_data_lake_catalog.py
```

Expected target changed files at the implementation commit:

```text
docs/workflows/orca_repo_map_v0.md
orca-harness/data_lake/catalog.py
orca-harness/runners/run_data_lake_catalog.py
orca-harness/tests/test_data_lake_catalog.py
```

## Implementation Summary To Verify

The implementation is intended to add Bronze Catalog v0:

- generated read state under `indexes/derived_retrieval/bronze_catalog/v0`;
- raw manifests and preserved bytes remain authoritative;
- rebuild scans committed sharded `raw/<packet_shard>/<packet_id>/` packets;
- every catalog entry is built through `DataLakeRoot.load_raw_packet(packet_id)`,
  so preserved body hashes are re-verified before indexing;
- no manifest v1 schema change;
- no semantic physical folders;
- no source-capture runner rewiring;
- universal facets for source family, source surface, session identity, series,
  and locator hash;
- source-family extractor for IG reels-grid payloads emitting creator handle,
  creator numeric id, and shortcode facets;
- inspect mode reports missing, stale, orphaned, and unreadable generated index
  state;
- rebuild mode replaces only the generated catalog directory;
- CLI is inspect-only by default and mutates only with `--rebuild`.

## Validation Evidence To Inspect

The implementation author reported:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --no-header --no-summary tests\test_data_lake_catalog.py -q
```

Observed result:

```text
4 passed
```

Broader lake/capture regression pack:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m pytest -p no:cacheprovider --no-header --no-summary tests/test_data_lake_catalog.py tests/test_data_lake_doctor.py tests/test_data_lake_root.py tests/test_data_lake_availability.py tests/test_data_lake_sharding.py tests/test_data_lake_record_set.py tests/test_data_lake_rebuild_proof.py tests/test_data_lake_read_loader.py tests/test_ecr_lake_pilot.py tests/test_signal_content_lake_pilot.py tests/test_retail_pdp_lake_pilot.py tests/test_ig_projection_lake_pilot.py tests/test_fragrantica_projection_lake_pilot.py tests/test_fragrantica_cleaning_lake_pilot.py tests/test_fragrantica_capture_to_silver_e2e.py tests/unit/test_silver_lineage.py tests/contract/test_capture_runner_lake_seam_coverage.py
```

Observed result:

```text
144 passed, 1 skipped
```

Other reported checks:

```powershell
git diff --check
python -m compileall -q data_lake\catalog.py runners\run_data_lake_catalog.py tests\test_data_lake_catalog.py
python .agents\hooks\check_retrieval_header.py --changed --strict
python .agents\hooks\header_index.py --strict
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_repo_map_freshness.py --changed --strict
```

Reported status: all passed; `header_index --strict` reported OK and
`check_map_links --strict` reported OK with annotated nonresolving debt.

You may rerun focused local tests and static checks. Do not run live capture,
network fetches, external services, browser automation, package installs,
deployment, or data-root mutation outside test temp roots.

## Review Questions

Prioritize blocker and major issues. Be adversarial about material
implementation risks:

1. **Authority boundary:** can any generated catalog file become de facto
   authority over raw manifests or preserved bytes?
2. **Rebuildability:** is the catalog deterministic and byte-rebuildable from
   raw only, without timestamps, ambient filesystem ordering, or stale generated
   state?
3. **Verified reads:** does every indexed packet go through verified
   `load_raw_packet` reads, including preserved file body hash checks?
4. **Sharded raw correctness:** can wrong-shard, malformed, legacy-flat, or
   partial raw containers be indexed accidentally?
5. **Inspect semantics:** can `inspect_catalog` miss stale/orphaned/missing
   generated files, duplicate packet entries, corrupt JSON, or a stale facet
   index while reporting `ok`?
6. **Facet correctness:** do universal facets and IG reels-grid extractor facts
   remain factual retrieval hints rather than semantic truth claims? Are handle,
   numeric id, shortcode, locator hash, session, and series values normalized
   without losing traceability?
7. **Future lane adaptability:** can new source-family extractors be added
   without changing manifest v1, physical raw layout, or downstream assumptions?
8. **Path and filename safety:** does `_safe_name` avoid traversal, unstable
   names, collisions, excessive length, or unreadable lookup paths?
9. **CLI fail-closed behavior:** does the runner surface root errors and return
   nonzero on stale/missing/orphan catalog state without fake success?
10. **Test strength:** are tests strong enough to catch non-authoritative
    rebuild, stale detection, orphan replacement, IG facet extraction, and CLI
    exit behavior without circularly asserting implementation details?
11. **Repo-map accuracy:** does the repo map describe the feature without
    overclaiming readiness, validation, raw authority, source-capture runner
    wiring, or production runtime?

## Findings Standard

Report findings first, ordered by severity. Use:

- `critical`: defect can corrupt raw authority, silently create false catalog
  truth, hide stale/generated index failure, or break verified raw reads.
- `major`: defect can produce wrong retrievability, miss stale/orphaned state,
  make future lane extractors brittle, or leave a material test gap before merge.
- `minor`: bounded correctness, documentation, test, or maintainability issue
  that should be considered but does not block by itself.
- `advisory`: optional hardening or future-work note.

Every actionable finding must include:

- finding id;
- severity;
- location with file and line;
- implementation evidence;
- authority/evidence basis;
- impact;
- minimum closure condition;
- next authorized action.

Do not emit `patch_queue_entry`. Do not patch files. Advisory remediation
direction is allowed, but executor-ready instructions are not.

## Output Contract

Write the full durable report to:

`docs/review-outputs/bronze_catalog_v0_delegated_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by`: operator/tooling-supplied model+version, or `unrecorded`;
- `authored_by`: `OpenAI GPT-family Codex home model`, or `unrecorded` if the
  operator does not accept that provenance;
- `de_correlation_bar`: `cross_vendor_discovery` |
  `same_vendor_sanity` | `self_fallback`;
- source context status;
- deep-thinking and code-review invocation status;
- findings first, ordered by severity with file/line references;
- validation evidence inspected and any checks rerun, or explicit not-run
  status;
- `not_proven` boundaries and strict-only blockers;
- residual risk;
- recommendation: `no_blockers_found`, `minor_findings_only`,
  `revise_before_merge`, or `blocked`.

After successfully writing the report, return only a concise chat summary plus:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/bronze_catalog_v0_delegated_adversarial_code_review_v0.md
  recommendation: no_blockers_found | minor_findings_only | revise_before_merge | blocked
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  findings_count:
    critical: <n>
    major: <n>
    minor: <n>
    advisory: <n>
  blocking_or_major_findings:
    - <id and one-line summary, or none>
  next_action: <owner/implementer next action>
```

Review-use boundary: findings are decision input only. This review does not
approve, validate, require remediation, authorize patches, authorize commits,
authorize merge, or authorize production/source-system runtime.
