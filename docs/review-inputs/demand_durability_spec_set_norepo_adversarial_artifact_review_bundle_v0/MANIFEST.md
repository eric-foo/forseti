# MANIFEST — Demand-Durability Spec Set No-Repo Cross-Vendor Adversarial Artifact Review Bundle v0

```yaml
retrieval_header_version: 1
artifact_role: Review-input bundle manifest (no_repo cross-vendor adversarial artifact review)
scope: Commission receipt, verbatim-attachment hashes, and freshness-gate result for the demand-durability spec-set review bundle.
authority_boundary: retrieval_only
```

## Commission receipt

```yaml
lane: delegated-review-and-patch (provisional, opt-in)            # .agents/workflow-overlay/delegated-review-patch.md
access_mode: no_repo                                              # delegate repo-blind, advisory-only (returns findings, not a diff); CA applies per-spec
review_lane: adversarial-artifact-review                          # workflow-adversarial-artifact-review (non-code artifacts)
de_correlation_bar: cross_vendor_discovery
authored_by_family: claude-opus-4.8 (Anthropic)
controller_family: OpenAI / GPT (operator couriers; any non-Anthropic vendor satisfies cross-vendor)
controller_constraint: cross-vendor (different vendor/lineage than the author) — who-constraint only, NOT runtime model routing; the bundle and prompt name no runtime model
required_followup: same-vendor bounded post-patch recheck before keep (after CA applies accepted findings)
reviewed_by: unrecorded                                           # set by operator/CA on the durable review report on return (= the GPT model+version used)
authored_by: claude-opus-4.8                                      # set on the durable review report on return
adjudication: CA adjudicates every finding (claims-not-premises) before anything is kept
report_destination: docs/review-outputs/adversarial-artifact-reviews/  # durable report on return
```

## Verbatim attachments (byte-exact copies; SHA256)

Each target was copied byte-for-byte from its lane worktree (no retyping). The
reviewer should confirm the provided copy matches the hash below.

```text
b19ebe96365ba51fd7fc1184eb4a5fd957b8bc9b4b64b199675dce3548848bdb  01_capture_envelope_durability_delta_spec_v0.md          (24359 bytes)  [PR #93 / capture-envelope-durability-delta @ dde1df9]
80354b6be41b8ff9dfdea356710185570119638d6494c3089ca172538980a111  02_demand_proxy_price_timeseries_capture_profile_v0.md   (20983 bytes)  [PR #96 / capture-proxy-price-availability @ dd09696]
8b3f2849bafcbb0d03988fdb9fbf8be07c58bd751701acd19e5dde927f1ce7ee  03_demand_proxy_availability_restock_capture_profile_v0.md (20968 bytes)  [PR #96 / capture-proxy-price-availability @ dd09696]
045c8898b8a3c3bcabd6572454554848b9d49dc8064d2b98af352902d2791219  04_demand_proxy_search_interest_capture_profile_v0.md    (14441 bytes)  [PR #95 / capture-proxy-search-review @ 81efbaa]
2ac5a9a0afcc685cc5a851ce4da1462e70fa5be045668bfd2b3ea2fcf4eee282  05_demand_proxy_review_velocity_corpus_capture_profile_v0.md (21975 bytes)  [PR #95 / capture-proxy-search-review @ 81efbaa]
```

> Note: bundle base is `origin/main` 8e54aad. PR #93's merge is owner-queued and
> merge-independent for review content (the verbatim spec is identical whether on
> its branch or merged). #95/#96 remain on their branches.

## Freshness gate (portable-method `derived_from` pins vs live canonical sources)

Run before bundling, per `.agents/workflow-overlay/delegated-review-patch.md`
(no_repo) and the portable method's `stale_if`. Live hashes computed against
`origin/main` blob content.

```yaml
freshness_gate:
  source_1:
    path: docs/prompts/templates/review/adversarial_artifact_review_v0.md
    pin:  0cb80057795215b3311d00c3d0ad603fbef78fe92e5ae24d8042490b8b60c3fc
    live: 0cb80057795215b3311d00c3d0ad603fbef78fe92e5ae24d8042490b8b60c3fc
    result: MATCH
  source_2:
    path: .agents/workflow-overlay/review-lanes.md
    pin:  7fd702f5bddd8d9e670f503dd7def6c1e0d8a04d9fce0103fa0336d6614f3c22
    live: 231d2f6c99e1bcdd0ad950b82e6c6bcb18b5e7f99b001289f760e660aeabef51
    result: MISMATCH
    disposition: pin-only (method block remains faithful)
    assessment: >
      Diffed the two post-pin commits to review-lanes.md: (eeb42e9 / #25) added
      the work-unit fitness_reference doctrine — already reflected in the shipped
      PORTABLE METHOD block §4 (fitness-to-goal, "no checkable success bar bound");
      (ff714c3 / #42) retired _generic/ model-target templates — Template
      Retrieval Binding only, outside the distilled reviewer stance/checks. Neither
      changed the reviewer stance, checks, severity, or output contract the method
      block distills. The shipped block is therefore content-faithful to current
      Review Doctrine.
    decision: ship the PORTABLE METHOD block as-is (recorded here per the gate).
    flagged_hygiene_followup: >
      Re-pin docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md
      derived_from review-lanes.md to 231d2f6c (pin-only note). Off-target for this
      bundle (single-target rule) — flagged, not edited.
```
