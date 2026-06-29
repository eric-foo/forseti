# YouTube Behavioral Projection Post-Patch Adversarial Code Recheck v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (implementation/code recheck)
scope: >
  De-correlated, read-only post-patch adversarial recheck of PR #424 at head
  7c7a64a8235741f65c4a1f03642019c437070b95, verifying whether accepted prior
  findings F-01 through F-04 were closed without new false-success paths.
authority_boundary: retrieval_only
reviewed_by: claude-opus-4.8
authored_by: gpt-family-codex
de_correlation_bar: cross_vendor_discovery
de_correlation_note: >
  Author vendor (OpenAI / GPT-family Codex) != reviewer vendor (Anthropic /
  Claude), so the cross-vendor bar is satisfied. The commission only required a
  post-patch recheck (same-vendor sanity tier would have sufficed); this pass
  exceeds that by running cross-vendor. The recheck scope is bounded to F-01..F-04
  closure plus new-false-success detection, NOT a from-scratch re-discovery of the
  whole PR, so it does not by itself assert the global no-new-seam standard for
  every line of PR #424.
source_repo: https://github.com/eric-foo/orca
source_pr: https://github.com/eric-foo/orca/pull/424
source_branch: codex/youtube-behavioral-completion
source_base: main at bba52fd54641f40534ed83d13a794d46f770fa5d
source_head: 7c7a64a8235741f65c4a1f03642019c437070b95
patch_commit: 7c7a64a8235741f65c4a1f03642019c437070b95 (parent 6c225137a0961959cc46f22b8bab2b29b88660fc)
target_blob_ids_verified:
  orca-harness/youtube_capture/behavioral_projection.py: d38366fffdaed007fe5ba081d4f2214fc5a5730a
  orca-harness/tests/unit/test_youtube_behavioral_projection.py: 2fea059ac493da13f5528bf67f51c2089a4ab83a
  orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py: 86ee164e9645847909cbe92d346b8c529100c927
intended_report_path: docs/review-outputs/youtube_behavioral_projection_post_patch_adversarial_code_recheck_v0.md
stale_if:
  - PR #424 head differs from 7c7a64a8235741f65c4a1f03642019c437070b95.
  - Any target blob id differs from the values above.
