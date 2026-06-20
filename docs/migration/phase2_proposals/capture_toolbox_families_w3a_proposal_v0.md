```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a proposal for capture/core/source_capture_toolbox + capture/core/source_families/:
  bloat/deletion candidates with full deletion-evidence records and ontology/doc-term
  findings against the SSOT. Covers orca/product/spines/capture/core/source_capture_toolbox/
  (29 files) and orca/product/spines/capture/core/source_families/ (21 files, 2 sub-dirs:
  social_media/instagram/ + retail_pdp/).
use_when:
  - Owner adjudicating Phase-2 deletion candidates for the capture toolbox and source-family areas.
  - Reviewing ontology/doc-term drift findings before a Phase-3 ratchet.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - Any file in the two scanned areas is moved, renamed, or deleted (inbound ref counts change).
  - A new source family or toolbox artifact is added.
```

# Phase-2 W3a Proposal — capture/toolbox+families

## Summary

Files scanned: 50 (29 in core/source_capture_toolbox/ + 21 in core/source_families/)
Deletion candidates: 0 high / 1 medium / 0 low
Ontology findings: 4

---

## A. Deletion candidates

### Candidate 1 (medium confidence) — `cloakbrowser_packet_runner_architecture_independent_pass_v0.md`

```yaml
targets:
  - orca/product/spines/capture/core/source_capture_toolbox/cloakbrowser_packet_runner_architecture_independent_pass_v0.md
evidence:
  reverse_ref_check: >
    Inbound refs found (grep orca/product/ + docs/ + .agents/):
    - docs/migration/repo_structure_spine_first_v0/moved_paths_index.md:208 (historical path-index row; migration bookkeeping)
    - docs/migration/repo_structure_phase2_consolidation_v0/reference_inventory.md:57 (reference inventory; 3 external hits listed there)
    - orca/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md:356 (direction-change propagation receipt — intentionally_not_updated entry, historical)
    - orca/product/spines/capture/core/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md:686,707,713,715 (the first-pass doc cross-references this as a corroborating artifact; these are historical cross-ref links in the first-pass DCP receipt)
    All references are migration-index bookkeeping or historical DCP receipts. No live source-loading, open_next, or authority-chain pointer outside migration scaffolding. The first-pass doc (cloakbrowser_packet_runner_architecture_v0.md) explicitly absorbed the independent-pass refinements and its DCP receipt records the intentional_not_updated for this artifact. Safe to remove after successor confirmed.
  successor: orca/product/spines/capture/core/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md
  semantic_delta: >
    The independent pass was a corroboration artifact (same architecture recommendation
    TARGET_RECOMMENDED, same contract shape, same packet-before-parser boundaries). Its
    four refinements (exit codes 4/5, storage_state / profile-manager state / proxy endpoint /
    disclosability-inverse language) were absorbed into the first-pass DCP receipt at
    cloakbrowser_packet_runner_architecture_v0.md (recorded in its direction-change
    propagation as intentionally_not_updated). The successor carries the full live adapter
    contract; this artifact is planning-phase corroboration with no live authority.
    No unique content is lost: the delta was the cross-check signal, not a separate ruling.
  rollback: git revert <executing merge sha>
confidence: medium
rationale: >
  superseded-by-v0-first-pass. The independent pass was explicitly commissioned as
  corroboration of the prior pass and explicitly does not overwrite or supersede it
  (per its own §0). The first pass is now the canonical architecture, indexed in the
  Armory README and the capture recon index. The independent pass has no live source-loading
  path — only migration-inventory and historical DCP receipt references. Medium confidence
  (not high) because the first-pass DCP receipt records the independent pass as a stale-language
  search target, which implies it was considered a live surface at DCP time; owner should
  confirm no current lookup chain still reaches this file before executing.
```

---

### Area scan summary — all other files

All remaining 48 files in the two areas are lean. Evidence summary for the higher-count files:

