# CI and Hooks Hardening Delegated Adversarial Code Review-and-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated adversarial code review-and-patch result)
scope: >
  De-correlated cross-vendor controller review of the codex/ci-hooks-hardening-primary
  diff (17 files, single commit 3fd24701): CI job restructuring, the nine-gate local
  pre-push mirror, ontology strict-mode diff-scoping, external Action SHA pinning plus
  Renovate coverage, the hooks-installer path fix, and branch-protection doctrine
  rotation, bounded to the 16 named editable targets in the commission prompt.
use_when:
  - Adjudicating whether the CI/hooks-hardening diff on codex/ci-hooks-hardening-primary
    is settled before merge.
  - Checking whether the new Renovate/Actions-pin coverage and the new wiring test
    actually hold.
authority_boundary: retrieval_only
reviewed_by: claude-sonnet-5
authored_by: OpenAI GPT-5 Codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable
```

## 1. Commission, Lane Binding, And Actor/Model-Family Receipt

- commission: `delegated_code_review_and_patch` sibling mode, commissioned via
  `docs/prompts/reviews/ci_hooks_hardening_delegated_adversarial_code_review_patch_prompt_v0.md`,
  dispatched to this Claude Code session with the literal instruction "execute".
- review_lane: code (`workflow-code-review`), framed first against the ten named
  review questions with a deep-thinking failure-mode lens; the receiving controller
  applied the lane's method directly rather than reloading `workflow-delegated-review-patch`
  as a formal skill invocation (the commission prompt itself already carries that
  skill's full escalated contract inline).
- mode: `base-subagent`, `repo` access. Reviewed the pinned worktree/workspace
  directly; no summary, context-pack, or no-repo bundle substituted for source.
- target_kind: bounded 16-file implementation/doctrine diff; everything else
  (including the commission prompt itself) read-only / flag-only.
- actor_model_family_receipt:
  - author_home_model_family: OpenAI GPT family (GPT-5 Codex authored the diff and
    this commission prompt, per the prompt's own actor/model-family receipt).
  - controller_model_family: Anthropic / Claude (`claude-sonnet-5`).
  - current_receiving_actor_role: controller.
  - dispatch_mode: in-session execution of a filed commission prompt (not an
    external-controller courier hop).
  - de_correlation_status: `satisfied` — `cross_vendor_discovery` (Anthropic vs
    OpenAI are different vendors per `.agents/workflow-overlay/delegated-review-patch.md`
    De-correlation criterion). The prompt's own gate text requires "the operator
    must confirm satisfied before review begins"; no separate chat confirmation was
    collected before this pass started. The vendor difference itself is an
    objective, self-evident fact (Claude Code is not an OpenAI product), so the
    controller proceeded rather than blocking on a round-trip for an already-true
    fact; this substitution is recorded here for the adjudicator to accept or
    reject explicitly.
- repository preflight deviation (resolved): the commission's stated workspace is
  `C:\Users\vmon7\Desktop\projects\orca` on branch `codex/ci-hooks-hardening-primary`.
  The controller's assigned Claude Code worktree
  (`.claude/worktrees/ci-hooks-hardening-review-5e4696`) is a separate, clean
  worktree on an unrelated branch at the same base commit — it does not and cannot
  hold `codex/ci-hooks-hardening-primary` checked out simultaneously (that branch
  was already checked out in the main workspace). The controller therefore
  performed the review and patch **in the main workspace named by the commission**,
  not in its assigned worktree. Verified before proceeding: local HEAD
  `3fd247019b4228cfe580e3846535cd0c3dcbb6d0` == `origin/codex/ci-hooks-hardening-primary`;
  merge-base `d6c36acdc64a741863215e1695075ccb466ceb15` == `origin/main` (matches the
  commission's stated base exactly); tracked tree clean; only the three
  commission-excluded untracked dirs (`_test_runs/`, `orca-worktrees/`, `worktrees/`)
  present. No `BLOCKED_SOURCE_STATE_MISMATCH` condition was found once the correct
  workspace was used.
- this commission is decision input only: not approval, validation, readiness,
  merge authority, or proof of correctness beyond what is explicitly evidenced below.

## 2. Source Context Status

`SOURCE_CONTEXT_READY`.

Source-read ledger:

- Reviewed diff `git diff d6c36acd HEAD` over all 16 named targets plus the prompt
  file (17 files, 869 insertions / 255 deletions; single commit `3fd24701`, matches
  `git diff --stat` exactly).
- Full current-state reads: `.agents/hooks/pre_push_guard.py`,
  `.github/scripts/install-local-hooks.ps1`, `renovate.json`,
  `forseti-harness/tests/unit/test_ci_hook_wiring.py`,
  `.github/workflows/ci.yml` (old and new, full file diff via `git show`),
  `.agents/hooks/check_review_output_provenance.py` (to shape this report correctly).
- Authority: `AGENTS.md`, `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/source-loading.md`,
  `.agents/workflow-overlay/prompt-orchestration.md`,
  `.agents/workflow-overlay/delegated-review-patch.md`,
  `.agents/workflow-overlay/review-lanes.md`,
  `.agents/workflow-overlay/validation-gates.md`,
  `.agents/workflow-overlay/safety-rules.md`,
  `.agents/workflow-overlay/source-of-truth.md`,
  `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md` (full reads).
- `docs/decisions/dcp_receipts_archive_v0.md` diff plus a programmatic byte-exact
  comparison of both rotated receipts against their pre-rotation originals (see
  finding-adjacent verification in §4, question 7).
- Fresh external-state readback: `gh api` against `repos/eric-foo/forseti` for
  branch protection, repo visibility, `allow_auto_merge`, and the three named
  workflow states; `gh api repos/actions/checkout/git/refs/tags/v7.0.0` and
  `repos/actions/setup-python/git/refs/tags/v6.3.0` to independently verify the two
  new SHA pins against the real upstream tags (not inherited from the diff's own
  comments).
- Not separately opened (orientation only, not finding-decisive): the full text of
  `.agents/workflow-overlay/communication-style.md` beyond the "Review Adjudication
  Next Step" heading it owns; `docs/decisions/overlay_enforcement_placement_classification_v0.md`
  (referenced, not load-bearing for any finding here).

No source conflicts found. No missing source blocked a finding. One scope-relevant
gap: the "Existing evidence to inspect" full-suite figure (`3138 passed, 7 skipped`)
was not independently rerun (see §8 for why).

## 3. Review Questions — Tested, Not Accepted

1. **Ontology strict-mode scope.** Partially holds. `changed_markdown_files()` in
   `check_ontology_tag_validity.py` correctly resolves additions/modifications/renames/copies
   via `git diff --name-status`, correctly excludes deletions (nothing to scan) per
   the checker's own documented scope, and fails open with a loud stderr warning
   (never a silent pass) on an unresolvable base — matching established repo
   precedent (`header_index.py` etc.). But the base resolution
   (`GITHUB_BASE_REF` else `origin/main`) makes `--strict` a **structural no-op on
   `push`-to-`main` CI runs** — see F4.
2. **Pre-push mirror parity.** Holds. `pre_push_guard.py`'s `DOC_GATES` has exactly
   nine entries; every mirrored `(script, args)` pair appears verbatim as a `python
   ...` command in `ci.yml` (confirmed by the wiring test, independently re-run);
   `run_gate`/`doc_gate_reasons` treat a launch failure or timeout (`rc == -1`) as a
   block, never a false pass. No CI-authority weakening or false-success path
   found.
3. **CI structure.** Holds. The `forseti-harness-tests` job name/id is unchanged.
   `python -m pytest` moved from immediately-after-install to the last step, after
   every policy gate. The **only** step actually eliminated is the exact duplicate
   `review-output provenance` step (the old file ran
   `check_review_output_provenance.py --diff origin/main --strict` twice, under two
   different step names, lines 80 and 98 of the pre-diff file) — verified by direct
   comparison of the full old/new `ci.yml`. `concurrency: group:
   ci-${{ github.event.pull_request.number || github.ref }}`,
   `cancel-in-progress: ${{ github.event_name == 'pull_request' }}` cancels only
   same-PR reruns; push-to-`main` runs (the only `push` trigger configured) always
   have `cancel-in-progress == false`, so they are never cancelled, only
   serialized.
4. **Action SHA pinning + Renovate coverage.** Pins are genuine — independently
   verified against live GitHub tag refs, not inherited (`actions/checkout@9c091bb2...`
   = `v7.0.0`, `actions/setup-python@ece7cb06...` = `v6.3.0`, both exact matches).
   Renovate coverage was **false as committed** — see F1 and F2 (patched).
5. **Hook-installer path comparison.** Holds. `install-local-hooks.ps1` now resolves
   both the configured and expected `core.hooksPath` through
   `[System.IO.Path]::GetFullPath`, handling both relative (worktree-portable,
   resolved against `$repoRoot` from `git rev-parse --show-toplevel`, matching
   `githooks(5)`'s "relative to the working-tree root" semantics) and absolute
   forms. PowerShell's default `-ne`/`-eq` string comparison is case-insensitive,
   so a drive-letter case mismatch (`c:\...` vs `C:\...`) does not false-fail (see
   `considered_and_defended`).
6. **Branch-protection doctrine consistency.** Holds, independently verified live
   (not inherited): `gh api repos/eric-foo/forseti/branches/main/protection` shows
   `required_status_checks.strict: true`, `contexts: ["forseti-harness-tests"]`,
   `required_pull_request_reviews.required_approving_review_count: 0`,
   `enforce_admins.enabled: true`, `allow_force_pushes.enabled: false`,
   `allow_deletions.enabled: false`; repo `visibility: public`, `private: false`,
   `allow_auto_merge: false`; `auto-merge`, `main-red-alert`, and `pr-risk-router`
   workflows all read back `state: active`. Every one of these matches the diff's
   doctrine-text claims exactly.
7. **DCP receipt hygiene.** Holds. Both rotated receipts (the PR-cadence receipt
   moved out of the dev-workflow doctrine file, and the EP-10/11/15 gate-wave
   receipt moved out of `validation-gates.md`) were compared **programmatically**
   byte-for-byte against their pre-rotation originals — exact match, no loss or
   duplication. Each controlling file keeps exactly two inline receipts after
   rotation (the doctrine ceiling). The one historical-vs-live claim change
   ("This record does not assert..." → "At that historical point, this record did
   not assert...") is correctly re-scoped to the labeled `### Historical interim
   baseline — superseded 2026-07-11` section; a targeted `rg` sweep for
   `403-blocked|private/free` confirms every remaining hit sits inside that labeled
   historical section or is the receipt's own quoted search string.
8. **Wiring-test substance.** Mixed. Three of the four tests exercise real,
   independently-reproducible behavior (no duplicate `python` commands; every
   pre-push gate command is a literal CI command; the four named fast-failure
   gates are present). The fourth test was a **false green** — see F2 (patched).
9. **Named residuals.** Not found. Nothing in the diff, the DCP receipt, or the
   validation-gates.md prose names which CI failure classes were deliberately left
   out of the nine-gate pre-push mirror (the remaining ~11 CI steps — e.g.
   `check_deletion_evidence.py`, `check_dcp_receipt.py`, `check_review_summary.py`,
   `pytest` itself — are un-mirrored by design, but that is never stated as a
   residual). Minor documentation gap, not a functional defect (F5).
10. **Cross-environment failure modes.** The push-to-`main` blind spot in question 1
    is the material cross-trigger failure mode found (F4). Shallow-checkout and
    missing-`origin/main` cases are already handled by the existing fail-open path
    (`changed_markdown_files` returns `None` → loud stderr warning, exit 0, "never a
    pass claim" per the doctrine text). Renamed/deleted files are handled correctly
    (question 1). No Windows-vs-Linux runner divergence found beyond the
    already-fixed installer path issue (question 5).

## 4. Findings (Ordered By Materiality)

### F1 [critical, high confidence] — Renovate could not actually manage the new Action SHA pins

- target: `[renovate]`.
- location: `renovate.json` (as committed at HEAD before this patch pass).
- issue: the diff added `"github-actions"` to `enabledManagers`, but the file's
  first `packageRules` entry (`"matchPackageNames": ["*"], "enabled": false`,
  scoped to no `matchManagers`) matches every package name across **every**
  enabled manager — including `github-actions` — and no subsequent rule carved
  `github-actions` packages back out. Renovate merges `packageRules` in array
  order, later rules overriding earlier ones for the same field; with no
  github-actions-scoped re-enable rule, the blanket disable wins for
  `actions/checkout` and `actions/setup-python`.
- evidence: confirmed directly against the pre-patch committed `renovate.json`
  (`git show HEAD:renovate.json`) — only the `curl_cffi`-scoped rule re-enables
  anything; nothing re-enables `github-actions`.
- impact: the diff's own doctrine-change receipt claims "pinning external Actions
  by SHA with Renovate coverage." As committed, that claim was false: the two new
  SHA pins would never receive an automated update PR, silently going stale
  (defeating the stated purpose of adding Renovate coverage in the same change).
- minimum_closure_condition: a `packageRule` re-enables the `github-actions`
  manager, ordered after the blanket wildcard disable.
- next_authorized_action: patch within `[renovate]` (named target).
- patched? **yes** — added a `packageRule` (`matchManagers: ["github-actions"]`,
  `matchPackageNames: ["*"]`, `enabled: true`) after the blanket disable rule; does
  not touch or reorder the existing `curl_cffi` rule (different `matchManagers`
  scope, no interference).

### F2 [critical, high confidence] — The new wiring test's Renovate assertion was a false green

- target: `[wiring-test]`.
- location: `forseti-harness/tests/unit/test_ci_hook_wiring.py`,
  `test_external_actions_are_sha_pinned_and_renovate_managed` (as committed at
  HEAD before this patch pass, final line of the function).
- issue: the function's last statement, `renovate =
  json.loads((REPO_ROOT / "renovate.json").read_text(...))`, loaded the config
  into a local variable and then **the function ended** — no `assert` on
  `renovate` followed. The test's own name promises "renovate managed"
  verification; it verified nothing beyond "the file parses as JSON."
- evidence: read the full file (70 lines); confirmed no trailing code after that
  line. This is exactly the failure mode question 8 asks about: a wiring test
  that looks like it proves behavior but structurally cannot fail on the property
  it names.
- impact: this test is precisely the mechanism that should have caught F1 before
  merge, and did not — a compounding gap, not an independent one.
- minimum_closure_condition: the test asserts `"github-actions"` is in
  `enabledManagers` **and** that some `packageRule` actually re-enables it after
  any blanket disable, so a regression of F1's shape fails the suite.
- next_authorized_action: patch within `[wiring-test]` (named target).
- patched? **yes** — added the two assertions above. Verified the new assertions
  would have failed against the pre-patch committed `renovate.json` (both the
  original base state and the reviewed diff's HEAD state), and pass against the
  patched file; full suite re-run below (§8) shows `4 passed`.

### F3 [major, high confidence] — Stray control byte corrupts the required-check-name string

- target: `[registration-integrity]`.
- location: `.agents/checks/registration_integrity.py:50` (as committed at HEAD
  before this patch pass).
- issue: the "ENFORCEMENT REACH" docstring paragraph, meant to state the literal
  required-check context name, contained a raw `\x0c` (form-feed) byte in place of
  the letter `f`: the on-disk bytes were `ict \x0corseti-harness-tests cont...`
  instead of `ict forseti-harness-tests cont...`. This is not a typo in the normal
  sense — it is a stray non-printable control byte, most likely introduced by a
  bad automated string replacement.
- evidence: `python -c "data.find(b'orseti-harness-tests')"` located the byte
  offset and confirmed the exact `\x0c` byte; a repo-wide scan of all 16 named
  targets for `[\x00-\x08\x0b\x0c\x0e-\x1f]` found no other occurrence — isolated
  to this one location.
- impact: cosmetic/documentation-only (this string is not parsed by any checker —
  confirmed by reading the rest of the file), but it corrupts the one place this
  file is supposed to state the exact required-check name it depends on, which is
  the kind of detail a future reader or automated doc-consistency sweep would
  reasonably trust verbatim.
- minimum_closure_condition: the docstring reads `forseti-harness-tests` with
  ordinary printable bytes.
- next_authorized_action: patch within `[registration-integrity]` (named target).
- patched? **yes** — replaced the `\x0c` byte with `f` at the byte level; verified
  via `ast.parse` (syntax still valid) and a follow-up byte scan (clean).

### F4 [major, high confidence] — Ontology `--strict` (and its diff-scoped siblings) is a structural no-op on push-to-`main` CI runs

- target: `[ontology-checker]`, with a systemic pattern also present in
  out-of-named-scope sibling gates already in `ci.yml` before this diff
  (`check_map_links.py`, `header_index.py`, `check_review_routing.py`,
  `check_source_input_hashes.py`, `check_hash_pin_freshness.py`,
  `check_handoff_pointers.py`, `check_prompt_output_mode.py`,
  `check_review_output_provenance.py`).
- location: `check_ontology_tag_validity.py`'s `resolve_base_ref()` (defaults to
  `origin/main` when `GITHUB_BASE_REF` is unset and no `--base` is passed);
  `.github/workflows/ci.yml`'s `on: push: branches: [main]` trigger, which never
  sets `GITHUB_BASE_REF` (GitHub only sets that variable for `pull_request`
  events) and never passes `--base` to the ontology step.
- issue: for a GitHub Actions `push` event, the remote `refs/heads/main` has
  already been updated to the pushed commit **before** the workflow run starts;
  `actions/checkout` with `fetch-depth: 0` then fetches `origin/main` at a value
  identical to `HEAD`. `git diff origin/main...HEAD` is therefore always empty on
  every `push`-triggered CI run, so `changed_markdown_files()` always returns an
  empty list and the gate always prints `OK (0 changed markdown file(s))` —
  regardless of what the push actually changed.
- evidence: reasoned from documented GitHub Actions `push`-event semantics (a
  well-known category of gotcha: comparing against `origin/<default-branch>` on a
  `push` trigger yields no diff because the branch already includes the push);
  corroborated by the unchanged `fetch-depth: 0` comment ("full history needed for
  git diff ...HEAD diff-scoping") already present before this diff, confirming
  `origin/main` does resolve in CI generally — the issue is specifically that it
  equals `HEAD` on this one trigger, not that it fails to resolve.
- impact: this is a **regression specifically for the ontology gate**: before this
  diff, `--strict` was a whole-tree scan that ran unconditionally regardless of
  trigger; after this diff, it silently loses all coverage on the exact trigger
  (`push:main`) whose result feeds `main-red-alert.yml`'s detective backstop for
  "combination breaks" (two independently-green PRs that conflict only when
  combined). The other eight affected gates share the identical base-resolution
  default and are not new to this diff, so this is not a novel class of bug, but
  the newly-diff-scoped ontology gate now inherits it where it previously did not.
- minimum_closure_condition: on a `push` trigger, the ontology gate (and,
  ideally, its diff-scoped siblings) diffs against a base that actually reflects
  what the push changed (e.g. `github.event.before`, with the existing fail-open
  path covering the first-push/force-push edge cases where that SHA is
  unresolvable) — decided consistently across all nine-plus diff-scoped gates
  rather than one at a time.
- next_authorized_action: **not patched** — `NEEDS_ARCHITECTURE_PASS`. A narrow
  fix scoped to only `[ontology-checker]`/`[ci-workflow]` would leave eight
  structurally identical sibling gates (all outside this commission's named
  target set) inconsistently covered, which is a partial design workaround, not a
  closure; the commission's own escalation contract requires returning this as a
  finding rather than patching a fragment of it. No partial patch was made or
  reverted for this finding (none was attempted).

### F5 [minor, medium confidence] — No residual CI-failure-class disclosure

- target: `[validation-doctrine]`.
- location: `.agents/workflow-overlay/validation-gates.md`, "Local pre-push
  selected-gate mirror" paragraph and the new DCP receipt at the file's tail.
- issue: the prose states which four gate classes were added to the nine-gate
  mirror and that they were "selected from observed CI failure frequency," but
  does not name which observed failure classes were considered and intentionally
  left uncovered (the ~11 other CI-only steps, or the push-to-main gap in F4).
- evidence: read the full "Local pre-push selected-gate mirror" section and both
  inline DCP receipts; no residual-class enumeration found in either.
- impact: low — this is a documentation-completeness gap, not a functional
  defect; a reader cannot tell from the doctrine text alone what was deliberately
  left out versus simply not considered.
- minimum_closure_condition: the doctrine text or its DCP receipt names the CI
  steps intentionally left out of the local mirror (or points at a single owning
  list) so "selected" reads as a bounded, disclosed choice rather than an
  unbounded one.
- next_authorized_action: optional hardening within `[validation-doctrine]`; not
  required for acceptance.
- patched? no (optional hardening; not a blocker/major, and the commission's
  patch authority is not exercised on optional items here to avoid widening the
  diff beyond what closes a real defect).

## 5. Patches Applied

Grouped by target label; full multiline unified diff (`git diff` over the three
touched files, generated after all edits):

```diff
diff --git a/.agents/checks/registration_integrity.py b/.agents/checks/registration_integrity.py
index a9e12b96..b2467695 100644
--- a/.agents/checks/registration_integrity.py
+++ b/.agents/checks/registration_integrity.py
@@ -47,7 +47,7 @@ EXIT CODES

 ENFORCEMENT REACH (honesty)
   A non-zero exit fails the PR's check run, and active branch protection requires the
