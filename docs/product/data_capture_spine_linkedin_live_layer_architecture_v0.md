```yaml
retrieval_header_version: 1
artifact_role: Architecture decision record (ACCEPTED; planning authority for the LinkedIn live layer)
scope: >
  The accepted target architecture for the NEW "live" layer of the Orca LinkedIn
  discovery lane (reanchored from no-live to LIVE targeted discovery). Planning
  authority for the live-layer build: it binds the core/satellite boundary,
  invariants, and slice sequence. It is NOT implementation, a route, validation,
  readiness, or legal/ToS clearance.
authority_boundary: retrieval_only
status: ACCEPTED — owner sign-off 2026-06-10 (shape + agnosticism tradeoff + the 3 review-raised reframes)
authored_by: claude-opus-4.x
review_provenance:
  - cross_vendor_discovery: openai/gpt-5.5 (advisory, no-repo) — 6 findings, all adjudicated/accepted (F5 modified)
  - same_vendor_recheck: anthropic/sonnet — clean closure, no regressions
  - record: docs/review-outputs/adversarial-artifact-reviews/linkedin_live_layer_architecture_cross_vendor_review_v0.md
  - input_bundle: docs/review-outputs/linkedin_live_layer_architecture_v0_no_repo_review_bundle.zip (commit 01a063d)
conforms_to:
  - AGENTS.md (kernel; Smallest Complete Intervention)
  - docs/product/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md (Hard Stops, Non-Claims, person-basis, D5)
```

# Live LinkedIn-Layer — Architecture Decision Record (v0, ACCEPTED)

## 1. Decision
Where the ToS-risky live-access runtime sits relative to the proven no-live core
(slices 1+2), and how "signal-agnostic extraction" is represented at the seam.
**Accepted: AO-4-as-AO-1** — a thin, isolated live-adapter feeding the existing
core, with named-field agnosticism and validated-predicate posture.

## 2. Frozen envelope (constraints; claim-status in §11)
- Live, **owner-present/attended only** — (1) manual + tool-assist; (2) owner-present autonomous (runs only with confirmed presence; POC-risk accepted).
- Design constraints we operate under (NOT achievements — §11): no entitlement-gate bypass; no black-letter ToS violations; single real account.
- Signal-agnostic + fail-closed: general plumbing, rails decide what is allowed OUT (default-deny). Capability = **extract any *authorized, named, minimized* signal after schema review** — not generic capture.
- Targeted/frontier, NOT bulk. Legal/ToS = DEFERRED HARD graduation-gate. Promotion separate; discovery != capture.

## 3. Decisive invariant — isolation (precisely)
1. **One-way dependency** — live layer depends on core; core never depends on live layer (deletable: removing it leaves slices 1+2 green).
2. **No *additional* core widening** — no new live/ToS fields or runtime in core.

NOT conceptual purity: the core **already** carries D5 concepts — `MethodMode.{SUPERVISED_BROWSER_ASSIST_OPTIONAL_POC_RISK, OWNER_PRESENT_ATTENDED_AUTOMATION_OPTIONAL_POC_RISK}`, `SourceSurface.SUPERVISED_BROWSER_ASSIST`, `optional_poc_risk_mode` (`linkedin_lane/models.py`). Already-incurred coupling; do not expand.

## 4. Options
AO-1 thin adapter (**build**) · AO-2 parallel pipeline (reserved) · AO-3 extend-in-place (**rejected** — widens core coupling) · AO-4 hybrid (**stance**, = AO-1 + honest enum naming) · AO-5 validator-as-only-door (principle adopted, §6; standalone module deferred).

## 5. Target + refinements
Thin isolated live-adapter, one-way import, deletable. (A) Agnosticism = named fields + open enum axes + closed allowlist; **no `dict[str,Any]` bag**; new signal = new named, separately-walked field → "any authorized, named, minimized signal." (B) Live posture = validated predicates the validator hard-fails on, enforced on the D5/`optional_poc_risk` fields the core already has (the `execution_authorized must be False` technique).

## 6. The three surfaced risks + resolutions
1. *Validators are post-hoc assertions, not a gate* → enforceable closure = **"adapter exported functions only ever return validated rows/dicts"** (checkable adapter-API invariant), NOT "raw constructor unreachable" (impossible in plain Python — public frozen dataclasses, constructed directly in tests). Import-boundary mechanism = separately-authorized option.
2. *Output-only rails; read-time over-capture* → the **observation contract (slice 3b) structurally excludes** retained profile bodies, contact data, follower/connection lists, relationship graphs, source content — minimization boundary at the 3b seam, before lowering. Runtime tape-test = slice 3c.
3. *Green no-live tests != live compliance* → explicit honesty boundary: a no-live test proves the rails reject bad rows; it does NOT prove the adapter only read/produced good things.

## 7. Core / satellite + invariants
Core (slices 1+2): no *new* live/ToS fields, no runtime; D5/POC tags frozen at current extent. Satellite (live adapter): one-way import, deletable.
Invariants: (1) one-way import; (2) no new live/ToS fields or runtime in core; (3) no free-form bag before the rails; (4) live posture = validated predicates with failing tests; (5)[3b+] adapter exports only validated rows/dicts; (6)[3b] observation contract excludes over-capture, [3c] runtime tape-test verifies read-time minimization.

## 8. Slice sequence
- **3a — Harden the EXISTING envelope validators (no new package, no runtime).** Enforce presence/no-bypass/attended as predicates on the already-present D5/`optional_poc_risk` fields; negatives-must-raise tests; zero new schema; existing 54 tests must stay green. The separate-package question is deferred to scoping.
- **3b — Live-adapter package + observation contract (with §6.2 minimization boundary) + the §6.1 adapter-API mint-path.**
- **3c — Live driver/runtime.** Separately authorized, behind the legal/ToS hard gate, requiring the read-time-minimization tape-test.

## 9. Rejected / reserved / change triggers
Rejected: AO-3; foreign abstractions (`Protocol`/registry). Reserved: AO-2 (real 2nd signal source); separate live-posture package (decided at scoping). Would change it: near-term 2nd live source; core validators can't gate a live-only invariant; #3 anonymized-aggregate resolving toward individual aggregation.

## 10. Sign-off
Owner accepted (2026-06-10): the isolated thin-adapter shape; the named-field agnosticism tradeoff; isolation reframe (F1); ToS/reachability claim-status downgrade (F2); slice-3a-harden-not-new-package (F5). F3/F4/F6 folded as corrections.

## 11. Non-claims
Planning authority only. NOT implementation/route/validation/readiness/promotion/live-runner. **Legal/ToS UNVERIFIED** — presence does not make automated access ToS-compliant; deferred hard gate. **Reachability is an owner-accepted, informal assumption**, outside this artifact's proven scope. "No black-letter ToS violations" is a chosen constraint, not a verified state. No live-layer code exists.
```
