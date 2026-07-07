# Core Spine v0 Data Lake Bronze Full-GT Next Material Decisions v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/decision-request record
scope: >
  Planning-only next material decision packet after the Bronze full-GT A-D
  scoping record: Batch A source inventory and Manifest/equivalent fork,
  Batch B/C physicalization decision gates, and Batch D proof/CI threshold
  hardening before any third-proof work.
use_when:
  - Continuing Bronze full-GT planning after the A-D scoping artifact.
  - Checking the source inventory seed for raw writers and non-raw lake touchpoints.
  - Preventing AR body/backend or retention/lawful-erasure convenience from choosing architecture.
  - Deciding whether a third consumer proof is materially necessary.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
  - docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
  - forseti-harness/data_lake/lane_registry.py
branch_or_commit: >
  Authored on codex/bronze-full-gt-next-decisions stacked on
  codex/bronze-full-gt-scoping at 165e5d802d78b1dbbf309b5d2a852dd493dca733.
  Recheck base state if PR #546 is merged, retargeted, or rewritten.
superseded_by:
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
stale_if:
  - PR #546 is closed without merge, materially rewritten, or superseded.
  - The Bronze MGT baseline, Storage Contract, Attachment Record contract, or Silver Vault contract changes.
  - Raw writer seam coverage, lane registry, Bronze catalog, or AR helper behavior materially changes.
  - A later accepted authority selects Manifest v2, AR body layout/backend, retention/lawful-erasure, or a full-GT path.
```

## Purpose

This is a source inventory and decision request, not runtime implementation.
It does not select Manifest v2, a manifest-equivalent serialization, AR body
layout, storage backend, retention mechanism, lawful-erasure mechanism,
lake-doctor/CI implementation, a third proof, or Bronze full GT.

The immediate goal is to make the next decisions hard to take accidentally:
first inventory writers and non-raw lake touchpoints, then decide Manifest or
equivalent serialization; separately gate AR body layout/backend; separately
gate retention/lawful-erasure/backend lock-in; and only then allow proof/CI work
to expand.

## Post-Merge Supersession Note

This packet remains useful as the A-D source inventory and decision-request
record. It is no longer the active continuation anchor after PR #555 hardened
the non-raw touchpoint inventory and scratch-safe enumeration gate.

Use
`core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
for the next physicalization decision. Do not use this packet's older
"Next Material Steps" to start a new PR/review/admin loop, third proof, backend
selection, or runtime implementation.

## Source And Assumption Gate

```yaml
assumption_gate:
  status: READY_WITH_VERIFIED_LEDGER
  applies_to: "planning-only Batch A, Batch B/C, and Batch D next material steps"
  load_bearing_assumptions:
    - assumption: "The A-D scoping artifact is the current planning base."
      why_load_bearing: "This packet derives its batch boundaries from that artifact."
      verify_by: source_read
      verdict: verified_real
      evidence: "Read forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md in this worktree."
    - assumption: "The repo already has source-visible raw-writer seam coverage and non-raw lane role surfaces that can seed Batch A inventory."
      why_load_bearing: "Without them this packet would invent inventory shape rather than request a real discovery gate."
      verify_by: source_read
      verdict: verified_real
      evidence: "Read test_capture_runner_lake_seam_coverage.py, lane_registry.py, source_capture writer/assembly, data_lake root, and catalog helper surfaces."
    - assumption: "The owner requested decision artifacts, not runtime implementation."
      why_load_bearing: "Runtime edits here would select architecture by implementation convenience."
      verify_by: owner
      verdict: verified_real
      evidence: "Current instruction: Batch A is source inventory and decision request, not runtime implementation; Batch B/C is a physicalization decision brief; Batch D is proof/CI threshold hardening."
  prerequisites:
    - item: "Keep this lane docs-only until review/adjudication."
      triage: blocker
      owner: agent
      order: 0
      basis: "Current instruction and A-D scoping artifact both forbid runtime implementation here."
    - item: "Run delegated review-patch after this authored artifact is written."
      triage: blocker
      owner: owner
      order: 1
      basis: "Owner explicitly requested delegated review-patch after; execution requires an independent de-correlated receiving lane."
  next_authorized_step: "Write this planning artifact, update repo-map reachability, then route a delegated review-patch commission."
```

