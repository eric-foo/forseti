# Adversarial Code Review — Source Capture `packet_assembly` (STEP-02 http reference port)

```yaml
artifact_role: Review prompt
review_lane: adversarial code review (read-only; reviewer does not patch)
output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/source_capture_packet_assembly_step02_adversarial_code_review_v0.md
authority_boundary: retrieval_only
load_rule: confirm-don't-trust — read the named source before any strict finding.
```

## Commission

Adversarially review the STEP-02 reference slice of the Source Capture Armory
adapter refactor: the new shared last-mile helper and the http runner port that
proves it. Decide whether the helper is a sound, behavior-preserving contract
that will **generalize** to the media runner (N slices + failure slices) and the
coming Reddit adapter (one slice per record, credentialed) **without** hiding
per-slice honesty or leaking secrets — or whether its shape will fight those
cases and should change before it propagates.

## Target (read these exact files in the current working tree)

- `orca-harness/source_capture/packet_assembly.py` (new) — the whole module.
- `orca-harness/runners/run_source_capture_http_packet.py` (modified) — the port.
- `orca-harness/docs/adapter_author_contract.md` (new) — the conventions doc.
- Compare against the untouched reference: `orca-harness/source_capture/writer.py`
  (`write_local_source_capture_packet`, `_copy_preserved_files`), `models.py`
  (`SourceCaptureSlice`, `VisibleFact`, `validate_preserved_file_references`),
  and `orca-harness/runners/run_source_capture_media_packet.py` (the NOT-yet-ported
  generalization target).

## Authority / frozen context

- Architecture (frozen): packet is the contract; NO adapter ABC/registry/dispatcher;
  build the result→packet last mile only. Adapter inputs stay native.
- Invariants the slice must preserve: no secrets/tokens in packets; packets stay
  scratch; capture-support only; **no rollup hides a failed slice**; honest limitations.
- Verification done: 62 tests pass (http + media + archive + packet + import-guard).
  http behavior preserved; media/archive untouched.

## Three facts the implementer confirmed from source (verify them, then attack)

1. Posture fields are `VisibleFact` (status + free-text), **not** a clean/failed
   enum. The honesty validator therefore uses: *any slice with non-empty
   `limitations` ⇒ capture-level `limitations` non-empty.*
2. Packets are **not** byte-identical across runs (ULID `packet_id`/`session_id`,
   `utc_now_z` capture_time); the gate is tests-green-modulo-those-fields.
3. Runner exit codes are **0/2/3** (2 = ValueError/bad-input, 3 = adapter/other).

## Decision criteria — attack these seams hardest

1. **Validator strength.** Is "slice limitation ⇒ packet limitation" too weak? A
   slice can carry a non-`known` `access_posture`/`archive_history_posture`/
   `media_modality_posture` (unknown_with_reason/not_attempted) with an EMPTY
   `limitations` list — the validator would pass a clean capture-level rollup over
   it. Should the rule also consider non-`known` posture status per axis? Is it too
   strong anywhere (would it reject a legitimately honest packet)?
2. **File-id coupling.** `staged_file_id_map` computes `file_NN` from artifact
   order; the writer independently assigns `file_NN` from `input_files` order.
   `stage_and_write_packet` builds `input_files` from the same `staged_artifacts`.
   Can the map and the writer's actual assignment ever diverge (duplicate
   filenames, ordering, a runner that builds slices from a different order)? Is the
   duplicate-filename guard sufficient?
3. **Generalization to media.** Walk the media runner's real shape (per-asset 2
   files, failure slices with `preserved_file_ids=[]` + a limitation, the final
   `packet_slices.sort(by slice_id)`). Does `stage_and_write_packet`'s contract fit
   it without forcing the runner to mis-order artifacts vs. slice references? Name
   the concrete failure if it doesn't.
4. **Generalization to Reddit (credentialed).** Is anything in the helper or the
   contract doc a latent secret-leak path once a credentialed adapter arrives
   (e.g., a runner stuffing a token into `writer_kwargs`/metadata that reaches
   `raw/`)? Is "secrets never in packets" structurally enforceable here, or only by
   convention?
5. **Behavior preservation.** Did the http port change ANY manifest byte beyond
   {packet_id, session_id, capture_time}? Specifically: reuse of a single shared
   `archive_posture`/`media_posture`/`recapture_posture` object vs. the original's
   separate-but-equal `not_attempted(...)` calls — confirm JSON-identical. The
   collision-guard message changed from http-specific to generic — acceptable, or a
   silent behavior regression?
6. **Honesty-validator placement.** It runs before the writer constructs the packet
   (on runner-supplied slices + the `limitations` kwarg). Can a runner bypass it
   (`enforce_posture_honesty=False`, or postures the validator never sees)? Should
   it instead validate the final packet object?

## Evidence boundaries / non-claims

Repo-visible code is the evidence. Working tree is dirty/uncommitted (broad
pre-existing dirt unrelated to this slice). This review does not patch, validate,
admit fixtures, or claim readiness; findings are advisory until the CA/owner binds
them. Use the Orca adversarial review summary shape: a copy-pasteable
`review_summary` YAML first (recommendation ∈ accept | accept_with_friction |
patch_before_acceptance | reject | blocked; blocking vs advisory finding IDs;
next_action), then detailed findings in the durable report.
