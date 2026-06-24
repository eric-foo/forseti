<!-- artifact_role: Orca review output -->
<!-- reviewed_by: claude-sonnet-4-6 (Anthropic) -->
<!-- authored_by: openai-gpt-5-codex (OpenAI) -->
<!-- de_correlation_bar: cross_vendor_discovery -->

# CSB Scanning Artifact Checker — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review output
scope: >
  Adversarial code review of commit b63f7b41: check_csb_scanning_artifact.py,
  its test suite, fixtures, scanning README update, and repo map update.
use_when:
  - CA adjudication of this review's findings.
  - Deciding whether PR #364 is accepted, friction-patched, or rejected.
authority_boundary: retrieval_only
```

## Provenance

```yaml
reviewed_by: claude-sonnet-4-6
authored_by: openai-gpt-5-codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable
source_context_status: SOURCE_CONTEXT_READY
review_commissioned_by: csb_scanning_artifact_checker_adversarial_code_review_prompt_v0.md
target_commit: b63f7b41aa053a8dd09a76adc70f8e6849c11a61
target_branch: codex/csb-scanning-artifact-checker
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-broad-scout-recency-default
review_date: 2026-06-23
edit_permission: read-only
```

## Source-Read Ledger

| Source | Why read | Status | Decision supported |
| --- | --- | --- | --- |
| `.agents/hooks/check_csb_scanning_artifact.py` | Primary review target | clean, HEAD=b63f7b41 | All code-review findings |
| `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py` | Test coverage assessment | clean, HEAD=b63f7b41 | Test-gap findings |
| `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md` | Fixture correctness | clean, HEAD=b63f7b41 | Pattern alignment, false-pass assessment |
| `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_missing_broad_scout.md` | Fixture correctness | clean, HEAD=b63f7b41 | Pattern alignment, false-pass assessment |
| `orca/product/spines/scanning/README.md` | Doctrine and description check | clean, HEAD=b63f7b41 | Artifact/doctrine leakage check |
| `.agents/hooks/check_commission_signal_board_output.py` | Adjacent comparison | clean, commit prior to b63f7b41 | Design consistency |
| `orca-harness/tests/unit/test_commission_signal_board_output_validator.py` | Adjacent comparison | clean | Design consistency |
| `AGENTS.md` | Behavior kernel | clean | Review authority framing |
| `.agents/workflow-overlay/README.md` | Overlay authority | clean | Review authority framing |
| `.agents/workflow-overlay/review-lanes.md` | Review lane contract | clean | Provenance fields, de-correlation |
| `.agents/workflow-overlay/validation-gates.md` | Gate requirements | clean | Validation bucket classification |
| `.agents/workflow-overlay/safety-rules.md` | Safety rules | clean | Scope framing |
| `.agents/workflow-overlay/delegated-review-patch.md` | De-correlation doctrine | clean | cross_vendor_discovery bar |
| `.agents/workflow-overlay/source-loading.md` | Source budget | clean | Source ledger discipline |
| `docs/workflows/orca_repo_map_v0.md` | Repo map description | clean (rg excerpt) | Doctrine leakage check |

**Available not read**: `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` (available; scanning doctrine detail not decision-bearing for receipt-shape review), `.agents/workflow-overlay/prompt-orchestration.md` (not decision-bearing for code review).

**Excluded by default**: review outputs, proof-run packets, method-validation replays, all other product spine files.

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_review_packet
  edit_permission: read-only
  target_scope: Check_csb_scanning_artifact.py change packet for false passes, test gaps, and doctrine leakage
  dirty_state_checked: yes
  blocked_if_missing: not triggered; all required sources confirmed clean at b63f7b41
```

**Workspace state**: branch `codex/csb-scanning-artifact-checker` confirmed. HEAD = `b63f7b41aa053a8dd09a76adc70f8e6849c11a61`. Only untracked file: the review prompt itself — within declared dirty-state allowance.

