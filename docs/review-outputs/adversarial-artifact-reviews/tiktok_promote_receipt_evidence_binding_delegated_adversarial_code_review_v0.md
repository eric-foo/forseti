# TikTok PROMOTE Receipt-Evidence Binding -- Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review output (delegated_code_review_and_patch sibling mode)
scope: >
  Cross-vendor delegated adversarial code review and bounded patch result for
  the four-file TikTok PROMOTE receipt-evidence binding on draft PR #849,
  commissioned by docs/prompts/reviews/tiktok_promote_receipt_evidence_binding_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md.
use_when:
  - Adjudicating this delegated review's findings and the one applied test patch before keeping any change.
  - Checking whether PR #849's four target files were independently reviewed and what residual risk remains.
authority_boundary: retrieval_only
branch_or_commit: codex/promote-receipt-evidence-binding @ 4721a76bdd38659dd02db50d68e2884b820701d3 (implementation commit) plus commission-prompt filing 6a53b6c557bfab07e31d6dd09ea638b4f96daa7d
```

## Review Summary

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/tiktok_promote_receipt_evidence_binding_delegated_adversarial_code_review_v0.md
  recommendation: accept_with_friction
  reviewed_by: claude-sonnet-5
  authored_by: openai-gpt-family (exact version unrecorded; commission-declared family only)
  summary: "Four target files correctly implement the claimed PROMOTE receipt-evidence binding and fail closed on every adversarial seam probed; one test-coverage gap was found and closed by this review's patch, and one major out-of-scope reachability gap (no shipped caller supplies a resolver) is flagged for separate Chief Architect routing."
  findings_count: 3
  blocking_findings: []
  advisory_findings:
    - CR-01: PROMOTE receipt-evidence gate is currently unreachable end-to-end via every shipped write path (major, out-of-scope to patch here)
    - CR-02: new promote_requires_candidate_node branch had zero regression-test coverage (minor, closed by this review's patch)
    - CR-03: Creator Registry receipt wrapper/registry_source accept unrecognized keys (minor, optional hardening only)
  prior_findings_remediated: []
  next_action: "Chief Architect adjudicates CR-01/CR-02/CR-03 and this review's one test-only patch; if kept, land the patch (commit/push/PR) as one batched step, then route CR-01 to a separate commission scoped to register_lake_writer.py and run_tiktok_creator_discovery_register.py."
```

## De-correlation Receipt

```yaml
de_correlation_receipt:
  author_model_family: OpenAI GPT-family
  home_adjudicator_family: OpenAI GPT-family
  controller_model_identity: claude-sonnet-5 (Claude Sonnet 5, Anthropic)
  controller_vendor_lineage: Anthropic
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: cross_vendor_discovery
```

## Repository And Revision Gate

- Repository: `https://github.com/eric-foo/forseti` (worktree: `C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\promote-receipt-evidence-binding`)
- Branch: `codex/promote-receipt-evidence-binding`, working tree clean at intake
- HEAD at intake: `6a53b6c557bfab07e31d6dd09ea638b4f96daa7d` (commission-prompt filing on top of the implementation commit) -- matches the allowed pre-review branch state exactly
- Pinned target-file SHA-256 values: all four matched the commission's pinned hashes against on-disk worktree bytes. (An initial `git show <rev>:<path> | sha256sum` comparison mismatched due to `core.autocrlf=true` LF->CRLF checkout conversion, not real drift; direct on-disk `sha256sum` of the checked-out files matched the pinned values exactly for all four files.)
- `BLOCKED_SOURCE_DRIFT`: not triggered.

## Source Context

