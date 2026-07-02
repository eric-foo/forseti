# Fragrantica Cleaning Audit Pack Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: workflow handoff packet
scope: Cold-reader handoff for splitting Fragrantica Cleaning audit packs from post-cleaned Silver records.
use_when:
  - Continuing Fragrantica Cleaning lake representation after FCR-04.
  - Deciding where Cleaning audit packs and post-cleaned Silver outputs belong in the Data Lake.
  - Preparing the next bounded contract/code patch for Fragrantica Cleaning output shape.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/source-loading.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - orca-harness/cleaning/fragrantica_lake.py
  - orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py
branch_or_commit: codex/fragrantica-cleaning @ d6fbebe7ff988dc0d4c65434401ee6e701195a79
stale_if:
  - codex/fragrantica-cleaning HEAD changes without rereading this packet's load-bearing sources.
  - Fragrantica Cleaning lake writer or Silver/Data Lake/Cleaning contracts change.
```

## Load Contract

- packet_version: handoff_v0
- mode: max
- created_at: 2026-06-29T22:55:53+08:00
- created_by_lane: Codex Fragrantica cleaning lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning`
- handoff_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning\docs\workflows\fragrantica_cleaning_audit_pack_handoff_v0.md`
- expected_branch: `codex/fragrantica-cleaning`
- expected_head: `d6fbebe7ff988dc0d4c65434401ee6e701195a79`
- expected_dirty_state_including_handoff_file: before writing, `git status --short --branch` showed only `## codex/fragrantica-cleaning...origin/codex/fragrantica-cleaning`; after writing this packet, expect this file to be untracked unless the receiver finds a later commit.
- source_loading_mode: repo-overlay-bound
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Build Orca's Fragrantica capture -> projection -> ECR -> Cleaning -> post-cleaned Silver path without blurring raw capture, projection, Cleaning audit evidence, Silver facts, or Judgment meaning.
- anchor_goal: Split Fragrantica Cleaning lake output into a raw-anchored Cleaning audit pack and separate post-cleaned Silver records that reference the audit pack.
- success_signal: A fresh lane can patch the contracts and Fragrantica writer so the full Cleaning transform ledger lives in a derived audit pack, while Silver records contain only post-cleaned consumable facts/views plus provenance pointers to raw, projection, ECR, and the audit pack.

## Open Decision / Fork

- decision: How should Fragrantica Cleaning output be represented in the Data Lake after FCR-04 exposed that `record_kind="observation"` is the wrong fit for a full `CleaningPacket`?
- options:
  - Option A: add `cleaning_ledger` to the Silver `record_kind` enum.
  - Option B: keep the full Cleaning ledger in its own derived audit pack, and emit separate post-cleaned Silver records/views that link to the audit pack.
  - Option C: create a generic `derived_record_envelope_v0` with `record_family`, then make both audit packs and Silver facts specializations.
- already constrained / off the table:
  - Do not keep a full `CleaningPacket` under `schema_version="silver_vault_record_v0"` with `record_kind="observation"`.
  - Do not put the audit pack body in `acknowledgements/`; acknowledgement records are completion/control receipts, not transformation evidence.
  - Do not make Silver records carry every transform ledger entry inline.
  - Do not let Cleaning decide sentiment, credibility, demand, independence effect, exclusion, Decision Strength, Action Ceiling, or Judgment meaning.
- trade-offs:
  - Option A is smallest enum churn but preserves the category error: `record_kind` stops meaning fact record kind.
  - Option B is the clearest lane separation and matches the owner's stated intent: audit pack for "what happened during cleaning," Silver for "what clean usable data came out."
  - Option C is architecturally strongest if multiple derived artifact families need one shared envelope, but it is broader than Fragrantica needs unless the next lane chooses to patch the Data Lake contract first.
- owner of the call: Orca owner / current user steers; next implementation lane can recommend but must not silently broaden into all Cleaning lanes.
- recommendation and why: choose Option B now, optionally implemented with the narrow part of Option C if the contract owner wants a named top-level discriminator. The audit pack should be a derived sibling under the same raw anchor; post-cleaned Silver records should point to it by lane namespace, record id, and content hash.

## Drift Guard

- invariant, non-goal, or scope boundary: The Cleaning audit pack is not a Silver fact record.
  - why it matters: Silver readers dispatching on `record_kind="observation"` expect an observation payload with subject/posture/value or text semantics; a full transform ledger is processing evidence.
  - what violating it would break: Downstream query layers could consume Cleaning process metadata as if it were a source-backed fact.
