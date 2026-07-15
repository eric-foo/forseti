# TikTok Profile Bio Capture Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Cross-vendor delegated adversarial code review-and-patch return for the
  bounded TikTok creator-onboarding public profile-bio capture change.
use_when:
  - Adjudicating the delegated findings and the one returned hunk before keep.
  - Deciding whether the bio selector needs a live-DOM-verified follow-up pass.
authority_boundary: retrieval_only
```

## Commission, target, and authority

```yaml
commission: delegated_code_review_and_patch (repo access mode)
target_worktree: C:\tmp\orca-tt-profile-bio-20260715
target_branch: codex/tiktok-onboarding-profile-bio
target_head: d25ba56bd3df3b184d34fa15e12b2803eda0241d
patchable_scope:
  - forseti-harness/source_capture/tiktok/creator_onboarding.py
  - forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
everything_else: read-only / flag-only
review_method: workflow-code-review applied to the bounded dirty diff
lifecycle_actions_taken: none (no commit, push, PR, merge, stash, reset, cleanup, or live capture)
```

## Provenance and de-correlation

```yaml
reviewed_by: claude-opus-4-8
authored_by: openai_gpt5_codex
reviewer_vendor: Anthropic
author_vendor: OpenAI
de_correlation_bar: cross_vendor_discovery
de_correlation_proof: >
  Reviewer runtime is Anthropic claude-opus-4-8; the commissioning prompt
  declares authored_by openai_gpt5_codex. Different vendor and model lineage,
  so the cross-vendor discovery bar is met. No same_vendor_rationale required.
```

## Receiver binding

Proved before any source loading, all from the live target worktree:

```yaml
direct_write_probe: >
  Wrote .claude_reviewer_write_probe.tmp (34 bytes) into the target worktree
  root, confirmed on disk, then removed it. Post-removal existence check
  reported PROBE REMOVED OK; the probe left no residue.
concurrent_writer_check: >
  No index.lock, HEAD.lock, MERGE_HEAD, RESERVE_HEAD, rebase-merge, or
  rebase-apply present. `git worktree list` shows exactly one worktree holding
  codex/tiktok-onboarding-profile-bio (the target). Dirty set was byte-identical
  before and after the probe.
target_state_match: exact (branch, HEAD, three-path dirty set, both commissioned hashes)
```

Fresh-read target state observed at binding time:

```yaml
observed_branch: codex/tiktok-onboarding-profile-bio
observed_head: d25ba56bd3df3b184d34fa15e12b2803eda0241d
observed_dirty_set:
  - " M forseti-harness/source_capture/tiktok/creator_onboarding.py"
  - " M forseti-harness/tests/unit/test_tiktok_creator_onboarding.py"
  - "?? docs/prompts/reviews/tiktok_profile_bio_capture_adversarial_code_review_and_patch_prompt_v0.md"
pre_review_hashes_observed:
  forseti-harness/source_capture/tiktok/creator_onboarding.py: 6d720de8b25ce960279543f78d91307608283e7544d1f75cb5cb236a16d02337
  forseti-harness/tests/unit/test_tiktok_creator_onboarding.py: 9eb35a09a71b16a29e9318f37b4b40ef825464721328a9832deae5d8dc2defcd
prompt_file_live_hash_observed: b74aa67b3aa0c4413632619e3bfd29799d04adbee1a73c592a8d79801f1a01a3
post_patch_hashes:
  forseti-harness/source_capture/tiktok/creator_onboarding.py: 45529057ac19c79d95b2a3d3968b45690f72631678a80f119e3759905fb794d8
  forseti-harness/tests/unit/test_tiktok_creator_onboarding.py: 064eedf7499b6040f805085a3e9922974d066d4c5c7d51512e6877247e340bae
```

Both commissioned hashes matched exactly, so no `BLOCKED_TARGET_STATE_MISMATCH`.
The prompt file is an authorized pre-existing dirty path and was not patched.

## Scope and sources loaded

```yaml
target_files:
  - forseti-harness/source_capture/tiktok/creator_onboarding.py (bio hunks + surrounding capture/receipt paths)
  - forseti-harness/tests/unit/test_tiktok_creator_onboarding.py (bio tests + fixtures)
