---
retrieval_header_version: 1
artifact_role: full_prompt_artifact
status: PROMPT_V0
scope: >
  Non-executing Chief Architect architecture prompt for designing how Orca should
  expose CloakBrowser to agents as a bounded Source Capture Packet runner rather
  than a freeform browser-control surface. The prompt commissions structure,
  contracts, tests, and runbook implications only; it does not authorize
  implementation, live capture, install, scraping, storage, scheduling, or
  production runtime.
use_when:
  - Planning the CloakBrowser packet runner architecture before implementation.
  - Deciding the boundary between agent intent, runner inputs, cloaked browser
    backend behavior, packet output, parser handoff, and consolidation.
  - Preventing "agent drives CloakBrowser like Computer Use" from becoming the
    Source Capture Spine path.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - docs/product/source_capture_toolbox/README.md
  - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
  - forseti-harness/docs/source_capture_agent_runbook.md
  - forseti-harness/docs/adapter_author_contract.md
stale_if:
  - CloakBrowser selection, availability, API shape, or source-access authority changes.
  - Reddit pre-commercial method order changes.
  - Source Capture Packet schema, writer, lifecycle, or contamination rules change.
  - Agent runbook runner-selection rules change.
  - Orca later authorizes storage, scheduler, queue, production runtime, or broad crawler behavior.
---

# CloakBrowser Packet Runner Architecture Prompt v0

## Prompt Status

This is a planning-only Chief Architect prompt.

Default output mode for the receiving CA: `file-write`.

Default target artifact:

`docs/product/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md`

The receiving CA must not implement the runner, install CloakBrowser, run live
capture, open Reddit, call external sources, configure proxies, create storage,
write parser code, alter packet writer code, stage commits, push, or create a
PR. This pass designs the runner contract and readiness path only.

## Commission

Design how Orca should expose CloakBrowser to agents as a bounded, repeatable
Source Capture Packet runner.

The owner intent is not:

```text
agent manually controls CloakBrowser like Computer Use
```

The owner intent is:

```text
agent supplies a bounded capture unit -> runner invokes CloakBrowser backend ->
runner writes a Source Capture Packet -> agent inspects manifest/receipt/raw ->
parser/consolidation consume preserved packet artifacts
```

The real architecture question:

> What runner contract makes CloakBrowser reliable for Capture Spine use while
> preventing freeform browsing, source discovery, session leakage, packet
> contamination, hidden state, vague success claims, storage drift, parser-body
> promotion, and commercial-scale escalation?

## Required Recommendation

Return one of:

- `RECOMMEND_PACKET_RUNNER_FIRST`
- `RECOMMEND_ADAPTER_CONTRACT_FIRST`
- `RECOMMEND_REDDIT_REFERENCE_RUNNER_FIRST`
- `RECOMMEND_MANUAL_CLOAKBROWSER_ONLY_FOR_NOW`
- `RECOMMEND_BLOCKED_UNTIL_CLOAKBROWSER_API_KNOWN`

Then explain the smallest complete route to a reusable agent-facing runner.

## Hard Boundary

This prompt does not authorize:

- live Reddit, LinkedIn, WSO, or other site capture;
- browser automation execution;
- CloakBrowser install or dependency setup;
- proxy provider setup;
- CAPTCHA-solving service setup;
- credentials, cookies, storage-state, browser profile import, or password automation;
- broad crawling, source discovery, link following, or recommendation walking;
- persistent storage, queue, scheduler, dashboard, deployment, or production runtime;
- ECR, Cleaning, Judgment, buyer proof, source-quality scoring, or fixture admission;
- commercial Reddit or commercial LinkedIn use;
- commits, pushes, PRs, or staging.

If the architecture needs any of those, name it as a later owner decision or
implementation authorization, not as part of this pass.

## Required Source Sequence

Use the Orca source-gated method contract:

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD `workflow-deep-thinking`.
4. REFERENCE-LOAD `workflow-architecture-planning`.
5. Do not APPLY either method yet.
6. SOURCE-LOAD the local source pack below.
7. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
8. Only then APPLY the methods and synthesize the architecture.

## Required Local Source Pack

