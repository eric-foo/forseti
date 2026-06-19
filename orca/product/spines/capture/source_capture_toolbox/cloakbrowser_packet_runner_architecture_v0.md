# CloakBrowser Packet Runner Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture planning artifact
status: ARCHITECTURE_RECOMMENDATION_V0
scope: >
  Non-executing architecture for exposing CloakBrowser to agents as a bounded
  Source Capture Packet runner path rather than a freeform browser-control
  surface.
use_when:
  - Scoping the CloakBrowser adapter contract and packet runner before any
    implementation pass.
  - Checking how agents may supply bounded capture units without manually
    controlling CloakBrowser.
  - Preserving packet-before-parser, no-secret, no-discovery, visible-stop, and
    commercial-reroute boundaries for Reddit pre-commercial capture.
authority_boundary: planning_only
open_next:
  - docs/prompts/architecture/cloakbrowser_packet_runner_architecture_prompt_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - orca/product/spines/capture/source_capture_toolbox/README.md
  - orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - orca-harness/docs/adapter_author_contract.md
stale_if:
  - CloakBrowser API shape, install path, executable contract, or local
    availability becomes known and contradicts the adapter-first recommendation.
  - Reddit pre-commercial method ordering changes.
  - Source Capture Packet schema, packet writer, no-secret rules, or packet
    lifecycle rules change.
  - Orca authorizes storage, scheduler, queue, dashboard, deployment,
    production runtime, broad crawler behavior, or commercial Reddit use.
```

## 1. Status And Non-Executing Boundary

This is a planning-only architecture artifact produced from
`docs/prompts/architecture/cloakbrowser_packet_runner_architecture_prompt_v0.md`.

It does not implement a runner, install CloakBrowser, run live capture, open
Reddit, configure proxies, solve CAPTCHA, create credentials, create storage,
write parser code, stage commits, push, or create a PR.

Architecture result: `TARGET_RECOMMENDED`.

Required recommendation:

```text
RECOMMEND_ADAPTER_CONTRACT_FIRST
```

The owner intent remains:

```text
agent supplies a bounded capture unit -> runner invokes CloakBrowser backend ->
runner writes a Source Capture Packet -> agent inspects manifest/receipt/raw ->
parser/consolidation consume preserved packet artifacts
```

The rejected path remains:

```text
agent manually controls CloakBrowser like Computer Use
```

## 2. Source Readiness And Source Gaps

`SOURCE_CONTEXT_READY`.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom CloakBrowser packet-runner architecture pack
  edit_permission: docs-write
  target_scope:
    - orca/product/spines/capture/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md
  dirty_state_checked: yes
  controlling_source_state: >
    Working tree contained modified and untracked files before this pass,
    including required source-pack files. They were used as repo-visible
    advisory context only; this artifact makes no validation, readiness,
    acceptance, or clean-source claim.
  blocked_if_missing: none for architecture; implementation remains blocked on
    CloakBrowser API shape.
```

Sources loaded:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/validation-gates.md`
- `workflow-deep-thinking` skill, reference-loaded
- `workflow-architecture-planning` skill, reference-loaded from the available
  Agent Workflow plugin copy
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
- `orca/product/spines/capture/source_capture_toolbox/README.md`
- `orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`
- `orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `orca-harness/docs/adapter_author_contract.md`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/writer.py`
- `orca-harness/source_capture/packet_assembly.py`
- `orca-harness/source_capture/adapters/browser_snapshot.py`
- `orca-harness/source_capture/adapters/reddit_api.py`
- relevant existing runners under `orca-harness/runners/`
- relevant tests under `orca-harness/tests/`

External public orientation checked after the initial artifact was written:

- `https://github.com/CloakHQ/cloakbrowser`

This external check is not Orca authority, validation, install proof, or legal
sufficiency. It informs only the adapter-contract question: public docs describe
CloakBrowser as a Playwright/Puppeteer-style wrapper over a custom Chromium
binary with optional proxy and persistent-profile features, so the Orca seam
must be explicit about anonymous-only v0, proxy secrecy, and local API/version
verification.

Source gaps:

