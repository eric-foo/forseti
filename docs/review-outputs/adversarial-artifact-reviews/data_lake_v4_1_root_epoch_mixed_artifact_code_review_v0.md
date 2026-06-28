# Data Lake v4.1 Root Epoch Mixed Artifact + Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Read-only delegated mixed review of PR #421 (DataLakeRoot v4.1 runtime
  migration): implementation/code correctness plus consistency with the v4.1
  forward-epoch data-lake contract, the Silver Vault record/read-model contract,
  and the physicality/location contract. Decision input for CA adjudication only.
use_when:
  - Adjudicating whether PR #421 should proceed, be patched, or be redesigned.
  - Checking whether DataLakeRoot v4.1 epoch enforcement faithfully implements the
    accepted v4.1 data-lake doctrine.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/data_lake_v4_1_root_epoch_mixed_artifact_code_review_prompt_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - orca-harness/data_lake/root.py
stale_if:
  - PR #421 head commit, base commit, branch state, or target worktree dirty state changes.
  - DataLakeRoot, the v4.1 forward-epoch contract, the Silver Vault record contract,
    or the data-lake root tests change.
```

## Review Provenance

```yaml
reviewed_by: claude-opus-4.8        # reviewer self-reported; CA/tooling may overwrite with the durable-record value
authored_by: unrecorded             # PR #421 author model/version not supplied; not fabricated
de_correlation_bar: unrecorded      # see note
de_correlation_note: >
  Reviewer is Claude (Opus 4.8), a cross-vendor reviewer relative to a GPT/OpenAI
  author. The repo branch-prefix convention (`codex/` vs `claude/`) suggests a
  likely OpenAI/Codex authoring lane for PR #421; IF the operator/CA confirms a
  non-Claude (OpenAI/Codex) author, this review meets the cross_vendor_discovery
  bar. Not self-asserted; provenance was not operator-supplied, so recorded
  `unrecorded` per review-lanes.md.
review_date: 2026-06-28
```

## Commission

Read-only delegated mixed review (implementation/code + artifact-consistency) of
**PR #421**, commissioned by the prompt
`docs/prompts/reviews/data_lake_v4_1_root_epoch_mixed_artifact_code_review_prompt_v0.md`.
This is **not** a delegated review-and-patch commission: no patch was applied; no
`patch_queue_entry` is emitted (per `.agents/workflow-overlay/review-lanes.md`).

## Target

- PR #421, branch `codex/data-lake-v4-1-runtime-migration` @ `aa9f7f245a684ab1ac9ad859880a5652fdb8036d`.
- Base `origin/main` @ `d4e6705b2394955c29efec11a7a2c17ddf3e9fe8`.
- Target worktree `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\data-lake-v4-1-runtime-migration`.
- Diff = exactly the 4 declared files (133 additions, 13 deletions):
  `orca-harness/data_lake/__init__.py`, `orca-harness/data_lake/root.py`,
  `orca-harness/tests/test_data_lake_root.py`,
  `orca-harness/tests/test_data_lake_rebuild_proof.py`.

**Source-context gate:** PASS. Target worktree verified clean at the pinned HEAD;
branch, HEAD, and base merge-base all match the prompt's expected values; diff
matches the declared target files. Not `SOURCE_CONTEXT_INCOMPLETE`.

## Authority

- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md` (controlling: v4.1 grammar, markers, old-root handling).
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` (controlling: derived/ record shape, generated read-model grammar).
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md` (controlling: location invariants, indexes rebuildable/non-authoritative).
- Overlay: `review-lanes.md`, `validation-gates.md`, `prompt-orchestration.md`, `source-loading.md`, `decision-routing.md`, `README.md`, `AGENTS.md`, `orca_prompt_behavior_contract_v0.md` (lane, gates, output, provenance).

Method: `workflow-deep-thinking` + `workflow-code-review` (implementation) +
`workflow-adversarial-artifact-review` lens (code↔contract consistency only,
not full data-lake architecture review) — all reference-loaded before source load,
applied after `SOURCE_CONTEXT_READY`.

## Decision Criteria (Fitness Reference)

The bound fitness reference is the three controlling contracts plus the prompt's
three fitness questions (answered below). Per `review-lanes.md`, the fitness
reference is an alignment axis the review must also attack, not a pass-if-matches
bar. Attack on the reference itself: the three questions emphasize root/init-time
creation and v0 rejection; they under-weight the *after-resolution* durability of
epoch enforcement (marker deleted/corrupted between `resolve()` and a later write).
The implementation actually handles that well (`_reverify` re-reads the epoch
marker every write session), but the test suite's coverage of it is thin (see
AR-01). No `no checkable success bar bound` gap exists — the contracts are the
bound reference.

