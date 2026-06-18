# Reddit Pre-Commercial Capture Consolidation Success-Signal Architecture Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: >
  Non-executing architecture-planning prompt for hardening the Reddit
  pre-commercial capture/consolidation planning thread so its success signals
  integrate with the Data Capture Spine and Source Capture Armory instead of
  becoming a standalone scraping, storage, source-discovery, ECR, Cleaning, or
  Judgment plan. Uses the standard three advisory architecture subagents.
use_when:
  - Running the architecture pass for Reddit capture/consolidation success signals.
  - Checking whether the Reddit planning thread should be patched for Armory integration.
  - Preventing Reddit capture/consolidation rows from becoming storage, source-quality verdicts, fixture admission, ECR, Cleaning, Judgment, or production monitoring by implication.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - orca/product/spines/capture/source_capture_toolbox/README.md
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - Reddit source-access order, CloakBrowser backend selection, or `.json` posture changes.
  - The Source Capture Armory packet shape, lifecycle, source-quality profile, queue template, or state assembler changes.
  - Data Capture Spine permits standing/opportunistic corpus capture inside v0 instead of requiring commissioned capture.
  - A later owner decision authorizes Reddit storage, production monitoring, broad crawling, commercial fetch, or commercial API operation.
```

## Status

Status: `PROMPT_V0`.

Prompt artifact path:
`docs/prompts/architecture/reddit_precommercial_capture_consolidation_success_signal_architecture_prompt_v0.md`.

Default output mode: `file-write`.

Default target architecture artifact:
`docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`.

This prompt is design-only. It does not authorize live Reddit access,
CloakBrowser installation, runner dispatch, parser implementation, storage,
dashboard, scheduler, deployment, production monitoring, ECR, Cleaning,
Judgment, commercial Reddit use, commits, pushes, or PRs.

## Commission

Create a non-executing architecture routing object that decides how to harden
the success signals in
`docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`.

The long-term goal is not a standalone Reddit scraper. The long-term goal is:

```text
Integrate bounded Reddit pre-commercial capture and consolidation into the
Source Capture Armory and Data Capture Spine as an obligation-visible
source-family route, with a clean later transition to sanctioned commercial /
enterprise Reddit API or data licensing when the project becomes commercial.
```

The anchor goal for this pass is:

```text
Define robust success signals that make every Reddit capture/consolidation
claim checkable against Data Capture obligations, Source Capture Packet
provenance, packet lifecycle, source-quality vocabulary, state-assembler
boundaries, source-access hard stops, and commercial-transition triggers.
```

The architecture output must answer:

```text
What success-signal structure should the Reddit planning thread use so that
future operators can tell when a Reddit capture unit is in-bounds, packet-owned,
parser-separated, lifecycle-visible, source-quality-compatible,
planning-only, and not broad crawling, storage, source discovery, ECR, Cleaning,
Judgment, validation, readiness, fixture admission, or commercial Reddit use?
```

## Hard Boundary

This is an architecture pass, not implementation and not capture execution.

Do not:

- fetch Reddit;
- install or run CloakBrowser, Patchright, Playwright, BeautifulSoup, PRAW, or
  any other runtime dependency;
- create parser code, runner code, schemas, tests, storage, queues, dashboards,
  schedulers, or deployment artifacts;
- perform live web research;
- patch the target Reddit planning artifact unless the current launch
  instruction explicitly adds patch authority;
- change Data Capture obligation doctrine, source-access boundary doctrine, or
  Source Capture Armory lifecycle doctrine;
- design ECR, Cleaning, Judgment, buyer proof, source-quality scoring, fixture
  admission, or commercial Reddit operation.

## Orca Authority

Use Orca authority in this order:

1. Current launch instruction.
2. `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable workflow methods only as mechanics, not Orca project authority.

Do not import `jb` rules, paths, lifecycle mechanics, product policy,
validation habits, model lanes, review labels, handoff rules, or artifact roles
as Orca authority.

## Thread Operating Target Continuity

