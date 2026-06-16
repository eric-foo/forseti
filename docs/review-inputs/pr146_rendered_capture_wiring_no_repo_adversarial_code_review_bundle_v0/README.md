# Multi-Retailer Rendered Capture Wiring (PR #146) — No-Repo Adversarial Code Review Bundle v0

```yaml
retrieval_header_version: 1
artifact_role: Review input
scope: No-repo delegated adversarial CODE review package for wiring the rendered (CloakBrowser) writer to the demand-durability cadence runner (PR #146).
use_when:
  - Commissioning the repo-blind cross-vendor advisory code review of the PR #146 rendered-capture wiring.
  - Rechecking the exact target diff / after-state attachments and hashes supplied to the external controller.
authority_boundary: retrieval_only
branch_or_commit: rendered-multiretailer-capture-v0 @ c1c51144467fa5ee95c4b260011f4655ac67bb27a (PR #146, base main)
input_hashes:
  pr146_target_scope.diff: 9e2f1920135493e3791b622c1c87bbc0c443301c0bee499f8666d1576122aab5
  after/orca-harness/source_capture/cli_support.py: 90041e5aeae89253c02a260a2b5ac549fedf0bbc3c4b2ae4616dfa28e0e0b34f
  after/orca-harness/runners/run_source_capture_cloakbrowser_packet.py: 80388f9ceedad43bd2d6983f7fcefeb2434acda22bf08e042b35f29edd5b8bf1
  after/orca-harness/runners/run_source_capture_durability_series.py: fb5390e6a97ec40c44b3d247cc699916e9c6232972c460554690f26e6a99a578
  after/orca-harness/runners/run_source_capture_http_packet.py: 2adbfa1128544607a28959ced8efd5238aa053697d48b3def00baaa060463836
  after/orca-harness/tests/unit/test_durability_multiretailer_rendered_wiring.py: a6bbf88ff1a19f4c0edf7661b7fdac7a3745eb8e69562c0b854480af9f9aba64
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom no_repo code-review pack (target-scope diff + after-state files + embedded authority excerpts)
  edit_permission: read-only for delegate (no_repo, advisory-only); CA patch-only within the bounded scope after adjudication
  target_scope: the 5 files of PR #146, listed under Review Target
  dirty_state_checked: yes
  blocked_if_missing: target attachment hash mismatch, wrong branch/HEAD, missing bounded-scope contract
```

Workspace preflight observed by the package assembler (CA):