## Source-Read Ledger

All sources read from the pinned target worktree (`data-lake-v4-1-runtime-migration`)
unless noted; all clean at HEAD `aa9f7f24`.

| Source | Why read | Supports | Status |
| --- | --- | --- | --- |
| `git status/rev-parse/diff` (target wt) | Verify pinned state | Source-context gate | clean, matches expected |
| `orca-harness/data_lake/root.py` (full) | Implementation under review | All findings, Q1–Q3 | clean |
| `orca-harness/data_lake/__init__.py` (full) | Package-surface check | Q2, check #12 | clean |
| `orca-harness/tests/test_data_lake_root.py` (full) | Test strength | AR-01, Q3, checks #13 | clean |
| `orca-harness/tests/test_data_lake_rebuild_proof.py` (full) | Rebuild proof | check #8, Q2/Q3 | clean |
| v4.1 forward-epoch contract (full) | Controlling grammar/markers | Q1, Q2, checks #1,#3,#9,#10,#15 | clean |
| Silver Vault record contract (full) | Read-model boundary | check #7,#14; R1 | clean |
| physicality/location contract (full) | Location invariants | check #6, #7; R2 | clean |
| overlay: review-lanes, validation-gates, prompt-orchestration, source-loading, decision-routing, README, behavior-contract | Lane/gate/output/provenance binding | verdict, validation buckets, provenance | clean |
| `AGENTS.md` | Kernel | absence-evidence discipline | clean (session-supplied, same repo) |
| `tests/` grep for epoch-value coverage | Confirm AR-01 absence claim against primary source | AR-01 | clean |

No source was dirty or unanchored. Source pack: custom PR #421 mixed-review pack
as named by the prompt; not widened (no unrelated review outputs, prompts, PR #422
runner work, or live data-lake contents loaded).

---

## Findings (severity-ordered)

No `critical` findings. One `major`, one `minor`.

### AR-01 (major) — Epoch-marker value-rejection branches are untested (regression-coverage gap on the core new enforcement)

- **phase:** correctness (code review)
- **reviewed target:** `orca-harness/data_lake/root.py` `_read_epoch_marker`; `orca-harness/tests/test_data_lake_root.py`
- **location:** `root.py:172-197` (`_read_epoch_marker`); tests at `test_data_lake_root.py:91-129`
- **issue:** `_read_epoch_marker` fails closed on five conditions: missing marker
  (`root.py:174`), wrong `lake_epoch` (`:184`), wrong `epoch_policy` (`:188`),
  `compatibility_migration is not False` (`:193`), and non-list `legacy_roots`
  (`:195`). Only the **missing-marker** branch is exercised by a test
  (`test_resolve_missing_epoch_marker_rejected`, `test_data_lake_root.py:114-118`).
  The four **value-rejection** branches have no test.
- **evidence:** The only epoch-value assertions in the entire `tests/` tree are
  positive write-path checks on a freshly-written marker
  (`test_data_lake_root.py:99-102` assert `lake_epoch`/`epoch_policy`/
  `compatibility_migration`/`legacy_roots` equal the expected constants; `:111`
  asserts `legacy_roots` recorded). Confirmed against the primary source by
  `grep -rIn -E "lake_epoch|epoch_policy|compatibility_migration|legacy_roots"
  orca-harness/tests/` — every hit is in `test_data_lake_root.py:99-111` (positive
  write-path); no test feeds a *malformed* epoch marker and asserts rejection.
- **strongest defense, and why it does not fully hold:** "missing-epoch and v0 are
  tested, and the write path is asserted." True, but the write-path assertions only
  prove the writer emits correct values; they do not prove the reader *rejects*
  wrong values. A regression that, e.g., weakened `:193` to accept
  `compatibility_migration: true`, or `:184` to accept a stale `lake_epoch`, would
  leave the suite fully green while admitting a non-clean-forward root — defeating
  owner decision #1 ("clean forward epoch, not compatibility migration"). The
  defense covers the enumerated failure modes but not the value branches.
- **impact:** The central new v4.1 safety mechanism (epoch-value enforcement) has
  no regression guard. This is precisely the prompt's riskiest assumption — "tests
  pass while still under-enforcing the clean epoch." Current behavior is correct
  (verified by source read and by the green run); this is a coverage gap, **not a
  live behavior defect**.