## Fitness Reference

Goal: reduce LLM memory burden in future CSB-first scanning runs by enforcing the receipt shape that operators otherwise have to remember.

Done looks like: checker catches missing broad-scout, CSB-row, exact-query, cap, closeout, overclaim, and Capture-route-binding mistakes — while explicitly not grading signal quality, proving demand, validating candidates, or binding Capture work.

Axis to attack (not a pass-if-matches bar): can the checker be satisfied by a structurally minimal artifact that violates one of these intents?

---

## Validation Commands Run

| Command | Exit status | Material output |
| --- | --- | --- |
| `python -B .agents\hooks\check_csb_scanning_artifact.py --selftest` | 0 | `PASS bad_missing_broad_scout.md expected fail: missing_broad_scout_accounting`, `PASS valid_csb_first_scan.md`, `SELFTEST OK` |
| `pytest -q tests\unit\test_commission_signal_board_output_validator.py tests\unit\test_csb_scanning_artifact_validator.py` | 0 | 34 tests passed |
| `git diff --check HEAD~1..HEAD` | 0 | No trailing-whitespace issues |
| `python .agents\hooks\check_retrieval_header.py --changed` | 0 | All changed durable `.md` files carry valid retrieval headers |
| `python .agents\hooks\check_placement.py --check` | nonzero | Violations are pre-existing whole-repo issues (`.github`, `.githooks`, `.gitattributes` not in map); none are from the files introduced by this commit |
| `rg -n "recency.*(proof\|proves...)..."` (leakage search) | 0 hits of concern | All hits are: finding-code names in checker machinery, test assertions referencing those codes, stale-search result text in the README DCP receipt, and a correct "enforces receipt shape only" description in the repo map |

`check_repo_map_freshness.py --changed` and `check_map_links.py --strict` were not run — these scripts were not found to exist in the workspace. Noted as not run.

---

## Findings (ordered by severity)

### CR-001 · Major · False pass — null/empty `closeout_state` bypasses validation

**File**: `.agents/hooks/check_csb_scanning_artifact.py`
**Lines**: 150–153

```python
closeout = _normalize_vocab(intake.get("closeout_state"))
if closeout and closeout not in VALID_CLOSEOUT_STATES:
```

`_normalize_vocab(None)` returns `""`. When `closeout_state` is present as a YAML key but has a null or empty value — for example `closeout_state:` or `closeout_state: null` — `closeout` becomes `""`, which is falsy. The `if closeout and ...` guard short-circuits: no `invalid_closeout_state` finding is emitted and the artifact passes closeout validation.

The `missing_intake_fields` check earlier only flags keys absent from the dict entirely; YAML `closeout_state: null` leaves the key present with value `None`, so `missing_intake_fields` does not fire either.

**Proof of bypass**: A minimal intake with `closeout_state:` (YAML null) passes every intake validation gate. The checker emits no finding and exits 0.

**Defense considered**: One could argue that `closeout_state:` in YAML is a malformed artifact and outside realistic use. That argument fails: null-valued required fields are a common author slip; the receipt-shape checker's stated purpose is to catch exactly these mechanical errors so LLMs do not have to remember them.

**Minimum closure condition**: `invalid_closeout_state` must fire whenever `closeout_state` is present but its normalized form is not in `VALID_CLOSEOUT_STATES`. Changing `if closeout and closeout not in VALID_CLOSEOUT_STATES:` to `if closeout not in VALID_CLOSEOUT_STATES:` achieves this — `""` is not in the valid set so it triggers the finding.

**Next authorized action**: CA adjudication; recommend fixing before the checker is referenced in scan artifacts as a passed gate. Patch requires a separate authorized patch turn.

**Red-green proof**: Adding `("closeout_state: no_candidate_after_discovery", "closeout_state:", "invalid_closeout_state")` to `test_intake_contract_failures` would fail against the current code and pass after the fix.

---

