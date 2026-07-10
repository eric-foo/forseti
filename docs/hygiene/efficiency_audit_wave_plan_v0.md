# Efficiency Audit — Wave Plan & Tracking Checklist v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow hygiene tracking checklist
scope: >
  Durable checklist for the efficiency-audit findings produced by a 14-lane
  read-only subagent fan-out on 2026-07-09. Groups ~100 findings into 8 topics
  and 3 execution waves. Tracking + navigation only.
use_when:
  - Executing or reviewing an efficiency-audit wave (T1-T8) on this lane.
  - Checking which audit findings are open, in-flight, landed, or deferred.
  - Locating the file:anchor for a specific finding ID.
authority_boundary: retrieval_only
stale_if:
  - A topic's findings are all landed or the topic is retired.
  - The orca->forseti filename-migration campaign completes (unblocks Deferred items).
  - A later audit supersedes this plan.
```

> **What this is.** A tracking checklist, not authority and not a readiness
> claim. Findings came from a read-only audit; each is advisory until verified
> in its own fix + validation. On any conflict the owning source wins.
>
> **Non-claims.** Not validation, not readiness, not approval, not a doctrine
> change, not buyer proof. Line anchors are as-observed on 2026-07-09 and may
> drift as the migration campaign lands other PRs — re-confirm before editing.

- Provenance: 14 read-only audit lanes (`APH-CORE, APH-RSCH, APH-IMPL, APH-HAND,
  OVL, HOOK, NAV, DEC, CER, RE-CSB, RE-CAP, RE-HARN, REF, DUP`), 2026-07-09.
- Lane: `claude/subagent-efficiency-plan-eab2dc` (worktree, off `main`).
- Status legend: `[ ]` open · `[~]` in-flight · `[x]` landed · `[-]` deferred · `[!]` owner-gated.

## Guardrails (do NOT)

- Do **not** consolidate the Aphrodite doctrine set — well-factored by lifecycle/ownership (verified by APH-CORE + APH-RSCH).
- Do **not** blanket `orca->forseti` sweep — `moved_paths_index.md` redirects work by design; fix only dead refs inside **live mechanisms** that bypass the redirect.
- Do **not** rewrite frozen review outputs for the rename (repo doctrine protects them).
- Do **not** strip retrieval headers or bespoke `## Non-Claims` bodies (protected overclaim guards, ~1,200+ files).
- Do **not** delete the "unwired" staged harness slices (RE-HARN-7) — intentional; decide wire-or-park.
- AGENTS.md is already tight (~1.5% reducible) — not a real lever.

---

## Wave 1 — safe sweep (high-confidence, low-effort, zero efficacy loss)

Execution order: T2 (rename bugs) → T1 (receipt archival) → T3 S-effort code bugs → T6 staleness → CER-3 drift.

### T2 · Rename-debt dead refs inside live mechanisms  `[bug]`
- [ ] **HOOK-2** (W1) — `header_index --report-orca` walks non-existent `orca/product/spines` tree → repoint to `forseti/product/spines` — `.agents/hooks/header_index.py:736`
- [ ] **HOOK-7** (W1) — `header_index` fallback reads legacy `orca_repo_map_v0.md` → repoint to `forseti_repo_map_v0.md` — `.agents/hooks/header_index.py:292`
- [ ] **NAV-2** (W1) — repo map's pasted permissions/hooks JSON has desynced from live settings → delete JSON, point to `.claude/settings.json` — `docs/workflows/forseti_repo_map_v0.md:113-121,274-303,329-337`
- [ ] **RE-CSB-4** (W1) — dead `orca_` paths in an active sha256 provenance-pin → repoint the 4 path strings (hashes stay; re-verify) — `forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md:36,48,51,57`
- [ ] **APH-HAND-4** (W1) — dead pointer to renamed binding in active v1 handoff — `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md:167`
- [ ] **REF-5** (W1) — Armory README points to retired `docs/product/source_capture_toolbox/` → repoint to actual location — `forseti/product/spines/capture/core/source_capture_toolbox/README.md:726`