```

## Recheck Verdict (summary)

**All four accepted findings (F-01, F-02, F-03, F-04) are CLOSED in the head
commit.** The fix is conservative — every change pushes toward *more* failure
visibility, not less — and the targeted offline tests genuinely exercise the
closure branches. I found **no new false-success path** introduced by the patch.

Severity of residuals: **no blocker, no major.** Three `minor` residuals/
observations and one `minor` optional hardening note are recorded below. None
blocks keeping PR #424; all are owner-decision input.

This is advisory implementation/code review. Formal reviewer verdict is
`NOT_CLAIMED`. Findings are decision input only — not approval, validation,
readiness, mandatory remediation, or patch authority.

## Commission · Target · Authority · Decision Criteria

- **Commission:** post-patch adversarial code recheck of PR #424 — were prior
  findings F-01..F-04 closed without introducing new false-success paths?
- **Target (commission-bound):**
  - `orca-harness/youtube_capture/behavioral_projection.py`
  - `orca-harness/tests/unit/test_youtube_behavioral_projection.py`
  - `orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py`
- **Authority:** advisory, read-only. No patch authority, no `patch_queue_entry`,
  no formal PASS/readiness/validation verdict. The shared capture core was not
  reviewed or redesigned; IG/YouTube acquisition-method parity was not required.
- **Decision criteria:** for each finding, did the patch reach the finding's
  closure end-state, and did it preserve true failure visibility (no fake-success,
  no hidden abort, no completion overclaim)?

## Source-Read Ledger

| Source | Why read | What it supports | State |
| --- | --- | --- | --- |
| `AGENTS.md` (supplied in context) | Orca kernel authority | review-as-allowed-work, fresh-read/verify discipline | clean (context) |
| `.agents/workflow-overlay/README.md` | overlay entrypoint | binding rule | clean |
| `.agents/workflow-overlay/source-loading.md` | read-pack + preflight | source discipline, ledger | clean |
| `.agents/workflow-overlay/prompt-orchestration.md` | source-gated method contract, review defaults | REFERENCE-LOAD vs APPLY, provenance fields | clean |
| `.agents/workflow-overlay/review-lanes.md` | review doctrine | findings-first, severity set, two-bar de-correlation, `reviewed_by`/`authored_by` | clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | de-correlation family=vendor | cross-vendor bar definition | clean |
| `.agents/workflow-overlay/safety-rules.md` | safety boundary | read-only posture, no forbidden drift | clean |
| Recheck prompt (`docs/prompts/reviews/youtube_behavioral_projection_post_patch_adversarial_code_recheck_prompt_v0.md`, codex worktree) | commission | F-01..F-04 scope, output contract | clean |
| Prior review prompt (`youtube_behavioral_projection_adversarial_code_review_prompt_v0.md`, codex worktree / branch `codex/youtube-behavioral-review-prompt`) | anchor prior findings framing | F-01..F-04 origin scope | clean |
| `behavioral_projection.py` @ head (blob `d38366ff`) | artifact under recheck | F-01/F-02/F-03 closure logic | verified blob match |
| `test_youtube_behavioral_projection.py` @ head (blob `2fea059a`) | F-04 unit coverage | closure-branch tests | verified blob match |
| `test_..._no_runtime_imports.py` @ head (blob `86ee164e`) | F-02 contract test | import-boundary guard | verified blob match |
| `git diff 6c225137..7c7a64a8` (the actual fix) | isolate what closed the findings | new-false-success analysis | reproduced locally |
| `orca-harness/data_lake/root.py` (unchanged base==head; not in PR diff) | adjudicate F-01 exception surface + F-03 read-only | `load_raw_packet`, `list_available`, `rebuild_availability` | clean |
| `orca-harness/tests/conftest.py`, `orca-harness/pyproject.toml`, `.gitignore` @ head | test runnability + hygiene | independent rerun, O-03 | clean |

**Source gap (disclosed):** the prior review **output** (the verbatim F-01..F-04
findings report) is not present anywhere in the repo tree or any git ref — only
the prior review **prompt** and this recheck's commission summary exist. I
anchored closure conditions to the recheck commission's four-point statement
(corroborated by the prior prompt's Review Scope §). The four findings are
therefore tested against the commission's stated end-states, not a verbatim prior
verdict. This does not block the recheck (the commission binds the scope) but is a
measurement gap worth noting.

## SOURCE_CONTEXT_READY

`SOURCE_CONTEXT_READY` — confirmed:

- PR #424 head = `7c7a64a8235741f65c4a1f03642019c437070b95` (`gh pr view 424`:
  state OPEN, base `main`, headRefOid matches).
- `bba52fd5` is the true merge-base/ancestor of head (base pin correct).
- All three `target_blob_ids` match the header exactly (`git rev-parse <head>:<path>`).
- The pinned commit and diff are directly inspectable in the shared object store.

The Source-Gated Method Contract was honored: authority + skills reference-loaded
first; `workflow-deep-thinking` and `workflow-code-review` applied only after
source readiness.

## Findings (findings-first)

### Closure status

| Finding | Closure | Severity of residual |
| --- | --- | --- |
| F-01 corrupt/unreadable packet no longer aborts healthy projection; visible residual | **CLOSED** | R-01 minor; O-01 minor |
| F-02 pure-projection import boundary guarded for the module, not over-banning | **CLOSED** | O-02 minor (optional hardening) |
| F-03 stale availability-index explicit; default read-only, rebuild opt-in | **CLOSED** | none material |
| F-04 targeted offline tests cover the decision-relevant closure branches | **CLOSED** | O-03 minor (gitignored; stylistic) |

---

### F-01 — CLOSED. Corrupt packet during discovery is residualized, healthy video survives.

**Evidence.** `transcript_sources_for_video` now wraps the per-packet load in a
guard (`behavioral_projection.py:119-130`):

```python
for packet_id in data_root.list_available(source_family="youtube"):
    try:
        loaded = data_root.load_raw_packet(packet_id)
    except DataLakeRootError as exc:
        sources.append(_discovery_failure_source(... packet_id=packet_id, error=str(exc)))
        continue
