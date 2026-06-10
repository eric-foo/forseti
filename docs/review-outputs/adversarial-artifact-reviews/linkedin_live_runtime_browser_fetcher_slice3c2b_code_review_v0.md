```yaml
retrieval_header_version: 1
artifact_role: Review-output record (cross-vendor code review + home-model adjudication)
scope: >
  Durable audit record of the adversarial CODE review of slice 3c-2b -- the real
  attended LinkedIn BrowserFetcher: the CdpAttachBrowserDriver live edge, the
  rendered-DOM -> CompanySignal extractor, and the clean-bag BrowserFetcher onto the
  committed Fetcher seam. One cross-vendor round, NO-REPO (portable bundle). Advisory;
  not a verdict.
authority_boundary: retrieval_only
reviewed_artifact: >
  capture_spine/linkedin_live_runtime/{extractor,browser_driver,fetcher,__init__}.py
  + tests/unit/test_linkedin_live_runtime_browser_fetcher.py
input_bundle: >
  docs/review-outputs/linkedin_live_runtime_browser_fetcher_slice3c2b_v0_no_repo_review_bundle.zip
  (zip sha256 3928c76be6c63c9cb096e81b6c336004e17e33c0229324413d18e3a96519d98d; reviewer
  confirmed every review-target + gate-context artifact matched its listed SHA256). The
  bundle is the AS-REVIEWED (pre-patch) snapshot; the working tree was patched after, per
  the accepted findings below.
implements: docs/product/data_capture_spine_linkedin_live_layer_architecture_v0.md (slice 3c-2b)
provenance:
  authored_by: anthropic/claude-opus-4.x
  reviewed_by: openai/gpt-5.5 (advisory, no-repo; de-correlated different vendor)
  same_vendor_recheck: not_run (cross-vendor pass + home-model adjudication + 160 lane tests)
  de_correlation_bar: cross_vendor_discovery
  method_pins: adversarial_artifact_review_v0.md@5fc263a1, review-lanes.md@43b1793d (freshness-gated current)
```

# LinkedIn live-runtime BrowserFetcher slice 3c-2b — Cross-Vendor Code Review + Adjudication (v0)

## What 3c-2b is
The real attended **BrowserFetcher** — the only path that turns a logged-in LinkedIn
company page into a minimized candidate row. `CdpAttachBrowserDriver` (the only live part;
owner-validated, not unit-tested) attaches over CDP to the owner's running browser →
`extract_company_signal` (rendered DOM → `CompanySignal`, offline) → `BrowserFetcher.fetch`
assembles a clean bag → `run_live_capture` minimizes (default-deny) + validates + projects.
Posture: owner-present attended automation, owner-accepted POC-risk, ToS-gray, NOT
legally-defensible.

## Outcome
4 findings (3 major, 1 minor). **All 4 accepted + applied.** One (F2) was accepted but the
reviewer's proposed mechanism was **corrected** by the home model (their ambiguity check sat
in `handle_endtag`, which the start-tag capture guard prevents from ever firing; moved to
`handle_starttag`). Three reviewer non-findings (regex subset, validation-before-import,
synthetic fixture) confirmed. No `NEEDS_ARCHITECTURE_PASS`. **160 lane tests pass** (was 152;
−1 stale parametrize case, +9 distinguishing tests).

| # | Sev | Finding (GPT-5.5) | Adjudication + fix |
|---|-----|-------------------|--------------------|
| F1 | major | Blocked-region tracking is depth-only, not tag-aware: an unmatched end tag inside `org-top-card-secondary-content`/`social-proof` can drive `_blocked_depth` to 0 and leak later person/connection content. | **ACCEPT (applied).** Replaced the depth counter with a tag-aware **stack**: only a matching end tag exits the region; unmatched end tags are ignored (over-block malformed DOM rather than leak). Test `test_blocked_region_tag_stack_survives_malformed_end_tags` distinguishes the fix (planted in-region info-item → `info_items == []`). |
| F2 | major | Fail-closed recognition too weak: a lone title class (no info-list, or a duplicate title) still mints a partial capture. | **ACCEPT (applied, mechanism corrected).** `extract_company_signal` now requires the display name AND a non-empty summary info-list AND no second top-card title → else `None`. Ambiguity is detected at **start-tag** time (the reviewer's end-tag placement could not fire under the capture guard). Tests: title-without-info-list → None; duplicate-title → None. |
| F3 | major | `cdp_endpoint` only checked non-empty: embedded credentials / unsupported scheme / remote host ride into `connect_over_cdp`, violating the clean-attach (no-credential, owner's-local-browser) posture. | **ACCEPT (applied).** Added `_validate_cdp_endpoint` (at construction): scheme ∈ {http,https,ws,wss}, netloc present, **no embedded credentials**, host ∈ {localhost,127.0.0.1,::1}. Tests reject creds/remote/bad-scheme; accept clean local. |
| F4 | minor | `BrowserFetcher` stores the raw `target` in `observed_source_locator` and trusts the injected driver to validate — a permissive driver could land a credentialed URL in the "clean" bag. | **ACCEPT (applied).** `fetch` now self-validates the locator (http(s), no creds) before driving and uses the normalized value for both the bag and `observation_id`. Test rejects a credentialed target. |

## Home-model adjudication notes
- The diff was adjudicated as a set of claims, not inherited. **F2's fix was rewritten** so
  the ambiguity flag is actually reachable — the reviewer's end-tag-based version was a
  no-op given the existing first-title-only capture guard. This is the kind of defect the
  CA-adjudication step (vs blind diff-apply) exists to catch.
- F1 + F2 harden the lane's highest-stakes invariant (no person/network data leaves the
  read edge) and its fail-closed posture; F3 enforces the clean-attach posture as code
  (mirrors the run-time legal gate philosophy); F4 makes the clean-bag docstring
  self-enforcing rather than downstream-dependent.
- No committed slice re-opened; all four changes are within the slice-3c-2b files.

## Residual risk (carried, reviewer-confirmed)
The live connect/navigate path (`CdpAttachBrowserDriver.rendered_dom`) remains
**owner-validated, not unit-tested**; the `browser.close()`-does-not-close-the-owner's-browser
behavior for `connect_over_cdp` is asserted in code comments, not proven by tests. Treat as
live-edge risk to confirm on the owner's attended run, not a resolved guarantee.

## Boundary
Advisory cross-vendor discovery only. Not approval / validation / readiness / live-runner /
commercial authorization. Claim: "module + its tests pass" (160 lane tests). The live
`CdpAttachBrowserDriver` is owner-validated; the live path is owner-accepted POC-risk
(ToS-gray, NOT "legally defensible").
