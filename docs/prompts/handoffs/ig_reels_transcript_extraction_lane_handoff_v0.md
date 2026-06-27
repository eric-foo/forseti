# Handoff Packet — IG Reels Transcript→Product Extraction Lane (reuse the YouTube structure)

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet
scope: >
  Transfers the YouTube transcript->product extraction STRUCTURE to a fresh IG
  Reels lane so it builds IG Reels transcript->product extraction by reuse, not
  reinvention. Carries the reusable spine/lake/extraction/daemon patterns and the
  IG-specific deltas only; not YouTube capture minutiae.
use_when:
  - Starting or staffing the IG Reels transcript->product extraction lane.
  - Deciding what of the YouTube transcript lane is reusable vs IG-specific.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
downstream_consumers:
  - IG Reels capture + transcript + extraction lane
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-25
- created_by_lane: YouTube transcript/extraction lane (provenance only; not authority)
- workspace: the Orca repo; the IG lane works off `main`
- handoff_path: `docs/prompts/handoffs/ig_reels_transcript_extraction_lane_handoff_v0.md`
- expected_branch: build on a fresh branch off `main` (e.g. `claude/ig-reels-transcript-extraction`)
- expected_head: whatever `origin/main` is when you start — **do not assume a pinned SHA; main moves fast**
- load_rule: **confirm-don't-trust** — every load-bearing fact below is a hypothesis; re-read the named source on current `main` before any strict/actionable claim. This packet orients; it does not authorize.

## Goal Handoff

- long_term_goal: a daemon-driven, medallion-lake fragrance-signal pipeline across public social/retail sources, feeding Judgment.
- anchor_goal: build **IG Reels transcript→product extraction** — capture public IG Reels, derive a transcript (ASR), and extract structured product mentions into the lake — reusing the already-merged YouTube lane's structure rather than reinventing it.
- success_signal: an IG Reel id flows end-to-end — capture → `SourceCapturePacket`(s) in the lake → ASR transcript derived record → `silver__cleaning__product_mentions` records with verbatim quote + timestamp — under the same daemon-readiness + no-LLM-zone + medallion guarantees the YouTube lane meets, with IG as its own `source_family`.

## Open Decision / Fork

- **decision:** Does the YouTube extraction prompt + `ProductMention` schema transfer to IG fragrance Reels as-is, or need IG-specific tuning?
  - options: (a) reuse `transcript_product_extractor.py` prompt/schema unchanged; (b) fork an IG-tuned prompt while keeping the schema; (c) extend the schema.
  - already constrained: the **extraction *pattern*** (LLM-reads-quote / code-locates-and-decides, no verdict field) is settled and must be preserved; only prompt wording / schema *fields* are in play.
  - trade-offs: (a) fastest, risks IG-context misses; (b) safest for quality, small dup; (c) only if a real IG-only field exists.
  - owner of the call: IG-lane builder + owner; recommend starting at (a), measure, escalate to (b) only on observed misses.
- **decision:** Do IG Reels need their own spec doc analogous to the YouTube one?
  - recommendation: yes, a thin `ig_reels_transcript_product_extraction_spec_v0.md` that *references* the YouTube spec's CE1–CE10 and records only the IG deltas (ASR-only, stealth capture, source_family).

## Drift Guard

- **IG is a SEPARATE lane from YouTube.** Do not modify YouTube lane code/spec to fit IG; add IG as its own `source_family` + its own modules. Cross-lane reuse is by *pattern*, not by editing the YouTube files.
- **Standing capture constraints (non-negotiable):** public-data only; **anonymous-only** (no login / no `po_token` / no authenticated session); **no proxy by default**; SG-legal non-criminal use; **NEVER commit captured or derived data** (the data root is external + gitignored).
- **The lake authority spine is ratified and source-family-agnostic — reuse it, do not re-derive it.** Raw is write-once + sha256-verified; derived is append-only; indexes are rebuildable/non-authoritative; gold is Judgment-only and never a stored label. Adding IG must not weaken any of these.
- **No-LLM zone:** AI lives only in `cleaning/`. Do not import `openai`/`anthropic`/`litellm`/`langchain` into scoring/reports/runners/schemas — a contract test (`tests/contract/test_no_llm_imports.py`) AST-bans it.
- **Do not trust this packet's code quotes.** Main moves fast; re-read every named file on current `main` before building.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: read `.agents/workflow-overlay/README.md` first, then `docs/workflows/orca_repo_map_v0.md` (the repo map) — per `AGENTS.md`. Follow the Orca overlay before project work.
- targets to enter the ladder early (re-read on current `main`): the YouTube transcript spine + extraction files and the data-lake authority spine, listed in the Source Ledger below.
- already loaded: nothing in your lane — this is a cold start.
- must load first (before any actionable step): the data-lake authority spine (it governs where IG packets/records land) and the YouTube extraction spec + extractor (the pattern you mirror).

