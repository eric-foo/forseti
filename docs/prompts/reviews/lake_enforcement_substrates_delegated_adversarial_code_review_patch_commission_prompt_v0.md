# Lake Enforcement Substrates — Delegated Adversarial Code Review-And-Patch Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact (delegated review-and-patch commission)
scope: >
  Commission prompt for the de-correlated adversarial code review-and-patch of
  the two Bronze-lake enforcement substrates (no-new-core-field gate +
  full-GT claim tripwire) on lane claude/lake-enforcement-substrates.
use_when:
  - Dispatching the delegated review of the lake-enforcement-substrates lane.
  - Adjudicating the return (this prompt binds the return contract).
authority_boundary: retrieval_only
```

Operator paste-instruction (who-constraint, not a model recommendation): the
author and adjudicator is Anthropic/Claude; paste the body below into a
different-family controller with repo access. Same-family defeats
de-correlation. Record the actual controller in the report's `reviewed_by`.

---

# Adversarial Delegated Code Review-And-Patch: Lake Enforcement Substrates

You are the de-correlated CONTROLLER under
`.agents/workflow-overlay/delegated-review-patch.md`
(`delegated_code_review_and_patch`, `access: repo`, base-subagent). Review and
patch directly in your working tree; do NOT commit; the commissioning Chief
Architect adjudicates every hunk before anything is kept.

**Goal (executor target + axis to attack, not a pass bar):** these two
substrates claim to convert two doctrine-tier rules into deterministic,
fail-capable code enforcement — (1) lake-core schema field sets cannot drift
without a cited owner decision, and (2) new unballasted "full God Tier" claim
language cannot land outside the claim-owning surfaces. Attack exactly that:
a checker that cannot fire, a pin that pins the wrong surface, an allowlist or
ballast hole that lets real inflation through, or a false-positive shape that
would train operators to ack reflexively.

## Preflight (verify before review)
- Repo: https://github.com/eric-foo/orca ; branch `claude/lake-enforcement-substrates`
  (base `origin/main` @ `2e542c8c`); expected head: the lane PR's current head
  — clean tree required; mismatch => STOP with the blocker.
- Required reads first: `AGENTS.md`; `.agents/workflow-overlay/README.md`;
  `.agents/workflow-overlay/delegated-review-patch.md`; the write-boundary
  contract's No-New-Core-Field Enforcement section
  (`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md`);
  the Bronze full-GT declaration's Erosion Guards
  (`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md`).
- repo_map_decision: not_needed (targets exhaustive below). Edit permission:
  patch-only inside the named set. Output mode: review-report; write the
  durable report at
  `docs/review-outputs/lake_enforcement_substrates_delegated_adversarial_code_review_v0.md`
  with a valid retrieval header, non-blank `reviewed_by:` (your model+version),
  `authored_by: Anthropic Claude (Fable 5)`, and a `review_use_boundary:`
  stating findings are decision input and not approval, validation, readiness,
  mandatory remediation, or patch authority.
- External-source boundary: `jb` and installed skills are not Orca authority.

## Method (Source-Gated Method Contract)
1. REFERENCE-LOAD `workflow-deep-thinking` then `workflow-code-review`; do not APPLY yet.
2. SOURCE-LOAD: `git diff origin/main...HEAD`, every named file in full, the
   two rule-authority sections above.
3. Declare SOURCE_CONTEXT_READY, then APPLY.

## Patchable named file set (CANNOT widen; label every finding/hunk)
- [core-field-gate] `orca-harness/tests/contract/test_data_lake_core_field_gate.py`
- [claim-checker] `.agents/hooks/check_full_gt_claims.py`
- [ci-wiring] `.github/workflows/ci.yml` (only the new tripwire step)
- [map-note] `docs/workflows/orca_repo_map_v0.md` (only the new Active Hooks block; commit-once-whole file — flag preferred over patch)

Read-and-flag-only (NO patch): `source_capture/models.py`, `data_lake/`
modules, the two rule-authority contracts, `.claude/settings.json` (hook
registration is owner-gated and deliberately absent from this lane),
everything else. Design-level problem => `NEEDS_ARCHITECTURE_PASS`, stop
patching, revert partials.

## Review emphasis (be maximally adversarial on material failure modes)
1. **Can the tripwire actually fire where it matters?** Attack the diff
   plumbing (`base...HEAD` three-dot, `-U0` hunk parsing, rename handling,
   line-number computation), the scope rule (added lines only; untracked files
   NOT scanned by `--changed` — is that hole acceptable or a real bypass at
   the CI boundary given PRs always commit?), and the fail-open branch (does
   an infra gap ever mask a real finding in CI where fetch-depth is 0?).
2. **Allowlist/ballast holes both directions**: (a) inflation that passes —
   e.g. ballast words in unrelated clauses ("this is not about X. Bronze is
   full God Tier"), allowlisted families where an unbounded claim would still
   be wrong; (b) false positives that would burn trust — legitimate bounded
   claims the ballast list misses.
3. **Pin correctness**: do the six pins actually bind the lake-core surface
   (live classes, not copies; manifest bytes vs model fields both pinned)?
   Can a new source-family payload field land anywhere the contract names
   without failing a pin (e.g. nested structures: `posture_summary`,
   `replay_version_pins`, slice `metric_observations`)? Is the promotion-rule
   failure message accurate to the contract?
4. **Fail-capability of the selftest**: does `--selftest` exercise the SAME
   classification path as production; can any selftest case pass while the
   production path is broken?
5. **Silent interaction with the running marker lane**: task_75586675 updates
   `catalog.py`'s baseline marker strings — confirm nothing in this diff
   collides or double-governs that surface.
6. **CI step correctness**: step ordering, working directory, exit-code
   semantics; `GITHUB_BASE_REF` resolution on PRs from branches.

## Validation obligations (run; report real results; never mask failures)
- From `orca-harness/` with `ORCA_DATA_ROOT` UNSET: `python -m pytest` — must
  stay green with any patch.
- `python .agents/hooks/check_full_gt_claims.py --selftest` and a red probe:
  a scratch non-allowlisted `.md` with an unballasted claim must fail
  `--strict` whole-file mode (delete the probe after).
- The report itself must pass
  `python .agents/hooks/check_review_output_provenance.py --strict <report path>`.

## Return contract (findings-first)
Findings with severity `critical`/`major`/`minor`, `[label]`, neutral
decision-sufficient file:line citations, `minimum_closure_condition`,
`next_authorized_action`; unified uncommitted working-tree diff with
label-tagged hunks; one overall verdict + per-surface sub-verdicts where they
differ; residual-risk note (named: forward-only scope, no retroactive
validation, shape-not-truth boundary, hook registration owner-gated); explicit
non-findings; no runtime-model recommendations; no PASS/readiness claims. End
with the adjudicator tail per `.agents/workflow-overlay/communication-style.md`
-> Review Adjudication Next Step (template:
`docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`).
