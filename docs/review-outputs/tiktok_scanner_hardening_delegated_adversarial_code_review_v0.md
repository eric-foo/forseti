# TikTok Scanner Hardening Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Findings-first cross-vendor delegated adversarial code review of the TikTok
  creator-scanner hardening branch at 9d1afd9e against base 2e8b0b80, including
  the commissioned bounded-patch decision and validation evidence.
use_when:
  - Adjudicating the scanner-hardening branch before any keep, merge, or downstream reliance.
  - Routing the schema, registry-preflight, and data-lake contract defects found by this pass.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5 (Codex)
authored_by: Anthropic Claude-family (version unrecorded)
de_correlation_bar: cross_vendor_discovery
commission: docs/prompts/reviews/tiktok_scanner_hardening_delegated_adversarial_code_review_patch_prompt_v0.md
review_target: claude/tiktok-scanner-hardening at 9d1afd9eb199d2d0c2545698bfb7f0d706a497d2 vs 2e8b0b809c3fefd1cd37cc5914fe86fa48babfef
mode: delegated_code_review_and_patch
access: repo
source_context_ready: true
patch_status: none_needs_architecture_pass
stale_if:
  - The reviewed target files or branch head change.
  - An architecture pass resolves the receipt/evidence bindings or lake-inventory disposition.
