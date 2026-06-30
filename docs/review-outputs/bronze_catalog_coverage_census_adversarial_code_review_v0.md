# Bronze Catalog Coverage Census Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated cross-vendor adversarial implementation/code review of PR #505's
  Bronze Catalog coverage census slice (the `--census` read-only coverage view
  over generated Bronze Catalog state).
use_when:
  - Adjudicating the PR #505 census slice before merge.
  - Checking the closure status of CENSUS-01..CENSUS-06.
authority_boundary: retrieval_only
reviewed_by: claude-opus-4.8
authored_by: openai-gpt-5-codex
de_correlation_bar: cross_vendor_discovery
target_pr: 505
target_base: 64e7333b5e6743c68bf76440e6a2eace4fc6fc7d
target_head: 2ecff496ce6fce0916f5680e3107102a66e034d6
```

## Source Context

`SOURCE_CONTEXT_READY`.

- **Target-file drift:** none. Branch HEAD is `842ddbe` (`Add Bronze census review
  prompt`), one prompt-only commit after the implementation commit
  `2ecff496`. That commit adds only
  `docs/prompts/reviews/bronze_catalog_coverage_census_adversarial_code_review_prompt_v0.md`;
  none of the four named target files changed
  (`git diff --name-status 2ecff496..842ddbe -- <targets>` returned empty).
- **Hash pins:** all four target-file SHA256 pins match the author-recorded
  values at `2ecff496` (recomputed on the Windows worktree). Reviewing the
  targets at HEAD is therefore byte-equivalent to reviewing at `2ecff496`.
- **De-correlation:** controller is Anthropic / Claude (Opus 4.8); author is
  OpenAI / GPT-family Codex. Different upstream vendor → `cross_vendor_discovery`
  bar is met. `reviewed_by` recorded as my real identity (factual, not
  fabricated); the operator/CA owns the durable provenance field and may confirm
  or normalize it.
- **Skills:** `workflow-deep-thinking` and `workflow-code-review` reference-loaded
  from the prompt's zero-config semantics; this is an advisory, findings-first
  implementation review. No strict review claim is made.
- **Conflicts / unavailable sources:** none blocking. Diff-scoped `--strict` CI
  hooks were not rerun (see Validation Run Ledger for why).

### Source-Read Ledger

Authority / boundary (read at HEAD; unchanged since `2ecff496`):

- `AGENTS.md` (in-session)
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` (adjacent context; grounds the AR-physicalization non-claim)

Target (read in full at HEAD):

