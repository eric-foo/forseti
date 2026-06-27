# YouTube Downstream ECR-Wiring + Cleaning-Validation Lane Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (Planning/Implementation handoff prompt)
scope: >
  Commission a fresh lane to wire YouTube transcript packets through the ECR
  integrity layer into cleaning (the YouTube equivalent of the retail/reddit/IG
  capture->ECR->cleaning path), and validate the already-built Pass-1
  product-mention extraction end-to-end on YouTube. Gold verdict, projection,
  derived_retrieval, and live LLM transport are deferred.
use_when:
  - Picking up the YouTube downstream ECR-wiring + cleaning-validation lane.
  - Checking what is built vs deferred in the YouTube capture->ECR->cleaning path.
authority_boundary: retrieval_only
open_next:
  - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
  - orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-26 (verify via `git log` on this file)
- created_by_lane: YouTube capture/enforcement closeout thread (provenance only; not authority)
- workspace: any clean worktree off `origin/main`; do NOT reuse the sender's worktree
- handoff_path: `docs/prompts/handoffs/youtube_downstream_ecr_cleaning_lane_handoff_v0.md`
- expected_branch: a fresh lane branch off `origin/main`
- expected_head: base was `origin/main @ 5a824d33` at authoring — **main moves FAST (many parallel lanes); refetch and branch off the latest `origin/main`, do not trust this SHA**
- expected_dirty_state_including_handoff_file: this packet is a tracked file on its authoring branch; your lane starts clean off `main`
- load_rule: confirm-don't-trust. Every load-bearing fact below is a hypothesis. Re-verify it against its compare target (here: `reread-required`, because main moves fast) before acting. Sender claims are not authority.

## Goal Handoff

- long_term_goal: Orca turns public social capture into usable demand-read signals through the pipeline capture -> ECR -> cleaning -> Judgment, per `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`.
- anchor_goal: Close YouTube's integrity gap. YouTube transcript packets are captured but never receipted through ECR (retail/reddit/instagram are). Wire YouTube into the capture->ECR->cleaning path, and validate the already-built Pass-1 product-mention extraction end-to-end on YouTube.
- success_signal: (1) A YouTube entry point in `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` produces SP-1/2/3/6 ECR receipts for a YouTube caption packet, covered by a new passing test `test_runner_writes_ecr_receipts_and_cleaning_packet_for_youtube` in `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` mirroring the reddit/instagram cases; AND (2) `orca-harness/runners/run_transcript_product_extract.py` is validated to produce `silver__cleaning__product_mentions` records from a YouTube transcript end-to-end (offline/injected transport), with the full `orca-harness` suite green including the no-LLM-zone contract test.

## Open Decision / Fork

