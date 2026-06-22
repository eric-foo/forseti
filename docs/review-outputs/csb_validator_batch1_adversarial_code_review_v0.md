# CSB Validator Batch 1 Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial code review report
scope: >
  Read-only adversarial code review findings for PR #360 CSB validator Batch 1.
use_when:
  - Adjudicating or patching PR #360 CSB validator Batch 1 review findings.
  - Checking the review evidence behind the unknown-mode cutoff bypass patch.
authority_boundary: retrieval_only
```
```yaml
review_meta:
  pr: "#360 - Harden CSB output validator structure checks"
  review_type: adversarial_code_review
  output_mode: filesystem-output
  report_path: docs/review-outputs/csb_validator_batch1_adversarial_code_review_v0.md
  commission: read-only adversarial code review; no patch queue; no approval or readiness claim
  worktree: C:\Users\vmon7\Desktop\projects\orca\worktrees\csb-validator-batch1
  source_loading_mode: zero-config findings-only advisory review
  review_skill_applied: workflow-code-review (zero-config advisory mode)
  deep_thinking_applied: yes (failure mode framing before findings)
  date: 2026-06-23
```

---

## Source-Read Ledger

| File | Role | Status |
| --- | --- | --- |
| `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.86\skills\workflow-deep-thinking\SKILL.md` | Skill contract (REFERENCE-LOAD) | READ |
| `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.86\skills\workflow-code-review\SKILL.md` | Skill contract (REFERENCE-LOAD) | READ |
| `.agents/hooks/check_commission_signal_board_output.py` | Primary review target — validator implementation | READ |
| `orca-harness/tests/unit/test_commission_signal_board_output_validator.py` | Primary review target — unit tests | READ |
| `orca-harness/tests/fixtures/commission_signal_board_outputs/valid_empty_backtest_output.txt` | Primary review target — valid fixture | READ |
| `orca-harness/tests/fixtures/commission_signal_board_outputs/valid_source_backed_backtest_output.txt` | Primary review target — valid fixture | READ |
| `orca-harness/tests/fixtures/commission_signal_board_outputs/valid_source_backed_forward_output.txt` | Primary review target — valid fixture | READ |
| `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` | Primary review target — playbook/description | READ |
| `docs/prompts/handoffs/imaginary_authors_csb_broad_scout_deep_scan_handoff_prompt_v0.md` | Context — NOT FOUND (file does not exist at that path) | MISSING |
| `.agents/workflow-overlay/delegated-review-patch.md` | Context — review convention | READ |
| `.agents/workflow-overlay/review-lanes.md` | Context — review authority | READ |
| `.agents/workflow-overlay/prompt-orchestration.md` | Context — prompt mechanics | READ |
| All 10 existing fixture files (7 bad_ + 3 valid_) | Evidence via selftest + inline | READ (7 bad via selftest output and targeted reads of 2 representative ones) |

---

## Worktree State Verification

```
HEAD observed:     995d107f6b65e38c978d22e3ef2050f28e30a367
Expected HEAD:     8287a079...  (from commission)
origin/main:       532f01038668455b774bb70dc05aa633ad5bca0e  (MATCHES expected)
```

**HEAD MISMATCH NOTED.** The worktree HEAD is one commit ahead of the commissioned
SHA `8287a079`. The extra commit `995d107f` adds only
`docs/prompts/reviews/csb_validator_batch1_adversarial_code_review_prompt_v0.md`
(the review-commission prompt) — a doc-only change that does not touch any
implementation target. All five implementation files named in the commission are
present and unchanged in the diff at the commissioned SHA. This mismatch is a
worktree timing artifact, not a blocking evidence gap. Review proceeds against the
full implementation set, which is on top of the commissioned base.

Diff filelist (origin/main..HEAD, implementation targets):
```
.agents/hooks/check_commission_signal_board_output.py
orca-harness/tests/fixtures/commission_signal_board_outputs/valid_empty_backtest_output.txt
orca-harness/tests/fixtures/commission_signal_board_outputs/valid_source_backed_backtest_output.txt
orca-harness/tests/fixtures/commission_signal_board_outputs/valid_source_backed_forward_output.txt
orca-harness/tests/unit/test_commission_signal_board_output_validator.py
orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
```

Git status: clean (no untracked or unstaged changes).

---

## Validation Evidence

**Selftest (`python -B .agents\hooks\check_commission_signal_board_output.py --selftest`):**

```
PASS bad_aeo_future_info_in_handoff_output.txt expected fail: handoff_row_aeo_visibility, handoff_row_cutoff_invalid, handoff_row_future_info, handoff_row_surface_cutoff_invalid, invalid_section_contract, missing_board_status_section
PASS bad_forward_excluded_future_info_handoff_output.txt expected fail: handoff_row_future_info, invalid_section_contract, missing_board_status_section
PASS bad_missing_handoff_mode_backtest_output.txt expected fail: invalid_section_contract, missing_board_status_section, missing_handoff_mode, missing_handoff_packet_fields
PASS bad_mixed_case_aeo_handoff_output.txt expected fail: handoff_row_aeo_visibility, invalid_section_contract, missing_board_status_section
PASS bad_surface_cutoff_uncertain_handoff_output.txt expected fail: handoff_row_surface_cutoff_invalid, invalid_section_contract, missing_board_status_section
PASS bad_to_retrieve_in_handoff_output.txt expected fail: handoff_row_not_source_backed, invalid_section_contract, missing_board_status_section
PASS bad_uncertain_cutoff_in_handoff_output.txt expected fail: handoff_row_cutoff_invalid, invalid_section_contract, missing_board_status_section
PASS valid_empty_backtest_output.txt
PASS valid_source_backed_backtest_output.txt
PASS valid_source_backed_forward_output.txt
SELFTEST OK
```

**Pytest (`python -m pytest ... test_commission_signal_board_output_validator.py -q`):**

```
..................                                                       [100%]
```

18 tests passed. No failures, no errors.

**Whitespace check (`git diff --check origin/main..HEAD`):**

No output. No whitespace errors in the diff.

**SOURCE_CONTEXT_READY** with one gap: `docs/prompts/handoffs/imaginary_authors_csb_broad_scout_deep_scan_handoff_prompt_v0.md` does not exist at the path named in the commission. This handoff file is context-only per the commission; its absence does not block the primary review targets.

---

## Failure Mode Framing (workflow-deep-thinking output)

Using `workflow-deep-thinking`.

**Real question:** What are the deterministic fake-pass modes this validator is supposed to prevent? And where does the implementation leave residual pass gaps?

**The validator's core job** is to prevent two classes of corruption:

1. *Structural corruption* — an output that is not a real full board (missing sections, wrong section order, broken table, invalid vocab) passes as if it were a complete board.
2. *Handoff corruption* — rows that are ineligible for classifier handoff (not source-backed, future info excluded, AEO visibility, backtest cutoff violations) slip into the handoff packet.

**Attack surface analysis by layer:**

**Layer 1: Section contract.** The validator checks that exactly sections 1–10 appear in order using a regex over all lines. A determined bypasser cannot omit a section heading and have the validator pass (strict equality check). However, the regex is NOT fence-aware — it would misfire if a YAML or code block contains a line starting with `### N. Title`. Testing confirms this is not a practical concern for the `### N.` pattern (digits-dot prefix) because real YAML values would not naturally include such lines, and YAML comment lines start with `#` not `###`. The more important direction is the OTHER way: a line like `### 11. Injected` inside a YAML fence would fail the contract correctly (extra heading injected). The fence-blindness creates a brittleness for boards that evolve to include sub-headers, but not a fake-pass risk.

