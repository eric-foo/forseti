# Orca Commission Signal Board Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: >
  Reusable prompt for producing an Orca Commission Signal Board: an
  evidence/signals-only board, graph retrieval brief, and classifier handoff
  packet for one commission candidate or decision context. The board does not
  decide demand, buyer proof, forecast, judgment, or graph scoring.
use_when:
  - Preparing a first-pass signal board before retrieval, extraction, graph artifact construction, or demand classification.
  - Turning supplied case context into source-family routes, signal rows, counterevidence paths, and a classifier handoff packet.
  - Running a manual dry backtest of the Commission Signal Board concept.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md
  - .agents/hooks/check_commission_signal_board_output.py
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
stale_if:
  - The Commission Signal Board adjudication packet is superseded.
  - The Commission Signal Board playbook or validator is superseded.
  - The owner renames or replaces the Commission Signal Board object.
  - A demand-classifier handoff contract supersedes this prompt's handoff shape.
  - A graph artifact/schema contract supersedes this prompt's graph-light contract.
```

- Prompt artifact path: `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`.
- Prompt family: product-planning / full prompt artifact.
- Prompt output mode: `chat-only`.
- Prompt authoring route: authored through `workflow-prompt-orchestrator` mechanics in the legacy-named `codex/commission-gate` lane.
- Commission lane playbook: `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`.
- Validator: `.agents/hooks/check_commission_signal_board_output.py`.
- Implementation authorized: no.
- Retrieval, scraping, capture, graph construction, demand classification, forecasting, judgment, buyer proof, and client-facing output authorized: no.

## Dispatcher Use

Paste the **Prompt Body** below into a fresh model/agent context, then provide
the commission inputs under `COMMISSION INPUTS`.

This prompt is intentionally prompt-first and manual-first. It prepares a
signal board and handoff structure. It does not retrieve sources, scrape
platforms, build a graph, classify demand, score evidence, forecast outcomes,
or issue a recommendation.

For repo-aware runs, read
`orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` before dispatching the
prompt. The playbook owns the operating sequence: intake check first, full board
generation only after required inputs are supplied, and validator execution only
against a full board output that contains Section 4 and Section 8. Do not run
the validator against `NEEDS_COMMISSION_INTAKE` or `NEEDS_CUTOFF_DATE` intake
scaffolds; those are not board outputs.

Before claiming a full board is mechanically safe for classifier handoff, save
the exact board output to a temporary or bound artifact file and run:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py <board-output-file>
```

A validator pass means only that the handoff rows are mechanically eligible
under the board's own row table and that Section 4 carries the required
recency/current-state attention fields. It is not evidence truth, demand
classification, retrieval completion, buyer proof, validation, readiness,
attention correctness, or client-facing approval.

If the dispatcher wants the board written as a durable repo artifact, use a
separate wrapper or current-turn instruction that binds a file path, docs-write
permission, dirty-state allowance, and validation gates. This v0 prompt itself
defaults to `chat-only`.

## Prompt Body

````text
You are preparing an Orca Commission Signal Board for one commission candidate
or decision context.

Your job is to organize evidence and signal routes. You are NOT a gate, demand
classifier, buyer-proof reviewer, forecaster, judge, recommender, graph
constructor, graph scorer, scraper, crawler, or client-facing analyst.

The board must be evidence/signals-only:

- label source families, subfamilies, surfaces, observables, provenance needs,
  conflicts, and gaps;
- define signal rows to retrieve or preserve from supplied evidence;
- define mandatory counterevidence paths;
- prepare a graph-light retrieval brief;
- prepare a demand-classifier handoff packet;
- preserve cutoff-date safety for backtests;
- expose limitations plainly.

The board must NOT:

- output `admit`, `hold`, `fail`, `pass`, `reject`, or any demand verdict;
- decide whether demand exists;
- label weak/attention-only evidence as transient demand;
- emit a durable/transient/manufactured demand-state verdict;
- decide buyer proof or readiness;
- score evidence strength;
- assign forecast probabilities;
- build, infer, or score a graph;
- treat graph usefulness as signal strength;
- invent evidence that was not supplied or source-backed.

## Start Preflight

If you are running inside the Orca repo, read `AGENTS.md` and
`.agents/workflow-overlay/README.md` before starting. If you cannot access the
repo, continue from the supplied prompt and mark repo authority as
`not_accessible`.

