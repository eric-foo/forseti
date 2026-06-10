# Daimler Advisory 001 Provenance Official Legal Core Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial artifact review report
scope: Adversarial review of the DSU-001 through DSU-003 provenance receipt for DAIMLER_ADVISORY_001 official/legal core.
use_when:
  - Deciding whether to accept, patch, or rerun the provenance receipt before proceeding to evidence-unit extraction or registry update.
  - Checking whether the provenance artifact's STEP-01/STEP-02 boundary claims are defensible.
  - Routing the registry delta and vocabulary cross-reference work.
authority_boundary: retrieval_only
input_hashes:
  review_target: AAC3ED0F17A7B3F4E2CAA66B6ECF62FD4141B7723727DC19E09834551786CB4F
open_next:
  - docs/research/daimler_advisory_001_provenance_official_legal_core_v0.md
  - docs/research/daimler_advisory_001_source_registry_v0.md
stale_if:
  - The provenance receipt is patched, re-run, or superseded.
  - The Daimler source registry is updated to reflect the provenance pass.
  - A later provenance pass captures source-body hashes and changes the DSU-001 through DSU-003 status.
```

## Commission

| Field | Value |
| --- | --- |
| Review type | Adversarial artifact review |
| Review lane | `docs/review-outputs/adversarial-artifact-reviews/` |
| Review target | `docs/research/daimler_advisory_001_provenance_official_legal_core_v0.md` |
| Target SHA256 (known) | `AAC3ED0F17A7B3F4E2CAA66B6ECF62FD4141B7723727DC19E09834551786CB4F` |
| Target SHA256 (observed) | `aac3ed0f17a7b3f4e2caa66b6ecf62fd4141b7723727dc19e09834551786cb4f` |
| Hash match | `yes` |
| Output mode | `filesystem-output` |
| Output path | `docs/review-outputs/adversarial-artifact-reviews/daimler_advisory_001_provenance_official_legal_core_adversarial_review_v0.md` |
| Scope | STEP-01 and STEP-02 boundary; DSU-001 through DSU-003 only |
| Pre-review skills | `workflow-deep-thinking` invoked; framing complete before review |
| Patch queue authorized | No — adversarial artifact review lane only |

**Central review question:** Can the artifact safely assign DSU-001, DSU-002, and DSU-003 the status `verified_pre_cutoff_for_provenance_only` without accidentally promoting them into evidence-unit-ready, packet-ready, validation-ready, buyer-proof, or judgment-quality evidence?

**Scope exclusions (held throughout):** No registry update. No participant packet. No model execution or scoring. No DSU-004 or later. No source-capture tooling, archive retrieval, media capture, schema or code changes, ECR, Cleaning, or Judgment design. No patch queue.

---

## Source-Read Ledger

### Orca Overlay Sources

| Source | Status in worktree | Role in this review |
| --- | --- | --- |
| `AGENTS.md` | Modified | Audit-trail and overlay authority; project boundary rules. |
| `.agents/workflow-overlay/README.md` | Modified | Overlay entrypoint; binding rule for overlay authority over reusable workflow guidance. |
| `.agents/workflow-overlay/review-lanes.md` | Modified | Adversarial artifact review lane definition, reviewer write permissions, finding schema requirements, `minimum_closure_condition` and `next_authorized_action` obligations. |
| `.agents/workflow-overlay/artifact-folders.md` | Modified | Accepted Orca artifact locations; `docs/research/` folder rules. |
| `.agents/workflow-overlay/validation-gates.md` | Modified | `orca_start_preflight` requirement for docs-write work; compaction-before-seal gate; retrieval-metadata gate. |
| `.agents/workflow-overlay/retrieval-metadata.md` | Unmodified (read) | Retrieval-header contract; core field rules; triggered field rules; forbidden field rules. |

**Note on dirty sources:** All overlay sources except `retrieval-metadata.md` are Modified in the worktree. Per validation-gates.md: "Modified or untracked controlling sources may support advisory work, but strict `PASS`, `ADEQUATE_NOW`, readiness, acceptance, source-of-truth, validation, or proof claims remain blocked." This review produces advisory findings and no strict formal verdicts. Modified state does not suppress findings; it blocks strict-only claims.

### Target Artifact and Supporting Sources

| Source | Status | Role |
| --- | --- | --- |
| `docs/research/daimler_advisory_001_provenance_official_legal_core_v0.md` | New (untracked) | Primary review target. |
| `docs/research/daimler_advisory_001_source_registry_v0.md` | Modified | Source registry: vocabulary definitions, DSU-001 through DSU-003 current status (`date_ambiguous`; `participant_safe_candidate`), `stale_if` conditions. |
| `docs/research/daimler_advisory_001_source_fanout_consolidation_v0.md` | Unmodified (read) | Fanout consolidation: blocker B1 (pre-cutoff provenance hygiene) and closure condition used as governing authority by the target artifact. |
| `docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md` | New (untracked) | Claim-tier classification: current state `no durable evidence`; correct `orca_start_preflight` vocabulary for comparison. |

### External URL Verification

| URL | WebFetch result | Notes |
| --- | --- | --- |
| `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-agenda-2019.pdf` | HTTP 403 Forbidden | Content not retrieved. 403 from automated fetch is common for PDF URLs that require browser-context or referer headers; does not conclusively prove URL inaccessibility. Manual browser verification required to confirm or rule out the `stale_if: Official Mercedes-Benz Group PDF URLs become inaccessible or are superseded` condition. |
| `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-hivedownagreement-2019.pdf?r=dai` | HTTP 403 Forbidden | Same limitation as above. |
| `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-hivedownreport-2019.pdf` | HTTP 403 Forbidden | Same limitation as above. |

**External verification verdict:** `not_proven`. The artifact's provenance observations (web-reader line references) cannot be independently confirmed in this review. Review of internal claim discipline proceeds as the fallback per commission. The inability to confirm URL accessibility at this moment does not in itself prove the `stale_if` condition is triggered, but it does mean the artifact's key evidentiary observations rest on prior session access that this review cannot re-verify.

---

## Deep-Thinking Framing Summary

Pre-review deep-thinking identified eight failure modes. The framing produced:

**Real failures (artifact does something materially wrong):**
- FM-4: Registry delta acknowledged, no handoff trail to close it. `open_next` doesn't route to registry update.
- FM-7: Start receipt uses custom field names, not the `orca_start_preflight` vocabulary required by validation-gates.md.
- FM-3: New status term `verified_pre_cutoff_for_provenance_only` sits between two registry terms; no cross-reference to explain the relationship.
- FM-2: DSU-002 and DSU-003 rely on an indirect chain-of-custody through DSU-001; all three get identical status treatment without distinguishing the chain asymmetry.
- FM-8: Compaction-handling field is ambiguous — unclear whether compaction actually occurred or the field is a prophylactic policy statement.

**Substantive but not fatal:**
- FM-6: Hash limitation is triply disclosed but consequence for future evidence-unit extraction is not explicitly connected.
- FM-5: Non-claims don't explicitly state `verified_pre_cutoff_for_provenance_only ≠ verified_pre_cutoff` (registry vocabulary).

**No failure:**
- FM-1: §124a chain soundness — the provenance argument is appropriately scoped and qualified for the narrow claim.

---

## Phase 1: Correctness Findings

### AR-01 — Start Receipt Does Not Use `orca_start_preflight` Vocabulary

| Field | Value |
| --- | --- |
| Finding ID | `AR-01` |
| Phase | Correctness |
| Severity (advisory label) | Major |
| Location | Target artifact, `## Start Receipt` section |
| Source authority | `validation-gates.md`: "Repo-aware prompt use, review setup, handoff creation, docs-write or overlay maintenance, source-changing work, and completion claims include or report the `orca_start_preflight` receipt from `.agents/workflow-overlay/source-loading.md`. Missing preflight evidence is a blocker for the claim or handoff." |