**Layer 2: Row parsing.** The validator enforces `SBR-NNN` format, monotonic ordering, duplicate detection, and 8-column vocab checks. Monotonic ordering catches gaps (SBR-001, SBR-004) but fires `non_monotonic_row_id` — it does NOT prevent the out-of-order row from being added to `rows`. The consequence: SBR-004 is in `rows`, and the next expected ID counter increments from `len(rows)=2`, so SBR-005 would expect SBR-003. This creates cascading noise codes for subsequent rows but does not create a fake-pass (the non-monotonic row itself fires a finding).

**Layer 3: Handoff packet shape.** `_validate_packet_shape` enforces required fields, `classifier_mapping_status: classifier_owned`, and `prohibited_claims` as a list of strings. The `classifier_owned` check uses `_normalize_vocab` (normalizes case, replaces non-alphanumeric with underscores) so `"Classifier_Owned"` or `"CLASSIFIER OWNED"` would both normalize to `classifier_owned` and pass — this is intentional normalization. The `prohibited_claims` check only verifies list-of-strings shape, not content — any strings pass.

**Layer 4: Mode and handoff row validation.** `backtest` mode enforces both `cutoff_status: in_window` and `surface_cutoff_status: existed_by_cutoff`. `forward` mode enforces only evidence status (source_backed) and AEO/future-info exclusions. **`unknown` mode skips all cutoff checks entirely** — a board with `mode: unknown` can include handoff rows with `cutoff_status: uncertain` and `surface_cutoff_status: post_cutoff_surface` without triggering any finding. This is the largest semantic gap: `unknown` mode is a blanket cutoff bypass.

**Layer 5: Section 10 board status.** The status check requires `board_status` in a controlled vocab, `run_boundary` in a controlled vocab, and `next_authorized_step` present. The check is sound for its scope. It does not prevent operators from claiming `READY_FOR_RETRIEVAL_HANDOFF` when rows are actually `to_retrieve` (that is explicitly out of scope for a mechanical validator).

**Subtle structural interaction:** `status_packet` is only checked via `_validate_board_status_shape` when `status_packet` is truthy (non-empty dict). `parse_board_status` returns `{}` on parse failure, which is falsy — so `_validate_board_status_shape` is correctly skipped on Section 10 parse failure. The structural findings (`missing_board_status_section`, `missing_board_status_yaml`, `invalid_board_status_yaml`) are emitted via `status_findings` before the early return, so they always appear. This is correct behavior.

