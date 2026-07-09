# Source Capture Lenient-Read Slice — Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Commissioned, de-correlated adversarial review-and-patch pass on the Phase-1
  lenient-read slice (the Source Capture packet inspection reader + its census
  integration + tests). The delegate reviews the diff for material/fake-success
  failure modes and returns a bounded PATCH PROPOSAL (unified diff) of its own
  accepted findings; the commissioning home model adjudicates what is kept.
use_when:
  - Dispatching the de-correlated review-and-patch on the lenient-read slice before it is treated as settled.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:   # 12-char sha256 prefixes; worktree is dirty — confirm via `git diff`, report drift
  orca-harness/source_capture/packet_inspection.py: E031FF2DF768
  orca-harness/source_capture/source_quality.py: 7B244BAE24DB
  orca-harness/tests/unit/test_packet_inspection.py: 3615168E8128
  orca-harness/tests/unit/test_source_quality_state_assembler.py: 23B323A08852
branch_or_commit: main @ 02d2ff0 (worktree dirty; the slice files + all controlling sources are uncommitted/untracked)
```

## Commission

Run a **de-correlated adversarial review-and-patch** on the Phase-1 lenient-read
slice. Review the diff for material failure modes — with the fake-success surface
as the priority — and return a **bounded patch PROPOSAL** (a unified diff) that
applies ONLY your accepted findings. The commissioning home model (the author)
adjudicates the returned diff before anything is kept; your diff, verdict, and
citations are decision input, not premises to inherit.

**Why ordinary source-read-only review is insufficient here.** The slice's entire
purpose is fake-success guards the author encoded (a distinct non-packet return
type; catch-only-`ValidationError`; a write-once/read-only invariant). The author
can re-introduce the exact failure mode those guards exist to prevent, and
same-family self-review structurally misses that blind spot. Hence a de-correlated
pass.

## Convention fit — two disclosed deviations (read first)

This commission adapts the provisional Delegated Review-and-Patch convention
(`.agents/workflow-overlay/delegated-review-patch.md`), which by default targets a
**single authored** doctrine/contract/eval artifact and has the delegate patch that
**one file in-repo**. This commission deviates on the CA's authority, deliberately:

1. **Target is a 4-file code slice, not a single authored artifact.** The bounded
   patch scope is the four slice files listed under *Target*; everything else is
   flag-only.
2. **Return a PROPOSED unified diff; do NOT apply it in-repo and do NOT commit.**
   The home model applies/adjudicates. (This is stricter than the convention's
   in-repo patch, by CA choice.)

Everything else follows the convention: de-correlation, neutral-tone citations,
combined review+patch, home adjudication, mechanical-lane patch discipline,
residual-risk note, and the `NEEDS_ARCHITECTURE_PASS` escalation.

## De-correlation (commission who-constraint, NOT runtime model routing)

- Record the **author model family** (Claude) and your **delegate model family**.
  The lane is satisfied only if they **differ**; if the author is Opus-class, the
  delegate must be a different, non-Opus family. A same-family or self pass does
  **not** satisfy it — disclose and mark the bar **not met**.
- If no different-family model is available, do **not** claim this lane: fall back
  to source-read-only findings + author self-review and record the limitation.
- This is a who-constraint recorded in the commission only. Do **not** put model
  selection/ranking advice anywhere in your output; Orca review-lane
  model-neutrality holds.

## Reviewer start state

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: read-only on the repo; output is a PROPOSED diff only (do not apply/commit)
  target_scope:
    - orca-harness/source_capture/packet_inspection.py
    - orca-harness/source_capture/source_quality.py
    - orca-harness/tests/unit/test_packet_inspection.py
    - orca-harness/tests/unit/test_source_quality_state_assembler.py
  dirty_state_checked: required_yes
  blocked_if_missing: yes
controlling_source_state: untracked/dirty; advisory only; no strict PASS/readiness/settled claims.
output_mode: review-report + proposed-diff courier
external_source_boundary: agent-workflow is read-only reusable mechanics; jb is NOT Orca authority.
```

## Target (commission-bound; do not retarget)

The four slice files above. Obtain the diff with `git diff` for the two modified
files (`source_quality.py`, `test_source_quality_state_assembler.py`) and read the
two new files in full (`packet_inspection.py`, `test_packet_inspection.py`).
Confirm the 12-char `input_hashes`; on mismatch, report drift and review the
current worktree content. The worktree is broadly dirty — review only the slice.

## Frozen contract (do NOT reopen; flag, do not patch, anything that would)

- **M2 mechanism:** the reader reuses `SourceCapturePacket.model_validate` as a probe
  inside `try/except ValidationError`; it catches **only** `ValidationError`; it
  returns a **distinct** `PacketConformanceReport` that carries a validated packet
  **only** when conforming. Single source of truth for "valid" is the model.
- **AR-01 honest fields only:** `declared_manifest_version`,
  `declares_current_manifest_version`, `conforms_to_current_schema`,
  `current_schema_errors`, and `declared_version_shape_validation =
  not_available_without_per_version_schema` for any non-current declared version.
  **No** general cross-version shape validation.
- **Census state:** `manifest_nonconforming` (valid JSON, fails current schema) is
  distinct from `manifest_uninspectable` (unparseable).
- **Invariants:** write-once / hash-pin (no re-serialize, no `raw/` touch, no
  `hash_basis` backfill); the on-disk v0 packets stay byte-frozen.