- invariant, non-goal, or scope boundary: The audit pack belongs in `derived/`, not a new lake top-level and not `acknowledgements/`.
  - why it matters: Data Lake storage already defines the Derived Result Store as the home for projection receipts, ECR/SCR records, Cleaning ledgers, and Judgment outputs keyed to raw.
  - what violating it would break: New lake roots or acknowledgement-body overloading would fork the lake grammar and hide raw-keyed replayability.
- invariant, non-goal, or scope boundary: Post-cleaned Silver records link to the audit pack but do not embed the whole ledger.
  - why it matters: Silver should stay queryable and fact/view-oriented; audit depth remains available by reference.
  - what violating it would break: Every Silver read becomes a processing-ledger read, and hash/provenance boundaries get noisy.
- invariant, non-goal, or scope boundary: This handoff does not authorize live capture, browser rendering, network probes, lake replay against external roots, commits, pushes, PRs, or broad migration of unrelated Cleaning lanes.
  - why it matters: The current turn is a handoff and structure decision, not execution.
  - what violating it would break: It would mix continuation state with unverified runtime changes.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - this packet
  - `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`
  - `docs/review-outputs/fragrantica_cleaning_adversarial_code_review_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - `orca-harness/cleaning/fragrantica_lake.py`
  - `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py`
- already loaded, weak orientation only: AGENTS instructions supplied in current task context; overlay README, decision-routing, prompt-orchestration, artifact-folders, source-loading, source-of-truth, retrieval-metadata; targeted Data Lake, Silver, Cleaning, Fragrantica writer/test, review-output, transcript-product-lake precedent, and DataLakeRoot append APIs.
- must load first before strict or actionable steps: AGENTS/current user instruction, overlay README/source-loading/source-of-truth, this packet, the three Data Lake contracts named above, the Cleaning foundation contract, current Fragrantica lake writer/test, and current git status/head.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Fragrantica is a `fragrance_native_database` source-family current-window capture, not a retail PDP and not a complete review archive.
  - decided in: `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`
  - compare target: SHA256 `36FD96984823722CAD736A492E385075503FED510828AB3945DD0065DF2EA291`; see lines 63-67 and 106-111 for active goal and lane split.
  - verify before: strict source-family, projection, ECR, or Cleaning claims.
- decision, framing, profile, or convention: Data Lake derived artifacts stay raw-keyed siblings; projection receipt, ECR/SCR, Cleaning ledger, and Judgment output are not merged into one blob.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
  - compare target: SHA256 `6EE1EA42CAF0A86D145A736C0DFBBBE3BCF3456FE0B44D2DE2192B6DE4443E37`; lines 70-94.
  - verify before: changing physical lake placement or lane namespace behavior.
- decision, framing, profile, or convention: Silver Vault `record_kind` is currently closed to `entity`, `relationship`, and `observation`.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - compare target: SHA256 `6891BC540AD9F9347F8A6569D45425657DF47BBDC8F99813B123BE73DCDF215F`; lines 130-164 and 264-352.
  - verify before: changing or relying on `record_kind`.
- decision, framing, profile, or convention: Cleaning owns transformation ledger and cleaned working view, not source acquisition, projection ownership, ECR final schema, Judgment meaning, or signal strength.
  - decided in: `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - compare target: SHA256 `B1539F5890877953A3CAFB4BB2607D6F7D36A3DE6638BF04E6A8BE07140798CB`; lines 101-116, 251-266, and 382-390.
  - verify before: Cleaning output or post-cleaned Silver design.

## Active Objective

Prepare the next Fragrantica Cleaning lane to replace the current Silver-observation-shaped `CleaningPacket` output with a dedicated raw-anchored Cleaning audit pack plus separate post-cleaned Silver records or views that link back to that audit pack.

## Exact Next Authorized Action

