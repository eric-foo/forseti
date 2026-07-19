# CP1 — Marc Jacobs Beauty Owned Proposition

```yaml
retrieval_header_version: 1
artifact_role: Dogfood checkpoint packet
scope: Cumulative R0-R1 evidence packet for the Marc Jacobs Beauty capture-stopping replay.
use_when:
  - Replaying CP1 under the pre-registered Policy A or Policy B.
authority_boundary: retrieval_only
stale_if:
  - The packet hash or included acquisition receipt stops resolving.
```

```yaml
packet_version: 1
dogfood_id: marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719
checkpoint_id: CP1
evidence_through_job: R1
as_of_date: "2026-07-19"
time_posture: recency_first
bound_question: What does current public evidence show about how the relaunched Marc Jacobs Beauty proposition is expressed across owned claims, assortment, Sephora presentation, and early user experience, and where do those surfaces align, conflict, or remain unproven?
claim_boundaries:
  - decision-neutral company understanding only
  - one attributable instance establishes existence only
  - no prevalence or comparison without a defined sample, denominator, and comparable method
included_receipt_ids: [CAP-R0-001, CAP-R1-001, CAP-R1-002]
included_observation_ids: [OBS-001, OBS-002]
severe_negative_observed: false
remaining_jobs: [R2, R3, R4, R5]
```

## Added route receipts

```yaml
- receipt_id: CAP-R1-001
  packet_id: 01KXX313AE1NP93A0TMP61AQ0X
  route: Marc Jacobs exact Joystick PDP through Direct HTTP
  result: PARTIAL_HTTP_403
  locator: .acquisition/captures/r1_marc_jacobs_joystick_blush/manifest.json
- receipt_id: CAP-R1-002
  packet_id: 01KXX341VGQWF4H5BJZ0J530VR
  route: Marc Jacobs exact Joystick PDP through anonymous browser
  result: PARTIAL_AKAMAI_ACCESS_DENIED
  locator: .acquisition/captures/r1_marc_jacobs_joystick_blush_browser/manifest.json
```

## Cumulative observations

- **OBS-001 — Coty first-party relaunch frame:** Joyride Sensoriality, bold
  self-expression, seven opening products, $26–$42 pricing, tactile packaging,
  and staged named-channel distribution. It is first-party and establishes no
  product performance or customer experience.

```yaml
observation_id: OBS-002
source_class: official_first_party
publisher: Marc Jacobs
observed_at: "2026-07-19"
locator: https://www.marcjacobs.com/us-en/the-marc-jacobs/beauty-fragrance/view-all/
observation: >
  Current owned category surfaces and indexed official product content showed
  the seven-product assortment, shade breadth, packaging language, textures,
  and product-specific long-wear or experience claims.
limitations:
  - exact Joystick PDP packet capture preserved Akamai denial
  - indexed official content is screen-light rather than packet-grade PDP fidelity
  - owned claims are not independent performance tests
```

## Unanswered commissioned work

- R2: whether Sephora presentation and dated reviews align with the owned proposition.
- R3: whether attributable community experience aligns, conflicts, or corrects it.
- R4: independent product testing, contradictions, hidden venues, and syndication.
- R5: route dominance and closure.
