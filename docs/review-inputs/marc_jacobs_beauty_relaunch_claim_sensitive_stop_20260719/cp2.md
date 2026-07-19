# CP2 — Marc Jacobs Beauty Sephora Translation

```yaml
retrieval_header_version: 1
artifact_role: Dogfood checkpoint packet
scope: Cumulative R0-R2 evidence packet for the Marc Jacobs Beauty capture-stopping replay.
use_when:
  - Replaying CP2 under the pre-registered Policy A or Policy B.
authority_boundary: retrieval_only
stale_if:
  - The packet hash or included acquisition receipt stops resolving.
```

```yaml
packet_version: 1
dogfood_id: marc_jacobs_beauty_relaunch_claim_sensitive_stop_20260719
checkpoint_id: CP2
evidence_through_job: R2
as_of_date: "2026-07-19"
time_posture: recency_first
bound_question: What does current public evidence show about how the relaunched Marc Jacobs Beauty proposition is expressed across owned claims, assortment, Sephora presentation, and early user experience, and where do those surfaces align, conflict, or remain unproven?
claim_boundaries:
  - customer rows are attributable examples, not prevalence
  - incentive markers remain attached to review rows
  - US market and USD offers do not establish delivery location or local stock
included_receipt_ids: [CAP-R0-001, CAP-R1-001, CAP-R1-002, CAP-R2-001, CAP-R2-002, CAP-R2-003]
included_observation_ids: [OBS-001, OBS-002, OBS-003, OBS-004, OBS-005]
severe_negative_observed: false
material_negative_observed: true
remaining_jobs: [R3, R4, R5]
```

## Added route receipts

```yaml
- receipt_id: CAP-R2-001
  packet_id: 01KXX3HN463G98Y4QQH3WJM0QD
  product: Joystick Buildable Cream Blush Stick
  result: PASS_US_USD_DELIVERY_UNPINNED
  locator: .acquisition/captures/r2_sephora_joystick_blush_verified/manifest.json
- receipt_id: CAP-R2-002
  packet_id: 01KXX3MEN3B0CXA2PNR2EWSA1F
  product: Born Star Cream-to-Powder Long-Wear Eyeshadow
  result: PASS_US_USD_DELIVERY_UNPINNED
  locator: .acquisition/captures/r2_sephora_born_star_verified/manifest.json
- receipt_id: CAP-R2-003
  packet_id: 01KXX3PYBM91TSMP5GA6D3H9ZJ
  product: Heart On Long-Lasting Soft Shine Lipstick
  result: PASS_US_USD_DELIVERY_UNPINNED
  locator: .acquisition/captures/r2_sephora_heart_on_verified/manifest.json
```

## Cumulative evidence

- **OBS-001 / OBS-002:** Coty and Marc Jacobs coherently express a maximalist,
  sensorial, tactile, playful seven-product proposition. Exact owned Joystick
  PDP preservation remains partial; owned claims do not prove performance.
- **OBS-003 — Sephora translation:** Sephora describes the relaunch as
  maximalist, playful, upgraded, multi-use, and long-wearing. Selected PDPs
  carry current USD offers. Product copy may be brand-supplied; delivery and
  local-stock state are unpinned.
- **OBS-004 — Heart On dated rows:** attributable reviewers describe smooth,
  moisturizing, buildable wear, while others report shade-photo mismatch, a
  loose cap, returns, and one 2–3-hour wear result. This conflicts with an
  absolute all-day/non-fading reading but establishes no prevalence.
- **OBS-005 — Born Star dated rows:** attributable reviewers report smooth,
  easy, crease-resistant experience alongside breakage or shrinkage in the pan,
  creasing, low pigment, warm-shade mismatch, and bulky-price concerns. These
  establish examples, not a defect rate.

## Unanswered commissioned work

- R3: independent community threads and possible recurrence or correction.
- R4: independent hands-on testing, contradictions, better origins, and syndication.
- R5: whether any remaining route can materially change the permitted claim or qualification.
