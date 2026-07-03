# Delegated Adversarial Code Review-And-Patch — YT RSS Tier-1 Monitor Lane

```yaml
retrieval_header_version: 1
artifact_role: delegated_review_dispatch_prompt
scope: >
  Commission prompt for a de-correlated (non-Anthropic) controller to run an
  adversarial code review-and-patch pass on the YT tier-1 RSS daily-monitor
  build (parser + runner + tests + two governance-gate declarations) on lane
  branch claude/yt-rss-tier1-monitor, under the provisional delegated
  review-and-patch convention (delegated_code_review_and_patch sibling mode,
  repo access). Filed as the lane's review-routing evidence; the commissioning
  CA adjudicates the return before anything is kept.
use_when:
  - Dispatching the delegated review for the YT RSS monitor lane PR.
  - Checking what scope, method, and output contract that review was bound to.
stale_if:
  - The lane branch is merged, closed, or rebased past the reviewed head.
  - The delegated review return has been adjudicated (packet becomes lane
    history).
authority_boundary: retrieval_only
```

## Operator Courier Instruction (who-constraint, not a model recommendation)

- `authored_by` (home/CA family): Anthropic Claude (Claude Code lane).
- Controller (you are pasting this to it): **must be a non-Anthropic vendor**
  (cross-vendor discovery bar per
  `.agents/workflow-overlay/delegated-review-patch.md`); `operator_to_fill`:
  record the controller vendor/model on the durable report as `reviewed_by`.
  Pasting this to an Anthropic model defeats de-correlation — do not.
- `access: repo` — the controller must have direct access to the repository
  worktree (e.g. an agent lane with the repo checked out). Couriered delivery
  does not imply no-repo.
- `dispatch_mode: external-controller-courier`; current receiving actor role:
  `controller`. Do not launch a replacement controller or sub-reviewers.

## Goal (executor target + review axis-to-attack, not a pass bar)

- **Goal:** the daily YT tier-1 RSS monitor must write TRUSTWORTHY packets to
  the data lake: exact-only metrics, honest gaps, correct first-seen flags —
  the registry's spike decisions will later stand on this data.
- **Done looks like:** an adversarial pass finds no seam by which a daily
  packet could carry silently wrong or silently missing data (zero-fill,
  precision inflation, wrong first-seen, invisible per-channel failure), or
  such seams are found, patched within scope, and cited.
- Upstream intent pointers (read, then attack the fit): merged assessment
  receipt
  `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_grid_tier_assessment_v0.md`
  (Run 3 + revised recommendation); owner two-tier direction quoted in
  `docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md`.

## Preflight (orca_start_preflight; repo-constants per docs/prompts/templates/shared/orca_preflight_defaults_v0.md)

- required_reads_confirmation: read `AGENTS.md` and
  `.agents/workflow-overlay/README.md` first; operating contract for this
  commission: `.agents/workflow-overlay/delegated-review-patch.md`.
- source_pack: bounded custom pack — the Named Target Set plus Context Reads
  below; `repo_map_decision: not_needed` (`repo_map_reason`: bounded named file
  set with explicit context reads).
- workspace: the Orca repository (`eric-foo/orca`), fresh fetch.
- branch: `claude/yt-rss-tier1-monitor` at the lane PR's current head (fresh
  `git fetch` then check out that exact head; record the SHA you reviewed in
  the report).
- dirty-state allowance: none — a clean tree at the pinned head; your own
  working-tree patch is the only allowed modification.
- controlling-source state: expected clean; if `AGENTS.md`, the overlay, or the
  target files differ from the lane head, stop and report, do not review a
  substitute.
- doctrine change: none — this lane changes no doctrine surface; no
  `direction_change_propagation` receipt is required.
- edit permission: `patch-only`, strictly bounded to the Named Target Set.
- output mode: `review-report` (durable report; see Output Contract) plus a
  working-tree unified diff (never commit, never push).
- validation gates: `python -m pytest` from `orca-harness/` (full suite; green
  baseline at commission time: 2476 passed, 7 skipped). Run it; report real
  results; a failure is surfaced, never masked. No `PASS`/readiness claims.
- external source boundary: external workflow source is read-only; `jb` is not
  Orca authority.

## Named Target Set (the ONLY patchable files; cannot silently widen)

| Label | Path | Bounded patch scope |
|---|---|---|
| `[rss-parser]` | `orca-harness/source_capture/youtube_channel_rss.py` | whole file (new in this lane) |
| `[rss-runner]` | `orca-harness/runners/run_source_capture_youtube_rss_monitor.py` | whole file (new in this lane) |
| `[parser-tests]` | `orca-harness/tests/unit/test_youtube_channel_rss.py` | whole file (new in this lane) |
| `[runner-tests]` | `orca-harness/tests/unit/test_youtube_rss_monitor.py` | whole file (new in this lane) |
| `[seam-decl]` | `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` | the one-line `EXPECTED_BRONZE_WRITER_RUNNERS` declaration only |
| `[inventory-decl]` | `orca-harness/data_lake/lake_touchpoint_inventory_v0.json` | regeneration via `data_lake.inventory` only (never hand-edit) |

Why read-only review is insufficient: the honesty semantics (gap postures,
first-seen, exact-only metrics) are exactly the class of defect the author can
reintroduce against their own guardrails; a de-correlated bounded patch with
citations is cheaper and safer than a review→instruct→patch round-trip.

