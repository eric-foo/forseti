---
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a deletion + ontology proposal for orca/product/spines/commission_signal_board/
  (~9 files). Read-only scan; no source edits. For owner adjudication before any execute PR.
use_when:
  - Deciding whether any commission_signal_board spine file is a Phase-2 deletion candidate.
  - Reviewing ontology / doc-term health of the commission_signal_board area before a cleanup pass.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - The commission_signal_board spine is retired, renamed, or merged into another spine.
  - A Phase-2 execute PR lands deletions in this area.
---

# Phase-2 W3a Proposal -- commission_signal_board

## Summary

Area: `orca/product/spines/commission_signal_board/` (9 files scanned).
Every file is canonically registered in `spine.yaml` and carries live inbound
references from within the spine and from external governed surfaces. No file is
pure bloat or a superseded duplicate. The area is lean: no deletion candidates
at any confidence level. Ontology / doc-term scan is clean for this area.

## A. Deletion candidates

None -- area is lean.

Evidence per file:

**README.md**
- External inbound: `docs/workflows/orca_repo_map_v0.md:392` (directory entry);
  `spine.yaml:11` (canonical_artifacts.readme); all 7 other area files in their
  `open_next` chains.
- Role: live spine entry point (status `LIVE_PILOT_SPINE`); canonical discovery
  target for all CSB work.
- Verdict: not a candidate.

**spine.yaml**
- External inbound: `README.md` open_next; referenced indirectly by every area
  file as the canonical manifest.
- Role: machine-readable spine manifest; lists all 7 canonical artifact paths.
  Removing it breaks the manifest contract for the pilot spine.
- Verdict: not a candidate.

**Prompt Structure Rules: authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md**
- External inbound:
  `docs/migration/phase2_proposals/scanning_w3a_proposal_v0.md:31` (reverse-ref
  check on scanning area); `scanning_w3a_proposal_v0.md:36` (second cite for
  LinkedIn lane index); `spine.yaml:13`; `README.md:33`; `prompts/...prompt_v0.md:18`.
- Role: Prompt Structure Rules document establishing the signal-board boundary vs gate
  semantics. Referenced by the scanning area proposal as an active outbound
  authority pointer; not superseded.
- Verdict: not a candidate.

**dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md**
- External inbound:
  `orca/product/spines/scanning/admissibility_checkability/orca_demand_scan_gate_adjudication_packet_v0.md:21` (open_next);
  `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md:195` (canonical path record);
  `docs/migration/orca_second_pass_consolidation_plan_v0.md:95` (B5 closed confirmation);
  `docs/decisions/orca_search_product_lane_binding_v0.md:53` (lane binding reference);
  `docs/decisions/orca_spine_first_blocker_authorization_v0.md:48` (B5 settlement record);
  `authority/...adjudication_packet_v0.md:21` (open_next).
- Role: the B5-settled gate-run commission criteria; PROPOSED status (owner
  ratification pending before it governs an actual commission). Still the live
  criteria artifact; no successor exists.
- Verdict: not a candidate. PROPOSED status is part of the artifact's stated
  semantics, not a deletion trigger.

**harness/validator.md**
- External inbound: `spine.yaml:15` (validator_pointer); `README.md:36`;
  `tests/validator_tests.md:14` (open_next); `prompts/...prompt_v0.md:19`
  (indirect via open_next chain to .agents/hooks/check_commission_signal_board_output.py).
- Role: pointer to `.agents/hooks/check_commission_signal_board_output.py`;
  explains why the script stays outside the spine. Removing it breaks the spine's
  harness discovery path.
- Verdict: not a candidate.

**migrations/moved_paths_index.md**
- External inbound: `spine.yaml:17`; `README.md:38,56`.
- Role: canonical old-path resolver for the three artifacts that moved from
  `docs/` into the spine. Active reverse plan documented.
- Verdict: not a candidate.

**Prompt Structure: prompts/orca_commission_signal_board_prompt_v0.md**
- External inbound: `spine.yaml:15`; `README.md:34`; `workflows/...playbook_v0.md:16,26,178`.
- Role: the full v0 durable prompt artifact (chat-only mode). No v1 or
  successor exists; still the live dispatching artifact.
- Verdict: not a candidate.

**tests/validator_tests.md**
- External inbound: `spine.yaml:16`; `README.md:37`; `harness/validator.md:14`.
- Role: pointer to `orca-harness/tests/unit/test_commission_signal_board_output_validator.py`
  and fixtures; explains why executable tests stay in orca-harness.
- Verdict: not a candidate.

**workflows/commission_signal_board_playbook_v0.md**
- External inbound: `spine.yaml:14`; `README.md:35`; `prompts/...prompt_v0.md:17,34,50`;
  `harness/validator.md:13`.
- Role: operating sequence for the CSB lane. No successor; playbook is the live
  run-sequence authority.
- Verdict: not a candidate.

## B. Ontology / doc-term findings

Clean.

The `check_doc_terms.py --report-orca` tool scanned all 218 files under
`orca/product/` (excluding `foundation/ontology/`). Two new-term candidates
were found repo-wide (`FailureEvent` -- 13 refs in 2 files; `RetailPdpProjectionPacket`
-- 1 ref in 1 file). Neither appears in any commission_signal_board area file
(confirmed by targeted regex scan over `orca/product/spines/commission_signal_board/**/*.md`).

SSOT-known ontology type references (e.g. `EvidenceUnit`, `SourceCapturePacket`,
`DecisionEvent`) are used contextually correctly in both the Prompt Structure Rules document
and the Prompt Structure (the prompt explicitly routes evidence and provenance language
consistent with the SSOT's adopted type roster). No deprecated aliases, no
non-SSOT type coinages, no new-term candidates in this area.

No proposed ontology read-only fixes needed.