- CloakBrowser local API shape is not verified inside this workspace. Current
  public CloakBrowser documentation presents it as a Python/JavaScript wrapper
  around a custom Chromium binary with Playwright/Puppeteer-style launch APIs,
  optional proxy support, automatic binary download, a self-hosted profile
  manager, MIT-licensed wrapper code, and a separately licensed compiled
  Chromium binary. Treat that as external orientation only until a later
  implementation pass verifies the exact local package/version/API.
- No CloakBrowser adapter or runner exists in the current harness.
- No Reddit API packet runner exists, though the Reddit API adapter and
  credential-store support are present.
- A broad `rg` search crossed scratch/cache directories with access-denied
  errors and was not used as validation.

## 3. Subagent Receipts

Three advisory subagents were launched. Each was read-only, given the prompt and
source pack boundary, and instructed to declare source readiness before analysis.
Subagents are advisory inputs only. They are not verdicts, implementation
authority, validation, or readiness proof.

| Subagent | Readiness | Advisory result |
| --- | --- | --- |
| Runner Contract Architect | `SOURCE_CONTEXT_READY` | Strongest shape is a spec-driven runner named `run_source_capture_cloakbrowser_packet.py`: agents submit a bounded capture-unit spec; the runner validates, invokes CloakBrowser through an adapter seam, writes normal Source Capture Packets, and exits with inspectable artifacts or visible stops. |
| Boundary And Contamination Adversary | `SOURCE_CONTEXT_READY` | Hardest blockers are raw cookies/storage-state/profile/HAR/proxy credentials in inputs or outputs, generic cloaked browsing, link-follow discovery, commercial escalation, parser body promotion, dependency absence disguised as source failure, and exit-code-0 false success. |
| Implementation Grounding Integrator | `SOURCE_CONTEXT_READY` | Repo-native sequence should be adapter contract first, then runner. Current harness convention is adapter free function plus frozen dataclasses plus injected engine seam; runner translates results into the existing packet writer. |

## 4. Real Architecture Question

What runner contract makes CloakBrowser reliable for Capture Spine use while
preventing freeform browsing, source discovery, session leakage, packet
contamination, hidden state, vague success claims, storage drift, parser-body
promotion, and commercial-scale escalation?

The decisive invariant:

```text
Agents control only a bounded capture-unit spec. CloakBrowser execution is owned
by an adapter seam. Source Capture Packet writing is owned by the existing packet
writer. Parser/consolidation output is derivative and never canonical source
body.
```

## 5. Current State

CloakBrowser is selected as Orca's primary anti-blocking browser backend for the
next third-tranche implementation lane. For Reddit pre-commercial capture, the
current order is CloakBrowser anti-blocking first once implemented, old Reddit
HTML where available, low-volume bounded capture, archive fallback, `.json`
opportunistic only, and commercial/API/data-licensing route once the source
becomes commercial, enterprise, client-funded, buyer-facing, or scale pressured.

The harness already has:

- Source Capture Packet models and writer;
- closed cutoff/archive/recapture posture vocabularies;
- no clean rollup over hidden limited slices;
- direct HTTP, media, Archive.org, browser snapshot, authenticated browser
  snapshot, and Reddit API adapter conventions;
- secret indirection patterns for authenticated browser and Reddit credentials;
- no-secret tests around authenticated browser and Reddit API adapter fields;
- runbook guidance that CloakBrowser is authorized but not implemented.

The harness does not yet have:

- a CloakBrowser adapter seam;
- a CloakBrowser packet runner;
- a verified local CloakBrowser package/version/API contract;
- an agent-facing runbook command for CloakBrowser.

External orientation checked after the initial pass: CloakBrowser's public
repository describes a drop-in Playwright/Puppeteer-style wrapper over a custom
Chromium binary, optional proxy parameters, persistent profile support, and a
self-hosted profile manager. That means Orca probably does not need Computer
Use-style GUI driving. It still needs an Orca adapter seam because public
examples include proxy and persistent-profile surfaces that are exactly where
packet contamination and hidden-state risk enter.

## 6. Option Comparison

