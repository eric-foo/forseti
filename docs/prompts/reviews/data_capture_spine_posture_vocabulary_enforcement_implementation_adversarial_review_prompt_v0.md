# Data Capture Spine Posture Vocabulary Enforcement — Implementation + Doctrine Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial review of the IMPLEMENTED Data Capture Spine
  posture-vocabulary enforcement (R2): the closed-vocabulary schema enforcement,
  the cutoff_posture untangle, the archive-posture (Option b) and hash_basis
  representations, the migration of every posture-setting runner/test, AND the
  matching obligation-contract amendment (Ob.9/10/15). Run before this change is
  treated as "settled" and before the Data Capture lane ratifies it or JSG-01
  binds to it.
use_when:
  - Dispatching the independent 2nd-opinion review of the R2 implementation + doctrine amendment.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/contracts/obligation_contracts/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md: 806E7CE9DC92CFB57CDFFD62AA14091DC9EA2C29BD28D23B21AE138F69DF3ED4
  orca-harness/source_capture/models.py: 6506ACA56FA7B3768552F0F382DAEB474EA4D0EB5B238C3BA47108B159121E75
branch_or_commit: main @ e4e854e (worktree dirty; ALL controlling sources below are uncommitted/untracked)
```

## Commission

Adversarially review the **implemented** Data Capture Spine posture-vocabulary
enforcement (R2) **and** the obligation-contract amendment that was made to match
it. Decide whether the code + migration + doctrine are sound enough to be treated
as *settled* (i.e., for the Data Capture lane to ratify and for JSG-01 to later
bind against) — and surface every material failure mode first. Read-only,
findings-first, advisory. This review does **not** approve, execute, ratify,
commit, or unfreeze any gate, and does not by itself make the change "settled."

## What changed (commission-bound; do not retarget)

The author is **Claude** (same model family as this prompt's origin). The change set:

- **Enforcement core** — `orca-harness/source_capture/models.py`: closed-vocabulary
  constants (`CUTOFF_POSTURE_VALUES`, `ARCHIVE_HISTORY_POSTURE_VALUES`,
  `RE_CAPTURE_RELATIONSHIP_VALUES`, `HASH_BASIS_VALUES`), the `_require_closed_posture`
  helper, the `validate_closed_postures` model-validators on `PacketTiming` /
  `SourceCaptureSlice` / `SourceCapturePacket`, and the new `PreservedFile.hash_basis`
  field + `validate_hash_basis`.
- **cutoff untangle (AR-03)** — `orca-harness/source_capture/source_quality.py`:
  `_source_time` no longer falls back to `cutoff_posture`.
- **hash_basis producer (AR-04)** — `orca-harness/source_capture/writer.py`:
  `_copy_preserved_files` sets `hash_basis="raw_stored_bytes"`.
- **Archive migration (Option b, AR-05)** — `orca-harness/runners/run_source_capture_archive_packet.py`:
  `_archive_posture` / `_body_archive_posture` now emit `archived` / `attempt_failed`
  (or `not_applicable` status), detail moved to metadata + limitations.
- **Other migrated runners/tests** — `run_source_capture_http_packet.py`,
  `run_source_capture_media_packet.py`, and the unit tests
  `test_source_capture_packet.py`, `test_source_capture_archive_org.py`,
  `test_source_capture_direct_http.py`, `test_source_capture_media_asset.py`,
  `test_source_quality_state_assembler.py`, `test_source_quality_report_skeleton.py`.
- **Doctrine amendment (STEP-05)** — `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
  §9 (cutoff), §10 (archive), §15 (re-capture): vocabularies stated as closed /
  write-time-enforced; status line + source basis updated.

Confirm the two `input_hashes` above. If either differs, that anchor changed since
this prompt was written — **report it as drift, review the current content, and
note the delta**. The worktree is dirty and concurrent lanes may touch files;
treat the file list as the scope and review whatever is on disk.

## Operator precondition (owner-set, NOT prompt-routed)

To satisfy the independent-review bar, dispatch to a reviewer in a **different
model family** from the author (Claude). A same-family review is exactly the
tester-testee blind spot this gate exists to avoid; if the runtime is same-family,
say so and mark the cross-family bar **not met**. This prompt is model-neutral.

## Reviewer start state

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: read-only
  target_scope:
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - orca-harness/source_capture/models.py
    - orca-harness/source_capture/source_quality.py
    - orca-harness/source_capture/writer.py
    - orca-harness/runners/run_source_capture_archive_packet.py
  dirty_state_checked: required_yes
  blocked_if_missing: yes
controlling_source_state: untracked/dirty; advisory review only; no strict PASS/readiness/ratification claims.
edit_permission: read-only
output_mode: review-report
external_source_boundary: agent-workflow is read-only reusable mechanics; jb is NOT Orca authority.
```

## Required read-pack — INCLUDES the implemented code, tests, and existing packets

A prior review missed a real collision because its read-pack excluded the
implemented capture code. Do not repeat that. Read the code, its tests, and the
actual packet outputs — not just the doctrine docs:

- **Doctrine (vocabulary source of truth, now amended):** the obligation contract
  above — §9, §10, §11 (visibility), §15. The closed sets in `models.py` must match
  §9/§10/§15 **exactly**; verify both directions (no code value missing from doctrine; no doctrine value missing from code).
- **Enforcement + schema:** `orca-harness/source_capture/models.py` (constants, helper,
  validators, `PreservedFile.hash_basis`), `writer.py`, `source_quality.py`,
  `packet_assembly.py`.
- **Migration reality — runners:** `run_source_capture_archive_packet.py`,
  `run_source_capture_http_packet.py`, `run_source_capture_media_packet.py`, and any
  other runner that constructs a packet/posture.
- **Migration reality — tests + existing packets:** the unit tests listed above, and
  existing packet manifests under `orca-harness/reports/source_capture/**/manifest.json`
  (untracked). Check what posture + `hash_basis` values real packets actually carry,
  and whether they still validate.
- **Harness contrast:** `orca-harness/schemas/case_models.py` (`EvidenceUnit.hash_basis`).
- **Intent of record:** `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`
  and its review `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_v0.md` (findings AR-01..AR-05).
- **Layer boundary:** `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`.

## Method sequence (Source-Gated Method Contract)

1. Read authority (`AGENTS.md`, overlay README, review-lanes, prompt-orchestration).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-adversarial-artifact-review`. Do **not** APPLY yet.
3. `SOURCE-LOAD` the read-pack; confirm the two anchor hashes.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only then APPLY deep-thinking to frame failure modes, then adversarial-artifact-review to produce findings, each cited to file:line.

