# Source Capture Packet Schema Evolution + Validation Placement — Architecture Planning Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: >
  Thin architecture-planning prompt for the durable structure of Source Capture
  packet schema evolution: where strict current-schema validation belongs
  (every-read vs admission/consume gate vs version-aware read), how persisted
  packets survive future breaking schema changes, and when to build the chosen
  mechanism vs defer. Surfaced by the R2 posture-vocabulary closure, which made a
  breaking packet-schema change and exposed that read-back ignores manifest_version.
  Non-executing; uses 3 subagents for option development + synthesis.
use_when:
  - Running or dispatching the Source Capture packet schema-evolution architecture decision.
authority_boundary: retrieval_only
open_next:
  - orca-harness/source_capture/models.py
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
input_hashes:
  orca-harness/source_capture/models.py: 3B89A19BAEAB90762C34FE0C95517A005D383933E48057C1ADD12E004A3A7245
branch_or_commit: main @ d69aeee (worktree dirty; controlling sources uncommitted/untracked)
```

## Commission

Make the **thin architecture decision** for Source Capture packet schema evolution.
Three coupled questions:

1. **Validation-placement model** — where strict *current-schema* validation belongs:
   **(A)** every read-back (current: `SourceCapturePacket.model_validate` on every load,
   e.g. `source_quality.py`), **(B)** an **admission/consume gate** (validate strictly
   only when a packet is promoted to a consumer — fixture admission / ECR handoff — and
   make read-back-for-inspection lenient), or **(C)** **version-aware read** (validate a
   packet against the schema its `manifest_version` declares).
2. **Version-evolution mechanism** — how persisted packets survive future breaking schema
   changes: version-dispatch + **upgrade-on-load** vs **clear-reject-with-message**; the
   versioning scheme (`_vN` vs semver vs separate write-version / read-compat-range);
   whether a version/compatibility registry is warranted yet.
3. **Build trigger** — when to *build* the chosen mechanism vs defer. Today only three
   scratch dry-run evidence packets predate the schema; there is **no live consumer** of an
   old packet. Name the concrete condition that should trigger the build.

**Binding constraint (NOT an open question — options must respect it):** persisted packets
are **write-once and hash-pinned** (each carries a `sha256`; packets are cited as evidence
with pinned hashes across review artifacts). No option may mutate a persisted packet in
place to fit a new schema — that breaks evidence integrity. In-place migration is already
rejected for this reason.

Output is a **non-executing architecture routing object**: the candidate models developed,
adversarial findings, a recommendation with decisive criteria, the chosen model at design
altitude, the build trigger, deferred implications, and the smallest complete next step.

## Authorization / boundary (read first)

- **Design-only, NON-EXECUTING.** No source, schema, code, or contract changes. Do not
  build the version-aware read / admission gate; the pass DECIDES the model + build trigger.
- **R2 is settled — do not reopen it.** The closed posture vocabularies, `hash_basis`, and
  the `manifest_version` bump `v0 → v1` are landed and settled (see the obligation contract's
  R2 closure note). This pass is about the *evolution structure around* the schema, not the
  R2 vocab/field decisions.
- **JSG-01 stays FROZEN.** Do not bind, unfreeze, or treat postures as enforced downstream.
- **The fixture-admission frontier is its own lane** (currently blocked by AC-10 — no named
  consumer). Option B touches it; coordinate with it, do **not** absorb or decide it here.
- **`access_posture` stays open (Ob.11).** Do not close it.
- **Build-trigger and any "build now" call are OWNER-RESERVED.** The lane recommends a
  trigger condition; it does not authorize the build.
- No `jb` import; `agent-workflow` is reusable mechanics only.

## Preflight (orca_start_preflight)

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: docs-write   # the architecture PLAN only; read-only for all source/code
  target_scope: [the packet schema-evolution architecture plan artifact under docs/ or chat]
  dirty_state_checked: required_yes
  blocked_if_missing: yes
external_source_boundary: agent-workflow reusable mechanics only; jb is NOT Orca authority.
```

## Source pack / required reads

- **Current schema + version field:** `orca-harness/source_capture/models.py` (SHA256
  `3B89A19B…7245`) — `SourceCapturePacket` (note `manifest_version`, `obligation_contract_version`),
  `PreservedFile.hash_basis`, the closed-vocab validators, `SOURCE_CAPTURE_MANIFEST_VERSION`.
  Confirm the hash; on drift, report and review current content.
- **The read-back call sites (where validation fires today):** `orca-harness/source_capture/source_quality.py`
  (`SourceCapturePacket.model_validate` on read), and any other `model_validate` of a packet.
- **The writer (where versions are stamped):** `orca-harness/source_capture/writer.py`.
- **R2 closure + doctrine:** `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
  (the "R2 closure note" + the Direction Change Propagation receipts) and
  `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`.
- **The triggering finding:** `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_implementation_adversarial_review_v0.md` (R2-01/R2-02).
- **Layering + reserved ECR / admission boundary:** `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`.
- **The 3 pre-R2 evidence packets (the concrete old-version case):** `orca-harness/reports/source_capture/slot3_reddit_batch1_*/manifest.json` (carry `manifest_version: ..._v0`, no `hash_basis`, off-vocab `cutoff_posture`).

## Current state (design basis — verify against source, do not trust this summary)

```text
- Packets are persisted directories with a manifest.json validated by the Pydantic
  SourceCapturePacket model. Each manifest carries manifest_version (currently
  "source_capture_packet_manifest_v1") and obligation_contract_version.
