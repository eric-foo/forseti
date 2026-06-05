# Reddit Pre-Commercial Capture And Consolidation Planning Thread v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture planning artifact
scope: Durable planning thread for bounded Reddit pre-commercial capture and consolidation for Orca personal-project use.
use_when:
  - Planning Reddit capture/consolidation before implementation.
  - Scoping CloakBrowser-first old Reddit HTML capture and parser handoff.
  - Distinguishing personal-project capture/consolidation from commercial API, storage, dashboard, ECR, Cleaning, or Judgment work.
authority_boundary: planning_only
open_next:
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/product/source_capture_toolbox/README.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - docs/product/data_capture_source_access_method_plan_v0.md
stale_if:
  - Reddit source-access ordering or selected anti-blocking backend changes.
  - Old Reddit HTML becomes unavailable or materially unsuitable.
  - CloakBrowser becomes infeasible as the selected primary backend.
  - Reddit anonymous `.json` access posture materially changes.
  - Source Capture Packet lifecycle, retention, or consolidation authority moves.
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

1. use the selected CloakBrowser route first once it exists;
2. prefer old Reddit HTML where available;
3. preserve source-visible bodies or body-equivalents in Source Capture Packets
   before parsing;
4. use BeautifulSoup-style parsing only after preservation;
5. consolidate parsed facts into a provenance-rich planning dataset or state
   artifact;
6. use archive capture as fallback or historical posture support;
7. treat anonymous `.json` as opportunistic fallback, not the spine;
8. move commercial Reddit work to sanctioned commercial / enterprise API or
   data-licensing routes.

## Locked Owner Decisions

- CloakBrowser is the primary future anti-blocking browser backend for Reddit
  pre-commercial capture once implemented.
- Patchright is only a compatibility fallback if CloakBrowser has a concrete
  blocker; it is not the default first probe.
- Old Reddit HTML is the preferred Reddit surface when available because it is
  more parser-stable than the modern app DOM.
- BeautifulSoup is parser-only. It does not fetch Reddit, bypass blocking,
  solve JavaScript rendering, replace provenance, or authorize capture.
- Anonymous Reddit `.json` is not the capture spine. If it works in a bounded
  run, record the observed access posture and preserve the output as a fallback
  source artifact.
- The pre-commercial bound is not URL-only. It may be subreddit-bounded,
  thematic, query-based, thread-family scoped, or a small monitored thread set.
- No broad crawling, site-wide walking, generic subreddit harvesting, stolen
  credentials, nonconsensual sessions, no-entitlement gate bypass, CAPTCHA
  solving, production monitoring, or commercial-scale use is authorized here.

## Option Comparison

| Option | Verdict | Reason |
| --- | --- | --- |
| `.json` first | Downgraded | Too brittle as the spine under current Reddit access posture; useful only if observed to work in a bounded run and preserved with provenance. |
| Modern Reddit app DOM first | Downgraded | Higher rendering and DOM volatility; can be used when old Reddit is unavailable, but should not be the default planning surface. |
| Old Reddit HTML via CloakBrowser | Primary | Best fit for the owner's selected backend, pre-commercial low-volume posture, and parser-stable extraction. |
| Archive-first | Fallback / complement | Useful for historical posture and unavailable live pages, but archive bodies may be missing, incomplete, or cutoff-mismatched. |
| Official Reddit commercial / enterprise API | Future commercial route | Correct route once the project becomes commercial or client-funded; not the current personal-project default. |

## Capture Unit Boundary

A Reddit capture unit must name its bounded source set before any acquisition
run is scoped.

Allowed boundary shapes:

- a named subreddit plus explicit topical or temporal cutoff;
- a thematic query or research theme with named inclusion/exclusion limits;
- a thread family, such as related submissions around one event, product, or
  claim;
- a small monitored thread set with named cadence and stop date;
- a fixed historical thread list supplied by the operator.

Required capture-unit fields:

- `capture_unit_id`;
- purpose / research question;
- source-set boundary;
- subreddit, theme, query, thread family, or monitored-thread list;
- time cutoff and local cutoff timezone;
- expected volume ceiling;
- monitoring cadence, if any;
- exclusions;
- selected method order;
- explicit non-commercial / personal-project posture;
- hard-stop acknowledgement.

