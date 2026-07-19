# Marc Jacobs Beauty Relaunch Understanding Acquisition Seal v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Completed Acquire & Seal record for the Marc Jacobs Beauty relaunch Understanding Intelligence Cycle.
use_when:
  - Verifying whether the separately authorized Deliver turn may consume this acquisition.
  - Auditing route dispositions, packet receipts, accepted residuals, and closure.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_commission_board_v0.md
  - docs/research/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_scan_receipt_v0.md
stale_if:
  - The acquisition is reopened or a cited current source materially changes.
```

## Capture Locator Resolution

Packet locators below preserve the acquisition-time `.acquisition/` prefix.
After collection and evaluator replay, the unchanged 78-file capture root was
moved to the placement-excluded worktree scratch path
`C:\tmp\forseti-marc-jacobs-stopping-dogfood\_acquisition\`. Resolve a recorded
`.acquisition/` locator by replacing that prefix with this bound scratch root.
The move retained all 15 packet IDs, three projections, and seven selected
Reddit URLs and changed no checkpoint bytes.

## Lifecycle Closeout

```yaml
current_lifecycle_status: ACQUISITION_SEALED
intelligence_cycle_phase_status: UNDERSTANDING_ACQUIRE_AND_SEAL_COMPLETED
resume_allowed: true_only_by_new_commission_or_material_source_change
correct_intake_result: SEALED_COMPLETE_WITH_ACCEPTED_RESIDUALS
```

```yaml
phase_acquisition_seal:
  cycle_id: marc_jacobs_beauty_relaunch_understanding_20260719
  commission_id: marc_jacobs_beauty_relaunch_understanding_csb_20260719
  phase: understanding
  turn: acquire_and_seal
  bound_question: What does current public evidence show about how the relaunched Marc Jacobs Beauty proposition is expressed across owned claims, assortment, Sephora presentation, and early user experience, and where do those surfaces align, conflict, or remain unproven?
  intended_consumer: Forseti Intelligence Cycle Deliver turn
  intended_use: decision-neutral company understanding
  phase_scope: Current Marc Jacobs Beauty relaunch proposition across owned, Sephora, independent editorial, and early community surfaces.
  outcome_signals:
    - question_fit
    - evidence_foundation
    - reasoning_quality
    - honest_uncertainty
    - implications_and_foresight
    - communication_efficiency
  resolved_routes:
    - route_id: R0
      source_or_venue: Coty
      information_job: official relaunch frame, operating identity, proposition, assortment, price, and named launch channels
      required: true
      route_identity: exact first-party announcement by direct HTTP
      route_authority: forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
      disposition: passed
    - route_id: R1
      source_or_venue: Marc Jacobs
      information_job: current owned assortment, claims, packaging, texture, and experience language
      required: true
      route_identity: current owned category and product URLs; exact Joystick direct and browser capture attempts
      route_authority: forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
      disposition: passed_with_partial_exact_pdp_capture
    - route_id: R2
      source_or_venue: Sephora US
      information_job: retailer translation plus dated selected-PDP review rows
      required: true
      route_identity: anonymous CloakBrowser with country_switch=us, source-confirmed US market and USD offer admission
      route_authority: forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
      disposition: passed_delivery_location_unpinned
    - route_id: R3
      source_or_venue: Reddit
      information_job: bounded native scout and exact selected-thread preservation
      required: true
      route_identity: canonical screening_read search surfaces followed by old_reddit_direct_http content-mode packets
      route_authority: docs/decisions/screening_reddit_read_route_decision_v0.md
      disposition: passed
    - route_id: R4
      source_or_venue: independent editorial, hidden venues, better origins, syndication, contradictions, and negatives
      information_job: independent corroboration and disconfirmation
      required: true
      route_identity: bounded public search and rendered editorial reads
      route_authority: forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
      disposition: passed
    - route_id: R5
      source_or_venue: Scanning frontier closure
      information_job: expected-decision-value closure
      required: true
      route_identity: branch-decay, pivot, and stop value test
      route_authority: forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
      disposition: passed
  dominated_or_conditional_routes:
    - source_or_venue: Quora
      disposition: not_required_no_decision_material_job
    - source_or_venue: TikTok
      disposition: not_applicable_no_unique_non_dominated_information_job
    - source_or_venue: Ulta
      disposition: out_of_scope_not_a_named_current_retailer_route
  scan_receipts:
    - docs/research/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_scan_receipt_v0.md
  capture_receipts:
    - receipt_id: CAP-R0-001
      packet_id: 01KXX30ECGZPFHG4GVE3BCTX79
      result: PASS
      locator: .acquisition/captures/r0_coty_relaunch/manifest.json
    - receipt_id: CAP-R1-001
      packet_id: 01KXX313AE1NP93A0TMP61AQ0X
      result: PARTIAL_HTTP_403
      locator: .acquisition/captures/r1_marc_jacobs_joystick_blush/manifest.json
    - receipt_id: CAP-R1-002
      packet_id: 01KXX341VGQWF4H5BJZ0J530VR
      result: PARTIAL_AKAMAI_ACCESS_DENIED
      locator: .acquisition/captures/r1_marc_jacobs_joystick_blush_browser/manifest.json
    - receipt_id: CAP-R2-001
      packet_id: 01KXX3HN463G98Y4QQH3WJM0QD
      result: PASS_US_USD_DELIVERY_UNPINNED
      locator: .acquisition/captures/r2_sephora_joystick_blush_verified/manifest.json
    - receipt_id: CAP-R2-002
      packet_id: 01KXX3MEN3B0CXA2PNR2EWSA1F
      result: PASS_US_USD_DELIVERY_UNPINNED
      locator: .acquisition/captures/r2_sephora_born_star_verified/manifest.json
    - receipt_id: CAP-R2-003
      packet_id: 01KXX3PYBM91TSMP5GA6D3H9ZJ
      result: PASS_US_USD_DELIVERY_UNPINNED
      locator: .acquisition/captures/r2_sephora_heart_on_verified/manifest.json
    - receipt_id: CAP-R3-BATCH
      result: SEVEN_OF_SEVEN_CONTENT_RECORDS_PRESERVED
      locator: .acquisition/captures/r3_reddit_selected_threads/batch_summary.json
      limitation: secondary consolidation counters are false-negative because raw HTML was intentionally discarded after content projection
  reddit_packet_ids:
    - 01KXX44CFFJYWTVVCJKW7DEY86
    - 01KXX44G0E513PCQHG42RS2VKN
    - 01KXX44KM2MAGS9GMBVJ9G2900
    - 01KXX44QSK79C36TDD0PMMTCR1
    - 01KXX44VBXETVR2E8S8VQD8K1N
    - 01KXX44YQJQHGS9XVY016818QG
    - 01KXX45276A0FK374ZBV9ECEX5
  material_gaps_and_failures:
    - gap_id: GAP-001
      requirement: exact owned PDP packet preservation
      state: accepted_residual
      detail: direct HTTP and browser packet routes preserved access-denial artifacts; current indexed official content and category pages supplied sufficient R1 screen-light evidence
    - gap_id: GAP-002
      requirement: delivery and local-stock inference
      state: bounded_unknown
      detail: Sephora US market and USD offers were confirmed, but delivery location and local availability were not pinned and are not claimed
    - gap_id: GAP-003
      requirement: customer/community representativeness
      state: accepted_evidence_boundary
      detail: dated rows and selected threads are attributable examples, not prevalence or representative demand
    - gap_id: GAP-004
      requirement: formula-equivalence inference
      state: unverified_not_adopted
      detail: one Reddit author compared ingredient lists and inferred a shared formula or manufacturer; the inference is preserved but not treated as company fact
    - failure_id: TOOL-001
      route: local derived data-lake catalog census
      observed: one silent timeout after the derived lookup returned not_found
      effect: no catalog-exhaustion or absence claim; the runner route was not retried
    - failure_id: TOOL-002
      route: Reddit batch secondary consolidation summary
      observed: zero consolidations reported after content-mode raw discard
      effect: manifests and seven packet-native content records fresh-read present; source evidence was not lost
  severe_negative_state:
    result: none_identified
    treatment: material product, packaging, shade, taste, quality-control, and wear negatives preserved without prevalence inference
  owner_unblock:
    required: false
    reason: no required route remained blocked after typed residuals were applied
  closure:
    method: expected_decision_value_stop
    result: closed
    rationale: all required R0-R4 jobs completed and no remaining frontier was expected to materially change the decision-neutral evidence shape
  seal_state: ACQUISITION_COMPLETE_WITH_ACCEPTED_RESIDUALS
  acquisition_gate: passed
  deliver_allowed: true
  deliver_scope: separately authorized decision-neutral Deliver turn only
  sealed_at: "2026-07-19"
```

## Seal Statement

`SEALED_COMPLETE_WITH_ACCEPTED_RESIDUALS`.

The acquisition gate passed. Deliver may consume the board, scan receipt, and
route-owned packet receipts in a separately authorized turn. This seal does not
run Deliver, establish representative demand or defect prevalence, infer local
availability, adopt the unverified formula-equivalence claim, or authorize new
capture by default.