1. Patch the controlling Data Lake/Silver/Cleaning contract surface narrowly enough to state this invariant: Cleaning audit packs are derived processing artifacts, while post-cleaned Silver facts/views are Silver records that reference the audit pack. Prefer not to add `cleaning_ledger` to the Silver `record_kind` enum.
2. Patch `orca-harness/cleaning/fragrantica_lake.py` so the full `CleaningPacket`/transform ledger emits as a Cleaning audit pack under a dedicated derived lane such as `cleaning_fragrantica_audit`, with `schema_version` like `cleaning_audit_pack_v0` or the contract-approved equivalent.
3. Add or adapt post-cleaned Fragrantica Silver output only for the consumable cleaned material that matters downstream. Each post-cleaned record must carry a provenance pointer to the audit pack: raw anchor, projection/ECR refs as available, audit lane namespace, audit record id, audit content hash, and cleaning method/ruleset id.
4. Update `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py` so it no longer asserts `schema_version == "silver_vault_record_v0"` and `record_kind == "observation"` for the full CleaningPacket. Add assertions that the audit pack is in the audit lane and that post-cleaned Silver output links to the audit pack.
5. Run the focused Fragrantica Cleaning tests after the patch. If the contract patch is docs-only and runtime code is deferred by owner decision, state that explicitly and do not claim implementation completion.

## Recommended Structure

Audit pack storage:

```text
derived/<anchor_shard>/<raw-anchor>/cleaning_fragrantica_audit/<audit-pack-id>.json
```

Audit pack body shape, subject to contract naming:

```json
{
  "schema_version": "cleaning_audit_pack_v0",
  "record_family": "processing_audit",
  "audit_kind": "cleaning_transform_audit",
  "record_id": "<audit-pack-id>.json",
  "raw_anchor": "<packet_id>",
  "lane_namespace": "cleaning_fragrantica_audit",
  "producer_id": "orca-harness.cleaning.fragrantica",
  "producer_schema_version": "fragrantica_cleaning_audit_pack_v0",
  "content_hash": "sha256:...",
  "content_hash_basis": "canonical_json_excluding_content_hash",
  "source_family": "fragrance_native_database",
  "source_surface": "fragrantica_product_page_direct_http",
  "source_captured_at": "<raw packet capture time>",
  "produced_at": "<cleaning derivation time if available>",
  "input_refs": {
    "raw_refs": [],
    "projection_refs": [],
    "ecr_refs": []
  },
  "output_refs": [],
  "payload_kind": "FragranticaCleaningAuditPack",
  "payload": {
    "cleaning_packet": {},
    "ruleset_version": "<cleaning ruleset>",
    "transform_ledger": [],
    "warnings": [],
    "residuals": [],
    "raw_pull_triggers": []
  },
  "non_claims": [
    "not_silver_fact",
    "not_judgment",
    "not_sentiment_analysis",
    "not_demand_signal",
    "not_archive_completeness",
    "not_evidence_unit_binding"
  ]
}
```

Post-cleaned Silver record shape:

```json
{
  "schema_version": "silver_vault_record_v0",
  "record_kind": "observation",
  "payload_kind": "TextObservation",
  "raw_anchor": "<packet_id>",
  "lane_namespace": "cleaning_fragrantica_silver",
  "payload": {
    "observation": {
      "subject": {},
      "text_artifact_type": "review_body",
      "text_value": "<cleaned review text>",
      "text_hash": "sha256:...",
      "text_posture": {
        "kind": "observed",
        "reason_code": null,
        "reason_detail": null
      },
      "coverage_window": {
        "start": null,
        "end": null
      }
    }
  },
  "provenance": {
    "raw_anchor": "<packet_id>",
    "projection_record_id": "<projection id or null>",
    "ecr_receipt_id": "<ecr id or null>",
    "cleaning_audit_pack": {
      "lane_namespace": "cleaning_fragrantica_audit",
      "record_id": "<audit-pack-id>.json",
      "content_hash": "sha256:..."
    },
    "cleaning_method_id": "fragrantica_cleaning_method_v0"
  },
  "non_claims": [
    "not_judgment",
    "not_sentiment_analysis",
    "not_demand_signal",
    "not_archive_completeness"
  ]
}
```

