# Core Spine v0 Method Validation Case-Frame Locks Directed Adversarial Review v2

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Directed adversarial review of Core Spine v0 method-validation case-frame locks, focused on replay contamination, NEEDS_VERIFICATION propagation, portfolio bias, and authorization drift.
use_when:
  - Deciding whether the case-frame lock artifact needs targeted patches before acceptance or replay authorization.
  - Checking the directed boundary-problem analysis that was not captured by the earlier review outputs.
  - Comparing current case-frame lock risks against prior v0 and v1 review reports.
authority_boundary: retrieval_only
open_next:
  - orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_locks_v0.md
  - docs/prompts/reviews/core_spine_v0_method_validation_case_frame_locks_adversarial_review_gpt54_prompt_v0.md
input_hashes:
  docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md: B4018996BECC8F79B254BF5A113265B873DCB9C1AE35746DABADAA4D99D4A537
  docs/prompts/reviews/core_spine_v0_method_validation_case_frame_locks_adversarial_review_gpt54_prompt_v0.md: 4777DB70B96B399D97698C2B897BE78BC09C7A782BE6159029C724D43FF94775
branch_or_commit: main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c
downstream_consumers:
  - docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md
stale_if: Target artifact hash changes, the case-frame lock artifact is patched, or a later accepted review supersedes this directed review.
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v2.md
  recommendation: patch_before_acceptance
  summary: "Directed-output review found no hard blocker, but identified two high-consequence frame risks and five targeted patch areas before relying on the case-frame locks."
  findings_count: 5
  blocking_findings: []
  advisory_findings:
    - AR-01: MV-09 positive-action frame is structurally biased toward caution
    - AR-02: MV-05 provisional cutoff creates a dependency cascade that may become a blocker
    - AR-03: MV-03 and MV-05 reframe conditions are too outcome-shaped
    - AR-04: Section 10 verification checklist can be misread as replay authorization
    - AR-05: MV-01 exclusion rule names a concrete post-window product outcome
  prior_findings_remediated: []
  next_action: "Patch AR-01 through AR-05 or explicitly accept the bias and authorization risks before treating the frame locks as accepted input for evidence replay."