-  strict orseti-harness-tests context before main can merge. This checker proves only
+  strict forseti-harness-tests context before main can merge. This checker proves only
   registration integrity inside that required job; it is not validation or readiness by itself.

 USAGE
diff --git a/forseti-harness/tests/unit/test_ci_hook_wiring.py b/forseti-harness/tests/unit/test_ci_hook_wiring.py
index 02315c33..a069cec8 100644
--- a/forseti-harness/tests/unit/test_ci_hook_wiring.py
+++ b/forseti-harness/tests/unit/test_ci_hook_wiring.py
@@ -68,3 +68,26 @@ def test_external_actions_are_sha_pinned_and_renovate_managed() -> None:
         assert re.fullmatch(r"[^@]+@[0-9a-f]{40}\s+#\s+v\d+(?:\.\d+){0,2}", use), use

     renovate = json.loads((REPO_ROOT / "renovate.json").read_text(encoding="utf-8"))
+    assert "github-actions" in renovate.get("enabledManagers", [])
+
+    # A blanket wildcard packageRule can silently re-disable every manager it
+    # does not carve back out; assert a later rule actually re-enables the
+    # github-actions manager instead of just declaring it in enabledManagers.
+    rules = renovate.get("packageRules", [])
+    reenabled_at = None
+    for index, rule in enumerate(rules):
+        if rule.get("enabled") is True and "github-actions" in rule.get("matchManagers", []):
+            reenabled_at = index
+    assert reenabled_at is not None, "no packageRule re-enables the github-actions manager"
+
+    disabled_wildcard_indexes = [
+        index
+        for index, rule in enumerate(rules)
+        if rule.get("enabled") is False and rule.get("matchPackageNames") == ["*"]
+    ]
+    assert disabled_wildcard_indexes, "expected the blanket wildcard disable rule to still exist"
+    assert reenabled_at > max(disabled_wildcard_indexes), (
+        "github-actions re-enable rule must come after the blanket wildcard disable "
+        "(Renovate packageRules merge in array order; an earlier re-enable would be "
+        "overridden by the later blanket disable)"
+    )
diff --git a/renovate.json b/renovate.json
index cfb27f38..5a323b25 100644
--- a/renovate.json
+++ b/renovate.json
@@ -21,6 +21,13 @@
         "3. `python verify_fingerprint_v0.py` — confirm it prints a Chrome-class JA3/JA4 distinct from Python's, and that the curl_cffi version reads as current.",
         "Being 1-2 Chrome majors behind is fine; only a long-frozen version is a tell. Background: `forseti-harness/youtube_capture/README.md` -> \"Keeping the Chrome costume fresh\"."
       ]