```yaml
source_context_status: SOURCE_CONTEXT_READY
source_read_ledger:
  - file: forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py
    why: target file, full read
    status: clean, matches pinned hash
  - file: forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py
    why: target file, full read (current file + isolated diff hunks)
    status: clean, matches pinned hash
  - file: forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py
    why: target file, full read (diff + helper functions + surrounding context)
    status: clean before patch; patched (see Patch Summary)
  - file: forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md
    why: target file, full diff read (PROMOTE Receipt-Evidence Binding section + DCP receipt)
    status: clean, matches pinned hash
  - file: forseti-harness/capture_spine/creator_profile_current/registry_match_preflight.py
    why: read-only source; the wrapper key/schema-version constants imported by validation.py, and the real receipt-row shape (to check builder-compatible evolution)
    status: clean, unmodified
  - file: forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
    why: read-only source; controlling usage contract for candidate clearance fields and non-claims
    status: clean, unmodified
  - file: forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_writer.py
    why: read-only; confirms the builder never emits frontier_decisions (always [])
    status: clean, unmodified
  - file: forseti-harness/capture_spine/tiktok_creator_discovery_frontier/frontier_selector.py
    why: read-only; confirms this is a pure advisory reader, no validator call
    status: clean, unmodified
  - file: forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py
    why: read-only; the only shipped lake-write caller of validate_tiktok_creator_discovery_frontier_register
    status: clean, unmodified
  - file: forseti-harness/runners/run_tiktok_creator_discovery_register.py
    why: read-only; the only shipped CLI entry point into the builder + lake writer
    status: clean, unmodified
  - overlay_files_read:
      - AGENTS.md
      - .agents/workflow-overlay/README.md
      - .agents/workflow-overlay/decision-routing.md
      - .agents/workflow-overlay/source-loading.md
      - .agents/workflow-overlay/source-of-truth.md
      - .agents/workflow-overlay/prompt-orchestration.md
      - .agents/workflow-overlay/review-lanes.md
      - .agents/workflow-overlay/delegated-review-patch.md
      - .agents/workflow-overlay/validation-gates.md
      - .agents/workflow-overlay/safety-rules.md
      - .agents/workflow-overlay/retrieval-metadata.md
      - .agents/workflow-overlay/communication-style.md
  - full_diff_read: origin/main...4721a76bdd38659dd02db50d68e2884b820701d3 (all four target files, hunk-by-hunk)
source_gaps: none material to the commissioned target
excluded_sources:
  - docs/workflows/creator_onboarding_first_batch_next_material_steps_handoff_v0.md (named read-only-flag-only; consumed checkpoint, orientation only per commission)
  - docs/prompts/reviews/tiktok_promote_receipt_evidence_binding_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md (the commission itself, read as the operating instruction, not re-cited as source authority)
```

## Commission And Contract-Impact Map (As Claimed)

The commission summarized the implementation as making every `promote`
decision depend on candidate-bound Creator Registry preflight receipt
evidence, with the legacy scalar status demoted to informational-only, and a
caller-supplied resolver required to verify exact receipt bytes. This review
judged that claim against current source rather than trusting the summary;
the source-read findings below confirm the claim is accurate for the four
target files' internal logic, with one material caveat (Finding CR-01) about
whether any shipped caller can actually exercise the gate end-to-end.

## Review Scope

- In scope (patchable): the four named target files.
- Read-only / flag-only: every other file, including
  `register_lake_writer.py`, `run_tiktok_creator_discovery_register.py`,
  `register_writer.py`, `frontier_selector.py`, and
  `registry_match_preflight.py`. Findings about these files are flags only,
  not patches.
- Review method: `workflow-code-review` under the
  `delegated_code_review_and_patch` sibling mode, with `workflow-deep-thinking`
  applied first per the Review Prompt Defaults escalation trigger (commissioned,
  adversarial, patch-authorized).

## Findings

### CR-01 -- PROMOTE receipt-evidence gate is currently unreachable end-to-end via every shipped write path

- severity: major
- confidence: high
- verdict: CONFIRMED
- file/line: `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py:46` (read-only); `forseti-harness/runners/run_tiktok_creator_discovery_register.py:82-103` (read-only)
- implementation evidence: `write_tiktok_creator_discovery_frontier_register` calls `validate_tiktok_creator_discovery_frontier_register(register)` with no `preflight_receipt_resolver` argument, so the parameter defaults to `None`. A repo-wide search (`rg "preflight_receipt_resolver|validate_tiktok_creator_discovery_frontier_register"` across `forseti-harness/`) found no other caller of the validator besides `register_writer.py` (also resolver-less), the test file, and the validator's own definition. `register_writer.py`'s `build_tiktok_creator_discovery_frontier_register` always emits `"frontier_decisions": []`, so no shipped builder path ever produces a PROMOTE decision either.
- authority / evidence basis: the product contract itself (`tiktok_creator_discovery_frontier_register_v0.md`, "PROMOTE Receipt-Evidence Binding"): "The validator does not guess how repo or lake pointers resolve. Its caller must supply a resolver..." -- an obligation no shipped caller in this repository fulfills.
- correctness / validation impact: this is **fail-closed, not fail-open** -- `_validate_promote_registry_preflight_evidence` raises `promote_preflight_receipt_resolver_required` whenever `resolver is None` (`validation.py:865-869`), so no PROMOTE decision can be wrongly accepted. But it also means: if an operator or a future tool hand-appends a `frontier_decisions` entry with `projection_decision: promote` and fully correct, genuinely-cleared `registry_preflight_receipt_evidence_or_none` to a register JSON, and then runs it through `run_tiktok_creator_discovery_register.py --data-root ...` (the only shipped lake-write path), that **legitimate** PROMOTE will still be rejected with `promote_preflight_receipt_resolver_required`. The receipt-evidence machinery this PR adds has no live caller that can successfully exercise its success path today.
- minimum_closure_condition: either (a) a caller change threading a real repo/lake receipt resolver through `register_lake_writer.write_tiktok_creator_discovery_frontier_register` -> `validate_tiktok_creator_discovery_frontier_register`, and/or through a `--receipt-resolver`-style flag on the runner, or (b) an explicit owner decision that PROMOTE registers are validated/promoted through a different, not-yet-built tool, with that boundary named in the product contract's non-claims.
- next_authorized_action: report as a finding for Chief Architect routing. Not patchable within this commission -- `register_lake_writer.py` and `run_tiktok_creator_discovery_register.py` are outside the named target-file set (read-only / flag-only per the commission).
- red/green: not applicable -- no patch authorized for this finding's closing file(s) under this commission's scope.