Forbidden capture-unit shapes:

- site-wide Reddit crawling;
- generic subreddit harvesting without a topical or temporal bound;
- indefinite production monitoring;
- adaptive expansion from links, users, comments, or recommendations without a
  separately named bound;
- capture intended to defeat a no-entitlement gate, private/admin surface, or
  credential requirement.

## Capture Flow

1. Commission a capture unit with the required boundary fields.
2. Fetch old Reddit HTML through the future CloakBrowser adapter once
   implemented, using only the named source set and low-volume posture.
3. Preserve raw HTML, visible text/body-equivalent, locator, capture time,
   access posture, cutoff posture, and warnings in a Source Capture Packet
   before parsing.
4. Parse the preserved HTML with BeautifulSoup-style parsing into a derivative
   extraction draft.
5. Consolidate extraction drafts into a planning dataset or state artifact that
   points back to packets and raw preserved files.
6. Add archive capture when live capture is unnecessary, unavailable, or useful
   for historical posture.
7. Use `.json` only as an opportunistic fallback when a bounded run actually
   observes it working; record it as method provenance.
8. Before any Judgment or client-facing use, perform a separate materiality
   gate: reacquire, verify, or carry limitations rather than upgrading this
   planning capture into proof.

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
| `surface` | `old_reddit_html`, `archive_html`, `modern_reddit_html`, or `json_fallback`. |
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
| `capture_method` | CloakBrowser, archive adapter, `.json` fallback, or other observed method. |
| `raw_packet_path` | Pointer to the Source Capture Packet. |
| `raw_html_file_id` | Pointer to raw/body-equivalent file inside the packet. |
| `parser_name_version` | Parser identity and version when known. |
| `parse_warning` | Visible extraction limitations. |
| `body_text` | Parsed derivative body text. |
| `visible_score` | Score if visible; otherwise visible hidden/unavailable state. |
| `visible_author` | Author label if visible; otherwise visible deleted/removed/unavailable state. |
| `deleted_removed_posture` | Deleted, removed, collapsed, hidden, or visible state. |
| `archive_posture` | Archive attempted, preserved, unavailable, not attempted, or mismatch state. |
| `limitations` | Human-readable limitation string. |

This is a candidate planning shape, not a final database schema, storage
authorization, or ECR/Cleaning/Judgment design.

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
5. Emit a local CSV or JSONL consolidation artifact only if storage/consolidated
   output is separately authorized.

Stop conditions for any future implementation:

- login, private, admin, paywalled, or no-entitlement surfaces appear;
- CAPTCHA solving, credential stuffing, direct cookie import, or nonconsensual
  session use would be required;
- volume/cadence pressure turns the task into broad crawling or production
  monitoring;
- the run needs persistent storage, dashboard, queue, scheduler, deployment, or
  commercial-scale operation;
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
fixture admission, retention approval, storage authorization, dashboard
authorization, scheduler/deployment authorization, production-runtime
authorization, commercial Reddit authorization, ECR design, Cleaning design,
Judgment design, buyer proof, or rights-to-process sufficiency.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Reddit pre-commercial capture/consolidation now has a durable planning artifact that frames the work as an architectural planning pass: CloakBrowser-first old Reddit HTML capture, packet preservation before BeautifulSoup parsing, provenance-first consolidation, archive fallback, `.json` opportunistic fallback, and explicit non-implementation stop lines."
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - "docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
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
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca-harness/docs/adapter_author_contract.md"
  intentionally_not_updated:
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Boundary permission and hard stops did not change; this artifact plans inside the existing discoverable/entitled plus disclosable boundary."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and forbidden outputs did not change; this artifact applies them to a Reddit planning route."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "CloakBrowser selection, Reddit ordering, `.json` posture, and commercial deferral were already authorized there; this artifact consolidates planning rather than expanding build authority."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Method ordering and parser posture were already updated; this artifact gives the planning thread a durable home."
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: "No runnable command, adapter behavior, or implementation status changed in this planning pass."
    - path: "orca-harness/docs/adapter_author_contract.md"
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
