```yaml
retrieval_header_version: 1
artifact_role: Review-output record (cross-vendor code review + home-model adjudication + same-vendor recheck)
scope: >
  Durable audit record of the adversarial CODE review of slice 3b-2 -- the
  LiveObservation->CandidateRow projection (project_observation_to_candidate_row):
  the mint-path + the observation/access-envelope posture binding (closes the
  slice-3b F3 deferral). Advisory throughout; not a verdict.
authority_boundary: retrieval_only
reviewed_artifact: capture_spine/linkedin_live_adapter/projection.py (+ __init__.py export) + tests/unit/test_linkedin_live_adapter.py (projection section)
input_bundle: docs/review-outputs/linkedin_live_projection_slice3b2_v0_no_repo_review_bundle.zip (blob ff7963ef; PRE-fix code GPT-5.5 reviewed)
implements: docs/product/data_capture_spine_linkedin_live_layer_architecture_v0.md (ADR §6.1 mint-path / §8 slice-3b-2)
provenance:
  authored_by: anthropic/claude-opus-4.x
  reviewed_by: openai/gpt-5.5 (advisory, no-repo; reconstructed the package, ran tests: 38 baseline, 40 after its own bounded patch)
  same_vendor_recheck: anthropic/sonnet (clean)
  de_correlation_bar: cross_vendor_discovery
```

# LinkedIn live-projection slice 3b-2 — Cross-Vendor Code Review + Adjudication (v0)

## Outcome
1 finding (major). The reviewer confirmed the mint-path + binding shape were
**intact** (validation precedes binding/projection; `live_access_id` and all
`run_id` values matched; `candidate_class` + `source_surface` declared against the
run envelope; the emitted dict passes `validate_candidate_row`) and caught one
minimization-boundary gap. Adjudication: **1/1 accepted + patched** (home model
added one test). Same-vendor recheck: **CLEAN. 106 pass.**

| # | Sev | Finding (GPT-5.5) | Adjudication + fix |
|---|-----|-------------------|--------------------|
| F1 | major | `visible_follower_count_or_none` / `visible_connection_count_band_or_none` are carried into `VisibleInfluenceNumbers` without a minimization check. The observation shape gate length-caps other free-text fields but not these two, so a copied profile/body payload could be smuggled through a field documented "counts / coarse bands only." | **ACCEPT** — verified against source: the two fields are absent from `validate_live_observation`'s `_LENGTH_CAPPED_FREETEXT_FIELDS`, and `validate_candidate_row` does not inspect nested influence content. In-scope projection fix: `_validate_visible_influence_value` (count/coarse-band format + 64-char cap, fail-closed) runs before the values are carried; codes `oversized_visible_influence_number` / `invalid_visible_influence_number`. **Home-model modification:** added a 3rd test pinning the short-prose (format-mismatch) path distinct from the oversized path. |

## Home-model adjudication notes
- The reviewer correctly stayed in the bounded scope (`projection.py` + tests); it flagged but did not edit the committed slice-3b `validation.py`.
- **Residual (accepted, by design):** the format guard is a CONTRACT-level boundary, not a runtime read-minimization proof; full content minimization remains the **slice-3c** runtime tape-test. The DURABLE home for capping these two fields is the slice-3b observation validator (`_LENGTH_CAPPED_FREETEXT_FIELDS`) — recorded as a follow-up, since `validation.py` is off-scope for 3b-2.
- **README test-count note (reviewer):** "103" is the full LinkedIn lane (3 files); the bundle shipped only the live-adapter test file (38 baseline). Doc-framing imprecision, no code impact.

## Same-vendor recheck (Sonnet)
Focused on the one real risk in a regex format guard — false-rejection of legitimate values. Traced 10 realistic minimized values (`1,234`, `500+`, `1K`, `1.2M`, `10K+`, `1K-5K`, `500-1000`, `1,000-5,000`, `under 500`, `more than 10K`): all match, no false-reject. No contract-level smuggle passes (the only letters admitted are `k/K/m/M`, the fixed band words `under/over/less than/more than`, and the range word `to`; every branch is `fullmatch`-anchored). The 3 tests target distinct codes and are non-hollow. Verdict: clean.

## Boundary
Advisory only. Not approval / validation / readiness / live-runner / commercial authorization. Claim: "module + tests pass" (106). The live runtime (browser/session/fetch) is slice 3c, behind a separate legal/ToS gate.