```

## 1. Why The Directed Output Was Not Used Earlier

The earlier durable review outputs did not use the directed boundary-problem
analysis because that analysis was added after the existing `v0` and `v1`
review reports were already present. The prior assistant turn patched the
review prompt with the directed questions, but it did not regenerate or write a
new durable review report from that directed output.

This `v2` report corrects the artifact placement problem: the directed
adversarial analysis now lives in the bound review-output folder for
method-validation adversarial reviews.

## 2. Review Target And Source-Read Ledger

Review target:

- `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`

Related review prompt:

- `docs/prompts/reviews/core_spine_v0_method_validation_case_frame_locks_adversarial_review_gpt54_prompt_v0.md`

Prior reports:

- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md`
- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v1.md`

Source state checked:

- Target artifact SHA256: `B4018996BECC8F79B254BF5A113265B873DCB9C1AE35746DABADAA4D99D4A537`
- Prompt SHA256 after directed-risk insertion: `4777DB70B96B399D97698C2B897BE78BC09C7A782BE6159029C724D43FF94775`
- Branch and HEAD: `main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c`

Dirty-state boundary:

- The workspace is dirty, and the target artifact is untracked. This report is
  anchored to the current workspace contents and target hash above, not to a
  committed revision.

## 3. Scope And Excluded Scope

In scope:

- Whether the case-frame artifact constrains replay without pre-populating it.
- Cutoff contamination and outcome-window leakage.
- `NEEDS_VERIFICATION` propagation into downstream fields.
- Reframe condition specificity.
- Portfolio imbalance and positive-action bias.
- Authorization drift from verification language and verdict wording.

Excluded:

- Evidence replay.
- External source verification.
- Judgment of whether any company made a good or bad decision.
- Source maps, source inventories, data spine, dashboards, scrapers, APIs,
  scoring systems, automation, feature planning, implementation, staging,
  commits, pushes, or PRs.

## 4. Boundary Problem Resolution

The structural line is whether a field constrains replay or populates replay.

Safe frame-lock detail constrains replay:

- cutoff dates or windows;
- source-family boundaries;
- allowed action verbs;
- evidence standards;
- post-window exclusion rules;
- result-label semantics.

Dangerous detail populates replay:

- concrete post-window product names;
- reframe paths that mirror actual outcomes;
- causal or moralized outcome language;
- remediation plans disguised as reframe conditions;
- asymmetrical threshold language that makes one result type much easier than
  another.

The artifact is mostly structurally sound, but it currently keeps several
outcome-shaped details in the frame. These are not hard blockers by themselves,
but they should be patched or explicitly accepted before the frame locks are
treated as accepted replay input.

## 5. Correctness Findings

### AR-01

MV-09 positive-action frame is structurally biased toward caution.

- Location: Section 9, `MV-09` case frame.
- Evidence: The frame defines the case around a known acquisition outcome while
  the "why later outcome was not obvious" field emphasizes accuracy,
  confidentiality, professional-duty, hallucination, workflow-fit, adoption,
  procurement, and integration risks.
- Why it matters: `MV-09` is the portfolio's positive-action case. If it starts
  with the highest convergence threshold and the richest caution-side risk
  list, the replay is structurally more likely to return `Hold`, `Probe`, or
  underconfidence even if positive action was the side the method needs to
  test.
- Next action: Rebalance the frame by stating action-side plausibility at the
  same abstraction level as caution-side risk. Keep the acquisition outcome
  excluded, and make the threshold action-type neutral: decisive capability
  capture, controlled partnership, build, license, acquire, or hold.

### AR-02

MV-05 provisional cutoff creates a dependency cascade that may become a blocker.

- Location: Section 8, `MV-05` case frame.
- Evidence: The cutoff is "Provisional cutoff of 2023-05-30" and the expected
  outcome-comparison window starts on 2023-06-01. Section 10 also says to
  "Confirm the cleanest cutoff around 2023-05-30 and separate pre-cutoff
  API-dependence evidence from June 2023 protest evidence."
- Why it matters: If verification moves the cutoff into June 2023, the
  currently stated outcome-comparison window collapses and may mix pre-cutoff
  evidence with outcome evidence. That is not a routine `NEEDS_VERIFICATION`
  gap; it can change whether `MV-05` is usable as framed.
- Next action: Mark the `MV-05` outcome-comparison window as
  `NEEDS_VERIFICATION` and state that if the cutoff cannot be pinned before
  broad third-party-app fallout, the case is blocked or must be reframed.

### AR-03

MV-03 and MV-05 reframe conditions are too outcome-shaped.

- Location: Section 6, `MV-03`, "Reframe conditions"; Section 8, `MV-05`,
  "Reframe conditions."
- Evidence: `MV-03` says the frame may shift toward "protect verified developer
  knowledge, license trusted data, and improve workflow retrieval." `MV-05`
  says the response may shift toward "segmented AI/data licensing, staged
  enforcement, moderator/tool exemptions, app transition support, or
  trust-preserving governance."
- Why it matters: These are plausible result categories, but at this level of
  specificity they read like known outcome or remediation paths. They direct a
  replay executor toward evidence for those paths rather than letting the
  replay discover the valid reframe.
- Next action: Generalize both fields to neutral move categories. For example:
  `MV-03` can say "from direct AI competition toward knowledge quality,
  data-value, or workflow-positioning strategy." `MV-05` can say "from broad API
  pricing toward segmented monetization, ecosystem protection, governance, or
  transition design."

### AR-04

Section 10 verification checklist can be misread as replay authorization.

- Location: Section 10, "Blockers And Verification Needs"; Section 12,
  "Current Verdict."
- Evidence: Section 10 says "Verification needs before evidence replay" and
  Section 12 says `ACCEPTED_CASE_FRAMES_AWAITING_EVIDENCE_REPLAY_AUTHORIZATION`.
- Why it matters: The artifact does not control replay authorization, but the
  phrase "before evidence replay" can be read as a checklist where completion
  unlocks replay. The current verdict also creates sequencing pull toward
  replay.
- Next action: Add an explicit sentence after the verification checklist:
  "Completing these verification steps does not itself authorize evidence
  replay; replay requires a separate later owner authorization." Consider
  replacing `ACCEPTED_CASE_FRAMES_AWAITING_EVIDENCE_REPLAY_AUTHORIZATION` with
  a non-acceptance verdict unless acceptance has been separately recorded.

### AR-05

MV-01 exclusion rule names a concrete post-window product outcome.

- Location: Section 5, `MV-01`, "Post-window exclusion rule."
- Evidence: The rule says to exclude "Resolution Platform material."
- Why it matters: The exclusion is directionally correct, but naming a specific
  post-window Zendesk product tells the replay reader a concrete later response
  existed. That creates unnecessary outcome awareness inside a pre-replay frame.
- Next action: Replace the specific product name with a category such as
  "post-cutoff Zendesk AI-agent, resolution, platform, acquisition, packaging,
  comparison, or response-positioning material."

## 6. Friction And Bias Notes

- `NEEDS_VERIFICATION` markers are present, but some downstream fields inherit
  those uncertainties without saying so. `MV-01` and `MV-05` outcome windows
  should inherit cutoff uncertainty. `MV-03` second-order source boundaries
  should inherit source-visibility uncertainty.
- Portfolio balance exists at the case-identity level, but the frame language
  loads caution more heavily than action. This matters commercially because the
  validation is supposed to test whether Orca can support action when evidence
  converges, not only whether it can avoid false moves.
- `MV-04` is clean on cutoff discipline, but its downgrade conditions are more
  source-discoverable than its upgrade conditions. That may be acceptable for a
  reverse case, but the asymmetry should be explicit.

## 7. Items Checked With No Hard Blocker

- The artifact does not authorize evidence replay, source maps, feature
  planning, implementation, staging, commits, pushes, or PRs in its explicit
  non-claims.
- The five locked case identities are preserved.
- The replacement rule preserves validation role rather than allowing an easy
  substitute case.
- The artifact remains structured as a frame lock, not a full case study.

## 8. Not-Proven Boundaries

- Public pre-cutoff source availability for any case is not proven.
- `NEEDS_VERIFICATION` items are unresolved.
- Case-frame acceptance is not proven by this review.
- Evidence replay is not authorized by this review.
- External willingness to pay, feature readiness, implementation readiness,
  data-spine readiness, source-map readiness, and product-market fit remain
  unproven.

## 9. Blockers Or No-Blocking-Finding Statement

No hard blocker is recorded at this stage.

Two risks are high consequence:

- `MV-09` may under-test positive-action judgment if the caution-side threshold
  remains structurally heavier than the action-side frame.
- `MV-05` may become blocked if the cutoff cannot be pinned before June 2023
  app-developer and moderator fallout.

These should be patched or explicitly accepted before the frame locks are used
as accepted replay input.

## 10. Next Authorized Step

Patch the five targeted frame-lock issues in `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`, then either run a narrow follow-up
review or have the Chief Architect explicitly accept the remaining friction.

Evidence replay remains separately unauthorized.

## 11. Review-Use Boundary

This report is decision input for the Chief Architect. It does not approve,
accept, validate, or execute the method-validation replay. It does not
authorize source collection, source inventories, source maps, data spine work,
feature planning, implementation, staging, commit, push, or PR work.