- decision: How do YouTube's hardcoded source postures flow through ECR, and which surface to wire first?
  - options / facts to verify: `caption_packet.py` and `asr_packet.py` hardcode `cutoff_posture=not_applicable` and `archive_history_posture=not_attempted`. The orientation read claims `not_applicable` clears ECR SP-3 (timing) and `not_attempted` routes SP-6 (source-visibility) to a CURRENT_CAPTURE_ONLY residual. **Re-verify this against the four derivers in `orca-harness/ecr/deriver.py` and the SP-6 architecture before relying on it** — if a YouTube posture does not satisfy an ECR invariant, surface it as a posture gap rather than forcing a clear.
  - already constrained / off the table: no new architecture — the four ECR derivers (`derive_timing_postures`, `derive_inspectability_postures`, `derive_identity_postures`, `derive_source_visibility_postures`) are source-family-agnostic; do not add a YouTube-specific override.
  - trade-offs: caption is YouTube's primary surface (recommend wiring caption first); ASR and audience-post (`orca-harness/source_capture/audience_post_packet.py`) are secondary and can follow.
  - owner of the call: the receiving lane's architect for wiring details; the human owner for any scope expansion.
  - recommendation: wire the **caption** surface first (like the reddit path: `_derive_ecr_receipt` then build cleaning input handles from the packet's `source_slices`, since YouTube has no projection packet — see Drift Guard). Treat ASR/audience-post as fast-follow.
- decision: Does YouTube need a projection packet (like IG's `IgCreatorMomentumProjectionPacket`) before ECR, or go packet -> ECR directly (like reddit)?
  - recommendation: packet -> ECR directly (reddit-shaped). YouTube writes straight to the raw lake; it does not stage externally, so no projection intermediary. Confirm by reading `_process_reddit_entry` vs `_process_instagram_entry` in the smoke runner.

## Drift Guard

- DO NOT build the Pass-2 gold product verdict (`scoring/product_verdict_fusion.py`). Deferred by the spec's "harvest before cook" rule — the deterministic verdict rubric is built from real extracted Pass-1 data, not guessed now.
- DO NOT build projection or `derived_retrieval` views (by_creator / by_mention / undone). Projection is for sources that stage externally first (IG grid, retail PDP); YouTube does not need it. Cross-source `by_mention` aggregation is a separate owner-gated `derived_retrieval` activation decision (`docs/decisions/orca_data_lake_derived_retrieval_activation_proposal_v0.md`), currently deferred.
- DO NOT wire live LLM transport. The cleaning runner is offline-testable with an injected transport; live/metered transport is owner-gated and out of scope.
- DO NOT touch IG branches or IG downstream lanes. IG's audio->ASR->extraction path is complete and lives on its own branches; reuse its *code* by pointer (it shares `transcript_product_extractor.py` etc.), but do not edit IG runners/lanes.
- Gold = Judgment-only. Never emit a gold/verdict label from ECR or cleaning. Authority: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md` (ratified 2026-06-21).
- AI stays confined to `cleaning/` (no-LLM-zone). Do NOT add `openai`/`anthropic`/`litellm`/`langchain` imports to `scoring/`, `reports/`, `runners/`, `schemas/`, or `harness_utils.py`. Enforced by `orca-harness/tests/contract/test_no_llm_imports.py` (CI-failing).
- ECR is receipt-only. No transformation, no stored capture field, no EvidenceUnit binding, no Cleaning/Judgment logic, no JSG-01 unfreeze. Authority: `orca-harness/ecr/__init__.py` (INV-1..5).
- Never commit captured or derived data. Lake output is gitignored; track code only.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `.agents/workflow-overlay/README.md` and `AGENTS.md` first, per the overlay).
- targets to enter the ladder: the files named in `open_next` above, plus `orca-harness/ecr/deriver.py`, `orca-harness/ecr/lake.py`, `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`, `orca-harness/source_capture/transcript/caption_packet.py`, and `docs/prompts/handoffs/ig_reels_transcript_extraction_lane_handoff_v0.md` (the IG precedent).
- already loaded (weak orientation, freshness-marked; NOT authority): an orientation map produced by the sender's read-only fan-out on 2026-06-26 — its conclusions are summarized in this packet and must be re-verified, not trusted.
- must load first (before strict or actionable steps): the ECR frame contract + the data/cleaning boundary contract + the extraction spec + `run_capture_ecr_cleaning_smoke.py` itself (the wiring template). Re-run progressive source loading; this packet only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- SCR (Signal Content Record) is DEPRECATED as a standalone pre-Judgment layer (#375); ECR is the only derived-record kind; default route is evidence-pack -> Judgment.
  - decided in: `orca/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md`; verify (`reread-required`) before any actionable use. DO NOT build SCR.
- Medallion: gold = Judgment-only, never leaks pre-Judgment; silver only for projection/ECR/cleaning.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`; `reread-required`.
- LLM-reads / code-decides doctrine: Pass-1 is LLM (extract mentions + quotes), Pass-2 is deterministic code (verdict). Source pointers verified in code, never the model.
  - decided in: the extraction spec `youtube_transcript_product_extraction_spec_v0.md` (owner-confirmed 2026-06-23); `reread-required`.
- "Harvest before cook": Pass-2 verdict rubric is built from real Pass-1 data, so Pass-2 is deferred. Same spec.
- Lake physical layout: `raw/<shard>/<packet_id>/`, `derived/<shard>/<anchor>/<lane>/<record_id>`, shard = `sha256(key)[:3]`; by-key reads recompute the shard (no index lookup). Authority: `orca-harness/data_lake/root.py` + the data-lake authority contracts; `reread-required`.

## Active Objective

Make YouTube transcript packets first-class in the integrity + cleaning pipeline: add a YouTube entry point to the capture->ECR->cleaning smoke runner so YouTube captions (then ASR) get SP-1/2/3/6 ECR receipts like retail/reddit/instagram, and validate that the existing Pass-1 product-mention runner produces silver records from a YouTube transcript end-to-end. Nothing downstream of silver, no projection, no live transport.

## Exact Next Authorized Action

1. Refetch and branch off the latest `origin/main` (main moves fast). State workspace/branch/dirty-state.
2. Re-verify the load-bearing facts (confirm-don't-trust): grep `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` to confirm it still has only `retail`/`reddit`/`instagram` entries and no YouTube path; confirm `run_transcript_product_extract.py` + `cleaning/transcript_product_extractor.py` still exist; reread the ECR frame contract + the data/cleaning boundary contract + the extraction spec.
3. ECR wiring: add a YouTube entry point to `run_capture_ecr_cleaning_smoke.py` mirroring `_process_reddit_entry` (packet -> `_derive_ecr_receipt` over all four derivers -> build cleaning input handles from the packet's `source_slices`). Verify YouTube's hardcoded postures (`cutoff_posture=not_applicable`, `archive_history_posture=not_attempted`) satisfy SP-3 and SP-6 against `ecr/deriver.py`; surface a posture gap if not. No source-family-specific deriver override.
4. Add `test_runner_writes_ecr_receipts_and_cleaning_packet_for_youtube` to `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`, covering at least the caption surface, mirroring the reddit/instagram test cases.
5. Cleaning validation (parallel, independent of ECR): run `run_transcript_product_extract.py` end-to-end on a YouTube transcript (caption json3 and/or ASR record) with an injected/offline transport, and confirm it appends `silver__cleaning__product_mentions` records with quote-verified, timestamped mentions; add/confirm a unit test if coverage is missing.
6. Validation / stop condition: full `orca-harness` suite green (`cd orca-harness && python -m pytest`), including the new YouTube ECR test, the existing ECR/cleaning tests, and `tests/contract/test_no_llm_imports.py`. If a YouTube posture cannot satisfy an ECR invariant without a deriver change, STOP and surface it (do not force a clear).
7. Land via the per-lane PR flow (owner-gated). This is implementation work in `orca-harness/` — it requires the bounded authorization carried by this handoff; stay within ECR-wiring + cleaning-validation.

## Authority And Source Ledger

(All `reread-required` — main moves fast; treat every entry as a hypothesis to re-verify.)

- Repository instructions: `AGENTS.md` + `CLAUDE.md` shim; overlay under `.agents/workflow-overlay/` (read `README.md` first).
- User constraints: scope = ECR-wire + validate cleaning (owner-confirmed 2026-06-26); gold/projection/derived_retrieval/live-transport deferred.
- Source-read ledger:
  - `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` — Role: the capture->ECR->cleaning wiring template (retail/reddit/instagram); the file you extend. Load-bearing: yes. Compare target: reread-required. Reuse rule: mirror `_process_reddit_entry` for YouTube.
  - `orca-harness/ecr/deriver.py` + `orca-harness/ecr/lake.py` — Role: the four source-agnostic derivers + lake persistence. Load-bearing: yes. Compare target: reread-required. Reuse rule: call as-is; no YouTube override.
  - `orca-harness/ecr/models.py` + `orca-harness/ecr/__init__.py` — Role: posture schemas + ECR invariants (receipt-only). Load-bearing: yes. Compare target: reread-required.
  - `orca-harness/source_capture/transcript/caption_packet.py`, `asr_packet.py` — Role: YouTube packet builders + the hardcoded postures to verify. Load-bearing: yes. Compare target: reread-required.
  - `orca-harness/runners/run_transcript_product_extract.py` + `orca-harness/cleaning/transcript_product_extractor.py` + `orca-harness/cleaning/transcript_product_lake.py` — Role: the already-built Pass-1 YouTube cleaning to validate. Load-bearing: yes. Compare target: reread-required.
  - `orca-harness/schemas/product_mention_models.py` — Role: silver `ProductMention` schema (Pass-2 `ProductVerdict` deferred/unbuilt). Load-bearing: yes. Compare target: reread-required.
  - `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` — Role: controlling ECR frame + SP-6 + M1/M2/M3 binding. Load-bearing: yes. Compare target: reread-required.
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` — Role: ECR-vs-Cleaning responsibility boundary. Load-bearing: yes. Compare target: reread-required.
  - `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md` — Role: owner-confirmed downstream spec (Pass-1 silver shipped, Pass-2 gold deferred). Load-bearing: yes. Compare target: reread-required.
  - `docs/prompts/handoffs/ig_reels_transcript_extraction_lane_handoff_v0.md` — Role: the IG downstream precedent (shared cleaning code). Load-bearing: no (orientation). Compare target: reread-required.
- Source gaps: whether YouTube caption postures cleanly satisfy SP-3/SP-6 is unverified (the central open decision).
- Strict-only blockers: none known; the work is bounded and code-agnostic to source family.
- Not-proven boundaries: nothing run live at scale; the Pass-1 cleaning has not been validated on real YouTube data end-to-end (that is step 5).

## Current Task State

- Completed: YouTube capture (caption + ASR transcript packets into the lake); Pass-1 YouTube cleaning (transcript -> `ProductMention` silver records) built against an owner-confirmed spec; ECR built + wired for retail/reddit/instagram.
- Partially completed: ECR exists but is NOT wired for YouTube (no entry point in the smoke runner, no YouTube test).
- Broken or uncertain: whether YouTube's hardcoded `cutoff_posture`/`archive_history_posture` flow correctly through ECR SP-3/SP-6 (must verify, not assume).

## Workspace State

- Branch: a fresh lane branch off the latest `origin/main` (the sender authored this packet on `claude/youtube-downstream-ecr-cleaning-handoff` off `origin/main @ 5a824d33`; do not reuse that worktree).
- Head: refetch `origin/main`; do not trust `5a824d33`.
- Dirty/untracked before your work: clean off `main`.
- Target files: `run_capture_ecr_cleaning_smoke.py`, `test_capture_ecr_cleaning_smoke_runner.py` (edit/add); the YouTube capture + cleaning modules (read); a possible new YouTube cleaning test.
- Related worktrees/branches: IG downstream lanes (DO NOT touch — Drift Guard).

## Changed / Inspected / Tested Files

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
  - Status: to edit (add YouTube entry).
  - Role: capture->ECR->cleaning bridge.
  - Symbols: `_entry_list`, `_process_retail_entry`, `_process_reddit_entry`, `_process_instagram_entry`, `_derive_ecr_receipt`. Add a `_process_youtube_entry` + `youtube_entries` handling and update the "must name at least one ..." guard.
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
  - Status: to edit (add YouTube test).
  - Role: integration test for the ECR receipts + cleaning packet per source family.
- `orca-harness/runners/run_transcript_product_extract.py`
  - Status: to validate (likely no edit).
  - Role: the built YouTube Pass-1 product-mention daemon runner.

## Frozen Decisions

- Scope: ECR-wire + validate cleaning; gold verdict / projection / derived_retrieval / live LLM transport DEFERRED (owner-confirmed 2026-06-26).
  - Consequence: do not expand into Pass-2 or projection without a new owner decision.
- ECR derivers are source-family-agnostic; YouTube reuses them unchanged.
- Wire the caption surface first; ASR/audience-post are fast-follow.
- The architecture invariants in Drift Guard (gold=Judgment-only, no-LLM-zone, ECR receipt-only, never-commit-data, SCR deprecated) are settled — do not re-litigate.

## Mutable Questions

- Does the YouTube caption posture set satisfy ECR SP-3/SP-6, or is a posture gap exposed? Resolved by reading `ecr/deriver.py` against `caption_packet.py` and running the new test.
- Should the YouTube ECR entry build cleaning handles from `source_slices` (reddit-shaped) or from a projection packet (IG-shaped)? Resolved by reading `_process_reddit_entry` vs `_process_instagram_entry`; sender recommends reddit-shaped.

## Superseded / Dangerous-To-Reuse Context

- SCR (Signal Content Record) standalone pre-Judgment layer — DEPRECATED (#375). Do not build or wire SCR. Replacement: ECR is the only derived-record kind; evidence-pack -> Judgment.
- `orca-harness/youtube_capture/capture_youtube_v0.py` (legacy metadata+comments capture writing gitignored `packets/<video_id>/`) is a SEPARATE path from the transcript pipeline this lane touches; do not conflate it with the `source_capture/transcript/` packets that feed ECR/cleaning.
- The orientation map summarized in this packet is a weak source class (a prior-thread fan-out). Re-verify before any strict claim.

## Commands And Verification Evidence

- Confirm the ECR gap still holds:
  ```bash
  grep -nE "youtube|_process_|entries" orca-harness/runners/run_capture_ecr_cleaning_smoke.py
  ```
  Re-run target: expect retail/reddit/instagram entries and NO youtube entry at handoff time.
- Full suite (the stop condition):
  ```bash
  cd orca-harness && python -m pytest
  ```
  Re-run target: green including the new YouTube ECR test + `tests/contract/test_no_llm_imports.py`.

## Confirm-Don't-Trust Load Checklist

- Re-verify (before acting): the smoke runner still lacks a YouTube entry; `run_transcript_product_extract.py` + the extractor/lake still exist; the four ECR derivers are unchanged and source-agnostic; the YouTube caption/ASR posture hardcodes; the extraction spec is still the owner-confirmed authority.
- Compare target for each: `reread-required` (main moves fast).
- Load outcomes: `REUSE` only if all re-verify; `STALE_REREAD_REQUIRED` if main moved materially (reread the smoke runner + ECR contract + spec); `BLOCKED_UNVERIFIABLE` if a load-bearing source is missing or unreadable.
- Sources that must be reread if drift is detected: the smoke runner, `ecr/deriver.py`, the ECR frame contract, the boundary contract, the extraction spec.

## Do Not Forget

- The ECR derivers are source-agnostic — wiring YouTube is an entry-point + test job, not new architecture.
- Two parallel deliverables: ECR receipts (via the smoke runner) AND validating the existing product-mention cleaning runner — they are independent.
- Stop and surface a posture gap rather than forcing an ECR clear for YouTube.
- Deferred (do not build): Pass-2 gold verdict, projection, derived_retrieval, live LLM transport.
