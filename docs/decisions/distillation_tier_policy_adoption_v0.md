# Distillation Tier-Policy Adoption — Orca (prepare-only)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Independent proof and adoption record for the distillation tier-enforcement
  mechanism: each binding declares a per-tier verification requirement; the
  distiller enforces it and caps cells that do not meet the declared requirement.
  Carries the proposed per-tier policy for the orca-harness code binding
  (three tiers: asserted / recorded / probed); records the 4-case proof run;
  notes one real finding and one advisory flag. Policy revised 2026-06-11 to
  add `recorded` (middle tier) based on courier feedback: the original policy
  collapsed partial-verification into `asserted` ("no test") incorrectly.
use_when:
  - Distilling a new cell into any Orca binding — apply per-tier requirement check.
  - Auditing whether an existing cell's tier claim is accurate.
  - Ratifying the per-tier policy for a specific binding (owner action).
authority_boundary: retrieval_only
open_next:
  - docs/decisions/distillation_binding_orca_harness_code_v0.md
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md
stale_if:
  - The orca-harness code binding's tier_policy is authoritatively declared
    inside the binding itself (supersedes the policy section here).
  - An owner ratifies the tier corrections for probe-gate-total-function
    (this record becomes the ratification evidence and retires the "pending" flag).
```

## Status

**PROPOSED ADOPTION — pending owner ratification of the per-tier policy.**

- The mechanism (enforce the binding's declared per-tier requirement; cap to
  the highest tier met) is adopted as Orca distiller discipline: when processing
  any cell for admission or ingest, the distilling agent checks the binding's
  declared tier requirement before accepting the claimed tier.
- The per-tier policy for the orca-harness code binding is *proposed* here.
  It is owner-gated before it becomes binding Orca authority. No cell tier is
  changed in this record; corrections are listed for the owner to ratify.
- This record does **not** install anything into the always-on overlay, edit any
  binding file, change any always-on overlay rule, build any substrate, or
  authorize implementation.

## Provenance

Received via courier (parallel distillation adopter channel).

Problem named by courier: distillation let confidence outrun proof — a cell
stamped `probed` with the verify-pair never run; a candidate called "most
important" on a single data point later refuted by ground truth. Root cause:
a rule claiming more verification than it has.

Goal: cells carry only the tier their evidence actually supports.

Mechanism (portable, from courier): the distiller enforces the binding's
declared per-tier requirement. A cell may claim a tier only if its verification
meets that tier's requirement; otherwise cap to the highest tier met. The
distiller reads the requirement from the binding — it does not hardcode one.

Policy (owner's call, Orca-local): declared below, per binding. Ours to decide,
not to copy.

## Per-tier policy — orca-harness code binding

The orca-harness code binding's verification substrate is the deterministic
pytest suite. Per-tier requirements for this binding:

```
asserted:   claim stated in the binding; no automated test in the current suite
            exercises the specific behavior being claimed.

recorded:   under-case test EXISTS in the current suite and runs green;
            over-edge test is NOT YET in the suite (owed). The under-case
            direction is verified; the over-edge direction is not.

probed:     under-case test AND over-edge test both (a) exist in the current
            suite and (b) run green. Structural code guards (ValueError, raise,
            assert) do NOT satisfy the over-edge requirement unless a test in
            the suite explicitly exercises that code path.

held:       outcome of the ingest check when the claimed tier's requirement is
            not met. Do not admit the cell to the binding at the claimed tier.
            Hold and note the gap; re-enter when the test is added.
