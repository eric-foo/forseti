---
retrieval_header_version: 1
artifact_role: adversarial code review report
scope: >
  Review report for the CSB-first scanning artifact checker mechanical-enforcement
  change packet at dbd7a67d.
use_when:
  - Adjudicating the delegated review findings for the scanning checker enforcement patch.
  - Checking the source-backed review of false-pass, duplicate-emission, and doctrine-leakage risks.
authority_boundary: retrieval_only
commission: csb_scanning_artifact_checker_enforcement_adversarial_code_review_v0
target_commit: dbd7a67d48e11e58445d72ffadb87fe525245fdf
base_commit: c6583dcdab18377c4cb1acea2a8fdcb7e88e5a59
target_branch: codex/csb-scanning-artifact-checker
workspace: worktrees/scanning-broad-scout-recency-default
report_date: 2026-06-23
reviewed_by: claude-sonnet-4-6
authored_by: openai-gpt-5-codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable (cross-vendor: OpenAI author, Anthropic reviewer)
review_lane: adversarial code review (implementation + test package)
output_mode: filesystem-output
report_path: docs/review-outputs/csb_scanning_artifact_checker_enforcement_adversarial_code_review_v0.md
prior_review: docs/review-outputs/csb_scanning_artifact_checker_adversarial_code_review_v0.md
---

# CSB Scanning Artifact Checker Enforcement — Adversarial Code Review v0

## Commission

Commissioned by prompt:
`docs/prompts/reviews/csb_scanning_artifact_checker_enforcement_adversarial_code_review_prompt_v0.md`
in workspace `worktrees/scanning-broad-scout-recency-default`.

**Target**: enforcement hardening commit `dbd7a67d` on branch
`codex/csb-scanning-artifact-checker`. Diff base: `c6583dcd` (the baseline prior to
the enforcement patch, which is the commit immediately prior to the hardening).

**Review purpose**: adversarial implementation review of the enforcement hardening to
`.agents/hooks/check_csb_scanning_artifact.py`, its test suite
(`orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`), its fixture
(`orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md`), and
the accompanying doc/map updates.

## Source-Read Ledger

| Source | Role | Status | Notes |
|---|---|---|---|
| `.agents/workflow-overlay/README.md` | overlay entry point | clean @ HEAD | loaded before work per AGENTS.md |
| `.agents/workflow-overlay/source-loading.md` | loading rules | clean @ HEAD | |
| `.agents/workflow-overlay/review-lanes.md` | review authority | clean @ HEAD | de-correlation bar: cross_vendor_discovery |
| `.agents/workflow-overlay/validation-gates.md` | validation gates | clean @ HEAD | |
| `.agents/workflow-overlay/safety-rules.md` | safety rules | clean @ HEAD | |
| `.agents/workflow-overlay/delegated-review-patch.md` | de-corr mechanics | clean @ HEAD | |
| `.agents/workflow-overlay/prompt-orchestration.md` | prompt contract | clean @ HEAD | |
| `.agents/hooks/check_csb_scanning_artifact.py` | primary target | clean @ HEAD | 664 lines total; ~330 lines added by enforcement patch |
| `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py` | test suite | clean @ HEAD | 277 lines; ~119 added |
| `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md` | valid fixture | clean @ HEAD | updated to satisfy new enforcement |
| `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_missing_broad_scout.md` | bad fixture | clean @ HEAD | not updated; triggers 5 failure codes |
| `orca/product/spines/scanning/README.md` | scanning spine doc | clean @ HEAD | minor recency-vocabulary update |
| `docs/workflows/orca_repo_map_v0.md` | repo map | clean @ HEAD | single entry updated |
| `docs/review-outputs/csb_scanning_artifact_checker_adversarial_code_review_v0.md` | prior review | read-only | for commit `b63f7b41`; 6 findings: CR-001..MI-002 |

HEAD at review time: `4a8aae5b` (`docs: add scanning checker enforcement review prompt`).
This is a prompt-only commit after `dbd7a67d`; per the prompt's `dirty_state_allowance`,
implementation target remains `dbd7a67d`. Confirmed by `git log`.

## Validation Results

All commands run in `worktrees/scanning-broad-scout-recency-default`.