**core/source_capture_toolbox/ (28 files excluding the candidate above):**
- `README.md`: 12+ inbound refs from docs/workflows/, .agents/workflow-overlay/, migration inventory. Canonical Armory entrypoint. Not deletable.
- `capture_recon_index_v0.md`: Referenced in orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md open_next; the recon-doctrine seed. Active.
- `source_capture_playbook_v0.md`: Referenced from .agents/workflow-overlay/source-loading.md:376 as the canonical playbook (retired `capture_investigation_playbook_v0.md` is its pre-rename). Active doctrine.
- `cloakbrowser_packet_runner_architecture_v0.md`: 5+ live inbound refs (retail_pdp spec, capture recon index, reddit playbook, prompt). Canonical architecture.
- `linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md`: 10 inbound refs per migration inventory; referenced by `data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md`, data_capture_spine_consolidation_map, orca_repo_map. Policy-boundary authority.
- `reddit_precommercial_capture_consolidation_planning_thread_v0.md`: Referenced by reddit playbook, consolidation map, orca_repo_map, and multiple decisions. Active Reddit architecture authority.
- `reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`: 15+ inbound refs from docs/decisions/, docs/workflows/, prompts, review-outputs. Active routing artifact.
- `reddit_capture_operator_playbook_v0.md`: Active operator procedure; referenced in README and consolidation map.
- `reddit_packet_consolidation_runner_structural_spec_v0.md`: Referenced in capture recon index (HIGH signal). Spec for packet-first boundary.
- `archive_org_capture_runner_resilience_learnings_v0.md`: Only 1 inbound ref (moved_paths_index migration entry). BUT this is an advisory learnings artifact that feeds a future hardening prompt; the capture-lane hardening prompt is not yet authored. LOW inbound. Owner may choose to propose as bloat once the hardening prompt is authored; not proposed here because the feed-purpose is declared in its header and a successor prompt does not yet exist (successor = "none -- pure bloat" would be incorrect; successor is the unborn hardening prompt).
- `archive_org_refinement_and_source_family_gap_spec_v0.md`: Referenced in review-outputs (4 files), docs/decisions/distillation_binding_data_capture_v0.md, source_capture_playbook_v0.md:226. Active spec; cited in review under adversarial artifact review.
- `cloakbrowser_local_setup_probe_receipt_v0.md`: Referenced in capture recon index. Receipt artifact; provides reachability evidence for the adapter contract. Lean but active evidence.
- `source_capture_toolbox_agent_usability_dry_run_closeout_v0.md`: Only 1 external ref (README DCP receipt). Closeout artifact; lean but indexed in the Armory README's DCP stale-language-search surface list. Low deletion risk but low value; not proposed because it is explicitly called out in the README as part of the controlled-surface list.
- `source_capture_packet_fixture_admission_criteria_v0.md`: 6+ inbound refs from review-outputs, packet_schema/source_capture_packet_schema_evolution_architecture_v0.md, prompts. PROPOSED artifact; live in schema evolution review.
- `armory_weapon_and_pipe_readme_templates_v0.md`, `weapon_anti_block_http_ladder_v0.md`, `weapon_rung15_embedded_payload_extraction_v0.md`, `pipe_block_wall_escalation_v0.md`: All indexed in migration inventory as armory core; cross-referenced among themselves. Active armory vocabulary.
- `source_capture_anti_block_ladder_usage_guide_v0.md`, `source_capture_anti_blocking_http_ladder_daimler_rung_resolution_closeout_v0.md`: Cross-referenced; the usage guide is in the weapon ladder's open_next. Active pair.
- Source-quality files (`source_quality_mini_god_tier_profile_v0.md`, `source_quality_source_unit_queue_template_v0.md`, `source_quality_state_assembler_v0.md`, `source_quality_mixed_source_trial_closeout_v0.md`, `source_quality_cw_p1/p4/p6_end_to_end_pass_closeout_v0.md`, `source_quality_slot3_post_recapture_closeout_v0.md`): All indexed in Armory README as named Armory components; referenced in README's stale-language-search and DCP receipts. The closeout set is operational evidence for the mini-god-tier profile; the profile is referenced in docs/decisions/ and review-outputs. Active.

**core/source_families/ (21 files):**
- All 15 instagram/ files and all 6 retail_pdp/ files have active inbound references from docs/workflows/, docs/decisions/, other orca/product/ files, or from each other's open_next chains. No abandoned orphans.
- `ig_capture_findings_consolidated_v0.md`: 10+ inbound refs; the IG signal consolidation document.
- `ig_creator_roster_frontier_ledger_spec_v0.md`, `ig_creator_discovery_spec_v0.md`, `orca_creator_momentum_pipeline_architecture_v0.md`, `orca_creator_monitoring_policy_architecture_v0.md`: All referenced in docs/hygiene/ig_creator_momentum_lane_handoff_v0.md and cross-referenced; active IG lane architecture.
- `ig_capture_shape_contract_spec_v0.md`: Referenced in orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md (3 hits). Active.
- `retail_pdp_typed_envelope_probe_v0.md`: Referenced in docs/workflows/ (2 hits), orca/product/spines/data_lake/ (2 hits), consolidation plan. Active.
- `demand_durability_multi_retailer_rendered_capture_spec_v0.md`, `demand_durability_us_storefront_pin_recon_verdict_v0.md`: Both have inbound refs from retail_pdp/retail_pdp_projection_contract_v0.md and retail_pdp_projection_playbook_v0.md. Active.

---

## B. Ontology / doc-term findings

SSOT canonical types (from ontology.yaml): `Vertical`, `Brand`, `Product`, `Venue`, `WindCaller`, `Call`, `Observation`, `TrendVector`, `DecisionEvent`, `Reading`, `Memo`, `Case`, `Outcome`, `CapturePacket`, `EvidenceUnit`, `Buyer`, `Org`.
Runtime/storage aliases (from runtime_bindings): `SourceCapturePacket` (alias for `CapturePacket`), `FacilitatorLedger` (alias for `Case`), `CaseReport` (composed with `Case`).