**The main fake-pass vectors remaining:**
- `mode: unknown` bypasses all cutoff enforcement.
- Negative fixtures only have partial boards (sections 1, 4, 8) so they also fire `invalid_section_contract` and `missing_board_status_section` — making them structurally misleading as behavioral specimens, though tests still pass because they use containment checks.
- No selftest coverage for the 19 new error codes from Batch 1 (selftest only runs fixture files; the new codes are exercised only by pytest mutation tests).

---

## Findings

### F-01 — `mode: unknown` bypasses all cutoff enforcement (material semantic gap)

- **finding_id:** F-01
- **commissioned target:** `check_commission_signal_board_output.py` — handoff row validation
- **file and anchor:** `.agents/hooks/check_commission_signal_board_output.py`, function `_validate_handoff_row` (lines 331–380), constant `VALID_HANDOFF_MODES = {"backtest", "forward", "unknown"}` (line 60)
- **implementation evidence:** `_validate_handoff_row` only applies `cutoff_status` and `surface_cutoff_status` checks inside `if mode == "backtest":`. The `forward` mode skips those checks by design (forward boards have no cutoff boundary). The `unknown` mode also skips them. A board with `mode: unknown` can include handoff rows with `cutoff_status: uncertain`, `surface_cutoff_status: post_cutoff_surface`, or even `cutoff_status: post_cutoff_excluded` and the validator will pass. Verified by runtime test: substituting `mode: backtest` with `mode: unknown` in the source-backed backtest fixture with an `uncertain` cutoff row returns zero findings.
- **authority / evidence basis:** The commission signal board playbook (`What The Validator Checks`) says the validator should fail when "in backtest mode, lacks `surface_cutoff_status: existed_by_cutoff`" and "in backtest mode, lacks `cutoff_status: in_window`" — it explicitly scopes these to backtest mode. The `unknown` bypass is not described as intended or blocked. The purpose of `unknown` mode (`VALID_HANDOFF_MODES = {"backtest", "forward", "unknown"}`) is not documented in the checker source. The cutoff exclusion rule ("only source observations observable on or before the cutoff date may enter downstream handoff") is the core safety invariant; `unknown` mode is an escape hatch that silently bypasses it.
- **correctness/validation/runtime/review-confidence impact:** A board author can relabel any backtest as `mode: unknown` to bypass cutoff enforcement and pass the validator. This is the most direct fake-pass route for cutoff safety. The AEO and `excluded_future_info` blocks still fire in `unknown` mode (they are not gated on mode), so the bypass is specific to the cutoff fields.
- **minimum_closure_condition:** Either (a) `unknown` mode must be removed from `VALID_HANDOFF_MODES` and the field-level handling, or (b) the cutoff checks must also apply in `unknown` mode with appropriate vocab allowance (e.g., `not_applicable` as a permitted cutoff status for truly mode-agnostic boards), or (c) the intended semantics of `unknown` mode must be documented and the checker must enforce that `unknown` mode rows may only have `cutoff_status: not_applicable` (not `uncertain` or `post_cutoff_excluded`). Before this finding is closed, the intent of `unknown` mode must be stated and the enforcement gap must either be closed or explicitly accepted with a documented rationale.
- **next_authorized_action:** Owner decision on `unknown` mode semantics; review finding only, no patch authority.
- **verification expectation:** A new test `test_unknown_mode_does_not_bypass_cutoff` or a fixture `bad_unknown_mode_uncertain_cutoff_output.txt` (expected fail) would provide same-check proof.
- **patch_queue_entry:** no

---

### F-02 — Negative fixtures are now structurally incomplete boards (misleading failure mode coupling)

- **finding_id:** F-02
- **commissioned target:** `orca-harness/tests/fixtures/commission_signal_board_outputs/bad_*.txt` (all 7 files); `test_invalid_commission_signal_board_outputs_fail`
- **file and anchor:** All 7 `bad_` fixtures; test file lines 41–60
- **implementation evidence:** The 7 existing negative fixtures only contain sections 1, 4, and 8 (the pre-PR required set). Under the new validator, all 7 now also fire `invalid_section_contract` and `missing_board_status_section` in addition to their intended target code. The selftest reports them as PASS because selftest checks `expected == "fail" and not passed` (any finding counts). The pytest tests use containment (`assert (expected_code, expected_row_id) in {...}`), so extra codes do not break the tests. However: (a) the selftest output is now diagnostically noisy — an operator inspecting a bad fixture will see 3 codes but the fixture description names 1, (b) the fixtures cannot serve as self-describing specimens of single-failure behavior, and (c) the `fixture_failure:` comment in the header no longer fully describes the actual failure output.

  Observed failure code sets from runtime:
  - `bad_uncertain_cutoff_in_handoff_output.txt`: `['invalid_section_contract', 'missing_board_status_section', 'handoff_row_cutoff_invalid']`
  - `bad_aeo_future_info_in_handoff_output.txt`: `['handoff_row_aeo_visibility', 'handoff_row_cutoff_invalid', 'handoff_row_future_info', 'handoff_row_surface_cutoff_invalid', 'invalid_section_contract', 'missing_board_status_section']`

