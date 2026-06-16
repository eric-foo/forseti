# PR83 L2 Claim-Support No-Repo Adversarial Code Review Bundle v0

```yaml
retrieval_header_version: 1
artifact_role: Review input
scope: No-repo delegated adversarial code review package for PR #83 L2 claim-support verifier.
use_when:
  - Commissioning the repo-blind cross-vendor advisory review of PR #83.
  - Rechecking the exact target attachments and hashes supplied to the external controller.
authority_boundary: retrieval_only
branch_or_commit: distill-l2-claim-support-v0 @ 978c6233355f79f0ab109ab7566b22b14675b927
input_hashes:
  pr83_target_scope.diff: 77FCB32F7E9AFE6115CB0ADDB59817686CFB010EAB71D1DF2F6F58D42C72E4E1
  pr83_full_changed_files.txt: 7AB2C74F393686C377E24C4A917A75EBA81AA033FD5C60CA74901EF854AD680B
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: read-only for delegate; CA patch-only after adjudication
  target_scope: PR #83 target-scope diff and after-state files listed below
  dirty_state_checked: yes
  blocked_if_missing: target attachment hash mismatch, wrong PR branch, missing bounded-scope contract
```

Workspace preflight observed by package assembler:

- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- package assembler branch: `ecr-sp3-timing-deriver-slice1`
- package assembler HEAD: `aed85c4d012bea648e601403f865595f1013b4ea`
- PR branch: `distill-l2-claim-support-v0`
- PR branch HEAD: `978c6233355f79f0ab109ab7566b22b14675b927`
- base branch observed: `origin/main`
- base branch HEAD observed: `96eb1ad1142b0f1fc87171e8f89332dde589f0e6`
- merge-base observed: `4947b2cbd9a7ea33b4808ba1cc8b96e396db4ac4`
- dirty-state allowance: unrelated dirty/untracked files exist in the assembler worktree; review target material is generated from pinned git revisions, not from the dirty worktree.

## Cynefin Routing

Smallest complete outcome: produce a no-repo advisory review package and wrapper for the external controller; do not review, patch, adjudicate, or claim readiness here.

Regime: Complicated.

Why: The task is bounded and source-backed, but it crosses review authority, prompt orchestration, no-repo packaging, and de-correlation constraints.

Decomposition: Layer-based: bind overlay contract, package target evidence, then route to advisory code review.

Current bottleneck: The external controller can only review the files attached here.

Riskiest assumption: A code review lane can be approximated from attachments when the external controller lacks Orca repo and skill access.

Stop or pivot condition: If the controller cannot read the attachments or cannot confirm their hashes, it must return a blocked advisory result rather than reviewing a substitute source.

Allowed next move: External controller performs advisory findings-only code review from this bundle and returns findings to the CA.

Disallowed next move: External controller patches files, widens scope, claims formal PASS/readiness, or treats the review as a no-new-seam discovery claim after CA patching.

## Commission Binding

- overlay_status: provisional commission-only; not a bound formal review lane.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- review_lane: code review posture, using `workflow-code-review` if available in the receiving runtime.
- access: `no_repo`; delegate is advisory-only and must not patch.
- mode: base-subagent.
- author_home_model_family: Anthropic / Claude, as supplied by CA.
- controller_model_family: non-Anthropic vendor, operator/tooling supplied.
- current_receiving_actor_role: controller once this bundle is handed off.
- dispatch_mode: external-controller-courier.
- de_correlation_status: satisfied only if the actual controller vendor differs from Anthropic; otherwise record `self_fallback` or `same_vendor_sanity` and do not claim cross-vendor discovery.

No runtime model is recommended, ranked, or selected by this package. The family field is a who-constraint only.

## Review Target

Primary attachment:

- `pr83_target_scope.diff`
  - SHA256: `77FCB32F7E9AFE6115CB0ADDB59817686CFB010EAB71D1DF2F6F58D42C72E4E1`
  - content: target-scope diff only.

After-state file attachments:

- `after/orca-harness/evidence_binding/models.py`
  - SHA256: `C280BC9CB1A95B555275A0F63B82137F85EFB3F49937EACBBD70AD40CC2275D4`
