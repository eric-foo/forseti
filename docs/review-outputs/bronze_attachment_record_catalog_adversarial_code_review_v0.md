# Bronze Attachment Record Catalog Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Findings-first cross-vendor adversarial implementation/code review of the Bronze
  Catalog AR-MGT-90 generated Attachment Record retrieval slice (commit b85e2a3d).
use_when:
  - Adjudicating whether the Bronze Catalog generated Attachment Record implementation is safe to keep/merge.
  - Checking the residual risks and test-coverage gaps named for the generated AR retrieval slice.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/bronze_attachment_record_catalog_adversarial_code_review_prompt_v0.md
  - .agents/workflow-overlay/review-lanes.md
```

## Review Provenance

```yaml
reviewed_by: claude-opus-4.8        # observed identity of the reviewing model (this run); operator/CA confirms on the durable record per review-lanes.md
authored_by: openai-gpt-5-codex     # per prompt-recorded author_home_model_family
de_correlation_bar: cross_vendor_discovery
de_correlation_basis: >
  Author vendor = OpenAI (GPT-family Codex); reviewer vendor = Anthropic (Claude Opus 4.8).
  Different upstream model lineage -> cross-vendor discovery bar satisfied (review-lanes.md
  two-bar rule; delegated-review-patch.md de-correlation criterion). who-constraint only;
  no runtime-model recommendation is made or implied.
same_vendor_rationale: not_applicable   # required only when de_correlation_bar = same_vendor_sanity
review_lane: read-only implementation/code review (advisory, findings-first)
patch_authority: none                # prompt commissions NO delegated patch; reviewer did not edit any source file
```

## Commission (as received)

- **Target:** implementation commit `b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179` on branch
  `codex/bronze-ar-mgt-90`, base `f36d7f62c6a8e932e26fcc94718d7eb91be6a981`.
- **Target files (only patchable/observed scope):** `orca-harness/data_lake/catalog.py`,
  `orca-harness/tests/test_data_lake_catalog.py`, `docs/workflows/orca_repo_map_v0.md`.
- **Purpose:** independently attack whether the generated `attachment_records/` catalog gives
  downstream lanes durable typed retrieval coordinates over preserved raw bodies without
  mutating raw packets or overclaiming final AR physicalization; verify fail-closed body
  resolution; check source-surface coordination honesty; check source-family-agnosticism;
  scan only the touched scope.
- **Authority basis used:** `AGENTS.md`, `.agents/workflow-overlay/{review-lanes,
  delegated-review-patch,validation-gates,safety-rules,source-of-truth,source-loading,
  prompt-orchestration}.md`, and the AR implementation contract
  `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
  as the code fitness bar (spec).

## Source-Read Ledger

