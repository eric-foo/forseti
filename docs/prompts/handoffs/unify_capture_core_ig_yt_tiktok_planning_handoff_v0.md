# Handoff Packet — Unify capture core across IG / YouTube (/ TikTok): PLANNING lane

```yaml
retrieval_header_version: 1
artifact_role: cold cross-lane handoff packet (planning lane kickoff; not authority, not validation, not a design decision)
scope: >
  Transfers a fresh PLANNING lane the goal + file pointers + drift guards to design a shared capture
  core across the Instagram, YouTube, and (later) TikTok capture lanes: analyse IG, analyse YT, design
  a core applicable to all three, then sync IG + YT first. The sender analysed the IG lane deeply; it
  did NOT analyse the YT lane (pointers only).
use_when:
  - Starting the capture-mechanics unification planning lane.
  - Re-locating which files own IG vs YT capture / transcript / save / extraction.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: workflow-handoff-max-v0
- mode: max
- created_at: 2026-06-27
- created_by_lane: claude/calibrate-pass1-note-stance (the IG Pass-1 calibration lane; provenance only, not authority)
- workspace: `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\great-curie-eb6ac9` ; repo `github.com/eric-foo/orca`
- handoff_path: `docs/prompts/handoffs/unify_capture_core_ig_yt_tiktok_planning_handoff_v0.md`
- expected_branch: the receiver branches a FRESH planning lane/worktree off `origin/main`. Do NOT reuse `claude/calibrate-pass1-note-stance` (it is merged).
- expected_head: `origin/main` @ `ba9b36b5` (Merge PR #414 — the IG Pass-1 extractor fix is on main).
- expected_dirty_state_including_handoff_file: this handoff file is newly written + UNTRACKED in the sender worktree (not yet committed to main). Also pre-existing untracked `docs/prompts/handoffs/calibrate_pass1_note_adjective_stance_resume_handoff_v0.md` (a different lane, ignore).
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact by READING the named files at `origin/main` before any strict/actionable claim. This packet is orientation, not authority. The sender analysed the IG lane deeply but did NOT analyse the YT lane — treat all YT pointers as unverified starting points.

## Goal Handoff

- long_term_goal: One capture core shared across Instagram, YouTube, and (later) TikTok that maximizes capture VOLUME at minimum detection FOOTPRINT, while still allowing platform-specific mechanics where they genuinely differ.
- anchor_goal: PLAN (analysis + architecture — NOT implementation) the shared capture core, in the owner's stated order: (1) analyse the IG lane's capture/extraction/saving, (2) analyse the YT lane's, (3) design a core applicable to all three (incl. TikTok later), (4) then sync IG + YT first.
- success_signal: a plan that (a) maps each lane's `enumerate -> render/scrape -> transcript -> comments -> persist -> extract` pipeline against the ACTUAL code, (b) names what is genuinely SHARED vs platform-DIVERGENT, (c) proposes the shared-core seam + per-platform adapter boundary with its lock-in explicitly called out, and (d) sequences the IG <-> YT sync as the first concrete unification step — all grounded in re-read source, not this packet's say-so.

## Open Decision / Fork

- decision: the SHAPE of the shared core (the step-3 architecture).
  - options:
    - (A) THIN core — share only low-lock-in layers (cadence / anti-detection pacing; the medallion lake save-schema; a `TranscriptSource` interface) and keep FAT platform adapters for enumerate + render.
    - (B) FRAMEWORK core — a full producer/consumer capture-orchestration (the IG ASR-decoupling shape) with platform plugins for enumerate / render / transcript.
    - (C) MINIMAL — formalize only what is ALREADY shared (the Pass-1 extractor) + a transcript-source interface; defer the rest.
  - already constrained / off the table: Pass-1 product extraction (`cleaning/transcript_product_extractor.py`) appears ALREADY shared by IG + YT (CONFIRM via the two extract tests) — so "extraction unification" is largely done; the real divergence is CAPTURE + SAVE + TRANSCRIPT-SOURCE. No-LLM in capture/scoring zones. Anonymous / no-proxy / no-stored-auth public capture. Never persist the transient signed media URL.
  - trade-offs: (B) FRAMEWORK is HIGH lock-in — a shared orchestration schema is costly to roll back; per the repo's Decision Priority (least compounded risk), surface it before committing. (A) THIN is reversible. IG (browser render + audio download + ASR) and YT (native captions + a different scrape) look mechanically quite different, which argues against forcing (B) prematurely.
  - owner of the call: the OWNER (the core architecture is a high-lock-in fork).
  - recommendation: do the analysis (steps 1-2) FIRST and let the real seams decide. Lean THIN (A) unless analysis shows the orchestration is genuinely common across IG-ASR and YT-captions. Put the core-architecture choice to the owner AFTER analysis, with lock-in flagged — do not default into a framework.

## Drift Guard

- This is a PLANNING lane: analyse + design + sequence. Do NOT implement the core or refactor either lane here.
- Do NOT break or refactor the working IG lane or YT lane; they ship independently today.
- no-LLM contract in capture/scoring zones (`tests/contract/test_no_llm_imports.py` scans `runners/`, `scoring/`, `schemas/`, `reports/`, `harness_utils.py`). Pass-1 extraction is agent-in-the-loop (subscription, no API key).
- Capture is anonymous, signed-out, no-proxy, no-stored-auth, public data only. The transient signed media URL must NEVER be persisted (host + used-flag only).
- The IG ASR-decoupling architecture is DESIGNED + de-correlated-reviewed but NOT merged; it lives ONLY in the sender's session scratchpad (ephemeral, likely UNREACHABLE to the fresh lane). It is INPUT to the core design, not a done thing. Key conclusion (inlined because the file may be gone): decouple the platform-touching render/scrape (the only footprint leg) from local ASR via a serial PRODUCER (the only platform-touching stage, independently paced/jittered via `source_capture/cadence.py`) + a bounded queue + PARALLEL ASR consumers. This "producer-with-independent-pacing + parallel local transcription" is the natural cross-platform core seam — evaluate it for IG/YT/TikTok, don't assume it.
- The Pass-1 extractor was just calibrated (`EXTRACTOR_RUBRIC_VERSION` 0.4, merged in #414). Do NOT re-touch the rubric in this lane.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: read `.agents/workflow-overlay/README.md` before project work (per `AGENTS.md`); entry map `docs/workflows/orca_repo_map_v0.md`.
- targets to enter the ladder: the IG / YT / shared file lists in the Source Ledger below, plus the two existing YT lane handoffs.
- already loaded (weak orientation, freshness-marked; NOT authority): the sender read the IG capture + extraction code deeply this session (rubric just calibrated). The sender did NOT read the YT capture code.
- must load first (before any strict/actionable step): the IG capture files + the YT capture files + `docs/prompts/handoffs/youtube_capture_lane_handoff_v0.md` and `docs/prompts/handoffs/youtube_downstream_ecr_cleaning_lane_handoff_v0.md` (the existing YT lane handoffs — read these for YT context the sender lacks).
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- IG capture mechanics: creator grid scan -> rank by engagement -> deep-capture top-N; per reel: browser render (fixed settle) -> parse DOM (audience comments + a transient signed audio URL) -> download audio -> faster-whisper ASR -> persist two silver lanes. Verify in: `source_capture/ig_reels_deep_capture.py` (`run_reel_deep_capture`) + `runners/run_source_capture_ig_reels_creator_deep_capture.py`. (origin/main; reread-required)
- Medallion lake: bronze->silver->gold under `F:/orca-data-lake` (EXTERNAL, gitignored). IG silver lanes `silver__capture__audience_comments` + `silver__capture__reel_transcript` per `<shortcode>`. Verify: `source_capture/ig_reels_deep_capture_lake.py` + `source_capture/writer.py`.
- Pass-1 extraction (likely SHARED): agent-in-the-loop product-mention extraction in `cleaning/transcript_product_extractor.py` (rubric 0.4). Used by BOTH IG reels and YT captions per `tests/unit/test_ig_reels_product_extract.py` + `tests/unit/test_youtube_caption_product_extract.py` — CONFIRM this is one shared extractor. Verify: those two tests + the extractor.
- Transcript divergence: IG = ASR only (no captions); YT = native CAPTIONS (`source_capture/transcript/youtube_captions.py`, `caption_packet.py`) and OPTIONALLY ASR (`runners/run_source_capture_youtube_asr_packet.py`). A `TranscriptSource` abstraction (captions | ASR) is a likely core seam. Verify: the `source_capture/transcript/` dir.

## Active Objective

A fresh PLANNING lane designs the unified cross-platform capture core. NOTE: the IG Pass-1 stance calibration that immediately preceded this is DONE + merged (#414) — this lane is a NEW direction (capture-mechanics unification), not a continuation of calibration.

## Exact Next Authorized Action

1. Branch a fresh planning lane/worktree off `origin/main` (`ba9b36b5`). Read `.agents/workflow-overlay/README.md` + `docs/workflows/orca_repo_map_v0.md`.
2. STEP 1 — Analyse the IG capture/extraction/save: read the IG files in the Source Ledger; produce a pipeline map (`enumerate -> render -> transcript -> comments -> persist -> extract`) + the footprint/cost of each leg.
3. STEP 2 — Analyse the YT capture/extraction/save: read the YT files + the two YT handoffs; produce the same pipeline map. (The sender has NO YT context — this step is genuinely new analysis.)
4. STEP 3 — Design the shared core: name SHARED vs DIVERGENT layers across IG/YT (and where TikTok would slot); propose the core seam + adapter boundary; put the core-architecture fork (A/B/C above) to the OWNER with lock-in flagged.
5. STEP 4 (only after the owner signs the core) — plan the IG <-> YT sync as the first concrete unification. STOP before implementing.
- Stop condition: planning only — do not implement or refactor. High-lock-in architecture decisions go to the owner.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/`. Entry map: `docs/workflows/orca_repo_map_v0.md`.
- User constraints: max capture / min footprint; per-platform mechanics may differ; eventually IG+YT+TikTok; PLAN first (analyse IG, analyse YT, design core, then sync IG+YT).
- Source-read ledger (all `Load-bearing: yes`; Compare target: `origin/main @ ba9b36b5`; `reread-required` — the receiver reads/analyses, the sender only points; sender verified IG paths exist via glob/grep, did NOT analyse YT):
  - IG capture: `orca-harness/source_capture/ig_reels_grid_capture.py`, `ig_reels_deep_capture.py`, `ig_reels_deep_capture_lake.py`, `ig_reels_comments.py`, `transcript/ig_reels_audio_packet.py`; `orca-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py`, `run_source_capture_ig_reels_deep_capture.py`, `run_ig_reels_product_extract.py`.
  - YT capture (sender NOT analysed): `orca-harness/youtube_capture/capture_youtube_v0.py`, `shorts_scroll_capture_v0.py`, `stealth_client.py`, `enrich_ryd_v0.py`; `orca-harness/source_capture/transcript/youtube_captions.py`, `caption_packet.py`; `orca-harness/runners/run_source_capture_youtube_caption_packet.py`, `run_source_capture_youtube_asr_packet.py`. YT handoffs: `docs/prompts/handoffs/youtube_capture_lane_handoff_v0.md`, `youtube_downstream_ecr_cleaning_lane_handoff_v0.md`.
  - SHARED candidates (the core surface): `orca-harness/source_capture/cadence.py` (pacing/anti-detection — `build_cadence_plan`), `source_capture/adapters/{browser_snapshot,cloakbrowser_snapshot,anti_blocking_http,direct_http}.py`, `source_capture/proxy_profiles.py`, `source_capture/auth_state.py`, `source_capture/transcript/{audio_asr,asr_packet}.py` (ASR, shared by IG + YT-ASR), `source_capture/writer.py` (lake writer), `cleaning/transcript_product_extractor.py` + `cleaning/models.py` (shared Pass-1 extractor), `runners/run_capture_ecr_cleaning_smoke.py` (the capture->ECR->cleaning pipeline shape).
  - Prior IG operating context: `docs/prompts/handoffs/ig_reels_transcript_extraction_lane_handoff_v0.md`, `ig_capture_rate_at_scale_operating_envelope_handoff_v0.md`.