Load these sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
- `docs/product/source_capture_toolbox/README.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `orca-harness/docs/adapter_author_contract.md`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/writer.py`
- `orca-harness/source_capture/packet_assembly.py`
- `orca-harness/source_capture/adapters/browser_snapshot.py`
- `orca-harness/source_capture/adapters/reddit_api.py`, if present.
- Existing runner files under `orca-harness/runners/` that define source-capture runner conventions.
- Existing tests under `orca-harness/tests/` relevant to browser snapshot, authenticated browser snapshot, packet assembly, direct HTTP, Reddit API, or no-secret packet behavior.

If a listed source is missing, record it as a source gap and continue only if the
gap does not block architecture. Do not substitute JB or any other project.

## Standard 3 Subagents

Use three advisory subagents when available. Each subagent must receive the same
source pack or a bounded source capsule and must declare source readiness before
analysis. Subagents are advisory only; the CA owns the final synthesis.

### Subagent 1 - Runner Contract Architect

Argue for the strongest bounded runner design.

Focus:

- Runner CLI inputs.
- Adapter result dataclass shape.
- Source-family mode handling.
- Packet writer integration.
- Exit codes.
- Post-run inspection.
- Agent report shape.
- How to make the runner fast and repeatable without turning it into Computer Use.

Expected output:

- Proposed runner name.
- Input contract.
- Output contract.
- Success/failure semantics.
- How agents should call it.

### Subagent 2 - Boundary And Contamination Adversary

Attack the runner design.

Focus:

- Session/cookie/storage-state leakage.
- Secret-bearing packets.
- Hidden browser profile state.
- Proxy/anti-detect opacity.
- Broad crawling via source-family bounds.
- Link-follow/source-discovery drift.
- Parser body promotion.
- Exit-code-0 false success.
- Commercial-scale escalation.
- Agent misuse of CloakBrowser as a manual browser.

Expected output:

- Hard stops.
- Must-fail tests.
- Contamination checks.
- Red flags that block agent-facing reuse.
- Minimum closure conditions.

### Subagent 3 - Implementation Grounding Integrator

Map the architecture into the existing harness and docs.

Focus:

- Existing packet model/writer constraints.
- Existing browser snapshot runner conventions.
- Existing Reddit API credential/secret handling.
- Existing runner/test patterns.
- Required runbook patches.
- Whether to implement adapter first, runner first, parser handoff first, or Reddit reference mode first.

Expected output:

- Repo-native file touch map for a later implementation pass.
- Required tests.
- Runbook update list.
- Explicit non-implementation boundaries.
- Smallest complete implementation sequence.

## Design Questions To Resolve

### 1. Runner Versus Freeform Browser

Define the boundary that prevents this shape:

```text
agent opens CloakBrowser -> agent explores/clicks/searches/follows links ->
agent saves whatever looks useful
```

and instead enforces this shape:

```text
bounded capture unit -> CloakBrowser packet runner -> Source Capture Packet ->
post-run inspection -> optional parser over preserved packet artifacts
```

Name what the agent controls and what the runner controls.

### 2. Required Runner Inputs

Define the minimum input contract. Candidate fields:

- `capture_unit_id`
- `decision_question`
- `capture_unit_intake_status`: `decision_frame_bound` or `candidate_or_scouting`
- `decision_frame_id_or_none`
- `source_family`
- `source_family_mode`
- `source_set_boundary`
- `target_locator` or source-family bounded target fields
- `volume_ceiling`
- `cutoff_posture`
- `monitoring_cadence`, only if applicable
- `stop_date`, required for monitored sets
- `method_order`
- `output_directory`
- `operator_noncommercial_posture`
- `hard_stop_acknowledgement`
- `packet_contamination_stop_acknowledgement`

Decide which fields belong in the runner CLI, a JSON/YAML capture-unit spec, or
both.

### 3. Source-Family Modes

Start with Reddit as the reference source family. Decide whether the runner
should have source-family modes such as:

- `reddit_old_html_thread`
- `reddit_old_html_listing`
- `reddit_thread_family`
- `reddit_subreddit_theme_bounded`
- `generic_cloaked_url`

Do not let a generic mode become broad crawling. If a generic mode exists, give
it stricter rules than Reddit-specific modes.

### 4. CloakBrowser Adapter Result Shape

Define what the adapter returns before the runner writes a packet.

Candidate result fields:

