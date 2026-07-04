# Creator Registry Match Preflight Enforcement — Adversarial Code Review + Bounded Patch (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + bounded patch record (docs/review-outputs/)
scope: >
  Durable record of the commissioned code-implementation review of the Creator
  Registry match preflight enforcement lane (exact-match duplicate-prevention
  turnstile between discovery and new social creator capture), run via the
  `workflow-code-review` lane per
  docs/prompts/reviews/creator_registry_match_preflight_enforcement_adversarial_code_review_prompt_v0.md,
  and the bounded patch applied for the one confirmed critical defect.
use_when:
  - Checking what the preflight enforcement review found and what was patched.
  - Citing the review-routing disposition for this code-root change.
authority_boundary: retrieval_only
review_provenance:
  reviewed_by: Anthropic claude-sonnet-5
  authored_by: unrecorded
  de_correlation_bar: not_applicable_direct_commission
  same_vendor_rationale: >
    This is a direct `workflow-code-review` invocation via a filed review
    prompt, not a `workflow-delegated-review-patch` commission, so the
    two-bar de-correlation classification (owned by
    .agents/workflow-overlay/delegated-review-patch.md) does not bind here.
    Recorded as a gap, not force-classified.
review_use_boundary: >
  Findings, evidence, and the applied patch are decision input only — not
  approval, validation, mandatory remediation, readiness, or patch authority.
  The home/CA lane adjudicates whether the applied patch is kept.
```

## Commission

- Prompt source: `docs/prompts/reviews/creator_registry_match_preflight_enforcement_adversarial_code_review_prompt_v0.md`.
- Target workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-preflight-enforcement`.
- Target branch: `codex/creator-registry-preflight-enforcement`.
- Base: `origin/main`.
- Review lane: code implementation review, invoked via `workflow-code-review`.
- Edit permission: bounded patch-only inside the submitted worktree scope; no commit/push/merge/PR action taken.

## Target Confirmation

- HEAD at review start: `8800e9cfe4f924c854df1ff5e74382dd70ac84d4` on `codex/creator-registry-preflight-enforcement`.
- Dirty state at review start: clean (`git status --porcelain` empty).
- Diff vs `origin/main` at review start: 5 files, 1003 insertions — matched the expected target files (candidate registry_match_preflight.py, run_creator_registry_match_preflight.py, its unit test, the usage note, and this review prompt itself).
- All required source/authority reads completed: `AGENTS.md`; `.agents/workflow-overlay/README.md`, `decision-routing.md`, `validation-gates.md`, `review-lanes.md`; the registry usage note; `registry_match_preflight.py`; `run_creator_registry_match_preflight.py`; both named unit test files. The registry JSON view (325.7KB) exceeded single-read size and was instead confirmed via targeted `grep` for the relevant public_handle/public_profile_url shapes and via the passing static-view unit tests.

## Review Scope

In scope: exact-match preflight logic in `registry_match_preflight.py`, its runner, its usage note, and its unit tests, judged against the intended MGT v0 enforcement contract in the commission prompt (exact-JSON-only matching, block `new_capture` on existing match, fail-closed ambiguity, in-batch duplicate rejection, no fuzzy/cross-platform/live/LLM/mutation capability). Out of scope (read-only, not touched): the registry view materializer, ideal-audience snapshot code, and all overlay/doctrine files.

## Findings

### F1 — CRITICAL — non-profile share/short-link URLs derived a false identity handle, producing a false "safe to capture" result — **PATCHED**

- Location: `registry_match_preflight.py`, `_handle_from_url` (pre-patch, no reserved-path or `@`-prefix guard for Instagram/TikTok).
- Evidence (red, pre-patch, live run against the real committed registry):
  - Candidate `https://www.instagram.com/p/Cxxxxxxxxxx/` (platform `instagram`, `intended_action: new_capture`) → `decision: new_candidate`, `can_start_new_capture: true`, runner exit `0`. The derived "handle" was the literal path segment `"p"` — Instagram's post-permalink share-link marker, not a username.
  - Candidate `https://vm.tiktok.com/ZMabcdEFGH/` (no explicit platform; inferred `tiktok`) → same `new_candidate` / `can_start_new_capture: true` / exit `0`. The derived "handle" was the short-link code `zmabcdefgh`.
  - Both are exactly the failure mode the commission prompt names as high-value: an already-known creator's post/share link could be misclassified as a brand-new candidate, allowing a duplicate `new_capture` to proceed — the one thing this turnstile exists to prevent.