## Source-Read Ledger

| Source | Why read | Decision support |
| --- | --- | --- |
| `core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md` | Current A-D planning base | Batch boundaries, non-claims, review timing. |
| `bronze_silver_two_family_consumer_proof_closeout_v0.md` | Proof boundary after PR #542 | Third-proof threshold and YouTube ambiguous-AR carry-forward. |
| `core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md` | Full-GT residual source | MGT items 1-7, no full-GT claim, Manifest/backend residuals. |
| `core_spine_v0_data_lake_storage_contract_v0.md` | Physicalization gate source | No-smart-lake invariants, backend selection boundary, blocker-1/2 direction. |
| `core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` | AR body relationship source | Compact entry plus immutable hash-checkable body; accepted and rejected shapes. |
| `core_spine_v0_data_lake_silver_vault_record_contract_v0.md` | Silver raw-ref intake source | Public Bronze packet/catalog/AR surfaces and missing-AR residual. |
| `source_capture/writer.py`, `packet_assembly.py`, `data_lake/root.py` | Writer primitives | Raw packet writer, staging/publish, availability, append-only derived writes. |
| `data_lake/catalog.py` | Bronze catalog/AR helper source | Generated read state, AR rows, body resolution and hash verification. |
| `test_capture_runner_lake_seam_coverage.py` | Current raw-writer seam detector | Existing AST discovery seed and explicit Bronze runner surface. |
| `data_lake/lane_registry.py` | Non-raw lane role registry | Derived lane roles, Silver front-door guard, pending bypass baseline. |

The source inventory below is a static read of current source. It is not a
deterministic discovery gate and not proof of completeness. Batch A should turn
the inventory logic into a fail-capable gate before any Manifest/equivalent
serialization is selected.

## Batch A - Source Inventory Plus Manifest/Equivalent Fork

### Raw-Packet Writer Surface

Current raw-packet writing is centralized around three primitives:

- `source_capture.writer.write_local_source_capture_packet` creates the packet
  manifest and receipt, copies preserved files, and when a `DataLakeRoot` is
  supplied publishes the completed staging directory to `raw/<shard>/<packet_id>/`
  and records content-free availability.
- `source_capture.packet_assembly.stage_and_write_packet` is the adapter-result
  last-mile helper: it stages ordered artifacts, validates capture-posture
  honesty, forwards to `write_local_source_capture_packet`, and cleans staging.
- `data_lake.root.DataLakeRoot` owns write-once raw staging/publish, append-only
  derived/ack record primitives, availability, and verified raw reads that
  re-hash preserved bodies against the manifest.

The existing contract test already acts as a partial raw-writer discovery seed:

- `EXPECTED_BRONZE_WRITER_RUNNERS` enumerates the current Bronze writer runner
  surface: fragrance review, Fragrantica/Parfumo MGT capture, IG orchestrator,
  generic source-capture packet runners, media/price/HTTP/archive/browser
  variants, TikTok batch/video, and YouTube ASR/caption/watch runners.
- `KNOWN_UNSYNCED` is empty, so the current test expects every detected
  packet-producing runner to expose and forward the Data Lake seam.
- `_source_capture_packet_writer_names()` recursively discovers indirect
  source-capture packet writer functions so thin wrappers cannot bypass the
  seam simply by not calling `stage_and_write_packet` directly.

AST source inventory from this lane observed current source-capture packet
writer functions including:

