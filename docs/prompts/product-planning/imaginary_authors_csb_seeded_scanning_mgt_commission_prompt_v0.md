# Imaginary Authors CSB-Seeded Scanning MGT Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (targeted scanning commission; product-planning family)
scope: >
  Commissions one bounded MGT intelligent-walk scan of Imaginary Authors as a
  CSB-branch-selected US indie/DTC fragrance seed. The scan looks for current or
  imminent public allocation, assortment, SKU, launch, restock, channel, or
  discontinuation signals worth routing to Capture. It is screen-light only and
  does not authorize capture, crawling, gate clearance, judgment, or buyer proof.
use_when:
  - Dispatching the first controlled targeted scanning-lane rehearsal after the MGT intelligent-walk model landed.
  - Testing precursor_signal / precursor_surface vocabulary on a CSB-selected fragrance brand.
  - Opening a capture_request handoff only after fresh scan observations justify it.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
  - forseti/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md
  - docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0_evidence.json
  - forseti/product/case_families/product_learning/fragrance/consumer_demand_candidate_pool_handoff_v0.md
stale_if:
  - The MGT intelligent-walk model changes its explicit-declaration, run-cap, or capture_request rules.
  - The scan-core targeted-forward mode is owner-adjudicated, superseded, or rejected.
  - The Commission Signal Board prompt/playbook changes its source-family vocabulary or handoff boundaries.
  - The owner rejects Imaginary Authors as an appropriate first scanning rehearsal seed.
```

## Orca Prompt Preflight

```yaml
output_mode: file-write
template_kind: full-prompt
template_source: project-local commission prompt shape plus prompt-orchestrator contract
edit_permission: docs-write
prompt_artifact_path: docs/prompts/product-planning/imaginary_authors_csb_seeded_scanning_mgt_commission_prompt_v0.md
downstream_output_artifact_path: docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md
workspace_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-fragrance-commission
branch: codex/scanning-fragrance-commission
base_revision: origin/main @ 01982bb9
csb_selection_source: commission-signal-board-spine @ ab63dc01
dirty_state_allowance: clean worktree except this prompt artifact and the downstream scan artifact if executed
doctrine_change_decision: no doctrine change; this is a case-local commission using existing scanning vocabulary
model_lane: unbound
reviews: findings-first if this prompt or the downstream scan is reviewed
```

## Fitness Reference

Goal: run the smallest useful first rehearsal of the new scanning lane on one
fragrance brand selected from CSB-visible material.

Success signal: the receiver produces either a bounded, dated scan artifact with
high-signal `precursor_signal`, `precursor_surface`, `observation`, `negative`,
`access_note`, and optional `capture_request` rows, or a precise blocker showing
why the scan cannot be run without capture/source-access authority.

## Commission

Run one targeted forward-mode MGT intelligent-walk scan for:

```yaml
commission_id: scanning_mgt_imaginary_authors_csb_seed_v0
mode: forward
candidate_or_subject: Imaginary Authors
market_or_geography: US indie/DTC fragrance
decision_context: >
  Look for current or imminent public signals of an allocation, assortment, SKU,
  launch, restock, channel, or discontinuation decision worth routing to Capture.
  Prior SKU-kill history is a decision-shape precedent only; it is not current
  evidence and must not fill a forward slot.
evidence_cutoff_at: not_applicable
scan_date: current run date
```

This commission **explicitly declares** the run as an MGT bounded intelligent
walk under
`orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
and invokes its branch-aware dry rule. The declaration lives here in the
authorizing commission; the scan must not self-declare MGT at runtime.

## Run Caps

Hard caps:

- maximum 18 screening moves total;
- maximum 5 active frontier branches;
- maximum 4 promoted observations;
- maximum 3 capture requests;
- maximum 2 short quotes per source;
- stop after all declared/discovered frontiers have decayed to minimal or zero
  expected value, or earlier if a source-policy/capture boundary fires.

Branch-aware dry handling applies only inside those caps. A dry move closes the
active branch after the guide's dry rule; it does not end the whole run while
another declared or freshly surfaced frontier has non-trivial expected value and
the total move cap remains open.

## Required Source Loading

