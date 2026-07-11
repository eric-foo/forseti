# Forseti Data-Root Runner Enforcement — Adversarial Code Review

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial read-only review of the pinned commit 64269fb5 (data_lake/inventory.py + test_capture_runner_lake_seam_coverage.py) hardening the Bronze-writer lake-seam detector and the TikTok live-probe explicit-root-only exception.
use_when:
  - Adjudicating PR #860 before merge.
  - Checking whether the seam detector's env-fallback heuristic or the explicit-root-only exception has known residual gaps.
authority_boundary: retrieval_only
branch_or_commit: codex/forseti-data-root-default @ 64269fb5d4ec5b0d8b4c2c97b0b83be65e125a12 (parent d94d211f83a500ff160bae4303d25966461fe059)
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/forseti_data_root_runner_enforcement_adversarial_code_review_v0.md
  recommendation: accept_with_friction
  reviewed_by: claude-sonnet-5
  authored_by: unrecorded
  de_correlation_bar: self_fallback
  same_vendor_rationale: null
  summary: "The pinned patch correctly closes the text-spoofed-compliance gap it targets and the TikTok live-probe cannot ambient-write, but the fix leans on flag-name-specific heuristics that create one concrete, PR-relevant regression-coverage gap (FDR-02) plus several lower-severity residual gaps."
  findings_count: 5
  blocking_findings: []
  advisory_findings: [FDR-01, FDR-02, FDR-03, FDR-04, FDR-05]
  prior_findings_remediated: []
  next_action: "CA adjudicates FDR-02 (missing --admit-output-named exclusivity regression coverage); no self-closable material issue found."
```

```yaml
adjudication_summary:
  status: completed
  adjudicated_by: unrecorded
  recommendation: accept
  accepted_and_closed:
    - FDR-02: direct parser-contract regression added for the --admit-output/--data-root mutually-exclusive group
  accepted_residuals:
    - FDR-01: current runner population defended; broader positive resolve-call AST proof is outside this patch
    - FDR-03: alternate environment-read idioms fail loud and are not current house usage
    - FDR-04: synthetic AST coverage is sufficient for the helper's bounded behavior
    - FDR-05: pre-existing whole-file token heuristic; no defect introduced by this diff
  severity_adjudication:
    FDR-02: minor  # real regression-coverage gap, but current runtime behavior is correct and selects one destination
  validation:
    - focused closure plus resolver/seam/inventory suite: passed (pytest exit 0; one known symlink skip)
    - git diff --check: passed
  next_action: "Land the review report and bounded FDR-02 closure test on PR #860; no further material detector work is required for this PR."