### CR-002 · Major · False pass risk — `broad_scout_accounting` text-anywhere match

**File**: `.agents/hooks/check_csb_scanning_artifact.py`
**Lines**: 45–47

```python
"broad_scout_accounting": re.compile(
    r"(^##\s+Broad Scout\b|\bbroad_scout_return\b)",
    re.IGNORECASE | re.MULTILINE,
),
```

The second alternative `\bbroad_scout_return\b` matches the token anywhere in the document — including YAML intake keys, YAML values, or arbitrary prose. An artifact with `broad_scout_return: deferred` in its intake YAML (or even a comment mentioning the term) passes the `broad_scout_accounting` check despite having no actual broad-scout section.

The scanning README states: "broad-scout phase is mandatory by default." An artifact that defers or omits the broad scout phase but mentions `broad_scout_return` in a YAML field satisfies the checker and passes silently.

**Contrast with CSB checker**: `check_commission_signal_board_output.py` uses section-anchored regexes (`^###\s+4\.\s+Signal Board Rows\s*$`) with no text-anywhere alternative. The new checker's second alternative is structurally weaker.

**Defense considered**: `broad_scout_return` is part of the scanning vocabulary; its appearance in a YAML block could represent a structured inline return rather than a section header. If that interpretation is intentional — i.e., a YAML `broad_scout_return` block counts as accounting — then this is correct design. The concern is that `broad_scout_return: skipped` or `broad_scout_return: pending` would also satisfy it.

**Minimum closure condition**: Either (a) the CA confirms the intent: any occurrence of `broad_scout_return` (as YAML key or section header) satisfies broad-scout accounting, including deferred or skipped values; OR (b) if only a populated broad-scout section qualifies, narrow the alternative (e.g., anchor it to a YAML section header or require the section to be non-empty). Until confirmed, this is an open false-pass risk for the mandatory broad-scout requirement.

**Next authorized action**: CA decision on design intent; if narrowing is required, patch in a separate turn.

**Red-green proof**: would need a fixture with `broad_scout_return: deferred` in intake and no `## Broad Scout` section; currently passes, should fail.

---

### MA-001 · Major · Test gap — no tests for `missing_observations` or `missing_closeout`

**File**: `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`
**Lines**: 59–75

`test_required_receipt_parts` covers six of the ten required section patterns but omits:
- `missing_observations` (no test removes `## Observations` or `## Screen-Light Observations` to verify the finding fires)
- `missing_closeout` (no test removes `## Closeout` to verify the finding fires)
- `missing_capture_request_accounting` as an explicit mutation (the bad fixture implicitly passes capture_request_accounting via `capture_requests: 0` in intake, which does not test whether removing both the section AND the intake field triggers the finding)

If either `observations` or `closeout` regex were accidentally broken (e.g., a pattern edit), no test would catch it.

**Defense considered**: The selftest covers the full pattern set at a high level via `bad_missing_broad_scout.md`, which must not produce `missing_observations` or `missing_closeout` findings (those sections are present in the bad fixture). That verifies the patterns don't over-fire but doesn't verify they under-fire correctly when the sections are absent.

**Minimum closure condition**: `test_required_receipt_parts` must include cases that remove `## Observations` and `## Closeout` and confirm the expected findings fire. A `missing_capture_request_accounting` case should also be added, using a fixture variant that removes both the section header and the `capture_requests` intake field.

**Next authorized action**: CA decision; recommend adding parametrized test cases in a separate patch turn. Blocking concern if the checker is to be referenced as tested in scan artifact headers.

---

### MA-002 · Minor · Test gap — no tests for `missing_scan_intake_receipt` or `invalid_yaml_fence`

**File**: `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`

The test suite covers the happy path (valid fixture passes) and intake-field mutations but does not cover:
1. A document with no YAML fences at all → should emit `missing_scan_intake_receipt`
2. A document with a YAML fence but neither `commission_id` nor `source_context_status` → should emit `missing_scan_intake_receipt`
3. A YAML fence with syntactically invalid YAML → should emit `invalid_yaml_fence` and `missing_scan_intake_receipt`

