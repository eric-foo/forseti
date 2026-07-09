# Data Lake v4.1 Assumption Gate Second-Opinion Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Second-opinion adversarial review of the fused-turn assumption gate that
  stopped v4.1 Source Capture runner implementation on (a) packet_shard named
  but undefined and (b) the v4.1 forward-epoch contract being branch-only, not
  on origin/main. Tests whether that stop is correct, overblocking, or
  mis-routed, and what the smallest complete next owner decision is.
use_when:
  - Deciding whether the v4.1 runner implementation gate should stay blocked,
    clear with named owner authorization, or reroute to a contract/spec decision.
  - Checking whether packet_shard (and anchor_shard) can be defaulted or must be
    owner-decided first.
  - Preparing the next Chief Architect decision before DataLakeRoot v4.1 work.
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/capture_runner_v4_1_blocker_adversarial_review_v0.md
  - docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - forseti-harness/data_lake/root.py
branch_or_commit: codex/ig-reels-capture-spine @ 49f8bc81
stale_if:
  - The v4.1 forward-epoch contract lands on origin/main, is rejected, or materially changes.
  - packet_shard, anchor_shard, lake_epoch, or orca-lake-epoch behavior appears in orca-harness.
  - DataLakeRoot root marker, raw pathing, staging, publishing, availability, or rebuild behavior changes.
  - Any Source Capture packet runner gains or loses --data-root / ORCA_DATA_ROOT support.
  - The fused assumption-gate decision is superseded by an owner decision.