- **authority / evidence basis:** The commission says valid fixtures should be "full-board examples that actually exercise the new parser surface." The negative fixtures are the inverse: they test handoff row validation against partial boards. The partial-board structure now adds structural findings that were not present before Batch 1, coupling two orthogonal failure modes.
- **correctness/validation/runtime/review-confidence impact:** Tests pass. Selftest passes. Operational risk is low. Review-confidence impact is moderate: future authors of test cases for handoff row validation will see misleading output if they run selftest to debug. The fixture pedagogical value is degraded.
- **minimum_closure_condition:** Either (a) the negative fixtures are updated to include all 10 sections (making them full-board bad fixtures that isolate only the intended handoff row failure), or (b) the fixture header comments are updated to list all expected codes under the new validator, or (c) a deliberate policy decision is recorded that partial-board negative fixtures are acceptable because tests use containment checks. Before closing, the coupling should be either resolved or explicitly accepted.
- **next_authorized_action:** Owner decision on whether to update fixtures or accept the coupling; review finding only.
- **verification expectation:** If fixtures are updated to full boards, the selftest output line should show only the target failure code, not the structural codes.
- **patch_queue_entry:** no

---

### F-03 — Selftest does not cover any of the 19 new Batch 1 error codes (selftest coverage gap)

- **finding_id:** F-03
- **commissioned target:** `.agents/hooks/check_commission_signal_board_output.py` — `selftest()` function (lines 489–510)
- **file and anchor:** `selftest()` function; fixture directory `orca-harness/tests/fixtures/commission_signal_board_outputs/`
- **implementation evidence:** The `selftest()` function only exercises fixture files on disk. All 7 negative `bad_` fixtures test pre-Batch-1 handoff row violations. No negative fixtures were added for the 19 new codes introduced in Batch 1:
  `invalid_section_contract`, `invalid_row_id_format`, `non_monotonic_row_id`, `invalid_source_family`, `invalid_signal_role`, `invalid_row_purpose`, `invalid_graph_role`, `invalid_graph_weight_hint`, `invalid_evidence_status`, `invalid_surface_cutoff_status`, `invalid_cutoff_status`, `missing_handoff_packet_fields`, `invalid_classifier_mapping_status`, `invalid_prohibited_claims`, `missing_board_status_yaml`, `invalid_board_status_yaml`, `invalid_board_status`, `invalid_run_boundary`, `missing_next_authorized_step`.

  All 19 codes are exercised only by pytest mutation tests (string substitution on valid fixtures). The selftest is the operator-facing gate described in the playbook for field use; it does not cover the new surface.

- **authority / evidence basis:** The playbook describes selftest as the routine operator gate: `python -B .agents\hooks\check_commission_signal_board_output.py --selftest`. If the selftest passes but a new check is broken, the operator has no signal.
- **correctness/validation/runtime/review-confidence impact:** Correctness of the new checks is verified by pytest. The selftest gap is a regression-detection risk: a future edit that accidentally breaks one of the 19 new checks would pass selftest undetected. The pytest gate would catch it, but selftest is the lower-friction first line of defense for manual operator use.
- **minimum_closure_condition:** At minimum, one `bad_` fixture per new structural check category should be added so that selftest exercises the new codes. A minimum viable set would cover: `invalid_section_contract`, one vocab failure (`invalid_source_family` or similar), `invalid_row_id_format`, `non_monotonic_row_id`, one packet shape failure (`missing_handoff_packet_fields`), and one Section 10 failure (`invalid_board_status`). Six fixtures would cover the new categories without creating fixtures per-code for all 19.
- **next_authorized_action:** Owner decision on selftest coverage target; review finding only.
- **verification expectation:** After adding fixtures, `python -B .agents\hooks\check_commission_signal_board_output.py --selftest` should show PASS lines for the new codes.
- **patch_queue_entry:** no

---

### F-04 — `validate_text` skips `_validate_board_status_shape` when packet fails but Section 10 is structurally valid (silent failure combination)