These are robustness cases for the intake detection logic. Their absence means a regression in `_yaml_blocks` or `_find_intake` could go undetected.

**Minimum closure condition**: At least one test each for `missing_scan_intake_receipt` (plain text, no YAML) and `invalid_yaml_fence` (malformed YAML fence).

**Next authorized action**: CA decision; advisory.

---

### MI-001 · Minor · UX friction — misleading error when `source_context_status` is absent

**File**: `.agents/hooks/check_csb_scanning_artifact.py`
**Lines**: 113–119

`_find_intake` requires both `commission_id` and `source_context_status` to identify the intake block:

```python
if "commission_id" in block and "source_context_status" in block:
    return block
```

If a YAML block has `commission_id` but no `source_context_status`, `_find_intake` returns `None`. The caller then emits `missing_scan_intake_receipt` ("No YAML scan intake receipt with commission_id and source_context_status found") rather than the more informative `missing_intake_fields` naming `source_context_status` specifically.

For an author debugging their artifact, the `missing_scan_intake_receipt` message suggests the entire intake block is absent, when it is actually present but missing one field.

**Defense considered**: Requiring both keys as a heuristic is defensible — it uniquely identifies a CSB-first intake block vs. other YAML blocks in the document. The alternative (require only `commission_id`) risks false matches on non-intake blocks.

**Minimum closure condition**: The checker emits a usable diagnostic when the intake block is partially valid. One approach: find by `commission_id` alone, then run full validation (which catches `source_context_status` via `missing_intake_fields`). Another: improve the error message in the `_find_intake` path to name which identifying field is missing.

**Next authorized action**: CA decision; advisory friction fix.

---

### MI-002 · Minor · Semantic ambiguity — `capture_owned` in `route_binding_state` allowed values

**File**: `.agents/hooks/check_csb_scanning_artifact.py`
**Lines**: 240–245

```python
if key_norm == "route_binding_state" and value_norm not in {"", "unknown", "not_bound", "capture_owned"}:
```

`"capture_owned"` is allowed. The intended reading appears to be: Capture has already claimed the route for this capture request, so the scanning artifact is correctly recording that state. However, the value `capture_owned` in a scanning artifact could be misread as scanning making a route-binding decision ("this route is owned by Capture because scanning says so"), which would be a boundary violation.

The forbidden text patterns (`scanning_binds_capture`, `capture_authorized_by_scan`) provide complementary prose-level protection. The YAML-level check is the structural gate.

**Defense considered**: If `capture_owned` means "Capture's lane has already recorded its ownership decision," it is not a scanning route-binding claim — it is an acknowledgment of a prior Capture decision. This is semantically different from `capture_authorized_by_scan` forbidden prose. The valid fixture uses `route_binding_state: unknown`, which is the expected value before Capture acts.

**Minimum closure condition**: Either (a) document the allowed meaning of `capture_owned` in the checker's docstring or inline comment; or (b) remove `capture_owned` from the allowed set if no scanning artifact should ever have this value (scan artifacts should exit with `unknown` or `not_bound`, leaving `capture_owned` for Capture-authored records).

**Next authorized action**: CA decision; advisory.

---

## Artifact and Doctrine Leakage Check (bounded — via workflow-adversarial-artifact-review)

This check applies to the doc surfaces in the mixed change packet: `orca/product/spines/scanning/README.md` and `docs/workflows/orca_repo_map_v0.md`.

**Scanning README** (`orca/product/spines/scanning/README.md`):