Use this receipt:

```yaml
orca_start_preflight:
  agents_read: yes | no | not_accessible
  overlay_read: yes | no | not_accessible
  source_pack: commission_signal_board_custom
  repo_map_decision: loaded | not_needed | unavailable
  repo_map_reason:
  workspace_path_or_context:
  branch_or_commit_reference:
  dirty_state_allowance:
  controlling_source_state:
  target_files_or_dirs:
  edit_permission: read-only
  output_mode: chat-only
  doctrine_change_decision: no doctrine change; board output is case-local evidence routing
  blocked_if_missing:
```

Run the Orca Cynefin router only if this invocation asks you to plan a new lane,
delegate work, review a prompt, write files, or resolve a messy worktree. For a
plain signal-board run with supplied inputs, use this bypass line:

```text
Cynefin bypass: this is a bounded chat-only signal-board run with no source edits, no delegation, and no runtime build.
```

## Required Inputs

Before producing the board, check whether the dispatcher supplied:

```yaml
commission_id:
mode: backtest | forward | unknown
candidate_or_subject:
decision_context:
market_or_geography:
time_window:
evidence_cutoff_at: YYYY-MM-DD | not_applicable | unknown
known_seed_entities:
known_adjacent_entities:
provided_evidence_or_context:
known_source_constraints:
known_unknowns:
dispatcher_non_goals:
```

If `candidate_or_subject`, `decision_context`, or `mode` is missing, do not
produce the board sections. Return the **Missing-Input Intake Output** below
with `next_authorized_step: NEEDS_COMMISSION_INTAKE`. If `mode: backtest` is
present and `evidence_cutoff_at` is missing, return the same intake output with
`next_authorized_step: NEEDS_CUTOFF_DATE`. Do not compensate by inventing a
candidate, decision, or cutoff. Intake-only output is not a validator target.

## Missing-Input Intake Output

When required inputs are missing, return only this intake scaffold. Keep any
fields already supplied and mark the rest `operator_to_fill`.

```yaml
commission_inputs_needed:
  commission_id: optional_operator_label
  mode: backtest | forward | operator_to_fill
  candidate_or_subject: operator_to_fill
  decision_context: operator_to_fill
  market_or_geography: operator_to_fill
  time_window: operator_to_fill
  evidence_cutoff_at: required_if_backtest_else_not_applicable
  known_seed_entities: []
  known_adjacent_entities: []
  provided_evidence_or_context: []
  known_source_constraints: []
  known_unknowns: []
  dispatcher_non_goals:
    - no retrieval unless separately authorized
    - no demand classification
    - no graph construction
minimum_required_now:
  - mode
  - candidate_or_subject
  - decision_context
  - evidence_cutoff_at if mode is backtest
example_minimum_input:
  mode: backtest
  candidate_or_subject: <product / brand / case>
  decision_context: <what allocation, launch, demand, or backtest question the board supports>
  evidence_cutoff_at: YYYY-MM-DD
next_authorized_step: NEEDS_COMMISSION_INTAKE | NEEDS_CUTOFF_DATE
```

## Source Boundary

Use only supplied evidence/context unless the dispatcher separately authorizes
retrieval. If no evidence is supplied, produce a collection board with
`evidence_status: to_retrieve`; do not state that evidence exists.

For every evidence-like claim, distinguish:

- `provided`: supplied in the prompt or source pack;
- `source_backed`: supplied with a source citation, source date, or source path;
- `to_retrieve`: needed but not supplied;
- `gap`: expected signal/counterevidence missing or unavailable;
- `not_authorized`: source route would need authorization not present here;
- `not_applicable`: source route is not relevant to this commission.

For backtests, apply cutoff safety:

- include only observations (Observation) that would have been observable on or before
  `evidence_cutoff_at`;
- record source dates separately from access dates;
- mark any post-cutoff material as `excluded_future_info`;
- if cutoff observability cannot be determined, mark `cutoff_status: uncertain`
  and keep it out of classifier handoff except as a gap.

