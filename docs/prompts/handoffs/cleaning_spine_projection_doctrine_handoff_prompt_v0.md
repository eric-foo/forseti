# Cleaning Spine Foundation - Projection Doctrine Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Cold-start handoff for a Cleaning Spine foundation lane that consumes the
  Projection Doctrine v0 candidate kept in PR #191, preserves the
  Data Capture / Evidence Candidate Record / Cleaning / Judgment split, and
  produces a docs-only Cleaning Spine foundation artifact.
use_when:
  - Starting the Cleaning Spine foundation lane after or alongside PR #191.
  - Checking whether Cleaning work may begin from Projection Doctrine v0 without waiting for platform-complete capture data.
  - Preventing Cleaning from absorbing Projection or Judgment responsibilities.
authority_boundary: retrieval_only
load_rule: confirm-don't-trust - re-read every named source before strict or actionable claims.
workspace: C:\Users\vmon7\Desktop\projects\orca
expected_branch_or_source: >
  Prefer main after PR #191 lands; before merge, use PR #191 / branch
  codex/projection-reddit-enforcement and re-check the current head on intake.
output_mode: file-write
target_output: docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md
edit_permission: docs-write only; no implementation, runtime, adapter, crawler, scraper, schema, or proof-run work.
commit_policy: ask the owner at lane start unless the launching turn explicitly grants commit/push.
prompt_contract: >
  Authored under workflow-prompt-orchestrator and workflow-handoff contracts:
  source-gated method sequencing, cold-reader self-containment, front-loaded
  goal/open-decision/drift-guard, and Orca overlay-owned output mode.
```

## What This Is For

```yaml
goal_handoff:
  long_term_goal: >
    Set up Orca's cleaning path so scanned, captured, projected, and raw public
    source material can become smaller, traceable, Judgment-usable working
    material without losing raw evidence or smuggling interpretation.
  anchor_goal: >
    Produce the first Cleaning Spine foundation artifact: the layer contract,
    allowed transforms, ledger obligations, raw/projection/cleaned relationship,
    raw-pull triggers, and installed owner-decision gates.
  success_signal: >
    A cold reader can tell, for any projected or raw source slice, what Cleaning
    may transform, what it must preserve and link, what it must defer to
    Judgment, and when it must pull raw or escalate an owner decision.
```

This is a planning handoff, not a request to build Cleaning code. The receiver's
first deliverable is the target output above, or a blocker explaining why that
artifact cannot be written without changing authority.

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: different_workstream
  changed_from_input: yes
  lifecycle_status: new_cleaning_lane_from_projection_closeout
  if_changed_reason: >
    The projection lane is closing into PR #191; this prompt starts the next
    Cleaning Spine foundation lane and does not carry projection-lane completion
    state as an active target.
```

## Installed Decisions First

Owner directions the Cleaning lane must carry without widening:

- **OD-1 / pipeline ordering:** Cleaning uses one input handle keyed to raw,
  with optional projection and ECR references attached when present. Projection
  and ECR remain keyed siblings over raw for Cleaning purposes; transform
  entries must not carry brittle triplicate references.
- **OD-4 / where dedupe and clustering live:** Cleaning core v0 may define
  exact-identity dedupe mechanics only. Near-match dedupe, copied-language
  grouping, and clustering remain candidate/deferred mechanics unless
  separately owner-authorized. Any independence, credibility, uncertainty,
  exclusion, Signal Integrity, Decision Strength, or Action Ceiling effect
  belongs to Judgment Spine.
- **OD-7 / naming and object model:** "Projected Unit" is a working label for
  the existing Data Capture Projection Packet row view. Do not promote
  "Projected Unit", "Cleaned Unit", or any new object into canonical spine
  ontology.

Recommended lane posture: proceed with the Cleaning foundation contract now,
while keeping those installed directions as visible constraints and blockers
where implementation would otherwise widen them into schema/runtime choices.

## Drift Guard

Hard constraints:

- Projection Doctrine v0 is a **candidate kept by vendor CA for owner
  confirmation**, not ratification, validation, readiness, or buyer proof.
- Projection is Data Capture-owned Mechanical Source Projection / Data Capture
  Projection Packet. It is not a new spine layer and not source truth.
- Raw source remains canonical. Projection and Cleaning are working views with
  traceability obligations.
- Cleaning must not remove evidence rows because they look low-value,
  low-score, repetitive, embarrassing, bot-like, deleted, awkward, or
  unhelpful.
- Cleaning must not decide credibility, discounting, exclusion, demand support,
  independence effect, Signal Integrity, Signal Use, Decision Strength, or
  Action Ceiling.
- Cleaning inclusion or blocker reasons must be mechanical-status reasons only.
  Do not use Judgment reasons such as `discounted`, `excluded`, `weak`,
  `strong`, `credible`, `not credible`, `supports demand`, or `action
  supporting`.
- Summaries, translations, normalizations, dedupe groups, and clusters must be
  non-destructive: originals stay addressable, counts stay visible, and every
  transform has raw/projection anchors.
- Compactness is never salience. Salience is frame-bound and belongs downstream;
  Cleaning may carry, residualize, or flag ambiguity, not decide what matters.
- No source-family rule may silently become universal. Declare each rule as
  source-invariant core, source-family adaptation, or unresolved candidate.
- No live capture, public web research, platform crawling, API use, proof run,
  runtime schema, dashboard, or automation is authorized by this prompt.

## Required Source Load

