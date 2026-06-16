# Demand-Durability Series Writer (Step 2) — No-Repo Adversarial Code Review Bundle v0

```yaml
retrieval_header_version: 1
artifact_role: Review input
scope: No-repo delegated adversarial CODE review package for the demand-durability series writer (PR #128, Ob.17 Elements 1/2/4).
use_when:
  - Commissioning the repo-blind cross-vendor advisory code review of the step-2 series writer.
  - Rechecking the exact target diff/after-state attachments and hashes supplied to the external controller.
authority_boundary: retrieval_only
branch_or_commit: demand-durability-series-writer-step2 @ a0b225315f6e293cbd61af01f1cf29fc863aa83c (PR #128, base main)
input_hashes:
  step2_target_scope.diff: e93a36287dccf5ae42aa64e6c2050bf47b62a4ea304e38cb556bfa0dacae17ff
  after/orca-harness/source_capture/writer.py: 7b6ac92fd41f5086dd05c6f449fbd1fde2fefc23688be1e63a26e9a2092067a4
  after/orca-harness/runners/run_source_capture_http_packet.py: 7f5ca0af69170ca8cf7fa36b9a99106d8878e1d19760c122fa395e5bbdbfe4e7
  after/orca-harness/tests/unit/test_source_capture_direct_http.py: cbc82a6c40fc349c39cea67b049976672b6d4d4f3007c178da13de9181f88a38
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom no_repo code-review pack (target-scope diff + after-state files + embedded authority excerpts)
  edit_permission: read-only for delegate (no_repo, advisory-only); CA patch-only within the bounded scope after adjudication
  target_scope: the 3 files of PR #128, listed under Review Target
  dirty_state_checked: yes
  blocked_if_missing: target attachment hash mismatch, wrong branch/HEAD, missing bounded-scope contract
```

Workspace preflight observed by the package assembler (CA):

