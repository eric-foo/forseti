# LinkedIn + Reddit Source Capture Armory Concurrent Structure Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture planning artifact
status: LINKEDIN_REDDIT_SOURCE_CAPTURE_ARMORY_CONCURRENT_STRUCTURE_ARCHITECTURE_V0
scope: >
  Non-executing architecture artifact for deciding whether LinkedIn and Reddit
  can be planned concurrently through one Source Capture Armory backbone while
  preserving separate source-family access, privacy, policy, provenance,
  commercial-transition, and hard-stop gates.
use_when:
  - Planning LinkedIn and Reddit as concurrent source-family lanes.
  - Checking whether shared Armory packet, lifecycle, source-quality, and state
    assembler vocabulary can be reused without merging platform risk.
  - Preventing Reddit pre-commercial capture precedent from becoming LinkedIn
    scraping, automation, account-session, or commercial-use authorization.
authority_boundary: planning_only
open_next:
  - orca/product/spines/capture/source_capture_toolbox/README.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
  - orca/product/spines/capture/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
stale_if:
  - LinkedIn policy, API, legal, or commercial-access posture changes.
  - Reddit source-access order, CloakBrowser backend, old Reddit HTML posture,
    `.json` posture, or commercial API/licensing posture changes.
  - Source Capture Armory packet lifecycle, source-quality vocabulary, queue
    vocabulary, or state-assembler boundary changes.
  - Orca creates a Candidate Signal Intake / Corpus Intake contract that gives
    pre-Decision-Frame source-family scouting units a compliant destination.
```

## 1. Status And Boundary

Architecture answer:

`RECOMMEND_SHARED_BACKBONE_WITH_SOURCE_FAMILY_SATELLITES`

This is an architecture-planning artifact only. It does not authorize browser
capture, scraping, login/session work, API calls, account creation, credential
use, storage, schedulers, queues, databases, source cleaning, ECR, Cleaning,
Judgment, buyer proof, commercial deployment, implementation, commits, pushes,
or PRs.

The target architecture is one Source Capture Armory backbone for packet,
lifecycle, provenance, source-quality, queue, and state-assembler vocabulary,
with separate Reddit and LinkedIn source-family satellites. The LinkedIn
satellite starts as official/API/manual/owner-supplied/entitled-only planning,
including Sales Navigator-level manual or entitled POC business-signal research.
Reddit's pre-commercial anti-blocking order does not transfer to LinkedIn.

## 2. Source Readiness And Preflight

`SOURCE_CONTEXT_READY`, with source gaps recorded below.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom LinkedIn + Reddit Source Capture Armory architecture pack
  workspace: C:\Users\vmon7\Desktop\projects\orca
  dirty_state_checked: yes
  dirty_state_summary: >
    Worktree has unrelated modified and untracked files, including modified
    source-capture docs read for this artifact. They support advisory
    repo-visible planning only and do not support validation/readiness claims.
  edit_permission: docs-write for this target architecture artifact only
  output_mode: file-write
  target_scope:
    - orca/product/spines/capture/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md
  implementation_authorized: no
  blocked_if_missing: >
    Required exact prompt-listed sources that were missing are recorded as
    source gaps rather than silently normalized.
```

Method sequence honored: `workflow-deep-thinking` and
`workflow-architecture-planning` were reference-loaded before task source
loading; synthesis occurred after source readiness. The prompt requested three
advisory architecture perspectives. Three subagents supplied directional,
adversarial, and grounding input. Their outputs are advisory only, not verdicts,
not implementation authority, and not readiness proof.

## 3. Source Gaps

Several prompt-listed exact paths were missing. Current repo-routed owner paths
were read where the loaded Data Capture consolidation map or Armory README named
them.

