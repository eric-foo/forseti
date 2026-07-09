# Capture Runner v4.1 Blocker Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Adversarial artifact review of the Capture Spine runner v4.1 lake-write blocker
  addendum: tests whether its blocker claim and patch sequence are source-backed,
  overstated, understated, stale, or wrong against current harness code.
use_when:
  - Deciding whether to authorize v4.1 DataLakeRoot / runner implementation.
  - Checking whether the v4.1 addendum's blocker and patch sequence hold up.
open_next:
  - docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md
  - docs/prompts/reviews/capture_runner_v4_1_blocker_adversarial_review_prompt_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - forseti-harness/data_lake/root.py
branch_or_commit: codex/ig-reels-capture-spine @ 558265a33031be973f3702d17164bf0f983f3d34
stale_if:
  - root.py, the seam test, or the data-lake availability/root tests change.
  - The v4.1 forward-epoch contract is materially edited, rejected, or lands on origin/main.
  - A v4.1 DataLakeRoot/runner implementation patch lands.
  - The dirty/untracked controlling-source state changes again.
authority_boundary: retrieval_only
```

## Body Opening

Purpose: a read-only adversarial review of
`docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md`. It tests
the addendum's blocker claim and patch sequence against the current harness code,
so a Chief Architect can decide whether to authorize v4.1 implementation.

Do not use for: implementation authorization, validation/readiness of the v4.1
contract or code, live-capture or live-root write authorization, Silver Vault
schema decisions, or a claim that the v4.1 contract is landed on `origin/main`.

Authority boundary: current user instruction, `AGENTS.md`, and
`.agents/workflow-overlay/` win. Code and read-only observations win over this
report when they drift.

Recheck recipe: rerun branch/HEAD/status; reread `root.py`, the seam test, the
data-lake availability/root tests, and the v4.1 contract; re-grep
`packet_shard|orca-lake-epoch|lake_epoch` across `orca-harness`; recheck whether
the v4.1 contract is on `origin/main`.

Non-claims: not validation, not readiness, not implementation authorization, not
approval to patch runners or `DataLakeRoot`, not permission to write/delete the
external root, not a claim that the v4.1 contract is merged to `origin/main`, and
not acceptance of sharded-vs-unsharded raw pathing.

## Provenance

- `reviewed_by`: `claude-opus-4-8`.
- `authored_by`: `unrecorded`. The reviewed addendum records no author; its branch
  `codex/ig-reels-capture-spine` suggests a Codex/GPT-family author, but that is an
  inference, not a recorded fact, so it is not asserted. (Provenance is observed
  metadata only; it implies no model recommendation. This review was commissioned
  via a filed review prompt — the source-read-only adversarial artifact review lane
  — not the delegated-review-patch convention, so no `de_correlation_bar` is bound.)

## Commission, Target, Authority

- Commission: `docs/prompts/reviews/capture_runner_v4_1_blocker_adversarial_review_prompt_v0.md`.
- Primary review target: `docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md`.
- Related context (not the primary target): `docs/review-outputs/capture_spine_runner_data_lake_dump_audit_v0.md`.
- Authority: read-only adversarial artifact review (`.agents/workflow-overlay/review-lanes.md`);
  reviewer may write only this report; severity set `critical/major/minor` is finding
  priority only and creates no approval/validation/readiness/mandatory-remediation authority;
  `patch_queue_entry` is forbidden in this lane.
- Decision criteria (bound `fitness_reference`, an alignment axis attacked, not a pass bar):
  the work succeeds if a Chief Architect can decide whether to authorize implementation from a
  source-backed answer to (1) can all current Source Capture packet writers write into a v4.1
  data lake today, (2) if not, the exact blocker set, (3) is the patch sequence the smallest
  complete route or does it miss a higher-priority blocker.

## Method And Skill Status

- `workflow-deep-thinking`: REFERENCE-LOADed before source-load (neutral lens for blocker
  failure modes: overstated / understated / stale / miscounted / seam-vs-v4.1 conflation /
  untracked-contract-as-landed / patch-sequence-not-smallest-complete / live-root misused),
  then APPLIED after `SOURCE_CONTEXT_READY`.
- `workflow-adversarial-artifact-review`: REFERENCE-LOADed and APPLIED after source readiness.
  Two-phase critique (correctness then friction) used.
- Source-gated sequence honored: authority reads -> reference-load -> source-load ->
  `SOURCE_CONTEXT_READY` -> apply.

## SOURCE_CONTEXT_READY

Declared. All load-bearing addendum cites were re-verified against current code at the
observed HEAD; no required source was missing for the core verdict. Two source/decision gaps
(contract not on `origin/main`; `packet_shard` derivation undefined) are reported as findings,
not as a block on the verdict.

### Observed Workspace State

- Reviewed in the main working tree (`C:\Users\vmon7\Desktop\projects\orca`) on
  `codex/ig-reels-capture-spine`. Observed HEAD advanced **during** this review from
  `3628dba` to `558265a3` ("docs: lock data lake v4.1 silver vault foundation"); the live
  worktree is being committed to concurrently. This review is anchored to HEAD `558265a3`.
- Commit lineage (older -> newer), all ancestors of HEAD: `13680ddd` (dump audit authored) ->
  `f95c33ae` (addendum committed; the commission prompt's `expected_head_at_prompt_authoring`)
  -> `3628dba` (this commission prompt committed) -> `558265a3` (HEAD).
- Code evidence clean at HEAD: `orca-harness/data_lake/root.py`, the seam test, and the
  data-lake availability/root tests show no working-tree or staged diff.
- Controlling-contract tracking state at HEAD (verified): the v4.1 forward-epoch contract is
  committed on this branch but **NOT on `origin/main`** (`git cat-file -e origin/main:<path>`
  fails); the physicality/location contract is committed on this branch **and on `origin/main`**.
  Both were dirty (staged/modified) at session start and were committed mid-review.
- The addendum and dump audit are committed at HEAD with no working-tree diff.
- Live external root `F:\orca-data-lake` was NOT re-read in this review (the commission scopes
  live-root inspection as optional); the addendum's live-root counts are accepted as its reported
  read-only observations, not independently re-verified here.

### Source-Read Ledger

| Source | Why read | Supports | Freshness |
| --- | --- | --- | --- |
| `docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md` | Primary target | All findings | committed @558265a3, clean |
| `docs/review-outputs/capture_spine_runner_data_lake_dump_audit_v0.md` | Related context (counts, incident) | Non-findings, AR-02 | committed @558265a3, clean |
| `orca-harness/data_lake/root.py` | Verify v0 marker/ref claims | Verdict, AR-02, AR-04 | clean @558265a3 |
| `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md` | Verify v4.1 obligations; landed status | Verdict, AR-01, AR-02 | committed on-branch, NOT on origin/main |
| `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` | Verify producer/seam detection + nine-allowlist | Checks #3/#4/#6 | clean @558265a3 |
| `orca-harness/tests/test_data_lake_availability.py:45` | Verify v0 `raw_path` assertion | Check #6 | clean @558265a3 |
| `orca-harness/tests/test_data_lake_root.py:90-92` | Verify v0 marker assertion | Check #6 | clean @558265a3 |
| `runners/` grep `write_local_source_capture_packet`/`stage_and_write_packet` | Count producers | Check #4 (12 producers) | live @558265a3 |
| `runners/` grep `data_root` | Count seam runners | Check #3 (3 seam) | live @558265a3 |
| `orca-harness` grep `packet_shard|orca-lake-epoch|lake_epoch` | Confirm no v4.1 code | Verdict, AR-02 | live @558265a3, zero matches |
| Authority overlay (`AGENTS.md`, README, source-of-truth, artifact-roles, review-lanes, validation-gates, source-loading, prompt-orchestration) + `orca_prompt_behavior_contract_v0.md` | Bind review lane, roles, severity, non-claims | Whole review | clean |
| `orca-harness/source_capture/writer.py`, `packet_assembly.py` | Shared write path | Verdict (no shard/epoch logic) | available, not opened in full; covered by the zero-match grep |

## Verdict (Headline)

**The addendum's blocker claim is SOURCE-BACKED and ACCURATE.** Every load-bearing
`file:line` cite was re-verified against current code at HEAD `558265a3`:

- `root.py:40` -> `ROOT_MARKER_CONTRACT_VERSION = "v0"` (verified).
- `root.py:202-203` -> availability refs `raw/{packet_id}` and `raw/{packet_id}/manifest.json`,
  unsharded (verified).
- `root.py:423-451` (`stage_raw_packet`/`publish_raw_packet`) -> publish to `raw/<packet_id>`
  via `self._within("raw", packet_id)`, unsharded (verified).
- v4.1 contract `:136-159` (v4.1 root marker + `.orca-lake-epoch.json`) and `:161-170`
  (forward-writer obligations incl. `raw/<packet_shard>/<packet_id>/`) (verified).
- No v4.1 lake code exists: `packet_shard|orca-lake-epoch|lake_epoch` returns **zero matches**
  across `orca-harness` (verified).
- Counts verified independently of the addendum: exactly **12** producer-token runners, of which
  exactly **3** carry `data_root` (`run_source_capture_packet.py`, `run_source_capture_http_packet.py`,
  `run_source_capture_ig_reels_grid_packet.py`); the remaining **9** match `KNOWN_UNSYNCED`
  (`test_capture_runner_lake_seam_coverage.py:26-36`) exactly.

The blocker is therefore **not overstated, not understated on its core claim, not miscounted,
and not stale in substance**. The addendum is a high-quality, source-faithful artifact. The
findings below are about **patch-sequence completeness and freshness descriptors**, not about
the blocker being wrong.

No `critical` findings (nothing invalidates the blocker). Two `major` completeness gaps and two
`minor` notes follow, correctness phase first.

## Findings

### AR-01 - Major (correctness) - Patch sequence omits the controlling-contract-acceptance gate

- Phase: correctness.
- Location: addendum "Patch Recommendation", steps 1-2 (`...addendum_v0.md:172-188`); cf.
  "Current State" (`:80-82`) and "Non-claims" (`:48-50`).
- Source authority: `core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md` (the entire
  blocker is defined against it); `.agents/workflow-overlay/prompt-orchestration.md`
  control-plane source-state gate (modified/untracked controlling sources block strict claims
  unless owner-accepted).
- Issue: the "smallest complete v4.1 patch sequence" jumps from test-safety (step 1) to
  "Patch `DataLakeRoot` to v4.1" (step 2), which bakes in v4.1 marker/epoch/sharded semantics
  drawn entirely from the v4.1 forward-epoch contract. That contract is **committed on this
  branch but not on `origin/main`** (verified), and by its own header it is `stale_if` "the
  owner rejects the clean v4.1 epoch reset." Acceptance/landing of the controlling contract is a
  higher-priority precondition than test-safety, yet it is not a numbered gate in the sequence.
- Strongest reading (and why it still matters): the addendum **does** disclose the not-landed
  status in "Current State" and "Non-claims" and explicitly disclaims implementation
  authorization, so a careful reader is warned. It still matters because the patch sequence is
  the actionable object a CA would follow to authorize implementation; fitness question 3 asks
  precisely whether a higher-priority blocker is missed, and contract-acceptance is one.
  Implementing sharding/epoch against a branch-only, still-rejectable contract is rework risk.
- Impact: a CA could read the sequence as "start at step 1" when the true first gate is
  "accept/land the v4.1 contract (and the physicality contract it leans on) as controlling
  authority." Without that gate, steps 2-5 may be built against a contract that still changes.
- minimum_closure_condition: the patch sequence names contract acceptance/landing as the explicit
  precondition gating steps 2-5 (or states the owner decision that implementation may proceed
  against a branch-only contract). Required end state, not an implementation instruction.
- next_authorized_action: owner/CA decision on whether to land/accept the v4.1 contract before
  authorizing `DataLakeRoot` work; no patch authority is granted by this review.
- Recommended direction (advisory only): add a step 0 — "v4.1 forward-epoch contract accepted as
  controlling authority" — ahead of the existing sequence.
- patch_queue_entry: not authorized in this lane.
- not proven: that the contract will or should land (owner decision); red-green proof
  not_applicable (non-executable artifact finding).

### AR-02 - Major (correctness) - `packet_shard` derivation is undefined; step 2 understates it as "add a helper"

- Phase: correctness.
- Location: addendum "Patch Recommendation" step 2 ("Add a packet shard helper and publish raw
  packets under `raw/<packet_shard>/<packet_id>/`", `...addendum_v0.md:184-186`); v4.1 contract
  `:95` and `:167` (`raw/<packet_shard>/<packet_id>/`); dump audit F1 (`...dump_audit_v0.md:81-93`).
- Source authority: v4.1 forward-epoch contract; `orca-harness/data_lake/root.py` (no sharding);
  repo-wide `packet_shard` grep (zero matches).
- Issue: the v4.1 contract requires a sharded raw path `raw/<packet_shard>/<packet_id>/` but never
  defines how `packet_shard` is derived. Current code has no sharding anywhere (grep zero). Yet the
  live legacy root already contains sharded entries such as `raw/67c/<packet_id>` (dump audit F1) —
  produced by a prior/external scheme that is **not present in the current tree and is not a prefix
  of the packet_id**, so it is neither specified nor reproducible from current sources. Step 2 frames
  "add a packet shard helper" as a mechanical addition, when it is actually an undefined design
  decision (shard width, hash basis, normalization) on which the rest of step 2 depends.
- Strongest reading (and why it still matters): the v4.1 contract's acceptance criterion 7
  ("sharding and availability refs are explicit") implies the shard rule must be made explicit, so
  one could argue the addendum delegates this to the contract. It still matters because the addendum
  presents step 2 as smallest-complete-ready and does not flag that the shard grammar is currently
  undefined; "smallest complete" cannot be satisfied until the rule is pinned, and the existing
  `raw/67c/...` evidence shows a real but unrecoverable prior scheme that a naive helper could
  silently diverge from.
- Impact: step 2 cannot be completed without first defining the shard-derivation rule; an
  implementer could invent a shard function that diverges from the legacy `raw/67c/...` shape,
  compounding the mixed-layout problem the dump audit already flagged.
- minimum_closure_condition: the `packet_shard` derivation grammar is defined in the controlling
  contract (or named as the open owner decision step 2 depends on) before v4.1 path work is treated
  as mechanical.
- next_authorized_action: owner/CA or contract-owner defines the shard grammar; no implementation
  authority is granted here.
- Recommended direction (advisory only): add a finding/flag that `packet_shard` is unspecified and
  must be defined by the v4.1 contract before the helper is written; capture whether the legacy
  `raw/67c/...` scheme is reproduced or deliberately abandoned (the clean-epoch contract permits
  abandoning it).
- patch_queue_entry: not authorized in this lane.
- not proven: the origin of the legacy sharded entries (no current source identifies the writer
  that produced them); red-green proof not_applicable.

### AR-03 - Minor (correctness) - Freshness descriptors overtaken by events

- Phase: correctness.
- Location: addendum "Current State" (`...addendum_v0.md:80-82`).
- Source authority: live git state at HEAD `558265a3` (verified this review).
- Issue: the addendum describes the v4.1 contract as "an untracked workspace source" and the
  physicality/location contract as "modified." As observed at HEAD `558265a3` (advanced during this
  review), the v4.1 contract is **committed on this branch** (still not on `origin/main`) and the
  physicality contract is **committed and on `origin/main`**. The descriptors are now stale.
- Strongest reading (and why it still matters): this is the normal consequence of reviewing a live,
  concurrently-committed worktree, and the addendum's substantive non-claim ("not landed on main")
  remains true for the v4.1 contract — so the authority handling is not wrong. It still matters at the
  margin: a CA reading "untracked" may under-weight that the contract is now branch-committed (more
  settled than "untracked" implies, though still not mainline).
- Impact: low; a stale freshness label, not an authority error. Reconciles with AR-01:
  committed-on-branch is not landed-on-`origin/main`.
- minimum_closure_condition: a refreshed branch/HEAD/status snapshot accompanies the addendum when it
  is next relied upon for a decision.
- next_authorized_action: re-snapshot on next use; no edit authorized by this review.
- patch_queue_entry: not authorized in this lane.

### AR-04 - Minor (correctness) - V41-F1 cite omits a third unsharded raw-write entry point

- Phase: correctness.
- Location: addendum V41-F1 evidence list (`...addendum_v0.md:108-112`).
- Source authority: `orca-harness/data_lake/root.py:406-421` (`allocate_raw_packet_dir`).
- Issue: V41-F1 cites `root.py:202-203` (availability refs) and `:423-451` (`stage`/`publish`) as the
  unsharded write paths, but `allocate_raw_packet_dir` (`:406-421`) is a third raw-write entry point
  that is also unsharded (`self._within("raw", packet_id)`). The omission strengthens rather than
  weakens the blocker, but a v4.1 path patch (step 2) must cover all three entry points
  (allocate / stage / publish), and the addendum's enumeration names only two.
- Strongest reading (and why it still matters): the claim "the shared write path is unsharded" is true
  regardless, so the finding does not change the verdict. It matters only as a completeness check on the
  v4.1 patch surface — missing `allocate_raw_packet_dir` could leave one unsharded write path behind.
- Impact: very low for the verdict; a small completeness note for the eventual patch surface.
- minimum_closure_condition: the v4.1 DataLakeRoot patch surface covers all raw-write entry points
  (`allocate_raw_packet_dir`, `stage_raw_packet`, `publish_raw_packet`), not only stage/publish.
- next_authorized_action: note for the implementer; no edit authorized by this review.
- patch_queue_entry: not authorized in this lane.

### Phase 2 (friction)

No material friction findings. The addendum is lean for its purpose; the runner matrix restated from
the dump audit is justified (the v4.1 overlay needs its own seam-vs-v4.1 column), not avoidable bloat.
No finding is invented to look thorough.

## Non-Findings (Survived Adversarial Attack)

These commission checks were attacked and held; recorded so the CA sees what was tested, not skipped:

- Check #1 (legacy seam vs v4.1 distinction): correct — V41-F1 and the matrix separate "lake seam
  today" from "v4.1 status."
- Check #2 (current DataLakeRoot v0 behavior, not missed code): verified v0; no v4.1 code anywhere.
- Check #3 (three seam runners): verified exact via independent grep.
- Check #4 (nine local-output-only writers): verified — 12 producers minus 3 seam equals the nine
  `KNOWN_UNSYNCED` entries exactly.
- Check #5 (two orchestrators): verified — `run_source_capture_durability_series.py` and
  `run_reddit_old_http_batch.py` carry neither producer token, so they correctly escape the
  producer-token seam contract; neither is already covered.
- Check #6 (tests enforce only seam presence, not v4.1): verified — the seam test asserts only
  presence/acknowledgement, and `test_data_lake_availability.py:45` / `test_data_lake_root.py:92`
  actively assert the v0 shape, which V41-F3 correctly says must change.
- Check #7 (no overclaim of untracked contract as landed): verified — handled correctly; Body
  Opening, Current State, and Non-claims all disclaim landing on main. (Freshness descriptor drift is
  AR-03; it does not become an overclaim.)
- Check #8 (live root used as legacy evidence, not a v4.1 target): correct per V41-F2; consistent with
  the clean-forward-epoch contract. Boundary: the live-root counts were not independently re-read here.

## Fitness-Reference Answers

1. **Can all current Source Capture packet writers write into a v4.1 data lake today?** No — none can.
   No v4.1 lake code exists (`packet_shard|orca-lake-epoch|lake_epoch` zero matches); `DataLakeRoot`
   emits a `v0` marker (`root.py:40`), unsharded raw refs (`:202-203`, `:406-451`), and no epoch
   marker; and only 3 of 12 direct producers expose any lake seam at all — those three still produce
   v0-shaped refs.

2. **If not, what is the exact blocker set?** (i) `DataLakeRoot` writes a `v0` root marker, unsharded
   `raw/<packet_id>` refs, and no `.orca-lake-epoch.json` (`root.py:40,202-203,406-451`); (ii) 9 of 12
   direct packet producers have no lake seam (`KNOWN_UNSYNCED`, seam test `:26-36`); (iii) 2
   packet-producing orchestrators (`run_source_capture_durability_series.py`,
   `run_reddit_old_http_batch.py`) escape the producer-token seam contract; (iv) tests assert the v0
   shape and enforce only seam presence. Two further blockers the addendum **understated**: (v) the
   controlling v4.1 contract is not landed on `origin/main` (AR-01), and (vi) the `packet_shard`
   derivation rule is undefined (AR-02).

3. **Is the patch sequence smallest complete, or does it miss a higher-priority blocker?** It is
   largely sound and well-ordered — test-safety-first is justified by the real live-root write incident,
   and DataLakeRoot-before-runners is the correct dependency order. But it misses two higher-priority
   preconditions: the contract-acceptance gate (AR-01) and the shard-derivation definition (AR-02).
   With those named as step 0 / a step-2 precondition, the sequence is complete; without them, the
   "smallest complete" claim is not yet met.

## Strict-Only Blockers / Not-Proven Boundaries

- This review proves the addendum's blocker is source-backed; it does **not** validate the v4.1
  contract, prove readiness, or authorize implementation.
- Live external root `F:\orca-data-lake` was not re-read; the addendum's live-root counts are accepted
  as reported observations, not re-verified.
- The origin of the legacy `raw/67c/...` sharded entries is not established by any current source.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness, mandatory remediation,
implementation authorization, or executor-ready patch authority until separately accepted or authorized
by the Orca owner / Chief Architect. Severity labels are finding priority only. No source file was
edited and no patch was executed.