Start with:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `orca/product/spines/scanning/README.md`
4. `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
5. `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md`

Then read only the targeted sources needed for this commission:

- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
  sections for targeted forward mode, candidate promotion, and capture_request.
- `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`
  for signal-board vocabulary boundaries; do not produce a full CSB board unless
  separately commissioned.
- `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md` and
  `_evidence.json` only for the CSB-visible seed that Imaginary Authors appeared
  in "top indie perfume brands in the US" answer-engine probes.
- `orca/product/case_families/product_learning/fragrance/consumer_demand_candidate_pool_handoff_v0.md`
  only to understand the historical SKU-kill decision shape and the rule that a
  backtest pool is not a forward-mode source.

Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before applying
the MGT model to the scan. Treat the CSB branch read as seed selection, not as
current source authority. Use current-main paths for the downstream artifact.

## Seed Frontiers

Initial frontiers, all subject to expected decision value:

| Frontier | Why inspect | Boundary |
| --- | --- | --- |
| Imaginary Authors official site and collection/product surfaces | Owned chronology, assortment, SKU availability, launch/discontinuation hints. | Owned claims only; not independent demand proof. |
| Specialist fragrance community surfaces around Imaginary Authors, Whispered Myths, Telegrama, discontinued tags, and current releases | Likely precursor surfaces for SKU/assortment movement and user language. | Public only; Reddit/Basenotes walls become access_note or orchestrator-mediated screening read, not direct capture. |
| Review/retail/PDP surfaces if current public pages exist | Possible corroboration, review-experience language, availability/discounting posture. | Retail is G4 corroboration only; not demand-origin by itself. |
| Search/AEO surfaces from the CSB/AEO seed query family | Visibility and cited-source ecosystem; may reveal better origin surfaces. | AEO is visibility annotation only, never independent demand-origin proof. |
| News/editorial/trade mentions of recent Imaginary Authors decisions | Launch chronology, third-party framing, possible org-motion context. | Press may launder an origin; do not double-count laundered siblings. |

## Output Shape

Write the downstream scan artifact to:

`docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md`

Minimum sections:

1. **Scan Intake Receipt**: commission id, scan date, mode, subject, run caps,
   source context status, and non-goals.
2. **Frontier Ledger**: selected frontiers, why selected, moves attempted, dry
   branches, pivots, and stop reason.
3. **Screen-Light Observations** using MGT minimum shape:

```yaml
observation_id:
source_move_id:
url:
retrieval_date:
short_quote_or_summary:
signal_stage: precursor | candidate_support | contradiction | negative | access_note | unknown
claim_it_might_support:
gate_role: none | demand_origin | costly_behavior | divergence | org_motion | decision_event | influence
independence_hypothesis:
uncertainty_or_limits:
```

4. **Candidate Observation Decision**: either no candidate minted, or a minimal
   candidate observation that explains why promotion meets scan-core rules.
5. **Capture Requests** if justified, using the MGT `capture_request` shape.
6. **Negatives And Access Notes**: decisive low/no-yield paths and public access
   walls tried.
7. **Closeout**: `SCAN_COMPLETE`, `SCAN_BLOCKED`, or `SCAN_HOLD`, with what the
   next lane may do.

## Hard Boundaries

- No crawler, monitor, registry, atlas, standing source map, scheduler, graph
  construction, outreach, buyer-contact, capture packet, ECR, Cleaning, Judgment,
  gate verdict, buyer proof, or client-facing output.
- No login, private/auth-gated access, bulk scrape, Discord scraping, LinkedIn
  live access, TikTok/Instagram live read, or person dossier.
- No route binding. Scanning may cite a known route state or say `unknown`;
  Capture owns route selection and packet-grade acquisition.
- No use of the historical Imaginary Authors backtest pool row as a forward slot
  source. It may only inform what decision shapes to look for.
- No demand verdict. A precursor signal may route the walk or request Capture;
  it does not prove demand, clear a gate, or mint a candidate without promotion.

## Validation And Closeout

After writing the downstream scan artifact, run:

```powershell
git diff --check
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_placement.py --check
```

If the scan emits a capture request, also run a targeted stale-language search
for accidental route binding:

```powershell
rg -n "route binding|capture owns|packet-grade|capture_request|gate clearance|demand proof" docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md
```

Return a concise closeout: path written, source context status, move count,
frontiers closed, observations promoted, capture requests emitted, validations
run/not run, and blockers.

## Non-Claims

This commission is not validation, readiness, demand proof, buyer proof,
judgment-quality evidence, scan-core ratification, source-class ratification,
capture authorization, source-access expansion, implementation authorization,
or permission to run a crawler/monitor/registry/atlas. It opens one bounded
screen-light scanning run only.