| Command | Result |
|---|---|
| `python .agents/hooks/check_csb_scanning_artifact.py` (selftest) | EXIT 0, SELFTEST OK |
| `pytest -q tests/unit/test_commission_signal_board_output_validator.py tests/unit/test_csb_scanning_artifact_validator.py` | All 72 tests pass |
| `git diff --check c6583dcd..dbd7a67d` | EXIT 0 (no whitespace issues) |
| `python .agents/hooks/check_retrieval_header.py --changed` | EXIT 0 |
| `python .agents/hooks/check_repo_map_freshness.py --changed` | EXIT 0 |
| `python .agents/hooks/check_map_links.py --strict` | EXIT 0, 0 findings (33 annotated non-resolving debt, pre-existing) |
| `python .agents/hooks/check_placement.py --check` | EXIT 0, advisory; 11 violations all pre-existing (`.gitattributes`, `.githooks`, `.github`) — none in the enforcement patch |
| Leakage search (stale vocab, forbidden patterns in changed files) | Clean — no stale `attention and relevance weight`, `not_bound`, `capture_owned`, or proof-language leakage in changed files |

Selftest details for bad fixture:
```
PASS bad_missing_broad_scout.md expected fail:
  exact_queries_count_mismatch, invalid_gate_role, missing_broad_scout_accounting,
  missing_observation_fields, screening_moves_count_mismatch
PASS valid_csb_first_scan.md
```

## Prior Review Remediation

All 6 findings from the prior review (`csb_scanning_artifact_checker_adversarial_code_review_v0.md`,
commit `b63f7b41`) are confirmed remediated in `dbd7a67d`.

| Prior finding | Severity | Remediation in `dbd7a67d` |
|---|---|---|
| CR-001: null `closeout_state` bypass — `if closeout and closeout not in VALID_CLOSEOUT_STATES:` guard allowed null to pass | Critical | Removed: now `if closeout not in VALID_CLOSEOUT_STATES:` (no guard). Confirmed at `_validate_intake` line ~295. |
| CR-002: `broad_scout_accounting` pattern had text-anywhere alternative `\bbroad_scout_return\b` allowing false pass | Critical | Removed: `SECTION_PATTERNS["broad_scout_accounting"]` is now `r"^##\s+Broad Scout\b"` only. |
| MA-001: test gap — no tests for `missing_observations` or `missing_closeout` | Major | Both now in `test_required_receipt_parts` parametrize. |
| MA-002: test gap — `missing_scan_intake_receipt` and `invalid_yaml_fence` tests missing | Minor | Both `test_missing_scan_intake_receipt_without_yaml_fails` and `test_invalid_yaml_fence_fails` present (were present prior; refactored to use `_codes()` helper). |
| MI-001: UX friction — absent `source_context_status` triggered wrong message | Minor | `_find_intake` now gates only on `commission_id`; missing `source_context_status` is caught by `missing_intake_fields` with the correct field name. |
| MI-002: semantic ambiguity — `capture_owned` in `VALID_ROUTE_BINDING_STATES` | Minor | `VALID_ROUTE_BINDING_STATES` is now `{cited_current, unknown, blocked_outside_current_binding, not_applicable}`. `capture_owned` and `not_bound` are rejected. |

## New Findings

### F-001 — False-pass on empty broad-scout section body
**Severity**: Major
**Phase**: correctness
**Location**: `.agents/hooks/check_csb_scanning_artifact.py` lines 366–368

```python
body = _section_body(text, SECTION_PATTERNS["broad_scout_accounting"])
if not body:
    return []
```

**Evidence**: `_section_body` returns `""` when the section heading exists but has no
content before the next `##` heading. `if not body: return []` exits before running any
of the 8 `BROAD_SCOUT_DETAIL_PATTERNS` checks.

**Strongest defense and why it fails**: One could argue that `_validate_required_receipt_parts`
already catches a missing broad-scout section (heading absent → `missing_broad_scout_accounting`).
But the failure mode here is a section that EXISTS (heading present, body empty). An artifact
with exactly `## Broad Scout Return\n\n## CSB Board Intake` passes `_validate_required_receipt_parts`
(heading found) and passes `_validate_broad_scout_detail` (empty body → early return). All 8
broad-scout detail requirements are bypassed. This is a real false-pass path: no finding fires
for an empty broad-scout section.

**Test gap**: No test exercises an artifact with a present-but-empty broad-scout section.

**Impact**: A scanner can satisfy the broad-scout requirement with a bare heading and no
content — the checker's core purpose (enforce that the broad scout ledger documents
frontiers, exact-query risk, venue evaluation, hidden venue pointers, negatives, access
notes, recency/current-state, and deepening direction) is fully bypassed.

