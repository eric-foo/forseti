# Forseti Live Root Migration PR826 - Delegated Adversarial Code Review-And-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Review-and-patch output report
scope: >
  De-correlated adversarial implementation/code review-and-patch findings,
  applied patch, and validation evidence for PR #826's live Forseti root
  migration (pinned commit range).
use_when:
  - CA adjudication of PR #826 before merge.
  - Checking whether the live-root migration's repo-map/README route
    integrity was independently reviewed and what was patched.
authority_boundary: retrieval_only
branch_or_commit: codex/forseti-live-root-migration-rebased target f53e6f2ef24df24bb88079453dd6b2383a508dd0; base 397b15705a68e22e1400c093d947a0f093d5eec9
stale_if:
  - PR #826 is rebased, force-pushed, or its target commit changes.
  - A later commit further edits docs/workflows/orca_repo_map_v0.md, docs/README.md, or docs/STRUCTURE.md beyond applying this report's unified diff.
```

```yaml
review_summary:
  recommendation: accept_with_friction
  source_context: SOURCE_CONTEXT_READY
  reviewed_by: claude-sonnet-5
  authored_by: OpenAI/Codex
  de_correlation_bar: cross_vendor_discovery
  same_vendor_rationale: not_applicable
  target_range: 397b15705a68e22e1400c093d947a0f093d5eec9..f53e6f2ef24df24bb88079453dd6b2383a508dd0
  report_path: docs/review-outputs/forseti_live_root_migration_pr826_delegated_adversarial_code_review_patch_v0.md