Everything outside the set is **read-only — flag, don't edit** (all other Orca
sources; canonical/frozen/hash-pinned artifacts; `.agents/**`; `AGENTS.md`;
ledgers; everything `.agents/workflow-overlay/safety-rules.md` forbids). A fix
that requires touching an unnamed file is a flagged finding, not an edit.

## Method (Source-Gated Method Contract)

1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review`. Do not
   APPLY them yet; use them only to prepare a neutral source-reading lens.
2. SOURCE-LOAD the Named Target Set, then these Context Reads (read-only):
   - `orca-harness/runners/run_source_capture_youtube_watch_batch.py` (the
     pacing/circuit-break/cooldown pattern the runner mirrors);
   - `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py` (the
     packet-shape precedent: slices, metric postures, limitations rollup);
   - `orca-harness/source_capture/models.py` and
     `orca-harness/source_capture/packet_assembly.py` (posture vocabularies —
     incl. Ob.15 `re_capture_relationship` closed values — and the
     posture-honesty gate);
   - `orca-harness/data_lake/root.py` (`list_available`, `read_availability`,
     `load_raw_packet` semantics the first-seen state derivation depends on);
   - `orca-harness/data_lake/inventory.py` (what `[inventory-decl]` declares);
   - `orca-harness/capture_spine/creator_profile_current/youtube_watch_packet_metric_document.py`
     and `orca-harness/youtube_capture/behavioral_projection.py` (the
     source_surface consumer-filter invariant the new surface relies on);
   - the two lake probe evidence pointers named in the Goal section.
3. Declare `SOURCE_CONTEXT_READY` (or `SOURCE_CONTEXT_INCOMPLETE` with the
   missing sources) in the report.
4. APPLY deep thinking first — frame the boundary problem, failure modes, and
   decision criteria — then APPLY `workflow-code-review` findings-first.

## Adversarial Axes To Attack (be maximally adversarial within scope)

- **Metric honesty**: any path where an absent/unparseable feed field becomes
  0, a rounded value, or an invented timestamp; any OBSERVED posture without a
  real value; precision inflation of starRating→like_count semantics.
- **First-seen correctness**: baseline vs `true`/`false` semantics; the
  cumulative known-set union; `_latest_channel_states` newest-first scan —
  including the ULID lexical-order assumption, same-millisecond ordering, the
  availability-index dependency, and the silent-baseline fallback when a prior
  packet readback fails (is honest-but-silent the right trade? attack it).
- **Packet contract fit**: slice shape, Ob.15 closed vocabulary use,
  capture-level limitations vs slice limitations (posture-honesty gate),
  preserved_file_ids correctness.
- **Consumer isolation**: could any existing consumer ingest
  `youtube_channel_rss_feed` packets; does the surface name collide.
- **Run mechanics**: exit-code truthfulness (0/2/4), circuit-break streak
  logic, cooldown write/read, pacing, per-channel exception visibility,
  null-channel-id row handling.
- **Test fake-pass risk**: do `[runner-tests]` actually exercise the real
  packet write + readback; could a regression pass them; missing red paths.
- **Declarations**: `[seam-decl]`/`[inventory-decl]` accuracy (runner is a
  direct packet writer; a2_fork_impact `manifest_shape`).

## Output Contract (controller return)

- Durable report written to
  `docs/review-outputs/youtube_rss_monitor_delegated_adversarial_code_review_v0.md`
  carrying: `reviewed_by` (your vendor/model; operator-supplied; `unrecorded`
  if not supplied — never fabricated), `authored_by: Anthropic Claude (Claude
  Code lane)`, the reviewed head SHA, `SOURCE_CONTEXT_READY` state, findings
  (findings-first; severity `critical`/`major`/`minor` for priority only; each
  actionable finding carries `minimum_closure_condition` — required end state,
  not implementation instructions — and `next_authorized_action`),
  non-findings, not-proven boundaries, and validation output (real pytest
  results).
- Working-tree unified diff for accepted findings within the Named Target Set
  (each hunk prefixed with its label tag, e.g. `# [rss-runner]`), left
  UNCOMMITTED; plus per-change source citations — neutral in tone,
  decision-sufficient in substance, each carrying its label tag.
- One overall verdict + residual-risk note. On a design-level problem return
  `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial diff, findings
  only.
- No formal `PASS`, readiness, acceptance, or validation-status authority: the
  diff, citations, and verdict are decision input only. The commissioning CA
  adjudicates before anything is kept and may veto any change at its
  discretion, even an individually defensible one.
- Return/courier note for the adjudicator: close per
  `.agents/workflow-overlay/communication-style.md` → Review Adjudication Next
  Step (adjudicate findings/diff/verdict/residuals as claims; same-turn-close
  self-closable material issues; one batched land step; deep-think the 1-5
  material next moves). Template:
  `docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`.

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: none
  if_changed_reason: none
```

## Non-Claims

- Provisional convention: not a bound review lane, not validation, not
  readiness, not acceptance, not runtime model routing (vendor families above
  are a who-constraint and observed provenance only).
- The commission grants patch authority ONLY within the Named Target Set on the
  lane branch working tree; no commit, push, merge, install, deploy, or
  lifecycle action.
