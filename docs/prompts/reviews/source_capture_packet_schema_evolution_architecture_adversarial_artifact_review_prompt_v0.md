# Source Capture Packet Schema Evolution Architecture — Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial review of the NON-EXECUTING architecture routing object
  for Source Capture packet schema evolution + validation placement
  (docs/product/source_capture_packet_schema_evolution_architecture_v0.md). The
  review object is the routing object's decision soundness, claim honesty,
  internal consistency, scope/altitude discipline, and boundary compliance — NOT
  the correctness of an (unbuilt) mechanism. Run before the owner relies on this
  routing object for the adopt / amend / reject decision.
use_when:
  - Dispatching the independent adversarial review of the packet schema-evolution architecture routing object.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md
  - docs/prompts/architecture/source_capture_packet_schema_evolution_architecture_prompt_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  docs/product/source_capture_packet_schema_evolution_architecture_v0.md: 8FDD1FDA745B87AE790C628CA4C74C2E7E7EF0B8A4877F471C8857F2C71AE7E9
  orca-harness/source_capture/models.py: 3B89A19BAEAB90762C34FE0C95517A005D383933E48057C1ADD12E004A3A7245
branch_or_commit: main @ d69aeee (worktree dirty; the target artifact and the controlling sources below are uncommitted/untracked)
```

## Commission

Adversarially review the **architecture routing object**
`docs/product/source_capture_packet_schema_evolution_architecture_v0.md`. Decide
whether it is a **sound, honest decision input** the owner can rely on for the
adopt / amend / reject decision it routes to — and surface every material
decision-relevant failure mode first. Read-only, findings-first, advisory.

This review does **not** adopt, accept, ratify, authorize a build, unfreeze
JSG-01, decide the fixture-admission frontier, or commit anything. A clean
result is what lets the owner treat the routing object as trustworthy decision
input; it is not itself adoption or build authorization (both owner-reserved).

## Review object and altitude (commission-bound; do not retarget)

The review **object** is a **non-executing, non-binding architecture planning
recommendation** (a routing object). Review it as such:

- **In scope:** is the recommendation sound; are its load-bearing claims true;
  is it internally consistent; does it answer its commission's three coupled
  questions at decision altitude; does it stay non-executing, non-binding, and
  inside its declared boundaries; are its `file:line` citations accurate; does it
  honor the Agent Behavior Kernel (real failure visibility, no fake-success
  paths, smallest complete intervention, claims traceable)?
- **Out of scope (do NOT retarget):** this is **not** a code review and **not**
  an implementation review of the (unbuilt) lenient-read mechanism. Do not
  demand the artifact build anything, do not score code quality, and do not
  re-open R2, JSG-01, `access_posture` (Ob.11), or the fixture-admission
  decision. Read source code/docs **only** to verify or refute the routing
  object's load-bearing claims.

The author runtime was **Claude (Opus 4.8)**, and the routing object's three
advisory subagents (SA-1/SA-2/SA-3) were **also Claude-family**. Independence is
therefore the point of this lane: anchoring on the author's framing is the exact
blind spot to avoid.

## Operator precondition (owner-set independence bar, NOT prompt-routed runtime model choice)

To satisfy the independent-review bar, dispatch to a reviewer that did **not**
author this artifact, preferably in a **different model family** from the author
(Claude). A same-author or same-family review is the tester-testee blind spot
this lane exists to avoid. Disclose the reviewer runtime and self-certify
whether the cross-family bar is **met** or **not met**. This prompt is
model-neutral: it states author provenance and asks for independence; it does
not select, rank, recommend, or require any runtime model.

## Reviewer start state

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: read-only
  target_scope:
    - docs/product/source_capture_packet_schema_evolution_architecture_v0.md
  dirty_state_checked: required_yes
  blocked_if_missing: yes
controlling_source_state: untracked/dirty; advisory review only; no strict PASS / readiness / acceptance / ratification claims.
edit_permission: read-only
output_mode: review-report
external_source_boundary: agent-workflow is read-only reusable mechanics; jb is NOT Orca authority.
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
```

## Required read-pack

**Primary target (the review object):**

- `docs/product/source_capture_packet_schema_evolution_architecture_v0.md`
  (confirm `input_hash` `8FDD1FDA…E7E9`).

**Claim-verification sources (read to verify/refute the artifact's load-bearing
claims — not as a code review):**

- `orca-harness/source_capture/models.py` (confirm `input_hash` `3B89A19B…7245`):
  `SourceCapturePacket`, the `manifest_version: str` field (claimed unchecked),
  `SOURCE_CAPTURE_MANIFEST_VERSION`, the closed-vocab + `hash_basis` validators.
