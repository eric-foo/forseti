# Reddit Candidate Intake Old Reddit HTML Projection Delegated Review Adjudication Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Chief Architect adjudication decision
scope: >
  Adjudicates the delegated adversarial review-and-patch output for the old
  Reddit HTML static-projection and Reddit .json refusal implementation slice.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_v0.md
  - docs/prompts/reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_prompt_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
```

## Decision

`ACCEPT_WITH_DEFERRED_MINORS`.

The Chief Architect accepts the delegated controller's two proposed bounded
changes as kept worktree state:

1. Add `"author"` and `"author_fullname"` to `FORBIDDEN_OUTPUT_FIELDS` in
   `orca-harness/capture_spine/reddit_candidate_intake/validation.py`.
2. Add `test_projection_rejects_undeclared_candidate_surface` in
   `orca-harness/tests/unit/test_reddit_candidate_intake.py`.

The delegated report did not return `NEEDS_ARCHITECTURE_PASS`, and this
adjudication does not find a design-level blocker.

## Basis

PC-01 is accepted because it is a low-risk extension of the already accepted
secondary forbidden-output denylist pattern. The typed candidate-row dataclasses
remain the primary output allowlist, but exact Reddit author identity keys are
reasonable to block in the secondary untyped mapping guard because Candidate
URL Intake must not emit user/profile/author identity data.

PC-02 is accepted because it closes a real regression-test gap for the
`source_surface` allowlist gate. The projection helper already enforced
`undeclared_candidate_surface`; the missing test meant a future refactor could
remove that guard without failing the narrow suite.

Both changes stay inside the delegated patch scope. They do not widen Candidate
URL Intake into live Reddit access, parser-runner behavior, Source Capture
Armory, Source Capture Packets, ECR, Cleaning, Judgment, source-quality scoring,
fixture admission, or Data Capture handoff.

## Local Verification

Fresh validation observed in this CA lane from `orca-harness/`:

```text
python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py
..............                                                           [100%]
14 passed in 0.06s
```

Observed post-adjudication hashes:

```yaml
delegated_review_report: B796DF7B3CAEF0A9EAE86DC858FCDF58680845BC7991DBF8D0A91A4BF1B44921
validation_py: D21716AE5E3FAC9951F172A81072101EF0E6579EAB8BA6DC9E1765FCB34B8DAF
unit_test_py: 35FA59C16D7AE3C9DB36DC1A6DEFB55F38B4F285E0367CB952E15424B30816BE
```

## Deferred Findings

The following delegated-review findings remain deferred and are not accepted
as blockers for this old Reddit HTML projection slice:

- dead/no-op tail in `validate_run_envelope` after the outbound-surface check;
- dead/no-op tail in `validate_promotion_receipt`;
- `writer.py` raising bare `ValueError` for outbound-row refusal;
- numeric cap ceilings not enforced against `DEFAULT_CAPS` maxima.

Those items may be cleaned up in a later bounded commission if repeated
friction warrants it. They do not change the acceptance of PC-01 or PC-02.

## Residual Risk

The forbidden-output denylist is a secondary guard for arbitrary mappings, not
a complete schema strategy. The durable boundary remains the typed output
allowlist: candidate subreddit rows, candidate thread URL rows, outbound URL
candidate rows, run provenance, and non-claim receipts only. If a later runner
accepts or emits arbitrary dictionaries, add row-shape allowlisting instead of
trying to enumerate every possible forbidden Reddit field name.

The validation here is local unit/contract validation only. It is not live
Reddit validation, CloakBrowser/proxy validation, runtime deployment evidence,
or source-access readiness.

## Non-Claims

This decision is not live Reddit authorization, Reddit `.json` intake
authorization, CloakBrowser/proxy authorization, Source Capture Armory
authorization, Source Capture Packet permission, fixture admission, ECR,
Cleaning, Judgment, source-quality scoring, Data Capture handoff, deployment
readiness, or whole-harness validation. It accepts only the two bounded
code/test changes listed above.