| Option | Verdict | Reason |
| --- | --- | --- |
| A - Minimal URL-only CloakBrowser Packet Runner | Downgraded | Useful later as the first executable runner mode, but too early before the no-secret adapter result shape and local CloakBrowser API/version are verified. |
| B - Reddit Reference Runner First | Downgraded | Reddit-specific behavior is the right first product family, but runner-first risks baking public-example proxy/profile/session surfaces into agent-facing CLI behavior before Orca has sealed the adapter boundary. |
| C - Generic Cloaked Browser Packet Runner With Source-Family Modes | Rejected for v0 | Too easy to become "browse anywhere." Generic mode should not be normal agent-facing v0 behavior. |
| D - Adapter Contract First, Runner Later | Selected | Matches existing harness conventions and closes the biggest unknown: what CloakBrowser returns, how secrets/session state are excluded, and how dependency/API absence is reported. |
| E - Manual CloakBrowser Fallback Only | Downgraded to exceptional operator-only | Manual use may remain an exceptional owner/operator action, but it must not be the agent-facing Capture Spine path. |

## 7. Recommendation

Recommend `RECOMMEND_ADAPTER_CONTRACT_FIRST`.

This is not a retreat from the packet runner goal. It is the smallest complete
route to that goal because the current risk is not "how to drive a browser";
public CloakBrowser docs suggest a Playwright-like automation surface exists.
The risk is what contract safely contains CloakBrowser so the runner cannot leak
secrets, hide profile/profile-manager state, turn proxy details into packet
contents, or become manual browser control.

The target path:

1. Define a CloakBrowser adapter result contract and injected engine seam.
2. Prove, with fake-engine tests, that the adapter can return preserved HTML,
   visible text, screenshot bytes, non-secret metadata, access/anti-blocking
   posture, JS-challenge posture, warnings, limitations, visible stop reasons,
   and contamination status without constructing packets.
3. Keep the v0 engine seam anonymous-only: no storage-state, profile, cookie,
   direct session, or profile-manager state argument.
4. Build the packet runner only after the adapter contract is narrow enough to
   prevent hidden state and secret-bearing result fields.
5. Start the runner with one supplied bounded Reddit old-HTML thread mode or a
   finite supplied thread-family list. Add bounded listing/theme modes only after
   no-discovery and volume-ceiling tests exist.

## 8. Runner Contract

Runner name for later implementation:

```text
orca-harness/runners/run_source_capture_cloakbrowser_packet.py
```

Normal agent-facing invocation should be spec-driven:

```powershell
python runners/run_source_capture_cloakbrowser_packet.py `
  --capture-unit-spec "<capture-unit.json>" `
  --output "<packet directory>"
```

The CLI should stay thin. Do not expose a large set of freeform flags that let
agents improvise browser behavior. The capture-unit spec is the control surface.

Required capture-unit fields:

| Field | Requirement |
| --- | --- |
| `capture_unit_id` | Stable operator-supplied unit id. |
| `decision_question` | Operator-supplied capture question. |
| `capture_unit_intake_status` | `decision_frame_bound` or `candidate_or_scouting`. |
| `decision_frame_id_or_none` | Required id for `decision_frame_bound`; explicit `none` otherwise. |
| `source_family` | Initially `reddit`. |
| `source_family_mode` | Closed mode token; see Section 10. |
| `source_set_boundary` | Human-readable bounded source set. |
| `target_locator` or bounded target fields | Supplied URL/list/thread family/subreddit/theme/query fields depending on mode. |
| `volume_ceiling` | Hard maximum; never inferred by the runner. |
| `cutoff_posture` | Closed posture where known, or unknown reason. |
| `method_order` | CloakBrowser first once implemented; old Reddit where available; archive fallback; `.json` opportunistic only. |
| `output_directory` | Fresh packet directory. |
| `operator_noncommercial_posture` | Must affirm pre-commercial posture; commercial pressure fails before adapter invocation. |
| `hard_stop_acknowledgement` | Explicit acknowledgement of source-access hard stops. |
| `packet_contamination_stop_acknowledgement` | Explicit acknowledgement of stop -> contaminated scratch -> no success claim. |

