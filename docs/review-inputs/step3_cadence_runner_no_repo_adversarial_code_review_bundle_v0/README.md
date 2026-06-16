# Demand-Durability Cadence Runner (Step 3) — No-Repo Adversarial Code Review Bundle v0

```yaml
retrieval_header_version: 1
artifact_role: Review input
scope: No-repo delegated adversarial CODE review package for the demand-durability cadence runner (PR #132, option A operator-triggered per-slot).
use_when:
  - Commissioning the repo-blind cross-vendor advisory code review of the step-3 cadence runner.
  - Rechecking the exact target diff/after-state attachments and hashes supplied to the external controller.
authority_boundary: retrieval_only
branch_or_commit: demand-durability-cadence-runner-step3 @ 3cfdeeb494170d4d79783979f50d6cf7d001feed (PR #132, base main)
input_hashes:
  step3_target_scope.diff: 9089133d7ceaf30f06eb30e72b2bdcdabe9730b38389d129162121d9ef52926c
  after/orca-harness/runners/run_source_capture_durability_series.py: aaa9257ea98745e016053061033cc54cfd2adea0ec933e4f792701504a94b398
  after/orca-harness/tests/unit/test_source_capture_durability_series.py: e6d824e22a3bc354fbed2c8bfcbccca69075e645148681c431b5e3a7cb515d3f
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom no_repo code-review pack (target-scope diff + after-state files + embedded authority excerpts)
  edit_permission: read-only for delegate (no_repo, advisory-only); CA patch-only within the bounded scope after adjudication
  target_scope: the 2 files of PR #132, listed under Review Target
  dirty_state_checked: yes
  blocked_if_missing: target attachment hash mismatch, wrong branch/HEAD, missing bounded-scope contract
```

Workspace preflight observed by the package assembler (CA):