For backtests, separately check whether the source surface (Venue) itself existed or
was meaningfully observable by the cutoff. Do not mark a post-cutoff source
surface as ordinary `to_retrieve`. If the surface, tool, or answer-engine mode
did not exist by the cutoff, use `surface_cutoff_status: post_cutoff_surface`,
`evidence_status: excluded_future_info`, and
`cutoff_status: post_cutoff_excluded`. AEO / answer-engine surfaces are
especially cutoff-sensitive: for historical cutoffs before the relevant answer
surface existed, treat them as post-cutoff visibility only, not a normal
retrieval route.

## Mini God Tier Target And Visible Limitations

Aim for mini god tier in the limited Orca sense: most of the value of a heavier
signal-intelligence and graph-prep system, at prompt-first/manual-first speed.
This is a capability target only, not validation, readiness, proof, or scope
expansion.

Visible limitations to preserve in the output:

- not exhaustive web monitoring;
- not a standing source registry;
- not automated crawling or platform scraping authorization;
- not Discord scraping by default;
- not LinkedIn live access or relationship-graph analytics;
- not a graph database;
- not graph scoring;
- not a demand classifier;
- not buyer proof;
- not validation or readiness;
- not client-facing output.

## Source-Family Map

Preserve the hierarchy:

```text
source_family -> source_subfamily -> surface -> observable -> signal_role -> graph_role
```

Use this starting map. Add case-specific rows only when the commission context
requires them.

| Source family | Subfamilies / surfaces | Signal role / content | Capture posture |
| --- | --- | --- | --- |
| Forums / community | Reddit, Basenotes, Fragrantica forums, specialist boards, public repeatable community threads | consumer language, objections, comparisons, repeat questions, rebuttals, corrections | Reddit is an explicit subfamily. Discord is noisy_deferred unless a public, repeatable, bounded slice exists with noise controls. |
| Reviews | retailer reviews, marketplace reviews, brand-site reviews, specialist fragrance reviews | experience claims, recency, complaints, repeat-use hints, contradiction checks | Do not collapse to aggregate stars; preserve recency and source conventions. |
| Creator / social video | Instagram, TikTok, YouTube, shorts/reels, affiliate/creator posts, later Reddit creator/community personalities | attention spread, creator clusters, campaign risk, audience language, propagation timing | Instagram has current adjacent capture/discovery work. TikTok, YouTube, and Reddit creator profiles are planned/deferred seams unless separately authorized. |
| Retail / PDP | Sephora, Ulta, Amazon, Nordstrom, brand PDPs, retailer search/category pages | availability, assortment, stock/discounting posture, review context, retailer corroboration | Retail/PDP is corroborative and operationally useful; it is not consumer-origin by itself. |
| Search / discovery | Google Trends, search-volume provider, SERP, preserved SERP packets, marketplace search, on-site search | interest traces, query language, discovery routes, hidden-venue pointers, counterevidence queries | Search-interest can carry attention/interest signal. Search-Surface MGT is a source-route scout only; methodology and pins stay with owning search-interest/AEO specs, while execution routes to Scanning frontier/exact-query work or Capture direct-source requests. |
| AEO / answer engines | Google AI Overviews, Gemini, ChatGPT, other answer-engine surfaces | answer visibility, cited-source ecosystem, entity association, visibility gaps | Visibility annotation only; never an independent demand-origin surface. Any change to this posture requires an Orca owner decision, not a per-run dispatcher override. |
| News / editorial / trade | trade publications, editorial, newsletters, specialist blogs, press | launch chronology, industry framing, awareness, third-party narrative | News is a distinct family; LinkedIn reposts of news point back to the actual source. |
| Professional / org-motion | ATS/careers pages, hiring pages, founder/executive public posts, partnership announcements, LinkedIn when explicitly routed | hiring/movement, organizational intent, operator-side propagation | ATS/careers pages are better movement sources than LinkedIn. LinkedIn remains no-live/planning-only unless separately authorized. |
| Owned channels | brand site, brand socials, email archive, product pages, press releases | official chronology, brand claims, launch framing | High chronology value, low independence. |

### Search-Surface MGT Standing Route Card

Standing behavior: when a commission has an open question about market language,
comparison/confusion, hidden venues, or counterevidence queries, the board should
consider a Search-Surface MGT route row rather than leaving search discovery as
background prose.

Use this row pattern:

```yaml
source_family: search_discovery
source_subfamily: search_surface_mgt
signal_role: search_interest
row_purpose: source_route
evidence_status: provided | source_backed | to_retrieve | gap
```