- `orca-harness/schemas/case_models.py`: `StrictModel` / `extra="forbid"` (the
  artifact's bidirectional-skew claim depends on this).
- `orca-harness/source_capture/source_quality.py`: the claimed **sole**
  production read-back at `:99` and the census try/except at `:509-525`.
- `orca-harness/source_capture/writer.py`: the claimed write-time strict gate at
  `:132` and `hash_basis` producer at `:266-267`.
- `orca-harness/source_capture/packet_assembly.py` (untracked) **and** the
  runners under `orca-harness/runners/run_source_capture_*` : independently
  check whether any OTHER path reads back or constructs/persists a packet — the
  "single read-back site" and "write is the standing correctness home" claims
  rise or fall here.
- The three on-disk v0 packets under
  `orca-harness/reports/source_capture/slot3_reddit_batch1_*/manifest.json`.

**Boundary / commission sources:**

- `docs/prompts/architecture/source_capture_packet_schema_evolution_architecture_prompt_v0.md`
  — the commission. Check the routing object answered all three coupled
  questions and honored every authorization boundary and quality gate the
  commission set (it must be able to fail this).
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
  (R2 closure note), `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  (reserved ECR/consume boundary),
  `docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md`
  (AC-10).
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_implementation_adversarial_review_v0.md`
  — the triggering finding / what is already settled.

**Authority:** `AGENTS.md`, `.agents/workflow-overlay/README.md`,
`review-lanes.md`, `prompt-orchestration.md`, `source-of-truth.md`,
`retrieval-metadata.md`, `artifact-folders.md`, `artifact-roles.md`.

Confirm the two `input_hashes`. If either differs, that anchor changed since this
prompt was written — **report it as drift, review the current content, and note
the delta** (especially: if `models.py` drifted, the artifact's technical claims
must be re-checked against the new content).

## Method sequence (Source-Gated Method Contract)

1. Read authority (`AGENTS.md`, overlay README, review-lanes, prompt-orchestration).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-adversarial-artifact-review`. Do **not** APPLY yet.
3. `SOURCE-LOAD` the read-pack; confirm the two anchor hashes.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` (name gaps/conflicts/excluded sources).
5. Only then APPLY deep-thinking to frame the failure modes, then
   adversarial-artifact-review to produce findings, each cited to `file:line`.

If `workflow-adversarial-artifact-review` is unavailable / not applied, return a
blocked or advisory-only result and emit **no** formal verdict, severity
authority, readiness, or validation claim — name the missing skill invocation.

## Decision criteria — attack these seams (be maximally adversarial; add others you find)

1. **"Single production read-back site" (load-bearing).** The artifact's
   "Phase 1 = one site, light, low-risk" claim and its core/satellite split rest
   on `source_quality.py:99` being the **only** production read-back of a
   persisted packet. Independently search the **whole repo** (not just
   `orca-harness`), including `packet_assembly.py` and every runner, for other
   packet `model_validate` / manifest-read paths. If another reader exists, what
   does it do to the "light/one-site" claim and the boundary?
2. **"Strict validation stays at write" (load-bearing).** The artifact names
   write-time model construction (`writer.py:132`) as the standing correctness
   home. Is there any packet-construction/persistence path — another runner,
   `packet_assembly.py`, a helper, or a hand-authored manifest — that can persist
   a packet **without** full model validation? If so, "write is the standing
   correctness home" is overclaimed; say so and bound the gap.
3. **`extra="forbid"` bidirectional-skew claim (technical correctness).** Verify
   against `case_models.py` + Pydantic v2 semantics that (a) a future **removed**
   field makes an OLD packet fail because the surviving key is now forbidden, and
   (b) a new **required** field also fails an old packet. The artifact rejects
   Option A and builds its delta-robustness on this. If the claim is wrong or
   overstated, a load-bearing argument collapses.
4. **Internal contradiction — does the recommended read need the deferred
   machinery?** The artifact (a) defers per-version models / version *dispatch*,
   yet (b) recommends the read detect `claim_shape_mismatch` (declared version ≠
   actual shape) and be "version-aware." Does detecting claim/shape mismatch
   require per-version schema knowledge the artifact claims to defer — or is it
   cheap (only current-shape + the declared string)? Is the artifact clear and
   consistent about exactly what Phase 1 needs, or does "version-aware reporting"
   smuggle in the deferred dispatch?
5. **Fake-success / failure-visibility (Agent Behavior Kernel).** Today a v0
   packet causes a **loud crash** at `:99`. The artifact recommends replacing
   that with a non-crashing conformance report. Is this a net **loss** of failure
   visibility for any current consumer? Does the proposed "return a type that
   cannot be mistaken for a validated packet" guard actually neutralize the
   fake-success risk, or is it asserted without a mechanism that could honor it?
   Does "never crash" risk tolerating genuine corruption (vs merely old-but-honest)?
6. **`TARGET_RECOMMENDED` honesty vs `OPTIONS_COMPARED_NO_SELECTION`.** Given how
   much is deferred (Phase 2, dispatch, upgrade/reject, registry, the admission
   gate), is "TARGET_RECOMMENDED" earned, or does it overclaim a selection that
   is mostly deferral? Test the artifact's own minimum selection threshold —
   especially **"no unresolved upstream blocker."** AC-10 is unresolved; the
   artifact argues AC-10 gates only the satellite, not the lenient-read core. Is
   that partition airtight, or does the lenient-read core also depend on a
   consumer/owner decision?
7. **Boundary discipline / soft pre-authorization.** Does the artifact stay
   non-executing, non-binding, design-altitude (no code, no `STEP-*`, no patch)?
   Does the "Phase 1 eligible now" framing plus the named implementation-scoping
   object **soft-cross** the owner-reserved build line — pressuring or
   pre-authorizing the build — even though it is labeled owner-gated? Did it
   actually coordinate-with rather than **decide** the fixture-admission frontier?
8. **Convergence-as-proof / citation accuracy.** All three subagents were
   Claude-family. Did the synthesis treat lane agreement as proof, or carry any
   subagent claim as fact without independent grounding? Spot-check a sample of
   the artifact's `file:line` citations for accuracy. Was the one adjudicated
   divergence (reject-vs-lenient read posture) resolved on stated criteria, or
   asserted?
9. **Doctrine-propagation treatment.** The artifact claims it carries **no**
   `direction_change_propagation` receipt because it "asserts no binding rule."
   Test this: do any statements (e.g., "bump-on-breaking-change as standing
   discipline"; "the only place a packet must satisfy the current strict schema
   is write + admission gate") function as durable doctrine despite the
   non-binding label? If it reads as doctrine, the missing DCP receipt (or a
   blocker) is a defect per `source-of-truth.md`.
10. **Retrieval-header / not-proven hygiene.** Is the header `retrieval_only`
    with no forbidden authority/validation/readiness fields and justified
    triggered fields (`artifact-roles.md`, `retrieval-metadata.md`)? Given the
    dirty worktree, does any phrasing overclaim settledness, acceptance, or
    readiness?

## Output contract

- `review-report` mode. Write the durable report to
  `docs/review-outputs/adversarial-artifact-reviews/source_capture_packet_schema_evolution_architecture_adversarial_artifact_review_v0.md`.
- Start the report with the compact `review_summary` YAML, then findings. Use
  this **prompt-specific recommendation vocabulary** (rates the routing object's
  soundness as decision input only — it is **not** a build/adopt approval, which
  is owner-reserved, and not validation/readiness):
  `recommendation: sound_for_owner_decision | sound_with_friction | revise_before_owner_decision | unsound | blocked`.
- Findings-first: `id`, `severity` (`critical | major | minor` — finding
  priority only, no approval/rejection authority), `seam`, `file:line` evidence,
  `minimum_closure_condition` (required end state, not how-to), and
  `next_authorized_action` (what this review authority allows next).
- Include **non-findings** (seams that held, with evidence) and **not-proven
  boundaries** (e.g., readers not enumerated outside the searched scope; whether
  this review is cross-family if the reviewer is same-family as the author).
- **Advisory only.** No `patch_queue_entry`, no executor-ready how-to. Any
  optional hardening must be clearly labeled optional and non-required.
- Preserve the Chief Architect consumption order: commission → target →
  authority → decision criteria → evidence → reviewer recommendation.
- After the durable report writes successfully, return the compact
  `review_summary` YAML plus a short findings summary in chat. If the report
  write fails, return `status: failed`, `review_location: chat_only_current_thread`,
  `recommendation: blocked`, name the failed path, and give enough
  human-readable routing detail (do not use `report_path`).

## Validation gates (must be able to fail)

- Source readiness declared before findings; the routing object **and** the
  claim-verification sources actually read (or `SOURCE_CONTEXT_INCOMPLETE`).
- Both anchor hashes confirmed; drift → report + review current content + note delta.
- `workflow-adversarial-artifact-review` applied after `SOURCE_CONTEXT_READY`, or
  the run is blocked/advisory-only with the missing invocation named.
- Untracked/dirty sources → advisory only; no strict PASS / readiness /
  acceptance / ratification claim.
- At least the "single read-back site" (seam 1), "write is the correctness home"
  (seam 2), and `extra="forbid"` (seam 3) claims are checked **against source**,
  not accepted from the artifact's own text.
- Durable report written before any YAML-only chat summary; on write failure use
  the failed-blocked chat shape above.

## Review-use boundary

Findings are decision input for the owner only — not approval, validation,
acceptance, ratification, adoption, build authorization, mandatory remediation,
or patch authority. This review does not adopt the routing object, authorize any
build, decide the fixture-admission frontier (AC-10), or unfreeze JSG-01. A clean
result is what lets the owner trust the routing object as decision input; it is
not that decision. `agent-workflow` is read-only reusable mechanics; `jb` is not
Orca authority.