**Artifact evidence:** The start receipt block uses:

```yaml
local_retrieval_timestamp: 2026-06-02T15:42:28.8980748+08:00
target_path_preexisted_before_write: false
source_heavy_compaction_handling: post_compaction_reverification_performed_before_write
preflight_registry_state: manual_registry_first_pass_no_external_source_body_retrieval
preflight_claim_tier_state: no durable evidence
case_cutoff_boundary: 2019-05-21 23:59 CEST
scope_units:
  - DSU-001
  - DSU-002
  - DSU-003
```

The contemporaneous claim-tier classification decision (`daimler_advisory_001_claim_tier_classification_decision_v0.md`) correctly uses the `orca_start_preflight` vocabulary with keys `agents_read`, `overlay_read`, `precompact_rehydrated`, `source_pack`, `edit_permission`, `target_scope`, `target_path_existed_before_write`, `dirty_state_checked`, `run_control_files_edited`, `blocked_if_missing`. The provenance artifact uses entirely different keys.

**Impact:** The provenance artifact is a docs-write, which validation-gates.md explicitly requires to carry `orca_start_preflight`. A downstream reviewer or agent looking for the standard preflight evidence by name will not find it. The substantive content of the custom receipt is useful, but it doesn't satisfy the named gate. Per validation-gates.md, "Missing preflight evidence is a blocker for the claim or handoff, not proof that the artifact body is false and not authority for broad cleanup."

