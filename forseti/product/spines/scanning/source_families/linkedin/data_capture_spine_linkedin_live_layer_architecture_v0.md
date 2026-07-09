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
status: ACCEPTED (v0.1) — owner sign-off 2026-06-10 (shape + agnosticism tradeoff + 3 review reframes); amended 2026-06-10 per assumption-gate (slice-3a → Opt 2 adapter contract record)
authored_by: claude-opus-4.x
review_provenance:
  - cross_vendor_discovery: openai/gpt-5.5 (advisory, no-repo) — 6 findings, all adjudicated/accepted (F5 modified)
  - same_vendor_recheck: anthropic/sonnet — clean closure, no regressions
  - assumption_gate (pre-build, source-read): slice-3a "harden existing core fields" verified_false — core lacks presence/no-bypass fields; amended to Opt 2 (attestation fields live in the adapter, not the core — honoring isolation)
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
Thin isolated live-adapter, one-way import, deletable. (A) Agnosticism = named fields + open enum axes + closed allowlist; **no `dict[str,Any]` bag**; new signal = new named, separately-walked field → "any authorized, named, minimized signal." (B) Live posture = validated predicates the validator hard-fails on (the `execution_authorized must be False` technique). [Amended per assumption-gate: the presence/no-bypass attestation fields do NOT exist in the core, and adding them would widen it — so they live as NEW validated fields in the **adapter** record (satellite), not on core fields. The core can carry only an optional consistency predicate on its existing `method_mode`/`optional_poc_risk_mode`.]

## 6. The three surfaced risks + resolutions
1. *Validators are post-hoc assertions, not a gate* → enforceable closure = **"adapter exported functions only ever return validated rows/dicts"** (checkable adapter-API invariant), NOT "raw constructor unreachable" (impossible in plain Python — public frozen dataclasses, constructed directly in tests). Import-boundary mechanism = separately-authorized option.
2. *Output-only rails; read-time over-capture* → the **observation contract (slice 3b) structurally excludes** retained profile bodies, contact data, follower/connection lists, relationship graphs, source content — minimization boundary at the 3b seam, before lowering. Runtime tape-test = slice 3c.
3. *Green no-live tests != live compliance* → explicit honesty boundary: a no-live test proves the rails reject bad rows; it does NOT prove the adapter only read/produced good things.

## 7. Core / satellite + invariants
Core (slices 1+2): no *new* live/ToS fields, no runtime; D5/POC tags frozen at current extent. Satellite (live adapter): one-way import, deletable.
Invariants: (1) one-way import; (2) no new live/ToS fields or runtime in core; (3) no free-form bag before the rails; (4) live posture = validated predicates with failing tests, **with the presence/no-bypass attestation fields living in the adapter record (satellite), never the core** [per assumption-gate]; (5)[3b+] adapter exports only validated rows/dicts; (6)[3b] observation contract excludes over-capture, [3c] runtime tape-test verifies read-time minimization.

## 8. Slice sequence — [amended per assumption-gate: 3a = Opt 2 adapter contract record, not core hardening]
- **3a — Minimal adapter contract record (new `linkedin_live_adapter/` package; NO runtime).** A frozen dataclass (e.g. `LiveAccessEnvelope`) carrying **presence-attested + no-entitlement-bypass + attended-mode as NEW validated predicate fields** (the validator hard-fails on them; the `execution_authorized must be False` technique). These fields live in the satellite, not the core — honoring isolation (the source read confirmed the core has no such fields, and adding them there would widen it). Reuse the slice-1 `LinkedInLaneError` + `assert_no_forbidden_output_fields` walk + key-allowlist; negatives-must-raise tests; no live code. **Optional ride-along:** a small core consistency predicate (POC-risk attended `method_mode` ⟺ `optional_poc_risk_mode=True`) — the only part enforceable on existing core fields with no widening; existing 54 tests must stay green.
  - *Why this amends F5/decision-5:* "harden existing, no new package" cannot carry presence/no-bypass — those fields are absent from the core and isolation forbids adding them there. A minimal adapter record is therefore required, but it is the **no-runtime contract** (slice-3a "no live code" spirit preserved).
- **3b — Observation contract + lowering + mint-path** (in the adapter): the named-field observation contract (with the §6.2 minimization boundary), its projection into the existing core types, and the §6.1 adapter-API mint-path invariant.
- **3c — Live driver/runtime.** Separately authorized, behind the legal/ToS hard gate, requiring the read-time-minimization tape-test.

## 9. Rejected / reserved / change triggers
Rejected: AO-3; foreign abstractions (`Protocol`/registry). Reserved: AO-2 (real 2nd signal source); separate live-posture package (decided at scoping). Would change it: near-term 2nd live source; core validators can't gate a live-only invariant; #3 anonymized-aggregate resolving toward individual aggregation.

## 10. Sign-off
Owner accepted (2026-06-10): the isolated thin-adapter shape; the named-field agnosticism tradeoff; isolation reframe (F1); ToS/reachability claim-status downgrade (F2). F3/F4/F6 folded as corrections. **Amendment (2026-06-10, per assumption-gate):** F5's "harden existing, no new package" superseded — slice-3a is a minimal adapter *contract* record (Opt 2), because the presence/no-bypass attestation fields are absent from the core and isolation forbids adding them there. Owner accepted Opt 2.

## 11. Non-claims
Planning authority only. NOT implementation/route/validation/readiness/promotion/live-runner. **Legal/ToS UNVERIFIED** — presence does not make automated access ToS-compliant; deferred hard gate. **Reachability is an owner-accepted, informal assumption**, outside this artifact's proven scope. "No black-letter ToS violations" is a chosen constraint, not a verified state. No live-layer code exists.
```
