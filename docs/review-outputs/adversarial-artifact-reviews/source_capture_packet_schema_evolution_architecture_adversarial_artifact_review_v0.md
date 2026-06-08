# Source Capture Packet Schema Evolution Architecture - Adversarial Artifact Review v0

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/source_capture_packet_schema_evolution_architecture_adversarial_artifact_review_v0.md
  recommendation: sound_with_friction
  summary: "The routing object's hybrid recommendation is sound as owner decision input, but its Phase 1 version/shape-mismatch language overpromises what can be detected without the deferred per-version machinery."
  findings_count: 2
  blocking_findings: []
  advisory_findings:
    - AR-01: Phase 1 overpromises claim_shape_mismatch detection while deferring per-version schemas.
    - AR-02: Bump-on-breaking-change wording risks reading as adopted doctrine before owner adoption.
  prior_findings_remediated: []
  next_action: "Owner may use the routing object for adopt/amend/reject, carrying AR-01 as an amendment condition if adopting the lenient-read slice."
```

## Commission

Adversarially review
`docs/product/source_capture_packet_schema_evolution_architecture_v0.md` as a
non-executing architecture routing object. The review object is whether it is a
sound, honest decision input for the owner adopt / amend / reject decision, not
whether an unbuilt mechanism is implemented correctly.

## Target

Reviewed target:
`docs/product/source_capture_packet_schema_evolution_architecture_v0.md`.

The target recommends a hybrid: strict validation stays at write, inspection
read-back becomes lenient and honest, strict admission/consume is deferred to a
named downstream consumer, and `manifest_version` becomes read-time reporting
input without building full per-version dispatch.

## Authority

- `AGENTS.md`: smallest complete intervention, real failure visibility, no fake
  success paths, verification for non-trivial changes.
- `.agents/workflow-overlay/README.md`: Orca overlay controls project facts.
- `.agents/workflow-overlay/review-lanes.md`: adversarial artifact review is
  read-only; reports may be written under
  `docs/review-outputs/adversarial-artifact-reviews/`; `critical | major |
  minor` are finding-priority labels only.
- `.agents/workflow-overlay/prompt-orchestration.md`: source-gated method
  contract and `review-report` output mode.
- `.agents/workflow-overlay/source-of-truth.md`: doctrine-change propagation
  applies when a source-changing edit changes durable doctrine.
- `.agents/workflow-overlay/retrieval-metadata.md`,
  `.agents/workflow-overlay/artifact-folders.md`, and
  `.agents/workflow-overlay/artifact-roles.md`: report destination, retrieval
  header, and role hygiene.

Reviewer runtime disclosure: Codex / GPT-5. The author and advisory subagents
were disclosed as Claude-family, so the cross-family review bar is met.

## Source Readiness

`SOURCE_CONTEXT_READY`.

Method sequence followed:

1. Read authority: `AGENTS.md`, overlay `README.md`, `review-lanes.md`,
   `prompt-orchestration.md`, `source-of-truth.md`, `source-loading.md`,
   `validation-gates.md`, `retrieval-metadata.md`, `artifact-folders.md`,
   `artifact-roles.md`, and `communication-style.md`.
2. `REFERENCE-LOAD`ed `workflow-deep-thinking`, then
   `workflow-adversarial-artifact-review`. Neither method was applied before
   source readiness.
3. `SOURCE-LOAD`ed the prompt read-pack and claim-verification sources.
4. Confirmed both anchor hashes.
5. Applied deep-thinking to the failure-mode frame, then applied adversarial
   artifact review to produce findings.

Anchor hashes:

- `docs/product/source_capture_packet_schema_evolution_architecture_v0.md`:
  confirmed
  `8FDD1FDA745B87AE790C628CA4C74C2E7E7EF0B8A4877F471C8857F2C71AE7E9`.
- `orca-harness/source_capture/models.py`: confirmed
  `3B89A19BAEAB90762C34FE0C95517A005D383933E48057C1ADD12E004A3A7245`.

Dirty-state boundary:

- `git status --short --branch` showed `main...origin/main [ahead 7]` with
  many modified and untracked Orca files, including controlling overlay/docs,
  source-capture code, untracked target prompt/artifact, untracked
  `packet_assembly.py`, and untracked reports.
- This report is advisory decision input only. It is not approval, validation,
  readiness, acceptance, ratification, build authorization, patch authority, or
  source-of-truth promotion.

Source-read ledger:

| Source | Why read | Status |
| --- | --- | --- |
| `docs/prompts/reviews/source_capture_packet_schema_evolution_architecture_adversarial_artifact_review_prompt_v0.md` | Commission, read-pack, decision criteria, output contract | untracked |
| `docs/product/source_capture_packet_schema_evolution_architecture_v0.md` | Review target | untracked; hash matched |
| `docs/prompts/architecture/source_capture_packet_schema_evolution_architecture_prompt_v0.md` | Original commission and quality gates | untracked |
| `orca-harness/source_capture/models.py` | Current schema, validators, `manifest_version`, hash basis | modified; hash matched |
| `orca-harness/schemas/case_models.py` | `StrictModel` / Pydantic `extra="forbid"` | tracked status not separately clean-claimed |
| `orca-harness/source_capture/source_quality.py` | production read-back and census try/except | modified |
| `orca-harness/source_capture/writer.py` | write-time strict gate and `hash_basis` producer | modified |
| `orca-harness/source_capture/packet_assembly.py` | untracked helper construction/persistence path | untracked |
| `orca-harness/runners/run_source_capture_*` | runner construction/persistence scan | modified/untracked mix by git status |
| `orca-harness/reports/source_capture/slot3_reddit_batch1_*/manifest.json` | v0 packet reality check | untracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | R2 closure and non-claims | modified |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | ECR/Cleaning boundary | modified |
| `docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md` | AC-10 downstream-consumer boundary | untracked |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_implementation_adversarial_review_v0.md` | Triggering R2 finding and v0 packet evidence | untracked |