| Missing prompt-listed path | Current repo-routed owner path used |
| --- | --- |
| `docs/product/source_capture_third_tranche_build_authorization_v0.md` | `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` |
| `docs/product/source_capture_method_selection_plan_v0.md` | `docs/product/data_capture_source_access_method_plan_v0.md` |
| `docs/product/source_capture_obligation_contract_v0.md` | `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` |
| `docs/product/source_capture_fixture_retention_and_sensitivity_policy_v0.md` | `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md` |
| `docs/product/source_capture_profile_mini_god_v0.md` | `orca/product/spines/capture/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` |
| `docs/product/source_capture_source_quality_queue_template_v0.md` | `orca/product/spines/capture/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` |
| `docs/product/source_capture_state_assembler_v0.md` | `orca/product/spines/capture/source_capture_toolbox/source_quality_state_assembler_v0.md` |
| `docs/product/source_capture_toolbox/source_capture_runbook_v0.md` | `orca-harness/docs/source_capture_agent_runbook.md` |
| `docs/product/source_capture_toolbox/adapter_contract_v0.md` | `orca-harness/docs/adapter_author_contract.md` |

These gaps do not block the planning recommendation because current owner paths
exist and were located through Orca-owned routing surfaces. They do block any
claim that the prompt-listed exact paths are current or authoritative.

## 4. External LinkedIn Policy Check

Official LinkedIn sources were checked on 2026-06-05. This artifact is not legal
advice and does not claim platform permission.