- assembler workspace: `C:\Users\vmon7\Desktop\projects\orca`
- target lane branch / HEAD: `demand-durability-series-writer-step2` @ `a0b225315f6e293cbd61af01f1cf29fc863aa83c` (PR #128)
- base: `main` (branch base `421b4a11`, an ancestor of current `origin/main`; clean-merge — upstream touched none of the 3 files)
- dirty-state allowance: review material is generated from the pinned commit `a0b22531`, not from a dirty worktree.

## Commission Binding

- overlay_status: `provisional_opt_in` — available only by explicit CA commission; not a bound formal review lane; not machine-routable.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- review_lane: **code** review posture, using `workflow-code-review` if available in the receiving runtime; otherwise advisory findings-only.
- access: `no_repo` — the delegate is **advisory-only and must not patch**; it returns findings. The CA applies accepted findings within the bounded scope, and a **bounded same-vendor post-patch recheck is required before keep**.
- mode: base-subagent.
- author_home_model_family: **Anthropic / Claude** (the build lane that authored the change ran on a Claude model; CA is `claude-opus-4.8`).
- controller_model_family: **non-Anthropic vendor** (operator/tooling supplied; the overlay binds no concrete model ID).
- current_receiving_actor_role: controller, once this bundle is handed off.
- dispatch_mode: external-controller-courier.
- de_correlation_status: satisfied (`cross_vendor_discovery`) **only if** the actual controller vendor differs from Anthropic; otherwise record `same_vendor_sanity` or `self_fallback` and do **not** claim cross-vendor discovery / no-new-seam.

No runtime model is recommended, ranked, or selected by this package. The family field is a **who-constraint only**.

## Review Target

Target-scope diff (primary):

- `step2_target_scope.diff` — SHA256 `e93a36287dccf5ae42aa64e6c2050bf47b62a4ea304e38cb556bfa0dacae17ff` — the full commit diff (3 files, +252 / −0).

After-state files (the post-change source to review):

- `after/orca-harness/source_capture/writer.py` — SHA256 `7b6ac92fd41f5086dd05c6f449fbd1fde2fefc23688be1e63a26e9a2092067a4`
- `after/orca-harness/runners/run_source_capture_http_packet.py` — SHA256 `7f5ca0af69170ca8cf7fa36b9a99106d8878e1d19760c122fa395e5bbdbfe4e7`
- `after/orca-harness/tests/unit/test_source_capture_direct_http.py` — SHA256 `cbc82a6c40fc349c39cea67b049976672b6d4d4f3007c178da13de9181f88a38`

Confirm each attachment you use matches its hash. If you cannot confirm, proceed advisory-only and say so.

## Bounded Scope

Editable scope for any later CA-applied patch: **the 3 files above only.**

Off-scope, **flag-only** (read-only — quoted below as authority, not as edit targets):

- `orca-harness/source_capture/models.py` (the hardened schema — already merged; the writer SETS its fields, does not reshape it);
- the obligation contract, the durability pilot spec, `cadence.py`, `packet_assembly.py`, and every other Orca source;
- all `.agents/workflow-overlay/` files; canonical / frozen / hash-pinned material; and every path the Orca safety rules forbid editing.

## Highest-Value Checks (be maximally adversarial; not exhaustive)

1. **Additive-optional / back-compat.** Does a **non-durability** capture truly leave all 8 fields `None`? Can any code path set one unintentionally? Is `SOURCE_CAPTURE_MANIFEST_VERSION` genuinely **un-bumped**, and do existing packets/manifests stay valid? (Back-compat break = breaks every prior packet + the 861-test baseline.)
2. **Schema-fields-not-`capture_context`.** Do the 8 fields land on `SourceCaptureSlice` / `SourceCapturePacket`, **never** `capture_context`? Verify the runner wires them to the model, and that the test's "no leak into `capture_context`" assertion is real (asserts placement, not just presence).
3. **INV-1.** Are the fields forwarded **verbatim as observed facts** — no weight, score, threshold, ranking, or durable-vs-hollow verdict smuggled into the runner, the cadence builder, or the postures?
4. **`intended_cadence` shape fidelity.** Is it built from `cadence.build_cadence_plan(...).to_dict()` (canonical), not a hand-invented dict that can drift from `CadencePlan`?
5. **Honest-gap wiring (Ob.17).** Do pins/postures use the honest-gap helper so a source-absent pin is `unknown_with_reason` / `not_applicable` (discharged `unavailable_by_source`) and **never written as a fabricated fact**? Any silent default that invents a value?
6. **Validation / no false-success.** Do the fields validate under the hardened `models.py` (`extra="forbid"`; correct `VisibleFact | None` / `dict | None` / `str | None` types)? Any path that fakes success or hides a failure?
7. **Series-diff (Element 3) NOT built.** Confirm no cross-observation change-detection/diff was smuggled in (it is deferred).
8. **No-gate-defeat.** No anti-bot / CAPTCHA / Cloudflare-challenge bypass added.
9. **Test quality.** Do the 2 subprocess tests actually **prove** the claims (all fields set as schema fields + no `capture_context` leak; non-durability `None` + manifest unchanged), or are they shallow / false-passable?
10. **Runner CLI / downstream executability.** Are the flags coherent and is failure visible (not faked) for a real operator driving a durability series?

---

## Authority Excerpts (the rules the change must conform to — repo-blind reviewer, read these as binding)

### A. Orca Agent Behavior Kernel + Smallest Complete Intervention (`AGENTS.md`)

> Default to the **smallest complete intervention** (narrowest sufficient scope; every changed line traces to the request or required validation). **Preserve real failure visibility; never create fake success paths.** `Complete` is load-bearing (no underfix); `Smallest` is load-bearing (no unrelated cleanup, speculative abstraction, or scope inflation).

### B. Ob.17 — Demand-Durability Series Facts (the conditional obligation this writer satisfies)

> This obligation applies ONLY to a commissioned demand-durability proxy series (price, availability, search-interest, review) that observes a source repeatedly over time… It does not apply to one-shot captures, which leave these facts unset.
>
> For such a series, Capture must record: the comparability pins held across the series — `session_visibility_pin`, `locale_pin`, `currency_pin`, `variant_pin` (Element 1), per observed slice. A pin the source does not expose is `unknown_with_reason` / `not_applicable`, and its capture obligation is discharged `unavailable_by_source` — **never written as a fact status**. The series origin — `series_id`, `cold_start_at`, `pre_coverage_history_posture` (Element 2)… The declared sampling cadence — `intended_cadence` (Element 4), with realized timings via per-observation `capture_time` / `recapture_time` and gaps recorded as visible limitations (an un-sampled gap is never "no change").
>
> These are observed facts that fix comparability and coverage extent; they are **never weights, scores, or a durable-vs-hollow demand verdict (INV-1)**. The series-level recapture-diff (Element 3) is **deferred**. All Element 1/2/4 fields are **additive and optional**: existing manifests stay valid with them unset (**no `SOURCE_CAPTURE_MANIFEST_VERSION` bump**).

### C. Step-2 Drift Guard (the build's hard constraints)

> **Additive-optional / back-compat:** new fields default `None`; no manifest bump. **INV-1:** fields are observed facts, never weights/scores/verdicts. **No-gate-defeat:** honest UA OK; STOP at any auth/CAPTCHA/Cloudflare *challenge*. **Schema fields, not `capture_context`** (do not copy the pilot's stopgap). **Series-diff (Element 3) is DEFERRED** — do not build it.

---

## Review Method For Controller

If your runtime can use `workflow-code-review`, **reference-load** it first, then **source-load** only the attachments in this bundle; do not apply the method until you have declared `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. If `workflow-code-review` is unavailable, continue as an **advisory findings-only** code review from the attached diff + after-state files and state `review_lane_status: workflow-code-review unavailable; advisory_no_skill_fallback` — do not claim a formal review lane ran.

Findings must be correctness, validation, back-compat, INV-1, or review-confidence issues supported by the attached source. Do **not** emit executor-ready patch steps; advisory remediation direction is allowed.

## Output Contract (return to the commissioning CA)

- `reviewed_by`: your model and version if known; else `unrecorded`.
- `authored_by`: `Anthropic Claude / exact model unrecorded` (the build lane), unless the operator supplies a more exact value.
- `de_correlation_bar`: `cross_vendor_discovery` (if your vendor ≠ Anthropic), else `same_vendor_sanity` or `self_fallback`.
- `source_context_status`: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- `review_lane_status`: per above.
- attachment hash confirmation status for every attachment used.
- findings ordered by materiality; for each: `severity` (`critical`/`major`/`minor` = priority labels only), `location`, `issue`, `evidence` (cite the attached source line **and** the conflicting authority excerpt), `impact`, `minimum_closure_condition` (end state, not how-to), `next_authorized_action`, advisory remediation direction.
- explicit off-scope flags, residual risk, and not-proven boundaries.

Use `NEEDS_ARCHITECTURE_PASS` if the problem is design-level rather than patch-level; if you use it, stop at findings and propose no patch.

## Non-Claims

This package is not validation, readiness, formal `PASS`, proof that the review ran, a no-new-seam claim, patch authorization for the external controller, or a runtime model recommendation. In `no_repo` mode the controller returns **findings only**; the CA applies any accepted patch within the bounded scope, and a **bounded same-vendor post-patch recheck is required before keep**. Landing PR #128 to `main` stays owner-gated.