```

## Commission

De-correlated adversarial implementation/code review-and-patch pass on PR #826's
live Forseti root migration (commit `f53e6f2ef24df24bb88079453dd6b2383a508dd0`,
base `397b15705a68e22e1400c093d947a0f093d5eec9`), per
`docs/prompts/reviews/forseti_live_root_migration_pr826_delegated_adversarial_code_review_patch_prompt_v0.md`.
Author/home model family: OpenAI/Codex. Reviewing controller: Claude Sonnet 5
(Anthropic) — different vendor, so this pass satisfies the `cross_vendor_discovery`
de-correlation bar. Findings and the applied patch are decision input for CA
adjudication only; not approval, readiness, or merge authority.

## Method

Applied `workflow-deep-thinking` to frame the highest-risk failure modes before
listing findings (asymmetric partial rename: a large mechanical diff — 1418
files, 1154 renames — is exactly the shape where *some but not all* occurrences
of a token get updated inside a single touched file, leaving internally
inconsistent prose that no gate catches because it's a string, not a path).
Applied `workflow-code-review` against the ten Attack Questions in the prompt.
Read `AGENTS.md`, `.agents/workflow-overlay/README.md`,
`review-lanes.md`, `prompt-orchestration.md`, `delegated-review-patch.md`,
`source-loading.md`, `validation-gates.md`, `safety-rules.md`, and inspected the
pinned diff (`git diff --stat` / `--name-status` / targeted `--` diffs) in an
isolated detached worktree at the pinned target commit
(`C:/tmp/orca-pr826-review`), separate from the CA/home lane.

`docs/hygiene/migrations/moved_paths_index.md`, named in the prompt's Source
Context list, does not exist anywhere in the repository (verified via
`git ls-tree` across the whole tree at the target commit and a full-repo
`find`/glob for `moved_paths_index.md` — four distinct files exist under
`docs/migration/*/` and one under `forseti/product/spines/commission_signal_board/migrations/`,
none under `docs/hygiene/migrations/`). This is a source-context gap in the
review prompt itself, not a PR826 defect; noted here rather than silently
skipped, and out of this review's patch scope (prior prompts are excluded from
the patch boundary).

## Findings

### F1 (medium) — Legacy repo-map "Top-Level Structure" table still declared a removed root

- File/line: `docs/workflows/orca_repo_map_v0.md:410` (pre-patch)
- Evidence: the migration commit itself edited this exact row —
  `git diff 397b1570..f53e6f2e -- docs/workflows/orca_repo_map_v0.md` shows
  `| \`orca/\` | Declared top-level product-tree root. Product substance lives
  under \`orca/product/\`; runtime remains under \`orca-harness/\`. |` rewritten to
  `| \`orca/\` | Declared top-level product-tree root. Product substance lives
  under \`forseti/product/\`; runtime remains under \`forseti-harness/\`. |` — i.e.
  the author touched the row's *content* but left its *claim* (that `orca/` is a
  "Declared top-level product-tree root") standing, even though this same commit
  deletes the physical `orca/` tree and drops `orca` from
  `repo-structure.yaml`'s `known_top_level.dirs` (confirmed: `ls orca` ->
  `No such file or directory` at the target commit; `repo-structure.yaml`
  `known_top_level.dirs` lists only `forseti`, `forseti-harness`, `.agents`,
  `.claude`, `.codex`, `.github`, `.githooks`, `docs`, `worktrees`).
- Risk: this is exactly the "route integrity" failure mode the commission's
  Attack Question #5 asks about — a durable, retrieval-header'd navigation doc
  asserting a physical root exists ("Declared top-level ... root") one commit
  after that root was removed. A cold-lane agent trusting this table would
  believe `orca/` is still a live top-level entry.
- Minimum closure condition: the "Top-Level Structure" table enumerates only
  roots that are actually present (or is explicit that an entry is retired).
- Next authorized action: patch (applied, see below) or CA acceptance of the
  row as-is.
- Patched: yes.

### F2 (minor) — Repo-map freshness hook's message pointed at a heading the migration didn't rename

- File/line: `.agents/hooks/check_repo_map_freshness.py` (message string,
  touched by this commit) vs. `docs/workflows/orca_repo_map_v0.md:473` (heading,
  also touched by this commit for unrelated content but not this heading)
- Evidence: the migration commit changed
  `check_repo_map_freshness.py`'s `structural_trigger()` return message from
  `"...is not named in the repo map's Orca Harness section (stale_if #2)"` to
  `"...Forseti Harness section (stale_if #2)"`, but the actual section heading
  in `docs/workflows/orca_repo_map_v0.md` (which this same commit substantively
  edited — 120 lines changed — including the `forseti-harness/` row two lines
  above the heading) remained literally `## Orca Harness`. The row's own pointer
  text ("See the Orca Harness section") still matched the stale heading, so the
  only actual mismatch was between the Python message and the doc.
- Risk: low — this string does not gate anything (the freshness check's actual
  match logic is a substring/glob test against `HARNESS_UNIT_GLOBS`, not the
  heading text), so no false pass/fail results. It is a human-facing
  misdirection: a contributor chasing a `check_repo_map_freshness.py` failure
  message would search the map for a "Forseti Harness" section and initially
  not find one.
- Minimum closure condition: the hook's message and the map heading it
  describes agree.
- Next authorized action: patch (applied, see below) or CA acceptance.
- Patched: yes — renamed the heading to `## Forseti Harness` (matching the
  hook's already-updated message and the migration's overall direction) and
  updated the one cross-reference pointer text in the same file; verified no
  other file references `#orca-harness` or the literal string "Orca Harness"
  (`rg`/grep across `*.md` and `*.py`, zero remaining hits).

### F3 (minor) — `docs/README.md` and `docs/STRUCTURE.md` titles disagreed with their own migrated body text

- File/line: `docs/README.md:1`, `docs/STRUCTURE.md:1`
- Evidence: this commit edited the body of both files (e.g.
  `docs/README.md:3` "This folder holds ~~Orca~~ **Forseti**-owned durable
  artifacts"; `docs/STRUCTURE.md` multiple `orca/product/` -> `forseti/product/`
  body edits — confirmed via targeted diff), but left both H1 titles as
  `# Orca Docs` / `# Orca Docs Structure`. The root `README.md` (also touched by
  this commit) already carries the `# Forseti` title, so these two front-door
  docs are now the odd ones out relative to the sibling file this same commit
  aligned.
- Risk: low/cosmetic, but it is the same "touched the body, missed the
  heading" pattern as F1/F2, on the two canonical docs-tree front doors named
  in `repo-structure.yaml`'s `entry_points` (`docs_readme`, `docs_guide`).
- Minimum closure condition: title and body agree on project identity in both
  files.
- Next authorized action: patch (applied) or CA acceptance.
- Patched: yes. Checked for anchor/link dependents first (`grep` for
  `orca-docs`, `#orca-docs`, `Orca Docs` across `*.md`/`*.py`): no markdown
  link or anchor reference to either heading exists elsewhere in the repo, so
  the rename carries no follow-on breakage.

## Patch Summary

Three files, five lines changed, all within the pinned migration range's
changed-file set (or its direct output-of-this-commit surface):

- `docs/workflows/orca_repo_map_v0.md`: removed the stale `orca/` top-level-root
  table row (F1); renamed `## Orca Harness` -> `## Forseti Harness` and its one
  cross-reference (F2).
- `docs/README.md`: `# Orca Docs` -> `# Forseti Docs` (F3).
- `docs/STRUCTURE.md`: `# Orca Docs Structure` -> `# Forseti Docs Structure` (F3).

No code, CI, hook logic, or harness file was touched — only doc prose/headings
inside files the migration itself already edited. Nothing outside the named
findings was changed.

## Unified Diff

```diff
diff --git a/docs/README.md b/docs/README.md
index f0e93cc3..b5273e10 100644
--- a/docs/README.md
+++ b/docs/README.md
@@ -1,4 +1,4 @@
-﻿# Orca Docs
+﻿# Forseti Docs
 
 This folder holds Forseti-owned durable artifacts. It does not contain software
 implementation. The detailed navigation map is `STRUCTURE.md`; the Orca overlay
diff --git a/docs/STRUCTURE.md b/docs/STRUCTURE.md
index 6317e856..c193c0ce 100644
--- a/docs/STRUCTURE.md
+++ b/docs/STRUCTURE.md
@@ -1,4 +1,4 @@
-# Orca Docs Structure
+# Forseti Docs Structure
 
 ```yaml
 retrieval_header_version: 1
diff --git a/docs/workflows/orca_repo_map_v0.md b/docs/workflows/orca_repo_map_v0.md
index 1df7e993..7fe1f80a 100644
--- a/docs/workflows/orca_repo_map_v0.md
+++ b/docs/workflows/orca_repo_map_v0.md
@@ -406,8 +406,7 @@ nickname: "crawling graph." The runner is
 | `.githooks/` | Tracked local Git hook adapters installed via `.github/scripts/install-local-hooks.ps1`; catches local Git push/commit boundaries where enabled. Bypassable with `--no-verify`; not a server-side lock. |
 | `.agents/workflow-overlay/` | Orca overlay authority for project facts, folders, source rules, prompt rules, validation, safety, and review lanes. |
 | `.agents/hooks/` | Portable enforcement/checker scripts for protected actions, retrieval headers, repo-map freshness, and local Git pre-push policy. Harness adapters invoke these scripts; passing checks are not validation or readiness. |
-| `forseti-harness/` | Bounded authorized implementation backing Data Capture source acquisition and the v0.14 Judgment Harness (capture adapters, source-observability, schemas, scoring, runners, fixtures, tests). Navigation context only; not runtime, acceptance, or readiness. See the Orca Harness section. |
-| `orca/` | Declared top-level product-tree root. Product substance lives under `forseti/product/`; runtime remains under `forseti-harness/`. |
+| `forseti-harness/` | Bounded authorized implementation backing Data Capture source acquisition and the v0.14 Judgment Harness (capture adapters, source-observability, schemas, scoring, runners, fixtures, tests). Navigation context only; not runtime, acceptance, or readiness. See the Forseti Harness section. |
 | `forseti/product/` | Spine-first product tree: product contracts, Core Spine artifacts, proof plans, source/evidence standards, offer, buyer-proof, demand-signal method/surface docs, satellites, case families, and shared product registries. Historical product-docs references resolve through `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md`. |
 | `forseti/product/spines/data_lake/` | Data Lake shared-foundation spine (promotion-bound 2026-06-18; contracts + mechanics landed by R2). Owns cross-layer storage contracts (raw-packet preservation, keyed retrievability, Attachment Record, passive Availability Index) and the medallion/gold-readiness contract consumed by projection/ECR/cleaning/judgment. Binding: `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`. |
 | `forseti/product/spines/data_lake/authority/` | Data Lake contracts/invariants: core, storage, Attachment-Record implementation, and medallion/gold-readiness contracts. |
@@ -470,7 +469,7 @@ nickname: "crawling graph." The runner is
 | `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` | Judgment Spine submap. Open before enumerating Judgment owners across `docs/research/judgment-spine/` and `forseti/product/spines/judgment/`. |
 | `forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md` | Operator playbook for the bounded Amazon/Sephora/Ulta Retail/PDP CloakBrowser sidecar smoke: canonical URLs, flags, scratch outputs, expected residuals, failure taxonomy, and code-enforceable follow-up flags. |
 
-## Orca Harness
+## Forseti Harness
 
 `forseti-harness/` is bounded, authorized implementation backing Data Capture
 source acquisition and the v0.14 Judgment Harness. It is navigation context
```

## Fresh-Read Evidence For Changed Files

Post-patch, re-read each patched file directly from disk (not from memory of
the edit) to confirm the durable state:

- `docs/README.md:1` -> `# Forseti Docs` (confirmed via `head -3`).
- `docs/STRUCTURE.md:1` -> `# Forseti Docs Structure` (confirmed via `head -3`).
- `docs/workflows/orca_repo_map_v0.md:472` -> `## Forseti Harness` (confirmed
  via `grep -n "^## Forseti Harness\|^## Orca Harness"`, single match, the new
  heading; zero remaining `## Orca Harness`).
- `docs/workflows/orca_repo_map_v0.md` Top-Level Structure table: `orca/` row
  absent (confirmed by re-reading lines 404-412 post-patch); `forseti-harness/`
  row now reads "See the Forseti Harness section."
- `git status --porcelain` in the isolated worktree shows exactly the three
  intended files modified, nothing else.

## Validation

Run in the isolated detached worktree (`C:/tmp/orca-pr826-review`) at the
patched tree, HEAD detached from `f53e6f2ef24df24bb88079453dd6b2383a508dd0`:

```text
$ git diff --check 397b15705a68e22e1400c093d947a0f093d5eec9..HEAD
(no output)                                                    -> GATE PASS (exit 0)

$ python .agents/hooks/check_retrieval_header.py --changed --strict
(no output)                                                    -> GATE PASS (exit 0)

$ python .agents/hooks/check_deletion_evidence.py --strict
check_deletion_evidence --strict: OK -- every governed deletion in this diff
carries a complete evidence record                             -> GATE PASS (exit 0)

$ python .agents/hooks/check_map_links.py --strict
check_map_links --strict: OK (0 findings)
annotated nonresolving: 35 (debt, not failures)                -> GATE PASS (exit 0)

$ python .agents/hooks/check_repo_map_freshness.py --changed
(no output)                                                    -> GATE PASS (exit 0)
```

`forseti-harness` pytest / ontology / drift gates were **not** re-run: the
patch touched only doc prose/headings in three `.md` files already inside the
migration's changed-file set — no code, CI, or harness file was patched, so
the prompt's conditional pytest re-run requirement does not trigger. The
prompt's Observed Implementation Context already records
`python -m pytest` -> `1241 passed, 3 skipped` and `check_ontology_ssot.py` /
`check_ontology_tag_validity.py` / `check_ontology_drift.py` all `--strict` OK
for this same commit; this review treated that as context to inspect (per the
commission), and independently re-derived the five gates above rather than
inheriting the rest, since only those five are the ones this patch could have
affected.

## Non-Findings / Seams That Held

- `orca/`, `orca/product/`, and `orca-harness/` are genuinely absent from the
  physical tree at the target commit (`ls` confirms `No such file or
  directory` for all three); `forseti/`, `forseti/product/`, and
  `forseti-harness/` are present with coherent contents.
- `.github/workflows/ci.yml` correctly points `working-directory` and the job
  name at `forseti-harness`; no residual `orca-harness` reference.
- `.agents/hooks/guard_protected_actions.py`'s `REPO_SLUGeric-foo/forseti` and
  associated selftest cases were updated consistently; `.github/scripts/merge-when-green.ps1`,
  `.github/workflows/pr-risk-router.yml`, and `.gitignore` were all correctly
  repointed at `forseti-harness/` / `eric-foo/forseti` with no missed lines.
- `check_deletion_evidence.py`'s `GOVERNED_ROOTS` moved from `("orca/product/",)`
  to `("forseti/product/",)` consistently, including every selftest fixture
  case (11 inline test-data paths all updated together).
- `check_map_links.py`, `check_ontology_ssot.py`, `check_ontology_tag_validity.py`,
  `check_ontology_drift.py`, `check_ontology_expansion.py`, `check_doc_terms.py`,
  `check_commission_signal_board_output.py`, and `remind_sci.py` all had their
  hardcoded `orca/product/` / `orca-harness/` path constants (not just
  comments) consistently repointed to `forseti/product/` / `forseti-harness/`,
  including nested selftest fixtures — checked each hook's full diff, not just
  a grep hit count.
- `forseti-harness/pyproject.toml` package name (`forseti-harness`) and
  `[tool.setuptools.packages.find]` block are internally coherent; no stray
  `orca` package name.
- `.agents/skills/forseti-product-lead/SKILL.md` and
  `.claude/skills/forseti-product-lead/SKILL.md` both exist at the target
  commit; no `orca-product-lead` alias exists there (one appears in this
  review's own home branch, `claude/forseti-live-root-migration-review-009fc0`,
  but that is a later, unrelated commit — not part of PR826's pinned range —
  confirmed by diffing the target commit's `.agents/skills/` /
  `.claude/skills/` listing directly).
- `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`
  is present at the target commit and is the successor of the deleted
  `orca/product/spines/foundation/ontology/fragrance_reference_v0.yaml` (git
  recorded it as delete+add rather than a detected rename, below the
  similarity threshold, but content lands at the new path — not a data-loss
  bug).
- Residual `ORCA_DATA_ROOT` (env var name), `--report-orca` (CLI flag name),
  `.orca-data-root` (marker filename), and `Orca...` user-agent strings inside
  `forseti-harness/` runtime code are all deliberately-deferred compatibility
  surfaces per the commission's boundary, not migration bugs — checked each
  one's actual runtime role (repo-root detection uses `.git`-marker search,
  not a hardcoded `orca` folder-name match, so none of these create live path
  breakage).
- `docs/migration/**`, `docs/review-inputs/**`, and `_scratch/**` still contain
  literal `orca-harness/` / `orca/product` path strings; these are frozen
  historical/provenance artifacts (completed one-time migration scripts, a
  frozen review-input snapshot, and non-canonical scratch), correctly left
  untouched per the commission's compatibility boundary.
- `.agents/hooks/check_map_links.py`'s `_COVERAGE_ROOT_PREFIXES` frozenset
  retains a bare `"orca"` entry alongside the renamed `"forseti/product"` etc.
  Reviewed and judged a non-finding: the comment above it was updated
  ("structural roots (`forseti/product`, docs, ...)"), and the leftover
  `"orca"` token can never match a live path now that `orca/` is deleted — it
  is inert, not a false-negative source. Below the bar for a patch (dead
  token, zero behavioral effect); flagged here as an optional, non-required
  cleanup opportunity for a future pass, per the "label optional hardening as
  optional" rule.

## Residual Risk

- The three patched files are docs-only; residual risk from this specific
  patch is near zero (verified by the fresh reads and the five validation
  gates above).
- Broader residual risk inherent to the underlying 1418-file migration (not
  addressed by this bounded patch, and outside its authorized scope): the
  "touched body, missed heading/adjacent-line" pattern found three times here
  (F1-F3) means other similar, lower-salience prose mismatches likely remain
  somewhere in the ~1400 untouched-by-this-review files; a full line-by-line
  read of the entire diff was not performed (infeasible within a bounded
  review), so this review's coverage is a targeted sweep (CI, hooks, repo
  maps, top-level docs, skills, package config, deletion set) rather than an
  exhaustive one. No evidence of a *functional* (gate-breaking or
  path-breaking) defect was found beyond the three patched items, all of
  which were message/prose-only.
- The review prompt's own `docs/hygiene/migrations/moved_paths_index.md`
  source-context reference does not resolve to any file in the repo (see
  Method section). This is a defect in the commissioning prompt, not in
  PR826, and is out of this review's patch authority (prior prompts are
  excluded from the Patch Boundary).

## Review-Use Boundary

These findings and the applied patch are decision input for Chief Architect
adjudication only. They are not approval, validation, mandatory remediation,
or merge authority. No commit, push, merge, or PR-metadata edit was made
anywhere in this review; all inspection and patching occurred in an isolated
detached worktree (`C:/tmp/orca-pr826-review`) separate from both the CA/home
lane and this report's own worktree.

## Verdict

`PATCHED_FOR_CA_ADJUDICATION`
