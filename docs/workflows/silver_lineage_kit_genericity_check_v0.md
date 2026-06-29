# Silver Lineage Kit Genericity Check v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow design check
scope: >
  Checks whether the proposed Silver lineage kit is generic enough for current
  Orca capture, projection, transcript, ECR/SCR, and Cleaning record shapes
  before implementation.
use_when:
  - Scoping or reviewing the Silver lineage helper/kit.
  - Deciding whether a source-specific provenance field should instead use the generic Silver lineage grammar.
  - Auditing whether a derived record may claim source-backed completeness.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca-harness/data_lake/root.py
branch_or_commit: >
  Authored on codex/silver-lineage-kit from origin/main e5dfd03d. Source scan
  also included the active IG deep-capture implementation worktree
  codex/ig-deep-capture-e2e at 5cda34b1 for the pending one-render deep-capture
  record shape.
stale_if:
  - Silver Vault common header fields, raw_refs, derived_refs, or DataLakeRoot derived path grammar change.
  - Projection raw_ref/raw_anchor models, CleaningRawAnchor, or transcript_asr record semantics change.
  - IG one-render deep capture gains a raw packet, Attachment Record, or other persisted raw source object.
```

## Purpose

This artifact answers one question before implementation: is the proposed Silver
lineage kit broad enough for Orca's current sources of information?

Answer: yes, if the kit is a generic source-reference grammar plus explicit
lineage limitations. No, if it is implemented as an IG/transcript-specific
`source_context` field, or if it quietly assumes all media bytes are persisted.

This is not implementation authority, validation, readiness, a migration plan,
or a data-lake schema change. It is a source-backed design check to prevent the
next patch from solving only the IG transcript case.

## Routing Boundary

Smallest complete outcome: record the genericity check and the required v0 kit
shape before writing code.

Regime: complicated.

Why: the current system already has multiple local lineage grammars; the work is
to consolidate their common reference shape without flattening source-specific
evidence.

Allowed next move after this artifact: implement the smallest additive helper
and representative tests.

Disallowed next move: build a shared acquisition/core refactor or claim full
source-backed completeness for rawless deep-capture records.

## Genericity Verdict

The generic kit must model references, not media.

It needs to answer:

1. Which raw packet, slice, file, hash, and intra-file anchor did this Silver
   fact come from?
2. Which prior derived record did this Silver fact consume, correct, supersede,
   or select?
3. Which source object is being observed without turning it into global identity?
4. What lineage is intentionally absent, transient, or limited?

That covers the current lanes because the real commonality is not "audio",
"caption", "comment", "review", "product", or "creator". The commonality is a
source-visible fact anchored to either preserved raw material or an exact
derived record.

## Coverage Scan

| Lane/source shape | Observed current shape | Kit fit |
| --- | --- | --- |
| DataLakeRoot append records | Derived records write under `derived/<anchor_shard>/<raw_anchor>/<lane>/<record_id>`; record sets write member lanes plus a completion marker. | Fits by addressing every source ref as `raw_anchor + lane + record_id` or raw packet/file refs. |
| ECR derived records | `derive_ecr_into_lake` reads a committed raw packet and writes sibling `ecr_*` records plus `ecr_set`. | Fits raw packet refs; record-set relations need member-lane addressing. |
| Signal Content | Reads raw packet bodies, writes `signal_content`, optionally carries ECR posture refs. | Fits raw packet refs plus optional derived refs. |
| Reddit projection | Rows carry `raw_ref(packet_id, slice_id)` and `raw_anchor(file_id, relative_packet_path, sha256, hash_basis, json_pointer)`. | Fits directly. |
| Retail/PDP projection | Rows and bindings carry packet/slice/file/hash anchors with `file`, `html_selector`, `script_index`, `text_pattern`, and `json_pointer` anchors. | Fits directly; anchor kind must stay open enough for DOM/text/embedded JSON. |
| Fragrantica projection | Rows carry packet/slice/file/hash anchors with file, selector, and text-pattern anchors, plus source object fields such as site id and product name. | Fits directly; source object identity must remain source-local. |
| IG legacy and reels-grid projection | Rows carry packet/slice/file/hash anchors, JSON pointers, source-surface candidates, and selection policy data. | Fits directly; source-surface disagreement belongs in payload, lineage points to raw evidence. |
| YouTube caption packets | Caption json3 is raw source material in a SourceCapturePacket; flat text is non-authoritative. | Fits raw packet/file refs. |
| YouTube and IG standalone ASR | Raw audio is staged as a SourceCapturePacket; generated transcript lives as a `transcript_asr` derived record with provenance back to packet/file/hash. | Fits raw refs for the ASR record and derived refs for downstream consumers. |
| Cleaning projection handles | `CleaningRawAnchor` already supports preserved-file anchors and `derived_record` anchors; projection refs remain separate. | Strong fit; this is existing proof that file refs and derived-record refs both need first-class support. |
| Product mentions from transcripts | Current product-mention silver records key by transcript anchor/source but need exact transcript derived-record identity to avoid same-shortcode ambiguity. | Fits, but this is a current gap the helper should close first. |
| IG one-render deep capture | Current pending shape writes comments and transcript members keyed by shortcode; media URL is transient and redacted; no raw media bytes or raw render packet are persisted. | Fits only with explicit `lineage_limitations`. Full source-backed completeness would require a raw packet or Attachment Record later. |

## Required v0 Grammar

The kit should be additive. It should not force every existing producer into a
new universal wrapper before value is proven.

Recommended v0 block:

```json
{
  "silver_lineage": {
    "schema_version": "silver_lineage_v0",
    "producer_id": "producer-or-builder",
    "producer_schema_version": "producer_schema_v0",
    "source_surface": "source-visible-surface-token",
    "source_object": {
      "namespace": "instagram|youtube|reddit|retail|fragrantica|...",
      "object_type": "platform_content|platform_account|thread|comment|pdp|review|transcript|...",
      "native_id": "source-local-id",
      "source_url": null
    },
    "observed_at": null,
    "captured_at": null,
    "raw_refs": [],
    "derived_refs": [],
    "lineage_limitations": []
  }
}
```

`source_object` is source-local identity only. It must not imply a global person,
creator, product, brand, or cross-platform entity.

Raw refs should be able to express:

```json
{
  "ref_type": "raw_packet",
  "packet_id": "packet-id",
  "slice_id": "slice-id-or-null",
  "file_id": "file-id-or-null",
  "sha256": "hash-or-null",
  "hash_basis": "raw_stored_bytes|...",
  "anchor": {
    "kind": "file|json_pointer|html_selector|script_index|text_pattern|time_span|byte_range|source_locator",
    "value": "anchor-value-or-null"
  },
  "relation": "observed_from|selected_from|derived_from|consumed"
}
```

Derived refs should be able to express:

```json
{
  "ref_type": "derived_record",
  "raw_anchor": "raw-anchor-or-shortcode",
  "lane": "transcript_asr|silver__capture__reel_transcript|...",
  "record_id": "record-id.json",
  "sha256": "derived-record-bytes-hash-or-null",
  "hash_basis": "derived_record_bytes|derived_record_marker_sha256|null",
  "relation": "derived_from|consumed|selected|corrects|supersedes|conflicts_with",
  "record_set_completion_lane": "optional-completion-marker-lane"
}
```

For a record-set member, `lane + record_id` identifies the member. The
completion marker remains the detectable-completeness guard; it does not replace
the member's address.

`lineage_limitations` is mandatory when a record has no resolvable raw ref and
no exact derived ref. A limitation is not a defect by itself, but it blocks a
full source-backed completeness claim.

## Agent Use Contract

Agents should not hand-build ad hoc provenance for each lane once the helper
exists. They should select the source path and let the helper construct the
lineage block.

Use cases:

1. Producer read a raw packet: build `raw_refs` from the loaded packet, slice,
   preserved file, hash, and intra-file anchor.
2. Producer read a prior derived record: build `derived_refs` from exact
   `raw_anchor`, lane, record id, and record bytes hash when available.
3. Producer read a projection row: preserve the projection row's raw ref/anchor
   and carry the projection row identity as a derived or secondary traceability
   ref, depending on the producer's input.
4. Producer used transient live material that is not persisted: write
   `lineage_limitations` and do not claim full source-backed completeness.
5. Producer writes a record set: every member record that contains facts gets
   its own lineage block; the completion marker stays a completeness marker.
6. Reporter/projection sees missing lineage refs: surface a residual rather than
   upgrading the record into complete source-backed evidence.

Mechanical checks should enforce this at the write boundary where possible:

- `derived/` and `silver__*` records cannot silently omit lineage once the helper
  is adopted for that lane.
- `raw_refs` must have enough packet/file/hash material to resolve or audit.
- `derived_refs` must name exact lane and record id, not just a shortcode or
  video id.
- A record with only `lineage_limitations` can be valid, but it is not eligible
  for full behavioral-completeness claims.

## Patch Implications

Patch 1 should be the generic Silver lineage helper and validator, not an IG-only
payload field.

Patch 2 should apply the helper to product mentions first because that is the
current ambiguity: multiple transcript records can share a shortcode or video id,
so mentions must reference the exact transcript record consumed.

Patch 3 should apply the helper to IG deep-capture records. If there is no raw
packet or Attachment Record for the render attempt, those records must carry a
clear limitation rather than pretending transient media was preserved.

Patch 4 should teach projections/read models to use the lineage block for
eligibility and residuals. This is how the same mechanism extends beyond IG
without every source lane inventing a new field.

## Accepted Residuals

- No historical lake rewrite in v0. Existing records remain readable; new
  records get lineage as producers are touched.
- No raw media byte retention decision. The kit can describe transient media
  limits, but it does not authorize storing signed media URLs or raw audio/video
  bytes beyond existing packet paths.
- No universal record wrapper migration. The first implementation should be an
  additive block plus validator.
- No cross-platform identity. Source object refs stay source-local.
- No claim that rawless IG one-render deep capture is fully source-backed.
- No shared acquisition machinery. The kit connects records after capture; it
  does not merge IG, YouTube, Reddit, retail, or Fragrantica acquisition paths.

## Non-Claims

- Not implementation.
- Not validation or readiness.
- Not a data-lake physicalization decision.
- Not authorization to persist raw media bytes.
- Not a claim that all existing Silver records already satisfy the kit.
- Not a shared-core capture refactor.