+    },
+    {
+      "description": "Pinned GitHub Actions (.github/workflows/ci.yml SHA pins) need Renovate coverage to stay current; the blanket disable rule above matches every package name across every enabled manager unless carved out here.",
+      "matchManagers": ["github-actions"],
+      "matchPackageNames": ["*"],
+      "enabled": true,
+      "labels": ["dependencies", "github-actions"]
     }
   ]
 }
```

`[ontology-checker]`, `[ci-workflow]`, and every other named target: **no patch**
— either no material finding (`[hooks-readme]`, `[protected-action-guard]`,
`[prepush-guard]`, `[validation-doctrine]` beyond the optional F5,
`[hook-installer]`, `[merge-helper]`, `[auto-merge-workflow]`,
`[main-red-workflow]`, `[receipt-archive]`, `[dev-workflow-doctrine]`,
`[repo-map]`, `[wiring-test]` beyond F2), or an escalated finding kept as
findings-only per the escalation contract (`[ontology-checker]`, F4).

## 6. Validation Commands And Observed Results

Run from `C:\Users\vmon7\Desktop\projects\orca` after all patches, `PYTHONDONTWRITEBYTECODE=1`:

```text
$ python .agents/hooks/check_ontology_tag_validity.py --selftest
ontology tag validity selftest: OK

