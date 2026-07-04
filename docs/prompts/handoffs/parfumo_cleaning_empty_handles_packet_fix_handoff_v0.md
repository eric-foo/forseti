# Parfumo Cleaning Empty-Handles Packet — Fix-or-Disposition Handoff (v0)

```yaml
retrieval_header_version: 1
artifact_role: Lane handoff prompt (docs/prompts/handoffs/; cold-start packet for the parfumo cleaning lane)
scope: >
  Cold cross-lane handoff for the one lane-owned defect blocking the bronze
  completion signal on the cleaning side: live packet
  01KWCG89CBFH90Z4ABKYWKF5VE (a real parfumo surface) fails CleaningPacket
  validation (empty handles list) inside derive_parfumo_cleaning_into_lake,
  re-surfacing loudly on every cadence run and never acked. Carries the
  verified dry-run evidence, the exact code locations, the fix-vs-disposition
  fork, drift guards, and the receiver's load contract.
use_when:
  - Kicking off the parfumo empty-handles fix in a fresh thread (the receiving lane owns cleaning/parfumo*).
  - Checking why the bronze cadence's parfumo post-sweep pending count is nonzero.
stale_if:
  - Packet 01KWCG89CBFH90Z4ABKYWKF5VE is derived-and-acked or formally dispositioned (then this is done history).
  - The parfumo cleaning deriver's zero-handle behavior changes on main.
authority_boundary: retrieval_only
```

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (census-closure record + live dry-run evidence + parfumo
    cleaning deriver/runner code; all compare targets pinned in-repo)
  edit_permission: docs-write (this handoff artifact only)
  target_scope: docs/prompts/handoffs/parfumo_cleaning_empty_handles_packet_fix_handoff_v0.md
  dirty_state_checked: yes (authored on claude/parfumo-empty-handles-handoff off origin/main @ ef2bcf18)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound by the artifact-folders overlay file and the in-repo handoff pattern.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-07-04
- created_by_lane: bronze census closure lane (PR #664 author; provenance only, not authority)
- workspace: the receiving lane's own fresh checkout/worktree off `origin/main`
- handoff_path: docs/prompts/handoffs/parfumo_cleaning_empty_handles_packet_fix_handoff_v0.md
- expected_branch: receiver creates a fresh lane branch off `origin/main` (per the standing workflow below)
- expected_head: `origin/main` at or after the merge of this packet's PR (the census record's dry-run section must be present — see compare target below)
- expected_dirty_state_including_handoff_file: clean tree at lane start; this packet is committed, not dirty
- load_rule: confirm-don't-trust — re-verify every load-bearing fact below against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

Derived from the census-closure record's stated blocker (not a ratified
`workflow-goal-framing` output — treat as orientation):

- long_term_goal: a trustworthy data lake whose layer-completion claims are executable, never asserted.
- anchor_goal: clear the parfumo blocker of the bronze completion signal — packet `01KWCG89CBFH90Z4ABKYWKF5VE` either derives-and-acks honestly or receives a recorded owner disposition.
- success_signal: `run_parfumo_cleaning_catchup --run` emits zero status entries for this packet on a second consecutive run, and the seam cadence's post-sweep parfumo pending count goes 1 → 0 — with no fake-success path (no ack without honest evidence, no silently relaxed validation).

## Open Decision / Fork

- decision: fix the deriver, fix the extraction, or disposition the packet — undecidable until the live packet is inspected.
  - options:
    1. **Extraction bug** — the packet's preserved parfumo page DOES contain review handles the parser misses → fix `cleaning/parfumo.py` extraction; the packet then derives normally.
    2. **Honest non-cleanable outcome** — the page genuinely yields zero handles (empty/blocked/changed page shape) → give the parfumo lane an explicit zero-handle completion path (ack with explicit `no_cleanable_content`-class evidence stating the basis), mirroring the existing known-out-of-scope ack shape in `run_parfumo_cleaning_catchup.py`. CAUTION: an automatic zero-handle ack can hide future extraction bugs — if chosen, the evidence must record WHY zero is honest for this packet class, and the fork between "parser found nothing" and "page has nothing" must stay distinguishable.
    3. **Packet disposition** — the capture itself is damaged/contaminated → owner-decided operator disposition (the packet stays loudly pending until then).
  - already constrained / off the table: relaxing `CleaningPacket.handles` `min_length=1` globally (shared model — fragrantica and basenotes ride the same contract); acking without completion evidence; editing the cadence runner or census semantics to make the signal pass.
  - trade-offs: option 2 is the likely durable shape but carries the fake-success risk above; option 1 is best if true but requires evidence from the actual page bytes; option 3 needs owner sign-off.
  - owner of the call: the parfumo cleaning lane for options 1-2 (code-owned); the owner for option 3.
  - recommendation: inspect first, decide second — run the gating read (live packet manifest + preserved bytes + its parfumo projection records) before any code plan.