**Minimum closure condition**: An artifact with a present but empty broad-scout body must
produce at least one finding. Either: (a) change `if not body: return []` to emit
`missing_broad_scout_detail` listing all 8 patterns as missing, or (b) emit a dedicated
`empty_broad_scout_section` finding. A corresponding test must cover this case.

**Next authorized action**: CA adjudication; patch authorization required.

---

### F-002 — Duplicate `invalid_capture_route_binding_state` emission
**Severity**: Major
**Phase**: correctness
**Location**: `.agents/hooks/check_csb_scanning_artifact.py` lines 456–462
(in `_validate_capture_requests`) and lines 562–568 (in `_validate_yaml_overclaims`)

```python
# _validate_capture_requests (line 456–462):
route_state = _normalize_vocab(request.get("route_binding_state"))
if route_state not in VALID_ROUTE_BINDING_STATES:
    findings.append(Finding("invalid_capture_route_binding_state", ...))

# _validate_yaml_overclaims (line 562–568):
if key_norm == "route_binding_state" and value_norm not in VALID_ROUTE_BINDING_STATES:
    findings.append(Finding("invalid_capture_route_binding_state", ...))
```

**Evidence**: Confirmed via leakage search — both lines emit `"invalid_capture_route_binding_state"`.
`_validate_yaml_overclaims` does a global YAML walk and finds the same `route_binding_state`
already validated per-record by `_validate_capture_requests`. When a capture request contains
an invalid state, `validate_text()` (which returns a list) will contain the finding twice.

**Why tests don't catch this**: The test helper `_codes()` is:
```python
def _codes(text: str) -> set[str]:
    return {finding.code for finding in validator.validate_text(text)}
```
Set-based deduplication silently absorbs the duplicate. All assertions on
`"invalid_capture_route_binding_state" in _codes(...)` pass whether the code appears once
or twice.

**Strongest defense and why it fails**: `_validate_yaml_overclaims` catches
`route_binding_state` in contexts OTHER than capture requests (e.g., candidate observations,
nested structures). But `_validate_capture_requests` already processes every `capture_request_id`
record recursively via `_records`. For any capture request record, the field is checked in
both validators. The YAML overclaims walk's `route_binding_state` check is fully redundant
with `_validate_capture_requests` for the capture-request context.

**Impact**: `validate_text()` returns a list. In production use (e.g., displaying findings in
a report), the same violation appears twice with different message formats (one gives the request
ID, one gives the YAML path). This doubles the finding count for this code, confuses
remediation tracking, and creates a false impression that there are two distinct violations.

**Minimum closure condition**: The `invalid_capture_route_binding_state` code must appear at
most once in `validate_text()` output for a single invalid `route_binding_state` field. Either
remove the `route_binding_state` key check from `_validate_yaml_overclaims` (relying on
`_validate_capture_requests` to cover it), or add a deduplication step in `validate_text()`.
A test must assert the code appears no more than once.

**Next authorized action**: CA adjudication; patch authorization required.

---

### F-003 — `main_deepening` pattern requires brittle exact vocabulary
**Severity**: Moderate
**Phase**: correctness
**Location**: `.agents/hooks/check_csb_scanning_artifact.py` line 147

```python
"main_deepening": re.compile(r"\b(main deepening|recommended deepening|recommended main deepening)\b", re.IGNORECASE),
```

**Evidence**: The pattern accepts only three exact phrases. The review prompt asks: "Does the
broad-scout ledger check enforce meaningful route-ledger shape without making one brittle
paragraph/token the only way to pass?" This pattern does make the vocabulary brittle:
synonymous forms "deepening phase", "targeted deepening", "deepening recommendation",
"recommended for deepening", and "suggest deepening" all fail.

**Contrast**: `access_note` pattern (`r"\b(access notes?|access walls?)\b"`) is more permissive,
accepting singular/plural variants.

**Strongest defense**: The pattern is IGNORECASE and matches the most natural phrasing for a
scanning deepening recommendation. The valid fixture uses `Recommended main deepening:` which
matches. If the scanning operating spec mandates this vocabulary, the pattern is intentional
prescription rather than accidental brittleness.

**Why this falls short**: The scanning operating spec (`orca/product/spines/scanning/README.md`)
does not mandate specific vocabulary for the deepening recommendation. The pattern requires
knowledge of the three magic phrases that is not documented in the scanner-facing spec. A
scanner writing natural English would likely use "recommended deepening" or "main deepening
path" — the latter fails because "main deepening path" does not match `\bmain deepening\b` (the
word boundary cuts off "path" correctly, but "recommended for deepening" fails because "for"
appears between words not in the pattern).

