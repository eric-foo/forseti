# YouTube Leading-Dash Residual - Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated adversarial code review)
scope: >
  Read-only adversarial code review of PR #511's YouTube leading-dash video-id
  residual fix (implementation commit 6b82343d) and its evidence receipts.
use_when:
  - Adjudicating whether PR #511 may be treated as reviewed input before merge.
  - Checking whether the leading-dash fix weakens CLI error visibility or overclaims IG/YT completeness.
authority_boundary: retrieval_only
commission: delegated adversarial code review prompt v0 (docs/prompts/reviews/youtube_leading_dash_residual_adversarial_code_review_prompt_v0.md)
review_lane: workflow-code-review after workflow-deep-thinking (no patch authority)
reviewed_by: claude-opus-4-8 (Anthropic / Claude vendor)
authored_by: OpenAI/GPT-family Codex; exact version unrecorded
de_correlation_bar: cross_vendor_discovery
de_correlation_note: >
  Author vendor (OpenAI/GPT) != reviewer vendor (Anthropic/Claude); cross-vendor
  discovery bar satisfied. Full-commit adversarial pass (whole diff + surrounding
  source + targeted repros), not patched-lines-only. This pass surfaced a seam
  (F-1); discovery did not return no-new-seam. Verdict is decision input only,
  not approval / validation / readiness, and not patch authority.
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-youtube-residual-burndown
branch: codex/ig-youtube-residual-burndown-pushable
base: origin/main @ 760fa28d (merge-base of origin/main and HEAD)
implementation_commit_under_review: 6b82343d3852566cfad076183b0060a0c9af8a22
output_mode: review-report (filesystem-output)
edit_permission: read-only (this report is the only authorized write)
```

## Method And Source Context

- **Source-loading mode:** strict-shaped severity labels are used under explicit prompt authorization (Orca review-lanes.md permits `critical`/`major`/`minor` as finding **priority** when the prompt names them). No formal `PASS`, validation, readiness, or patch-queue claim is made. No `patch_queue_entry` is emitted (read-only code-review lane).
- **Method contract:** `workflow-deep-thinking` and `workflow-code-review` reference-loaded from the pinned cache copies, then applied after source readiness.
- **`SOURCE_CONTEXT_READY`** - declared. Required Source Pack read directly from the pinned worktree:
  - Authority/routing: `AGENTS.md` (session context), `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/validation-gates.md`, `.agents/workflow-overlay/safety-rules.md`.
  - Implementation target: full `git show 6b82343d` for all ten touched files; current source of the three runners and `_youtube_cli.py`; the three test files; the three workflow docs.
  - **Source gaps / excluded sources:** `README.md`, `source-loading.md`, `prompt-orchestration.md` were not separately re-read - they govern prompt authoring, source-pack budgets, and protected-path/strict-validation claims that this read-only findings pass does not exercise; non-material to these findings. F-lake live state was treated as an observed external receipt (prompt-directed), not re-captured.
  - **Conflicts:** none blocking. The prompt header's `branch: codex/ig-youtube-residual-burndown` differs from the worktree's actual branch `codex/ig-youtube-residual-burndown-pushable`; same lane of work, HEAD `4c7acd1f` (the prompt-file add). Commit `6b82343d` is present and confirmed **not** an ancestor of `origin/main` (unmerged, as expected for PR #511).
- **Validation evidence:** the commission reported the targeted pytest set at exit 0 / `[100%]`. I did not re-run the full suite (prompt: rerun only if needed for a finding). I ran two targeted, read-only repros against the shipped helper and a faithful argparse model to substantiate F-1 (shown inline). The negative-path test gap in F-2 is, by definition, not covered by the reported green run.

## Findings (severity = priority only; not approval/rejection authority)

### F-1 - `major` - `normalize_video_id_argv` absorbs the runners' own `--data-root` flag, masking a missing-value error

**Reviewed target:** `orca-harness/runners/_youtube_cli.py` (and all three runners that call it).

**Evidence.** The normalizer rewrites `--video-id <value>` whenever `<value>` starts with `-` and `fullmatch`es `[A-Za-z0-9_-]{11}`:

- `orca-harness/runners/_youtube_cli.py:7` - `_YOUTUBE_VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}")`
- `orca-harness/runners/_youtube_cli.py:18-19` - `if value.startswith("-") and _YOUTUBE_VIDEO_ID.fullmatch(value):`
- `orca-harness/runners/_youtube_cli.py:11` (docstring) - *"Allow `--video-id -abc...` without hiding ordinary argparse errors."*

`--data-root` - a **real, registered flag in every one of these runners** (`...asr_packet.py:26`, `...caption_packet.py:29`, `...watch_packet.py:67`) - is exactly 11 characters and entirely within the id charset, so it matches. Confirmed against the shipped helper:

```text
len("--data-root") == 11
n(["--video-id","--data-root","F:/x"]) -> ['--video-id=--data-root', 'F:/x']
n(["--video-id","--model","small"])    -> ['--video-id', '--model', 'small']   # 7 chars, correctly passed through
n(["--video-id","--output"])           -> ['--video-id', '--output']            # 8 chars, correctly passed through
```

Downstream argparse consequence (faithful model of the asr parser), comparing pre-fix vs post-fix:

```text
PRE-FIX  --video-id --data-root F:/x   -> SystemExit rc=2  "argument --video-id: expected one argument"
POST-FIX --video-id=--data-root F:/x   -> SystemExit rc=2  "unrecognized arguments: F:/x"   (real cause now hidden)
POST-FIX --video-id=--data-root        -> parses: Namespace(video_id='--data-root', ...)    (NO error at all)
```

**Impact.** This directly contradicts the change's own stated guarantee and the prompt's named alignment axis (CLI error visibility). When an operator/batch produces `--video-id --data-root <path>` because the id was omitted or templated empty - a realistic mistake, and exactly the leading-dash batch context this fix serves - the ordinary "expected one argument" error is no longer surfaced:

- 3-token form still exits rc=2, but with a misleading "unrecognized arguments" message that hides the missing-value root cause.
- 2-token form (`--video-id --data-root` with `ORCA_DATA_ROOT` set, the asr/data-lake default) **parses cleanly** with `video_id == "--data-root"`, so the runner proceeds to attempt **live capture with a bogus id** instead of failing at the parser. A missing-value typo is escalated into a network fetch rather than a clean rejection.

`--data-root` is the only self-collision among the runner flags (`--video-id`=10, `--model`=7, `--output`=8, `--comment-pages`=15, `--decision-question`= long); the defect is precise, not pervasive.

**`minimum_closure_condition`:** `normalize_video_id_argv` must not rewrite `--video-id <value>` when `<value>` exactly equals one of the target runner's registered option strings (notably `--data-root`), so that omitting the id still surfaces the ordinary argparse "expected one argument" failure. (Required end state; implementation not prescribed. Advisory direction: pass the parser's known option strings - or a small denylist of the runners' long flags - into the helper and skip the rewrite when `value` is among them.)

**`next_authorized_action`:** owner decision - accept as a named residual, or authorize a bounded follow-up patch (this lane has no patch authority). If patched, pair with the F-2 negative test as red-green proof.

**Verification expectation:** a same-check test asserting `--video-id --data-root <path>` and bare `--video-id` still yield `SystemExit`/rc=2 fails against today's behavior (2-token form) and passes after the closure condition is met.

---

### F-2 - `minor` - No negative/regression test for argparse error visibility

**Reviewed target:** `orca-harness/tests/unit/test_youtube_asr_runner_cli.py`, `test_youtube_caption_runner_output_mode.py`, `test_youtube_watch_runner_output_mode.py`.

**Evidence.** All three new tests are happy-path only: each calls `runner.main(["--video-id", "-V7MN2IWMpA", ...])` and asserts the leading-dash id reaches the fetch/write layer (e.g. `test_youtube_asr_runner_cli.py` asserts `video_id == _LEADING_DASH_VIDEO_ID` inside `fake_download` and `fake_write_asr_transcript`). This positive coverage is genuine and good - it proves the normalized path reaches the runner/fetch/write layer, not just a mocked parser. But there is **no** test that a missing value, a `--video-id --data-root` collision, or a mistyped flag still errors. The corpus receipt's own next-step #3 frames test coverage as positive-only ("so future batches can pass `--video-id -...`").

**Impact.** This is the gap that let F-1 ship: the contract clause "without hiding ordinary argparse errors" is asserted in code and docs but never guarded by a test. Review-confidence impact on the error-visibility half of the change.

**`minimum_closure_condition`:** the suite includes at least one negative case proving the runners still reject a missing/garbled `--video-id` value (including the `--data-root` adjacency) with the ordinary parser failure.

**`next_authorized_action`:** owner decision; if F-1 is patched, add this test in the same change as red-green proof.

**Verification expectation:** the negative test is red against current `6b82343d` (the 2-token collision parses today) and green after F-1's closure.

---

### F-3 - `minor` - Closeout receipt non-claim "Not a code patch or runtime behavior change" is contradicted by its own commit

**Reviewed target:** `docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md:350`.

**Evidence.** Commit `6b82343d` ships a new runtime helper (`_youtube_cli.py`) and changes the `parse_args` call in all three runners, and in the same commit edits this receipt to fold the leading-dash video into the corpus (n30->n31, line 16/25). The receipt's `## Non-Claims` (line 350) still reads **"Not a code patch or runtime behavior change."** The n=31 evidence exists *only because of* that runtime change. The sibling corpus receipt (`youtube_behavioral_measurement_corpus_receipt_v0.md`) correctly discloses the patch in its new "Leading-Dash Residual Retry" section; the closeout receipt does not, leaving a non-claim that is false for the commit touching it.