## Drift Guard

- Never write to `F:\orca-data-lake` outside the sanctioned runners; live-lake READS need a fresh owner grant each turn (per-turn; the permission classifier enforces this — do not work around it).
- Do not edit `runners/run_seam_cadence.py`, its gates, or the census record's classification sections to make the signal pass; the census record's dry-run section is updated only with newly observed results.
- Do not touch the ASR backlog (472 pending) — separate blocker, owner-operated compute, not this lane.
- Do not relax shared cleaning models for a parfumo-local problem.
- Standing workflow (inherit verbatim from the census lane): fresh branch off `origin/main`; `workflow-assumption-gate` → `/fused`; full-suite validation via `--junitxml` + ElementTree parse with `ORCA_DATA_ROOT` cleared; re-run tracked-scan gates AFTER committing; explicit `git push -u origin <lane>`; owner merges; per-unit repo-mode cross-vendor delegated review commission (pin commit SHA + LF-blob SHA256s; non-Anthropic who-constraint; owner couriers; home-CA adjudicates).

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` + `.agents/workflow-overlay/README.md` first, always).
- targets to enter the ladder: the files in the source ledger below.
- already loaded by the sender (weak orientation, 2026-07-04; not authority): parfumo runner/deriver code paths, census record, live dry-run output.
- must load first: `AGENTS.md`, overlay README, then the census record's "Live dry-run status" section, then the parfumo code paths below.

### Earlier-decided concepts (inline gist + verify pointer)

- **Bronze completion signal is executable**: `runners/run_seam_cadence.py --run` must exit 0 (second cycle zero + final pending sweep zero). Decided in `docs/decisions/bronze_consumer_census_closure_record_v0.md` (PR #664) + F-CAD-001 adjudication (`docs/review-outputs/adversarial-artifact-reviews/seam_cadence_bronze_census_closure_delegated_adversarial_code_review_v0.md`). Verify before actionable use.
- **Out-of-scope-surface ack convention**: known other-lane surfaces are acked with explicit evidence; unknown surfaces stay visible and unacked (F-FRAG-002/F-IGRC-002 class). See `run_parfumo_cleaning_catchup.py` `run_catchup`. Verify before reusing the shape for zero-handle acks.

## Active Objective

Make live packet `01KWCG89CBFH90Z4ABKYWKF5VE` stop failing the parfumo
cleaning catch-up: inspect it under an owner read grant, classify the root
cause into the fork above, then implement the chosen fix or record the owner
disposition — honestly, with the packet either derived-and-acked or loudly
pending by decision.

## Exact Next Authorized Action

1. Read `AGENTS.md` + `.agents/workflow-overlay/README.md`; state isolation (fresh branch off `origin/main`).
2. Request the per-turn owner live-lake read grant; inspect packet `01KWCG89CBFH90Z4ABKYWKF5VE`: manifest (`source_surface`, capture context), preserved raw bytes, and its committed parfumo projection records (the deriver input).
3. Classify into the fork (extraction bug / honest zero-handle / damaged capture); bring the classification + chosen option to the owner if option 3, else run `workflow-assumption-gate` → `/fused` for the code fix under the standing workflow.
4. Validation target: `run_parfumo_cleaning_catchup` unit suite + a regression pinning the chosen zero-handle behavior; then a live re-run of the parfumo catch-up (owner grant) showing the packet resolved and the cadence post-sweep parfumo pending at 0.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (root), `.agents/workflow-overlay/` (Forseti authority).
- User constraints: live-lake reads owner-granted per turn; owner merges PRs.
- Source-read ledger:
  - `docs/decisions/bronze_consumer_census_closure_record_v0.md`
    - Role: names this defect as a bronze-closure blocker; carries the verified dry-run evidence.
    - Load-bearing: yes
    - Compare target: section "Live dry-run status" must contain packet id `01KWCG89CBFH90Z4ABKYWKF5VE` and "CleaningPacket ValidationError"; if the section still says "Blocked pending", you are on a pre-result revision — fetch current `origin/main`.
    - Last checked: 2026-07-04
    - Reuse rule: re-read on current `origin/main` before acting.
  - `orca-harness/cleaning/models.py`
    - Role: the failing contract — `CleaningPacket.handles: list[CleaningInputHandle] = Field(min_length=1)` (line ~411).
    - Load-bearing: yes
    - Compare target: quoted field definition above; shared by fragrantica/basenotes (do not relax globally).
    - Last checked: 2026-07-04
    - Reuse rule: reread-required at lane start.
  - `orca-harness/cleaning/parfumo.py`
    - Role: `build_parfumo_cleaning_packet` (line ~61) builds `CleaningPacket(handles=enriched_handles, ...)` (line ~116) — the zero-handle producer.
    - Load-bearing: yes
    - Compare target: quoted call above.
    - Last checked: 2026-07-04
    - Reuse rule: reread-required at lane start.
  - `orca-harness/cleaning/parfumo_lake.py`
    - Role: `derive_parfumo_cleaning_into_lake` (line ~63) — the derivation the catch-up calls; where the ValidationError raises.
    - Load-bearing: yes
    - Compare target: function name + the audit/silver record writes it performs.
    - Last checked: 2026-07-04
    - Reuse rule: reread-required at lane start.
  - `orca-harness/runners/run_parfumo_cleaning_catchup.py`
    - Role: repro entrypoint + the existing explicit-evidence ack shape (known-out-of-scope surfaces path in `run_catchup`).
    - Load-bearing: yes
    - Compare target: `derive_failed` status emission wraps `derive_parfumo_cleaning_into_lake` exceptions.
    - Last checked: 2026-07-04
    - Reuse rule: reread-required at lane start.
  - Live lake `F:\orca-data-lake`, packet `01KWCG89CBFH90Z4ABKYWKF5VE`
    - Role: the failing input — root-cause evidence lives here.
    - Load-bearing: yes
    - Compare target: reread-required (owner-gated per-turn read grant; the sender did NOT open this packet's contents — only the runner's error output was observed).
    - Last checked: never opened by sender
    - Reuse rule: never act on the fork classification without this read.
- Source gaps: the packet's actual page content and its projection records are unread — this is the gating read.
- Strict-only blockers: option 3 (disposition) needs an owner decision; any live run needs a per-turn grant.
- Not-proven boundaries: nothing in this packet proves the root cause; the error shape alone is compatible with all three fork options.

## Current Task State

- Completed (by the sending lane, merged as PR #664 + landed dry-run record):
  the seam cadence executable, its gates, the census-closure record, the
  F-CAD-001 review adjudication, and the owner-granted live dry-run.
- Broken or uncertain: this packet's derivation (the subject); root cause unknown.

## Commands And Verification Evidence

- Command (owner-granted live dry-run, 2026-07-04, two consecutive invocations):
  ```
  python orca-harness/runners/run_seam_cadence.py --run --skip-asr --data-root F:\orca-data-lake
  ```
  Result (verbatim status line, both cycles, both invocations):
  ```
  cycle=1  01KWCG89CBFH90Z4ABKYWKF5VE  ValidationError: 1 validation error for CleaningPacket
  handles
    List should have at least 1 item after validation, not 0 [type=too_short, input_value=[], input_type=list]
  ```
  - Steady state after the run: every driven lane second-cycle-zero except this packet (`post_cycle_pending` parfumo=1) and the skipped ASR backlog (472).
  - Re-run target so the receiver can confirm rather than trust (cheap, owner grant required):
    `python orca-harness/runners/run_parfumo_cleaning_catchup.py --check --data-root F:\orca-data-lake` → expect `1`.

## Blockers And Risks

- Per-turn owner read grant required before the gating read (hard gate).
- Fake-success risk if option 2 is implemented as a blanket zero-handle ack (see the fork's caution) — the delegated review commission for the fix should name this as the special stake.
- The other bronze blocker (ASR backlog) is explicitly out of scope here.

## Superseded / Dangerous-To-Reuse Context

- The census record's pre-2026-07-04 "Blocked pending" dry-run section and the
  predecessor's carried backlog counts (6+1 cleaning) — superseded by the
  verified dry-run results now in the census record.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: the census record's dry-run section (compare target above); the four code compare targets; the live pending count (`--check` → 1, owner grant).
- Load outcomes: `REUSE` only after all of the above verify; a missing dry-run section → `STALE_REREAD_REQUIRED` (fetch current main); an unreadable lake or no grant → stop at step 2 of the next actions and request the grant.

## Do Not Forget

The exit-0 bronze signal is the point of all of this: whatever option is
chosen must leave the cadence truthful — a resolved packet or a loudly
pending one, never a quietly acked one.