owning_sources_read_to_adjudicate:
  - forseti-harness/source_capture/tiktok/admission.py (sensitive-material guard, lines 25-50, 366-385)
  - forseti-harness/source_capture/tiktok/batch_packet.py (Bronze staging + suggested-evidence validation)
  - forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py (frontier anchor)
  - forseti-harness/tests/unit/test_tiktok_batch_admission.py (Bronze raw/04 boundary, read-only)
overlay_authority_read:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/safety-rules.md
```

## Findings

Severity and confidence are priority labels only. They are not thresholds for
reporting, and they create no approval, readiness, or remediation authority.

### F1 — Primary bio absence destroys real fallback bio evidence and reports a false `visible_empty`

```yaml
severity: major
confidence: high
verdict: CONFIRMED (empirically reproduced)
fitness_criteria_violated: [3, 5]
attack_resolved: "Could primary/fallback merge order erase, misattribute, or manufacture bio evidence?"
file: forseti-harness/source_capture/tiktok/creator_onboarding.py
line: 1049
disposition: patched
```

In `_capture_suggested_accounts`, the merge guard was:

```python
if primary.dom_observation.get(
    "profile_bio_element_detected"
) is True or (
    isinstance(primary_bio_text, str) and primary_bio_text.strip()
):
    fallback.dom_observation["profile_bio_text_or_none"] = primary_bio_text
    fallback.dom_observation["profile_bio_element_detected"] = True
```

The second disjunct is fully implied by the first: the extract scripts set
`profile_bio_element_detected: Boolean(profileBioNode)`, and non-empty text is
impossible without the node. So the guard reduced to *"whenever the primary
route saw the bio element at all, overwrite the fallback's bio text with the
primary's — including when the primary's is `None`."*

The fallback is a second, independent full page load of the same profile URL, so
its bio observation is real evidence. When the primary saw the element but
extracted no text (hydration timing, or a rendered-empty node) and the fallback
load actually captured the bio, the fallback's real text was replaced with
`None` and the receipt reported `profile_bio_status: visible_empty` — a false
empty observation of a bio that was in fact captured.

Reviewer probe against the live target worktree, before the patch:

```text
fallback route observed bio : 'Budget fragrance reviews | daily uploads'
merged dom_observation bio  : None
receipt profile_bio_text    : None
receipt profile_bio_status  : 'visible_empty'
suggested_accounts preserved: ['fallback_creator']
```

The same probe after the patch:

```text
merged dom_observation bio  : 'Budget fragrance reviews | daily uploads'
receipt profile_bio_text    : 'Budget fragrance reviews | daily uploads'
receipt profile_bio_status  : 'captured'
suggested_accounts preserved: ['fallback_creator']
```

The existing merge test (`test_suggested_capture_uses_profile_view_all_only_after_primary_not_visible`)
covers only the primary-has-real-text case, which is exactly the branch that
already worked, so the defect was invisible to the suite.

```yaml
minimum_closure_condition: >
  An actually observed primary bio still wins, and a primary route that observed
  no bio text can no longer replace a fallback-observed bio with absence or
  relabel it visible_empty; a test fails if that regresses.
next_authorized_action: adjudicate the returned hunk in the commissioning Codex lane
```

### F2 — `profile_bio_element_detected` is bare DOM presence, so `visible_empty` asserts a visibility never checked and the selector can bind a non-root node

```yaml
severity: major
confidence: medium
verdict: PLAUSIBLE (not decidable without live DOM)
fitness_criteria_at_risk: [1, 5]
attacks_resolved:
  - "Could the selector capture a bio from a modal, candidate card, stale SPA subtree, or hidden/non-root node?"
  - "Does visible_empty require an actually detected root bio element rather than a hidden/stale selector hit?"
