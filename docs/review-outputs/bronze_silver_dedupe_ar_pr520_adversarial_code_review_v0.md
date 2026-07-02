# Bronze Silver Dedupe AR PR520 Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (advisory implementation/code review)
reviewed_by: anthropic-claude-opus-4-8 (delegated controller; dispatched by operator)
authored_by: openai-gpt-5-codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable
review_lane: code (workflow-code-review; findings-first advisory)
review_prompt: docs/prompts/reviews/bronze_silver_dedupe_ar_pr520_adversarial_code_review_prompt_v0.md
pr: https://github.com/eric-foo/orca/pull/520
implementation_target_range: eb29555ae771821d2c9581f4e8ca17061bb229ef..1cacaa6e96a855e02fe80d0f48d2b8d1e86d6100
recommendation: accept_with_friction
authority_boundary: retrieval_only
review_use_boundary: >
  Findings are decision input only. They are not approval, validation, mandatory
  remediation, readiness, merge authorization, or executor-ready patch authority
  until the Chief Architect separately accepts or authorizes them. No source
  files were edited; no commit/push/merge/lake mutation was performed.
```

## De-correlation Receipt

- Author / home model family: **OpenAI/Codex** (`openai-gpt-5-codex`), per the prompt Lane Binding.
- Reviewing controller: **Anthropic Claude (`claude-opus-4-8`)**, dispatched by the operator.
- Different upstream vendor lineage (Anthropic vs OpenAI) ⇒ **`cross_vendor_discovery`** bar is satisfiable.
- Tester/testee separation honored: the reviewer did not review its own authored work and launched no replacement controller. Review performed in this lane against the pinned worktree source.

## Hash-Pin / Target Verification

Target worktree: `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-silver-dedupe-ar` (branch `codex/bronze-silver-dedupe-ar`).

- Worktree HEAD: `e5b43b4c` (`Add PR 520 delegated review prompt`). The only commit after the implementation pin `1cacaa6e` is a **prompt-only carrier** (1 file, `docs/prompts/reviews/...prompt_v0.md`, +415). It touches **none** of the five implementation target files. `1cacaa6e` is an ancestor of HEAD.
- All five target-file SHA256 pins **MATCH** at the worktree:
  - `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py` MATCH
  - `orca-harness/data_lake/catalog.py` MATCH
  - `orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py` MATCH
  - `orca-harness/tests/test_data_lake_catalog.py` MATCH
  - `orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py` MATCH
- No `HASH_MISMATCH`. Reviewed the pinned implementation target range as instructed.

## Source-Read Ledger

Read in place at the pinned worktree:

- Prompt: `docs/prompts/reviews/bronze_silver_dedupe_ar_pr520_adversarial_code_review_prompt_v0.md`
- Diff: `git diff eb29555..1cacaa6e -- <5 target files>` (534-line patch; +261/-16, matches readback)
- `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py` (full)
- `orca-harness/data_lake/catalog.py` (constants 19-31; AR build 740-869; query row + `load_attachment_record_body` 1150-1239)
- `orca-harness/data_lake/root.py` (full — shard grammar, `append_record`, `resolve`, `for_test`, `load_raw_packet`)
- `orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py` (full)
- `orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py` (full)
- `orca-harness/tests/test_data_lake_catalog.py` (diff hunks + AR assertions 346-415)
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` (full)
- Repo-wide greps for stale `bronze_*_schema_1` strings and other consumers of the changed AR fields/constants
- AGENTS.md authority + MGT doctrine summary already in working context (capability-target lens, owner-invoked, names residuals)

Not loaded (not needed for the findings): Silver Vault / derived-layout-rebuild / Gold-readiness contracts in full, `ig_reels_grid_projection.py` body (lane-constant single-segment property confirmed via `_validate_segment` in `root.py`), live lake data, bulk review outputs.

## SOURCE_CONTEXT_READY

`SOURCE_CONTEXT_READY`. No missing load-bearing source, no unresolved tool gap. `workflow-code-review` / `workflow-deep-thinking` applied as findings-first advisory method (no strict Orca review-lane verdict authority claimed). Repo execution was available and used (see Validation).

---

## Findings

No blocker and no major correctness finding. The change is careful, fail-closed,
and the central claims hold under inspection and execution. Findings are minor /
advisory and cluster on **test-durability gaps** and one **undocumented implicit
coupling** in the local drill-back pointer.

