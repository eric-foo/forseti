# Core Spine v0 Method Validation Case-Frame Locks Adversarial Review

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Full adversarial artifact review of Core Spine v0 method-validation case-frame locks, run from the v0 review prompt with workflow-deep-thinking + workflow-adversarial-artifact-review.
use_when:
  - Deciding whether the case-frame lock artifact is safe to use as pre-replay input.
  - Checking current findings against the prior v0, v1, and v2 reports.
  - Determining what patches are needed before replay authorization.
authority_boundary: retrieval_only
open_next:
  - forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_locks_v0.md
  - docs/prompts/reviews/core_spine_v0_method_validation_case_frame_locks_adversarial_review_gpt54_prompt_v0.md
input_hashes:
  docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md: B4018996BECC8F79B254BF5A113265B873DCB9C1AE35746DABADAA4D99D4A537
branch_or_commit: main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c
downstream_consumers:
  - docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md
stale_if: Target artifact hash changes, or a later accepted review supersedes this report.
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md
  recommendation: patch_before_acceptance
  summary: "Full rerun found no hard blockers, confirmed all prior v0/v1 advisory findings remediated, and identified five targeted patch areas before treating the frame locks as accepted replay input."
  findings_count: 5
  blocking_findings: []
  advisory_findings:
    - AR-01: MV-09 positive-action frame is structurally biased toward caution
    - AR-02: MV-05 provisional cutoff creates a dependency cascade that may become a blocker
    - AR-03: MV-03 and MV-05 reframe conditions are outcome-shaped
    - AR-04: Section 10 verification checklist creates implicit replay authorization pull
    - AR-05: MV-01 post-window exclusion rule names a concrete post-window product outcome
  prior_findings_remediated:
    - "AR-01 (prior): MV-01 reframe condition no longer encodes SH-01 proof result"
    - "AR-02 (prior): MV-04 outcome-obviousness language no longer presupposes backlash"
    - "AR-03 (prior): MV-04 downgrade conditions no longer name install-count ambiguity"
    - "AR-04 (prior): MV-05 fair-cutoff rationale no longer anchors against known revolt"
    - "AR-05 (prior): MV-09 upgrade conditions no longer name acquisition timing advantage"
    - "FF-01 (prior): MV-03 academic/preprint source family narrowed to typed subject area"
  next_action: "Patch AR-01 through AR-05 or explicitly accept risks before treating frame locks as accepted replay input; evidence replay remains separately unauthorized."