- Authority/evidence basis: registry-fixture inspection (`grep` confirmed `public_profile_url` is always stored as the base profile page, e.g. `https://www.instagram.com/hyram/`, never a post/share/short-link form) plus the commission's own named failure mode ("a known profile URL/handle/account id fails to match because normalization is wrong").
- Impact: false-negative duplicate detection — a `new_capture` for a share-link candidate that actually belongs to an existing registered creator would be silently permitted.
- `minimum_closure_condition`: URLs whose path shape cannot resolve to a real profile handle (Instagram reserved path segments; TikTok/short-link paths not starting with `@`) must not silently derive a handle, and should fail closed (`invalid_candidate`) rather than pass as `new_candidate`.
- Fix applied: `_handle_from_url` now rejects Instagram reserved first-path-segments (`p`, `reel`, `reels`, `tv`, `stories`, `explore`, `accounts`, `direct`, `developer`, `about`, `legal`, `api`, `embed`) and requires TikTok's first path segment to start with `@` (mirroring the already-conservative YouTube channel-URL handling). A new helper `_is_non_profile_url_shape` flags these same shapes as a per-candidate `unresolvable_profile_url` error, so the candidate now resolves to `decision: invalid_candidate` / `action_status: blocked` instead of a false `new_candidate`.
- Verification (same-check red→green): re-ran the identical two probe candidates against the identical registry after the patch — both now return `decision: invalid_candidate`, `action_status: blocked`, `can_start_new_capture: false`, runner exit `2`. Locked in with three new unit tests (`test_instagram_post_permalink_does_not_derive_a_bogus_handle`, `test_tiktok_short_link_does_not_derive_a_bogus_handle`, `test_tiktok_profile_url_with_handle_still_matches` — the last proves legitimate `@handle` TikTok profile URLs still resolve and still correctly reach `new_candidate`/allowed for a genuinely new candidate). All 10 tests in the target suite pass; the full validation-gate set below is green after the patch.
- `next_authorized_action`: none — closed by this review under the commission's bounded patch scope. No architecture change was required (no fuzzy resolver, no live lookup, no schema change); this only tightens exact-URL-to-handle normalization.
- `patch_queue_entry`: not applicable — this is a direct bounded-patch review lane per the commission (`Edit permission: bounded patch-only`), not a patch-queue review; the patch was applied directly with red→green proof, not queued for a separate executor.

### F2 — MAJOR — a single structurally malformed candidate aborts receipt generation for the entire batch, including other valid candidates — **NOT PATCHED (owner decision needed)**

- Location: `registry_match_preflight.py`, `_normalize_candidate` — `_reject_unknown_keys` (unknown candidate key), the `candidate_id` extraction, and the `intended_action` extraction/enum check all raise `ValueError` directly, unlike every other structural problem in the same function (e.g. `unsupported_platform`, `unsupported_profile_url_host`, `missing_identity_key`), which are appended to a per-candidate `errors` list and resolve to a per-row `invalid_candidate` decision.
- Evidence (red, live run): a two-candidate batch — one well-formed `new_capture` candidate plus one candidate with a typo'd `intended_action: "new_captur"` — produced **no receipt at all**: `creator registry match preflight failed: intended_action must be one of ['classify', 'new_capture', 'update_existing']`, runner exit `2`. Nothing was written even for the sibling well-formed candidate, and the exception message does not identify which candidate (no `candidate_id` or index) caused the failure.
- Authority/evidence basis: the usage note (`creator_registry_match_preflight_usage_v0.md`) documents `invalid_candidate` as a per-candidate receipt outcome ("fix the candidate input before capture") with no carve-out for structural fields; the commission prompt separately names "tests prove the dangerous paths, not only happy paths" and this exact path (missing/invalid required fields, unknown keys) has no test coverage in either direction.
- Impact: this is fail-closed, not fail-open (no unsafe capture is enabled), so it is not a safety hole on its own. But it silently denies processing of every other candidate in the same scan batch whenever one row is malformed, contradicts the documented per-row `invalid_candidate` contract, and its diagnostics don't name the offending row.
- `minimum_closure_condition`: an owner-decided remediation shape — either (a) convert these three structural checks into per-candidate soft errors consistent with the rest of the function (schema-shape change: `intended_action` and `candidate_id` could then carry off-enum/placeholder values in the receipt for an `invalid_candidate` row), or (b) keep the whole-batch-abort design but make the exception message name the offending candidate index/id. Both are legitimate; (a) changes the receipt's documented value-shape contract for these two fields and deserves owner sign-off rather than an unreviewed patch under this bounded-patch scope.
- `next_authorized_action`: owner decision on remediation shape, or `patch_before_acceptance` once a shape is chosen.
- Not patched: this was left unpatched because both viable fixes touch the receipt's documented field-shape contract (option a) or are a smaller diagnostics-only change (option b) with materially different scope — a judgment call outside "the correct fix requires no architecture change and has one clear shape," which F1 satisfied but this does not.

### F3 — MINOR (optional hardening) — `platform_account_id` registry index key is not platform-namespaced

- Location: `registry_match_preflight.py`, `_registry_identity_keys` — the `platform_account_id:{id}` key has no platform prefix, unlike the sibling `platform_handle:{platform}:{handle}` and `platform_public_account_id:{platform}:{id}` keys.
- Evidence/authority basis: static code reading of `_registry_identity_keys`; not exercised by a failing test (no cross-platform ID collision exists in the current 33-profile fixture — YouTube channel IDs are `UC…`-prefixed, Instagram/TikTok native IDs are distinct numeric formats in practice).
- Impact: theoretical only — a platform-native account ID that happened to collide in value across two different platforms would incorrectly merge into a single registry match. No live evidence this is a foreseeable production risk given the ID formats observed.
- `minimum_closure_condition`: namespace this key by platform for consistency with its siblings, if/when cross-platform ID collision becomes a real concern.
- `next_authorized_action`: none required now; optional hardening, not a blocker.