### Earlier-decided concepts (inline gist + verify pointer)

- **Medallion lake / tier-via-lane-name:** bronze = `raw/<packet_id>/` (raw capture); silver/gold = `derived/<raw-anchor>/<lane>/<record>` where the lane *name* encodes tier+producer+kind (e.g. `silver__cleaning__product_mentions`); gold is Judgment-only. Verify in `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`.
- **Per-surface packets:** one write-once packet per surface per item (watch-metadata, comments, audio) — a fat multi-surface packet is forbidden because raw is write-once and surfaces refresh on different cadences; use `source_slices` for co-captured sub-views; correlate surfaces via a per-item index. Verify in the raw-admission + storage contracts.
- **Typed metric_observations:** engagement counts (views/likes/comments) are typed observations with a posture, so absence is never stored as a fake `0`. Verify in `orca-harness/source_capture/models.py` (`SourceCaptureSlice.metric_observations`, `MetricPosture`).
- **CE5/CE9 quote-locator (the extraction crux):** the LLM returns a *verbatim quote*, not a timestamp; code locates that quote in the transcript cues to **both** prove it is real (reject if absent = CE9) **and** assign `start_ms`/`end_ms` from the covering cue (CE5). Verify in `orca-harness/cleaning/transcript_product_extractor.py` (`locate_quote`, `parse_mentions`).
- **Daemon-readiness contract:** idempotent skip-if-done, stateless/resumable, per-packet + per-item failure isolation, single entrypoint a cron wraps. Verify in `orca-harness/runners/run_transcript_product_extract.py`.

## Active Objective

Build the IG Reels transcript→product extraction lane: IG-Reel capture (stealth HTTP) → per-surface `SourceCapturePacket`s → VAD-gated faster-whisper ASR on the Reel audio → `transcript_asr` derived record → Cleaning extraction → `silver__cleaning__product_mentions`. Reuse the YouTube *patterns*; add IG as its own `source_family`.

## Exact Next Authorized Action

1. Read the overlay (`.agents/workflow-overlay/README.md`) + repo map, then the Source Ledger files on current `main`.
2. Confirm the current lake raw/derived layout on `main` (see drift note: raw+derived sharding may have landed — build against whatever is on `main`).
3. Architecture-plan the IG lane: which YouTube modules map 1:1 (extractor, lake driver, runner, schema, asr_packet) vs need an IG variant (capture, source_family, ASR entrypoint). Surface the two Open Decisions above.
4. Build capture (reuse `stealth_client.py`) → ASR (reuse `audio_asr.py`/`asr_packet.py` pattern) → extraction (reuse `transcript_product_extractor.py` pattern) → daemon runner; offline/network-free tests throughout.
5. Stop condition: do not touch YouTube lane files; do not weaken any lake invariant; keep AI out of the no-LLM zone.

## Authority And Source Ledger

All entries are **`reread-required`** (main moves fast; read on current `main` before strict use). All are **Load-bearing: yes** unless noted.

