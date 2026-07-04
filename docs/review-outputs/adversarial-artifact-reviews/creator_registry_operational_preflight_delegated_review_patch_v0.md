# Creator Registry Operational Preflight — Delegated Adversarial Review-and-Patch (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + patch record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode delegated adversarial
  review-and-patch pass over PR #654 (Creator Registry match preflight
  operational visibility): the runbook binding, the usage note, and the
  repo-map index edit. Records findings, the applied bounded patch, and
  validation evidence for home-CA adjudication.
use_when:
  - Checking what the PR #654 operational-visibility review found and fixed.
  - Adjudicating whether the applied runbook patch should be kept.
authority_boundary: retrieval_only
review_provenance:
  authored_by: "OpenAI / GPT / Codex"
  reviewed_by: "Anthropic claude-sonnet-5 (Claude Code)"
  de_correlation_bar: cross_vendor_discovery
  access_mode: "repo (worktree C:/Users/vmon7/Desktop/projects/orca/worktrees/creator-registry-operational-preflight, branch codex/creator-registry-operational-preflight, HEAD 2e308ab2014313acd6a7432a75654c8dd7db7b93 confirmed clean at start)"
  dispatch: "PR #654 lane-scoped paste-ready prompt (chat-delivered; not filed as a canonical docs/prompts/** artifact)"
  reviewer_recommendation: accept_with_patch
  findings: 3
non_claims: >
  Advisory review-and-patch decision input only — not approval, not
  validation, not readiness, not mandatory remediation, and not a merge
  decision. The commissioning Chief Architect adjudicates what is kept.
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_registry_operational_preflight_delegated_review_patch_v0.md
  recommendation: accept_with_patch
  reviewed_by: "Anthropic claude-sonnet-5 (Claude Code)"
  authored_by: "OpenAI / GPT / Codex"
  de_correlation_bar: cross_vendor_discovery
  same_vendor_rationale: null
  findings_count: 4
  blocking_findings: []
  advisory_findings:
    - "AR-03: folder README uses a pre-existing 'preflight/dedupe list' label for creator_registry_index_v0.json; out of PR #654 patch scope."
  patches_applied:
    - "AR-01: runbook new_capture gate now binds to intended_action: new_capture plus can_start_new_capture: true."
    - "AR-02: runbook Agent Boundary now authorizes running the Creator Registry match preflight runner."
    - "AR-04: DCP receipt now records the observed stale_language_search_result."
  residual_risk:
    - "AR-03 remains unpatched pending owner decision or a separate README-scoped pass."
    - "Docs-only wording is not mechanically bound to the Python can_start_new_capture field name."
  next_action: "Chief Architect adjudicates keep/modify/revert for the three applied hunks and owner decides whether AR-03 warrants a follow-up pass."
```

## Commission

Reviewed PR #654 target scope only:

- `orca-harness/docs/source_capture_agent_runbook.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
- `docs/workflows/orca_repo_map_v0.md`

Purpose stated in the commission: PR #654 makes Creator Registry match
preflight operationally visible to cold source-capture agents before new
social creator/account capture. The named risk is that the runbook, usage
note, or repo map could create a false sense of enforcement, contradict
source-capture boundaries, overclaim registry readiness, miss a required
receipt/reporting surface, or make the preflight hard for a cold agent to
execute correctly.

## Source Context

`SOURCE_CONTEXT_READY`. Read before findings: `AGENTS.md`; the Forseti
overlay README; `prompt-orchestration.md` (Forseti Prompt Preflight +
`review-lanes.md`/`delegated-review-patch.md` sections); `review-lanes.md`
(Current Lanes, Review Doctrine, Rules); `delegated-review-patch.md` (When it
applies, The loop, Access selection rule, De-correlation, Overlay Interface);
`validation-gates.md` (Current Gates, Prompt Orchestration Gates,
Enforcement Placement); `source-loading.md` (Rule, Forseti Start Preflight).
Reference-loaded (not applied until source readiness) `workflow-deep-thinking`
and `workflow-adversarial-artifact-review`.