## Validation (all gates re-run after F1's patch, on the current working tree)

| Gate | Command | Result |
|---|---|---|
| GATE PASS | `python -m py_compile registry_match_preflight.py run_creator_registry_match_preflight.py` | exit 0 |
| GATE PASS | `python -m pytest -q tests/unit/test_creator_registry_match_preflight.py` | 10 passed (7 pre-existing + 3 new) |
| GATE PASS | `python -m pytest -q tests/unit/test_creator_profile_current_static_view.py` | 19 passed |
| GATE PASS | `python runners/run_creator_profile_current_materialize.py --check` | up to date, exit 0 |
| GATE PASS | `python -m pytest -q tests/contract/test_no_llm_imports.py` | 1 passed |
| GATE PASS | `python .agents/hooks/check_retrieval_header.py --changed --strict` | exit 0 |
| GATE PASS | `python .agents/hooks/header_index.py --strict --base origin/main` | OK — 1 changed durable `.md` file, headers present, map-reachable |
| GATE PASS | `python .agents/hooks/check_map_links.py --strict` | OK (0 findings; 33 pre-existing nonresolving annotations, debt not failures) |
| GATE PASS | `python .agents/hooks/check_review_routing.py --strict --base origin/main` | OK |
| GATE PASS | `git diff --check origin/main..HEAD` | exit 0 |

All ten commanded gates were run; none were skipped.

## Patch Summary

Two files patched, both inside the authorized patch scope:

- `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py`: tightened `_handle_from_url`, added `_is_non_profile_url_shape` and the `unresolvable_profile_url` error path (F1).
- `orca-harness/tests/unit/test_creator_registry_match_preflight.py`: added three regression tests locking in F1's fix.

`orca-harness/runners/run_creator_registry_match_preflight.py` and the usage note were reviewed but not touched — no defect was found in either.

No commit, push, merge, or PR action was taken; the patch remains uncommitted in the target worktree per the bounded edit-permission scope.

## Residual Risks

- F2 (batch-abort-on-malformed-candidate) remains open — fail-closed, not a safety hole, but an untested code path and a documented-contract mismatch.
- F3 (platform_account_id namespacing) remains open as optional hardening.
- The Instagram reserved-path list in F1's fix is a fixed allowlist of currently-known Instagram system paths; if Instagram introduces a new reserved top-level path in the future, that specific new path would not yet be excluded (the `@`-prefix / registry-exact-URL match still applies as a fallback safety net, so this is a narrowing-only residual, not a regression versus pre-patch behavior).

## Owner Decisions Needed

- Choose a remediation shape for F2 (or accept the current whole-batch-abort behavior as intentional and only improve its diagnostics).

## Review Use Boundary

This report's findings, applied patch, and validation evidence are decision input only. They are not approval, validation, mandatory remediation, deployment readiness, or patch authority. They also are not a claim that F2/F3 are acceptable to leave open - that is an owner call. recommendation: patch_before_acceptance (see courier below) reflects F2 being open, not a rejection of the applied F1 patch.

## Home / CA Adjudication Addendum

This section was added by the home/CA lane after receiving the delegated review return. It is not part of the original reviewer-authored finding text above.

- F1 disposition: accepted and kept. The false-safe-to-capture URL-shape bug was real, bounded to exact URL normalization, and the delegated patch matches the minimum closure condition.
- F2 disposition: accepted as material and patched before acceptance. The chosen remediation is per-row soft failure: malformed candidate rows now produce blocked `invalid_candidate` receipt rows with `invalid_candidate_shape` diagnostics, while sibling valid rows still receive decisions in the same receipt. Document-level errors still fail the run.
- F3 disposition: deferred as optional hardening. `platform_account_id` remains non-platform-namespaced because current registry IDs are internally global-style IDs and no live collision exists; revisit only if raw external platform IDs enter that field or a collision appears.

Post-adjudication validation observed by the home/CA lane on this working tree:

- `python -m py_compile orca-harness\capture_spine\creator_profile_current\registry_match_preflight.py orca-harness\runners\run_creator_registry_match_preflight.py` — exit 0.
- `python -m pytest -q orca-harness\tests\unit\test_creator_registry_match_preflight.py` — 12 passed.
- `python -m pytest -q orca-harness\tests\unit\test_creator_profile_current_static_view.py` — 19 passed.
- `python orca-harness\runners\run_creator_profile_current_materialize.py --check` — up to date.
- `python -m pytest -q orca-harness\tests\contract\test_no_llm_imports.py` — 1 passed.
- `git diff --check origin/main..HEAD` — exit 0.

Remaining accepted residual: exact-match preflight still does not do fuzzy duplicate detection, cross-platform identity proof, live social search, metric refresh, or registry mutation; F3 stays optional, not blocking.