```text
source_capture.writer.write_local_source_capture_packet
source_capture.packet_assembly.stage_and_write_packet
source_capture.audience_post_packet.write_audience_post_packet
source_capture.fragrance_review_lake.write_fragrance_review_capture_packet
source_capture.youtube_watch_packet.write_youtube_watch_packet
source_capture.tiktok.batch_packet.write_tiktok_batch_packet
source_capture.tiktok.video_packet.write_tiktok_video_packet
source_capture.transcript.caption_packet.write_caption_packet
source_capture.transcript.asr_packet.write_asr_transcript
source_capture.transcript.ig_reels_audio_packet.write_ig_reels_asr_transcript
```

Decision request A1:

Adopt the existing seam detector as the seed for a deterministic Batch A
touchpoint inventory, but do not treat its current test as sufficient for full
GT. The future gate should produce a durable inventory of:

1. raw packet writers and runner seams;
2. non-raw lake touchpoints;
3. explicit exclusions with reasons;
4. owner-reviewed unknowns;
5. the Manifest/equivalent decision fork each touchpoint would affect.

### Non-Raw Lake Touchpoints

Non-raw lake writes and reads appear through these current surfaces:

- `DataLakeRoot.append_record` and `append_record_set` create append-only
  derived/ack records with create-only semantics and detectable record-set
  completion markers.
- `data_lake.silver_record.append_silver_record` is the validating front-door
  for `silver_envelope` lanes.
- `data_lake.lane_registry.LANE_ROLES` classifies current derived lanes:
  `silver_envelope`, `silver_lineage`, `cleaning_audit`, `projection`, `ecr`,
  `signal_content`, and `transcript_capture`.
- `FRONT_DOOR_PENDING` is empty, meaning no current `silver_envelope` lane is
  allowed to bypass the Silver front-door as a grandfathered exception.
- `data_lake.catalog.rebuild_catalog`, `source_surface_catalog_rows`, and
  `load_attachment_record_body` are generated Bronze read surfaces, not raw
  authority. They rebuild from verified raw manifests and resolve AR bodies by
  re-loading raw packets and checking body hash.

AST source inventory observed non-raw callers in ECR, signal-content, cleaning,
source-capture projection lanes, transcript-derived records, Silver record
front-door, and catalog runner/helper surfaces. That is enough to request a
deterministic inventory gate; it is not enough to claim every current or future
touchpoint is already covered.

Decision request A2:

Do not select Manifest v2 or a manifest-equivalent serialization until A1's
deterministic inventory exists. After A1, compare these forks:

| Fork | Shape | Why it may win | Why it may lose |
| --- | --- | --- | --- |
| A2-F1 Manifest v2 | Promote packet manifest schema/versioning to carry the needed index/AR relationship directly. | One canonical packet manifest path; clear migration target. | Highest migration and schema lock-in; risks mutating raw-truth assumptions too early. |
| A2-F2 Manifest-equivalent packet index | Keep raw manifests stable; add rebuildable packet-index/AR entries over preserved bodies. | Lower raw schema lock-in; matches current catalog/AR helper posture. | Must prevent generated index from being treated as authority; still needs replay/dual-read rules. |
| A2-F3 Hybrid dual-read/replay | Keep legacy direct fields readable while new material uses AR/index entries, with explicit replay triggers. | Most compatible with incumbent packets and current contracts. | Can become permanent ambiguity unless cutoff and replay ownership are explicit. |

Recommended decision posture for now: accept A1 as the immediate next
implementation-scoping input, and hold A2 as an owner decision after inventory.
Do not let the convenience of current generated catalog rows become an implicit
Manifest-equivalent selection.

## Batch B/C - Physicalization Decision Brief

This is one physicalization brief with two gates. Gate 1 decides the AR
body-layout/backend posture. Gate 2 decides retention, lawful-erasure, and
backend lock-in constraints. Backend convenience is not allowed to choose either
gate.

### Gate 1 - AR Body Layout / Backend

Question:

Which physical relationship should bind a compact AR entry to an immutable,
hash-checkable body while preserving public Bronze/Silver re-resolution and no
private packet-member path inference?

Gate 1 must answer:

- What key finds the body: packet id, slice id, file/attachment id, body hash,
  payload kind, and replay/version pins.
