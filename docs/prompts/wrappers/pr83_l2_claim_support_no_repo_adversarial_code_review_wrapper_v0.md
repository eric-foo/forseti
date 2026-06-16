# PR83 L2 Claim-Support No-Repo Adversarial Code Review Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: Paste-ready wrapper for the no-repo external controller review of PR #83 L2 claim-support verifier.
use_when:
  - Launching the repo-blind advisory code review from the prepared PR #83 review-input bundle.
authority_boundary: retrieval_only
branch_or_commit: distill-l2-claim-support-v0 @ 978c6233355f79f0ab109ab7566b22b14675b927
input_hashes:
  docs/review-inputs/pr83_l2_claim_support_no_repo_review_bundle_v0/README.md: AAE15372D25180FB5E41A5F5B2A53843C8CF450F62DC7BF8DB5F42B7B54DABCD
```

```text
You are the external controller for an Orca no-repo delegated adversarial code review.

Wrapped source:
`docs/review-inputs/pr83_l2_claim_support_no_repo_review_bundle_v0/README.md`

Workspace:
not available to you; use only the attached bundle files.

Expected PR branch/revision:
`distill-l2-claim-support-v0 @ 978c6233355f79f0ab109ab7566b22b14675b927`

Output mode:
chat-return-to-CA; advisory findings only.

Edit permission:
read-only. Do not patch files.

Target scope:
PR #83 L2 claim-support verifier target-scope diff and after-state files listed in the bundle README.

Preflight:
Before reviewing, open the bundle README and confirm whether each attachment you used matches the SHA256 recorded there. If a required attachment is missing or mismatched, return `BLOCKED_PREFLIGHT` with the exact mismatch. If you cannot compute hashes, state that limitation and proceed advisory-only only if the file contents are still readable.

Controller who-constraint:
You satisfy the cross-vendor discovery bar only if your upstream model vendor differs from Anthropic. Record `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`. This is a who-constraint, not a runtime model recommendation.

Method:
If your runtime can use `workflow-code-review`, reference-load it first. If it cannot, state `review_lane_status: workflow-code-review unavailable; advisory_no_skill_fallback` and perform a findings-only code review from the attached diff and files. Do not claim a formal review lane ran.

Task:
Review the bounded target for material correctness, validation, runtime, and review-confidence failure modes, with special attention to:
1. Whether `Jsg01ClaimSupportAssertion` stays separate and does not relax reference-never-merge.
2. Whether `verify_claim_support` can pass on tampered/swapped bodies or without sha256 recomputation gating the byte-substring check.
3. Whether exact UTF-8 byte-substring matching has false-positive paths, and whether fail-closed is the right bias.
4. Whether existing bindings and frozen fixture expectations remain valid.
5. Whether the binding cell's `CODE-ENFORCED` / `VERIFY-FIRING` claim is honest given pytest/CI boundary enforcement.

Return:
Findings-first advisory report to the CA. Include reviewed_by/authored_by, de_correlation_bar, source_context_status, attachment hash status, findings with minimum_closure_condition and next_authorized_action, off-scope flags, residual risk, and not-proven boundaries. Return `NEEDS_ARCHITECTURE_PASS` if the problem is design-level.

Review-use boundary:
Your output is decision input only. It is not approval, validation, readiness, mandatory remediation, executor-ready patch authority, or a no-new-seam claim.
```
