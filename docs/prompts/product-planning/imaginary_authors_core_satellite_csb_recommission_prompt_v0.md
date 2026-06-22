# Imaginary Authors Core-Satellite CSB Recommission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (core-satellite CSB recommission; product-planning family)
scope: >
  Recommissions a fresh bounded MGT intelligent-walk scan of Imaginary Authors
  from the durable CSB board, revised so CSB core asks every source-family
  question while retrieval is conditional by decision relevance. The run must
  preserve the prior executed scans and prompts, retrieve the board's existing
  gaps where authorized and valuable, add a narrow default channel check across
  main specialist retailers and major retailers/marketplaces, and pull
  satellites only when their decision trigger fires. This prompt does not
  execute capture, crawling, standing source-map work, gate clearance, judgment,
  buyer proof, or client-facing output.
use_when:
  - Recommissioning the Imaginary Authors scanning rehearsal after adopting the
    core/satellite CSB shape.
  - Testing whether CSB can ask complete source-family questions without forcing
    every satellite retrieval.
  - Producing a fresh downstream scan artifact that supersedes the prior v0 run
    for this revised commission, without mutating prior artifacts.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - docs/prompts/product-planning/imaginary_authors_csb_first_venue_eval_scanning_commission_prompt_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_csb_first_venue_eval_v0.md
  - orca/product/spines/scanning/README.md
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
stale_if:
  - The CSB board is superseded, rejected, or re-run.
  - The MGT operating model changes CSB-first, exact_query, venue_eval,
    hidden_venue_pointer, run-cap, or capture_request rules.
  - The owner rejects the core/satellite CSB shape or changes the target from
    Imaginary Authors.
  - A later accepted scan supersedes this recommission's downstream output path.
```

## Orca Prompt Preflight

```yaml
output_mode: file-write
template_kind: full-prompt
template_source: project-local commission prompt shape plus CSB playbook, scanning MGT operating model, and owner core/satellite decisions from current thread
edit_permission: docs-write
prompt_artifact_path: docs/prompts/product-planning/imaginary_authors_core_satellite_csb_recommission_prompt_v0.md
downstream_output_artifact_path: docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
workspace_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-fragrance-commission
branch: codex/scanning-csb-first-followup
base_revision: origin/main at dispatch time
source_pack: S3 target deepening
csb_board_source: docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
do_not_modify:
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_csb_first_venue_eval_v0.md
  - docs/prompts/product-planning/imaginary_authors_csb_seeded_scanning_mgt_commission_prompt_v0.md
  - docs/prompts/product-planning/imaginary_authors_csb_first_venue_eval_scanning_commission_prompt_v0.md
dirty_state_allowance: clean worktree except this prompt and the fresh downstream scan artifact if executed
doctrine_change_decision: >
  no new durable doctrine change claimed; this is a fresh commission applying
  the owner-selected core/satellite scan shape for this target
model_lane: unbound
reviews: findings-first if this prompt or downstream scan is reviewed
```

## Fitness Reference

Goal: run a fresh, bounded CSB-first scanning rehearsal where core asks the
complete source-family question set, then retrieves only the source families
whose decision relevance warrants it.

Success signal: the receiver writes a new dated scan artifact that shows, for
each core source-family question, whether it was `retrieve_now`, `defer`,
`not_relevant`, `blocked`, `negative`, or `capture_request`; then records the
actual bounded moves, satellites triggered, observations promoted, hidden venue
pointers, capture requests, and non-claims. The receiver must not edit the prior
scan artifacts or prior commission prompts.

## Commission

Run one fresh targeted forward-mode MGT intelligent walk for:

```yaml
commission_id: scanning_mgt_imaginary_authors_core_satellite_csb_v0
mode: forward
candidate_or_subject: Imaginary Authors
market_or_geography: US indie/DTC fragrance
decision_context: >
  Evaluate whether public source families can reveal current or imminent
  allocation, assortment, SKU, launch, restock, channel, pricing, promotion, or
  discontinuation decisions. The CSB core must ask the source-family question
  set broadly, but retrieval should stay conditional: main specialist retailers
  and major retailers/marketplaces are default channel checks; historical,
  creator/social including public YouTube/Shorts creator-video routes,
  announcement, resale/decant, stockist/local boutique, and control-venue
  satellites are pulled only when their decision trigger fires.
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

- maximum 24 screening moves total;
- maximum 6 active venue/frontier branches;
- maximum 5 promoted observations;
- maximum 8 exact queries within the total move cap;
- maximum 5 default channel checks across main specialist retailers and major
  retailers/marketplaces, excluding owned/DTC;