- **finding_id:** F-04
- **commissioned target:** `.agents/hooks/check_commission_signal_board_output.py` — `validate_text` function (lines 434–478)
- **file and anchor:** `validate_text`, lines 475–477 (`if status_packet: findings.extend(...)`) and lines 440–441 (`if packet_findings or not rows: return findings`)
- **implementation evidence:** The early return at line 440–441 (`if packet_findings or not rows: return findings`) fires before `_validate_board_status_shape` is called. The `status_findings` (structural findings from `parse_board_status`) ARE included in `findings` at that point and will appear. But if Section 10 is structurally valid (parses to a non-empty `status_packet`) while the packet has errors AND Section 10 has an invalid `board_status` or missing `next_authorized_step`, the early return suppresses the Section 10 shape findings.

  Verified by runtime test: a fixture with a missing `classifier_mapping_status` AND `board_status: MADE_UP` produces codes `['missing_handoff_packet_fields', 'invalid_classifier_mapping_status', 'invalid_board_status']`. So Section 10 shape IS checked when the packet has non-empty-dict findings. Further investigation reveals: `status_packet` is set from `parse_board_status` BEFORE the early return check, and `if status_packet:` check is AFTER the early return. When packet_findings is non-empty, the early return fires, `if status_packet:` is never reached. However, the observed test shows `invalid_board_status` IS produced — because `status_findings` (from `parse_board_status`) includes the structural parsing findings, not the shape findings. The shape findings (`invalid_board_status`, `invalid_run_boundary`, `missing_next_authorized_step`) come from `_validate_board_status_shape`, which is only called in the non-early-return path.

  Correction to the above: runtime test (`text_bad`) shows `invalid_board_status` IS in the output even with packet errors. Re-examining: `status_findings` captures results of `parse_board_status` which includes `_validate_board_status_shape`? No — `parse_board_status` only parses; `_validate_board_status_shape` is called separately. Let me reconcile: the test shows `['missing_handoff_packet_fields', 'invalid_classifier_mapping_status', 'invalid_board_status']`. `invalid_board_status` comes from... `_validate_board_status_shape`. But the early return should have stopped before that call. This needs re-examination.

  Re-reading `validate_text`: `findings = [*section_findings, *row_findings, *packet_findings, *status_findings]` then `if packet_findings or not rows: return findings`. In the test: `text_bad` has `missing_handoff_packet_fields` and `invalid_classifier_mapping_status` in `packet_findings`? No — those come from `_validate_packet_shape`, which is called AFTER the early return check. So the early return must be firing BEFORE `_validate_packet_shape` is called. But then how does `invalid_board_status` appear?

  Closer reading of the code flow:
  1. `packet_findings` comes from `parse_classifier_handoff` — this only checks YAML structure, NOT packet shape. The function returns `(packet, [])` if packet YAML parses successfully.
  2. When `classifier_mapping_status` is removed, the YAML still parses. `packet_findings = []`. `not rows = False` (rows exist). Early return does NOT fire.
  3. `_validate_packet_shape` IS called, producing `missing_handoff_packet_fields` and `invalid_classifier_mapping_status`.
  4. `if status_packet:` IS reached — `_validate_board_status_shape` IS called.

  So the early return only fires when `parse_classifier_handoff` itself returns findings (YAML missing/invalid/lacks `classifier_handoff_packet`), not when `_validate_packet_shape` finds issues. This is the actual control flow. F-04 as originally framed is less severe than stated: `_validate_board_status_shape` IS called whenever the YAML parses correctly, regardless of shape issues. The actual gap: when Section 8 YAML is structurally absent or unparseable, the early return suppresses Section 10 shape validation. This is an acceptable early-termination behavior, not a fake-pass risk.

- **revised impact:** Low. The early return on Section 8 parse failure is appropriate — if Section 8 cannot be parsed, running Section 10 shape checks provides limited diagnostic value. This is not a correctness issue.
- **revised minimum_closure_condition:** Not a required fix. Owner may note this as a documentation clarification if desired.
- **next_authorized_action:** No action required; note for owner awareness only.
- **patch_queue_entry:** no

---

### F-05 — `validate_section_contract` is not fence-aware; `### N. Title` lines inside fences are counted as section headings (theoretical brittleness)

- **finding_id:** F-05
- **commissioned target:** `.agents/hooks/check_commission_signal_board_output.py` — `validate_section_contract` (lines 164–177)
- **file and anchor:** `validate_section_contract`, line 165: `re.finditer(r"^###\s+(?P<number>\d+)\.\s+(?P<title>.+?)\s*$", text, re.MULTILINE)`
- **implementation evidence:** The section contract scanner runs on the full raw text without stripping YAML or code fences. Any line starting with `### N. ` (where N is one or more digits) anywhere in the document — including inside YAML fences or code blocks — will be counted as a section heading. Testing confirms: if a YAML block contains `### 11. Injected`, the validator sees 11 headings and fails the contract correctly. However, if a YAML block contains a line that exactly matches one of the 10 expected headings with the right number, it would be double-counted and the contract would fail (appearing to have a duplicate). In practice, real CSB board YAML is not expected to contain `### N. Title` lines, and the standard prompt-generated YAML keys are plain-word keys without `###` prefixes.
- **authority / evidence basis:** Repo-visible evidence only. The current fixtures do not trigger this path. The risk is forward-looking: if prompt outputs evolve to include section-reference comments in YAML, or if a board includes a code block showing a prior section example, the section contract would fire on valid content.
- **correctness/validation/runtime/review-confidence impact:** Not a current correctness issue with any known board output. Brittleness risk for edge cases and future output format evolution.
- **minimum_closure_condition:** No closure required unless a real board triggers a false `invalid_section_contract`. If triggered, the fix is to strip code/YAML fences before scanning for headings.
- **next_authorized_action:** Owner awareness; no required action.
- **patch_queue_entry:** no

---

### F-06 — Duplicate row ID plus non-monotonic code creates noisy finding set; second duplicate fires both `duplicate_row_id` AND `non_monotonic_row_id` simultaneously

