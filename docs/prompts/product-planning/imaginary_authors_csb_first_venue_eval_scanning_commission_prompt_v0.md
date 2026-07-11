# Imaginary Authors CSB-First Venue-Evaluation Scanning Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (fresh CSB-first scanning commission; product-planning family)
scope: >
  Commissions a fresh bounded MGT intelligent-walk scan of Imaginary Authors
  from the durable CSB board, with scanning focused on venue-value evaluation,
  exact-query discovery, and hidden-venue discovery. This prompt does not revise the prior executed
  scan artifact and does not authorize capture, crawling, gate clearance,
  judgment, or buyer proof.
use_when:
  - Rerunning the Imaginary Authors scanning rehearsal in the corrected CSB-first order.
  - Testing whether CSB-nominated venues are valuable and whether hidden venues were missed.
  - Producing a fresh scan artifact without mutating the earlier MGT scan output.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md
  - forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md
stale_if:
  - The CSB board is superseded, rejected, or re-run.
  - The MGT operating model changes CSB-first, exact_query, venue_eval, hidden_venue_pointer, run-cap, or capture_request rules.
  - The prior scan artifact is amended by a later accepted correction.
  - The owner changes the target from Imaginary Authors or rejects a fresh rerun.
```

## Forseti Prompt Preflight

```yaml
output_mode: file-write
template_kind: full-prompt
template_source: project-local commission prompt shape plus CSB playbook and scanning MGT operating model
edit_permission: docs-write
prompt_artifact_path: docs/prompts/product-planning/imaginary_authors_csb_first_venue_eval_scanning_commission_prompt_v0.md
downstream_output_artifact_path: docs/research/orca_discovery_candidate_scan_imaginary_authors_csb_first_venue_eval_v0.md
workspace_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-fragrance-commission
branch: codex/scanning-csb-first-followup
base_revision: origin/main at dispatch time
csb_board_source: docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
do_not_modify:
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md
  - docs/prompts/product-planning/imaginary_authors_csb_seeded_scanning_mgt_commission_prompt_v0.md
dirty_state_allowance: clean worktree except this prompt, the CSB-first model patches, and the fresh downstream scan artifact if executed
doctrine_change_decision: no new doctrine change beyond the accompanying CSB-first scanning alignment patch
model_lane: unbound
reviews: findings-first if this prompt or downstream scan is reviewed
```

## Fitness Reference

Goal: run a fresh, bounded scanning rehearsal in the corrected order: CSB first,
then scanning as venue-value evaluation, exact-query discovery, and hidden-venue
discovery.

Success signal: the receiver writes a new dated scan artifact that maps each
CSB row or source family to one of: valuable venue, low-value venue,
exact-query result, access note, hidden venue pointer, observation, negative, or
justified capture_request.
The receiver must not edit the prior scan artifact.

## Commission

Run one fresh targeted forward-mode MGT intelligent walk for:

```yaml
commission_id: scanning_mgt_imaginary_authors_csb_first_venue_eval_v0
mode: forward
candidate_or_subject: Imaginary Authors
market_or_geography: US indie/DTC fragrance
decision_context: >
  Evaluate whether CSB-nominated venues can reveal current or imminent public
  allocation, assortment, SKU, launch, restock, channel, or discontinuation
  decisions. Find hidden venues CSB missed only when they appear likely to
  improve venue value, independent-origin discovery, contradiction checks, or
  capture routing.
evidence_cutoff_at: not_applicable
scan_date: current run date
```

This commission **explicitly declares** the run as an MGT bounded intelligent
walk under
`forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md`
and invokes its branch-aware dry rule. The declaration lives here in the
authorizing commission; the scan must not self-declare MGT at runtime.

## Run Caps

Hard caps:

- maximum 18 screening moves total;
- maximum 5 active venue/frontier branches;
- maximum 4 promoted observations;
- maximum 6 exact queries within the total move cap;
- maximum 4 hidden venue pointers;
- maximum 2 capture requests;
- maximum 2 short quotes per source;
- stop after CSB-nominated and discovered venues decay to minimal or zero
  expected value, or earlier if a source-policy/capture boundary fires.

Branch-aware dry handling applies only inside those caps. A dry move closes the
active venue branch; it does not end the whole run while another CSB-nominated
or freshly discovered venue has non-trivial expected value and the total move
cap remains open.

## Required Source Loading

Start with:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`
4. `forseti/product/spines/scanning/README.md`
5. `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md`
6. `forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md`

Then read only targeted sources needed for this commission:

- `forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md`
  sections for targeted forward mode, candidate promotion, and capture_request.
- `docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md`
  only as prior-run context and anti-repeat evidence. Do not edit it. Do not
  treat its old observations as fresh evidence without re-verification.

Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before applying
the MGT model to the scan.

## Starting Venue Map

Use the CSB board as the upstream route map. At minimum, evaluate:

| CSB row | Venue evaluation task | Boundary |
| --- | --- | --- |
| SBR-001 owned channels | Re-check official collection/PDP surfaces for volatile SKU, availability, launch, or restock value. | Owned chronology only; not independent demand proof. |
| SBR-002 retail/PDP | Test whether retailer venue adds review, assortment, or route value beyond owned chronology. | Retail is G4/channel corroboration only. |
| SBR-003/SBR-004 editorial/trade | Test whether editorial venues reveal better origin venues or only visibility. | Visibility is not demand-origin proof. |
| SBR-005 forums/community | Determine whether public community venues are reachable and valuable or access-walled/noisy. | No login, scraping, or direct capture. |
| SBR-006 reviews | Determine whether review venues expose dated experience language or only aggregate listing context. | Preserve recency and source conventions. |
| SBR-007 exact-query discovery | Run bounded exact public queries to find hidden venues CSB missed and decisive negatives. | Exact queries are route discovery, not proof, search-volume, or monitoring. |
| SBR-008 AEO | Treat as visibility provenance only; use only to find better source routes. | Excluded from classifier handoff. |
| SBR-009 creator/social | Do not run live creator/social access unless separately authorized. | Record planned/deferred only. |
| SBR-010 org motion | Prefer original partner/official surfaces over LinkedIn live access. | No LinkedIn live read. |

## Output Shape

Write the fresh downstream scan artifact to:

`docs/research/orca_discovery_candidate_scan_imaginary_authors_csb_first_venue_eval_v0.md`

Minimum sections:

1. **Scan Intake Receipt**: commission id, scan date, mode, subject, run caps,
   source context status, and explicit prior-artifact non-edit statement.
2. **CSB Board Intake**: CSB board path, rows consumed, rows skipped, and why.
3. **Venue Evaluation Ledger**: each CSB row or discovered venue, moves tried,
   value class, dry/blocked state, and stop reason.
4. **Exact Query Discovery Ledger**: each `exact_query`, intent, retrieval date,
   result class, hidden venue or negative produced, and next-route decision.
5. **Hidden Venue Pointers** if any, using `hidden_venue_pointer` language.
6. **Screen-Light Observations** using MGT minimum shape with
   `signal_stage: venue_value | precursor | candidate_support | contradiction | negative | access_note | unknown`.
7. **Candidate Observation Decision**: either no candidate minted, or a minimal
   candidate observation that explains why promotion meets scan-core rules.
8. **Capture Requests** only if the capture-request promotion bar is met.
9. **Negatives And Access Notes**: decisive low/no-yield venues and public
   access walls tried.
10. **Closeout**: `SCAN_COMPLETE`, `SCAN_BLOCKED`, or `SCAN_HOLD`, with what the
   next lane may do.

## Capture Request Bar

Do not emit a capture_request merely because a venue produced a non-empty clue.
At least one must be true:

- source state is volatile or time-sensitive enough that packet-grade
  preservation could matter;
- the next useful read is blocked by a source-access, entitlement, or
  route-binding boundary scanning must not cross;
- a promoted or near-promoted candidate-support observation needs Capture to
  preserve provenance before gate use;
- a hidden venue is high-yield enough that Capture-owned acquisition is the
  right next action, not another screen-light scan move.

## Hard Boundaries

- Do not edit, rewrite, or "correct" the prior scan artifact at
  `docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md`.
- Do not edit the prior commission prompt at
  `docs/prompts/product-planning/imaginary_authors_csb_seeded_scanning_mgt_commission_prompt_v0.md`.
- No crawler, monitor, registry, atlas, standing source map, scheduler, graph
  construction, outreach, buyer-contact, capture packet, ECR, Cleaning,
  Judgment, gate verdict, buyer proof, or client-facing output.
- No login, private/auth-gated access, bulk scrape, Discord scraping, LinkedIn
  live access, TikTok/Instagram live read, or person dossier.
- No route binding. Scanning may cite a known route state or say `unknown`;
  Capture owns route selection and packet-grade acquisition.
- No demand verdict. Exact queries, venue value, hidden venue pointers, and
  precursor surfaces do not prove demand, clear a gate, or mint a candidate
  without promotion.

## Validation And Closeout

After writing the fresh downstream scan artifact, run:

```powershell
git diff --check
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_placement.py --check
```

If the scan emits a capture request, also run:

```powershell
rg -n "route binding|capture owns|packet-grade|capture_request|gate clearance|demand proof" docs/research/orca_discovery_candidate_scan_imaginary_authors_csb_first_venue_eval_v0.md
```

Return a concise closeout: path written, source context status, move count,
CSB rows evaluated, exact queries used, hidden venue pointers, observations
promoted, capture requests emitted, validations run/not run, and blockers.

## Non-Claims

This commission is not validation, readiness, demand proof, buyer proof,
judgment-quality evidence, scan-core ratification, source-class ratification,
capture authorization, source-access expansion, implementation authorization,
or permission to run a crawler/monitor/registry/atlas. It opens one fresh
screen-light CSB-first venue-evaluation scanning run only.