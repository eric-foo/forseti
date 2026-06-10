# Packing Phase To v0.14 Judgment Harness Foundation Interface Architecture CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Saved Chief-Architect prompt that commissions a docs-only workflow-architecture-planning lane for the Packing Phase -> Judgment Harness Foundation interface.
use_when:
  - Re-running or auditing the Packing -> Harness Foundation interface architecture decision.
  - Authoring a follow-up CA prompt for the same boundary (e.g., a v1 rerun, a second non-Unity pressure test, or an owner-acceptance review).
  - Checking which source pack, subagent contract, hard boundaries, output path, and result vocabulary were bound when the v0 architecture artifact was produced.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v0.md
  - docs/research/packing-phase/README.md
  - docs/research/judgment-spine/harness/v0_14/index.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
input_hashes:
  docs/research/packing-phase/README.md: E108281113DA1C27DB241BBB600B19D79334CB407707C6234EE1E1264626EF06
  docs/research/judgment-spine/harness/v0_14/index.md: 59194297235C65E099C356D5141C6B2D64C4E21AECD5A1F13CD364BAD37F7163
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md: 4AF1F45964DBB560D7C6E02827BC30A9161D4433EA754580239C122DAEF532A5
branch_or_commit: main @ b7627d3 (dirty pre-existing workspace state allowed and reported)
stale_if:
  - Any pinned task-source hash changes materially.
  - v0.14 is superseded by a later harness version.
  - Packing Phase ownership or output obligations are materially changed.
  - Orca accepts a different Data Capture, Cleaning, Packing, Judgment, or Harness phase boundary.
  - The target architecture artifact path is renamed, retired, or superseded.
downstream_consumers:
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v0.md
```

- Status: SAVED_PROMPT_V0
- Artifact type: Full prompt artifact (workflow-architecture-planning commission)
- Output mode used for this prompt artifact: file-write
- Output mode the prompt itself commissions: file-write (architecture artifact) plus optional narrow discovery pointers
- Implementation authorized: no
- Runtime, package, test, automation, probe execution, model run, scoring run, validation execution, proof-run, product-proof, lesson-promotion, commit, push, or PR authorized: no
- Strict readiness, validation, acceptance, source-of-truth promotion, probe-pass, score-readiness, implementation authorization, harness superiority, product-proof, buyer-proof, memory compounding, or lesson-promotion claims: not proven

## Saved-Prompt Use Boundary

This file is the saved CA prompt that was used to produce the Packing -> Harness Foundation interface architecture artifact under `workflow-architecture-planning`. It is a durable prompt artifact for future retrieval and rerun, not an execution authorization, not a verdict, not validation, and not implementation authority. Reading this prompt does not re-run the architecture-planning lane; only an explicit invocation of `workflow-architecture-planning` with the bindings below does.

The retrieval header is `retrieval_only`. It does not upgrade the saved prompt into Orca authority beyond what the prompt body and overlay already grant. If the architecture artifact body, the overlay, an accepted Orca source, or a later user instruction conflicts with this prompt, the saved prompt loses.

## Prompt Body (verbatim)

The text below is the controlling user prompt that commissioned the v0 architecture artifact. It is preserved verbatim. Do not edit clauses, source pack, hashes, hard boundaries, or closeout shape when rerunning. If a rerun needs different bindings, save a new prompt artifact (v1) with a `supersedes:` link rather than mutating this one.

---

# Orca Architecture Planning Prompt: Packing -> Harness Foundation Interface

You are operating inside the Orca repo:

`C:\Users\vmon7\Desktop\projects\orca`

Run a docs-only `workflow-architecture-planning` lane for the **Packing Phase -> Judgment Harness Foundation interface**.

This is architecture planning only. Do not implement, run probes, score cases, create runtime code, create tests, install packages, run models, claim validation, claim readiness, claim product proof, or promote lessons.

## Goal Context

```yaml
goal_handoff:
  long_term_goal: "Build Orca's Judgment Spine into a trustworthy harness for improving frontier-LLM judgment through clean case inputs, bounded blind judgments, deterministic scoring, and failure logs without fake validation or product-proof claims."
  anchor_goal: "Define the Packing -> Harness Foundation interface so future CAs/operators know what Packing must produce, what the harness freezes and scores, what remains blocked, and how phase ownership is preserved."
  success_signal: "A future CA or operator can prepare or reject one case before harness execution by checking explicit Packing outputs, Harness freeze inputs, contestant visibility, deterministic checks, report meaning, inadmissibility states, and non-claims."
  status: user_stated_for_this_prompt
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal
  drift_guard: "Do not substitute Unity fixture polish, broad harness implementation, or template/overlay hygiene for the Packing -> Harness Foundation interface decision."
  conflict_behavior: call_out_conflict_before_proceeding