```

`accepted-orca-gate` is not used for orca-harness code binding cells; all real
cells here use `asserted`, `recorded`, or `probed` (sourced from test evidence,
not from an existing accepted overlay rule).

**Owner ratification needed:** this policy is proposed and recorded here; it
becomes binding Orca authority when the owner accepts it, either in a reply to
this record or by incorporating it into the binding file under the A4 slots.

## Proof record

**Family used:** orca-harness code binding (code-enforced pole). De-correlated
from the actor-carried/maximize pole (product-proof binding), which is the
closest analog to the courier's "maximize" test surface.

---

### Case A — claimed probed, under-case OWED → must be HELD

Synthetic cell: `GUARD probe-gate-total-future` — "when a new enum member is
added to ProbeResult or IsolationResult, interpret_probe_gate must explicitly
route the new combination." Author note: "test will be added when new member
is added." Claims tier: `probed`.

Policy check: `probed` requires under-case test AND over-edge test in suite
→ neither exists.

**Result: HELD** — mechanism correctly blocks the claim. ✓

---

### Case B — under-case run, over-edge OWED, claims probed → ADMIT capped down

Real cell: `probe-gate-total-function`
(`docs/decisions/distillation_binding_orca_harness_code_v0.md`)
Claimed tier: `probed (review-confirmed)`

Under-case evidence:
  `test_ambiguous_with_proven_isolation_routes_to_quarantine_explicitly`
  at `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py:350`
  → **VERIFIED EXISTS** — exercises AMBIGUOUS + PROVEN → AMBIGUOUS_QUARANTINE.

Over-edge evidence:
  Binding says: "over-edge (an unhandled pair) → raises (no silent fallthrough)"
  Code guard: `raise ValueError(...)` at `orca-harness/schemas/probe_models.py:222`
  → **EXISTS IN CODE** but **NO TEST in the suite exercises this code path**.
  Grep of `interpret_probe_gate` calls in tests shows only line 352
  (the under-case call); the ValueError branch is never exercised by a test.

Policy check: `probed` requires over-edge test in suite → NOT MET.

**Result: ADMIT, capped from `probed` to `recorded`** — mechanism correctly
surfaces the inflated tier claim. ✓

**REAL FINDING:** `probe-gate-total-function` claims `probed (review-confirmed)`
but only the under-case is test-exercised. The over-edge (unhandled combination
raises) is a defensive code guard without a test. The corrected tier is `recorded
(under-case tested; over-edge code guard at probe_models.py:222, no test in suite)`.
Tier correction is blocked until the owner ratifies the policy above.

---

### Case C — under-case + over-edge complete → ADMIT at probed

Real cell: `secret-value-chokepoint`
(`docs/decisions/distillation_binding_orca_harness_code_v0.md`)
Claimed tier: `probed (dual-guard test)`

Under-case: `test_secret_like_output_values_are_rejected`
  at `orca-harness/tests/unit/test_reddit_candidate_intake.py:555`
  → **VERIFIED EXISTS**

Over-edge: `test_legit_token_like_values_are_not_rejected`
  at `orca-harness/tests/unit/test_reddit_candidate_intake.py:573`
  → **VERIFIED EXISTS**

Policy check: both tests exist → MEETS `probed` requirement.

**Result: ADMIT at `probed`** ✓

---

### Case D — GATE CHECK: known-good cell → ADMIT (if rejected, run is invalid)

Cell: `secret-value-chokepoint` (same as Case C; used as explicit gate check).

Same evidence, same policy check → same result.

**GATE: ADMIT** ✓ — mechanism does not over-enforce on a confirmed known-good
cell. Gate passes; the run is valid.

---

## Verdict: ADOPT

All 4 cases produce the correct behavior:
- Case A (HELD): ✓
- Case B (capped): ✓ — and reveals a real tier inflation in the existing binding
- Case C (admitted at probed): ✓
- Case D (gate check — admitted): ✓

The mechanism works. It reads the declared per-tier requirement from the binding
and caps cells that do not meet it. It does not reject known-good cells. It
surfaces a real finding in an existing cell. ADOPT.

## Cross-adopter signal (received 2026-06-11)

The courier reported that their own maximize/actor-carried binding carries the
SAME failure shape as Case B: a cell claiming `probed` whose over-edge branch
is a field marked `COMPLETE` but not independently verified. Two bindings,
two independent adopters, same over-edge-overclaim — found independently on
different substrates (code-enforced vs actor-carried). The failure mode is
general, not binding-specific. This is the expected output of de-correlated
adoption: a second data point that the distillation tier mechanism closes a
real, recurring gap.

The courier also returned the middle-tier finding (their `recorded` analog):
original `asserted` definition ("no test") contradicted Case B which has the
under-case test. The policy above has been corrected to add `recorded` as the
middle rung. This section records the exchange as part of the proof provenance.

## Actor-carried substrate caveat

The orca-harness code proof passed cleanly because the substrate is
grep-verifiable: "does the over-edge test exist?" is answerable by reading
the test file. That is the free over-edge-honesty check this substrate provides.

Actor-carried bindings (Judgment Spine, Prompt-orchestration, Product-proof,
Review/patch lanes, Core-Spine proof — five of eight Orca bindings) have
self-reported evidence fields, not test files. On those bindings, "did the
over-edge run?" is a trusted field value, not a mechanical check. The same
inflation that Case B caught on a code binding can pass undetected on an
actor binding if the field is over-asserted.

Consequence: the per-tier enforcement mechanism is necessary but not sufficient
for actor-carried bindings. Those bindings need an adversarial-review layer
(an independent reviewer who attempts to refute each `probed` tier claim before
it is accepted) to provide the honesty that grep provides on the code binding.

The five actor-carried bindings currently have all real cells at
`accepted-orca-gate` (no `probed` tier claims to check today). The caveat
becomes load-bearing when new cells are distilled into those bindings at
`probed`. Flag and enforce it at that ingest event.

## Downstream work (owner-gated)

**P1 — ratify or amend the per-tier policy** (above). Until ratified, the tier
correction below is blocked.

**P2 — update probe-gate-total-function tier** (after P1):
In `docs/decisions/distillation_binding_orca_harness_code_v0.md`, change:
```
tier: probed (review-confirmed)
```
to:
```
tier: recorded (under-case tested; over-edge code guard at probe_models.py:222,
no test exercises that path in current suite)
```
Gap to close: add a test that exercises `interpret_probe_gate` with a combination
not covered by the current branches (or add it to the testing plan for the next
enum extension).

## Advisory flag (not a proof case — auditable but uncertain under this policy)

`content-lossless-agent-view` claims `tier: probed (mutation-checked red→green)`.
The under-case (mutation check: drop a protected field → test goes red) is
exercised by `test_strip_retention_contract` and related tests. The binding's
over-edge is described as "a true non-substantive field → green." No test named
in the binding or visible in the test suite specifically checks that a
non-protected field IS correctly stripped without causing a false-positive
failure. This may be an implicit structural guarantee (the retention contract
only covers protected fields) or a gap. Recommend auditing this cell against
the policy when P1 is resolved.

## Non-claims

- Prepare-only. No always-on overlay change; no substrate built; no binding file
  edited; no cell tier corrected.
- The policy is proposed; tier corrections follow from ratification, not from
  this proof alone.
- This record is proof that the mechanism behaves correctly, not proof that all
  existing cells are correctly tiered. Only the 4 proof cases were checked.
- Not validation, readiness, approval, source-of-truth promotion, or
  implementation authorization.

## Preflight receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: partial
    # README, decision-routing, artifact-roles, safety-rules, source-loading,
    # validation-gates read this turn. Other overlay sections via prior context
    # and repo map.
  source_pack: custom
    # overlay core + distillation doctrine index + code binding + product-proof
    # binding + test suite grep + probe_models.py read.
  edit_permission: docs-write
    # new decision record under docs/decisions/ only;
    # no binding file edited; no overlay file edited.
  target_scope:
    - docs/decisions/distillation_tier_policy_adoption_v0.md (this file)
  dirty_state_checked: yes
    # branch ecr-sp3-timing-deriver-slice1; many untracked docs;
    # orca-harness modified. This adds one new file; edits no overlay file.
  blocked_if_missing: no
```