file: forseti-harness/source_capture/tiktok/creator_onboarding.py
lines: [189, 356]
disposition: reported, deliberately not patched
```

Both extract scripts use an unscoped, presence-only lookup:

```javascript
const profileBioNode = document.querySelector('[data-e2e="user-bio"]');
```

Two distinct problems follow, sharing one root cause:

1. **Unchecked visibility.** `profile_bio_element_detected` is
   `Boolean(profileBioNode)` — DOM presence, not visibility. The status token
   `visible_empty` therefore asserts an observation the code never makes. The
   primary script already defines and uses a `visible()` helper for the
   suggested surface (line 143), so the bio path is inconsistent with the
   file's own idiom for that same token. (The fallback script's
   `suggested_surface_detected` is likewise not visibility-gated, so the
   inconsistency is partly pre-existing rather than introduced here.)
2. **Unscoped first-match.** `querySelector` returns the first match in
   document order with no root scoping. If TikTok renders a responsive
   duplicate, a stale SPA subtree, or a modal/candidate node carrying
   `data-e2e="user-bio"` earlier in document order than the real profile
   header, the capture binds the wrong node. `innerText || textContent` then
   masks a hidden duplicate that still carries text (yielding `captured` from
   a non-root node), while a hidden *empty* duplicate yields `visible_empty`
   and the real bio is missed entirely.

I did not patch this. Every candidate fix — gating detection on `visible()`,
preferring the first visible match, or scoping to a profile-header container —
turns on TikTok's actual live DOM, which this commission forbids me to observe
and which no gate here exercises. Gating detection alone would relabel the
hidden-duplicate case `not_visible`, which is no truer than `visible_empty`
when a real bio is visible on the page. Guessing a container selector risks
`null` and total bio loss, which is strictly worse than the current behavior.
This needs one coherent fix designed against a real captured profile DOM.

```yaml
minimum_closure_condition: >
  Against a real captured TikTok profile DOM (including a profile whose bio is
  empty), the bio node bound by the extract is shown to be the root profile bio,
  and visible_empty is emitted only for a bio element actually observed visible.
next_authorized_action: >
  owner decision on a follow-up lane with live-capture authority; not closable
  under this commission's two-file, no-live-capture authority
```

### F3 — `innerText || textContent` can silently drop internal line breaks

```yaml
severity: minor
confidence: medium
verdict: PLAUSIBLE
fitness_criterion_at_risk: 4
file: forseti-harness/source_capture/tiktok/creator_onboarding.py
lines: [190, 357]
disposition: reported, not patched
```

`innerText` is layout-aware and renders block boundaries and `<br>` as `\n`;
`textContent` does not. When the bio node is present but not rendered,
`innerText` returns `''` and the code falls through to `textContent`, so a
multi-line bio is captured with its internal line breaks collapsed. The stored
text would then not be the *exact* bio the commission asks for, while still
reporting `captured`. The `||` fallback is the established idiom throughout this
file (`display_text_or_none`, view-count footers), so changing it only for the
bio would fork the file's convention for a case that is entangled with F2's
hidden-node question. Left for the same live-DOM-verified pass.

```yaml
minimum_closure_condition: >
  A bio with internal line breaks is shown to round-trip with breaks intact, or
  the receipt stops claiming exactness for the textContent path.
next_authorized_action: fold into the F2 follow-up lane
```

### F4 — A public bio containing token-shaped text would abort the whole receipt build

```yaml
severity: minor
confidence: low
verdict: PLAUSIBLE
fitness_criterion_at_risk: 6
file: forseti-harness/source_capture/tiktok/creator_onboarding.py
line: 2208
disposition: reported, not patched
```

`_build_suggested_accounts_receipt` ends with
`assert_no_sensitive_tiktok_material(receipt)`, and the bio is now inside that
receipt. `_SENSITIVE_QUERY_RE` matches `msToken=`, `sessionid=`, `ttwid=` and
similar (`admission.py:30`). A public bio containing such a literal substring
would raise and discard the whole receipt — including the suggested-account and
external-link evidence that has nothing to do with the bio. The probability is
very low, and failing loud is the correct default over silently admitting
session-shaped material, so I am not proposing a scrub path; the finding is the
blast radius, not the guard. Worth noting only if bio capture is later widened
to lower-trust text.

```yaml
minimum_closure_condition: >
  Either the blast radius is accepted in writing, or bio-triggered sensitive
  hits fail the bio field alone without discarding co-captured evidence.
next_authorized_action: owner decision; no action required for this change
```

### F5 — Bronze carriage of the bio is structural, not asserted

```yaml
severity: minor
confidence: high
verdict: CONFIRMED
fitness_criterion: 8 (second half)
file: forseti-harness/tests/unit/test_tiktok_batch_admission.py
line: 316
disposition: reported, outside patch authority
```

Criterion 8's Bronze half holds structurally: `batch_packet.py:130` stages the
runner-written `tiktok_suggested_accounts_attempt.json` **raw bytes** as
`raw/04_tiktok_suggested_accounts_attempt.json`, and
`_validate_suggested_accounts_evidence` is a gate that returns parsed evidence
without merging it into `payload`, so there is no top-level packet duplication.
But the Bronze test asserts only `suggested_accounts[0].handle`, never a bio
field — so bio carriage across the boundary is inferred from pass-through, not
observed by a test. `test_tiktok_batch_admission.py` is outside this
commission's two-file patch authority, so I did not add the assertion.

```yaml
minimum_closure_condition: >
  A test observes profile_bio_text_or_none surviving into
  raw/04_tiktok_suggested_accounts_attempt.json.