**Blocked state:** The artifact's completion claim is technically blocked by the missing `orca_start_preflight` gate, though the artifact body remains informative and advisory findings are not suppressed.

**Minimum closure condition:** The start receipt must be reformatted or supplemented to carry the `orca_start_preflight` vocabulary as defined in `.agents/workflow-overlay/source-loading.md`, with at minimum `agents_read`, `overlay_read`, `dirty_state_checked`, `target_scope`, `target_path_existed_before_write`, and `edit_permission` fields populated with values consistent with what the custom receipt implies.

**Next authorized action:** Owner decision: accept the artifact as advisory-only under the current incomplete gate, or authorize a patch to add the `orca_start_preflight` block. Patch execution requires a separate patch authorization turn.

**Patch queue entry:** Not authorized in this lane.

---

### AR-02 — New Vocabulary Term Not Cross-Referenced to Registry Classification

| Field | Value |
| --- | --- |
| Finding ID | `AR-02` |
| Phase | Correctness |
| Severity (advisory label) | Major |
| Location | Target artifact, `## DSU Status Records` table, `Provenance status after this pass` column; `## Registry Delta` section |
| Source authority | `daimler_advisory_001_source_registry_v0.md`: Classification Vocabulary table defines `verified_pre_cutoff` as "Durable source-level record proves public availability before the case cutoff." The provenance artifact introduces `verified_pre_cutoff_for_provenance_only` as a distinct, weaker status. |

**Artifact evidence:** The registry defines five classification terms; `verified_pre_cutoff_for_provenance_only` is none of them. The registry's note says: "Current assignment note: no source unit in this registry is promoted to `verified_pre_cutoff`, because this pass did not retrieve and receipt external source bodies." The provenance artifact's new term attempts to occupy an intermediate position between `date_ambiguous` and the registry's `verified_pre_cutoff`, but:

1. The term is not defined in the registry.
2. The provenance artifact's `Registry Delta` section explains the distinction in prose but doesn't provide a cross-reference from the registry to this receipt.
3. The non-claims do not state that `verified_pre_cutoff_for_provenance_only` does not constitute `verified_pre_cutoff` in registry vocabulary.

**Impact (two-vector):**