For monitored sets, both `monitoring_cadence` and `stop_date` are required. A
monitored set without a stop date fails input validation.

The agent controls only the spec. The runner controls:

- CloakBrowser engine invocation;
- timeout and artifact caps;
- no-discovery behavior;
- staging cleanup;
- Source Capture Packet writer invocation;
- exit code and visible-stop semantics.

## 9. Adapter Result Contract

Later adapter module:

```text
orca-harness/source_capture/adapters/cloakbrowser_snapshot.py
```

Adapter shape:

```text
fetch_cloakbrowser_snapshot_capture(...native inputs..., engine: CloakBrowserEngine | None)
  -> CloakBrowserSnapshotSuccess | CloakBrowserSnapshotFailure
```

The adapter returns frozen dataclasses. It never imports the writer and never
constructs a packet.

The v0 `CloakBrowserEngine` seam is anonymous-only. It must not accept
`storage_state`, profile, cookie, direct session, raw browser-profile, or
profile-manager state arguments. Authenticated/session cloaked capture is a
separate later gate, because adding those parameters to the first seam would make
session leakage a default integration shape.

Success result fields:

- requested locator or bounded source-set descriptor;
- final locator;
- rendered HTML bytes or text;
- visible text bytes or text;
- screenshot bytes;
- non-secret browser metadata;
- source-family mode;
- access posture;
- anti-blocking method posture, recording disclosable method category without
  endpoint, credential, exit-IP, or secret-bearing values;
- JS-challenge posture;
- source-set posture;
- warning notes;
- limitation notes;
- contamination check status;
- visible stop reason, if the run completes with limitations.

Failure result fields:

- requested locator or source-set descriptor;
- failure kind;
- message;
- final locator if safely known;
- visible dependency/API absence flag when relevant.

The adapter must not:

- construct packets;
- decide source meaning;
- parse semantic claims;
- select evidence;
- discover sources;
- follow links, users, comments, recommendations, or "more like this" surfaces;
- score source quality;
- finalize result tokens;
- expose credentials, cookies, tokens, authorization headers, proxy credentials,
  proxy endpoints, proxy exit IPs, raw browser profiles, storage-state JSON, HAR
  files, environment dumps, or secret-bearing logs.

## 10. Source-Family Modes

Recommended v0 modes:

| Mode | Scope |
| --- | --- |
| `reddit_old_html_thread` | One supplied old Reddit thread URL. Smallest later executable runner mode. |
| `reddit_thread_family_supplied` | Explicit finite list of supplied thread URLs; no discovery, no expansion. |
| `reddit_bounded_listing_seed` | Deferred until no-discovery, volume-ceiling, cutoff, and stop-date tests exist. |

Do not expose normal-agent `generic_cloaked_url` in v0.

If a generic mode is later authorized, it should be named
`generic_cloaked_url_one_supplied_url`, accept exactly one supplied URL, and
forbid source-set/listing/query behavior, link following, discovery, retries that
change scope, and parser/consolidation handoff.

## 11. Packet Output Contract

On success, the runner writes a normal Source Capture Packet through existing
writer conventions:

- `manifest.json`;
- `receipt.md`;
- `raw/`;
- source family;
- source surface;
- source locator;
- capture method;
- access posture;
- archive/history posture;
- media/modality posture;
- cutoff posture;
- re-capture relationship;
- per-slice preserved files;
- per-slice warnings and limitations;
- hashes and `hash_basis`;
- receipt non-claims.

For CloakBrowser, source surface should distinguish the source-family mode, for
example `cloakbrowser_reddit_old_html_thread`.

Per-source or per-slice limits must stay visible. A capture-level rollup must
not hide failed, limited, unknown, fallback, blocked, or not-preserved slices.

Receipt non-claims must include at least:

- not validation;
- not readiness;
- not source completeness proof;
- not fixture admission;
- not source-quality scoring;
- not parser correctness proof;
- not ECR, Cleaning, Judgment, buyer proof, or commercial-readiness evidence;
- not broad crawling;
- not source discovery;
- not storage, queue, scheduler, dashboard, deployment, or production runtime;
- not commercial Reddit authorization;
- not legal sufficiency.