next_authorized_action: patch authorization request for test_tiktok_batch_admission.py
```

### F6 — Missing bio keys are reported as `not_visible`

```yaml
severity: minor
confidence: medium
verdict: CONFIRMED
fitness_criterion_at_risk: 5
file: forseti-harness/source_capture/tiktok/creator_onboarding.py
line: 2122
disposition: reported, not patched
```

When `dom_observation` carries no bio keys at all,
`_build_suggested_accounts_receipt` reports `not_visible` — an affirmative claim
that the page was observed to have no bio element — where the truth is that the
extract said nothing about the bio. `test_suggested_receipt_distinguishes_empty_bio_from_missing_bio`
(line 1913) codifies this mapping. It is unreachable today because both live
extract scripts always emit both keys, so the current blast radius is nil; it
becomes a false-absence path the moment a third extract shape reaches this
builder. Recorded rather than patched because the fix (distinguishing
`not_reported` from `not_visible`) is a receipt-vocabulary change and therefore
a product decision, not a defect closure.

```yaml
minimum_closure_condition: >
  Either the invariant "every extract feeding this builder emits both bio keys"
  is enforced, or an unreported bio is distinguishable from an absent one.
next_authorized_action: owner decision; no action required for this change
```

## Considered and defended

Candidates I attacked and could not sustain. Listed so the adjudicator sees the
discard pile rather than inheriting my filter. These are not findings.

- **Bio extraction failure discarding suggested-account evidence (criterion 6).**
  Defended: the bio hunks only add keys; the reviewer probe confirmed
  `suggested_accounts` survives the merge intact, and a genuine script throw
  returns `BrowserSnapshotFailure`, routing to the explicit `failed` branch
  (line 2086) rather than a false empty. The one residual path is F4.
- **JS exception turning failure into `not_visible`.** Defended: the bio lines
  are `document.querySelector` plus `String(...).trim()` with no throwing
  operation; a whole-script failure is surfaced as `failed`, not `not_visible`.
- **Suggested-account and external-link semantics changed by the merge
  (criterion 7).** Defended: the `profile_external_links` merge is pre-existing
  and untouched; the bio merge writes only bio keys; the status expression for
  `status` and `profile_external_links_status` is unchanged.
- **Geography/audience inference in acquisition (criterion 9, and the
  "do tests silently encode UK/US inference" attack).** Defended: no added code
  reads, parses, or branches on bio content. The `🇬🇧` in the fixtures
  (lines 670, 1568) is evidence-shaped fixture text exercising emoji
  preservation, not an inference path; the branch name is bio-scoped.
- **Outer-trim exactness (criterion 4, trimmed path).** Defended: JS `.trim()`
  and Python `.strip()` are both outer-boundary only and idempotent;
  `test_suggested_receipt_preserves_profile_bio_and_clean_external_links`
  observes outer trim with an internal `\n`, emoji, and a bullet preserved. The
  unrendered-node case is F3.
- **Runner proving only an isolated helper (criterion 8, first half; the
  "does the normal runner write the receipt Bronze admits" attack).** Defended:
  `test_onboarding_writes_selection_before_same_engine_deep_capture` drives
  `run_tiktok_creator_onboarding` end-to-end and reads the bio back out of the
  actually written `tiktok_suggested_accounts_attempt.json` (lines 764-770) —
  the same file Bronze stages.
- **Auth/session leakage through fields, fixtures, or diagnostics
  (criterion 11).** Defended: the receipt is scanned by
  `assert_no_sensitive_tiktok_material` (line 2208) and again at the packet
  boundary (`batch_packet.py:117`, `:235`); no bio field, fixture, or
  diagnostic in the diff carries auth material. No credential or token value
  appears in this report.
- **Candidate profiles opened / Linktree search / account mutation
  (criterion 10).** Defended: `candidate_profiles_opened: 0` and
  `account_mutations_taken: 0` are unchanged; no navigation was added. No live
  capture was performed by this review.

## Patch applied

One hunk, in the authorized source file only.

```diff
--- a/forseti-harness/source_capture/tiktok/creator_onboarding.py
+++ b/forseti-harness/source_capture/tiktok/creator_onboarding.py
@@ -1049,15 +1049,12 @@ def _capture_suggested_accounts(
             primary_bio_text = primary.dom_observation.get(
                 "profile_bio_text_or_none"
             )
-            if primary.dom_observation.get(
-                "profile_bio_element_detected"
-            ) is True or (
-                isinstance(primary_bio_text, str) and primary_bio_text.strip()
-            ):
+            if isinstance(primary_bio_text, str) and primary_bio_text.strip():
                 fallback.dom_observation["profile_bio_text_or_none"] = (
                     primary_bio_text
                 )
-                fallback.dom_observation["profile_bio_element_detected"] = True
+            if primary.dom_observation.get("profile_bio_element_detected") is True:
+                fallback.dom_observation["profile_bio_element_detected"] = True
```

Resulting semantics, matching criterion 3:

- primary observed real text: primary text wins (an actually observed primary
  bio is preserved);
- primary observed no text, fallback did: the fallback's text stands (primary
  absence no longer overwrites real fallback evidence);
- element detection is the union of both routes, so a primary-only empty
  observation still yields `visible_empty` rather than `not_visible`.

One test added to `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`
(`test_primary_bio_absence_does_not_overwrite_observed_fallback_bio`, inserted
after the existing merge test): drives `_capture_suggested_accounts` with a
primary that detected an empty bio element and a fallback that observed real bio
text, then asserts the receipt reports the fallback's text as `captured` and
still carries the fallback suggested account. It fails on the pre-patch source.

No other file was created, edited, deleted, renamed, staged, or restored.

## Validation

All commands run from the target worktree; harness commands from
`C:\tmp\orca-tt-profile-bio-20260715\forseti-harness`.

| Gate | Command | Exit | Result |
| --- | --- | --- | --- |
| 1 | `git diff --check` | 0 | GATE PASS — no whitespace/conflict defects |
| 2 (pre-patch baseline) | `python -m pytest tests/unit/test_tiktok_creator_onboarding.py -q` | 0 | GATE PASS — 49 passed (matches author evidence) |
| 2 (post-patch) | `python -m pytest tests/unit/test_tiktok_creator_onboarding.py -q` | 0 | GATE PASS — 50 passed (49 + the added regression test) |
| 3 | `python -m pytest tests/unit -k tiktok` | 0 | GATE PASS — 352 passed, 2583 deselected, 2 warnings in 18.26s |
| 4 | `python -m pytest tests` | 0 | GATE PASS — 3301 passed, 7 skipped, 64 warnings in 230.87s |
| 5 | `check_review_output_provenance.py --strict <this report>` | 0 | GATE PASS — no findings; `--selftest` run alongside to prove the checker fires (SELFTEST OK) |
| 5b | `check_review_summary.py --check <this report>` | 0 | GATE PASS — 0 findings, `templates/placeholders skipped: 0` |
| 5c | `check_retrieval_header.py <this report>` | 0 | GATE PASS — header shape clean |

Gate 5b is recorded because the first draft of this report's `review_summary`
block omitted `summary` and `next_action` and was therefore classified a
placeholder and silently skipped by the shape gate (`templates/placeholders
skipped: 1`). The block was rewritten to the canonical shape in
`.agents/workflow-overlay/communication-style.md`; the gate now inspects it and
reports 0 findings with 0 skips. A skipped block is not a passed block, so the
first result is not reported as a pass.

The 2 warnings in gate 3 are the pre-existing `datetime.utcnow()` deprecations
in `source_capture/tiktok/video_packet.py:276`, unrelated to this change and
consistent with the author's context. No test failed at any gate.

Gate 4 is the full harness suite required because source was patched. It also
closes the author-declared gap "current post-fast-forward full harness: not
rerun" — the suite is green at `d25ba56b` with the bio change plus this patch
applied.

**Stated limitation, per the prompt's instruction:** no gate executed the browser
JavaScript. `TIKTOK_SUGGESTED_ACCOUNTS_DOM_EXTRACT_SCRIPT` and its fallback are
Python string constants here; every test drives Python with a fake engine and
hand-authored `dom_observation` dicts. Nothing in this validation observed
`document.querySelector('[data-e2e="user-bio"]')` against any DOM, real or
simulated. F1 is confirmed because it is a pure-Python merge defect that the
suite can reach; F2 and F3 live in the unexercised JavaScript, which is exactly
why I report them rather than patch them.

## Residual risks and untested paths

- **Reviewer-authored hunks are not independently reviewed.** The F1 patch and
  its test were written by this reviewer and reviewed by no one. Returned to the
  commissioning lane as a named residual, per the prompt.
- **F2 is the material open risk**: if the live TikTok profile renders any
  earlier-in-document-order `[data-e2e="user-bio"]` node, the capture may bind a
  non-root bio or emit a false `visible_empty`, and nothing in this repo can
  currently detect that. F1's fix does not touch it.
- No live-site behavior is established for any route: primary, fallback, or
  merge. The merge fix is proven only against fabricated `dom_observation`
  dicts.
- Bio carriage into `raw/04_tiktok_suggested_accounts_attempt.json` is proven
  structurally (raw-byte pass-through), not by an assertion (F5).
- The `visible_empty` vocabulary question (F2, F6) may be a product decision
  about what the token is meant to assert, not purely a code defect.

## Use boundary

This review does not establish live-site correctness, TikTok DOM stability,
creator geography, primary audience geography, US-market fit, or Registry
priority/eligibility. The bio is evidence only; nothing in this change or review
infers anything downstream from it. These findings are decision input only. They
are not approval, not validation, not readiness, not mandatory remediation, and
not executor-ready patch authority until separately accepted or authorized by
the commissioning lane. A green gate here is not proof that the capture works
against the live site.

## Verdict

```yaml
verdict: issues_found
confirmed_defects_patched: 1 (F1 — major, empirically reproduced and closed)
reported_not_patched: 5 (F2 major; F3, F4, F5, F6 minor)
architecture_pass_needed: false
blocked: false
```

`NEEDS_ARCHITECTURE_PASS` is not raised: F2 needs a live-DOM-verified selector
pass inside the existing capture design, not new architecture, a new runtime, or
a product-model change. It does need authority this commission does not carry.

## Lifecycle statement

No commit, push, PR creation or modification, merge, stash, reset, clean,
worktree removal, or live TikTok capture was performed. The only writes to the
target worktree were: the two authorized files, this report, and a removable
write probe that was removed. Reviewer scratch (the merge probe script) lives
outside the repository in the session scratchpad. The dirty set is the
commissioned three paths plus this report.

## Next action

Return to the commissioning Codex lane (`codex/tiktok-onboarding-profile-bio`)
for adjudication of: the F1 hunk and its test (reviewer-authored, unreviewed);
whether F2 warrants a follow-up lane with live-capture authority before this
change is relied on for bio evidence; and whether F5 warrants a patch
authorization request for `test_tiktok_batch_admission.py`.

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/tiktok_profile_bio_capture_adversarial_code_review_v0.md
  review_location: durable_report
  reviewed_by: claude-opus-4-8
  authored_by: openai_gpt5_codex
  de_correlation_bar: cross_vendor_discovery
  verdict: issues_found
  recommendation: accept_with_friction
  summary: "One confirmed major merge defect silently replaced an observed fallback bio with absence and reported a false visible_empty; it is patched and covered by a new regression test, while the unscoped presence-only bio selector remains an open live-DOM risk this commission could not close."
  findings_count: 6
  blocking_findings:
    - "F1: primary bio absence destroyed observed fallback bio evidence (patched; reviewer hunk needs adjudication)"
  advisory_findings:
    - "F2: unscoped presence-only bio selector; visible_empty asserts unchecked visibility (needs live-DOM pass)"
    - "F3: innerText/textContent fallback can drop internal line breaks"
    - "F4: token-shaped bio text would abort the whole receipt build"
    - "F5: Bronze bio carriage structural, not asserted (outside patch authority)"
    - "F6: missing bio keys reported as not_visible"
  prior_findings_remediated: []
  next_action: "Adjudicate the F1 hunk and its test in the commissioning Codex lane, then decide whether F2 needs a follow-up lane with live-capture authority before this change is relied on for bio evidence."
  validation_full_harness: "3301 passed, 7 skipped, 230.87s, exit 0"
  validation_tiktok_tests: "352 passed, 2 pre-existing warnings, exit 0"
  validation_focused_tests: "50 passed, exit 0"
  validation_javascript_executed: false
  lifecycle_actions_taken: none
```