### CR-02 -- New `promote_requires_candidate_node` fail-closed branch had zero regression-test coverage (closed by this review's patch)

- severity: minor
- confidence: high
- verdict: CONFIRMED (pre-patch); outcome: fixed
- file/line: `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py:650-655`
- implementation evidence: the diff adds a brand-new fail-closed check -- a PROMOTE decision must select a `tiktok_creator_candidate` node, or it raises `promote_requires_candidate_node` -- but no test in the shipped diff exercised this branch. A full read of the test file's PROMOTE test block (`test_promote_decision_without_registry_preflight_evidence_raises` through `test_non_promote_decision_without_preflight_passes`) confirmed no test ever pointed a PROMOTE decision at the RUN or SEED node.
- authority / evidence basis: commission section 5, "Test quality: ...include negative cases for each load-bearing boundary."
- correctness / validation impact: without a regression test, a future refactor of `_validate_decision` could silently drop this candidate-node-only gate with no test failing to catch it.
- minimum_closure_condition: a passing test that constructs a PROMOTE decision selecting a non-candidate node (with otherwise-valid receipt evidence attached, to isolate the node-kind check from the evidence checks) and asserts `promote_requires_candidate_node`.
- next_authorized_action: none -- closed by this review's bounded patch (see Patch Summary).
- red/green: **weaker evidence, labeled as such.** A genuine disable-and-restore red/green proof was attempted (temporarily wrapping the check in dead code to confirm the new test fails without it) but was correctly blocked by the harness's own security-test-removal guard before any edit landed (confirmed via `Grep "if False"` on `validation.py` finding no match, and via `git status --short` showing only the test file modified). In place of that proof: full-file code read confirms `promote_requires_candidate_node` is raised from exactly one call site (the guarded `if` at `validation.py:651`), and the new test passes against the current shipped implementation (`pytest` exit 0, see Validation Evidence).

### CR-03 -- Optional: Creator Registry preflight receipt wrapper/registry_source accept unrecognized keys (row-level permissiveness is correct and required)

- severity: minor
- confidence: medium
- verdict: PLAUSIBLE (as optional hardening only -- not a defect)
- file/line: `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py:715-848` (`_validate_creator_registry_preflight_receipt_wrapper`)
- implementation evidence: every other object shape this file validates (register top level, wrapper, node, edge, decision, `registry_preflight_receipt_evidence_or_none`, `root_seed`, `provenance`) calls `_reject_unknown_keys`. The new `_validate_creator_registry_preflight_receipt_wrapper` never does, for the wrapper, `registry_source`, or each result row.
- authority / evidence basis: commission section 5, "Receipt integrity: ...unknown or missing keys."
- correctness / validation impact: **not exploitable** -- no fail-open path results, since only named fields are read and cross-checked. Critically, row-level permissiveness is *required*, not merely tolerated: the real receipt rows produced by `registry_match_preflight.py`'s `_build_candidate_result` carry additional legitimate fields this validator never reads (`input_index`, `allowed_next_actions`, `action_blockers`, `matched_registry_profiles`, `duplicate_candidate_identity_keys`, `errors`). Adding row-level `_reject_unknown_keys` would break validation of genuine builder output -- confirmed directly: the test suite's own `_preflight_receipt_bytes()` helper builds receipts through the real `build_creator_registry_match_preflight_receipt` function, and those rows carry exactly these extra fields. Wrapper- and `registry_source`-level unknown-key rejection, by contrast, would not break compatibility (the builder emits exactly the required 7/5 keys at those two levels), but closes no live gap either.
- minimum_closure_condition: owner decision on whether wrapper/`registry_source` strictness is worth the added coupling to future receipt-schema evolution at those two levels only (never at row level).
- next_authorized_action: optional, non-required hardening. Not patched in this pass under smallest-complete-intervention -- there is no live gap to close.
- red/green: not applicable.