- **finding_id:** F-06
- **commissioned target:** `.agents/hooks/check_commission_signal_board_output.py` — `parse_signal_rows` (lines 191–263)
- **file and anchor:** `parse_signal_rows`, lines 239–247 (monotonic check before duplicate check)
- **implementation evidence:** For a second appearance of `SBR-003`: (1) `expected_row_id = SBR-NNN` where N = len(rows)+1 (after 3 are already in rows, expects SBR-004); (2) `SBR-003 != SBR-004` fires `non_monotonic_row_id`; (3) `SBR-003 in rows` fires `duplicate_row_id`; (4) `continue` prevents re-adding. Verified by runtime test: `[('non_monotonic_row_id', 'SBR-003'), ('duplicate_row_id', 'SBR-003')]`. The `non_monotonic_row_id` code on the duplicate is technically inaccurate — the row is not "in the wrong position in a monotonic sequence"; it is simply a duplicate. An operator debugging a duplicate would need to understand why `non_monotonic_row_id` fires.
- **authority / evidence basis:** Repo-visible code analysis and runtime verification.
- **correctness/validation/runtime/review-confidence impact:** Low correctness impact (both codes fire; the issue is detected). Operator-facing diagnostic clarity is reduced when a duplicate also triggers `non_monotonic_row_id`.
- **minimum_closure_condition:** Not required. The duplicate is caught. If operator diagnostics warrant improvement, the monotonic check could be skipped when the `row_id in rows` check fires first (check duplicate before monotonic for already-inserted rows).
- **next_authorized_action:** No required action; owner may optionally reorder the checks.
- **patch_queue_entry:** no

---

### F-07 — All three valid fixtures and the test file are missing a final newline (style / hygiene)

- **finding_id:** F-07
- **commissioned target:** `valid_empty_backtest_output.txt`, `valid_source_backed_backtest_output.txt`, `valid_source_backed_forward_output.txt`, `test_commission_signal_board_output_validator.py`
- **file and anchor:** Last byte of each file; visible as `No newline at end of file` in the diff
- **implementation evidence:** All four files in this PR end without a trailing newline (`\n`). Observed: `repr(text[-20:])` = `'ival route map.\n\`\`\`'` — the final character is a backtick, not a newline. The diff shows `\ No newline at end of file` on the last line of each changed file.
- **authority / evidence basis:** POSIX convention; ripgrep and some git diff viewers may show diffs differently for files missing EOF newlines. Does not affect runtime correctness.
- **correctness/validation/runtime/review-confidence impact:** No runtime impact. Style gap only.
- **minimum_closure_condition:** Add a trailing newline to each affected file. Not a required fix.
- **next_authorized_action:** No required action.
- **patch_queue_entry:** no

---

### F-08 — Playbook says "non-`SBR-001` row IDs" but means "non-`SBR-NNN` format" (description precision gap)

- **finding_id:** F-08
- **commissioned target:** `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`, "What The Validator Checks" section
- **file and anchor:** Playbook, line "non-`SBR-001` row IDs" in the What The Validator Checks list
- **implementation evidence:** The playbook text says the validator fails "non-`SBR-001` row IDs." The implemented error code is `invalid_row_id_format` with message "Row ID must use SBR-001 format." The validator uses `ROW_ID_RE = re.compile(r"^SBR-(\d{3})$")` — it requires `SBR-` followed by exactly 3 digits. `SBR-001` in the playbook is an example, not the only valid value. A reader seeing "non-SBR-001 row IDs" could misread this as the validator only accepts `SBR-001` specifically, rather than the `SBR-NNN` (three-digit zero-padded) pattern.
- **authority / evidence basis:** Playbook text vs. implementation evidence (`ROW_ID_RE`).
- **correctness/validation/runtime/review-confidence impact:** Documentation clarity gap. The validator implementation is correct. A prompt author may misunderstand valid row IDs from the playbook description.
- **minimum_closure_condition:** The playbook phrase should read "non-`SBR-NNN` format row IDs" or "row IDs not matching the `SBR-\d{3}` pattern" to match the implementation.
- **next_authorized_action:** No required action; documentation improvement.
- **patch_queue_entry:** no

---

### F-09 — Playbook "Validator Applicability" section describes a two-section gate (S4+S8) but the validator now requires all 10 sections (coverage mismatch)

- **finding_id:** F-09
- **commissioned target:** `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`, "Validator Applicability" section
- **file and anchor:** Playbook, "Validator Applicability" section (lines 85–93)
- **implementation evidence:** The playbook "Validator Applicability" section says:
  > Run the validator only when the saved output contains both:
  > - `### 4. Signal Board Rows`
  > - `### 8. Demand-Classifier Handoff Packet`
  > Do not run it against intake-only output. A `NEEDS_COMMISSION_INTAKE` or `NEEDS_CUTOFF_DATE` response is expected to fail with missing Section 4 and Section 8, because it is not a board.

  This guidance is accurate but incomplete after Batch 1: the validator now checks all 10 sections, not just 4 and 8. A partial board with S4+S8 but missing S1, S2, S3 etc. will now also fail with `invalid_section_contract`. The Applicability guidance still describes the pre-Batch-1 gate. "What The Validator Checks" was correctly updated, but "Validator Applicability" was not.

