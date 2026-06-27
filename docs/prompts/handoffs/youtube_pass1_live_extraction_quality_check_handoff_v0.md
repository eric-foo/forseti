# Handoff Packet — YouTube Pass-1 Live-Model Extraction Quality Check

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (continuation artifact; NOT validation/readiness evidence) -- transfers the YouTube Pass-1 product-mention extraction LIVE-MODEL QUALITY CHECK to a fresh lane (Codex).
scope: >
  The only remaining deferred slice of the completed YouTube ECR/cleaning lane: validate that a real
  Sonnet model extracts product mentions well from REAL captured YouTube transcripts, run on the owner's
  Claude subscription (no API key, no metered billing, no production daemon). A quality check, not a build.
use_when:
  - Picking up the YouTube Pass-1 live-extraction quality check.
  - Confirming what is done/merged vs deferred on the YouTube transcript->product lane.
authority_boundary: retrieval_only
status: HANDOFF_OPEN -- cold-reader continuation artifact; the receiver runs the confirm-don't-trust load contract before any actionable step.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-27 (verify via `git log`)
- created_by_lane: Claude Code session on branch `claude/agents-decision-priority-and-scoping` -- provenance only, NOT an authority claim
- workspace: the Orca repo (github.com/eric-foo/orca)
- handoff_path: docs/prompts/handoffs/youtube_pass1_live_extraction_quality_check_handoff_v0.md
- expected_branch: main (this packet was authored off `origin/main`; branch YOUR work off the LATEST `origin/main`)
- expected_head: `origin/main @ 949ed187` at authoring -- STALE by the time you read this; re-fetch
- expected_dirty_state_including_handoff_file: this handoff `.md` is newly added (committed on branch `claude/youtube-pass1-live-check-handoff`); tree otherwise clean
- load_rule: confirm-don't-trust -- re-verify every load-bearing fact against its compare target before acting; the sender's claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: a working YouTube consumer-demand pipeline where creator product mentions become trustworthy verdicts (capture -> ECR -> cleaning -> judgment).
- anchor_goal: validate that a real Sonnet model extracts product mentions WELL from REAL captured YouTube transcripts -- run on the owner's Claude subscription (no API key) -- as a quality check, not a production build.
- success_signal: a recorded sample of real captured YouTube transcripts run through a LIVE Sonnet extraction, with the extracted mentions + a plain quality read (does it find the right products; get brand / line / stance / verbatim-quote right on messy real transcripts), produced WITHOUT an API key.

## Open Decision / Fork

- decision: which execution path for the live check.
  - options:
    1. Reuse a CODEX-side IG / social-media live-extraction or subscription-Sonnet-check setup IF one exists -- the owner believes one may; Codex MUST search its own worktrees / sessions / notes FIRST.
    2. Reuse the Claude-side proven pattern `claude_sonnet_isolated_subagent_v0` (a Sonnet subagent run ISOLATED, `tool_uses=0`, subscription-backed, structured output + a run receipt) under `orca-harness/cases/product_learning/*/runs/`.
    3. Build a thin live transport for `run_extraction` ONLY if neither precedent fits.
  - already constrained / off the table: NO production daemon; NO metered API key (subscription only); NO Pass-2 / gold; NO IG (YouTube-only).
  - trade-offs: (1) least work if it exists; (2) proven Claude pattern but built for JUDGMENT, so adapt the rubric to product-extraction; (3) most work, last resort.
  - owner of the call: the implementing agent (Codex), with owner steering.
  - recommendation: do (1) FIRST; if absent, do (2) adapted to the Pass-1 product-extraction rubric. Sonnet 4.6 default; optionally benchmark ONE sample on Opus 4.8 for a quality ceiling.

## Drift Guard (do NOT cross)

- NO always-on production daemon -- explicitly not wanted; this is a one-off sample check.
  - why it matters: the owner does not want production infra; "live transport" was deferred as a QUALITY question, not a build. Violating it builds unwanted infra.
- NO metered API key -- subscription only.
  - why: owner constraint. A programmatic daemon would need the metered Anthropic API; out of scope. Violating it spends money + handles a key the owner declined.
- NO Pass-2 / gold verdicts -- owner-deferred (the "gold-write" lane, deferred pending IG+YT structural sync).
  - why: touching gold re-opens a deferred, high-lock-in lane.