- `after/orca-harness/evidence_binding/verifier.py`
  - SHA256: `78BB268D46E1C512AD6C81FCBE2ADA970C020369271EBA69DDDEB0424EF036E2`
- `after/orca-harness/evidence_binding/__init__.py`
  - SHA256: `9F13B7FE84DB40C5B918B2E417F617020833E3D62B2C7CC459F409E735B33F8D`
- `after/orca-harness/tests/unit/test_claim_support_verifier.py`
  - SHA256: `6F45828479793A3D1DAF66E6DB8CF5A7CAEF9E3DC03AE43907FBFBAD7222D848`
- `after/docs/decisions/distillation_binding_judgment_spine_v0.md`
  - SHA256: `788A847A0B8C0D09D36714A21E4F46714499FA87B32D47AA11A1F2D79C8A35BA`

Changed-file manifest:

- `pr83_full_changed_files.txt`
  - SHA256: `7AB2C74F393686C377E24C4A917A75EBA81AA033FD5C60CA74901EF854AD680B`
  - purpose: reveals that the PR branch contains one off-target added file.

## Bounded Scope

Editable scope for any later CA-applied patch:

- `orca-harness/evidence_binding/models.py`
- `orca-harness/evidence_binding/verifier.py`
- `orca-harness/evidence_binding/__init__.py`
- `orca-harness/tests/unit/test_claim_support_verifier.py`
- only the GUARD claim-support-span-in-body cell in `docs/decisions/distillation_binding_judgment_spine_v0.md`

Off-scope, flag-only:

- `docs/decisions/distillation_held_lessons_beautypie_pilot_v0.md`, present in the full PR changed-file list but excluded from this bounded review target.
- `case_models.py` including `EvidenceUnit` and `FacilitatorLedger`.
- `Jsg01EvidenceBinding`'s existing three-key binding shape, except where the new separate assertion could relax it.
- Frozen Beauty Pie fixture material.
- All other overlay, canonical, generated, hash-pinned, external, installed, user-level, and plugin sources.

## Highest-Value Checks

1. Does `Jsg01ClaimSupportAssertion` genuinely avoid relaxing reference-never-merge by staying a separate record rather than laundering content into `Jsg01EvidenceBinding`?
2. Can `verify_claim_support` pass on a tampered or swapped body, or be satisfied without the sha256 recomputation gating the byte-substring check?
3. Are there false-positive paths in the exact UTF-8 byte-substring match? Is fail-closed the right integrity bias?
4. Does the additive/optional field leave the frozen fixture and existing bindings valid?
5. Is the binding cell's `CODE-ENFORCED` / `VERIFY-FIRING` claim honest, given enforcement is at the CI/pytest boundary and not a write-time assembly runner?

## Review Method For Controller

If your runtime can use `workflow-code-review`, reference-load it first, then source-load only the attachments in this bundle. Do not apply the method until you have declared `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.

If `workflow-code-review` is unavailable, continue only as an advisory findings-only code review from the attached diff and after-state files. State `review_lane_status: workflow-code-review unavailable; advisory_no_skill_fallback` in your output. Do not claim a formal review lane ran.

Findings must be correctness, validation, runtime, or review-confidence issues supported by the attached source. Do not emit executor-ready patch steps. Advisory remediation direction is allowed.

## Output Contract

Return findings in chat to the commissioning CA. Include:

- `reviewed_by`: actual model and version if known; otherwise `unrecorded`.
- `authored_by`: `Anthropic Claude / exact model unrecorded`, unless the operator supplies a more exact value.
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`.
- `source_context_status`: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- attachment hash confirmation status for every attachment you used.
- findings ordered by materiality.
- for each finding: location, evidence from attachment, impact, minimum_closure_condition, next_authorized_action, and advisory remediation direction.
- explicit off-scope flags, if any.
- residual risk and not-proven boundaries.

Use `NEEDS_ARCHITECTURE_PASS` if the problem is design-level rather than patch-level. If you use it, stop at findings and do not propose a patch.

## Non-Claims

This package is not validation, readiness, formal PASS, proof that the review ran, a no-new-seam claim, patch authorization for the external controller, or a runtime model recommendation. In no-repo mode, the controller returns findings only; the CA applies any accepted patch and a bounded same-family post-patch recheck is required before keep.
