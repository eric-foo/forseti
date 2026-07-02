# Bronze Catalog Source Surface Coverage — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: cross-vendor delegated adversarial code review output
scope: Review findings for PR #491 Bronze Catalog source-surface coverage slice (source_surfaces.json, inspect/rebuild coverage, registered/universal_only labeling, tests).
use_when:
  - Adjudicating PR #491 Bronze Catalog source-surface coverage review findings.
  - Auditing source-surface retrievability / false-completeness risk before Silver/projection coordination.
authority_boundary: retrieval_only
```

Read-only, findings-first adversarial implementation review of PR #491's merged
Bronze Catalog source-surface coverage slice, commissioned via
`workflow-delegated-review-patch` and routed to read-only `workflow-code-review`.

```yaml
reviewed_by: Anthropic/Claude (claude-opus-4-8)
authored_by: OpenAI/Codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable
review_location: lane_worktree_docs_review_outputs
review_path_note: >
  Commission named an absolute path under the main checkout
  (C:\Users\vmon7\Desktop\projects\orca\docs\review-outputs\...). Written instead to
  the same relative path inside the executing isolated worktree
  (.claude/worktrees/loving-allen-8773b0/docs/review-outputs/...), which is the
  tracked on-main review-outputs convention and is PR-flowable on a lane branch.
  The main checkout was flagged dirty/out-of-scope by the commission, so a direct
  write there would drop an untracked, off-lane file. Relocate/cherry-pick to the
  Bronze lane if the owner prefers.
authority_boundary: retrieval_only
output_mode: file-write
posture: adversarial, findings-only, advisory decision-input
not_claimed:
  - formal verdict
  - severity authority
  - approval / readiness / validation pass-fail
  - patch queue / executor-ready handoff
  - runtime model recommendation
