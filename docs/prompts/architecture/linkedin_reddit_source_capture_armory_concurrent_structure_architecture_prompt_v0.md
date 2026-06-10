---
retrieval_header_version: 1
artifact_role: full_prompt_artifact
status: PROMPT_V0
scope: >
  Non-executing Chief Architect prompt for deliberating whether and how LinkedIn
  should be planned concurrently with Reddit inside the Source Capture Armory and
  Data Capture Spine. The prompt designs structure, success signals, and owner
  decisions only. It does not authorize scraping, browser automation, account
  use, storage, scheduling, or runtime capture.
use_when:
  - Deliberating LinkedIn and Reddit as concurrent source-family lanes.
  - Deciding shared Armory backbone versus separate source-specific satellites.
  - Preventing Reddit capture precedent from leaking into LinkedIn without a
    separate policy, privacy, account/session, and commercial-use decision.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/README.md
  - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - docs/prompts/architecture/reddit_precommercial_capture_consolidation_success_signal_architecture_prompt_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/product/data_capture_source_access_boundary_decision_v0.md
stale_if:
  - LinkedIn policy, API, legal, or commercial-access posture changes.
  - Reddit method-order, CloakBrowser, or archive-capture doctrine changes.
  - Orca source-access, safety, or downstream propagation doctrine changes.
  - Source Capture Armory lifecycle, packet, source-quality, or state-assembler
    doctrine changes.
---

# LinkedIn + Reddit Source Capture Armory Concurrent Structure Architecture Prompt v0

## Prompt Status

This is a planning-only Chief Architect prompt.

Default output mode: write a durable architecture artifact unless the receiving
operator explicitly chooses chat-only deliberation.

Default target artifact:

`docs/product/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md`

The receiving CA must not execute browser capture, scraping, login/session
activity, API calls, storage work, scheduler work, database work, source cleaning,
or Judgment Spine integration.

## Commission

Deliberate whether LinkedIn should be planned concurrently with Reddit for the
Source Capture Armory and Data Capture Spine, and design the smallest complete
structure that lets both be reasoned about without collapsing their risks into a
single generic "social scraping" lane.

The owner hypothesis is:

- Reddit remains a high-value public/community discussion source, with a
  pre-commercial path ordered around anti-blocking browser capture first,
  low-volume bounded capture second, and archive capture third.
- LinkedIn may also be a high-value professional, company, hiring, market,
  narrative, and institutional signal source.
- Concurrent planning is probably useful, but LinkedIn must not inherit Reddit's
  method order, consent assumptions, personal-data posture, or commercial
  transition path without a separate explicit decision.

Your architecture question:

> Can Reddit and LinkedIn share the same Source Capture Armory backbone while
> retaining separate source-family lanes with distinct access, privacy, policy,
> provenance, and commercial-transition gates?

## Required Answer

Answer with one of:

- `RECOMMEND_SHARED_BACKBONE_WITH_SOURCE_FAMILY_SATELLITES`
- `RECOMMEND_SEPARATE_ARMORIES`
- `RECOMMEND_REDDIT_FIRST_LINKEDIN_DEFERRED`
- `RECOMMEND_LINKEDIN_OFFICIAL_OR_MANUAL_ONLY`
- `RECOMMEND_NO_LINKEDIN_UNTIL_OWNER_RISK_DECISION`

Then provide the structure, success signals, owner decisions, and non-claims
needed to make the recommendation durable.

## Hard Boundaries

This pass is architectural only.

Do not:

- Run live Reddit or LinkedIn capture.
- Use credentials, cookies, browser profiles, account sessions, or logged-in
  access.
- Install, configure, or invoke CloakBrowser, Patchright, Playwright, scraping
  libraries, proxies, API clients, schedulers, queues, databases, or workers.
- Design broad crawling, URL-unbounded capture, follower-graph harvesting,
  connection-graph capture, personal dossiers, or identity enrichment.
- Treat publicly visible information as automatically safe to capture, store,
  process, or commercialize.
- Treat Reddit's pre-commercial method order as LinkedIn authorization.
- Promote candidate/scouting material into Data Capture without a Decision Frame
  or equivalent commissioned question.
- Design ECR, source cleaning, Judgment Spine, buyer proof, client evidence, or
  commercial deployment.

If any requested structure depends on legal review, source owner approval,
platform permission, API access, or a new implementation authorization, mark it
as an open owner decision rather than resolving it inside this pass.

## Current External Policy Check Required