- `AGENTS.md` + `.agents/workflow-overlay/README.md` — repo instructions + overlay; read first. Reuse rule: follow before project work.
- `docs/workflows/orca_repo_map_v0.md` — repo map / navigation. Reuse rule: orient, then read named source.
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md` — the extraction spec (CE1–CE10, Decisions 1–10). Role: the pattern you mirror for IG.
- `orca-harness/cleaning/transcript_product_extractor.py` — the LLM extractor + CE5/CE9 quote-locator. Role: copy the pattern, not the YouTube specifics.
- `orca-harness/cleaning/transcript_product_lake.py` — silver-mentions persist + cue conversion. Role: lake-driver pattern.
- `orca-harness/schemas/product_mention_models.py` — `ProductMention` / `StatedRating` (finite-guarded, verdict-free). Role: candidate reuse as-is (Open Decision).
- `orca-harness/runners/run_transcript_product_extract.py` — daemon-ready runner (isolation, idempotency). Role: runner pattern.
- `orca-harness/source_capture/transcript/audio_asr.py` + `asr_packet.py` — VAD-gated faster-whisper ASR → `transcript_asr` derived record. Role: **the primary IG transcript path** (Reels have no caption track).
- `orca-harness/source_capture/transcript/youtube_captions.py` + `caption_packet.py` — caption-first path. Role: **context only — does NOT apply to IG** (no caption API).
- `orca-harness/source_capture/models.py` — `SourceCapturePacket` / `SourceCaptureSlice` / `metric_observations`. Role: the packet model IG capture must produce.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_*.md` (storage, physicality_location, raw_admission_key_grammar, derived_layout_index_rebuild, medallion_gold_readiness) — ratified, source-family-agnostic lake law. Role: governs where IG packets/records land.
- `orca-harness/youtube_capture/stealth_client.py` — Chrome-impersonating anonymous HTTP client (`curl_cffi`). Role: **the reusable capture network layer for IG** (not yt-dlp).
- `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py` — existing IG Reels capture. Role: existing IG capture entrypoint to build on.
- `tests/contract/test_no_llm_imports.py` — the no-LLM-zone guard. Role: keep AI in `cleaning/` only.
- Not-proven boundary: nothing has been run live at scale; IG comment-capture depth/limits and IG ASR quality on Reel audio are unmeasured.

## Current Task State

- Completed (merged on `main`, reusable): the entire YouTube transcript spine + product extraction Pass-1 + the ratified data-lake authority spine.
- Partially completed / in-flight (NOT on `main` yet): raw (and possibly derived) directory **sharding** — see Superseded/Drift.
- Broken or uncertain (for IG): none yet — IG lane is greenfield on top of reusable structure.

## Frozen Decisions (reuse — do not re-litigate)

- Transcript spine shape: acquisition → `SourceCapturePacket` → ECR/SCR/Cleaning derived records. Consequence: IG follows the same shape.
- Extraction = LLM-reads-quote / code-locates-and-decides; `ProductMention` has **no verdict field by construction** (CE4). Consequence: keep verdict deterministic + deferred (Pass 2).
- Lake placement is ratified + source-family-agnostic. Consequence: IG reuses it; it does not get its own lake.
- AI confined to `cleaning/`. Consequence: IG capture/ASR/runner code stays LLM-free.

## Mutable Questions (the IG deltas to design)

- IG extraction prompt/schema: reuse vs IG-tune (Open Decision 1).
- IG Reels spec doc: thin delta-spec recommended (Open Decision 2).
- IG comment capture depth/limits — unmeasured; decide at build.
- ASR quality on Reel audio (music/voiceover mix) — measure; the YouTube VAD gate (faster-whisper `vad_filter`) is the starting point.

## Superseded / Dangerous-To-Reuse Context

- **Lake raw/derived layout is changing:** raw sharding `raw/<shard>/<packet_id>/` (shard = `sha256(packet_id)[:3]`, 4096 buckets) is **in-flight on branch `claude/data-lake-raw-sharding`, NOT merged**, and derived sharding is undecided. **Do not hardcode `raw/<packet_id>/`** — always go through the `data_lake.root.DataLakeRoot` by-key API (`find_packet`/`load_raw_packet`/`allocate`/`stage`/`publish`), which abstracts the physical path. Build against whatever lake layout is on `main` when you start; re-read `orca-harness/data_lake/root.py` then.
- The caption-first transcript path (`youtube_captions.py`) does **not** transfer to IG (no caption API) — ASR is primary. Reusing it for IG would be a dead end.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: current `origin/main` HEAD; the lake raw/derived layout on `main` (sharded or not — read `data_lake/root.py`); the extractor's `locate_quote`/`parse_mentions` still match the CE5/CE9 description; the no-LLM contract test still guards the same dirs.
- Compare target for each: `reread-required` (read the file on current `main`).
- Load outcomes: `REUSE` only after re-reading the lake authority + extractor on `main`; `STALE_REREAD_REQUIRED` if `main` moved (it will have); `BLOCKED_UNVERIFIABLE` if a named source is missing — report which and stop, do not proceed on this packet's say-so.
- Reread on drift: the data-lake authority spine, `data_lake/root.py`, `transcript_product_extractor.py`, `stealth_client.py`.

## Do Not Forget

- IG is its own `source_family` and its own lane — reuse YouTube by pattern, never by editing YouTube files.
- ASR is the IG transcript path; captions are YouTube-only.
- Go through the `DataLakeRoot` by-key API; never hardcode raw physical paths (they are sharding).
- Public-only, anonymous, no-proxy-default, never-commit-captured-data, SG-legal — these bind every capture line.
