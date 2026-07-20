# Cleaning Derived-Record Anchor Contract v0 (AO-2)

```yaml
retrieval_header_version: 1
artifact_role: Architecture/contract decision (spec pending re-review) -- a first-class Cleaning input anchor for derived records (no preserved-file substrate), plus the lake-read coupling the audit needs to verify it, for the ASR transcript surface.
scope: >
  How a CleaningInputHandle honestly anchors and re-verifies a cleaning input that is a DERIVED record
  (youtube_audio -> transcript_asr), which lives in the data lake under derived/, not as a preserved file
  in a packet dir. Adds the `derived_record` anchor kind, injected DataLakeRoot read access for the smoke
  runner + periodic audit, the derived-record verification path, fail-closed selection, and audit coverage.
  Cross-spine (Cleaning x Data Lake x ECR audit). Pre-implementation spec; reworked after an UNSOUND first review.
use_when:
  - Building or reviewing the ASR (youtube_audio) ECR + Cleaning wiring.
  - Deciding how a derived record is referenced + verified as a cleaning input.
  - Checking what AO-2 changes vs. leaves invariant across the model, the smoke runner, and the audit.
open_next:
  - orca-harness/cleaning/models.py
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
  - orca-harness/runners/run_transcript_product_extract.py
  - orca-harness/data_lake/root.py
  - docs/decisions/cleaning_spine_data_lake_representation_defer_v0.md
authority_boundary: retrieval_only
status: SPEC_REVIEWED_SOUND_WITH_CHANGES -- v1 reworked after an UNSOUND first cut; a fresh de-correlated re-review returned SOUND_WITH_CHANGES with bounded fixes (see "Re-review adjudication"), now folded into implementation. Owner-authorized full AO-2 + un-defer 2026-06-27. Authorizes no merge; implementation in progress on this lane.
```

## Problem

ASR captures audio as a preserved file (`source_family=youtube`, `source_surface=youtube_audio`) **into a
DataLakeRoot** (`raw/<shard>/<audio_packet_id>/`), then writes the transcript as a DERIVED record at
`derived/<shard>/<audio_packet_id>/transcript_asr/<record_id>` via `data_root.append_record`
(`source_capture/transcript/asr_packet.py:87-185`, write-once/create-only). The transcript text -- the
actual cleaning input -- is therefore **not a preserved file**, and the whole ASR artifact set lives in
the lake (unlike #401 captions, which the smoke test provisions as a *plain packet directory* via
`write_caption_packet`). The existing cleaning anchor (`CleaningRawAnchor`) and the audit verifier resolve
only preserved files inside packet dirs (`packet_id -> slice_id -> file_id -> relative_packet_path ->
sha256`), and **neither the smoke runner nor the audit has any `DataLakeRoot` access** (confirmed: zero
matches for `DataLakeRoot|data_root|record_path` in either runner). The owner authorized building the full,
honest version (un-defer, 2026-06-27).

## What the first review found (and this rework resolves)

The first spec was reviewed **UNSOUND**. Resolutions, traceable per finding:

- **F1 (blocker) -- the audit cannot reach the lake.** RESOLVED: this spec adds an *injected* `DataLakeRoot`
  to the smoke runner + audit (mirroring `run_transcript_product_extract.run_extraction(*, data_root, ...)`),
  used only for lake-resident (`youtube_audio`) entries and `derived_record` anchors; **fail-closed** when a
  derived anchor is present but no lake root is wired (a finding, never a silent skip).
- **F2 (blocker) -- `validate_anchor_specificity` forces `anchor_value` on every non-file/json_pointer kind.**
  RESOLVED: the validator is amended to exclude `derived_record` (whole-record input, like `file`).
- **F3 (major) -- a 2nd/3rd anchor-kind allowlist my survey missed.** RESOLVED: full consumer list below;
  `cleaning/projection.py:_CLEANING_ANCHOR_KINDS` is deliberately **not** extended (projection rows are
  preserved-file-backed; a `derived_record` must never originate from a projection) and a guard/test pins that.
- **F4 (major) -- record selection not fail-closed.** RESOLVED: fail-closed selection below.
- **F5 (major) -- "re-verified on read" over-claimed.** RESOLVED: honest integrity statement below.
- **F6 (major) -- doctrine coherence.** RESOLVED: "Doctrine relationship" names the new audit<->lake read
  coupling explicitly.