- assembler workspace: `C:\Users\vmon7\Desktop\projects\orca`
- target lane branch / HEAD: `demand-durability-cadence-runner-step3` @ `3cfdeeb494170d4d79783979f50d6cf7d001feed` (PR #132)
- base: `main`; PR mergeable state observed `CLEAN`; net change vs merge-base = the 2 new files only (+822, **zero** diff to `models.py`/`writer.py`).
- dirty-state allowance: review material generated from the pinned commit `3cfdeeb`, not a dirty worktree.

## Commission Binding

- overlay_status: `provisional_opt_in` — available only by explicit CA commission; not a bound formal review lane; not machine-routable.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- review_lane: **code** review posture, using `workflow-code-review` if available in the receiving runtime; otherwise advisory findings-only.
- access: `no_repo` — the delegate is **advisory-only and must not patch**; it returns findings. The CA applies accepted findings within the bounded scope, and a **bounded same-vendor post-patch recheck is required before keep**.
- mode: base-subagent.
- author_home_model_family: **Anthropic / Claude** (the build lane authored the change on a Claude model; CA is `claude-opus-4.8`).
- controller_model_family: **non-Anthropic vendor** (operator/tooling supplied; the overlay binds no concrete model ID).
- current_receiving_actor_role: controller, once this bundle is handed off.
- dispatch_mode: external-controller-courier.
- de_correlation_status: satisfied (`cross_vendor_discovery`) **only if** the actual controller vendor differs from Anthropic; otherwise record `same_vendor_sanity` or `self_fallback` and do **not** claim cross-vendor discovery / no-new-seam.

No runtime model is recommended, ranked, or selected by this package. The family field is a **who-constraint only**.

## Review Target

Target-scope diff (primary):

- `step3_target_scope.diff` — SHA256 `9089133d7ceaf30f06eb30e72b2bdcdabe9730b38389d129162121d9ef52926c` — the net change vs merge-base (2 files, +822 / −0).

After-state files (the source to review):

- `after/orca-harness/runners/run_source_capture_durability_series.py` — SHA256 `aaa9257ea98745e016053061033cc54cfd2adea0ec933e4f792701504a94b398` (the new runner; subcommands `init` / `run-slot` / `mark-gap` / `status`).
- `after/orca-harness/tests/unit/test_source_capture_durability_series.py` — SHA256 `e6d824e22a3bc354fbed2c8bfcbccca69075e645148681c431b5e3a7cb515d3f` (9 end-to-end tests against a local HTTP server).

Confirm each attachment you use matches its hash. If you cannot confirm, proceed advisory-only and say so.

## Bounded Scope

Editable scope for any later CA-applied patch: **the 2 files above only.**

Off-scope, **flag-only** (read-only — quoted below as authority, not as edit targets):

- the step-2 writer (`run_source_capture_http_packet.py`, already landed/reviewed), `cadence.py`, `models.py`, `packet_assembly.py`;
- the obligation contract, the durability pilot spec, and every other Orca source;
- all `.agents/workflow-overlay/` files; canonical / frozen / hash-pinned material; and every path the Orca safety rules forbid editing.

## Highest-Value Checks (be maximally adversarial; not exhaustive)

1. **Gap ≠ no-change — on BOTH gap paths.** An un-sampled slot (operator `mark-gap` skip, **and** a fetch failure) must be recorded as **un-observed / a visible limitation** — NEVER as "the source did not change." Verify both paths; verify the test for the fetch-failure path is real.
2. **Bounded / commissioned (Ob.1).** The series is bounded to `slot_count` and tied to a Decision Frame + fixed URL set — it cannot run unbounded or drift into an open crawler. Can any path exceed `slot_count`, or run without a Decision-Frame reference?
3. **INV-1.** No weight, score, ranking, threshold, trend, or durable-vs-hollow verdict anywhere — the runner records observed facts + limits only. (The non-claims disclaimer *names* these to deny them; that is not a violation.) Any comparison/judgment computed over observations?
4. **Correct reuse, no re-invention.** Cadence comes from `cadence.build_cadence_plan(...).to_dict()` and observations from the **step-2 writer's own durability flags** — not re-implemented cadence/pin math. Verify no shadow re-implementation that could drift.
5. **`SystemExit`-from-writer handling.** The step-2 writer's `main()` raises `SystemExit` on fetch failure; `run_slot` must catch it and record an `un_observed` `fetch_failed` gap — not crash, and not record a false success.
6. **Additive / no schema or manifest change.** No `SOURCE_CAPTURE_MANIFEST_VERSION` bump; no change to `models.py`/`writer.py` (the diff shows zero) — back-compat preserved.
7. **Not standing / not a daemon.** Option A operator-triggered per slot — no cron, no scheduled task, no long-running loop/queue. Verify nothing spawns a background process or standing infra.
8. **Series-state integrity.** Realized timings / lateness / gaps recorded as facts; `init` refuses to overwrite an existing series; no silent overwrite of a prior slot record; the index version is honest.
9. **Failure visibility / no false success.** Fetch failures, skipped slots, and errors are visible (non-zero exit / recorded limitation), never a faked-success packet or a swallowed error.
10. **Test quality.** Do the 9 tests actually **prove** the claims above (especially the two gap paths, bounded-to-`slot_count`, and INV-1), or are any shallow / false-passable?

---

## Authority Excerpts (the rules the change must conform to — repo-blind reviewer, read these as binding)

### A. Orca Agent Behavior Kernel + Smallest Complete Intervention (`AGENTS.md`)

> Default to the **smallest complete intervention** (narrowest sufficient scope; every changed line traces to the request or required validation). **Preserve real failure visibility; never create fake success paths.** `Complete` is load-bearing (no underfix); `Smallest` is load-bearing (no scope inflation, speculative abstraction, or standing infra beyond what is required).

### B. Ob.1 — Commissioning Gate (the bounded/commissioned rule this runner must honor)

> The capture must be tied to a Decision Frame. Minimum: the capture is connected to a specific decision question; the decision consequence/owner-context is known enough to keep capture from becoming **free-floating source collection**; the cutoff posture is known or explicitly unknown; **standing or opportunistic capture is rejected or routed outside this contract**. Failure mode: if there is no Decision Frame, Data Capture Spine has not started.

### C. Ob.17 — Demand-Durability Series Facts (the conditional obligation the per-observation writer satisfies)

> Applies ONLY to a commissioned demand-durability proxy series that observes a source repeatedly over time… records comparability pins (Element 1), series origin `series_id`/`cold_start_at`/`pre_coverage_history_posture` (Element 2), and the declared `intended_cadence` (Element 4), with **realized timings via per-observation `capture_time`/`recapture_time` and gaps recorded as visible limitations (an un-sampled gap is never "no change")**. These are observed facts, **never weights, scores, or a durable-vs-hollow demand verdict (INV-1)**. Series-diff (Element 3) is **deferred**. All fields are **additive and optional** (no `SOURCE_CAPTURE_MANIFEST_VERSION` bump).

### D. Step-3 Drift Guard (the build's hard constraints)

> **Commissioned capture only:** bounded series tied to a Decision Frame + fixed SKU/source set (Ob.1) — NOT standing/opportunistic crawling. **No-gate-defeat:** STOP at any auth/CAPTCHA/Cloudflare *challenge*. **INV-1:** facts + limits, never a verdict. **A gap is un-observed, never "no change."** **Series-diff (Element 3) STILL DEFERRED** — no change-detection here.

---

## Review Method For Controller

If your runtime can use `workflow-code-review`, **reference-load** it first, then **source-load** only the attachments in this bundle; declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE` before applying it. If `workflow-code-review` is unavailable, continue as an **advisory findings-only** code review and state `review_lane_status: workflow-code-review unavailable; advisory_no_skill_fallback` — do not claim a formal review lane ran.

Findings must be correctness, validation, bounded/commissioned, INV-1, gap-handling, or review-confidence issues supported by the attached source. Do **not** emit executor-ready patch steps; advisory remediation direction is allowed.

## Output Contract (return to the commissioning CA)

- `reviewed_by`: your model and version if known; else `unrecorded`.
- `authored_by`: `Anthropic Claude / exact model unrecorded` (the build lane), unless the operator supplies a more exact value.
- `de_correlation_bar`: `cross_vendor_discovery` (if your vendor ≠ Anthropic), else `same_vendor_sanity` or `self_fallback`.
- `source_context_status`, `review_lane_status`, attachment hash confirmation status for every attachment used.
- findings ordered by materiality; each: `severity` (`critical`/`major`/`minor` = priority labels only), `location`, `issue`, `evidence` (cite the attached source line **and** the conflicting authority excerpt), `impact`, `minimum_closure_condition` (end state, not how-to), `next_authorized_action`, advisory remediation direction.
- explicit off-scope flags, residual risk, and not-proven boundaries.

Use `NEEDS_ARCHITECTURE_PASS` if the problem is design-level rather than patch-level; if you use it, stop at findings and propose no patch.

## Non-Claims

This package is not validation, readiness, formal `PASS`, proof that the review ran, a no-new-seam claim, patch authorization for the external controller, or a runtime model recommendation. In `no_repo` mode the controller returns **findings only**; the CA applies any accepted patch within the bounded scope, and a **bounded same-vendor post-patch recheck is required before keep**. Landing PR #132 to `main` stays owner-gated.
