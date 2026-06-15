# Handoff Packet — Demand-Durability Series Writer (Step 2)

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (continuation artifact, not readiness evidence)
scope: Transfer step 2 of the demand-durability capture rollout (build the durability-series writer) to a fresh lane with none of the sender's context.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-15
- created_by_lane: capture-spine CA thread (provenance only; not an authority claim)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/demand_durability_series_writer_step2_handoff_v0.md
- expected_branch: a fresh worktree/branch off `origin/main` (do NOT work on the hot home branch `ecr-sp3-timing-deriver-slice1`)
- expected_head: `origin/main` was `739411f` at handoff (the #113 merge). It moves; re-fetch.
- expected_dirty_state_including_handoff_file: this packet is newly created under tracked `docs/prompts/handoffs/` → untracked until committed on its own lane.
- load_rule: **confirm-don't-trust** — re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: a trustworthy demand-durability substrate for Orca's beauty-vertical demand-read — capture that does not silently lie about comparability, coverage, tampering, or sampling gaps — **without capture ever scoring or judging demand (INV-1)**.
- anchor_goal: **build the durability-series writer** — a capture runner path that POPULATES the now-hardened additive-optional durability fields as first-class schema fields for a commissioned demand-durability proxy series, instead of stuffing them in `capture_context` (the way the pilot did).
- success_signal: a demand-durability capture run produces a `SourceCapturePacket` whose durability fields are set as first-class schema fields and validate under the hardened `models.py`; a non-durability capture leaves them `None` (back-compat); the full offline suite stays green; no `SOURCE_CAPTURE_MANIFEST_VERSION` bump.

## Open Decision / Fork

- decision: **runner shape** — how to emit the durability fields.
  - options: (A) extend the existing `runners/run_source_capture_http_packet.py` with optional durability flags (`--series-id`, `--session-visibility-pin`, `--locale-pin`, `--currency-pin`, `--variant-pin`, `--cold-start-at`, `--pre-coverage-history-posture`, `--intended-cadence`); (B) a dedicated `runners/run_source_capture_durability_packet.py` that wraps the same `fetch → stage_and_write_packet` path.
  - already constrained / off the table: must stay additive-optional; must set the **schema fields** (not `capture_context`); must reuse `stage_and_write_packet` + `cadence.py build_cadence_plan`; series-diff (Element 3) is out of scope.
  - trade-offs: (A) smallest diff, reuses the proven entrypoint, but loads many flags onto a general runner; (B) cleaner separation, but more new code + some duplication.
  - owner of the call: the receiving lane, with the owner's bounded build authorization.
  - recommendation: **(A) extend the existing http runner** — smallest-complete, reuses the proven path; promote to (B) only if the flag surface gets unwieldy.

## Drift Guard

- **additive-optional / back-compat**: never break existing packets; new fields default `None`; **no `SOURCE_CAPTURE_MANIFEST_VERSION` bump** (mirror the `archive_snapshot_time` precedent). Violating it breaks every prior packet + the 861-test suite.
- **INV-1**: the durability fields are observed facts, never weights, scores, or a durable-vs-hollow verdict. Smuggling a verdict into capture breaks the whole substrate's no-scoring invariant.
- **no-gate-defeat**: anti-bot (honest/anti-blocking UA) is OK; **STOP at any auth / CAPTCHA / Cloudflare *challenge*** and record the limitation. Do not defeat a gate.
- **schema fields, not `capture_context`**: the pilot stuffed pins in `capture_context` as a stopgap; step 2's whole point is to set the hardened **schema fields**. Do not copy the capture_context-stuffing pattern.
- **series-diff Element 3 is DEFERRED**: do not build it. It is a cross-packet record needing an extracted-value extractor; when later built it keys change on EXTRACTED values, raw `PreservedFile.sha256` is only a coarse inspect-flag (distillation binding A1c).
- **authorization**: building the writer is runtime/code work. This packet **scopes; it does not authorize**. The receiver needs explicit bounded build authorization in its own turn (AGENTS.md: implementation/runtime work requires explicit bounded authorization).

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `.agents/workflow-overlay/README.md` first, per AGENTS.md). The handoff carries pointers only; the receiver re-runs progressive source loading.
- targets to enter the ladder: `orca-harness/source_capture/models.py` (the hardened fields), `orca-harness/runners/run_source_capture_http_packet.py` (the proven runner to extend), `orca-harness/source_capture/packet_assembly.py` (`stage_and_write_packet`, `staged_file_id_map`), `orca-harness/source_capture/writer.py`, `orca-harness/source_capture/cadence.py` (`build_cadence_plan`, `CadencePlan.to_dict()`), `docs/product/data_capture_spine/demand_durability_capture_pilot_v0.md` (protocol §3), `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md` (Ob.17), `docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md` (Elements 1–5).
- already loaded (weak orientation, freshness-marked; not authority): this packet's claims about the hardened schema (from the sender's verification at `origin/main` `739411f`).
- must load first (before strict/actionable steps): `models.py` (to see the exact field names/types) + the pilot spec §3 (the protocol the writer realizes).
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **Elements 1/2/4 hardened additive-optional** (the fields to populate): `SourceCaptureSlice` has `session_visibility_pin`, `locale_pin`, `currency_pin`, `variant_pin` (each `VisibleFact | None = None`); `SourceCapturePacket` has `series_id: str | None`, `cold_start_at: VisibleFact | None`, `pre_coverage_history_posture: VisibleFact | None`, `intended_cadence: dict[str, object] | None`.
  - decided in: `orca-harness/source_capture/models.py` (PR #113); contract obligation in the obligation contract Ob.17.
  - compare target: `origin/main` `models.py` sha256 `6b71dbe2b91ce9715f9eb601d390ae19f633be99936bc3616830727cda8cbf5d`; or `grep -E "session_visibility_pin|intended_cadence"`.
  - verify before: writing any field-population code.
- **The pilot proved the machinery on live data** (pins / price / availability / cold-start / cadence on SdJ Bum Bum Cream): the writer realizes what the pilot did by hand.
  - decided in: `docs/product/data_capture_spine/demand_durability_capture_pilot_v0.md` (PR #108) §2–3.
  - compare target: reread-required (read §3 "Runnable series protocol").
  - verify before: choosing what the writer must set.
- **Series-diff (Element 3) deferred + the A1c refinement** (diff EXTRACTED values, raw hash = inspect-flag only): not part of step 2.
  - decided in: `docs/decisions/distillation_binding_data_capture_v0.md` A1c (PR #107).
  - compare target: reread-required (`grep "series-diff-on-extracted-values"`).
  - verify before: resisting any temptation to build change-detection in step 2.
- **INV-1** (no scoring/weighting at capture): the fields are facts only.
  - decided in: `docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md` §"INV-1 Preservation"; `docs/product/product_lead/orca_buyer_proof_packet_v0.md`.
  - compare target: reread-required.
  - verify before: any field whose value could look like a judgment.

## Active Objective

Build the durability-series writer (step 2): extend the capture runner path so a commissioned demand-durability proxy series sets the hardened Element 1/2/4 schema fields, additive-optional, INV-1-preserving, with tests + a green offline suite, landed via a per-lane PR off fresh `origin/main`.

## Exact Next Authorized Action

1. **Confirm-don't-trust**: `git fetch origin main`; verify `models.py` carries the 8 durability fields (`grep -E "session_visibility_pin|locale_pin|currency_pin|variant_pin|series_id|cold_start_at|pre_coverage_history_posture|intended_cadence"`) and Ob.17 is present in the obligation contract. If absent → `BLOCKED_DRIFT` (hardening not where this packet claims).
2. **Get explicit bounded build authorization** for runtime/code work (this packet does not grant it).
3. Decide the runner shape (Open Decision; recommend extend).
4. Implement field population in a fresh worktree off `origin/main`; reuse `stage_and_write_packet` + `cadence.py`; keep additive-optional.
5. Add tests (a durability capture sets the fields; a non-durability capture leaves them `None`); run the full offline suite — `orca-harness/.venv/Scripts/python.exe -m pytest` — expect green (baseline 861 passed / 2 skipped at handoff); run `.agents/hooks/check_map_links.py --strict` if docs change.
6. Per-lane PR off fresh `origin/main` (the `settings.json` push/PR prompts are the owner gate).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read overlay `README.md` first).
- Overlay authority: source-loading (`.agents/workflow-overlay/source-loading.md`), dev-workflow / per-lane PR (`docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`), safety/no-gate-defeat (`.agents/workflow-overlay/safety-rules.md`).
- User constraints: hardening "merged all"; step 2 = the writer; step 3 (cadence runner/scheduler over days) is separate; token-conscious; confirm-don't-trust; owner takes merges.
- Source-read ledger:
  - `orca-harness/source_capture/models.py`
    - Role: the hardened schema (fields to populate). Load-bearing: **yes**.
    - Compare target: `origin/main` sha256 `6b71dbe2b91ce9715f9eb601d390ae19f633be99936bc3616830727cda8cbf5d`.
    - Last checked: 2026-06-15 @ `origin/main 739411f`. Reuse rule: reread + re-verify sha before populating.
  - `orca-harness/runners/run_source_capture_http_packet.py`
    - Role: the proven runner to extend (Open Decision A). Load-bearing: **yes**. Compare target: `reread-required`. Reuse rule: read its arg-parsing + `stage_and_write_packet` call before extending.
  - `orca-harness/source_capture/packet_assembly.py` (`stage_and_write_packet`, `staged_file_id_map`)
    - Role: the packet build/write path the writer calls. Load-bearing: **yes**. Compare target: `reread-required`.
  - `orca-harness/source_capture/cadence.py` (`build_cadence_plan`, `CadencePlan.to_dict()`)
    - Role: produces the `intended_cadence` dict. Load-bearing: **yes**. Compare target: `reread-required`.
  - `docs/product/data_capture_spine/demand_durability_capture_pilot_v0.md` (§3 protocol)
    - Role: what the writer must set, per the proven protocol. Load-bearing: **yes**. Compare target: `reread-required`.
  - `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md` (Ob.17)
    - Role: the conditional obligation the writer satisfies. Load-bearing: **yes**. Compare target: `reread-required` (`grep "Demand-Durability Series Facts"`).
  - `docs/decisions/distillation_binding_data_capture_v0.md` (A1c)
    - Role: series-diff deferral + refinement (context for what NOT to build). Load-bearing: no. Compare target: `reread-required`.
- Source gaps: none known for step 2.
- Strict-only blockers: build authorization (runtime work) not yet granted.
- Not-proven boundaries: the writer is unbuilt; the real over-time series (step 3) + series-diff (Element 3) are unbuilt.

## Current Task State

- Completed (landed on `origin/main 739411f`): schema hardening (#113), pilot spec (#108), distill A1c (#107) — all MERGED.
- Partially completed: the rollout — step 2 (this writer) not started; step 3 (cadence runner/scheduler over days) not started.
- Broken or uncertain: none known; the pilot put pins in `capture_context` (a stopgap step 2 replaces).

## Workspace State

- Branch: receiver creates a fresh worktree/branch off `origin/main`.
- Head: `origin/main 739411f` at handoff (moves; re-fetch).
- Dirty/untracked before handoff: home tree (`ecr-sp3-timing-deriver-slice1`) carries unrelated untracked files; ignore it — do not work there.
- Dirty/untracked after writing this handoff file: + this file (untracked under `docs/prompts/handoffs/` until committed on its lane).
- Target files: `models.py` (read-only here — already hardened), the runner(s) (to extend/add), a new test, optionally the pilot spec (cross-link).
- Related worktrees/branches: the hardening/pilot/distill lanes are merged (prunable). Create a new one for step 2.

## Changed / Inspected / Tested Files

- `orca-harness/source_capture/models.py`
  - Status: hardened + merged (#113); read-only input for step 2.
  - Role: defines the additive-optional durability fields to populate.
  - Symbols: `SourceCaptureSlice` (4 pins), `SourceCapturePacket` (`series_id`, `cold_start_at`, `pre_coverage_history_posture`, `intended_cadence`), `VisibleFact` + `known_fact`/`unknown_with_reason`/`not_attempted`/`not_applicable` helpers.

## Frozen Decisions

- Elements 1/2/4 hardened **additive-optional** (#113 merged); no manifest bump. Evidence: `models.py` sha `6b71dbe2…`, Ob.17. Consequence: the writer SETS these fields; it does not re-shape the schema.
- Series-diff **Element 3 deferred** (#107 A1c). Consequence: step 2 builds no change-detection.
- INV-1 preserved. Consequence: fields are facts only.

## Mutable Questions

- Runner shape (extend vs dedicated) — see Open Decision; resolved by the receiver + owner.
- Step 3 cadence runner/scheduler shape (cron/scheduled-task over days) — deferred; will consume `intended_cadence`.
- Which SKUs/sources for the real series — step 3 concern; the pilot used SdJ Bum Bum Cream via `direct_http`.

## Superseded / Dangerous-To-Reuse Context

- **Pilot "pins in `capture_context`" approach** — superseded. Why dangerous: copying it defeats step 2 (the whole point is first-class schema fields). Current replacement: set the hardened `models.py` fields.
- **`_scratch/pilot/sdj_obs1`+`sdj_obs2`** — pilot evidence, gitignored, ephemeral; a reference for what real data looks like, NOT a code template and NOT durable.

## Commands And Verification Evidence

- Verify the schema landed:
  ```bash
  git fetch origin main && git show origin/main:orca-harness/source_capture/models.py | grep -E "session_visibility_pin|intended_cadence"
  ```
  Result at handoff: present (8 durability fields). Re-run target: the receiver confirms before building.
- Full offline suite (the green gate):
  ```bash
  cd orca-harness && .venv/Scripts/python.exe -m pytest -q
  ```
  Result at handoff: 861 passed, 2 skipped (on #113). Re-run after the writer + new tests.

## Blockers And Risks

- Blocker: build authorization not granted (runtime/code work). Likely next action: receiver requests bounded authorization in its turn.
- Risk: `intended_cadence` is an untyped `dict[str, object]` on the envelope — populate it from `CadencePlan.to_dict()` (do not invent a shape). Evidence: models.py comment + `cadence.py`.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: (1) `models.py` carries the 8 durability fields (sha `6b71dbe2…` / grep); (2) Ob.17 present in the obligation contract; (3) `origin/main` HEAD (≥ `739411f`); (4) suite-green baseline (861/2).
- Load outcomes: `REUSE` only after all four re-verify; `STALE_REREAD_REQUIRED` if `origin/main` moved (expected — re-read); `BLOCKED_DRIFT` if the durability fields are absent from `models.py` (then the hardening this packet assumes is not present — stop and reconcile).
- Reread on drift: `models.py`, the runner, the pilot spec §3, the obligation contract Ob.17.

## Do Not Forget

- This packet **scopes, it does not authorize** — get bounded build authorization first.
- Set the **schema fields**, not `capture_context`. Additive-optional, no manifest bump.
- **Series-diff (Element 3) is deferred** — do not build it.
