# TikTok Zero-Wheel React Subtitle Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Cross-vendor delegated adversarial code review-and-patch return for the
  bounded TikTok zero-wheel overlay React subtitle-source repair.
use_when:
  - Adjudicating the delegated findings and returned hunks before keep.
  - Resuming AK Fragrance onboarding after adjudication.
authority_boundary: retrieval_only
```

## Commission, target, and authority

```yaml
commission: delegated_code_review_and_patch (repo access mode)
target_worktree: C:\tmp\orca-tt-react-subs-20260715
target_branch: codex/tiktok-zero-wheel-react-subtitles
target_head: 1ebcf4b6842052f824bf09c21b74e24fe593dd64
patchable_scope:
  - forseti-harness/source_capture/tiktok/live_batch_probe.py
  - forseti-harness/tests/unit/test_tiktok_live_batch_probe.py
everything_else: read-only / flag-only
review_method: workflow-code-review applied to the bounded dirty diff
lifecycle_actions_taken: none (no commit, push, PR, merge, stash, reset, or hygiene)
```

Fresh target-state read before source loading observed the expected branch and
HEAD, exactly the three allowed dirty paths and no extras, and both commissioned
target hashes (`a1c7e1b0...`, `b5aa81ed...`). Direct write capability was proved
by a write-and-remove probe in the target worktree; `codex/tiktok-zero-wheel-react-subtitles`
was checked out in exactly one worktree and no `index.lock` was present.

## Provenance and de-correlation

```yaml
reviewed_by: claude-opus-4-8
authored_by: openai_gpt5_codex
de_correlation_bar: cross_vendor_discovery
author_vendor: OpenAI
controller_vendor: Anthropic
de_correlation_status: satisfied (author vendor != controller vendor, observed)
boundary: who-constraint only; not a runtime-model recommendation or selection.
```

## Behavior criteria applied

The frozen contract in the commission: overlay-only React read for an exact path
video-ID match; source priority `item_struct` -> exact overlay React video info
-> exact profile item-list metadata -> matched visible DOM track; `item_struct_present`
stays hydration-only with distinct `overlay_react_video_info` provenance; raw
subtitle URLs stay ephemeral; unsupported hosts stay a loud rejection with no
fallthrough; identity mismatch fails closed; no-URL videos keep the honest
non-attempt outcome; comments, cadence, blocker triage, and the direct route do
not regress.

## Findings

### F1 — Unguarded React walk can destroy the entire DOM extract

```yaml
severity: critical
confidence: medium
file: forseti-harness/source_capture/tiktok/live_batch_probe.py
evidence_lines: "53-54 (script shape), 227 (pre-patch call site), 643 and creator_onboarding.py:1664 (shared consumers)"
status: patched
```

`TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT` is a single arrow function with no exception
containment anywhere. Pre-patch, `findReactVideoSubtitleSource()` was called
unconditionally at line 227 — after comment candidates, overlay detection,
subtitle tracks, and blocker-triage inputs were computed, but before the return
object was constructed. Any throw inside the new walk therefore discarded the
whole extract, not just the subtitle enrichment.

The walk reaches throwing surfaces: `Object.entries(value)` invokes getters on
own enumerable properties, and the walk descends into DOM nodes (see F2), where
properties such as an iframe's `contentWindow` raise `SecurityError` under
cross-origin access. F1 and F2 compound — the fiber escape is what carries the
walk to those surfaces.

This is a regression of a frozen criterion: comment admission, cadence, and
blocker triage must not regress. The blast radius is not the probe alone —
`creator_onboarding.py` imports and runs the same script in the production
onboarding path.

- `minimum_closure_condition`: a failure inside the optional React subtitle
  enrichment cannot prevent the extract from returning its other fields.
- `next_authorized_action`: adjudicate the returned hunk.

### F2 — Walk escapes the open overlay via React fiber references

```yaml
severity: major
confidence: medium
file: forseti-harness/source_capture/tiktok/live_batch_probe.py
evidence_lines: "209-221 (pre-patch child enumeration), 174-175 (overlay seed set)"
status: patched
```

Pre-patch, child enumeration excluded only `_owner`, `memoizedState`,
`updateQueue`, and functions. React 17+ attaches `__reactFiber$<key>` and
`__reactProps$<key>` to DOM nodes as own enumerable properties, so the walk could
reach a fiber and then climb `return` / `alternate` / `stateNode` to parent
fibers and their `memoizedProps` — objects outside `overlayRoot`. A reachable
path within the depth-12 cap: props -> `children` -> element -> `ref` ->
`{current: DOMNode}` -> `__reactFiber$` -> `return` -> `memoizedProps`.

This contradicts the frozen criterion that React metadata may be read "only from
the currently open overlay". The harm is bounded rather than open: the exact
path-ID equality check still prevents cross-video and cross-creator reuse, so
this is a false boundary claim and an unbounded-traversal surface rather than an
observed data-mixing defect.

- `minimum_closure_condition`: the walk cannot traverse outside the open
  overlay's React props.
- `next_authorized_action`: adjudicate the returned hunk.

### F3 — The JS walk has no test coverage at all

```yaml
severity: major
confidence: high
file: forseti-harness/tests/unit/test_tiktok_live_batch_probe.py
evidence_lines: "3174-3299 (new tests stub dom_observation directly)"
status: not_patched
```

Both new tests inject `react_video_subtitle_source` as an already-formed Python
dict into `capture.dom_observation`. They exercise the Python selection,
sanitization, and identity re-check — genuinely, including a real fetch
(`fetched_urls == [subtitle_url]`), a real WebVTT parse (`cue_count == 1`), and
URL absence from serialized output. They do not execute a single line of
`findReactVideoSubtitleSource`.

The ~80 new JS lines carry all the risk in this repair — shape binding, cycles,
depth, object budget, getters, exceptions, overlay boundary — and are the only
part with zero automated coverage. F1 and F2 were both found by reading, not by
a failing test, and no test in the suite would have caught either.

Not patched: proving the walk needs a JS runtime and a representative React
overlay fixture. No such harness exists (the script is referenced only from
source, never from tests), so building one falls outside the two named files.

- `minimum_closure_condition`: the JS walk is exercised against a representative
  React overlay fixture covering shape binding, a cycle, depth and budget
  exhaustion, a throwing getter, and the overlay boundary.
- `next_authorized_action`: owner decision on test-infrastructure scope; this
  needs an off-scope file and is not a delegate-side expansion.

### F4 — `videoInfo` special-case can hijack the identity check

```yaml
severity: minor
confidence: medium
file: forseti-harness/source_capture/tiktok/live_batch_probe.py
evidence_lines: "190-199"
status: not_patched
```

`candidate` becomes `value.videoInfo` whenever that property is an object, and
both the ID and `subtitleInfos` are then read from `candidate` only. Two shapes
miss: if `value` carries the id and `subtitleInfos` but also has any `videoInfo`
object, `value` itself is never evaluated as a candidate (it is marked in
`seenObjects` and only its children are pushed); and if `videoInfo` holds
`subtitleInfos` while the id lives on the enclosing object, `candidateId` is
empty and never matches. Only a shape with id and `subtitleInfos` on the same
object matches.

The special-case also adds no reach the walk lacks — `value.videoInfo` is pushed
as a child and visited on a later iteration regardless — so it contributes only
the hijack risk.

Not patched deliberately: the commission records a live read-only check that
bound the exact ID and found one subtitle record on video `7659469523459902753`,
so the shipped shape demonstrably matches today. Changing candidate selection
without a real React fixture risks breaking an observed-working path to close a
hypothetical one, which the returned diff should not do.

- `minimum_closure_condition`: candidate selection evaluates `value` and
  `value.videoInfo` independently, or evidence records that TikTok's `videoInfo`
  always carries the video id.
- `next_authorized_action`: owner decision.

### F5 — JS field allowlist drops a URL casing Python accepts

```yaml
severity: minor
confidence: high
file: forseti-harness/source_capture/tiktok/live_batch_probe.py
evidence_lines: "152-161 (allowlist), 2667 and 2565 (Python readers)"
status: not_patched
label: optional hardening, non-required
```

`reactSubtitleFields` allows `Url` and `url` but not `URL`, while
`_subtitle_url_from_item_struct` and `_sanitize_subtitle_infos` both read `URL`
as a valid casing. A `URL`-cased React record would be silently stripped at the
JS boundary and degrade to the no-metadata outcome. This is an internal
inconsistency between the two layers, not a speculative future shape — but no
evidence records TikTok emitting that casing, so it is labeled optional and
non-required rather than patched.

- `minimum_closure_condition`: the JS allowlist and the Python URL readers agree
  on the accepted casings.
- `next_authorized_action`: owner decision.

### F6 — React identity validation runs before higher-priority sources

```yaml
severity: minor
confidence: high
file: forseti-harness/source_capture/tiktok/live_batch_probe.py
evidence_lines: "2459-2462, 2483-2499"
status: not_patched
```

`_subtitle_source_from_dom_react_state` is evaluated eagerly at the top of
`_select_subtitle_source`, so a mismatched React id raises `ValueError` and
aborts the entire batch run — every remaining video included — even when
`item_struct` (priority 1) would have supplied the subtitle without consulting
React at all.

This is loud and fail-closed, which the frozen contract requires, and it mirrors
the existing profile-grid rejection shape, so it is consistent with accepted
behavior rather than new drift. Practically it fires only on serialization drift
or tampering, because the JS returns a record only when `candidateId ===
expectedVideoId`. Reported for coverage, not patched.

- `minimum_closure_condition`: an owner decision records whether whole-run abort
  is the intended blast radius for a mismatch on a non-winning source.
- `next_authorized_action`: owner decision.

## considered_and_defended

- Raw subtitle URL leaking into cadence results or admitted packets — defended:
  `_select_subtitle_source` returns the source dict, but the row embeds only
  `_sanitize_subtitle_infos(...)` (line 2564-2566 maps a URL to
  `url_present_but_redacted`) and `_subtitle_capture_from_item_struct` (lines
  2601-2607 emit only host, sha256, and length). `assert_no_sensitive_tiktok_material`
  guards each return path, and the new test asserts `subtitle_url not in json.dumps(result)`.
- Unsupported-host fallthrough to a lower-priority supported source — defended:
  lines 2476-2477 return the first source carrying any URL, so an unsupported-host
  React URL returns the React source and is rejected at lines 2609-2612 before any
  fetch; it cannot silently fall through.
- Metadata present but no usable URL — defended: `first_metadata_source` (lines
  2470-2479) preserves the honest non-attempt outcome rather than skipping to a
  lower-priority source.
- `item_struct_present` provenance drift — defended: line 1839 still derives it
  from `item_struct` alone; React provenance is the distinct
  `overlay_react_video_info` label at line 2466.
- Cycles and unbounded traversal — defended: a `seenObjects` WeakSet (lines
  187-188), a depth cap of 12 (line 186), and a 12000-object budget shared across
  all nodes (lines 176, 189).
- Exact-ID check lost after serialization — defended: independently re-checked in
  Python at lines 2493-2498 against the caller-supplied `expected_video_id`.
- Public-call compatibility and direct-route drift — defended:
  `_select_subtitle_source` is private with a single caller (line 1775) that
  passes `expected_video_id`; the direct route (lines 1781-1794) is untouched.

## Returned diff

Working-tree edits authored by this review, isolated from the author's hunks
(generated by reconstructing the pre-review file and diffing it against the live
file):

```diff
@@ -211,11 +211,16 @@ TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT = r"""
               key === '_owner' ||
               key === 'memoizedState' ||
               key === 'updateQueue' ||
+              key.startsWith('__reactFiber$') ||
+              key.startsWith('__reactProps$') ||
               typeof child === 'function'
             ) {
               continue;
             }
-            if (child && typeof child === 'object') {
+            if (
+              child && typeof child === 'object' &&
+              !(typeof Node === 'function' && child instanceof Node)
+            ) {
               stack.push({value: child, depth: depth + 1});
             }
           }
@@ -224,7 +229,12 @@ TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT = r"""
     }
     return null;
   };