```

## Findings

### F-01 — The new lake touchpoint fails the mandatory inventory contracts

- Commissioned target and purpose: the new frontier-register lake writer and runner, reviewed for correct lake integration and existing-contract regressions.
- Location: `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py:44`; `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:223`; `forseti-harness/tests/contract/test_data_lake_inventory_gate.py:27`; `forseti-harness/tests/contract/test_data_lake_inventory_gate.py:45`.
- Evidence: the full commissioned unit/contract command reached 100 percent and exited 1 with three failures. Fresh discovery added `('capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py', 'append_record'): 1`; the checked-in inventory and the independent contract baseline do not declare it.
- Authority basis: the contract tests explicitly require every new non-raw lake touchpoint to be classified and the checked-in inventory regenerated deliberately. Those contract and inventory paths are flag-only under the commission.
- Impact: the branch fails its mandatory validation gate and cannot be treated as merge-ready. Closing it requires edits outside the named patch set, including a deliberate lake-touchpoint classification/inventory update; the commission says a contract-test rewrite routes to `NEEDS_ARCHITECTURE_PASS`.
- Confidence: high.
- `minimum_closure_condition`: the new writer is deliberately classified in the owning lake inventory and independent contract baseline, with its A2 fork-impact disposition recorded, and `python -m pytest tests/unit tests/contract -q` exits 0 on the resulting branch.
- `next_authorized_action`: architecture/contract pass; no delegate-side edit is authorized by this commission.
- Verification expectation: rerun the full unit/contract command and inspect the regenerated inventory diff.
- `patch_queue_entry` authorized: no.

### F-02 — PROMOTE accepts self-certified, known-negative, and non-string preflight values

- Commissioned target and purpose: the PROMOTE preflight guard, reviewed for vacuous values and false-success onboarding decisions.
- Location: `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py:600`; `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py:605`; `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py:159`.
- Evidence: `_validate_decision` checks only truthiness. Adversarial probes were accepted with `registry_preflight_status_or_none="not_run_suggested_frontier_only"` and with integer `1`. The read-only historical register corpus contains the known-negative `not_run_suggested_frontier_only` marker, proving this is not a contrived vocabulary value.
- Authority basis: `.agents/workflow-overlay/validation-gates.md` requires clearance fields to be owner-produced and provenance-bound or independently verifiable; self-asserted fields do not clear. The Creator Registry usage contract at `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md:27` says clearance comes from a candidate-specific receipt row, not an inferred scalar status.
- Impact: a caller can validate a PROMOTE decision without running exact-match preflight and can promote a node using a value that explicitly says preflight was not run. This defeats the central P5 guarantee.
- Confidence: high.
- `minimum_closure_condition`: PROMOTE consumes a candidate-bound, independently checkable preflight receipt/result rather than a free-form scalar; known-negative, malformed, unrelated, and non-string inputs fail closed.
- `next_authorized_action`: architecture pass to decide the receipt pointer/embedded evidence contract and the exact clearance semantics before code changes.
- Verification expectation: same-check red/green probes for known-negative, unrelated, malformed, wrong-candidate, non-string, and genuine cleared receipt cases.
- `patch_queue_entry` authorized: no.

### F-03 — Materialization accepts a fabricated or unrelated “clean” receipt

- Commissioned target and purpose: the new-account materialization gate, reviewed for bypasses inside the named runner.
- Location: `forseti-harness/runners/run_creator_profile_current_materialize.py:154`; `forseti-harness/runners/run_creator_profile_current_materialize.py:179`; `forseti-harness/capture_spine/creator_profile_current/registry_match_preflight.py:149`; `forseti-harness/tests/unit/test_creator_profile_materialize_preflight.py:38`; `forseti-harness/tests/unit/test_creator_profile_materialize_preflight.py:75`.
- Evidence: the runner calls `has_blocking_preflight_results`, which reduces the decision to truthiness of `summary.blocked_actions`. The passing unit fixture contains no schema version, registry hash, results, candidate identity, or action fields. A probe using that minimal wrapper was accepted while introducing `acct_new`.
- Authority basis: the owning receipt builder emits schema, registry source/hash, summary, and per-candidate results; the usage contract requires candidate-specific `intended_action`, `decision`, `action_status`, and clearance fields. The current gate verifies none of them and does not bind the receipt to `new_ids` or the current output view.
- Impact: any JSON file containing `{"creator_registry_match_preflight_receipt":{"summary":{"blocked_actions":0}}}` can authorize new registry-account materialization, including a receipt for a different registry snapshot or different candidates.
- Confidence: high.
- `minimum_closure_condition`: the runner validates receipt schema and internal summary consistency, verifies the referenced current registry snapshot, and requires every newly introduced account to match an appropriate non-blocking result row; missing, unrelated, duplicate, stale, or malformed rows fail closed.
- `next_authorized_action`: include this implementation closure in the architecture pass after the receipt-binding decision; do not keep an isolated partial fix.
- Verification expectation: same-check red/green tests for fabricated, stale-registry, wrong-candidate, partial-batch, duplicate, blocking, and fully bound clean receipts.
- `patch_queue_entry` authorized: no.

### F-04 — The lake writer does not prove that its raw anchor exists and exposes a duck-typed second-home seam

- Commissioned target and purpose: derived-register persistence, reviewed for correct anchoring, one writable home, append-only behavior, and missing-parent failure.
- Location: `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py:21`; `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py:34`; `forseti-harness/data_lake/root.py:575`; `forseti-harness/data_lake/root.py:807`; `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py:682`.
- Evidence: the writer checks only that the register carries a truthy anchor string, then calls `append_record`. `append_record` enforces containment and no-overwrite but does not require a committed raw packet. The existing success test writes into a newly initialized empty test lake, and an adversarial probe observed `PROBE_MISSING_RAW_PACKET_ANCHOR=ACCEPTED:True`. The public writer also accepts `data_root: Any`, so a duck-typed object can bypass `DataLakeRoot` root verification entirely.
- Authority basis: the writer's own docstring claims the derived record is anchored to committed raw truth and fails closed when no committed parent packet exists. `DataLakeRoot.find_packet`/`load_raw_packet` are the available by-key checks; neither is called.
- Impact: a derived register can be persisted beneath a syntactically plausible but nonexistent anchor, and direct API callers are not constrained to the verified production root implementation. Append-only overwrite protection itself remains intact for genuine `DataLakeRoot` calls.
- Confidence: high.
- `minimum_closure_condition`: the writer accepts only a verified `DataLakeRoot`, verifies the parent raw packet is committed and structurally loadable before append, and tests both genuine committed-anchor success and absent/malformed-anchor failure.
- `next_authorized_action`: include the bounded code/test fix after architecture disposition; no partial patch is kept in this pass.
- Verification expectation: focused writer tests plus the full unit/contract suite.
- `patch_queue_entry` authorized: no.

### F-05 — Link-hub v1 records an assertion, not captured evidence

- Commissioned target and purpose: the v1 link-hub outcome contract, reviewed for skipped-visible-hub and evidence-free captured claims.
- Location: `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py:486`; `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py:501`; `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py:635`; `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py:645`.
- Evidence: `captured` requires only a truthy value in `link_hub_url_or_none`; the probe `link_hub_url_or_none="x"` validated successfully. The schema has no link-hub evidence locator/hash or candidate-specific packet binding. `none_visible`, `blocked`, and `deferred_not_authorized` are likewise self-authored outcomes, so a visible hub can still be silently skipped by asserting `none_visible`.
- Authority basis: the commission requires that a captured claim carry evidence and that a visible link hub cannot fake-pass as skipped. The non-self-certification gate forbids clearing that claim from a by-hand field alone.
- Impact: v1 makes silence syntactically impossible but does not make the claimed outcome trustworthy. It cannot meet the prompt's “cannot fake-pass” objective without an evidence-binding decision.
- Confidence: high.
- `minimum_closure_condition`: the schema/contract binds the outcome to independently checkable source evidence; captured requires a valid credential-free absolute HTTP(S) hub URL and its evidence locator, while non-captured outcomes have explicit evidence/reason semantics that cannot be replaced by a bare scalar assertion.
- `next_authorized_action`: schema/contract architecture pass. The commission forbids a schema redesign in this lane, so no partial URL-only hardening is kept.
- Verification expectation: red/green tests for non-URL, credentialed URL, missing evidence, wrong packet, contradictory status/evidence, and genuine captured/blocked/none-visible cases.
- `patch_queue_entry` authorized: no.

### F-06 — Invalid probe parameters can be reported as clean browser unavailability

- Commissioned target and purpose: the report-only local CDP probe, reviewed for local-only posture and false-unavailable paths.
- Location: `forseti-harness/source_capture/adapters/browser_session_probe.py:27`; `forseti-harness/source_capture/adapters/browser_session_probe.py:39`; `forseti-harness/source_capture/adapters/browser_session_probe.py:49`; `forseti-harness/source_capture/adapters/browser_session_probe.py:67`.
- Evidence: timeout is not checked for finiteness or positivity, and ports are coerced with `int` rather than validated as non-boolean integers in range. Endpoint construction emits `http://::1:9223/json/version` for the explicitly allowed IPv6 loopback host instead of bracketed `http://[::1]:9223/json/version`. A negative-timeout injected probe returned `browser_available=False` rather than rejecting invalid configuration.
- Authority basis: the probe exists to prevent unsupported “no controllable browser session” claims. Invalid probe configuration must be distinguished from a real dead endpoint.
- Impact: caller/operator input errors can become a clean false-unavailability report. The exact host allowlist and absence of credential-bearing URL inputs do prevent non-local and embedded-credential coercion.
- Confidence: high.
- `minimum_closure_condition`: reject non-finite/non-positive timeouts and invalid ports before probing, format IPv6 loopback correctly, and cover each case with injected-opener tests.
- `next_authorized_action`: bounded implementation/test fix after the architecture pass; do not retain it as a partial patch here.
- Verification expectation: focused probe tests plus full unit/contract suite.
- `patch_queue_entry` authorized: no.

