# EP-35 Review-Routing Disposition Gate - Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated adversarial implementation/code review of the EP-35 review-routing
  disposition gate on branch claude/competent-jennings-692f70.
use_when:
  - Consuming review findings for the EP-35 review-routing disposition gate.
  - Checking whether the EP-35 gate has known correctness gaps before merge or
    follow-up patching.
authority_boundary: retrieval_only
reviewed_by: openai-gpt-5-codex
authored_by: claude-fable-5  # CA-supplied at adjudication per review-lanes provenance rule
branch_or_commit: claude/competent-jennings-692f70 @ 650b7ea8b995785585cba5c3ddabf5a5e0016e49
open_next:
  - .agents/hooks/check_review_routing.py
  - .agents/workflow-overlay/validation-gates.md
```

## Review Provenance

- `reviewed_by`: openai-gpt-5-codex.
- `authored_by`: `claude-fable-5` — reviewer recorded `unrecorded`; supplied by the commissioning CA at return adjudication (2026-07-02), per the review-lanes rule that these fields are operator/CA-set on the durable record.
- De-correlation measurement: cross-vendor satisfied at adjudication (openai-gpt-5-codex vs claude-fable-5 — OpenAI vs Anthropic lineage); the reviewer's own `not proven` stance at review time was correct given the then-unrecorded field.
- Requested output path: `docs/review-outputs/ep35_review_routing_disposition_gate_delegated_adversarial_code_review_v0.md`.
- Note: the requested path did not exist before this review. It was treated as the required durable review-output path, not as a source prompt.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 plus EP-35 target files
  edit_permission: docs-write
  target_scope: delegated adversarial code review report for EP-35 review-routing disposition gate
  dirty_state_checked: yes
  blocked_if_missing: requested review target, EP-35 implementation diff, review-output write path
```

## Source-Read Ledger

| Source | Status | Why read |
| --- | --- | --- |
| `AGENTS.md` | READ from current task context | Project behavior kernel and Orca work rules. |
| `.agents/workflow-overlay/README.md` | READ | Overlay entrypoint and authority boundary. |
| `.agents/workflow-overlay/source-loading.md` | READ | Start-preflight and source-loading rule. |
| `.agents/workflow-overlay/decision-routing.md` | READ | Cynefin routing for delegated/review work. |
| `.agents/workflow-overlay/review-lanes.md` | READ | Review lane output/provenance boundary. |
| `.agents/workflow-overlay/validation-gates.md` | READ targeted | EP-35 rule, enforcement placement, and DCP receipt. |
| `.agents/workflow-overlay/retrieval-metadata.md` | READ | Required header shape for this review output. |
| `.agents/workflow-overlay/artifact-roles.md` | READ | Review report write location and role. |
| `workflow-code-review` skill | READ | Implementation/code review mechanics; used advisory/findings-first. |
| `.agents/hooks/check_review_routing.py` | READ full | Primary implementation target. |
| `.githooks/commit-msg` | READ full | Local advisory wiring target. |
| `.github/workflows/ci.yml` | READ full | CI strict wiring target. |
| `.agents/hooks/README.md` | READ full | Hook documentation update. |
| `docs/decisions/overlay_enforcement_placement_classification_v0.md` | READ targeted | EP-35 enforcement-placement registration. |
| `docs/workflows/orca_repo_map_v0.md` | READ targeted | EP-35 repo-map registration. |
| `docs/review-inputs/fused_skill_post_a_closeout_hardening_review_input_v0.md` | READ full | Companion review input staged on the branch. |
| Git diff `main...HEAD` | READ | EP-35 changed-file surface and commit-message disposition evidence. |

**SOURCE_CONTEXT_READY**

## Validation Commands Run

| Command | Status | Evidence |
| --- | --- | --- |
| `python .agents/hooks/check_review_routing.py --selftest` | PASS | `SELFTEST OK`; all listed pure-function cases passed. |
| `python .agents/hooks/check_review_routing.py --strict --base main` | PASS | `check_review_routing --strict: OK (base: main)`. |
| `python .agents/hooks/check_dcp_receipt.py --strict --base main` | PASS | `OK -- every real receipt in the changed .md files is shape-valid`. |
| `python .agents/hooks/header_index.py --strict --base main` | PASS | `OK -- 5 changed durable .md file(s) all have headers and are map-reachable`. |
| `python .agents/hooks/check_map_links.py --strict` | PASS | `OK (0 findings)` with 33 annotated nonresolving links as debt. |
| `python .agents/hooks/check_review_output_provenance.py --selftest` | PASS | `SELFTEST OK`. |
| `python -m pytest` from `orca-harness/` | FAILED / timed out at harness boundary after output | 2363 passed, 4 skipped, 2 failed, 1 warning in reported pytest output. Failures were `test_cli_requires_exactly_one_target` and `test_youtube_shorts_fragrance_creator_observation_ledger_live_lake_refs_when_available`; both are outside the EP-35 checker surface and appear tied to local `ORCA_DATA_ROOT` / live-lake environment behavior. |
| Direct function probe for rename-out path list | CONFIRMED BUG SHAPE | `evaluate(['docs/moved/gate_target.py'], [], ...)` returned `[]`; including the old code-root path returned the expected missing-disposition findings. |

