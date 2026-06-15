# Orca Demand Scan-Core Spec v0 — Delegated Adversarial Review/Patch Report

```yaml
retrieval_header_version: 1
artifact_role: Adversarial review output (delegated review/patch report — advisory; decision input for commissioning-CA adjudication)
scope: >
  Delegated adversarial review/patch report on the 2026-06-13 draft of
  orca_demand_scan_core_spec_v0 (PROPOSED), de-correlated controller (OpenAI
  GPT-5) vs Anthropic author home. Advisory findings only. Covers the prior
  schema; the spec was re-derived 2026-06-16 after this review (see the spec's
  Status), so the gate_family-with-retail remedy here is superseded while its
  mechanical-checkability principle is preserved.
use_when:
  - Reviewing the delegated adversarial findings on the scan-core spec draft.
  - Tracing the gate_family / org_motion_route schema patches and their citations.
authority_boundary: retrieval_only
```

## De-correlation self-check

Controller vendor/lineage: OpenAI GPT-5. Author home model family recorded by the commission: Anthropic Claude Fable 5 (`claude-fable-5`). De-correlation status: satisfied by commission constraint; not Anthropic and not unknown/undisclosed.

Claim level: advisory findings only. Formal Orca review tooling/lane authority is not invoked by this controller report; this is decision input for commissioning-CA adjudication.

## Preflight receipts

- Worktree: `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-demand-scan-spec-wt`
- Branch: `demand-scan-core-spec-v0`
- HEAD: `64c442a`
- Starting dirty state matched the commission allowance:
  - ` M docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md`
  - `?? docs/product/core_spine/orca_demand_scan_core_spec_v0.md`
  - `?? docs/prompts/reviews/orca_demand_scan_core_spec_delegated_adversarial_review_patch_prompt_v0.md`
- Target raw-byte SHA256 at start: `1DA22088746012B474639AA8EF401ED7FCD63E65B1137D4829C6929CFA3C0856` — matched.
- Pinned source hashes: all matched the commissioned SHA256 prefixes:
  - `docs/prompts/product-planning/consumer_demand_scanning_lane_commission_prompt_v0.md` — `92146714330AF783`
  - `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — `BC478D890419B2B6`
  - `docs/product/core_spine/beauty_venue_card_set_v0.md` — `65E22CDAE5EDE781`
  - `docs/product/core_spine/orca_vertical_exploration_guide_v0.md` — `EF9F5C6E716E9857`
  - `docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md` — `C672C1678F98878F`
  - `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md` — `19009D43A7C29858`
  - `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md` — `48B5534E056FD42A`
  - `docs/decisions/orca_product_thesis_consumer_demand_v0.md` — `B119E24691066E47`
  - `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — `25EBD39AE95C3A07`
- Report path write preflight: succeeded.

`SOURCE_CONTEXT_READY`

## review_summary

Structured reasoning pass:

- Load-bearing target claims: one scan core serves backward and forward modes; scan authorization is external; the target owns hunting grammar and emission schema while guide/frame/brief/pool keep their own downstream authority; no capture route is set by the scan.
- Boundary/decision criteria attacked: whether the emitted schema makes the Demand-Substrate Hard Gate mechanically checkable; whether the guide/frame reconciliation avoids duplicating adopted walk mechanics; whether forward mode remains outcome-free and pool-is-never-slot-source; whether no person/outreach/registry surfaces leak in.
- Likely failure modes: laundering a demand signal through trade press without preserving the underlying gate family; treating detector/trade/org evidence as equivalent to a gate-counting demand family; letting `unknown` org-route state pass slot qualification; accidentally turning wind-caller observations into a standing registry or person profile.

```yaml
review_summary:
  status: review_complete
  recommendation: advisory_keep_after_CA_adjudication_of_diff
  findings_count: 2
  blocking_findings:
    - "major: observation schema lacked an observation-level gate-family field, so the two-family Hard Gate was not mechanically checkable across laundered/evidence venues."
    - "major: org-motion route state was too weak to enforce the capture-lane binding/no-outside-route stop condition."
  advisory_findings: []
  summary: "Patch is narrow and schema-level; no design-level NEEDS_ARCHITECTURE_PASS condition found."
```

