# Corpus Intake Contract — No-Repo Adversarial Artifact Review Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: Paste-ready wrapper for the no-repo external controller adversarial artifact review of the PROPOSED standing-capture / Corpus Intake obligation contract (PR #112).
use_when:
  - Launching the repo-blind cross-vendor advisory artifact review from the prepared corpus-intake review-input bundle.
authority_boundary: retrieval_only
branch_or_commit: standing-capture-corpus-intake-contract-v0 @ bf69d3bc
input_hashes:
  docs/review-inputs/corpus_intake_contract_no_repo_adversarial_artifact_review_bundle_v0/README.md: d729e083d59b9953d83d09a518c9e70cb44ffee28b8b6ef562ea7dc9fbf9583f
  target/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md: 2e3d03bb4b6f964700c1a4439bcec752e7bef5676d906c0b117f9f02dfd30ee5
```

```text
You are the external controller for an Orca no-repo delegated adversarial ARTIFACT review.

Wrapped source (read and execute it — it is self-contained):
`docs/review-inputs/corpus_intake_contract_no_repo_adversarial_artifact_review_bundle_v0/README.md`
plus its attachment `target/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md`.
The README carries the PORTABLE METHOD, the authority excerpts the target must conform to, the
fitness reference, the highest-value checks, and the output contract. You need nothing else — no
repo, no skills, no overlay. If you cannot open the in-bundle files, ask for the PORTABLE METHOD
block and authority excerpts to be inlined.

Workspace:
not available to you; use only the attached bundle files.

Expected target PR branch/revision:
`standing-capture-corpus-intake-contract-v0 @ bf69d3bc` (PR #112). Base `origin/main @ f883b68e`.

Output mode:
chat-return-to-CA; advisory findings only.

Edit permission:
read-only. Do NOT patch files. (no_repo mode: you return findings; the CA applies accepted changes
within the single target file and runs a bounded same-vendor post-patch recheck before keep.)

Target scope:
the single file `target/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md` only.
Everything else named in the README's Authority Excerpts is flag-only context, not an edit target.

Preflight:
Before reviewing, confirm the target attachment matches SHA256
`2e3d03bb4b6f964700c1a4439bcec752e7bef5676d906c0b117f9f02dfd30ee5`. If it is missing or mismatched,
return `BLOCKED_PREFLIGHT` with the exact mismatch. If you cannot compute hashes, state that and
proceed advisory-only only if the content is readable.

Controller who-constraint:
You satisfy the cross-vendor discovery bar only if your upstream model vendor differs from Anthropic
(the target's author is Anthropic/Claude). Record `de_correlation_bar: cross_vendor_discovery |
same_vendor_sanity | self_fallback`. This is a who-constraint, not a runtime model recommendation.

Method:
Follow the PORTABLE METHOD in the bundle README exactly (reasoning-before-findings; maximally
adversarial within the named target). If your runtime can use `workflow-adversarial-artifact-review`,
reference-load it first and say so; if not, state `review_lane_status:
workflow-adversarial-artifact-review unavailable; advisory_no_skill_fallback` and do not claim a
formal review lane ran.

Task:
Adversarially review the bounded target for material, decision-relevant failure modes, using the
README's Highest-Value Checks (sibling-vs-amendment coherence; rebind-gate airtightness; never-a-feed
enforceability; INV-1 no-scoring; charter-gate vs free-floating; standing-registry deconfliction;
layer collision with Candidate URL Intake / v0 rebind; scope discipline over/under; inheritance
honesty; proposal-status honesty). Treat the fitness reference as an axis to ATTACK, not a
pass-if-matches bar; if no checkable success bar is bound, name `no checkable success bar bound`.

Return:
Findings-first advisory report to the CA per the README Output Contract. Include reviewed_by /
authored_by, de_correlation_bar, source_context_status, review_lane_status, attachment hash status,
the review_summary YAML, then findings (critical → major → minor) each with location, evidence
(target section + conflicting authority excerpt), impact, minimum_closure_condition,
next_authorized_action, and advisory remediation direction; plus off-scope flags, residual risk, and
not-proven boundaries. Return `NEEDS_ARCHITECTURE_PASS` if the problem is design-level.

Review-use boundary:
Your output is decision input only. It is not approval, validation, readiness, mandatory remediation,
executor-ready patch authority, or a no-new-seam claim. The contract under review is
PROPOSED_NOT_RATIFIED; your review is one input to the owner's ratification decision.
```