- **authority / evidence basis:** Playbook diff shows "What The Validator Checks" was updated but "Validator Applicability" text is unchanged.
- **correctness/validation/runtime/review-confidence impact:** An operator following the playbook's Applicability guidance may run the validator against a board that has S4+S8 but missing other sections, expecting only S4/S8 failures, and will be surprised by `invalid_section_contract`. Documentation gap, not a correctness issue in the validator itself.
- **minimum_closure_condition:** The "Validator Applicability" section should be updated to say the validator requires the output to contain all 10 sections in the prompt-defined order, not just S4 and S8.
- **next_authorized_action:** Documentation improvement; no required action.
- **patch_queue_entry:** no

---

### F-10 — `test_full_board_requires_sections_one_through_ten_in_order` is brittle (exact-string fixture dependency)

- **finding_id:** F-10
- **commissioned target:** `orca-harness/tests/unit/test_commission_signal_board_output_validator.py`, line 96
- **file and anchor:** `test_full_board_requires_sections_one_through_ten_in_order`, line 96
- **implementation evidence:**
  ```python
  text = text.replace("### 9. Visible Limitations\n\nThis fixture proves only mechanical eligibility under declared row fields.\n\n", "", 1)
  ```
  This replacement requires exact match of the Section 9 header plus its body text plus a trailing double-newline. If the fixture's Section 9 body text is changed in any future update (e.g., a whitespace edit, or the fixture body is changed to say something different), the `str.replace()` will silently find 0 replacements, the text will be unchanged, and the test will pass trivially (the section is present, no finding fires) while asserting `invalid_section_contract` — the test would then FAIL at the assert. The replacement count is not checked.
- **authority / evidence basis:** Code inspection and runtime verification (text != removed confirmed the replacement does occur with current fixture content, so this is a future brittleness risk, not a current failure).
- **correctness/validation/runtime/review-confidence impact:** Test currently passes. Brittleness risk for future fixture maintenance. A safe replacement would use a regex that matches `### 9. Visible Limitations` and the following non-heading content up to the next `###` heading.
- **minimum_closure_condition:** Not a required fix for Batch 1. Can be addressed as a test hygiene improvement.
- **next_authorized_action:** No required action; owner awareness.
- **patch_queue_entry:** no

---

### F-11 — `mode: unknown` is in `VALID_HANDOFF_MODES` but has no documentation of its intended semantics or enforcement contract

- **finding_id:** F-11
- **commissioned target:** `.agents/hooks/check_commission_signal_board_output.py`, constant `VALID_HANDOFF_MODES` (line 60)
- **file and anchor:** Line 60: `VALID_HANDOFF_MODES = {"backtest", "forward", "unknown"}`
- **implementation evidence:** The constant includes `unknown` without a comment explaining when it is valid or what enforcement applies. `_validate_handoff_row` silently skips all cutoff checks for `unknown` mode. No fixture exercises `unknown` mode. No test verifies `unknown` mode behavior. The playbook mentions "mode" as a required field but does not mention `unknown` as a valid value.
- **authority / evidence basis:** Code inspection; no overlay or playbook authority governing `unknown` mode semantics was found in the read sources.
- **correctness/validation/runtime/review-confidence impact:** Combined with F-01, this is the documentation side of the same concern. The lack of an explicit semantics statement means any operator (or future code author) who sees `unknown` as a valid mode will not know whether cutoff checks are intentionally bypassed or accidentally omitted.
- **minimum_closure_condition:** The `unknown` mode handling must be documented with a comment in the checker source and/or a note in the playbook. The comment must state whether cutoff bypass is intentional and under what circumstances `mode: unknown` is a valid emission from the CSB prompt.
- **next_authorized_action:** Owner decision on `unknown` mode intent; review finding only.
- **patch_queue_entry:** no

---

## Strict-Only Blockers and Not-Proven Boundaries

The following cannot be determined from repo-visible evidence alone:

- **not proven:** Whether `mode: unknown` was intentionally designed as a cutoff bypass or is an accidental omission. The code supports `unknown` but provides no semantic documentation.
- **not proven:** The intended relationship between the `imaginary_authors_csb_broad_scout_deep_scan_handoff_prompt_v0.md` context file (not found at the named path) and the validator's constraints. No authority gap from this missing file was found in the primary review targets.
- **not proven:** Whether the CSB prompt itself can emit `mode: unknown` outputs, or whether `unknown` is a legacy/placeholder value that has no real prompt-side source. This would require reading the prompt file (not in scope for this review).
- **strict-only blocker:** No formal PR verdict, severity authority, readiness claim, approval, or mandatory remediation authority is held by this review. These are findings-only under advisory mode.

---

## Open Questions

1. When does the CSB prompt emit `mode: unknown`? Is there a valid prompt scenario, or is `unknown` a placeholder that should be removed?
2. Should the negative fixtures be upgraded to full Section 1-10 boards to isolate single failure modes, or is the multi-code failure set an acceptable operator-debugging posture?
3. Should `selftest` coverage be expanded to cover at least one fixture per new check category, given that selftest is the operator-facing gate described in the playbook?
4. The playbook "Validator Applicability" section describes a two-section gate (S4+S8). Is this intentionally left in its pre-Batch-1 form, or should it be updated to say "all 10 sections required"?

