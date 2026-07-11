# TikTok Supervised Onboarding Runner Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated adversarial code review-and-patch of the supervised TikTok
  creator-onboarding runner, followed by home-model adjudication and the
  accepted bounded correction on branch codex/tiktok-supervised-onboarding-runner.
use_when:
  - Consuming the adjudicated review result for the TikTok creator-onboarding runner.
  - Checking which delegated claims were accepted, modified, or rejected before merge.
authority_boundary: retrieval_only
reviewed_by: Anthropic Claude (Sonnet 5)
authored_by: OpenAI Codex (exact model/version unrecorded by commission; author_model_family stated as "OpenAI / Codex")
de_correlation_bar: cross_vendor_discovery
commission: docs/prompts/reviews/tiktok_supervised_onboarding_runner_delegated_adversarial_code_review_patch_prompt_v0.md
review_target: branch codex/tiktok-supervised-onboarding-runner, pre-adjudication head 89f8b8e38931da88ced1aa98c7234f18ed0091fd, diff range origin/main...HEAD
mode: delegated_code_review_and_patch
access: repo
source_context_ready: true
report_written: docs/review-outputs/tiktok_supervised_onboarding_runner_delegated_adversarial_code_review_v0.md
patch_status: adjudicated_modify_applied
stale_if:
  - The accepted patch below is reverted, amended, or superseded on the lane branch.
  - A later review round over the same scope replaces this report.
non_claims:
  - not validation
  - not readiness
  - not acceptance for merge
  - not a live-capture proof
  - not runtime model routing