- maximum 4 satellite moves total unless a boundary or high-yield observation
  justifies using remaining move budget;
- maximum 4 hidden venue pointers;
- maximum 2 capture requests;
- maximum 2 short quotes per source;
- stop after core questions and triggered satellites decay to minimal or zero
  expected value, or earlier if a source-policy/capture boundary fires.

Branch-aware dry handling applies only inside those caps. A dry move closes the
active venue branch; it does not end the whole run while another declared,
core-question, or freshly discovered venue has non-trivial expected value and
the total move cap remains open.

## Required Source Loading

Start with:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/decision-routing.md`
4. `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`
5. `docs/prompts/product-planning/imaginary_authors_csb_first_venue_eval_scanning_commission_prompt_v0.md`
6. `docs/research/orca_discovery_candidate_scan_imaginary_authors_csb_first_venue_eval_v0.md`
7. `orca/product/spines/scanning/README.md`
8. `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
9. `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md`

Then read only targeted sources needed for this commission:

- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
  sections for targeted forward mode, candidate promotion, and capture_request.
- `docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md`
  only as prior-run context and anti-repeat evidence. Do not edit it. Do not
  treat its old observations as fresh evidence without re-verification.

Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before applying
the MGT model to the scan.

## Core-Satellite Contract

Core always asks the question. Core does **not** always retrieve the source.
Every core row must receive one of these dispositions:

```yaml
retrieve_now: public source family is decision-relevant inside this commission and caps
defer: relevant in principle, but another lane, later run, or stronger trigger should own it
not_relevant: source family does not bear on this decision in this run
blocked: source boundary, access wall, login, platform policy, or route-binding issue blocks scan retrieval
negative: checked path produced decisive low/no yield
capture_request: Capture-owned preservation or access decision is warranted
```

The downstream scan must include a `Core Question Ledger` that records the
question, disposition, rationale, and whether a satellite was triggered.

## Core Questions And Default Retrieval

At minimum, ask these core questions:

| Core source family | Core question | Default retrieval posture | Boundary |
| --- | --- | --- | --- |
| Owned/DTC | What do official collection/PDP surfaces reveal about current SKU, price, availability, copy, launch, restock, promotion, or discontinuation state? | Retrieve now. | Owned chronology only; not independent demand proof. |
| Main specialist retailers | Do the main niche-fragrance retailers show current assortment, pricing, samples, availability, review volume/text, or SKU selection signal? | Retrieve now, capped. Start with Ministry of Scent and LuckyScent, then only obvious high-signal specialist routes surfaced by exact queries. | Specialist presence is a strong indie-fragrance precursor, not proof by itself. |
| Major retailers / marketplaces | Do major retailers or marketplaces show scale-channel presence, price, availability, broad review volume, or absence where the decision specifically concerns major-channel expansion? | Retrieve now, capped. Check Sephora, Ulta, Amazon, and only relevant major/partner routes such as Anthropologie if surfaced. | Major-retailer absence is not negative by default for indie fragrance. |
| Buyer-language venues | Do forums, detailed reviews, specialist communities, or retailer review text expose dated product-specific experience, objections, repeat-use/full-bottle language, comparisons, or unmet questions? | Retrieve when public and reachable inside caps; prioritize detailed review text over aggregate stars. | No login, scraping, Discord, or direct platform capture. |
| Exact-query discovery | Which exact SKU/brand queries reveal hidden venues, better origin routes, or decisive negatives? | Retrieve now, capped. | Exact queries are route discovery and logged negatives, not search volume or proof. |
| Creator/social influence | Is there SKU-specific creator/social momentum, and does it look organic, PR/affiliate, retailer-amplified, or brand-reposted? | Core question always; retrieve only authorized public/non-login web routes, including public YouTube videos/Shorts when reachable without login, or record deferred/blocked. | No live TikTok/Instagram read unless separately authorized; no comment scraping, channel/person dossier, or creator graph. |
| Announcement / campaign archive | Are launch, sale, restock, event, newsletter, or public post archives needed to establish chronology or duplication/campaign risk? | Satellite only. | Announcement archives are chronology/duplication context, not demand evidence. |
| Historical inventory / pricing | Are archived PDPs, Wayback snapshots, clearance pages, promotion history, or repeated stock checks needed to distinguish sell-through from temporary stockout, launch spike, or promotion? | Satellite only, high value when triggered. | Wayback is coarse corroboration, not a reliable restock monitor. |
| Resale / decant / interest proxies | Do completed resale, sample/decant availability, shopping surfaces, Trends, or exact-SKU suggestions matter for durability or unmet demand? | Satellite only. | Proxy signals require corroboration and do not prove demand alone. |
| Original partner / org motion | Do original partner, retailer, event, stockist, or official surfaces reveal channel/org motion better than editorial visibility? | Retrieve when surfaced and public. | Prefer original partner/official surfaces; no LinkedIn live access. |
| Negative/control venues | What checked venues produce decisive no-yield, discounting, stale listing, complaint, return, or absence signals that bear on this decision? | Satellite only; trigger when pressure-testing an optimistic signal. | Absence from major retail is not negative unless major-channel presence is the decision. |