- final locator;
- requested locator or bounded source-set description;
- rendered HTML path or bytes;
- visible text path or bytes;
- screenshot path or bytes;
- browser metadata without secrets;
- access posture;
- anti-blocking method posture;
- JS-challenge posture;
- source-set posture;
- warning notes;
- limitation notes;
- visible stop reason;
- no-secret/contamination check status.

The adapter must not construct packets, decide source meaning, parse semantic
claims, select evidence, discover sources, score source quality, or finalize
result tokens.

### 5. Packet Output Contract

Define exactly how the runner fills the Source Capture Packet:

- source family;
- source surface;
- source locator;
- capture method;
- access posture;
- archive/history posture;
- media/modality posture;
- cutoff posture;
- re-capture relationship;
- preserved files;
- hashes;
- warnings;
- visible limitations;
- receipt non-claims.

Define how bounded source-set posture is preserved without hiding per-source or
per-slice limits.

### 6. No-Secret And Contamination Boundary

Define a mandatory no-secret-in-packet gate.

The architecture must forbid packets from preserving:

- credentials;
- cookies;
- OAuth tokens;
- authorization headers;
- raw browser profiles;
- storage-state JSON;
- session sidecars;
- proxy credentials;
- environment variable dumps;
- HAR files or logs containing request headers unless redacted under a later
  explicit design.

Define the contamination response:

```text
stop -> mark contaminated scratch -> do not claim packet success -> require owner decision
```

### 7. Exit Codes And Visible Stops

Bind exit-code semantics to existing runner conventions:

- success with packet written;
- bad input;
- adapter/runtime failure;
- visible source-access stop;
- contamination stop, if distinct;
- blocked by missing dependency or missing CloakBrowser executable/API.

Avoid treating dependency absence as source failure.

### 8. Reddit Reference Behavior

For Reddit pre-commercial use, preserve current owner decisions:

- CloakBrowser first once implemented;
- old Reddit HTML where available;
- low-volume bounded subreddit/thematic/thread-family capture;
- no broad crawling;
- no link-follow/source-discovery expansion;
- archive capture fallback;
- `.json` opportunistic only;
- BeautifulSoup parser-only after packet preservation;
- commercial/API/data-licensing route once commercial/client-funded.

Define whether the first runner should support:

- one supplied old Reddit URL only;
- thread-family list;
- subreddit/theme bounded listing;
- small monitored set;
- or only the minimal thread URL mode first.

### 9. Parser Handoff

Define what the runner does not do.

The runner preserves source-visible artifacts. Parser handoff should be a later
or separate step over already preserved packet files. The parser may extract
Reddit title, body text, comments, visible author labels, timestamps, scores,
permalinks, IDs, parent/nesting cues, deleted/removed posture, links, and parser
warnings, but it must never become the canonical source body.

### 10. Agent Runbook Update

Specify the exact runbook changes needed before normal agents can use the runner:

- runner-selection row;
- required inputs;
- command example;
- network/escalation discipline;
- output directory discipline;
- post-run inspection fields;
- visible stop semantics;
- no-secret caveat;
- Reddit mode caveats;
- non-claims.

### 11. Required Test And Review Gates

Define tests for later implementation:

- adapter unit tests with injected CloakBrowser engine seam;
- runner CLI input validation tests;
- packet-writing contract tests;
- no-secret-in-packet tests across manifest, receipt, raw files, logs, and metadata;
- no broad crawling / no source discovery tests;
- per-slice limitation visibility tests;
- old Reddit fixture preservation test;
- dependency-missing visible blocker test;
- parser handoff fixture test, if parser scope is included;
- runbook command smoke test;
- adversarial implementation review before agent-facing reuse.

Do not claim validation or readiness in this architecture pass.

## Option Set

Compare at least these options:

### Option A - Minimal URL-Only CloakBrowser Packet Runner

One supplied URL in, packet out. Fastest to implement, lowest scope, but does not
yet satisfy subreddit/theme/thread-family bounded capture without pre-supplied
URLs.

### Option B - Reddit Reference Runner First

Build a Reddit-specific runner or source-family mode first, encoding old Reddit
preference, thread-family bounds, no-discovery rules, and packet fields.

### Option C - Generic Cloaked Browser Packet Runner With Source-Family Modes

One runner with explicit modes. More reusable, but riskier if generic mode
becomes "browse anywhere."

### Option D - Adapter Contract First, Runner Later