**Impact**: False-positive `missing_broad_scout_detail` (listing `main_deepening`) for valid
scan artifacts that describe the deepening recommendation using natural variation. Adds
friction without adding signal-protection value (the checker's stated purpose is receipt shape).

**Minimum closure condition**: Either (a) broaden the `main_deepening` pattern to accept
common variations (e.g., add `\bdeepen(ing)?\b` as a standalone match), or (b) document in
the scanner-facing spec that the broad scout section must contain one of the exact phrases.

**Next authorized action**: CA decision on vocabulary policy; patch authorization if broadening.

---

### F-004 — Redundant findings when `signal_stage` or `gate_role` is absent from observation
**Severity**: Moderate
**Phase**: correctness
**Location**: `.agents/hooks/check_csb_scanning_artifact.py` lines 415–424

```python
signal_stage = _normalize_vocab(observation.get("signal_stage"))
if signal_stage not in VALID_SIGNAL_STAGES:          # runs even when field absent
    findings.append(Finding("invalid_signal_stage", ...))
gate_role = _normalize_vocab(observation.get("gate_role"))
if gate_role not in VALID_GATE_ROLES:                # runs even when field absent
    findings.append(Finding("invalid_gate_role", ...))
```

**Evidence**: When `signal_stage` is absent, `_normalize_vocab(None)` returns `""`. `"" not in
VALID_SIGNAL_STAGES` is True → `invalid_signal_stage` fires. But `signal_stage` is in
`REQUIRED_OBSERVATION_FIELDS`, so `_required_missing` also fires `missing_observation_fields`
with `signal_stage` listed. The observation gets two findings for the same root cause.

**Observed in selftest**: `bad_missing_broad_scout.md` emits both `missing_observation_fields`
AND `invalid_gate_role` for the same observation (OBS-001 is missing `gate_role`, which is
also in `REQUIRED_OBSERVATION_FIELDS`).

**Contrast (correct pattern)**: Lines 411–413 guard `url` and `retrieval_date` vocabulary
checks with `if "url" in observation:` — so absent fields produce only `missing_observation_fields`,
not also `invalid_observation_url`. The `signal_stage`/`gate_role` checks lack this guard.

**Strongest defense**: Dual findings (both "missing" and "invalid") make it immediately
visible that the field is absent AND that the value is wrong — even if the "wrong" value is
a null. In practice this is surprising rather than helpful because `invalid_gate_role` implies
a field is present but wrong.

**Impact**: Report noise (two findings per absent vocabulary field). Risk of misleading the
scanner — `invalid_gate_role: gate_role must be one of...` implies a wrong value was
provided, not that the field is absent. Makes it harder to diagnose and remediate artifacts.

**Minimum closure condition**: `invalid_signal_stage` and `invalid_gate_role` must only fire
when the field is PRESENT in the observation record but has an invalid value. Apply the
`if "signal_stage" in observation:` / `if "gate_role" in observation:` guard, matching the
existing pattern for `url` and `retrieval_date`.

**Next authorized action**: CA adjudication; patch authorization required.

---

### F-005 — `bad_missing_broad_scout.md` fixture is now a multi-failure fixture
**Severity**: Minor
**Phase**: friction
**Location**: `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_missing_broad_scout.md`

**Evidence**: Selftest output: `PASS bad_missing_broad_scout.md expected fail: exact_queries_count_mismatch, invalid_gate_role, missing_broad_scout_accounting, missing_observation_fields, screening_moves_count_mismatch`. The fixture was designed to test `missing_broad_scout_accounting` (the heading is absent), but with the new enforcement checks, the fixture now additionally triggers:
- `screening_moves_count_mismatch` — `screening_moves_used: 4` in intake but only 1 unique move ID (M01)
- `exact_queries_count_mismatch` — `exact_queries_used: 2` but only 1 EQ ID (EQ-001)
- `missing_observation_fields` — OBS-001 lacks `claim_it_might_support`, `gate_role`, `independence_hypothesis`, `short_quote_or_summary`, `uncertainty_or_limits`
- `invalid_gate_role` — absent `gate_role` in OBS-001 (see F-004)

The fixture was not updated to comply with the new count and observation schema requirements.

**Strongest defense**: The selftest PASSES because the fixture is `fixture_expected: fail`. Any
non-zero finding set satisfies `expected: fail`. The test suite does not break.

**Why this is still a defect**: A targeted failure fixture should document its intent by
failing for ONE reason. A fixture that fails for 5 reasons, only one of which was intended,
degrades testability: (a) future regressions in the four unintended failure modes would be
masked, and (b) the fixture is no longer usable as documentation of the `missing_broad_scout_accounting`
check in isolation.

**Impact**: Test clarity and future regression visibility. Does not block current correctness.

**Minimum closure condition**: Either (a) update `bad_missing_broad_scout.md` to have
consistent counts and correct observation schema (so it fails only for `missing_broad_scout_accounting`),
or (b) add a comment in the fixture noting it intentionally tests multiple failures and listing
which ones are intentional.

**Next authorized action**: CA adjudication; advisory.

---

### F-006 — `_validate_csb_row_ids` false positive for zero-row scans
**Severity**: Minor
**Phase**: correctness
**Location**: `.agents/hooks/check_csb_scanning_artifact.py` line 375–378

```python
def _validate_csb_row_ids(text: str) -> list[Finding]:
    if SECTION_PATTERNS["csb_row_accounting"].search(text) and not CSB_ROW_ID_RE.search(text):
        return [Finding("missing_csb_row_ids", "CSB row accounting must cite at least one SBR-NNN row id.")]
    return []
```

**Evidence**: `SECTION_PATTERNS["csb_row_accounting"]` matches `r"(csb_rows_consumed|Rows consumed as route map:)"`.
If an intake has `csb_rows_consumed: 0`, the pattern matches. No SBR-NNN IDs would exist in a
legitimate zero-row scan. `CSB_ROW_ID_RE.search(text)` would return None → `missing_csb_row_ids` fires.

**Strongest defense**: Zero-row scans (no CSB rows consumed) are valid but likely uncommon;
the checker may be intentionally requiring that any scan that uses the `csb_rows_consumed` key
must also cite at least one row, even if count is zero — forcing consistency. Also,
`csb_rows_consumed: 0` in YAML is parsed as integer 0, which when stringified in the regex
match does not produce `csb_rows_consumed: 0` as a text match — the regex matches the KEY
`csb_rows_consumed` in the text, not the value. So `csb_rows_consumed: 0` in text does match
the pattern.

**Why this is still a concern**: A valid scan with no rows consumed would have
`csb_rows_consumed: 0` in its intake (or the intake would omit the field). If the field is
present with value 0, `missing_csb_row_ids` fires as a false positive. The validator gives
no way to distinguish "zero rows consumed and correctly citing none" from "claimed to consume
rows but cited none."

**Impact**: Valid zero-row scans would need to either (a) omit `csb_rows_consumed` entirely
(suppressing the check) or (b) manually suppress the finding. Minor friction for edge-case scans.

**Minimum closure condition**: Either gate the check on `csb_rows_consumed != 0` (parse the
value from the intake), or document that `csb_rows_consumed: 0` must not appear when no rows
were consumed (use omission or a different key to signal zero rows).

**Next authorized action**: CA decision on scanning spec; advisory.

---

### F-007 — Count consistency checks use document-wide text scan, not section-scoped
**Severity**: Minor
**Phase**: correctness
**Location**: `.agents/hooks/check_csb_scanning_artifact.py` lines 386–387

```python
("screening_moves_used", len(set(MOVE_ID_RE.findall(text))), "screening_moves_count_mismatch"),
("exact_queries_used", len(set(EXACT_QUERY_ID_RE.findall(text))), "exact_queries_count_mismatch"),
```

**Evidence**: `MOVE_ID_RE = re.compile(r"\bM\d{2,}\b")` and `EXACT_QUERY_ID_RE = re.compile(r"\bEQ-\d{3,}\b")`
search the entire document text. Contrast with hidden venue pointer and capture request counts
which use YAML record lookups (`_records(blocks, "hidden_venue_pointer_id")`), which are
inherently scoped to structured YAML.

**Strongest defense**: In practice, move IDs (M01, M02) and exact query IDs (EQ-001) are
distinctive enough that they are unlikely to appear in unrelated prose. The set-based
deduplication also means multiple references to the same ID in different sections don't inflate
the count.

**Why this is still a risk**: An artifact that legitimately references prior-scan move IDs in
context (e.g., "This scan extends M01 and M02 from the prior scan...") would have those IDs
counted, inflating the apparent unique move count. The scanner would then need to adjust
`screening_moves_used` to include the cross-referenced IDs, which conflates current-scan moves
with prior-scan references.

**Impact**: False-positive `screening_moves_count_mismatch` or `exact_queries_count_mismatch`
for artifacts that reference prior move IDs as context. Uncommon in current scanning practice
but possible.

**Minimum closure condition**: Either (a) document that all `M\d{2+}` and `EQ-\d{3+}` IDs
anywhere in the document count toward the declared totals, or (b) scope the count to the
Venue Evaluation Move Log section body.

**Next authorized action**: CA decision on scanning spec; advisory.

---

### F-008 — Closeout section substring check uses normalized form against raw body
**Severity**: Minor
**Phase**: correctness
**Location**: `.agents/hooks/check_csb_scanning_artifact.py` line 514

```python
if closeout and closeout not in body:
    findings.append(Finding("closeout_state_not_in_closeout_section", ...))
```

**Evidence**: `closeout` is the normalized form (underscores, lowercase, e.g.,
`"no_candidate_after_discovery"`). `body` is the raw closeout section text. The check does a
raw Python substring search for the normalized form in the raw body. An artifact whose closeout
section writes the state as `"No Candidate After Discovery"` (natural prose) or
`"no-candidate-after-discovery"` (hyphenated) would not contain the normalized substring, firing
a false-positive finding.

**Strongest defense**: The valid fixture demonstrates the expected convention: the closeout
section contains the state in backtick code formatting with underscores (e.g.,
`` `no_candidate_after_discovery` ``). Given all `VALID_CLOSEOUT_STATES` use snake_case already,
the most natural way to write the state is with underscores. In practice, false positives here
are unlikely if scanners follow the convention shown in the fixture.

**Why this is worth flagging**: The convention is implicit — there is no explicit documentation
requiring scanners to use the underscored form in the closeout prose. An author who writes
"This scan closes as no-candidate-after-discovery" would trigger a false positive. The valid
fixture teaches the correct form, but there is no spec enforcement of it beyond this implicit
check.

**Impact**: False-positive `closeout_state_not_in_closeout_section` for valid artifacts that
write the closeout state name in non-underscored natural prose. Low probability in practice.

**Minimum closure condition**: Either (a) document in the scanning spec that the closeout
section prose must contain the exact underscored state name as a literal substring, or (b)
normalize the body text before the substring check (e.g., `if closeout and closeout not in
_normalize_vocab(body):`).

**Next authorized action**: CA decision; advisory.

---

## Summary Table

| Finding | Severity | Area | Closure required |
|---|---|---|---|
| F-001: Empty broad-scout body false pass | Major | checker logic | Yes — blocker |
| F-002: Duplicate `invalid_capture_route_binding_state` emission | Major | checker logic + test gap | Yes — blocker |
| F-003: `main_deepening` brittle vocabulary | Moderate | checker logic | CA vocabulary decision |
| F-004: Redundant findings for absent `signal_stage`/`gate_role` | Moderate | checker logic | Yes — patch advised |
| F-005: `bad_missing_broad_scout.md` multi-failure fixture | Minor | test fixture | Advisory |
| F-006: `_validate_csb_row_ids` false positive for zero-row scans | Minor | checker logic | CA spec decision |
| F-007: Count consistency uses document-wide regex | Minor | checker logic | CA spec decision |
| F-008: Closeout substring check uses normalized form vs raw body | Minor | checker logic | Advisory |

**Net assessment**: The enforcement patch correctly remediates all 6 prior review findings and
adds substantial mechanical enforcement across observation schema, capture request schema,
count consistency, route vocabulary, and closeout consistency. Two major issues were found
(F-001: empty-body false pass; F-002: duplicate emission masked by test helper). Neither
creates doctrine leakage or quality-signal bypass — both are checker-correctness defects. The
test suite is comprehensive for the happy path but has two structural gaps (empty broad-scout
body, no assertion on finding count for F-002). Five moderate/minor findings are advisory.

## Review-Use Boundary

These findings are decision input for the Chief Architect; they are not approval, validation,
mandatory remediation, readiness, or patch-queue authority. Only a separately authorized
patch, acceptance, validation, lifecycle, or implementation lane can make remediation
mandatory or executor-ready. The two major findings (F-001, F-002) represent real false-pass
and duplicate-emission paths and warrant CA adjudication before this checker is used as a
hard gate on new scan artifacts.