| Source | Why read | Range/section | Supports | State |
| --- | --- | --- | --- | --- |
| `docs/prompts/reviews/bronze_attachment_record_catalog_adversarial_code_review_prompt_v0.md` (@`c57bc79a`) | The commission | full | scope, output contract | clean (read from carrier commit; file not on review lane's working tree) |
| `AGENTS.md`, overlay `README.md` | Orca authority gate | full | authority, lane rules | clean |
| `.agents/workflow-overlay/review-lanes.md` | Lane + de-correlation + provenance rules | full | findings-first, two-bar, reviewed_by/authored_by | clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | Code-review-and-patch convention, no-patch routing | full | read-only routing, de-correlation criterion | clean |
| `.agents/workflow-overlay/{validation-gates,safety-rules,source-of-truth,source-loading,prompt-orchestration}.md` | Boundaries, completion evidence, source-gated method | full | strict-claim boundary, fail-visible | clean |
| `orca-harness/data_lake/catalog.py` (@`b85e2a3d`) | Primary review object | full (916 lines) | all findings | clean; sha256(LF blob)=`D66EB6A1…` matches author pin |
| `orca-harness/tests/test_data_lake_catalog.py` (@`b85e2a3d`) | Test contract coverage | full (620 lines) | AR-06, F5 | clean; sha256(LF blob)=`940AAFE2…` matches author pin |
| `docs/workflows/orca_repo_map_v0.md` (@`b85e2a3d`) | Repo-map honesty | AR diff hunk | AR-05 | clean; see drift note below |
| `orca-harness/data_lake/root.py` (@`b85e2a3d`) | `load_raw_packet`/`_reverify`/`raw_shard`/`_within` semantics | targeted | AR-02 fail-closed | clean |
| `orca-harness/source_capture/{models,writer}.py` (@`b85e2a3d`) | `hash_basis` universe + preserved-file shape | targeted | F2 | clean |
| `…/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` (@`b85e2a3d`) | Code fitness bar (spec) | full | AR-01..AR-07 | clean |
| `orca-harness/runners/run_data_lake_catalog.py` (@`b85e2a3d`) | Runner exit-code/error surface | full (40 lines) | AR-06 | clean |

**Target-file drift note (benign).** The carrier commit `c57bc79a` adds only the review
prompt and touches none of the three target files (`git diff --stat b85e2a3d..c57bc79a` =
prompt file only). Two of three author SHA pins reproduce exactly from the `b85e2a3d` blob
(`catalog.py`, test file). The `repo_map` pin differs (`8D9686BC…` LF blob vs author
`A281D224…`) **solely because the author hashed the CRLF Windows worktree copy**: re-encoding
the exact `b85e2a3d` LF blob to CRLF reproduces `A281D224…` byte-for-byte. Content under review
is identical to what the author committed; no retarget needed.

## SOURCE_CONTEXT_READY

`SOURCE_CONTEXT_READY`. Required Orca authority, the three target files at `b85e2a3d`, adjacent
implementation/contract context, and the validation environment were all loaded with no
unresolved conflicts. `workflow-deep-thinking` and `workflow-code-review` were REFERENCE-LOADED
(available as resolver skills) and APPLIED only after this declaration; strict review claims are
`NOT_CLAIMED` (advisory, findings-first — consistent with the prompt's strict-claim boundary).

## Findings (lead)

No `blocker` and no `major` finding. The slice is well-built and tightly aligned to the AR
implementation contract: bodies are referenced (never copied), raw packets are never mutated,
the loader fails closed, and the honesty/non-completeness labels are explicit and tested. Five
`minor` findings follow — robustness, forward-coupling, and test-coverage hardening, none a live
defect.

---

### F1 — `attachment_record_id` material string uses an unescaped `|` delimiter
- **Severity:** minor (priority only; not an Orca verdict)
- **Target:** `orca-harness/data_lake/catalog.py:480`–`484` (`_attachment_record_id`), esp. `:483`
  `material = "|".join((packet_id, file_id, relative_packet_path, body_sha256))`
- **Evidence:** the AR id is `ar_` + `sha256(material)[:32]` over four fields joined by a bare `|`
  with no escaping/length-prefix. Distinct field tuples that differ only by where a `|` falls map
  to the same `material` (e.g. `file_id="a|b", path="c"` vs `file_id="a", path="b|c"`).
- **Authority/evidence basis:** prompt review-scope question "avoid positional `file_id` … while
  still remaining stable and collision-resistant"; AR-01 goal (collision-resistant ids).
- **Concrete impact:** today low-probability — `packet_id` is a 26-char Crockford ULID and
  `body_sha256` is hex (neither can contain `|`), and the writer mints `file_id=file_{index:02d}`.
  But the generator reads `file_id`/`relative_packet_path` from the manifest, so a future writer,
  projection, or POSIX path containing `|` could collide two bodies onto one AR id, silently
  dropping one record from `by_attachment_record/` (last write wins on the `{record_id}.json`).
- **Minimum closure condition:** AR id derivation is collision-safe for any string field values
  (e.g. length-prefixed/NUL-joined material, or per-field hashing) — or the field domains are
  asserted `|`-free at generation so a violation fails loud.
- **Next authorized action:** owner decision to accept as residual (constrained inputs) or
  authorize a bounded hardening patch.
- **Validation expectation:** a unit test constructing two preserved files whose `(file_id,
  relative_packet_path)` differ only by `|` placement asserts distinct AR ids.

### F2 — Loader's supported-`hash_basis`/`body_ref_kind` set is an independent literal that must co-evolve with `HASH_BASIS_VALUES`
- **Severity:** minor / optional hardening (forward-coupling; not a live bug)
- **Target:** generation `orca-harness/data_lake/catalog.py:424`, `:458`, `:460`; loader
  `:770`–`:781` (`expected_body_ref_kind != "raw_packet_relative_path"`,
  `expected_hash_basis != "raw_stored_bytes"`); upstream
  `orca-harness/source_capture/models.py:66` `HASH_BASIS_VALUES = frozenset({"raw_stored_bytes"})`.
- **Evidence:** `_packet_attachment_records` copies the manifest `hash_basis` verbatim and
  hard-codes `body_ref_kind="raw_packet_relative_path"`; `load_attachment_record_body` accepts
  **only** `hash_basis=="raw_stored_bytes"` and that one `body_ref_kind`. The two
  accepted-value sets are separate literals in two modules.
- **Authority/evidence basis:** AR contract Required Shape #1/#3 (carry `hash_basis`, "hash basis
  must say what bytes are covered"); `models.py` validator message: "Add a value only when a
  writer produces that basis."
- **Concrete impact:** **currently safe** — the `PreservedFile` validator constrains `hash_basis`
  to the singleton `raw_stored_bytes`, so every generated AR is loadable. The fail-closed loader is
  a genuine strength. The risk is forward: if `HASH_BASIS_VALUES` is ever extended, the catalog will
  mint ARs with the new basis and the loader will fail-closed on them — index-present-but-unresolvable
  records with **no generation-time signal**, surfacing only when a reader calls
  `load_attachment_record_body`.
- **Minimum closure condition:** the catalog-supported basis/ref set is a single shared constant
  (or generation asserts membership), so an unsupported basis fails loud at `rebuild` rather than
  silently at load.
- **Next authorized action:** owner decision; bounded hardening optional.
- **Validation expectation:** a test asserting that an AR whose `hash_basis` is outside the
  catalog-supported set is rejected at generation (or covered by F5's load-time test).

### F3 — `attachment_records_path` / `by_source_surface_path` are surface-keyed but emitted beside family-scoped counts
- **Severity:** minor
- **Target:** `orca-harness/data_lake/catalog.py:361`–`379` (`_source_surface_summary` row build,
  esp. `:366`–`:372`), `:382`–`:391` (`_source_surface_bucket_path`,
  `_attachment_records_source_surface_path`), AR bucket keyed by `record.source_surface` at
  `:705`, `:735`; field-semantics notes `:33`–`:44`.
- **Evidence:** each summary row is keyed by `(source_family, source_surface)` and carries a
  family-scoped `packet_count` / `attachment_record_count`, but its `by_source_surface_path` and
  `attachment_records_path` are computed from `source_surface` **alone** and the underlying JSONL
  buckets group by surface alone. When two families share one `source_surface` string, both rows
  point to the same surface-wide file whose row count is the cross-family sum.
- **Authority/evidence basis:** prompt review-scope ("same-source-surface/different-family … handled
  honestly"; "expose … without implying … source-family completeness"). The `field_semantics` strings
  do document "the bucket may include multiple source families and consumers must still filter rows by
  source_family when needed," which mitigates retrieval correctness.
- **Concrete impact:** a consumer reading a row's `attachment_records_path` while trusting the
  adjacent family-scoped count would over-read (file has more rows than the row's count). Behavior is
  documented but the count-beside-path adjacency is a footgun, and **no test exercises the
  cross-family-same-surface case** (the multi-packet test reuses one family/surface).
- **Minimum closure condition:** the count adjacent to a surface-keyed path is itself surface-scoped
  or explicitly labeled family-scoped-while-file-is-surface-scoped; **and** a regression test asserts
  the documented multi-family mixing so the contract is locked.
- **Next authorized action:** owner decision; bounded doc/test hardening optional.
- **Validation expectation:** a test with two families sharing one `source_surface` asserts both rows
  reference the same surface file and that the file contains the union, with per-family counts intact.

### F4 — `payload_schema_version` carries the packet **manifest** version, not a body payload schema
- **Severity:** minor (naming/semantics honesty)
- **Target:** `orca-harness/data_lake/catalog.py:464`
  `"payload_schema_version": _string_or_none(manifest.get("manifest_version"))`.
- **Evidence:** the field is populated from `manifest_version` (`source_capture_packet_manifest_v1`,
  asserted by the test at `:298`). The AR contract Required Shape #1 lists "payload kind, payload
  schema version" as distinct keying facts describing the payload, not the manifest envelope.
- **Authority/evidence basis:** AR contract Required Shape #1; `source_capture/models.py:12`
  `SOURCE_CAPTURE_MANIFEST_VERSION`.
- **Concrete impact:** a downstream consumer may read `payload_schema_version` as a body-format
  version when it actually tracks the packet manifest schema. For opaque Bronze bodies there may be no
  payload schema version, so reusing the manifest version is a defensible stand-in, but the field name
  invites misread.
- **Minimum closure condition:** the field's meaning for Bronze is unambiguous — either documented in
  `field_semantics` as "mirrors the packet manifest version; not a body-format version," or sourced from
  a real payload-schema signal when one exists.
- **Next authorized action:** owner decision; doc-only clarification optional.
- **Validation expectation:** none beyond the existing equality assertion if documented; otherwise a
  field-semantics presence assertion.

### F5 — Three of four `load_attachment_record_body` fail-closed guards are untested
- **Severity:** minor (test coverage; bears on AR-02/AR-06)
- **Target:** loader guards `orca-harness/data_lake/catalog.py:773`–`:802` (unsupported
  `body_ref_kind`, unsupported `hash_basis`, manifest path mismatch, manifest/body sha256 mismatch);
  test coverage `orca-harness/tests/test_data_lake_catalog.py:314`–`:317`.
- **Evidence:** the only negative-path test mutates `body_ref_kind="sidecar_body"` and asserts a raise.
  The `hash_basis`, `relative_packet_path`-mismatch, and `body_sha256`-mismatch guards have no direct
  test. `test_catalog_runner_reports_corrupt_raw_verified_read_failure` (`:577`) exercises
  `load_raw_packet`'s own rebuild-time verification ("sha256 mismatch"), **not** these loader guards.
- **Authority/evidence basis:** prompt review-scope ("Does `load_attachment_record_body` fail closed
  on …"; "tests assert the behavioral contracts that would catch … raw resolver overtrust"); AR-06.
- **Concrete impact:** the resolver's fail-closed behavior — the core AR-02 guarantee that the index
  cannot silently return drifted bytes — is asserted for only one of four drift classes. A regression
  weakening any of the other three guards would pass CI.
- **Minimum closure condition:** focused tests mutate a generated AR's `hash_basis`,
  `relative_packet_path`, and `body_sha256` and assert each raises `DataLakeRootError`.
- **Next authorized action:** owner decision to authorize a bounded test-only patch.
- **Validation expectation:** the three new tests pass; the four guards are each exercised.

## Non-Findings Affirmatively Checked (residual risk noted)

- **Raw authority preserved (AR-02).** `rebuild_catalog` (`:105`–`:126`) builds entries via
  `load_raw_packet` (verified load) + `root._reverify()`, then `rmtree`s only the **generated**
  `_catalog_root` and rewrites it; raw packets are never written. `load_attachment_record_body`
  re-resolves through `load_raw_packet` (re-verifies size+sha per `root.py`) and additionally checks
  manifest path, manifest sha, and recomputed body sha against the AR. Solid.
- **Private field non-leak.** `_packet_index_entry` (`:404`) strips `_`-prefixed keys, so
  `_attachment_records` never reaches public `by_packet/*.json` or the inspect comparison; the public
  surface carries only `attachment_record_count` / `attachment_record_ids`. Verified at both write
  (`:275`) and compare (`:161`) sites.
- **`inspect_catalog` honesty incl. AR files.** `expected_snapshot` includes
  `_attachment_record_snapshot`, and `_read_snapshot` rglobs the whole catalog root, so
  missing/orphaned/stale detection covers AR files (tested at `:429`–`:457`). Read failures are
  surfaced, not swallowed (`:498`–`:523`).
- **Safe names collision-resistant.** `_safe_name` (`:872`) appends `sha256(value)[:16]`, so distinct
  surface/facet/payload strings cannot collide on a cleaned prefix; blank cleans to `blank__{digest}`.
- **Source-family-agnostic `payload_kind` (AR-04).** `_payload_kind` (`:526`) is a generic byte-shape
  classifier (json/html/text/binary); `field_semantics` states source-family semantic kinds "require a
  future registry and are not lake-core fields." Contract Required Shape #1 sanctions a generic
  "payload kind," so this is contract-permitted, not a hidden source-family field. Future-surface test
  (`:234`) and binary multi-file test (`:526`) pass.
- **Determinism.** Snapshots sort dict keys (`_json_bytes`) and bucket/jsonl rows; AR list is sorted by
  `attachment_record_id`. AR `by_packet`/`by_source_surface` row order within a `packet_id` tie relies
  on Python's stable sort over the id-presorted input — deterministic in practice but implicit; an
  explicit total-order key would be more robust (optional, not a finding).

## Validation Commands (independently rerun)

Run in the named target worktree `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-ar-mgt-90`
(`orca-harness/` cwd), whose three target files match `b85e2a3d` byte-for-byte (LF blob) and are
clean. Tests use `tmp_path` fixtures; no network, no live capture, no lake mutation.

| Command | Result | vs author |
| --- | --- | --- |
| `python -m py_compile data_lake/catalog.py tests/test_data_lake_catalog.py` | exit 0 | matches |
| `python -m pytest -p no:cacheprovider tests/test_data_lake_catalog.py` | `14 passed, 1 skipped` (2.69s) | matches `14 passed, 1 skipped` |
| `python -m pytest -p no:cacheprovider tests/test_data_lake_root.py tests/test_data_lake_catalog.py` | `46 passed, 2 skipped` (3.95s) | matches `46 passed, 2 skipped` |

- The 1/2 skips are the directory-symlink rebuild-rejection test (skips when symlink creation is
  unavailable on the platform).
- **Not independently rerun (author-supplied, not revalidated):** the retrieval-header / header-index /
  map-links / repo-map-freshness / staged-header hooks and `git diff --check`. These are repo-doc/CI
  hygiene gates outside the AR review object; the author reported all exit 0 with only CRLF warnings.
- **Not run by design:** live capture, public web research, live lake mutation, network source access,
  Cleaning/ECR/Judgment materialization, Silver/Gold migration, final AR storage migration.

## Intended Closure Check (AR-01 … AR-06)

| ID | Verdict | Basis |
| --- | --- | --- |
| AR-01 typed generated entries, stable ids, explicit field semantics | **closed** | `ar_`+`sha256[:32]` (not positional `file_id`, tested `:293`,`:556`); `_ATTACHMENT_RECORD_FIELD_SEMANTICS` documented. Residual: F1 delimiter (collision-resistance caveat for future string fields). |
| AR-02 raw authority preserved (resolve via verified manifests, no copy/mutate) | **closed** | verified-load resolution + four loader guards; raw never written. Residual: F5 (3 of 4 guards untested) lowers regression assurance, not the code behavior. |
| AR-03 coordination surface/packet → body without semantic folder names | **partially_closed** | `_safe_name` digesting + `stable_query_paths` work; F3 cross-family-same-surface count/path adjacency is a documented-but-untested footgun. Min closure: F3. |
| AR-04 future-lane adaptability, no source-family lake-core fields | **closed** | generic `payload_kind`; `field_semantics` defers source-family kinds to a future registry; future-surface + binary tests pass. |
| AR-05 honesty (not Manifest v2 / final physicalization / payload validation / currentness) | **closed** | `_ATTACHMENT_RECORD_COMPLETENESS` + `_SOURCE_SURFACE_COMPLETENESS` + manifest non-claims; repo-map hunk describes retrieval coverage only (no readiness/source-of-truth/Manifest-v2/body-copy claim). |
| AR-06 regression coverage (stale/missing files, resolver byte reads, bad refs, multi-file, future surfaces, summaries) | **partially_closed** | broad coverage present and passing; gaps: F5 (3 loader guards) and F3 (cross-family-same-surface). Min closure: F5 + F3 tests. |

## Open Questions / Residual Risk

- **F2 forward-coupling** is the highest-leverage residual: it is dormant only while
  `HASH_BASIS_VALUES`/`body_ref_kind` stay singletons. Owner should decide whether to fail-loud at
  generation now or accept the coupling with a code comment linking the two literals.
- **F5** leaves the AR-02 fail-closed contract under-tested; cheapest high-value hardening.
- The review did not exercise concurrent `rebuild_catalog` runs (rmtree → write is not atomic); a
  crash mid-write yields a partial catalog, but `inspect_catalog` detects it on next run and rebuild is
  idempotent. Acceptable for a rebuildable generated index; named as residual, not a finding.

## Review-Use Boundary

These findings are decision input only. They are **not** approval, validation, mandatory remediation,
readiness, a formal Orca verdict, or executor-ready patch authority, and no `patch_queue_entry` is
emitted. This was a read-only advisory cross-vendor implementation/code review; no source file was
edited. Severity labels (`blocker`/`major`/`minor`) are finding-priority only. Any patch — including
the test-only closure for F5 — requires separate Chief Architect acceptance/authorization. Per the
review-adjudication tail (`communication-style.md` → Review Adjudication Next Step), the commissioning
CA should, after adjudicating these findings, batch admin/lifecycle follow-ups (commit/push/PR/merge)
into one no-deep-thinking land step and deep-think only the material moves (here: F2 co-evolution
decision and the F5 test-coverage patch).
