# Reddit Candidate Intake No-Live-Access Delegated Review Adjudication Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Chief Architect adjudication decision
scope: >
  Adjudicates the delegated adversarial code review-and-patch output for the
  no-live-access Reddit Candidate URL Intake implementation slice.
authority_boundary: decision_record
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_no_live_access_adversarial_code_review_v0.md
  - docs/prompts/reviews/reddit_candidate_intake_no_live_access_adversarial_code_review_prompt_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/product/data_capture_spine/data_capture_spine_candidate_url_intake_contract_v0.md
  - docs/product/data_capture_spine/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
```

## Decision

`ACCEPT_WITH_DEFERRED_MINORS`.

The Chief Architect accepts the delegated controller's three proposed bounded
changes as kept worktree state:

1. Add Reddit body/HTML/DOM/parser-output key names to
   `FORBIDDEN_OUTPUT_FIELDS` in
   `orca-harness/capture_spine/reddit_candidate_intake/validation.py`.
2. Add the `selftext` / `selftext_html` / `body_html` regression test in
   `orca-harness/tests/unit/test_reddit_candidate_intake.py`.
3. Add `http`, `subprocess`, `pycurl`, `websocket`, `websockets`, and `ftplib`
   to the no-live-access forbidden import roots in
   `orca-harness/tests/contract/test_reddit_candidate_intake_contract.py`.

The delegated report's three minor findings remain deferred owner-policy or
cleanup items. They are not blockers for this no-live-access implementation
slice:

- dead/no-op tail branches in two validators;
- outbound-row refusal raising bare `ValueError` rather than
  `RedditCandidateIntakeError`;
- numeric cap ceilings not enforced against `DEFAULT_CAPS` maxima.

## Basis

The accepted changes are in-bounds for the commissioned patch scope and close
guardrail-completeness gaps without changing lane architecture. They reinforce
the existing contract boundaries:

- no body/comment/profile/raw HTML/rendered DOM/parser-output output;
- no live Reddit/HTTP/browser/proxy/Armory import path in this package;
- no Source Capture Packet output or source-capture coupling.

The review did not return `NEEDS_ARCHITECTURE_PASS`, and this adjudication does
not find a design-level blocker.

## Local Verification

Fresh validation observed in this CA lane:

```text
python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py
..........                                                               [100%]
10 passed in 0.07s
```

Observed post-adjudication hashes:

```yaml
validation_py: A970F14E664C104493B28F63BDFE3FD9C59F91C839F83F7D6A93F1B02F683E43
contract_test_py: EF4A251E69D61B30BD92A6571C0F897871D246963FCAD62C303784265C42D0AE
unit_test_py: C2EE3D5B1082E173AAEF9FC020258EDE2F18B8944632398AE5A1144F7A31DB66
delegated_review_report: 797F7E6892547662076C885EF13975237E5EAC00122481EDDA87796676514424
```

## Residual Risk

The accepted denylist hardening is not a full design guarantee for arbitrary
hand-built dictionaries. The typed dataclass output path remains the stronger
allowlist. If later implementation accepts arbitrary output mappings from a
runner, add a per-row-shape allowlist instead of relying on an ever-growing
forbidden-key list.

## Non-Claims

This decision is not live Reddit authorization, CloakBrowser/proxy
authorization, Source Capture Armory authorization, fixture admission, Source
Capture Packet permission, deployment readiness, or whole-harness validation.
It accepts only the bounded no-live-access code/test changes listed above.
