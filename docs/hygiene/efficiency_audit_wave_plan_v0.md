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
- [ ] **RE-HARN-2** (W1) — wheel omits runner-imported `youtube_capture` + `reports` → `ModuleNotFoundError` on install — `forseti-harness/pyproject.toml:38-51`
- [ ] **RE-HARN-1** (W1) — read-phase `TimeoutError`/`ConnectionResetError` aborts capture; copy sibling clauses — `forseti-harness/source_capture/adapters/anti_blocking_http.py:119-142`
- [ ] **RE-HARN-3** (W1) — reddit OAuth breaks transport Protocol on read timeout → runner crash — `forseti-harness/source_capture/adapters/reddit_api.py:461-477,498-524`
- [ ] **RE-HARN-4** (W1) — `yt-dlp`/ASR `subprocess.run` has no `timeout=` → can hang forever — `forseti-harness/source_capture/transcript/youtube_captions.py:157-161`, `audio_asr.py:35-39`
- [ ] **RE-HARN-6** (W1) — sha committed over non-`sort_keys` JSON → idempotency drift — `forseti-harness/source_capture/transcript/asr_packet.py:127`, `ig_reels_audio_packet.py:203`
- [ ] **RE-HARN-8** (W1) — fragrantica metric not float-coerced vs parfumo sibling — `forseti-harness/cleaning/fragrantica_lake.py:321`
- [ ] **RE-HARN-9** (W1) — structurally unreachable comment-reconciliation guard (false assurance) — `forseti-harness/source_capture/reddit_consolidation/parser.py:71-78`
- [ ] **APH-IMPL-3** (W1) — attempt rows always `receipt_pointer=null` (reads absent key) — IG heartbeat `control.py:497`
- [ ] **APH-IMPL-1** (W1) — session artifacts keyed by `bucket` not `(bucket,lane)` → roster/summary clobber + inflated telemetry — IG heartbeat `control.py:264,292-294,332,536`
- [ ] **HOOK-1** (W1) — Google-route hook no-ops on every real edit (absolute path never normalized) — `.agents/hooks/check_search_surface_google_route.py:106-117,206-209,298-303`
- [ ] **HOOK-8** (W1) — `check_full_gt_claims --hook` emits stderr (never reaches context) + scans whole file — `.agents/hooks/check_full_gt_claims.py:207-222`

### T6 · Staleness debt + 1 render bug  `[dead-reference / staleness]`
- [ ] **APH-HAND-3** (W1) — unpaired ``` fence opens code block to EOF wrapping leaked courier-prompt; delete lines — `docs/prompts/handoffs/aphrodite_fragrance_subontology_build_handoff_v0.md:247-255`
- [ ] **APH-HAND-2** (W1) — handoff says "NOT AUTHORIZED" after build shipped; apply SUPERSEDED banner — same file `:25-30,66,149-155`
- [ ] **APH-HAND-1** (W1) — monitoring handoff open after deliverable shipped; mark delivered + repoint repo-map row — `docs/workflows/aphrodite_silver_metric_monitoring_docs_handoff_v0.md` + `forseti_repo_map_v0.md:680`
- [ ] **APH-CORE-2** (W1) — charter + vetting panel point to superseded v0 handoff → repoint to v1 — `aphrodite_carveout_charter_v0.md:302`, `aphrodite_vetting_sprint_panel_design_v0.md:23`
- [ ] **APH-RSCH-2** (W1) — 3 files call fragrance ontology an open "build task" though it exists — `docs/research/aphrodite_depth_rehearsal_grade_v0.md:80-84`, `round2_gentsscents_grade_v0.md:154-155`, `ontology_slice_v0.md:20-21`
- [ ] **APH-RSCH-3** (W1) — dead handoff path cited 3× → repoint — `docs/research/aphrodite_creator_capture_field_map_v0.md:22,116,149`
- [ ] **APH-RSCH-4** (W1) — "not yet run" claim stale (sibling ran it) — `docs/research/aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md:164-176`
- [ ] **APH-RSCH-1** (W1) — `docs/research/README.md` indexes 3 of 12 lane files — `docs/research/README.md:26`
- [ ] **APH-RSCH-5** (W1) — ontology-slice orphaned from forward-nav chain (add link-back) — `docs/research/aphrodite_depth_rehearsal_ontology_slice_v0.md`
- [ ] **APH-HAND-5** (W1) — cites superseded handoff's OPEN gates as binding → repoint to v1 — `docs/prompts/handoffs/aphrodite_silver_integration_direction_handoff_v0.md:126-128`
- [ ] **RE-CSB-5** (W1) — stale CSB reconciliation note (its `stale_if` fired) — `forseti/product/spines/commission_signal_board/migrations/commission_signal_board_current_main_reconciliation_v0.md:46-50,58-71`
- [ ] **DEC-2** (W1) — intra-doc contradiction: retired doc still listed live in checklist — `docs/decisions/forseti_search_product_lane_binding_v0.md:177`
- [ ] **DEC-1** (W1) — stale `decisions/README.md` front door (no pointer to doctrine index) — `docs/decisions/README.md`

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
