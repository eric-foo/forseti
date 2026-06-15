# Corpus Intake (Standing-Capture) Obligation Contract — Cross-Vendor Adversarial Review + CA Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (cross-vendor adversarial artifact review + home-model adjudication record)
scope: >
  Records the no_repo cross-vendor adversarial artifact review of the PROPOSED standing-capture /
  Corpus Intake obligation contract (PR #112) and the CA's home-model adjudication of its 5 findings.
  Decision input only — not validation, readiness, ratification, or a formal review-lane verdict.
authority_boundary: retrieval_only
branch_or_commit: standing-capture-corpus-intake-contract-v0 (target reviewed @ bf69d3bc)
reviewed_by: GPT-5 Codex, OpenAI (exact runtime version unrecorded)
authored_by: claude-opus-4.8, Anthropic/Claude
de_correlation_bar: cross_vendor_discovery
use_when:
  - Checking how the cross-vendor review of the corpus-intake contract was adjudicated and what was kept.
  - Tracing the R1 hardening patches on the contract back to their review findings.
stale_if:
  - The contract is re-reviewed, materially re-patched, or ratified.
  - A finding's adjudication is reopened by the owner.
```

## Commission

- Lane: delegated review-and-patch (`provisional_opt_in`), operating contract `.agents/workflow-overlay/delegated-review-patch.md`; access `no_repo`; mode base-subagent; review lane adversarial artifact.
- Target: `docs/product/data_capture_spine/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md` @ `bf69d3bc`, attachment SHA256 `2e3d03bb…` — reviewer confirmed **MATCH**.
- Bundle/wrapper: `docs/review-inputs/corpus_intake_contract_no_repo_adversarial_artifact_review_bundle_v0/` + `docs/prompts/wrappers/corpus_intake_contract_no_repo_adversarial_artifact_review_wrapper_v0.md`.
- Provenance: `reviewed_by: GPT-5 Codex / OpenAI` (cross_vendor_discovery); `authored_by: claude-opus-4.8`. Source context: bundle-only; repo/revision not independently verified in no_repo (expected).

## Reviewer verdict (verbatim summary)

```yaml
review_summary:
  status: review_complete
  recommendation: NEEDS_ARCHITECTURE_PASS before ratification; strong boundary language but two highest-risk gates left non-checkable.
  findings_count: 5
  blocking_findings:
    - "AR-01 critical: S5 does not bind a checkable rebind operation, leaving an evidence-by-stealth path."
    - "AR-02 major: S7 is mostly declarative and does not structurally prevent feed-shaped use."
    - "AR-03 major: S1 replaces Ob.1 with an approved charter but leaves approval/record/version authority open."
    - "AR-04 major: the pressure-test requirement has no checkable success bar bound."
    - "AR-05 major: S3's same-entrypoint requirement smuggles future runtime architecture into an obligation contract."
```

## CA adjudication (claims to adjudicate, not premises to inherit)

**Overall:** all 5 findings **accepted as legitimate** — the cross-vendor pass earned its keep, AR-05 most of all (the "same entrypoint" clause was imported from the company-aggregate decision's trigger-agnostic-entrypoint hedge and genuinely overreaches as runtime architecture inside an obligation contract). **The blanket `NEEDS_ARCHITECTURE_PASS` verdict is NOT accepted:** the contract's gates exist; four findings are checkability/crispness gaps (patchable tightening) and one (AR-05) is a scope-reduction. CA-adjudicated remedy = **a bounded R1 patch round within the single target file**, not a redesign. The one genuinely-downstream item (the ECR-side *field representation* of rebind provenance) stays correctly deferred, because defining ECR fields is a forbidden capture output.

| Finding | Verdict | Remedy kept |
| --- | --- | --- |
| **AR-01** (S5 rebind not checkable) | **Accept; remedy modified** (patch, not architecture pass) | S5 now binds a **checkable rebind gate** (a Decision Frame + a v0 Ob.1–16 re-discharge for the rebound/recaptured observation + an auditable corpus→evidence provenance link; absent any one → stays substrate). "Rebound" explicitly is **not a status label**; a standing row **never hands off to ECR directly**. ECR field representation stays a deferred knob; the gate *condition* is bound. |
| **AR-02** (S7 declarative, not structural) | **Accept** | S7 gains a **behavioral boundary**: corpus-derived material reaches any consumer only wrapped in a calibrated decision with an action ceiling; periodic raw-series delivery / dashboard / alert subscription / trend stream / market-monitoring view is barred *by behavior, regardless of naming*. |
| **AR-03** (S1 charter authority open) | **Accept** | S1 now binds the charter as a **gate, not a description**: approval is **owner-gated**, the charter is a **versioned artifact proving authorization**, changes require a revision, and capture **has not started / must stop** with no current approved charter. Exact record *format* stays a knob. |
| **AR-04** (no checkable success bar) | **Accept** | The Pressure-Test section binds **per-obligation closure criteria** (observed-evidence pass conditions for S1/S2/S4/S5/S6/S7; a failed test blocks any hardening claim; "reviewed examples" are not pressure-test evidence). |
| **AR-05** (S3 smuggles runtime architecture) | **Accept; strongest catch** | S3's "must be structured so … the same entrypoint without re-architecting" is **removed** as an obligation and demoted to a clearly-labeled **non-binding future-compatibility note**; S3 now states the contract specifies **no** runtime/scheduler/entrypoint/interface shape, keeping it to cadence facts + caps + stop + manual-shortfall visibility. |

**Rejected/modified claims:** the reviewer's overall `NEEDS_ARCHITECTURE_PASS` framing is **modified to a bounded patch round** (per the above). No finding was rejected on substance.

## What was kept (final state)

The contract remains `PROPOSED_NOT_RATIFIED`. Seven edits applied to the single target file (S1, S3, S5, S7, the Pressure-Test section, one Open Design Knob, and a Status R1-hardening note). No other file touched; off-scope authorities (v0 contract, Candidate URL Intake, company-aggregate decision, discovery charter, buyer-proof, overlay) were flag-only and unedited.

## Post-patch recheck (bounded; same-vendor sanity)

- `de_correlation_bar` for the recheck: **`same_vendor_sanity`** (the CA, Anthropic, verified its own patches; this is bounded verification, **not** a cross-vendor discovery / no-new-seam claim).
- Result: each finding's closure condition is met by its patch; the touched delta introduced no new blocker/major (changes are additive tightening + one scope reduction, each consistent with the contract's existing no-runtime-design / INV-1 / never-a-feed / rebind boundaries).

## Residual risk / not-proven

- The contract is still a **proposal**; this hardening does **not** ratify it. Ratification is owner-gated and remains pending (and is gated behind sibling PR #106 landing).
- The cross-vendor pass ran `no_repo` on the bundle only; it did not independently verify the PR branch/base or any off-bundle authority — those were carried in as embedded excerpts.
- The closure criteria (AR-04) are now bound but **not yet exercised**: the contract is not pressure-tested. No hardening is claimed.
- A novel cross-vendor-shared blind spot absent from both passes remains bounded-but-nonzero (the standard `no_repo` + same-vendor-recheck residual).

## operator_closeout_source

```yaml
operator_closeout_source:
  what_ran: cross-vendor (OpenAI GPT-5 Codex) no_repo adversarial artifact review of PR #112's corpus-intake contract proposal.
  reviewer_verdict: NEEDS_ARCHITECTURE_PASS, 5 findings (1 critical, 4 major).
  ca_adjudication: all 5 accepted; verdict downgraded to a bounded patch round (gates existed; gaps were checkability + one scope overreach).
  applied: 7 edits to the single target file (S1 owner-gated charter gate; S3 runtime-architecture overreach removed; S5 checkable rebind gate; S7 behavioral never-a-feed boundary; pressure-test closure criteria; open-knob clarification; Status R1 note).
  recheck: same_vendor_sanity bounded recheck passed; no new blocker/major; patches kept.
  final_state: contract remains PROPOSED_NOT_RATIFIED, now R1-hardened; committed to PR #112.
  blocked_next_step: owner ratification (gated behind PR #106 landing); pressure-testing not yet run.
  not_claimed: validation, readiness, ratification, no-new-seam, pressure-test pass, propagation.
```

## Non-Claims

This record is decision input only. It is not validation, readiness, ratification, formal review-lane `PASS`, a no-new-seam claim, patch authority beyond the bounded CA application recorded here, or runtime model routing. The contract it reviews remains `PROPOSED_NOT_RATIFIED`.