### AR-F1 (minor) — Runner `--from-lake`/`--data-root`/`--projection` mode logic has no automated test

- File: `orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py:86-98`
- Evidence: The three new mode guards (`--from-lake` + `--projection` conflict; `--data-root` requires `--from-lake`; neither provided) and the `--from-lake` discovery branch are new behavior. A repo-wide grep for any test importing this runner module returns **none** (only `run_source_capture_packet` and `run_source_capture_ig_reels_grid_packet` have runner tests). Author evidence for this surface is `--help` exit 0 only.
- Authority/basis: Prompt review scope #4 and closure item `test_durability_01` ("tests would catch ... runner-mode misuse").
- Impact: The logic is **correct** (I confirmed all three guards fire with exit 2 and the exact messages, and `--help` advertises both flags — see Validation). But there is **no regression guard**: a future edit that drops a guard, flips `--data-root`'s dependency, or breaks the discovery wiring would pass CI silently.
- Minimum closure: add a unit test importing `main([...])` that asserts (a) each invalid combo exits non-zero, (b) `--from-lake` resolves and feeds discovered paths, (c) explicit `--projection` still works.
- Next authorized action: home model decides whether to require the test before merge or accept as a tracked follow-up.
- Validation expectation: new test green; full `orca-harness/tests` stays green with `ORCA_DATA_ROOT` unset.

### AR-F2 (minor) — `_source_packet_pointer` silently assumes `projection.packet_id == derived raw_anchor`