- "Before closeout, a fresh CSB-first scan artifact must pass `.agents/hooks/check_csb_scanning_artifact.py` **or record why the checker was not run**." The "must" is bounded by the "or" escape; this correctly describes the checker as a process expectation, not an automated CI-enforced gate. ✓
- "The checker enforces receipt shape only: source context, caps, broad-scout accounting, CSB-row accountability, exact-query accounting, venue/hidden-venue accounting, observations, negatives/access notes, capture-request accounting, and candidate closeout. It does not grade signal quality, prove buyer demand, validate candidates, or bind Capture routes." Clear and accurate. ✓
- The DCP receipt includes `non_claims: [not validation, not readiness, not scan authorization, not capture authorization, not source-access authorization, not implementation authorization]`. ✓
- `stale_language_search_result` states: "No capless crawl, standing monitor, gate-proof leakage, Capture route binding, mandatory subagent-runtime claim, or checker-as-proof leakage was found." Confirmed by independent rg run. ✓
- The README does not describe the checker as validation, proof, readiness, or automatic hook wiring. ✓

**No doctrine leakage found in the README.**

**Repo map** (`docs/workflows/orca_repo_map_v0.md`, excerpt via rg):

- "`.agents/hooks/check_csb_scanning_artifact.py` enforces receipt shape only for future scan artifacts, with fixtures/tests under `orca-harness/tests/`" — correct scope, no automation or CI claim. ✓
- "future scan artifacts" correctly signals the checker is forward-only; existing scan artifacts are not retroactively required to pass. ✓
- No claim of CI integration, automatic blocking, or wired hook. ✓

**No doctrine leakage found in the repo map entry.**

**Retrieval header check** (from `check_retrieval_header.py --changed`): exit 0 — all changed durable `.md` files carry valid retrieval headers. ✓

---

## Not-Assessed Gaps

- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` was not read. It is the controlling authority for the broad-scout mandatory rule and the `broad_scout_return` vocabulary. CR-002's resolution depends on understanding whether `broad_scout_return` as a YAML key in an intake block is a valid receipt form under that spec. This is the one source gap that is decision-bearing for CR-002's disposition.
- `check_repo_map_freshness.py --changed` and `check_map_links.py --strict` were not run (scripts not confirmed present in workspace). These are stale-link and map-freshness checks; their absence is noted as a validation gap but not a known failing gate.
- `orca-harness/tests/unit/test_commission_signal_board_output_validator.py` and adjacent checker were read for comparison but no findings arise from them.

---

## Residual Risks

1. **CR-002 uncertainty**: Until the CA confirms whether `broad_scout_return` as a YAML key (vs. section header) is an accepted receipt form, there is an unresolved false-pass risk for the mandatory broad-scout requirement. If a future scan artifact is authored with `broad_scout_return: skipped` in its intake and no broad-scout section, it passes the checker today.

2. **Test suite fragility for observations/closeout**: MA-001 means that if the observations or closeout patterns break silently, the selftest still passes (those sections are present in the bad fixture, so over-firing is checked but under-firing is not). The checker's reliability for these two sections rests entirely on the selftest's limited fixture coverage.

3. **Incremental fixture growth**: Both current fixtures only test one failure at a time. A real scan artifact with multiple concurrent shape defects may produce findings in a different order or with different specificity than single-defect tests suggest. This is not a blocking risk but represents a coverage ceiling.

---

## Non-Claims

- This review is advisory decision input. It is not validation, readiness, approval, acceptance, or mandatory remediation authority.
- Findings are not pre-authorized for patch execution. Each finding requires CA adjudication before any source edit is made.
- The passing selftest and pytest suite confirm current fixture coverage; they do not prove the checker is correct for all conformant or adversarial inputs.
- Cross-vendor de-correlation (Anthropic reviewer / OpenAI author) satisfies the `cross_vendor_discovery` bar for this pass. It does not prove the checker passes all attack surfaces; a novel shared-vendor blind spot would not be caught by either party's review.

---

## Review-Use Boundary

Review findings are decision input for CA adjudication only. They are not approval, validation, mandatory remediation, or patch-execution authority until the CA separately accepts them and authorizes a patch turn.
