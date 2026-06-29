# Handoff Packet — Fragrance Purchase-Review Capture Lane (completion → next unit)

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff
scope: >
  Cold completion handoff for the fragrance purchase-review CAPTURE lane after
  PR #489 merged; carries the lane's done-state and routes the next unit (the
  typed Attachment Record entry on the data-lake lane).
use_when:
  - Picking up or routing the fragrance purchase-review lane now that its
    capture objective is done and merged.
  - Scoping the typed Attachment Record entry that must reference/supersede the
    fragrance preserved bodies without inheriting positional file_id semantics.
  - Checking what the fragrance review lake tee pilot does and does NOT claim.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-06-30
- created_by_lane: claude/fragrance-review-lake-pilot (sender; provenance only, not authority)
- workspace: `C:\Users\vmon7\Desktop\projects\orca` (Orca repo; this packet was authored from worktree `.claude/worktrees/distracted-newton-1323ec`)
- handoff_path: `docs/workflows/fragrance_purchase_review_capture_lane_handoff_v0.md`
- expected_branch (where this packet lands): `claude/fragrance-review-lane-handoff` (a docs-only branch off `origin/main`); **the receiver's NEXT unit starts off `origin/main`, not this branch**
- expected_head (of `origin/main` at handoff): `54c7dc1a` (Merge pull request #489)
- expected_dirty_state_including_handoff_file: this file is newly created → untracked until committed on the docs branch; the merged lane code is clean on `origin/main`
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: durably preserve replayable raw review evidence in the off-tree Orca data lake so a typed, discoverable evidence record can later be built from it — the source-capture discipline, beyond fragrance.
- anchor_goal: the recommended next unit is the **typed Attachment Record (AR) entry on the DATA-LAKE lane** that references/supersedes the fragrance preserved bodies this lane shipped. (Owner routes; see Open Decision.)
- success_signal: a typed AR entry exists that satisfies its own contract's acceptance checks and can reference the merged preserved bodies **without inheriting the positional `file_id` or any staging-path semantics**, round-tripping the provenance the tee pilot deliberately left unattributed.

## Open Decision / Fork

- decision: what is the next unit now that the capture lane's objective is done and merged?
  - options:
    1. **Typed AR entry (DATA-LAKE lane)** — build the durable typed record over the preserved bodies. Highest value, highest lock-in (sets a durable schema).
    2. **Background chip `task_816ff6af`** — "Extend fragrance companion auto-fallback to Yotpo v3" (capture lane). Owner-owned.
    3. **Broader tee proof (capture lane, optional)** — multi-widget-per-PDP, pagination, the second (coverage) producer, wiring the live companion capture to auto-tee.
    4. **Park the lane** — the active objective is complete; no further work required now.
  - already constrained / off the table: the typed AR entry is **not** capture-lane work; do not build it inside this capture lane. The tee pilot makes **no** AR-physicalization / 7-AR-checks / closure claim.
  - trade-offs: option 1 is the most valuable but is high-lock-in (durable schema) → an architecture/contract pass should precede implementation; its contract doc explicitly "does not authorize runtime implementation," so it needs a bounded authorization first. Options 2–3 are smaller, lower-lock-in. Option 4 is valid (clean stopping point).
  - owner of the call: human owner / Chief Architect.
  - recommendation: option 1, **preceded by an architecture/contract pass** (e.g. `workflow-architecture-planning`) and a bounded build authorization, because it sets a durable, costly-to-reverse schema.

## Drift Guard

- Do NOT claim the merged tee pilot is a typed Attachment Record, AR physicalization, the data-lake "7 AR checks," or closure — it preserves raw bytes + re-derives a coverage view, proven on ONE synthetic fixture only.
  - why it matters: that exact over-claim was caught and corrected in this thread (a GPT-5.5 cross-vendor review); re-asserting it re-introduces a known internal inconsistency.
- Do NOT auto-start the owner-owned chip `task_816ff6af` (Yotpo v3 fallback). It is owner-owned.
- The typed AR entry is DATA-LAKE-lane work, not capture — building it in the capture lane violates lane ownership and the lock-in tiebreaker.
- Start any new unit on a NEW branch/worktree off updated `origin/main` (`54c7dc1a`); the sender branch `claude/fragrance-review-lake-pilot` is SPENT (PR #489 merged; remote branch may be deleted).
- The harness runs via `uv` and must ALWAYS use `--frozen` (a non-frozen `uv run` once mutated `uv.lock`); add `--with pytest` for tests, `--with certifi` for live TLS.
- The AR contract doc "does not authorize runtime implementation" — an architecture/contract pass + a bounded build authorization must precede any AR-entry implementation.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/README.md` (read before project work, per `AGENTS.md`); repo-map entry point `docs/workflows/orca_repo_map_v0.md`. Not zero-config — overlay-bound.
- targets to enter the ladder (for the recommended AR-entry unit): the AR contract doc; the retail-PDP lake precedent; `data_lake/root.py`; the merged fragrance tee module (all named in the ledger below).
- already loaded (weak orientation; not authority): this packet + the merged PR #489 diff.
- must load first (before strict/actionable AR-entry steps): the AR contract doc + the retail precedent + `data_lake/root.py`, reread against current `origin/main`.
- load rule: receiver re-runs progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- Decision: the AR work was **downgraded** from "AR physicalization that proves the 7 acceptance checks" to a **"capture-lane preserved-body tee pilot"** that makes no AR-closure claim, after a GPT-5.5 cross-vendor adversarial review found the over-claim.
  - decided in: this thread; now embodied in merged PR #489 (`git show 54c7dc1a`) and its commit messages.
  - compare target: `reread-required` (read the merged `fragrance_review_lake.py` module docstring on `origin/main`, which states the claim ceiling + named residuals).
  - verify before: any strict claim about what the lake currently provides for fragrance.
- Decision: the tee preserves `body_text.encode("utf-8")` and gates each body against the companion's independent capture-time witness (`body_sha256`/`body_byte_count`) — an admission gate added in review.
  - decided in: PR #489 commit `af35b8a7`.
  - compare target: `reread-required` (`_verify_capture_witness` in `fragrance_review_lake.py`).
  - verify before: relying on the "exact capture-time bytes" property.

## Active Objective

The fragrance purchase-review CAPTURE lane's active objective — capture review-positive retailer PDPs and durably preserve their review-widget evidence in the lake — is **complete and merged**. This packet hands off a clean completion point so the owner can route the next unit (recommended: the typed AR entry on the data-lake lane).

## Exact Next Authorized Action

1. Owner decides the next unit from Open Decision (recommended: typed AR entry, data-lake lane).
2. If option 1: start a NEW branch/worktree off `origin/main` (`54c7dc1a`); run an architecture/contract pass against `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` and obtain a bounded build authorization BEFORE implementing.
3. Stop condition: do not begin AR-entry implementation without the architecture pass + bounded authorization (the contract doc does not authorize runtime implementation).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (kernel) + `.agents/workflow-overlay/` (README, decision-routing, artifact-folders, validation-gates, safety-rules).
- Overlay or equivalent authority: capture-lane authority covered the shipped work; the AR entry needs DATA-LAKE-lane authority + the contract doc below.
- User constraints: owner routes the next unit; do not auto-start the owner-owned Yotpo chip.
- Source-read ledger:
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
    - Role: the AR entry's required shape + 7 acceptance checks; defers layout/serialization/backend; "does not authorize runtime implementation".
    - Load-bearing: yes
    - Compare target: `reread-required` (present on `origin/main` `54c7dc1a`, verified via `git cat-file -e`).
    - Last checked: 2026-06-30 (existence only).
    - Reuse rule: reread in full before any AR-entry architecture/build claim.
  - `orca-harness/source_capture/retail_pdp_projection.py` (`project_retail_pdp_into_lake`) + `orca-harness/tests/test_retail_pdp_lake_pilot.py`
    - Role: the ratified lake-pilot precedent the fragrance tee mirrors.
    - Load-bearing: yes
    - Compare target: `reread-required` (HEAD-bound to `origin/main` `54c7dc1a`).
    - Reuse rule: reread before mirroring for the AR entry.
  - `orca-harness/data_lake/root.py`
    - Role: lake substrate — `load_raw_packet` (fail-closed re-hash), `append_record`, `rebuild_availability` (packet-grained), `for_test`.
    - Load-bearing: yes
    - Compare target: `reread-required` (HEAD-bound `54c7dc1a`).
    - Reuse rule: reread before AR-entry storage decisions.
  - `orca-harness/source_capture/fragrance_review_lake.py` + `runners/run_fragrance_review_lake_packet.py` + `tests/test_fragrance_review_lake_pilot.py`
    - Role: the shipped tee pilot the AR entry must reference/supersede.
    - Load-bearing: yes
    - Compare target: `reread-required` (merged into `origin/main` `54c7dc1a` via PR #489).
    - Reuse rule: reread the module docstring (claim ceiling + named residuals) before stating what the lake provides.
  - `orca-harness/source_capture/packet_assembly.py` (`stage_and_write_packet`) + `tests/contract/test_capture_runner_lake_seam_coverage.py` + `tests/contract/test_source_capture_packet_no_runtime_imports.py`
    - Role: the in-memory-bytes tee seam + the two contracts any new packet-producing runner must satisfy.
    - Load-bearing: yes
    - Compare target: `reread-required` (HEAD-bound `54c7dc1a`).
    - Reuse rule: a new packet-producing runner needs the `--data-root` seam and must stay import-clean.
- Source gaps: none blocking. The AR entry's layout/serialization/backend are deferred by its contract (a decision the architecture pass must make).
- Strict-only blockers: AR-entry implementation is blocked until an architecture/contract pass + bounded authorization exist.
- Not-proven boundaries: the tee pilot proves ONE fixture's preserved-body invariants only — not multi-variant, pagination, or full projection fidelity.

## Current Task State

- Completed: Option A product-corpus pilot (4/5 retailers); Option B discovery layer (PR #481); preserved-body tee pilot (PR #489, merged `54c7dc1a`), cross-vendor reviewed + hardened.
- Partially completed: none.
- Broken or uncertain: none. (The `api.judge.me` burst-throttle that dropped Indigo was a session/IP artifact, not a code defect.)

## Workspace State

- Branch: `claude/fragrance-review-lake-pilot` @ `af35b8a7` is SPENT (PR #489 merged). This packet is authored on docs branch `claude/fragrance-review-lane-handoff` off `origin/main`.
- Head: `origin/main` @ `54c7dc1a`.
- Dirty or untracked state before handoff: clean.
- Dirty or untracked state after writing the handoff file: this file untracked (then committed on the docs branch).
- Target files or artifacts: the merged tee (3 files) + repo map; this handoff doc (new).
- Related worktrees or branches: many concurrent Orca lanes (see `git worktree list`); none block the next unit.

## Changed / Inspected / Tested Files

- `orca-harness/source_capture/fragrance_review_lake.py`
  - Status: merged (`54c7dc1a`).
  - Role: the tee (`write_fragrance_review_capture_packet`) + projection (`project_fragrance_review_into_lake`) + `PROJECTION_FRAGRANCE_REVIEW_LANE`.
  - Important observations: import-clean (TYPE_CHECKING-only for `DataLakeRoot`/`FragranceWidgetResponseCapture`); capture-time admission gate `_verify_capture_witness`; named residuals in the docstrings.
- `orca-harness/runners/run_fragrance_review_lake_packet.py`
  - Status: merged. Role: `--data-root`/`--output` seam over a companion receipt; mirrors `run_source_capture_http_packet.py`.
- `orca-harness/tests/test_fragrance_review_lake_pilot.py`
  - Status: merged. Role: 6 tests — exact-bytes equivalence, append-on-rederive, byte-identical rebuild, contamination guard, capture-witness admission gate (negative), named-residual observability.

## Frozen Decisions

- Decision: preserved bodies = exact raw widget-response bytes only; coverage/selection fields live only under `derived/`; positional `file_id` = body key, NOT a typed attachment key.
  - Evidence: `fragrance_review_lake.py` + the contamination-guard test.
  - Consequence: the typed AR entry must NOT inherit the positional `file_id` or staging-path semantics.
- Decision: claim ceiling — no AR physicalization / 7-checks / closure; one-fixture proof.
  - Evidence: module docstring + PR #489 description.
  - Consequence: the AR closure claim remains open work for the data-lake lane.

## Mutable Questions

- Question: should the typed AR entry round-trip the per-response provenance (response_origin/kind/url/index) + operator widget_route/source_id the tee leaves unattributed?
  - Why still mutable: it's the AR entry's design choice, deferred to that lane.
  - What would resolve it: the AR architecture/contract pass.
- Question: AR-entry layout/serialization/backend?
  - Why still mutable: the AR contract explicitly defers these.
  - What would resolve it: the architecture pass + owner decision.

## Superseded / Dangerous-To-Reuse Context

- Stale: the ORIGINAL framing "honest tee that proves the 7 AR acceptance checks" / "AR physicalization".
  - Why dangerous: a GPT-5.5 cross-vendor review found it an internal over-claim (PreservedFile is the body discipline, NOT the typed AR entry).
  - Current replacement: the shipped "preserved-body tee pilot" with NO 7-checks/closure claim (the Frozen Decisions above).
- Stale: any precompact packet in the session scratchpad (`...\scratchpad\precompact_ar_tee_pilot_packet.md`).
  - Why dangerous: it predates the build; the build is now MERGED.
  - Current replacement: this handoff packet + the merged code on `origin/main`.

## Commands And Verification Evidence

- Command:
  ```bash
  uv run --frozen --with pytest --directory orca-harness python -m pytest tests/test_fragrance_review_lake_pilot.py tests/contract/test_capture_runner_lake_seam_coverage.py tests/contract/test_source_capture_packet_no_runtime_imports.py
  ```
  Result:
  - Passed (14 tests at last run; 64 across the fragrance + contract suites).
  - Re-run target so the receiver can confirm rather than trust: the same command on `origin/main` `54c7dc1a`.
- Command:
  ```bash
  gh pr view 489 --json state,mergeCommit
  ```
  Result:
  - `state: MERGED`, mergeCommit `54c7dc1a` (== current `origin/main` HEAD). Re-run to confirm the merge is durable.

## Blockers And Risks

- Blocker: AR-entry implementation is gated on an architecture/contract pass + bounded authorization (the contract doc does not authorize runtime implementation).
  - Evidence: the contract doc's own "does not authorize runtime implementation" clause.
  - Likely next action: run `workflow-architecture-planning` on the AR contract, then seek bounded authorization.
- Risk: building the typed AR entry in the capture lane (wrong lane) or letting it inherit the tee's positional `file_id`.
  - Likely next action: keep AR work on the data-lake lane; treat the preserved bodies as referenced inputs, not as the typed entry.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - PR #489 merged + `origin/main` HEAD = `54c7dc1a` → `gh pr view 489 --json state,mergeCommit`; `git log --oneline -1 origin/main`.
  - The merged tee module + its claim ceiling/residuals → reread `orca-harness/source_capture/fragrance_review_lake.py` on `origin/main`.
  - The AR contract's "does not authorize runtime implementation" + 7 checks → reread the AR contract doc on `origin/main`.
  - Tests green → re-run the pytest command above with `--frozen`.
- Load outcomes and what each means: `REUSE` only if all re-verify; `STALE_REREAD_REQUIRED` if `origin/main` advanced past `54c7dc1a` (reread the ledger sources against the new HEAD before AR work); `BLOCKED_DRIFT` if the merged tee was reverted/changed unexpectedly.
- Sources that must be reread if drift detected: the AR contract doc, `retail_pdp_projection.py` + its pilot test, `data_lake/root.py`, and the merged `fragrance_review_lake.py`.

## Do Not Forget

- The next unit (typed AR entry) is a DIFFERENT lane (data-lake) and is gated on architecture + authorization; the capture lane itself is DONE.