```
## Goal (carried from commission)

Future capture runners and captures use the centrally resolved Forseti
data-lake root, while the explicitly excepted TikTok live probe cannot
silently turn a routine staging probe into a durable ambient write. Done
looks like: an adversarial reviewer can account for every detector
pass/fail path and packet-writer classification in the pinned diff, with
regression tests that catch spoofed compliance and preserve the
explicit-root-only exception honestly. Treated as an axis to attack, not a
pass-if-matches bar.

## Source Context

`SOURCE_CONTEXT_READY.`

Files read in full: `forseti-harness/data_lake/inventory.py`,
`forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`,
`forseti-harness/data_lake/root.py` (central resolver),
`forseti-harness/runners/run_source_capture_tiktok_live_batch_probe.py`.
Targeted greps: `runners/*.py` for `ORCA_DATA_ROOT`, `"--output"`,
`os.environ.get`, `os.getenv`. Overlay sections read: README, source-loading
(Rule/Preflight/Source Pack Tiers/Targeted Read Protocol), review-lanes
(Current Lanes/Review Doctrine/Rules), validation-gates (Current
Gates/Prompt Orchestration Gates), prompt-orchestration (full, per the
delegated-review-patch escalation trigger), artifact-roles, retrieval-metadata.
`workflow-deep-thinking` and `workflow-code-review` were reference-loaded
(their descriptions consulted for an adversarial, coverage-first posture)
but not separately invoked as nested Skill calls; the failure-mode checklist
already supplied by the commission was used directly as the adversarial
frame, and the actual analysis below was performed by direct source reading
and verification rather than delegated to another agent. This is a
deliberate compression, named rather than silently taken — see
`review-use boundary` below.

Sources available not read: `forseti-harness/pyproject.toml` (import/test
discovery behavior was not in question), other 22 EXPECTED_BRONZE_WRITER
runner files beyond the three spot-checked for the OR-fallback heuristic
(spot-checked as a representative, not exhaustive, sample).

Controlling-source state: worktree clean; branch and HEAD matched the
pinned `expected_branch`/`expected_revision` exactly; parent matched
`base_revision` exactly (all verified via fresh `git status --short
--branch` / `git rev-parse HEAD` / `git show --stat` reads before any
analysis).

## Findings

### FDR-01 — `exposes_env_fallback`'s OR-heuristic infers ambient support from flag absence, not from a verified resolve() call

- Severity: minor · Confidence: medium
- File/line: `forseti-harness/data_lake/inventory.py:802-805`

```python
exposes_env_fallback=(
    "FORSETI_DATA_ROOT" in env_names
    or ("--output" not in flags and "--admit-output" not in flags)
),
```

For a runner with neither a literal `--output` nor `--admit-output` flag,
`exposes_env_fallback` is granted unconditionally — with no check that the
runner actually calls `DataLakeRoot.resolve(explicit=args.data_root)` with
a nullable `args.data_root`, as opposed to e.g. a hardcoded explicit value
or a coding bug that silently drops the user's `--data-root` argument. I
spot-checked the three current runners that rely on this branch alone
(`run_source_capture_ig_reels_audio_packet.py`,
`run_source_capture_youtube_asr_packet.py`,
`run_source_capture_youtube_rss_monitor.py`) and each genuinely does
`parser.add_argument("--data-root", default=None, ...)` then
`DataLakeRoot.resolve(explicit=args.data_root)` — so the heuristic's
assumption holds for the present runner population (see
`considered_and_defended`). The residual is architectural: a future runner
without `--output`/`--admit-output` that gets this wrong would earn the same
credit with no positive evidence.
- Why it matters: this is exactly the "ambient-write safety" axis the PR
  is meant to hardenpath — the check that is supposed to prove a runner
  supports the canonical env fallback is an absence-of-flags inference, not
  a call-site verification.
- `minimum_closure_condition`: either a positive AST check that the
  runner's `DataLakeRoot.resolve(...)` call is passed the same nullable
  `--data-root` argument value, or an explicit named acceptance that this
  heuristic is intentionally coarse for the current runner population.
- `next_authorized_action`: owner/CA decision on whether to harden now or
  accept as a named residual.

### FDR-02 — Flag-name mismatch leaves the TikTok runner's `--admit-output`/`--data-root` exclusivity outside the AST-level regression suite

- Severity: major · Confidence: medium-high
- File/line: `forseti-harness/data_lake/inventory.py:583-587` (`has_exclusive_output_mode`), `:800` (`exposes_output_arg`), vs `:804` (`exposes_env_fallback`'s own flag check); `forseti-harness/runners/run_source_capture_tiktok_live_batch_probe.py:67-85`

`exposes_output_arg` checks only the literal flag `"--output"` (line 800).
The TikTok runner exposes `--admit-output`/`--data-root` instead (a
`mutually_exclusive_group`, lines 67-85), so `exposes_output_arg` is
`False` for it and `has_exclusive_output_mode` short-circuits to `True`
(`if not self.exposes_output_arg: return True`, line 585) without ever
checking `rejects_output_and_data_root` or
`env_fallback_uses_output_omitted`. Concretely: `test_packet_runner_output_modes_are_exclusive`
never examines this runner's local-vs-lake exclusivity at all. The only
thing enforcing "don't admit to both `--admit-output` and `--data-root`
simultaneously" for this runner is the runtime `add_mutually_exclusive_group(required=False)`
call — which I verified is correct today — but a future edit that
weakened or removed that grouping would not be caught by the contract-test
suite the way an equivalent regression in an `--output`-named runner would
be. Notably, the *same* diff's own `exposes_env_fallback` OR-clause (line
804) *does* recognize `--admit-output` as a local-output escape valve for
the opposite purpose (denying ambient-fallback credit) — so the two
flag-recognition sets inside this one dataclass are inconsistent with each
other for this exact runner.
- Why it matters: this is the one runner the PR is specifically about, and
  its most safety-relevant property (can't accidentally admit to both a
  local file and the lake) is invisible to the mechanical regression suite.
- `minimum_closure_condition`: either extend `exposes_output_arg` (or add a
  parallel check) to recognize `--admit-output`-style local-output flags so
  `has_exclusive_output_mode` actually inspects this runner, or an explicit
  named acceptance that the argparse-level guard alone is the accepted
  control for this runner.
- `next_authorized_action`: owner/CA decision; this is advisory remediation
  direction, not a patch queue entry.

### FDR-03 — `environment_get_names` only recognizes the `os.environ.get(...)` call form

- Severity: minor · Confidence: high
- File/line: `forseti-harness/data_lake/inventory.py:718-736`

`os.getenv("FORSETI_DATA_ROOT")` or `os.environ["FORSETI_DATA_ROOT"]` would
not be detected. I grepped `runners/`, `source_capture/`, and `data_lake/`
for `os.getenv` and found zero uses repo-wide, so this is currently latent,
not exploited. Because a runner using either alternate idiom would simply
fail to earn `exposes_env_fallback` credit (and, for a dual-mode runner,
fail `test_every_packet_runner_is_lake_wired_or_acknowledged` loudly), this
gap fails in the safe direction (false negative / loud test failure), not
as a silent false pass.
- Why it matters: coverage-first — worth naming even though it currently
  fails safe.
- `minimum_closure_condition`: recognize the additional call/subscript
  forms, or explicitly document that `os.environ.get(...)` is the required
  house style.
- `next_authorized_action`: optional hardening; non-blocking.

### FDR-04 — No integration-level regression test proves the help-text-spoof fix for an ordinary (non-exception) runner

- Severity: minor · Confidence: medium
- File/line: `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:268-281`, `:327-350`

`test_detector_requires_a_real_canonical_environment_read` (lines 268-281)
exercises `environment_get_names` only against synthetic, hand-built ASTs.
The only integration-level proof against a real file is
`test_explicit_data_root_runner_declarations_are_current_and_reasoned`
(lines 327-350), and that is scoped to the one runner already in
`EXPLICIT_DATA_ROOT_RUNNERS`. There is no test asserting that an ordinary
dual-mode runner whose only textual evidence of env support is a help-text
mention (with no real `os.environ.get` call) would now correctly fail
`has_seam`. I did not find such a runner in the current tree to exercise
this against, and did not add one (out of scope for a read-only review).
- Why it matters: the reviewed diff's headline claim is "help text no
  longer certifies compliance"; the regression proof for the general case
  (not just the one named exception) rests on a synthetic unit test plus
  one specific real-file check.
- `minimum_closure_condition`: an integration test asserting `exposes_env_fallback`
  is `False` for a real (or minimal fixture) dual-mode runner whose only
  FORSETI_DATA_ROOT mention is in help text.
- `next_authorized_action`: optional hardening; non-blocking.

### FDR-05 — Detector-wide substring/token matching is not AST-verified to the specific write path (pre-existing, not introduced by this diff)

- Severity: minor · Confidence: high
- File/line: `forseti-harness/data_lake/inventory.py:592-598` (`missing_seam_parts` naming, `resolves_data_root`), `:67-71` (`EXPLICIT_PAIR_REJECT_TOKENS`), `:63-66` (`ENV_OUTPUT_OMITTED_TOKENS`)

`resolves_data_root="DataLakeRoot.resolve" in src` and the
`EXPLICIT_PAIR_REJECT_TOKENS`/`ENV_OUTPUT_OMITTED_TOKENS` checks are exact
substring/token matches over the whole file, not AST-verified to confirm
the matched pattern actually gates the specific packet-writer call in
question. This is unchanged by the reviewed diff (which only edits which
literal token strings are in the `ENV_OUTPUT_OMITTED_TOKENS` tuple and adds
the new `environment_get_names` AST helper alongside it) — I am naming it
because the commission asks whether the detector "can be satisfied by
incidental text... dead code... constants," and this is a standing,
broader instance of that same class of risk outside the two-file patch's
literal edits.
- Why it matters: bears on the review's mandate even though it predates
  this patch.
- `minimum_closure_condition`: n/a — named as a residual, not a defect in
  the pinned diff.
- `next_authorized_action`: no action required by this review; informational.

## Considered and Defended

- **TikTok runner's own help text literally contains the string
  "FORSETI_DATA_ROOT"** (`run_source_capture_tiktok_live_batch_probe.py:82-83`),
  which under the *pre-diff* naive substring check (`"FORSETI_DATA_ROOT" in
  src`) would have falsely certified `exposes_env_fallback=True` — the
  exact text-spoofed-compliance bug this diff fixes. Defense: post-diff,
  `environment_get_names` requires an actual `os.environ.get(...)` call
  (none exists in this runner), and the OR-fallback clause is blocked
  because `--admit-output` is present in its flags; the seam is granted
  instead through the new, correctly-scoped `explicit_data_root_only`
  branch. Verified by reading the real AST-detection code path and by the
  passing `test_explicit_data_root_runner_declarations_are_current_and_reasoned`,
  which runs `_packet_producers()` against the real file and asserts
  `exposes_env_fallback` is `False` for it.
- **Legacy-only `ORCA_DATA_ROOT` token removal from `ENV_OUTPUT_OMITTED_TOKENS`
  could regress a runner that relied solely on the legacy-only gating
  form.** Defense: grepped `runners/` for `ORCA_DATA_ROOT` outside
  `FORSETI_DATA_ROOT` context; the only two hits are help-text mentions
  (`run_source_capture_tiktok_live_batch_probe.py:83`,
  `run_tiktok_creator_discovery_register.py:56`), not gating code. The
  full pinned pytest set (below) passed clean.
- **The OR-fallback heuristic (FDR-01) could be silently wrong for real
  runners today, not just hypothetically.** Defense: identified the three
  real runners that rely on it alone
  (`run_source_capture_ig_reels_audio_packet.py`,
  `run_source_capture_youtube_asr_packet.py`,
  `run_source_capture_youtube_rss_monitor.py`) and confirmed each correctly
  passes a nullable `args.data_root` into `DataLakeRoot.resolve(explicit=...)`,
  so the ambient fallback genuinely exists via the shared resolver for all
  three. The heuristic's assumption is currently sound; FDR-01 remains open
  only as a structural/future-proofing concern.
- **The TikTok runner could still ambient-write if `FORSETI_DATA_ROOT` is
  set in the process environment.** Defense: traced the control flow —
  `DataLakeRoot.resolve(explicit=args.data_root)` is called only inside
  `if args.data_root is not None:` (runner lines 278-284), and `_production_candidate`
  in `data_lake/root.py:318-336` returns the explicit value immediately
  without consulting `env` when `explicit is not None`. With neither
  `--admit-output` nor `--data-root` passed (the default), the runner
  writes local staging JSON only and prints `"staging_only"` — no lake
  admission path is reachable at all.
- **The new `explicit_data_root_only`/`EXPLICIT_DATA_ROOT_RUNNERS` fields
  could silently drift into the generated, checked-in inventory JSON,
  creating undetected record drift.** Defense: `build_inventory()`
  (`inventory.py:854-915`) does not serialize any `RunnerSeam` field at all
  (only `runner`/`kind`/`a2_fork_impact`/`identity_binding`), so this
  change cannot desync `lake_touchpoint_inventory_v0.json`. Confirmed by a
  clean run of `test_data_lake_inventory_gate.py`.

## Validation Evidence Inspected / Rerun

All commands run from `forseti-harness/`, in the pinned worktree, with the
process-level `FORSETI_DATA_ROOT` and `ORCA_DATA_ROOT` removed for the
child process (verified unset, not merely assumed):

```
git status --short --branch
  -> ## codex/forseti-data-root-default...origin/codex/forseti-data-root-default (clean)
git rev-parse HEAD
  -> 64269fb5d4ec5b0d8b4c2c97b0b83be65e125a12  (matches expected_revision)
git show --stat --oneline --no-renames 64269fb5...
  -> "Harden Forseti data-root runner enforcement"; 2 files changed, 84 insertions(+), 6 deletions(-)
python -m pytest -p no:cacheprovider -q \
  tests/contract/test_capture_runner_lake_seam_coverage.py \
  tests/contract/test_data_lake_inventory_gate.py \
  tests/test_data_lake_root.py
  -> 68 passed, 1 skipped in 32.89s (exit 0)
  -> the 1 skip is tests/test_data_lake_root.py:393, "symlinks not supported in
     this environment" (Windows without symlink privilege) -- pre-existing,
     unrelated to this diff
git diff --check 64269fb5...^
  -> exit 0, no output (no whitespace-error findings)
```

Not rerun (recorded as reported evidence only, per the commission's
validation boundary, and outside the "at minimum" command list): `check_review_routing.py
--strict`, the local pre-push guard's full 5-gate run, and the GitHub
`forseti-harness-tests` required check. These remain `reported, not
independently verified` by this review.

## Source Gaps, Residual Uncertainty, Not-Proven Boundaries

- Only 3 of the ~13 runners that rely on the FDR-01 OR-fallback branch (by
  my rough classification) were spot-checked directly; the remaining
  producers were not individually re-verified against the heuristic's
  assumption (not proven for the full population, though the full pinned
  pytest run passing is corroborating evidence).
- `authored_by` is `unrecorded`: I have no verified provenance for which
  model/agent authored the pinned commit. The branch name
  (`codex/forseti-data-root-default`) is suggestive but not authoritative
  provenance, so it was not used to infer cross-vendor status.
- This review was performed directly by the reviewing agent in the
  requesting session rather than through a separately spawned,
  vendor-distinct delegate; `de_correlation_bar: self_fallback` reflects
  that no actual de-correlation occurred, not a claim that one was
  attempted and failed.
- `workflow-deep-thinking` and `workflow-code-review` were not invoked as
  separate Skill calls; the commission's own extensive failure-mode
  checklist was used as the adversarial frame instead, and the findings
  above were derived from direct source reads and reruns rather than a
  nested skill invocation. Named here rather than silently substituted.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation,
mandatory remediation, or executor-ready patch authority until separately
accepted or authorized by the commissioning Chief Architect/owner. No
patch, edit, commit, push, or PR action was taken or is authorized by this
report.

## CA Adjudication Closeout Instruction

Adjudicate in order: commission -> target -> authority -> decision
criteria -> evidence -> findings above. None of the five findings is
blocking; FDR-02 is the one with the clearest safety-relevant rationale
(a concrete, PR-relevant regression-coverage gap on the exact runner this
PR hardens) and is the natural candidate for a follow-up bounded patch if
the CA wants tighter coverage before or shortly after merge. If no
unresolved material issue remains, batch commit/push/PR/merge follow-ups
into one named land step with no deep-thinking, and deep-think the
material next moves that need judgment (for example: whether to extend
`exposes_output_arg`-style detection to `--admit-output`-named runners
repo-wide, or accept it as a named residual).