If the next lane wants to write audit pack and post-cleaned records as one detectable set, use the existing `DataLakeRoot.append_record_set(subtree="derived", raw_anchor=<packet_id>, record_id=<shared-id>, members={...}, completion_lane=<marker-lane>)` pattern. The marker is completeness evidence only; the audit pack body remains a derived member, not an acknowledgement body.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Orca agent behavior kernel supplied in current context.
    - Load-bearing: yes
    - Compare target: user-supplied current-turn AGENTS content; reread `AGENTS.md` before source-changing continuation.
    - Last checked: 2026-06-29 current task context
    - Reuse rule: orientation only until reread from disk in the receiving lane.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint and binding rule.
    - Load-bearing: yes
    - Compare target: current file content read 2026-06-29; reread-required for strict continuation.
    - Last checked: 2026-06-29
    - Reuse rule: reread before source-changing work.
  - `.agents/workflow-overlay/source-of-truth.md`
    - Role: source hierarchy, checkpoint/handoff lifecycle, doctrine propagation.
    - Load-bearing: yes
    - Compare target: checkpoint artifacts are non-authoritative and single-consumption; reread-required.
    - Last checked: 2026-06-29
    - Reuse rule: governs this packet as a convenience handoff, not authority.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading and handoff read-pack discipline.
    - Load-bearing: yes
    - Compare target: reread-required.
    - Last checked: 2026-06-29
    - Reuse rule: receiver must re-run progressive source loading.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: accepted docs/workflows durable artifact folder.
    - Load-bearing: yes
    - Compare target: docs/workflows accepted for workflow records.
    - Last checked: 2026-06-29
    - Reuse rule: reread if moving or renaming this packet.
- User constraints:
  - Current owner direction: "post cleaning should link to the ledger in its audit file"; "deep think then handoff to new lane."
    - Role: current-turn scope and recommendation target.
    - Load-bearing: yes
    - Compare target: current user message.
    - Last checked: 2026-06-29
    - Reuse rule: follow unless explicitly redirected by current user.