- **Settled context (out of scope to reopen):** R2 (closed vocab + `hash_basis` +
  v0→v1) is settled; JSG-01 frozen; `access_posture` open (Ob.11); the AC-10
  fixture-admission frontier and the deferred satellite (per-version models /
  dispatch / upgrade adapters / strict admission gate) are separate lanes.
- Reference: `docs/product/source_capture_packet_schema_evolution_architecture_v0.md`
  including its **Adjudication & Amendment** section (the binding AR-01 + M2 record).

## Method sequence (Source-Gated Method Contract)

1. Read authority (`AGENTS.md`, overlay `README`, `review-lanes`, `delegated-review-patch`, `prompt-orchestration`, `safety-rules`).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-code-review`. Do **not** APPLY yet.
3. `SOURCE-LOAD` the slice diff + the frozen-contract references; confirm anchors.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. APPLY deep-thinking to frame failure modes, then code-review to produce findings; only then compose the bounded patch proposal.

If `workflow-code-review` is unavailable/not applied, return findings-only/advisory; emit no formal verdict.

## Attack seams (the fake-success surface — try to break each, cite file:line)

1. **Distinct-type guard.** Can a non-conforming read EVER hand a `SourceCapturePacket`
   (or a packet-shaped object/dict) to a caller? Trace every call site — the census
   branch and any helper that indexes preserved files (e.g. `preserved_by_id[...]`).
2. **Catch scope.** Is it strictly `except ValidationError`? Any path where a
   non-`ValidationError` is swallowed and laundered into a false "non-conforming"?
3. **Write-once.** Is the read genuinely read-only? Is the before/after-`sha256`
   test real, or does it pass vacuously (e.g. never actually mutating, or hashing
   the wrong set of files)?
4. **Census vocabulary.** Is `manifest_nonconforming` vs `manifest_uninspectable` an
   honest, non-lossy cut? Does declares-current-but-fails (corruption) vs
   declares-non-current (off-version) read honestly? Did **updating the prior
   invalid-manifest test** track the new distinction, or paper over a regression?
5. **AR-01 honesty.** Does the report ever overpromise declared-version shape
   validation? Is `declared_version_shape_validation` correct as a function of
   `declares_current` only — including in the **conforming** branch (a packet that
   declares a non-current version but satisfies the current schema)?
6. **Double-validate.** The census runs the lenient probe, then the strict skeleton
   re-validates a conforming packet — any correctness, ordering, or cost issue?
7. **Deferred gap.** The **direct** skeleton/CLI entry stays strict (leniency is only
   at the census). Honest named deferral, or a real hole a reviewer would expect closed?
8. **Test honesty.** Do the tests actually pin the guards, or pass for the wrong
   reason (wrong exception type asserted, missing-field error masquerading as the
   intended rejection, etc.)?

## Patch proposal discipline (mechanical-lane)

- Patch **only** accepted findings. No scope expansion, no new architecture, no
  opportunistic cleanup, no style churn. If a finding needs design change rather
  than a bounded patch, do **not** patch it — escalate (below).
- Stay inside the four target files. All other paths — other Orca sources, the
  frozen v0 packets, hash-pinned/provenance/review-output ledgers,
  `.agents/workflow-overlay/*`, `AGENTS.md`/`CLAUDE.md`, and everything
  `.agents/workflow-overlay/safety-rules.md` forbids — are **flag-only**.
- Return the patch as a **PROPOSED unified diff**. Do **not** apply it in-repo and
  do **not** commit.
- **Escalation:** if the slice's problem is design-level rather than patch-level,
  return `NEEDS_ARCHITECTURE_PASS`, stop patching, and return findings only; any
  partial diff is quarantined, not kept.

## Output contract (paste-ready courier to the commissioning home model)

1. **Findings** — for each: `id`, `severity` (`critical|major|minor`, priority label
   only), seam, **file:line citation**, and `minimum_closure_condition`.
2. **Citations** — neutral in tone (factual source evidence, no advocacy or
   editorializing) but decision-sufficient in substance. Argument goes in the
   verdict/residual, not the citations.
3. **Proposed patch** — a single unified diff over only the accepted findings,
   within the four target files. Not applied, not committed.
4. **Verdict** — `recommendation: sound | patch_proposed | needs_architecture_pass | blocked`.
5. **Residual-risk note** — what the patch does not cover; what stays not-proven.
6. **De-correlation disclosure** — author family (Claude) vs your delegate family,
   and whether the cross-family bar is **met / not met**.

Write a durable report to
`docs/review-outputs/source_capture_lenient_read_slice_delegated_adversarial_code_review_and_patch_v0.md`
(include the diff there); if the write fails, use `status: failed`,
`review_location: chat_only_current_thread`, `recommendation: blocked`. Return a
compact chat summary + the courier after a successful write.

## Validation gates (must be able to fail)

- Source readiness declared before findings; the actual diff read (or `SOURCE_CONTEXT_INCOMPLETE`).
- Anchors confirmed or drift reported.
- Untracked/dirty sources → advisory only; no strict PASS/readiness/settled claim.
- Diff is a proposal only; no in-repo application, no commit, no push.
- Same-family delegate → bar **not met**, disclosed.

## Review-use boundary

Decision input for the commissioning home model only. Not approval, validation,
acceptance, ratification, readiness, formal verdict authority, or settled status.
The home model adjudicates the returned diff and reserves final authority over what
is kept (and may veto any change it judges net-negative, even if individually
defensible). "Settled" still requires that home adjudication after this pass.
`agent-workflow` is read-only reusable mechanics; `jb` is not Orca authority.