```

## Status

- `SOURCE_CONTEXT_READY` — all commissioned targets, the PR #491 diff range, the
  CLI runner, and the controlling repo-map rows were source-loaded.
- **Hash pins: VERIFIED (no `HASH_MISMATCH`).** All three pins match the
  Windows-checkout (CRLF) variant of the blob at merge commit
  `0342a3b3602513e57acce457bf2035fb297a68b1`; the underlying content is
  byte-identical to the pinned bytes. The bronze-lane worktree working-tree
  files reproduce the same `Get-FileHash` SHA256 values.

  | path | pinned SHA256 | result |
  | --- | --- | --- |
  | `orca-harness/data_lake/catalog.py` | `2AC2…B40D` | match |
  | `orca-harness/tests/test_data_lake_catalog.py` | `77D8…A1EA` | match |
  | `docs/workflows/orca_repo_map_v0.md` | `45B3…ED44` | match |

- **Validation rerun (reviewer-observed, this turn):** `python -m pytest -p
  no:cacheprovider tests\test_data_lake_catalog.py` →
  **`8 passed, 1 skipped in 2.31s`**, run in
  `worktrees\bronze-lane-coverage-review-prompt\orca-harness` whose
  `catalog.py`/`test_data_lake_catalog.py` match the pins. Reproduces the
  dispatcher's observed `8 passed, 1 skipped`. The single skip is the
  directory-symlink test, which `pytest.skip`s when symlink creation is
  unavailable (expected on this Windows host).

## Commission Recap, Scope, Excluded Scope

- **Target:** PR #491 Bronze Catalog source-surface coverage —
  `source_surfaces.json` generation, inspect/rebuild report coverage,
  `registered | universal_only` extractor labeling, future-lane adaptability,
  and tests.
- **Purpose:** Determine whether the merged slice creates traceable,
  rebuildable, **non-authoritative** retrieval coverage for current and future
  capture lanes without false completeness, stale-index, schema-consumer, or
  authority-overclaim risk; give the home model actionable findings to
  adjudicate.
- **In scope:** the three pinned files and the `c197ec46…` over `230511aa…`
  diff; the `run_data_lake_catalog.py` consumer was read as context for the
  schema-compat axis.
- **Excluded:** patch execution, formal verdict/severity authority, readiness,
  approval, the dirty root checkout's unrelated untracked files, and any runtime
  model recommendation.

## Method Order Applied

REFERENCE-LOADED the named methods' intent, then SOURCE-LOADED targets + diff +
runner, then applied adversarial failure-mode framing (deep-thinking) and a
findings-first code-review pass. The named methods are Codex-side
`SKILL.md` paths under `~/.codex/...`; as the de-correlated Anthropic reviewer I
applied the Orca repo's own `workflow-code-review` skill contract (loaded this
thread) for the findings standard. The commission's Output Contract pins the
finding field set and overrides any skill-default format.

## What Is Solid (confidence signal, not approval)

These held up under adversarial inspection and are stated so the home model can
weight the findings below:

- **Generation purity / non-authority.** `source_surfaces.json` is derived
  entirely from `_source_surface_summary(entries)` where `entries` come from
  `_build_entries` reading verified raw packet manifests (`catalog.py:55-57`,
  `76-78`, `140-175`, `255-287`). It introduces no second authority over
  capture-lane truth; the sibling `manifest.json` re-states
  `"generated_from_raw_packet_manifests; raw remains authoritative"`
  (`catalog.py:247`).
- **Inspect honesty parity.** `source_surfaces.json` is a first-class member of
  the snapshot dict, so the generic byte-level diff in `inspect_catalog`
  (`catalog.py:80-87`, `113-121`) detects it as `missing_files` /
  `stale_files` / `orphaned_files`, and an unreadable copy surfaces in both
  `catalog_read_failures` and `missing_files` (same mechanism the
  `all_packets.jsonl` read-failure test exercises). The `issues` boolean and the
  runner exit code (`run_data_lake_catalog.py`) reflect it honestly.
- **Future-lane adaptability with no hardcoded family list.** Bucketing keys on
  whatever `(source_family, source_surface)` appear; unknown lanes get a row
  with `facet_extractor: universal_only` and their universal facet namespaces
  (`test_…_marks_unknown_future_surface_universal_only`). No false negative for
  unknown lanes.
- **Determinism.** Summary sorted by `(family or "", surface or "")`,
  `facet_namespaces` `set`→`sorted`, `_json_bytes(..., sort_keys=True)`.
  Report `source_surfaces` and the on-disk `source_surfaces.json` are the same
  computation and are asserted byte-equal after round-trip
  (`test_…_indexes_universal_and_ig_facets`, lines 138-146). No unstable
  generated bytes observed.
- **Per-entry label accuracy.** `facet_extractor` is keyed on the same
  `_string_or_none`-normalized `(family, surface)` tuple used both for the
  extractor lookup and for bucketing (`catalog.py:145`, `162`, `258`,
  `328-332`), so registered-ness is internally consistent within a bucket; the
  upgrade loop at `270-271` cannot produce a mixed/incorrect bucket label.

## Findings (ordered by materiality)

### F-01 — `facet_extractor` / `facet_namespaces` carry implicit completeness with no inline semantics (false-completeness / misread risk)

- **Commissioned target & purpose:** retrieval labeling that "cannot be misread
  as semantic completeness, capture support, Silver readiness, or downstream
  projection coverage."
- **Reviewed target / role:** `data_lake/catalog.py` — generated
  `source_surfaces.json` + report fields.
- **Location:** `catalog.py:162` (`"registered" | "universal_only"`),
  `223-229` (`source_surfaces.json` payload), `255-287`
  (`_source_surface_summary`, esp. `272-275` namespace union).
- **Implementation evidence:** `facet_extractor` is set to `"registered"`
  purely because `_extractor_key(manifest) in _EXTRACTORS` — i.e. *an extractor
  function is wired*, not that it produced any facets. A registered packet with
  a malformed/absent `ig_reels_grid_capture.json` body yields zero extractor
  facets (`_extractor_facets` returns `[]`, `323-325`) yet still labels
  `registered`. `facet_namespaces` is a **union** across a surface's packets
  (`bucket["facet_namespaces"].add(namespace)`), so a namespace present in one
  packet is reported for the surface even if other packets lack it. The emitted
  `source_surfaces.json` (`223-229`) contains no legend defining either field.
- **Authority / evidence basis:** code as read; commission fitness reference
  ("without false completeness"); repo doctrine that Bronze is non-authoritative
  generated read state.
- **Impact (retrieval / review-confidence):** a downstream Silver/projection
  consumer can read `registered` as "lane fully supported / Silver-ready" and
  `facet_namespaces` as "every packet on this surface exposes these
  identifiers." Both are stronger than the data guarantees (registered =
  extractor-wired; namespaces = present-in-some). This is exactly the
  false-completeness overclaim the commission targets. No correctness break;
  the risk is in consumer interpretation.
- **minimum_closure_condition:** `source_surfaces.json` (and/or the repo-map /
  harness docs) state inline that `facet_extractor` describes only whether a
  richer facet extractor is *registered* (not capture/Silver/projection
  completeness) and that `facet_namespaces` is a union (presence-in-some, not a
  per-packet guarantee).
- **next_authorized_action:** report only (read-only lane). Owner decides
  whether to add an inline semantics note / `"semantics"` key or a docs line.
- **verification expectation:** confirm a definition string ships with the
  generated file or in the consuming doc; optionally a test asserting a
  union-vs-intersection case (one IG packet with shortcodes + one without still
  lists `instagram_shortcode` for the surface).
- **patch_queue_entry authorized:** no.

### F-02 — `source_surfaces.json` payload carries no inline non-authority / non-completeness marker

- **Commissioned target & purpose:** keep Bronze "generated, non-authoritative
  read state" and prevent a second source of authority.
- **Reviewed target / role:** `data_lake/catalog.py` — `source_surfaces.json`
  payload.
- **Location:** `catalog.py:223-229` vs `245-251` (`manifest.json` authority
  line at `247`).
- **Implementation evidence:** the catalog's `manifest.json` carries
  `"authority": "generated_from_raw_packet_manifests; raw remains
  authoritative"`. The new `source_surfaces.json` payload carries only
  `catalog_version`, `source_surface_count`, `source_surfaces`. A consumer that
  loads `source_surfaces.json` in isolation (a plausible "what lanes exist?"
  entry point) sees no authority/completeness disclaimer.