### T1 · DCP-receipt archival backlog  `[bloat + live gate failure]`
Destination for all: `docs/decisions/dcp_receipts_archive_v0.md` (verbatim move, keep ≤2 inline + pointer).
- [ ] **CER-2 / OVL-1a** (W1) — `review-lanes.md` fails `check_dcp_receipt_hygiene.py --strict` today; archive 2 oldest of 3 — `.agents/workflow-overlay/review-lanes.md:228-335`
- [ ] **OVL-1b** (W1) — 9 receipts (~88% of file); archive all but 2 — `.agents/workflow-overlay/artifact-folders.md:55-477`
- [ ] **DEC-4 / OVL-1c** (W1, `[!]` overlay-owned) — 3 receipts vs own 2-cap; archive oldest — `.agents/workflow-overlay/source-of-truth.md:155-345`
- [ ] **APH-CORE-1** (W1) — charter 3 receipts, would fail `--strict`; archive oldest — `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:358-426`
- [ ] **RE-CSB-1** (W1) — ~680 lines of receipts across 7 scanning/CSB files; archive to pointer — `forseti/product/spines/scanning/README.md:130-257` + 6 siblings (see audit_RE-CSB.md)
- [ ] **RE-CAP-2** (W1) — Armory ~400 lines / 8 receipts; archive 6 oldest — `forseti/product/spines/capture/core/source_capture_toolbox/README.md:799-1196`
- [ ] **NAV-6** (W1) — 2 large inline receipts on repo map; archive — `docs/workflows/forseti_repo_map_v0.md:1068-1156`

