# Daimler Advisory 001 Provenance Official Legal Core v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Source-provenance receipts for DAIMLER_ADVISORY_001 official/legal core DSU-001 through DSU-003.
use_when:
  - Checking DSU-001 through DSU-003 pre-cutoff public-availability status.
  - Deciding whether the official/legal core may proceed to evidence-unit extraction.
  - Preserving non-claims after the first official/legal provenance pass.
authority_boundary: retrieval_only
open_next:
  - docs/research/daimler_advisory_001_source_registry_v0.md
  - docs/research/daimler_advisory_001_source_fanout_consolidation_v0.md
  - docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md
input_hashes:
  docs/research/daimler_advisory_001_source_registry_v0.md: sha256:08629ED76F5DC96F8DF4391122EE7DFA640464D3D9860D673EE2C481F12085D1
  docs/research/daimler_advisory_001_source_fanout_consolidation_v0.md: sha256:0A9EE8700E5A7E9C2AA7F5D2BEFE71768A2E80EB13BED5DCC3B3C44E29A3FD38
  docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md: sha256:36A78F2523D76EC4F74C67F73F89F66E4B6223A3AA183D85B03C2EF310EED336
downstream_consumers:
  - Future Daimler source-registry reconciliation pass.
  - Future DSU-001 through DSU-003 source-body capture or evidence-unit extraction pass.
stale_if:
  - Official Mercedes-Benz Group PDF URLs become inaccessible or are superseded.
  - Source bodies are later captured locally and hashed.
  - The Daimler source registry changes DSU-001 through DSU-003 status.
  - The Daimler claim-tier classification changes from no durable evidence.
  - A participant packet supersedes this provenance-only pass.
```

Status: `DAIMLER_ADVISORY_001_PROVENANCE_OFFICIAL_LEGAL_CORE_V0`.

Scope boundary: this artifact implements only STEP-01 and STEP-02 of the
accepted provenance-pass route. It covers DSU-001, DSU-002, and DSU-003. It does
not attempt DSU-004 or later registry units.

This artifact records current source provenance. It does not retrieve local PDF
bodies, preserve archives, compute source-body hashes, extract evidence units,
build participant packet text, run a model, score an answer, validate Daimler,
or create buyer-facing proof.

## Start Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: DAIMLER_ADVISORY_001 DSU-001 through DSU-003 provenance-only receipt.
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/research/daimler_advisory_001_source_registry_v0.md
    - docs/research/daimler_advisory_001_source_fanout_consolidation_v0.md
    - docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md
initial_provenance_write_receipt:
  local_retrieval_timestamp: 2026-06-02T15:42:28.8980748+08:00
  target_path_preexisted_before_write: false
  compaction_before_artifact_write: yes
  partial_precompact_source_outputs_used_as_authority: no
  post_compaction_reverification_scope:
    - official Mercedes-Benz Group PDF URLs for DSU-001 through DSU-003 re-opened
    - AGM invitation/agenda line references L358-L363, L714-L720, and L728-L729 reverified
    - hive-down agreement line references L99-L114 reverified
    - hive-down report line references L7816-L7840 reverified
patch_receipt_for_adversarial_review_findings:
  local_patch_timestamp: 2026-06-02T16:02:42.0415932+08:00
  patch_scope:
    - AR-01 through AR-08 closure language in this artifact
    - no registry update
    - no source-body capture
    - no evidence-unit extraction
local_retrieval_timestamp: 2026-06-02T15:42:28.8980748+08:00
target_path_preexisted_before_write: false
preflight_registry_state: manual_registry_first_pass_no_external_source_body_retrieval
preflight_claim_tier_state: no durable evidence
case_cutoff_boundary: 2019-05-21 23:59 CEST
scope_units:
  - DSU-001
  - DSU-002
  - DSU-003
```

The governing fanout consolidation says the official/legal core needs durable
evidence that the AGM invitation, hive-down agreement, and hive-down report were
publicly available before `2019-05-21 23:59 CEST`. The source registry currently
keeps DSU-001 through DSU-003 as `date_ambiguous`;
`participant_safe_candidate` and says no unit has been promoted to
`verified_pre_cutoff` because external source bodies were not previously
retrieved and receipted.