- Source gaps: the sender has NO YT-lane analysis; TikTok has no code yet (greenfield). The IG ASR-decoupling arch doc is scratchpad-only (key conclusion inlined in Drift Guard).
- Not-proven boundaries: "extraction is shared" is inferred from test names — CONFIRM. The shared-core architecture is undecided (owner fork).

## Current Task State

- Completed: IG Pass-1 calibration lane (separate, merged #414). Both IG and YT capture lanes exist + ship independently.
- Partially completed: the IG ASR-decoupling architecture (designed + reviewed, NOT merged, scratchpad-only).
- Broken or uncertain: none known; the capture-unification is a fresh planning effort.

## Workspace State

- Branch (sender): `claude/calibrate-pass1-note-stance` @ `770295dc` (MERGED via #414; DO NOT reuse).
- `origin/main` @ `ba9b36b5` (carries the IG Pass-1 fix). Receiver branches off this.
- Dirty before this handoff: pre-existing untracked `docs/prompts/handoffs/calibrate_pass1_note_adjective_stance_resume_handoff_v0.md` (other lane).
- Dirty after writing this handoff: + `docs/prompts/handoffs/unify_capture_core_ig_yt_tiktok_planning_handoff_v0.md` (UNTRACKED). NOT committed. For the fresh lane to read it durably, the owner should commit/PR it to main (owner-gated) OR the fresh lane reads it from this worktree path.
- Related: no worktree for the new lane yet — the receiver creates one off main.

## Changed / Inspected / Tested Files

- None changed (planning handoff). The files to ANALYSE are in the Source Ledger. The sender INSPECTED (this session): the IG capture + extractor files; did NOT inspect the YT files.

## Frozen Decisions

- The Pass-1 extractor (`cleaning/transcript_product_extractor.py`, rubric 0.4, #414) is shared + calibrated; capture-unification does NOT change extraction. Evidence: #414 merged; both IG + YT extract tests reference it.
- Capture stays anonymous / no-proxy / no-stored-auth; no-LLM in capture/scoring; never-persist-signed-URL. Consequence: the shared core must preserve these invariants.

## Mutable Questions

- How much is genuinely shared vs platform-divergent (the analysis answers this).
- Is the IG ASR-decoupling producer/consumer shape the right cross-platform core, or IG-specific?
- Does YT's native-captions path obviate ASR for YT, changing the transcript-source seam?
- TikTok specifics (no code yet — greenfield; what does its capture surface look like?).

## Superseded / Dangerous-To-Reuse Context

- Branch `claude/calibrate-pass1-note-stance` is MERGED — do not reuse; branch fresh off main. Replacement: a new lane off `ba9b36b5`.
- The scratchpad ASR-decoupling arch doc (`asr_decouple_architecture_v0.md`) is in the SENDER's session scratchpad (ephemeral, likely inaccessible). Replacement: its key conclusion is inlined in the Drift Guard; do not assume the file is reachable.
- The IG calibration corpus + read scripts are sender scratchpad working data — irrelevant to capture-mechanics unification.

## Commands And Verification Evidence

- Confirm main carries the IG fix (sanity that you're on the right base):
  ```bash
  git show origin/main:orca-harness/cleaning/transcript_product_extractor.py | grep EXTRACTOR_RUBRIC_VERSION
  ```
  Result: expect `"0.4"` (not run / passed: receiver runs to confirm).
- no-LLM contract (re-run target so the receiver confirms the invariant before designing a core that must preserve it):
  ```bash
  python -m pytest orca-harness/tests/contract/test_no_llm_imports.py -q
  ```

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify before acting: (a) the IG file roles — re-read the IG files (sender analysed these, but rebind fresh); (b) the YT file roles — re-read the YT files + YT handoffs (sender did NOT analyse — these are unverified); (c) "extraction is shared" — confirm via the two extract tests; (d) base = `origin/main @ ba9b36b5`.
- Compare target for each: `origin/main @ ba9b36b5`; `reread-required`.
- Load outcomes: `REUSE` only after reading the named files; `STALE_REREAD_REQUIRED` if main advanced past `ba9b36b5`; `BLOCKED_MISSING_PACKET` if this handoff path is gone; `BLOCKED_UNVERIFIABLE` if a YT pointer cannot be located (the sender did not verify YT roles).
- Sources to reread on drift: the Source Ledger files at the current `origin/main`.

## Do Not Forget

- This lane PLANS; it does not implement. The core architecture is a HIGH-lock-in fork for the OWNER — surface it, do not default.
- Extraction is LIKELY already shared (confirm) — the real divergence is CAPTURE + SAVE + TRANSCRIPT-SOURCE.
- The sender analysed IG deeply; did NOT analyse YT — STEP 2 is genuinely new analysis; trust the YT pointers only after reading them.
