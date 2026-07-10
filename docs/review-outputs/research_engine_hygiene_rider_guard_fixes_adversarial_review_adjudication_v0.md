# Research-Engine Hygiene-Rider Guard Fixes — Review Adjudication + Patch Record v0

```yaml
retrieval_header_version: 1
artifact_role: Review adjudication record (delegated adversarial code review findings, home-model adjudication, patch pointer)
scope: >
  Adjudicates the 2026-07-10 delegated adversarial code review of the
  hygiene-rider guard fixes (commit e16b5e39) and records the bounded patch
  applied in response. Findings-only input; this record adds verdicts and the
  patch/verification receipt.
use_when:
  - Checking whether the hygiene-rider review findings were adjudicated and patched.
  - Auditing the FIND-01/02/03 fix and its verification evidence.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/research_engine_hygiene_rider_guard_fixes_delegated_adversarial_code_review_prompt_v0.md
stale_if:
  - A later review pass supersedes these verdicts.
  - The patched hooks are materially rewritten.
```

- Review input: delegated adversarial code review of `e16b5e39` (read-only,
  findings-first), returned 2026-07-10. Review prompt:
  `docs/prompts/reviews/research_engine_hygiene_rider_guard_fixes_delegated_adversarial_code_review_prompt_v0.md`.
- Adjudicator: home model, this lane (`claude/research-engine-strategy-3a7619`).
- Each finding was re-verified against source before patching.

## Verdicts

| Finding | Verdict | Adjudication note |
| --- | --- | --- |
| FIND-01 — HOOK-1 mishandles POSIX/rooted absolute paths (`_to_posix` pre-mangle in `analyze_paths`; out-of-repo rooted path could collide with an in-repo relative path) | **CONFIRMED** | Verified in source: `analyze_paths` normalized with `_to_posix()` (lstrip of `/` and `.`) before `_relativize()` could see the raw path; the original selftest bypassed the production entry. |
| FIND-02 — HOOK-8 diff parser drops added lines beginning `++` (rendered `+++...` inside a hunk, misread as file header; line numbers desync) | **CONFIRMED** | Verified by inspection; same defect class existed in BOTH parsers (`added_lines_by_file` for `--changed`/CI and `_added_lines_vs_head` for `--hook`). |
| FIND-03 — HOOK-8 "always exit 0" contract false for valid non-object JSON (`[]`, `{"tool_input":"bad"}` → AttributeError → exit 1) | **CONFIRMED** (retained pre-existing defect, not introduced by `e16b5e39`) | Verified: no type guards, no fail-open wrapper at the `--hook` entry. |

## Patch Applied (this lane)

- **FIND-01** (`check_search_surface_google_route.py`): `analyze_paths` now
  relativizes raw paths FIRST (dedupe on the relativized result);
  `_relativize` handles absolute AND rooted (`anchor`) paths and returns `""`
  (never in scope) for paths resolving outside the repo instead of a stripped
  relative-looking string. Selftest extended: in-repo absolute, Windows-drive
  out-of-repo, POSIX-rooted out-of-repo, UNC out-of-repo, backslash payload,
  and a production-path `analyze_paths` case.
- **FIND-02** (`check_full_gt_claims.py`): extracted one pure structural
  parser `_parse_added_lines_by_file` (headers recognized only OUTSIDE a hunk)
  used by both the CI/`--changed` path and the `--hook` path. Red-green
  selftest fixture: an added `++ Bronze is full God Tier.` line followed by a
  second finding line, asserting content retention and line numbering.
- **FIND-03** (`check_full_gt_claims.py`): both payload layers type-checked
  (`payload` dict, `tool_input` dict, `file_path` str); `--hook` entry wrapped
  in a fail-open try/except (prints to stderr, exits 0). Selftest feeds
  `[]`, `{"tool_input": "bad"}`, `{"tool_input": {"file_path": 5}}`, and
  non-JSON through the real `run_hook()` and asserts exit 0.

## Verification (observed 2026-07-10)

- `check_full_gt_claims --selftest`: OK (18 cases). `check_search_surface_google_route --selftest`: OK.
- FIND-02 e2e: appended `++ Bronze is full God Tier.` to a tracked in-scope
  doc; `--hook` emitted the `additionalContext` finding at the correct line
  (`...god_tier_target_v0.md:193`); file restored.
- FIND-03 e2e: `[]` and `{"tool_input": "bad"}` → exit 0, silent.
- FIND-01 e2e: rooted out-of-repo payload → exit 0, silent.
- Focused unit suites (`test_csb_scanning_artifact_validator.py`,
  `test_hook_internal_error_gating.py`): 130 passed.

## Reviewer Residual (accepted)

Future rewrites of a grandfathered legacy scan artifact retaining the exempt
filename remain auto-skip by design (exact-path grandfather). Accepted:
explicit-path validation stays strict, and a rewrite that modernizes the
artifact should also remove it from `PRE_CONTRACT_LEGACY_ARTIFACTS`.

## Non-Claims

Records adjudication and a verified patch only. Not validation beyond the named
checks, not readiness, not approval to merge, and not a claim that the hooks
are defect-free.