- NO re-doing the ECR / cleaning / audit wiring -- done + merged (#401, #405, #408).
- NO changes to the deterministic core / no-LLM zone (`orca-harness/scoring/`, `orca-harness/tests/contract/test_no_llm_imports.py`).
- NO IG wiring -- that is the IG lane's, deferred. This handoff is YouTube-only.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/` -- read `README.md` first, `source-of-truth.md` for precedence, the repo map `docs/workflows/orca_repo_map_v0.md` for navigation. Per `AGENTS.md`, read the overlay before project work.
- targets to enter the ladder: the seam files (below) + the `product_learning` cases receipts + the YouTube transcript->product extraction spec.
- already loaded (weak orientation, freshness-marked, NOT authority): this packet's claims about the seam + the precedent; freshness = authored at `origin/main 949ed187`, STALE on read.
- must load first (before any actionable step): the two seam files + one `claude_sonnet_isolated_subagent_v0` receipt, on the LATEST `origin/main`.
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only SEEDS the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- The transport seam is the ONLY AI station; capture, ECR, Pass-2 fusion, and the audit are all deterministic / no-LLM.
  - decided in: `orca-harness/cleaning/transcript_product_extractor.py` + the no-LLM contract test. compare: reread-required. verify before: any actionable step.
- AO-2: ASR transcripts get a `derived_record` cleaning anchor + audit lake-read (PR #405, MERGED).
  - decided in: `docs/decisions/cleaning_derived_record_anchor_contract_v0.md`. compare: reread-required.
- Durable derivation-time content hash for derived records (PR #408, MERGED).
  - decided in: `docs/decisions/derived_record_durable_content_hash_v0.md`. compare: reread-required.
- Medallion tiers: bronze = raw bytes; silver = the transcript AND the extracted mentions (`silver__cleaning__product_mentions`); gold = verdicts (DEFERRED). The live check is silver -> silver.
  - decided in: the YouTube transcript->product spec under `orca/product/spines/capture/core/source_families/social_media/youtube/`. compare: reread-required.

## Active Objective

Run a one-off, subscription-backed LIVE Sonnet extraction over a SAMPLE of real captured YouTube transcripts, using the existing transport-injected Pass-1 extractor, and produce the extracted product mentions + a plain quality read -- answering "does a real model extract well on real transcripts?" without an API key or any production infra.

## Exact Next Authorized Action

1. CHECK CODEX-SIDE PRECEDENT FIRST: search Codex's own worktrees / sessions / notes for an existing IG (or social-media) live-extraction / subscription-Sonnet-check setup; if found, reuse / adapt it for YouTube.
2. Re-read the seam on the LATEST `origin/main`: `orca-harness/cleaning/transcript_product_extractor.py` (`extract_transcript_products` -- the rubric, the CE9 quote-locator, the CE5 timestamp-from-cue) + `orca-harness/runners/run_transcript_product_extract.py` (`run_extraction(*, data_root, transport, provider, model, api_key, ...)`). Re-read the offline `FakeTransport` stub in `orca-harness/tests/unit/test_youtube_caption_product_extract.py` to see the transport contract the live model must satisfy.
3. Re-read the proven pattern: `orca-harness/cases/product_learning/*/runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml` + the sibling `cross_vendor_blind_run_findings_v0.md` -- mirror the isolated-subagent (`tool_uses=0`) + run-receipt shape.
4. Obtain a SAMPLE of real captured YouTube transcripts (a few `youtube_captions` / `youtube_audio` packets in a data lake; capture a small handful if none exist -- staying within the no-daemon / no-IG guard).
5. Run the extraction LIVE via the subscription-subagent pattern (Sonnet 4.6): feed each transcript + the Pass-1 rubric to an isolated Sonnet subagent, get the structured mentions, and confirm the CE9 quote-locator still finds the quotes verbatim in the cues.
6. Deliverable: the extracted mentions for the sample + a plain quality read (right products? brand / line / stance / quote correct?), recorded with a run receipt. Optionally benchmark ONE sample on Opus 4.8.
- Stop condition / success: the recorded sample + quality read exists, produced WITHOUT an API key. Do NOT proceed to a production daemon, Pass-2 / gold, or IG.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ `CLAUDE.md` shim) + `.agents/workflow-overlay/`. reread-required.
- Overlay / authority: `.agents/workflow-overlay/` (source-of-truth, safety-rules, decision-routing). reread-required.
- User constraints: subscription only (no API key); no production daemon; YouTube-only (IG deferred); Pass-2 / gold deferred.
- Source-read ledger:
  - `orca-harness/cleaning/transcript_product_extractor.py`
    - Role: the Pass-1 LLM extractor (the rubric + CE9 quote-locator + CE5 timestamp). Load-bearing: yes. Compare target: reread-required (main moves fast). Reuse rule: the live model must satisfy the transport contract this file expects.
  - `orca-harness/runners/run_transcript_product_extract.py`
    - Role: the daemon-ready runner with an INJECTED transport / model / api_key. Load-bearing: yes. Compare target: reread-required. Reuse rule: inject a real (subscription-backed) transport here for a SAMPLE; do NOT turn it into an always-on daemon.
  - `orca-harness/tests/unit/test_youtube_caption_product_extract.py`
    - Role: the offline `FakeTransport` contract the live transport must mimic. Load-bearing: yes. Compare target: reread-required.
  - `orca-harness/cases/product_learning/*/runs/claude_sonnet_isolated_subagent_v0/`
    - Role: the proven subscription-Sonnet-subagent pattern + run-receipt shape (built for JUDGMENT; adapt the rubric). Load-bearing: yes. Compare target: reread-required.
  - `docs/decisions/cleaning_derived_record_anchor_contract_v0.md` + `docs/decisions/derived_record_durable_content_hash_v0.md`
    - Role: the merged AO-2 + durable-hash context. Load-bearing: no (context). Compare target: reread-required.
- Source gaps: whether a Codex-side IG precedent exists (check Codex); where real captured YouTube transcripts live (a data lake / `ORCA_DATA_ROOT`).
- Strict-only blockers: a live model call needs the owner's subscription session (Codex / Claude Code), not an API key.
- Not-proven boundaries: extraction QUALITY on real transcripts is UNPROVEN -- only the offline stub has run. Proving it is exactly this lane's job.

## Current Task State

- Completed (MERGED to main): #401 (captions -> ECR + Pass-1), #405 (ASR `derived_record` anchor + audit lake-read), #408 (derivation-time durable hash). Verify via `gh pr view` / `git log`.
- Partially completed: none -- the ECR / cleaning wiring is complete; this live-check slice is NOT started.
- Broken or uncertain: none known. The only open question is extraction quality on real data (the goal of this lane).

## Workspace State

- Branch: main (author off the LATEST `origin/main`; do not build on this packet's stale head).
- Head: `origin/main @ 949ed187` at authoring (stale on read; re-fetch).
- Dirty / untracked before handoff: clean.
- Dirty / untracked after writing this file: this handoff `.md` is newly added on branch `claude/youtube-pass1-live-check-handoff`.
- Target files / artifacts: the seam files + a sample of real transcripts + a recorded extraction sample.
- Related worktrees / branches: many active lanes (main moves fast); Codex worktrees may hold the IG precedent.

## Frozen Decisions

- The transport is INJECTED (the seam exists); the live check plugs a real Sonnet in at that one seam.
  - Evidence: `run_extraction(*, transport, model, api_key, ...)` + the `FakeTransport` stub. Consequence: no new architecture needed for the check.
- Subscription, not API key; no production daemon.
  - Evidence: owner instruction this session. Consequence: use the isolated-subagent pattern, not a metered-API daemon.
- Pass-2 / gold + IG are deferred.
  - Evidence: owner; the gold-write article (deferred); IG -> IG-lane (owner, chat-only). Consequence: out of scope.

## Mutable Questions

- Does a Codex-side IG / social live-extraction precedent exist? -- resolves by Codex checking its own side.
- Sonnet 4.6 (default) vs an Opus 4.8 benchmark on a sample? -- resolves by the sample quality read.
- Where are real captured YouTube transcripts (which data lake)? -- resolves by checking the owner's `ORCA_DATA_ROOT` / capturing a small sample.

## Superseded / Dangerous-To-Reuse Context

- The ORIGINAL YouTube lane handoff `docs/prompts/handoffs/youtube_downstream_ecr_cleaning_lane_handoff_v0.md` -- its scope (ECR-wiring + offline Pass-1) is DONE + merged; do not re-do it. Its "Pass-2 deferred" guard is STILL true. Replacement: THIS packet (the live-check slice).
- "Pass-1 validated" -- TRUE only OFFLINE (`FakeTransport`). Do NOT read it as "extraction quality proven on real data." That is unproven and is this lane's job.

## Commands And Verification Evidence

- Confirm the merged work:
  ```bash
  gh pr view 401 --repo eric-foo/orca --json state,mergedAt
  gh pr view 405 --repo eric-foo/orca --json state,mergedAt
  gh pr view 408 --repo eric-foo/orca --json state,mergedAt
  ```
  Result: all MERGED at authoring (re-run to confirm; do not trust).
- Find the seam + the precedent on latest main:
  ```bash
  git grep -n "def run_extraction" origin/main -- orca-harness/runners/run_transcript_product_extract.py
  git ls-tree -r --name-only origin/main -- 'orca-harness/cases/product_learning' | grep claude_sonnet_isolated_subagent
  ```
- Offline suite (the deterministic baseline -- must stay green):
  ```bash
  cd orca-harness && python -m pytest --junit-xml=out.xml -q   # read the <testsuite errors=.. failures=.. tests=..> header
  ```

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify before acting:
  - the `run_extraction` signature + the transport contract (re-read the extractor + the `FakeTransport` stub).
  - the `claude_sonnet_isolated_subagent_v0` receipt shape (re-read a `run_001/blind_judgement.yaml`).
  - that #401 / #405 / #408 are merged (`gh pr view`).
- Compare target for each: reread-required -- re-fetch + re-read on the LATEST `origin/main`.
- Load outcomes: `REUSE` only after re-verifying the seam + precedent on latest main; `STALE_REREAD_REQUIRED` if the seam moved; `BLOCKED_UNVERIFIABLE` if the named files are gone (then re-locate by content, do not proceed on say-so).
- Sources to reread if drift: the two seam files + one cases receipt + the overlay `README.md`.

## Do Not Forget

- Check the CODEX side for an existing IG live-extraction precedent BEFORE building anything -- the owner believes one may exist there.
- This is a one-off SUBSCRIPTION quality check, NOT a build: no daemon, no API key, no Pass-2 / gold, no IG.