- **Authority creep risk:** A future agent reading only the provenance artifact sees `verified_pre_cutoff_for_provenance_only`. The substring `verified_pre_cutoff` is identical to the registry's stronger term. Without a cross-reference explaining the distinction, the agent may conflate the two and treat the units as having passed the registry's `verified_pre_cutoff` threshold.
- **Routing gap:** A future agent reading only the registry sees `date_ambiguous`; `participant_safe_candidate` for DSU-001 through DSU-003 with no pointer to this receipt. The registry's `stale_if` conditions (which include "A later source provenance pass retrieves, hashes, and dates external Daimler source bodies") are NOT triggered by this pass, because this pass did not retrieve, hash, or date source bodies. So the registry doesn't self-invalidate; it just silently disagrees with the provenance receipt.

**Minimum closure condition:** Either (a) the provenance artifact adds an explicit statement that `verified_pre_cutoff_for_provenance_only` is a standalone receipt term distinct from and weaker than the registry's `verified_pre_cutoff`, with a cross-reference to the registry; OR (b) the registry is updated to reference this receipt and assign the intermediate status visibly, with a note that `verified_pre_cutoff` remains unachieved.

**Next authorized action:** Owner decision: accept the vocabulary gap as a known risk, or authorize a patch to add cross-reference language to the provenance artifact's `Registry Delta` section and/or a pointer in the registry. Registry updates require a separate docs-write authorization.

**Patch queue entry:** Not authorized in this lane.

---

### AR-03 — Registry Delta Acknowledged But No Handoff Trail

| Field | Value |
| --- | --- |
| Finding ID | `AR-03` |
| Phase | Correctness |
| Severity (advisory label) | Major |
| Location | Target artifact, `## Registry Delta` section; retrieval header `open_next` field |
| Source authority | `artifact-folders.md`: "Track parked or temporary material through `docs/hygiene/queue.md` when it may need promotion, review, archiving, or deletion." `retrieval-metadata.md`: `open_next` — "use when one or more controlling sources should be opened after this artifact." |

**Artifact evidence:** The `Registry Delta` section says: "This pass supports a narrow registry-level delta for DSU-001 through DSU-003: their pre-cutoff public-availability ambiguity is resolved at provenance level." It then explicitly does not update the registry. The `open_next` field in the retrieval header lists:

```yaml
open_next:
  - docs/research/daimler_advisory_001_source_registry_v0.md
  - docs/research/daimler_advisory_001_source_fanout_consolidation_v0.md
  - docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md
```

The registry is listed in `open_next` for reading, but NOT flagged as needing a status update. A future agent following `open_next` will open the registry to read it, not to update it. There is no hygiene queue entry, `downstream_consumers` pointer, or handoff language explaining that the registry needs a follow-up docs-write.

**Impact:** The system is left in an acknowledged inconsistent state (registry says `date_ambiguous`; provenance receipt says `verified_pre_cutoff_for_provenance_only`) with no documented path to resolution. The stopping point is defensible under overlay rules — a provenance receipt need not update the registry — but the failure to leave a trail means the inconsistency is silent to future agents unless they read both artifacts and compare them.

**Minimum closure condition:** One of the following: (a) the provenance artifact's `open_next` or a new `downstream_consumers` triggered field explicitly flags that the source registry requires a status update pass; OR (b) a hygiene queue entry at `docs/hygiene/queue.md` records the pending registry delta; OR (c) the registry is updated in a separately authorized docs-write pass.

**Next authorized action:** Owner decision: add a hygiene queue entry or registry pointer, or defer the registry update to a named future turn. This review does not authorize registry edits.

**Patch queue entry:** Not authorized in this lane.

---

### AR-04 — DSU-002 and DSU-003 Chain-of-Custody Asymmetry Not Disclosed

| Field | Value |
| --- | --- |
| Finding ID | `AR-04` |
| Phase | Correctness |
| Severity (advisory label) | Moderate |
| Location | Target artifact, `## Provenance Basis` section; `## DSU Status Records` table |
| Source authority | Review-lanes.md: "adversarial reviewers should be maximally adversarial about material decision-relevant failure modes." Artifact evidence itself: "This does not prove that the currently opened PDF bytes are identical to the pre-cutoff copies." |