```yaml
goal_handoff:
  long_term_goal: "Integrate bounded Reddit pre-commercial capture and consolidation into the Source Capture Armory and Data Capture Spine as an obligation-visible source-family route, with a clean later transition to sanctioned commercial / enterprise Reddit API or data licensing when the project becomes commercial."
  anchor_goal: "Define robust success signals that make every Reddit capture/consolidation claim checkable against Data Capture obligations, Source Capture Packet provenance, packet lifecycle, source-quality vocabulary, state-assembler boundaries, source-access hard stops, and commercial-transition triggers."
  success_signal: "A future operator can decide whether a proposed Reddit capture/consolidation pass is in-bounds by checking concrete gates for Decision Frame or candidate-intake status, bounded source set, volume and cadence ceiling, method order, disclosability, packet-before-parser handoff, lifecycle/sensitivity state, source-quality vocabulary compatibility, planning-only consolidation, and commercial/API switch triggers."
  status: user_stated
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: yes
  lifecycle_status: active_thread_local
  if_changed_reason: "Owner corrected the long-term goal from Reddit scraping planning alone to integration with the Source Capture Armory and Capture Spine."
```

## Preflight

Before source analysis, record:

```yaml
orca_start_preflight:
  agents_read: yes/no
  overlay_read: yes/no
  source_pack: custom Reddit capture/consolidation success-signal architecture pack
  workspace: C:\Users\vmon7\Desktop\projects\orca
  edit_permission: docs-write for the target architecture artifact only
  output_mode: file-write
  target_scope:
    - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
  source_target_read_only:
    - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  dirty_state_checked: yes/no
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/source_capture_toolbox/README.md
```

If the target architecture artifact already exists, read it first and do not
silently overwrite it. Choose the next version suffix or return a visible
collision blocker.

## Required Method Sequence

1. `REFERENCE-LOAD` `workflow-deep-thinking`.
2. `REFERENCE-LOAD` `workflow-architecture-planning`.
3. Do not `APPLY` either method before source readiness. Use them only to form
   neutral source-reading questions.
4. `SOURCE-LOAD` the required source pack below.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. Only after source readiness, `APPLY` `workflow-deep-thinking` to identify
   the real architecture question, failure modes, success-signal criteria, and
   live option set.
7. Then `APPLY` architecture planning to synthesize the target routing object.

If any named method is unavailable, report the missing method and continue only
as advisory. Do not claim a formal method-backed architecture result.

## Required Source Pack

Read these before producing the architecture artifact:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_spine_lane_product_thesis_v0.md`
- `docs/product/source_capture_toolbox/README.md`
- `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
- `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`
- `docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md`
- `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`

Conditional reads only if a finding depends on harness implementation reality:

- `orca-harness/docs/source_capture_agent_runbook.md`
- `orca-harness/docs/adapter_author_contract.md`
- `orca-harness/source_capture/`
- `orca-harness/runners/`

Do not bulk-load unrelated product, review, prompt, research, inbox, or
implementation files.

## Source Readiness Gate

Before analysis, declare:

- `SOURCE_CONTEXT_READY`; or
- `SOURCE_CONTEXT_INCOMPLETE`.

If incomplete, name missing sources, what claims cannot be made, and the
smallest source capsule needed. Do not write the architecture artifact if the
missing sources could change the target architecture.

## Subagents - 3 Standard, Required When Available

Launch exactly three advisory architecture subagents when subagent tooling is
available. Each subagent receives the source pack or a bounded source capsule,
runs its own source-readiness gate, and returns advisory input only. The main
planner owns synthesis. Subagent agreement is not proof.

If subagent tooling is unavailable, blocked, or rejected, return
`BLOCKED_SUBAGENTS_UNAVAILABLE` unless the launch instruction explicitly
authorizes `plain_model_local_fallback`.

### SA-1 - Directional Architect

Develop the strongest source-backed target architecture for robust Reddit
success signals.

Focus:

- integrating Reddit into Data Capture Spine and Source Capture Armory;
- Decision Frame versus candidate-intake split;
- packet-before-parser success;
- source-quality vocabulary compatibility;
- minimal success-signal taxonomy that future operators can apply.

Output:

- recommended success-signal structure;
- what must be added to the Reddit planning thread;
- decisive source citations;
- source gaps that could change the recommendation.

### SA-2 - Adversarial Architect

Attack the strongest target architecture.

Focus:

- standing corpus capture sneaking into commissioned Data Capture v0;
- broad crawling, production monitoring, source discovery, or adaptive
  expansion;
- storage/database/dashboard/scheduler drift;
- parser output becoming canonical source body;
- packet existence becoming source-quality success;
- consolidation rows becoming ECR, Cleaning, Judgment, fixture admission,
  validation, readiness, or buyer proof;
- login/paywall/CAPTCHA wording conflicting with the accepted boundary.

Output:

- material failure modes;
- required hard gates;
- exact success-signal wording needed to close fake-success paths;
- unresolved owner questions.