## 12. No-Secret And Contamination Boundary

The runner and adapter must forbid packets from preserving:

- credentials;
- cookies;
- OAuth tokens;
- authorization headers;
- raw browser profiles;
- storage-state JSON;
- session sidecars;
- proxy credentials;
- proxy endpoints;
- proxy exit IPs;
- environment variable dumps;
- HAR files or request logs containing headers unless a later explicit design
  defines redaction.

The existing `stage_and_write_packet(...)` helper is not a secrecy boundary. The
adapter and runner own no-secret enforcement before bytes or metadata are staged.

Proxy handling is two-sided:

- proxy category and anti-blocking method category are disclosable provenance and
  must be recorded when used;
- proxy endpoint, username, password, provider account details, and assigned
  exit IP are secret-bearing or operator-sensitive and must not enter packet
  outputs.

Proxy support is out of v0 unless a later pass defines a `local_secret_store.py`
specialization for proxy configuration. Do not create a second credential
subsystem.

Contamination response:

```text
stop -> mark contaminated scratch if anything exists -> do not claim packet
success -> require owner decision for disposal, redaction, or isolation
```

A contaminated run must not produce a normal successful `manifest.json` /
`receipt.md` pair.

## 13. Exit Codes And Visible Stops

Preserve the current runner exit-code convention from the adapter-author
contract unless the owner explicitly amends it: `0` for packet produced, `2` for
bad input / boundary preflight failure, and `3` for adapter or other failure.
Contamination and dependency absence still need distinct machine-readable report
tokens, but they must not silently introduce new exit codes.

| Exit | Meaning |
| --- | --- |
| `0` | Packet written; manifest/receipt/raw exist; post-run inspection still required. |
| `2` | Bad input or boundary preflight failure: missing required fields, invalid mode, invalid volume, missing monitored stop date, source-discovery request, generic browsing request, commercial posture conflict, missing hard-stop/contamination acknowledgement, or candidate unit claiming Data Capture handoff. |
| `3` | Adapter/runtime/source-access failure: navigation failed, timeout, empty DOM/screenshot, artifact cap exceeded, source returned visible block, packet artifact write failed before success, CloakBrowser dependency/backend unavailable, or contamination stop. No normal packet. |

Dependency absence must never be reported as source limitation or exit `0`.
Record it as a distinct visible report token such as
`cloakbrowser_dependency_unavailable`. Record contamination as
`cloakbrowser_contamination_stop`. A later owner decision may amend the global
runner convention to add exit `4` / `5`, but this architecture does not make that
change.

## 14. Reddit Reference Behavior

For Reddit pre-commercial use:

- CloakBrowser is first once implemented.
- Old Reddit HTML is preferred where available.
- Capture is low-volume and bounded by supplied thread, supplied thread family,
  named subreddit/theme/query boundary, or small monitored set with stop date.
- Broad crawling, source discovery, link following, user walking, comment
  expansion as discovery, recommendations, and "more like this" expansion are
  forbidden.
- Archive capture remains fallback or historical posture support.
- `.json` is opportunistic only and does not become the spine.
- BeautifulSoup-style parsing happens only after packet preservation.
- Commercial, client-funded, enterprise, buyer-facing durable use, scale
  pressure, or data-licensing pressure stops anti-blocking capture and reroutes
  to sanctioned commercial / enterprise API or data-licensing path.

First later runner mode should be `reddit_old_html_thread`. The broader
`reddit_bounded_listing_seed` mode should wait until the no-discovery and
volume-ceiling tests exist.

## 15. Parser Handoff Boundary

The runner preserves source-visible artifacts. It does not parse source meaning.

A later parser may extract from already preserved packet files:

- Reddit submission title and body text;
- comment body text;
- visible author labels;
- visible timestamps;
- visible score or score-hidden state;
- permalinks and ids;
- parent/nesting cues;
- deleted, removed, collapsed, hidden, unavailable, lock, edit, and moderation
  posture where visible;
- outbound links and media pointers;
- parser warnings.

Parser output is derivative. `raw_packet_path` and raw file id are the source-body
ownership path. A row without a resolvable packet pointer must not present
`body_text` as canonical source body.

