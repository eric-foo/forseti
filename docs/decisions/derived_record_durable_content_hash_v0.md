# Derived-Record Durable Content Hash (v0)

```yaml
retrieval_header_version: 1
artifact_role: Architecture/contract decision (spec pending delegated review) -- commit a derived record's content sha256 at derivation time (in the record-set completion marker) so the AO-2 audit verifies a transcript against a derivation-time commitment, not a stitch-time snapshot.
scope: >
  Strengthen derived-record integrity from stitch-time binding (AO-2 / #405) to a derivation-time
  commitment. Adds a per-member sha256 to the record-set completion marker (additive, lake-wide), a
  focused marker-sha reader, switches the ASR transcript write to append_record_set, and points the
  AO-2 smoke/audit at the durable sha. Cross-spine (Data Lake x Capture x Cleaning audit). Builds on #405.
use_when:
  - Building or reviewing derivation-time integrity for derived lake records.
  - Deciding how a derived record commits a durable content hash.
  - Checking what changes vs. stays invariant in the record-set marker contract.
open_next:
  - orca-harness/data_lake/root.py
  - orca-harness/source_capture/transcript/asr_packet.py
  - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - docs/decisions/cleaning_derived_record_anchor_contract_v0.md
authority_boundary: retrieval_only
status: SPEC_REVIEWED_SOUND_WITH_CHANGES -- owner-authorized 2026-06-27; a fresh delegated adversarial review returned SOUND_WITH_CHANGES (architecture validated against code; fixes folded -- see adjudication). Builds on AO-2 (#405). Authorizes no merge; implementation in progress on this lane.
```

## Problem

AO-2 (#405) binds a `derived_record` cleaning anchor's `sha256` at **stitch time** (the smoke runner reads
the lake record and records its sha). Under the lake's write-once + single-operator threat model (DL-003)
that detects out-of-band mutation, but it is weaker than the preserved-file guarantee, which commits the
sha at **capture** (the earliest point). Derived records carry **no durable derivation-time content hash**:
`append_record` writes bytes with no sha, and the transcript record's provenance carries the AUDIO sha, not
its own. So today the earliest commitment point for a derived record's content is the stitch read.

## Decision

Commit each derived record's content `sha256` at **derivation time**, inside the record-set **completion
marker** (additive), expose a focused reader, switch the ASR transcript write to `append_record_set`, and
point the AO-2 smoke/audit at the durable sha. Lake-wide: every record-set marker becomes a
content-integrity manifest; ASR is the first consumer. Recommended over a per-record sidecar because it
reuses the existing record-set machinery additively (verified: no runtime consumer strict-parses the marker).

## Contract

### A. Lake (`data_lake/root.py`)

- `append_record_set`: compute each member's `sha256` (from the bytes it writes) and add
  `member_sha256: {lane: sha256}` to the completion-marker body (alongside `record_id` + `member_lanes`).
  **Additive** -- `is_record_set_complete` (line 587) and every current consumer read the marker via
  `.get()` and ignore unknown keys.
- NEW reader `read_record_set_member_sha256(*, subtree, raw_anchor, record_id, completion_lane, member_lane)
  -> str | None`: read the marker, return that member's committed sha (`None` if the marker is absent, or
  `member_sha256` is absent for an old marker). Fail-closed on a malformed marker (return `None`); validate
  segments like the sibling methods.
- `is_record_set_complete` is **UNCHANGED** -- presence-only semantics preserved; no caller is forced to
  re-hash on a skip-if-done check.

### B. ASR writer (`source_capture/transcript/asr_packet.py`)

- Switch the transcript write from
  `append_record(subtree="derived", raw_anchor=<audio_packet_id>, lane="transcript_asr", record_id=...)`
  to
  `append_record_set(subtree="derived", raw_anchor=<audio_packet_id>, record_id=...,
  members={"transcript_asr": <bytes>}, completion_lane="transcript_asr__set")`.
- The member record's path + `record_id` are **UNCHANGED** (still
  `derived/<anchor>/transcript_asr/<record_id>`); the marker is a sibling in the completion lane. So #405's
  `record_path` resolution AND existing readers (`run_transcript_product_extract._asr_records`) still find
  the record unchanged.
- The write-once / no-overwrite + posture/cue contracts are unchanged.

### C. AO-2 integration (`run_capture_ecr_cleaning_smoke.py` + `run_cleaning_spine_periodic_audit.py`)

