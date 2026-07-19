# Dr.Jart+ Broad Company Understanding Acquisition Seal v0

```yaml
retrieval_header_version: 1
artifact_role: Intelligence Cycle acquisition seal
scope: Completed Acquire & Seal closeout after bounded exact-URL preservation recovery for the Dr.Jart+ broad Understanding dogfood.
use_when:
  - Verifying whether Deliver is authorized.
  - Auditing the original preservation failure, recovery packets, and accepted residuals.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_dr_jart_broad_company_understanding_commission_board_v0.md
  - docs/research/forseti_beauty_dr_jart_broad_company_understanding_scan_receipt_v0.md
  - docs/workflows/dr_jart_broad_company_understanding_20260720_dogfood_v0.md
```

```yaml
current_lifecycle_status: ACQUISITION_SEALED
intelligence_cycle_phase_status: UNDERSTANDING_ACQUIRE_AND_SEAL_COMPLETED
resume_allowed: true_only_by_new_commission_or_material_source_change
correct_intake_result: SEALED_READY_FOR_DELIVER
```

```yaml
phase_acquisition_seal:
  cycle_id: dr_jart_broad_company_understanding_20260720
  commission_id: dr_jart_broad_company_understanding_csb_20260720
  phase: understanding
  turn: acquire_and_seal
  bound_question: What does current public evidence show about Dr.Jart+ as a company and brand system—its proposition, offering architecture, markets and channels, recent strategic and operating motion, customer and community response, and bounded competitive context—and which observable tensions warrant later Problem Framing?
  intended_consumer: Forseti Intelligence Cycle Deliver turn
  intended_use: decision-neutral broad company understanding that is Problem-Framing-ready
  commission_board_locator: docs/research/forseti_beauty_dr_jart_broad_company_understanding_commission_board_v0.md
  scan_receipt_locator: docs/research/forseti_beauty_dr_jart_broad_company_understanding_scan_receipt_v0.md
  outcome_signals:
    - question_fit
    - evidence_foundation
    - reasoning_quality
    - honest_uncertainty
    - implications_and_foresight
    - communication_efficiency
  resolved_routes:
    - COV-001 owned current product and collection
    - COV-002 parent ownership and operating disclosure
    - COV-003 partial Sephora US retailer translation
    - COV-004 Sephora incentive policy with product-review data blocked
    - COV-005 bounded Reddit scout
    - COV-006 category-aware channel discovery
    - COV-007 sparse independent/trade scout
    - COV-008 one bounded comparator pointer
  material_tension_checks:
    - tension: owned upgraded-formula framing versus attributable reformulation and color/finish concerns
      check: current canonical owned PDP and collection
      result: current upgraded-product framing exists; formula delta and response distribution remain unverified
    - tension: parent-reported regional weakness versus current channel presence
      check: current local retailer notice
      result: one dated Japanese location exit exists; global strategy, cause, and importance remain unknown
    - tension: retailer headline review evidence may be incentive-polluted
      check: retailer incentive policy plus exact PDP
      result: policy was readable but product review rows and filter state were unavailable; no approval metric was produced
  capture_receipts:
    - evidence_row: OBS-002
      packet_id: 01KXXXYT2WQ8RJJWRTDH0YBGKE
      result: PASS_RENDERED_EXACT_URL
      locator: _acquisition/dr_jart_preservation_recovery/obs_002_drjart_pdp_rendered/manifest.json
    - evidence_row: OBS-003
      packet_id: 01KXXXZWV62A9GFPBX2G6C4XVG
      result: PASS_RENDERED_EXACT_URL
      locator: _acquisition/dr_jart_preservation_recovery/obs_003_drjart_redness_collection_rendered/manifest.json
    - evidence_row: OBS-005
      packet_id: 01KXXXR6J79NTV967X2JRV47TX
      result: PASS_HTTP_200
      locator: _acquisition/dr_jart_preservation_recovery/obs_005_elc_fy2025/manifest.json
    - evidence_row: OBS-006
      packet_id: 01KXXY33E8ZKJD2F9KTP2JXJ05
      result: PASS_NARROW_US_USD_PAGE_PRESERVATION_PROFILE_LITERAL_RESIDUAL
      locator: _acquisition/dr_jart_preservation_recovery/obs_006_sephora_pdp_rendered/manifest.json
    - evidence_row: OBS-007
      packet_id: 01KXXY0FX2YPNB0MVARFW49X8Z
      result: PASS_RENDERED_EXACT_URL
      locator: _acquisition/dr_jart_preservation_recovery/obs_007_sephora_policy_rendered/manifest.json
    - evidence_row: OBS-008
      packet_id: 01KXXY5FR0CXV5VHEWA8CT1TBX
      result: PASS_SAME_THREAD_RENDERED_FALLBACK
      locator: _acquisition/dr_jart_preservation_recovery/obs_008_asianbeauty_rendered/manifest.json
    - evidence_row: OBS-009
      packet_id: 01KXXY5W1V0J0DN2BE68YBB3HX
      result: PASS_SAME_THREAD_RENDERED_FALLBACK
      locator: _acquisition/dr_jart_preservation_recovery/obs_009_30plusskincare_rendered/manifest.json
    - evidence_row: OBS-010
      packet_id: 01KXXXQZR7YXB0YTVB9KNHHDXZ
      result: PASS_HTTP_200
      locator: _acquisition/dr_jart_preservation_recovery/obs_010_cosmeme_notice/manifest.json
    - evidence_row: OBS-012
      packet_id: 01KXXXR23T4KNX2MJWNWS9H2P0
      result: PASS_HTTP_200
      locator: _acquisition/dr_jart_preservation_recovery/obs_012_peach_lily_comparator/manifest.json
    - evidence_row: HVP-002
      packet_id: 01KXXY8CNRZNSNAXFEZ5J4J50V
      result: PASS_RENDERED_EXACT_URL
      locator: _acquisition/dr_jart_preservation_recovery/hvp_002_fashionography_rendered/manifest.json
  blocked_requirements: []
  typed_gaps:
    - GAP-002 retailer PDP rendering limit
    - GAP-003 product-level incentive-filter data unavailable
    - GAP-004 current independent trade sparsity
  accepted_route_residuals:
    - Sephora aggregate capture preserved the exact page and confirmed the US/USD storefront conjunction, but failed a product-specific `Lip Sleeping Mask` profile literal; only the previously observed narrow retailer translation is admitted.
    - Reddit content-mode HTTP failed to retain a usable derived record after raw discard; exact-thread rendered fallback packets are admitted instead.
    - Direct HTTP access failures for the owned pages and Sephora policy remain preserved alongside their rendered fallbacks.
  seal_state: SEALED_READY_FOR_DELIVER
  acquisition_gate: pass
  deliver_allowed: true
  next_authorized_step: Fresh-context Deliver may use only this sealed evidence set and its typed gaps; it may not reopen acquisition by default.
```

`SEALED_READY_FOR_DELIVER`.

The acquisition gate passed after exact-URL preservation recovery. This does
not close GAP-002 through GAP-004, admit any product-review approval metric,
establish prevalence, or authorize a rescan.