Define only the CloakBrowser adapter result contract and engine seam first, then
write runner after the contract review clears.

### Option E - Manual CloakBrowser Fallback Only

Allow manual CloakBrowser use only as an exceptional operator action, not as an
agent-facing Capture Spine path.

## Required Output Artifact Structure

If writing the default artifact, use this structure:

1. Title
2. Retrieval header
3. Status and non-executing boundary
4. Source readiness and source gaps
5. Subagent receipts
6. Real architecture question
7. Current state
8. Option comparison
9. Recommendation
10. Runner contract
11. Adapter result contract
12. Source-family modes, with Reddit reference mode
13. Packet output contract
14. No-secret / contamination boundary
15. Exit codes and visible stops
16. Parser handoff boundary
17. Agent runbook update requirements
18. Required test and review gates
19. Implementation sequence for a later authorized pass
20. Open owner decisions
21. Non-claims
22. Next authorized step

## Success Signals

The architecture is successful only if it makes these checkable:

| Signal | Meaning |
| --- | --- |
| `runner_not_freeform_browser_pass` | Agents invoke a bounded runner, not a manual CloakBrowser browsing session. |
| `input_contract_complete_pass` | Required runner inputs are explicit enough to prevent scope drift. |
| `source_family_mode_bounded_pass` | Reddit/source-family modes cannot expand into broad crawling or source discovery. |
| `packet_writer_contract_pass` | The runner writes normal Source Capture Packets through existing writer conventions. |
| `no_secret_packet_pass` | Credentials, cookies, tokens, storage state, profiles, headers, and secrets cannot enter packet outputs. |
| `contamination_stop_pass` | Secret/session contamination has a visible stop path and cannot clear packet success. |
| `visible_failure_pass` | Missing dependency, access block, source limitation, and hard stop are distinguishable. |
| `exit_code_semantics_pass` | Runner exit codes match existing runner discipline and do not fake source failure. |
| `parser_derivative_boundary_pass` | Parser output remains derivative and never becomes canonical source body. |
| `reddit_reference_route_pass` | Reddit v0 preserves CloakBrowser-first, old Reddit preference, low-volume bounds, no discovery, archive fallback, and `.json` opportunistic-only posture. |
| `commercial_transition_pass` | Commercial/client-funded/source-scale pressure stops pre-commercial anti-blocking and reroutes to sanctioned path. |
| `agent_runbook_ready_to_patch_pass` | The architecture names exact runbook updates needed before agents may use the runner. |
| `test_plan_blocks_false_reuse_pass` | Required tests would block agent-facing reuse if no-secret, no-discovery, packet, or visible-stop behavior fails. |

## Open Owner Decisions To Preserve

Do not answer these by assumption:

- Should the first implementation be URL-only, Reddit-specific, or generic with source-family modes?
- Is small monitored Reddit-set support in v0, or deferred until candidate intake exists?
- Should candidate/scouting units be allowed to run before a Candidate/Corpus Intake contract exists, or held as planning-only until that contract exists?
- Is parser handoff in the same implementation tranche as the runner, or a separate follow-on?
- What exact volume ceiling is acceptable for Reddit v0?
- Should any LinkedIn mode be considered now, or should LinkedIn wait for the separate LinkedIn/Reddit concurrent-structure architecture?
- What CloakBrowser API surface is actually available locally, and does absence of a stable API block implementation?

## Non-Claims Required In Output

The resulting architecture must explicitly say it is not:

- implementation authorization;
- CloakBrowser install proof;
- live capture authorization;
- scraping execution;
- broad crawling authorization;
- source discovery authorization;
- storage, queue, scheduler, dashboard, deployment, or production-runtime design;
- credential/session/profile import authorization;
- CAPTCHA-solving-service authorization;
- source-quality scoring;
- fixture admission;
- ECR, Cleaning, Judgment, buyer proof, or commercial evidence design;
- legal sufficiency;
- validation or readiness.

## Closeout Requirement

If the architecture changes product doctrine, architecture doctrine, workflow
authority, validation philosophy, review authority, output authority, or
lifecycle boundaries, include a `direction_change_propagation` receipt or an
explicit `direction_change_propagation_blocker` in the written artifact.

If the pass only applies existing authority to a new implementation architecture
target, state why no propagation was required.

Do not stage, commit, push, create a PR, or run implementation.