Target diff read in full (`git diff origin/main...HEAD`, one commit
`2e308ab2` "docs: bind creator registry preflight in capture runbook",
77 insertions / 2 deletions across exactly the three named files — no
scope drift). Evidence sources read to check claims against ground truth
rather than trusting the doc's own prose:

- `orca-harness/runners/run_creator_registry_match_preflight.py` (confirms
  `--candidates`/`--output`/`--registry` flags match the usage note's command
  shape; confirms exit 0 vs 2 fail-closed behavior).
- `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py`
  (confirms `decision` enum, `action_status`, and the authoritative
  `can_start_new_capture` boolean; confirms non-claims list).
- `orca-harness/tests/unit/test_creator_registry_match_preflight.py` (12
  tests; confirms `existing_match`/`new_candidate`/`ambiguous_match`/
  `invalid_candidate` behavior and exit codes empirically, not from docs).
- `orca-harness/README.md`, `orca/product/spines/capture/core/source_capture_toolbox/README.md`,
  `orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md`
  (checked the runbook's own `intentionally_not_updated` claims about these
  three files against their actual content rather than accepting the claim).

`forseti_start_preflight`: `agents_read: yes`, `overlay_read: yes`,
`source_pack: custom (targeted overlay sections per Routine Read Shapes +
full target-file/code/test read)`, `edit_permission: patch-only (named
target: orca-harness/docs/source_capture_agent_runbook.md)`,
`target_scope: PR #654 three named files`, `dirty_state_checked: yes
(clean at start)`.

## Phase 1 — Correctness Findings

### AR-01 (major) — Runbook proceed-condition does not bind to the runner's authoritative safety field

- **Location**: `orca-harness/docs/source_capture_agent_runbook.md`,
  "Required Inputs" section, the sentence beginning "Do not start
  `new_capture` unless the receipt row is `new_candidate` and action status is
  allowed." (pre-patch).
- **Source authority**:
  `registry_match_preflight.py::_build_candidate_result` computes
  `can_start_new_capture = action_status == "allowed" and
  candidate["intended_action"] == "new_capture"`. A candidate preflighted
  with `intended_action: classify` can independently receive
  `decision: new_candidate` and `action_status: allowed`
  (`_action_disposition`: `classify` always returns `"allowed"`), while
  `can_start_new_capture` is `False` for that same row because the query
  never asserted `new_capture`.