- **Authority / evidence basis:** code as read; module docstring (`catalog.py:1-6`)
  and `manifest.json:247` establish the intended non-authority posture that this
  file does not echo.
- **Impact (authority / review-confidence):** mild authority-overclaim surface —
  the most "registry-like" generated file is the one without the disclaimer the
  rest of the catalog carries. Bounded because the file lives inside the
  generated catalog dir alongside `manifest.json`.
- **minimum_closure_condition:** `source_surfaces.json` echoes a short authority
  / non-completeness marker (e.g. an `"authority"` field mirroring
  `manifest.json`), or docs explicitly state the catalog `manifest.json` is the
  single authority anchor for all generated files.
- **next_authorized_action:** report only; owner decides.
- **verification expectation:** the disclaimer string is present in the
  generated file or the owning doc names `manifest.json` as the catalog-wide
  anchor.
- **patch_queue_entry authorized:** no.

### F-03 — No reverse index from a surface name to its `by_source_surface` file; consumers must reimplement `_safe_name`

- **Commissioned target & purpose:** whether a downstream Silver/projection lane
  could still fail to coordinate because the catalog "lacks a stable query
  path."
- **Reviewed target / role:** `data_lake/catalog.py` — surface inventory vs
  per-surface index files.
- **Location:** `catalog.py:223-229` (`source_surfaces.json` lists raw surface
  strings) vs `231` + `433-441` (`by_source_surface/<safe>.jsonl`) +
  `485-491` (`_safe_name`).
- **Implementation evidence:** `source_surfaces.json` lists surfaces by raw
  string (e.g. `"r/B2BMarketing"`), but the per-surface packet list is written
  to `by_source_surface/{_safe_name(surface)}.jsonl`, where `_safe_name` is
  `sha256[:16]` + ASCII-alnum lowercasing + 64-char truncation + `__digest`
  suffix. There is no stored mapping from the raw surface name to that filename.
- **Authority / evidence basis:** code as read; commission's downstream-coordination
  axis.
- **Impact (retrieval / coordination):** a consumer using `source_surfaces.json`
  as the discovery entry point cannot deterministically locate the surface's
  index file without re-deriving `_safe_name`, making that private helper an
  implicit cross-lane contract. Severity is bounded: a consumer can instead
  full-scan `all_packets.jsonl` or `by_packet/*.json` and filter on
  `source_surface` (packet ids and `source_surface` are on every row,
  `415-425`), so the capability exists — this is friction/coupling, not a dead
  end.
- **minimum_closure_condition:** either `source_surfaces.json` carries the
  resolved relative path (or safe-name) for each surface's index file, or the
  docs state that `all_packets.jsonl` / `by_packet` is the stable query path and
  the `by_*` buckets are convenience-only with a non-contract filename scheme.
- **next_authorized_action:** report only; owner decides whether to expose a
  path/locator field.
- **verification expectation:** a consumer can map a `source_surfaces.json` row
  to its packet list without importing `catalog.py` internals.
- **patch_queue_entry authorized:** no.