**Impact.** Evidence-receipt accuracy: a load-bearing claim-boundary bullet is self-contradicted by its commit. Low blast radius (doc-only; the authoritative detail receipt it points to is correct), so a diligent reader can reconcile - but a careful adjudicator must flag it.

**`minimum_closure_condition`:** the closeout receipt's non-claim is scoped or corrected so it no longer disclaims the runtime change that its own n=31 evidence depends on (e.g., qualify it to the measurement evidence, or note that this revision rides the leading-dash runtime fix).

**`next_authorized_action`:** owner decision on doc wording; no code impact.

---

### F-4 - `minor` - Repo-map description echoes the inaccurate "without weakening ordinary argparse errors" claim

**Reviewed target:** `docs/workflows/orca_repo_map_v0.md:130`.

**Evidence.** The new navigation row states `_youtube_cli.py` *"allows a valid leading-dash 11-character YouTube id to pass as `--video-id -...` without weakening ordinary argparse errors."* Per F-1 this is not fully true (the `--data-root` collision weakens a missing-value error).

**Impact.** Same root cause as F-1; the repo map is navigation-only (not a validation/authority claim), so impact is descriptive accuracy only - the weakest of the four. The entry is otherwise correctly placed in the runners section and makes no validation claim.

**`minimum_closure_condition`:** the row's wording is reconciled with actual behavior once F-1 is resolved (or qualified now). Lowest priority.

**`next_authorized_action`:** fold into F-1's closure if patched; otherwise owner decision.

## Non-Findings And Verified Boundaries

- **Happy path works.** `--video-id -V7MN2IWMpA` -> `['--video-id=-V7MN2IWMpA']` (11 chars, leading dash); the three positive tests assert the id reaches the fetch/write layer. Mistyped flags (`--vidoe-id ...`), bare `--video-id`, short `-abc`, and ordinary positive ids (`dQw4w9WgXcQ`) all pass through **un-rewritten** and reach normal argparse handling - the normalizer is appropriately narrow except for the F-1 collision.
- **Import/runtime compatibility holds.** `orca-harness/runners/__init__.py` exists (regular package); each runner's `if __package__ in {None, ""}:` block inserts `parents[1]` (= `orca-harness`) on `sys.path`, so `from runners._youtube_cli import normalize_video_id_argv` resolves in both module/test imports and direct script execution. `import sys` is present in all three runners, so the new `sys.argv[1:] if argv is None else argv` reference is safe. The reported pytest green corroborates module-mode resolution.
- **Exit-code / exception semantics preserved.** `parse_args(...)` remains outside each runner's `try:`; argparse `SystemExit(2)` for genuine parse errors still propagates. Normalization is idempotent (an already `--video-id=...` token is not re-processed) and does not touch the `--output`/`--data-root` mutual-exclusion logic.
- **Availability-index rebuild honestly disclosed.** The closeout receipt narrows its prior "Not a data-lake availability-index rebuild" to "Not a ... schema or semantics change" and discloses that the residual-burndown verification ran `rebuild_availability()` (a write) before the fresh readback. This is an accurate narrowing, not a hidden write - a good catch by the author.
- **Corpus-receipt claim boundary intact.** ASR/no-caption (`not observed`), live provider-API extraction (`not observed`), platform-wide completeness (`not proven`), and IG/YT shared-core / full-IG completeness all remain disclaimed. Counts reconcile: 31 records = 2 manual + 28 batch + 1 retry; 122 mentions = 120 + 2; `-V7MN2IWMpA` projects `complete`, mentions=2 (matches the commission's F-lake receipt). The partial-staging failure and cleanup for the first retry are candidly recorded.

## Residual Risk

- **Inherent id ambiguity (bounded, acceptable).** Any 11-char in-charset value starting with `-` is treated as a valid id - a fat-fingered 11-char garbage id is captured as-is and fails downstream rather than at parse time. This is intrinsic to YouTube id syntax and out of scope to "fix"; the F-1 defect is narrower and specific to collisions with the runners' *own* flags.
- **F-lake evidence not independently re-verified.** Per the commission, the live readback for `-V7MN2IWMpA` is treated as an observed external receipt; I did not re-run live capture, so the F-lake writes are accepted, not reproduced.
- **Negative-path behavior unproven by test (F-2).** Until a regression test exists, the error-visibility contract rests on code reading plus this review's repros, not on the green suite.
- **Discovery surfaced a seam.** This cross_vendor_discovery pass found F-1; it therefore does **not** support a "survives adversarial review with no new seam" claim for the patched surface. That claim, if wanted, would require F-1 closure plus re-review.

## Review-Use Boundary

These findings are **decision input only**. They are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority, and this lane holds no patch authority. The Chief Architect adjudicates findings -> diff -> verdict; if a material issue remains (F-1 is the candidate), route the smallest complete closure for it before batching admin/lifecycle follow-ups.