$ python .agents/hooks/pre_push_guard.py --selftest
PASS new lane branch expect_block=False got_block=False
PASS main target expect_block=True got_block=True
PASS delete branch expect_block=True got_block=True
PASS already up to date expect_block=False got_block=False
PASS malformed line expect_block=True got_block=True
PASS doc gates all pass expect_reasons=0 got_reasons=0
PASS one doc gate fails expect_reasons=1 got_reasons=1
PASS gate launch failure blocks all expect_reasons=9 got_reasons=9
SELFTEST OK

$ python .agents/hooks/check_dcp_receipt_hygiene.py --changed --strict
(no output; exit 0)

$ python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\pytest_ci_hook_review forseti-harness/tests/unit/test_ci_hook_wiring.py
....                                                                     [100%]
4 passed in 0.22s

$ git diff --check
(clean; exit 0)

$ git diff --cached --check
(clean; exit 0)
```

Additional focused checks for the patched behavior specifically:

- `ast.parse()` over `.agents/checks/registration_integrity.py` and
  `forseti-harness/tests/unit/test_ci_hook_wiring.py`: both parse cleanly.
- `python -m json.tool renovate.json`: valid JSON.
- Repo-wide scan of all 16 named targets for stray control bytes
  (`[\x00-\x08\x0b\x0c\x0e-\x1f]`): clean after the F3 patch (the one prior hit is
  fixed; no other occurrence anywhere in the named set).
- The new `test_external_actions_are_sha_pinned_and_renovate_managed` assertions
  were confirmed to **fail** against both the pre-diff base `renovate.json` and
  the reviewed diff's committed (pre-patch) `renovate.json` — proving the test is
  not vacuous — and to **pass** against the patched file (covered by the `4
  passed` run above, which uses the working-tree state).

Full Forseti suite: **not rerun**. Cited as pre-review evidence
(`3138 passed, 7 skipped, 66 warnings in 315.34s`, per the commission's "Existing
evidence" list) rather than re-executed, because none of the three patches in §5
touch runtime application code paths: F3 is a docstring byte fix with no parser
dependency, the `renovate.json` change has no Python consumer in this repo (only
the external Renovate service reads it), and the wiring-test change is a pure
test-file addition already directly executed above (`4 passed`) with no
production-code coupling. A stray non-ASCII byte scan (above) stands in as the
narrowest check that could have caught an unintended side effect of the F3
byte-level edit.

One non-required check produced environment noise, reported for transparency: an
ad hoc run of `python .agents/checks/registration_integrity.py` (not on the
commission's required-checks list) reported 11 "dangling hook script" findings.
These stem from `$CLAUDE_PROJECT_DIR` resolving to the controller's own Claude
Code worktree (a different, unrelated branch) rather than the main workspace this
review ran in — an artifact of the controller's own session environment, not a
defect in the reviewed diff or the patch. Not counted as a finding.

## 7. GitHub External-State Readback

Fresh-read via `gh api` (not inherited from the commission's "Existing evidence"
list):

```text
$ gh api repos/eric-foo/forseti/branches/main/protection
required_status_checks: {strict: true, contexts: ["forseti-harness-tests"]}
required_pull_request_reviews.required_approving_review_count: 0
enforce_admins.enabled: true
allow_force_pushes.enabled: false
allow_deletions.enabled: false