## Satellite Trigger Rules

Pull a satellite only when one of its triggers fires:

| Satellite | Trigger | Output if pulled |
| --- | --- | --- |
| Historical inventory / pricing / restock | Current sold-out/restock/price/promo/discontinuation clue, reorder/allocation question, durability question, or need to distinguish sustained movement from launch/promo noise. | dated historical trace, reliability limit, corroboration need, and whether Capture should preserve source state. |
| Creator/social / announcement archive | Influence or campaign-risk question, public YouTube/Shorts video pointer, launch/restock/promo chronology gap, PR/affiliate duplication concern, or high-signal public pointer from exact-query discovery. | dated visibility/campaign/duplication note, not demand proof. |
| Resale / decant / sample / interest proxy | Durability, unmet demand, secondary-market, trial-behavior, or post-launch-interest question. | proxy observation or negative with corroboration limits. |
| Official stockist / local boutique expansion | Channel expansion, local allocation, or stockist network question not answered by main specialist and major retailer checks. | channel pointer or negative; not a full census. |
| Comparable-brand controls | Optimistic signal needs pressure-testing against similar brands or expected venues. | control negative/contrast, not a blanket disqualifier. |

## Exact Query Definition

An `exact_query` is a bounded public query using exact brand/SKU text and a
decision modifier to find hidden venues or decisive negatives. Examples:

```text
"Imaginary Authors" +"A Little Secret" review
"Dipped in Chocolate" +"sold out"
"First Peach of the Season" sample
"Imaginary Authors" restock
"Imaginary Authors" discontinued
"A Little Secret" +"LuckyScent"
"Dipped in Chocolate" +decant
"Imaginary Authors" +"A Little Secret" YouTube
"Dipped in Chocolate" +"Shorts"
```

Each exact query must record: query text, intent, retrieval date, result class,
venue or negative produced, and next-route decision.

## Review Text Priority

When review text is available, prioritize reviews that are:

- dated;
- product-specific;
- high-information rather than merely long;
- possession/use-indicating;
- comparison-rich;
- objection-bearing;
- repeat-use, full-bottle, repurchase, or return-language bearing;
- photo-bearing when the photo materially improves provenance or source confidence.

Do not treat word count, star count, or photo presence alone as a demand signal.

## Wayback / Historical Reliability Boundary

Use Wayback or archived PDPs as targeted corroboration, not as a default restock
monitor. They are useful for coarse facts such as PDP existence, copy changes,
visible price shifts, visible sold-out states, promo/clearance context, or SKU
disappearance. They are weak for efficient restock cadence because snapshots can
be sparse, dynamic stock UI can be missing, and geography/session state may
differ. Historical movement observations should name corroboration gaps.

## Starting Venue Map

Use the CSB board as the upstream route map, but convert its rows into the
core/satellite contract above. At minimum, evaluate:

| CSB row | Recommissioned task | Boundary |
| --- | --- | --- |
| SBR-001 owned channels | Retrieve official collection/PDP state and decide whether historical satellite is triggered. | Owned chronology only; not independent demand proof. |
| SBR-002 retail/PDP | Retrieve main specialist + major retailer/marketplace default checks, including LuckyScent and Ministry of Scent. | Retail is channel/precursor context; major absence is not negative by default. |
| SBR-003/SBR-004 editorial/trade | Use editorial to find original partner, announcement, or specialist routes; downgrade standalone visibility. | Visibility is not demand-origin proof. |
| SBR-005 forums/community | Retrieve reachable public buyer-language venues where authorized; otherwise record access note/defer. | No login, scraping, or direct capture. |
| SBR-006 reviews | Prioritize detailed review text, not aggregate stars. | Preserve recency and source conventions. |
| SBR-007 exact-query discovery | Run bounded exact public queries for hidden venues and decisive negatives. | Search is route discovery, not proof or monitoring. |
| SBR-008 AEO | Treat as visibility provenance only; use only to find better source routes if already visible. | Excluded from classifier handoff. |
| SBR-009 creator/social | Ask the influence/campaign question; retrieve only authorized public/non-login routes, including public YouTube videos/Shorts when reachable without login, or defer. | No live TikTok/Instagram read, comment scraping, or channel/person dossier. |
| SBR-010 org motion | Prefer original partner/official surfaces and public stockist/wholesale context when decision-relevant. | No LinkedIn live read. |