## 16. Agent Runbook Update Requirements

Do not patch the runbook until the runner behavior exists. A later runbook patch
must add:

- runner-selection row for CloakBrowser packet runner;
- required capture-unit spec fields;
- command example with `--capture-unit-spec` and `--output`;
- network/escalation discipline for live runner use;
- fresh output directory discipline;
- post-run inspection fields for `manifest.json`, `receipt.md`, and `raw/`;
- exit-code table including dependency absence and contamination;
- no-secret caveat;
- Reddit old-HTML, low-volume, no-discovery, `.json` opportunistic-only, parser
  derivative-only, and commercial-reroute caveats;
- explicit instruction not to simulate CloakBrowser with the honest browser
  runner.

## 17. Required Test And Review Gates

Required later tests before agent-facing reuse:

- adapter unit tests with fake CloakBrowser engine;
- dependency-missing, timeout, runtime failure, empty DOM, empty screenshot, and
  artifact size-cap tests;
- runner CLI/spec validation tests for required fields, invalid modes, invalid
  volume, monitored cadence without stop date, commercial posture, hard-stop
  acknowledgements, and contamination acknowledgement;
- packet-writing contract tests for raw HTML, visible text, screenshot, metadata,
  source slices, file ids, staging cleanup, warnings, limitations, and receipt
  non-claims;
- no-secret-in-packet tests across manifest, receipt, raw files, metadata files,
  logs if any, and staging leftovers;
- disclosability inverse-test: if anti-detect, proxy, or JS-challenge behavior
  is used, the packet/report must record the method category; a missing category
  is a failure even when no secret leaks;
- proxy boundary tests if proxy support is later scoped: category recorded,
  endpoint/credentials/exit-IP absent;
- anonymous-only seam test: v0 engine seam rejects or lacks storage-state,
  profile, cookie, direct-session, or profile-manager state arguments;
- no broad crawling / no source discovery tests;
- per-slice limitation visibility tests;
- old Reddit fixture preservation test using local saved HTML, not live Reddit;
- dependency-missing visible blocker test;
- parser handoff fixture test if parser scope is included;
- runbook command smoke test after runner exists;
- adversarial implementation review before normal agents can use the runner.

Do not claim validation or readiness from this architecture pass.

## 18. Implementation Sequence For A Later Authorized Pass

Later implementation should be separately authorized and should proceed in this
order:

1. Define CloakBrowser adapter dataclasses, failure kinds, and anonymous-only
   injected engine `Protocol`.
2. Add fake-engine adapter tests proving non-secret result shape and visible
   failures.
3. Implement minimal adapter for one supplied bounded locator.
4. Add runner accepting `--capture-unit-spec` and `--output`, mapping adapter
   results into current packet writer/assembly conventions.
5. Add no-secret, disclosability-inverse, proxy-boundary-if-scoped,
   anonymous-only-seam, no-discovery, and exit-code/report-token tests before
   runbook exposure.
6. Patch `orca-harness/docs/source_capture_agent_runbook.md` with exact command,
   inputs, stops, inspection, and report shape.
7. Add Reddit-specific bounded modes only after the minimal old-thread mode is
   closed enough to review.
8. Treat parser handoff as a separate follow-on unless the owner explicitly
   authorizes it in the same tranche.

## 19. Open Owner Decisions

- Should the first implemented mode be only `reddit_old_html_thread`, or also a
  finite supplied thread-family list?
- Is small monitored Reddit-set support in v0, or deferred until candidate
  intake exists?
- Should `candidate_or_scouting` units be runnable at all before a Candidate
  Signal Intake / Corpus Intake contract exists?
- Is parser handoff in the same implementation tranche as the runner or a
  separate follow-on?
- What exact volume ceiling is acceptable for Reddit v0?
- Should LinkedIn remain completely out of this runner until the separate
  LinkedIn/Reddit concurrent-structure architecture is accepted?
- What CloakBrowser API surface is actually available locally, and does absence
  of a stable API block implementation?
- Should Orca ever amend the frozen runner exit-code convention from `0`/`2`/`3`
  to add distinct contamination/dependency exits such as `4`/`5`, or should those
  remain report tokens under exit `3`?
