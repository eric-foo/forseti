# Bronze Catalog v0 — Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review output
reviewed_by: claude-opus-4.8
authored_by: OpenAI GPT-family Codex home model
scope: Read-only de-correlated adversarial implementation/code review of Bronze Catalog v0 (PR #485) at commit b2a9c8f6.
use_when:
  - Adjudicating whether Bronze Catalog v0 has blocker/major correctness or false-traceability defects before merge consideration.
  - Checking the verified-read, non-authority, determinism, and fail-closed properties of the generated Bronze catalog.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/bronze_catalog_v0_delegated_adversarial_code_review_prompt_v0.md
```

## Provenance & Commission

| Field | Value |
| --- | --- |
| `reviewed_by` | `claude-opus-4.8` |
| `authored_by` | `OpenAI GPT-family Codex home model` |
| `de_correlation_bar` | `cross_vendor_discovery` (author = OpenAI GPT-family Codex; reviewer = Claude/Anthropic — different vendor lineage) |
| Commission | Read-only de-correlated adversarial implementation/code review of Bronze Catalog v0 |
| Review prompt | `docs/prompts/reviews/bronze_catalog_v0_delegated_adversarial_code_review_prompt_v0.md` |
| Review target | `codex/bronze-v41-clean-verify..b2a9c8f6cd4f74c11bb71a8a9794e174e2f76714` |
| PR | [eric-foo/orca#485](https://github.com/eric-foo/orca/pull/485) |
| Output mode | `review-report` (filesystem-output) |
| Edit permission | read-only review; report-write only to this path |

This review is **decision input for CA adjudication only**. It is not approval, validation, readiness, mandatory remediation, patch authority, merge authority, or production/runtime authorization. No `patch_queue_entry` is emitted; remediation is advisory direction only.

## Review Target Integrity & Staleness

- Review commit `b2a9c8f6` **exists and is fully reviewable** (subject: "Add Bronze catalog rebuild index", Eric, 2026-06-30).
- Base `codex/bronze-v41-clean-verify` = `879107981121b5bf64dbf9c4dbd064221a6aaf34`.
- **PR #485 head has advanced** to `31c312f54ea53f65b2e16d59a00192ffa3423b7f` — the prompt's `stale_if` ("PR #485 changes after commit b2a9c8f6") is triggered. The gap was quantified: `git diff b2a9c8f6..31c312f5` is **exactly one file** — the review prompt `.md` itself (+321), changing **none** of the four target files. This is precisely what the prompt anticipated ("This prompt file may appear in a later branch commit for routing… not part of the review target"). **Conclusion: staleness is immaterial.** Reviewing `b2a9c8f6` equals reviewing the current PR head minus the out-of-scope prompt file.
- Target diff `base..b2a9c8f6` verified via git: 4 files, `+698 / −2`, matching the prompt's "Expected target changed files":
  - `M docs/workflows/orca_repo_map_v0.md` (+4 / −2)
  - `A orca-harness/data_lake/catalog.py` (+461)
  - `A orca-harness/runners/run_data_lake_catalog.py` (+40)
  - `A orca-harness/tests/test_data_lake_catalog.py` (+193)

## Source Context Status — `SOURCE_CONTEXT_READY`

All required authority files, target files, support files, and the target diff were loaded; nothing required is missing. Target/support files were read from worktree `…/worktrees/bronze-catalog-v0` (HEAD `31c312f5`), which is **clean** and **byte-identical to `b2a9c8f6` for all seven files** (verified: `git diff b2a9c8f6 -- <files>` empty; `git status --porcelain` empty) — so the read line numbers correspond to the review commit.

Source-read ledger:

| Source | Why | Status |
| --- | --- | --- |
| `AGENTS.md` | Behavior kernel / project authority | clean (supplied in context) |
| `.agents/workflow-overlay/README.md`, `review-lanes.md`, `prompt-orchestration.md`, `source-loading.md`, `safety-rules.md` | Review lane, output, de-correlation, safety doctrine | clean (worktree HEAD; capsule: doctrine matches origin/main) |
| `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` | Preflight constants | clean |
| `orca-harness/data_lake/catalog.py` | Review target (new) | == `b2a9c8f6` |
| `orca-harness/runners/run_data_lake_catalog.py` | Review target (new) | == `b2a9c8f6` |
| `orca-harness/tests/test_data_lake_catalog.py` | Review target (new) | == `b2a9c8f6` |
| `docs/workflows/orca_repo_map_v0.md` (diff) | Review target (modified) | == `b2a9c8f6` |
| `orca-harness/data_lake/root.py` | Support: `load_raw_packet`, `raw_shard`, write guard | == `b2a9c8f6` |
| `orca-harness/source_capture/models.py` | Support: manifest/`VisibleFact`/`PreservedFile` shapes | == `b2a9c8f6` |
| `orca-harness/source_capture/writer.py` | Support: packet write path / manifest production | == `b2a9c8f6` |

## Method Invocation Status

- `workflow-deep-thinking`: REFERENCE-LOADed before source loading; APPLIED after `SOURCE_CONTEXT_READY` to frame failure modes (authority leakage, non-determinism, unverified reads, shard mis-indexing, false-`ok` inspect, facet over-claim, write-boundary divergence, fail-open CLI, test circularity).
- `workflow-code-review`: REFERENCE-LOADed before source loading; APPLIED after `SOURCE_CONTEXT_READY` in adversarial posture. Mode: **strict formal review** — lane (code review), severity vocabulary (`critical`/`major`/`minor`/`advisory`), output mode + `required_output_path`, and validation evidence are prompt-bound. Both skills resolved and were applied; no advisory-only fallback was required.

---

## Findings

**No `critical` findings. No `major` findings.** Findings are `minor` (3) and `advisory` (5). The implementation is non-authoritative by construction, deterministic/byte-rebuildable, routes every indexed packet through verified raw reads, and is fail-closed at the CLI. The minor findings concern write-discipline consistency, fail-closed test coverage, and ungraceful (but loud) error handling; advisories are robustness/clarity/future-extensibility notes.

### MINOR

#### BCV0-M1 — Catalog generation is a second writer that bypasses the lake's write-boundary guard
- **severity:** minor
- **reviewed target / purpose:** Bronze Catalog v0 write path / non-authority + write-boundary discipline.
- **location:** `orca-harness/data_lake/catalog.py:53` (`rebuild_catalog`), `:58-60` (`shutil.rmtree` + `_write_snapshot`), `:387-391` (`_write_snapshot` → `Path.write_bytes`), `:412-413` (`_catalog_root`).
- **evidence:** `rebuild_catalog` mutates the catalog by `shutil.rmtree(catalog_root)` then `path.write_bytes(body)` via raw `pathlib` joins. It does **not** use `DataLakeRoot`'s guarded write primitives — `_reverify()` (root-identity recheck before each write session, DL-003) and `_within()` (per-component symlink rejection + containment), which `root.py:483-506` applies to every raw/derived/availability write.
- **authority/evidence basis:** `root.py:1-31, 483-557` states the lake's write-boundary contract ("a single deterministic writer"; re-verify identity before each write session; reject symlinked components). The recently merged Silver Vault "validating write front-door" (repo HEAD `3475221d`) sits on a sibling path under `indexes/derived_retrieval/`. The Bronze catalog writes to `indexes/derived_retrieval/bronze_catalog/v0` without an equivalent guarded front-door.
- **impact:** The catalog is non-authoritative, disposable, and rebuildable, so blast radius cannot reach raw bytes; this is why it is minor, not major. But the catalog mutation gets no root-identity recheck (a swapped/remounted root between `resolve()` and rebuild is not re-detected for the catalog write the way it is for raw), and a symlink planted at/under the catalog dir would be followed by `write_bytes`/`rmtree` (within the module's already-accepted same-host active-adversary residual). It is a real divergence from the lake's own single-guarded-writer doctrine.
- **minimum_closure_condition:** Either catalog mutation routes through a guarded write surface that applies `_reverify()` + containment (reusing the existing root guards), **or** an explicit accepted-residual note records that generated, rebuildable `derived_retrieval` indexes write unguarded, reconciled with the Silver Vault write-front-door decision.
- **next_authorized_action:** Owner/CA decision on whether `derived_retrieval` writers must share one guarded front-door. (Advisory direction only; no patch authorized.)
- **not_proven:** Whether Orca doctrine *requires* all `indexes/derived_retrieval/` writers to use a validating/guarded write front-door is **not proven here** — the Silver Vault write-front-door decision was outside this review's bound source basis and was not loaded. Treat the consistency question as a CA determination, not a confirmed invariant breach.
- **verification expectation:** If unified, a same-check test asserting catalog writes fail closed on a swapped-root / symlinked-component condition.

#### BCV0-M2 — Fail-closed CLI root-error path and verified-read fail-closed are untested
- **severity:** minor
- **reviewed target / purpose:** CLI fail-closed behavior + verified-read guarantee / test strength (Q9/Q10/Q3).
- **location:** `orca-harness/tests/test_data_lake_catalog.py:174-193`; untested branches at `orca-harness/runners/run_data_lake_catalog.py:30-33` (`DataLakeRootError → status:error → return 2`) and `orca-harness/data_lake/catalog.py:134-137` (`load_raw_packet` per packet).
- **evidence:** `test_catalog_runner_inspects_and_rebuilds` monkeypatches `DataLakeRoot.resolve` to always return a valid root (`:180-184`), so the exit-2 root-error path is never exercised. No test tampers with a preserved file to confirm that a body-hash mismatch makes rebuild/inspect fail closed at the catalog level (it relies transitively on `load_raw_packet`'s own coverage in `test_data_lake_root`).
- **authority/evidence basis:** Prompt Review Questions 9 (CLI fail-closed) and 3/10 (verified reads, test strength). `run_data_lake_catalog.py:36` returns `2` only on the untested branch; `catalog.py:136-137` is the sole verified-read entry.
- **impact:** The two most safety-relevant guarantees of this feature — "surface root errors with a nonzero exit" and "never index an unverifiable packet" — have no direct regression test in this PR. A regression in either could pass CI.
- **minimum_closure_condition:** A test asserting a resolve failure yields `status:error` and exit `2`; a test asserting a tampered/short preserved file makes `rebuild_catalog`/`inspect_catalog` raise (or the runner exit nonzero) rather than index it.
- **next_authorized_action:** Implementer adds the two tests under the existing lane (advisory direction; not an executor-ready patch).
- **verification expectation:** Same-check red-green: the new exit-2 test fails against a build that swallows resolve errors; the tamper test fails against a build that skips `load_raw_packet`.

#### BCV0-M3 — `inspect_catalog` file read is unguarded against `OSError`, inconsistent with the packet-level scan
- **severity:** minor
- **reviewed target / purpose:** inspect semantics on unreadable generated state (Q5).
- **location:** `orca-harness/data_lake/catalog.py:394-401` (`_read_snapshot`, no try/except) vs `:87-99` (by_packet scan catches `OSError`/`ValueError` into `catalog_read_failures`).
- **evidence:** `_read_snapshot` does `path.read_bytes()` for every file under the catalog root with no error handling. An unreadable generated file (permission/IO error) raises an uncaught `OSError` out of `inspect_catalog`; the runner's `try` catches only `DataLakeRootError` (`run_data_lake_catalog.py:30`), so the process exits 1 with a traceback and **no** JSON report.
- **authority/evidence basis:** Q5 ("can `inspect_catalog` … [miss] … unreadable generated index state while reporting `ok`?"). The by_packet path already models the graceful pattern (`catalog_read_failures`); `_read_snapshot` does not.
- **impact:** Fails **loud** (no false `ok`), so it is not a correctness/false-success defect — hence minor. But the failure is an unstructured traceback rather than a reported issue, exit 1 becomes ambiguous with `issues_found`, and error handling is internally inconsistent.
- **minimum_closure_condition:** Unreadable generated files are surfaced as a structured catalog issue (e.g., a read-failure list) or the runner converts unexpected read errors into a visible structured error distinct from `issues_found`.
- **next_authorized_action:** Implementer hardens `_read_snapshot` / runner error handling (advisory direction).
- **verification expectation:** A test making a generated file unreadable yields a structured non-`ok` report, not a raw traceback.

### ADVISORY

#### BCV0-A1 — Extractor framework does not isolate extractor exceptions (Q7 future-adaptability)
`_extractor_facets` (`catalog.py:271-275`) calls `list(extractor(manifest, bodies))` with no guard. A *future* source-family extractor that raises on a malformed body would abort the entire rebuild/inspect (every packet), not just that packet's facets. The shipped IG extractor (`:278-329`) is defensively coded (pervasive `isinstance` checks, no raises), so there is **no live defect**. Direction: consider per-packet/per-extractor error isolation (skip + record) so one bad extractor cannot take down the whole catalog as new families are added.

#### BCV0-A2 — IG handle normalization edges (Q6)
`value = handle.lower().lstrip("@")` (`catalog.py:292`) with the truthiness guard applied to the *pre-normalization* handle (`:285-286`). A degenerate handle of only `@` (or chars that strip to empty) yields an empty facet value, which `_safe_name("")` maps to the `blank__<digest>` bucket (`:426`) rather than dropping it. Also `lstrip("@")` strips a character *set*, not a single prefix (`"@@x" → "x"`). Real IG handles are unaffected (low impact). Direction: guard on the normalized value (drop empty) and prefer `removeprefix("@")` if single-prefix semantics are intended. Traceability is otherwise intact — every IG facet carries `source` + `json_pointer` into the raw payload (`:293-295, 304-306, 325-327`), and `json_pointer` uses the true raw `joined_rows` index via `enumerate` (`:311, 326`).

#### BCV0-A3 — `_first_json_body` matches payload structure, not filename, despite a filename-shaped argument (Q6)
`_first_json_body(bodies, "ig_reels_grid_capture.json")` (`catalog.py:278-355`) ignores the filename: `_payload_looks_like` (`:352-355`) returns true for any dict containing both `creator_profile_snapshot` and `joined_rows`. The `(source_family, source_surface)` dispatch key (`:332-334`) already scopes this to IG reels packets, so risk is low, but the `suffix=`/`…json` naming is misleading, and a packet with two structurally-matching bodies would index only the first (by sorted `file_id`). Direction: rename the parameter to reflect structural matching; optionally assert a single matching body.

#### BCV0-A4 — `_safe_name` strip/digest inconsistency and Windows path-length worst case (Q8)
`_safe_name` (`catalog.py:420-426`) hashes the **unstripped** `value` for the 16-hex digest but builds the cleaned prefix from `value.strip()`. Current callers feed already-stripped values (`_string_or_none` / hashes), so there is **no live bug**; a future unstripped caller would split `"x"` and `" x "` into two buckets sharing a visible prefix but differing by digest. Separately, three nested `by_facet` segments of up to 82 chars each plus a Windows data-root prefix could approach the 260-char `MAX_PATH` limit for maximal-length facet values without long-path support, surfacing as an uncaught `OSError` at rebuild (fail-loud). Realistic facet values (short handles/shortcodes/families; the locator is hashed to 64 bits) stay well under the limit. Strengths confirmed: `_safe_name` is traversal-proof (every non-alphanumeric char → `_`; `..`/`/`/`\` neutralized), collision-safe (64-bit digest suffix), length-bounded (≤82 chars/segment), and deterministic/stable. Direction: hash the stripped value for consistency; be mindful of Windows path length for long values.

#### BCV0-A5 — Wrong-shard / legacy-flat raw are silently absent from the catalog; doctor owns that anomaly (Q4)
`_iter_committed_packet_ids` (`catalog.py:170-186`) indexes only `raw/<shard>/<pid>/` containers where `shard == raw_shard(pid)` and `manifest.json` exists, matching `root.py:rebuild_availability` (`:917-931`). Wrong-shard, legacy-flat, and partial containers are therefore **skipped** (failure-as-absence), and the catalog's `inspect` does **not** report them as anomalies — `run_data_lake_doctor.py` owns raw-placement anomaly detection. This is correct and by-design, but it means a catalog `inspect: ok` does **not** imply raw is correctly sharded; operators must also run the doctor. Direction: ensure operator docs/repo-map keep the catalog↔doctor division visible (the repo-map already lists the two runners separately).

---

## Adversarial Coverage Map (Review Questions 1–11)

| # | Question | Result |
| --- | --- | --- |
| 1 | Authority boundary | **No defect.** `rebuild_catalog` `rmtree`s then rebuilds entirely from raw via `load_raw_packet`; the written `manifest.json` declares `"generated_from_raw_packet_manifests; raw remains authoritative"` (`catalog.py:228-234`). Catalog lives under `indexes/` on the external data root (not committed). Nothing reads the catalog as authority. |
| 2 | Rebuildability / determinism | **Strong.** Entries sorted by `packet_id` (`:167`); buckets/facets sorted on write (`:218, 380-383`); JSON `sort_keys=True` (`:405, 409`). No rebuild-time wall-clock — `capture_time` is sourced from the frozen raw manifest (`:156-160`), and the catalog `manifest.json` carries **no** `generated_at`. Byte-identical rebuild is proven by `test…orphaned…byte_identically`. |
| 3 | Verified reads | **Satisfied.** Every indexed packet goes through `root.load_raw_packet` (`:136-137`), which re-hashes every preserved file vs the manifest `sha256`, checks size, rejects path escape, and fails closed (`root.py:855-882`). Both `rebuild` and `inspect` share this path via `_build_entries`. |
| 4 | Sharded raw correctness | **Satisfied** (see BCV0-A5). Wrong-shard / legacy-flat / partial / manifest-less containers are excluded; malformed manifests raise via `load_raw_packet` → exit 2. |
| 5 | Inspect semantics (false `ok`?) | **Strong; no false `ok` found.** A full byte-level snapshot diff (`missing_files`/`orphaned_files`/`stale_files`, `:76-82`) plus a packet-level diff and `catalog_read_failures` (`:84-117`) drive `issues`. Any missing, extra, or byte-changed generated file (including a stale facet index or corrupt JSON) sets `issues_found`. Caveat: unreadable generated file → loud crash, not a structured issue (BCV0-M3). |
| 6 | Facet correctness / traceability | **Satisfied** with minor edges (BCV0-A2/A3). Universal + IG facets are verbatim/normalized facts carrying `source` + `json_pointer` provenance; the locator is hashed in the facet while the cleartext stays in the `by_packet` entry (`:154, 257-267`), so hash→cleartext traceability is preserved. No semantic-truth overreach. |
| 7 | Future lane adaptability | **Good.** New extractors register in `_EXTRACTORS` keyed by `(source_family, source_surface)` (`:332-334`) with a generic `(manifest, bodies) → Iterable[CatalogFacet]` signature; no manifest-v1 or raw-layout change needed. See BCV0-A1 (exception isolation) for hardening. |
| 8 | Path/filename safety | **Strong.** `_safe_name` is traversal-proof, collision-safe (64-bit digest), length-bounded, deterministic (BCV0-A4 notes a latent strip inconsistency + Windows worst case). |
| 9 | CLI fail-closed | **Satisfied.** Exit `0` (`ok`/`rebuilt`), `1` (`issues_found`), `2` (root error) (`run_data_lake_catalog.py:30-36`); `inspect` is read-only; `--rebuild` `rmtree`s only the catalog dir. Coverage gap in BCV0-M2. |
| 10 | Test strength | **Adequate, non-circular** for the named behaviors (missing/stale/orphan/byte-identity/IG facets/CLI exit 0-1). Gaps: fail-closed root error (exit 2), corrupt-raw verified-read, empty-lake, wrong-shard skip, locator facet (BCV0-M2). Assertions are behavioral (status, exit codes, byte-identity, facet values), not implementation-circular. |
| 11 | Repo-map accuracy | **Accurate, non-overclaiming.** The added rows (`orca-harness/data_lake/`, `run_data_lake_catalog.py`, tests row, Refreshed line) correctly state "non-authoritative", "from verified raw packet manifests", inspect-by-default/rebuild-only-with-`--rebuild`, and make no readiness/validation/production-runtime or source-capture-runner-rewiring claim. The standing "Implementation authorized: no" header line is the map's own retrieval-only authority boundary (unchanged context), not a claim that no code was added. |

## Validation Evidence Inspected

| Check | Source | Status |
| --- | --- | --- |
| Focused catalog tests (`tests/test_data_lake_catalog.py`) | **Rerun by reviewer** in `…/worktrees/bronze-catalog-v0/orca-harness` (`python -m pytest -p no:cacheprovider tests/test_data_lake_catalog.py`) | **`4 passed in 2.53s`, exit 0** — independently reproduced the author's reported "4 passed". |
| Broad lake/capture regression pack (17 files) | Author-reported `144 passed, 1 skipped` | **Not rerun by reviewer** (scope/time); reported only. |
| `git diff --check`, `compileall`, `check_retrieval_header`, `header_index --strict`, `check_map_links --strict`, `check_repo_map_freshness --strict` | Author-reported all pass | **Not rerun by reviewer**; reported only. |
| Target diff identity (`base..b2a9c8f6`, 4 files, +698/−2) | Reviewer `git diff --stat` / `--name-status` | **Verified.** |
| Worktree-vs-commit identity for 7 read files | Reviewer `git diff b2a9c8f6 -- <files>` (empty) | **Verified.** |

## Not-Proven Boundaries & Strict-Only Notes

- Whether Orca doctrine **requires** all `indexes/derived_retrieval/` writers to share a validating/guarded write front-door — **not proven** (Silver Vault write-front-door decision not loaded; out of bound source basis). BCV0-M1 is framed as a CA consistency question, not a confirmed invariant breach.
- The broad 144-test regression pack and the six static/strict hooks were **not rerun** by this reviewer; their pass status is author-reported only.
- Runtime/production and real external-data-root behavior were **not exercised**; tests use `DataLakeRoot.for_test` temp roots.
- Concurrent mutation during `inspect`/`rebuild` (TOCTOU) is out of scope — single-operator local tool, consistent with `root.py`'s module-level accepted residual (DL-003).
- This review confers no acceptance, validation, readiness, or merge authority.

## Residual Risk

**Low.** The feature is non-authoritative, deterministic/byte-rebuildable, verified-read, and fail-closed at the CLI; the central safety property (inspect cannot report `ok` while generated state diverges from raw) holds under adversarial analysis. Residual risk concentrates in: (a) a second write path that does not share the lake's guarded-writer discipline (disposable-index blast radius only); (b) absent regression coverage for the fail-closed root-error and corrupt-raw paths; (c) ungraceful-but-loud handling of unreadable generated files. None can corrupt raw authority, fabricate catalog truth, or hide stale generated state behind a false `ok`.

## Recommendation

**`minor_findings_only`** — no blocker or major correctness/false-traceability defects found. The minor findings (BCV0-M1 write-discipline consistency, BCV0-M2 fail-closed test coverage, BCV0-M3 unreadable-file handling) and advisories are worth addressing but do not, individually or together, block merge on correctness grounds. Disposition is the CA's.

## Review-Use Boundary

These findings are **decision input only**. This review does not approve, validate, require remediation, authorize patches, authorize commits, authorize merge, or authorize production/source-system runtime. Severity labels (`critical`/`major`/`minor`/`advisory`) are prompt-bound finding-priority labels and create no approval, rejection, readiness, or mandatory-remediation authority. CA consumption order: commission → target → authority → decision criteria → evidence → reviewer recommendation.