- Source-read ledger:
  - `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`
    - Role: prior Fragrantica capture/projection/ECR/Cleaning handoff and source-family boundary.
    - Load-bearing: yes
    - Compare target: SHA256 `36FD96984823722CAD736A492E385075503FED510828AB3945DD0065DF2EA291`; active goal lines 63-67; lane actions lines 106-111.
    - Last checked: 2026-06-29
    - Reuse rule: reread before continuing Fragrantica lane semantics.
  - `docs/review-outputs/fragrantica_cleaning_adversarial_code_review_v0.md`
    - Role: FCR-04 source for the Silver record-kind ambiguity.
    - Load-bearing: yes
    - Compare target: SHA256 `7F555A8214C4D88981990A1B2F54FFCE8F58959363318FC80E33302AE799C59E`; FCR-04 lines 240-266.
    - Last checked: 2026-06-29
    - Reuse rule: reread before claiming review finding status or closure.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
    - Role: Data Lake slot ownership for derived result store and acknowledgement log.
    - Load-bearing: yes
    - Compare target: SHA256 `0248FA723972AEFFD04220876229F1E116F6BB9855391855ABFBC05C2F98B262`; lines 88-112.
    - Last checked: 2026-06-29
    - Reuse rule: reread before changing lake placement.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
    - Role: physical `derived/<anchor_shard>/<raw-anchor>/<lane>/<record-id>` grammar and sibling-kind rule.
    - Load-bearing: yes
    - Compare target: SHA256 `6EE1EA42CAF0A86D145A736C0DFBBBE3BCF3456FE0B44D2DE2192B6DE4443E37`; lines 70-94.
    - Last checked: 2026-06-29
    - Reuse rule: reread before path grammar or lane namespace changes.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
    - Role: Silver fact envelope, record_kind enum, observation payload expectations.
    - Load-bearing: yes
    - Compare target: SHA256 `6891BC540AD9F9347F8A6569D45425657DF47BBDC8F99813B123BE73DCDF215F`; lines 130-164 and 264-352.
    - Last checked: 2026-06-29
    - Reuse rule: reread before changing Silver fact records.
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
    - Role: Cleaning layer boundary, transform ledger, cleaned working view, Judgment handoff constraints.
    - Load-bearing: yes
    - Compare target: SHA256 `B1539F5890877953A3CAFB4BB2607D6F7D36A3DE6638BF04E6A8BE07140798CB`; lines 101-116, 251-266, 382-390.
    - Last checked: 2026-06-29
    - Reuse rule: reread before Cleaning output design.
  - `orca-harness/cleaning/fragrantica_lake.py`
    - Role: current Fragrantica Cleaning lake writer.
    - Load-bearing: yes
    - Compare target: SHA256 `0F2E442AB3AA6B0E3868D76C8F14DAE6271D14D35FCFC3D8AB52C8B017C0FA6E`; lines 77-125 currently emit `silver_vault_record_v0` and `record_kind="observation"` for a full CleaningPacket.
    - Last checked: 2026-06-29
    - Reuse rule: reread before editing.
  - `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py`
    - Role: focused test asserting current lake record shape.
    - Load-bearing: yes
    - Compare target: SHA256 `60F613232A4CEE808FC2FBF29CF7D86803D180025C61E962E22BFB240D1B1CAA`; lines 35-59 assert current Silver-observation shape.
    - Last checked: 2026-06-29
    - Reuse rule: update with code patch.
  - `orca-harness/cleaning/transcript_product_lake.py`
    - Role: nearby precedent for derived Cleaning lane record-set without Silver Vault envelope.
    - Load-bearing: no
    - Compare target: SHA256 `4F6C4AE4F3216B08B85B8B0AC8B8A65FB877B3AC7F39947079F76E887EB9DEB2`; lines 1-12 and 128-140.
    - Last checked: 2026-06-29
    - Reuse rule: precedent only; do not treat as authority.
  - `orca-harness/data_lake/root.py`
    - Role: append_record and append_record_set API shape.
    - Load-bearing: yes if using record-set implementation.
    - Compare target: SHA256 `EA78BCEF550E35A69A7A495FA76D067C1069469C821CCC5A21D1FFA84971AE6D`; lines 560-632.
    - Last checked: 2026-06-29
    - Reuse rule: reread before implementation.
  - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md`
    - Role: mechanics-map summary of Cleaning input/output boundary.
    - Load-bearing: no
    - Compare target: SHA256 `690B5BEA46FA2883359DEA08EFE22609C27A9AEB022C00DDA2838CDD8E8A7908`; lines 104-112.
    - Last checked: 2026-06-29
    - Reuse rule: orientation only; contracts above win.
- Source gaps:
  - No accepted `cleaning_audit_pack_v0` contract exists yet in the loaded sources.
  - No accepted generic `derived_record_envelope_v0` contract exists in the loaded sources.
  - The exact post-cleaned Silver row taxonomy for Fragrantica review/product facts has not been settled in this packet.
- Strict-only blockers:
  - Do not claim FCR-04 closed until the next lane patches the controlling contract and code/tests or records an explicit owner decision to defer runtime changes.
  - Do not claim live lake replay or append succeeded; no replay was run in this handoff turn.
- Not-proven boundaries:
  - Not validation, not readiness, not acceptance, not proof that post-cleaned Silver schema is final.
  - Not a commitment that all Cleaning lanes should migrate immediately.

## Current Task State

- Completed:
  - Fragrantica capture/projection/ECR/Cleaning lane got through capture, projection replay, ECR, and initial Cleaning writer work in earlier lane turns.
  - Fragrantica Cleaning review FCR-01/FCR-02/FCR-03/FCR-05/FCR-06 were patched or adjudicated in the current branch history.
  - FCR-04 remains the structural-fit issue: full `CleaningPacket` as `record_kind="observation"` is not the right long-term shape.
  - Current user direction accepts splitting audit from post-cleaned Silver output.
- Partially completed:
  - Current code can persist a Cleaning-derived record, but it uses the wrong Silver-observation wrapper for the full audit payload.
  - Existing tests assert the current wrapper shape and must be updated when the structure is patched.
- Broken or uncertain:
  - There is no settled audit-pack schema name or generic derived-envelope schema name in the loaded contracts.
  - The post-cleaned Silver row set is not yet authored.

## Workspace State

- Branch: `codex/fragrantica-cleaning`
- Head: `d6fbebe7ff988dc0d4c65434401ee6e701195a79`
- Dirty or untracked state before handoff: `git status --short --branch` showed only `## codex/fragrantica-cleaning...origin/codex/fragrantica-cleaning`.
- Dirty or untracked state after writing the handoff file: expected untracked `docs/workflows/fragrantica_cleaning_audit_pack_handoff_v0.md`.
- Target files or artifacts for next lane:
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
  - optionally `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
  - `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
  - `orca-harness/cleaning/fragrantica_lake.py`
  - `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py`
  - possibly `orca-harness/tests/unit/test_fragrantica_cleaning_projection_integration.py`
- Related worktrees or branches:
  - Main workspace `C:\Users\vmon7\Desktop\projects\orca` is on unrelated branch `codex/ig-reels-capture-spine` with many untracked artifacts. Do not edit or claim this Fragrantica lane from that root without rechecking isolation.