- Smoke `_process_youtube_asr_entry`: after selecting the one transcribed record, read the durable sha via
  `read_record_set_member_sha256(...)`.
  - **If present:** set `anchor.sha256` = the marker sha, `hash_basis = "derived_record_marker_sha256"` (the
    derivation-time commitment). DEFENSIVELY verify `marker_sha == sha256(record bytes)` at stitch; on
    mismatch raise (a marker/record disagreement is corruption -- fail closed, never silently prefer one).
  - **If absent (backward-compat -- an old `append_record` record with no marker):** fall back to
    `sha256(record bytes)`, `hash_basis = "derived_record_bytes"` (stitch-time, exactly #405).
- Audit `_verify_derived_record_anchor`: **mechanism UNCHANGED** (resolve the record + re-hash + compare to
  `anchor.sha256`). Because `anchor.sha256` is now the derivation-time marker sha for new records, the audit
  verifies against the derivation-time commitment; `hash_basis` records which guarantee (derivation-time vs
  stitch-time) applies. No new finding codes.

## Integrity (now stronger, still honest)

For records written after this lane: the anchor binds the transcript to the `sha256` the **lake computed
when the transcript was written** (derivation time). The audit re-hash then detects ANY change since
derivation -- matching the preserved-file commit-at-source guarantee. For old (markerless) records the
stitch-time fallback applies, marked honestly via `hash_basis`. The lake's write-once still holds; the
marker sha is trustworthy by construction (the lake computes it from the bytes it writes).

## Acceptance criteria

1. `append_record_set` writes `member_sha256[lane] == sha256(member bytes)` in the marker;
   `read_record_set_member_sha256` returns it; `is_record_set_complete` is unchanged (presence-only; a set
   with the new marker field still reports complete).
2. `write_asr_transcript` writes the transcript via `append_record_set`; the marker records the transcript's
   sha; the record path/id are unchanged (existing `_asr_records` reader + #405 audit still resolve it).
3. AO-2 smoke sets `anchor.sha256` = the marker sha with `hash_basis="derived_record_marker_sha256"`; the
   full-path audit passes (verifies against the derivation-time commitment).
4. Tamper: mutate the record bytes after derivation -> the audit re-hash != `anchor.sha256` (the marker sha)
   -> `cleaning_derived_record_anchor_hash_mismatch` + fail. (Now a derivation-time check.)
5. Backward-compat: an ASR record written via the OLD `append_record` path (no marker) -> smoke falls back
   to stitch-time (`hash_basis="derived_record_bytes"`); the audit still verifies + passes.
6. Marker/record disagreement: if the marker sha != the record bytes at stitch, the smoke runner fails
   closed (raise) rather than trusting either.
7. All current record-set consumers (ECR `ecr/lake.py`, cleaning silver `transcript_product_lake.py`, IG
   deep-capture) stay green; exact-match marker tests (`test_ecr_lake_pilot.py:221`, any in
   `test_data_lake_record_set.py`) are updated for the additive field.

## Non-goals

- Changing `is_record_set_complete`'s semantics (stays presence-only; no forced re-hash).
- Making ECR / cleaning-silver / IG lanes *consume* the durable sha -- they get it in their markers
  (available for future use), but only ASR's audit reads it here.
- A standalone derived-record integrity index / `derived_retrieval` view (still deferred).
- Migrating existing markerless records (the backward-compat fallback covers them).
- The cleaning->lake WRITER / cross-packet dedupe (still deferred by
  `cleaning_spine_data_lake_representation_defer_v0.md`).

## Considered and rejected

- **Per-record sidecar sha for single `append_record`** -- new per-record file machinery; the marker-based
  approach reuses the existing record-set mechanism additively. Rejected (more machinery, new file per record).
- **Extend `is_record_set_complete` to verify content shas** -- changes a widely-used primitive's semantics
  (presence -> presence+integrity), forcing re-hashes on every skip-if-done check across ECR/silver/IG.
  Rejected; a separate opt-in reader instead.
- **Keep stitch-time only (AO-2 as-is)** -- the owner chose the stronger derivation-time commitment.

## Doctrine relationship

Realizes the deferred enhancement named in `cleaning_derived_record_anchor_contract_v0.md` (AO-2). Builds on
#405. The cleaning->lake WRITER + cross-packet dedupe + `derived_retrieval` view stay deferred. The marker
gaining a content sha is a lake-contract change; it is additive and backward-compatible, so it does not
amend the derived-layout contract's identity/path grammar.

## Delegated-review adjudication (fresh reviewer, v0 -> implementation)

A fresh adversarial review returned **SOUND_WITH_CHANGES**: the architecture is validated against code -- the
marker-format change is genuinely additive (no production consumer reads the marker body directly; all use
`append_record_set` + `is_record_set_complete`), the lake computes the per-member sha from the bytes it
writes (trustworthy by construction), the audit mechanism is unchanged, and the `transcript_asr__set` marker
lane does not pollute the `transcript_asr` iterators. Fixes folded into implementation:

- **[F3, major -- most important] No silent weakening.** The reader must distinguish **marker-absent**
  (legitimate old markerless record -> stitch-time fallback) from **marker-present-but-malformed / missing
  member sha** (corruption -> **fail closed**). Every record written via `append_record_set` (the new ASR
  path) MUST have a marker, so a new record whose marker is unreadable or lacks its `member_sha256` must
  **raise**, never silently downgrade to `derived_record_bytes`. Concretely: `read_record_set_member_sha256`
  returns `None` ONLY when the marker file is absent; a present-but-malformed marker, or a present marker
  missing the member's sha, raises (smoke treats it fail-closed). Add acceptance: "new ASR record, marker
  corrupted / missing sha -> smoke fails closed, not silent stitch-time."
- **[F2, major] ASR writer return shape.** `append_record_set` returns `dict[str, Path]`, not a `Path`.
  `asr_packet.py` takes `written["transcript_asr"]` for the rel-path and keeps the returned
  `(code, message)` string **byte-for-byte unchanged** (parsers depend on it: `test_youtube_asr_packet.py:37,41`,
  `test_asr_ecr_cleaning_smoke_audit.py:71`).
- **[F1, major] Blast-radius miss.** `test_asr_ecr_cleaning_smoke_audit.py:155` asserts
  `hash_basis == "derived_record_bytes"` on a clean run; it becomes `"derived_record_marker_sha256"` after
  the switch. Update it, and ADD the missing ASR backward-compat test (write via legacy `append_record` ->
  assert the `derived_record_bytes` fallback) that acceptance #5 needs.
- **[F6] Acceptance #7 precision.** The only EXISTING exact-match marker assertion that breaks is
  `test_ecr_lake_pilot.py:220`. `test_data_lake_record_set.py` has no breaking assertion (its exact-dict
  lines are injected corruption fixtures); it gets a NEW positive `member_sha256` assertion (acceptance #1).
- **[F5] Integrity framing.** The marker sha binds to the member bytes at marker-creation; the stitch-time
  `marker_sha == sha256(record bytes)` re-check (§C) is **load-bearing** (it closes the gap against post-write
  divergence), not defensive decoration.
- **[F4] Line ref.** `is_record_set_complete` is defined at `root.py:563` (marker-body read at 582-599).

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Data Lake record-set completion marker now commits each member's lake-computed content
    sha256 (additive `member_sha256` field), giving derived records a derivation-time
    content-integrity commitment; the AO-2 audit verifies a transcript against that derivation-time
    sha rather than a stitch-time snapshot. Additive + backward-compatible: is_record_set_complete
    and every existing record-set consumer read the marker via .get() and ignore the new field;
    legacy markerless records keep the stitch-time fallback.
  trigger: architecture_doctrine
  related_triggers: []
  controlling_sources_updated:
    - docs/decisions/derived_record_durable_content_hash_v0.md
  downstream_surfaces_checked:
    - orca-harness/data_lake/root.py
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - docs/decisions/cleaning_derived_record_anchor_contract_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        The derived-layout identity/path grammar (derived/<anchor>/<lane>/<record-id> + the
        completion-marker mechanism) is UNCHANGED; member_sha256 is an additive field inside the
        existing marker body, not a new layout, lane, or grammar.
    - path: docs/decisions/cleaning_derived_record_anchor_contract_v0.md
      reason: >
        AO-2 names this durable derivation-time hash as its recommended deferred enhancement; this
        lane realizes it. The AO-2 doc correctly described its own pre-realization state; a one-line
        "realized in derived_record_durable_content_hash_v0.md" touch-up is a trivial doc-sync
        fast-follow, not load-bearing (no behavior or authority depends on it).
  stale_language_search: >
    rg -n "deferred.*derivation-time|stitch-time only|named, deferred enhancement"
    docs/decisions/ orca-harness/
  stale_language_search_result: >
    The only load-bearing hit is the AO-2 contract's description of stitch-time binding as its
    pre-realization state + the named deferred enhancement -- correctly superseded by this lane and
    noted above as a trivial doc-sync fast-follow. No surface falsely asserts the durable
    derivation-time hash is still unavailable for the transcript_asr lane.
  non_claims:
    - not validation
    - not readiness
    - not acceptance
    - not a cleaning->lake WRITER authorization
    - not a derived-layout identity/path grammar change
    - not a content-verification gate for ECR/silver/IG lanes (they gain the marker sha, but only ASR's audit consumes it here)
```

## Non-claims

Reviewed SOUND_WITH_CHANGES (fresh delegated reviewer); fixes folded + verified (suite green, F3 fail-closed
proven). Authorizes no merge. Not validation, readiness, or acceptance. Final acceptance is the green suite
plus the acceptance criteria above; merge is owner-gated and stacked on #405.
