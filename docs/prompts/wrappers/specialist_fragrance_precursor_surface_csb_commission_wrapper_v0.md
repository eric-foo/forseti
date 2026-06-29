# Specialist Fragrance Precursor Surface CSB Commission Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: CSB-first commission for specialist-fragrance precursor-surface qualification.
use_when:
  - Dispatching the Commission Signal Board run that should precede specialist-fragrance Scanning, Capture, or Data Lake work.
  - Reconstructing why this lane starts from CSB instead of a retailer PDP implementation or routine lake check.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md
  - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - orca/product/spines/scanning/README.md
stale_if:
  - The Commission Signal Board prompt output contract changes.
  - The Scanning README changes the CSB-first handoff or broad-scout rule.
  - A later decision authorizes direct Capture/Data Lake expansion for this exact surface set.
```

## Orca Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
authorization_basis: Owner accepted CSB-first route for retail/PDP reviews plus specialist fragrance precursor surfaces in the current thread on 2026-06-29.
objective_intended_decision: >
  Produce a Commission Signal Board output that structures which specialist-fragrance
  surfaces should be sent to Scanning for precursor-demand qualification before
  Capture or Data Lake expansion.
output_mode: file-write
template_kind: thin-wrapper
referenced_full_prompt: orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md
referenced_full_prompt_revision: main@190e1ef2
prompt_artifact_path: docs/prompts/wrappers/specialist_fragrance_precursor_surface_csb_commission_wrapper_v0.md
downstream_output_artifact_path: docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md
edit_permission: docs-write
target_files_or_dirs:
  - docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md
  - docs/prompts/wrappers/specialist_fragrance_precursor_surface_csb_commission_wrapper_v0.md
workspace_path: C:/Users/vmon7/Desktop/projects/orca/worktrees/specialist-fragrance-csb
branch: codex/specialist-fragrance-csb
base_revision: main@190e1ef2
dirty_state_allowance: >
  The receiving lane may write only the downstream CSB board artifact and any
  explicit validation notes required to report validator results. Do not edit
  CSB, Scanning, Capture, Data Lake, or overlay authority files.
controlling_source_state: >
  This wrapper was authored from the isolated worktree above. The full CSB
  prompt, CSB playbook, Scanning README, and MGT operating model are controlling
  sources for the receiving lane.
doctrine_change_decision: No doctrine change. This is a case-local CSB commission using existing CSB and Scanning contracts.
isolation_decision: Worktree off main for this repo-changing docs lane.
retrieval_authorization: >
  No public web retrieval is authorized inside the CSB board run. The board may
  mark rows as to_retrieve and prepare handoff rows for later Scanning.
validation_gates:
  wrapper_authoring:
    - git diff --check -- docs/prompts/wrappers/specialist_fragrance_precursor_surface_csb_commission_wrapper_v0.md
    - python .agents/hooks/check_retrieval_header.py --changed
    - python .agents/hooks/check_repo_map_freshness.py --changed
    - python .agents/hooks/check_placement.py --check
  downstream_csb_board:
    - python -B .agents/hooks/check_commission_signal_board_output.py docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md
reviews: Findings-first if reviewed; no review is required by this wrapper unless validator failure or owner request creates one.
thread_operating_target_continuity: >
  Continue the current target: establish CSB-first specialist-fragrance
  precursor-surface qualification before any Capture, Data Lake, or retailer-PDP
  expansion. Drift cue: the work becomes a store list, crawler map, Data Lake
  schedule, or demand verdict before Scanning has source-backed observations.
```

## Fitness Reference

Goal handoff: Orca identifies early fragrance demand before mainstream retail or press while preserving source-backed decision discipline. The current anchor is to establish a CSB-first specialist-fragrance precursor-surface qualification lane before Capture or Data Lake expansion.

This wrapper is fit when it lets a downstream actor produce one validator-checkable CSB board that:

- Names the source families and specialist-fragrance surfaces Scanning should test.
- Separates community/tracker, sampling/decant, specialist retail, blog/review, search/AEO, and major retail/PDP roles.
- Preserves known unknowns and counterevidence paths.
- Does not claim demand proof, capture readiness, source-map completeness, or routine monitoring authority.

## Required Reads For The Receiving Lane

Read these before producing the CSB board:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`
4. `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md`
5. `orca/product/spines/scanning/README.md`
6. `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
7. `orca/product/satellites/beauty/beauty_venue_card_set_v0.md`
8. `orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md`

## Dispatch Instructions

Use the full CSB prompt's Prompt Body as the controlling prompt. Supply the commission inputs below. Do not restate or fork the CSB output contract.

When executing this wrapper:

1. Produce the full Section 1-10 CSB board required by the CSB prompt.
2. Write the exact board output to `docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md`.
3. Run `python -B .agents/hooks/check_commission_signal_board_output.py docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md`.
4. Report the validator output. A passing validator means only that the board is mechanically handoff-eligible; it is not evidence truth, demand proof, Capture authorization, Data Lake authorization, or buyer proof.

## Commission Inputs

```yaml
commission_id: specialist_fragrance_precursor_surface_csb_v0
mode: forward
candidate_or_subject: Specialist fragrance precursor surfaces for US indie and DTC fragrance demand.
decision_context: >
  Identify and structure the source-family rows needed to decide which
  specialist-fragrance surfaces should be sent to Scanning for precursor-demand
  qualification before Capture or Data Lake expansion.
market_or_geography: US-first fragrance within beauty and personal care.
time_window: Current forward source-qualification pass.
evidence_cutoff_at: not_applicable_forward_mode
known_seed_entities:
  community_tracker_surfaces:
    - Basenotes
    - Fragrantica
    - Parfumo
  specialist_retail_surfaces:
    - LuckyScent / Scent Bar
    - Twisted Lily
    - Ministry of Scent
    - ZGO Perfumery
    - Aedes Perfumery
    - Arielle Shoshana
  sampling_decant_surfaces:
    - Scent Split
    - Surrender to Chance
    - The Perfumed Court
    - DecantX
  specialist_blog_review_surfaces:
    - CaFleureBon
    - The Scented Hound
    - The Plum Girl
  major_retail_context:
    - Ulta
    - Sephora
    - Amazon
known_adjacent_entities:
  - Reddit fragrance communities
  - TikTok fragrance creator discussion
  - YouTube fragrance reviewers
  - Google search and AEO surfaces
provided_evidence_or_context:
  - >
    The Beauty Venue Card Set identifies Basenotes as a fragrance tracker and
    subtle-class home where detection may precede press by weeks to months, with
    direct HTTP 403 access and search-snippet fallback noted.
  - >
    The Beauty Venue Card Set identifies Fragrantica as a tracker/aggregator and
    second aggregation layer, with direct HTTP 403 access and snippet-only access
    noted.
  - >
    The Beauty Venue Card Set identifies specialist fragrance blogs as outcome
    gauges with direct fetch generally available.
  - >
    The current thread route is CSB first, then Scanning, then Capture only after
    an explicit capture_request, with Data Lake routine checks later after raw
    packets exist.
  - >
    Major retailer PDP/review capture already has projection and rendered-capture
    contracts for Amazon, Sephora, and Ulta; this commission is not a request to
    expand that implementation.
known_source_constraints:
  - Public-only source posture; no logins, private groups, account-only material, auth bypass, or CAPTCHA/Cloudflare workarounds.
  - No scraping, crawling, monitoring, graph construction, capture, scoring, demand classification, forecasting, judgment, or buyer proof in the CSB lane.
  - Treat Basenotes and Fragrantica direct-access walls as access notes and route constraints, not as reasons to bypass access controls.
  - Treat specialist retail and sampling/decant stores as candidate surfaces until Scanning source-backs which dated signals they expose.
  - Treat major retailer PDP/review data as downstream corroboration or later durability context, not the first precursor-discovery route.
known_unknowns:
  - Which specialist surfaces expose dated review text, review counts, stockout/restock behavior, sample availability, full-bottle availability, discovery/list position, or waitlist-like cues?
  - Which surfaces are earliest for indie/DTC fragrance uptake versus only reflecting already-mainstream popularity?
  - Which source families are public, current, and low-policy-risk enough for Scanning?
  - Which rows should become Scanning broad-scout targets, exact-query targets, or negative/counterevidence paths?
  - Which surfaces, if any, could later justify a Capture request after Scanning returns source-backed observations?
dispatcher_non_goals:
  - Do not perform public web retrieval in this CSB board run.
  - Do not choose the final top specialist stores.
  - Do not create a source registry, crawler plan, capture implementation, Data Lake routine, or monitoring schedule.
  - Do not label any fragrance, brand, store, or source family as proven demand.
  - Do not alter CSB, Scanning, Capture, Data Lake, overlay, hook, CI, or runtime files.
```

## Downstream Handoff Rule

The CSB board may hand off to Scanning only after the full board exists at the bound path and the CSB validator has been run. The Scanning lane must then apply the CSB-first broad-scout rule, return dated observations or negatives, and emit `capture_request` only when a surface has enough source-backed value to justify packet-level Capture.

Capture work remains blocked until Scanning emits a bounded `capture_request`. Data Lake routine checks remain blocked until Capture has committed raw packets and the lake has something durable to serve or refresh.

## Non-Claims

This wrapper does not prove precursor value, rank specialist stores, authorize retrieval, authorize scraping, authorize Capture, authorize Data Lake work, validate demand, create buyer proof, or change Orca doctrine.
