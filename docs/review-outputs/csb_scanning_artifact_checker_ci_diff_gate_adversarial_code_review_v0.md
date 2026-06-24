# CSB Scanning Artifact Checker CI Diff Gate — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Adversarial implementation/code review of the CSB-first scanning artifact
  checker CI diff gate (PR #367, commit aa331e53).
use_when:
  - Consuming findings from this review as CA decision input for PR #367.
  - Verifying enforcement closure status for E-01 through E-04.
authority_boundary: retrieval_only
reviewed_by: claude-sonnet-4-6
authored_by: openai-gpt-5-codex
de_correlation_bar: cross_vendor_discovery
```

## Review Provenance

- `reviewed_by`: claude-sonnet-4-6 (Anthropic / Claude lineage)
- `authored_by`: openai-gpt-5-codex (OpenAI / GPT lineage)
- `de_correlation_bar`: `cross_vendor_discovery` — reviewer and author are
  different upstream vendors (Anthropic vs OpenAI); cross-vendor discovery bar
  is satisfied.
- `same_vendor_rationale`: not applicable (cross-vendor).
- Commission: `csb_scanning_artifact_checker_ci_diff_gate_delegated_adversarial_code_review_prompt_v0.md`
- Source-loading mode: advisory implementation/code review (no formal Orca
  implementation-review lane is bound; review lane from prompt commission).
- Reviewer write permission: write to `docs/review-outputs/` only.

---

## Source-Read Ledger

| Source | Status | Notes |
| --- | --- | --- |
| `AGENTS.md` | READ | Agent behavior kernel, smallest complete intervention, operating economy. |
| `.agents/workflow-overlay/README.md` | READ | Overlay entrypoint. |
| `.agents/workflow-overlay/source-loading.md` | READ | Source-pack tiers, High-Context Guard, orca_start_preflight receipt. No material change to implementation findings. |
| `.agents/workflow-overlay/prompt-orchestration.md` | READ | Source-Gated Method Contract, review prompt defaults, output modes. No material change to implementation findings. |
| `.agents/workflow-overlay/review-lanes.md` | READ | Review lane doctrine, two-bar de-correlation, advisory boundary. |
| `.agents/workflow-overlay/delegated-review-patch.md` | READ | Incomplete commission route-out: multi-file implementation diff → implementation/code review. |
| `.agents/workflow-overlay/validation-gates.md` | READ | Enforcement placement, gate semantics. |
| `.agents/workflow-overlay/safety-rules.md` | READ | Project-specific safety, reviewer read-only rule. |
| `.agents/workflow-overlay/source-of-truth.md` | READ | Source hierarchy. |
| `.agents/hooks/check_csb_scanning_artifact.py` | READ (full) | Primary review target. |
| `.github/workflows/ci.yml` | READ (full) | CI wiring target. |
| `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py` | READ (full) | Test target. |
| `orca/product/spines/scanning/README.md` | READ (full) | Scanning doc target. |
| `docs/workflows/orca_repo_map_v0.md` | READ (full) | Repo map target. |
| `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md` | READ (full) | Reference fixture. |
| `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_missing_broad_scout.md` | GLOB FOUND, NOT READ | Existence confirmed. |
| Implementation diff (commit range) | RUN | `git diff c4cc9e3e..aa331e53 -- [5 target files]`. |
| Later prompt-only commit | CONFIRMED CLEAN | `47b79943` (docs: add review prompt) — zero changes to any target file. |

**SOURCE_CONTEXT_READY**

Target files at `aa331e53` are confirmed unchanged by the later prompt-only commit `47b79943`. The five review targets are exactly as committed.

---

## Validation Commands Run

| Command | Status | Output |
| --- | --- | --- |
| `python -B .agents/hooks/check_csb_scanning_artifact.py --diff origin/main --strict` (30 s timeout) | PASS | `check_csb_scanning_artifact: no changed CSB-first scan artifacts detected` exit 0 |
| `python -B .agents/hooks/check_csb_scanning_artifact.py --selftest` | PASS | `SELFTEST OK` exit 0 |
| `python -B -m pytest -q -p no:cacheprovider orca-harness/tests/unit/test_csb_scanning_artifact_validator.py` | PASS | All 47 tests exit 0 |

Commands NOT independently rerun (author-supplied evidence accepted):
- `--changed --strict`
- Full harness pytest
- `git diff --check`, retrieval-header check, repo-map freshness, map-links, placement check, CI YAML parse
- PR #367 CI readback

---

## Findings

**No blocker or major findings.** The implementation closes all four enforcement goals. Advisory findings follow.

### FIND-01 (minor): `repo_root()` followed by three blank lines instead of two

- **Target file**: `.agents/hooks/check_csb_scanning_artifact.py:622`
- **Evidence**: The diff adds `repo_root()` at line 622 followed by three blank lines before `_git_lines`. PEP 8 and the existing codebase pattern uses two blank lines between top-level functions.
- **Authority**: PEP 8 / codebase consistency.
- **Impact**: No correctness impact. Minor visual inconsistency.
- **minimum_closure_condition**: Remove one blank line between `repo_root()` and `_git_lines()`.
- **next_authorized_action**: Owner may fix inline or leave as cosmetic debt; not a gate condition.
- **Validation expectation**: Not testable; visual review suffices.
- `patch_queue_entry`: NOT AUTHORIZED (advisory review lane only).

### FIND-02 (minor): Two-dot diff fallback could over-detect on atypical branch topology

- **Target file**: `.agents/hooks/check_csb_scanning_artifact.py:672`
- **Evidence**:
  ```python
  def diff_paths(root: Path, base_ref: str) -> list[str] | None:
      lines = _git_lines(root, ["diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"])
      if lines is not None:
          return lines
      return _git_lines(root, ["diff", "--name-only", "--diff-filter=ACMR", base_ref, "HEAD"])
  ```
  The three-dot diff (`origin/main...HEAD`) computes the symmetric difference from the merge base: only files changed on the PR branch since diverging from main. The two-dot fallback (`origin/main HEAD`) computes ALL files differing between the tips of the two refs — this includes any file that differs between current main tip and the PR branch tip, even files that were modified on main but not on the PR branch. If main has scan artifacts that differ from the branch baseline, the two-dot fallback could over-detect them.
- **Authority**: Git diff semantics; `git-scm.com` three-dot vs two-dot diff definition.
- **Impact**: The fallback only fires when three-dot diff returns non-zero (git error). With `fetch-depth: 0` in CI, `origin/main` is always available, and this condition should not occur in normal CI. If it did fire, the over-detection would yield false findings on the incorrectly detected files (not false passes). Risk is low in practice.
- **minimum_closure_condition**: Document the fallback semantics in a comment, or remove the fallback and let `None` trigger fail-open directly. As-is the fallback adds theoretical risk with no demonstrated benefit when `fetch-depth: 0` is the CI checkout posture.
- **next_authorized_action**: Owner decision — accept residual risk (guarded by `fetch-depth: 0`) or tighten by removing the fallback. Advisory; not a gate condition.
- **Validation expectation**: Not covered by existing tests; would require a mock git environment.

### FIND-03 (minor): `--strict` flag is accepted but is a no-op

- **Target file**: `.agents/hooks/check_csb_scanning_artifact.py:760`
- **Evidence**:
  ```python
  parser.add_argument("--strict", action="store_true",
      help="accepted for CI readability; findings already exit 1")
  ```
  `args.strict` is never read after parsing.
- **Authority**: The help text accurately documents this as intentional. This matches the existing pattern in other Orca hooks (e.g., `check_map_links.py --strict`).
- **Impact**: No functional gap. The flag is a CI API convention for readability/parity with sibling hooks. The absence of any `--strict` gate elevation (e.g., converting warnings to errors) means the strict mode does nothing additional, which is consistent with "findings already exit 1."
- **minimum_closure_condition**: No closure needed if this is intentional API parity. Optionally add a comment: `# --strict is a no-op; provided for API parity with sibling hooks`.
- **next_authorized_action**: Confirm intent as documented; no action required.
- **Validation expectation**: Intentional design; no test needed.

### FIND-04 (minor): `csb_row_accounting` detection uses text-presence, not section-heading anchor

- **Target file**: `.agents/hooks/check_csb_scanning_artifact.py:129`
- **Evidence**:
  ```python
  "csb_row_accounting": re.compile(
      r"(csb_rows_consumed|Rows consumed as route map:)",
      re.IGNORECASE | re.MULTILINE,
  ),
  ```
  Unlike `broad_scout_accounting` (requires `^## Broad Scout`), `csb_row_accounting` passes if either token appears anywhere in the document. A doc that says "the csb_rows_consumed field was not applicable" in a prose paragraph would satisfy this section check without a dedicated accounting block.
- **Authority**: Compared against `SECTION_PATTERNS` for other required sections (all other patterns are `^##` anchored except `csb_row_accounting`).
- **Impact**: Lower receipt bar for CSB row accounting than other sections. The secondary check `_validate_csb_row_ids` requiring at least one `SBR-NNN` ID partly compensates. The valid fixture satisfies both checks with in-line prose "Rows consumed as route map: SBR-001 through SBR-003." under a "## CSB Board Intake" heading, which is the documented pattern.
- **minimum_closure_condition**: Acceptable as-is if prose-level CSB row accounting (not a dedicated `##` section) is the intended artifact shape. The secondary `_validate_csb_row_ids` check adds meaningful coverage.
- **next_authorized_action**: Owner confirms intended artifact shape; no code change required if prose accounting is valid.
- **Validation expectation**: Covered by `test_required_receipt_parts` (replacing the accounting text removes section detection) and `test_csb_row_accounting_requires_sbr_ids`.

### FIND-05 (advisory): Auto-detection could trigger on non-scan `docs/research/` docs that contain all required markers

- **Target file**: `.agents/hooks/check_csb_scanning_artifact.py:679`
- **Evidence**:
  ```python
  AUTO_SCAN_REQUIRED_MARKERS = (
      "commission_id:",
      "source_context_status:",
      "closeout_state:",
  )
  AUTO_SCAN_ROUTE_MARKERS = (
      "csb-first",
      "csb board",
      "csb_rows_consumed",
      "rows consumed as route map",
  )
  ```
  A `docs/research/` file that discusses CSB-first scanning methodology (e.g., a research note that includes a template snippet) could match all markers and be run through the validator, producing false findings. This does NOT create a false pass (the malformed file would fail validation) but could create noisy CI failures on innocent research docs.
- **Impact**: Advisory noise only. The path filter (`docs/research/`) and the requirement for ALL three YAML field names plus at least one route marker makes accidental matches unlikely in practice.
- **minimum_closure_condition**: Acceptable given the low false-match probability. No action required.
- **next_authorized_action**: Monitor; act if a real false-match CI failure appears.
- **Validation expectation**: `test_auto_detection_requires_csb_route_marker` covers one direction; no test for the false-positive direction (acceptable gap given low risk).

---

## Open Questions And Residual Risk

1. **`changed_paths` (`--changed` mode) covers working-tree, staged, and untracked changes but not stashed changes.** If a developer stashes a scan artifact and runs `--changed`, it would not be detected. This is standard git behavior and an acceptable gap.

2. **The `resolve_base_ref` env-var override**: if `GITHUB_BASE_REF` is set in a non-CI local environment (e.g., a developer with that env var set from a prior session), the CLI argument `origin/main` would be silently ignored and `GITHUB_BASE_REF` would be used instead. Low practical risk but worth noting for local debugging ergonomics.

3. **No test for the fail-open path** (`diff_paths` returns `None`). The CI behavior on git failure is documented and the message goes to stderr, but the path is not unit-tested. Acceptable gap.

4. **The `csb board` route marker** (lowercase match) is fairly broad. "CSB Board" appears in the fixture under "## CSB Board Intake" and "Rows consumed as route map" is the prose accounting line. These are strong enough signals in `docs/research/` context.

---

## Intended Enforcement Closure Check

| Goal | Status | Evidence |
| --- | --- | --- |
| **E-01** — changed-file discovery (`--changed` and `--diff BASE` find changed CSB-first scan artifacts by path and marker shape) | `closed` | `changed_paths` covers unstaged/staged/untracked. `diff_paths` uses three-dot diff against `origin/main` (with two-dot fallback). `looks_like_csb_first_scan_artifact` requires path prefix + all three YAML markers + at least one CSB route marker. `test_auto_detection_*` tests cover the discovery boundaries. Residual: two-dot fallback semantics (FIND-02, minor, low-risk in practice). |
| **E-02** — CI gate wiring (PR CI runs the checker against `origin/main` in strict diff mode) | `closed` | CI step added between retrieval-header-index and ontology-SSOT, working-directory set to `${{ github.workspace }}`, command `python .agents/hooks/check_csb_scanning_artifact.py --diff origin/main --strict`. `fetch-depth: 0` ensures `origin/main` is available. `GITHUB_BASE_REF` override in `resolve_base_ref` correctly handles all PR contexts. False-failure risk on unrelated PRs: none (only `docs/research/*.md` with CSB markers are detected). |
| **E-03** — preservation of explicit validation (existing explicit-path and selftest validation still works) | `closed` | Explicit paths parsed by argparse as positional `args.paths`; prepended to `auto_targets` result. `--selftest` still routes to `selftest()`. `validate_paths` extracted from the old inline loop with identical behavior. |
| **E-04** — scan-lane doctrine alignment (docs frame the checker as mechanical receipt enforcement, not quality proof, capture authorization, or candidate readiness) | `closed` | Scanning README updated to add "CI also runs the checker in forward-only diff mode"; retains "enforces receipt shape only... does not grade signal quality, prove buyer demand, validate candidates, or bind Capture routes." Repo map updated from "portable/manual" to "portable + CI diff-scoped" with the same non-claim text. DCP receipt in README updated with `.github/workflows/ci.yml` in both `controlling_sources_updated` and `downstream_surfaces_checked`. No overclaiming found. |

---

## Review Use Boundary

Review findings are decision input only. They are not approval, validation, mandatory remediation, readiness, or executor-ready patch authority until the Chief Architect separately accepts or authorizes them.

This is a zero-config findings-only advisory implementation/code review. No formal Orca implementation-review lane is bound. No formal `PASS`/`FAIL` verdict, severity taxonomy, patch queue, or readiness claim is made. The de-correlation bar is `cross_vendor_discovery` (Anthropic reviewer, OpenAI author); this satisfies the discovery bar for findings about the new changed-file logic and CI wiring.