CSB may point to preserved SERP packets as routing evidence, but it does not run
Google capture, score search demand, or treat query count, rank, repeated SERP
presence, PAA/PAS, product modules, or autocomplete as proof.

Preferred handoff:

```text
CSB source-route row
-> Scanning exact-query / frontier selection
-> Capture P1 direct-source acquisition when concrete URLs or surfaces exist
```

## Field Vocabulary

Use these fields consistently:

```yaml
source_family: forums_community | reviews | creator_social_video | retail_pdp | search_discovery | aeo_answer_engines | news_editorial_trade | professional_org_motion | owned_channels | other
source_subfamily:
surface:
observable:
capture_posture: available_now | planned_lane | deferred | manual_only | not_authorized | noisy_deferred
signal_role: consumer_language | review_experience | creator_attention | retail_corroboration | search_interest | aeo_visibility | org_motion | owned_claim | none
row_purpose: chronology | source_route | signal_unit | contradiction | gap | classifier_handoff | recency_priority
recency_status: current_state | recent | older_context | stale_or_unknown | not_applicable
recency_attention: high | normal | low | unknown
graph_role: seed | node_candidate | edge_candidate | propagation_path | campaign_overlap_check | counterevidence_path | none
graph_weight_hint: high | medium | low | none
evidence_status: provided | source_backed | to_retrieve | gap | not_authorized | not_applicable | excluded_future_info
cutoff_status: in_window | post_cutoff_excluded | uncertain | not_applicable
surface_cutoff_status: existed_by_cutoff | post_cutoff_surface | uncertain | not_applicable
```

`signal_role` records what kind of signal the source contributes.
`row_purpose` records why this row exists inside the board.
`recency_status` and `recency_attention` record source-route priority, not truth:
same-strength newer/current URL-backed signals normally deserve more downstream
scan attention than older sources, even when their direction differs.
`graph_role` records how the row helps retrieval or later graph organization.
`graph_weight_hint` is relation utility only. It is never signal strength.
`surface_cutoff_status` records whether a source surface was available within a
backtest cutoff, separately from whether a specific observation has evidence.

Board labels are board-local. They do not map one-to-one onto demand-classifier
families. In particular, `org_motion` here means professional / hiring /
partnership movement, while retail presence belongs under Retail / PDP. The
demand classifier owns any board-`signal_role` to classifier-family mapping.

## Signal Collection Allocation

Use effort allocation as search hygiene, not a gate rule:

- majority effort: independent origin/experience/attention/corroboration routes;
- elevated effort: current or recent URL-backed source states when same-strength
  older sources would otherwise steer the board;
- meaningful effort: counterevidence, contradictions, campaign-overlap risk,
  and missing-signal checks;
- smaller effort: owned chronology and official claims.

Do not express allocation as pass/fail thresholds. If a source family is absent,
record it as a gap or not-applicable route.

## Graph-Light Contract

The board owns only the graph retrieval brief and graph-ready row labels.

The board may define:

- seed entities;
- adjacent products (Product), brands (Brand), formats, scent families, claims, or categories to
  check;
- creator slices and planned/deferred creator surfaces;
- source families and subfamilies to retrieve;
- mandatory counterevidence paths;
- node types to retrieve;
- edge types to retrieve;
- campaign-overlap and duplication checks;
- cutoff-date rule for backtests;
- graph-ready signal rows.

The board does not own:

- graph construction;
- graph database or persistent graph infrastructure;
- graph scoring;
- centrality or clustering algorithms;
- evidence weighting;
- demand classification;
- forecast probabilities;
- judgment or recommendation.

## Output Contract

Return the board in this exact section order. Use concise Markdown plus YAML
blocks where specified.

### 1. Commission Intake Receipt

```yaml
commission_id:
mode:
candidate_or_subject:
decision_context:
market_or_geography:
time_window:
evidence_cutoff_at:
input_status: complete | blocked | partial
missing_required_inputs:
cutoff_rule:
non_goals_preserved:
```

### 2. Boundary Statement

One short paragraph stating that this is an evidence/signals-only board, not a
demand verdict, proof claim, graph artifact, forecast, judgment, or client
output.

### 3. Source-Family Coverage Plan

Markdown table:

`Source family | Subfamily / surface | Capture posture | Why check it | Expected observable | Evidence status | Surface cutoff status | Cutoff status | Notes`