## Considered And Defended

- **Provenance vs. self-certification.** Whether a caller could manufacture a positive-looking receipt plus matching self-supplied hash/resolver and clear PROMOTE without an owner-produced, repo/lake-bound, independently verifiable provenance fact: yes, mechanically, the validator only proves internal receipt self-consistency (hash matches, schema matches, summary matches results, candidate row matches). It does not and cannot verify that `receipt_pointer` resolves to an authentic, access-controlled Creator Registry Runner Ladder output -- that trust boundary is explicitly delegated to the resolver's caller by the product contract ("Its caller must supply a resolver...") and the non-claims section ("does not prove... source truth"). This is an explicitly accepted boundary, not a silent gap -- and per CR-01, it is currently moot in practice because no shipped caller supplies a resolver at all.
- **Staleness (registry snapshot drift / receipt age).** The validator checks pointer-byte/hash drift (evidence's claimed `receipt_sha256` vs. the actually-resolved bytes) but does not check whether the receipt's `registry_source` snapshot is current relative to the live registry, nor whether `generated_at_utc` is recent. This is explicitly disclaimed by the product contract's "under that receipt's registry snapshot" scoping and the Creator Registry usage note's accepted residual ("Metric freshness is not handled here"). Contract and implementation agree on this boundary; per the commission's own instruction not to invent a freshness policy where none exists, this is not treated as a defect.
- **`registry_source.sha256` case handling.** It is validated with a case-insensitive regex (`[0-9a-fA-F]{64}`) while `evidence.receipt_sha256` is lowered before an all-lowercase check. Cosmetic asymmetry only -- both ultimately compare correctly against a lowercase `hashlib.hexdigest()` value; not exploitable.
- **Two narrow untested-but-correct branches.** The resolver returning a non-`bytes` value, and the resolved JSON document (or its wrapper) not being a `Mapping`, are both handled with an `isinstance` check plus fail-closed `_fail`, but neither has a dedicated unit test. Not selected for patching: the same defensive pattern is exercised and proven correct dozens of times elsewhere in this same file's test suite, so the incremental confidence a dedicated test would add is low relative to CR-02's genuinely novel, previously-uncovered branch.
- **Legacy `registry_preflight_status_or_none` v0-schema retention.** The product contract's additivity claim is precisely scoped to "non-PROMOTE nodes" and does not overclaim compatibility for already-promoted candidates. Since `register_writer.py` never emits a PROMOTE decision, no register persisted by shipped code today can be broken by the tightened PROMOTE gate.
- **Test design quality (positive).** `_preflight_receipt_bytes()` constructs receipts through the real `build_creator_registry_match_preflight_receipt` builder rather than a hand-rolled fake, so the suite automatically tracks real receipt-schema drift instead of validating against an idealized fixture -- this is the kind of test design the commission's "fake-pass-prone tests" question was checking for, and it holds up well.

## Patch Summary

One bounded patch was applied, inside the named target file set:

- `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py`: added
  `test_promote_decision_on_non_candidate_node_raises_even_with_valid_evidence`,
  closing CR-02. No other target file was modified. `models.py`,
  `validation.py`, and the product-contract `.md` are unchanged from the
  pinned implementation commit.

```diff
diff --git a/forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py b/forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py
index 402c52ad..95eea12e 100644
--- a/forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py
+++ b/forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py
@@ -747,6 +747,30 @@ def test_promote_decision_without_registry_preflight_evidence_raises() -> None:
     _raises_code(register, "promote_requires_registry_preflight_receipt_evidence")


+def test_promote_decision_on_non_candidate_node_raises_even_with_valid_evidence() -> None:
+    receipt_bytes = _preflight_receipt_bytes()
+    evidence = _preflight_evidence(receipt_bytes)
+    nodes = [
+        _node(_RUN_NODE_ID, FrontierNodeType.RUN, None).to_dict(),
+        _node(
+            _SEED_NODE_ID,
+            FrontierNodeType.TIKTOK_CREATOR_SEED,
+            "fragranceknowledge",
+            registry_preflight_receipt_evidence_or_none=evidence,
+        ).to_dict(),
+    ]
+    register = _register(
+        nodes=nodes,
+        edges=[],
+        frontier_decisions=[_decision(selected_node_id=_SEED_NODE_ID)],
+    )
+    _raises_code(
+        register,
+        "promote_requires_candidate_node",
+        resolver=_receipt_resolver(receipt_bytes),
+    )
+
+
 def test_promote_legacy_status_string_does_not_clear_receipt_gate() -> None:
```

No canonical, compiler-emitted, hash-pinned, or otherwise protected path was
touched. The patch remains uncommitted in the named worktree per the
commission's `dirty_state_allowance`.

## Validation Evidence

All commands run from
`C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\promote-receipt-evidence-binding`.

```yaml
validation_results:
  - command: python -m pytest -p no:cacheprovider forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py -q
    exit_code: 0
    observed: "77 passed (all tests including the new CR-02 regression test); no failures"
    bucket: GATE PASS
  - command: python .agents/hooks/check_retrieval_header.py --changed --strict
    exit_code: 0
    observed: "no header findings on changed files"
    bucket: GATE PASS
  - command: python .agents/hooks/header_index.py --strict --base origin/main
    exit_code: 0
    observed: "1 changed durable .md file(s) all have headers and are map-reachable (base: origin/main)"
    bucket: GATE PASS
  - command: python .agents/hooks/check_map_links.py --strict
    exit_code: 0
    observed: "check_map_links --strict: OK (0 findings); annotated nonresolving: 36 (debt, not failures)"
    bucket: GATE PASS
  - command: python .agents/hooks/check_dcp_receipt.py --strict
    exit_code: 0
    observed: "check_dcp_receipt --strict: OK -- every real receipt in the changed .md files is shape-valid (base: origin/main)"
    bucket: GATE PASS
  - command: git diff --check
    exit_code: 0
    observed: "no whitespace errors"
    bucket: GATE PASS
  - command: python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/tiktok_promote_receipt_evidence_binding_delegated_adversarial_code_review_v0.md
    exit_code: 0
    observed: "clean on the final write (no output); the file was changed after an earlier run flagged missing reviewed_by/authored_by and two trailing-whitespace lines, both fixed, then this command was rerun against the corrected file per the finalization-gate's rerun-and-report-final-result requirement"
    bucket: GATE PASS
not_run_checks: []
```

## Reviewer Verdict (Decision Input Only)

This verdict is decision input for the commissioning Chief Architect / home
model, not acceptance, approval, readiness, or merge authority.

- The four target files internally implement the claimed PROMOTE
  receipt-evidence binding correctly and fail closed on every adversarial seam
  probed in the commission's section 5 (provenance self-certification is
  explicitly bounded, not silently gapped; candidate binding, receipt
  integrity, and compatibility all held up under adversarial reading; one
  genuine test-coverage gap (CR-02) was found and closed).