### F-04 — Generated schema changed without bumping `BRONZE_CATALOG_VERSION`

- **Commissioned target & purpose:** whether adding `source_surface_count` /
  `source_surfaces` (and the per-entry `facet_extractor`) is schema-compatible
  for existing CLI or programmatic consumers.
- **Reviewed target / role:** `data_lake/catalog.py` — version constant vs new
  schema.
- **Location:** `catalog.py:20` (`BRONZE_CATALOG_VERSION = "bronze_catalog_v0"`,
  unchanged); new shape at `67-68`, `127-128`, `162`, `223-229`.
- **Implementation evidence:** this PR adds `facet_extractor` to every
  `by_packet/*.json` entry, adds the `source_surfaces.json` file, and adds
  `source_surface_count` / `source_surfaces` to both reports — all still tagged
  `catalog_version: "bronze_catalog_v0"`, identical to the pre-PR schema.
- **Authority / evidence basis:** code as read; `run_data_lake_catalog.py` emits
  the report verbatim and keys its exit code only on `status`.
- **Impact (schema-compat):** **additive and safe for lenient consumers**
  (unknown keys ignored; exit-code logic untouched). The residual is that
  `catalog_version` no longer uniquely identifies the on-disk schema — a
  consumer that branches on `catalog_version` to decide which fields/files exist
  cannot distinguish pre- vs post-PR catalogs, and `by_packet` entries silently
  gained a field under the same version. Blast radius is bounded: the byte-level
  inspect diff flags a pre-PR catalog as `stale_files` and forces `--rebuild`,
  and the catalog is non-authoritative generated state.
- **minimum_closure_condition:** either bump the version for the new shape, or
  document that `catalog_version` is a family tag (not a schema-shape
  identifier) and consumers must feature-detect.
- **next_authorized_action:** report only; owner decides version policy.
- **verification expectation:** a stated version/feature-detection contract for
  consumers.
- **patch_queue_entry authorized:** no.

### F-05 — Test gaps: new file's stale/missing detection and multi-packet / null-key surface buckets are unexercised

- **Commissioned target & purpose:** whether tests protect meaningful behavior,
  including "generated-file parity, and stale/orphan detection."
- **Reviewed target / role:** `tests/test_data_lake_catalog.py`.
- **Location:** `test_data_lake_catalog.py:194-213` (stale targets `by_packet`),
  `216-234` (orphan targets a `junk/` file), `255-280` (read-failure targets
  `all_packets.jsonl`); `_source_surface_summary` paths
  `catalog.py:255-287`.
- **Implementation evidence:** parity of `source_surfaces.json` with the report
  is asserted (lines 138-146), and registered/universal/future-lane labels are
  covered. But **no test directly deletes or mutates `source_surfaces.json` and
  asserts it appears in `missing_files` / `stale_files`** — that file's
  honesty rides entirely on the generic snapshot diff (which the strengths
  section confirms is sound, but it is the new artifact and lacks a dedicated
  regression test). Also unexercised: a surface with **≥2 packets** (so
  `packet_count` increments past 1 and `facet_namespaces` unions across
  packets), and a manifest with **missing/empty `source_family`/`source_surface`**
  (the `(None, None)` bucket and the `or ""` sort path at `284-286`).
- **Authority / evidence basis:** test file as read; commission's tests axis.
- **Impact (validation confidence):** low probability of a live defect (the
  mechanism is generic and partly covered elsewhere), but a future refactor that
  drops `source_surfaces.json` from the expected snapshot, mishandles
  multi-packet union, or crashes on null keys would not be caught by a named
  test. This is a coverage/regression-durability gap, not a current failure.
- **minimum_closure_condition:** add tests that (a) mutate/remove
  `source_surfaces.json` and assert `stale_files` / `missing_files`, (b) put two
  packets on one surface and assert `packet_count == 2` with a unioned
  `facet_namespaces`, and (c) build a packet with absent family/surface and
  assert a stable `(null, null)` row without error.
- **next_authorized_action:** report only; owner decides whether to add tests.
- **verification expectation:** the proposed tests would fail against any
  regression in the named behaviors and pass against current code (red-green
  expectation; not executed by this read-only lane).
- **patch_queue_entry authorized:** no.

## Source-Read Ledger