authority_boundary: retrieval_only
```

## Body Opening

Purpose: a read-only second opinion on the fused-turn assumption gate that
stopped before implementing v4.1-friendly Source Capture runners. The question
under review is **not** "can it be implemented" but **"is the stop the right
decision, or is it overblocking / mis-reasoned?"** so a Chief Architect can make
one concrete next move.

Do not use for: implementation authorization, validation/readiness of the v4.1
contract or code, live-capture or live-root write authorization, Silver Vault
schema decisions, or a claim that the v4.1 contract is landed on `origin/main`.

Authority boundary: current user instruction, `AGENTS.md`, and
`.agents/workflow-overlay/` win. Code and read-only observations win over this
report when they drift.

Recheck recipe: rerun branch/HEAD/status on the main working tree (codex
branch); re-grep `packet_shard|anchor_shard|lake_epoch|orca-lake-epoch` across
`orca-harness`; reread `root.py`, the seam test, and the data-lake
availability/root tests; recheck whether the v4.1 contract is on `origin/main`;
recount packet producers and `data_root` seam exposure.

Non-claims: not validation, not readiness, not implementation authorization, not
approval to patch runners or `DataLakeRoot`, not permission to write/delete the
external root, not a claim the v4.1 contract is merged to `origin/main`, and not
acceptance of any specific shard grammar.

## Provenance

- `reviewed_by`: `claude-opus-4-8` (the model performing this review; observed
  from the runtime environment, not operator-supplied; observed provenance only,
  implies no model recommendation).
- `authored_by`: `unrecorded`. The "reviewed artifact" is a fused-turn gate
  *decision*, not a single authored file; the model that ran that fused turn was
  not supplied. The branch `codex/ig-reels-capture-spine` suggests a
  Codex/GPT-family actor, but that is an inference, not a recorded fact, so it is
  not asserted.
- This review was commissioned via a filed review prompt
  (`docs/prompts/reviews/data_lake_v4_1_assumption_gate_second_opinion_adversarial_review_prompt_v0.md`)
  on the source-read-only adversarial artifact review lane, **not** the
  delegated-review-patch convention, so no `de_correlation_bar` is bound.

## Commission, Target, Authority, Decision Criteria

- **Commission:** decide whether the fused assumption gate should remain blocked,
  clear with named owner authorization, or reroute to a narrower owner/spec/
  contract decision before implementation.
- **Review target (commission-bound):** the fused-turn assumption-gate *decision*
  to stop v4.1 runner implementation, with its two stated reasons — `packet_shard`
  named but undefined, and the v4.1 contract being branch-only (not on
  `origin/main`).
- **Authority:** read-only adversarial artifact review
  (`.agents/workflow-overlay/review-lanes.md:17-24`); reviewer may write only this
  report under `docs/review-outputs/adversarial-artifact-reviews/`; severity set
  `critical/major/minor` is **finding priority only** and creates no approval /
  validation / readiness / mandatory-remediation authority
  (`review-lanes.md:73-76`); `patch_queue_entry` is forbidden in this lane
  (`review-lanes.md:86-90`). Source hierarchy:
  `.agents/workflow-overlay/source-of-truth.md:14-27`.
- **Decision criteria — bound `fitness_reference` (an alignment axis attacked,
  not a pass bar):** goal = prevent the v4.1 runner implementation from baking in
  a wrong or unstable lake-path contract; done = the CA can make one concrete next
  decision (keep blocked / clear with named authorization / reroute to a precise
  spec or contract decision). The fitness reference is itself attacked in
  SO-01/SO-03 and the attack-question answers below.

## Method And Skill Status

- `workflow-deep-thinking`: REFERENCE-LOADed before source-load (neutral lens
  for the gate's failure modes: right-stop-wrong-reason / overblocking /
  durable-layout-invention / understated-residual-prerequisite / authority
  overstep / fitness-reference-itself-wrong), then APPLIED after
  `SOURCE_CONTEXT_READY`.
- `workflow-adversarial-artifact-review`: REFERENCE-LOADed, then APPLIED after
  source readiness. Two-phase critique (correctness then friction) used.
- Source-gated sequence honored: authority reads -> reference-load methods ->
  source-load task sources -> `SOURCE_CONTEXT_READY` -> apply
  (`.agents/workflow-overlay/prompt-orchestration.md:67-102`).

## SOURCE_CONTEXT_READY

Declared. All load-bearing cites were verified first-hand against current code at
the observed HEAD; no required source was missing for the verdict. The two
source/decision gaps (`packet_shard`/`anchor_shard` undefined; contract not on
`origin/main`) are reported as findings, not as a block on the verdict.

### Observed Workspace State (fresh checks, this review)

- Reviewed against the **main working tree** `C:\Users\vmon7\Desktop\projects\orca`
  on `codex/ig-reels-capture-spine` @ `49f8bc81`. The session's own auto-worktree
  is off `main` and does **not** contain the v4.1 sources, so the codex checkout
  is the correct read/write surface (matches the prompt's `isolation_decision:
  neither`).
- Branch advancement: the prompt-authoring HEAD `b82551f5` is an **ancestor** of
  `49f8bc81`; the only commit since is `49f8bc81 docs: add v4.1 assumption gate
  second-opinion prompt` (this prompt). **No v4.1 source changed** between prompt
  authoring and review.
- Dirty state: 18 unrelated untracked entries in the main tree; **zero tracked
  modifications**; none of the required review sources are untracked or modified.
  Required-source evidence is clean at `49f8bc81`.
- `origin/main`: the v4.1 forward-epoch contract is **absent**
  (`git cat-file -e origin/main:<path>` fails); the prior blocker review, the
  addendum, and this prompt are all codex-branch-only. (Confirms prompt-author
  observation.)
- Harness grep `packet_shard|anchor_shard|lake_epoch|orca-lake-epoch` across
  `orca-harness`: **zero matches** (confirms prompt-author observation; also
  confirms `anchor_shard` is absent).
- Runner counts re-derived first-hand: **12** packet-producing runners (producer
  tokens `write_local_source_capture_packet|stage_and_write_packet`), of which
  **3** carry the `data_root` seam (`run_source_capture_packet.py`,
  `run_source_capture_http_packet.py`,
  `run_source_capture_ig_reels_grid_packet.py`) and **9** are the
  `KNOWN_UNSYNCED` set exactly (confirms prompt-author observation 12/3/9).
- Live external root `F:\orca-data-lake` was NOT read (out of scope; the prior
  reviews' live-root counts are accepted as reported, not re-verified).

### Source-Read Ledger

| Source | Why read | Supports | Freshness |
| --- | --- | --- | --- |
| `orca/.../core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md` | The controlling contract; defines the sharded grammar + markers | Verdict, SO-01/02/03/04 | committed on-branch, clean; NOT on origin/main |
| `orca-harness/data_lake/root.py` | Verify v0 marker / unsharded refs / rebuild walk / derived addressing | Verdict, SO-02/03/04, non-findings | clean @49f8bc81 |
| `orca-harness/source_capture/writer.py` | Confirm raw-write path routes through DataLakeRoot unsharded | Verdict, SO-04 | clean @49f8bc81 |
| `orca-harness/source_capture/packet_assembly.py` | Confirm `stage_and_write_packet` seam has no shard/epoch logic | Verdict | clean @49f8bc81 |
| `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` | Verify producer/seam detection + 9-allowlist | Counts, non-findings | clean @49f8bc81 |
| `orca-harness/tests/test_data_lake_availability.py` | Verify v0 `raw_path` assertion + round-trip shape | SO-04, non-findings | clean @49f8bc81 |
| `orca-harness/tests/test_data_lake_root.py` | Verify v0 marker assertion + `raw/<pid>` assertions | SO-04, non-findings | clean @49f8bc81 |
| `docs/review-outputs/adversarial-artifact-reviews/capture_runner_v4_1_blocker_adversarial_review_v0.md` | Prior adversarial review (AR-01..AR-04) | SO-01/02/03, non-findings | committed, clean |
| `docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md` | Prior addendum + 5-step patch sequence | SO-02/03/04, non-findings | committed, clean |
| Authority overlay (`AGENTS.md`, README, source-of-truth, source-loading, decision-routing, artifact-roles, review-lanes, prompt-orchestration, validation-gates, communication-style, template-registry) + `orca_prompt_behavior_contract_v0.md` + `adversarial_artifact_review_v0.md` | Bind lane, roles, severity, source hierarchy, lock-in tiebreaker, YAML shape, non-claims | Whole review | clean @49f8bc81 |
| `git` branch/HEAD/status; `origin/main` cat-file; harness grep; runner-token grep | Fresh checks | Observed-state section | live @49f8bc81 |

Available, not read (not decision-bearing): `retrieval-metadata.md` (header
shape mirrored from the prior in-lineage review, which the EP-06 hook already
accepts), the live external root `F:\orca-data-lake` (out of scope).

## Verdict (Headline)

**The fused assumption gate's decision to STOP is correct and well-founded —
keep it — but narrow and re-reason it.** Recommendation `accept_with_friction`
refers to the *gate decision* (its stop is upheld under adversarial attack); it
is **not** acceptance of any implementation.

Two things hold up strongly under attack and are re-verified first-hand:

1. The **hard blocker is real**: the v4.1 contract mandates
   `raw/<packet_shard>/<packet_id>/` (`contract:95,167`) and
   `derived/<anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>.json`
   (`contract:103-104`) but defines **no derivation rule** for either shard;
   `orca-harness` has zero shard/epoch code (grep). A shard function is a
   **durable physical-layout primitive**: once packets are written under
   `raw/<shard>/<packet_id>/`, every path, availability ref, reader, and rebuild
   walk is baked to it, and changing it later means rewriting the layout. Under
   the Smallest Complete Intervention lock-in tiebreaker (`AGENTS.md:22-29`) and
   the complex-regime rule "resolve the highest-uncertainty assumption before
   expanding implementation" (`decision-routing.md:88-93`), this is an
   owner-grade decision the agent must **surface, not silently invent**. Stopping
   was the doctrinally-correct move.

2. The gate **did not overstep** by stopping. Surfacing a high-lock-in durable
   decision to the owner is exactly what the Operating Economy ("surface a risky
   assumption" — keep) and the lock-in tiebreaker ("pause and surface the
   tradeoff for a decision before proceeding") require. The overstep would have
   been to auto-pick a shard function and proceed.

The friction (findings) is calibration, not reversal: one of the gate's two
stated reasons is overstated (SO-01), a second undefined shard primitive is
missing from the prior framing (SO-02), the circulating default shard function
must not be adopted silently (SO-03), and the implementation surface is broader
than "name a shard" (SO-04) — so the cheapest correct unblock is **one bounded
owner decision recorded in the contract**, not indefinite block and not a full
fresh spec cycle.

No `critical` findings. Three `major` (correctness) and two `minor` follow,
correctness phase first.

## Findings

### SO-01 — Major (correctness) — "Not on origin/main" is overstated as a co-equal hard blocker

- Phase: correctness.
- Location: the gate's second stated stop reason ("contract exists on the branch
  but not on `origin/main`").
- Source authority: `source-of-truth.md:14-27` (hierarchy = user -> `AGENTS.md`
  -> overlay -> docs; **no rule requires a doc to be on `origin/main` to be
  authoritative**); contract status `V4_1_FORWARD_EPOCH_SELECTED_V0`, owner
  direction recorded 2026-06-28 (`contract:30-37`); control-plane source-state
  gate (`validation-gates.md:83-89`) blocks strict claims on *modified/untracked*
  controlling sources — the contract is now **committed and clean** on-branch,
  so that gate is satisfied.
- Issue: branch-only status is **not, by itself, a hard blocker** for
  branch-local implementation. The contract is a committed, owner-**selected**
  architecture contract; nothing in the source hierarchy demands mainline
  landing before work that lives on the same branch. Treating "not on
  `origin/main`" as a co-equal hard stop (alongside the genuine shard blocker)
  over-blocks: it implies the contract must merge to `main` before any
  implementation, when the owner can authorize branch-local work directly.
- Strongest reading (and why it still matters): branch-only **is** a real
  *rework risk* — the contract's own header is `stale_if` "the owner rejects the
  clean v4.1 epoch reset" (`contract:24`), so building against it before it
  settles can churn. The prior blocker review's AR-01 correctly framed this as a
  **named precondition the owner decides**, not an absolute block. It still
  matters because conflating a disclosed risk with a hard blocker changes the
  CA's menu: the honest unblock is "owner authorizes branch-local implementation
  against the selected contract," not "land the contract on `main` first."
- Impact: a CA could over-scope the unblock (wait for a mainline merge) when a
  one-line owner authorization suffices; or mis-weight the two stop reasons as
  equally hard.
- minimum_closure_condition: the gate (and any forward note) distinguishes the
  **hard blocker** (undefined durable shard grammar) from the **disclosed
  branch-only rework risk**, and the owner records whether branch-local
  implementation may proceed against the selected-but-unlanded contract.
- next_authorized_action: owner one-line decision authorizing (or declining)
  branch-local v4.1 implementation against the branch-committed contract; no
  patch authority granted here.
- not proven: whether/when the contract lands on `origin/main` (owner decision);
  red-green proof `not_applicable` (non-executable decision finding).

### SO-02 — Major (correctness) — `anchor_shard` is a second undefined durable shard primitive, unnamed by the prior framing and the gate

- Phase: correctness.
- Location: contract `derived/<anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>.json`
  (`contract:103-104`); current derived addressing `root.py:454-469`
  (`append_record` -> `derived/<raw_anchor>/<lane>/<record_id>`, **no
  anchor_shard, no lane_namespace rename**); harness grep `anchor_shard` zero.
- Source authority: the contract; `root.py`; repo grep.
- Issue: the gate, the prior blocker review (AR-02, titled solely "`packet_shard`
  derivation is undefined"), and the addendum (step 2 mentions only the *packet*
  shard helper, `addendum:184-186`) all focus on `packet_shard` for the `raw/`
  path. The contract independently shards the **`derived/`** path with
  `anchor_shard`, which is **equally undefined** and **equally durable**. Even
  after `packet_shard` is locked, the derived/Silver write path carries the
  identical undefined-grammar blocker — and would re-trigger the same gate when
  Silver Vault implementation begins. The contract also renames the derived
  middle segment `lane` -> `lane_namespace` without a stated semantic, a smaller
  parallel gap.
- Strongest reading (and why it still matters): the immediate fused scope was the
  **raw capture runner** path, so `anchor_shard` is arguably out of the *first*
  slice and deferrable to Silver Vault implementation. It still matters because
  (a) the owner shard decision should lock **one consistent scheme for both
  shards** in a single pass rather than discover `anchor_shard` later as a
  surprise, and (b) a review that names only `packet_shard` understates the
  contract's true undefined-primitive surface.
- Impact: a second durable-layout decision is currently invisible; locking only
  `packet_shard` leaves the derived side to re-block later, and risks two
  inconsistent shard schemes.
- minimum_closure_condition: the owner shard-grammar decision (and the contract
  record of it) covers **both** `packet_shard` and `anchor_shard` (and resolves
  `lane` vs `lane_namespace`), or explicitly scopes `anchor_shard` as a named,
  deferred Silver-Vault-phase decision rather than an unflagged gap.
- next_authorized_action: owner / contract-owner defines (or explicitly defers
  with a name) the `anchor_shard` grammar alongside `packet_shard`; no
  implementation authority granted here.
- not proven: whether the derived side is in or out of the first implementation
  slice (owner scope decision); red-green proof `not_applicable`.

### SO-03 — Major (correctness) — The circulating default "first 3 lowercase hex of sha256(packet_id)" must not be adopted silently; defensible only as an owner decision, and not obviously optimal

- Phase: correctness.
- Location: the candidate default named in the commission ("first three lowercase
  hex chars of `sha256(packet_id)`"); legacy live-root evidence `raw/67c/...`
  (prior blocker review AR-02, `...blocker_review_v0.md:204-217`); `packet_id`
  grammar `root.py:55-58` (Crockford base32, 26 chars).
- Source authority: the contract (clean-forward-epoch, abandons the legacy root,
  `contract:69-83,186-206`); `root.py`; the prior blocker review.
- Issue: adopting any shard function as a **silent agent default** is an
  unjustified durable-layout invention (the lock-in tiebreaker, `AGENTS.md:22-29`).
  As an **owner decision** the `sha256[:3]` candidate is defensible — it is a
  deterministic pure function of `packet_id` (so readers and `rebuild_availability`
  can locate a packet by key with no index), gives ~4096 even buckets, and
  matches the **width/alphabet** of the legacy `raw/67c/...` scheme — but it is
  **not obviously optimal**:
  - `packet_id` is already a high-entropy Crockford-26 ULID, so sharding on the
    **packet_id's own leading characters** (e.g. first 2 Crockford chars) is
    simpler, single-alphabet, and equally uniform — no `sha256` compute and no
    second (hex) namespace.
  - 3 hex chars = 4096 buckets **over-shards a ~242-packet lake** (mostly empty
    shard dirs); 2 chars / 256 buckets is likely ample at current scale.
  - Whatever is chosen must apply **consistently to both `packet_shard` and
    `anchor_shard`** (SO-02) and propagate to availability refs and the rebuild
    walk (SO-04).
- Strongest reading (and why it still matters): the prior blocker review's AR-02
  worried a naive helper "could silently diverge from the legacy `raw/67c/...`
  shape, compounding the mixed-layout problem." Under the **clean forward epoch**
  the new v4.1 root is separate and the legacy root is archived/abandoned
  (`contract:69-83,186-206`), so the new shard need **not** reproduce the legacy
  scheme — which *defuses* the legacy-divergence worry for the new epoch and
  makes the unblock **cheaper** than AR-02 implied (the owner need not
  reverse-engineer `raw/67c/...`; they pick a clean forward grammar). The
  residual that genuinely matters is only that the grammar is a durable
  forward choice and must be owner-locked.
- Impact: silently shipping `sha256[:3]` bakes an un-owned, possibly
  over-scaled, dual-alphabet layout into the new epoch; the decision is costly to
  roll back once packets exist.
- minimum_closure_condition: the owner locks the shard grammar (basis + width)
  for both shards, recorded in the controlling contract (the contract's own
  acceptance criterion 7 already requires "sharding and availability refs are
  explicit", `contract:257`); it is not silently invented by the implementer.
- next_authorized_action: owner picks the shard grammar (recommend evaluating
  packet_id-prefix vs `sha256`-prefix and 2 vs 3 chars); contract-owner records
  it; no implementation authority granted here.
- not proven: the origin/derivation of the legacy `raw/67c/...` entries (no
  current source identifies the writer); red-green proof `not_applicable`.

### SO-04 — Minor (correctness) — The implementation surface is broader than "name a shard"; this reinforces (does not weaken) the stop

- Phase: correctness.
- Location/evidence (all first-hand): marker bump + epoch marker — `root.py:40`
  (`ROOT_MARKER_CONTRACT_VERSION = "v0"`) and `LAKE_SUBDIRECTORIES`
  (`root.py:46-53`, no `.orca-lake-epoch.json`, no `silver_vault` substructure)
  vs `contract:138-159`; **three** unsharded raw-write entry points —
  `allocate_raw_packet_dir` (`root.py:413`), `stage_raw_packet` (`root.py:430`),
  `publish_raw_packet` (`root.py:444`) (AR-04 named this); availability strings —
  `raw_path`/`manifest_relpath` (`root.py:202-203`) and the **two-level rebuild
  walk** `rebuild_availability` (`root.py:702-723`, iterates `raw/` one level and
  `fullmatch`-es Crockford-26 on the child name — sharding breaks it); and the
  **test surface** — `test_data_lake_availability.py:45` asserts
  `raw_path == f"raw/{pid}"` plus ~6 assertions of `container == .../raw/<pid>`
  across the two test files, and `test_data_lake_root.py:92` ties the marker to
  the `v0` constant.
- Source authority: `root.py`, the two data-lake tests, the contract.
- Issue: largely consolidates what the addendum (step 2/3) and AR-04 already
  named, plus the specific `rebuild_availability` two-level-walk and test-surface
  breadth. The point for *this* review: the gate is correct that v4.1 is a
  multi-surface change (marker, epoch file, three raw entry points, availability
  refs, rebuild walk, ~6 test assertions), **not** a one-line shard insertion —
  which strengthens "don't rush past the owner decision into a deceptively small
  patch."
- Impact: low on the verdict; it sizes the work and guards against a thin patch
  that leaves an unsharded entry point or a broken rebuild behind.
- minimum_closure_condition: the eventual (separately authorized) v4.1
  `DataLakeRoot` patch covers all three raw-write entry points, the availability
  write/read/rebuild refs, the marker+epoch, and updates every test that locks
  the `raw/<pid>` / `v0` shape.
- next_authorized_action: fold this surface into the implementation-scoping
  refresh once the owner unblocks; no edit authorized here.

### SO-05 — Minor (friction) — The stop should be returned as a pre-loaded owner micro-decision, not a bare "blocked pending packet_shard"

- Phase: friction.
- Location: the gate's return shape (the stop itself).
- Source authority: Operating Economy (`AGENTS.md:45-75`: act-default on
  reversible work; surface a risky assumption; "reach the owner with the fewest
  ceremony steps per delivered unit").
- Issue: surfacing the high-lock-in fork is correct (verdict), but the *economy*
  of the stop matters. The cheapest path to the owner is a **crisp single
  decision pre-loaded with a recommendation and alternatives** — "lock the shard
  grammar: basis (packet_id-prefix vs `sha256`-prefix) and width (2 vs 3 chars),
  applied to both `packet_shard` and `anchor_shard`; confirm marker bump to
  `v4.1` + `.orca-lake-epoch.json` now" — rather than a bare "blocked: packet_shard
  undefined" that forces an extra round-trip for the owner to discover the
  decision shape.
- Strongest reading (and why it still matters): if the fused turn already
  returned the decision in this shape, this finding is satisfied and is a
  no-op note. It still matters as the standard the unblock hand-back should meet,
  and because under-specifying the stop is avoidable latency.
- Impact: low; a round-trip-economy refinement, not a correctness defect.
- minimum_closure_condition: the owner-facing hand-back states the shard-grammar
  decision as one bounded choice with a recommended default and named
  alternatives, plus the marker/epoch confirmation.
- next_authorized_action: when re-surfacing the gate, present the pre-loaded
  owner decision; no edit authorized here.

### Phase 2 (friction)

Beyond SO-05, no material friction findings. The gate is lean for its purpose;
its stop is justified by a genuine durable-layout decision, not avoidable
ceremony. No finding was invented to look thorough.

## Explicit Attack-Question Answers

1. **Is the assumption gate correctly blocking because `packet_shard` is
   undefined, or is a defensible rule already derivable from current sources?**
   **Correctly blocking.** No shard rule is derivable from current sources: the
   contract names `packet_shard` (and `anchor_shard`) but defines no derivation
   (`contract:95,103-104,167`); `orca-harness` has zero shard code (grep); and
   the legacy `raw/67c/...` scheme is "not a prefix of the packet_id" and "not
   reproducible from current sources" (prior blocker review AR-02). The rule must
   be **chosen** (owner) or **defined** (contract), and it is a durable,
   high-lock-in primitive — exactly an owner-grade decision (`AGENTS.md:22-29`;
   `decision-routing.md:88-93`).

2. **Is "not on `origin/main`" a real blocker here, or can the current branch
   contract plus owner "fused go" authorize branch-only implementation?**
   **It is not an independent hard blocker (SO-01).** The source hierarchy has no
   must-be-on-`main` rule (`source-of-truth.md:14-27`); the contract is committed
   and owner-**selected** (`contract:30-37`). Branch contract + owner "fused go"
   **can** authorize branch-only implementation. Branch-only remains a disclosed
   **rework risk** (the contract is `stale_if` the owner rejects it,
   `contract:24`), to be named — not a stop.

3. **Would "first three lowercase hex chars of `sha256(packet_id)`" be a safe
   default, a reasonable owner decision, or an unjustified durable-layout
   invention?**
   **All three, depending on who decides (SO-03):** an *unjustified invention* if
   adopted as a silent agent default; a *reasonable owner decision* (deterministic,
   rebuildable-by-key, ~4096 even buckets, legacy-width-compatible); but **not
   obviously optimal** — sharding on the packet_id's own Crockford prefix is
   simpler and single-alphabet, and 3 hex chars over-shards a ~242-packet lake.
   The clean-forward-epoch contract abandons the legacy root, so the choice need
   not reproduce `raw/67c/...`. Lock it as an owner decision recorded in the
   contract; do not default it silently.

4. **Is the right next step spec writing, owner decision, contract patch,
   implementation scoping refresh, or direct implementation with warnings?**
   **A bounded owner decision, recorded in the contract, then scoping refresh,
   then implementation** — in that order. Concretely: (i) owner locks the shard
   grammar for **both** shards (+ confirms marker bump/epoch now) and authorizes
   branch-local work; (ii) record the locked grammar in the contract (a small
   patch — acceptance criterion 7 already demands sharding be explicit,
   `contract:257`); (iii) refresh implementation scoping using the addendum's
   5-step sequence with AR-01/AR-02/AR-04 and SO-02/SO-04 folded in; (iv)
   implement `DataLakeRoot` v4.1 + tests. **Not** a full fresh spec cycle (the
   contract already specifies everything except the shard function); **not**
   direct implementation with warnings (that bakes an un-owned durable layout).

5. **Did the prior blocker review or addendum understate any prerequisite that
   should block fused even after `packet_shard` is defined?**
   **Yes — `anchor_shard` (SO-02).** The contract shards the `derived/` path with
   an equally undefined, equally durable `anchor_shard` that neither the addendum
   (packet-shard-only step 2) nor the blocker review (AR-02, packet_shard-titled)
   named; it re-blocks the derived/Silver write path after `packet_shard` is
   defined. Secondary, already-named residuals: the third unsharded raw-write
   entry point `allocate_raw_packet_dir` (AR-04) and the marker/epoch + rebuild +
   ~6-assertion test surface (SO-04). Test-root safety (the prior live-root write
   incident, addendum step 1) is a real *safety* prerequisite and was correctly
   named.

6. **Did the fused gate overstep its authority by stopping on a decision the
   owner could make in chat?**
   **No.** Stopping to surface a high-lock-in durable-layout decision to the owner
   is the doctrinally-mandated move (Operating Economy "surface a risky
   assumption"; lock-in tiebreaker "pause and surface the tradeoff for a decision
   before proceeding", `AGENTS.md:22-29,45-75`). The overstep would have been to
   auto-invent the shard. The only refinement is economy (SO-05): pre-load the
   owner decision with a recommendation and alternatives so the stop costs one
   round-trip, not two. Note the *opposite* risk: reading this gate as
   "overblocking" and pushing to auto-pick the shard would itself violate the
   lock-in tiebreaker.

## Non-Findings (Survived Adversarial Attack)

Recorded so the CA sees what was tested, not skipped:

- **Gate core stop is source-backed.** Zero shard/epoch code (grep); contract
  mandates the sharded path (`contract:95,167`); `root.py` emits a `v0` marker
  (`:40`) and unsharded refs (`:202-203`, `:413`, `:430`, `:444`). The stop is
  not a phantom.
- **No fake-success path.** The gate preserved real failure visibility — it did
  not silently invent a shard and claim "done." Consistent with the kernel's
  no-fake-success rule (`AGENTS.md:8`).
- **Implementation-gap is by design.** The contract's own DCP receipt lists
  `orca-harness/data_lake/root.py` under `intentionally_not_updated`
  ("Runtime implementation is intentionally not patched in this docs turn",
  `contract:299-302`) — the docs/implementation split is deliberate, so the gap is
  expected, and implementation is a separate authorized lane.
- **Prior blocker review verdict holds.** Its core finding (the addendum's
  blocker is source-backed and accurate) and counts (12 producers / 3 seam / 9
  unsynced) re-verified first-hand at `49f8bc81`.
- **Contract authority is settled enough.** The contract is committed and clean
  on-branch (not modified/untracked), so the control-plane source-state gate does
  not block strict reliance on it for branch work (`validation-gates.md:83-89`).

## Strict-Only Blockers / Not-Proven Boundaries

- This review upholds the *gate decision*; it does **not** validate the v4.1
  contract, prove readiness, or authorize implementation.
- The live external root `F:\orca-data-lake` was not read; the prior reviews'
  live-root counts are accepted as reported, not re-verified.
- The origin/derivation of the legacy `raw/67c/...` sharded entries is not
  established by any current source.
- Whether `anchor_shard` (the derived side) is in or out of the first
  implementation slice is an owner scope decision, not settled here.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness,
mandatory remediation, implementation authorization, or executor-ready patch
authority until separately accepted or authorized by the Orca owner / Chief
Architect. Severity labels are finding priority only. `accept_with_friction`
refers to the gate decision (its stop is upheld), not to any implementation. No
source file was edited and no patch was executed.