- R2 made a BREAKING change (required PreservedFile.hash_basis; closed cutoff/archive/
  re_capture vocabularies) and bumped manifest_version v0 -> v1.
- Read-back today: source_quality.py calls SourceCapturePacket.model_validate(...) and
  validates against the CURRENT model, ignoring the packet's declared manifest_version.
  => a v0 packet raises a hard pydantic error on read.
- 3 pre-R2 v0 packets (slot3_reddit_batch1 dry-runs) exist on disk; they are scratch
  review evidence with NO live consumer, scoped out of the v1 schema (frozen evidence).
- Each PreservedFile carries a sha256; packets are hash-pinned as evidence in reviews.
- A fixture-admission frontier exists (promote scratch -> admitted/consumable) but is
  blocked by AC-10 (no named downstream consumer yet).
```

## Method sequence (Source-Gated Method Contract)

1. Read authority (`AGENTS.md`, overlay README, prompt-orchestration, source-of-truth).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-architecture-planning`. Do **not** APPLY yet.
3. `SOURCE-LOAD` the pack; confirm the `models.py` anchor hash.
4. Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE`.
5. APPLY deep-thinking to frame failure modes, then architecture-planning to compare options and name the routing object.

## Subagents — 3 standard (general-purpose), explicitly authorized

Each subagent receives this source pack, runs its own source-readiness gate, does
**source-backed** option work, applies no method before `SOURCE_CONTEXT_READY`, and
discloses its approach. Subagents are advisory; the architecture lane synthesizes and owns
the routing object.

- **SA-1 — "Version-aware read" architect:** develop the model where read-back dispatches on
  `manifest_version` and validates against the declared version's schema. Design the
  version registry / migration-chain shape, the **upgrade-on-load vs clear-reject** decision,
  where the version-dispatch lives, what a future Nth version costs, the build trigger, pros/cons.
- **SA-2 — "Validation-at-admission" architect:** develop the model where strict current-schema
  validation moves to an **admission/consume gate** (fixture admission / ECR handoff) and
  read-back-for-inspection becomes **lenient** (parse + report conformance, never crash).
  Design the admission-gate boundary, what a lenient read returns, how it interacts with the
  AC-10 fixture-admission frontier, the build trigger, pros/cons.
- **SA-3 — Adversary / integrator:** attack both — does version-aware read re-introduce an
  unbounded migration-maintenance burden (mutation-by-proxy)? does validation-at-admission
  leave a consumer reading a malformed packet? is the write-once/hash-pin invariant truly
  preserved in each? robustness across N future breaking versions; the "version-string honesty"
  failure mode; whether a **hybrid** (lenient version-aware read + strict admission gate +
  bump-on-breaking-change) is the real answer. Propose the smallest-complete synthesis, the
  build trigger, and the next routing object.

The lane synthesizes SA-1..SA-3. The build-trigger and any "build now" call are **surfaced for
the owner, not decided by the lane.**

## Output (non-executing architecture routing object)

- Each candidate model developed (validation placement; version-evolution mechanism; how it
  honors write-once/hash-pin; pros/cons), cited to source.
- Adversarial findings on each.
- Recommendation with **decisive criteria** (author's prior, NOT binding: a hybrid — lenient
  version-aware read + strict validation at an admission/consume gate + bump-on-breaking-change
  + write-once invariant — with the upgrade/reject machinery **deferred**; the lane judges and
  may differ).
- The chosen model at **design altitude**: where validation fires, how a read encounters an
  off-version packet, the versioning scheme, and whether a version/compat registry is needed yet.
- The **build trigger**: the concrete condition (e.g., first live consumer-bound old packet;
  2nd breaking amendment) that should move this from deferred to built.
- Deferred implications + the **smallest complete next routing object**.
- Explicit note: build authorization and the fixture-admission frontier are owner-reserved /
  separate-lane.

Output mode: `file-write` the plan to `docs/` (or `chat-only`). **No** source, code, schema, or
contract change. Do not execute implementation.

## Quality gates (must be able to fail)

- Each model developed against the current schema + read-back call sites, with cited inputs.
- The write-once/hash-pin invariant is shown to hold under each model (no in-place packet mutation).
- R2 not reopened; JSG-01 not unfrozen; `access_posture` not closed; the fixture-admission
  frontier coordinated-with, not decided.
- A build trigger is named (the pass must not silently imply "build now" or "never").
- Delta-robustness: behavior across at least two future breaking versions is reasoned, not just v0→v1.

## Non-claims

Architecture-planning / design only. Not implementation, not validation, not ratification, not a
build authorization, not JSG-01 unfreeze, not the fixture-admission decision, not an R2 reopen.
The current state is a design basis, not a commitment to keep it.
```
