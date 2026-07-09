# Distillation Binding — orca-harness Code Harness (prepare-only draft)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: per-spine distillation binding for the orca-harness deterministic code harness (capture/scoring/probe + tests)
use_when:
  - Distilling an orca-harness lesson into a carried rule (agent working orca-harness).
  - Sizing/pruning carried rules for the code harness; deciding code-enforced vs actor-carried.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md
  - forseti-harness/docs/source_capture_agent_runbook.md
```

**Status: PREPARE-ONLY DRAFT** (see the index). This is Orca's **code-enforced pole** — the closest
analog to the jb render binding. It *reads* the harness's recorded lessons and the tests that
already enforce them; it installs nothing and edits no `orca-harness/` file. The harness's authority
lives in its lane (build authorizations + runbook); this binding does not own or edit it.

## Harness bound

The agent operating or modifying `orca-harness/` — the bounded Python implementation backing Data
Capture source acquisition and the v0.14 Judgment Harness (capture adapters, source-capture packet
core, schemas, deterministic band scorer, runners, and contract/unit/integration tests). Governed
actor: the agent (LLM or human) working the harness, not the Python code itself.

## Pole / key finding

**Code-enforced.** Every cell below is hardened into a deterministic pytest that *records the
failure it prevents*. Each **always fires**, satisfies VERIFY FIRING by construction, and costs
**zero** of the agent's rule-count budget. CONFLICT-CHECK is engine-caught (the suite runs). The
only actor-carried tails are "do not delete this guard on refactor."

## A1 — outcome → cell pairs (real, cited)

### GUARD secret-value-chokepoint  (code-enforced)
- decision_node: `node:no-forbidden-output-fields-chokepoint`
- `GUARD secret-value-chokepoint: WHEN building candidate-intake/frontier output → reject a forbidden field NAME and any secret-like VALUE (PEM key, bearer token, URL userinfo, Set-Cookie) → UNLESS the value is a legitimate token-like id (thread/run/permalink).`
- outcome_class: a credential in a legitimately-named free-text field passes the name blocklist and leaks downstream
- causal_miss: a field-NAME blocklist alone cannot catch a secret embedded in a legitimately-named field; a VALUE scan is needed (defense-in-depth)
- verification: under-case (`test_secret_like_output_values_are_rejected`) → reject; over-edge (`test_legit_token_like_values_are_not_rejected`) → pass
- enforced_in: `orca-harness/capture_spine/reddit_candidate_intake/validation.py` (`assert_no_forbidden_output_fields`); dual-guard tests in `orca-harness/tests/unit/`
- PROV: `validation.py:157` "this stops a credential that lands in a legitimately [named field]"; commit `d2efd1f`. tier: probed (dual-guard test). date 2026-06.

### GUARD content-lossless-agent-view  (code-enforced)
- decision_node: `node:agent-view-strip`
- `GUARD content-lossless-agent-view: WHEN stripping a raw artifact into a cleaned agent view → preserve every runbook-protected field (bodies, visible candidate values, bounds/caps/exclusions, stop reasons) → UNLESS the field is genuinely non-substantive page chrome.`
- outcome_class: a cleaned/stripped agent view silently drops decision-relevant bounds (caps/exclusions/stop reasons), so the agent cannot see the traversal boundary
- causal_miss: treating the cleaned view as a free reduction instead of a content-lossless projection bound by the runbook preserve rule
- verification: under-case (`test_strip_retention_contract` — drop any protected field) → red; over-edge (a true non-substantive field) → green
- enforced_in: `orca-harness/tests/unit/test_reddit_agent_view.py` (`test_strip_retention_contract`, `test_graph_frontier_view_retains_caps_and_exclusions_once`, `test_candidate_intake_view_retains_run_level_exclusions`)
- PROV: `orca-harness/docs/source_capture_agent_runbook.md:236-237` "**content-lossless**: it preserves all substantive content (thread/post/comment text, visible candidate values, bounds/caps/exclusions, stop reasons...)"; commits `d1a2dc6`, `61dd925`. tier: probed (mutation-checked red→green). date 2026-06.

### GUARD probe-gate-total-function  (code-enforced)
- decision_node: `node:probe-gate-interpretation`
- `GUARD probe-gate-total-function: WHEN interpreting (ProbeResult × IsolationResult) → route every combination explicitly (AMBIGUOUS + PROVEN → AMBIGUOUS_QUARANTINE) and raise on any unhandled combination → UNLESS n/a.`
- outcome_class: an unhandled enum combination silently falls through gate logic (no explicit branch)
- causal_miss: a non-total interpretation function over a finite product type, with no guard for future enum members
- verification: under-case (`test_ambiguous_with_proven_isolation_routes_to_quarantine_explicitly`) → AMBIGUOUS_QUARANTINE; over-edge (an unhandled pair) → raises (no silent fallthrough)
- enforced_in: `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py:350`; `interpret_probe_gate` + ValueError guard in `orca-harness/schemas/probe_models.py`
- PROV: review `docs/review-outputs/no_tools_probe_runner_step04_post_patch_adversarial_recheck_v0.md:196` (finding R-06, "Test passes ✓"). tier: probed (review-confirmed). date 2026-06.

## A2 — core size / budget

Near-zero actor budget: all three cells are code-enforced (live in the suite), so they cost nothing
resident. The only actor-carried tail is "do not delete/weaken these guards on refactor" — a single
low-frequency reminder, not a per-turn rule. No budget pressure.

## A3 — spine / decision nodes

`node:no-forbidden-output-fields-chokepoint` · `node:agent-view-strip` · `node:probe-gate-interpretation`
· `node:band-scorer-mapping-pin` · `node:no-llm-import-guard` · `node:no-tools-isolation-contract`.
Cells index by `decision_node`.

## A4 — slots filled

- **intervention-type set** (closed; owner-extensible): `GUARD`, `CONTRACT-TEST`, `SCHEMA` (typed `BLOCKED_*`/`FAILED_*`/enum).
- **verification substrate**: the deterministic pytest suite (`unit/`, `contract/`, `integration/`), including the no-LLM-import and no-tools contract guards; mutation-checked retention contract.
- **fire-log capability**: **STRONG** — pass/fail is a deterministic log, so the telemetry-gated prune triggers (Inert / Marginal-gain-gone) ARE fireable here, unlike an un-instrumented harness.
- **tier enum**: recorded cells are at least `probed` (each reproduced as a passing/mutation-checked test).
- **review window**: owner sets (e.g. per harness change / suite run).
- **owner map**: the orca-harness lane owner.

## Secondary finding

`VERIFY FIRING` is cheap here (the suite is a direct firing signal), confirming the core's
signal-bounded framing — same result as the jb render pole. The agnostic core's decision-node
admission, GUARD shape, conflict-check, one-in/one-out, and provenance separation all transfer
cleanly. The only strain is the LLM-instruction-budget assumption, which barely applies to a
mostly-deterministic harness.

## Non-claims

Prepare-only; references existing tests, installs nothing, edits no `orca-harness/` file; not
validation, readiness, runtime, or judgment-quality proof; a passing guard enforces a behavior
shape, never the truth of any downstream claim.
```