## Findings

### Finding 1

- severity: major
- location: `docs/product/core_spine/orca_demand_scan_core_spec_v0.md`, Candidate Observation Schema, `observation` and `gate_check`
- issue: The original schema recorded `venue_family` but did not separately record the Hard Gate family actually evidenced by an observation. That made the gate check non-mechanical when a trade-press receipt launders a community-originated signal, when a detector supports a subtle event, or when org motion corroborates but does not count toward the two-family minimum.
- evidence: Target section originally said the Hard Gate counts only `review_surfaces`, `forums_community`, `search_interest`, `retail_presence`, while `trade_press`, `tracker_detector`, and `org_motion_surface` are evidence venues. Buyer-proof packet requires at least two independent venue families from those four demand families and says no single venue's bias or manipulation carries the answer. The beauty card set says NEWSY community origination can be laundered into trade press and SUBTLE detector evidence can be the record, creating exactly the host-venue vs gate-family split the schema must preserve.
- impact: A consuming brief or proof lane could be forced to re-judge gate families from prose and citations instead of reading the schema, or worse, count trade/detector/org evidence as demand-family coverage. That weakens the Demand-Substrate Hard Gate and makes slot qualification less checkable.
- minimum_closure_condition: Every observation states both its host/evidence venue family and its gate-counting demand family or `none`, with the candidate gate check backed by observation IDs and independence basis.
- next_authorized_action: bounded patch to the target schema only.
- advisory remediation direction: Add `gate_family` and `gate_family_basis` to observations; clarify laundering behavior; require gate-family entries to be backed by observation IDs and independence basis.

### Finding 2

- severity: major
- location: `docs/product/core_spine/orca_demand_scan_core_spec_v0.md`, Candidate Observation Schema, `gate_check.org_motion_route`
- issue: The original enum `cited_binding | unknown` did not distinguish usable current capture-route coverage from unknown, not applicable, or blocked/outside-current-binding states.
- evidence: The target-selection brief says Demand-Substrate Hard Gate qualification requires no route outside the capture lane's current bindings and its stop rules say to stop if qualification would require such a route. The buyer-proof packet says org-motion routes follow owning capture decisions and route-binding changes are capture-lane decisions, never per-proof stretches.
- impact: A forward candidate entry could appear mechanically slot-ready with `unknown`, even when the real state is a route blocker that should hold or disqualify the candidate.
- minimum_closure_condition: The schema distinguishes route available under cited binding, unknown/unavailable, blocked outside current binding, and not applicable.
- next_authorized_action: bounded patch to the target schema only.
- advisory remediation direction: Replace the two-value enum with a route-state enum that preserves the stop condition.

## Unified diff

```diff
--- a/docs/product/core_spine/orca_demand_scan_core_spec_v0.md
+++ b/docs/product/core_spine/orca_demand_scan_core_spec_v0.md
@@ -201,6 +201,8 @@
 venue:                    # card number/name, or discovered venue
 venue_class: newsy | subtle
 venue_family: review_surfaces | forums_community | search_interest | retail_presence | trade_press | tracker_detector | org_motion_surface
+gate_family:              # review_surfaces | forums_community | search_interest | retail_presence | none
+gate_family_basis:        # why this observation does or does not count toward the Hard Gate family count
 costly_behavior: yes | attention_only
 integrity_notes:          # amplification risk, incentive distortion, copied/coordinated marks, venue bias
 event_dates:              # when the observed thing happened (as dateable from the receipt)
@@ -210,13 +212,17 @@
 us_flag: us | non_us | border
 ```
 
