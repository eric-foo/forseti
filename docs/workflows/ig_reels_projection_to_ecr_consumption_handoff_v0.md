# IG Reels-Grid Projection To ECR Consumption Handoff

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet (cold cross-lane)
scope: >
  Cold-reader handoff from the just-landed IG reels-grid Projection adapter to a fresh ECR
  (Evidence Candidate Record) source-side lane. The ECR lane's bounded job: decide whether
  existing ECR/SCR consumers need a reference to the projection ROW HANDLE or whether
  packet/slice keys already suffice -- by key, never by merging projection fields into ECR
  integrity posture fields. Projection, capture, Cleaning, and Judgment work are out of scope.
use_when:
  - Continuing the ECR source-side lane's consumption check for IG reels-grid projection rows.
  - Checking what may be referenced by key from the projection adapter without lane blur.
  - Preventing projection fields or ad/sponsorship/demand/credibility/integrity conclusions
    from entering ECR posture fields.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/ecr_spine_submap_v0.md
  - forseti-harness/source_capture/ig_reels_grid_projection.py
  - docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - The IG reels projection row contract (row_id / raw_ref / raw_anchor / join_status /
    source_surface_count_candidates) changes shape.
  - ECR/SCR carry-or-residualize, reference-never-merge, or one-record-per-kind discipline changes.
  - The owner revives SCR as a default pre-Judgment layer or unfreezes the JSG-01 reserved architecture.
```

## Load Contract

- packet_version: workflow-handoff-v1
- mode: max
- created_at: 2026-06-25 (authored; see Workspace State for the volatile working-tree facts)
- created_by_lane: Claude Projection-lane implementation/closeout lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca` (the canonical repo where orca-harness is tracked and checked out)
- handoff_path: `docs/workflows/ig_reels_projection_to_ecr_consumption_handoff_v0.md`
- expected_branch: `codex/ig-reels-capture-spine` (the IG capture lane; orca-harness is TRACKED here)
- expected_head: `4162f6e2` (the projection-adapter commit) -- HEAD may have advanced; re-verify.
- expected_dirty_state_including_handoff_file: dirty working tree. The adapter + its test carry
  uncommitted refinements beyond `4162f6e2` (see Superseded), other unrelated codex-lane files are
  dirty/untracked, and THIS handoff file is newly created (untracked) on write.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target
  before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Build Orca social-source capture and downstream evidence plumbing that can
  monitor public creator/content traction without confusing raw Capture, Projection, ECR,
  Cleaning, or Judgment responsibilities.
- anchor_goal: Decide how the ECR source-side spine relates to the new IG reels-grid projection
  rows -- reference the projection ROW HANDLE by key, or rely on existing packet/slice keys --
  without merging any projection field into ECR integrity posture fields.
- success_signal: A cold ECR lane re-opens the ECR submap and the projection adapter and either
  (a) confirms packet_id/slice_id keys already suffice and records that, or (b) adds a by-key
  reference to the projection row handle -- with NO projection field copied into SP-1/2/3/6
  posture fields and NO interpretive meaning authored from projection prose.

## Open Decision / Fork

- decision: Do existing ECR/SCR consumers need a reference to the projection ROW HANDLE
  (`row_id` and/or `raw_ref{packet_id,slice_id}`), or do the packet_id/slice_id keys they already
  key to raw suffice?
  - options:
    1. Keys suffice: ECR postures key to raw by packet_id/slice_id (as today); record that the
       projection row is a keyed sibling over the same raw, reachable by the same keys, and add
       nothing.
    2. Add a by-key reference: a named ECR/SCR consumer that must point at the reconciled
       source-surface view stores the projection `row_id` (or `raw_ref`) as a reference only.
  - already constrained / off the table: reference-never-merge -- the projection's
    `source_surface_count_candidates`, `chosen_source_surface`, `selection_*`, and
    `source_visible_fields` must NOT be copied into ECR integrity posture fields
    (SP-1 identity / SP-2 inspectability / SP-3 timing-cutoff / SP-6 source-visibility). No
    ad/sponsorship/demand/credibility/integrity/Decision-Strength/Action-Ceiling conclusion may
    enter ECR. Do NOT author a new derived-record kind without owner authorization.
  - trade-offs: Option 1 is lowest lock-in (no schema/reference surface added; the projection row
    is re-derivable on read and already keyed to raw). Option 2 adds a durable reference handle
    only where a consumer genuinely needs the reconciled view, at the cost of a new reference field.
  - owner of the call: current Orca owner / current receiving ECR-lane user instruction.
  - recommendation and why: Start at Option 1. The ECR postures key to RAW, and the projection is
    a keyed sibling over that same raw (projection doctrine OD-1: keyed siblings over raw, neither
    owns the other). A row-handle reference is only warranted if a named consumer must point at the
    reconciled source-surface disagreement view specifically -- and even then by key/reference,
    never by field copy. Confirm against the actual `orca-harness/ecr/` consumers before adding any
    reference.

