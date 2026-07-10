# Enforcement Gate Wave (EP-10/EP-11/EP-15) — Delegated Adversarial Code Review-And-Patch Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact (delegated review-and-patch commission)
scope: >
  Commission prompt for the de-correlated adversarial code review-and-patch of
  the EP-10/EP-11/EP-15 enforcement gate wave (three new .agents/hooks checkers
  plus CI/test/guard wiring) on lane claude/sub-agent-spawning-plan-2dc064.
use_when:
  - Dispatching the delegated review of the enforcement gate-wave lane.
  - Adjudicating the return (this prompt binds the return contract).
authority_boundary: retrieval_only
```

Operator paste-instruction (who-constraint, not a model recommendation): the
author and adjudicator is Anthropic/Claude; paste the body below into a
different-family controller with repo access. Same-family defeats
de-correlation. Record the actual controller in the report's `reviewed_by`.

**Goal:** three doctrine rules (prompt output-mode presence, review_summary
shape, markdown hash-pin freshness) become deterministic CI gates that cannot
silently pass on broken logic. **Done looks like:** a reviewer attacking the
checkers finds no way to make a real violation read green, no born-red false
positive on legitimate corpus shapes, and every claimed selftest/audit result
reproduces. (Executor target + axis to attack, not a review pass bar.)

---

# Adversarial Delegated Code Review-And-Patch: EP-10/EP-11/EP-15 Gate Wave

You are the de-correlated CONTROLLER under
`.agents/workflow-overlay/delegated-review-patch.md`
(`delegated_code_review_and_patch`, `access: repo`, base-subagent). Review and
patch directly in your working tree; do NOT commit; the commissioning Chief
Architect adjudicates every hunk before anything is kept.

## Preflight (verify before review)
- Repo: https://github.com/eric-foo/orca ; branch
  `claude/sub-agent-spawning-plan-2dc064` (base `origin/main` @ `668b0e0d`);
  expected head: the lane PR's current head — clean tree required; mismatch =>
  STOP with the blocker.
- `AGENTS.md` and `.agents/workflow-overlay/README.md` read: required first.
- Required reads next: `.agents/workflow-overlay/delegated-review-patch.md`;
  the three rule-owner surfaces the checkers reference —
  `.agents/workflow-overlay/validation-gates.md` (Output-mode gate bullet,
  Review-summary shape gate bullet, Hash-pin freshness gate bullet, and the
  three new Enforcement Placement paragraphs),
  `.agents/workflow-overlay/communication-style.md` (review_summary shape,
  ~lines 185-255), `.agents/workflow-overlay/prompt-orchestration.md`
  (§ Output Modes).
- repo_map_decision: not_needed (targets exhaustive below). Source pack:
  bounded custom (the reads above plus the named diff). Edit permission:
  patch-only inside the named set. Dirty-state allowance: clean tree only;
  untracked files out of scope.
- Output mode: review-report; write the durable report at
  `docs/review-outputs/enforcement_gate_wave_ep10_ep11_ep15_delegated_adversarial_code_review_v0.md`
  with a valid retrieval header, non-blank `reviewed_by:` (your
  model+version), `authored_by: Anthropic Claude (Fable 5)`, and a
  `review_use_boundary:` stating findings are decision input and not approval,
  validation, readiness, mandatory remediation, or patch authority.
- Doctrine change: none authorized from this commission; the lane's own DCP
  receipt lives in `validation-gates.md` — flag defects in it, do not rewrite
  doctrine.
- External-source boundary: `jb`, external workflow source, and installed
  skills are not Forseti authority.

## Method (Source-Gated Method Contract)
1. REFERENCE-LOAD `workflow-deep-thinking` then `workflow-code-review`; do not
   APPLY yet.
2. SOURCE-LOAD: `git diff origin/main...HEAD`, every named file in full, the
   rule-owner sections above.
3. Declare SOURCE_CONTEXT_READY, then APPLY.

## Patchable named file set (CANNOT widen; label every finding/hunk)
- [output-mode] `.agents/hooks/check_prompt_output_mode.py`
- [review-summary] `.agents/hooks/check_review_summary.py`
- [hash-pin] `.agents/hooks/check_hash_pin_freshness.py`
- [ci-wiring] `.github/workflows/ci.yml` (only the three new gate steps)
- [test-wiring] `forseti-harness/tests/unit/test_hook_internal_error_gating.py`
  (only the three new CASES rows)
- [guard-mirror] `.agents/hooks/pre_push_guard.py` (only the new
  `check_hash_pin_freshness` DOC_GATES line)

Read-and-flag-only (NO patch): `.agents/workflow-overlay/**` (including
`validation-gates.md`, `skill-adoption.md`, `communication-style.md`,
`prompt-orchestration.md`), `docs/decisions/**`, `docs/workflows/**`,
`.agents/hooks/README.md`, `.claude/settings.json`, every other checker, and
everything else. Design-level problem => `NEEDS_ARCHITECTURE_PASS`, stop
patching, revert partials.

## Review emphasis (be maximally adversarial on material failure modes)
1. **Can each gate actually fire where it matters?** Attack the diff plumbing
   in all three (`GITHUB_BASE_REF`/`--base`/`origin/main` resolution, three-dot
   name-status, rename handling), the scope predicates (templates/README
   exclusions in [output-mode]; `docs/review-outputs/` bound in
   [review-summary]; the `source_captures/**/receipt.md` restriction in
   [hash-pin]), and every fail-open branch — does an infra gap ever mask a
   real finding in CI where the base is always resolvable?
2. **Bucket integrity**: findings vs INFO. [output-mode] must never gate
   multi-declaration/multi-token shapes; [review-summary] must never gate enum
   membership; confirm no code path leaks an advisory bucket into a nonzero
   `--strict` exit — and conversely that the strict buckets cannot be
   reclassified into INFO by crafted input (e.g. a forbidden key with unusual
   spacing, a `report_path` wrapped in quotes/backticks, a declaration line
   inside an HTML comment).
3. **Regex over/under-match, both directions**: [output-mode] lookbehind vs
   `receiver_output_mode`-family keys, the prose denylist, de-hyphenated token
   text; [review-summary] template-skip bypass (a real defect dressed as a
   placeholder) and its inverse (a template read as real); [hash-pin] pairing
   logic (mismatched labels, duplicate labels, hash-only lines like
   `- Compare target: sha256 ...`, table rows, truncated hex), grammar-2
   outside receipt files.
4. **Hash semantics** [hash-pin]: CRLF normalization identical to
   `check_source_input_hashes.py`; case-insensitive compare; path resolution
   (repo-root vs receipt-dir relative); the re-pinned
   `.agents/workflow-overlay/skill-adoption.md` values verify on an LF
   checkout, not only on Windows CRLF.
5. **Selftest fail-capability**: does each `--selftest` exercise the SAME
   classification path as production; can any selftest case pass while the
   production path is broken; does the [output-mode] token-drift assertion
   really parse the owning prompt-orchestration section?
6. **Wiring correctness**: CI step ordering/single-line `run:` format (a
   local runner parses `run: python .agents/hooks/...` lines — PR #815);
   CASES rows match each checker's real mode surface; the pre-push mirror
   entry cannot brick pushes on an infra gap.
7. **Non-overlap claims**: [review-summary] vs `check_review_output_provenance.py`
   (no double-governance) and [hash-pin] vs `check_source_input_hashes.py`
   (md/json partition) — confirm the docstrings' claims are true.

## Validation obligations (run; report real results; never mask failures)
- `python .agents/hooks/check_prompt_output_mode.py --selftest` ·
  `python .agents/hooks/check_review_summary.py --selftest` ·
  `python .agents/hooks/check_hash_pin_freshness.py --selftest` — all green
  with any patch applied.
- Each checker `--strict` at repo root on the lane (green) and
  `--force-internal-error --strict` (exit 1, "internal error" on stderr) /
  `--force-internal-error --audit` (exit 0).
- `python -m pytest forseti-harness/tests/unit/test_hook_internal_error_gating.py`
  — green with any patch.
- Red probes (delete after): a scratch `docs/prompts/` file with no
  output-mode line must fail [output-mode] `--check`; a scratch review output
  with a forbidden key must fail [review-summary] `--check`; a tampered pin
  hex must fail [hash-pin] `--check`.
- The report itself must pass
  `python .agents/hooks/check_review_output_provenance.py --strict <report path>`.

## Return contract (findings-first)
Findings with severity `critical`/`major`/`minor` and `confidence`, `[label]`,
neutral decision-sufficient file:line citations, `minimum_closure_condition`,
`next_authorized_action`; unified uncommitted working-tree diff with
label-tagged hunks; one overall verdict + per-surface sub-verdicts where they
differ; residual-risk note (named: forward-only scope, shape-not-truth
boundary, enum membership deliberately advisory-only pending an owner
decision, EP-11 backlog surfaced-never-gated); explicit non-findings;
`considered_and_defended` one-liners for steelman-defeated candidates; no
runtime-model recommendations; no PASS/readiness claims. End with the
adjudicator tail per `.agents/workflow-overlay/communication-style.md` ->
Review Adjudication Next Step (template:
`docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`).
