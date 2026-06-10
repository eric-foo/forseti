# Unity Runtime Fee v0.14 Fixture Authoring Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Receipt for the docs-only Unity Runtime Fee v0.14 draft fixture pack.
use_when:
  - Checking what was authored in the draft Unity v0.14 fixture pack.
  - Verifying blocked-before-scoring status before any later review or patch.
  - Finding the source-read ledger and hard gates for the draft pack.
authority_boundary: retrieval_only
input_hashes:
  fixture_authoring_prompt: E04DC7C16F733E827709EDEC32CC5BADE6F2F273225916B5F92DC6A3B4FD0E23
  extraction_plan: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  source_packet: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
  pydantic_schema_reference: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  case_construction_protocol: FDEA14A1767D135A8DD56AF073AF0E5E3206B945FB9E603F597491D795889C71
  band_input_labeling_rubric: 0CE6E9584F4F1C4716559A654870AF43EBED3E5D53D3279AB658993B7DE1C2AE
  post_authoring_review: BB1EAD239DF2A1EE5704B888BD5F1F261B0E2DD2D656E5FCB4330708A19C674C
open_next:
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
  - docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md
```

- Status: DRAFT_FIXTURE_PACK_BLOCKED_BEFORE_SCORING
- Artifact type: docs-only draft fixture pack receipt
- Draft fixture root: `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/`
- Implementation, runtime, package, test, automation, model run, memorization-probe execution, scoring execution, validation execution, proof-run, product-proof, lesson-promotion, commit, push, or PR authorized: no
- Strict readiness, validation, acceptance, source-of-truth promotion, probe-safety, score-readiness, harness superiority, product-proof, or lesson-promotion claims: not proven

## Source Context Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus Unity fixture-authoring prompt, patched extraction plan, Unity review report, v0.14 schemas/protocols, Unity source packet, sealed memo, outcome calibration, and reveal readout
  edit_permission: docs-write
  target_scope: Create the docs-only Unity v0.14 draft fixture pack and narrow discovery pointers only.
  dirty_state_checked: yes
  blocked_if_missing: no
source_context_status: SOURCE_CONTEXT_READY
method_sequence:
  workflow_deep_thinking_reference_loaded: yes
  applied_only_after_source_context_ready: yes
```

Repository state caveat: `git status --short --branch` showed `main...origin/main [ahead 17]`, modified Orca overlay and docs files, and many untracked Judgment Spine, prompt, review, and Unity specimen files before this fixture pack was authored. These sources were used for this bounded draft pack, but dirty or untracked state does not prove acceptance, validation, readiness, source-of-truth promotion, implementation authorization, probe-safety, score-readiness, product proof, or harness superiority.

## Working Notes - Goal Fit

The source-loaded task still fits the anchor goal: define a case-to-v0.14 bridge lane that maps existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation.

The source-loaded task still fits the success signal: this draft pack exposes the minimum Unity harness-entry shape, names the v0.14 specs controlling participant packet, evidence registry, facilitator ledger, blind-judgment adaptation, probe, scoring, and failure logging, exposes missing or unsafe inputs, and names later implementation implications only as non-executable context.

The source-loaded task still fits the selected next move output-fit check: the pack writes a participant packet draft, evidence registry draft, facilitator ledger draft, sealed-memo adapter note, and this receipt while remaining blocked before scoring and without authorizing implementation, probe execution, model runs, scoring, validation, proof, product proof, or lesson promotion.

No `BLOCKED_GOAL_CONFLICT` was found.

## Canonical Draft Case ID

```yaml
case_id: unity_runtime_fee_2023_v0_14
case_id_status: frozen_for_this_docs_only_draft_pack
format_basis: lowercase filesystem-safe slug with digits and underscores only
non_claim: This case ID freeze is draft-pack consistency only; it is not fixture admission, probe pass, score-readiness, validation, or source-of-truth promotion.
```

## Draft Fixture Pack Inventory

| Artifact | Path | Status |
| --- | --- | --- |
| Fixture authoring receipt | `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md` | Created; this file |
| Participant packet draft | `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md` | Created; packet-safe draft only |
| Evidence registry draft | `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md` | Created; per-source hashes and timestamps missing |
| Facilitator ledger draft | `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md` | Created; ledger not frozen |
| Sealed memo adapter note | `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/sealed_memo_adapter_note_v0.md` | Created; advisory adapter note only |

## Post-Review Patch Receipt

```yaml
review_report: docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_draft_fixture_pack_adversarial_review_v0.md
review_report_hash: BB1EAD239DF2A1EE5704B888BD5F1F261B0E2DD2D656E5FCB4330708A19C674C
patched_findings:
  AR-01: participant packet permitted-assumption wording no longer echoes facilitator must-address conclusion
  AR-02: EU-08 removed from participant-facing evidence summaries and preserved as unresolved source-gap adapter matter
  AR-03: S-01 SEC accession filing locator added to participant source manifest
  AR-04: inherited Phase 0 option-laden decision question caveat recorded below without changing the draft decision frame
  AR-05: fixture-side participant packet distinction from case-folder residue recorded below
  AR-06: upstream input_hashes added to fixture-pack artifact retrieval headers
post_review_status: patched_draft_only_not_accepted_not_validated_not_score_ready
```