## Changed / Inspected / Tested Files

- `docs/workflows/fragrantica_cleaning_audit_pack_handoff_v0.md`
  - Status: newly created by this handoff turn; expected untracked until staged/committed by a later lane.
  - Role: cold handoff packet.
  - Important observations: not authority; receiver must reread controlling sources.
  - Symbols or sections: all.
- `orca-harness/cleaning/fragrantica_lake.py`
  - Status: inspected, not edited.
  - Role: current lake writer.
  - Important observations: full CleaningPacket currently emits as `silver_vault_record_v0`, `record_kind="observation"`, `payload_kind="FragranticaCleaningPacket"`.
  - Symbols or sections: `fragrantica_cleaning_record_payload`.
- `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py`
  - Status: inspected, not edited.
  - Role: focused test for derived Fragrantica Cleaning record.
  - Important observations: currently asserts the shape that should change.
  - Symbols or sections: `test_derives_fragrantica_cleaning_packet_into_derived_record`.
- `docs/review-outputs/fragrantica_cleaning_adversarial_code_review_v0.md`
  - Status: inspected, not edited.
  - Role: source of FCR-04 finding.
  - Important observations: FCR-04 was correctly left for contract-owner adjudication.
  - Symbols or sections: FCR-04.
- Data Lake and Cleaning contracts named in the source ledger
  - Status: inspected, not edited.
  - Role: governing architecture context.
  - Important observations: derived sibling placement and Silver fact record-kind closure jointly support the audit-pack split.

## Frozen Decisions

- Decision: Do not add `cleaning_ledger` to Silver `record_kind` as the preferred route.
  - Evidence: Silver contract closes `record_kind` to entity/relationship/observation fact categories; Cleaning ledger is processing evidence, not an entity/relationship/observation fact.
  - Consequence: The next patch should separate audit pack from Silver facts rather than expanding the fact enum.
- Decision: Put the Cleaning audit pack under `derived/<anchor_shard>/<raw-anchor>/<lane-namespace>/<record-id>.json`.
  - Evidence: Data Lake storage and derived-layout contracts say Cleaning ledgers are derived sibling artifacts keyed to raw.
  - Consequence: No new lake top-level and no acknowledgement-body overloading.
- Decision: Silver/post-cleaned output should link to the audit pack.
  - Evidence: Current user instruction explicitly says post-cleaning should link to the ledger in its audit file.
  - Consequence: Post-cleaned records need provenance fields for audit lane namespace, record id, content hash, and method/ruleset id.

## Mutable Questions

- Question: Should the next lane introduce a generic `derived_record_envelope_v0`, or a narrower `cleaning_audit_pack_v0` only?
  - Why still mutable: The loaded contracts do not yet define either.
  - What would resolve it: Contract owner chooses smallest complete scope. Recommendation: start with `cleaning_audit_pack_v0`; add generic `derived_record_envelope_v0` only if the patch would otherwise duplicate shared fields across derived artifact families.
- Question: What exact post-cleaned Silver records should Fragrantica emit first?
  - Why still mutable: The current writer emits only a CleaningPacket, not a fact/view set.
  - What would resolve it: Next lane chooses a minimal first output set, likely review-body text observations and source-visible normalized product/review facts that already exist in projection/cleaning handles.
- Question: Should audit pack + post-cleaned records be written through `append_record_set`?
  - Why still mutable: All-or-nothing detectable completeness is useful, but it may be more than the first patch needs.
  - What would resolve it: If the next lane emits both audit and Silver siblings in one derivation, use `append_record_set`; if it emits only the audit pack first, `append_record` is enough.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "Cleaning ledger packet can be made a Silver observation because it is derived/silver-ish."
  - Why stale or dangerous: It conflates physical derived storage with fact-record semantics.
  - Current replacement: Audit pack in derived Processing/Cleaning lane; post-cleaned Silver records separately link to the audit pack.
- Stale instruction, idea, artifact, or finding: "Put the audit bank in acknowledgements."
  - Why stale or dangerous: Acknowledgements are completion/control facts, not the transformation ledger body.
  - Current replacement: Audit body in `derived/`; optional completion marker may be written if using record-set semantics.