- **Failure scenario**: a cold agent preflights a candidate batch with
  `intended_action: classify` (plausible reading of "just checking before
  deciding"), observes `decision: new_candidate` and `action_status:
  allowed`, and — following the runbook's literal wording, which names only
  those two fields — concludes the `new_capture` gate is cleared. The
  runner itself never authorized `new_capture` for that query
  (`can_start_new_capture` is `False`), so the agent proceeds on a receipt
  that does not actually clear the action it takes. This is exactly the
  "false sense of enforcement" failure mode named in the commission's
  purpose statement.
- **Strongest defense**: the runbook directs the agent to the usage note for
  "candidate JSON shape, receipt outcomes, and the runner command," and the
  usage note's own text — "`new_candidate`: a new capture may proceed for
  candidates whose `intended_action` is `new_capture`" — already states the
  correct compound condition. A cold agent who reads the usage note in full
  would not be misled. This defense fails as a sufficient safeguard because
  the runbook restates a shorter, independently-parseable proceed condition
  inline rather than only pointing at the usage note, and a cold agent
  skimming the runbook's own four-decision-category summary (which appears
  self-contained) has no textual signal that the runbook's own restatement
  is incomplete.
- **Verdict**: CONFIRMED — patched.
- **minimum_closure_condition**: the runbook's proceed condition names the
  authoritative `can_start_new_capture` field (or equivalently states the
  `intended_action: new_capture` precondition) so a row satisfying only
  `decision: new_candidate` + `action_status: allowed` from a non-`new_capture`
  query cannot be read as clearing the gate.
- **next_authorized_action**: patched in place (see Patch Applied below);
  CA adjudicates keep/revert.

### AR-02 (major) — "Agent Boundary" authorized-actions list omits the newly-required preflight action

- **Location**: `orca-harness/docs/source_capture_agent_runbook.md`, "Agent
  Boundary" section, "The agent may:" list (pre-patch: ends at "inspect
  `manifest.json`, `receipt.md`, and `raw/`;").
- **Source authority**: the runbook's own framing — "Do not use methods that
  do not have an implemented runner in this runbook" under "The agent must
  not" — treats the "may" list as the boundary of authorized actions.
  "Required Inputs" (the added text) obligates running
  `run_creator_registry_match_preflight.py` before new social
  creator/account capture, but that action was not added to the "may" list.
- **Failure scenario**: a cold agent that treats "Agent Boundary" as the
  exhaustive authorization surface (a reasonable reading, since every other
  runner named anywhere in the runbook also appears there) either hesitates
  to run the preflight runner because it isn't listed as an authorized
  action, or runs it without a clear textual grant, both of which are
  friction/consistency defects in a runbook whose stated purpose is to tell
  a cold agent exactly what it may do.
- **Strongest defense**: "Required Inputs" is itself an operative
  instruction and arguably implies authorization by direction. This defense
  is weak because the doc's own internal convention (every other runner
  action is listed in both places: instructed under its section AND granted
  under "Agent Boundary") is broken only for this one new action, which
  reads as an oversight rather than a deliberate omission.
- **Verdict**: CONFIRMED — patched.
- **minimum_closure_condition**: "Agent Boundary" → "The agent may:" lists
  running the Creator Registry match preflight runner as an authorized
  action, matching the doc's existing convention for every other runner.
- **next_authorized_action**: patched in place; CA adjudicates keep/revert.

### AR-03 (advisory, not-proven, out of scope to patch) — Two differently-named "preflight" registries in the same folder

- **Location**: `orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md`
  (out-of-scope, flag-only), lines 96-100 of its own
  `direction_change_propagation` receipt: "`creator_registry_index_v0.json`
  is the known-account preflight/dedupe list for Discovery and Capture."
- **Source authority**: the target files under review point the new
  operational-preflight requirement at a *different* file —
  `creator_profile_current_view_v0.json` (`run_creator_registry_match_preflight.py`'s
  `DEFAULT_REGISTRY`, and the usage note's stated registry file). The
  folder-level README describes `creator_registry_index_v0.json` as "the"
  preflight/dedupe list for Capture, using the same word ("preflight") for
  a sibling artifact this PR does not touch.
- **Failure scenario**: a cold agent who opens the folder README before the
  usage note could reasonably believe the README's `creator_registry_index_v0.json`
  dedupe check already satisfies "the Creator Registry match preflight," or
  could be uncertain which of the two same-named "preflight" concepts the
  runbook's mandatory step refers to.
- **Strongest defense**: the runbook and usage note (in scope, already
  precise) never mention `creator_registry_index_v0.json` and point a cold
  agent directly and only at the specific runner + specific usage note +
  specific registry file, so an agent who follows the runbook's own pointer
  chain (not the folder README) never encounters the ambiguity. This defense
  substantially holds for an agent that follows the stated chain, which is
  why this finding is advisory rather than patched.
- **Verdict**: PLAUSIBLE — not patched (design-level naming overlap between
  two pre-existing sibling artifacts, predates PR #654, and the fix would
  require editing the out-of-scope folder README or reconciling two
  registries' naming — outside this commission's three-file patch scope).
- **minimum_closure_condition**: the folder README and the usage note use
  distinguishable names for the two registries' respective "preflight"/dedupe
  roles (e.g., qualify one as "known-account index preflight" vs. the other
  as "match preflight receipt"), or an owner decision that the naming
  overlap is acceptable.
- **next_authorized_action**: owner decision or a separate, explicitly
  authorized pass over the folder README; no action available inside this
  commission's scope.

## Phase 2 — Friction Findings

### AR-04 (minor, hygiene) — New DCP receipt omitted `stale_language_search_result`

- **Location**: `orca-harness/docs/source_capture_agent_runbook.md`, the new
  "Direction Change Propagation - Creator Registry Match Preflight" block
  (pre-patch).
- **Observation**: every other `direction_change_propagation` receipt read
  across the five overlay files pairs `stale_language_search` with a
  `stale_language_search_result` recording what the search actually found.
  The new receipt declared the search command but never recorded a result,
  leaving an implied-but-undone check. `check_dcp_receipt.py`'s shape gate
  does not require this field (`REQUIRED_RECEIPT_KEYS` = `doctrine_changed`,
  `trigger`, `controlling_sources_updated`, `non_claims`), so this is a
  documented-convention gap, not a gate failure.
- **Verdict**: CONFIRMED — patched. I executed the declared search myself
  (`rg -n "Creator Registry match preflight|creator_registry_match_preflight|run_creator_registry_match_preflight|visual registry|projection scan|new social creator"` across the six named files)
  and recorded the actual result rather than leaving the field absent.
- **minimum_closure_condition**: the receipt records the search's actual
  result, consistent with sibling receipts in this repo.
- **next_authorized_action**: patched in place; CA adjudicates keep/revert.

## Non-Findings (checked, held up)

- `existing_match` / `new_candidate` / `ambiguous_match` / `invalid_candidate`
  semantics in both the runbook and usage note match
  `_build_candidate_result` and `_action_disposition` exactly, verified
  against the 12-test suite, not just doc prose.
- The usage note's command shape (`--candidates`, `--output`) matches the
  runner's actual `argparse` flags.
- Non-claims lists (fuzzy matching, cross-platform identity, silver refresh,
  registry mutation, live search, "not a Source Capture packet writer") are
  each individually true of the runner's actual behavior — the runner only
  writes a JSON receipt via `--output`, never a Source Capture packet
  (`manifest.json`/`receipt.md`/`raw/`).
- The repo-map's new runners-index entry ("fail-closed candidate account
  matching" / "exact-match candidate account receipts that block unsafe
  `new_capture`") is accurate: any error, ambiguity, or blocked action
  exits 2; only a fully clean `new_candidate` + `new_capture` query exits 0.
- The `orca-harness/README.md`, `source_capture_toolbox/README.md`, and
  `creator_registry/README.md` `intentionally_not_updated` claims in the new
  DCP receipt were checked against those files' actual content (not just
  the claim's own prose) and hold: `orca-harness/README.md` already points
  agents to this runbook; the other two READMEs carry no registry-preflight
  language that the new binding would contradict or duplicate.
- `check_dcp_receipt.py --strict` confirms the new receipt's `trigger`
  (`lifecycle_boundary`) and `related_triggers` (`output_authority`) are
  in the controlled seven-value vocabulary and all required keys are
  present — checked mechanically, not asserted.

## Patch Applied

Bounded to `orca-harness/docs/source_capture_agent_runbook.md` (the only file
this commission authorized patching against; the usage note and repo-map
required no patch). Unified diff:

```diff
diff --git a/orca-harness/docs/source_capture_agent_runbook.md b/orca-harness/docs/source_capture_agent_runbook.md
index 71f6d679..ee220abf 100644
--- a/orca-harness/docs/source_capture_agent_runbook.md
+++ b/orca-harness/docs/source_capture_agent_runbook.md
@@ -26,6 +26,9 @@ The agent may:
 - run Authenticated Browser Snapshot capture against one explicitly supplied URL
   using a previously bootstrapped storage-state label and an allowed session
   mode;
+- run the Creator Registry match preflight runner against candidate social
+  creator/account identities before starting new social creator/account
+  capture;
 - inspect `manifest.json`, `receipt.md`, and `raw/`;
 - report packet path, exit code, preserved files, warnings, and limitations.

@@ -134,8 +137,13 @@ creator capture, run the Creator Registry match preflight before capture and
 carry its receipt in the agent report or handoff. Use
 `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
 for candidate JSON shape, receipt outcomes, and the runner command. Do not start
-`new_capture` unless the receipt row is `new_candidate` and action status is
-allowed. `existing_match` routes to updating or working against the matched
+`new_capture` unless the candidate batch was preflighted with
+`intended_action: new_capture` and the resulting receipt row shows `decision:
+new_candidate` and `can_start_new_capture: true` (`action_status: allowed`). A
+row that only shows `decision: new_candidate` and `action_status: allowed` from
+a `classify` or `update_existing` query does not clear `new_capture`; check
+`can_start_new_capture` directly rather than reconstructing the condition.
+`existing_match` routes to updating or working against the matched
 registry identity; `ambiguous_match` and `invalid_candidate` stop the capture
 until resolved. A manual visual scan of the registry or projection is useful
 orientation, but it is not a substitute for the preflight receipt.
@@ -1076,6 +1084,13 @@ direction_change_propagation:
     - path: "orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md"
       reason: "Registry architecture and source split did not change; usage-note/runbook binding owns operator sequencing."
   stale_language_search: "rg -n \"Creator Registry match preflight|creator_registry_match_preflight|run_creator_registry_match_preflight|visual registry|projection scan|new social creator\" orca-harness/docs/source_capture_agent_runbook.md orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md orca-harness/README.md orca/product/spines/capture/core/source_capture_toolbox/README.md docs/workflows/orca_repo_map_v0.md"
+  stale_language_search_result: >
+    Executed 2026-07-04 after edits. Hits are only the new runbook/usage-note/
+    repo-map text itself (Required Inputs, Agent Boundary, agent-report
+    template, and the runners-index entry) plus this receipt's own quoted
+    search string. orca-harness/README.md, the source_capture_toolbox README,
+    and the creator_registry README carry no hits, consistent with the
+    intentionally_not_updated reasons above.
   non_claims:
     - "not validation"
     - "not readiness"
```

Per-change citation: hunk 1 closes AR-02; hunk 2 closes AR-01; hunk 3 closes
AR-04.

## Residual Risk

- AR-03 (two same-named "preflight" registries) remains open and
  unpatched — out of this commission's scope. Recorded above with a named
  `minimum_closure_condition` for a future owner-authorized pass.
- No test or code file was touched; the 12-test suite passing pre- and
  post-patch (docs-only edit) is not evidence about the AR-01/AR-02 fix
  quality — there is no automated check that a cold agent actually follows
  the corrected runbook wording. This residual is inherent to docs-only
  review and not a gap this patch could close.
- The patch's wording repeats the field name `can_start_new_capture` in the
  runbook. If that field is ever renamed in
  `registry_match_preflight.py`, this runbook sentence becomes stale; no
  mechanical checker binds runbook prose to that Python field name today.

## Validation (observed)

```text
git diff --check origin/main..HEAD
  EXIT: 0

python .agents/hooks/check_retrieval_header.py --changed --strict
  EXIT: 0

python .agents/hooks/header_index.py --strict --base origin/main
  header_index --strict: OK -- 1 changed durable .md file(s) all have headers and are map-reachable (base: origin/main)
  EXIT: 0

python .agents/hooks/check_dcp_receipt.py --strict --base origin/main
  check_dcp_receipt --strict: OK -- every real receipt in the changed .md files is shape-valid (base: origin/main)
  EXIT: 0

python .agents/hooks/check_handoff_pointers.py --strict --base origin/main
  check_handoff_pointers --strict: OK (0 findings in 3 changed file(s) vs origin/main)
  pinned/exempt handoff pointers: 0 (annotated debt, not failures)
  EXIT: 0

python .agents/hooks/check_review_routing.py --strict --base origin/main
  check_review_routing --strict: OK (base: origin/main)
  EXIT: 0

python .agents/hooks/check_map_links.py --strict
  check_map_links --strict: OK (0 findings)
  annotated nonresolving: 33 (debt, not failures)
  EXIT: 0

python .agents/hooks/check_full_gt_claims.py --changed --strict
  check_full_gt_claims: OK -- no unballasted full-GT claim language in scope
  EXIT: 0

python -m pytest -q orca-harness/tests/unit/test_creator_registry_match_preflight.py
  ............ [100%] (12 passed)
  EXIT: 0
```

All eight named gates plus the test suite pass. This validation run was
executed against the post-patch tree (all three findings applied); no
patch-around of a failing gate occurred, because none failed.

`check_review_output_provenance.py --strict` against this report path is run
after this file's final write, per the delegated-review-output finalization
gate; its result is reported in the closeout message to the commissioning
session rather than embedded here, since this file cannot observe its own
post-write hash before being written.

## Review-Use Boundary

These findings, the applied patch, and the validation evidence above are
decision input for the commissioning Chief Architect only: not approval, not
validation, not mandatory remediation, and not executor-ready patch
authority beyond this commission's own bounded scope. The CA adjudicates
AR-01/AR-02/AR-04 (patched — keep, modify, or revert) and AR-03 (unpatched —
accept the residual, or authorize a follow-up pass) before this branch is
treated as closed.

## Adjudication Next Step (for the commissioning Chief Architect)

Per `.agents/workflow-overlay/communication-style.md` → Review Adjudication
Next Step and `.agents/workflow-overlay/delegated-review-patch.md` →
Adjudication closeout: adjudicate the three findings, the diff, and the
residual above as claims (not premises); the self-closable material issue
here is applying your own modify/reject call to each of the three applied
hunks, which sits inside your own authority and this commission's scope —
close that in this same turn rather than deferring it. AR-03 needs an
owner decision or a separately authorized pass (it is not self-closable
inside this commission). Once adjudication is clean, batch admin/lifecycle
follow-ups (commit message, push, PR comment, merge) into one named land
step with no deep-thinking, and separately deep-think the small number of
material next moves that need judgment (e.g., whether AR-03 warrants an
immediate follow-up commission or can ride as accepted residual).

DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated artifact review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission or review target: PR #654, three named files
  (source_capture_agent_runbook.md, creator_registry_match_preflight_usage_v0.md,
  orca_repo_map_v0.md), on branch `codex/creator-registry-operational-preflight`
  at commit `2e308ab2014313acd6a7432a75654c8dd7db7b93`.
- reviewed artifact and bounded patch scope: all three read; patch authority
  used only against `orca-harness/docs/source_capture_agent_runbook.md`.
- findings and source evidence: AR-01 through AR-04 above, each with
  file/line anchors and source-code/test citations.
- proposed artifact patch: applied directly (see unified diff above); no
  patch proposed for the usage note or repo map (none needed) and none
  applied to the out-of-scope creator_registry README (AR-03).
- citations: `registry_match_preflight.py` (`can_start_new_capture`,
  `_action_disposition`), `run_creator_registry_match_preflight.py` (CLI
  flags, exit codes), `test_creator_registry_match_preflight.py` (12 tests),
  the three README files checked for the DCP receipt's own claims.
- reviewer verdict: `accept_with_patch`.
- residual risk: AR-03 (unpatched, out of scope) and the two working-tree
  residuals under Residual Risk above.
- blockers, off-scope flags, not-proven boundaries: none blocking; AR-03 is
  explicitly flagged off-scope and not patched; no `NEEDS_ARCHITECTURE_PASS`
  — this was a bounded wording/routing defect, not a design-level problem.