**Finding 1 — `SubNiche` used as ontology-shaped term in core/source_families/social_media/instagram/ (not in SSOT)**

- Term: `SubNiche`
- File:line:
  - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_discovery_suggested_accounts_recon_v0.md:122,131` (prose: "ontology `SubNiche` / keyword filter")
  - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_discovery_spec_v0.md:25,103,107,109` (prose: "ontology backbone is adopted and SubNiche becomes a live classifier"; "live in the ontology's `SubNiche` object type — a candidate object"; "forward owner"; "re-expressed in `SubNiche` terms on adoption")
- SSOT status: NOT in ontology.yaml as a type. The backbone architecture folds SubNiche into `Vertical` (self-parent via `narrows_to`; see backbone §"Folds applied" and ontology.yaml namespaces where `vertical:` supports dotted sub-niche). `SubNiche` is a deprecated candidate folded away at design time.
- Proposed fix (read-only): Both files should qualify uses of `SubNiche` as the deprecated candidate name (folded into `Vertical` self-parent). Preferred prose in new text: "sub-niche (`vertical:beauty.fragrance`-style Vertical)" or "sub-niche level of Vertical". The existing references are accurately flagged as forward-links to a non-adopted type, and the ig_creator_discovery_spec_v0.md correctly notes this is awaiting adoption — so the usage is epistemically honest, not a drift error. No silent rename needed; the two files already annotate the status. Future sessions authoring near these files should not coin new `SubNiche` type references as if adopted.

**Finding 2 — `SourceCapturePacket` used as a standalone type name in retail_pdp and other toolbox files**

- Term: `SourceCapturePacket`
- File:line:
  - `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md:63,126` ("SourceCapturePacket stays canonical", "-> SourceCapturePacket [canonical raw authority]")
  - `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md:77` ("a preserved `SourceCapturePacket`")
  - `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md:79` ("existing `SourceCapturePacket`")
  - `orca/product/spines/capture/core/source_capture_toolbox/armory_weapon_and_pipe_readme_templates_v0.md:24,35` ("produces a `SourceCapturePacket`")
  - `orca/product/spines/capture/core/source_capture_toolbox/cloakbrowser_packet_runner_architecture_independent_pass_v0.md:254,255` (references `SourceCapturePacket` model)
- SSOT status: `SourceCapturePacket` is a RECORDED STORAGE ALIAS for ontology type `CapturePacket` (per `ontology.yaml runtime_bindings.CapturePacket.name_alias`). This is a valid alias per the ID-doctrine pattern (forward-only, both resolve). NOT a non-SSOT term; not drift. Usage is correct — these files use the runtime class name.
- Proposed fix: None required. Usage is SSOT-aligned. For clarity, new docs may prefer the canonical ontology name `CapturePacket` in prose type references and reserve `SourceCapturePacket` for code-identifier contexts (the alias pattern intent), but the current usage is not wrong.

**Finding 3 — Stale internal H1 title in `source_capture_playbook_v0.md`**

- Term: not a type-term finding; a doc-hygiene finding
- File:line: `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md:33` (H1 reads "Capture-Investigation Playbook (v0, review-hardened + risk-posture-amended)")
- Context: The file was renamed from `capture_investigation_playbook_v0.md` to `source_capture_playbook_v0.md` as noted in `archive_org_refinement_and_source_family_gap_spec_v0.md:38-40` and `.agents/workflow-overlay/source-loading.md:376`. The external path is correct but the internal H1 still says "Capture-Investigation Playbook". The `archive_org_refinement_and_source_family_gap_spec_v0.md` explicitly calls this out as "title-only drift, not a content fork."
- Proposed fix (read-only): In a future edit, update the H1 of `source_capture_playbook_v0.md` line 33 from "Capture-Investigation Playbook" to "Source Capture Playbook". Low-priority; already documented; not a deletion or authority issue.

**Finding 4 — Stale inbound reference to `capture_investigation_playbook_v0.md` inside the scanned area**

- Term: not an ontology term; a stale-path finding
- File:line: `orca/product/spines/capture/core/source_families/social_media/instagram/ig_wind_caller_capture_feasibility_recon_v0.md:108` (names `capture_investigation_playbook_v0.md` as the commission's source-loading target, then self-corrects inline: "actual: `source_capture_playbook_v0.md`")
- Context: The recon correctly self-notes the naming gap in-document. The corrected path resolves. Additional out-of-scope refs to `capture_investigation_playbook_v0.md` exist in `docs/research/orgmotion_beautypie_capture_feasibility_v0.md:19` and `docs/hygiene/topicals_case2_lane_log_v0.md:64` (both outside this scan area); source-loading.md:376 already flags the retirement.
- Proposed fix (read-only): The in-scope reference is self-correcting and no action blocker. For future hygiene: `ig_wind_caller_capture_feasibility_recon_v0.md:108` could be simplified to drop the old name now that the new name is confirmed. Not load-bearing; no runtime/authority impact.
