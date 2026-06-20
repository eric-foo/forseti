```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a deletion + ontology proposal for orca/product/spines/capture/
  sub-areas: contracts/, demand_durability_indicators/, packet_schema/, and
  any files directly under capture/ or in other capture subdirs (excluding
  operating_model/, source_capture_toolbox/, source_families/ which are covered
  by sibling subagents). Read-only evidence gathering; no deletions executed.
use_when:
  - Adjudicating deletion candidates for the capture/contracts+rest area in Phase-2.
  - Reviewing ontology / doc-term cleanliness for these paths.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - Phase-2 deletions execute (register entries supersede this proposal).
  - The obligation contract, posture proposal, or corpus intake contract changes status.
```

# Phase-2 W3a Proposal — capture/contracts+rest

## Summary

Files scanned: 19 (after excluding operating_model/, source_capture_toolbox/,
source_families/ subtrees). The scan covers:

- contracts/obligation_contracts/ (3 files)
- contracts/corpus_intake/ (1 file)
- contracts/candidate_intake/ (3 files)
- contracts/source_access_boundary/ (2 files)
- demand_durability_indicators/ root (4 files) + subdirs (3 files in price_timeseries/,
  availability_restock/, search_interest/, review_velocity/ — 4 profile files)
- packet_schema/ (3 files)

Two files in this area are `_proposal_v0.md` artifacts. Both have been verified
against the parent contract to determine absorption status.

Deletion candidates: 2 high / 0 medium / 0 low.
Ontology findings: 1 (minor; non-SSOT runtime class name used as display term in
two files — informational, no wrong-type claim).

---

## A. Deletion candidates

### Candidate 1

```yaml
targets:
  - orca/product/spines/capture/core/contracts/obligation_contracts/data_capture_spine_obligation_contract_patch_proposal_v0.md

evidence:
  reverse_ref_check: >
    Inbound refs confirmed by grep across orca/product/, docs/, .agents/:
    - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md:29
      (source_basis list — self-reference as historical input)
    - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md:775,788
      (direction_change_propagation: intentionally_not_updated, reason "proposal
      remains historical candidate-language input; the controlling contract now
      consumes the accepted package")
    - docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md:13,40,168,177,200
      (owner decision consuming/citing this proposal — historical record)
    - docs/review-outputs/adversarial-artifact-reviews/* (multiple: historical
      review records citing the SHA-pinned v0 text — point-in-time records,
      not live authority)
    - docs/prompts/reviews/* (review/recheck prompt source lists — load the file
      as historical input, not as live authority)
    - docs/migration/repo_structure_*/moved_paths_index.md + moves_manifest.csv
      (migration tracking entries pointing to new canonical path)
    - docs/review-inputs/*/sources/* (frozen review-input snapshots — historical)
    All remaining refs are: (a) the parent contract's intentionally_not_updated
    entry explicitly stating the proposal is "historical candidate-language input";
    (b) frozen review-outputs/review-inputs citing the SHA-pinned pre-merge text;
    (c) migration tracking; (d) prompt source lists that load it for review.
    No ref treats it as a live operative authority or live contract source.
    The parent contract's direction_change_propagation states the package (PCP-01
    through PCP-08) is now operationalized in the obligation contract. Safe to
    remove; refs that need provenance are satisfied by the parent contract's
    own DCP receipt and the owner decision record.

  successor: >
    orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md

  semantic_delta: >
    PCP-01 through PCP-08 (cannot_assess, assessed_not_met, access_failed,
    blocked clarification, Ob.16 handoff readiness, Ob.6 fidelity split,
    checker token glossary, pass-2 checker, checker invocation comparability)
    are ALL operationalized in the obligation contract (verified: the contract
    carries all nine discharge states, the full Ob.6 fidelity text, the Ob.16
    rename, and the full checker vocabulary section). The proposal's own
    direction_change_propagation receipt (line 788) states it is "historical
    candidate-language input; the controlling contract now consumes the accepted
    package." No unique durable meaning is carried in the proposal that the parent
    contract does not now carry. Patch history and authoring rationale are
    recoverable from git; the proposal's "Rejected alias" notes and "Owner decision
    needed" sections are superseded by the accepted contract text.

  rollback: >
    git revert <executing merge sha>

confidence: high

rationale: superseded-by-parent-contract-absorbed
```