### F-07 — The live product contract still requires scan receipt v0

- Commissioned target and purpose: schema-bump completeness across producers, consumers, and decision-bearing contracts.
- Location: `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py:19`; `forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md:168`.
- Evidence: repository search found the implementation constant at `tiktok_creator_discovery_scan_receipt_v1`, while the live product architecture contract says the preferred builder consumes validated `tiktok_creator_discovery_scan_receipt_v0`. Historical `docs/review-inputs/*_scan_receipt_*.json` remain v0 as intended provenance and are not this finding.
- Authority basis: the architecture contract is a live retrieval source, not a historical receipt. The prompt explicitly asks for schema-bump completeness and forbids silently divergent producers/consumers.
- Impact: cold agents following the product contract will produce or expect v0 while the only validator accepts v1, creating a guaranteed contract mismatch once the runner is used.
- Confidence: high.
- `minimum_closure_condition`: an owner/architecture decision confirms the v1 contract, updates the live architecture/usage surfaces and any real producer/consumer together, and explicitly preserves historical v0 receipts as provenance-only inputs.
- `next_authorized_action`: off-scope architecture/product-contract pass; do not edit the contract from this bounded code patch lane.
- Verification expectation: repository-wide exact-version search plus focused runner/validator tests against the accepted v1 file shape.
- `patch_queue_entry` authorized: no.

## Reviewer Verdict

`NEEDS_ARCHITECTURE_PASS`.

The branch has multiple proven fake-pass paths and fails the mandatory full validation gate. F-02 and F-05 require a receipt/evidence schema decision; F-01 requires contract/inventory changes outside the commissioned patch set. Under the commission's escalation rule, no partial source patch is kept. This verdict is decision input for the commissioning Chief Architect, not CA acceptance.

## Patch Summary And Diff

- Source patch: none.
- Changed implementation/test files by this controller: none.
- Reason: the correct closure crosses schema and contract-test boundaries explicitly reserved for an architecture pass; retaining only the locally patchable parts would leave the central false-success paths intact.
- Unified source diff: none.
- Durable output only: this review report.

## Validation Results

### Commissioned gates

- `python -m pytest tests/unit/test_tiktok_creator_discovery_frontier.py tests/unit/test_tiktok_creator_discovery_frontier_selector.py tests/unit/test_browser_session_probe.py tests/unit/test_creator_profile_materialize_preflight.py -q`
  - observed exit: 0
  - observed output: `.......................................................................  [100%]`