Source checks run:

- Whole-repo `rg` search for `SourceCapturePacket`, `model_validate`,
  `manifest.json`, `manifest_version`, `hash_basis`,
  `write_local_source_capture_packet`, `stage_and_write_packet`, and
  `packet_assembly`.
- Focused production search over `orca-harness/source_capture` and
  `orca-harness/runners` for `SourceCapturePacket.model_validate`,
  `model_validate(json.loads`, `manifest_path.read_text`, and `manifest.json`.
- Focused persistence search over `orca-harness/source_capture` and
  `orca-harness/runners` for `write_local_source_capture_packet`,
  `stage_and_write_packet`, direct manifest writes, and packet construction.
- Pydantic v2 strictness probe confirming removed fields fail as
  `extra_forbidden` and added required fields fail as `missing`.
- Structured read-back of the three v0 manifests through
  `SourceCapturePacket.model_validate`; all three fail current strict schema, as
  expected for v0 scoped-out evidence.

## Decision Criteria

The review applied the prompt's attack seams:

- whether `source_quality.py:99` is truly the single production read-back;
- whether all production persistence goes through the write-time strict gate;
- whether the `extra="forbid"` bidirectional-skew argument is technically true;
- whether Phase 1's version-aware reporting smuggles in deferred per-version
  machinery;
- whether replacing a loud crash with a conformance report creates fake
  success risk;
- whether `TARGET_RECOMMENDED` is earned despite deferral;
- whether the artifact soft-authorizes build or fixture admission;
- whether convergence among same-family advisory subagents was overused as
  proof;
- whether doctrine-propagation treatment is honest;
- whether retrieval-header and dirty-state hygiene hold.

## Findings

### AR-01 - Phase 1 overpromises claim_shape_mismatch detection while deferring per-version schemas