```

## Review Provenance

- Review type: full adversarial artifact review, rerun from the v0 review prompt.
- Review target: `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`.
- Skill sequence: `workflow-deep-thinking` invoked first to frame the boundary problem; `workflow-adversarial-artifact-review` then ran the formal review.
- Review date context: 2026-05-21, Asia/Singapore.
- Target artifact SHA256: `B4018996BECC8F79B254BF5A113265B873DCB9C1AE35746DABADAA4D99D4A537` — matches prompt specification.
- Edit permission: read-only for the reviewed artifact.
- Output mode: review-report.
- Prior review history: this report replaces the earlier chat-derived v0 pre-patch record. Related reports at v1 (post-patch) and v2 (directed analysis) remain in place.

## 1. Review Target And Source-Read Ledger

Review target: `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`

Review lane: artifact review, read-only, per `.agents/workflow-overlay/review-lanes.md`.

Source-loading mode: strict overlay-bound formal review with declared dirty-state allowance.

| Source | Status at review time | Role in review |
| --- | --- | --- |
| `AGENTS.md` | committed | Overlay entrypoint; docs-first, no implementation authority |
| `.agents/workflow-overlay/README.md` | modified | Overlay binding and entrypoint |
| `.agents/workflow-overlay/project-authority.md` | committed | Project identity and forbidden drift |
| `.agents/workflow-overlay/source-of-truth.md` | modified | Source hierarchy and conflict rules |
| `.agents/workflow-overlay/artifact-roles.md` | modified | Review report role, destination, and permission |
| `.agents/workflow-overlay/review-lanes.md` | modified | Artifact review lane; read-only; report under `docs/review-outputs/` |
| `.agents/workflow-overlay/validation-gates.md` | modified | Prompt orchestration and git-status gates |
| `.agents/workflow-overlay/safety-rules.md` | committed | No implementation; no commit/push without authorization |
| `.agents/workflow-overlay/communication-style.md` | modified | YAML summary first; detailed report in durable file |
| `docs/product/core_spine_v0_first_proof_run_packet_v0.md` | committed | Prior SH-01 proof result; backtest leakage-control baseline |
| `docs/product/core_spine_v0_method_validation_rubric_v0.md` | untracked | Validation rubric and five-case design rules |
| `docs/product/core_spine_v0_method_validation_case_locks_v0.md` | untracked | Locked case identities and replacement rule |
| `docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md` | untracked | Safe vs dangerous frame-lock detail contract |
| `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md` | untracked | **Reviewed target** |

Sources not read in this run that were available in prior reviews:

- `docs/decisions/turn_08_product_thesis_v0.md` — committed but not found in this run; product thesis context was drawn from the rubric and proof packet instead.
- `docs/product/core_spine_v0_product_contract.md` — committed but not found.
- `docs/product/core_spine_v0_information_production_foundation_v0.md` — committed but not found.
- `docs/product/core_spine_v0_proof_protocol_v0.md` — committed but not found.

These files were available to the v1 reviewer. Their absence limits this review to artifact-visible evidence for any finding that would require the product contract or proof protocol for authority. No findings in this report require those sources; they are noted for completeness.

## 2. Dirty Sources Relied On

The four untracked method-validation product files (rubric, case locks, frame lock contract, reviewed target) and the modified overlay convention files. All relied upon under the explicit dirty-state allowance from the review prompt. Their uncommitted state means this review is anchored to the current workspace contents and the target hash above, not to a committed revision.

## 3. Scope And Excluded Scope

In scope:

- Cutoff contamination: whether any cutoff sits after the outcome window, after the company move being judged, or after source families that should be post-window.
- Recommendation leakage: whether any frame implies what Orca should recommend before replay.
- Case-study drift: whether any frame becomes a rich narrative or outcome story.
- Source-boundary looseness: whether source-family boundaries are too broad to prevent source fishing.
- `NEEDS_VERIFICATION` misuse: whether gaps are hidden, minimized, or treated as proven.
- Authorization leakage: whether the artifact authorizes evidence replay, source maps, source inventories, data spine, feature planning, or implementation.
- Portfolio imbalance: whether positive-action and reverse-case roles are framed in a way that pre-biases validation.
- Replacement-rule weakness: whether blocked cases could be replaced with easier cases that do not preserve the validation role.
- Remediation check: whether prior findings AR-01 through AR-05 and FF-01 are remediated.

Excluded:

- External URL or source correctness.
- Evidence replay or source collection.
- Pass/fail prediction for any case.
- Judgment of company decisions.
- Implementation, code, tests, runtime architecture, source systems, dashboards, scrapers, APIs, databases, scoring engines, automation, feature plans, or commercial willingness to pay.
- Patch execution against the reviewed artifact.

## 4. Boundary Problem

The structural line is whether a frame-lock field constrains replay or populates it.

Safe fields reduce the replay's degrees of freedom: cutoff dates, source-family boundaries, allowed action verbs, evidence standards, post-window exclusion rules, result-label semantics.

Dangerous fields supply replay with material to confirm: post-window product names, reframe paths that mirror actual outcomes, moralized or causal language, remediation plans disguised as reframe conditions, and threshold asymmetries that make one result type much easier to produce than another.

The artifact is structurally lean and largely correct. The five findings below identify targeted locations where the constraint/population line is crossed or at risk.

## 5. Correctness Findings

### AR-01

MV-09 positive-action frame is structurally biased toward caution.

- Location: Section 9, `MV-09` case frame — "Why later outcome was not obvious at cutoff" and "Upgrade conditions."
- Evidence: The "why not obvious" field lists accuracy, confidentiality, professional-duty, hallucination, workflow-fit, adoption, procurement, and integration risks — eight caution factors — with no corresponding action-side plausibility list. The upgrade conditions require convergence across five concurrent criteria: practitioner workflow pain, credible AI capability, incumbent content advantage, buyer urgency, and manageable professional-risk controls.
- Why it matters: `MV-09` is the portfolio's sole positive-action case, and its validation purpose is to test whether Orca can support decisive action before the outcome is obvious. A "why not obvious" field that is eight caution factors with no action-side plausibility, combined with a five-criteria convergence threshold that is the highest of the five cases, creates asymmetric framing. The replay is structurally more likely to return `Hold`, `Probe`, or underconfidence — not because the evidence fails to converge, but because the frame loads the caution side more heavily. Compare: MV-03's "why not obvious" field lists several incompatible responses and explicitly names action paths alongside caution paths; MV-05 acknowledges legitimate data-monetization incentives before naming caution factors. MV-09 does not provide the same balance.
- Next action: Rebalance the "why not obvious" field by stating action-side plausibility at the same abstraction level as caution-side risk — for example, acknowledging that incumbent content advantage, practitioner workflow pain, first-mover opportunity, and proven AI capability could support decisive action before the outcome was known. Keep the upgrade conditions threshold appropriate but action-type neutral; the five-criteria bar may be reasonable for a high-stakes acquisition-vs-hold decision but should be stated as the reliability standard, not a barrier.

### AR-02

MV-05 provisional cutoff creates a dependency cascade that may become a blocker.

- Location: Section 8, `MV-05` case frame — "Cutoff date or cutoff window" and "Expected outcome-comparison window"; Section 10, MV-05 verification need.
- Evidence: Cutoff is stated as "Provisional cutoff of 2023-05-30... exact cutoff remains `NEEDS_VERIFICATION`." The outcome-comparison window is stated as "2023-06-01 through 2023-08-31 for immediate ecosystem response." The gap between provisional cutoff and outcome window start is two days.
- Why it matters: If cutoff verification moves the cutoff into early June 2023 — which is plausible, since Reddit's API pricing intent was public in April 2023 but the concrete third-party-app fallout wave was already building in late May — the outcome-comparison window may need to start later or be collapsed entirely. The artifact states the outcome window as if fixed even though it directly depends on the NEEDS_VERIFICATION cutoff. This is not a routine gap: a cutoff that cannot be pinned before broad third-party-app and moderator fallout would change whether MV-05 is usable as framed. The outcome-comparison window should inherit the cutoff's NEEDS_VERIFICATION status.
- Next action: Mark the MV-05 outcome-comparison window as `NEEDS_VERIFICATION` with an explicit dependency note: "window start depends on cutoff verification; if the cutoff cannot be pinned before broad third-party-app fallout, the case is blocked or must be reframed."

### AR-03

MV-03 and MV-05 reframe conditions are outcome-shaped.

- Location: Section 6, `MV-03` case frame, "Reframe conditions"; Section 8, `MV-05` case frame, "Reframe conditions."
- Evidence: MV-03 states "The frame shifts from 'compete with ChatGPT' to 'protect verified developer knowledge, license trusted data, and improve workflow retrieval.'" MV-05 states "The response shifts from one broad API price to segmented AI/data licensing, staged enforcement, moderator/tool exemptions, app transition support, or trust-preserving governance."
- Why it matters: Both reframe conditions are specific enough to read as known outcome or remediation paths. MV-03's three-path reframe mirrors Stack Overflow's actual post-announcement strategic direction. MV-05's five-path reframe describes the remediation trajectory Reddit eventually pursued or should have pursued. A replay executor reading these conditions before collecting evidence will search for evidence supporting those specific paths rather than discovering what the at-cutoff evidence actually suggests. The prior review patched a similar finding in MV-01 (AR-01 in v0), where the reframe condition encoded the prior SH-01 proof result; the same pattern is present here for MV-03 and MV-05. Note: these reframe conditions were not touched in the prior patch cycle.
- Next action: Generalize both fields to neutral move categories. For MV-03: "from direct AI competition response toward knowledge quality, data-value capture, or workflow-positioning strategy." For MV-05: "from broad API pricing toward segmented monetization, ecosystem protection, governance design, or staged rollout."

### AR-04

Section 10 verification checklist can be misread as replay authorization.

- Location: Section 10, "Blockers And Verification Needs" heading and five verification bullet points; Section 12, "Current Verdict."
- Evidence: Section 10 frames each verification item as "Confirm [X] before evidence replay." Section 12 uses the verdict `ACCEPTED_CASE_FRAMES_AWAITING_EVIDENCE_REPLAY_AUTHORIZATION`, which contains "awaiting" — a word that positions evidence replay as the natural next step.
- Why it matters: The artifact does not control replay authorization. However, the "before evidence replay" framing can be read as: complete these five steps, then replay is authorized. A future replay executor receiving this artifact could treat completion of the Section 10 checklist as sufficient authorization, bypassing the separate launch authorization the prompt explicitly requires. The "awaiting" language in the verdict reinforces this pull without adding any safeguard. The artifact correctly states "Evidence replay authorized: no" in Section 1, but that declaration is not echoed near the verification checklist.
- Next action: Add an explicit sentence after the verification checklist in Section 10: "Completing these verification steps does not itself authorize evidence replay; a separate later owner authorization is required." Consider replacing `ACCEPTED_CASE_FRAMES_AWAITING_EVIDENCE_REPLAY_AUTHORIZATION` with a non-pull verdict such as `CASE_FRAMES_ACCEPTED_REPLAY_AUTHORIZATION_NOT_GRANTED` unless the "awaiting" framing is intentional and acceptable.

### AR-05

MV-01 post-window exclusion rule names a concrete post-window product.

- Location: Section 5, `MV-01` case frame, "Post-window exclusion rule."
- Evidence: "Exclude Zendesk AI-agent announcements, Resolution Platform material, acquisition announcements, changed Intercom/Fin positioning, refreshed comparison pages, and forum/review material published or materially changed after cutoff from the at-cutoff recommendation."
- Why it matters: "Resolution Platform" is a specific Zendesk product name. Its presence in the exclusion rule tells a replay reader that Zendesk launched a product of this name after the cutoff window — a concrete outcome detail. The exclusion is directionally correct and the material is properly quarantined, but naming a specific post-window product introduces outcome awareness inside a pre-replay frame. The category (AI-agent or resolution platform announcement material) achieves the same exclusion without naming the outcome. A similar concern applies to "acquisition announcements," which signals that an acquisition occurred.
- Next action: Replace specific product and event names with their categories. For example: "Exclude post-cutoff Zendesk AI-agent, resolution product, or platform-restructuring announcements; post-cutoff Intercom or Fin repositioning or pricing changes; refreshed comparison pages; and forum or review material published or materially changed after cutoff."

## 6. Friction Notes

These items were checked and did not produce advisory findings but are noted for replay-authorization decision-making:

- `NEEDS_VERIFICATION` propagation: the MV-01 outcome-comparison window start of 2024-10-09 inherits uncertainty from the provisional MV-01 cutoff, but is stated without a `NEEDS_VERIFICATION` qualifier. This is lower consequence than AR-02 (MV-05) because the MV-01 cutoff window spans nine days (2024-09-30 to 2024-10-08) rather than two days, creating more room to absorb cutoff movement without collapsing the window.
- MV-04 threshold asymmetry: the downgrade conditions are longer and more source-discoverable (trust sensitivity, pricing-formula complexity, retroactive cost-exposure risk, credible alternatives) than the upgrade conditions (developers accept pricing logic, switching risk low, migration threats weak). This asymmetry may be appropriate for a reverse case where the validation role is to test avoidance of a bad move, but a replay executor should be aware that finding downgrade evidence will be structurally easier than finding upgrade evidence given the available source landscape.
- Portfolio balance at case-identity level is preserved. The five roles — competitor narrative pressure (MV-01), AI disruption and developer workflow (MV-03), reverse pricing and ecosystem trust (MV-04), platform and data monetization (MV-05), positive legal-AI action (MV-09) — remain distinct and serve the rubric's requirement for both upside recognition and mistake avoidance. AR-01 above addresses the most consequential imbalance risk (MV-09 caution framing). After that patch, the portfolio-level balance concern is reduced.

## 7. Prior Findings Status

All prior advisory findings from the v0 and v1 review cycle are confirmed remediated.

- AR-01 (prior): MV-01 reframe condition no longer encodes the SH-01 proof result. Current text ("Evidence shifts the competitive response angle away from direct feature matching toward a different buyer-facing claim or response basis") is now generic and does not reference the prior output.
- AR-02 (prior): MV-04 outcome-obviousness language no longer presupposes backlash as a known event. Current text frames uncertainty around whether ecosystem trust was fragile enough for disruption, not around the scale, speed, or durability of a backlash already known to have occurred.
- AR-03 (prior): MV-04 downgrade conditions no longer name install-count ambiguity. Current text uses "pricing-formula complexity, unclear or retroactive cost-exposure risk," which names the category without the outcome-specific term.
- AR-04 (prior): MV-05 fair-cutoff rationale no longer anchors against "the public revolt" and no longer implies a narrower or phased move as the expected answer. Current text is neutral: "the full scale of app-developer and moderator response had not yet materialized."
- AR-05 (prior): MV-09 upgrade conditions no longer name acquisition timing advantage. Current text uses "timing advantage for decisive capability capture over a wait-and-see or build-only path" — action-type neutral.
- FF-01 (prior): MV-03 second-order source family preprint category has been narrowed. Current text reads "publicly available academic or preprint studies of developer AI behavior, Stack Overflow usage patterns, or knowledge-platform adoption visible before cutoff" — subject-typed and bounded.

## 8. Items Checked With No Finding

- Cutoff placement: all five cutoffs sit before the named outcome or announcement window. MV-03 (2023-07-26, day before OverflowAI) and MV-09 (2023-06-25, day before acquisition announcement) are sharp and clean.
- `NEEDS_VERIFICATION` usage: markers are consistently applied to unresolved cutoff and source-visibility claims and are not treated as resolved facts elsewhere in the artifact.
- Authorization boundaries: Section 1 explicitly excludes evidence replay, source maps, source systems, data spine, automation, dashboards, scoring engines, feature planning, and implementation. Section 11 restates these non-claims in full.
- Case-study drift: the frames remain structured and lean, with no narrative arc, rich outcome story, causal claim, moralized framing, marketing language, or buyer-value claim.
- Replacement rule: Section 10 requires that a blocked case's replacement preserve the blocked case's validation role; the roles are named per case.
- Portfolio positive-action representation: MV-09 is preserved as the positive-action case despite the AR-01 framing concern; the case role is not missing, only the balance within the frame needs adjustment.

## 9. Not-Proven Boundaries

- Public pre-cutoff source availability for any of the five cases is not proven; `NEEDS_VERIFICATION` items are unresolved.
- Case-frame acceptance is not proven by this review; acceptance remains a Chief Architect decision.
- Evidence replay is not authorized by this review.
- External willingness to pay, feature readiness, implementation readiness, data-spine readiness, source-map readiness, and product-market fit remain unproven.
- This review report is untracked. It is anchored to the current workspace contents and the target artifact hash above, not to a committed revision.

## 10. Blockers

No hard blocker is recorded.

Two findings carry elevated consequence:

- AR-01 is high consequence because the portfolio's positive-action validation test may under-test upside-recognition judgment if the MV-09 frame loads caution more heavily than action before replay begins.
- AR-02 is high consequence because MV-05 may become blocked — not merely uncertain — if the cutoff cannot be pinned before early June 2023 third-party-app and moderator fallout. This would change the case from a NEEDS_VERIFICATION delay to a blocked or replacement situation.

Neither finding creates a hard block on using the frame locks as decision input at this stage, but both should be resolved before replay authorization.

## 11. Next Authorized Step

Patch AR-01 through AR-05 against `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`, then either run a narrow follow-up review or have the Chief Architect explicitly accept any remaining friction.

Alternatively, explicitly accept each finding as a known risk and proceed to replay authorization under those risks; the framing risks are advisory and do not constitute hard blockers.

Evidence replay requires a separate later owner authorization. If replay is subsequently authorized, the five case-specific `NEEDS_VERIFICATION` timing and source-visibility items must be resolved before any source family is used for at-cutoff reasoning.

## 12. Review-Use Boundary

These findings are decision input for the Chief Architect. They are not mandatory remediation unless separately accepted and authorized by a patch or integration execution assignment.

This review does not approve, accept, validate, or authorize the method-validation replay. It does not authorize source collection, source inventories, source maps, data spine work, feature planning, implementation, staging, commit, push, or PR work.