- `python -m pytest tests/unit tests/contract -q`
  - observed exit: 1 after 233.9 seconds
  - observed result: three failures, all caused by the undeclared new `append_record` lake touchpoint:
    - `tests/contract/test_capture_runner_lake_seam_coverage.py::test_non_raw_lake_touchpoint_inventory_is_explicit`
    - `tests/contract/test_data_lake_inventory_gate.py::test_inventory_record_matches_fresh_discovery_byte_identical`
    - `tests/contract/test_data_lake_inventory_gate.py::test_declared_inventory_has_no_gate_violations`

### Adversarial probes

- `PROBE_LINK_HUB_VACUOUS_URL=ACCEPTED`
- `PROBE_PROMOTE_NOT_RUN_STATUS=ACCEPTED`
- `PROBE_PROMOTE_NON_STRING_STATUS=ACCEPTED`
- `PROBE_MISSING_RAW_PACKET_ANCHOR=ACCEPTED:True`
- `PROBE_MALFORMED_UNBOUND_PREFLIGHT=ACCEPTED`
- `PROBE_IPV6_URL=http://::1:9223/json/version`
- `PROBE_NEGATIVE_TIMEOUT_BROWSER_AVAILABLE=False`
- Network/browser activity: not run; all probe behavior used injected openers and temporary test roots.

## Source-Read Ledger

- Authority and operating sources, clean at branch HEAD: `AGENTS.md`; overlay README; source-loading, review-lanes, delegated-review-patch, safety-rules; targeted prompt-orchestration, communication-style, and validation-gates sections.
- Method references: `workflow-deep-thinking`; `workflow-code-review`; `workflow-delegated-review-patch` commission/adjudication contract.
- Review input: full `2e8b0b80..9d1afd9e` branch diff; all 11 named target files read in full.
- Required read-only attachments: register builder; relevant data-lake root resolver, append, and by-key raw-read sections; full registry-match preflight implementation; full LinkedIn CDP endpoint validator; source-capture import contract test; rename closeout handoff.
- Targeted expansion: live TikTok frontier product contract, Creator Registry preflight usage note, failing lake seam/inventory contract sources, and the report provenance checker.
- Missing sources: none.
- Dirty/untracked source note: the checkout was clean before review; this report is the only controller-authored durable output.

## Off-Scope Flags

- Lake touchpoint inventory and contract baselines must change or explicitly reject the new writer: `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json` and the two failing contract-test surfaces are outside patch scope.
- The live TikTok frontier architecture contract still names receipt v0 and is outside patch scope.
- Direct calls to `capture_spine.creator_profile_current.materialize.py` remain outside the runner gate; the prompt already names this as a read-only residual.
- The standalone CDP probe is not integrated into a scanner executor; it can report evidence but cannot mechanically prevent another caller from making an unsupported browser-unavailable claim. Scanner-executor architecture is an explicit non-goal here.

## Residual Risks

- No live browser, TikTok capture, or data-lake production write was exercised.
- There is no live v1 scan-receipt producer in the reviewed branch, so end-to-end v1 file/wrapper interoperability remains not proven.
- Fuzzy Creator Registry duplicates remain an accepted limitation of the exact-match preflight and are not widened by this review.
- A novel leak class not represented by the existing forbidden key/value sweep remains possible; the reviewed probe report itself emits no `session` or `cookies` keys.

## Considered And Defended

- Non-local or credentialed CDP endpoints: defended. The probe API uses an exact loopback host allowlist and constructs its own credential-free URL; the CLI does not expose a host override.
- `session`/`cookies` report keys: defended for the reviewed shapes. The probe report does not emit them, and scan/register validators recursively reject those exact keys.
- Runner `--output` plus `--data-root`: defended. `argparse` places them in one mutually exclusive group, and environment roots are considered only when `--output` is absent.
- Derived-record overwrite: defended for genuine `DataLakeRoot.append_record` calls. `_atomic_create` is create-only and refuses an existing target; F-04 is about missing-anchor proof and the duck-typed public seam, not overwrite behavior.
- Historical v0 scan receipts: defended as provenance. The prompt explicitly preserves them; F-07 concerns the still-live product contract only.

## Review Use Boundary

review_use_boundary: >
  These review findings are decision input only. They are not approval,
  validation, mandatory remediation, or patch authority. The commissioning
  Chief Architect decides what is kept and supplies any new architecture or
  implementation authorization.

## Adjudication Closeout Instruction

The commissioning Chief Architect should adjudicate the findings, no-patch disposition, `NEEDS_ARCHITECTURE_PASS` verdict, and residuals as claims. Close any self-closable material issue in the same turn; route the smallest complete architecture/contract closure for the non-self-closable issues; then, only after the review is clean enough to proceed, use one batched land step plus the deep-thought 1-5 material next moves required by `.agents/workflow-overlay/communication-style.md` -> Review Adjudication Next Step.