- id: AR-01
- severity: major
- seam: internal consistency / version-aware reporting / deferred machinery
- phase: correctness

Evidence:

- The target says Phase 1 is eligible now, with no AC-10 dependency, one
  production site at `source_quality.py:99`, no packet mutation, and the three
  v0 packets as regression corpus
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:230`).
- The target's lenient read report includes `claim_shape_mismatch` and says it
  is typed so it cannot be mistaken for a validated `SourceCapturePacket`
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:291`).
- The target then says the recommended read will "cross-check the declared
  version against shape" while not crashing, dispatching, or upgrading
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:303`).
- The same target defers per-version models, dispatch, and adapters until a real
  off-version consumer exists
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:306`,
  `docs/product/source_capture_packet_schema_evolution_architecture_v0.md:383`).
- In current source, `manifest_version` is an unchecked free `str`
  (`orca-harness/source_capture/models.py:160`), with the current version
  constant at `source_capture_packet_manifest_v1`
  (`orca-harness/source_capture/models.py:12`).
- There is no frozen v0 model or version registry in the reviewed source pack;
  `packet_assembly.py` delegates staging and writing to the current writer, not
  historical read dispatch (`orca-harness/source_capture/packet_assembly.py:95`,
  `orca-harness/source_capture/packet_assembly.py:140`).

Why this matters:

The core recommendation does not need full dispatch, and that part is sound.
But the target's Phase 1 language implies it can detect a declared-version /
actual-shape mismatch as an integrity signal while explicitly deferring the
schema knowledge needed to judge historical or future version shapes. Without
per-version schemas, Phase 1 can honestly report only current-schema
conformance and declared-version facts such as "declares non-current" or
"declares current but fails current shape." It cannot generally know whether a
packet declaring `v0` actually conforms to v0, or whether a future off-version
packet conforms to its declared shape.

That distinction matters because `claim_shape_mismatch` is presented as the
"sharpest" version-string honesty signal. If the owner adopts the routing object
as written, a later implementation-scoping lane could treat that signal as
required in Phase 1 and either smuggle in the deferred per-version registry or
fake the signal from incomplete evidence.

minimum_closure_condition:

The routing object must bound Phase 1 version-aware reporting to what is
knowable without deferred per-version schemas, or explicitly move
`claim_shape_mismatch` into the deferred per-version/registry satellite. The
owner-facing decision input should distinguish current-schema conformance
reporting from declared-version shape validation.

next_authorized_action:

Owner may still use the routing object for adopt / amend / reject. If adopting,
accept it with an amendment condition that Phase 1 does not promise general
declared-version shape validation unless the per-version machinery is separately
authorized.

### AR-02 - Bump-on-breaking-change wording risks reading as adopted doctrine before owner adoption

- id: AR-02
- severity: minor
- seam: doctrine-propagation hygiene / non-binding boundary
- phase: friction

Evidence:

- The target's status says it is planning-only, non-executing, asserts no
  binding rule, authorizes no build, and leaves adoption/build authorization to
  owner decision
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:41`).
- The start preflight says doctrine propagation is expected to be none because
  the artifact asserts no binding rule, and owner adoption/build authorization
  would carry the receipt
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:62`).
- The target also lists "standing invariants" in the recommended core,
  including write-once + hash-pin and `bump-on-breaking-change` of
  `SOURCE_CAPTURE_MANIFEST_VERSION`
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:130`).
- Later it calls bump-on-breaking-change a "Standing discipline" and says it is
  "free" and should be adopted as doctrine when the owner accepts
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:222`).
- Its doctrine-propagation section correctly says owner adoption of the target
  architecture or build authorization must carry a DCP receipt
  (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:491`).
- Orca's source-of-truth rule says doctrine-changing work is a source-changing
  edit that changes a durable rule future agents may follow
  (`.agents/workflow-overlay/source-of-truth.md:32`), and requires updating the
  controlling source plus downstream surfaces before claiming completion
  (`.agents/workflow-overlay/source-of-truth.md:60`).

Why this matters:

This is not a blocker because the artifact repeatedly says owner adoption is
required before doctrine changes, and the DCP deferral is mostly honest. The
friction is that "standing invariants" mixes already-binding evidence integrity
(write-once/hash-pin) with a proposed future discipline
(`bump-on-breaking-change`). That phrasing can be misread by a later agent as
current doctrine rather than recommended doctrine.

minimum_closure_condition:

Before owner adoption or downstream implementation scoping, the artifact or
owner decision should separate already-binding invariants from proposed
owner-adopted invariants, and any owner adoption of bump-on-breaking-change as a
durable rule must carry the required DCP receipt.

next_authorized_action:

No patch is authorized by this review. If the owner adopts the routing object,
carry this as wording hygiene in the owner decision or a bounded amendment to
the routing object.

## Non-Findings

### NF-01 - The single production read-back claim holds under whole-repo search

The focused production search found the only production
`SourceCapturePacket.model_validate(json.loads(...manifest...))` at
`source_quality.py:99`
(`orca-harness/source_capture/source_quality.py:99`). The source-quality census
path wraps the helper in try/except and degrades to `manifest_uninspectable`
with visible stops
(`orca-harness/source_capture/source_quality.py:509`,
`orca-harness/source_capture/source_quality.py:519`).

The whole-repo search surfaced tests, docs, historical review outputs, and
manifest reads in tests, but no second production reader of a persisted Source
Capture packet. The target's own caveat that readers outside `orca-harness`
were not enumerated
(`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:431`)
is now closed by this review's broader search for the current worktree state.

### NF-02 - Write-time strict validation is the production correctness home for new packets

`writer.py` constructs a `SourceCapturePacket` before writing the manifest
(`orca-harness/source_capture/writer.py:132`) and writes the dumped model only
after construction succeeds (`orca-harness/source_capture/writer.py:167`).
The writer stamps the current manifest version
(`orca-harness/source_capture/writer.py:134`) and produces
`hash_basis="raw_stored_bytes"` from copied bytes
(`orca-harness/source_capture/writer.py:253`,
`orca-harness/source_capture/writer.py:267`).

All reviewed production runner persistence paths call either
`write_local_source_capture_packet` directly or `stage_and_write_packet`, which
then calls `write_local_source_capture_packet`:

- archive runner:
  `orca-harness/runners/run_source_capture_archive_packet.py:186`;
- direct HTTP runner:
  `orca-harness/runners/run_source_capture_http_packet.py:112`;
- media runner:
  `orca-harness/runners/run_source_capture_media_packet.py:180`;
- local packet runner:
  `orca-harness/runners/run_source_capture_packet.py:81`;
- browser runner:
  `orca-harness/runners/run_source_capture_browser_packet.py:136`;
- authenticated browser runner:
  `orca-harness/runners/run_source_capture_authenticated_browser_packet.py:169`;
- shared helper:
  `orca-harness/source_capture/packet_assembly.py:140`.

The three current v0 manifests under `orca-harness/reports/source_capture/` do
not satisfy current strict validation, but the target treats them as scoped-out,
hash-pinned v0 evidence rather than new-write correctness examples. Structured
read-back in this review confirmed all three fail current strict validation:
one on missing `hash_basis`, two on off-vocabulary cutoff posture plus missing
`hash_basis`.

### NF-03 - The `extra="forbid"` bidirectional-skew claim holds

`StrictModel` sets `ConfigDict(extra="forbid", populate_by_name=True)`
(`orca-harness/schemas/case_models.py:10`). `SourceCapturePacket` inherits
`StrictModel` (`orca-harness/source_capture/models.py:160`).

A direct Pydantic v2 probe confirmed the target's claim: when an old packet has
a field removed from the future model, validation fails as `extra_forbidden`;
when a future model adds a required field, the old packet fails as `missing`.
This supports the target's rejection of "strict current schema on every read" as
the long-term read-back model.

### NF-04 - Fake-success risk is acknowledged at the right boundary

The target explicitly requires the lenient reader to return a different
conformance-report type, not a validated `SourceCapturePacket`, when a packet is
non-conforming
(`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:291`).
It also states the admission/consume gate must use the strict path rather than
the lenient one
(`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:373`).

That is adequate at architecture altitude. AR-01 only limits what one field in
that report can honestly mean without deferred schemas; it does not reject the
report-type guard.

### NF-05 - The owner/build/AC-10 boundaries mostly hold

The original commission requires a non-executing routing object and says build
trigger and "build now" calls are owner-reserved
(`docs/prompts/architecture/source_capture_packet_schema_evolution_architecture_prompt_v0.md:51`,
`docs/prompts/architecture/source_capture_packet_schema_evolution_architecture_prompt_v0.md:67`).
The target repeats that it authorizes no build and admits no packet
(`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:41`).

AC-10 requires a named downstream consumer before fixture admission
(`docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md:119`),
and the criteria proposal says no unit is admissible today because every unit is
blocked at least by AC-10
(`docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md:157`).
The target correctly defers the strict admission/consume gate to AC-10
resolution
(`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:235`)
and says Phase 1 remains owner-gated.

### NF-06 - Retrieval-header and dirty-state hygiene are acceptable

The target has the required retrieval header fields with
`authority_boundary: retrieval_only`, uses `input_hashes` for safety-critical
source provenance, and does not put approval, validation, readiness, or build
authorization in the header
(`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:3`).

The broad dirty worktree is disclosed in the target preflight
(`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:59`)
and in this review. This prevents strict readiness, acceptance, validation,
ratification, or PASS claims, but it does not block advisory review.

## Not-Proven Boundaries

- This review did not run the repository test suite. It ran source-search
  checks, hash checks, a Pydantic strictness probe, and a structured manifest
  read-back check only.
- Whole-repo search is bounded to the current worktree. Untracked and modified
  sources may change before any later implementation scoping or owner decision.
- The "single production read-back" non-finding is source-search evidence, not
  a future-proof guarantee. New runners, docs-promoted scripts, or external
  consumers would need a fresh search.
- The report-type fake-success guard is judged at architecture altitude only.
  It is not proof that a later implementation cannot accidentally return a
  dict or object that a caller treats as validated.
- The owner adoption decision, build authorization, fixture-admission frontier,
  JSG-01 state, and ECR/consume semantics remain owner-reserved or separate-lane.

## Optional Hardening

Optional, non-required: if the owner adopts the architecture, name the Phase 1
report fields in owner-decision language as:

- `declared_manifest_version`;
- `declares_current_manifest_version`;
- `conforms_to_current_schema`;
- `current_schema_errors`;
- `declared_version_shape_validation: not_available_without_per_version_schema`
  for non-current declared versions.

That would preserve the recommended hybrid while preventing
`claim_shape_mismatch` from becoming an overpromised integrity result.

## Recommendation

`sound_with_friction`.

The routing object's central decision input is sound: strict every-read is the
wrong long-term model under `extra="forbid"`; new-write strictness is currently
centralized at the writer; the single production read-back site exists; and
AC-10 correctly gates admission/consume machinery rather than the inspection
read fix.

The owner should not adopt the artifact verbatim as implementation-scoping
input until AR-01 is carried as an amendment: Phase 1 can be version-aware in
the sense of reading and reporting the declared version and current-schema
conformance, but it cannot generally validate declared-version shape without
the deferred per-version machinery.

## Review-Use Boundary

These findings are decision input for the owner only. They are not approval,
validation, acceptance, ratification, adoption, build authorization, mandatory
remediation, executor-ready patch authority, fixture admission, JSG-01 unfreeze,
or ECR/Cleaning/Judgment design.