**Artifact evidence:** The provenance basis describes three distinct argument chains:

- **DSU-001** (AGM invitation/agenda): Direct chain. The PDF itself is the §124a document. The observed Federal Gazette publication date (April 3, 2019) is stated inside the AGM invitation PDF, which is also the document being claimed as pre-cutoff available. Self-attestation by the primary §124a document.
- **DSU-002** (hive-down agreement): Indirect chain. The standalone PDF at the current official URL is claimed pre-cutoff available because "the agreement also appears in Section B of the AGM invitation/agenda, whose Agenda Item 9 documents were available online from the convocation date." The provenance claim depends on: (1) DSU-001's §124a language, (2) the inference that the current standalone PDF at the Mercedes-Benz Group URL is the same document as what was referenced in AGM Item 9.
- **DSU-003** (hive-down report): Same indirect chain. Pre-cutoff availability is claimed through the AGM invitation's statement that "the Hive-down Report and other hive-down documents were available online." Identity of current standalone PDF with the §124a-referenced document is assumed, not verified.

The DSU status table assigns identical `verified_pre_cutoff_for_provenance_only` status to all three units with no disclosure of the asymmetry.

**Impact:** The indirect chain for DSU-002 and DSU-003 introduces an unverified identity assumption: the PDFs currently hosted at the official Mercedes-Benz Group URLs are the same documents as what was published under §124a coverage. If those PDFs were re-uploaded, corrected, or replaced after the AGM, the current bytes would not be identical to the pre-cutoff versions — but the §124a language would still be satisfied by whatever document was published at the time. Without source-body hashes, this identity assumption cannot be verified. The artifact correctly notes the absence of hashes but does not identify that DSU-002 and DSU-003 carry this additional assumption compared to DSU-001.

**Not a fatal failure.** The `verified_pre_cutoff_for_provenance_only` qualifier and the "no local PDF preservation, no source-body hash" remaining limits are present for all three units. But a future operator planning evidence-unit extraction for DSU-002 and DSU-003 should understand that the provenance basis is one step weaker than for DSU-001.

**Minimum closure condition:** The artifact's `## Provenance Basis` or `## DSU Status Records` section explicitly notes that DSU-002 and DSU-003 rely on an indirect chain through DSU-001's §124a coverage, and that the identity of the current standalone PDFs with the §124a-referenced documents is an unverified assumption until source-body hashes are captured.

**Next authorized action:** Owner decision: accept the current treatment as sufficient given the provenance-only scope, or authorize a patch to add the chain-asymmetry disclosure. This finding does not block advisory use of the provenance receipt.

**Patch queue entry:** Not authorized in this lane.

---

### AR-05 — Compaction-Handling Claim Is Ambiguous

| Field | Value |
| --- | --- |
| Finding ID | `AR-05` |
| Phase | Correctness |
| Severity (advisory label) | Moderate |
| Location | Target artifact, `## Start Receipt`, field `source_heavy_compaction_handling: post_compaction_reverification_performed_before_write` |
| Source authority | `validation-gates.md`: "Compaction-before-seal gate: if context compacts before the current source-heavy unit artifact is written and hashed, the run must stop as `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL`; any partial outputs from that unit are contaminated scratch until archived or cleanly rerun." |

**Artifact evidence:** The field value `post_compaction_reverification_performed_before_write` is ambiguous between two readings:

- **Reading A (event record):** Compaction occurred during the run; reverification was performed after compaction and before writing the artifact.
- **Reading B (policy statement):** The prescribed handling for the compaction scenario is reverification before write; whether compaction actually occurred is not stated.

