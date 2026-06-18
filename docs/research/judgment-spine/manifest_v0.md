# Judgment Spine Manifest v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Manifest of Judgment Spine cases, prompts, artifact status, and known residue.
use_when:
  - Finding the current Judgment Spine case inventory.
  - Finding the working Judgment Harness spec.
  - Checking whether a case is complete enough for blind reuse or lesson extraction.
  - Selecting the next case without relying on chat memory.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/README.md
  - orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
  - docs/research/judgment-spine/judgment_spine_thesis_v0.md
  - docs/research/judgment-spine/harness/v0_14/index.md
  - docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/case_index.md
  - docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md
  - docs/research/judgment-spine/cases/canoo-walmart/case_index.md
  - docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
```

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S1 plus target Judgment Spine artifacts
  edit_permission: docs-write
  target_scope: Create a compact Judgment Spine manifest for current cases and residue.
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Status

- manifest_status: maintained index
- current_scope: docs-tree case tracks (Milwaukee, Unity, Canoo/Walmart, Daimler carve-out, two DvC frame-locks), harness-side product-learning realizations plus the backtest batch-1 pointer, preservation prompt, and the v0.14 Judgment Harness spec inventory
- maintenance_note: brought current 2026-06-11 (hygiene rows ORCA-HYGIENE-009/012) — daimler case track and fixture-prep set indexed, batch-1 ledger referenced, six stale pre-Phase-2 `docs/product/` paths re-pointed to their by-lane homes
- dirty_state_note: workspace was dirty before this manifest was created; this manifest only indexes the scoped Judgment Spine files
- strict_claims: not proven

## Parent Contract

- `docs/research/judgment-spine/README.md`

## Parent Thesis

| Path | Role | Status |
| --- | --- | --- |
| `docs/research/judgment-spine/judgment_spine_thesis_v0.md` | Long-term Judgment Spine optimization thesis | Working thesis; not validation, readiness, implementation authorization, or CA execution |
| `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md` | Operating contract for consuming, protecting, and applying the parent thesis | Working contract; not validation, readiness, approval, implementation authorization, or source-of-truth promotion |

## Operating Model And Gate Doctrine

| Path | Role | Status |
| --- | --- | --- |
| `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md` | Conductor that sequences gates JSG-01 to JSG-10 with mechanical receipt predicates, total fail/blocked transitions, a by-hand isolation cap, and named run lifecycle states | Working operating model; routes and verifies receipts; not validation, readiness, scoring, fixture admission, or judgment-quality evidence |
| `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md` | Claim-tier and closeout-state vocabulary the conductor routes to | Controlling doctrine |
| `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md` | Gate ownership the conductor sequences | Controlling doctrine |
| `docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md` | JSG-08 receipt shape the conductor reads | Controlling doctrine |

## Reusable Prompt

| Path | Role | Status |
| --- | --- | --- |
| `docs/prompts/deep-thinking/orca_judgment_spine_case_learning_preservation_prompt_v0.md` | Preservation prompt for post-reveal case learning | Exists; not a skill; not evidence of adoption |
| `docs/prompts/deep-thinking/judgment_spine_thesis_operating_contract_ca_prompt_v0.md` | CA prompt for creating the Judgment Spine thesis operating contract | Exists; prompt artifact only; not CA execution, validation, readiness, or implementation authorization |

## Judgment Harness Spec Inventory

| Path | Role | Status |
| --- | --- | --- |
| `docs/research/judgment-spine/harness/README.md` | Harness allocation point | Exists; routing artifact only |
| `docs/research/judgment-spine/harness/v0_14/index.md` | v0.14 Judgment Harness spec index | Working spec index; does not authorize implementation by itself |
| `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md` | Case-to-v0.14 bridge foundation | Working non-implementation bridge; selects Unity as first bridge candidate and preserves not-proven boundaries |
| `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md` | Unity v0.14 fixture extraction plan | Working docs-only extraction plan; maps Unity into fixture-admission surfaces and preserves probe, leakage, scoring, implementation, and proof non-claims |
| `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md` | Unity v0.14 draft fixture pack receipt | Draft docs-only fixture pack; blocked before scoring; does not authorize implementation, probe execution, model runs, validation, scoring, proof, product proof, or lesson promotion |
| `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md` | Canoo/Walmart v0.14 draft fixture pack receipt | Draft docs-only fixture pack; blocked before scoring; does not authorize implementation, probe execution, model runs, validation, scoring, proof, product proof, or lesson promotion |
| `docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/` | Daimler corporate-structure vote 2019 fixture-prep set (fixture entry plan, source acquisition plan + receipt, evidence registry draft, participant packet draft + conversion plan, memorization-probe request prep, facilitator work queue) | Draft docs-only prep set; no `fixture_authoring_receipt` yet; blocked before scoring; does not authorize implementation, probe execution, model runs, validation, scoring, proof, product proof, or lesson promotion |
| `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md` | Numeric action-band mapping source | Imported v0.14 spec |
| `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md` | Mapping function interface and behavior | Imported v0.14 spec |
| `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md` | Pydantic-ready schema contracts | Imported v0.14 spec |
| `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md` | Band scoring formulas | Imported v0.14 spec |
| `docs/research/judgment-spine/harness/v0_14/review_prompts/` | Imported review prompts for v0.14 readiness/sanity checks | Side prompt material; not active review result |
| `docs/research/judgment-spine/harness/adjacent-context/README.md` | Side-context index | Context only; not controlling v0.14 spec authority |

## Case Inventory

| Case | Folder | Learnability tier | Spoiler state | Current status |
| --- | --- | --- | --- | --- |
| inoreader-repricing (DvC) | `docs/research/judgment-spine/cases/inoreader-repricing/` | decide-vs-confirm subject; tier TBD | Frame-locked; outcome sealed facilitator-side | Frame-lock only; participant packet, ledger, evidence, sealed outcome `NEEDS_CAPTURE` |
| craft-expressionengine (DvC) | `docs/research/judgment-spine/cases/craft-expressionengine/` | decide-vs-confirm subject; tier TBD | Frame-locked; outcome sealed facilitator-side | Frame-lock only; participant packet, ledger, evidence, sealed outcome `NEEDS_CAPTURE` |
| Milwaukee fiscal crossroads | `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/` | Tier 0 candidate, single-case transfer unproven | Revealed | Reveal readout exists; case index exists; source packet and safety artifacts still missing |
| Unity Runtime Fee monetization crossroads | `docs/research/judgment-spine/cases/unity-runtime-fee/` | Tier 0 candidate, single-case transfer unproven | Revealed | Reveal readout exists; case index exists; canonical source packet, sealed memo, and outcome calibration exist in `docs/product/`; participant packet and safety artifacts still missing |
| Canoo/Walmart last-mile EV fleet commitment | `docs/research/judgment-spine/cases/canoo-walmart/` | Tier 0 case learning captured; artifact volume is not readiness; not repeatability proof, scoreable fixture, or model validation | Revealed and qualitatively calibrated | Case index, preflight, source packet, safety receipt, adversarial source-packet review, participant packet, blind LLM judgment, owner-assisted judgment, pre-reveal comparison, facilitator ledger, reveal readout, calibration-gate adversarial review, outcome calibration, JSG-08 reveal/calibration receipt, fixture-admission review, and draft v0.14 fixture pack exist; no model run, score, or score-ready fixture exists |
| Daimler corporate-structure vote 2019 (carve-out) | `docs/research/judgment-spine/cases/daimler-carve-out/` | Case-2 candidate per the selection rule below; tier TBD | Not assessed in this index pass | Case-02 preflight, participant packet, and safety receipt exist (indexed 2026-06-11 per ORCA-HYGIENE-009); fixture-prep set exists in the harness tree (row above); case index, source packet, facilitator ledger, blind judgments, and reveal artifacts not present in the track |

## Harness-Side Product-Learning Realizations (2026-06-11)

Distinct from the docs-tree case track above: a product-learning cross-vendor blind
exam was built and **run in the harness** on the Inoreader 2019 decide-vs-confirm
subject at `orca-harness/cases/product_learning/inoreader_repricing_2019_v0/` plus an
anonymized re-skin at `.../feedhaven_repricing_2019_anon_v0/`. Each carries a
participant packet, evidence units, a frozen facilitator ledger, and scored contestant
runs; the Inoreader dir also carries `cross_vendor_blind_run_findings_v0.md`.

| Field | State |
| --- | --- |
| Tier | **Capped at product-learning** (by-hand contestants; instructed/attested isolation; one sub-agent run verified `tool_uses=0`). |
| Relation to the `inoreader-repricing` row above | Realizes that frame-lock **subject** in a different tree (harness `cases/`, not the docs case track). It is **not** the docs-tree case-track artifacts and does **not** clear its `NEEDS_CAPTURE`. |
| Headline findings (honest; detail in the findings doc) | Anti-over-reach replicated across vendors; anonymizing a famous case did **not** defeat strong recognizers (structural fingerprint re-identifies even neutral-framed); the scored band floor (3 vs 4) is **contested/unresolved**; a dr construct-critique of the scoring key was **walked back by cross-family review** — open thread is an *architecture pass* (surface band-input definitions → re-author → re-harden). |
| Working discipline adopted | Claim-lifecycle (confidence-label + kill-criterion per finding; de-correlation-harden before any durable action) — itself a **hypothesis**, not doctrine. |
| Caps | Not judgment-quality, not buyer-proof, not a scoreable fixture; the JSG-08-style reveal/calibration here is by-hand product-learning only. |

## Backtest Batch 1 Pointer (product-learning)

The active backtest batch is governed by its own pre-declared decision record:
`docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
(`BATCH1_ACTIVE_OWNER_SIGNED`, 2026-06-11; six cases — the two harness
realizations above as retro dev cases plus four beauty-vertical cases, two of
them holdouts; pinned scoring key; swap pool; all-results rule; dated
org-motion amendment for case #3). This manifest only routes to it: the ledger
owns batch scope, execution rules, and amendments; per-case findings records
land as they run, and the batch closes with one distillation record.

## Milwaukee Artifact Status

| Artifact | Path | Status |
| --- | --- | --- |
| Case index | `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/case_index.md` | Created for navigation and residue tracking |
| Reveal readout | `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/reveal_readout_v0.md` | Exists |
| Initial blind judgment | `docs/decisions/consultant_loop/milwaukee_initial_judgement.md` | Exists outside case folder |
| Owner judgment | `docs/decisions/consultant_loop/milwaukee_owner_judgement.md` | Exists outside case folder |
| Participant packet | `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/participant_packet_v0.md` | Missing |
| Safety receipt | `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/safety_receipt_v0.md` | Missing |
| Consolidated blind judgments | `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/blind_judgments_v0.md` | Missing |

## Unity Runtime Fee Artifact Status

| Artifact | Path | Status |
| --- | --- | --- |
| Case index | `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md` | Created for navigation and residue tracking |
| Reveal readout | `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md` | Exists |
| Pre-cutoff source packet | `docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` | Exists outside case folder |
| Sealed at-cutoff memo | `docs/product/core_spine/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` | Exists outside case folder |
| Outcome calibration | `docs/product/core_spine/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` | Exists outside case folder |
| Draft v0.14 fixture pack | `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md` | Draft docs-only pack exists; blocked before scoring and not probe-safe or score-ready |
| Adjacent MV-04 method replay | `docs/product/core_spine/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md` | Exists outside case folder; secondary method-validation evidence |
| Participant packet | `docs/research/judgment-spine/cases/unity-runtime-fee/participant_packet_v0.md` | Missing |
| Safety receipt | `docs/research/judgment-spine/cases/unity-runtime-fee/safety_receipt_v0.md` | Missing |
| Consolidated blind judgments | `docs/research/judgment-spine/cases/unity-runtime-fee/blind_judgments_v0.md` | Missing |

## Canoo/Walmart Artifact Status

| Artifact | Path | Status |
| --- | --- | --- |
| Case index | `docs/research/judgment-spine/cases/canoo-walmart/case_index.md` | Created for navigation and residue tracking |
| Case-track preflight | `docs/research/judgment-spine/cases/canoo-walmart/case_track_preflight_v0.md` | Created; recommends source-packet step under zero-spoiler cutoff discipline |
| Source packet | `docs/research/judgment-spine/cases/canoo-walmart/source_packet_v0.md` | Created; clean pre-cutoff source substrate candidate |
| Safety receipt | `docs/research/judgment-spine/cases/canoo-walmart/safety_receipt_v0.md` | Created; adversarial review completed before participant packet |
| Adversarial source-packet review | `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_source_packet_safety_adversarial_artifact_review_v0.md` | Completed; recommendation `accept_with_friction` for participant-packet authoring |
| Participant packet | `docs/research/judgment-spine/cases/canoo-walmart/participant_packet_v0.md` | Created; candidate for blind judgment capture, not sealed judgment or validation |
| Blind judgments | `docs/research/judgment-spine/cases/canoo-walmart/blind_judgments_v0.md` | Created; user-supplied blind LLM contestant result, not independently verified clean |
| Owner-context judgments | `docs/research/judgment-spine/cases/canoo-walmart/owner_context_judgments_v0.md` | Created; owner-assisted judgment, separate from blind result |
| Pre-reveal judgment comparison | `docs/research/judgment-spine/cases/canoo-walmart/pre_reveal_judgment_comparison_v0.md` | Created; freezes comparison between blind LLM and owner-assisted judgments before reveal |
| Facilitator ledger | `docs/research/judgment-spine/cases/canoo-walmart/facilitator_ledger_v0.md` | Created; sealed facilitator-only actual-action, agreement, and outcome source ledger |
| Reveal readout | `docs/research/judgment-spine/cases/canoo-walmart/reveal_readout_v0.md` | Created; qualitative facilitator-side readout, not scoring or outcome calibration |
| Calibration-gate adversarial review | `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_reveal_readout_calibration_gate_adversarial_artifact_review_v0.md` | Completed; recommendation `accept_with_friction` before outcome calibration |
| Outcome calibration | `docs/research/judgment-spine/cases/canoo-walmart/outcome_calibration_v0.md` | Created; qualitative split-axis calibration, no score or validation claim |
| JSG-08 reveal/calibration receipt | `docs/research/judgment-spine/cases/canoo-walmart/jsg_08_reveal_calibration_receipt_v0.md` | Created; companion receipt applies the JSG-08 owner contract and caps the case at qualitative learning only |
| Fixture-admission adversarial review | `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_fixture_admission_scoring_readiness_adversarial_artifact_review_v0.md` | Completed; recommendation `accept_with_friction`; admits fixture authoring only, not scoring |
| Draft v0.14 fixture pack | `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md` | Draft docs-only pack exists; blocked before scoring and not probe-safe, blind-run-clean, or score-ready |

## Selection Rule For Case 2

Do not start case 2 from brand prestige or consulting-firm authorship alone. Select the next case because it has a reconstructable decision, clean cutoff, visible tradeoff, revealed action or outcome, and enough source depth to expose judgment misses.

## Non-Claims

- This manifest does not validate the Judgment Spine.
- This manifest does not prove the Milwaukee lesson transfers.
- This manifest does not make any case product-ready, buyer-validated, or model-training-ready.
- This manifest does not authorize scraping, automation, fine-tuning, custom infrastructure, or a miner.
