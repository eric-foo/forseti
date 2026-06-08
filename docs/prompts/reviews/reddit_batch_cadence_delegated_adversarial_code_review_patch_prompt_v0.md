---
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: Delegated adversarial code review-and-patch prompt for the Reddit old-HTTP batch cadence patch.
use_when:
  - Reviewing the bounded cadence implementation added to the old Reddit Direct HTTP batch runner.
  - Checking that cadence receipts, tests, and operator docs preserve hard caps and visible failures.
authority_boundary: prompt_only
---

# Reddit Batch Cadence Delegated Adversarial Code Review-And-Patch Prompt v0

## Objective

Perform a de-correlated adversarial code review-and-patch pass on the bounded
Reddit old-HTTP batch cadence patch. The goal is to catch bugs, fake-success
paths, documentation drift, or receipt ambiguity introduced by adding
`bounded_jitter` cadence support.

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: patch-only within submitted target files
  target_scope: reddit_old_http_batch cadence implementation, tests, and docs
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, .agents/workflow-overlay/README.md, target files, validation evidence below
```

Workspace: `C:\Users\vmon7\Desktop\projects\orca`
Expected branch: `ecr-sp3-timing-deriver-slice1`
Observed short HEAD at prompt authoring: `db519f0`

Dirty-state allowance: the worktree is known dirty. Review only the target files
listed below. Do not treat unrelated dirty or untracked files as review scope.

## Receiving Actor / De-Correlation Receipt

- author / CA / home model family: GPT-5 / Codex home model
- required controller: different vendor or materially different model family
  from the author/home model
- current receiving actor role: controller, if this prompt is pasted directly
  to the reviewer; otherwise home-dispatcher must launch a de-correlated
  controller
- de-correlation status: controller must verify before review; if not
  satisfied, return `BLOCKED_CONTROLLER_NOT_DECORRELATED`
- model choice is a who-constraint, not a recommendation

## Required Method Sequence

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD `workflow-deep-thinking`; do not apply it before source
   readiness.
4. REFERENCE-LOAD `workflow-code-review`; do not apply it before source
   readiness.
5. SOURCE-LOAD the target files and validation evidence listed below.
6. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
7. After `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the
   failure modes, then APPLY `workflow-code-review`.
8. Patch only material findings inside the submitted target files. Do not stage,
   commit, push, install, deploy, or run live Reddit/network capture.

## Target Files

Editable review-and-patch scope:

- `orca-harness/source_capture/cadence.py`
- `orca-harness/runners/run_reddit_old_http_batch.py`
- `orca-harness/tests/unit/test_reddit_old_http_batch.py`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `docs/product/source_capture_toolbox/README.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`

Read-only context if needed:

- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `orca-harness/tests/unit/test_reddit_batch_quality_summary.py`

## Validation Evidence To Inspect

The author reported these focused validation commands passing after the patch:

```powershell
python -m pytest -p no:cacheprovider -q --basetemp orca-harness\_pytest_tmp_reddit_cadence orca-harness\tests\unit\test_reddit_old_http_batch.py
```

Observed output:

```text
..........                                                               [100%]
```

```powershell
python -m pytest -p no:cacheprovider -q --basetemp orca-harness\_pytest_tmp_reddit_cadence_quality orca-harness\tests\unit\test_reddit_batch_quality_summary.py
```

Observed output:

```text
........                                                                 [100%]
```

You may rerun these tests. Do not run live network, live Reddit, proxy,
CloakBrowser, browser, archive, or warm-JSON commands.

## Review Questions

Prioritize blocker and major issues. Patch minor issues only when the patch is
small and directly reduces false-success risk.

1. Does `bounded_jitter` always preserve hard ceilings: exact supplied URL
   count, `max_urls`, no retries, no source discovery, no browser/proxy
   fallback, and no live expansion?
2. Can the cadence planner create schedules outside its stated window, below
   the minimum gap, above the maximum gap, or with hidden deterministic bias
   that makes the receipt misleading?
3. Does invalid cadence fail before creating packet directories or a
   `batch_summary.json`?
4. Are `batch_summary.json` and per-row receipts clear about which delay mode is
   active, including `delay_seconds: null` under `bounded_jitter`?
5. Do tests prove both fixed backwards-compatible behavior and bounded-jitter
   provenance without using real network calls?
6. Do docs explain how to use the cadence feature without implying stealth,
   human impersonation, access-control bypass, broad crawl, monitoring, proxy
   escalation, or commercial posture?
7. Did the patch accidentally broaden Source Capture Armory authority,
   candidate intake, warm JSON, CloakBrowser, archive fallback, ECR, Cleaning,
   Judgment, fixture admission, or source-quality scoring?

## Patch Scope

Allowed:

- patch the six target files above;
- add or adjust unit tests in `orca-harness/tests/unit/test_reddit_old_http_batch.py`;
- adjust wording in the listed docs to remove ambiguity introduced by this
  cadence patch.

Forbidden:

- edits outside the target files;
- live capture, live Reddit access, proxy use, CloakBrowser use, browser use,
  archive calls, warm-JSON diagnostics, or installs;
- staging, committing, pushing, deployment, fixture admission, source-quality
  scoring, ECR, Cleaning, Judgment, source discovery, monitoring, or commercial
  claims;
- broad refactors, new batch runners, source-discovery/crawler work, or moving
  docs between folders.

If the correct fix requires broader architecture or a new runner, return
`NEEDS_ARCHITECTURE_PASS` and do not patch that broader work.

## Required Output

Write the full review report to:

`docs/review-outputs/reddit_batch_cadence_delegated_adversarial_code_review_patch_v0.md`

The report must include:

- source context status;
- findings first, ordered by severity with file/line references;
- patches applied, if any;
- unified diff or a precise changed-file summary;
- validation run or explicit not-run status;
- residual risk;
- verdict: `PATCHED_FOR_CA_ADJUDICATION`, `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`,
  `NEEDS_ARCHITECTURE_PASS`, or `BLOCKED_*`;
- non-claims: no deployment, no staging/commit, no live Reddit/network use, no
  source-capture readiness claim, and no auto-keep before CA adjudication.

After writing the report, return only a compact human summary and the report
path in chat. The reviewer output is decision input for CA adjudication, not
automatically kept truth.
