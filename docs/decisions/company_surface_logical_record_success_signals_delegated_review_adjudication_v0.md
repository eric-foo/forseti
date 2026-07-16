# Company Surface Logical-Record Success Signals Delegated Review Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Chief Architect adjudication decision
scope: >
  Adjudicates the de-correlated delegated adversarial artifact review-and-patch
  return for the Company Surface logical-record success signals and cold-agent
  front door.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/company_surface_logical_record_success_signals_delegated_adversarial_review_patch_v0.md
  - docs/prompts/reviews/company_surface_logical_record_success_signals_delegated_adversarial_review_patch_prompt_v0.md
  - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
  - forseti/product/information/company_surface/README.md
  - forseti/product/information/company_surface/purpose_contract_v0.md
  - forseti/product/information/company_surface/company_identity_boundary_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
```

## Decision

`ACCEPT_WITH_ONE_CA_MODIFICATION`.

The Chief Architect accepts AR-01 through AR-05 and keeps the controller's five
bounded contract hunks:

1. the retrieval scope names the record-level acceptance bar;
2. LRS-02 uses routed, contract-native language for the rule that downstream
   selection is not evidence;
3. LRS-03 makes captured time and relevant capture posture recoverable;
4. LRS-07 fails visibly when the current Silver envelope or single-raw-anchor
   addressing grammar cannot lawfully carry the logical record; and
5. LRS-11 makes the already-bound resolved-roll-up admission gate observable.

AR-06 is also accepted, but the CA closes it rather than deferring it. The
Coverage or failure marker family now mirrors the semantic cases exercised by
LRS-06: attempted-with-evidence, partial, failed, excluded, not-attempted, and
not-covered. Exact serialized labels remain an implementation choice, so this
does not amend Capture's discharge vocabulary or choose a physical schema.

No finding requires `NEEDS_ARCHITECTURE_PASS`.

## Adjudication By Finding

| Finding | Decision | Basis |
| --- | --- | --- |
| AR-01 | accept | The Common Logical Envelope requires captured time, and the activity family requires relevant capture posture. An inspectability signal omitting either permits a false pass. |
| AR-02 | accept as LRS-11 | Resolved-roll-up admission is independent of whether temporal views declare two cutoffs. Keeping it as its own signal preserves a distinct failure test; ten was never an owner-bound count. |
| AR-03 | accept | `research-pool row` had no routed owning definition. The replacement preserves the intended selection-is-not-evidence rule without a hidden GTM dependency. |
| AR-04 | accept | Silver's authoritative derived path carries one `raw_anchor`; an assertion with no determinate lawful anchor must stop and route rather than choose one arbitrarily. |
| AR-05 | accept | The retrieval scope must describe the cold-agent acceptance bar now routed from the README. |
| AR-06 | accept with CA modification | The mismatch is local to the owning contract and directly affects LRS-06. Mirroring semantic cases closes it without claiming a closed Capture enum. |

## Residual Adjudication

- **Eleventh-row shape:** rejected as a blocker. LRS-11 adds no policy and tests
  a separate admission failure; folding it into LRS-05 would make that signal
  carry two independent pass conditions.
- **Cold-agent test absent:** rejected as stale at adjudication. Before this
  delegated pass, a fresh agent started from `company_surface/README.md`, used
  only routed owning sources, answered all five reference-check questions, and
  rejected persistence-plus-resolved-identity as evidence-readiness laundering.
  Observed status: `cold_dogfood_status: no_failure_found`.
- **Three acceptance surfaces:** accepted residual. The record-level LRS bar,
  purpose-signal mapping, and whole-contract acceptance conditions serve
  different consumers. Future drift is possible, but no fourth registry or
  maintenance surface is justified by this review.
- **Reviewer-authored hunks:** closed by this source-backed home adjudication
  and local validation. They remain advisory review input until this decision
  and the accepted patch land together.
- **Report repository field:** the controller report preserves
  `repo: github.com/eric-foo/orca` as returned. The observed remote for this
  adjudication is `https://github.com/eric-foo/forseti.git`; this decision is
  the correction and the reviewer-authored report is not rewritten.

## Evidence And Verification Basis

Fresh primary-source reads confirmed:

- the Common Logical Envelope distinguishes effective/observation, captured,
  and recorded time;
- the activity family requires relevant capture posture;
- the Time And View Contract and identity boundary prohibit provisional,
  ambiguous, unresolved, or temporally indeterminate assertions from entering
  a resolved roll-up;
- Silver addresses authoritative derived records through one `raw_anchor`; and
- the Capture standing contract carries visible `not_attempted` discharge
  semantics while leaving exact Company Surface coverage labels deferred.

The returned report bytes were observed before adjudication as:

```yaml
delegated_review_report_sha256: 5F0CE38685FC7C0E91C8B5314482DA8B2F9C8251847341AF28B67C4EA7C7DC51
reviewed_head: 47b8cc9f89d2c80742872c845de574656122288d
controller_family: Anthropic / Claude
author_home_family: OpenAI / GPT
de_correlation_status: satisfied
```

## Remaining Risk

The success signals remain logical acceptance tests, not executable schema
validation. A later physical mapping can still expose a Silver or producer
incompatibility; LRS-07 requires that incompatibility to stop visibly rather
than authorizing a guessed fit. The accepted cold-agent result establishes
retrieval clarity for this revision only, not source completeness, runtime
enforcement, or product readiness.

## Non-Claims

This adjudication does not choose serialized fields, canonical identifiers,
producer lanes, storage paths, a Silver amendment, Org graduation, runtime,
GTM policy, outreach, validation, readiness, or owner acceptance of any later
mapping. It accepts only the bounded documentation changes named above.