### T3 · Code bugs — S-effort subset  `[bug]`
- [x] **RE-HARN-2** (W1·landed) — wheel omitted runner-imported `youtube_capture` (a bare namespace dir) + `reports`; added `youtube_capture/__init__.py` and listed both in `packages.find` — `forseti-harness/pyproject.toml`, `forseti-harness/youtube_capture/__init__.py`
- [x] **RE-HARN-1** (W1·landed) — added read-phase `except TimeoutError`/`except OSError` clauses (mirrors `direct_http` sibling) + 2 regression tests — `forseti-harness/source_capture/adapters/anti_blocking_http.py`
- [x] **RE-HARN-3** (W1·landed) — read-phase timeout/OSError now raise `RedditApiTransportError` in `get()` AND `_ensure_token()` — `forseti-harness/source_capture/adapters/reddit_api.py`
- [x] **RE-HARN-4** (W1·landed) — bounded `timeout=` + `TimeoutExpired` handling on ALL THREE yt-dlp sites (3rd site `ig_reels_audio_packet.py:328` found on read); policy pins bumped (decision: not output-shaping) — `youtube_captions.py`, `audio_asr.py`, `ig_reels_audio_packet.py`
- [x] **RE-HARN-4b** (landed — from Slice-1 delegated review) — also bounded the in-process `_extract_info()` yt-dlp metadata call via `socket_timeout=30` (the one gap the cross-vendor Codex review found); a hard total-wall-time bound (subprocess/thread wrap) is a deferred design residual — `youtube_captions.py:47`
- [x] **RE-HARN-6** (closed — NOT a live bug) — `model_info` is built in deterministic literal order (`audio_asr.py:70-96`), so the committed content-sha is already stable; `sort_keys` would only re-derive committed ASR records for no gain. No change (add a "field order is load-bearing" comment on the next legitimate pinned touch). Owner + independent cross-vendor (Codex) review confirmed. — `asr_packet.py:127`
- [x] **RE-HARN-8** (closed — NOT a bug) — fragrantica review votes are discrete ordinal integers (`rating`/`longevity`/`sillage` from `perfume_votes` JSON, e.g. `5`/`3`/`2`); parfumo ratings are continuous floats. The int-vs-float difference is deliberate domain modeling, not an inconsistency; coercing would be output-shaping on a pinned module for no correctness gain. No change. Owner + independent cross-vendor (Codex) review confirmed. — `cleaning/fragrantica_lake.py:312`
- [x] **RE-HARN-9** (landed) — deleted the structurally-unreachable `comment_reconciliation_mismatch` hard-raise guard (false assurance); the real, reachable reconciliation check is the tested batch quality-flag in `run_reddit_batch_quality_summary.py:164-167` (`comments_parsed != observable_comment_nodes`). Behavior-neutral; reddit tests green. — `reddit_consolidation/parser.py`
- [x] **APH-IMPL-3** (W1·landed #830) — attempt rows now carry `receipt_pointer` = str(receipt_jsonl) (was: always null from absent key) — IG heartbeat `control.py`
- [x] **APH-IMPL-1** (W1·landed #830) — session artifacts now keyed `session_{bucket}_{lane_id}` (roster/receipts/summary; roster-snapshot-id carries lane); bucket-scoped lock stays deferred (F2) — IG heartbeat `control.py`
- [x] **HOOK-1** (W1·landed #835) — hook path now relativizes absolute payload paths via `to_relposix` (+ `_to_posix` dotfile fix, 3 selftest pins) — `.agents/hooks/check_search_surface_google_route.py`
- [x] **HOOK-8** (W1·landed #835) — `--hook` now emits `additionalContext` + scopes to added-lines-vs-HEAD; adjudicated cross-vendor review patch on top: tracked no-diff → no findings, whole-file fallback only for untracked — `.agents/hooks/check_full_gt_claims.py`

### T6 · Staleness debt + 1 render bug  `[dead-reference / staleness]`
- [x] **APH-HAND-3** (W1·landed) — deleted the stray fence + leaked courier block (was :248-256); fence parity restored (4, even) — `docs/prompts/handoffs/aphrodite_fragrance_subontology_build_handoff_v0.md`
- [x] **APH-HAND-2** (W1·landed) — STATUS UPDATE banner added (SUPERSEDED — overtaken by events): the commissioned artifact exists as `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml` (windcaller_kind amendment 2026-07-04 resolved the framing); the 2026-07-04 gate banner kept as history — same file
- [x] **APH-HAND-1** (W1·landed) — DELIVERED banner + repo-map row repointed to the shipped inventory (`aphrodite_silver_metric_monitoring_inventory_v0.md`); map anchor had drifted :680→:695 — `docs/workflows/aphrodite_silver_metric_monitoring_docs_handoff_v0.md` + `forseti_repo_map_v0.md`
- [x] **APH-CORE-2** (W1·landed) — charter :302 prose cite + vetting-panel open_next repointed to v1 (v1:30 states supersession); point-in-time cites in decision/propagation registers left as records — 2 files
- [x] **APH-RSCH-2** (W1·landed) — dated update-notes at the 3 sites pointing to `fragrance_reference_v0.yaml`; historical text preserved. Premise re-verified against primary source (initial gate check false-negatived on the `*ontology*` name; artifact shipped as `fragrance_reference`) — 3 files
- [x] **APH-RSCH-3** (W1·landed) — the 3 cites were already annotated nonresolving/discharged; completed them with the resolving design-spec path (`.../instagram/aphrodite_proposed_creator_stats_design_spec_v0.md`) — `aphrodite_creator_capture_field_map_v0.md:22,116,149`
- [x] **APH-RSCH-4** (W1·landed) — update-note: the extraction since ran (`aphrodite_depth_rehearsal_round2_share_of_voice_v0.md`; `fragrance_reference_v0.yaml` consumed its output); pre-run section kept as history — `round2_gentsscents_grade_v0.md`
- [x] **APH-RSCH-1** (W1·landed) — README bullet now enumerates the full `aphrodite_*` set incl. the 10-artifact depth-rehearsal series — `docs/research/README.md`
- [x] **APH-RSCH-5** (W1·landed via RSCH-1 + banner) — README row is the inbound link; the slice's new STATUS banner cross-links `fragrance_reference_v0.yaml` — `aphrodite_depth_rehearsal_ontology_slice_v0.md`
- [x] **APH-HAND-5** (W1·landed) — repointed to v1 with supersession note (v0's PR #661 provenance kept) — `aphrodite_silver_integration_direction_handoff_v0.md`
- [x] **RE-CSB-5** (W1·landed) — dated Update block added per the doc's own re-pin instruction (rename landed; live `forseti_*prompt_structure*` names cited); pinned baseline lists preserved — `commission_signal_board_current_main_reconciliation_v0.md`
- [x] **DEC-2** (W1·landed) — real anchor was :190 (audit :177 drifted): controlling-sources row for `docs/product/search/README.md` now carries the retired/nonresolving annotation matching the doc's own header — `forseti_search_product_lane_binding_v0.md`
- [x] **DEC-1** (W1·landed) — README front door now routes via `forseti_doctrine_index_v0.md` (router) + `dcp_receipts_archive_v0.md` — `docs/decisions/README.md`

### T4 · Drifted duplication (correctness subset)  `[drift-bug]`
- [ ] **CER-3** (W1) — prompt-preflight in 4 copies drifted: `edit_permission` 4-value vs 3-value enum + orphaned `isolation_decision` — `.agents/workflow-overlay/prompt-orchestration.md:32,549` vs `forseti_preflight_defaults_v0.md:59`

---

## Wave 2 — structural (design pass / sign-off in parts)

### T5 · Repo-map slimming (~40% reducible)  `[bloat/navigation]`
- [ ] **NAV-1** (W2) — Active-Hooks section 428 lines triplicated → `hook|boundary|authority|wired?` table + pointers — `docs/workflows/forseti_repo_map_v0.md:74-501`
- [ ] **NAV-3** (W2) — ~30 migration rows bury live tree — `:562-608`
- [ ] **NAV-4** (W2) — stale runner enumeration it calls non-authoritative — `:741-756`
- [ ] **NAV-5** (W2) — `source-of-truth.md` "Known Source Documents" duplicates map tables — `source-of-truth.md:349-377`
- [ ] **NAV-7** (W2) — Reddit CloakBrowser Quick Route belongs in the submap — `:503-556`
- [ ] **NAV-8** (W2) — deep read-chain (≤6 hops); surface Ordinary-Start Quick Path + 2 Quick-Index rows

### T7 · Hook latency + guard coverage gaps  `[ceremony/latency + coverage]`
- [ ] **HOOK-3** (W2) — 6 Python spawns per Write/Edit → single in-process dispatcher (verify fail-open preserved) — `.claude/settings.json:38-73`
- [ ] **HOOK-5** (W2) — `check_token_burn` reads whole transcript each Stop → tail-read — `.agents/hooks/check_token_burn.py:64-84`
- [ ] **HOOK-4** (W2) — byte-identical CI gate step runs twice → delete one — `.github/workflows/ci.yml:71-73,80-82`
- [ ] **HOOK-6** (W2) — no automated runner for `--selftest` suites (incl. security guard) → add parametrized pytest
- [ ] **HOOK-9** (W2) — diff-scoping boilerplate duplicated across ~6 gate hooks (verify per-hook isolation first)
- [ ] **HOOK-10** (W2) — git segment-parse regexes duplicated across two security-adjacent hooks
- [ ] **REF-6/7** (W2) — two submap-like files escape the link checker (name lacks "submap")
- [ ] **REF-11** (W2) — "intentionally uncreated" self-doc style not in checker exemption vocab

### T4 · Doctrine single-sourcing (remainder)  `[bloat/dedup]`
- [ ] **OVL-2/3/4/5/7/9/10** (W2) — review-doctrine + skill-adoption restatements → single-source at named owner + pointer
- [ ] **CER-1** (W2) — ~150 lines review doctrine dual-maintained `prompt-orchestration.md:368-517` ↔ `review-lanes.md:38-226`
- [ ] **RE-CSB-2** (W2) — CSB Prompt vs Rules ~90 lines byte-identical → canonicalize in Rules
- [ ] **RE-CSB-3** (W2) — engagement/resonance restated in 6+ files; cite canonical `engagement_logic_registry_v0.md`
- [ ] **DUP-2** (W2) — inline template scaffolds on warm-read artifacts → pointer + delta
- [ ] **DUP-3** (W2) — `pack:overlay-core` named alias to replace overlay-path lists in ~1,000 files
- [ ] **DUP-4** (W2) — shared `moved_paths_index` preamble
- [ ] **RE-CAP-3/4** (W2) — family routing table dup + per-family README template
- [ ] **RE-HARN-5** (W2) — forbidden-output/secret-value guard copy-pasted across 5 families (already drifted)
- [ ] **RE-HARN-10** (W2) — `_enum_values` byte-identical in 6 model files + 3 silver-metric producers
- [ ] **APH-IMPL-4** (W2) — `_recompute_ig` vs `_recompute_tiktok` near-identical → extract trio helper
- [!] **OVL-6** (W2, owner-gated) — identical multi-file receipt verbatim in 3 files; fix changes the DCP contract → decide with owner

### T8 · Structural navigation gaps  `[navigation/format-bug]`
- [ ] **RE-CAP-1** (W2) — Capture spine has no README (CSB/Scanning do) → add thin front door
- [ ] **RE-CSB-6** (W2) — Scanning lacks the moved-path index CSB built for the same rename
- [ ] **CER-4** (W2) — "Supported Prompt Families" table missing `architecture/`, `advisory/`, `wrappers/` — `prompt-orchestration.md:193-206`
- [ ] **CER-5** (W2) — lane template invisible to `template-registry.md` (or state generic-only scope)
- [ ] **RE-CAP-6** (W2) — Retail/PDP review-capture spec orphaned outside `core/` (add pointers, don't move)
- [ ] **REF-1..4** (W2) — `icp_wedge` `open_next` entries lack `# ` delimiter → parsed as one filename — `forseti/product/spines/product_lead/icp_wedge/` (3 files)
- [ ] **CER-6** (W2) — `orca-product-lead` alias clean but no dated sunset trigger

---

## Deferred (blocked on migration campaign)

- [-] **DEC-5** — 18 filename-migration decision records (~2,004 lines, 13% of `docs/decisions/`) → consolidate/relocate under `docs/migration/` **after** the `orca->forseti` campaign completes.
- [-] **DUP-5** — 8 stems with co-living superseded versions → archive per-stem (verify each is truly superseded first).
- [-] **DUP-1** — retrieval-header invariant default (flips fail-safe direction; owner decision).
- [-] **APH-RSCH-7 / RE-CAP-7/8** — self-flagged/dormant splits; surface only.