## Drift Guard

- Reference, never merge. ECR/SCR references provenance and projection BY KEY (one-directional);
  it never collapses projection fields into integrity posture fields.
  - why it matters: ECR integrity postures (SP-1/2/3/6) answer "can I trust the saying"; projection
    answers "what the mechanical source-visible rows are." Merging blurs the lanes.
  - what violating it would break: an ECR posture would carry projection-derived content, making the
    integrity read non-re-derivable and lane-contaminated.
- Carry-supplied-or-residualize; never author from prose. Every ECR field is carried from a frozen
  input or emitted as a named residual; no deriver classifies or infers interpretive values.
- No Judgment conclusions in ECR. Ad/sponsorship/paid-comment/demand/credibility/artificial-
  amplification/Decision-Strength/Action-Ceiling are Judgment-owned, never ECR.
- SCR (Signal Content Record) is deprecated/dormant as a default pre-Judgment layer (PR #375). Do
  NOT revive SCR to "consume" projection; the default route is evidence pack -> Judgment-authored
  interpretation.
- JSG-01 gate ownership and the reserved final Evidence Unit field architecture are owner-reserved
  and unchanged by this packet; nothing here authorizes a run or widens that architecture.
- The projection adapter is `view_only; not_cleaned; not_normalized; not_judgment_ready`. ECR must
  not treat it as authority over raw; raw stays canonical.
- TikTok/YouTube and Cleaning/Judgment design are out of scope for this packet.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` -- use the
  **ECR Source-Side Spine Read Pack** (front door = `docs/workflows/ecr_spine_submap_v0.md`).
- targets to enter the ladder:
  - `docs/workflows/ecr_spine_submap_v0.md` (cross-kind invariants + owner routing)
  - `orca-harness/source_capture/ig_reels_grid_projection.py` (the projection row contract to reference)
  - `orca-harness/ecr/` (the built ECR integrity derivers SP-1/2/3/6 -- the actual consumers to check)
  - `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md` (the upstream split packet)
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- already loaded (weak orientation only; not authority): this packet, the projection adapter + its
  test, the ECR submap, the projection doctrine, the IG capture->projection handoff. All read on
  2026-06-25 against the codex-lane ($ROOT) copies.
- must load first (before strict or actionable steps): `AGENTS.md`, `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/source-loading.md`, the ECR submap, and the projection adapter row contract.
- load rule: receiver re-runs progressive source loading per the overlay; this packet's loaded set
  only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- Projection is a mechanical, re-derivable VIEW over raw (no salience, no downstream effects,
  carry-or-residualize). The IG reels adapter re-attaches the cross-surface count disagreement
  (DOM / clips_user / web_profile_info) the capture slice collapsed, and carries `chosen_source_surface`
  by value-match (decision-free), `join_status`, selection audit, and `view_only` certification.
  - decided in: `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
    (Rules 1/7/9/10) and the adapter module docstring.
  - compare target: projection doctrine SHA256 `BE22FD65CB9D6D31682D74847631C51E766D01BD0A86063B65585CC994F6CDC0`;
    adapter -> commit `4162f6e2` + `reread-required` (working tree in flux).
  - verify before: any strict claim about what the projection emits.
- ECR records are siblings over raw, reference BY KEY, follow carry-supplied-or-residualize, and are
  re-derived-not-migrated; one derived record per epistemic kind, composed by the Evidence Unit, never merged.
  - decided in: `docs/workflows/ecr_spine_submap_v0.md` ("The Spine In One Screen" invariants 1-5).
  - compare target: SHA256 `B1F2BD6D10B05D53F22052349784B3C0802E47A8A155AC81E43CE9CCDD2494A1`.
  - verify before: deciding keys-vs-handle or touching any ECR deriver.
- Cleaning owns non-destructive transformation mechanics only; Judgment owns credibility, exclusion,
  demand, integrity effect, Decision Strength, and Action Ceiling.
  - decided in: `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`.
  - compare target: SHA256 `3D50EEA84071490B563A36ABE37F974654A820274EFD767FFB37FFAB05F2509D`.
  - verify before: any cross-layer claim.

## Active Objective

Determine, for the ECR source-side spine, whether any existing ECR/SCR consumer needs a by-key
reference to the new IG reels-grid projection rows, or whether the packet_id/slice_id keys already
suffice -- and record the decision (or make the bounded by-key reference change) without merging
projection fields into ECR posture fields or authoring interpretive meaning.

## Exact Next Authorized Action

1. Source-load the ECR submap (`docs/workflows/ecr_spine_submap_v0.md`), the projection adapter
   (`orca-harness/source_capture/ig_reels_grid_projection.py`; baseline commit `4162f6e2`, then reread
   the working tree for the current `join_status` value set), and the upstream split packet
   (`docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md`).
2. Enumerate the actual ECR/SCR consumers in `orca-harness/ecr/` (SP-1/2/3/6 derivers + models) and
   `orca-harness/signal_content/` (retained, dormant); for each, check what it keys to today
   (packet_id/slice_id over raw) and whether any consumer must point at the reconciled projection view.
3. Decide the Open Decision fork: Option 1 (keys suffice -- record it, change nothing) or Option 2
   (add a by-key reference to the projection `row_id`/`raw_ref` for a named consumer). Do NOT copy any
   projection field into an ECR posture field.
4. Validation / stop condition: if code changes, run `python -m pytest orca-harness/tests/unit/test_ecr_*`
   plus the IG projection suite (`tests/unit/test_source_capture_ig_reels_projection.py`); if doc-only,
   `git diff --check` over the touched files. Stop and surface if any consumer would require merging a
   projection field into a posture field (that is a Drift-Guard violation, not a patch).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (Orca kernel); `.agents/workflow-overlay/README.md` + `source-loading.md`.
- Overlay authority: `.agents/workflow-overlay/` (ECR Source-Side Spine Read Pack owns the ECR read route).
- User constraints: continue the ECR lane "1 by 1" after the Projection lane; reference-never-merge; no lane blur.
- Source-read ledger (compare targets are the canonical codex-lane / $ROOT copies):
  - `docs/workflows/ecr_spine_submap_v0.md`
    - Role: ECR source-side front door + cross-kind invariants. Load-bearing: yes.
    - Compare target: SHA256 `B1F2BD6D10B05D53F22052349784B3C0802E47A8A155AC81E43CE9CCDD2494A1`.
    - Last checked: 2026-06-25. Reuse rule: reread before any ECR change.
  - `orca-harness/source_capture/ig_reels_grid_projection.py`
    - Role: the projection adapter whose row contract ECR may reference. Load-bearing: yes.
    - Compare target: commit `4162f6e2` (immutable baseline) + `reread-required` -- the working tree
      carries uncommitted refinements (the `join_status` Literal was widened to include
      `missing_shortcode` and `ambiguous`; row fields are otherwise stable). Do not pin a working-tree hash.
    - Last checked: 2026-06-25. Reuse rule: reread the working tree; reference the row HANDLE by key only.
  - `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md`
    - Role: upstream split packet (Capture -> Projection/ECR/Cleaning). Load-bearing: yes (but see Superseded).
    - Compare target: SHA256 prefix `2ED2A581EF1D0027...` ($ROOT/codex copy; differs from the worktree copy).
    - Last checked: 2026-06-25. Reuse rule: orientation; its "no projection adapter implemented" gap is STALE.
  - `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
    - Role: projection view contract (mechanical/no-salience/carry-or-residualize). Load-bearing: yes.
    - Compare target: SHA256 `BE22FD65CB9D6D31682D74847631C51E766D01BD0A86063B65585CC994F6CDC0`.
    - Last checked: 2026-06-25. Reuse rule: reread before any projection<->ECR boundary claim.
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
    - Role: Data/Cleaning/Judgment boundary. Load-bearing: yes.
    - Compare target: SHA256 `3D50EEA84071490B563A36ABE37F974654A820274EFD767FFB37FFAB05F2509D`.
    - Last checked: 2026-06-25. Reuse rule: reread before cross-layer claims.
- Source gaps: this packet did NOT enumerate the actual `orca-harness/ecr/` consumers' fields -- that is
  the ECR lane's Action 2. No ECR code was changed.
- Strict-only blockers: any merge of a projection field into an ECR posture field; any new derived-record
  kind; any SCR revival -- all owner-gated.
- Not-proven boundaries: no ECR consumption of IG projection rows is implemented or reviewed; no Evidence
  Unit binding; no JSG-01 run; no ad/sponsorship/demand/credibility classification.

## Current Task State

- Completed: IG reels-grid projection adapter built, adversarially reviewed + patched, and committed
  (`4162f6e2`) on `codex/ig-reels-capture-spine`; IG suite green at last check (41 passed). Raw-vs-projected
  data shape demonstrated.
- Partially completed: ECR consumption boundary is identified (this packet) but NOT decided or patched.
- Broken or uncertain: the adapter + its test are in ACTIVE working-tree flux (hash changed between reads
  this session); re-read the current file rather than trusting any pinned working-tree hash.

## Workspace State

- Branch: `codex/ig-reels-capture-spine`.
- Head: `4162f6e2` at authoring (may have advanced -- re-verify with `git -C <workspace> rev-parse --short HEAD`).
- Dirty or untracked state before handoff: adapter + test carry uncommitted refinements beyond `4162f6e2`;
  other unrelated codex-lane files are dirty/untracked (pre-existing IG-lane work, not this packet's).
- Dirty or untracked state after writing the handoff file: this file
  (`docs/workflows/ig_reels_projection_to_ecr_consumption_handoff_v0.md`) is newly created and untracked.
- Target files or artifacts: `orca-harness/ecr/` (the ECR lane's actual edit/inspect surface).
- Related worktrees or branches: a `claude/awesome-driscoll-16c6c2` worktree exists but its `orca-harness`
  is an empty stub and its doctrine docs have DRIFTED hashes -- do NOT use it as the ECR workspace
  (see Superseded). `main` has diverged from `codex` (harness + doctrine); merge debt is the codex lane's.

## Changed / Inspected / Tested Files

- `orca-harness/source_capture/ig_reels_grid_projection.py`
  - Status: committed (`4162f6e2`) + uncommitted working-tree refinement. Role: the projection adapter.
  - Important observations: emits `IgReelsGridProjectionRow` with `row_id`, `raw_ref{packet_id,slice_id}`,
    `raw_anchor{file_id,relative_packet_path,sha256,hash_basis,json_pointer}`, `metric/posture/value`,
    `chosen_source_surface`, `source_surface_count_candidates[]`, `join_status`, `selection_policy_version`,
    `selection_limitations`, `source_visible_fields`, `residuals`; `certification` view_only. These are the
    handles ECR may reference BY KEY -- not fields to copy.
- `orca-harness/tests/unit/test_source_capture_ig_reels_projection.py`
  - Status: committed (`4162f6e2`) + uncommitted refinement. Role: the adapter's tests (currently 41 passed total in the IG suite).

## Frozen Decisions

- The projection adapter exists and is committed (`4162f6e2`); its row-handle fields are the reference
  surface. Evidence: `git log`/`git show 4162f6e2`. Consequence: the ECR lane references it, does not rebuild it.
- Reference-never-merge and carry-or-residualize are doctrine, not preferences. Evidence: ECR submap invariants 1+3.
- SCR is deprecated/dormant as a default pre-Judgment layer (#375). Consequence: do not route projection through SCR.

## Mutable Questions

- Keys-vs-handle (the Open Decision). Why still mutable: depends on the actual `orca-harness/ecr/` consumers'
  needs, which this packet did not enumerate. What would resolve it: Action 2 (inspect the consumers).
- Whether any ECR consumer must point at the reconciled source-surface view specifically. What would resolve
  it: reading the SP-1/2/3/6 deriver inputs against the projection row handle.

## Superseded / Dangerous-To-Reuse Context

- Upstream packet claim "no downstream IG creator-grid projection adapter was implemented": STALE. The
  adapter now exists (`orca-harness/source_capture/ig_reels_grid_projection.py`, committed `4162f6e2`).
  Current replacement: this packet + the committed adapter.
- The `claude/awesome-driscoll-16c6c2` worktree's `orca-harness` (empty stub) and its DRIFTED doctrine
  hashes (ECR submap `C945C079...`, projection `81AE300C...`): NOT the canonical state. Dangerous to use as
  the ECR workspace. Current replacement: the `codex/ig-reels-capture-spine` checkout at workspace root,
  whose ECR submap is `B1F2BD6D...` and projection doctrine `BE22FD65...` (matching this ledger).
- "orca-harness is gitignored": FALSE/misdiagnosed. `.gitignore` ignores only ephemeral subdirs
  (`_scratch/`, `_test_runs/`, caches, `reports/`, `memory/logs/`, ...); the harness source is tracked
  (codex 917 files). Landing = ordinary `git add` on the codex lane.

## Commands And Verification Evidence

- Command:
  ```bash
  python -m pytest tests/unit/test_ig_reels_grid.py tests/unit/test_source_capture_ig_reels_grid_packet.py \
    tests/unit/test_source_capture_ig_projection.py tests/unit/test_source_capture_ig_reels_projection.py -q
  ```
  Result:
  - Passed/failed/not run: passed (41 passed at last run, 2026-06-25, from `orca-harness/`).
  - Re-run target so the receiver can confirm rather than trust: re-run the same command after re-reading the
    (in-flux) adapter; expect green.
- Command:
  ```bash
  git -C C:/Users/vmon7/Desktop/projects/orca show --stat 4162f6e2
  ```
  Result: the 2-file projection-adapter commit (+1225 lines) on `codex/ig-reels-capture-spine`. Re-run to confirm the baseline exists.

## Blockers And Risks

- Risk: adapter/test in active working-tree flux. Evidence: file hash changed between two reads this session
  (`72ef72b2...` -> `4685309f...`). Likely next action: reread the current file; do not pin a working-tree hash.
- Risk: `main` <-> `codex` divergence (harness: 32 files only on main + 40 differing; doctrine docs differ too).
  Evidence: `git diff --name-status main codex/ig-reels-capture-spine -- orca-harness`. Likely next action: the
  codex lane owner rebases/merges main before landing; the ECR lane should work on codex and re-verify doctrine
  hashes against this ledger, not against the worktree.
- Blocker (hard): any ECR consumer that would require merging a projection field into a posture field -- stop and
  surface to the owner; that is a doctrine violation, not a patch.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - branch/head and dirty state of the workspace;
  - the projection adapter's current row contract (reread the in-flux file; baseline `4162f6e2`);
  - ECR submap invariants (reference-never-merge / carry-or-residualize / one-record-per-kind);
  - projection doctrine mechanical-only/no-salience rules;
  - the actual `orca-harness/ecr/` consumer fields (not enumerated here).
- Compare target for each: the SHA256s in Authority And Source Ledger; commit `4162f6e2`; fresh
  `git rev-parse --short HEAD`; fresh `git status --short --branch`; rerun the IG projection suite if code changes.
- Load outcomes and what each means:
  - `REUSE`: all load-bearing facts re-verified; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: only non-load-bearing facts drifted; reuse verified boundaries, refresh the rest.
  - `STALE_REREAD_REQUIRED`: material source drifted (expected for the in-flux adapter) but can be reread/re-derived.
  - `BLOCKED_DRIFT`: drift conflicts with scope/ownership (e.g., a consumer needs a field-merge) -- stop.
  - `BLOCKED_MISSING_PACKET`: this file absent/unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim lacks a compare target and cannot be re-derived.
- Sources that must be reread if drift is detected: ECR submap, projection doctrine, Data/Cleaning boundary,
  the projection adapter, and the affected `orca-harness/ecr/` derivers/tests.

## Do Not Forget

ECR references provenance and projection BY KEY and carries-or-residualizes; it never merges projection fields
into SP-1/2/3/6 posture fields and never authors meaning from projection prose. Projection is `view_only`; raw
stays canonical. SCR stays dormant. Work the ECR lane on the `codex/ig-reels-capture-spine` checkout at the
workspace root -- NOT the drifted worktree -- and re-verify doctrine hashes against this ledger before strict claims.