If `workflow-adversarial-artifact-review` is unavailable/not applied, return blocked or advisory-only; emit no formal verdict/readiness/validation claim.

## Decision criteria — attack these seams

1. **Code ⇄ doctrine exactness.** Do `CUTOFF_POSTURE_VALUES` / `ARCHIVE_HISTORY_POSTURE_VALUES`
   / `RE_CAPTURE_RELATIONSHIP_VALUES` match the amended §9/§10/§15 **exactly**, both
   directions (file:line each side)? Did the doctrine amendment introduce, drop, or
   rename any value the code does not enforce, or vice versa? Is `access_posture`
   (Ob.11) still genuinely OPEN in **both** code and doctrine?
2. **Migration completeness (no silent survivor).** Is there ANY packet-constructing
   path — runner, helper, test fixture, or existing on-disk manifest — that still
   emits a posture value outside the closed set, or a `known` posture whose value is
   free-text narrative? Grep the runners; read the packets. Would such a packet now
   fail validation (regression) or has it been migrated?
3. **cutoff untangle (AR-03) — nothing lost.** Does `_source_time` truly no longer
   derive time from `cutoff_posture`? Did the narrative that used to live in off-vocab
   `cutoff_posture` values land somewhere recoverable (`capture_context` / reason /
   limitation), or was decision-bearing context dropped in the migration?
4. **Archive Option (b) — recoverability.** With the posture collapsed to
   `archived`/`attempt_failed`, are the snapshot timestamp and the specific
   non-preservation reason actually still present in the preserved metadata +
   limitations (not just claimed to be)? Is the status/value split clean, or does it
   double-encode / conflict with how `packet_assembly.py` uses statuses?
5. **hash_basis recomputation-bound (AR-04).** Is `raw_stored_bytes` honest — does
   `hash_file` hash the raw stored bytes with no normalization? Can a reviewer
   actually recompute a preserved file's `sha256` from (`relative_packet_path`,
   basis) and verify it? Is the field schema-closed (not a free string)? Is
   required-with-no-default correct, or does it break read-back of any real/older
   manifest that lacks the field?
6. **Value-vs-sufficiency boundary held.** Did closing any vocabulary smuggle a
   downstream Judgment/sufficiency call into Capture (e.g., is `archived` vs
   `attempt_failed` strictly a value, not a "good-enough/corroborated" verdict)?
7. **Doctrine fidelity (no over-claim).** Does the amended contract describe what the
   code actually does — no claimed enforcement that isn't in the schema, no described
   representation the code doesn't implement? Does the amendment stay within the
   contract's `retrieval_only` boundary (states enforcement as fact; grants no new
   implementation authority)?
8. **Global blast radius.** The validators fire on every packet write. Does the
   enforcement break, or silently change, any packet path elsewhere in the repo that
   is NOT in the migration set?
9. **Suite-green honesty.** Is "full suite green" load-bearing — do the changed
   assertions actually pin the new behavior (exact-value posture checks, `hash_basis`
   round-trip), or were assertions weakened/loosened to pass? Did any test start
   passing for the wrong reason (e.g., a missing-field error masquerading as the
   intended rejection)?

## Output contract

- `review-report` mode. Write to
  `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_implementation_adversarial_review_v0.md`.
- Start with the compact `review_summary` YAML
  (`recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked`),
  then findings.
- Findings-first: ID, `severity` (`critical|major|minor`, priority only), seam,
  file:line evidence, `minimum_closure_condition` (end state), `next_authorized_action`.
- Include non-findings (seams that held) and not-proven boundaries (e.g., that the
  schema change is safe for packet shapes beyond those read; that this review is
  cross-family if the reviewer is same-family as the author).
- **Advisory only.** No `patch_queue_entry`, no executor-ready how-to. Optional
  hardening labeled optional.

## Validation gates (must be able to fail)

- Source readiness declared before findings; the implemented code + existing packets
  actually read (or `SOURCE_CONTEXT_INCOMPLETE`).
- Both anchor hashes confirmed; drift → report + review current content.
- Untracked/dirty sources → advisory only; no strict PASS/readiness/ratification claim.
- Durable report written before any YAML-only chat summary; on write failure use
  `status: failed`, `review_location: chat_only_current_thread`, `recommendation: blocked`.

## Review-use boundary

Findings are decision input for the owner / Data Capture lane only — not approval,
validation, ratification, mandatory remediation, or patch authority. This review
does not execute or commit the change and does not unfreeze JSG-01. A clean result
is what lets the owner treat R2 as settled; it is not itself that ratification.
`agent-workflow` is read-only reusable mechanics; `jb` is not Orca authority.