If Reading A is correct: the artifact is a provenance receipt whose entire evidentiary value rests on web-reader line references from three PDFs (DSU-001 L714-L720, L728-L729, L358-L363; DSU-002 L99-L114; DSU-003 L7816-L7840). If compaction erased those observations from context, the question is whether the reverification re-opened all three PDFs and re-confirmed all six sets of line references, or whether the observations were reconstructed from precompact scratch or memory. The artifact does not document the scope of what was reverified.

If Reading B is correct: no compaction occurred, and the field is prophylactic. In that case the correct value would be `no_compaction_before_write` or similar, and the current value creates false ambiguity.

**Impact:** A downstream reviewer cannot distinguish between these readings without external evidence. For a provenance receipt, the specific observations (Federal Gazette date, Section 124a availability language, signature dates) are the primary evidence. Uncertainty about whether those observations survived a compaction event is material to the receipt's reliability.

**Minimum closure condition:** The compaction-handling field must unambiguously state either (a) no compaction occurred during the run that produced this artifact (`no_compaction_before_write` or equivalent), or (b) compaction occurred and the reverification scope is documented — specifically, whether the web-reader line references for all three PDFs were re-confirmed post-compaction.

**Next authorized action:** Owner decision: clarify the compaction-handling record in a patch, or accept the current ambiguity with an explanatory note. If compaction did not occur, the simplest fix is a field value change. This review does not authorize edits.

**Patch queue entry:** Not authorized in this lane.

---

## Phase 2: Friction Findings

### AR-06 — Hash Limitation Consequence Not Connected to Future Extraction Risk

| Field | Value |
| --- | --- |
| Finding ID | `AR-06` |
| Phase | Friction |
| Severity (advisory label) | Minor |
| Location | Target artifact, `## Source Body And Hash Limitation` section |
| Source authority | Advisory: the limitation is correctly disclosed; this finding addresses presentation completeness for future operator planning. |

**Artifact evidence:** The limitation section correctly states: "This does not prove that the currently opened PDF bytes are identical to the pre-cutoff copies, because no source bodies were locally preserved and no source-body hashes were captured in this pass." It also provides a tooling planning note.

**Gap:** The section does not explicitly state the consequence for a future evidence-unit extraction pass: any evidence unit extracted from DSU-002 or DSU-003 in a future pass must independently verify that the passage comes from a document version that predates the cutoff — not just that a document with that name was available pre-cutoff. Without content identity, pre-cutoff availability of the document title does not guarantee pre-cutoff provenance of a specific extracted passage. This distinction is most acute for DSU-002 and DSU-003 (indirect chain; see AR-04) but applies to all three.

**Impact:** A future source-capture or evidence-unit extraction operator reading the tooling planning note may plan for URL/archive capture and hashing without understanding that the extraction pass itself must address document-version identity as a separate concern.

**Minimum closure condition:** The limitation section adds a note that future evidence-unit extraction must independently verify the document version for each extracted passage, not only re-capture the URL and hash the current bytes.

**Next authorized action:** Owner decision: add the note as advisory prose in a patch, or accept the current disclosure as sufficient. This finding does not block use of the provenance receipt.

**Patch queue entry:** Not authorized in this lane.

---

### AR-07 — Non-Claims Missing Vocabulary Equivalence Negation

| Field | Value |
| --- | --- |
| Finding ID | `AR-07` |
| Phase | Friction |
| Severity (advisory label) | Minor |
| Location | Target artifact, `## Non-Claims` section |
| Source authority | Advisory: non-claims are otherwise comprehensive; this is a precision gap relative to AR-02's vocabulary concern. |

**Artifact evidence:** The non-claims list seventeen explicit negations covering: durable raw answer, product-learning evidence, buyer proof, commercial readiness, validation readiness, blind-use readiness, packet readiness, evidence-unit extraction, PDF preservation, source-body hashes, fixture admission, model run, scoring, reveal-only use, ECR/Cleaning/Judgment/source-access/archive/media/schema/code, Judgment Spine validation, and claim-tier state change.