- assembler workspace: `C:\Users\vmon7\Desktop\projects\orca`
- target lane branch / HEAD: `rendered-multiretailer-capture-v0` @ `c1c51144` (PR #146)
- base: `main` — the lane was rebased onto current `origin/main`; upstream touched **none** of the 5 files (clean), so the diff is the change in isolation.
- dirty-state allowance: review material is generated from the pinned commit `c1c51144`, not from a dirty worktree.

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

- `pr146_target_scope.diff` — SHA256 `9e2f1920135493e3791b622c1c87bbc0c443301c0bee499f8666d1576122aab5` — the full commit diff (5 files, +553 / −142).

After-state files (the post-change source to review):

- `after/orca-harness/source_capture/cli_support.py` — SHA256 `90041e5aeae89253c02a260a2b5ac549fedf0bbc3c4b2ae4616dfa28e0e0b34f`
- `after/orca-harness/runners/run_source_capture_cloakbrowser_packet.py` — SHA256 `80388f9ceedad43bd2d6983f7fcefeb2434acda22bf08e042b35f29edd5b8bf1`
- `after/orca-harness/runners/run_source_capture_durability_series.py` — SHA256 `fb5390e6a97ec40c44b3d247cc699916e9c6232972c460554690f26e6a99a578`
- `after/orca-harness/runners/run_source_capture_http_packet.py` — SHA256 `2adbfa1128544607a28959ced8efd5238aa053697d48b3def00baaa060463836`
- `after/orca-harness/tests/unit/test_durability_multiretailer_rendered_wiring.py` — SHA256 `a6bbf88ff1a19f4c0edf7661b7fdac7a3745eb8e69562c0b854480af9f9aba64`

Confirm each attachment you use matches its hash. If you cannot confirm, proceed advisory-only and say so.

## What The Change Does (context, not authority)

PR #146 wires a **rendered (CloakBrowser) writer** to the step-3 demand-durability cadence runner so the SAME SKU can be captured across JS / embedded-JSON retail PDPs (Ulta `__APOLLO_STATE__`, Sephora Bazaarvoice) that the `direct_http` (stdlib urllib) writer cannot read. It is **wiring only** — no live capture. Three moves:

1. **`cli_support.py`** — extracts the demand-durability CLI contract (`add_durability_arguments`, `build_intended_cadence`, `require_series_identity`, `CADENCE_SUBFLAG_ATTRS`, `DURABILITY_FIELD_ATTRS`) into the shared helper both writers import, so the two writers share one definition and cannot drift.
2. **`run_source_capture_http_packet.py`** (the `direct_http` writer) — refactored to import those helpers instead of defining them locally (the −142 is the deleted local copies; intended behavior-preserving).
3. **`run_source_capture_cloakbrowser_packet.py`** (the rendered writer) — exposes the SAME durability flag surface and populates Ob.17: the four Element-1 pins ride on the `SourceCaptureSlice`; `series_id` + Element-2 origin postures + Element-4 `intended_cadence` ride on the packet (pass-through to `write_local_source_capture_packet`, which already accepts them).
4. **`run_source_capture_durability_series.py`** (the cadence runner) — a `WRITER_MAINS` registry + `run-slot --writer {direct_http,cloakbrowser}` (default `direct_http`) + a repeatable `--writer-arg` passthrough appended to the forwarded writer argv; `run_slot` gains `writer_extra_argv`.

## Bounded Scope

Editable scope for any later CA-applied patch: **the 5 files above only.**

Off-scope, **flag-only** (read-only — quoted below / referenced as authority, not as edit targets):

- `orca-harness/source_capture/models.py` (the schema — already merged; the writer SETS its Ob.17 fields, does not reshape it), `writer.py`, `cadence.py`, `packet_assembly.py`, `source_capture/adapters/cloakbrowser_snapshot.py` (the rendered adapter — already merged), and every other Orca source;
- the demand-durability spec, the obligation contract, and the source-access boundary decision;
- all `.agents/workflow-overlay/` files; canonical / frozen / hash-pinned material; and every path the Orca safety rules forbid editing.

If the correct fix is off-scope (e.g., a schema or adapter change, or a design-level rework), **flag it — do not patch it** — and consider `NEEDS_ARCHITECTURE_PASS`.

## Highest-Value Checks (be maximally adversarial; not exhaustive)

1. **Same-interface guarantee (the core claim).** The cadence runner forwards ONE fixed durability argv to whichever writer `--writer` selects. Does the rendered writer accept **every** flag the runner can forward — `--series-id`, all `--intended-cadence-*`, `--session/locale/currency/variant-pin` (+`-unknown-reason`/`-not-applicable-reason`), `--cold-start-at`, `--pre-coverage-history-posture`? A single missing/renamed flag → argparse aborts the rendered writer (exit 2) and the slot is silently mis-recorded. Is the drift-guard test (`test_rendered_and_direct_writers_expose_identical_durability_flags`) actually exhaustive, or does its substring filter (`series-id`/`intended-cadence`/`-pin`/`cold-start`/`pre-coverage`) miss a flag that differs outside those tokens?
2. **Behavior-preserving refactor of `direct_http`.** The −142 deletes the local helper copies from `run_source_capture_http_packet.py` and imports the shared ones. Are the extracted `cli_support` functions **byte-equivalent in behavior** to the originals (same flag names, defaults, `build_intended_cadence` validation order, `require_series_identity` gate, the `*_ATTRS` tuples)? Any subtle change (a dropped flag, a changed default, a reordered validation) silently regresses the already-merged `direct_http` writer.
3. **No state-model / schema / manifest change (hard constraint).** Does `--writer` / `--writer-arg` / `writer_extra_argv` touch the **series index schema** or the slot record shape in any way? Is `SOURCE_CAPTURE_MANIFEST_VERSION` genuinely un-bumped? The runner's series state must be byte-identical to before for a `direct_http` run.
4. **Ob.17 placement on the rendered writer.** Do the 4 pins land on `SourceCaptureSlice` and `series_id`/`cold_start_at`/`pre_coverage_history_posture`/`intended_cadence` on the packet — **never** smuggled into `capture_context` or metadata? Is `build_optional_fact` used so a source-absent pin is `unknown_with_reason`/`not_applicable`, **never a fabricated fact**?
5. **`--writer-arg` passthrough safety.** It is appended **verbatim** to the writer argv. Can a passthrough arg (a) override a runner-forwarded flag (argparse last-wins) and corrupt the series identity/pins for a slot; (b) inject a flag that defeats an anti-bot/auth gate or changes the source-access posture; or (c) smuggle a second `--url`/`--output` that redirects the capture? Is the “each packet self-records its capture config in metadata, so per-slot knobs stay auditable” claim actually true for the cloakbrowser path, or can a knob change capture behavior without leaving a trace?
6. **Import safety / no runtime acquisition.** The cadence runner now imports the cloakbrowser writer's `main` at module top. Confirm this does **not** transitively import `cloakbrowser` / `playwright` / network libs at load time (the rendered adapter must import the runtime lazily, only at capture time). A module-load import of the runtime would break every offline/CI run that lacks the optional dependency and violate the no-runtime-acquisition contract.
7. **Gap ≠ no-change preserved.** When the rendered writer fails — `cloakbrowser_dependency_unavailable`, an access-block page, a timeout, or argparse rejecting a forwarded flag — does the runner record an **un-observed gap** (never a fake success, never "no change")? Trace the `SystemExit`/non-zero/`PATCH`-style failure paths through `run_slot`.
8. **INV-1.** Is anything in the wiring a weight, score, threshold, ranking, or durable-vs-hollow verdict? It must all be observed facts + limits forwarded verbatim.
9. **Back-compat / default writer.** With no `--writer`, does `run-slot` behave **exactly** as before (direct_http)? Does a non-durability rendered capture (no durability flags) leave all Ob.17 fields `None` and write a valid packet?
10. **Test quality.** Do the 7 tests in `test_durability_multiretailer_rendered_wiring.py` actually **prove** the claims (identical flags; Ob.17 placement incl. the `variant_pin` honest-gap status `unknown_with_reason`; series-identity gate exits 2; `--writer` routing; `--writer-arg` appended; default = direct_http), or are any shallow / false-passable (e.g., asserting presence without placement, or routing without confirming the *other* writer was not used)?

---

## Authority Excerpts (the rules the change must conform to — repo-blind reviewer, read these as binding)

### A. Orca Agent Behavior Kernel + Smallest Complete Intervention (`AGENTS.md`)

> Default to the **smallest complete intervention** (narrowest sufficient scope; every changed line traces to the request or required validation). **Preserve real failure visibility; never create fake success paths.** `Complete` is load-bearing (no underfix); `Smallest` is load-bearing (no unrelated cleanup, speculative abstraction, or scope inflation).

### B. The binding spec — required behavior (`demand_durability_multi_retailer_rendered_capture_spec_v0.md`)

> **Same packet shape, per retailer.** Each authorized retailer is captured into the **same `SourceCapturePacket`** the `direct_http` path produces — the Ob.6 fidelity dimensions and the Ob.17 durability fields (Element 1 pins, Element 2 series origin, Element 4 cadence) are populated as first-class schema fields, so the cadence runner treats a rendered observation identically to a `direct_http` one.
>
> **Wired to the cadence runner's existing seam.** The runner already accepts an injectable `writer_main` (it defaults to the `direct_http` writer). The rendered path must be a writer with the **same interface** so the runner can invoke it per slot per retailer — **no re-architecture of the runner, no schema change, no `SOURCE_CAPTURE_MANIFEST_VERSION` bump.**
>
> **Source-access posture — public + measured-ToS, NOT entitlement. No-gate-defeat: STOP at any auth / CAPTCHA / Cloudflare *challenge*** and record the limitation.
>
> **Non-goals:** not series-diff (Element 3, deferred); not a new schema, manifest bump, or change to the cadence runner's state model; **not any demand verdict (INV-1 — capture records observed facts + limits only).**

### C. Commission hard constraints (this build)

> **Source-access boundary + NO-GATE-DEFEAT:** anti-bot OK; STOP at any auth / CAPTCHA / Cloudflare challenge — never defeat a gate. **INV-1:** capture records observed facts + limits only; no demand verdict, no scoring. **Additive:** no schema change, **no `SOURCE_CAPTURE_MANIFEST_VERSION` bump, no change to the runner's state model.** One series PER retailer (the same SKU across retailers is parallel per-retailer series, never one `series_id` spanning retailers).

### D. No-runtime-acquisition import contract (the already-merged cloakbrowser contract test)

> The CloakBrowser adapter **and** `run_source_capture_cloakbrowser_packet.py` must contain **no** top-level import of runtime-acquisition roots (`cloakbrowser`, `playwright`, `httpx`, `socket`, `requests`, …); the runtime is imported lazily only at capture time. A module-load import breaks offline/CI and the dependency-optional contract.

---

## Review Method For Controller

If your runtime can use `workflow-code-review`, **reference-load** it first, then **source-load** only the attachments in this bundle; do not apply the method until you have declared `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. If `workflow-code-review` is unavailable, continue as an **advisory findings-only** code review from the attached diff + after-state files and state `review_lane_status: workflow-code-review unavailable; advisory_no_skill_fallback` — do not claim a formal review lane ran.

Findings must be correctness, validation, back-compat, INV-1, security/gate-defeat, or review-confidence issues supported by the attached source. Do **not** emit executor-ready patch steps; advisory remediation direction is allowed.

## Output Contract (return to the commissioning CA)

- `reviewed_by`: your model and version if known; else `unrecorded`.
- `authored_by`: `Anthropic Claude / exact model unrecorded` (the build lane), unless the operator supplies a more exact value.
- `de_correlation_bar`: `cross_vendor_discovery` (if your vendor ≠ Anthropic), else `same_vendor_sanity` or `self_fallback`.
- `source_context_status`: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- `review_lane_status`: per above.
- attachment hash confirmation status for every attachment used.
- findings ordered by materiality; for each: `severity` (`critical`/`major`/`minor` = priority labels only), `location` (file + line in the attached source), `issue`, `evidence` (cite the attached source line **and** the conflicting authority excerpt), `impact`, `minimum_closure_condition` (end state, not how-to), `next_authorized_action`, advisory remediation direction.
- explicit off-scope flags, residual risk, and not-proven boundaries.

Use `NEEDS_ARCHITECTURE_PASS` if the problem is design-level rather than patch-level; if you use it, stop at findings and propose no patch.

## Non-Claims

This package is not validation, readiness, formal `PASS`, proof that the review ran, a no-new-seam claim, patch authorization for the external controller, or a runtime model recommendation. In `no_repo` mode the controller returns **findings only**; the CA applies any accepted patch within the bounded scope, and a **bounded same-vendor post-patch recheck is required before keep**. Landing PR #146 to `main` stays owner-gated.