- **minimum_closure_condition:** A test exists that, for a constructed v4.1 root,
  mutates the epoch marker on each of the four value dimensions (wrong `lake_epoch`;
  wrong `epoch_policy`; `compatibility_migration` true/missing; `legacy_roots`
  non-list) and asserts `resolve()`/`initialize()` raises `DataLakeRootError` for
  each — and that test fails against the unfixed read path for at least the
  weakened-branch case (red-green).
- **next_authorized_action:** CA decides whether to require the added tests
  pre-merge (→ `PATCH_BEFORE_KEEP`) or accept as a fast-follow under
  `ACCEPTABLE_FOR_CA_ADJUDICATION`.
- **advisory remediation direction (not executor-ready):** add four small
  `pytest.raises(DataLakeRootError)` cases mirroring `test_resolve_legacy_v0_marker_rejected`'s
  shape but mutating the epoch marker rather than the root marker. No
  `patch_queue_entry` (read-only lane).
- **red-green proof status:** not run by this review (read-only; would require
  authoring the test). Recommended as same-check red-green when the test is added.

### AR-02 (minor) — Unreachable epoch-presence guard can misattribute the enforcement point

- **phase:** correctness (code review)
- **reviewed target:** `orca-harness/data_lake/root.py` `_init_at`
- **location:** `root.py:465-466`
- **issue:** `if marker.is_file() and not epoch_marker.is_file(): raise ...` can
  never fire. Every branch that leaves `marker.is_file()` true also guarantees the
  epoch marker exists: the `marker.is_file()` branch (`:451-453`) calls
  `_read_epoch_marker`, which raises on absence; the empty-dir branch (`:458-460`)
  and the new-dir branch (`:461-464`) both `_write_epoch_marker`. So at `:465`
  either we already raised or `epoch_marker.is_file()` is true.
- **strongest defense:** defense-in-depth — if a future refactor drops the
  `_read_epoch_marker` call at `:453`, this guard would catch it. Partly holds,
  which is why this is `minor`, not removed-on-sight.
- **impact:** Low. Harmless, but it can mislead a maintainer into reading `:465-466`
  as the epoch-enforcement point, when actual enforcement is `_read_epoch_marker`
  at `__init__` (`:352`), `_init_at` (`:453`), and `_reverify` (`:482`).
- **minimum_closure_condition:** either a one-line comment marking it as
  unreachable belt-and-suspenders (naming the real enforcement points), or a test
  demonstrating a reachable path, or removal.
- **next_authorized_action:** advisory only; owner/CA decision. No blocker.

---

## Answers to the Three Fitness Questions