- File: `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py:421-430`
- Evidence: The sharded-vs-flat discriminator is `len(after_derived) >= 4 and after_derived[0] == anchor_shard(packet_id)`, where `packet_id` is the projection **document's** `packet_id` field and `after_derived[0]` is the path's shard segment = `anchor_shard(raw_anchor)` chosen at `append_record` time (`root.py:573`). Correctness therefore requires `anchor_shard(raw_anchor) == anchor_shard(packet_id)`, i.e. effectively `raw_anchor == packet_id`. This invariant is real for today's single-anchor IG reels projections but is neither documented nor asserted.
- Authority/basis: prompt review scope #3; closure `silver_dedupe_03`.
- Impact: **Low / contained.** If a projection is ever anchored under a `raw_anchor` different from its own `packet_id` (multi-anchor derivation) or the lake is mid-migration (derived sharded but raw still flat, or vice-versa), the discriminator misfires and the pointer falls back to a **wrong** local path. This is tolerable because the field is explicitly the "optional local-only drill-back pointer ... not portable provenance" (`instagram_metric_seed.py:150-160`) and the load-bearing provenance (`source_packet_id_or_none`, `raw_anchor`) is carried separately per row. So this is a wrong *convenience* pointer, not a provenance-integrity defect. Note the shard function is shared (`raw_shard == anchor_shard == _sha256_hex_shard`, `root.py:91-103`), so a 3-hex shard *collision* is harmless — the returned raw pointer is always recomputed from `packet_id` and stays correct; only the `raw_anchor != packet_id` case is wrong.
- Minimum closure: document the `raw_anchor == packet_id` assumption at the function (or derive the pointer from the path's own shard segment instead of recomputing from `packet_id`, so a sharded path always yields a sharded raw pointer regardless of the coupling).
- Next authorized action: advisory; home model may fold a one-line doc/assertion into a follow-up.
- Validation expectation: behavior unchanged for the consistent-layout case; an added assertion would fail loud on a divergent anchor.

### AR-F3 (minor, test gap) — legacy-flat drill-back pointer branch is unasserted

- File under test: `instagram_metric_seed.py:430` (`return str(root / "raw" / packet_id)`); test `orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py:286-288`
- Evidence: The new mixed-layout test selects the **sharded** `strong` projection, so the only `source_packet_pointer_or_none` assertion exercises the **sharded** branch (`root/raw/raw_shard/packet_id`). The legacy-flat branch (`len(after_derived) < 4` ⇒ `root/raw/packet_id`) is never asserted; the pre-existing builder tests use tmp paths with no `derived/` segment, so they hit the `None` branch only.
- Authority/basis: closure `silver_dedupe_03`, `test_durability_01`.
- Impact: a regression that breaks the flat-pointer branch (or the flat-vs-sharded discrimination) would not be caught by the suite.
- Minimum closure: extend the test (or add one) to select a legacy-flat projection and assert the flat raw pointer, ideally alongside a divergent-anchor case for AR-F2.
- Next authorized action: advisory follow-up test.
- Validation expectation: added assertion green.

### AR-F4 (advisory) — discovery is a full unfiltered `derived/` scan with re-reads; lane trust is positional

- File: `instagram_metric_seed.py:433-457` (`_iter_...`, `_json_files`), `:38-44` (dedupe re-read)
- Evidence: `--from-lake` walks every top-level entry under `derived/` and, per entry, every child, statting `<entry>/<lane>` and `<entry>/<child>/<lane>` (handles both flat and sharded). Every `.json` in the IG-reels-grid lane is read for sha256 in discovery, then re-read by `_projection_summary` (`load_json` text read + a second `read_bytes` for sha256) — ~3 reads per selected file. Any `.json` physically present in that lane dir is treated as a projection (no marker/`is_record_set_complete` awareness; safe today because the lane carries only single `append_record` projections and completion markers live in a separate `completion_lane`, `root.py:577-653`).
- Authority/basis: prompt review scope #1; design note on dedupe boundary.
- Impact: O(all derived anchors) per run and 3× file reads — acceptable for the v4.1 local single-operator scale, but a latent scalability residual. A stray non-projection `.json` mistakenly written into the lane would fail the build loudly (`_projection_summary` raises) rather than corrupt output — fail-closed, which is the desired direction.
- Minimum closure: none required for current scope; if the lake grows, consider scanning by known anchors / availability index rather than a full tree walk, and a single read per file.
- Next authorized action: note as an accepted residual; no change needed for merge.

### AR-F5 (advisory) — `source_projection_files_supplied` reports post-dedupe count, not on-disk file count

- File: `instagram_metric_seed.py:147` → `_counts` `:395-418`; test assertion `test_..._dedupes_exact_duplicates:283`
- Evidence: discovery dedupes 3 on-disk files (weak sharded + weak legacy + strong) to 2 paths; `source_projection_files_supplied == 2`. The count honestly reflects what entered the builder, but an operator reading "2" while 3 files exist on disk may be surprised.
- Impact: cosmetic transparency only; defensible (byte-identical files are not distinct inputs, and the dedupe rule is documented at `:32-37` and `:135-138`).
- Minimum closure: optional — surface a `*_discovered` vs `*_deduped` breakdown if operator transparency is wanted. Not a defect.

---

## Intended Closure Check

- `silver_dedupe_01` (lake-native discovery across flat + sharded `derived/`): **closed.** `_iter_...` (`:433-448`) correctly probes both depths, scoped to `PROJECTION_IG_REELS_GRID_LANE` (a single safe segment, enforced by `_validate_segment`), with deterministic sorting. The mixed-layout test exercises both layouts and passes (verified by execution). No unrelated JSON is admitted outside the lane dir.
- `silver_dedupe_02` (exact dedupe without weakening semantic per-username selection): **closed.** Dedupe is exact-content SHA-256 with a deterministic lexical tie-break (`:38-44`); semantic `(observed_count, capture_time, path)` selection stays in the builder (`_select_projection_per_username` `:210-227`). Identical bytes ⇒ identical `packet_id`/`capture_time`, so no current-vs-stale or cross-source distinction can be hidden by exact dedupe. Test confirms supplied=2 / selected=1 with the stronger projection chosen.
- `silver_dedupe_03` (sharded drill-back correct where layout proves v4.1; legacy preserved): **partially_closed.** Sharded derivation is correct and asserted; legacy flat is preserved by construction. Residual: undocumented `raw_anchor == packet_id` coupling (AR-F2) and the unasserted flat-pointer branch (AR-F3). Both low-impact because the pointer is explicitly local-only/non-portable.
- `ar_mgt_01` (typed manifest-equivalent entries, not positional `file_id`): **closed.** `attachment_record_id` is `ar_<sha256[:32]>` over `[packet_id,file_id,relative_packet_path,body_sha256]` (`catalog.py:843-851`), explicitly "not the positional file_id"; structured `body_ref` repeats the keys so consumers do not inherit positional `file_id`. Test asserts `id != file_id` and exact `body_ref`.
- `ar_mgt_02` (enough replay/version/body-ref to resolve+verify without source-family interpretation): **closed.** `payload_schema_version`, `replay_version_pins`, and structured `body_ref` map directly onto the AR contract's Required Shape item 1 ("payload schema version, replay/version pins, attachment reference, hash, hash_basis"). `load_attachment_record_body` (`:1162-1214`) verifies `body_ref` internal consistency then re-hashes the raw body fail-closed. New fields are **generated catalog read state** (under `indexes/derived_retrieval`, `authority = generated_from_raw_packet_manifests; raw remains authoritative`), not new lake-core/raw-manifest fields — satisfying the contract's no-new-core-field rule (acceptance check 6). `source_capture/models.py` is untouched.
- `ar_mgt_03` (residuals explicit): **closed.** `_ATTACHMENT_RECORD_COMPLETENESS` (`:96-101`) states physicalized manifest-equivalent ARs over preserved raw packet bodies, body remains a hash-checked raw packet member "not a copied attachments/ body", "not Manifest v2, not source-family payload validation, and not downstream currentness". This stays inside the AR contract's accepted shape #3 and names the same residuals. No Gold/Judgment/cleaning/currentness semantics leak into the rows.
- `test_durability_01` (tests catch the main regressions): **partially_closed.** Strong coverage exists for AR fields, `body_ref` mismatch / path / sha / hash_basis error paths, the physicalization tag, replay pins, and mixed-layout discovery + exact dedupe + sharded pointer. Gaps: no runner-mode test (AR-F1) and no legacy-flat-pointer assertion (AR-F3). The schema bump (`_schema_1` → `_schema_2`, both catalog and AR) is explicit and additive; a repo-wide grep found **no** stale `_schema_1` references outside `catalog.py`/its test, and no other consumer reads the new fields in a way that breaks (`load_attachment_record_body` treats `body_ref` as optional for backward compatibility).

## Open Questions / Residual Risk

1. Is `raw_anchor == packet_id` a guaranteed invariant for every IG-reels-grid projection writer, now and planned (AR-F2)? If multi-anchor projections are foreseeable, prefer path-derived sharding over `packet_id`-recomputed sharding.
2. Mixed-epoch lakes (derived sharded but raw still flat, or the reverse) are not exercised; the drill-back pointer can be wrong there. Acceptable only while the pointer stays explicitly local-only/non-portable.
3. Runner-mode and flat-pointer regressions are currently caught only by human review, not tests (AR-F1, AR-F3).

## Validation Commands

Run independently by the reviewer (repo execution available; `ORCA_DATA_ROOT` cleared for the process, matching the author's clean-run method):

- `python -m pytest -q orca-harness\tests\unit\test_instagram_reels_creator_metric_seed.py orca-harness\tests\test_data_lake_catalog.py` → **exit 0** (passes; 1 skip). Independently revalidated.
- Runner mode guards by direct execution (no automated test exists):
  - `--from-lake --projection foo.json --check` → exit 2, "--from-lake cannot be combined with explicit --projection files"
  - `--data-root <p> --check` → exit 2, "--data-root requires --from-lake"
  - `--check` (neither) → exit 2, "provide at least one --projection or use --from-lake"
  - `--help` → exit 0, advertises `--from-lake` and `--data-root`
- Hash-pin verification on all five target files → all MATCH.
- Repo-wide grep for stale `bronze_*_schema_1` / new-field consumers → no stale references; changes contained.

Author-supplied, **not** independently re-run by the reviewer (reported as such):

- `test_data_lake_sharding.py`, `test_data_lake_rebuild_proof.py`, `test_ig_reels_behavioral_lake.py` focused runs.
- Full `orca-harness/tests` (author: exit 0 with `ORCA_DATA_ROOT` unset; a prior run with the operator-local `ORCA_DATA_ROOT` set failed two environment-sensitive live-root checks — environment-sensitive, not an implementation pass/fail).

Not run (out of bounds per prompt): live capture, public web research, live lake mutation, Cleaning/ECR/Judgment materialization, Silver/Gold migration, final AR body-copy migration.

## Recommendation

**`accept_with_friction`.** No blocker or major correctness defect; the Silver
discovery/dedupe/pointer and the Bronze AR physicalization both do what they
claim, the residuals are named honestly, and the schema bump is explicit and
contained. The friction is test-durability: before (or shortly after) merge, add
a runner-mode unit test (AR-F1) and a legacy-flat-pointer assertion (AR-F3), and
document the `raw_anchor == packet_id` coupling (AR-F2). These are decision input
for the Chief Architect, not merge gates set by this review.

Review findings are decision input only; they are not approval, validation,
mandatory remediation, readiness, merge authorization, or executor-ready patch
authority until the Chief Architect separately accepts or authorizes them.
