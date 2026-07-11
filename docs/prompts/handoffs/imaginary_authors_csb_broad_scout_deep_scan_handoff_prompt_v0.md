# Imaginary Authors CSB Broad-Scout + Deep-Scan Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Filed cross-recipient scanning-lane prompt that tests the proposed default
  split pattern: one bounded broad-scout subagent for venue discovery while the
  main lane owns CSB interpretation, source loading, scan-core gate discipline,
  deepening, and final candidate decision.
use_when:
  - Commissioning another scanning lane to work from the Imaginary Authors CSB board.
  - Testing whether broad scout plus main deep adjudication reduces missed venue rungs without becoming a crawler.
  - Producing a fresh scan artifact for CA adjudication against Output A and Output B.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_buyer_language_rerun_v0.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md
stale_if:
  - Any named source artifact changes after this prompt is launched.
  - The owner changes the task from scanning/venue discovery to Capture, ECR, Cleaning, Judgment, outreach, or candidate execution.
  - The receiving lane cannot create a fresh artifact or cannot source-load the CSB/scanning sources.
```

## Prompt Authoring Preflight

```yaml
orchestrator_mode: filed_handoff_prompt_plus_paste_ready_copy
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
forseti_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes - .agents/workflow-overlay/README.md read in current task context
  source_pack: custom_scanning_csb_broad_scout_deep_scan_handoff
  edit_permission: docs-write for this prompt; downstream lane writes a fresh docs/research scan artifact only
  target_scope: launch a fresh scanning lane using CSB-first broad-scout plus main deep adjudication structure
  dirty_state_checked: yes - scanning worktree checked; unrelated untracked prior review output excluded
  blocked_if_missing: CSB board, returned CSB scan, scanning README/MGT, scan-core, fresh-output path
workspace_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-fragrance-commission
expected_branch: receiving lane should spin a clean branch/worktree from current main or an explicitly supplied base
dirty_state_allowance: receiving lane may create its own fresh scan artifact and map pointer; must not edit prior scan outputs
controlling_source_state: not claimed; receiving lane must fresh-read sources in its own workspace
output_mode: paste-ready-chat
downstream_output_artifact: docs/research/orca_discovery_candidate_scan_imaginary_authors_broad_scout_deep_scan_v0.md
template_kind: handoff
template_source: direct Forseti handoff prompt under prompt-orchestration contract
workflow_sequence_policy: overlay_owned
workflow_sequence_source: active_overlay plus current user instruction
workflow_sequence_status: bound
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
doctrine_change_decision: >
  This prompt tests an operating pattern inside one fresh scan commission. It
  does not change scanning doctrine by itself, does not make subagents mandatory,
  and does not alter review, validation, product, or lifecycle authority.
non_claims:
  - not scan execution
  - not validation
  - not readiness
  - not candidate admission
  - not Capture authorization
  - not a doctrine change making subagents default