- Should proxy support be in v0 at all? Current canonical recommendation is no:
  proxy category may be designed as provenance, but endpoint/credentials/exit-IP
  handling needs a later local-secret-store specialization before use.

## 20. Non-Claims

This artifact is not:

- implementation authorization;
- CloakBrowser install proof;
- live capture authorization;
- scraping execution;
- broad crawling authorization;
- source discovery authorization;
- storage, queue, scheduler, dashboard, deployment, or production-runtime
  design;
- credential/session/profile import authorization;
- CAPTCHA-solving-service authorization;
- source-quality scoring;
- fixture admission;
- ECR, Cleaning, Judgment, buyer proof, or commercial evidence design;
- legal sufficiency;
- validation or readiness.

## 21. Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now has a planning-only CloakBrowser packet-runner architecture
    recommendation: define the CloakBrowser adapter contract and engine seam
    first, then expose an agent-facing spec-driven Source Capture Packet runner
    only after no-secret, no-discovery, visible-stop, and packet-writer
    boundaries are testable; the canonical artifact now preserves the existing
    `0`/`2`/`3` runner exit convention, requires disclosable anti-blocking method
    provenance, keeps proxy endpoint/credential/exit-IP values out of packets,
    and makes the v0 CloakBrowser engine seam anonymous-only.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - orca/product/spines/capture/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
    - docs/product/data_capture_source_access_boundary_decision_v0.md
    - docs/product/data_capture_source_access_method_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md
    - orca/product/spines/capture/source_capture_toolbox/README.md
    - orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
    - orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
    - orca-harness/docs/source_capture_agent_runbook.md
    - orca-harness/docs/adapter_author_contract.md
    - orca-harness/source_capture/models.py
    - orca-harness/source_capture/writer.py
    - orca-harness/source_capture/packet_assembly.py
    - orca-harness/source_capture/adapters/browser_snapshot.py
    - orca-harness/source_capture/adapters/reddit_api.py

  intentionally_not_updated:
    - path: docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
      reason: >
        CloakBrowser selection, third-tranche authorization, Reddit ordering,
        deferred surfaces, and non-claims already exist there; this artifact
        designs the runner contract inside that authority.
    - path: orca/product/spines/capture/source_capture_toolbox/README.md
      reason: >
        README already states CloakBrowser is selected but not implemented; no
        component implementation status changed in this planning pass.
    - path: orca-harness/docs/source_capture_agent_runbook.md
      reason: >
        No runnable CloakBrowser command exists yet. Runbook patch belongs after
        a separately authorized implementation creates exact behavior.
    - path: orca-harness/docs/adapter_author_contract.md
      reason: >
        Existing adapter convention remains sufficient and its `0`/`2`/`3`
        runner exit convention is preserved. A CloakBrowser-specific section
        should be added only if implementation exposes a new constraint or owner
        explicitly amends runner exit semantics.
  stale_language_search: >
    rg -n "exit `4`|exit `5`|Recommended later runner exit codes|storage_state|profile-manager state|proxy endpoint|proxy exit IP|disclosability inverse"
    orca/product/spines/capture/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md
    orca-harness/docs
  stale_language_search_result: >
    Executed after this patch. Live hits are expected: this canonical artifact's
    public-orientation note, no-secret/proxy boundary, anonymous-only seam,
    disclosability inverse-test, owner-decision wording, DCP receipt/search
    string. No live canonical section silently recommends exit `4`/`5` without
    owner convention amendment.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not CloakBrowser installed
    - not live capture authorization
    - not source-access boundary amendment
```

## 22. Next Authorized Step

Owner review of this patched canonical architecture recommendation. If accepted,
the smallest complete next authorized step is a bounded implementation-scoping
prompt for the CloakBrowser adapter contract only, not the runner, not parser
handoff, not live capture, and not runbook exposure.

Implementation scoping should first verify the local CloakBrowser
package/version/API. It should stop as blocked if the actual local API cannot be
represented without secret-bearing result fields, hidden profile/profile-manager
state, source discovery, or non-disclosable method provenance.