-`venue_family` vocabulary note (gate checkability): the Demand-Substrate Hard
-Gate counts independence across its four demand families only —
-`review_surfaces`, `forums_community`, `search_interest`, `retail_presence`.
-`trade_press`, `tracker_detector`, and `org_motion_surface` are evidence
-venues (decision events, detection records, corroboration) but do not count
-toward the gate's two-family minimum. The schema records both so the gate
-check is mechanical, not judgment-at-consumption.
+`venue_family` / `gate_family` vocabulary note (gate checkability): the
+Demand-Substrate Hard Gate counts independence across its four demand families
+only — `review_surfaces`, `forums_community`, `search_interest`,
+`retail_presence`. `trade_press`, `tracker_detector`, and
+`org_motion_surface` are evidence venues (decision events, detection records,
+corroboration) but do not themselves count toward the gate's two-family
+minimum. If a trade-press receipt launders a community-originated demand signal,
+`venue_family` stays `trade_press` and `gate_family` records the underlying
+demand family evidenced by the receipt. If no demand family is evidenced,
+`gate_family: none`. The schema records both so the gate check is mechanical,
+not judgment-at-consumption.
 
 ### Candidate entry
 
@@ -230,10 +236,10 @@
 venue_class: newsy | subtle
 observations: []          # observation_ids supporting this entry
 gate_check:               # derived from observations; makes the Hard Gate columns checkable
-  gate_families_seen: []  # of the four demand families; independence stated
+  gate_families_seen: []  # of the four demand families; each backed by observation_ids + independence_basis
   costly_behavior_present: yes | no   # with supporting observation_ids
   integrity_labels_applicable: yes | no
-  org_motion_route: cited_binding | unknown   # cites the owning capture-lane binding; never sets one
+  org_motion_route: available_cited | unavailable_unknown | blocked_outside_current_binding | not_applicable   # cites the owning capture-lane binding when available; never sets one
 decision_owner_pointer:   # public role (named only when the name is itself the public receipt); or unknown
 flags: []                 # FAME | NON_US | BORDER | WEAK | CORR (pool vocabulary, carried verbatim)
 zero_spoiler_feasibility: # backward only — can a pre-cutoff packet be built without outcome leakage? (note, not proof)
```

## Per-change citation map

### Change 1 — add `gate_family`, `gate_family_basis`, and laundering note

- Target original: Candidate Observation Schema used `venue_family` for both gate-counting families and evidence venues.
- Buyer-proof packet, `Demand-Substrate Hard Gate`: a qualified read requires demand signal from at least two independent venue families: review surfaces, forums/community, search interest, retail presence.
- Buyer-proof packet, same section: every venue's evidence carries integrity labels before it enters the fused read; reviews are one fused venue, never the sole basis.
- Beauty venue card set, `The Chain`: NEWSY community origination can launder into trade press; SUBTLE detector evidence can be the record.
- Demand taxonomy, `Read Types`: convergence and divergence depend on independent venue families, wind callers, org motion, and cross-venue disagreement; brand-decision events use trend/wind/integrity as decide-grade context.

### Change 2 — replace `org_motion_route: cited_binding | unknown`

- Target-selection brief, `Qualification Objectives`: confirming the Hard Gate requires no route outside the capture lane's current bindings.
- Target-selection brief, `Stop Rules`: stop if qualification would require a route outside the capture lane's current bindings or an absurd-risk approach.
- Buyer-proof packet, `Demand-Substrate Hard Gate`: org-motion routes follow owning capture decisions, and route-binding changes are capture-lane decisions, never per-proof stretches.

## Verdict

Advisory verdict: keep the patched target only after commissioning-CA adjudication of the two schema changes. I found no design-level defect requiring `NEEDS_ARCHITECTURE_PASS`; the failures are patch-level checkability weaknesses inside the target schema. The diff is intentionally narrow and leaves thesis, guide, frame, pool, brief, overlay, and taxonomy authority untouched.

## Residual risk

The 21-day forward freshness default remains an explicitly labeled adjudication surface, not validated doctrine. The gate-family vocabulary split is now more mechanically checkable, but the consuming lane still needs to enforce the schema by requiring observation IDs and independence basis in actual scan artifacts. No public web research was performed, per commission.

## Provenance

- authored_by: Claude Fable 5 (`claude-fable-5`)
- reviewed_by: GPT-5 (OpenAI), version unrecorded