### Candidate 2

```yaml
targets:
  - orca/product/spines/capture/core/contracts/obligation_contracts/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md

evidence:
  reverse_ref_check: >
    Inbound refs confirmed by grep across orca/product/, docs/, .agents/:
    - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md:29
      (source_basis list — historical input, intentionally_not_updated at line 824
      states "proposal remains historical candidate-language input")
    - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md:824
      (direction_change_propagation: intentionally_not_updated, reason "review-outputs
      and source_quality_cw_p* closeouts are historical point-in-time records")
    - orca/product/spines/judgment/source_side_receipts/jsg01_sp6_source_visibility_derivation_architecture_routing_v0.md:20,60,108
      (loads for JSG-01 SP-6 derivation context — but JSG-01 is FROZEN per AR-01 of
      the posture proposal itself; the routing object references the proposal for
      context, not as live authority; JSG-01 frozen = no operative path through it)
    - orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md:25,310
      (hash-pinned source-read; the plan uses the proposal's schema content as a
      read-only input — the plan itself is architecture-only and does not forward
      the proposal as live authority)
    - docs/review-outputs/adversarial-artifact-reviews/* (historical review records
      SHA-pinned, point-in-time — not live authority)
    - docs/prompts/reviews/*, docs/prompts/handoffs/* (prompt source lists and
      handoff scope — historical input to now-completed implementation)
    - docs/hygiene/reddit_data_capture_lane_hygiene_inventory_v0.md:82 (hygiene
      inventory entry stating "awaiting Data Capture lane ratification" — this
      status is stale: the R2 posture-vocabulary closure has landed and is stated
      as "settled" in the obligation contract's R2 closure note, line 874-876)
    - docs/migration/* (tracking entries)
    The obligation contract's R2 closure note (lines 852-916) confirms: R2 posture-
    vocabulary closure is settled; `SOURCE_CAPTURE_MANIFEST_VERSION` bumped v0→v1;
    DCP receipt present. The proposal itself states "Status:
    PROPOSED_CANDIDATE_INPUT_PATCHED_POST_REVIEW" and "authorizes nothing." Its
    pre-ratification conditions (migration, source_quality.py collision, hash_basis
    contract) are verified closed in the R2 closure note. JSG-01 ref is FROZEN and
    does not constitute a live operative dependency.

  successor: >
    orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md

  semantic_delta: >
    The proposal's substance (closed posture vocabularies for Ob.9 cutoff, Ob.10
    archive/history, Ob.15 re-capture; hash_basis contract; Ob.10 status/value
    representation; cutoff_posture overload diagnosis; implementation impact surface
    naming) is fully absorbed:
    (a) The obligation contract's §9, §10, §15 state the closed vocabularies as
    write-time enforced (contract lines 265-456).
    (b) The R2 closure note (contract lines 852-916) records the full resolution
    including scope-out of frozen v0 packets, v1 manifest bump, and "settled" status.
    (c) The cutoff_posture overload finding and source_quality.py fallback collision
    are historical diagnosis, now resolved.
    (d) The implementation impact surface (models.py, writer.py, source_quality.py,
    packet_assembly.py, tests) is captured in the DCP receipt and in the R2 adversarial
    review at the referenced path.
    No unique durable meaning is lost. The proposal's own non-claims state it
    "authorizes nothing." Pre-ratification conditions are closed per the R2 note.

  rollback: >
    git revert <executing merge sha>

confidence: high

rationale: superseded-by-parent-contract-absorbed
```

---

### Non-candidates (why kept)

The following files were examined and are NOT deletion candidates:

- `contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
  — the live operative contract; successor to both proposals above.
- `contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md`
  — status is `CONTRACT_RATIFIED_V0_2026_06_15`; this is the standing-capture sibling
  contract, ratified and in active use. The name includes "proposal" but the file is
  the ratified contract, not a superseded proposal.
- `contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md`
  — active architecture contract (status `TARGET_RECOMMENDED`); inbound refs from
  consolidation map, corpus intake contract, and Reddit crawler architecture.
- `contracts/candidate_intake/data_capture_spine_intake_surface_consolidation_v0.md`
  — accepted consolidation capsule (status `ACCEPTED_AS_BOUNDED_PRESSURE_TEST_TARGET_V0`);
  still referenced as the pressure-test intake-surface target.
- `contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`
  — source-specific specialization of the candidate intake contract; referenced in parent.
- `contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md`
  — live operative boundary decision; controlling basis for Ob.2.
- `contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md`
  — accepted method plan; actively referenced by source_capture_toolbox/README and
  the build authorization decisions.
- `demand_durability_indicators/capture_envelope_durability_delta_spec_v0.md`
  — keystone durability delta; consumed by all four indicator profiles and Ob.17.
- `demand_durability_indicators/demand_durability_capture_pilot_v0.md`
  — pilot execution record; historical but hash-pinned evidence for Ob.17 pilot.
- `demand_durability_indicators/demand_durability_indicator_capture_deconfliction_note_v0.md`
  — reconciliation provenance for the proxy→indicator rename; not a deletion candidate.
- `demand_durability_indicators/demand_durability_indicator_standing_capture_obligation_home_decision_framing_v0.md`
  — decision framing consumed by corpus intake contract; records owner direction
  selection D1=general + D3=deferred.
- All four indicator profiles (price_timeseries, availability_restock, search_interest,
  review_velocity) — active capture profile specifications; consumed by Ob.17 and the
  corpus intake contract.
- `packet_schema/source_capture_core_payload_split_explainer_v0.md`
  — plain-language companion to the accepted payload boundary; actively open_next'd.
- `packet_schema/source_capture_packet_schema_evolution_architecture_v0.md`
  — adopted architecture routing object (status `ADOPTED_WITH_AMENDMENT_V0`); open_next'd
  by tenant_payload_attachment_boundary_v0 and the schema evolution prompt.
- `packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md`
  — owner-accepted target boundary (status `OWNER_ACCEPTED_TARGET_BOUNDARY_V0`);
  live architecture contract for payload attachment.

---

## B. Ontology / doc-term findings

### Finding 1 — `SourceCapturePacket` as display term (non-SSOT runtime alias in narrative prose)

The ontology SSOT (`ontology.yaml`) defines the canonical type as `CapturePacket`
(namespace: `packet`). The runtime binding records the alias:
  `CapturePacket.name_alias: SourceCapturePacket` (ontology.yaml:157-161).

Two files in this scan area use `SourceCapturePacket` as a display term in body prose:

- `demand_durability_indicators/demand_durability_capture_pilot_v0.md:38`
  ("two valid `SourceCapturePackets` (model-validated on write)")
- `demand_durability_indicators/capture_envelope_durability_delta_spec_v0.md:61`
  ("SourceCapturePacket (the packet), SourceCaptureSlice...")

And two packet_schema files reference it as the runtime class name (expected):
- `packet_schema/source_capture_packet_schema_evolution_architecture_v0.md:84,85,295,318`
  — correct: discussing the runtime class directly.
- `packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md:189`
  — correct: architecture discussing the runtime bundle.

Assessment: the uses in `demand_durability_capture_pilot_v0.md` and
`capture_envelope_durability_delta_spec_v0.md` refer to the runtime Python class
by its implementation name when discussing packet construction/validation. This is
a documented alias, not an unknown term — the ontology.yaml's `name_alias` entry
explicitly records `SourceCapturePacket` as the runtime storage alias for
`CapturePacket` and `not_payload_identifier: true` confirms it is not a type
discriminator. The `packet_schema/` uses correctly discuss the runtime class.

Proposed read-only fix: no source edit required. The alias is governed by
ontology.yaml's runtime_bindings. If a doc-term linting pass is tightened to
require the SSOT canonical name in prose outside the implementation context,
the two demand_durability_indicators files could be updated to say "capture packet
(`SourceCapturePacket`)" to make the alias relationship explicit — but that is a
cosmetic preference, not a correctness issue.

Severity: informational / cosmetic. The alias is fully governed; no wrong-type claim.

### Other ontology terms

No other non-SSOT, deprecated, or aliased ontology type names were found in the
scanned files. The files use domain terms (`Decision Frame`, `ECR`, `Cleaning`,
`Judgment`, `WindCaller`, `TrendVector`, `Observation`, etc.) consistently without
introducing non-SSOT variants. No distinctive new-term candidates were found that
would warrant SSOT expansion.

Conclusion: **Clean** aside from the one informational alias note above.