- What bytes are covered by `hash_basis`.
- Whether the body is a packet member, sidecar, external blob, database row, or
  equivalent immutable material.
- How `source_surface_catalog_rows` and `load_attachment_record_body` or their
  successors remain public helper surfaces.
- How Availability Index/catalog rebuilds remain non-authoritative and
  rebuildable from committed packet/attachment keys.
- How corrections/replays append new material rather than mutating pinned
  historical packets.

Options to compare:

| Option | Shape | Fit | Lock-in risk |
| --- | --- | --- | --- |
| B1 Current preserved-body AR | Keep generated AR entries over preserved raw packet bodies. | Lowest change; preserves raw authority and current Silver proof paths. | Not full physicalization; no final layout/backend; generated index may be overread. |
| B2 Packet-member or packet-bundle body | Store AR body as explicit immutable packet material with compact manifest/index entry. | Strong fit with write-once raw and hash basis. | Requires packet/manifest serialization and migration/replay decision. |
| B3 Immutable sidecar/body object | Store body outside the manifest body but packet-keyed and hash-pinned. | Can separate large bodies from compact manifest/index entries. | Loose sidecars are rejected unless keyed, indexed, and hash-checkable; backend can leak into architecture. |
| B4 External backend/object/database body | Store body in object/database backend with immutable hash-checked reference. | May solve scale, query latency, or operational constraints. | Highest backend lock-in; must pass Gate 2 before selection. |

Gate 1 decision request:

Select the relationship and evidence required, not the backend by convenience.
The minimum acceptable Gate 1 output is an ADR-style option ledger with one
chosen or deferred body relationship, explicit read helpers, exact hash-basis
rules, replay/migration implications, and rejected-shape reasons. If the owner
does not want an ADR yet, keep B1 as current MGT posture and mark full-GT
physicalization not selected.

### Gate 2 - Retention / Lawful-Erasure / Backend Lock-In

Question:

Which retention and lawful-erasure constraints must be true before any AR body
layout or backend becomes hard to reverse?

Gate 2 must be answered before choosing B3 or B4, and before any backend
selection is treated as more than an implementation convenience.

Constraints to name:

- Raw packet immutability and create-only write discipline.
- Append-only derived records and acknowledgements.
- Rebuildable, non-authoritative indexes.
- By-key discovery as authority before queues/events.
- No-smart-lake boundary: the lake does not clean, dedupe, score, judge,
  schedule, retry, route, or call downstream lanes.
- Operational data stays outside Git unless a later physicality-location
  contract explicitly supersedes that model.
- Retention and lawful-erasure cannot be hidden inside storage-engine choice.

Options to compare:

| Option | Shape | Fit | Lock-in risk |
| --- | --- | --- | --- |
| C1 Current no-selection posture | Keep retention/erasure/backend deferred while using current raw-preserved-body helpers. | Best for this planning lane; avoids fake compliance. | Cannot support full-GT physicalization claim. |
| C2 Append-only plus tombstone/supersession | Preserve raw/derived history and express corrections or unavailability as new records. | Fits current lake invariants. | Does not by itself answer lawful-erasure obligations. |
| C3 Key-separated encrypted body posture | Put erasure-sensitive body material behind explicit keying/crypto-shred semantics. | Candidate if lawful erasure becomes a real requirement. | High lock-in; requires owner/legal decision and backend-specific tests. |
| C4 Backend-native retention controls | Use object/database retention, WORM, lifecycle rules, or policy controls. | Operationally strong if selected deliberately. | Storage convenience can silently choose architecture; must not precede Gate 1 and owner erasure posture. |

Gate 2 decision request:

Owner should decide whether this lane needs a retention/lawful-erasure ADR
before any backend ADR, or whether full-GT physicalization remains deferred. If
full-GT physicalization proceeds, backend selection must prove the Data Lake
invariants and the chosen retention/erasure posture; it cannot be justified only
by query convenience, local filesystem convenience, or implementation speed.

