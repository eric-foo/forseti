# Cleaning Spine Last Enforcement Batch — Cross-Vendor Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (implementation/code review, advisory)
scope: >
  Cross-vendor adversarial implementation/code review of the Cleaning spine
  last-enforcement batch on the cleaning-spine-continuation branch.
use_when:
  - Checking the advisory findings and residuals from the last-enforcement Cleaning review batch.
  - Reconstructing what source context the delegated reviewer inspected.
authority_boundary: retrieval_only
reviewed_by: Claude (Anthropic), Opus 4.8 — cross-vendor controller, read-only
authored_by: gpt-family-codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable  # reviewer lineage (Anthropic/Claude) differs from author lineage (OpenAI/GPT-family)
review_type: implementation/code review — findings-only advisory (no formal Orca review-lane authority supplied)
implementation_under_review: 0d2f3be955a469f7bfae1727e551f771e5e771be..aef50b05efdb57fbe57a71433d7e2f30db861b4e
branch_or_commit: codex/cleaning-spine-continuation at aef50b05efdb57fbe57a71433d7e2f30db861b4e
target_files:
  - orca-harness/runners/run_cleaning_spine_periodic_audit.py
  - orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
diff_observed: 2 files changed, 640 insertions(+), 16 deletions(-)  # confirmed against the named range
source_context: SOURCE_CONTEXT_READY
overall_reviewer_signal: no blocker found; 1 major + 2 minor advisory findings; E-06/E-07 enforced, E-04/E-05 partially closed
```

## SOURCE_CONTEXT_READY

`SOURCE_CONTEXT_READY` with caveats recorded in the source-read ledger.

Drift / staleness checks (all clear):

- Branch `codex/cleaning-spine-continuation` HEAD is `3e1f0ec9`. The only commit after the target `aef50b05` is `3e1f0ec9 "Add Cleaning last enforcement batch review prompt"` — a prompt-only carrier. `git diff --stat aef50b05..HEAD -- <both target files>` is **empty**: both target files still match `aef50b05`. The `prompt_carrier_note` holds; no retarget needed.
- Output destination `docs/review-outputs/cleaning_spine_last_enforcement_batch_claude_cross_vendor_adversarial_code_review_v0.md` did not exist before this write — no `BLOCKED_OUTPUT_DESTINATION_COLLISION`.
- Worktree clean; numstat matches the prompt's claim exactly (368/16 runner, 272/0 test).
- Reviewer lineage (Anthropic/Claude) differs from author lineage (OpenAI/GPT-family) → `cross_vendor_discovery` is legitimate; the `stale_if` "not a different-vendor controller but still claims cross_vendor_discovery" does **not** apply.

### Source-read ledger

| Source | Read mode | Evidence weight |
| --- | --- | --- |
| `git diff 0d2f3be..aef50b05` (both target files, full) | direct, primary | high |
| `orca-harness/runners/run_cleaning_spine_periodic_audit.py` (status pipeline, lane wiring, all new functions + adjacent verifiers) | direct, primary | high |
| `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` (7 new tests + fixture helper) | direct, primary | high |
| `orca-harness/cleaning/models.py` (handle/anchor/transform/packet validators) | direct, primary | high |
| Projection doctrine "carry-or-residualize; never author from prose" (`core_spine_v0_projection_doctrine_v0.md:139-141`) | direct, primary (load-bearing quote re-verified) | high |
| `AGENTS.md`, overlay `review-lanes/delegated-review-patch/validation-gates/safety-rules/source-loading`, cleaning contracts (readme/foundation/boundary), `ecr_spine_submap_v0.md`, `cleaning_spine_lane_handoff_v0.md` | **delegated read** (Explore subagent digest); only the projection carry-or-residualize quote independently re-verified against primary | medium — authority/orientation basis; specific line numbers in the digest not all independently re-verified |
| Independent test rerun (7 new tests) | direct, primary | high |

Honesty note: the overlay/contract authority files were read through a delegated read (summarized digest), not line-by-line by the reviewer. All correctness findings below rest on directly-read implementation code and tests; doctrine is cited only as the authority basis for *why* a gap matters, and the one load-bearing doctrine quote (carry-or-residualize) was confirmed against the primary file.

### Independent validation (not author-supplied)

Reviewer reran the 7 new tests in the codex worktree (`orca-harness`, Python 3.11.15, pytest 9.0.3, `PYTHONDONTWRITEBYTECODE=1 python -B`):

```
test_periodic_audit_accepts_transform_original_value_from_projection
test_periodic_audit_flags_transform_original_value_not_from_projection_or_raw
test_periodic_audit_supported_source_families_have_adapter_coverage
test_periodic_audit_flags_projection_row_kind_outside_source_family_adapter
test_periodic_audit_flags_anchor_kind_outside_source_family_adapter
test_periodic_audit_execution_does_not_open_network_socket
test_periodic_audit_flags_failed_capture_handle_missing_raw_pull_trigger
=> 7 passed
```

No `_scratch` `PermissionError` reproduced in this environment. Author-supplied broader-suite and `--help`/`git diff --check` results were **not** independently rerun and are reported as author-supplied.

---

## Findings (advisory — severity is for prioritization only, not a formal Orca verdict)

**No blocker found.** The new enforcement is wired so that every new finding uses `severity="major"`, and `_lane_status` (`run_cleaning_spine_periodic_audit.py:1856-1862`) promotes any blocker/major to lane `fail`, which makes `overall_status` `fail` (`:214-220`). So all four enforcements **do** drive audit status, not side-channel notes. The findings below are about *strength/coverage of the enforcement*, not status plumbing.

### F-01 — MAJOR (E-05): raw-bytes provenance is a whole-file substring match, not anchored, and is untested

- **Location:** `_transform_original_value_in_raw` — `run_cleaning_spine_periodic_audit.py:1153-1176`, decisive line `return original_value in raw_text` where `raw_text = raw_path.read_bytes().decode("utf-8", errors="replace")` (the entire preserved file).
- **Evidence:** The projection branch `_transform_original_value_in_projection` (`:1109-1129`) is strong — it uses **exact set membership** against flattened leaf values (`return original_value in set(_source_visible_text_values(...))`). The raw branch is the opposite: a plain **substring scan of the whole decoded file**. It ignores the handle's `raw_anchor` specificity (`anchor_kind` / `anchor_value` / `json_pointer` / `slice_id`) that is available and already validated elsewhere (`_verify_anchor_specificity`, `:1324`).
- **Authority basis:** Projection doctrine `core_spine_v0_projection_doctrine_v0.md:139-141` — *"Carry-or-residualize; never author from prose. Every projected field value is carried from the packet or mechanically computed from it; anything absent is … a named residual, never inferred from prose or invented."* A whole-file substring match confirms only that the value's characters appear *somewhere* in the bytes, not that the value was **carried from the anchored location**.
- **Impact:** A short or common `original_value` (e.g. `"0"`, `"true"`, `"div"`, `"Add to Cart"`, a single token) will coincidentally be a substring of a multi-KB HTML/JSON capture and pass provenance, so an invented or mis-attributed `original_value` can be reported as "sourced from raw." This under-enforces the exact "not arbitrary invented text" guarantee E-05 exists for, and the audit reports clean while provenance is only coincidental.
- **Test gap (compounding):** No test exercises the raw-acceptance branch. The passing positive test resolves through projection; the negative test (`test_periodic_audit_flags_transform_original_value_not_from_projection_or_raw`) uses a long sentinel that fails **both** branches. The raw branch is therefore unverified by this batch.
- **Bounding / fair-minority view:** The value does literally occur in the preserved bytes, so a literal reading of "resolve to raw bytes" is satisfiable; a reviewer could rate this **minor**. It is rated major here because the check is weaker than the available anchor specificity allows and the weak path is untested — the combination is what makes coincidental false-acceptance plausible in practice.
- **`minimum_closure_condition`:** Scope the raw match to the handle's `raw_anchor` location — extract the anchored value (via `json_pointer` / `anchor_value` / slice) and require exact equality, or otherwise require the matched substring to be the carried value at the anchor rather than any whole-file occurrence — **and** add a test that (a) accepts a genuine raw-anchored value and (b) rejects a short coincidental substring.
- **`next_authorized_action`:** Advisory only. Home model adjudicates whether to tighten the raw branch and add the missing raw-path test; reviewer is read-only and emits no `patch_queue_entry`.
- **Verification expectation:** Same-check red-green — a new test asserting a short coincidental substring is *rejected* should fail against the current substring implementation and pass after the anchor-scoped fix.

### F-02 — MINOR (E-05): projection leaf-flattening accepts a match against any field in the row, plus bool/number coercions

- **Location:** `_source_visible_text_values` — `run_cleaning_spine_periodic_audit.py:1131-1151`; consumed by `_transform_original_value_in_projection:1109-1129`.
- **Evidence:** The helper recursively flattens the **entire** row's `source_visible_fields` into one leaf-value set (all dict values, all list items), and coerces `bool -> ["true"/"false", str(value)]` and `int/float -> str(value)`. Acceptance is exact-per-leaf but against *any* leaf anywhere in the row, not the specific field the transform claims to have touched (the `CleaningProjectionRef` carries `row_id`/`row_kind` but no field path, so the check cannot scope further).
- **Impact:** Bounded over-acceptance: an `original_value` of `"true"`/`"True"` matches any boolean leaf in the row; a common number matches any numeric leaf; a value from field A is accepted even if the transform actually concerns field B of the same row. Narrower than F-01 because it is exact-per-leaf and confined to the row's own visible fields.
- **Authority basis:** Same carry-or-residualize doctrine (`:139-141`) — provenance should bind to the carried field, not "any visible field in the row."
- **`minimum_closure_condition`:** If/when a transform can name its source field, scope the projection match to that field; otherwise document that row-level (not field-level) provenance is the accepted bar for core v0 and note the bool/number coercion behavior intentionally.
- **`next_authorized_action`:** Advisory. No `patch_queue_entry`.
- **Verification expectation:** Not independently testable today without a field reference on the transform; flag as design note.

### F-03 — MINOR (E-04): failed-capture detection is a fixed substring token list over free-text, with no producer binding and no positive control

- **Location:** `_verify_failed_capture_handle_raw_pull_trigger` (`:1178-1207`) + `_raw_pull_required_reasons` (`:1209-1218`), matching against `_RAW_PULL_TRIGGER_REQUIRED_REASON_TOKENS` (`:118-128`, in-diff).
- **Evidence:** Detection is `any(token in warning_or_residual.lower())` over a fixed token set (`access_blocked/failed`, `capture_blocked/failed`, `capture_validity_not_supported`, `{instagram,retail,source}_structure_not_preserved`). `CleaningInputHandle` (`cleaning/models.py:200-211`) only forbids **Judgment** vocabulary in `warnings`/`residuals`/`raw_pull_triggers`; it does **not** require failed-capture posture to use any of these tokens. So a genuinely failed/blocked capture whose Cleaning warnings use other wording (e.g. `http_403`, `render_timeout`, `blocked_by_robots`, a localized string) produces **no** missing-trigger finding — a false negative on the exact posture E-04 protects. There is no shared constant binding the audit's token list to the producer's emitted vocabulary.
- **Test gap:** `test_periodic_audit_flags_failed_capture_handle_missing_raw_pull_trigger` proves *trigger-absent → finding* (good red), but does not assert that the **unmodified** failed handle (trigger present) passes clean — the positive control is only implicit. The canonical token `capture_validity_not_supported:rendered_dom_error_or_block_page_marker` is the one exercised.
- **Impact:** Enforcement strength is coupled to vocabulary alignment between the Cleaning producer and this token list; drift silently disables the check. Bounded today because the canonical token is covered and tested.
- **`minimum_closure_condition`:** Bind the audit token list to a shared producer-side constant, or have Cleaning emit a structured failed-capture posture flag the audit reads directly (rather than free-text substring); add an explicit positive-control assertion (failed handle *with* trigger ⇒ no finding).
- **`next_authorized_action`:** Advisory. No `patch_queue_entry`.
- **Verification expectation:** Same-check red-green possible for the positive control test once added.

---

## Observations / residual risk (not findings)

- **O-1 (E-06 scope, accepted):** `test_periodic_audit_execution_does_not_open_network_socket` monkeypatches `socket.socket` and `socket.create_connection` to raise, then asserts the full audit (including Lane B in-process projection/cleaning rebuilds) reaches `overall_status == "pass"`. This is a sound regression guard for **in-process socket-based** egress. It does **not** cover subprocess-spawned network, pre-bound `from socket import socket` references captured at import time, or non-socket async transports. The audit is file-based (frozen packet/projection/consolidation/ECR/Cleaning artifacts; Lane B re-runs the in-process smoke runner), so this is reasonable for the runner's scope and matches the prompt's own "cover only the periodic audit runner" framing. Residual is named, not a defect.
- **O-2 (Lane-A-only enforcement, mostly mitigated):** `_verify_cleaning_packet_traceability` — and therefore the new E-04/E-05/E-07-anchor checks — runs **only** for Lane A (`:360`). Lane B cleaning breakpoint (`:510-559`) only compares signatures. This is largely benign: `_cleaning_signature` (`:1620-1643`) includes `raw_pull_triggers` and `raw_anchor` (incl. `anchor_kind`), so a Lane-B rebuild that diverged in those would surface as a `cleaning_rebuild_signature_mismatch` (major). The transform `original_value` is **not** in the signature, but Lane B calls the smoke runner **without** `include_cleaning_transform_smoke=True` (`:519-522`), so the rebuild produces no transform ledger to drift. Net: the scoping is appropriate for this batch; note only that transform-ledger drift is not a Lane-B rebuild breakpoint in general.
- **O-3 (fail-closed confirmed — a positive):** The cross-cutting "malformed input causes an earlier exception that masks the specific finding yet still allows a clean status" risk does **not** materialize. Lane A wraps `_verify_cleaning_packet_traceability` in try/except that emits a `blocker` (`:368-376`) ⇒ `fail`; the contract validator (`:171`, `_validate_source_family_adapter_contract:632`) raises uncaught at startup ⇒ loud crash, no report. No malformed-input path yields a silent clean `pass`. Per-handle verifiers do not swallow their own exceptions, so any internal error bubbles to the lane blocker.
- **O-4 (E-07 contract is static self-consistency):** `_validate_source_family_adapter_contract` checks the adapter constant against `SUPPORTED_SOURCE_FAMILIES`, the mapping completeness, and that anchor kinds have validators — it does not validate adapters against real-world kinds beyond flagging *unknown* rows/anchors at runtime (which `_projection_rows_by_id:773` and `_verify_source_family_anchor_adapter_coverage:901` do correctly). `source_type` cannot escape the supported set: `_source_entries:1667` iterates `SUPPORTED_SOURCE_FAMILIES`, so the adapter dict lookups cannot `KeyError`.
- **O-5 (doctrine maturity, out of diff scope):** Per the authority digest, the source-family row/anchor rules are at satellite-promotion stage (cross-family validation pending). That is a doctrine-readiness caveat, not a code defect in this diff; the *code-level* E-07 enforcement is implemented and tested.
- **Lane-correctness (clean):** The diff introduces no credibility/salience/independence/demand/actionability/Judgment vocabulary as a Cleaning decision. It deals only in mechanical references (raw-pull triggers, original_value provenance, row/anchor kinds). The existing `_verify_no_judgment_reason_tokens` and the model's `_JUDGMENT_TOKENS` validators remain in force. Cleaning boundary preserved.

---

## Intended enforcement closure table

| ID | Goal | Status | Evidence / material variant remaining |
| --- | --- | --- | --- |
| **E-04** | failed/blocked capture posture ⇒ non-empty raw-pull trigger | `partially_closed` | Handle-level major finding fires and drives status; canonical token covered + red test passes. **Material variant:** detection is a fixed substring token list over free-text warnings/residuals with no model/producer binding (F-03) ⇒ false-negative on postures phrased with other vocabulary; positive control untested. |
| **E-05** | transform `original_value` ⇒ projection source-visible value or raw bytes (not invented) | `partially_closed` | Projection branch is exact set-membership (strong) and invented-value negative test passes. **Material variant:** raw branch is whole-file substring, not anchor-scoped, admits coincidental matches and is untested (F-01); projection branch accepts any leaf in the row incl. bool/number coercions (F-02). |
| **E-06** | periodic audit must not open a network socket | `closed` (for the bounded runner scope) | Socket creation patched to raise; full audit incl. Lane B rebuilds reaches `pass`. Reviewer reran the test ⇒ pass. **Named residual (O-1):** subprocess/pre-bound/non-socket egress not covered — acceptable per prompt scope. |
| **E-07** | every supported source family declares row+anchor kinds; unsupported rows/anchors flagged | `closed` | Contract validator requires non-empty row/anchor kinds + validators + exact mapping completeness; unsupported row kinds (major) and unsupported anchor kinds incl. Instagram `text_pattern` (major) and unknown families (major) are flagged; three red tests pass (reran ⇒ pass); `source_type` cannot escape the supported set by construction. Residual is doctrine-maturity only (O-5), outside diff scope. |

---

## Open questions / residual risk

1. **E-05 raw bar (F-01):** Is whole-file substring the intended "raw bytes" bar, or should provenance bind to the `raw_anchor` location? This is the load-bearing decision for whether E-05 is "closed." Owner/home-model call.
2. **E-04 vocabulary binding (F-03):** Is there (or should there be) a single owned constant or structured flag that both the Cleaning producer and this audit share for failed-capture posture? Without it, the token list and producer vocabulary can drift apart silently.
3. **E-05 field-level provenance (F-02):** Is row-level (not field-level) provenance the accepted core-v0 bar? If transforms could carry a source field path, both F-01 and F-02 tighten naturally.
4. **E-06 egress completeness:** Confirm the audit path never spawns a subprocess or uses a non-socket transport; if that can change, the guard needs broadening.

## Validation rerun status

- Reviewer-rerun: 7 new tests ⇒ **7 passed** (codex worktree, Python 3.11.15 / pytest 9.0.3).
- Author-supplied (not independently rerun): broader no-network Cleaning/ECR/projection suite, `runners/run_cleaning_spine_periodic_audit.py --help`, `git diff --check`. Reported as author-supplied.

## Strict-only blockers and non-claims

- This is **findings-only advisory** review. No formal Orca implementation-review authority was supplied; no formal PASS/READY/approval/mandatory-remediation/patch-queue is emitted.
- `patch_queue_entry`: **none** (read-only review; overlay validation-gates bar read-only reviews from emitting patch queues).
- Reviewer made no source edits, no commit/push/PR, ran no live capture / network / crawler / scheduler / API / storage / product-proof / Judgment checks.
- Strict claims NOT_CLAIMED: deployment readiness, resolver/plugin readiness, formal verdict, capture-to-cleaning live readiness.
- The only durable write this review performs is this report file at the prompt-named path.

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

- Original commission / review target:
  Cross-vendor (Anthropic/Claude reviewing OpenAI/GPT-family-authored) adversarial implementation/code review of the
  Cleaning-spine last enforcement batch, range 0d2f3be..aef50b05 (commits: raw-pull triggers, transform original-value
  provenance, no-network audit guard, source-family audit adapter coverage), on branch codex/cleaning-spine-continuation.
  Routed as implementation/code review (not single-artifact delegated review-and-patch) per the multi-file diff and the
  prompt's instruction. de_correlation_bar = cross_vendor_discovery.

- Implementation context, diff, and reviewed files:
  2 files changed, 640 insertions(+), 16 deletions(-).
  orca-harness/runners/run_cleaning_spine_periodic_audit.py (368/16); orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py (272/0).
  Target files unchanged since aef50b05 (only post-target commit is the prompt carrier). No output collision.

- Findings and implementation evidence:
  F-01 MAJOR (E-05): _transform_original_value_in_raw (runner:1153-1176) uses whole-file substring `original_value in raw_text`,
       not anchor-scoped; admits coincidental matches for short/common values; raw-acceptance branch untested.
       Authority: projection_doctrine:139-141 carry-or-residualize.
  F-02 MINOR (E-05): _source_visible_text_values (runner:1131-1151) flattens the whole row and coerces bool/number,
       accepting a match against any leaf in the row rather than the transformed field.
  F-03 MINOR (E-04): _verify_failed_capture_handle_raw_pull_trigger / _raw_pull_required_reasons (runner:1178-1218) detect
       failure posture via a fixed substring token list over free-text; CleaningInputHandle model (cleaning/models.py:200-211)
       does not bind failure postures to that vocabulary ⇒ false-negative risk; positive control untested.
  Observations: O-1 socket guard scope; O-2 Lane-A-only enforcement (mostly mitigated by _cleaning_signature + opt-in transforms);
       O-3 fail-closed confirmed (exceptions ⇒ blocker, not silent pass); O-4 static contract + source_type can't KeyError;
       O-5 doctrine maturity out of scope. Lane-correctness preserved.

- Intended enforcement closure statuses:
  E-04 partially_closed; E-05 partially_closed; E-06 closed (bounded scope, named residual); E-07 closed.

- Proposed patch / diff / exact requested edits, if authorized:
  None emitted (read-only review). Advisory remediation direction is in each finding's minimum_closure_condition.

- Citations:
  runner: 49, 171, 214-220, 360, 510-559, 632, 773, 901, 1048, 1109-1176, 1178-1218, 1620-1643, 1856-1862.
  models: 102-138, 181-219, 252-298, 301-329, 354-377. doctrine: projection_doctrine:139-141.

- Reviewer verdict:
  No blocker. 1 major + 2 minor advisory findings. E-06 and E-07 enforced (closed); E-04 and E-05 partially closed.
  The load-bearing decision is E-05 raw-provenance strength (F-01): whole-file substring vs anchor-scoped match.

- Validation evidence and not-run checks:
  Reviewer reran the 7 new tests ⇒ 7 passed (Python 3.11.15 / pytest 9.0.3). Broader suite, --help, git diff --check are
  author-supplied and not independently rerun. No live capture / network / scheduler / storage / product-proof / Judgment checks run.

- Residual risk:
  E-05 raw substring false-acceptance for short/common values; E-04 vocabulary-drift false negatives; E-06 non-socket/subprocess
  egress not covered; transform-ledger drift not a Lane-B rebuild breakpoint (currently moot).

- Blockers, off-scope flags, and not-proven boundaries:
  No blocker. Off-scope (not widened): unrelated Cleaning/Capture/Data Lake/scheduler/product-proof/Judgment review, live capture readiness.
  Not proven (advisory only): formal PASS/READY, deployment/resolver/plugin readiness, capture-to-cleaning live readiness.
  Authority files read via delegated digest (not line-by-line) except the re-verified carry-or-residualize quote.
```