Before finalizing the LinkedIn branch of the architecture, verify current
official LinkedIn sources. Do not rely on memory or on this prompt's summary.

Minimum official-source checks:

- LinkedIn User Agreement: `https://www.linkedin.com/legal/user-agreement`
- LinkedIn Help or Safety content on prohibited software, bots, browser
  extensions, scraping, automated activity, or profile-data copying.
- LinkedIn API, data, or service terms if the architecture discusses sanctioned
  commercial access.

Observed policy context during prompt authoring on 2026-06-05:

- Official LinkedIn policy surfaces describe restrictions on third-party
  software, bots, crawlers, browser extensions, automated activity, scraping,
  copying profiles, and similar data-extraction behavior.
- Treat this as a routing caution only. The receiving CA must verify current
  official text and should not treat this prompt as legal advice or platform
  permission.

## Required Local Source Load

Load these sources before deliberating:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/product/source_capture_toolbox/README.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`
- `docs/prompts/architecture/reddit_precommercial_capture_consolidation_success_signal_architecture_prompt_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/source_capture_third_tranche_build_authorization_v0.md`
- `docs/product/source_capture_method_selection_plan_v0.md`
- `docs/product/source_capture_obligation_contract_v0.md`
- `docs/product/source_capture_fixture_retention_and_sensitivity_policy_v0.md`
- `docs/product/source_capture_profile_mini_god_v0.md`
- `docs/product/source_capture_source_quality_queue_template_v0.md`
- `docs/product/source_capture_state_assembler_v0.md`
- `docs/product/source_capture_toolbox/source_capture_runbook_v0.md`, if present.
- `docs/product/source_capture_toolbox/adapter_contract_v0.md`, if present.

If any listed local source is missing, record it in the output as a source gap.
Do not substitute JB or other repository doctrine.

## Workflow Instruction

Reference-load and apply:

- `workflow-deep-thinking`
- `workflow-architecture-planning`

Use standard 3 advisory architecture subagents when available. They are advisory
only; the CA owns the final synthesis.

### Subagent 1 - Directional Architect

Argue the strongest architecture for concurrent LinkedIn and Reddit planning.

Focus:

- Shared Armory backbone.
- Source-family satellite split.
- Capture packet shape.
- Lifecycle stage compatibility.
- Source-quality queue compatibility.
- Candidate/scouting versus Decision Frame handoff boundary.
- How LinkedIn signal types differ from Reddit signal types.

Expected output:

- Recommended shared primitives.
- Recommended separate source-family fields.
- Capture-unit taxonomy for Reddit and LinkedIn.
- The smallest complete structure that allows concurrent planning without
  runtime execution.

### Subagent 2 - Adversarial Architect

Attack the LinkedIn inclusion case.

Focus:

- Member/profile data sensitivity.
- Personal dossier risk.
- Account/session and login-bound access risk.
- Platform policy and anti-abuse posture.
- Browser automation and anti-blocking ambiguity.
- Commercialization risk.
- Fake success signals caused by volume, broad crawling, or low-quality capture.
- Reddit precedent leakage into LinkedIn.

Expected output:

- Hard stops.
- Failure modes.
- Owner decisions that must be explicit.
- Reasons to defer LinkedIn or restrict it to official/manual/entitled routes.

### Subagent 3 - Grounding Integrator

Map the recommendation into Orca's existing product and workflow structure.

Focus:

- Exact target artifact boundaries.
- Existing vocabulary to reuse.
- Whether the Source Capture Armory needs a source-family sub-map.
- Whether this belongs under the Data Capture Spine consolidation map.
- Required propagation surfaces if the recommendation changes doctrine.
- Non-implementation closeout.

Expected output:

- Repo-native document structure.
- Success signal table.
- Downstream propagation list.
- Open owner questions.
- Smallest complete next artifact or prompt, if any.

## Architecture Issues To Resolve

### 1. Shared Backbone Versus Separate Armories

Decide whether Reddit and LinkedIn should share:

- Packet schema primitives.
- Method provenance fields.
- Capture-unit classification.
- Source-quality queue fields.
- Lifecycle stage names.
- State assembler handoff shape.
- Data Capture Spine intake posture.

Also decide which fields must be source-family specific.

Likely source-family specific fields include:

- `source_family`
- `platform_policy_basis`
- `access_surface`
- `account_session_required`
- `public_or_entitled_basis`
- `capture_unit_type`
- `personal_data_sensitivity`
- `commercial_transition_required`
- `method_disclosability`
- `anti_blocking_authorization_basis`
- `retention_class`
- `decision_frame_binding`

### 2. LinkedIn Capture-Unit Taxonomy

Do not start from "scrape LinkedIn." Start from bounded capture units.

Possible LinkedIn capture units to evaluate:

- Company or organization page snapshots.
- Public job postings.
- Public company posts.
- Public industry or topic posts.
- Public event pages.
- Public school or institution pages.
- Owner-supplied exports or entitled data.
- Official API or partner-access records.
- Manual research notes with source links and provenance.

High-risk or non-default units:

- Member profile pages.
- Connection graphs.
- Follower graphs.
- Inferred employment histories.
- Recruiter lead lists.
- Message content.
- Logged-in-only surfaces.
- Any capture that could become a person-level dossier.

For each unit type, classify:

- Allowed for planning now.
- Requires owner decision.
- Requires legal/platform/API review.
- Out of scope for this architecture.

### 3. Reddit Versus LinkedIn Method Order

For Reddit, preserve the user's current ordering unless a controlling Orca source
overrides it:

1. Anti-blocking browser first.
2. Low-volume bounded capture second.
3. Archive capture third.

For LinkedIn, do not copy that order automatically.

LinkedIn method order must be separately recommended from the verified policy
and risk posture. Candidate method classes may include:

- Official API, partner, or sanctioned export route.
- Manual capture / analyst research note.
- Owner-supplied or entitled dataset.
- Public web capture only if explicitly permitted by owner decision and policy
  review.
- Anti-blocking browser only if separately authorized and disclosable.

If the CA cannot justify a LinkedIn method order, recommend a LinkedIn planning
lane with method unresolved rather than inventing permission.

### 4. Data Capture Spine Boundary

Classify each source-family item as one of:

- Decision-Frame-bound Data Capture.
- Pre-decision candidate/scouting context.
- Source-quality reconnaissance.
- Method research.
- Out-of-scope or blocked.

Only Decision-Frame-bound units may claim Data Capture handoff posture. Candidate
or scouting material can inform source discovery, but cannot become a standing
corpus by default.

### 5. Armory Sub-Map Decision

Decide whether the Source Capture Armory needs a source-family sub-map analogous
to the Judgment Spine sub-repo map.

If yes, define the map's minimum durable shape:

- Armory backbone.
- Source-family lanes.
- Source-specific hard stops.
- Capture-unit taxonomies.
- Method-order status.
- Success signal gates.
- Current prompt/artifact lineage.
- Open owner decisions.

Do not create the map unless the receiving CA's commission includes writing it.
For this pass, recommending the map is enough unless the operator explicitly
authorizes propagation.

## Success Signal Candidates

The receiving CA must harden, rename, add, or reject these. Do not copy them
blindly into final architecture.

| Signal | Meaning |
| --- | --- |
| `shared_armory_backbone_pass` | Reddit and LinkedIn can reuse packet, lifecycle, source-quality, provenance, and state-assembler primitives without hiding platform-specific obligations. |
| `source_family_satellite_split_pass` | Each platform has its own source-family lane for access basis, policy posture, capture-unit taxonomy, privacy class, method order, and commercial transition. |
| `linkedin_policy_current_check_pass` | Current official LinkedIn policy/API/service sources were checked and summarized with source links and dates. |
| `reddit_policy_current_check_pass` | Current Reddit source-access assumptions were checked or marked as inherited from the prior Reddit planning prompt. |
| `linkedin_member_data_sensitivity_pass` | Member/profile/person-level material is explicitly classified as high-risk and non-default. |
| `no_person_dossier_pass` | The architecture blocks profile harvesting, graph capture, lead-list assembly, and identity enrichment as default capture routes. |
| `account_session_disclosability_pass` | Any account, cookie, session, logged-in, or profile-dependent access is blocked or escalated to owner/legal/platform review. |
| `bounded_source_unit_pass` | Capture is bounded by source-family unit, theme, subreddit, company, post, job, event, or commissioned question rather than URL-unbounded crawling. |
| `decision_frame_or_candidate_intake_classified` | Every unit is classified as Decision-Frame-bound Data Capture or candidate/scouting/source-quality context. |
| `method_provenance_recorded` | The method, access surface, date, policy basis, and operator decision are recorded in the packet. |
| `packet_before_parser_pass` | The architecture prioritizes packet and lifecycle contract before parser implementation. |
| `source_quality_compatibility_pass` | Outputs can feed source-quality queue/state assembler without becoming cleaned or judged data. |
| `commercial_transition_check` | The architecture defines when commercial/API/legal review is triggered before client-funded or commercial use. |
| `planning_only_pass` | The output cannot be read as permission to scrape, automate, store, schedule, or commercialize LinkedIn or Reddit capture. |
| `owner_decision_visibility_pass` | Every unresolved policy, legal, method, or commercial judgment is named as an owner decision rather than hidden in implementation language. |

## Output Artifact Contract

If writing the target architecture artifact, use this structure:

1. Title
2. Retrieval header
3. Status
4. Source readiness and source gaps
5. External policy check with dated official links
6. Subagent receipts
7. Real architecture question
8. Current state
9. Option comparison
10. Recommendation
11. Shared Armory backbone
12. Source-family satellite model
13. Reddit lane
14. LinkedIn lane
15. Data Capture Spine handoff boundary
16. Armory sub-map recommendation
17. Success signal table
18. Hard stops and non-defaults
19. Open owner decisions
20. Non-claims
21. Next authorized step

The output must include:

- A clear recommendation.
- A table comparing Reddit and LinkedIn.
- A table separating shared backbone fields from source-family-specific fields.
- A table classifying LinkedIn capture-unit types.
- A success signal table with pass/fail meaning.
- Explicit non-claims.
- A current-policy verification note for LinkedIn using official sources.

## Option Set To Consider

### Option A - Shared Backbone With Source-Family Satellites

Use one Source Capture Armory backbone for packets, lifecycle, provenance,
source-quality queue, and state-assembler handoff, while Reddit and LinkedIn each
own their own lane for access, method order, privacy, source-unit taxonomy, and
commercial transition.

This is the likely default recommendation if the CA can keep LinkedIn risk
visible.

### Option B - Separate Armories

Create separate Reddit and LinkedIn armories.

Use this only if the shared backbone would blur safety, ownership, vocabulary, or
operational boundaries.

### Option C - Reddit First, LinkedIn Deferred

Continue Reddit planning and defer LinkedIn until the Reddit success-signal
architecture stabilizes.

Use this if concurrent planning creates too much doctrine churn.

### Option D - LinkedIn Official/API/Manual-Only Lane

Allow LinkedIn in the Armory as a planning lane, but restrict it to official,
manual, owner-supplied, or entitled access paths until a later legal/platform
decision.

Use this if LinkedIn is valuable but automated web capture is not currently
defensible.

### Option E - No LinkedIn Until Owner Risk Decision

Block LinkedIn planning until the owner explicitly resolves platform policy,
privacy, commercial-use, and acceptable-source-unit posture.

Use this if the CA cannot keep the architecture from implying unauthorized
access.

## Open Owner Questions

Answer or preserve these explicitly:

- Is LinkedIn initially limited to company, job, organization, event, and public
  post surfaces, or are member/profile surfaces being considered?
- Are personal profile pages off-limits by default?
- Does LinkedIn require a named owner decision separate from the existing
  third-tranche anti-blocking browser authority?
- Is anti-blocking browser capture ever acceptable for LinkedIn, or must
  LinkedIn begin as official/API/manual/entitled only?
- What counts as commercial or client-funded use for LinkedIn-derived material?
- What retention class applies to LinkedIn material that contains person names,
  employment history, or role information?
- Should the Source Capture Armory receive its own source-family sub-map now?
- Should LinkedIn planning wait until the Reddit success-signal architecture is
  adjudicated?

## Non-Claims

The final architecture must explicitly say it is not:

- Legal advice.
- Platform permission.
- A scraping authorization.
- A bypass authorization.
- A credential, cookie, or account-session authorization.
- A personal-data processing authorization.
- A storage, scheduler, database, dashboard, or production pipeline design.
- A Data Cleaning, ECR, Judgment Spine, buyer-proof, or commercial evidence
  design.
- A claim that LinkedIn and Reddit have equivalent access posture.
- A claim that public visibility alone is sufficient capture authority.

## Closeout Requirements

If the output changes Orca product doctrine, architecture doctrine, workflow
authority, validation philosophy, review authority, output authority, or
lifecycle boundaries, apply the Orca direction-change propagation rule.

If the pass only produces a bounded recommendation prompt or planning artifact,
state that no propagation was required and why.

Do not stage, commit, push, create a PR, or launch a new runtime unless the
operator explicitly authorizes that separate action.