### SA-3 - Grounding Integrator

Keep the architecture repo-native, minimal, and vocabulary-consistent.

Focus:

- mapping Reddit rows to existing queue/profile/state-assembler vocabulary
  without inventing parallel states;
- packet lifecycle, retention, sensitivity, and fixture-admission boundaries;
- source-access method order and disclosability;
- commercial/API switch trigger;
- one-off planning table versus storage/consolidated output boundary;
- smallest complete patch recommendation.

Output:

- integration fields or bridge gates to name explicitly;
- terms to reuse from existing sources;
- terms to avoid;
- smallest complete architecture result and next authorized step.

## Known Issues To Test

Treat these as candidate concerns, not settled findings. Confirm or reject them
from source:

- The current Reddit planning artifact may not clearly say that a Reddit
  capture unit is Data Capture Spine work only when bound to an existing
  Decision Frame; otherwise it may be candidate-source scouting or corpus-intake
  planning, not ECR-ready capture.
- The current consolidation shape may be provenance-forward but not
  obligation-complete: it may need contract version, operator/session
  provenance, mode changes, per-obligation discharge state, related-chain
  fairness boundary, recapture relationship, and categorical handoff posture.
- The current row shape may need a bridge to existing source-quality fields:
  `source_id`, `case_or_slot`, `bounded_source_context`, `current_state`,
  `target_posture`, `primary_runner`, `fallback_runner`, `row_status`,
  `result_token`, `packet_lifecycle`, `operator_finalization_required`,
  `source_quality_report_block_path_or_none`, `sensitivity_note`,
  `retention_basis`, `allowed_downstream_use`, and
  `separate_fixture_admission_decision_or_none`.
- Success may need tiered non-successes: planning success, packet success,
  parser success, consolidation success, source-quality success, and batch
  state are different and must not be silently promoted into each other.
- Blanket "login", "paywall", "credential requirement", or "CAPTCHA" stops may
  conflict with the accepted source-access boundary unless narrowed to
  no-entitlement, undisclosed, raw credential/session, private/admin spillover,
  or standalone CAPTCHA-solving cases.
- Any monitored thread set likely needs both named cadence and stop date; no
  indefinite monitoring.
- The artifact should define the line between a one-off local planning/state
  table and separately authorized storage/consolidated output.

## Candidate Success-Signal Gates

The architecture pass must decide whether to accept, modify, or reject these
gates:

| Gate | Candidate requirement |
| --- | --- |
| `decision_frame_or_candidate_intake_classified` | Each Reddit unit is classified as Decision-Frame-bound Data Capture or pre-decision candidate/scouting context; only the former can claim Data Capture handoff posture. |
| `bounded_source_set_pass` | Source set is named by subreddit/theme/query/thread family/small monitored set plus purpose, exclusions, time cutoff, volume ceiling, cadence if any, and stop date if monitored. |
| `method_order_observed` | CloakBrowser old Reddit HTML first once implemented; archive fallback/historical support; `.json` only observed opportunistic fallback; commercial/API route after commercial trigger. |
| `method_provenance_recorded` | Capture method, source surface, backend, access posture, anti-blocking/JS-challenge category if used, fallback posture, packet path, raw file pointer, and limitations are visible. |
| `disclosability_pass` | Orca can disclose exactly how the source was obtained; no stolen credentials/cookies, raw profile import, nonconsensual session, no-entitlement bypass, private/admin spillover, secret-bearing packet, or internally non-disclosable method. |
| `packet_before_parser_pass` | Raw/body-equivalent material is preserved in a Source Capture Packet before parser/consolidation output is trusted. |
| `parser_derivative_pass` | Parser output points back to packet-owned source body, carries parser warnings, and never becomes the canonical source body. |
| `obligation_visibility_pass` | Contract version, operator/session provenance, mode/mode changes, timing/cutoff, archive/access/visibility, recapture, limitations, and relevant obligation states are visible or marked unknown with reason. |
| `related_thread_context_pass` | Thread slice preserves enough parent/reply/correction/rebuttal/confirmation/moderator/official/lock/edit/delete/exclusion context for ECR reconstruction floor and fairness ceiling. |
| `lifecycle_sensitivity_pass` | Packet lifecycle, sensitivity note, retention basis, allowed downstream use, and fixture-admission state remain visible. |
| `source_quality_compatibility_pass` | Rows do not claim source-quality success unless mapped to Mini God-Tier vocabulary and operator-finalized report blocks under the existing profile. |
| `planning_only_pass` | Consolidation remains a planning/state artifact; no database, durable corpus, queue, scheduler, dashboard, production monitor, fixture admission, ECR, Cleaning, Judgment, or client-facing role without separate authorization. |
| `commercial_transition_check` | Client-funded, commercial, enterprise, buyer-facing durable use, scale pressure, or data-licensing pressure triggers stop-and-reroute to sanctioned Reddit API/licensing path. |

