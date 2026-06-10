---
artifact_id: no_tools_execution_foundation_blind_spot_adversarial_review_v0
artifact_role: Bounded system-level adversarial blind-spot review — no-tools execution foundation
created_at: 2026-06-01
review_mode: bounded_adversarial_blind_spot_review
output_mode: filesystem-output
status: completed
reviewed_by: claude-opus-4-8 via workflow-deep-thinking (system-level framing) + workflow-code-review (cross-surface findings posture)
commission: >
  Is the current no-tools execution foundation coherent enough to support owner
  consideration of a separately authorized live no-case provider smoke test or
  fresh-case public-identifiers-only probe? "Coherent" = contracts, runner
  behavior, tests, docs, and review evidence align. Not readiness, not
  validation, not judgment quality.
recommendation: accept_with_friction
source_context_status: SOURCE_CONTEXT_READY
authority_hashes_verified: true
head_label_note: >
  Prompt stated expected HEAD c57a669; actual HEAD is d70e25f (one commit ahead).
  All 19 in-scope source hashes match the current working tree, so the prompt's
  hashes were captured at/after d70e25f. Review targets are byte-identical to the
  intended set. See Section 3.
findings_count: 5
blocking_findings: 0
advisory_findings:
  critical: 0
  major: 2
  minor: 2
  optional: 1
tests_run:
  focused: "22 passed"
  full: "66 passed"
  git_diff_check: "clean (benign LF/CRLF working-copy notice on orca-harness/README.md only)"
---

# Bounded System-Level Adversarial Blind-Spot Review: No-Tools Execution Foundation

## 1. Commission and Stance

**Central question.** Is the no-tools execution foundation coherent enough to support
owner *consideration* of a separately authorized live no-case provider smoke test, or a
future fresh-case public-identifiers-only memorization probe?

**Stance.** This is a system-level blind-spot review of the foundation as a whole
(contract + protocol + schema + dry runner + raw-API runner + tests + operator docs +
prior review evidence). It is **not** a line-level adapter code review (already done and
accepted) and **not** a live probe. The goal is to surface hidden assumptions,
cross-surface mismatches, stale doctrine, operator ambiguity, or audit gaps that could
make a first controlled live smoke test (or a future fresh-case probe) **unauditable or
misleading**.

**Hard boundaries enforced.** No file patched. No live provider call. `--allow-live-provider-call`
never passed. No API key read/printed/tested. No participant packet exposed. No real
memorization probe, blind judgment, scoring, ledger freeze, fixture validation, or
admission. No readiness / product-proof / judgment-quality claim.

**Method.** `workflow-deep-thinking` applied first to frame system-level failure modes
(Section 5), then a `workflow-code-review` adversarial posture for cross-surface findings
(Section 6). This is a **read-only adversarial review lane** (review-lanes.md): findings
are decision input only; **no `patch_queue_entry` is emitted**; advisory remediation
direction only.

---

## 2. Surfaces Reviewed (as one foundation)

| Layer | Surface |
|---|---|
| Authority / contract | `contestant_no_tools_execution_contract_v0.md`, `memorization_probe_protocol.md`, closure/blast-radius check |
| Runtime / schema | `schemas/probe_models.py`, `runners/run_memorization_probe.py` (dry), `runners/run_memorization_probe_raw_api.py` (live), `pyproject.toml` |
| Tests | `tests/contract/test_memorization_probe_no_tools_contract.py`, `tests/contract/test_no_llm_imports.py` |
| Operator docs | `orca-harness/README.md`, `orca-harness/docs/v0_14/README.md` |
| Review evidence | dry-runner step04 post-patch recheck, raw-API adapter review, raw-API adapter post-patch recheck |
| Load-bearing deps (read for alignment) | `harness_utils.py` (`NON_CLAIM_NOTICE`, `write_yaml_file`), `schemas/case_models.py` (`StrictModel`) |

---

## 3. Source Context and Hash Verification