## Findings

### FIND-01: Recognized renames out of a code root bypass the strict gate

- Review target: `.agents/hooks/check_review_routing.py`.
- Location: `diff_paths()` lines 200-207 and `run_commit_msg()` lines 266-272.
- Evidence:

```python
parts = ln.split("\t")
if len(parts) < 2:
    continue
status, path = parts[0].strip(), parts[-1].strip()
touched.append(path)
if status.startswith("A") or status.startswith("R") or status.startswith("C"):
    added.append(path)
```

For Git rename rows, `--name-status --find-renames` emits `Rnnn<TAB>old<TAB>new`. The checker keeps only `parts[-1]`, so a recognized rename such as `R100<TAB>orca-harness/gate_target.py<TAB>docs/moved/gate_target.py` contributes only `docs/moved/gate_target.py` to `touched`. That path is outside `CODE_ROOTS`, so `touches_code_root()` returns false and the change is silently out of scope.

The same parse pattern exists in `run_commit_msg()`, so the local advisory nudge misses the same staged rename shape.

- Impact: A branch can remove or relocate code out of `orca-harness/` or `.agents/hooks/` without adding a review artifact or commit-message disposition, and `--strict` can still pass. This is a false negative in the exact code-root-change detector EP-35 is meant to enforce.
- Minimum closure condition: For rename/copy rows, include both old and new paths in `touched`; for `added`, include only the destination path when the destination is added/copied/renamed into a review root. Add a selftest that simulates `R100\torca-harness/a.py\tdocs/a.py` and requires a missing-disposition finding.
- Next authorized action: Patch the checker and its selftests, then rerun `check_review_routing.py --selftest` and `check_review_routing.py --strict --base main`.
- Patch queue: not authorized by this review report.

### FIND-02: Strict CI can still fail open on internal checker exceptions

- Review target: `.agents/hooks/check_review_routing.py`.
- Location: top-level exception handler lines 454-459.
- Evidence:

```python
if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # never ghost-fail; print and fail open
        sys.stderr.write("check_review_routing: internal error, allowing: %s\n" % exc)
        sys.exit(0)
```

The validation overlay says unknown findings and wrapper-internal errors default to `GATE FAIL`, never `INFO`; this checker's own detection contract only justifies fail-open for infrastructure gaps such as missing Git/base resolution. The blanket `except Exception` converts any strict-mode implementation bug after startup into a green CI step.

- Impact: EP-35 can report success when the checker itself crashes for a non-infrastructure reason. That weakens "preserve real failure visibility" for this new gate. The risk is partly inherited from sibling gates, but this change adds another strict CI gate with the same behavior.
- Minimum closure condition: Keep explicit fail-open only around known infrastructure gaps (`git` unavailable, base ref unresolvable, timeout where explicitly classified as infra). For `--strict` and `--selftest`, unexpected internal exceptions should exit nonzero. If report/commit-msg modes need advisory behavior, scope the fail-open there instead of using a blanket process-level catch.
- Next authorized action: Owner/implementer decision. This is broader than a one-line patch if the project wants all strict hooks to share the same error-bucket behavior, but EP-35 should not add a new strict gate that contradicts the validation-gate error policy.
- Patch queue: not authorized by this review report.

## Non-Finding Notes

- The branch's current PR-range gate passes because commit `adf6af3a` carries `review_routing_status: not_needed -- governance-substrate lane adjudicated in-chat with the owner this turn; no Review Timing Advisory was carried (the gate itself is the deliverable)`.
- The checker intentionally verifies disposition presence and shape only. This review does not treat the truth of `not_needed`, the quality of a filed review, or whether review should have been recommended as mechanically checkable by EP-35.
- Adding any review artifact under `docs/prompts/reviews/` or `docs/review-outputs/` satisfies the gate by shape. That is permissive, but it matches the stated "shape only" boundary and is not reported as a bug here.

## Review Use Boundary

Review findings are decision input only. They are not approval, validation, mandatory remediation, readiness, or executor-ready patch authority until the Chief Architect separately accepts or authorizes them.

This is an advisory implementation/code review. No formal Orca implementation-review lane verdict, validation pass/fail claim, mandatory remediation, approval, readiness claim, or patch queue is emitted.