-  const reactVideoSubtitleSource = findReactVideoSubtitleSource();
+  let reactVideoSubtitleSource = null;
+  try {
+    reactVideoSubtitleSource = findReactVideoSubtitleSource();
+  } catch (error) {
+    reactVideoSubtitleSource = null;
+  }
   return {
     hydration_json_text: hydration ? hydration.textContent : null,
     visible_comment_candidates: candidates,
```

Per-change neutral citations:

- Hunk 1 (F2) — React 17+ assigns `__reactFiber$<key>` and `__reactProps$<key>`
  to DOM nodes as own enumerable properties; the pre-patch exclusion list at
  lines 210-217 covered `_owner`, `memoizedState`, `updateQueue`, and functions
  only. The seed set at lines 174-175 is `overlayRoot` plus its descendants; the
  frozen contract binds the read to the currently open overlay.
- Hunk 2 (F1) — the script is one arrow function opened at line 54 with no
  `try` anywhere pre-patch; the call site sat at line 227 ahead of the return
  object at lines 228-242; `creator_onboarding.py:1664` passes the same script
  constant. `null` is the value the function already returns on every
  no-match path (line 225), and `_subtitle_source_from_dom_react_state` maps a
  falsy value to `None` (lines 2488-2492), preserving the existing honest
  non-attempt outcome.

## Validation evidence

Run from `C:\tmp\orca-tt-react-subs-20260715\forseti-harness` after the review
edits. Observed exit codes, not assumed:

```yaml
gate_1_focused:
  command: pytest tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_tiktok_live_batch_probe.py -q
  observed: 105 passed
  exit: 0
  state: GATE PASS
  author_baseline: 105 collected and passed, exit 0 -- matches
gate_2_all_tiktok_unit:
  command: pytest <rg-selected test_tiktok_*.py> -q
  observed: 339 passed, 2 datetime deprecation warnings
  exit: 0
  state: GATE PASS
  author_baseline: 339 passed, exit 0, two existing datetime deprecation warnings -- matches
gate_3_full_harness:
  command: pytest -n 4 --dist=loadfile
  observed: 3298 passed, 7 skipped, 67 warnings in 120.68s
  exit: 0
  state: GATE PASS
  author_baseline: 3,298 passed, 7 skipped, 67 warnings, exit 0 -- matches
gate_4_diff_check:
  command: git diff --check
  observed: no output
  exit: 0
  state: GATE PASS
live_overlay_check:
  state: NOT RUN
  reason: >
    The commission authorizes no extra wheel, direct-video navigation, or second
    acquisition route, and a live re-check was not commissioned to the delegate.
    The author-observed live result is inspected as evidence, not reproduced.
```

The gates constrain the diff; they do not prove the repair correct. Gate 3
matching the author's baseline exactly shows the returned hunks introduce no
regression across the harness — it does not exercise the JS walk (F3).

## Verdict

```yaml
verdict: issues_found
patched: [F1, F2]
reported_only: [F3, F4, F5, F6]
architecture_pass_required: no
```

`NEEDS_ARCHITECTURE_PASS` is not returned: F1 and F2 were closable wholly inside
the named target file, and the remaining findings are bounded reports or an
owner-scope test-infrastructure question, not a broken design.

## Residual risks

- The returned hunks are not adjudicated. Nothing here is kept until the
  commissioning Chief Architect adjudicates the findings, diff, and verdict.
- F1 and F2 are patched but unproven by test. The suite cannot execute the JS
  walk (F3), so their closure rests on reading the code, not on a failing test
  turning green. Gate 3 shows only that they break nothing else.
- F1 confidence is medium on trigger, not on blast radius. That an overlay
  property getter actually throws in production is inferred from the reachable
  surfaces, not observed; the consequence if it does throw is confirmed by the
  script's structure.
- F4 is knowingly left open. The shipped candidate selection is fragile to React
  shape drift but is observed working; a TikTok-side shape change would degrade
  it to the honest non-attempt outcome rather than to wrong data.
- **Working-tree byte identity of the patched file no longer reproduces the
  commissioned hash, and this was caused by this review, not by the author.**
  The commissioned files were mixed-EOL (the untouched test file still measures
  3506 CRLF plus 131 bare LF and still hashes to `b5aa81ed...`). The edit tooling
  rewrote `live_batch_probe.py` to uniform CRLF, so it now hashes to
  `beb042c144bf967c5f11a3a0026eec4aec47e51aa3f5e5327c5254808dad66af` rather than
  `a1c7e1b0...`, and re-deriving the original mixed-EOL bytes is not possible.
  Content impact is none and this is verifiable: `core.autocrlf=true` and
  `live_batch_probe.py` matches no `-text` or `eol=lf` rule in `.gitattributes`,
  so git normalizes on staging; the repo-visible insertion count moved from 105
  to 115, exactly the 10 lines this review added, with no line-ending noise and
  no other path touched. A commit stores LF either way. Adjudication should use
  the git-normalized diff rather than a re-hash for this file.
- Cross-vendor discovery covers the author's diff, but this review authored its
  own two hunks, and that sliver is not independently reviewed here.

## Review-use boundary

The findings, returned diff, and verdict in this report are decision input only.
They are not approval, not validation, not readiness, not mandatory remediation,
and not executor-ready patch authority. The commissioning Chief Architect decides
what is kept, may veto any hunk it judges to add no benefit, and owns all
lifecycle state; this review advanced none.