```

The failure source (`behavioral_projection.py:173-184`) is `source_kind="discovery"`,
`source_status="discovery_failed"`, `posture="discovery_failed"`, and (via
`_base_transcript_source:293-297`) `extraction_eligible=False`. `discovery_failed`
was added to `SOURCE_COMPLETION_PROBLEMS` (`:31-35`) and `EXTRACTION_PROBLEM_STATUSES`
(`:25-30`), so it counts as a source problem in the rollup, forcing status to at
best `complete_with_residuals` (never `complete`) and emitting a
`youtube_transcript_source_discovery_failed:<key>` residual (`_extraction_rollup:434-435`).

**Exception-surface adjudication (the key adversarial question).** The guard
catches only `DataLakeRootError`. I verified against `data_lake/root.py:714-795`
that `load_raw_packet` raises `DataLakeRootError` for the **entire** corruption
surface it models: missing packet (`:724-725`), missing manifest (`:727-728`),
**unreadable/malformed manifest** via `except (OSError, ValueError) -> DataLakeRootError`
(`:729-732`, and `json.JSONDecodeError` is a `ValueError` subclass), non-object
manifest (`:733-734`), bad `preserved_files` (`:735-758`), path escape (`:761-767`),
missing preserved file (`:768-771`), and size/sha256 mismatch (`:773-793`). So the
narrow except does cover manifest corruption and integrity failures comprehensively.

**Independent verification.** The unit test
`test_transcript_discovery_residualizes_corrupt_youtube_packet_without_aborting_healthy_video`
(`test_youtube_behavioral_projection.py:147-181`) passes (reran locally, see
Validation). **Mutation test:** removing the `try/except` guard makes that test
**fail** with `DataLakeRootError: unreadable raw manifest ...` — proving the test
is load-bearing (not vacuous) and that without the fix the abort recurs.

**R-01 (minor residual).** One corruption path is *not* a `DataLakeRootError`:
the preserved-body read `body = file_path.read_bytes()` (`root.py:772`) is not
wrapped, so an `OSError` raised *after* the `is_file()` check passes (`:768`) —
e.g. an I/O error, permission flip, or delete-after-check race on an existing body
file — would propagate as a raw `OSError` and still abort the whole projection.
This is narrow (the dominant "corrupt/unreadable packet" cases — manifest +
integrity — are fully covered), but "unreadable" in the finding's wording can
include an unreadable body file.
- `minimum_closure_condition`: a post-`is_file()` body-read failure on one packet
  produces a visible `discovery_failed` residual instead of aborting the projection
  (achievable either by wrapping `read_bytes()` in `DataLakeRootError` inside
  `load_raw_packet`, or — in this PR's scope — by also catching `OSError` in the
  `transcript_sources_for_video` discovery guard).
- `next_authorized_action`: owner decides whether to harden now or accept the
  residual as below the threat model's center of mass. (`root.py` is outside this
  PR's diff/target set; any change there is advisory only.)

**O-01 (minor observation — attribution/blast-radius, not a false-success).**
The discovery-failure source is appended **before** the per-video
`if meta_video_id != platform_video_id: continue` filter (`:135-136`) and is
stamped with the *queried* `platform_video_id`, because the corrupt packet's own
video id is unknowable once the load fails. Consequence: a single corrupt YouTube
packet is attributed to **every** video projected from that lake (the loop scans
all youtube packets and cannot video-filter the unreadable one), downgrading each
video's `behavioral_completeness` to `complete_with_residuals`. The test confirms
this — a corrupt packet committed for `other000000` surfaces when projecting
`_VIDEO_ID` (`:150-164`). This is the conservative, fail-visible direction (it
does not hide anything), so it is **not** a false-success; but for a per-video
"what we know about this video" projection it can mis-attribute the corruption and
inflate residual noise across unrelated videos.
- `minimum_closure_condition`: either the global discovery-failure attribution is
  scoped/deduped so one corrupt packet does not independently downgrade unrelated
  videos, or the per-video projection contract explicitly documents that a
  `discovery_failed` residual may originate from a packet not belonging to the
  projected video.
- `next_authorized_action`: owner decides whether the current fail-visible-but-
  global behavior is acceptable for the v0 projection contract.

### F-02 — CLOSED. Import boundary guarded for the module without over-banning.

**Evidence.** The new contract test
`test_youtube_behavioral_projection_has_no_runtime_acquisition_or_llm_imports`
(`test_..._no_runtime_imports.py:28-33`) AST-parses **only**
`youtube_capture/behavioral_projection.py` (`:29-30`) and asserts it imports no
forbidden network/LLM/browser roots (`FORBIDDEN_IMPORT_ROOTS:11-25`). It is scoped
to the single projection module — it does **not** scan or ban acquisition modules
elsewhere in `youtube_capture/` (correctly satisfying the "without wrongly banning
acquisition modules elsewhere" condition). Two positive self-tests prove the
detector actually fires: `from urllib import request -> {"urllib.request"}`
(`:47-51`) and `import openai -> {"openai"}` (`:54-58`), so the guard is not
vacuous. The module under test imports only `json`, `typing`, and
`data_lake.root` (the injected-lake error type) — consistent with pure projection.

**Independent verification.** 3 passed (reran locally).

**O-02 (minor — optional hardening, non-required).** The guard is a *denylist*,
which structurally drifts. Notable absences: `urllib3`, `http.client`, `ftplib`,
`websockets`, `grpc`, `pycurl`, and dynamic import (`importlib` / `__import__`). A
future acquisition import via one of those would pass the guard. An **allowlist**
(permit only `json`, `typing`, and `data_lake.*`; flag anything else) would be
strictly tighter. This is optional hardening, not a closure blocker — the current
module passes and the finding's stated condition (a scoped, real guard exists) is met.

### F-03 — CLOSED. Default projection is read-only; index rebuild is opt-in.

**Evidence.** `transcript_sources_for_video(..., rebuild_availability=False)`
(`behavioral_projection.py:104-116`) calls `data_root.rebuild_availability()`
**only** when `rebuild_availability=True`; the convenience wrapper
`project_youtube_behavioral_item_from_lake` passes the flag through with the same
`False` default (`:260-278`). I confirmed in `root.py` that the default path is
genuinely side-effect-free: `list_available` (`:805-815`) only reads
`indexes/availability/*.json` and returns `[]` when the dir is absent — no
`_reverify`, no writes; `rebuild_availability` (`:817-845`) is the sole writer
(it deletes and regenerates the index) and is reached only on opt-in. The test
`test_transcript_discovery_requires_explicit_availability_rebuild_for_stale_index`
(`test_youtube_behavioral_projection.py:289-300`) deletes the availability entries,
asserts the default call returns `[]` (stale index honored, not silently rebuilt),
and that `rebuild_availability=True` recovers the caption source. `data_root.path`
used by the test is a real public property (`root.py:296`).

**Independent verification.** Covered by the 9-passed unit suite (reran locally).

### F-04 — CLOSED. Targeted offline tests cover the decision-relevant closure branches.

**Evidence.** The patch adds/extends exactly the closure-branch coverage: F-01
corrupt-packet residualization (`:147-181`), F-03 explicit availability rebuild
(`:289-300`), and the F-02 contract test + detector self-tests. All are offline:
the unit tests use `DataLakeRoot.for_test(tmp_path/...)` and commit fixtures
locally; the contract test parses files via `ast`. Pre-existing decision-relevant
tests remain green (mixed/partial rollups, failed-ASR-as-source-problem, ambiguous
anchor result, metadata mismatch, metadata-only postures).

**Independent verification.** 9 / 3 / 20 passed across the three reported commands
(reran locally; counts match the home lane's report). The F-01 mutation test
demonstrates the new coverage is load-bearing.

**O-03 (minor — test hygiene, stylistic).** The contract test's `scratch_dir`
fixture writes to `orca-harness/_test_runs/<uuid>` inside the repo tree
(`:36-44`) rather than pytest `tmp_path` as the unit tests do. Cleanup is
`shutil.rmtree(..., ignore_errors=True)`. I confirmed `orca-harness/_test_runs/`
**is** gitignored (`.gitignore:26`), so this creates **no tracked litter** — the
only residual is a stylistic inconsistency (in-tree scratch vs `tmp_path`) and a
small chance of orphaned ignored files on hard interruption.
- `minimum_closure_condition`: contract-test scratch files use `tmp_path` (or an
  equally isolated, auto-cleaned location) for consistency with the unit tests.
- `next_authorized_action`: optional; owner may accept as-is (no functional or
  VCS-hygiene impact).

## New-False-Success-Path Analysis (core recheck question)

I specifically attacked whether the patch could let a video be reported as more
complete or healthier than reality. Conclusion: **no new false-success path.**

- `discovery_failed` was added to *problem* sets only (`:25-35`); it can never
  raise completion. A discovery source has `extraction_eligible=False`, so it is
  excluded from `eligible`/`complete` counts in `_extraction_rollup` (`:409-424`)
  and cannot inflate completion.
- With any discovery failure present, `_extraction_rollup` cannot return
  `"complete"` (it requires `source_problem_count == 0`, `:446-448`); it degrades
  to `complete_with_residuals`/`source_problem`. Verified by test (`:176-181`).
- A discovery source cannot be chosen as `canonical_source` — that selector
  considers only `extraction_eligible is True` sources (`:473-477`).
- No source-key collision: a discovery source's key is `<packet_id>:discovery`
  (`_transcript_source_key:606-614`), distinct from `:caption`/`:asr` keys, so it
  cannot shadow or be shadowed by a real source's extraction result.

The patch's net effect is strictly *more* failure visibility (the O-01
over-surfacing direction), which is the correct side of the no-fake-success rule.

## Validation Evidence Inspected

**Independently reran** (throwaway detached worktree pinned at head
`7c7a64a8`, Python 3.11.15 / pytest 9.0.3, worktree removed after):

| Command (from recheck prompt) | Reported | Observed |
| --- | --- | --- |
| unit `test_youtube_behavioral_projection.py` | 9 passed | **9 passed** |
| contract `test_..._no_runtime_imports.py` | 3 passed | **3 passed** |
| existing `test_youtube_caption_product_extract.py` + `test_transcript_product_lake.py` + `test_no_llm_imports.py` | 20 passed | **20 passed** |

**Mutation probe (added by this recheck):** removing the F-01 `try/except` guard
flips the corrupt-packet test to FAILED (`DataLakeRootError`), confirming the test
guards the fix.

## Validation Not-Run Gaps

- `git diff --check` / `git diff --cached --check` and
  `check_repo_map_freshness.py --changed` (reported clean by the home lane) were
  **not** independently rerun — out of the bounded code-recheck scope; treated as
  author-supplied.
- No live capture run (correctly out of scope; offline evidence answered the
  recheck question).
- The prior-review **output** report does not exist in the repo (source gap above);
  closure was assessed against the commission's stated F-01..F-04 end-states.
- Recheck scope is bounded to F-01..F-04 + new-false-success detection; this pass
  does not assert a full from-scratch no-new-seam discovery over all of PR #424.

## Review-Use Boundary

These findings are **decision input only**. This recheck is advisory and
read-only: it is not approval, not validation, not readiness, not mandatory
remediation, and not executor-ready patch authority, and it confers no live-capture
authorization. The home model adjudicates this recheck before keeping or landing
PR #424. Reviewer verdict: `NOT_CLAIMED`.

## review_summary

```yaml
review_summary:
  reviewed_by: claude-opus-4.8
  authored_by: gpt-family-codex
  de_correlation_bar: cross_vendor_discovery
  source_context: SOURCE_CONTEXT_READY
  recheck_verdict: NOT_CLAIMED
  closure:
    F-01: closed   # residuals R-01 (minor), O-01 (minor)
    F-02: closed   # O-02 minor optional hardening
    F-03: closed
    F-04: closed   # O-03 minor stylistic (gitignored scratch)
  new_false_success_paths: none_found
  blocker_or_major_findings: none
  minor_findings: [R-01, O-01, O-02, O-03]
  independent_validation: 9_passed / 3_passed / 20_passed (counts match home lane) + F-01 mutation probe load-bearing
  non_claims: [not approval, not validation, not readiness, not patch authority, not live capture]
```