```

## Required Method

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read the required overlay files named below.
4. REFERENCE-LOAD `workflow-architecture-planning`.
5. Do not APPLY architecture planning until task sources are loaded.
6. SOURCE-LOAD the bounded source pack below.
7. Declare:

```yaml
source_context_status: SOURCE_CONTEXT_READY
```

or:

```yaml
source_context_status: SOURCE_CONTEXT_INCOMPLETE
missing_or_mismatched_sources:
  - ...
```

8. After source context is ready, APPLY `workflow-architecture-planning`.
9. Use **standard profile**.
10. Explicitly launch **exactly three advisory architecture subagents** if the host supports subagents:
    - Directional subagent: strongest source-backed case for the best target interface architecture.
    - Adversarial subagent: strongest case against that target, including coupling, boundary leakage, fake-success paths, hidden implementation gravity, and overfitting to Unity.
    - Grounding subagent: repo-native, source-bounded, anti-bloat, reversible where possible; identify what to cut or defer.

Subagents are advisory inputs only. They are not verdicts, validation, readiness, implementation authority, or proof. Use inherited/default runtime settings; do not recommend or route runtime model choice.

If subagents are unavailable, return `BLOCKED_SUBAGENTS_UNAVAILABLE` and do not pretend local passes were delegated subagents.

## Workspace Preflight

Expected branch/head:

```yaml
branch: main
head: b7627d3
```

Dirty state is allowed but must be reported. Modified or untracked sources may support working architecture planning, but they do not prove acceptance, validation, readiness, source-of-truth promotion, implementation authorization, or product proof.

## Required Overlay Sources

Read:

- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/review-lanes.md`
- `docs/workflows/orca_repo_map_v0.md`

## Required Task Sources

Verify these current hashes before using them for strict source-pinning claims:

- `docs/research/packing-phase/README.md`
  - `E108281113DA1C27DB241BBB600B19D79334CB407707C6234EE1E1264626EF06`

- `docs/research/judgment-spine/harness/v0_14/index.md`
  - `59194297235C65E099C356D5141C6B2D64C4E21AECD5A1F13CD364BAD37F7163`

- `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`
  - `1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192`

- `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`
  - `DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7`

- `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`
  - `4AF1F45964DBB560D7C6E02827BC30A9161D4433EA754580239C122DAEF532A5`

Also read, targeted from the v0.14 index as needed:

- `judgement_case_construction_protocol.md`
- `pydantic_schema_reference.md`
- `blind_judgement_schema_and_harness_protocol.md`
- `band_input_labeling_rubric.md`
- `action_band_mapping_table_numbers.md`
- `action_band_mapping_executable_spec.md`
- `scorer_formula_spec.md`
- `memorization_probe_protocol.md`
- `failure_event_log_spec.md`
- `proof_and_memory_plan.md`
- `phase_1_infrastructure_architecture.md` only for deferred implementation implications, not implementation authorization.

Concrete exemplar sources are optional and should be targeted only if needed to test the interface against a real case:

- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md`
- `participant_packet_draft_v0.md`
- `evidence_registry_draft_v0.md`
- `facilitator_ledger_draft_v0.md`
- `sealed_memo_adapter_note_v0.md`
- PP-01 closure review, if available.

Do not make the architecture Unity-specific. Unity is an exemplar, not the interface owner.

## Architecture Question

What target architecture should govern the boundary between Packing Phase outputs and Judgment Harness Foundation inputs, so that:

- Packing can transform cleaned evidence into judgment-ready case artifacts;
- Harness can freeze inputs and run deterministic checks without absorbing Packing, Cleaning, Data Capture, or lesson-promotion responsibilities;
- future implementation scoping has a stable interface;
- missing provenance, leakage, unresolved evidence adapters, or missing labels block admission instead of being silently repaired by the harness?

## Options To Compare

Compare at least these options unless source context eliminates one:

1. Cleaning feeds Harness directly.
2. Packing produces a formal Harness Entry Bundle consumed by Harness.
3. Harness owns packing/admission internally.
4. Case-specific fixture authoring remains manual with no general interface.
5. Hybrid: Packing owns bundle construction, Harness owns freeze/admission/scoring contract, with a small adapter layer for case-specific gaps.

## Required Output Artifact

Write a docs-only architecture artifact to:

`docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v0.md`

If that path already exists, use the next version suffix or return a visible collision blocker.

Use retrieval metadata. Include at minimum:

- source context receipt;
- architecture frame;
- subagent evidence disclosure and three subagent summaries;
- questions this architecture decision must answer;
- option comparison;
- target architecture result;
- selected or deferred target architecture;
- core/satellite boundaries;
- Packing-owned outputs;
- Harness-owned freeze inputs;
- contestant-visible boundary;
- deterministic scoring/checking boundary;
- report meaning and non-meaning;
- inadmissibility/block states;
- deferred implementation implications;
- what is intentionally undecided;
- what would change the recommendation;
- bloat-cut queue;
- non-claims;
- smallest complete next routing object;
- source-read ledger.

Allowed docs-write scope:

- the target architecture artifact;
- at most narrow discovery pointers in `docs/research/judgment-spine/harness/v0_14/index.md`, `docs/research/packing-phase/README.md`, or `docs/research/judgment-spine/manifest_v0.md` if needed for future retrievability.

Do not update broader repo maps unless you can name a concrete future-agent failure if unchanged.

## Required Architecture Result Vocabulary

Return exactly one:

- `TARGET_RECOMMENDED`
- `OPTIONS_COMPARED_NO_SELECTION`
- `NEEDS_ARCHITECTURE_QUESTION`
- `NEEDS_PRODUCT_DECISION`
- `NEEDS_FEATURE_PLANNING`
- `NEEDS_SOURCE_CONTEXT`
- `DEFER_OR_REJECT`
- `AUTHORITY_BLOCKED`
- `BLOCKED_SUBAGENTS_UNAVAILABLE`

## Hard Boundaries

Do not authorize:

- implementation;
- runtime architecture;
- package/test/build work;
- probe execution;
- model runs;
- scoring runs;
- validation claims;
- source-of-truth promotion;
- acceptance;
- product proof;
- buyer proof;
- lesson promotion;
- harness superiority;
- memory compounding.

## Closeout

Return a compact human summary plus this YAML:

```yaml
architecture_planning_summary:
  status: completed | blocked
  artifact_path:
  architecture_result:
  target_recommended: yes | no
  subagents_launched: 3 | 0
  recommendation_summary: ""
  changed_files: []
  navigation_pointers_changed: []
  blockers: []
  not_proven:
    - validation
    - readiness
    - implementation_authorization
    - scoring
    - probe_pass
    - product_proof
    - lesson_promotion
  next_authorized_step: ""
```

---

## Rerun Notes

If rerunning this prompt verbatim:

- Recompute each pinned task-source hash before strict source-pinning claims. Hashes drift when an upstream artifact is patched; treat any mismatch as a `SOURCE_CONTEXT_INCOMPLETE` blocker.
- Workspace preflight `head: b7627d3` is the head at original authoring time. Recheck `git rev-parse HEAD` and `git status` and report new state; do not silently accept divergence.
- Treat the collision rule on the architecture artifact path as binding. If `packing_to_harness_foundation_interface_architecture_v0.md` exists at rerun time, either bump to `_v1.md` with a `supersedes:` retrieval-metadata link, return a visible collision blocker, or replace v0 only after explicit current-turn owner authorization.
- Do not edit the prompt body inline. If a rerun needs different bindings (new source pack, new options, new closeout shape, different hard boundaries), save a new prompt artifact (v1) with a `supersedes:` link and a clear binding-delta note rather than mutating this one.
- Do not import jb prompt templates, GAP/CV Engine paths, compiler paths, handoff rules, product-lead rules, or repo-local lifecycle mechanics. Do not recommend or route runtime model choice for review or subagent lanes.
- Subagents must use inherited/default runtime settings. If delegation is unavailable, return `BLOCKED_SUBAGENTS_UNAVAILABLE` and do not pretend local passes were delegated subagents.

## Non-Claims

This saved prompt does not claim:

- Judgment Spine validation.
- v0.14 harness validation.
- case admission, score-readiness, or probe-pass for any case.
- participant-packet cleanliness for blind use.
- implementation readiness.
- source-of-truth promotion.
- acceptance or approval of the v0 architecture artifact body beyond what its own non-claims section says.
- buyer validation, product readiness, feature readiness, commercial readiness, or model-training readiness.
- harness superiority, baseline comparability, or semantic evidence support.
- lesson transfer, lesson promotion, or memory compounding.
- that any subagent output is verdict, implementation authority, validation, readiness, or proof.
- that dirty or untracked sources are accepted authority.
- that this prompt itself authorizes runtime design, schemas, scrapers, automation, tests, packages, commits, pushes, PRs, proof runs, or feature planning.
