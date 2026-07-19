# CP0 — Marc Jacobs Beauty Relaunch Frame

```yaml
retrieval_header_version: 1
artifact_role: Dogfood checkpoint packet
scope: Cumulative R0 evidence packet for the Marc Jacobs Beauty capture-stopping replay.
use_when:
  - Replaying CP0 under the pre-registered Policy A or Policy B.
authority_boundary: retrieval_only
stale_if:
  - The packet hash or included acquisition receipt stops resolving.
```

```yaml
packet_version: 1
dogfood_id: marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719
checkpoint_id: CP0
evidence_through_job: R0
as_of_date: "2026-07-19"
time_posture: recency_first
bound_question: What does current public evidence show about how the relaunched Marc Jacobs Beauty proposition is expressed across owned claims, assortment, Sephora presentation, and early user experience, and where do those surfaces align, conflict, or remain unproven?
claim_boundaries:
  - decision-neutral company understanding only
  - one attributable instance establishes existence only
  - no prevalence or comparison without a defined sample, denominator, and comparable method
  - heritage is contextual only when a current source invokes it
included_receipt_ids: [CAP-R0-001]
included_observation_ids: [OBS-001]
severe_negative_observed: false
remaining_jobs: [R1, R2, R3, R4, R5]
```

## Route receipt

```yaml
receipt_id: CAP-R0-001
packet_id: 01KXX30ECGZPFHG4GVE3BCTX79
route: Coty exact first-party relaunch announcement through Direct HTTP
result: PASS
locator: .acquisition/captures/r0_coty_relaunch/manifest.json
```

## Available observation

```yaml
observation_id: OBS-001
source_class: official_first_party
publisher: Coty
publication_date: "2026-05-20"
locator: https://www.coty.com/news/coty-launches-marc-jacobs-beauty-one-of-the-most-requested-luxury-comebacks
observation: >
  Coty framed the relaunch around Joyride Sensoriality and bold
  self-expression, named a seven-product opening assortment, stated US prices
  from 26 to 42 dollars, described tactile packaging, named Marc Jacobs and
  Coty as partners, and described staged Marc Jacobs, Sephora, Selfridges, and
  travel-retail distribution.
limitations:
  - first-party launch framing is not independent corroboration
  - does not establish product performance or customer experience
  - does not establish prevalence, representative demand, or local availability
```

## Unanswered commissioned work

- R1: current owned assortment, product claims, packaging, textures, and experience language.
- R2: Sephora retail translation and dated product-review evidence.
- R3: mandatory bounded Reddit scout and selected-thread preservation.
- R4: independent corroboration, contradictions, hidden venues, and syndication.
- R5: current Scanning expected-decision-value closure.