| Official source | Current architecture relevance |
| --- | --- |
| [LinkedIn User Agreement](https://www.linkedin.com/legal/user-agreement), effective November 3, 2025 | Section 8.2 describes prohibited conduct unless LinkedIn permits it in separate writing, including scraping/copying services including profiles and other data, unauthorized automated access, copying/using/displaying/distributing information without consent, bypassing access controls/use limits, and monetizing LinkedIn services or related data without consent. |
| [LinkedIn Prohibited Software And Extensions](https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions) | LinkedIn states that third-party crawlers, bots, browser plug-ins/extensions, or software that scrape, modify appearance, or automate activity are not permitted. |
| [LinkedIn Automated Activity](https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin?lang=en) | LinkedIn frames automation as member-safety and privacy risk, including exporting or scraping data without consent and possible privacy-law issues. |
| [LinkedIn API Terms](https://www.linkedin.com/legal/l/api-terms-of-use) | LinkedIn API use is program-bound, documentation/limit-bound, privacy/data-processing-bound, and subject to suspension or termination. This supports official/API/partner access as the preferred sanctioned commercial route, not unsanctioned automation. |

Architecture implication: LinkedIn cannot inherit Reddit's pre-commercial
CloakBrowser / anti-blocking / old-HTML / archive-fallback route. For LinkedIn,
automation, browser extension, crawler, bot, scraping, anti-blocking, session,
cookie, or logged-in capture is blocked unless a later owner decision, legal
review, and platform/API/entitlement basis explicitly authorize the exact method
and unit.

## 5. Subagent Receipts

| Lane | Advisory result |
| --- | --- |
| Directional Architect | Recommended one shared Armory backbone with source-family satellites. Key invariant: shared packets, separate permissions. |
| Adversarial Architect | Attacked LinkedIn inclusion and recommended restriction to org-level, official/API/manual/owner-supplied or entitled routes; no LinkedIn member/profile, graph, dossier, session, login, automation, or commercial path without explicit approval. |
| Grounding Integrator | Kept the target artifact in `docs/product/source_capture_toolbox/`; advised recording source gaps, reusing existing queue/lifecycle/result-token/state-assembler vocabulary, and not creating a standalone workflow sub-map yet. |

These perspectives are inputs only. The synthesis below is the owning
architecture recommendation.

## 6. Real Architecture Question

The question is not whether Orca should "scrape social sites." That framing is
too sloppy and would cause the wrong decision.

The real architecture question is:

```text
Can Reddit and LinkedIn share one Source Capture Armory backbone for packet,
lifecycle, provenance, source-quality, queue, and state-assembler behavior
while each platform keeps a separate source-family satellite for access basis,
policy posture, personal-data sensitivity, capture-unit taxonomy, method order,
retention, and commercial transition?
```

Answer: yes, but only if the shared backbone is a vocabulary and packet
discipline, not a shared permission model.

## 7. Current State

Reddit already has a bounded pre-commercial planning route:

- CloakBrowser anti-blocking first once implemented;
- old Reddit HTML preferred where available;
- low-volume bounded capture over subreddit, theme, query, thread-family, or
  small monitored-thread units;
- archive capture where live capture is unnecessary or fails visibly;
- `.json` opportunistic fallback only;
- packet before parser;
- parser output derivative only;
- Decision-Frame-bound versus candidate/scouting classification;
- no broad crawling, source-discovery expansion, storage, scheduler, dashboard,
  production runtime, ECR, Cleaning, Judgment, or commercial Reddit authority;
- commercial/client-funded/durable buyer use reroutes to sanctioned Reddit API
  or data licensing.

LinkedIn has no equivalent Orca planning route. It has current official policy
constraints that make a Reddit-style automated path indefensible as a default.
LinkedIn may still be useful as a professional, organization, hiring, market,
narrative, and institutional signal source, but only through a stricter
source-family satellite.

Owner clarification recorded 2026-06-05: the intended LinkedIn use is not
commercial deployment and not scraping. It is proof-of-concept business-signal
research for B2B understanding, with Sales Navigator already available as the
practical bar. In that POC posture, LinkedIn may be used manually or through
entitled first-party product surfaces to observe companies, roles, jobs,
business topics, organization pages, and member-authored business posts. The
target object is the business signal, not the person. Orca should avoid
retaining member profiles, contact lists, connection graphs, employment-history
datasets, lead lists, or person dossiers.

Owner decision recorded 2026-06-08: the owner accepts small supervised
LinkedIn browser-assist as green inside the LinkedIn Lane only when tagged
`optional_poc_risk_mode`. This means personal / pre-commercial Orca POC work
with owner-accepted ToS, account, reputation, and platform-enforcement risk,
not LinkedIn-sanctioned or commercial-safe access. The mode requires low
volume, visible human supervision, a declared run envelope, visible provenance,
no background runs, no session-cookie extraction, no bulk export, no contact
harvesting, no follower/connection/commenter list retention, no profile body
harvesting, no hidden credential handling, no personal dataset, and immediate
stop on friction, lockout, policy concern, or person-data drift. Lead
harvesting and contact acquisition are deferred to a separate future Outreach
Lane.

## 8. Option Comparison

| Option | Verdict | Reason |
| --- | --- | --- |
| Shared backbone with source-family satellites | Recommended | Reuses Armory packet/lifecycle/source-quality vocabulary without merging platform permission or privacy posture. |
| Separate armories | Rejected for now | Would duplicate packet and lifecycle vocabulary and create drift without improving LinkedIn safety if method gates are explicit. |
| Reddit first, LinkedIn deferred | Downgraded | Useful if owner wants zero LinkedIn risk, but concurrent architecture is safe when LinkedIn is restricted to a policy-first satellite. |
| LinkedIn official/API/manual-only lane | Adopted inside the recommended satellite | This is the correct initial LinkedIn method posture, but it does not require a separate armory. |
| No LinkedIn until owner risk decision | Contingency | Use this if the owner refuses the LinkedIn restrictions or wants member/profile/automation surfaces without a separate legal/platform/API decision. |

## 9. Recommendation

Use a shared Source Capture Armory backbone with two source-family satellites:

1. **Backbone:** one packet, lifecycle, provenance, source-quality, queue, and
   state-assembler contract.
2. **Reddit satellite:** current pre-commercial Reddit route preserved as
   source-specific.
3. **LinkedIn satellite:** official/API/manual/owner-supplied/entitled-only by
   default, with Sales Navigator/manual POC business-signal research allowed as
   an entitled first-party surface. Small supervised browser-assist sessions are
   accepted as `optional_poc_risk_mode` for personal / pre-commercial Orca POC
   only, with strict run-envelope, supervision, minimization, and stop-condition
   guardrails. Session-cookie extraction, contact harvesting, profile body
   harvesting, follower/connection/commenter graph capture, lead-list, and
   person-dossier surfaces remain non-default or blocked.

Decisive invariant:

```text
Shared packets. Separate permissions.
```

## 10. Shared Armory Backbone

The shared backbone may own these primitives for both Reddit and LinkedIn:

| Shared primitive | Backbone rule |
| --- | --- |
| Source Capture Packet (CapturePacket) | Canonical capture and provenance container before parser, source-quality, or state assembly. |
| Packet lifecycle | Reuse `scratch`, `candidate_evidence`, `recommended_fixture_admission`, `separately_admitted`; default `scratch`. |
| Provenance | Record method, access surface, policy/access basis, operator/session posture, capture time, source time, cutoff, archive/history, packet/raw pointers, hash, warnings, and limitations. |
| Parser boundary | Parser output is derivative and never canonical source body. |
| Source-quality queue | Reuse `planned`, `ready_for_tool_run`, `blocked_missing_input`, `packet_written_needs_report`, `reported`. |
| Mini God-Tier result tokens | Reuse the existing result-token set; do not create platform-local success tokens. |
| State assembler | Census/router only; not verdict, not conductor, not runner dispatch, not source-quality scoring, not fixture admission. |
| Intake classification | Every unit is `decision_frame_bound` or `candidate_or_scouting`; only the former may claim Data Capture handoff posture. |
| Non-promotion ladder | Planning, packet, parser, consolidation, source-quality, batch, fixture admission, ECR/Cleaning/Judgment, and buyer proof are separate tiers. |

## 11. Source-Family Satellite Model

These fields must remain source-family specific:

| Field | Reddit | LinkedIn |
| --- | --- | --- |
| `source_family` | `reddit` | `linkedin` |
| `platform_policy_basis` | Current Reddit pre-commercial route plus commercial reroute. | Current official LinkedIn policy/API terms check; automation/scraping restricted. |
| `access_surface` | old Reddit HTML, modern Reddit HTML, archive HTML, official/API, `.json` fallback. | Sales Navigator/manual entitled UI, official API/partner/export, owner-supplied data, manual notes, company/org/job/event/school/public-post pages, and member-authored business posts where the retained object is the business signal. |
| `account_session_required` | Non-default and contamination-sensitive; credentials/secrets never enter packets. | Default blocked for capture; any logged-in/session/account route requires separate owner/legal/platform decision. |
| `public_or_entitled_basis` | Public/discoverable, account-created, archive, sanctioned API/licensing, or observed fallback. | Official/API, owner-supplied, entitled/client-provided, or manual source-note basis; public visibility alone is not capture authority. |
| `capture_unit_type` | subreddit/theme/query/thread-family/small monitored thread/fixed thread list. | company/org page, job post, company post, event/school page, Sales Navigator manual business-signal note, owner export, official API record, manual note; member-profile/graph/person-dataset units non-default or blocked. |
| `personal_data_sensitivity` | Public handles, user-authored posts, screenshots, raw third-party bodies require sensitivity notes. | Higher default sensitivity for names, titles, roles, employment history, profile-derived material, commenters, followers, and graph edges; minimize or avoid retaining person fields when the signal is business-level. |
| `method_order` | CloakBrowser once implemented, old Reddit HTML, low-volume bounded capture, archive, `.json` opportunistic fallback. | Official/API/partner, owner-supplied/export, manual analyst note, entitled data; supervised browser-assist only when tagged `optional_poc_risk_mode`. |
| `anti_blocking_authorization_basis` | Source-specific pre-commercial owner decision. | Optional POC-risk mode for supervised personal/pre-commercial Orca work only; not LinkedIn-sanctioned or commercial-safe. |
| `commercial_transition_required` | Client-funded/commercial/durable buyer use reroutes to sanctioned Reddit API/licensing. | Commercial/client-funded use requires LinkedIn API/partner/licensing/legal/platform review before reliance. |
| `retention_class` | Existing packet retention/sensitivity decision plus Reddit-specific sensitivity note. | Existing packet retention/sensitivity decision plus stricter person-data and rights/consent note. |
| `decision_frame_binding` | Mandatory for Data Capture handoff. | Mandatory for Data Capture handoff; candidate/scouting LinkedIn has no default Data Capture destination. |

## 12. Reddit Lane

Reddit keeps the current planning route and does not need a new source-family
permission model in this pass.

| Reddit capture unit | Planning status |
| --- | --- |
| Named subreddit plus topical/time bound | Allowed for planning. |
| Thematic/query-bound thread set | Allowed for planning. |
| Thread family around one event, claim, product, or market signal | Allowed for planning. |
| Small monitored thread set | Allowed only with cadence, stop date, volume ceiling, and no production monitoring. |
| Fixed operator-supplied thread list | Allowed for planning. |
| Generic subreddit harvesting | Out of scope. |
| Site-wide walking, link/user/comment/recommendation expansion | Out of scope. |
| Commercial/client-funded Reddit capture | Stop and reroute to sanctioned commercial/API/licensing path. |

Reddit success cannot silently promote across tiers. A packet, parser row,
source-quality token, or state-assembler census is not validation, readiness,
fixture admission, ECR, Cleaning, Judgment, buyer proof, or commercial authority.

## 13. LinkedIn Lane

LinkedIn is valuable enough to plan concurrently, but not valuable enough to
pretend the Reddit method order applies. The LinkedIn satellite begins with the
following method posture for personal proof-of-concept work:

1. official API, partner, or sanctioned export route;
2. Sales Navigator or another first-party entitled UI used manually for
   business-signal research;
3. owner-supplied, client-provided, or otherwise entitled dataset;
4. manual analyst research note with source link and provenance;
5. organization, job, company-post, event, school, and member-authored
   business-post notes where the retained object is the business signal rather
   than a member profile or person record;
6. small supervised browser-assist sessions when tagged
   `optional_poc_risk_mode`, with human oversight, low volume, visible
   provenance, no session-cookie tooling, no bulk export, no contact
   harvesting, no profile body harvesting, no follower/connection/commenter
   list retention, no personal dataset, and visible stop conditions.
   Anti-detect/cloaked browser behavior, residential/rotating proxies, and
   in-browser JS-challenge handling may be used only to reach discoverable or
   entitled LinkedIn surfaces, only because Orca's source-access doctrine already
   permits them as a disclosable pre-commercial risk posture, not because
   LinkedIn or Sales Navigator sanctions them; no-entitlement gate bypass to
   reach non-entitled data remains a hard stop;
7. public web automation, anti-blocking, browser extension, bot/crawler,
   session-cookie extraction, bulk export, or member-profile capture remains
   unresolved and blocked by default.

LinkedIn capture-unit classification:

| LinkedIn unit type | Classification |
| --- | --- |
| Official API / partner-access record | Allowed for planning if API/program eligibility, documentation limits, privacy/data-processing obligations, and commercial terms are satisfied. |
| Sales Navigator manual business-signal note | Allowed for POC planning when used as a first-party entitled UI, without automated extraction, session-cookie tooling, profile harvesting, or lead-list export. |
| Supervised low-volume browser-assist business-signal note | Allowed optional POC-risk mode for personal/pre-commercial Orca work only; requires live human supervision, visible provenance, low volume, declared run envelope, no session-cookie extraction, no bulk export, no contact harvesting, no profile body harvesting, no follower/connection/commenter list retention, and no personal dataset. Anti-detect/proxy/JS-challenge handling may be used only under the already accepted Orca pre-commercial risk posture. |
| Owner-supplied export or entitled dataset | Allowed for planning with provenance, entitlement basis, retention, sensitivity, and allowed-use notes. |
| Manual research note with source link | Preferred low-risk planning unit; still needs sensitivity and commercial-use boundaries. |
| Company or organization page snapshot/note | Allowed for planning only through official/API/manual/entitled or separately approved method. |
| Public job posting | Allowed for planning only through official/API/manual/entitled or separately approved method; person names and role details carry sensitivity notes. |
| Public company post, event page, school/institution page | Allowed for planning only through official/API/manual/entitled or separately approved method. |
| Member-authored business post or public industry/topic post | Allowed for POC planning as a business-signal note when captured manually/entitled, with person-data minimization and no profile/person dataset construction. |
| Member profile pages | Non-default; requires explicit owner/legal/platform/API decision and strict no-dossier handling. |
| Connection graphs, follower graphs, inferred employment histories | Out of default scope. |
| Recruiter lead lists, person-level dossiers, identity enrichment | Out of scope. |
| Messages, private/account areas, nonconsensual sessions, stolen cookies/credentials, no-entitlement bypass | Hard stop. |

## 14. Data Capture Spine Handoff Boundary

Every Reddit or LinkedIn unit must be classified before any Data Capture handoff
claim:

| Classification | Meaning | Handoff status |
| --- | --- | --- |
| `decision_frame_bound` | The unit is bound to a specific commissioned question / Decision Frame. | May claim Data Capture handoff posture if all other gates pass. |
| `candidate_or_scouting` | The unit is pre-decision discovery, source-quality reconnaissance, market scanning, or method research. | No compliant Data Capture handoff destination by default; planning-only unless a separate Candidate Signal Intake / Corpus Intake contract exists or the unit is recaptured under a Decision Frame. |
| `method_research` | The work is evaluating access route, policy basis, or source-family constraints. | Planning-only; no packet/source-quality/commercial claim. |
| `out_of_scope_or_blocked` | A hard stop, missing authority, or forbidden unit shape applies. | Stop; no capture, packet, handoff, or persistence claim. |

## 15. Armory Sub-Map Recommendation

Do not create a standalone Source Capture source-family sub-map yet.

The smallest complete move is this architecture artifact plus a source-family
section/table inside it. The existing Data Capture consolidation map already
orients Source Capture Armory and current Reddit routing. A separate
`docs/workflows/` source-family sub-map becomes justified only if future owner
decisions add enough source families or durable routing changes that the Data
Capture consolidation map becomes too dense or stale.

Minimum future sub-map shape, if later authorized:

- Armory backbone;
- source-family lanes;
- source-specific hard stops;
- capture-unit taxonomies;
- method-order status;
- success signal gates;
- current prompt/artifact lineage;
- open owner decisions.

## 16. Success Signal Table

| Signal | Pass meaning | Failure / stop meaning |
| --- | --- | --- |
| `shared_armory_backbone_pass` | Both lanes reuse packet, lifecycle, provenance, queue, source-quality, and state-assembler vocabulary without creating platform-local tokens. | Any lane invents `done`, `passed`, `validated`, platform-local result tokens, lifecycle states, or verdict vocabulary. |
| `source_family_satellite_split_pass` | Reddit and LinkedIn each retain separate access basis, policy posture, method order, privacy class, capture taxonomy, and commercial transition. | LinkedIn inherits Reddit anti-blocking or Reddit inherits LinkedIn policy assumptions. |
| `linkedin_policy_current_check_pass` | Current official LinkedIn User Agreement, Help/Safety content, and API terms were checked with dates and links. | LinkedIn branch relies on memory, prompt summary, or generic public-data assumptions. |
| `linkedin_official_manual_default_pass` | LinkedIn starts official/API/manual/owner-supplied/entitled by default, including Sales Navigator manual POC business-signal research. | LinkedIn automated web capture, anti-blocking, bots, crawlers, extensions, session-cookie extraction, bulk export, or logged-in scraping are treated as default. |
| `supervised_browser_assist_not_baseline_pass` | Any small automated browsing session is tagged `optional_poc_risk_mode`, supervised by a human, low-volume, provenance-visible, and non-extractive. Anti-blocking, if used, is justified only by Orca's accepted pre-commercial risk posture. | Supervised automation is treated as equivalent to manual browsing, used as a generic LinkedIn capture route, or treated as platform-sanctioned. |
| `linkedin_member_data_sensitivity_pass` | Member/profile/person-level material is high-risk and non-default. | Profiles, titles tied to named people, employment histories, graph edges, or lead lists become ordinary capture units. |
| `business_signal_not_person_record_pass` | Member-authored posts may be used as business-signal notes when the retained object is the business claim/topic/company signal, not the author as a lead/person record. | LinkedIn "company intelligence" quietly becomes person-level dossier construction. |
| `no_person_dossier_pass` | Profile harvesting, graph capture, recruiter lead lists, identity enrichment, and inferred employment-history dossiers are blocked by default. | POC research turns into contact harvesting or a reusable person dataset. |
| `account_session_disclosability_pass` | Any account, cookie, credential, storage-state, session, logged-in, or profile-dependent route is blocked or escalated to owner/legal/platform review. | Successful account/session access is treated as evidence of permission. |
| `bounded_source_unit_pass` | Every unit names source family, unit type, purpose, locator/provenance, cutoff, volume/cadence where relevant, and exclusions. | URL-unbounded crawling, site-wide walking, broad profile/search harvesting, or adaptive expansion appears. |
| `decision_frame_or_candidate_intake_classified` | Every unit is `decision_frame_bound`, `candidate_or_scouting`, `method_research`, or `out_of_scope_or_blocked`. | Candidate/scouting material claims Data Capture handoff posture by implication. |
| `method_provenance_recorded` | Method, access surface, policy/access basis, date, operator decision, packet pointer, and limitations are visible. | Method is hidden, generalized as "public web", or separated from policy basis. |
| `packet_before_parser_pass` | Raw/body-equivalent material is packeted before parser/consolidation/source-quality reliance. | Parser text, note text, or screen-extracted body becomes canonical without packet provenance. |
| `source_quality_compatibility_pass` | Rows use existing queue statuses, Mini God-Tier tokens, lifecycle states, and state-assembler census rules. | Source-quality row becomes score, validation, admission, readiness, or platform-local status. |
| `commercial_transition_check` | Reddit commercial use reroutes to sanctioned API/licensing; LinkedIn commercial use requires API/partner/licensing/legal/platform review before reliance. | Pre-commercial capture becomes buyer-facing, client-funded, productized, or resold evidence without transition. |
| `planning_only_pass` | Output cannot be read as permission to scrape, automate, store, schedule, commercialize, or build. | Architecture wording becomes an execution, capture, storage, implementation, or deployment route. |
| `owner_decision_visibility_pass` | Legal, policy, method, personal-data, retention, and commercial uncertainties are named as owner decisions. | The artifact resolves policy/legal/platform permission questions by implication. |

## 17. Hard Stops And Non-Defaults

Hard stops:

- stolen credentials, stolen cookies, nonconsensual sessions, credential
  stuffing, malware, security exploits, no-entitlement gate bypass, or methods
  Orca would refuse to disclose internally;
- obvious cross-account, private, admin, confidential, message, or personal
  account spillover once noticed;
- LinkedIn member-profile body harvesting, follower/connection/commenter graph
  capture, lead-list creation, contact harvesting, identity enrichment,
  inferred employment-history dossiers, message capture, session-cookie
  extraction, or automated logged-in capture outside `optional_poc_risk_mode`;
- LinkedIn anti-blocking, crawler, bot, browser extension, or automated capture
  by inheritance from Reddit;
- unsupervised LinkedIn automation, background runs, account/session tooling,
  session-cookie extraction, bulk export, or any automated path that continues
  after friction, lockout, policy concern, or person-data drift appears;
- broad crawling, site-wide walking, adaptive expansion, production monitoring,
  storage, dashboard, scheduler, queue, database, deployment, or production
  runtime;
- ECR, Cleaning, Judgment, buyer proof, fixture admission, source-quality
  scoring, validation, readiness, or commercial evidence claims.

Non-defaults requiring explicit owner decision:

- any LinkedIn member/profile/person-level dataset or reusable person-record
  unit;
- any LinkedIn automated public-web capture;
- any LinkedIn session-cookie, browser-profile, bulk-export, or automation route;
- any small supervised LinkedIn browser-assist run without the
  `optional_poc_risk_mode` tag, declared run envelope, supervision,
  minimization, and stop-condition receipt;
- any LinkedIn commercial/client-funded/customer-facing/productized use;
- any durable retention of LinkedIn material with personal names, employment
  history, roles, profile URLs, comments, followers, or graph relationships.

## 18. Open Owner Decisions

1. Is LinkedIn initially limited to Sales Navigator/manual entitled POC
   business-signal research, company, job, organization, event, school,
   official/API, owner-supplied/export, and manual-note surfaces?
2. Are LinkedIn member profile pages off-limits by default?
3. Are names, titles tied to named people, employment histories, commenters,
   followers, and connection edges categorically excluded as retained datasets,
   or allowed only as incidental provenance/minimized context under a separate
   person-data decision?
4. Must every later LinkedIn commercial or client-funded use route through API/partner/
   licensing/legal/platform review before any product proof claim?
5. Should LinkedIn remain candidate/scouting only until Orca creates a Candidate
   Signal Intake / Corpus Intake contract?
6. Closed 2026-06-08 for personal / pre-commercial Orca POC: supervised
   browser-assist is acceptable only as `optional_poc_risk_mode`, not as a
   generic LinkedIn capture route, platform-sanctioned method, commercial path,
   or background automation.
7. Closed 2026-06-08 for current POC posture: the hard limits are low volume,
   live supervision, declared run envelope, visible provenance, no background
   runs, no session-cookie extraction, no bulk export, no contact harvesting,
   no profile body harvesting, no follower/connection/commenter list retention,
   no personal dataset, and immediate stop on friction, lockout, policy
   concern, or person-data drift.
8. What retention class applies to LinkedIn material containing personal names,
   role information, employment history, profile URLs, comments, followers, or
   screenshots?
9. Should a Source Capture source-family sub-map be created later, after this
   architecture is accepted and at least one additional source-family decision
   exists?

## 19. Non-Claims

This artifact is not:

- legal advice;
- platform permission;
- a scraping authorization;
- a bypass authorization;
- a credential, cookie, account-session, storage-state, or browser-profile
  authorization;
- a general LinkedIn automation authorization;
- a personal-data processing authorization;
- a storage, scheduler, database, dashboard, queue, deployment, or production
  pipeline design;
- a Data Cleaning, ECR, Judgment Spine, buyer-proof, or commercial evidence
  design;
- a claim that LinkedIn and Reddit have equivalent access posture;
- a claim that public visibility alone is sufficient capture authority;
- validation, readiness, source completeness proof, fixture admission,
  source-quality scoring, or commercial-readiness evidence.

## Direction Change Propagation - LinkedIn Lane Optional POC Risk Mode

```yaml
direction_change_propagation:
  doctrine_changed: "The owner accepted supervised LinkedIn browser-assist as green inside the LinkedIn Lane only when tagged optional_poc_risk_mode for personal/pre-commercial Orca POC work, while keeping contact acquisition, lead harvesting, profile body harvesting, follower/connection/commenter graph capture, and commercial use out of this lane."
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - "docs/product/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md"
    - "orca/product/spines/capture/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
  intentionally_not_updated:
    - path: "orca/product/spines/capture/source_capture_toolbox/README.md"
      reason: "The LinkedIn Lane is upstream of Source Capture Armory and does not emit Source Capture Packets."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "The general source-access boundary and hard stops did not change."
  stale_language_search: "rg -n \"optional_poc_risk_mode|POC-risk|browser-assist|separate owner decision|contact harvesting|lead-list|follower/connection\" docs/product/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md orca/product/spines/capture/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not legal sufficiency"
    - "not live LinkedIn authorization"
    - "not Outreach Lane authorization"
    - "not commercial authorization"
```

## 20. Doctrine Change Check

No direction-change propagation is required for this file-write. This artifact
creates a bounded planning recommendation and does not amend the Source Capture
Armory README, Data Capture consolidation map, source-access boundary, method
plan, build authorization, obligation contract, packet retention decision,
Mini God-Tier profile, queue template, state assembler, runbook, adapter
contract, or overlay.

If the owner later accepts this architecture as doctrine or asks to update live
routing surfaces, check at minimum:

- `orca/product/spines/capture/source_capture_toolbox/README.md`;
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`;
- `docs/workflows/orca_repo_map_v0.md`;
- `.agents/workflow-overlay/source-loading.md`;
- `.agents/workflow-overlay/source-of-truth.md`;
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`;
- `docs/product/data_capture_source_access_method_plan_v0.md`;
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`;
- `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`;
- `orca/product/spines/capture/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`;
- `orca/product/spines/capture/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md`;
- `orca/product/spines/capture/source_capture_toolbox/source_quality_state_assembler_v0.md`;
- `orca-harness/docs/source_capture_agent_runbook.md`;
- `orca-harness/docs/adapter_author_contract.md`.

## 21. Next Authorized Step

Smallest complete next step: owner review of this architecture recommendation.

If accepted, the next artifact should be a narrow owner decision or patch prompt
that answers the LinkedIn open owner decisions above and, only then, updates the
Armory README or Data Capture consolidation map if durable routing doctrine is
intended to change.

No runtime, implementation, LinkedIn access, Reddit access, API call, browser
automation, scraping, storage, source-quality pass, fixture admission, ECR,
Cleaning, Judgment, commercial work, commit, push, or PR is authorized by this
architecture artifact.