## Batch D - Proof / CI Threshold Hardening

Batch D controls when proof work expands. Its job is to prevent third-proof
work from becoming default activity and to prevent CI from passing while hiding
the one branch that would invalidate the AR join model.

### YouTube Ambiguous-AR Branch

The YouTube producer source carries an explicit ambiguous-AR fallback kind and
limitation:

```text
raw_packet_fallback_ambiguous_attachment_record
typed_attachment_record_ambiguous_for_raw_ref
```

This lane did not observe a dedicated YouTube ambiguous-AR unit test in the
narrow grep for those exact tokens under the YouTube producer tests. Therefore
Batch D must carry the branch explicitly as:

```text
YouTube ambiguous AR is code-present but not test-proven in this source inventory.
```

If a later targeted read proves a dedicated test exists, Batch D may upgrade the
status to test-pinned with the exact test path and line. Until then, no third
proof may rely on the ambiguous branch as validated.

### Materially Different Raw-Body / AR-Join Test

Before any third-proof work, define a test that distinguishes "another source
family" from "materially different raw-body or AR-join shape."

A candidate is materially different only if at least one of these is true:

- The raw body is not a single JSON-like preserved file with a one-body-one-row
  relationship.
- A source packet has multiple bodies that a Silver producer must join or
  choose among.
- One AR body can produce many Silver observations or many AR bodies can
  support one observation.
- The join key is not the current IG-style raw-ref tuple and not the current
  YouTube packet/body-hash shape.
- The body type is binary/media, HTML plus companion payload, transcript/comment
  partitioned text, or another shape where payload identity is not obvious from
  packet/file hash alone.
- Ambiguous candidates are possible and choosing any one would create a false
  source-backed raw ref.

The materially-different test must include at least one fixture where the
producer's join key matches multiple AR candidates. Expected behavior: the
producer does not choose one, emits an explicit ambiguous/missing AR residual or
fallback raw ref allowed by its contract, and preserves enough hash material for
later re-resolution. A test that covers only hit and missing paths is not enough
to unlock third-proof work.

### CI Threshold

Future proof/CI hardening should promote checks that can fail on the specific
failure classes below:

- a new packet-producing runner lacks a real Data Lake seam or data-root
  forwarding;
- a new non-raw derived lane is undeclared or bypasses the correct front-door;
- Bronze catalog rows are stale, missing, orphaned, or treated as authority;
- `load_attachment_record_body` cannot re-resolve and hash-check the body;
- a Silver producer hides missing or ambiguous AR state;
- generated indexes pass while raw manifests or preserved bodies fail
  verification;
- representative fixture lakes omit the raw-body/AR-join shape being claimed.

CI should not be treated as full-GT proof merely because these gates are green.
The gates are failure visibility and representative coverage, not production
lake validation, all-source coverage, or Bronze readiness.

Decision request D:

Accept the threshold: no third-proof work until the YouTube ambiguous-AR branch
is either test-pinned or explicitly carried as code-present/not-test-proven, and
the materially-different raw-body/AR-join test above is part of the third-proof
entry contract.

## Next Material Steps

1. Continue from
   `core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`.
2. Decide or explicitly defer Gate 1: Attachment Record body layout/backend
   relationship.
3. Decide or explicitly defer Gate 2: retention/lawful-erasure/backend lock-in.
4. Only after those gates are answered or consciously deferred, scope
   implementation or proof/CI expansion. Do not start third-proof work as a
   substitute for the physicalization decision.

## Non-Claims

- Not runtime implementation authorization.
- Not Manifest v2, manifest-equivalent, dual-read, replay, or migration selection.
- Not AR body layout, sidecar, backend, object store, database, or DuckDB selection.
- Not retention, lawful-erasure, WORM, crypto-shredding, or compliance posture.
- Not lake-doctor/CI implementation.
- Not validation, readiness, production lake proof, Silver readiness, all-source coverage, or Bronze full GT.
- Not a claim that this static inventory is complete or live as a deterministic discovery gate.
