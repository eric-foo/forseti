# CP3 — Marc Jacobs Beauty Community Experience

```yaml
retrieval_header_version: 1
artifact_role: Dogfood checkpoint packet
scope: Cumulative R0-R3 evidence packet for the Marc Jacobs Beauty capture-stopping replay.
use_when:
  - Replaying CP3 under the pre-registered Policy A or Policy B.
authority_boundary: retrieval_only
stale_if:
  - The packet hash or included acquisition receipt stops resolving.
```

```yaml
packet_version: 1
dogfood_id: marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719
checkpoint_id: CP3
evidence_through_job: R3
as_of_date: "2026-07-19"
time_posture: recency_first
bound_question: What does current public evidence show about how the relaunched Marc Jacobs Beauty proposition is expressed across owned claims, assortment, Sephora presentation, and early user experience, and where do those surfaces align, conflict, or remain unproven?
claim_boundaries:
  - selected threads are attributable external evidence, not representative demand
  - recurrence may be stated only for bounded repeated observations
  - no prevalence, defect-rate, or line-wide comparison is supported
included_receipt_ids: [CAP-R0-001, CAP-R1-001, CAP-R1-002, CAP-R2-001, CAP-R2-002, CAP-R2-003, CAP-R3-BATCH]
included_observation_ids: [OBS-001, OBS-002, OBS-003, OBS-004, OBS-005, OBS-006, OBS-007, OBS-008]
severe_negative_observed: false
material_negative_observed: true
remaining_jobs: [R4, R5]
```

## Added route receipt

```yaml
receipt_id: CAP-R3-BATCH
route: four bounded Reddit-native search surfaces followed by seven selected old-Reddit content-mode packets
result: SEVEN_OF_SEVEN_CONTENT_RECORDS_PRESERVED
locator: .acquisition/captures/r3_reddit_selected_threads/batch_summary.json
limitation: >
  The batch summary's secondary-consolidation counter is a false negative
  caused by intentional raw-HTML discard. Seven manifests and seven
  raw/01_content_record.json files are present.
```

## Cumulative community evidence

- **OBS-006:** one first-hand review found creamy eyeshadow and blendable blush,
  then updated that blush lasted only a couple of hours while eyeshadow lasted
  all night. Comments repeatedly split on visually attractive design versus
  light, cheap, bulky, or flimsy hand-feel.
- **OBS-007:** eyeliner experience is sharply shade-dependent. Some black and
  brown shades are described as smooth and extremely durable; Delulu and bright
  blue reports describe softness, breakage, patchiness, weak payoff, smudging,
  or short waterline wear.
- **OBS-008:** multiple attributable users describe Money Shot arriving dried
  or shrunken, tiny, patchy, or goopy and mention replacements or returns.
  Related comments also contain liner breakage and shade mismatch.
- The bounded evidence now contains repeated examples of short blush wear,
  packaging hand-feel concerns, and product/shade-specific performance
  conflicts. It still has no defined sample or denominator and therefore
  supports no prevalence or defect-rate claim.
- A Reddit user's same-formula/manufacturer inference from ingredient lists is
  preserved but unverified and cannot be adopted as company fact.

## Unanswered commissioned work

- R4: independent hands-on sources must test whether the observed alignments and conflicts survive outside retailer/community surfaces and whether launch-copy syndication is being mistaken for independent corroboration.
- R5: closure remains unassessed.
