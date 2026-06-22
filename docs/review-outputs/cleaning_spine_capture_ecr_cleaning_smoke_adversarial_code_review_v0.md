# Cleaning Spine Capture/ECR/Cleaning Smoke Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (implementation/code review, advisory)
scope: >
  Findings-first adversarial implementation/code review of the no-network
  Capture -> ECR -> Cleaning smoke stitcher patch on the Cleaning spine lane.
use_when:
  - Adjudicating whether to keep/commit/PR the smoke-runner patch.
  - Checking what was inspected, what holds, and the residual risks.
authority_boundary: retrieval_only
reviewed_by: claude-opus-4.8
authored_by: gpt-family-codex
de_correlation_bar: cross_vendor_discovery
branch_or_commit: codex/cleaning-spine-continuation at bc950cdfeeb3a02f33bf52217d71e049aa9093f2
```

## Actor / De-Correlation Receipt (filled)

- `author_home_model_family`: OpenAI / GPT-family Codex (recorded from the authoring lane).
- `controller_model_family`: Anthropic / Claude (Opus 4.8) — the receiving controller-reviewer.
- `current_receiving_actor_role`: controller.
- `dispatch_mode`: external-controller-courier.
- `de_correlation_status`: cross-vendor satisfied (author vendor `OpenAI` != reviewer vendor `Anthropic`).
  Recorded as a who-constraint provenance fact only; it is **not** a runtime-model
  recommendation and does **not** by itself confer formal review, no-new-seam,
  readiness, or validation authority (see Strict-Claim Boundary).
- No runtime model recommendation is made by this review.

## Source Context

`SOURCE_CONTEXT_READY`.

Source-loading mode: **zero-config findings-only advisory** implementation/code
review. No Orca-bound formal implementation-review lane exists
(`review-lanes.md` keeps implementation/code review a separate, unbound lane),
so formal verdict / readiness / validation / patch-queue authority is
`NOT_CLAIMED`. Severity labels below are **priority only**, not Orca verdict
authority.

### Source-Read Ledger

| Source | Why read | State |
| --- | --- | --- |
| `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` | Primary review target | untracked (??), read in full |
| `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` | Target test | untracked (??), read in full + rerun |
| `docs/workflows/orca_repo_map_v0.md` (smoke-runner edit) | Repo-map route accuracy | modified (M), diff inspected |
| `.agents/workflow-overlay/README.md` | Overlay authority entrypoint | clean |
| `.agents/workflow-overlay/review-lanes.md` | Review authority / output rules | clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | Commission routing / de-correlation | clean |
| `.agents/workflow-overlay/safety-rules.md` | Boundary / no-network framing | clean |
| `.agents/workflow-overlay/source-loading.md` | Source-gated method contract | clean |
| `.agents/workflow-overlay/prompt-orchestration.md` | Review-prompt output contract | clean |
| `orca-harness/cleaning/models.py` | `CleaningInputHandle`/anchor/ref invariants | modified (M), read in full |
| `orca-harness/cleaning/projection.py` | Projection->handle adapter behavior | read in full |
| `orca-harness/ecr/deriver.py` | Four source-side posture derivers (purity) | read in full |
| `orca-harness/source_capture/models.py` | `SourceCapturePacket`/`PreservedFile`/slice invariants | read in full |
| `orca-harness/source_capture/retail_pdp_projection.py` | Retail projection row/anchor shape | read in full |
| `orca-harness/source_capture/reddit_consolidation/consolidator.py` | Consolidation JSON shape the runner parses | read in full |
| `orca-harness/harness_utils.py` | `hash_file` / `utc_now_z` purity | read in full |
| import sweep over the runner's dependency chain | no-network confirmation | clean (no hits) |

Notes:
- `AGENTS.md` and the Agent Behavior Kernel were supplied in session context
  (focused-brown worktree copy). The operative review-lane / safety authority
  files above were read directly from the codex target worktree.
- `docs/hygiene/cleaning_spine_lane_handoff_v0.md` is **absent** in this
  worktree (confirmed by `ls`); review proceeds from the prompt target plus
  current sources, as the prompt allows.
- Worktree pin verified: HEAD `bc950cdfeeb3a02f33bf52217d71e049aa9093f2`,
  branch `codex/cleaning-spine-continuation`, dirty state matches the prompt's
  observed status. The review-output destination did not previously exist (no
  `stale_if` triggered).

## Headline

**No blocker and no major finding.** The runner's load-bearing promises hold by
inspection and by an independent rerun of its test file: it stays no-network and
consumes only existing packet/projection/consolidation artifacts; it preserves
raw/projection/ECR anchors with packet-key coupling enforced at the model layer;
it verifies preserved-file hashes against both the packet manifest and the
consuming artifact; it contains preserved-file reads to the packet directory; it
makes Reddit row-level anchors only when the fullname/id pattern is actually
present in the raw HTML and otherwise downgrades with a reported finding; it
derives all four ECR source-side postures for every packet; and it surfaces
overwrite, empty-manifest, packet-mismatch, hash-mismatch, and path-escape
failure modes as raised errors rather than fabricated success. Residuals
(`structure_preserved=false`, downgraded anchors) are recorded as findings, not
turned into validation or readiness claims.

Four **minor** findings and two residual risks follow. All are advisory; none
blocks keeping the patch.

## Findings (priority-ordered)

### F1 — Retail handle `slice_id` is trusted from the projection, not re-derived against the packet (asymmetric with the Reddit path) — `minor`

- **Commissioned target/purpose:** smoke-runner patch; raw/projection/ECR
  traceability integrity.
- **Reviewed target:** `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`.
- **Location:** `_verify_retail_projection_anchors` lines 440-474 (slice check
  455-459; file verify 467-473); slice copied into the handle anchor at
  `orca-harness/cleaning/projection.py:41`. Contrast the Reddit path's
  `_slice_id_for_file` (runner lines 536-540).
- **Evidence:** For retail rows the runner checks `row.raw_ref.slice_id in
  packet_slice_ids` (the slice *exists*) and hash-verifies the file by
  `file_id`/`relative_packet_path`/`sha256`, but never checks that
  `row.raw_anchor.file_id` is a member of that `slice_id`'s
  `preserved_file_ids`. The emitted handle's `raw_anchor.slice_id` is taken
  verbatim from `raw_ref.slice_id`. The Reddit path instead **derives** the
  slice from the packet and raises if the file belongs to no slice.
- **Authority/basis:** repo-visible code; `CleaningRawAnchor`
  (`cleaning/models.py:101-138`) carries `slice_id` and `file_id` but imposes no
  slice<->file coupling validator.
- **Impact:** A stale or hand-edited `projection_json` could pair a genuine,
  hash-valid preserved file with a different but existing `slice_id`; the runner
  would still pass and emit a handle that mis-attributes the file to the wrong
  slice. Hash and packet-id integrity are preserved; slice-level traceability is
  not. Bounded: in-pipeline the projection is freshly derived from the same
  packet (`build_retail_pdp_projection` iterates `slice.preserved_file_ids`), so
  the coupling holds by construction there. The runner's stated contract is to
  consume *existing* (possibly stale) artifacts, which is where the gap bites.
- **Minimum closure condition:** for each retail row, the file's owning slice is
  re-derived from / cross-checked against the packet's
  `source_slices[*].preserved_file_ids` (mirroring `_slice_id_for_file`) and a
  mismatch raises.
- **Next authorized action:** home model decides whether to tighten; advisory
  only (read-only review).
- **Validation expectation:** a negative unit test feeding a retail row whose
  `raw_ref.slice_id` names a slice that does not contain its `file_id` should
  raise after the fix (currently it would pass).

### F2 — `main()` catches only `ValueError`; pydantic `ValidationError` and the empty-`CleaningPacket` case escape as a raw traceback — `minor`

- **Reviewed target:** `run_capture_ecr_cleaning_smoke.py` CLI wrapper.
- **Location:** `except ValueError` at lines 636-637; `CleaningPacket(handles=
  handles)` at line 106; `*.model_validate(...)` at lines 152-154 and 484-486.
- **Evidence:** Pydantic v2 `ValidationError` is **not** a subclass of
  `ValueError`. A retail-only manifest whose projection has zero rows yields
  `handles=[]`, so `CleaningPacket(handles=[])` raises a `min_length=1`
  `ValidationError` that the `main()` handler does not catch; likewise a
  malformed packet/projection/consolidation that fails schema validation.
- **Authority/basis:** repo-visible code; `cleaning/models.py:340`
  (`handles: ... Field(min_length=1)`).
- **Impact:** These inputs exit with a Python traceback and a non-zero code
  rather than the wrapper's `capture/ECR/Cleaning smoke failed: ...` / exit-2
  contract. This is the **safe** direction (loud, visible failure — no
  fabricated success), so it is a robustness/uniformity polish item, not a
  correctness or safety defect. The in-process `run_capture_ecr_cleaning_smoke`
  API still raises cleanly.
- **Minimum closure condition:** either `main()` also catches
  `pydantic.ValidationError` (mapping to exit 2), or the CLI's error-message
  contract is documented as covering only `ValueError`-shaped failures.
- **Next authorized action:** home model decides; advisory only.
- **Validation expectation:** a CLI-level test invoking `main()` with a
  zero-row retail manifest currently surfaces a traceback; after the fix it
  exits 2 with the friendly message.

### F3 — Repo-map edit folds a (today-dated) runner addition into the prior 2026-06-20 refresh entry and commingles an unrelated reconciliation-checklist row — `minor`

- **Reviewed target:** `docs/workflows/orca_repo_map_v0.md` (smoke-runner edit).
- **Location:** the `Refreshed:` line (2026-06-20 parenthetical extended with
  "...and added the no-network Capture/ECR/Cleaning smoke stitcher runner") and
  the added table row for
  `docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md`.
- **Evidence:** `git diff docs/workflows/orca_repo_map_v0.md` shows three hunks:
  (a) the refresh-marker extension, (b) a new nav row for the
  reconciliation-checklist artifact, and (c) the runners-cell clause adding
  `run_capture_ecr_cleaning_smoke.py` ("no-network ...; consumes existing
  packet/projection/consolidation artifacts only"). The prompt's own dirty-state
  list identifies the reconciliation checklist as **pre-existing adjacent
  cleaning work**, not the smoke-runner patch. Today is 2026-06-21; the runner
  file is untracked/new.
- **Authority/basis:** repo-visible diff; the runner-route clause itself is
  accurate and **does not overclaim** capture execution or ECR/Cleaning
  readiness (answering the prompt's repo-map question).
- **Impact:** Two narrow issues. (i) Freshness-marker accuracy: a 2026-06-21
  addition is attributed to the 2026-06-20 pass, against the repo-map's own
  dated-refresh convention. (ii) Commit hygiene: committing the smoke-runner
  patch as a unit including the whole repo-map file change would sweep in the
  unrelated reconciliation-checklist nav row.
- **Minimum closure condition:** when staging, the smoke-runner repo-map edits
  (runners-cell clause + the smoke clause on the refresh line) are separated
  from the reconciliation-checklist row, and the runner addition is attributed
  to an accurate date (e.g. a dated refresh entry).
- **Next authorized action:** home-model commit-shaping decision; advisory only.
- **Validation expectation:** the committed smoke-runner change set contains
  only smoke-runner-attributable repo-map lines.

### F4 — Test coverage gap: three of the five named failure-mode guards are untested — `minor`

- **Reviewed target:** `tests/unit/test_capture_ecr_cleaning_smoke_runner.py`.
- **Location:** existing coverage at lines 153-185 (empty-manifest +
  existing-output) and 112-150 (Reddit downgrade). Uncovered guards: retail
  packet-id mismatch (runner 155-159; Reddit 236-240), sha256 mismatch (runner
  511-518), path-escape containment (runner 522-533).
- **Evidence:** the suite exercises overwrite and empty-manifest (both named in
  the review scope) but no test drives packet-mismatch, hash-mismatch, or
  path-containment raises.
- **Authority/basis:** repo-visible tests + runner code. The guards are present
  and correct by inspection; the gap is coverage, not behavior.
- **Impact:** these guards are load-bearing for the "no fabricated success"
  promise; a future regression weakening any of them would not be caught by the
  current suite.
- **Minimum closure condition:** focused negative tests exist for packet-id
  mismatch, sha256 mismatch, and path-escape.
- **Next authorized action:** home model decides whether to add coverage;
  advisory only (read-only review cannot author tests).
- **Validation expectation:** added negative tests fail against a deliberately
  weakened guard and pass against the current guard (same-check red/green).

## Residual Risks (not defects)

- **R1 — Reddit row-anchor fidelity is coupled to the upstream parser's id
  shape.** The runner reconstructs `f"{t3|t1}_{id}"` and substring-matches it in
  raw HTML (runner 340, 376-392). The fixture parser emits bare ids
  (`abc`/`c1`), so the un-mutated test asserts `anchor_kind=="text_pattern"` for
  all three handles (test 102-103) — coupling confirmed for the fixture. If the
  upstream Reddit parser ever emitted already-prefixed ids, **every** Reddit
  anchor would silently downgrade to file-level (with `reddit_row_anchor_
  downgraded` findings). This is the **safe** direction (no false anchor), but
  the degradation would be blanket and visible only as a flood of findings. A
  parser contract test, or carrying the anchor the parser already matched
  instead of reconstructing it, would remove the coupling. Not a current-state
  defect.
- **R2 — Anchor search runs over an `errors="replace"` decode of the raw HTML**
  (runner 254). The file hash is verified on raw bytes first, so integrity is
  intact; a non-UTF-8 byte could only perturb the substring search and, at
  worst, cause a (reported) downgrade. Safe direction; noted for completeness.

## Validation Evidence Inspected / Not-Run Gaps

- **Independently revalidated:** `python -m pytest -p no:cacheprovider --no-header
  -q tests/unit/test_capture_ecr_cleaning_smoke_runner.py` rerun by this
  reviewer in the codex target worktree — **3 passed**. This directly confirms
  the runner's retail+reddit happy path, the missing-row-anchor downgrade, and
  the empty-manifest/existing-output refusals, and (by static cross-check) that
  the test assertions match the implementation.
- **Author-supplied, not independently revalidated:** the broader 8-file suite
  and the `--help` / `check_repo_map_freshness.py --changed` /
  `check_placement.py --check` runs reported in the prompt were **not** rerun
  here (the reviewer stayed read-only and avoided executing the broader suite in
  the intentionally-dirty lane). The pasted "[100%]" output is taken as
  author-supplied.
- **Not run by anyone (coverage gaps):** see F4 — packet-mismatch,
  hash-mismatch, and path-containment guards have no direct unit test.

## Open Questions

- Is consuming a *stale* retail `projection_json` (out of sync with the packet)
  an in-scope input for this runner, or is it always freshly derived upstream?
  The answer sets whether F1 is worth closing now or is acceptable as a
  documented assumption.
- Is the reconciliation-checklist repo-map row (F3) intended to land with the
  smoke-runner commit, or with the separate cleaning-reconciliation work?

## Review-Use Boundary

These findings are **decision input only**. This is advisory implementation/code
review: it is **not** approval, validation, readiness, acceptance, a formal
pass/fail verdict, mandatory remediation, or executor-ready patch authority, and
it emits no `patch_queue_entry`. Formal review authority remains `NOT_CLAIMED`
unless Orca overlay authority is supplied separately. No source files were
edited; nothing was committed, pushed, PR'd, or run as live capture. Severity
labels are priority only.