- Stale instruction, idea, artifact, or finding: "Silver should contain the whole ledger because it matters."
  - Why stale or dangerous: It bloats every consumer-facing fact/view with processing internals and hides the fact/audit boundary.
  - Current replacement: Silver carries compact provenance pointers to the audit pack.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed.
  - Important output before writing this packet: `## codex/fragrantica-cleaning...origin/codex/fragrantica-cleaning`
  - Re-run target so the receiver can confirm rather than trust: run the same command in `C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-cleaning`.
- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed.
  - Important output: `d6fbebe7ff988dc0d4c65434401ee6e701195a79`
  - Re-run target so the receiver can confirm rather than trust: run the same command.
- Command:
  ```powershell
  Get-FileHash <source files> -Algorithm SHA256
  ```
  Result:
  - Passed.
  - Important output: hashes recorded in `Authority And Source Ledger`.
  - Re-run target so the receiver can confirm rather than trust: hash the named source files before acting.
- Command:
  ```powershell
  rg -n "record_kind|payload_kind|schema_version|silver_vault|cleaning_packet|transform_ledger" orca-harness\cleaning\fragrantica_lake.py
  ```
  Result:
  - Passed.
  - Important output: writer currently emits `silver_vault_record_v0`, `record_kind="observation"`, `payload_kind="FragranticaCleaningPacket"`.
  - Re-run target so the receiver can confirm rather than trust: inspect `fragrantica_cleaning_record_payload`.
- Command:
  ```powershell
  rg -n "FCR-04|record_kind|observation|cleaning|ledger|Silver" docs\review-outputs\fragrantica_cleaning_adversarial_code_review_v0.md
  ```
  Result:
  - Passed.
  - Important output: FCR-04 lines 240-266 define the structural-fit issue.
  - Re-run target so the receiver can confirm rather than trust: reread FCR-04.

## Blockers And Risks

- Blocker or risk: Contract scope can sprawl into all derived artifact families.
  - Evidence: A generic `derived_record_envelope_v0` is attractive but not currently defined.
  - Likely next action: Keep the patch Fragrantica/Cleaning-audit first unless the shared contract edit is necessary.
- Blocker or risk: Post-cleaned Silver records may be underspecified.
  - Evidence: Current code persists only a full CleaningPacket.
  - Likely next action: Pick a minimal first post-cleaned output and test it; do not invent broad product ontology in this patch.
- Blocker or risk: Existing tests assert the wrong shape.
  - Evidence: `test_fragrantica_cleaning_lake_pilot.py` lines 52-55.
  - Likely next action: Update tests alongside writer.
- Blocker or risk: Rewriting historical lake records would violate append-only assumptions.
  - Evidence: Data Lake storage says re-derive rather than mutate raw or rewrite prior derived records.
  - Likely next action: If live records exist in a real lake root, append corrected siblings or write a supersession relationship/receipt later; do not mutate old derived files.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - workspace path, branch, head, and dirty state;
  - this handoff path readability;
  - all source-file hashes listed in `Authority And Source Ledger`;
  - current Fragrantica writer/test shape;
  - Data Lake derived placement and storage-slot rules;
  - Silver `record_kind` and observation payload rules;
  - Cleaning contract's transform-ledger/cleaned-working-view boundary;
  - current user instruction if a newer instruction exists.
- Compare target for each:
  - branch/head/status commands;
  - SHA256 hashes and line ranges in the source ledger;
  - direct reread of named sources when hashes drift.
- Load outcomes and what each means:
  - `REUSE`: all load-bearing facts match; continue from `Exact Next Authorized Action`.
  - `PARTIAL_REUSE`: non-load-bearing precedent or orientation drifted; reuse verified core and reread the rest.
  - `STALE_REREAD_REQUIRED`: a target source or HEAD changed; reread before acting.
  - `BLOCKED_DRIFT`: source drift conflicts with this packet's recommendation or user scope.
  - `BLOCKED_MISSING_PACKET`: this packet is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be re-derived from available sources.
- Sources that must be reread if drift is detected:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - all Data Lake/Silver/Cleaning contracts named in this packet
  - `orca-harness/cleaning/fragrantica_lake.py`
  - Fragrantica Cleaning tests

## Do Not Forget

The cleanest answer to the owner question is: the audit bank is not a new lake ocean. It is a raw-anchored derived Cleaning audit lane. Silver gets the post-cleaned facts/views that downstream consumers query, and each one points back to the audit pack for replay and accountability.