Before producing any recommendation or artifact, do this sequence:

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD, but do not yet APPLY, these method/overlay sources:
   `.agents/workflow-overlay/decision-routing.md`,
   `.agents/workflow-overlay/source-loading.md`,
   `.agents/workflow-overlay/prompt-orchestration.md`, and
   `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.78\skills\workflow-architecture-planning\SKILL.md`
   if you use architecture-planning mechanics.
3. SOURCE-LOAD the task sources listed below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY any planning or architecture method.

Task sources to load:

- `docs/product/core_spine_v0_projection_doctrine_v0.md` - Projection Doctrine
  v0 candidate. If missing on `main`, load PR #191 or block as
  `BLOCKED_MISSING_PROJECTION_DOCTRINE`.
- `docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md`
  - vendor-CA closeout; confirms kept candidate status and residual risk.
- `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  - current Data Capture / Evidence Candidate Record / Cleaning / Judgment
  boundary.
- `docs/product/core_spine/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`
  - dedupe/clustering versus Judgment-owned independence/amplification split.
- `docs/product/data_capture_spine/core_spine_v0_data_capture_context_preservation_note_v0.md`
  - capture-context preservation rules Cleaning must not flatten.
- `docs/workflows/orca_repo_map_v0.md` - only if path placement, source-pack
  selection, or map freshness becomes decision-bearing.

Available but do not load by default:

- Existing source-capture runbooks, Reddit fixtures, or social-platform packet
  examples. Use them only as small specimens if the foundation artifact needs a
  concrete example. Do not turn specimen examples into data requirements.

## Receiver Task

Write `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md`
as a docs-only product-method artifact. If the file already exists, choose the
next version suffix or return a collision blocker before overwriting.

The artifact should answer these questions:

1. What is Cleaning Spine responsible for after raw capture / mechanical source
   projection / Evidence Candidate Record?
2. What transformations are allowed: normalization, translation,
   summarization, dedupe mechanics, clustering mechanics, and receipt/ledger
   propagation?
3. What invariants must every transformation preserve: raw anchor, projection
   anchor where applicable, source identity, timing, hierarchy, bundle
   structure, semantic binding, counts, omissions, residuals, and warnings?
4. What is the minimum transformation ledger contract without freezing a runtime
   schema?
5. When must Cleaning pull raw, halt, or escalate to owner/Judgment?
6. What Cleaning outputs are acceptable inputs to Judgment, and what claims must
   Judgment re-open raw for?
7. What remains deferred or candidate because OD-1, OD-4, or OD-7 is bounded?

Keep the artifact small enough to become a foundation, not a universal source
manual. Use a section for source-family adaptation rules rather than embedding a
Reddit/TikTok/Instagram/retailer/review-site playbook.

## Suggested Foundation Shape

Use this shape unless source loading reveals a better local pattern:

```text
# Core Spine v0 Cleaning Spine Foundation

<retrieval header>

Status / scope / non-claims
Purpose
Layer Boundary
Inputs Cleaning May Receive
Allowed Transform Classes
Non-Destructive Ledger Contract
Traceability And Raw-Pull Rules
Dedupe / Clustering Mechanics
Source-Family Adaptation Boundary
Cleaning-To-Judgment Handoff
Owner Directions Installed
Validation / Review Needed
```

Do not freeze field names beyond illustrative candidates unless the artifact
labels them `candidate` and names the owner direction or separate authorization
that would promote them.

## Validation Gates For The Receiver

Run and record actual outputs:

- `git status --short --branch`
- `python .agents/hooks/check_retrieval_header.py --changed`
- `python .agents/hooks/check_repo_map_freshness.py --changed`
- `git diff --check`

If the receiver touches repo maps or overlay files, run the corresponding
strict checker or record why it was not needed. If the receiver creates only the
Cleaning foundation artifact under an existing mapped folder, a repo-map update
is not automatically required, but the map freshness checker must still be run.

## Output Contract

Return a short closeout with:

- `artifact_path`
- `source_context: ready | incomplete`
- `projection_doctrine_source: main | PR_191 | missing`
- `changed_files`
- `validation`
- `owner_reserved_decisions`
- `non_claims`
- recommended next lane, if any

Do not report Cleaning Spine as validated, ready, buyer-proof, runtime-ready, or
Judgment-quality. A clean checker run means only that the docs artifact has the
expected structural metadata and no mechanical diff issue.

## Superseded / Dangerous-To-Reuse Context

- The old chat-only Cleaning lane handoff said Cleaning should block or produce
  requirements only until Projection Doctrine existed. That is superseded for
  foundation work: Projection Doctrine now exists in PR #191 as a kept candidate.
- "We need all platform data before starting Cleaning" is not the current
  architecture. Cleaning foundation can start from layer contracts and a small
  specimen bench, while preserving source-family adaptation boundaries.
- "Cleaned data replaces raw" is dangerous and false. Raw remains canonical;
  cleaned material is a traceable working view.
- "Projection decides what is important" is dangerous and false. Projection and
  Cleaning preserve inspectability and mechanics; Judgment decides use and
  salience under a decision frame.

## Prompt Verdict At Authoring

```yaml
prompt_verdict: PASS_WITH_WARNINGS
warnings:
  - PR #191 may not be merged when this prompt is used; receiver must re-check current source location.
  - Projection Doctrine v0 is candidate-kept for owner confirmation, not ratified doctrine.
  - This prompt authorizes docs-only Cleaning foundation work, not implementation or proof runs.
```