---

## Residual Risk

After the tests pass and selftest reports OK:

- **Unknown-mode cutoff bypass (F-01/F-11):** Unresolved until the `unknown` mode semantics decision is made. An operator or a prompt-generated board with `mode: unknown` will silently bypass all cutoff enforcement. This is the only material fake-pass vector remaining after Batch 1.
- **Selftest coverage (F-03):** If a future edit breaks one of the 19 new codes, selftest will not catch it. The pytest suite will catch it only if run.
- **Negative fixture noise (F-02):** An operator debugging a bad fixture using selftest will see 3+ codes where 1 is expected. Low operational risk; medium diagnostic clarity risk.
- **Playbook description (F-09):** An operator following the "Validator Applicability" section may apply the validator to a board missing sections 2, 3, 5, 6, 7, or 9 and receive unexpected `invalid_section_contract` codes. Documentation risk only.

---

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, readiness, formal verdict, mandatory remediation, or executor-ready patch authority. No finding in this report creates a blocked state, a required action, or a lifecycle claim. Each finding states a `next_authorized_action` of "owner decision" or "no action required." Owner adjudicates all findings independently.

---

## Provenance

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: operator_to_fill_or_unrecorded
de_correlation_bar: same_vendor_sanity
same_vendor_rationale: >
  This is a bounded implementation review of a new structural checker, not a
  full doctrine-surface or seam-discovery pass. The review verifies that the
  new checks do what they say and identifies gaps; it does not claim the
  no-new-seam discovery bar. A cross-vendor pass is not required for this
  advisory code review.
```

---

CODE_REVIEW_RETURN_FOR_HOME_MODEL

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Commission: adversarial code review of PR #360 (CSB Validator Batch 1 structure
checks). Read-only; no patch queue; no approval or readiness claim.

Review target: check_commission_signal_board_output.py, test file, three valid
fixtures, seven negative fixtures (inspected via selftest output and two targeted
reads), CSB playbook.

Implementation context: PR adds validate_section_contract (Sections 1-10 in
order), expanded vocab enforcement for 8 Section 4 fields, Section 8 packet
shape validation (required fields, classifier_owned, prohibited_claims shape),
Section 10 board status and run boundary parsing, and accompanying tests and
fixture expansions.

Validation evidence: selftest SELFTEST OK (10/10 fixtures pass/fail correctly);
pytest 18/18 passed; git diff --check shows no whitespace errors.

Key findings (materiality-ordered):

F-01 [MATERIAL]: mode=unknown bypasses all cutoff enforcement. VALID_HANDOFF_MODES
includes 'unknown'; _validate_handoff_row only applies cutoff checks inside
'if mode == "backtest"'. A board with mode=unknown and uncertain/post-cutoff
rows in the handoff packet passes the validator. Verified by runtime test.
No documentation of unknown mode semantics or intent. Owner decision required.

F-02 [MODERATE]: Existing 7 negative fixtures are partial boards (sections 1,4,8
only). Under Batch 1, they also fire invalid_section_contract and
missing_board_status_section. Tests still pass (containment checks). Selftest
shows noisy multi-code failures. Fixture pedagogical value degraded.

F-03 [MODERATE]: Selftest covers 0 of 19 new Batch 1 error codes. New codes
are exercised only by pytest mutation tests. Selftest is the playbook-described
operator gate; regression risk if a new code breaks in a future edit.

F-04 [RESOLVED AS LOW]: Early return behavior (packet parse failure suppresses
_validate_board_status_shape) is correct and expected. The shape findings
(_validate_packet_shape) are NOT gated by the early return; only YAML structure
parse failures trigger it. No fake-pass risk.

F-05 [LOW]: Section contract scanner is not fence-aware; ### N. Title lines inside
YAML fences would be counted. Not a current correctness issue; theoretical
brittleness for future output format evolution.

F-06 [LOW]: Duplicate row ID also fires non_monotonic_row_id; slightly noisy for
operators, not a correctness gap.

F-07 [STYLE]: Three valid fixtures and test file missing final newline. No
runtime impact.

F-08 [DOCUMENTATION]: Playbook says "non-SBR-001 row IDs" when it means
non-SBR-NNN format. Precision gap only.

F-09 [DOCUMENTATION]: Playbook "Validator Applicability" still describes the
pre-Batch-1 two-section gate (S4+S8); not updated to reflect the new all-10
sections requirement.

F-10 [TEST HYGIENE]: test_full_board_requires_sections_one_through_ten_in_order
uses exact string replacement with no count check; brittle if fixture body changes.

F-11 [DOCUMENTATION, companion to F-01]: mode=unknown has no documented semantics
in source or playbook. No comment explaining whether cutoff bypass is intentional.

Residual risk: F-01/F-11 (unknown mode cutoff bypass) is the only material
unresolved fake-pass vector. All other findings are documentation, diagnostic
clarity, or test hygiene.

Non-claims: not approval; not readiness; not a formal verdict; not mandatory
remediation; not a patch queue. Owner adjudicates all findings.
```