- **Branch:** `main` (matches expected).
- **HEAD:** `d70e25f3f3fe544b4c60315ac823d35b48f504a1` — **one commit ahead** of the prompt's
  expected `c57a669…`. The extra commit `d70e25f` ("docs: add source observability record
  guide") touched `orca-harness/README.md` (+3 lines) and added one **out-of-scope** doc.
- **Reconciliation (review-trust):** the prompt's expected hash for `orca-harness/README.md`
  matches the **current (post-`d70e25f`)** file, so the prompt's hashes were captured at/after
  `d70e25f`. The "Expected HEAD" label is stale by one commit; the **authoritative hash gate
  matches the exact files reviewed**. No review-trust impact.
- **Source hashes:** all **19/19 MATCH** (independently recomputed via `Get-FileHash -SHA256`).
- **Output collision:** `docs/review-outputs/no_tools_execution_foundation_blind_spot_adversarial_review_v0.md`
  did not exist before write. No `BLOCKED_OUTPUT_COLLISION`.

**`SOURCE_CONTEXT_READY`**

---

## 4. Allowed Offline Validation (independently reverified)

| Check | Command | Result |
|---|---|---|
| Whitespace/conflict | `git diff --check` on the four patched files | exit 0; only a benign LF→CRLF working-copy notice on `orca-harness/README.md` (same as prior recheck) |
| Focused contract suite | `pytest … test_memorization_probe_no_tools_contract.py test_no_llm_imports.py` | **22 passed** (matches expected) |
| Full suite | `pytest -p no:cacheprovider` | **66 passed** (matches expected) |

No network, provider call, credential, or live probe was used. The full suite honours
`testpaths = ["tests"]`, so it did not traverse `pytest_tmp_raw_api/`.

---

## 5. Deep-Thinking System-Level Failure-Mode Frame

The gate logic is the part most prior reviews scrutinised, and it is sound: `interpret_probe_gate`
enumerates all 9 `(ProbeResult × IsolationResult)` combinations; `VIOLATED` dominates (checked
first regardless of probe_result); the **only** path to `PASS_VALID` is `PASS + PROVEN`; and
`PROVEN` requires `no_tools` + a proof-grade evidence kind + an empty/not-applicable trace +
all four disabled flags `True` + a non-empty hidden-context boundary. The raw-API runner derives
`PROVEN` from **request-shape validation** (forbidden-key recursion + per-provider allow-list +
exact-prompt equality + endpoint pinning), not from assertion. Errors raise before any write, so
failed live calls produce **no** artifact. Secret hygiene is handled (key never stored, redacted
in HTTP-error bodies). These are real strengths and they hold.

So the residual risk is **not** inside the gate logic. Reframing the commission's question — *what
could make the first controlled live receipt unauditable or misleading?* — moves the attack surface
to the **boundary between the artifact and the world**:

1. **Provenance of a clean receipt.** The gate logic proves "given this evidence, the result is
   `pass_valid`." It does **not** prove the evidence describes a real isolated *live* execution.
   The evidence fields are operator-supplied in the dry path and hard-coded in the live path. So
   the decisive question is whether a `pass_valid` artifact can be **trusted on its face** to have
   come from a validated live execution — i.e., whether the foundation records *where the receipt
   came from*. (→ F-01)

2. **What a "no-case smoke test" even is.** The foundation defines a dry normalizer and a live
   raw-API runner, but **no surface defines a no-case smoke test**, its inputs, or how its receipt
   is handled. An undefined activity cannot be audited. (→ F-02)

3. **Doc↔code seams that only bite a fresh-case probe.** The probe-result classifier and the
   protocol's evaluation rule diverge on one input class; harmless for a no-case smoke test,
   relevant before a fresh-case probe. (→ F-03)

4. **Failure visibility.** Failure is the safe direction (no artifact), but a smoke test's value
   is partly diagnostic, and failure leaves only transient stderr. (→ F-04)

This frame deliberately sets aside the gate-logic re-derivation (done by the step04 recheck and
the raw-API adapter review) and the two closed majors (M-01 full-response hashing, M-02 endpoint
pinning), which I re-confirmed against current code (Section 7).

---

## 6. Findings

Severity per the commission's live-use-risk scale. Each finding carries
`minimum_closure_condition` (required end state) and `next_authorized_action` (what this read-only
lane permits next). **No `patch_queue_entry` is emitted** (read-only adversarial lane). This review
holds **no patch or implementation authority**; closure-path selection is an owner decision.

---

### F-01 — (major) A `pass_valid` receipt records no execution provenance; non-live surfaces can mint a receipt indistinguishable from a genuine live raw-API one

**Reviewed target.** `schemas/probe_models.py` (`MemorizationProbeArtifact`,
`ContestantExecutionIsolation`, `derive_isolation_result`), `runners/run_memorization_probe.py`
(dry-runner CLI surface), cross-checked against `runners/run_memorization_probe_raw_api.py`.

**Location / structural anchors.**
- `run_memorization_probe.py:180` — dry-runner `--execution-surface` `choices` is the **entire**
  `ExecutionSurface` enum, including `raw_api_no_tools`; `:206–217` builds isolation evidence
  directly from operator CLI args.
- `probe_models.py:171–203` — `derive_isolation_result` returns `PROVEN` for **any**
  `execution_surface` that meets the evidence conditions (no surface↔evidence-kind cross-check;
  `local_fixture`/`manual_unknown` are not excluded).
- `probe_models.py:135–149` + `:91–102` — artifact/isolation fields contain **no** provider,
  endpoint/`api_url`, live-call, transport, or producing-runner field; `case_models.py:10–11`
  (`StrictModel`, `extra="forbid"`) confirms no provenance can ride along outside the schema.
- `test_memorization_probe_no_tools_contract.py:357–476` — the **dry** CLI (no live call) is
  driven with `--execution-surface raw_api_no_tools --tool-config-evidence-kind structural_config
  --tool-call-trace-status not_applicable …` and asserts `isolation_result=proven`,
  `gate_interpretation=pass_valid`.

**Evidence.** A hand-authored/normalized dry receipt and a genuine live raw-API receipt are
**byte-equivalent in every gate-relevant field** (`execution_surface`, `tool_access_policy`,
`tool_config_evidence_kind`, `tool_call_trace_status`, the four disabled booleans,
`isolation_result`, `probe_result`, `gate_interpretation`). `execution_surface` *is* recorded but
is **operator-settable** in the dry runner, so it is not a trustworthy discriminator; the fixed
`tool_config_evidence` string the live runner emits is visible in source and copyable. A second
instance: `local_fixture` + `empty_trace` + `structural_config` + all-true also reaches `proven`
(schema-valid, untested), so a surface that by definition made no live call can carry
`isolation_result: proven`.

**Authority / evidence basis.** Contract Purpose ("prevents a contestant probe … from being treated
as clean merely because the prompt told the model not to search", lines 49–53) and Isolation Result
Semantics; protocol Limits ("Probe passing cannot clear a gate unless execution isolation is
proven"); review-lanes findings standard. The endpoint-validation guarantee
(`validate_standard_provider_endpoint`) only binds the *live* runner — a dry receipt asserting
`raw_api_no_tools` never passed through it.

**Impact (Q3, Q5, Q7).** A `pass_valid` artifact cannot, on its face, certify that it came from a
validated live isolated execution. Trust in a first controlled smoke-test (or fresh-case probe)
receipt therefore rests on **out-of-band operator attestation**, not the artifact. This is a
cross-surface path by which a non-live `pass_valid` could later be mistaken for a live clean pass
(Q5), and it is the single largest reason the first live receipt is harder to audit (Q3). It does
**not** create *automatic* false gate clearing (it requires deliberate or careless operator action,
the gate logic is otherwise sound, and `pass_valid` only authorizes proceeding to a *separately
authorized* next gate) — hence major, not critical.

**Minimum closure condition.** The foundation can distinguish a gate-eligible **live** raw-API
receipt from a non-live/normalized one. Satisfied by **any one** of:
- (a) the schema records execution provenance (e.g., `live_call_made` / producing-runner /
  `provider` / `endpoint`) and gate-eligibility requires a live-runner receipt; or
- (b) the schema/`derive_isolation_result` bars `proven` (hence `pass_valid`) for
  `execution_surface ∈ {local_fixture, manual_unknown}`, and the dry runner is barred from emitting
  `raw_api_no_tools`; or
- (c) a controlling doc rule + the F-02 operator checklist state that **only** the live raw-API
  runner's receipt is gate-eligible, dry/normalized receipts are never gate-clearing regardless of
  computed fields, and live provenance (provider, exact endpoint, UTC timestamp, exit status) is
  captured out-of-band and bound to the receipt by `prompt_hash`/`raw_response_hash`.

**Next authorized action.** Owner selects a closure path. Paths (a)/(b) require a separately
authorized bounded implementation turn (this review has no patch authority). Path (c) is
docs-only and is the cheapest path to make a smoke test auditable without code change.

**Verification expectation.** For (a)/(b): same-check red-green — a new offline contract test that
**fails** against current code (dry CLI mints `raw_api_no_tools`+`pass_valid`; `local_fixture`
reaches `proven`) and **passes** after the guard. For (c): the doc rule + checklist exist and the
smoke-test authorization references them.

**`patch_queue_entry`:** not authorized (read-only lane).

---

### F-02 — (major) No operator decision artifact defines or governs a "no-case smoke test"

**Reviewed target.** Operator docs (`orca-harness/README.md`, `docs/v0_14/README.md`) and the
v0_14 harness doc set; contract Applies-To.

**Location / anchors.** `orca-harness/README.md:85–100` documents the dry runner and the live
raw-API runner and says a *real* probe needs "separate owner authorization for the exact model/case
pair" — but **no surface names a no-case smoke test**, its synthetic inputs, or its receipt handling.
Contract `applies_to` (lines 61–71) covers public-identifiers probes and blind runs; a no-case
plumbing smoke test is not enumerated anywhere.

**Evidence.** Absence across all in-scope surfaces: there is no definition of what a no-case smoke
test is, no synthetic-`probe_input` convention, no rule marking a smoke receipt non-gate-clearing,
and no out-of-band provenance-capture procedure.

**Authority / evidence basis.** Commission Q12; validation-gates.md:13 ("Validation must be able to
fail. Missing evidence is not a pass."); review-lanes findings standard.

**Impact (Q3, Q12).** If a no-case smoke test is authorized, there is no defined procedure to
(i) mark its synthetic receipt non-gate-clearing, (ii) capture live-call provenance, or (iii) keep
the smoke receipt from being mis-filed as a real probe result. This is the operator-facing
mitigation surface for F-01; without it, an authorized smoke test's evidence is at material risk of
being unauditable or misleading.

**Minimum closure condition — smallest complete artifact.** A single small operator
authorization/checklist exists **before the smoke test is run** (not before owner *consideration*),
under an Orca-owned harness v0_14 path, stating:
1. **Purpose:** plumbing-only confirmation; no real case; explicitly distinct from a fresh-case
   probe and from blind judgment.
2. **Synthetic input convention:** a reserved `case_id` marker (e.g., a `SMOKE_NOCASE_*` prefix)
   that is, by rule, **never gate-clearing**, plus clearly-synthetic decision question / identifiers
   / cutoff.
3. **Non-gate-clearing rule:** `pass_valid` on a smoke receipt is plumbing confirmation only and
   clears no gate; it must never be cited as a clean probe pass for any model/case pair.
4. **Out-of-band provenance capture:** provider, exact endpoint URL, UTC timestamp, process exit
   status, full console output, and the receipt's `prompt_hash` + `raw_response_hash` — recorded
   alongside the receipt (this also closes F-04's auditability gap and operationalises F-01(c)).
5. **Authorization boundary:** which model/account is authorized, and that `--allow-live-provider-call`
   use is one-shot for this smoke test only.
6. **Non-claims** + the required closeout line `plumbing works only; not judgment quality`.

**Next authorized action.** Owner authorizes a bounded docs-write turn to create this artifact;
**this review does not create it** (read-only lane) and only specifies it.

**Verification expectation.** Artifact exists at an Orca-owned path with the six elements above and
is referenced by the smoke-test authorization. (Doc artifact; red-green N/A.)

**`patch_queue_entry`:** not authorized.

---

### F-03 — (minor) `classify_probe_response` silently resolves the protocol's `partial` + empty-`claimed_outcome` overlap toward `PASS`

**Reviewed target.** `schemas/probe_models.py:225–230` vs `memorization_probe_protocol.md`
Evaluation Rule (lines 84–97).

**Location / anchors.** `probe_models.py:226–227`
(`if recognition_status == "unknown" or claimed_outcome is None: return ProbeResult.PASS`); protocol
`pass` clause includes "claimed_outcome is empty/generic/incorrect", `ambiguous` clause includes
"model partially identifies the case but does not reveal outcome".

**Evidence.** A response `{recognition_status: partial, claimed_outcome: empty/None, confidence: x}`
matches **both** the protocol pass clause and the ambiguous clause; the code resolves it to `PASS`.
The empty-string→`None` validator (`ParsedProbeResponse.empty_string_to_none`) routes empty outcomes
into this branch. No test covers it — the existing ambiguous test (lines 186–218) uses a **non-empty**
`"maybe approved"` outcome → `AMBIGUOUS`. Code also does not evaluate "generic/incorrect" outcomes
(it treats confident `recognized` + any non-empty outcome as `FAIL`, which is the conservative
direction); the **non-conservative** divergence is specifically `partial` + *empty*.

**Authority / evidence basis.** The protocol Evaluation Rule is the controlling probe-result
document and is internally ambiguous for this input; the code silently picks one resolution.

**Impact (Q1, Q11).** Irrelevant to a no-case smoke test (no real recognition). For a **future
fresh-case probe**, a coy `partial` recognition that states no outcome is classified `PASS`
(→ eligible for `PASS_VALID` if isolation is proven) rather than `AMBIGUOUS` quarantine — a result
that could mislead relative to a reasonable reading of the ambiguous clause.

**Minimum closure condition.** The protocol states an unambiguous intended result for `partial` +
empty `claimed_outcome`, and the classifier + an offline test agree with it.

**Next authorized action.** Owner decision on intended semantics before a fresh-case probe is
authorized; bounded docs (+ test) turn if a change is wanted. **Not** a no-case smoke-test blocker.

**Verification expectation.** Offline test asserting `classify_probe_response(partial, None)` →
the chosen result; same-check red-green if code changes.

**`patch_queue_entry`:** not authorized.

---

### F-04 — (minor) Failure states are correctly non-gate-clearing but leave no durable structured error record

**Reviewed target.** `runners/run_memorization_probe_raw_api.py` `main()` and
`run_memorization_probe_raw_api()`.

**Location / anchors.** Raw-API runner `:389–414` (every error path → `parser.exit(status=2)`); all
validation/parse errors raise before `write_yaml_file` (`:291`). Tests
`test_raw_api_provider_malformed_response_writes_no_artifact` and
`…_rejects_response_text_shortcut` assert `not output_path.exists()`.

**Evidence.** Blocked-by-flag, invalid max_tokens/timeout, credential-missing, non-standard-endpoint,
forbidden/unexpected request key, provider HTTP/URL error, non-JSON response, empty model text, and
YAML/schema mismatch all produce **exit 2 + no artifact**. This is the **safe** direction: no
artifact can be mistaken for a pass. The only record of *why* a run failed is the process exit code
and transient stderr; there is no machine-readable error receipt.

**Authority / evidence basis.** Commission Q6 (blocked/error states must be visibly
non-gate-clearing — they are); validation-gates.md:13.

**Impact (Q6).** Failure visibility is non-gate-clearing and correct, but a smoke test is partly a
diagnostic exercise; auditing *why* a smoke test failed depends on the operator capturing console
output. This is auditability, not gate safety.

**Minimum closure condition.** The F-02 smoke-test procedure mandates capturing exit code + full
stderr (sufficient); a structured non-gate-clearing error record is optional hardening only.

**Next authorized action.** Fold capture into the F-02 checklist; optional runner hardening at owner
discretion. **Not** a no-case smoke-test blocker.

**Verification expectation.** Checklist requires capture; (optional) a test if an error-record
feature is later added.

**`patch_queue_entry`:** not authorized.

---

### O-01 — (optional) `parsed_response.claimed_outcome` stores the model's guessed outcome (fresh-case handling caveat)

**Reviewed target.** `schemas/probe_models.py` `ParsedProbeResponse.claimed_outcome`;
`memorization_probe_protocol.md` Artifact Path (`cases/<batch>/<case_id>/probes/…`).

**Evidence / impact (Q9).** For a fresh-case probe, `claimed_outcome` may contain the model's *guess*
at a real case outcome. This is facilitator-side audit content **by design** (the probe must record
what the model claimed) and is **not** ground truth; the raw provider body is hashed but **not**
stored. No defect for a no-case smoke test (no real outcome). The optional caveat is that probe
artifacts must never be routed into participant-facing surfaces (zero-spoiler gate,
validation-gates.md:160–165).

**Minimum closure condition (optional).** The fresh-case probe authorization states that probe
artifacts stay facilitator-side and are excluded from participant packets. Out of this review's
scope to mandate.

**`patch_queue_entry`:** not authorized.

---

## 7. Relationship to Prior Review Evidence (accepted residuals, not re-opened)

| Item | Prior disposition | This review |
|---|---|---|
| **M-01** `raw_response_hash` covers full provider body | Closed (option a) | Re-confirmed: live runner `:286` passes `raw_response_text=raw_response_body`; test `:517` asserts full-body hash. **Closed holds.** |
| **M-02** endpoint pinning for `NOT_APPLICABLE`+`PROVEN` | Closed (option b) | Re-confirmed: `validate_standard_provider_endpoint` pins https + exact host/path + no params/query/fragment, fires before transport. **Closed holds.** |
| **R-06** `AMBIGUOUS_QUARANTINE` absent from contract gate table | Closed via **code** (explicit branch + `ValueError` fallthrough), doc deliberately not updated | **Accepted prior decision.** Protocol Case Handling (`if_ambiguous` → quarantine) covers the intent; not re-opened. |
| **Q8 residual** provider-side server tools | Raised in M-02; resolved-to-scope by endpoint pinning + two-provider documentation | **Accepted residual.** The runner derives `PROVEN` from request shape + pinned endpoints and does **not** inspect responses for tool-use signals to downgrade isolation; it assumes the two standard endpoints perform no server-side retrieval given no tool params. Reasonable and documented. A no-case smoke test is precisely the cheap way to sanity-check live request/response shape against this assumption. |
| **m-01/m-02/m-03/O-01 (raw-API)** | Addressed in patch (shortcut removed; double-validate removed; stderr redaction added; CLI-only guard documented) | Re-confirmed present in current code. |

**Novel to this review:** F-01 (cross-surface receipt-provenance gap) and F-02 (undefined no-case
smoke test). Prior reviews checked only that the dry runner's **hash was unchanged** (step04 recheck
§7.4); none examined whether a dry/normalized receipt can present as a live raw-API `pass_valid`.

---

## 8. Blind-Spot Question Matrix

| # | Question | Assessment |
|---|---|---|
| 1 | Contract/code/docs alignment | Strong on the core gate (9 combinations tested, `VIOLATED` dominates, `PASS_VALID` only from `PASS+PROVEN`, proof-grade evidence-kind requirement is stricter than and consistent with the contract). Two seams: F-03 (`partial`+empty classification) and the accepted `AMBIGUOUS_QUARANTINE` doc-table omission (R-06). Otherwise aligned. |
| 2 | Live-use boundary | Clear and well-fenced. `--allow-live-provider-call` required and tested; both READMEs state a real probe needs separate model/case authorization; dry runner makes no calls; live runner is "plumbing only." Coherent. |
| 3 | No-case smoke test as decision input | Plumbing is **coherent enough to consider** the smoke test. But F-01 (no receipt provenance) + F-02 (no smoke-test artifact) would make the smoke-test **receipt** hard to audit / at risk of misfiling. Coherent for consideration **with named friction** to resolve in the authorization. |
| 4 | Fresh-case probe boundary | Distinct from a no-case smoke test; README requires separate model/case authorization. Adequately separated. F-03 + O-01 are fresh-case-only items to resolve before that separate authorization. |
| 5 | `pass_valid` misuse | Gate logic cannot mint `pass_valid` except `PASS+PROVEN`. The single cross-surface misuse path is F-01 (a non-live receipt computing `pass_valid`, with no provenance to catch it). Closed by F-01 + F-02. |
| 6 | Blocked/error semantics | All enumerated states (blocked, malformed, access-failed, credential-missing, non-standard-endpoint, provider-error, unparseable) are non-gate-clearing — **no artifact, exit 2** — verified by code + tests. Visible via exit code/stderr; no durable error record (F-04, minor). |
| 7 | Metadata sufficiency | Present: requested model id, model snapshot/fingerprint, prompt hash, **full** provider-response hash (post M-01), parsed response, isolation evidence, operator-review status, ULID, created_at. **Gaps:** provider, endpoint/`api_url`, and live-call provenance are **not** in the receipt (F-01). Sufficient *except* provenance. |
| 8 | Endpoint/provider assumptions | Endpoint pinning (M-02 closed) removes the arbitrary-URL risk. Residual accepted assumption: the two pinned endpoints perform no server-side tool/retrieval given no tool params, and the runner does not inspect responses to downgrade isolation. Reasonable + documented; a smoke test sanity-checks it. No hidden re-opening. |
| 9 | Secret/transcript hygiene | Key never stored; redacted in HTTP-error bodies (m-03 closed); receipt key-free (tested); raw body hashed but **not** stored; `StrictModel extra="forbid"` blocks stray fields. Residual: `claimed_outcome` stores the model's guess (O-01, fresh-case handling). Strong. |
| 10 | Daimler/Opus contamination | Fenced by the contract's `direction_change_propagation` receipt; `stale_language_search` run 2026-06-01; Daimler/Opus hits classified as intentional historical caveats, **non-governing**. Adequately handled. Optional clarity only: the contract's `open_next` lists a Daimler Opus review without an inline "historical/non-governing" tag — below the material-ambiguity bar for a no-case smoke test. No finding. |
| 11 | Test blind spots | Highest-risk semantics are well covered. **Single most valuable missing offline test:** one that pins the live-vs-non-live provenance boundary — that a dry / `local_fixture` / `manual_unknown` surface cannot mint a gate-eligible `pass_valid` indistinguishable from a live one (ties to F-01). Secondary: F-03's `partial`+empty classification. |
| 12 | Operator flow gap | **Yes — F-02.** Smallest complete artifact (no-case smoke-test authorization/checklist) is specified in F-02's minimum closure condition, with the reason it is needed (it defines the activity, marks the receipt non-gate-clearing, and captures the provenance F-01 omits). |

---

## 9. Recommendation

**`accept_with_friction`**

The no-tools execution foundation is **coherent enough to support owner consideration of a
separately authorized no-case provider smoke test (or a future fresh-case probe).** The plumbing is
sound and safe at the level this review examined: the gate invariant holds, the live runner derives
isolation from structural request validation against pinned standard endpoints, `--allow-live-provider-call`
guards accidental calls, errors produce no artifact, secrets are not stored, the 22/66 suites pass,
and the two prior majors (M-01, M-02) remain closed. **No critical findings.**

The friction is two **major** auditability gaps that do not threaten gate safety but would make the
**first live receipt unauditable or misleading** if left implicit:

- **F-01** — a `pass_valid` receipt records no execution provenance, so it cannot self-certify it
  came from a validated live execution (a dry/normalized receipt can present identically).
- **F-02** — no operator artifact defines or governs a no-case smoke test, so an authorized run has
  no non-gate-clearing receipt handling or provenance-capture procedure.

These are best resolved **as conditions of the separate smoke-test authorization**, not as blockers
to owner *consideration*. The cheapest sufficient path is doc-only: F-01 option (c) + the F-02
checklist (which also absorbs F-04 capture). F-03 and O-01 are fresh-case-probe items, not no-case
smoke-test blockers. Because major findings remain, `accept` is not available; because the
foundation is coherent for consideration with a clear, bounded friction set, `patch_before_acceptance`
would overstate the blocker.

---

## 10. Review-Use Boundary and Non-Claims

**Review-use boundary.** These findings are **decision input only**. They are not approval,
validation, mandatory remediation, readiness, or executor-ready patch authority until separately
accepted or authorized. Severity labels (`critical/major/minor/optional`) order priority; they do
not by themselves create approval, rejection, readiness, validation, or remediation authority. This
review emits **no `patch_queue_entry`** and holds no patch/implementation authority.

**Non-claims.**
- No live provider call was made; `--allow-live-provider-call` was never passed.
- No live probe, model judgment run, or blind judgment was run.
- No probe pass/fail is claimed; no scoring was performed.
- No participant packet was loaded or exposed.
- No ledger was frozen; no fixture was validated or admitted.
- No schema, runtime, readiness, product-proof, or judgment-quality claim is made.
- No API key was read, printed, or tested.
- This review does not authorize a smoke test, a probe, blind judgment, fixture admission, or gate
  clearing; it supports owner *consideration* only.

plumbing works only; not judgment quality.