```

## Fitness Reference

Goal: test whether a CSB-first scan is better when the main lane owns gate
discipline and deepening while one bounded broad-scout subagent searches for
cheap high-value venues the main lane might miss.

Done looks like: the receiving lane writes a fresh scan artifact that can be
adjudicated against the owner commission, Output A, and Output B, with clear
evidence of what the broad scout added, what the main lane deepened, and what
candidate/capture decision follows under scan-core.

This goal and signal are review axes to attack, not a pass-if-matches bar.

## Paste-Ready Prompt

````markdown
# Imaginary Authors CSB Broad-Scout + Deep-Scan Scanning Commission

You are opening a **fresh Forseti scanning lane** for Imaginary Authors.

The purpose is to test a proposed scanning structure:

- Main lane owns source loading, CSB interpretation, run caps, scan-core gate
  discipline, deepening, final candidate decision, and overclaim control.
- One bounded broad-scout subagent may look for cheap high-value venue rungs the
  main lane could miss.

This is not a crawler. It is not a Capture run. It is not ECR, Cleaning,
Judgment, outreach, buyer contact, source-class ratification, route binding,
monitoring, or client output.

## Access Gate

If you have repo/filesystem access, open the required files and re-read their
load-bearing sections before making strict or actionable claims.

If you do not have repo/filesystem access, stop and request a source capsule or
pasted copies of the required sources. Do not scan from memory, summaries, or
chat claims.

## Required Method And Source Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read `.agents/workflow-overlay/source-loading.md`,
   `.agents/workflow-overlay/artifact-roles.md`, and
   `.agents/workflow-overlay/validation-gates.md` only as needed to bind the
   prompt/report/write contract.
3. SOURCE-LOAD the CSB/scanning pack below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, run the scan.

Do not treat prior scan outputs as authority. They are comparison artifacts and
anti-repeat context only.

## Required Sources

Commission and CSB/scanning sources:

- `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`
- `docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md`
- `forseti/product/spines/scanning/README.md`
- `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md`
- `forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md` targeted to Walker Equipment Kit / public-source and access-note boundaries

Comparison artifacts, read after the required sources:

- Output A: `docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md`
- Output B: `docs/research/orca_discovery_candidate_scan_imaginary_authors_buyer_language_rerun_v0.md`

Exclude by default:

- prior adversarial review reports;
- PR descriptions, chat summaries, or agent closeouts;
- live social expansion, login-gated reads, anti-bot solving, Capture runners,
  ECR, Cleaning, Judgment, outreach, buyer contact, and broad crawls.

## Objective

Create a fresh scan artifact that answers:

> Starting from the Imaginary Authors CSB, does a broad-scout plus main deep-scan
> structure find valuable venues, hidden venues, buyer-language surfaces,
> access notes, negatives, capture requests, or low-commitment candidate entries
> more reliably than the prior single-lane outputs?

Fresh artifact path:

```text
docs/research/orca_discovery_candidate_scan_imaginary_authors_broad_scout_deep_scan_v0.md
```

Do not edit Output A, Output B, or the returned core-satellite CSB scan.

## Operating Structure

### Main lane

The main lane owns:

- source readiness and source ledger;
- CSB row interpretation;
- run caps and stop conditions;
- what the broad scout may inspect;
- deepening of the highest-value surfaces;
- candidate observation and candidate-entry decisions;
- capture_request boundaries;
- final closeout state;
- validation and stale-language checks.

### Broad-scout subagent

Use at most one broad-scout subagent. If subagents are unavailable, run this as
a separate section in the main lane and mark `broad_scout_mode: inline`.

The broad scout is read-only and returns only a route ledger. It must not mint
candidates, decide gate clearance, set Capture routes, run Capture, or claim
proof.

Broad-scout cap:

```yaml
broad_scout_cap:
  max_exact_queries: 12
  max_venue_families: 6
  max_first_pass_pages: 18
  max_candidate_surfaces_returned: 8
  stop_when: value drops to access-only/noisy/generic for two consecutive venue families after at least three high-priority families are checked
```

Broad-scout priority order:

1. specialist fragrance community/review venues: Parfumo, Basenotes,
   Fragrantica, Reddit only as public/search-result or access note unless
   authorized route exists;
2. retailer or brand review surfaces that expose dated text, not counts alone;
3. original partner/channel routes: Salt & Straw, Anthropologie, official
   partner/brand pages;
4. exact-query hidden venue discovery for each target SKU;
5. archive/snippet checks only when they answer a specific CSB gap;
6. stop before generic web crawling or broad social expansion.

Broad-scout return shape:

```yaml
broad_scout_return:
  source_context_status: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  moves_used:
  exact_queries_used:
  venues_tested:
    - venue:
      target_sku:
      url_or_query:
      result_class: venue_value | candidate_surface | access_note | negative | noisy | duplicate | excluded
      short_reason:
      suggested_main_deepening: yes | no
  hidden_venue_pointers:
    - venue:
      url_or_query:
      why_it_matters:
      not_a_claim_of:
        - proof
        - candidate admission
        - Capture route binding
  access_notes:
  negatives:
  stop_reason:
```

## Main Deepening Rules

Target SKUs:

- `A Little Secret`
- `Dipped in Chocolate`
- `First Peach of the Season`

Main lane must deepen only surfaces that can change one of these:

- venue value / hidden venue value;
- candidate-support observation;
- contradiction;
- negative or access note;
- preservation-only capture_request;
- candidate decision under scan-core.

Do not deepen ordinary owned availability, retail assortment, editorial
visibility, partner/channel motion, or aggregate counts unless they expose dated
buyer language, costly behavior, decision-event evidence, contradiction, or a
specific preservation need.

Candidate promotion is allowed only under existing scan-core rules. One
qualifying independent demand-origin may support a candidate entry only at
`hold_low_commitment`; material action requires at least two independent
converging origins. Retail and org-motion can corroborate but do not count as
demand-origin.

Capture requests are preservation-only and Capture-owned. Scanning may request
Capture to preserve volatile or gate-relevant pages, but must not bind a route,
run Capture, create ECR/Cleaning/Judgment work, or treat Capture as proof.

## Output Contract

Write the fresh artifact at:

```text
docs/research/orca_discovery_candidate_scan_imaginary_authors_broad_scout_deep_scan_v0.md
```

The artifact must include:

- retrieval header;
- `forseti_start_preflight`;
- source loading ledger;
- CSB rows consumed;
- run caps;
- broad-scout dispatch and return ledger, or `broad_scout_mode: inline`;
- main deepening ledger;
- exact queries used;
- venues tested;
- hidden venue pointers;
- observations;
- negatives;
- access notes;
- capture_requests;
- candidate decision;
- combined comparison against Output A and Output B;
- adjudication packet for CA couriering.

Closeout must choose exactly one:

- `candidate_ready_for_next_lane`
- `capture_preservation_only`
- `no_candidate_after_discovery`
- `blocked_source_context_incomplete`

Candidate decision must state:

```yaml
candidate_decision:
  closeout_state:
  candidate_entries:
  independent_origins_seen:
  costly_behavior_floor:
  commitment_ceiling:
  material_action_eligible:
  capture_preservation_option:
  supersedes_prior_output_on:
  does_not_supersede_prior_output_on:
  not_a_claim_of:
    - buyer proof
    - demand proof
    - validation
    - readiness
    - material-action eligibility unless explicitly cleared
    - Capture route binding
```

## Adjudication Packet To Return In Chat

After writing the artifact and running checks, return this compact packet:

```yaml
scanning_lane_return:
  status: completed | blocked | failed
  artifact_path:
  branch:
  commit:
  source_context_status:
  broad_scout_mode: subagent | inline | unavailable
  broad_scout_value_added:
  closeout_state:
  candidate_entries:
  capture_requests:
  supersedes_output_a_on:
  supersedes_output_b_on:
  preserves_from_output_a:
  preserves_from_output_b:
  validation:
    git_diff_check:
    retrieval_header:
    repo_map_freshness:
    placement:
    map_links:
    stale_language_search:
  blockers_or_residual_risks:
  next_authorized_action:
```

Also include a short human summary:

- what the broad scout found that the main lane might have missed;
- what the main lane accepted or rejected after deepening;
- whether the structure appears useful for future scanning lanes.

## Validation

If a new artifact is written, run:

- `git diff --check`
- `python .agents/hooks/check_retrieval_header.py --changed`
- `python .agents/hooks/check_repo_map_freshness.py --changed`
- `python .agents/hooks/check_placement.py --check`
- `python .agents/hooks/check_map_links.py --strict`

Run targeted stale-language searches for:

- crawler/monitor/registry/atlas overclaims;
- Capture route binding or Capture-as-proof language;
- demand-proof / buyer-proof / validation / readiness overclaims;
- precursor terms used as gate proof;
- candidate promotion without `hold_low_commitment` when only one origin family clears.

If you commit/push/PR, verify durable state with fresh reads before claiming it.

## Review-Use Boundary

This scan is CA input only. It is not buyer proof, demand proof, validation,
readiness, candidate admission, material-action approval, Capture authorization,
or executor-ready work unless a separate Forseti decision or execution lane accepts
it.
````