## Output Shape

Write the fresh downstream scan artifact to:

`docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md`

Minimum sections:

1. **Scan Intake Receipt**: commission id, scan date, mode, subject, run caps,
   source context status, and explicit prior-artifact non-edit statement.
2. **CSB Board Intake**: CSB board path, rows consumed, rows skipped, and why.
3. **Core Question Ledger**: each core question, disposition, rationale,
   satellite trigger state, and retrieval/non-retrieval reason.
4. **Default Channel Ledger**: main specialist retailer and major
   retailer/marketplace checks, including price, availability, review
   count/text availability, and channel interpretation.
5. **Satellite Trigger Ledger**: satellites pulled, satellites deferred, and
   why.
6. **Exact Query Discovery Ledger**: query, intent, retrieval date, result
   class, hidden venue or negative produced, and next-route decision.
7. **Venue Evaluation Ledger**: each CSB row or discovered venue, moves tried,
   value class, dry/blocked state, and stop reason.
8. **Hidden Venue Pointers** if any, using `hidden_venue_pointer` language.
9. **Screen-Light Observations** using MGT minimum shape with
   `signal_stage: venue_value | precursor | candidate_support | contradiction | negative | access_note | unknown`.
10. **Candidate Observation Decision**: either no candidate minted, or a minimal
    candidate observation that explains why promotion meets scan-core rules.
11. **Capture Requests** only if the capture-request promotion bar is met.
12. **Negatives And Access Notes**: decisive low/no-yield venues, public access
    walls tried, and control negatives that actually bear on the decision.
13. **Closeout**: `SCAN_COMPLETE`, `SCAN_BLOCKED`, or `SCAN_HOLD`, with what
    the next lane may do.

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

- Do not edit, rewrite, or "correct" the prior scan artifacts at
  `docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md` or
  `docs/research/orca_discovery_candidate_scan_imaginary_authors_csb_first_venue_eval_v0.md`.
- Do not edit the prior commission prompts at
  `docs/prompts/product-planning/imaginary_authors_csb_seeded_scanning_mgt_commission_prompt_v0.md` or
  `docs/prompts/product-planning/imaginary_authors_csb_first_venue_eval_scanning_commission_prompt_v0.md`.
- No crawler, monitor, registry, atlas, standing source map, scheduler, graph
  construction, outreach, buyer-contact, capture packet, ECR, Cleaning,
  Judgment, gate verdict, buyer proof, or client-facing output.
- No login, private/auth-gated access, bulk scrape, Discord scraping, LinkedIn
  live access, TikTok/Instagram live read, or person dossier.
- Public YouTube videos/Shorts are allowed only as bounded non-login source
  routes: no comment scraping, channel/person dossier, subscriber/follower
  graph, or standing creator monitoring.
- No route binding. Scanning may cite a known route state or say `unknown`;
  Capture owns route selection and packet-grade acquisition.
- No demand verdict. Exact queries, channel presence, specialist-retailer
  presence, major-retailer absence, venue value, historical traces, hidden venue
  pointers, proxies, and precursor surfaces do not prove demand, clear a gate,
  or mint a candidate without promotion.

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
rg -n "route binding|capture owns|packet-grade|capture_request|gate clearance|demand proof" docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
```

Return a concise closeout: path written, source context status, move count,
core questions asked, dispositions, default channel checks, satellites pulled
or deferred, exact queries used, hidden venue pointers, observations promoted,
capture requests emitted, validations run/not run, and blockers.

## Non-Claims

This commission is not validation, readiness, demand proof, buyer proof,
judgment-quality evidence, scan-core ratification, source-class ratification,
capture authorization, source-access expansion, implementation authorization,
or permission to run a crawler/monitor/registry/atlas. It opens one fresh
screen-light CSB-first core/satellite venue-evaluation scanning run only.