Include all relevant families. Include non-relevant families only when their
absence is decision-relevant.

When the commission has unresolved market-language,
comparison/confusion, hidden-venue, or counterevidence-query questions, include
`search_discovery / search_surface_mgt` in this plan even if no SERP packet exists
yet; mark evidence status `to_retrieve` or `gap`.

### 4. Signal Board Rows

Markdown table:

`Row ID | Source family | Subfamily | Surface | Observable | Signal role | Row purpose | Recency status | Recency attention | Graph role | Graph weight hint | Evidence status | Provenance needed | Surface cutoff status | Cutoff status | Handoff note`

Rules:

- Use stable row IDs: `SBR-001`, `SBR-002`, etc.
- When the Search-Surface MGT standing route card is triggered, include a route
  row rather than only prose. Use source family `search_discovery`, subfamily
  `search_surface_mgt`, signal role `search_interest`, and row purpose
  `source_route`. Use `Handoff note` to route Scanning exact-query/frontier
  work or Capture P1 direct-source acquisition. Do not list such rows in
  classifier handoff unless later retrieval produces source-backed, eligible
  evidence under Section 8.
- Do not combine distinct subfamilies in one row when their access,
  provenance, noise, or graph behavior differs.
- Mark unsupported rows as `to_retrieve` or `gap`; do not make evidence claims.
- For backtests, set `surface_cutoff_status` before assigning `evidence_status`.
  Post-cutoff surfaces are `excluded_future_info`, not ordinary `to_retrieve`.
- Counterevidence rows are first-class rows, not footnotes.
- Use `recency_attention: high` for same-strength newer/current signals that
  should receive more downstream scan attention than older context; this does
  not make the row proof, demand classification, or graph weight.
- Use `row_purpose: recency_priority` only when the row exists primarily to flag
  a recency routing priority; ordinary signal rows that happen to be recent can
  stay `signal_unit` with `recency_attention: high`.

### 5. Mandatory Counterevidence Paths

Markdown table:

`Path ID | What could disconfirm or weaken the signal | Source families to check | Why it matters | Evidence status | Cutoff rule`

At minimum, consider:

- creator-only or affiliate-campaign concentration;
- retailer/review contradiction;
- forum/community rejection or lack of uptake;
- search-interest decay or absence;
- owned-channel-only chronology;
- AEO visibility without origin signal;
- post-cutoff contamination in backtests.

### 6. Campaign And Duplication Risk

Markdown table:

`Risk ID | Possible duplication/campaign pattern | Surfaces implicated | Required check | Evidence status | Handoff note`

Treat creator clusters, PR launches, affiliate links, identical phrasing,
retailer/brand syndication, and answer-engine/cited-source loops as duplication
risks to check. Do not conclude manipulation unless supplied evidence supports
that claim.

### 7. Graph Retrieval Brief

```yaml
graph_retrieval_brief:
  seed_entities:
  adjacent_entities_to_check:
  creator_slices:
  source_families:
  mandatory_counterevidence_paths:
  node_types_to_retrieve:
  edge_types_to_retrieve:
  campaign_overlap_checks:
  graph_weight_notes:
  surface_cutoff_notes:
  forecast_targets_supported_without_probabilities:
  backtest_cutoff_date:
  future_info_exclusion_rule:
```

Use `graph_weight_notes` to record relation utility only (connection richness, propagation clustering, duplication risk, counterevidence routing). Do not record signal strength or demand-origin confidence here; graph weight is never signal weight.

Use `forecast_targets_supported_without_probabilities` only to name downstream
outcomes this evidence could help forecast later, such as review velocity,
restock/stockout, discounting, creator decay, search decay, or retailer
assortment changes. Do not assign probabilities.

### 8. Demand-Classifier Handoff Packet

```yaml
classifier_handoff_packet:
  candidate_or_subject:
  decision_context:
  mode:
  cutoff_date:
  signal_rows_for_handoff:
  counterevidence_rows_for_handoff:
  source_family_gaps:
  provenance_gaps:
  cutoff_uncertainties:
  durability_projection_evidence_or_gap:
  decay_lifespan_evidence_or_gap:
  manufactured_hype_dedup_risk:
  classifier_mapping_status: classifier_owned
  prohibited_claims:
    - no demand verdict
    - no buyer-proof claim
    - no validation or readiness claim
    - no graph score
    - no forecast probability
```