## Provenance Basis

Observed official/current source URLs:

| DSU | Current official source opened | Source-body preservation status |
| --- | --- | --- |
| `DSU-001` | `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-agenda-2019.pdf` | `not_locally_preserved`; `source_pdf_hash_not_captured` |
| `DSU-002` | `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-hivedownagreement-2019.pdf?r=dai` | `not_locally_preserved`; `source_pdf_hash_not_captured` |
| `DSU-003` | `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-hivedownreport-2019.pdf` | `not_locally_preserved`; `source_pdf_hash_not_captured` |

Observed public-availability basis:

- The AGM invitation/agenda PDF was opened from the current official
  Mercedes-Benz Group URL. The retrieved PDF identifies the Annual Meeting date
  as May 22, 2019 and includes Agenda Item 9 for approval of the hive-down and
  acquisition agreement.
- The AGM invitation/agenda states that Section 124a Annual Meeting information
  and documentation, including the convocation, Annual Report 2018, and documents
  for Agenda Item 9, were available online from the date of convocation at the
  Daimler annual meeting page. Observed web-reader lines: agenda PDF L714-L720.
- The AGM invitation/agenda states that the convocation was published in the
  German Federal Gazette on April 3, 2019. Observed web-reader lines: agenda PDF
  L728-L729.
- The AGM invitation/agenda states that the Hive-down Report and other documents
  relating to the hive-down were available online at the Daimler annual meeting
  page. Observed web-reader lines: agenda PDF L358-L363.
- The current official standalone hive-down agreement PDF identifies the
  notarial deed and annex as dated March 25, 2019 and names Daimler AG,
  Mercedes-Benz AG, and Daimler Truck AG as parties. Observed web-reader lines:
  hive-down agreement PDF L99-L114.
- The current official standalone hive-down report PDF records Board of
  Management signature dates of March 26, 2019 for Daimler AG, Mercedes-Benz AG,
  and Daimler Truck AG. Observed web-reader lines: hive-down report PDF
  L7816-L7840.

Because April 3, 2019 is before `2019-05-21 23:59 CEST`, the observed
convocation and Section 124a publication language resolves the pre-cutoff
public-availability question for the official/legal core at provenance level.
This does not prove that the currently opened PDF bytes are identical to the
  pre-cutoff copies, because no source bodies were locally preserved and no
  source-body hashes were captured in this pass.

Chain-strength distinction:

| DSU | Chain type | Meaning for this receipt |
| --- | --- | --- |
| `DSU-001` | `direct_section_124a_anchor` | The same current official agenda PDF carries the Section 124a availability language and Federal Gazette date used for the provenance claim. |
| `DSU-002` | `indirect_agenda_item_9_chain` | The current official standalone agreement PDF is tied to the pre-cutoff chain through Agenda Item 9 and Section B of the AGM invitation/agenda; this pass did not prove standalone PDF byte identity against a pre-cutoff preserved copy. |
| `DSU-003` | `indirect_agenda_item_9_chain` | The current official standalone hive-down report PDF is tied to the pre-cutoff chain through the AGM invitation/agenda's statement that the Hive-down Report and related documents were available online; this pass did not prove standalone PDF byte identity against a pre-cutoff preserved copy. |

## DSU Status Records

| DSU | Source unit | Provenance status after this pass | Basis | Remaining limits |
| --- | --- | --- | --- | --- |
| `DSU-001` | Daimler Annual Meeting 2019 invitation / agenda | `verified_pre_cutoff_for_provenance_only` | Current official agenda PDF opened; convocation publication date observed as April 3, 2019; Section 124a availability language observed for annual-meeting documents from the convocation date. | No local PDF preservation, no source-body hash, no archive URL, no evidence-unit extraction, no participant packet text. |
| `DSU-002` | Daimler Annual Meeting 2019 hive-down and acquisition agreement | `verified_pre_cutoff_for_provenance_only` | Current official standalone agreement PDF opened; indirect chain through Section B / Agenda Item 9 of the AGM invitation/agenda, whose Agenda Item 9 documents were available online from the convocation date. | No local PDF preservation, no source-body hash, no archive URL, no standalone PDF byte-identity proof against a pre-cutoff copy, no annex-level extraction, no participant packet text. |
| `DSU-003` | Daimler AM 2019 hive-down report / Ausgliederungsbericht | `verified_pre_cutoff_for_provenance_only` | Current official standalone hive-down report PDF opened; indirect chain through the AGM invitation/agenda's statement that the Hive-down Report and other hive-down documents were available online, plus Section 124a publication language for Agenda Item 9 documents from convocation. | No local PDF preservation, no source-body hash, no archive URL, no standalone PDF byte-identity proof against a pre-cutoff copy, no claim-level evidence-unit extraction, no participant packet text. |