- `orca-harness/data_lake/catalog.py`
- `orca-harness/runners/run_data_lake_catalog.py`
- `orca-harness/tests/test_data_lake_catalog.py`
- `docs/workflows/orca_repo_map_v0.md` (diff)
- `orca-harness/data_lake/root.py` (adjacent; confirms read-only / write-boundary behavior of `_within`, `inspect_catalog`'s call graph, and exit-path handling)

Not read (out of scope / not load-bearing for findings): `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/prompt-orchestration.md` (prompt-authoring process, not code-review substance — their findings-first / output-mode boundary is already carried by `review-lanes.md`); `source_capture/fragrance_review_lake.py` and the two sibling review prompts (not needed to adjudicate this slice).

## Validation Run Ledger

Independently rerun by this reviewer (cwd `orca-harness/` unless noted):

| Command | Result | Bucket |
| --- | --- | --- |
| `python -m py_compile data_lake/catalog.py runners/run_data_lake_catalog.py` | exit 0 | GATE PASS |
| `python -m pytest -q tests/test_data_lake_catalog.py` | `18 passed, 1 skipped` (skip = directory-symlink test, platform) | GATE PASS |
| `git diff --check 64e7333b..2ecff496` | exit 0 | GATE PASS |
| `python .agents/hooks/check_retrieval_header.py docs/workflows/orca_repo_map_v0.md` | exit 0 | GATE PASS |
| `python .agents/hooks/check_repo_map_freshness.py docs/workflows/orca_repo_map_v0.md` | exit 0 | GATE PASS |

Author-supplied, **not** independently revalidated:

- `python .agents/hooks/header_index.py --strict` and
  `python .agents/hooks/check_map_links.py --strict` — these gates diff-scope
  against `origin/main`, but PR #505's base is `codex/bronze-v41-clean-verify`,
  so a local rerun would mis-scope to the whole branch-from-main delta rather
  than this slice. Reported as author-supplied (author observed exit 0).
- `python orca-harness/runners/run_data_lake_catalog.py --census --root F:\work\orca-lake` — live real-lake census; out of scope under the prompt's no-live-lake boundary. The author-observed result (`status=issues_found`, `expected_packet_count=99`, `attachment_record_count=216`, `source_family_count=6`, `source_surface_count=7`, stale/missing generated-file samples) is consistent with the code path I traced, but I did not run it.
- `gh pr checks 505 --watch` — author observed `orca-harness-tests` passing; not rerun.

## Findings

**No blocker and no major finding.** The slice is correctly read-only, the
exit-code contract is right, the counting is deterministic, and the focused
test suite passes on an independent rerun. The findings below are all `minor`
(prioritization label only, not an Orca verdict): four are regression-coverage
gaps and one is a count-honesty / self-description gap. The strongest in
*latent stakes* is F-03, because the invariant its missing test would protect
is the read-only guarantee itself.

---

### F-01 — `minor` — Issue-sample bounding (`[:25]` truncation) is asserted but never exercised

- **Target:** `orca-harness/data_lake/catalog.py:362-366` (the
  `report[field][:_COVERAGE_CENSUS_ISSUE_SAMPLE_LIMIT]` slice in
  `_coverage_census_issue_summary`); test `orca-harness/tests/test_data_lake_catalog.py:653-654`.
- **Evidence:** The census's flood-protection guarantee is the `[:25]` slice. The
  only test coverage is `assert ...["issue_sample_limit"] == 25` (the constant)
  and `assert "missing_files" in ...["issue_samples"]` (presence). No test ever
  produces more than 25 issues of any kind, so the truncation behavior is never
  observed. A regression that dropped the slice (or widened the limit) would
  leave every assertion green while the census re-gained the ability to flood
  operator output on a large real lake.
- **Authority / basis:** Review Scope — "Are issue samples bounded and
  deterministic so a large lake cannot flood operator output…"; CENSUS-02.
- **Impact:** The headline operator-safety property of `--census` (bounded
  output on a large/broken lake) is unverified by the suite.
- **Minimum closure condition:** A test that drives at least one issue field
  above the limit and asserts both `issue_counts[field] > 25` and
  `len(issue_samples[field]) == 25`.
- **Next authorized action:** Owner decision to add the regression test
  (no source change to the census itself is required).
- **Validation expectation:** New test passes; `issue_counts` still reports the
  true (un-truncated) total alongside the capped sample.

---

### F-02 — `minor` — Census-mode tests cover only `missing` and `ok`; the stale/orphaned/read-failure issue-summary path is untested

- **Target:** `orca-harness/data_lake/catalog.py:351-372`
  (`_coverage_census_issue_summary`, the `issue_fields` tuple);
  tests `test_catalog_coverage_census_is_observed_only_and_read_only`
  (`:637-682`) and `test_catalog_runner_emits_read_only_coverage_census`
  (`:746-772`).
- **Evidence:** Both census tests exercise exactly two catalog states: nothing
  generated (`missing_files`, `indexed_packet_count == 0`) and a freshly rebuilt
  `ok` catalog. `inspect_catalog` has dedicated tests for `stale_packets`,
  `stale_files`, `orphaned_files`, and `catalog_read_failures`
  (`:403-446`, `:534-598`), and the census delegates to it, so the *status*
  signal is mechanically sound. But the census-specific mapping from those
  fields into `issue_counts` / `issue_samples` is never asserted for any
  non-missing failure mode. A regression that dropped a field from the
  `issue_fields` tuple (e.g. `stale_files` or `catalog_read_failures`) would be
  invisible to the census suite.
- **Authority / basis:** Review Scope — read-only behavior "when generated
  catalog files are stale, missing, orphaned, unreadable, or internally
  inconsistent"; CENSUS-02.
- **Impact:** Census fidelity for stale/orphaned/read-failure (the
  non-missing failure modes an operator most needs distinguished from "missing")
  is unverified at the census layer.
- **Minimum closure condition:** A census test that rebuilds, then mutates one
  generated file to be stale (and/or plants an orphan / forces a read failure)
  and asserts the corresponding `catalog_issue_summary.issue_counts.*` is
  nonzero while `status == "issues_found"`.
- **Next authorized action:** Owner decision to extend census test coverage.
- **Validation expectation:** New test passes; census continues to return
  `issues_found` and a bounded sample for the mutated field.

---

### F-03 — `minor` — `--census` / `--rebuild` mutual exclusion is correct but untested, and the guard protects the read-only invariant

- **Target:** `orca-harness/runners/run_data_lake_catalog.py:31-41`.
- **Evidence:** The guard `if args.rebuild and args.census: parser.error(...)`
  (line 31-32) runs before the dispatch. The dispatch checks `if args.rebuild:`
  **first** (line 36), so if the guard were ever removed, `--census --rebuild`
  would silently fall through to `rebuild_catalog` — a lake **write** — which is
  the single outcome a read-only census must never produce. The guard is present
  and correct today, but no test asserts it: the runner suite covers
  `--rebuild` alone, `--census` alone, and no-flag, never the conflicting
  combination.
- **Authority / basis:** CENSUS-05 ("clear `--rebuild` / `--census` mutual
  exclusion"); CENSUS-01 read-only invariant; `safety-rules.md` (lake writes are
  gated, never a side effect of an inspect path).
- **Impact:** Low today (guard correct), but the missing regression test guards
  an asymmetric failure: a future edit that removes/reorders the guard fails
  *toward* a write, not toward an error.
- **Minimum closure condition:** A test asserting
  `main(["--data-root", ..., "--census", "--rebuild"])` exits nonzero (argparse
  `error()` → exit 2) and that no catalog root is written.
- **Next authorized action:** Owner decision to add the regression test.
- **Validation expectation:** New test passes; combined-flag invocation never
  reaches `rebuild_catalog`.

---

### F-04 — `minor` — `source_family_count` silently includes the null/unknown family bucket

- **Target:** `orca-harness/data_lake/catalog.py:247` (`"source_family_count":
  len(source_families)`) with `_coverage_census_source_families` (`:321-348`),
  which keys a bucket on `None` for packets carrying no non-blank
  `source_family`.
- **Evidence:** Packets with a missing/blank `source_family` are normalized to
  `None` (`_string_or_none`) and grouped into a real `None`-keyed bucket. That
  bucket is counted in the headline scalar `source_family_count`. So a lake with
  N named families plus any family-less packets reports `source_family_count =
  N+1`. The `field_semantics` entry for the `source_families` *list* documents
  the null inclusion (`:94-97`), but the headline scalar has no `field_semantics`
  entry and reads naturally as "families covered."
- **Authority / basis:** CENSUS-03 (counts "line up… and remain useful");
  AGENTS.md "preserve real failure visibility / never overstate." This is a
  mild over-count, not a correctness break — `source-of-truth.md` keeps raw
  authoritative and the null bucket is itself a real observed fact.
- **Impact:** A coverage headline can over-report the number of source families
  by one whenever any packet lacks a `source_family`. (The author-observed live
  run reported `source_family_count=6`; whether one of those six is the null
  bucket is not determinable from the census output alone.)
- **Minimum closure condition:** Either exclude the `None` bucket from
  `source_family_count` (and expose it separately, e.g.
  `unknown_source_family_packet_count`), or add a `field_semantics` entry stating
  that `source_family_count` includes the null/unknown bucket.
- **Next authorized action:** Owner decision on which disambiguation to take
  (count-change vs. semantics note); both are in-scope for the census file.
- **Validation expectation:** A census test with a blank-family packet asserts
  the chosen behavior (count excludes null, or semantics documents inclusion).

---

### F-05 — `minor` — Headline count fields carry no per-field semantics, and there is no indexed/generated AR count to mirror `indexed_packet_count`

- **Target:** `orca-harness/data_lake/catalog.py:87-103`
  (`_COVERAGE_CENSUS_FIELD_SEMANTICS` documents only `catalog_status`,
  `source_families`, `source_surfaces`) vs. the ~20-field census return
  (`:233-258`), including `expected_packet_count`, `indexed_packet_count`,
  `attachment_record_count`, `source_family_count`, `source_surface_count`.
- **Evidence:** The load-bearing honesty distinction — that the headline counts
  and per-surface/per-family counts are **raw-derived (expected)** coverage, not
  generated-catalog currentness — lives only in the prose `semantics` string
  ("not generated-catalog currentness unless catalog_status is ok") and the
  `catalog_status` note. The count fields themselves are undocumented. Two
  consequences:
  (a) When `catalog_status == issues_found`, `attachment_record_count` and the
  per-row counts report raw truth while `stable_query_paths` /
  `catalog_query_paths` (`:251-256`, `:314-317`) point at generated files that
  may be missing or stale — an operator scripting against a count then opening
  the advertised path can find a mismatch. The mitigations (status field,
  `catalog_issue_summary`, the asserted `semantics` string, and
  `indexed_packet_count` exposing the packet-level gap) make this defensible, not
  airtight.
  (b) The gap signal is asymmetric: packets expose both `expected_packet_count`
  and `indexed_packet_count`, but Attachment Records expose only the
  raw-derived `attachment_record_count` — there is no `indexed_attachment_record_count`.
  AR currentness must be inferred from `catalog_status` / `issue_samples`, not
  read as a clean expected-vs-indexed delta.
- **Authority / basis:** CENSUS-03; `source-of-truth.md` ("the catalog… is never
  authority; raw… remains the source of truth"); the AR implementation contract
  (the count must not imply final AR physicalization — which the census's
  `authority`/`coverage_basis` fields correctly avoid).
- **Impact:** Self-description is thinner than the rest of the catalog module
  (`source_surfaces.json` documents most of its fields). A reader who keys
  automation off the headline counts without reading the prose `semantics` could
  conflate raw-expected coverage with generated-catalog currentness.
- **Minimum closure condition:** Add `field_semantics` entries for the count
  fields stating they are raw-derived (expected) totals, and either add an
  `indexed_attachment_record_count` or a note that AR currentness is read from
  `catalog_status` / `catalog_issue_summary`, not a count delta.
- **Next authorized action:** Owner decision (documentation-only vs. add the
  indexed-AR count); both are in-scope for the census file.
- **Validation expectation:** Census output carries the added semantics; any new
  count field is covered by an assertion in the census tests.

## Residual Risks (no blocker/major found)

- **Corrupt-raw-packet path:** if a *raw* packet is unreadable/hash-mismatched,
  `catalog_coverage_census` → `inspect_catalog` → `_build_entries` →
  `load_raw_packet` raises `DataLakeRootError`, which the runner converts to
  `status=error`, exit 2 (verified by the existing corrupt-raw test at
  `:700-721`, which is on the rebuild path; the census shares the same
  `_build_entries` front half). This is read-only and fail-loud — correct — but
  means `--census` is not a "always returns a census" command: a corrupt *raw*
  packet yields an error rather than a partial coverage view. Acceptable and
  arguably desired (fail-closed), but worth the operator knowing.
- **Generated-catalog corruption is handled gracefully** (read failures →
  `catalog_read_failures`, no raise); only raw-side corruption escalates to
  `error`. The asymmetry is correct given raw is authoritative.
- **Repo-map wording is in scope and clean:** the two edited rows add the census
  as "inspect-only / read-only observed… coverage census" with explicit
  non-claims ("not… a capture-lane registry, Silver readiness, or final
  Attachment Record physicalization"). No "god tier", completeness, validation,
  authority, source-of-truth, or live-lake-mutation leakage. No finding.

## Closure Check (CENSUS-01..CENSUS-06)

- **CENSUS-01 — read-only real-lake visibility — `closed`.** Verified by code:
  `catalog_coverage_census` calls only `inspect_catalog`; neither writes, and
  `DataLakeRoot._within` resolves paths without `mkdir` (root.py:493-506), so the
  census never materializes the catalog root. Two tests assert catalog-root
  absence and byte-identical snapshot equality across a census call; pytest
  reran green.
- **CENSUS-02 — honest stale-index signal — `partially_closed`.** Status and
  issue-summary plumbing are sound and the `missing` state is tested in census
  mode, but the sample-bounding truncation (F-01) and the
  stale/orphaned/read-failure census issue-summary (F-02) are untested. Material
  variant: a large or stale real lake's census output fidelity is unverified at
  the census layer. **Minimum closure:** add F-01 and F-02 tests.
- **CENSUS-03 — coverage accounting — `partially_closed`.** Counts line up with
  generated-catalog semantics and the ok/missing cases are tested. Residual:
  `source_family_count` includes the null bucket (F-04) and the count fields lack
  per-field semantics with no indexed-AR mirror (F-05). Material variant:
  headline counts can over-state family coverage by one and can be conflated with
  generated-catalog currentness when `catalog_status == issues_found`.
  **Minimum closure:** F-04 disambiguation + F-05 semantics.
- **CENSUS-04 — future-lane adaptability — `closed`.** The census derives
  families and surfaces purely from observed manifests; `_EXTRACTORS` only
  enriches facets and never gates census structure, so unknown/new families
  appear with no lake-core schema change — consistent with the AR contract's
  Required-Shape #6. Unknown-future-surface handling is tested at the
  rebuild/inspect layer (`:236-270`) that the census passes through. Residual
  (not closure-blocking): no census-mode test names a genuinely unknown future
  family, but the mechanism is shared and covered upstream.
- **CENSUS-05 — CLI/operator ergonomics — `partially_closed`.** Exit contract is
  correct (`0` ok / `1` issues_found / `2` resolution-error or flag-misuse) and
  default inspect/rebuild behavior is preserved and tested; the
  `--census`/`--rebuild` mutual-exclusion guard is present and correct but
  untested (F-03). **Minimum closure:** add the F-03 mutual-exclusion test.
- **CENSUS-06 — regression coverage — `partially_closed`.** Read-only, happy,
  missing, and CLI-exit paths are covered; gaps are F-01 (bounding), F-02
  (stale/orphaned census), F-03 (mutual exclusion), and F-04 (null-family
  census). **Minimum closure:** the four tests above.

## Strict-Claim Boundary (not claimed)

This is advisory, findings-first implementation/code review under the zero-config
`workflow-code-review` semantics. It does **not** assert: formal verdict,
PASS/FAIL, readiness, approval, validation pass/fail authority, severity
authority (the `minor` labels are prioritization only), `patch_queue_entry`, a
proposed patch or diff, or any runtime-model recommendation. No source file was
edited, committed, pushed, merged, or run against a live lake under this review.
Review findings are decision input only until the home model (CA) adjudicates.

## Courier Block

```yaml
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL:
  source_context: SOURCE_CONTEXT_READY
  reviewed_by: claude-opus-4.8
  authored_by: openai-gpt-5-codex
  de_correlation_bar: cross_vendor_discovery
  same_vendor_rationale: not_applicable_cross_vendor
  target_pr: 505
  target_base: 64e7333b5e6743c68bf76440e6a2eace4fc6fc7d
  target_head: 2ecff496ce6fce0916f5680e3107102a66e034d6
  reviewed_files:
    - docs/workflows/orca_repo_map_v0.md
    - orca-harness/data_lake/catalog.py
    - orca-harness/runners/run_data_lake_catalog.py
    - orca-harness/tests/test_data_lake_catalog.py
  report_path: docs/review-outputs/bronze_catalog_coverage_census_adversarial_code_review_v0.md
  findings:
    - {id: F-01, severity: minor, summary: "issue-sample [:25] bounding asserted via constant only, truncation never exercised"}
    - {id: F-02, severity: minor, summary: "census tests cover missing+ok only; stale/orphaned/read-failure issue-summary path untested"}
    - {id: F-03, severity: minor, summary: "--census/--rebuild mutual-exclusion guard correct but untested; removal would fail toward a lake write"}
    - {id: F-04, severity: minor, summary: "source_family_count includes the null/unknown family bucket"}
    - {id: F-05, severity: minor, summary: "count fields lack per-field semantics; no indexed/generated AR count mirrors indexed_packet_count"}
  closure_check:
    CENSUS-01: closed
    CENSUS-02: partially_closed
    CENSUS-03: partially_closed
    CENSUS-04: closed
    CENSUS-05: partially_closed
    CENSUS-06: partially_closed
  proposed_patch_present: no
  needs_architecture_pass: no
  validation_run:
    - {cmd: "py_compile catalog.py run_data_lake_catalog.py", result: "exit 0", rerun: independent}
    - {cmd: "pytest -q tests/test_data_lake_catalog.py", result: "18 passed, 1 skipped", rerun: independent}
    - {cmd: "git diff --check 64e7333b..2ecff496", result: "exit 0", rerun: independent}
    - {cmd: "check_retrieval_header.py orca_repo_map_v0.md", result: "exit 0", rerun: independent}
    - {cmd: "check_repo_map_freshness.py orca_repo_map_v0.md", result: "exit 0", rerun: independent}
    - {cmd: "header_index.py --strict", result: "author exit 0", rerun: not_independent_mis_scopes_vs_origin_main}
    - {cmd: "check_map_links.py --strict", result: "author exit 0", rerun: not_independent_mis_scopes_vs_origin_main}
    - {cmd: "run_data_lake_catalog.py --census --root F:\\work\\orca-lake", result: "author status=issues_found expected_packet_count=99 attachment_record_count=216 source_family_count=6 source_surface_count=7", rerun: not_independent_live_lake_out_of_scope}
    - {cmd: "gh pr checks 505 --watch", result: "author orca-harness-tests passing", rerun: not_independent}
  not_claimed:
    - formal_verdict
    - readiness
    - approval
    - validation_pass_fail_authority
    - patch_queue
    - runtime_model_recommendation
  ca_adjudication_required: true
```