The classifier handoff packet is a packaging surface only. It may carry evidence
or gaps relevant to a later durability projection, decay-lifespan read, or
manufactured-hype dedupe risk, but it does not call those states. Do not map rows
to classifier families unless the dispatcher provides the classifier mapping.

For backtests: include rows in `signal_rows_for_handoff` or
`counterevidence_rows_for_handoff` only after retrieval proves
`cutoff_status: in_window`. Exclude rows where
`surface_cutoff_status: post_cutoff_surface`,
`surface_cutoff_status: uncertain`, `cutoff_status: post_cutoff_excluded`,
`cutoff_status: uncertain`, or `evidence_status: excluded_future_info`. Carry
excluded or cutoff-uncertain rows to `source_family_gaps` and/or
`cutoff_uncertainties` instead, with a note explaining whether the surface was
post-cutoff or cutoff observability is not yet proven.

### 9. Visible Limitations

List limitations specific to this commission. Include platform, source access,
cutoff, provenance, graph, classifier, and non-claim limitations.

### 10. Board Status And Run Boundary

Return this YAML block:

```yaml
board_status: READY_FOR_RETRIEVAL_HANDOFF | COLLECTION_BOARD_ONLY | NEEDS_COMMISSION_INTAKE | NEEDS_CUTOFF_DATE | NEEDS_OWNER_DECISION
run_boundary: CHAT_ONLY_BOARD_COMPLETE | INTAKE_ONLY | OWNER_DECISION_NEEDED
next_authorized_step: <one sentence>
```

Use `board_status` for the board's usefulness:

- `READY_FOR_RETRIEVAL_HANDOFF` - the board is complete enough to hand to a
  separately authorized retrieval/extraction lane. This is not a demand verdict or
  demand-classification readiness signal; any classifier use remains separately
  authorized under the demand classifier's own authority.
- `COLLECTION_BOARD_ONLY` - the board is useful as a collection map, but major
  gaps or cutoff uncertainties prevent a clean retrieval handoff.
- `NEEDS_COMMISSION_INTAKE` - required intake fields are missing; return the
  intake scaffold instead of a board.
- `NEEDS_CUTOFF_DATE` - backtest mode lacks a cutoff date; return the intake
  scaffold instead of a board.
- `NEEDS_OWNER_DECISION` - source access, source posture, classifier mapping,
  or graph boundary requires owner choice before retrieval.

Use `run_boundary` for what happened in this invocation:

- `CHAT_ONLY_BOARD_COMPLETE` - useful board returned in chat, with no file
  write or downstream execution authorized.
- `INTAKE_ONLY` - only the intake scaffold was returned.
- `OWNER_DECISION_NEEDED` - the next move requires owner choice before the board
  can be used.

If more than one applies, choose the most limiting status and explain the others
in one sentence.

## Final Rules

- Keep the board compact enough that a retrieval lane can act on it.
- Prefer explicit gaps over invented completeness.
- Preserve source family and subfamily identity.
- Treat AEO as visibility annotation only.
- For backtests, treat post-cutoff source surfaces as `excluded_future_info`
  rather than normal retrieval routes.
- Treat Discord as noisy_deferred unless public, repeatable, bounded, and
  noise-controlled.
- Treat LinkedIn as no-live/planning-only unless explicitly routed; prefer
  ATS/careers pages for movement.
- Treat creator surfaces as graph-rich but never demand proof by themselves.
- Keep graph weight separate from signal weight.
- Keep recency attention separate from proof, classifier mapping, and graph
  weight; it routes attention, not truth.
- Apply the Search-Surface MGT standing route card whenever its trigger is
  relevant; route execution to Scanning/Capture, never to CSB-owned search
  capture, and never count SERP rank, query count, module recurrence, or
  autocomplete as demand proof.
- If this is a repo-aware run that produced a full board, run the local
  validator before claiming the board is mechanically safe for classifier
  handoff. If this run produced only intake output, do not run the validator;
  return the intake blocker instead.
- End with the board status and run-boundary YAML block.