**Gap:** The non-claims do not explicitly state that `verified_pre_cutoff_for_provenance_only` as used in this artifact does not constitute `verified_pre_cutoff` in the Daimler source registry's classification vocabulary. This is the mirror of the vocabulary cross-reference gap in AR-02, expressed from the non-claims side. A future agent checking the non-claims for guidance on what this status does not mean will not find explicit language preventing registry-vocabulary conflation.

**Proposed addition (advisory only):** `verified_pre_cutoff_for_provenance_only` as used in this artifact does not constitute the `verified_pre_cutoff` status defined in the source registry's classification vocabulary.

**Minimum closure condition:** A non-claim entry is added stating that the provenance receipt's `verified_pre_cutoff_for_provenance_only` status does not satisfy the source registry's `verified_pre_cutoff` classification.

**Next authorized action:** Owner decision: add the non-claim in a patch, or accept the current list as sufficient given AR-02 addresses the same gap from the vocabulary side. This finding is advisory only.

**Patch queue entry:** Not authorized in this lane.

---

### AR-08 — Retrieval Header Missing `input_hashes` for Orca Input Artifacts

| Field | Value |
| --- | --- |
| Finding ID | `AR-08` |
| Phase | Friction |
| Severity (advisory label) | Minor |
| Location | Target artifact, retrieval header |
| Source authority | `retrieval-metadata.md`: "`input_hashes`: use when exact provenance is safety-critical, especially for review reports, rerun prompts, patch prompts, proof/replay artifacts, cutoff-sensitive artifacts, cross-repo inputs, or dirty-state-dependent claims." |

**Artifact evidence:** The retrieval header does not carry an `input_hashes` field. The provenance artifact is explicitly cutoff-sensitive (the entire claim turns on whether documents were available before `2019-05-21 23:59 CEST`). It consumed three Orca input artifacts as its governing source basis: the source registry, the source fanout consolidation, and the claim-tier classification decision.

The retrieval-metadata contract notes `input_hashes` is a triggered field — it should be added "when exact provenance is safety-critical." This artifact's input artifacts carry their own SHA256 hashes (the claim-tier classification decision records hashes for its source basis). Adding `input_hashes` for the three Orca inputs would allow a future reviewer to confirm the governing source basis has not changed since the provenance pass was written.

**Limitation note:** The PDFs themselves cannot be hashed here because they were not downloaded. `input_hashes` in the header is appropriate only for the Orca artifacts consumed, not the external PDFs.

**Impact:** Minor. A future reviewer will need to independently confirm that the registry, fanout consolidation, and claim-tier decision have not changed in ways that would alter the provenance receipt's conclusions. The `stale_if` conditions provide some coverage, but explicit hashes would remove ambiguity.

**Minimum closure condition:** The retrieval header adds `input_hashes` entries for the three Orca input artifacts consumed (source registry, fanout consolidation, claim-tier classification decision) with their SHA256 values at the time of the provenance pass.

**Next authorized action:** Owner decision: add `input_hashes` in a patch, or accept the current header as sufficient given the `stale_if` conditions provide partial coverage. This is optional hardening, not a required blocker.

**Patch queue entry:** Not authorized in this lane.

---

## Summary Table