**Q1 — Does PR #421 enforce the v4.1 root/epoch contract at the right runtime
boundary without embedding stale bronze/silver/gold or compatibility-migration
semantics?**
**Yes.** Enforcement sits at construction (`__init__` reads both markers,
`root.py:351-352`), at init (`_init_at` writes/verifies both, `:446-466`), and
before every write session (`_reverify` re-reads the epoch marker, `:482`).
`resolve()` returns `cls(...)`, so a bad root never yields a usable object: a v0
root is rejected by `_read_marker`'s `contract_version` check (`:150-156`) and a
missing/malformed epoch marker by `__init__ → _read_epoch_marker`. No
`bronze/silver/gold` folders are introduced (`LAKE_SUBDIRECTORIES`, `:55-68`,
matches the contract's "no gold/ folder"). `compatibility_migration` is forced to
exactly `False` on read (`:193`, identity check). `legacy_roots` is annotation-only
(written `:204`, validated as a list `:195`, never consumed for behavior) — recorded
without migration semantics (check #10 ✓). Boundary is correct: the root/foundation
class is exactly where epoch identity belongs, ahead of any reachable write path
(check #1, #2 ✓).

**Q2 — Does the implementation faithfully create and verify the root marker, epoch
marker, staging slot, sharded raw/derived behavior, availability/retrieval split,
and Silver Vault generated-folder skeleton required by the contracts?**
**Yes, with the AR-01 test caveat.** Root-marker fields match the v4.1 contract
(`contract_version` "v4.1" `:45`; default label "orca-canonical-v4-1" `:46,:164`;
`root_uuid`; `created_at`). Epoch-marker fields match (`lake_epoch` "v4.1",
`epoch_policy` "clean_forward_epoch", `legacy_roots`, `compatibility_migration`
false; `:200-210`). `.staging` is in the skeleton (`:56`) per the grammar. Sharded
`raw/<packet_shard>/<packet_id>/` and `derived/<anchor_shard>/<raw_anchor>/<lane>/<record_id>`
behavior is **unchanged** by the diff (no regression to flat layout; check #6 ✓).
`indexes/availability` vs `indexes/derived_retrieval` split preserved. The six
Silver Vault homes (`:62-67`) match the record contract's Generated Read Models
grammar (record contract `:372-382`) **exactly**, and the v4.1 contract grammar
(`:108-119`). Creation is verified by `test_initialize_creates_skeleton_and_marker`
(iterates all of `LAKE_SUBDIRECTORIES`, `test_data_lake_root.py:91-102`) and the
production-path `initialize` test (`:105-111`). Caveat: marker-value *rejection* is
under-tested (AR-01).

**Q3 — Do the tests meaningfully catch missing epoch markers, old v0 markers,
root-identity swaps, generated retrieval directory assumptions, and old-root
acceptance regressions?**
**Mostly yes — every enumerated failure mode is covered; one adjacent gap (AR-01).**
Missing epoch marker → `test_resolve_missing_epoch_marker_rejected` (`:114-118`).
Old v0 markers → `test_resolve_legacy_v0_marker_rejected` (`:121-129`). Root-identity
swap → `test_reverify_catches_root_identity_change` (`:295-310`), **notably
de-masked**: the updated test preserves `contract_version: v4.1` and mutates only
`root_uuid` (`:299-304`), so the identity check (`root.py:480`) is what fires —
previously (per the diff) the test wrote a `v0` marker, which the new code would
reject on `contract_version` *before* the identity comparison, passing for the wrong
reason. This directly closes check #13's "marker identity changes masked by
contract-version failures." Generated-retrieval-dir-as-file →
`test_indexes_rebuild_byte_identical_from_authoritative_truth` (`:33-56`): the
`not any(p.is_file() ...)` guard (`:45`) allows the empty skeleton but forbids
files, and the `after == before` byte-identity check (`:56`) — over a `_snapshot`
that filters to `p.is_file()` (`:29`) — would fail if a non-rebuildable file were
smuggled in (check #8 ✓). Old-root acceptance regression → v0 rejection above.
The gap (AR-01) is the malformed-epoch-*value* branches, outside the enumerated
list but a legitimate adversarial coverage gap on the core enforcement.

### Disposition of the prompt's 15 review checks (compact)

1 ✓ (rejects v0/missing/malformed epoch; compat-migration forced false). 2 ✓
(`resolve()` fails closed via `__init__` before any object returns). 3 ✓ (marker
pair + skeleton incl. `.staging` + silver_vault homes). 4 ✓ (`for_test` still writes
both v4.1 markers `:435,:459-464`; no production fallback —
`test_test_root_is_never_a_production_fallback`). 5 ✓ (`_reverify` catches identity
swap and epoch loss/mutation, `:480-482`). 6 ✓ (sharding untouched). 7 ✓
(silver_vault homes empty; non-authoritative; rebuild proof). 8 ✓ (empty skeleton
allowed, files forbidden). 9 ✓ (all marker defaults match the contract exactly).
10 ✓ (`legacy_roots` annotation-only). 11 ✓ (v0 error says "Archive or abandon the
legacy root and initialize a clean v4.1 root", `root.py:151-156`). 12 ✓ (`__init__.py`
re-exports 4 new module-level string constants; all resolve in `root.py:45-49`; no
circular import / package-surface risk; import verified by the green test run).
13 ✓ (with AR-01 caveat for malformed-epoch values). 14 — see R1 (no harmful
overfit: code stops at the contract-named generic homes, bakes in no platform
names). 15 ✓ (no live-root archive/cutover logic; no `F:\orca-data-lake` write;
no migration/cutover-completion claim — see R2).

## Validation Commands Run + Observed Output

Buckets per `.agents/workflow-overlay/validation-gates.md`. All runs used the
target worktree's `orca-harness`, with **`ORCA_DATA_ROOT` unset in the subprocess**
(ambient value was the live `F:\orca-data-lake`) and a basetemp under the session
scratchpad — no live-root write, no `F:\orca-data-lake` mutation, no live capture.

- **GATE PASS** — `python -m pytest -p no:cacheprovider --basetemp <scratch>
  tests/test_data_lake_root.py tests/test_data_lake_sharding.py
  tests/test_data_lake_availability.py tests/test_data_lake_read_loader.py
  tests/test_data_lake_rebuild_proof.py` → observed `56 passed, 1 skipped in 2.57s`
  (exit 0). **Independently reproduces the implementer-reported `56 passed, 1
  skipped`.** The four key changed tests also pass by name (4 passed).
- **GATE PASS** — `git diff --check origin/main...HEAD` → no whitespace/conflict
  errors (observed).
- **INFO** — the 1 skipped test is `test_within_rejects_symlinked_component`
  (`test_data_lake_root.py:325`): "symlinks not supported in this environment"
  (Windows without symlink privilege). Pre-existing and environmental; not a PR #421
  change. Consequence: the DL-003 symlink-rejection guard is not exercised in this
  environment (see R3).
- **INFO (corroborated transitively)** — the implementer's
  `python -c "compile(...)"` syntax check was not separately rerun; pytest
  successfully imported and ran all four changed modules, which is stronger evidence
  than a bare compile and corroborates it.
- **OUT OF SCOPE** — GitHub Actions `orca-harness-tests` (implementer-reported pass
  in 1m24s): not independently observed by this review (no CI access used). Owning
  surface: CI on PR #421. Labeled implementer-reported, not verified here.

## Residual Risk

- **R1 — Foundation↔read-model coupling (answer to check #14).** `LAKE_SUBDIRECTORIES`
  hard-codes the Silver Vault read-model subtree. This is *faithful* to the v4.1
  grammar (acceptance criterion #1: "a new v4.1 root can be initialized with the
  canonical folder grammar") and creates only **empty homes** (no authority; the
  rebuild proof confirms no files). No harmful overfit: the code stops at the
  contract-named generic homes and bakes in no platform/account names. But it
  couples the root/foundation module to a downstream read-model lane's internal
  folder shape, which the record contract's `stale_if` (`:31-32`) contemplates
  changing; if that shape changes, `LAKE_SUBDIRECTORIES` must track it in lockstep.
  Mild tension with the two deeper contracts framing `derived_retrieval` population
  as generated/governance-gated/build-deferred — resolved because empty dirs ≠
  generated read models, and the controlling v4.1 contract explicitly requires the
  grammar at init. Maintenance coupling, not a correctness or authority violation.
- **R2 — Hard cutover.** v0 roots now fail closed on **both read and write** paths
  (`resolve`/`load_raw_packet`/`_reverify` all gate on the markers). Intended per
  the owner's clean-forward-epoch decision ("archive or abandon"), and the error
  message guides archival. Consequence: the existing live lake is fully walled off
  *through DataLakeRoot* until archived and a new v4.1 root is initialized and
  `ORCA_DATA_ROOT` repointed. Selectively copying old packets into fixtures (a
  contract-allowed treatment) must be done by direct file copy, not through
  DataLakeRoot. Runner cutover sequencing (PR #422) is the separate surface and is
  out of scope here.
- **R3 — Symlink guard unverified in this environment** (the 1 skip). Pre-existing,
  environmental; not introduced by PR #421.
- **R4 — `legacy_roots` contents unvalidated** (only list-ness is checked, `:195`).
  Negligible: `legacy_roots` is a pure annotation never consumed for behavior.
- **R5 — Epoch marker carries an extra `created_at`** not shown in the contract's
  epoch-marker example. Additive and tolerant on read (`_read_epoch_marker` does
  not require it), harmless; arguably useful provenance.

## Verdict

**ACCEPTABLE_FOR_CA_ADJUDICATION.**

PR #421 faithfully implements the v4.1 forward-epoch contract, the Silver Vault
record/read-model boundary, and the physicality/location invariants at the correct
runtime boundary. Behavior is correct and fails closed on v0 roots, missing/malformed
epoch markers, and root-identity swaps; independent validation reproduces
`56 passed, 1 skipped`. The one `major` finding (AR-01) is a **regression-coverage
gap on the new epoch-value enforcement, not a live defect**; the one `minor`
(AR-02) is an unreachable guard. Neither is a design-level mismatch (so not
`NEEDS_ARCHITECTURE_PASS`), and the review completed fully (not `BLOCKED`).

**Tips to `PATCH_BEFORE_KEEP`** if the CA's bar requires regression coverage on
newly added fail-closed enforcement before merge — in that case, land the AR-01
epoch-value rejection tests first. Otherwise AR-01 is a defensible fast-follow.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness,
mandatory remediation, implementation authorization, merge authorization, or
executor-ready patch authority until separately accepted or authorized by the Orca
owner / Chief Architect. Findings are ordered by severity for priority, not as a
pass/fail gate. No source files were edited; no `F:\orca-data-lake` write or live
capture was performed; no `patch_queue_entry` is emitted (read-only lane).
```