## Registry Delta

This pass supports a narrow registry-level delta for DSU-001 through DSU-003:
their pre-cutoff public-availability ambiguity is resolved at provenance level.

The correct vocabulary for this pass is
`verified_pre_cutoff_for_provenance_only`, not packet-ready, evidence-unit-ready,
validated, scored, buyer-proof, or judgment-quality evidence.

`verified_pre_cutoff_for_provenance_only` is a local receipt status in this
artifact. It is strictly weaker than, and does not constitute, the source
registry's `verified_pre_cutoff` classification. The registry may continue to
show DSU-001 through DSU-003 as `date_ambiguous` until a separately authorized
registry reconciliation pass decides whether and how to incorporate this
provenance receipt.

Registry handoff trail: future work that opens the source registry should also
open this receipt before deciding whether DSU-001 through DSU-003 remain
`date_ambiguous`, gain a registry pointer to this provenance-only receipt, or
are promoted under the registry's own vocabulary. This artifact does not
authorize the registry update.

Participant visibility remains conditional. `participant_safe_candidate` is still
only a candidate label until source passages are extracted, checked for leakage,
and assembled into a participant-safe packet under a separate accepted route.

## Source Body And Hash Limitation

This pass did not download, preserve, archive, or hash the underlying source PDF
bodies. It opened current official Mercedes-Benz Group URLs and recorded observed
line references from the web reader.

The artifact hash for this file, once computed, hashes only this provenance
receipt. It does not hash the underlying DSU-001, DSU-002, or DSU-003 PDFs.

If a later source-capture/tooling phase is authorized, it should capture source
bodies, compute source hashes, preserve archive URLs where available, and record
any mismatch between current official URLs and archived or pre-cutoff copies.
This artifact does not authorize that tooling work.

If a later evidence-unit extraction phase is authorized, that phase must
independently address document-version identity for the passages it extracts.
Pre-cutoff availability of a document title or document family is not by itself
proof that a specific passage in the current standalone PDF bytes existed in the
pre-cutoff version.

## Non-Claims

This artifact does not claim:

- Daimler has a durable raw answer.
- Daimler has completed product-learning evidence.
- Daimler is buyer proof.
- Daimler is commercially ready.
- Daimler is validation-ready.
- Daimler is blind-use-ready.
- Daimler is packet-ready.
- DSU-001 through DSU-003 have been extracted into evidence units.
- DSU-001 through DSU-003 source bodies have been locally preserved.
- DSU-001 through DSU-003 source-body hashes have been captured.
- Any fixture has been admitted.
- Any model run has been performed.
- Any score has been produced.
- Any reveal-only material has been used.
- Any ECR, Cleaning, Judgment, source-access, archive, media-capture, schema, or
  code work has been authorized.
- Judgment Spine has been validated.
- The Daimler claim-tier state has changed from `no durable evidence`.
- `verified_pre_cutoff_for_provenance_only` constitutes the source registry's
  `verified_pre_cutoff` classification.
- A registry update is authorized or complete.

## Stop Receipt

```yaml
route_step_stop: STEP-02
completed_scope:
  - preflight_registry_and_claim_tier_state
  - official_legal_core_provenance_for_DSU_001_to_DSU_003
not_attempted:
  - DSU-004_or_later_provenance
  - source_body_capture
  - source_body_hashing
  - archive_retrieval
  - evidence_unit_extraction
  - participant_packet_rebuild
  - model_run
  - scoring
  - validation_or_readiness_claim
```