- One material, out-of-scope finding (CR-01) means the feature this diff adds
  has no shipped caller that can exercise its success path yet -- worth
  Chief Architect routing, but it does not indicate a defect *in* the four
  target files themselves, and closing it requires editing files outside this
  commission's patch authority.
- `NEEDS_ARCHITECTURE_PASS`: not triggered for the four target files. CR-01 is
  named as a residual for separate routing, not as a reason to escalate or
  unwind this diff.

## Residual Risks, Off-Scope Flags, Not-Proven Boundaries

- Residual: CR-01 (PROMOTE gate currently unreachable via any shipped write
  path) -- off-scope to patch here; needs a caller-side change or an owner
  decision, in a separate commission.
- Residual: CR-03 (optional wrapper/registry_source key strictness) -- named,
  not required, not patched.
- Not proven: receipt authenticity/provenance beyond internal self-consistency
  (considered and defended above; explicitly non-claimed by the product
  contract).
- Not proven: registry-snapshot freshness / receipt age (considered and
  defended above; explicitly non-claimed).
- Off-scope flags: no issues found in `registry_match_preflight.py`,
  `register_writer.py`, or `frontier_selector.py` themselves during this
  read-only pass; they were read only to check compatibility and reachability
  for the target files' changes, not independently reviewed line-by-line.
- Not proven: this review does not constitute buyer-proof, product-learning,
  or judgment-quality evidence; it is a source-backed code review only.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation,
mandatory remediation, or executor-ready patch authority until separately
accepted or authorized by the commissioning Chief Architect / home model,
which must fresh-read the resulting diff before any keep decision.