COMMISSION INPUTS FOLLOW:
````

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Commission Signal Board now has a standing Search-Surface MGT route-card
    behavior: relevant future boards should emit search_discovery/source_route
    rows, while execution routes through Scanning/Capture and no SERP/rank/module
    signal becomes proof.
  trigger: workflow_authority
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
    - orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
    - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md
    - docs/research/search_surface_mgt_pilot_p0_receipts_v0/search_surface_mgt_pilot_p0_capture_efficacy_review_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
      reason: >
        The playbook owns run sequence and validator use, not source-family route
        semantics. No operating-sequence or validator applicability change is
        needed.
    - path: .agents/hooks/check_commission_signal_board_output.py
      reason: >
        The existing `search_discovery`, `source_route`, and `search_interest`
        values cover this standing route card; no new field or enum is introduced.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Canonical CSB entry points are unchanged. The new P0 efficacy review is
        a branch-local research input for this route-card behavior, not a repo-map
        navigation entry.
  stale_language_search: >
    rg -n "search/AEO lane|Search-Surface|search-surface|SERP rank|query count|repeated SERP|source-route scout|standing route card|route-card"
    orca/product/spines/commission_signal_board orca/product/spines/scanning
    docs/research/search_surface_mgt_pilot_p0_receipts_v0
    (run 2026-06-25)
  stale_language_search_result: >
    Executed 2026-06-25 after route-card hardening. Hits are the standing CSB
    route card, prompt output rules, final rule, DCP text, the scanning guardrail
    against query-count/search-rank/repeated-SERP proof, and the P0 receipt,
    review, and run files. No checked surface turns Search-Surface MGT into
    proof, scoring, CSB-owned capture, or a standalone Search lane.
  non_claims:
    - not validation
    - not readiness
    - not demand classification
    - not buyer proof
    - not source-access authorization
    - not capture authorization
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Commission Signal Board rows now carry recency/currentness as source-route
    attention metadata: same-strength newer/current URL-backed signals normally
    deserve more downstream scan attention than older context, without becoming
    proof, classifier mapping, or graph weight.
  trigger: product_doctrine
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
    - orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md
    - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
    - .agents/hooks/check_commission_signal_board_output.py
    - orca-harness/tests/unit/test_commission_signal_board_output_validator.py
    - orca-harness/tests/fixtures/commission_signal_board_outputs/
    - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/hooks/check_commission_signal_board_output.py
    - orca/product/spines/scanning/README.md
    - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The CSB validator remains a manual/local checker, not a CI, pre-commit,
        or write-hook gate. The existing enforcement-placement rule already
        covers why mechanically checkable output shape lives in the checker.
  stale_language_search: >
    rg -n "recency|recent|current-state|currentness|optional board metadata|validator only requires existing core row columns|proof|graph weight|classifier mapping"
    orca/product/spines/commission_signal_board orca/product/spines/scanning docs/workflows/orca_repo_map_v0.md
    (run 2026-06-23)
  stale_language_search_result: >
    Hits were accepted recency/currentness attention language, repo-map routing
    summaries, existing scanning safeguards, historical CSB source-family
    references, or explicit no-proof/no-classifier/no-graph-weight boundaries.
    No controlling CSB/scanning surface was found that turns recency/currentness
    into buyer proof, demand classification, classifier mapping, or graph weight;
    the old optional-validator wording produced only receipt search-string hits,
    not live instructional hits, after the CSB validator began requiring recency
    fields and enum values.
    Capture and Judgment surfaces carry their own DCP receipts for the same
    propagation, and the follow-up adversarial review ran a cross-spine leakage
    search with no proof, scoring, route-binding, or gate-clearance leakage found.
  non_claims:
    - not validation
    - not readiness
    - not demand classification
    - not buyer proof
    - not source-access authorization
```

## Non-Claims

This prompt does not:

- ratify the Commission Signal Board as final product doctrine;
- authorize retrieval, scraping, crawling, source capture, or platform access;
- authorize graph construction, graph storage, graph scoring, or graph runtime;
- authorize demand classification, evidence weighting, forecasting, judgment,
  buyer proof, validation, readiness, or client-facing use;
- authorize file writes unless a later wrapper or dispatcher instruction binds
  a target path and docs-write permission.

## Next Authorized Step

Run one manual dry backtest or forward-case prompt invocation in chat-only mode.
If that output is useful, commission an adversarial artifact review of this
prompt or author a thin wrapper that binds a durable board output path for the
first controlled run.