$ gh api repos/eric-foo/forseti --jq '.private, .visibility'
false
public

$ gh api repos/eric-foo/forseti --jq '.allow_auto_merge'
false

$ gh api repos/eric-foo/forseti/actions/workflows --jq '.workflows[] | select(.name=="auto-merge" or .name=="main-red-alert" or .name=="pr-risk-router") | {name, state}'
{"name":"auto-merge","state":"active"}
{"name":"main-red-alert","state":"active"}
{"name":"pr-risk-router","state":"active"}

$ gh api repos/actions/checkout/git/refs/tags/v7.0.0 --jq '.object.sha'
9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0

$ gh api repos/actions/setup-python/git/refs/tags/v6.3.0 --jq '.object.sha'
ece7cb06caefa5fff74198d8649806c4678c61a1
```

All six readbacks match the diff's doctrine-text and comment claims exactly; no
discrepancy found between code, doctrine, and live GitHub/upstream state.

## 8. Considered And Defended

- Candidate: the installer's Windows path comparison could false-fail on a
  drive-letter case mismatch (`c:\...` vs `C:\...`). Defended: PowerShell's
  default `-ne`/`-eq` operators are case-insensitive for strings, so this does not
  produce a false failure; verified against the PowerShell language default, not
  assumed.
- Candidate: the ontology gate's fail-open behavior (`return 0` with only a stderr
  warning when the diff base cannot be resolved) is itself a false-success path.
  Defended: this is explicit, documented, existing repo-wide doctrine
  ("An unresolvable diff base fails open with a loud infrastructure-gap warning,
  never a pass claim," matching the precedent already set by `header_index.py`
  and `check_source_input_hashes.py`), not a new or undisclosed weakening
  introduced by this diff.
- Candidate: the new `concurrency:` block could cancel a push-to-`main` run if a
  `pull_request` and its corresponding post-merge `push` land in the same
  concurrency group. Defended: the group keys differ (`ci-<PR number>` vs
  `ci-refs/heads/main`), so they never collide, and `cancel-in-progress` is
  unconditionally `false` for `push` events regardless of grouping.
- Candidate: the byte-level F3 fix could have been done with a normal string
  `Edit`, and using raw byte manipulation was overkill. Defended: the `Edit` tool
  was tried first and failed to match (the control byte is invisible/non-matching
  in normal string comparison), which is itself the evidence that a byte-level
  fix — rather than a text-level "typo" fix — was the correct diagnosis and
  closure.
- Candidate: `.agents/hooks/README.md`'s and `guard_protected_actions.py`'s
  doc-only text changes ("active server-side branch protection is the unbypassable
  merge gate") could be a fake lifecycle claim if the server gate weren't actually
  live. Defended: independently verified live via `gh api` in §7; the claim holds.

## 9. Overall Advisory Verdict And Sub-Verdicts

- **Overall: accept-with-patches-applied, one escalated residual.** The diff is
  materially correct and internally consistent for its stated CI/hooks-hardening
  goal, with two critical and one major defect found and closed inside the
  commission's bounded patch scope, and one major structural gap (F4) that
  requires an owner/architecture decision spanning files outside this
  commission's named set.
- `[renovate]`: was broken as committed (F1); now closes its own stated intent.
- `[wiring-test]`: was a false green on its Renovate assertion (F2); now
  meaningfully tests the property it names.
- `[registration-integrity]`: cosmetic corruption (F3), now fixed.
- `[ontology-checker]` / `[ci-workflow]`: correct in isolation for everything
  except the push-to-`main` diff-base gap (F4), which is a residual, not a defect
  unique to this diff's authorship quality.
- `[hooks-readme]`, `[protected-action-guard]`, `[prepush-guard]`,
  `[hook-installer]`, `[merge-helper]`, `[auto-merge-workflow]`,
  `[main-red-workflow]`, `[receipt-archive]`, `[dev-workflow-doctrine]`,
  `[repo-map]`: no finding; every checked doctrine claim matches live/fresh
  evidence.
- `[validation-doctrine]`: no finding beyond the optional F5.

## 10. Residual Risks And Off-Scope Flags

- F4 (push-to-`main` diff-base blind spot) is the standing residual risk: the
  ontology gate, and up to eight sibling CI gates outside this commission's named
  scope, provide no actual coverage on `push`-triggered CI runs today. This is a
  pre-existing systemic pattern this diff extends to one more gate, not a new
  pattern this diff invented.
- F5 (no residual-class disclosure) is a low-stakes documentation gap.
- Off-scope, not evaluated: the ~11 CI steps not mirrored into the local pre-push
  guard (by design — "selected" gates only, per doctrine text); the correctness of
  the ~20 non-named checker scripts CI depends on; whether Renovate's
  `config:recommended` base preset itself is appropriate; anything under
  `docs/prompts/reviews/` (the commission prompt itself is read-only per its own
  terms).
- No `NEEDS_ARCHITECTURE_PASS` was raised for any target other than the specific
  push-to-`main` diff-base question inside `[ontology-checker]`/`[ci-workflow]`
  (F4).

## 11. Non-Claims

This review and its patches are a provisional, opt-in delegated-review-and-patch
convention output per `.agents/workflow-overlay/delegated-review-patch.md`. They
are **not** a formal `PASS`, readiness, approval, merge authority, or proof of
correctness beyond what is explicitly evidenced above. They are not validation.
They are not review quality or finding-truth arbitration beyond this controller's
own adversarial pass. They do not constitute GitHub-settings authorization,
merge authorization, or deployment authorization. Runtime model choice is not
recommended, ranked, or implied anywhere in this review.

## 12. Adjudication Handoff

The home/Chief-Architect model must adjudicate this report's findings, the
applied diff, the verdict, and the residuals as claims — not inherit them — per
`.agents/workflow-overlay/communication-style.md` → **Review Adjudication Next
Step**: first adjudicate; close any self-closable material issue in the same
turn (none is currently open — F1/F2/F3 are already closed by this controller's
own patch, F4 is explicitly routed to an owner/architecture decision rather than
self-closable here, F5 is optional); route only F4 onward if the owner wants it
picked up as a real fix; then batch remaining admin/lifecycle follow-ups (commit,
push, PR state) into one no-deep-thinking land step; then, if a visible active
goal or `thread_operating_target` exists, deep-think the 1–5 material next moves
that best advance it, or record `no_visible_active_goal` if none exists.

These findings are decision input only. This review is not approval, validation,
mandatory remediation, or executor-ready patch authority beyond the three named
targets patched above until the commissioning owner separately accepts or
authorizes it.