| Finding ID | Phase | Severity | Topic | Minimum Closure Condition |
| --- | --- | --- | --- | --- |
| AR-01 | Correctness | Major | Start receipt lacks `orca_start_preflight` vocabulary | Start receipt reformatted or supplemented to use standard `orca_start_preflight` keys |
| AR-02 | Correctness | Major | `verified_pre_cutoff_for_provenance_only` not cross-referenced to registry vocabulary | Explicit statement or cross-reference distinguishing new term from registry's `verified_pre_cutoff` |
| AR-03 | Correctness | Major | Registry delta acknowledged without handoff trail | Hygiene queue entry, `downstream_consumers` pointer, or `open_next` update flagging pending registry update |
| AR-04 | Correctness | Moderate | DSU-002/DSU-003 indirect chain undisclosed | Provenance basis or status table notes indirect chain for DSU-002/DSU-003 vs. direct chain for DSU-001 |
| AR-05 | Correctness | Moderate | Compaction-handling field ambiguous | Field explicitly states whether compaction occurred; if yes, reverification scope documented |
| AR-06 | Friction | Minor | Hash limitation not connected to extraction-pass implication | Limitation section notes that future evidence-unit extraction must address document-version identity independently |
| AR-07 | Friction | Minor | Non-claims missing vocabulary equivalence negation | Non-claim added: `verified_pre_cutoff_for_provenance_only` ≠ `verified_pre_cutoff` (registry) |
| AR-08 | Friction | Minor | Retrieval header missing `input_hashes` for Orca inputs | Optional: `input_hashes` added for three Orca input artifacts |

---

## External Source Verification Summary

All three official Mercedes-Benz Group PDF URLs returned HTTP 403 Forbidden under automated WebFetch. External source content was not retrieved. Conclusions:

1. External source verification for this review is `not_proven`.
2. The artifact's web-reader line references cannot be independently confirmed in this review.
3. HTTP 403 from automated fetch does not conclusively prove browser inaccessibility; servers commonly block automated PDF fetching. The `stale_if` condition "Official Mercedes-Benz Group PDF URLs become inaccessible or are superseded" cannot be confirmed as triggered from this review alone.
4. Manual browser verification of all three URLs is recommended before treating the provenance receipt as definitively up-to-date.

---

## What This Review Did NOT Find

The following were tested and found sound under the provenance-only scope:

- **FM-1 (§124a chain soundness):** The provenance argument — Section 124a AktG online availability from convocation date, Federal Gazette publication April 3, 2019 observed, April 3 < cutoff May 21 — is correctly scoped and explicitly qualified as provenance-level only. The chain is sound for the stated purpose.
- **Non-claim completeness (downstream conversion):** The non-claims correctly and comprehensively block evidence-unit conversion, participant packet use, validation, scoring, fixture admission, ECR/Cleaning/Judgment, buyer proof, commercial readiness, and claim-tier state change. This aspect is not a failure.
- **Folder placement:** `docs/research/` is the correct folder under `artifact-folders.md` for a source provenance receipt.
- **Scope enforcement:** The artifact correctly stopped at STEP-02, did not attempt DSU-004 or later, did not authorize source-capture tooling, did not perform extraction, did not update the claim-tier state.

---

## Review-Use Boundary

These findings are decision input for the authorized decision-maker (Chief Architect). They are not:

- mandatory remediation;
- validation, approval, or readiness proof;
- executor-ready patch authority;
- acceptance of the provenance receipt as correct or adequate;
- rejection of the provenance receipt.

Only a separately authorized patch, acceptance, or docs-write lane can make any finding actionable as executor work. The reviewer makes no formal verdict on whether the artifact is acceptable, blocked, or ready for downstream use. The three major findings (AR-01, AR-02, AR-03) represent the highest-priority decision input; the two moderate findings (AR-04, AR-05) are next; the three minor/friction findings (AR-06, AR-07, AR-08) are optional hardening.

---

## Non-Claims

This review does not claim:

- The provenance artifact is approved, validated, ready, or adequate for downstream use.
- The provenance artifact must be patched or rerun before any use.
- The DSU-001 through DSU-003 provenance claim is false.
- Any finding constitutes a formal artifact-role verdict, blocked/ready determination, or lifecycle completion claim.
- External URL accessibility is confirmed or denied.
- The registry update is authorized, scoped, or ready for execution.
- This review is a patch queue, an execution handoff, or a completion claim.
- AR-08 (missing `input_hashes`) is a required blocker; it is optional hardening only.
- Review-lane authority to edit the target artifact, the registry, or any overlay file.
