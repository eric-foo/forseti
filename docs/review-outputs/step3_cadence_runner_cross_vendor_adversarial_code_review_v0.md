# Demand-Durability Cadence Runner (Step 3) — Cross-Vendor Adversarial Code Review + CA Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (cross-vendor adversarial code review + home-model adjudication record)
scope: >
  Records the no_repo cross-vendor adversarial code review of the demand-durability cadence runner
  (PR #132) and the CA's home-model adjudication of its 3 findings + the applied bounded patch.
  Decision input only — not validation, readiness, a formal review-lane verdict, or merge authority.
authority_boundary: retrieval_only
branch_or_commit: demand-durability-cadence-runner-step3 (reviewed @ 3cfdeeb → patched @ 757c3075)
reviewed_by: OpenAI GPT-5 / Codex (exact runtime version unrecorded)
authored_by: Anthropic Claude / exact model unrecorded (the step-3 build lane)
de_correlation_bar: cross_vendor_discovery
use_when:
  - Checking how the cross-vendor code review of the step-3 cadence runner was adjudicated and what was kept.
  - Tracing the PR #132 immutable-slot + commissioning-gate hardening back to its review findings.
stale_if:
  - PR #132 is re-reviewed, materially re-patched, or merged.
  - A finding's adjudication is reopened by the owner.
```

## Commission

- Lane: delegated review-and-patch (`provisional_opt_in`); access `no_repo`; mode base-subagent; review lane **code** (`workflow-code-review`).
- Target: PR #132 (`demand-durability-cadence-runner-step3`) reviewed @ `3cfdeeb`; bundle `docs/review-inputs/step3_cadence_runner_no_repo_adversarial_code_review_bundle_v0/`; wrapper `docs/prompts/wrappers/step3_cadence_runner_no_repo_adversarial_code_review_wrapper_v0.md`.
- Reviewer confirmed all 3 attachment hashes MATCH; `cross_vendor_discovery`; advisory no-repo (`workflow-code-review` reference-loaded; no formal verdict).

## Reviewer findings (verbatim summary)

- Critical: none.
- **Major 1** — slot records can be silently overwritten after observation or gap (`run_slot`/`mark_gap` never require `status == pending`).
- **Major 2** — Decision-Frame binding is syntactic only; blank/whitespace commissioning fields can initialize a runnable series (Ob.1 undercut).
- **Minor 1** — the fetch-failure test proves the recorded gap outcome but not the `SystemExit` branch as an isolated contract.
- Off-scope flags: step-2 writer / `cadence.py` / `models.py` / manifest not inspected (no-repo boundary); no patch authored; no approval/readiness/landing claimed.

## CA adjudication (claims to adjudicate, not premises to inherit)

All three findings **verified real against the actual code** (the reviewer was repo-blind). Verdict + remedy:

| Finding | Verdict | Remedy kept |
| --- | --- | --- |
| **Major 1** | **Accept** — silent mutation of a recorded slot violates "no silent overwrite" + failure visibility | Pending-only guard in `run_slot` + `mark_gap`: a non-`pending` slot is refused (`ValueError` → CLI exit 2) before any mutation; a recorded slot is immutable. Tests prove all 4 transitions (observed→rerun, observed→gap, gap→run, gap→gap) rejected with the prior record byte-unchanged. |
| **Major 2** | **Accept** — Ob.1 ("tied to a Decision Frame; if none, Data Capture Spine has not started") | `build_series_index` rejects blank/whitespace `decision_frame_ref` / `decision_question` after `.strip()`; one builder-level gate covers both the direct and CLI `init` paths. Tests prove rejection (direct + CLI, no series state written). |
| **Minor 1** | **Accept** | Isolated test injects `writer_main` raising `SystemExit(3)` → asserts `un_observed`/`fetch_failed` gap, non-empty reason, no crash; the real-writer fetch-failure test retained. |

No finding rejected. **No `NEEDS_ARCHITECTURE_PASS`** — runner state/commissioning validation, within the 2 bounded files.

## What was kept (final state)

Patch commit `757c3075` on PR #132: `run_source_capture_durability_series.py` (+26, the three guards) and `test_source_capture_durability_series.py` (+173, the new tests). No change to `models.py`/`writer.py`/`cadence.py`/schema/manifest. Additive validation only; INV-1 preserved (guards mark themselves "state/input guard only").

## Post-patch recheck (bounded; same-vendor sanity)

- `de_correlation_bar` for the recheck: **`same_vendor_sanity`** (the CA, Anthropic, verified the lane's patch; bounded verification, not a cross-vendor discovery / no-new-seam claim).
- Result (verified against primary source): PR #132 HEAD = `757c3075`; diff scope = the 2 bounded files only; all three guards present and correct; 9 new negative test defs present; INV-1 preserved. Suite: **897 passed / 2 skipped** (882 + 15), reported by the patch lane via JUnit XML (the `-q` summary did not flush to redirected stdout on this Windows/pytest setup). No new blocker/major in the touched delta.

## Residual risk / not-proven

- Advisory review; the cross-vendor pass did not inspect the step-2 writer / `cadence.py` / `models.py` / manifest internals (no-repo boundary), and `build_cadence_plan` slot/jitter validation + the step-2 writer's gate-stop behavior are carried as authority, not re-proven by the reviewer.
- The suite-green claim rests on the patch lane's observed JUnit XML, not a CA re-run; the CA independently verified the code diff, guard logic, and test presence.
- PR #132 merge stays **owner-gated**. A novel cross-vendor-shared blind spot absent from both passes remains bounded-but-nonzero.

## operator_closeout_source

```yaml
operator_closeout_source:
  what_ran: cross-vendor (OpenAI GPT-5 / Codex) no_repo adversarial code review of PR #132 (demand-durability cadence runner).
  reviewer_findings: 0 critical, 2 major, 1 minor — series-state integrity + commissioning-gate enforcement; verified real.
  ca_adjudication: all 3 accepted; not an architecture pass.
  applied: patch 757c3075 — immutable-slot pending-only guard (Major 1), non-empty Decision-Frame/decision-question gate per Ob.1 (Major 2), isolated SystemExit-branch test (Minor 1); 2 files, +199; no schema/manifest change; INV-1 preserved.
  recheck: same_vendor_sanity bounded recheck passed; closure verified against primary source; suite 897/2.
  final_state: PR #132 OPEN @ 757c3075, hardened; merge owner-gated.
  blocked_next_step: owner merge of PR #132; the first real commissioned series (SKU + Decision Frame) remains a pending owner decision.
  not_claimed: validation, readiness, merge, no-new-seam, CA-independent suite re-run.
```

## Non-Claims

Decision input only. Not validation, readiness, formal `PASS`, proof the review ran, a no-new-seam claim, patch authority beyond the bounded CA-adjudicated application recorded here, merge authority, or runtime model routing. PR #132 landing to `main` stays owner-gated.
