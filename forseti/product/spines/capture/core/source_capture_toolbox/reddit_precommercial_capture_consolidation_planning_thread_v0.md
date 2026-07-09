# Reddit Pre-Commercial Capture And Consolidation Planning Thread v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture planning artifact
scope: Durable planning thread for bounded Reddit pre-commercial capture and consolidation for Orca personal-project use.
use_when:
  - Planning Reddit capture/consolidation before implementation.
  - Scoping old Reddit exact-thread capture, CloakBrowser anti-blocking fallback, and parser handoff.
  - Distinguishing personal-project capture/consolidation from commercial API, storage, dashboard, ECR, Cleaning, or Judgment work.
authority_boundary: planning_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md
stale_if:
  - Reddit source-access ordering or selected anti-blocking backend changes.
  - Old Reddit HTML becomes unavailable or materially unsuitable.
  - CloakBrowser becomes infeasible as the selected primary backend.
  - Reddit warm same-context `.json` access posture materially changes.
  - Source Capture Packet lifecycle, retention, or consolidation authority moves.
  - Candidate Signal Intake / Corpus Intake receives its own contract and gives
    pre-Decision-Frame Reddit scouting units a compliant destination.
```

## Status

Status: `REDDIT_PRECOMMERCIAL_CAPTURE_CONSOLIDATION_PLANNING_THREAD_V0`.

Pass type: architectural planning pass.

Implementation authorized by this artifact: no.

Runtime, dependency install, live Reddit run, storage, dashboard, scheduler,
deployment, or production monitoring authorized by this artifact: no.

## Decision Question

How should Orca plan bounded Reddit capture and consolidation for a
personal-project data spine without turning capture into broad crawling,
production scraping, storage infrastructure, ECR, Cleaning, Judgment, or
commercial evidence handling?

## Architectural Verdict

This is an architectural pass because it defines the capture route, source-set
boundary, parser role, consolidation handoff, packet provenance expectations,
and implementation stop lines. It is not a mere operator note.

The recommended spine is a bounded hybrid:

1. use exact old Reddit Direct HTTP first for supplied thread URLs when current
   old Reddit HTML is the capture target and the bounded batch runner accepts
   the URL;
2. use the selected CloakBrowser route when Direct HTTP is unsuitable, blocked,
   or browser-visible anti-blocking capture is explicitly needed;
3. prefer old Reddit HTML where available;
4. preserve source-visible bodies or body-equivalents in Source Capture Packets
   before parsing;
5. use BeautifulSoup-style parsing only after preservation;
6. consolidate parsed facts into a provenance-rich planning dataset or state
   artifact;
7. use archive capture as fallback or historical posture support, bounded to
   the same thread URL and same-thread canonical variants;
8. treat cold anonymous `.json` as downgraded, while allowing warm
   same-context `.json` after the exact old Reddit HTML thread loads
   successfully in the same browser context;
9. move commercial Reddit work to sanctioned commercial / enterprise API or
   data-licensing routes.
10. require success-signal gates that keep Decision-Frame-bound capture,
    candidate/scouting context, packet preservation, parser output,
    consolidation rows, source-quality posture, and batch state from silently
    promoting into one another.

## Locked Owner Decisions

- CloakBrowser is the primary anti-blocking browser backend for Reddit
  pre-commercial capture.
- Exact old Reddit Direct HTTP is the current operator default for supplied
  thread URLs when current old Reddit HTML is the capture target and the bounded
  batch runner accepts the URL.
- Patchright is only a compatibility fallback if CloakBrowser has a concrete
  blocker; it is not the default first probe.
- Old Reddit HTML is the preferred Reddit surface when available because it is
  more parser-stable than the modern app DOM.
- BeautifulSoup is parser-only. It does not fetch Reddit, bypass blocking,
  solve JavaScript rendering, replace provenance, or authorize capture.
- Cold anonymous Reddit `.json` is not the capture spine. If same-context
  `.json` works only after the exact old Reddit HTML thread has loaded
  successfully, record the warm-up, access posture, and both preserved bodies.
  HTML remains the browser-visible provenance surface; JSON is a structured
  enrichment body, not a standalone cold access method.
- The pre-commercial bound is not URL-only. It may be subreddit-bounded,
  thematic, query-based, thread-family scoped, or a small monitored thread set.
- No broad crawling, site-wide walking, generic subreddit harvesting, stolen
  credentials or cookies, nonconsensual sessions, no-entitlement gate bypass,
  security exploits, malware, credential stuffing, standalone CAPTCHA-solving
  services, cross-account/private/admin spillover once noticed, methods Orca
  would refuse to disclose internally, production monitoring, or
  commercial-scale use is authorized here.

## Option Comparison

| Option | Verdict | Reason |
| --- | --- | --- |
| Cold `.json` first | Downgraded | Too brittle as the spine under current Reddit access posture; Orca's 2026-06-08 bounded probes saw direct cold `.json`, browser cold `.json`, and CloakBrowser+proxy cold `.json` return network-security blocks. |
| Warm same-context `.json` after old Reddit HTML | Recommended enrichment path | A bounded 2026-06-08 probe loaded the exact old Reddit HTML thread first in no-proxy CloakBrowser, then fetched the same thread's `.json` URL in the same browser context and received valid JSON. HTML remains the visible provenance/warm-up surface; JSON is the structured body. |
| Modern Reddit app DOM first | Downgraded | Higher rendering and DOM volatility; can be used when old Reddit is unavailable, but should not be the default planning surface. |
| Old Reddit HTML via Direct HTTP | Current primary for supplied exact thread URLs | Cheapest working implemented route when current old Reddit HTML is the capture target and the bounded batch runner accepts the URL. |
| Old Reddit HTML via CloakBrowser | Anti-blocking/browser-visible route | Best fit when Direct HTTP is unsuitable, blocked, or browser-visible anti-blocking capture is explicitly needed. |
| Archive-first | Fallback / complement | Useful for historical posture and unavailable live pages, but archive bodies may be missing, incomplete, or cutoff-mismatched. |
| Official Reddit commercial / enterprise API | Future commercial route | Correct route once the project becomes commercial or client-funded; not the current personal-project default. |

## Capture Unit Boundary

A Reddit capture unit must name its bounded source set before any acquisition
run is scoped.

A Reddit capture unit is Data Capture Spine work only when it is bound to a
specific, pre-existing Decision Frame. A bounded source set — subreddit, theme,
query, thread family, or small monitored thread set — is not a Decision Frame
and does not by itself satisfy the Data Capture Commissioning Gate.

Each unit must be classified before capture as:

- `decision_frame_bound`: the unit may claim Data Capture handoff posture if it
  satisfies the remaining gates;
- `candidate_or_scouting`: the unit is pre-decision context and must not claim
  Data Capture handoff, source-quality completeness, fixture admission, ECR
  readiness, Cleaning readiness, Judgment readiness, validation, or buyer proof.

Candidate/scouting units are corpus-intake context only. The required separate
Candidate Signal Intake / Corpus Intake contract does not exist in this repo
yet, so a candidate/scouting Reddit unit currently has no compliant Data Capture
handoff destination. It may be held as planning-only context or recaptured later
under a real Decision Frame.

Allowed boundary shapes:

- a named subreddit plus explicit topical or temporal cutoff;
- a thematic query or research theme with named inclusion/exclusion limits;
- a thread family, such as related submissions around one event, product, or
  claim;
- a small monitored thread set with named cadence and stop date;
- a fixed historical thread list supplied by the operator.

Required capture-unit fields:

- `capture_unit_id`;
- `capture_unit_intake_status`: `decision_frame_bound` or
  `candidate_or_scouting`;
- `decision_frame_id_or_none`;
- purpose / research question;
- source-set boundary;
- subreddit, theme, query, thread family, or monitored-thread list;
- time cutoff and local cutoff timezone;
- expected volume ceiling;
- batch cadence budget, if batched;
- monitoring cadence, if any;
- stop date, if monitored;
- exclusions;
- selected method order;
- explicit non-commercial / personal-project posture;
- source-family hard-stop acknowledgement;
- packet-contamination stop acknowledgement.

Forbidden capture-unit shapes:

- site-wide Reddit crawling;
- generic subreddit harvesting without a topical or temporal bound;
- indefinite production monitoring;
- adaptive expansion from links, users, comments, recommendations, related
  surfaces, or "more like this" surfaces; re-bounding a followed hop does not
  convert it into in-bounds commissioned capture;
- capture intended to defeat a no-entitlement gate, private/admin surface, or
  credential requirement.

## Capture Flow

1. Commission a capture unit with the required boundary fields and classify it
   as `decision_frame_bound` or `candidate_or_scouting`.
2. Fetch old Reddit HTML through the future CloakBrowser adapter once
   implemented, using only the named source set and low-volume posture.
3. Preserve raw HTML, visible text/body-equivalent, locator, capture time,
   access posture, cutoff posture, and warnings in a Source Capture Packet
   before parsing.
4. Parse the preserved HTML with BeautifulSoup-style parsing into a derivative
   extraction draft.
5. Consolidate extraction drafts into a local planning/state table that points
   back to packets and raw preserved files. This table is not a database,
   durable corpus, reusable exported dataset, queue, scheduler, dashboard, or
   production monitor.
6. Add archive capture when live capture is unnecessary, unavailable, or useful
   for historical posture. For live access blocks, archive fallback stays inside
   the same source unit: exact supplied URL first, then same-thread canonical
   old/new host variant if applicable, then stop and record absence or preserved
   body. Do not use archive fallback to discover related Reddit targets.
7. Use warm same-context `.json` only after the exact old Reddit HTML thread
   loads without an access block in the same browser context. Preserve both the
   HTML/body-equivalent and JSON response with method provenance. Do not use
   cold `.json` probing as the primary route.
8. Before any Judgment or client-facing use, perform a separate materiality
   gate: reacquire, verify, or carry limitations rather than upgrading this
   planning capture into proof.
9. If credentials, cookies, raw browser-profile material, Playwright or browser
   storage-state JSON, session sidecars, authorization headers, or secrets
   appear in a packet, stop and treat the packet as contaminated scratch until a
   separate owner decision says how to dispose, redact, or isolate it.

## Parser Handoff

The parser may extract:

- submission title and body text;
- comment body text;
- visible author label;
- visible timestamp;
- visible score or score-hidden state;
- subreddit and permalink;
- submission id and comment id when visible or derivable from preserved source;
- parent / nesting cue;
- deleted, removed, collapsed, hidden, or unavailable posture;
- outbound links and media pointers;
- parser warnings.

The parser must not:

- decide credibility, relevance, quality, inclusion, exclusion, sentiment, or
  meaning;
- treat missing comments as absent from the original source;
- repair blocked, deleted, or unavailable content by inference;
- overwrite packet provenance;
- become the canonical source body.

## Consolidation Spine Shape

The planning consolidation artifact should be provenance-first. Candidate
fields:

| Field | Purpose |
| --- | --- |
| `capture_unit_id` | Links rows to the commissioned bounded source set. |
| `source_family` | `reddit`. |
| `surface` | `old_reddit_html`, `old_reddit_warm_context_json`, `archive_html`, or `modern_reddit_html`. |
| `subreddit` | Named subreddit when known. |
| `theme_or_query` | Thematic/query bound when applicable. |
| `thread_id` | Submission/thread identifier when visible or derivable. |
| `comment_id` | Comment identifier when visible or derivable. |
| `parent_id` | Parent/nesting relationship when extracted. |
| `source_locator` | URL, archive locator, or supplied provenance pointer. |
| `capture_time` | Time Orca captured or preserved the source. |
| `source_time_visible` | Source-visible post/comment timestamp when present. |
| `cutoff_posture` | Relationship to the local cutoff. |
| `access_posture` | Public, account-created, archive-only, failed, blocked, or limitation state. |
| `capture_method` | CloakBrowser, warm HTML -> same-context JSON, archive adapter, or other observed method. |
| `raw_packet_path` | Pointer to the Source Capture Packet. |
| `raw_html_file_id` | Pointer to raw/body-equivalent file inside the packet. |
| `parser_name_version` | Parser identity and version when known. |
| `parse_warning` | Visible extraction limitations. |
| `body_text` | Parsed derivative body text. |
| `visible_score` | Score if visible; otherwise visible hidden/unavailable state. |
| `visible_author` | Author label if visible; otherwise visible deleted/removed/unavailable state. |
| `deleted_removed_posture` | Deleted, removed, collapsed, hidden, or visible state. |
| `archive_posture` | Archive attempted, preserved, unavailable, not attempted, or mismatch state. |
| `visible_limitations` | Human-readable limitation string. |
| `row_status` | Source-unit queue row status: `planned`, `ready_for_tool_run`, `blocked_missing_input`, `packet_written_needs_report`, or `reported`. |
| `result_token` | Mini God-Tier result token, empty before a source-quality pass and never row-local vocabulary. |
| `packet_lifecycle` | Packet lifecycle state from the existing closed set; default `scratch`. |
| `sensitivity_note` | Required for Reddit rows because they may contain handles, user-authored posts, screenshots, or raw third-party bodies. |
| `retention_basis` | Why the row or packet facts may be retained or cited, if retained beyond scratch. |
| `allowed_downstream_use` | Visible downstream-use limit, if any; default is planning-only unless separately authorized. |
| `operator_completion_required` | State-assembler flag preserving operator review where required. |
| `separate_fixture_admission_decision_or_none` | Cited separate admission decision, or `none`. |
| `packet_or_manifest_hash` | Packet or manifest hash when available. |

This is a candidate planning shape, not a final database schema, storage
authorization, or ECR/Cleaning/Judgment design.

`raw_html_file_id` is the canonical source body pointer. `body_text` is
parser-derivative only and must remain row-marked as derivative with live
pointers to `raw_packet_path` and `raw_html_file_id`. A row without a resolvable
packet pointer must not present `body_text` as the source body.

## Success Signals

Every Reddit capture/consolidation claim must be checkable as a pass, fail, or
visible stop. Obligation-bearing items must use the existing obligation
discharge states (`met`, `partial`, `assessed_not_met`, `cannot_assess`,
`access_failed`, `blocked`, `unavailable_by_source`, `not_applicable`,
`not_attempted`) or a visible unknown-with-reason posture. The Reddit thread
does not create parallel obligation vocabulary.

G1 `decision_frame_or_candidate_intake_classified`: mandatory first gate. Each
unit is `decision_frame_bound` or `candidate_or_scouting`. A bounded source set
is not a Decision Frame.

G2 `bounded_source_set_pass`: named source set, purpose, exclusions, time
cutoff, and volume ceiling are visible. Any monitored set must carry both
`monitoring_cadence` and a hard `stop_date`; no stop date means the gate fails.
For bounded batch capture, cadence is a hard-ceiling budget (`max_threads` in a
time window with min/max gaps and visible stop reason), not a claim to mimic
human behavior or permission to retry around blocks.

G3 `method_order_observed`: use exact old Reddit Direct HTTP first for supplied
thread URLs when current old Reddit HTML is the capture target and the bounded
batch runner accepts the URL; use CloakBrowser anti-blocking when Direct HTTP is
unsuitable, blocked, or browser-visible anti-blocking capture is explicitly
needed; use warm same-context `.json` only after exact-thread HTML loads in the
same browser context; and use archive fallback where live capture is unnecessary
or fails visibly. Cold `.json` remains downgraded. Archive fallback for a
blocked thread must remain exact-unit bounded: exact URL, same-thread canonical
host variant if needed, visible `snapshot_count` / body-preservation result,
then stop. Commercial use moves to the sanctioned API/licensing path.

G4 `method_provenance_recorded`: capture method, source surface, backend, access
posture, anti-blocking or JS-challenge category if used, fallback posture,
packet path, raw file pointer, and limitations are visible.

G5 `disclosability_pass`: Orca can disclose exactly how the source was obtained
and no hard stop occurred.

G6 `packet_before_parser_pass`: raw/body-equivalent source material is preserved
in a Source Capture Packet before parser or consolidation output is trusted.

G7 `parser_derivative_pass`: parser output points back to the packet, carries
warnings, is row-marked derivative, and never becomes canonical body.

G8 `obligation_visibility_pass`: contract version, operator/session provenance,
mode/mode changes, timing/cutoff, archive/access/visibility, recapture, and
limitations carry the existing closed obligation/posture vocabulary rather than
Reddit-local substitutes.

G8a `blocked_access_preserved_or_fallback_recorded`: HTTP block pages and other
non-content interstitials are preserved as access outcomes when packetized, not
parser failures. If archive fallback is attempted, record whether the archive
body was preserved or absent; `snapshot_count=0` is not source completeness proof
and must not be promoted into a content claim.

G9 `related_thread_context_pass`: thread slice preserves parent, reply,
correction, rebuttal, confirmation, moderator/official, lock, edit, delete, and
exclusion context when visible enough for downstream reconstruction limits.

G10 `lifecycle_sensitivity_pass`: `packet_lifecycle` uses the closed lifecycle
set and defaults to `scratch`; `sensitivity_note`, `retention_basis`, and
`allowed_downstream_use` stay visible.

G11 `source_quality_compatibility_pass`: a row may claim source-quality posture
only through the Mini God-Tier profile after an operator-commissioned pass and
with `operator_completion_required` respected. This is not source-quality
scoring.

G12 `planning_only_pass`: no database, durable corpus, exported reusable
dataset, queue, scheduler, dashboard, production monitor, fixture admission,
ECR, Cleaning, Judgment, or client-facing role is created without separate
authorization.

G13 `commercial_transition_check`: client-funded, commercial, enterprise,
buyer-facing durable use, scale pressure beyond low-volume bounded capture, or
data-licensing pressure stops anti-blocking Reddit capture for that source and
reroutes to the sanctioned commercial/enterprise API or data-licensing path.

G14 `tier_no_silent_promotion_pass`: every claim names its tier and what that
tier does not clear; no tier is satisfied by a weaker tier.

G15 `no_source_discovery_expansion`: capture must not follow links, users,
comments, recommendations, related surfaces, or "more like this" surfaces to
discover new units. New units are separately commissioned.

G16 `no_secret_bearing_packet`: the packet never preserves credentials, cookies,
raw browser-profile material, storage-state JSON, session sidecars,
authorization headers, or secrets. If any appears, stop and treat the packet as
contaminated scratch.

## Success / Non-Success Ladder

Reddit capture success is tiered and non-promoting:

| Tier | Claim | Existing owner/evidence | Does not clear |
| --- | --- | --- | --- |
| Planning | Unit is in-bounds to scope. | G1-G2 plus queue `row_status`. | Capture, packet, or readiness. |
| Packet | Packet exists and owns the body/body-equivalent. | Packet path, manifest/hash, and obligation visibility. | Parser, source-quality, or fixture admission. |
| Parser | Extraction ran as derivative output. | `parser_name_version`, `parse_warning`, and packet pointers. | Meaning, credibility, body ownership, or source quality. |
| Consolidation | Rows are assembled and point to packets. | Planning/state table. | Storage, ECR, dedupe, cross-row verdict, or validation. |
| Source-quality | Row has a Mini God-Tier posture. | Profile-owned `result_token` after operator pass. | Validation, fixture admission, credibility, Judgment, or buyer proof. |
| Batch | Multi-row state is visible. | State-assembler census. | "All rows passed", rollup verdict, ladder-complete claim, or admission. |

## Armory Bridge

The Mini God-Tier profile, source-unit queue template, state assembler, packet
fixture/retention/sensitivity decision, and obligation contract own the
vocabularies this thread reuses. This thread defines no Reddit-local row-status,
result-token, lifecycle, finalization, retention, or obligation vocabulary.

Reuse these closed sets verbatim:

- row-status: `planned`, `ready_for_tool_run`, `blocked_missing_input`,
  `packet_written_needs_report`, `reported`;
- result tokens: `mini_god_tier_met`,
  `mini_god_tier_with_visible_limitations`,
  `current_body_standardized_only`, `archive_body_not_preserved`,
  `body_possession_not_proven`,
  `needs_separate_fixture_admission_decision`, `visible_stop`;
- packet lifecycle: `scratch`, `candidate_evidence`,
  `recommended_fixture_admission`, `separately_admitted`;
- state-assembler finalization: `suggested_result_token`,
  `result_token_finalization: operator_review_required`, and
  `operator_completion_required`;
- recapture relationship: `supersede`, `supplement`, `conflict`, `mixed`;
- cutoff posture: `pre_cutoff`, `post_cutoff`, `mixed`, `unknown`;
- archive posture: `archived`, `attempt_failed`, `not_attempted`,
  `not_applicable`.

Avoid new local terms such as `reddit_captured`, `consolidated`, `done`,
`operator_finalization_required`, `validated`, `ready`, `admitted`, `complete`,
`passed`, `score`, `scored`, `ranking`, `corpus`, `database`, `store`, `index`,
`monitor`, `pipeline`, or `dashboard` as row-level authority. The post's own
visible Reddit score may be recorded as `visible_score`; no row-level quality
score is created.

## Candidate And Scouting Gap

This planning thread can classify `candidate_or_scouting` units, but it cannot
give them a Data Capture Spine handoff destination. Until Orca creates a
separate Candidate Signal Intake / Corpus Intake contract, pre-Decision-Frame
Reddit scouting remains planning-only context or must be recaptured later under
a real Decision Frame.

## Implementation Plan Shape

This artifact does not authorize implementation, but it names the smallest
future implementation route that would be coherent if separately authorized:

1. Write a CloakBrowser adapter contract that preserves old Reddit HTML into
   Source Capture Packets without parser-side meaning decisions.
2. Make a separate install/runtime decision for CloakBrowser and any local
   dependency handling.
3. Build parser tests against local saved old Reddit HTML fixtures only before
   live capture.
4. Add packet-to-parser handoff with explicit derivative-output markers.
5. Emit a local CSV or JSONL consolidation artifact only if durable
   storage/consolidated output is separately authorized; otherwise keep the
   consolidation as an in-place planning/state table.

Stop conditions for any future implementation:

- no-entitlement gate bypass, private/admin surface access without consent, or
  obvious cross-account/private/admin spillover once noticed would be required;
- stolen credentials or cookies, nonconsensual sessions, security exploits,
  malware, credential stuffing, direct cookie import, standalone CAPTCHA-solving
  services, or any internally non-disclosable method would be required;
- packet contamination appears: credentials, cookies, raw browser-profile
  material, storage-state JSON, session sidecars, authorization headers, or
  secrets in the packet or sidecar output;
- volume/cadence pressure turns the task into broad crawling or production
  monitoring;
- the run needs persistent storage, dashboard, queue, scheduler, deployment, or
  commercial-scale operation;
- client-funded, commercial, enterprise, buyer-facing durable use, or
  data-licensing pressure appears before the source is rerouted to the sanctioned
  commercial/API path;
- parser output would need to decide credibility, relevance, quality, source
  meaning, or Judgment implications.

## What Would Change This Plan

- Old Reddit HTML becomes unavailable or no longer carries enough body and
  nesting structure.
- CloakBrowser becomes infeasible or materially worse than another bounded
  backend.
- Reddit grants or restores an official low-friction route suitable for the
  personal project.
- The project becomes commercial or client-funded, triggering commercial /
  enterprise API or licensing expectations.
- The desired volume becomes broad crawling, production monitoring, or
  source-discovery infrastructure.
- Legal, client, or platform obligations require stricter access, retention, or
  deletion handling.

## Non-Claims

This planning thread is not validation, readiness, legal sufficiency,
implementation execution, live Reddit capture authorization, CloakBrowser
installation proof, parser correctness proof, source completeness proof,
source-quality scoring, fixture admission, retention approval, storage
authorization, dashboard authorization, scheduler/deployment authorization,
production-runtime authorization, commercial Reddit authorization, Candidate
Signal Intake / Corpus Intake design, ECR design, Cleaning design, Judgment
design, buyer proof, or rights-to-process sufficiency.

The success signals classify and constrain claims. They do not authorize
capture, storage, scraping execution, source discovery, source-quality scoring,
fixture admission, ECR, Cleaning, Judgment, or commercial use by implication.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Reddit pre-commercial capture/consolidation now has a durable planning artifact that frames the work as an architectural planning pass: CloakBrowser-first old Reddit HTML capture, packet preservation before BeautifulSoup parsing, provenance-first consolidation, archive fallback, `.json` opportunistic fallback, and explicit non-implementation stop lines."
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "forseti-harness/docs/source_capture_agent_runbook.md"
    - "forseti-harness/docs/adapter_author_contract.md"
  intentionally_not_updated:
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Boundary permission and hard stops did not change; this artifact plans inside the existing discoverable/entitled plus disclosable boundary."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and forbidden outputs did not change; this artifact applies them to a Reddit planning route."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "CloakBrowser selection, Reddit ordering, `.json` posture, and commercial deferral were already authorized there; this artifact consolidates planning rather than expanding build authority."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Method ordering and parser posture were already updated; this artifact gives the planning thread a durable home."
    - path: "forseti-harness/docs/source_capture_agent_runbook.md"
      reason: "No runnable command, adapter behavior, or implementation status changed in this planning pass."
    - path: "forseti-harness/docs/adapter_author_contract.md"
      reason: "No adapter contract changed; future CloakBrowser and parser implementation remain separately scoped."
  stale_language_search: "rg -n \"reddit_precommercial_capture_consolidation_planning_thread|Reddit Pre-Commercial Capture|CloakBrowser-first old Reddit HTML|BeautifulSoup-style parsing|\\.json.*opportunistic\" docs/product/source_capture_toolbox docs/workflows/data_capture_spine_consolidation_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution"
    - "not live Reddit capture authorization"
    - "not CloakBrowser installed"
    - "not storage, dashboard, scheduler, deployment, or production runtime"
    - "not broad crawling"
    - "not commercial Reddit authorization"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - Success-Signal Hardening Patch

```yaml
direction_change_propagation:
  doctrine_changed: "The Reddit pre-commercial capture/consolidation planning thread now requires Decision-Frame-or-candidate classification, explicit non-promoting success tiers, Armory vocabulary reuse, contamination stops, no source-discovery expansion, commercial stop-and-reroute, and visible candidate-intake gap handling before any Reddit capture/consolidation claim can be treated as in-bounds."
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - lifecycle_boundary
    - workflow_authority
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/validation-gates.md"
    - ".agents/workflow-overlay/review-lanes.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md"
  intentionally_not_updated:
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "The obligation contract already states Data Capture Spine v0 is commissioned-capture-only and routes pre-Decision-Frame corpus capture to a separate Candidate/Corpus Intake contract."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "The hard-stop and disclosability standard did not change; this patch applies it to Reddit wording."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "CloakBrowser ordering, Reddit pre-commercial route, and commercial stop-and-reroute were already authorized there."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "The method plan already records CloakBrowser-first Reddit ordering, `.json` opportunistic fallback, old Reddit HTML preference, and BeautifulSoup parser-only posture."
    - path: "docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md"
      reason: "Packet lifecycle, sensitivity, retention, contaminated scratch, and fixture-admission rules did not change."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "Mini God-Tier tokens and lifecycle vocabulary remain the owner; this patch reuses them without changing the set."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
      reason: "Queue row-status vocabulary remains the owner; this patch reuses it without changing the set."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md"
      reason: "State assembler census/finalization posture remains unchanged; this patch only names it as an existing owner."
  stale_language_search: "rg -n \"bounded source set is not a Decision Frame|candidate_or_scouting|operator_finalization_required|login, private, admin, paywalled|limitations\\`|Reddit success-signal|reddit_precommercial_capture_consolidation_success_signal_architecture\" forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md forseti/product/spines/capture/core/source_capture_toolbox/README.md docs/workflows/data_capture_spine_consolidation_map_v0.md"
  stale_language_search_result: "Executed after this patch. Remaining hits are intended: new Decision-Frame/candidate classification text, inbound references to the success-signal architecture object, the explicit avoid-list entry for `operator_finalization_required`, and this DCP receipt/search string. No live wording keeps blanket `login, private, admin, paywalled` stop logic, a row-level `limitations` field, or a hidden orphan routing object."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution"
    - "not live Reddit capture authorization"
    - "not Candidate Signal Intake / Corpus Intake design"
    - "not storage, dashboard, scheduler, deployment, or production runtime"
    - "not source-quality scoring, fixture admission, ECR, Cleaning, Judgment, buyer proof, or commercial Reddit authorization"
```