Phase 0 framing caveat: `participant_packet_draft_v0.md` intentionally preserves the inherited Phase 0 option-laden decision question for this draft fixture pack. A later clean v0.14 participant-packet authoring lane must decide whether to keep that frame or restate it more neutrally before blind contestant use.

Fixture-side participant packet distinction: `participant_packet_draft_v0.md` is a harness-side v0.14 fixture draft. It does not satisfy, retire, or replace the missing case-folder `participant_packet_v0.md` residue listed for the parent Unity case.

## Hard Blockers Before Scoring

- Clean participant packet hash: not computed for readiness; the packet remains a draft.
- Per-source source-byte hashes: missing for S-01, S-03, S-04, S-05, S-06, S-07, and any source retained from the source ledger.
- Per-source retrieval timestamps: not normalized into v0.14 EvidenceUnit fields.
- EU-08 adapter decision: unresolved; currently treated as an excluded or gap-note candidate, not affirmative evidence.
- Facilitator ledger freeze: not performed; `ledger_freeze_hash` is `NOT_COMPUTED`.
- Frozen band inputs: not frozen; all labels remain candidate or unfrozen.
- Second-label audit: not performed.
- Must-address items: candidate only; not frozen.
- `decision_shape`: candidate protocol/run metadata only; not frozen for a contestant output.
- Memorization probe: not run for any model family; Unity probe-safety is not proven.
- Sealed memo adapter: unresolved; the legacy memo is not a fresh contestant run and is not directly comparable to future contestant outputs.
- BlindJudgement schema instance: not created.
- Participant packet hash, facilitator ledger hash, prompt hash, run metadata, evidence IDs, and must-address coverage for any contestant output: missing.
- Mapping and scoring: not run; no action band, scoring result, case report, or failure event exists.

## Leakage And Memorization Gates

Participant-facing drafting used only the pre-cutoff Unity source packet and v0.14 packet requirements. The participant draft excludes facilitator labels, later post-cutoff event material, hidden judgement material, calibration material, and scoring hints.

Facilitator-only material was used only in `facilitator_ledger_draft_v0.md` and `sealed_memo_adapter_note_v0.md`.

Unity remains a widely public real-world case with elevated memorization risk. A memorization probe must run before a contestant/model family sees the participant packet. Probe `fail` rejects or quarantines the contestant-case pair for that model family. Probe `ambiguous` quarantines until operator review. Probe `pass` is model-family scoped and still does not prove no memorization.

## Not-Proven Boundaries

This draft pack does not prove:

- Judgment Spine validation;
- v0.14 harness validation;
- case admission;
- participant-packet cleanliness for blind use;
- memorization-probe pass;
- scoring readiness;
- implementation readiness;
- source-of-truth promotion;
- acceptance or approval;
- buyer validation;
- product readiness;
- feature readiness;
- commercial readiness;
- model-training readiness;
- harness superiority;
- memory compounding;
- lesson transfer or lesson promotion.

## Source-Read Ledger

| Source | Why read |
| --- | --- |
| `AGENTS.md` and `.agents/workflow-overlay/README.md` | Workspace and overlay authority. |
| `.agents/workflow-overlay/source-of-truth.md`, `source-loading.md`, `prompt-orchestration.md`, `artifact-roles.md`, `artifact-folders.md`, `validation-gates.md`, `retrieval-metadata.md` | Source hierarchy, source budget, method sequencing, artifact role, accepted folder, completion gates, and retrieval metadata. |
| `docs/workflows/orca_repo_map_v0.md` | Repo navigation and Judgment Spine area. |
| `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md` | Commissioning prompt, output paths, boundaries, and required closeout. |
| `docs/research/judgment-spine/judgment_spine_thesis_v0.md` and `judgment_spine_thesis_operating_contract_v0.md` | Parent Judgment Spine goal, layer boundary, drift guard, and non-claims. |
| `docs/research/judgment-spine/README.md` and `manifest_v0.md` | Case unit, learnability tiers, current case inventory, and harness inventory. |
| `docs/research/judgment-spine/harness/v0_14/index.md` | v0.14 spec index and source-of-truth roles. |
| `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md` | Bridge recommendation and minimum harness-entry shape. |
| `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md` | Patched extraction plan controlling this fixture-authoring lane. |
| `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md` | Prior review findings and patched distinctions to preserve. |
| `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md` | Unity case artifact status, spoiler state, and missing residue. |
| v0.14 protocol and schema files | Participant packet, EvidenceUnit, FacilitatorLedger, band inputs, BlindJudgement, mapping, scoring, probe, and failure-log controls. |
| `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` | Packet-safe pre-cutoff Unity evidence and source gaps. |
| `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` | Facilitator-only legacy sealed memo and adapter gap context. |
| `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` | Facilitator-only calibration and parent-only exclusion context. |
| `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md` | Facilitator-only reveal/readout and parent-only lesson boundary. |

Sources deliberately not read: optional proof/memory plan, phase 1 infrastructure architecture, Daimler fallback files, all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, implementation code, tests, packages, and runtime files. They were not needed to write this docs-only draft pack.

## Next Authorized Step

The next authorized step is a docs-only adversarial artifact review of this draft fixture pack, or owner-authorized patching of specific fixture-authoring defects. Do not route directly to implementation, probe execution, model runs, scoring, validation, proof-run, product-proof, lesson promotion, or harness-superiority claims.