| source | how read | role |
| --- | --- | --- |
| `orca-harness/data_lake/catalog.py` @ `0342a3b3` | `git show` → scratchpad, full read | primary implementation |
| `orca-harness/tests/test_data_lake_catalog.py` @ `0342a3b3` | `git show` → scratchpad, full read | test evidence |
| `docs/workflows/orca_repo_map_v0.md` @ `0342a3b3` | hash-verified; diff rows read | doc target |
| PR #491 diff `230511aa..c197ec46` | `git diff` full read | change under review |
| `orca-harness/runners/run_data_lake_catalog.py` @ `0342a3b3` | `git show`, full read | schema-compat consumer context |
| pins vs blob (raw LF + CRLF) | `git show \| sha256sum` + `Get-FileHash` | hash verification |
| focused pytest in bronze-lane worktree | rerun this turn | validation evidence |

No dirty/untracked source was used as evidence. The reviewed bytes are the
pinned merge-commit bytes; the bronze-lane worktree working tree matches them.

## Strict-Only Blockers / `not proven`

- No formal verdict, severity ranking, readiness, approval, or pass/fail is
  claimed — none is authorized by this prompt.
- **`not proven`:** behavior of real downstream Silver/projection consumers
  against this catalog (none inspected — F-03 reasons from the catalog surface
  only); runtime behavior on a populated production lake (only fixture-scale
  packets were exercised); cross-platform symlink-rejection path (skipped on
  this host).

## Validation Run Status

`validation_rerun = passed_observed` — `8 passed, 1 skipped` reproduced this
turn against pin-matching files. Treated as evidence, not as a review pass/fail
claim.

## Open Questions (for the home model / owner)

1. Is `source_surfaces.json` intended as a standalone discovery entry point? If
   yes, F-01/F-02/F-03 (inline semantics, authority marker, surface→file path)
   gain weight; if it is only ever read alongside `manifest.json` and `by_*`,
   they shrink to docs notes.
2. Are there programmatic consumers that branch on `catalog_version` (F-04), or
   is feature-detection the assumed contract?
3. Should `facet_extractor` distinguish "extractor registered" from "extractor
   produced facets," or is the registered/found distinction intentionally out of
   scope for v0?

## Residual Risk

Low for correctness — the slice is internally consistent, deterministic, and
honestly inspected, with passing focused tests. The residual risk is
**interpretation**: a downstream lane over-reading `registered` /
`facet_namespaces` / the disclaimer-free `source_surfaces.json` as completeness
or authority (F-01/F-02), plus coordination friction if that file is used as a
standalone index without a path bridge (F-03). F-04/F-05 are durability concerns
(version contract, regression coverage), not active defects.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation,
readiness, mandatory remediation, severity authority, or executor-ready patch
authority until separately accepted or authorized. `proposed patch`, `diff`,
`exact requested edits`, formal verdict, and patch queue are `NOT_CLAIMED`.

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission/target: PR #491 Bronze Catalog source-surface coverage
  slice — source_surfaces.json generation, inspect/rebuild report coverage,
  registered|universal_only labeling, future-lane adaptability, tests, repo-map
  wording. Pinned at merge commit 0342a3b3; diff 230511aa..c197ec46.
- implementation context/diff/files: catalog.py (+69/-9), test_data_lake_catalog.py
  (+62), orca_repo_map_v0.md (wording). Reviewed at verified hash pins; runner
  run_data_lake_catalog.py read for schema-compat.
- findings + evidence: F-01 registered/facet_namespaces imply completeness with
  no inline semantics (catalog.py:162,223-229,255-287); F-02 source_surfaces.json
  lacks the non-authority marker manifest.json carries (223-229 vs 247); F-03 no
  reverse index from surface name to by_source_surface/_safe_name file
  (223-229,433-441,485-491); F-04 schema changed without bumping
  BRONZE_CATALOG_VERSION (20); F-05 no dedicated test for source_surfaces.json
  stale/missing or multi-packet/null-key buckets (test file 194-280).
- proposed patch/diff/edits: NOT_CLAIMED (read-only commission).
- citations: line anchors above; pins verified; PR #491.
- reviewer verdict: NOT_CLAIMED (advisory findings only; no verdict lane bound).
- validation evidence/not-run: reran focused pytest → 8 passed, 1 skipped
  (symlink test skipped on Windows). No populated-lake or real-consumer run.
- residual risk: interpretation/overclaim (F-01/F-02), coordination friction
  (F-03); version-contract + coverage durability (F-04/F-05). Correctness risk low.
- blockers/off-scope/not-proven: no formal verdict/severity/readiness/patch
  authorized; downstream-consumer and production-lake behavior not proven;
  cross-platform symlink path skipped.
```