- **F7/F9 (minor/nit) -- bidirectional validator + `_SAFE_SEGMENT`.** RESOLVED in the model contract.
- **F8 (minor, compounding) -- false-pass risk.** RESOLVED: a **tamper test** is a required acceptance criterion.
- **Representation (R1 vs R2):** R1 upheld (the consumer survey confirms a union would touch *more* sites).

## Decision

1. Add a `derived_record` anchor kind to the existing `CleaningRawAnchor` (additive R1).
2. Give the smoke runner and the periodic audit an **injected, optional `DataLakeRoot`**, used to load the
   lake-resident ASR audio packet and to resolve + re-hash the derived transcript record.
3. Bind the derived-record anchor's integrity at **handle-construction (stitch) time**, honestly framed
   (see Integrity guarantee); a durable derivation-time commitment is a named, deferred enhancement.

## Contract

### A. Model (`cleaning/models.py`)

- `anchor_kind`: add `"derived_record"` to the `Literal` (`:108`).
- `packet_id` (required, unchanged): for `derived_record`, the audio packet the record is keyed to
  (its `raw_anchor`); keeps `validate_refs_stay_keyed_to_raw` (`:213-219`) working unchanged.
- `sha256` (required, unchanged): for `derived_record`, the sha256 of the derived RECORD's bytes.
- `hash_basis` (required, unchanged): for `derived_record`, `"derived_record_bytes"`.
- `slice_id`, `file_id`, `relative_packet_path`: become `str | None`. New conditional `model_validator`:
  - preserved-file kinds (`file`, `json_pointer`, `html_selector`, `script_index`, `text_pattern`):
    REQUIRE all three non-empty AND `derived_record_ref is None` (today's behavior, preserved).
  - `derived_record`: REQUIRE `derived_record_ref` non-None AND FORBID all three preserved-file fields
    (assert each is None). Both directions explicit (F7).
- NEW `derived_record_ref: CleaningDerivedRecordRef | None`:
  - `CleaningDerivedRecordRef`: `{ subtree: Literal["derived"] = "derived", lane: str, record_id: str }`;
    `lane` and `record_id` non-empty AND each must satisfy the lake's `_SAFE_SEGMENT` grammar
    (`[A-Za-z0-9][A-Za-z0-9._-]{0,127}`) so `record_path` never raises mid-audit (F9).
- AMEND existing `validate_anchor_specificity` (`:128-138`): its catch-all that requires `anchor_value`
  must EXCLUDE `derived_record` (change the guard set to the specific kinds that truly need a value, i.e.
  treat `derived_record` like `file` -- no `anchor_value`). (F2)
- `CleaningInputHandle.raw_anchor` stays a single `CleaningRawAnchor` (NO union).
- `cleaning/core.py:_raw_anchor_identity` (`:23`): confirm the dedup-identity tuple is well-formed when
  `slice_id`/`file_id` are None (use `packet_id` + `anchor_kind` + `derived_record_ref` + `sha256` for
  derived records). A `None` in the tuple is acceptable for dedup; pin with a test.

### B. Lake-read coupling (smoke runner + audit)

- Both gain an OPTIONAL injected `data_root: DataLakeRoot | None` parameter (mirroring
  `run_transcript_product_extract`/`run_ig_reels_product_extract`, which take `data_root` as a kwarg and
  read via `data_root.lane_dir(...)`, `record_path(...)`, `load_raw_packet(...)`). Tests use
  `DataLakeRoot.for_test(tmp_path)`.
- NEW smoke manifest entry type `youtube_asr` (distinct from the caption `youtube` entry): fields
  `{ source_label?, audio_packet_id }`. The audio packet + transcript are resolved from the injected
  `data_root` by `audio_packet_id`, NOT from a `packet_dir`.
- Audit `_run_capture_preflight`: for `youtube_asr` entries, load the audio packet into `packet_index`
  via `data_root.load_raw_packet(audio_packet_id)` (its `container` is the lake `raw/<shard>/<packet>`
  dir, which the existing preserved-file checks then use unchanged for the ECR receipt).
- FAIL-CLOSED: if a `youtube_asr` entry or a `derived_record` anchor is encountered and `data_root is
  None`, emit a finding (`cleaning_derived_record_anchor_lake_unavailable`) / raise in the smoke runner --
  never silently skip (F8).

### C. Audit verification (`run_cleaning_spine_periodic_audit.py`)

- `_verify_cleaning_raw_anchor` (`:1317`): add a `derived_record` branch taken BEFORE the packet/slice/file
  resolution. Resolve `data_root.record_path(subtree="derived", raw_anchor=packet_id,
  lane=derived_record_ref.lane, record_id=derived_record_ref.record_id)`; read bytes; recompute sha256;
  compare to `anchor["sha256"]`. Fail-closed findings: `cleaning_derived_record_anchor_unresolved`
  (path absent), `cleaning_derived_record_anchor_hash_mismatch`, `cleaning_derived_record_anchor_unreadable`,
  `cleaning_derived_record_anchor_lake_unavailable` (no `data_root`). The packet/slice/file branch is NOT
  entered for `derived_record`.
- `_verify_anchor_specificity` (`:1428`): add a `derived_record` early-return (like `file` -- no
  `anchor_value` to verify); it must NOT fall through to `_specific_anchor_issue`.
- `_ANCHOR_VALIDATOR_KINDS` (`:54`): add `"derived_record"` so the adapter-contract subset check
  (`:685-714`) accepts it.
- `_PROJECTION_LESS_SOURCE_FAMILIES` (`:92`): extend `"youtube"` from `frozenset({"file"})` to
  `frozenset({"file", "derived_record"})` (captions=file from #401; ASR=derived_record). The projection-less
  coverage check (`:964-986`) then accepts `derived_record` for youtube.
- `_anchor_note` in the smoke runner (`:993-1012`): add a `"derived_record"` -> `"derived_record_anchor"` case.

### D. Smoke stitch (`run_capture_ecr_cleaning_smoke.py`)

New `_process_youtube_asr_entry`:
- `audio_packet = data_root.load_raw_packet(audio_packet_id)`; build the `SourceCapturePacket` from its
  manifest; `_derive_ecr_receipt(packet)` -- reused unchanged (audio IS a preserved file; receipt clears
  identity + inspectability, with timing + source_visibility residuals mirroring the #401 caption profile).
- Locate transcript records: `data_root.lane_dir(subtree="derived", raw_anchor=audio_packet_id,
  lane="transcript_asr")`, iterate (as `run_transcript_product_extract._asr_records` does -- returns a LIST).
  **Fail-closed selection (F4):** keep only records with `posture == "transcribed"`; require **exactly one**;
  on zero or many, raise (mirrors `_process_youtube_entry`'s `len(caption_files) != 1` discipline at
  `:834-843`).
- Build ONE `CleaningInputHandle` with a `derived_record` anchor: `packet_id=audio_packet_id`,
  `sha256=<sha256 of the selected record bytes>`, `hash_basis="derived_record_bytes"`,
  `derived_record_ref={subtree:"derived", lane:"transcript_asr", record_id}`, `projection_ref=None`,
  `ecr_ref` to the audio packet's receipt.

### E. Projection (`cleaning/projection.py`) -- deliberately NOT extended

`_CLEANING_ANCHOR_KINDS` (`:9`) and `_projection_anchor_kind` (`:131-144`) stay preserved-file-only.
Rationale: projection rows are views over preserved files; a `derived_record` anchor must never originate
from a projection. Add a one-line comment + a test asserting a derived record never traverses the
projection adapter. (Addresses F3 honestly rather than widening an allowlist that should stay narrow.)

## Integrity guarantee (honest statement -- F5)

The `derived_record` anchor binds the transcript's content to the `sha256` recorded in the cleaning handle
**at stitch time**. Because the lake's `append_record` is **write-once / create-only** (`data_lake/root.py`
refuses overwrite) and the v0 deployment is single-operator with the documented threat model (DL-003 scopes
out active same-host filesystem adversaries), the audit's re-hash **detects post-binding byte corruption of
the derived record**. This is integrity-on-read **relative to the cleaning handle**, NOT an independent
capture-time/derivation-time provenance commitment -- the lake stores no per-derived-record hash, so the
earliest commitment point is the stitch read. This is weaker than the preserved-file guarantee (which is
fixed at capture in the packet manifest) and is stated as such; it is sufficient under the current threat
model. **Named, deferred enhancement (recommended next):** commit each derived record's sha256 at
derivation time -- e.g. switch `asr_packet` to `append_record_set` and extend the completion marker to
record member sha256s -- so re-verification compares against a derivation-time value. That is a generic
lake-contract change (it benefits every record-set) and is intentionally scoped OUT of this lane to keep the
blast radius off the shared lake contract; flag it for owner decision.

## Acceptance criteria

1. ECR receipts on the `youtube_audio` packet clear identity + inspectability; timing + source_visibility
   carry honest residuals (mirrors the #401 caption clears-profile) -- pinned by test.
2. The smoke runner builds a valid `derived_record` handle for an ASR packet; it round-trips through the model.
3. **Full-path audit passes** (`overall_status` pass) for a well-formed ASR capture: it RESOLVES the derived
   record from the lake and re-hashes it.
4. **Tamper test (F8):** mutating the actual derived record bytes in the lake makes the audit emit
   `cleaning_derived_record_anchor_hash_mismatch`; a missing record emits `..._unresolved`; no `data_root`
   emits `..._lake_unavailable`. (A pass-only test cannot distinguish "verified" from "silently skipped".)
5. Model negative matrix (F2/F7): `derived_record` with ANY preserved-file field present, or without
   `derived_record_ref`, is rejected; a preserved-file anchor carrying `derived_record_ref` is rejected; a
   `derived_record` anchor with `anchor_value=None` is ACCEPTED (round-trips).
6. Fail-closed selection (F4): zero or multiple `transcribed` records for one audio packet -> the smoke
   runner raises; pinned by test.
7. Existing `file`/`json_pointer`/... anchors and ALL current tests stay green (no required-field regression);
   the projection adapter still rejects unknown kinds (E).

## Non-goals (out of scope)

- The cleaning->lake WRITER, cross-packet dedupe, `derived_retrieval` view (still deferred by
  `cleaning_spine_data_lake_representation_defer_v0.md`).
- A durable derivation-time hash for derived records (named above; deferred -- shared-lake-contract change).
- Pass-2 / gold writes (owner-deferred).
- Promoting the transcript to a preserved file ("laundering" -- forbidden by `asr_packet.py`).
- IG ASR (`ig_reels_audio`): same shape, validated after youtube_audio is green.

## Considered and rejected

- **Separate `CleaningDerivedAnchor` type + union `raw_anchor`** -- the consumer survey (3 anchor-kind
  allowlists + ~12 branch sites) shows a union touches MORE sites (`isinstance` everywhere `raw_anchor` is
  read/dumped) for no integrity gain. Rejected per Decision Priority #1 (least compounded risk). R1 upheld.
- **Reuse preserved-file fields for the derived record** -- dishonest (no slice/preserved file); the AO-3
  "fake fit". Rejected.
- **Bundle the durable derivation-time hash into this lane** -- it is a generic lake-contract change with
  blast radius across every record-set (ECR, cleaning silver, ...); deferred + named to keep this lane's
  blast radius contained. Owner may pull it forward.

## Doctrine relationship

`cleaning_spine_data_lake_representation_defer_v0.md` deferred the cleaning->lake WRITER + cross-packet work.
This spec un-defers ONLY the cleaning INPUT-anchor for derived records (owner-authorized 2026-06-27) AND, as
its read-side twin, introduces **audit/smoke lake-READ coupling** (an injected `DataLakeRoot`) -- which is
new and must be named (F6): the audit gains a dependency on the lake to verify derived records, while the
WRITER/dedupe machinery stays deferred. On sign-off, cross-reference both docs and record the un-defer.

## Re-review adjudication (fresh reviewer, v1 -> implementation)

A fresh de-correlated adversarial review of v1 returned **SOUND_WITH_CHANGES**: the design is validated
against code (injected-lake mirrors `run_transcript_product_extract.run_extraction`; `_derive_ecr_receipt`
accepts the lake container as `packet_dir`; lake-manifest -> `SourceCapturePacket` holds; F5 honesty
confirmed; projection-non-extension safe). The refinements below are folded into implementation; two
correct errors in the sections above.

- **[F-NEW-1, blocker] `reject_blank_anchor_fields` must be made None-tolerant.** That field-validator
  (`models.py:114-126`) runs `value.strip()` on `slice_id/file_id/relative_packet_path` BEFORE the
  model-validator; once they are Optional, a `derived_record`'s `None` crashes construction. Amend it to
  reject only NON-None blanks for those three (keep `packet_id/sha256/hash_basis` strictly non-empty).
  Without this, the round-trip criterion cannot pass.
- **[F-NEW-5, corrects A] dedup tuple `None` is NOT acceptable -- it crashes group-id minting.**
  `_group_id_for_identity` (`cleaning/core.py:29`) does `"\x1f".join(identity)`; `_raw_anchor_identity`
  (`:15-26`) already coerces `anchor_value`/`json_pointer` with `or ""` but passes the three preserved-file
  fields raw. Fix: coerce those three with `or ""` AND fold `derived_record_ref` (lane, record_id) into the
  tuple so distinct derived records do not false-collide. The "a None is acceptable" line in A is withdrawn.
- **[F-NEW-7, corrects C] there is no `_anchor_note` helper.** Verified: `run_capture_ecr_cleaning_smoke.py:991+`
  is `_retail_anchor_unverified_reason`/`_script_anchor_unverified_reason`; no `_anchor_note` exists. That C
  bullet is withdrawn -- there is no anchor-note sink to update for `derived_record`.
- **[F-NEW-2, expands C] full F1 threading surface.** Injecting `data_root` touches: `main` (CLI builds it via
  `DataLakeRoot.resolve()`), `run_cleaning_spine_periodic_audit(...)` (new `data_root` param), `_source_entries`
  (accept a `youtube_asr` entry shaped `{audio_packet_id, source_label?}`, carry `data_root`),
  `_run_capture_preflight` (branch: `data_root.load_raw_packet(audio_packet_id)` -> validate `loaded.manifest`
  to `SourceCapturePacket`, set `packet_dir = loaded.container`), `_verify_cleaning_raw_anchor` (derived
  branch), and `_run_lane_b_cleaning_breakpoint` (forward `data_root` to the re-invoked smoke runner). The
  smoke runner takes an injected `data_root` likewise; tests pass `DataLakeRoot.for_test(tmp_path)`.
- **[F-NEW-3] the `derived_record` branch is the FIRST statement** in `_verify_cleaning_raw_anchor` after the
  `packet_record is None` guard -- before `slice_by_id`/`preserved_by_id` are built -- so it never falls
  through to a misleading `..._slice_unresolved`. The tamper test asserts `cleaning_derived_record_anchor_hash_mismatch`.
- **[F-NEW-4] split the no-lake criterion:** (a) smoke runner with a `derived_record`/`youtube_asr` entry +
  no `data_root` -> raise; (b) audit of a CleaningPacket containing a `derived_record` handle with
  `data_root=None` -> blocking `cleaning_derived_record_anchor_lake_unavailable` and `overall_status != pass`.
- **[F-NEW-6] the new validator also forbids `anchor_value` AND `json_pointer` on `derived_record`** (assert
  both None), not just the three preserved-file fields.
- **[F-NEW-8] `youtube_asr` is a manifest ENTRY TYPE** mapping to `source_family="youtube"` +
  `source_surface="youtube_audio"`; add it to `_AUDIT_ENTRY_SOURCE_TYPES`; `_PROJECTION_LESS_SOURCE_FAMILIES`
  stays keyed by family `"youtube"` (extended to include `derived_record`).
- **[F-NEW-9] data_root sourcing:** the runner takes an already-constructed `DataLakeRoot` (injected, like
  `run_extraction`); the CLI `main` builds it via `DataLakeRoot.resolve()`; tests use `for_test`. Do not bake
  `resolve()` into the runner body.
- **[F5 wording] integrity coverage tightened:** the audit re-hash detects OUT-OF-BAND byte mutation of the
  derived record (the criterion-#4 tamper test exercises exactly this); in-contract `append_record` is
  create-only and cannot rewrite the record. The guarantee is integrity-on-read relative to the handle, not a
  derivation-time provenance commitment.

## Non-claims

Reviewed SOUND_WITH_CHANGES (fresh de-correlated reviewer); findings folded into implementation above.
Authorizes no merge. Not validation, readiness, or acceptance. Implementation + tests proceed on this lane;
final acceptance is the green suite plus the acceptance criteria above.