```

Use boundary: the cross-vendor review supplied decision input only. The
commissioning home-model lane adjudicated its findings, diff, verdict, and
residuals under `.agents/workflow-overlay/delegated-review-patch.md` and
`.agents/workflow-overlay/review-lanes.md`. This report records that
adjudication; it is not approval, readiness, or merge authority.

## Preflight And Provenance

- Commissioned repository: `C:\Users\vmon7\Desktop\projects\orca`.
- Dedicated implementation worktree:
  `C:\Users\vmon7\.codex\worktrees\13cf\orca`.
- Observed starting state: clean detached worktree at
  `89f8b8e38931da88ced1aa98c7234f18ed0091fd`; local and remote
  `codex/tiktok-supervised-onboarding-runner` refs matched that SHA. The
  worktree was then attached to that free existing branch without touching
  the shared checkout.
- Existing PR observed before edits: #870, open and draft, base `main`, head
  `codex/tiktok-supervised-onboarding-runner`, head SHA `89f8b8e3`.
- Reviewer worktree input:
  `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\tiktok-onboarding-code-review-cec6cc`.
  Its observed state matched the handoff: two modified target files plus this
  untracked report.
- Reviewer report input SHA256:
  `491D0D733FC037ECC1C18F75D108FAEF85D11F106056332F4E3308CA6D662A98`.
- Reviewer identity and authorship provenance are preserved exactly in the
  header. The delegate's cross-vendor discovery remains decision input; the
  accepted implementation below is the home-model lane's modified closure,
  not the delegate's original patch.

## Source Context

The home-model lane re-read `AGENTS.md`, the Forseti workflow-overlay entrypoint,
decision routing, review-lane and delegated-review adjudication closeout rules,
the commission prompt, the complete reviewer report and diff, and the complete
target implementation and unit-test files before editing. The reviewer had
previously recorded `SOURCE_CONTEXT_READY: true` after reading the full
commissioned source and diff surface.

## Home-Model Adjudication

Disposition: **MODIFY**.

### Accepted underlying defect

Two ownership/count seams combine to make the frozen creator grid less
trustworthy than intended:

1. `TIKTOK_PROFILE_GRID_DOM_EXTRACT_SCRIPT` admitted every TikTok-like video
   anchor found on the rendered page without restricting the anchor's handle
   to the requested creator, and `build_tiktok_grid_window` trusted those
   injected rows without an independent scheme/host/path check.
2. `_metric_items_from_payload` recursively treated nested `stats` + `id`
   mappings inside each direct `/api/post/item_list` row as independent metric
   candidates. A nested duet, stitch, source-video, ad, or similar object could
   therefore inflate the response-count stop condition and become eligible for
   final ID intersection.

These are the accepted defect. The live frequency of either trigger remains
unmeasured because the commission forbade live TikTok/browser capture.

### Rejected delegate policy

The delegate proposed requiring every admitted metric row to carry an explicit
matching `author.uniqueId`. That policy is rejected. Missing author attribution
alone does not prove contamination when a direct profile-list row's video ID
intersects a source-visible DOM URL whose normalized path is exactly
`/@creator/video/<id>`. Existing fixture coverage includes an authorless
profile item marked `isAd`; exact-author-only admission could discard a
legitimate creator-grid row.

The delegate's exact-author-only implementation hunk and its
`test_grid_window_excludes_items_lacking_creator_author_attribution` regression
did not land. Explicit mismatched authors remain excluded; missing authors are
intentionally allowed only when final creator-scoped URL and ID intersection
establishes ownership.

### F-02 optional residual retained

If both the real browser context close and browser close fail, the later
exception can mask the earlier diagnostic detail. Failure visibility remains:
the run still fails and the receipt is forced to `failed`. This is optional
diagnostic hardening, not part of the accepted ownership/count patch, and
remains unpatched.

## Accepted Patch Summary

The home-model lane applied the smallest complete correction inside the
commissioned files:

- `TIKTOK_PROFILE_GRID_DOM_EXTRACT_SCRIPT` now accepts
  `dom_extract_arg.creator_handle`, normalizes it, and emits only anchors whose
  `/@handle/video/id` handle exactly matches.
- `_capture_creator_grid` passes
  `{"creator_handle": creator_handle}` as `dom_extract_arg`.
- `build_tiktok_grid_window` independently rejects each DOM row unless its URL
  uses HTTP(S), has a TikTok host, and has the exact normalized
  `/@creator_handle/video/video_id` path.
- `_metric_items_from_payload` treats direct mappings in an `itemList` as the
  only candidates from that list and does not recursively mine their nested
  structures. Other sibling payload branches continue to be visited, and
  generic hydration traversal remains available where there is no direct
  `itemList` boundary.
- The existing author policy is preserved: explicit mismatch is excluded;
  missing author is allowed pending final creator-scoped URL/ID intersection.
- Focused tests cover authorless exact-URL admission, unrelated-handle DOM
  exclusion, explicit author mismatch, nested direct-`itemList` exclusion, and
  creator-handle DOM argument propagation.

The delegate's exact-author-only diff and test were not imported.

## Same-Check Red/Green Evidence

The defect tests were added before the implementation patch and run together
against the pinned implementation:

```text
python -m pytest -q tests/unit/test_tiktok_creator_onboarding.py::test_grid_window_excludes_unrelated_handle_dom_url tests/unit/test_tiktok_creator_onboarding.py::test_grid_window_does_not_count_nested_item_list_metric_node
FF                                                                       [100%]
FAILED ...::test_grid_window_excludes_unrelated_handle_dom_url - Failed: DID NOT RAISE <class 'source_capture.tiktok.creator_onboarding.TikTokCreatorOnboardingError'>
FAILED ...::test_grid_window_does_not_count_nested_item_list_metric_node - Failed: DID NOT RAISE <class 'source_capture.tiktok.creator_onboarding.TikTokCreatorOnboardingError'>
exit 1
```

The identical two-test command after the implementation patch:

```text
..                                                                       [100%]
exit 0
```

The three preserved-policy/wiring checks were then run together:

```text
python -m pytest -q tests/unit/test_tiktok_creator_onboarding.py::test_grid_window_accepts_missing_author_with_exact_creator_url tests/unit/test_tiktok_creator_onboarding.py::test_grid_window_excludes_explicit_mismatched_payload_author tests/unit/test_tiktok_creator_onboarding.py::test_onboarding_writes_selection_before_same_engine_deep_capture
...                                                                      [100%]
exit 0
```

## Validation Evidence

Observed before this report was written:

```text
cd forseti-harness
python -m pytest -q tests/unit/test_tiktok_grid_video_selection.py tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_source_capture_browser_snapshot.py tests/unit/test_tiktok_live_batch_probe.py
........................................................................ [ 52%]
................................................................         [100%]
exit 0
```

```text
cd forseti-harness
python -m pytest -q tests/contract
........................................................................ [ 57%]
.....................................................                    [100%]
exit 0
```

No live TikTok capture, browser production session, data-lake production write,
or registry mutation was run.

```text
git diff --check
exit 0
```

```text
python .agents/hooks/check_review_routing.py --strict
check_review_routing --strict: OK (base: origin/main)
exit 0
```

```text
python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/tiktok_supervised_onboarding_runner_delegated_adversarial_code_review_v0.md
exit 0
```

## Adjudicated Verdict And Residuals

The delegate identified a real ownership/count problem, but its proposed
exact-author-only closure was over-strict. The final disposition is `MODIFY`:
the DOM ownership gate and direct-`itemList` traversal boundary are accepted and
closed; legitimate authorless direct rows are intentionally preserved behind
the final creator URL/ID intersection.

Residuals and limits:

- Real-world trigger frequency remains unmeasured; no live capture was
  authorized or performed.
- Authorless legitimate profile rows are intentionally preserved. Ownership
  depends on the independent final TikTok host/path and video-ID intersection,
  not on author absence being treated as proof.
- F-02 double-close diagnostic masking remains optional and unpatched; failure
  visibility is not weakened.
- This patch does not claim readiness, live-session success, paid/organic
  classification, exhaustive suggested-account discovery, registry mutation,
  or merge approval.

## Review Use Boundary And Closeout

The delegated report, findings, and original patch were decision input only;
they were not approval, validation, mandatory remediation, or patch authority.
This amended report truthfully records what was kept, modified, and rejected;
it does not retroactively convert the delegate's recommendation into authority.

Next authorized step: one batched land step — complete the repository-root
validation and provenance gates, commit the three authorized files, push the
existing branch, verify the remote SHA, and update existing draft PR #870
without merging or changing draft state. Material next moves: none; the current
request ends at verified PR closeout.