## Options To Compare

Treat these as candidates, not defaults:

- **A. Patch current artifact with a Success Signals section only.**
  Smallest edit, but may leave row-shape and Decision Frame ambiguity.
- **B. Add Success Signals plus a Success/Non-Success Ladder.**
  Separates planning, packet, parser, consolidation, source-quality, and batch
  states.
- **C. Add Success Signals plus an Armory Bridge section.**
  Names how Reddit rows later map to source-quality queue/profile/state
  assembler without becoming those outputs.
- **D. Split into two artifacts.**
  One for Decision-Frame-bound Data Capture Reddit units and one for
  pre-decision candidate/scouting posture. Heavier, but may be cleaner if the
  standing-corpus risk cannot be patched inline.
- **E. No patch yet.**
  Return a blocker if source context shows the open owner decisions are too
  large for this architecture pass.

## Decision Criteria

The selected architecture should:

- optimize for Armory integration, not Reddit scraping volume;
- preserve commissioned-capture-only Data Capture v0;
- make candidate/scouting posture visible when no Decision Frame exists;
- keep Source Capture Packet as the source body/provenance owner;
- keep parser and consolidation derivative;
- reuse Source Capture Armory lifecycle, source-quality, queue, and assembler
  vocabulary;
- preserve disclosability and hard stops;
- make broad crawling, indefinite monitoring, storage, production runtime, ECR,
  Cleaning, Judgment, validation, readiness, fixture admission, and commercial
  use impossible to claim by implication;
- name exact patchable success-signal clauses.

## Target Artifact Contract

Write the architecture routing object to:

`docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`

Use this structure:

1. Title.
2. Retrieval header.
3. Status and non-executing boundary.
4. Source readiness and preflight receipt.
5. Evidence mode: `delegated_three_subagents`, `plain_model_local_fallback`, or
   blocked.
6. Subagent summaries: directional, adversarial, grounding.
7. Real architecture question.
8. Current artifact diagnosis.
9. Options compared.
10. Recommended architecture result:
    - `TARGET_RECOMMENDED`
    - `OPTIONS_COMPARED_NO_SELECTION`
    - `NEEDS_OWNER_DECISION`
    - `NEEDS_SOURCE_CONTEXT`
    - `AUTHORITY_BLOCKED`
11. Recommended success-signal structure.
12. Exact patch clauses to apply to the Reddit planning thread.
13. Armory bridge vocabulary to reuse and vocabulary to avoid.
14. Open owner questions.
15. Deferred implications.
16. Non-claims.
17. Smallest complete next authorized step.

Do not update the Reddit planning thread itself unless the launch instruction
explicitly grants patch authority for that file.

## Quality Gates

The output must be able to fail these gates:

- Source readiness declared before method application.
- Exactly three advisory subagent lanes launched if available, or a strict
  blocker/local-fallback disclosure if not.
- Decision Frame versus candidate-intake distinction addressed.
- Success signals are concrete gates, not prose aspirations.
- Tiered success/non-success states prevent promotion from packet -> parser ->
  row -> source-quality -> batch verdict -> fixture/ECR/Judgment.
- Existing Armory vocabulary is reused; parallel lifecycle/result/row-status
  vocabulary is not invented.
- Login/paywall/CAPTCHA/credential wording matches the accepted boundary.
- Commercial/API transition trigger is explicit.
- Storage/consolidated-output boundary is explicit.
- No validation, readiness, implementation, live Reddit, storage, production,
  ECR, Cleaning, Judgment, fixture admission, buyer proof, or commercial-use
  claim is made.

## Chat Closeout Contract

After writing the target architecture artifact, return:

- artifact path;
- architecture result;
- evidence mode;
- three subagent lane receipts;
- highest-risk finding;
- recommended next authorized step;
- statement that no implementation/runtime/live Reddit/storage/ECR/Cleaning/
  Judgment work was performed or authorized.

Do not stage, commit, push, or open a PR unless separately instructed.
