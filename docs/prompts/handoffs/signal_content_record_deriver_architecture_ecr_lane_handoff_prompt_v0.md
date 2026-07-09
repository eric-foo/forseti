# Handoff — Signal Content Record Deriver: Architecture-First Slice (ECR-Consolidation Lane) v0

```yaml
retrieval_header_version: 1
artifact_role: Cross-lane handoff prompt (architecture commission)
scope: Cold handoff commissioning the ECR-consolidation lane to ARCHITECT (not yet build) the Signal Content Record deriver — the deferred interpretive extraction step (raw observation -> signal_family + event-core -> filled SignalContentRecord), the next derived-record kind after SP-6.
use_when:
  - Picking up the Signal Content Record deriver slice in the ECR-consolidation lane.
  - Deciding the derivation/extraction contract before any deriver build.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
  - forseti-harness/signal_content/models.py
  - forseti-harness/ecr/__init__.py
```

You are a fresh reader. Treat this packet as a pointer, not as authority:
**confirm-don't-trust**. Verify every pinned commit, path, and claim below
against a fresh read of the live repo before acting. The branch is active and
its worktree is heavily dirty (many unrelated other-lane untracked/modified
files); rely on the **named, pinned source files**, not on a clean tree.

---

## 1. Goal Handoff / Active Objective

Produce the **derivation architecture** for the Signal Content Record — the
deferred interpretive extraction step that turns a captured raw observation into
a filled `SignalContentRecord` (`raw_observation` -> `signal_family` +
event-core + the optional generic sub-objects), keyed to an existing
`SourceCapturePacket`. This is the **next derived-record kind after the ECR
SP-1/2/3/6 source-side derivers**.

**Architecture-first, not a build.** The v0 *model* already exists and is green
(see §3). What is undecided — and what this commission must settle — is the
**extraction contract**: the brief flags that the extraction "likely needs a
provenance-bound **authored** input, residualized when absent — like SP-5's
deferred finalizer." That authored-input question is the load-bearing design
uncertainty. Do not build past it; architect it first.

`anchor_goal`: a re-derivable, honesty-preserving content-extraction contract
that a later (separately authorized) build can implement without inventing
family or content.
`success_signal`: the architecture lets a build derive filled records from real
packets, residualize cleanly when the authored input is absent (never invent),
and re-derive from the still-frozen raw observable rather than migrate a stored
column.
`long_term_goal` (horizon only): the Core Spine content layer feeds Cleaning ->
ECR -> Judgment by reference; this slice is one page of that build-up.

## 2. Preflight (`orca_start_preflight` — complete before APPLY)

- `agents_md_read`: REQUIRED — read `AGENTS.md` and
  `.agents/workflow-overlay/README.md` in this task context first; then the
  overlay files they route to (source-of-truth, source-loading, safety-rules,
  decision-routing). They are modified in the worktree (other-lane) — read them
  fresh.
- `source_pack`: bounded custom pack (see §3); budgets owned by
  `.agents/workflow-overlay/source-loading.md`.
- `repo_map_decision`: `not_needed`. `repo_map_reason`: the pack is named
  explicitly; the controlling brief orients. (The record is registered in the
  working copy of `docs/workflows/orca_repo_map_v0.md` Core Spine Files + Orca
  Harness, if you want the map view.)
- `workspace`: the Orca repo (`.../projects/orca`).
- `branch`: `ecr-sp3-timing-deriver-slice1`. **Active/shared — HEAD advances.**
  Do not pin to HEAD; pin to the source commits in §3.
- `dirty_state_allowance`: worktree is dirty with extensive unrelated other-lane
  untracked + modified files. **Out of scope.** Treat the pinned files as truth;
  do not clean, revert, or commit other lanes' work.
- `controlling_source_state`: the brief + the model + tests are committed/clean
  at `834c930`; ECR SP-6 at `6329d71`. Overlay + repo map are modified
  (other-lane) — read fresh, do not trust cached state.
- `doctrine_surfaces`: this work is `architecture_doctrine` + `lifecycle_boundary`
  (it designs a derived-record producer that steps toward Cleaning/binding). The
  architecture doc you produce MUST carry a `direction_change_propagation`
  receipt (see §8).
- `target`: ONE new architecture/plan doc under `docs/product/` (follow the SP-6
  precedent `docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md`);
  suggested slug `signal_content_record_deriver_architecture_plan_v0.md`. Final
  placement/slug is the lane's call.
- `source_hierarchy`: `AGENTS.md` -> overlay (`source-of-truth.md`) -> the brief
  (controlling owner doc) -> boundary doc -> model/ECR source.
- `edit_permission`: **`docs-write`** — the architecture doc only. NOT
  implementation. The deriver build is a separate, later authorization.
- `output_mode`: `file-write` (one architecture doc) + a chat closeout summary.
- `validation_gate`: the architecture-planning quality bar (below); no code, so
  no test run this turn — instead the doc must *name* the build's validation
  expectations.
- `external_source_boundary`: `jb` is NOT Orca authority; external/installed
  workflow source is read-only. Use Orca overlay + the named Orca docs only.

## 3. Source Hierarchy & Required Reads (bounded custom pack — cite, verify)

| Read | Why | Pin |
| --- | --- | --- |
| `docs/product/core_spine_v0_signal_content_record_architecture_v0.md` | **Controlling owner doc.** Esp. "Deferred — NOT authorized here" + "Carry-don't-coin + evolution" + the shape. | committed `834c930` |
| `orca-harness/signal_content/models.py`, `__init__.py` | The built v0 model you derive INTO (`SignalContentRecord`, `ContentReferences`, `Delta`, `Reaction`, `SignalEventTimeReference`, closed `SignalFamily`/`DecisionRelevance`). | committed `834c930` |
| `orca-harness/ecr/` (module + `__init__.py`) and the SP-6 source-visibility deriver | **The pattern to reuse**: M1-carry / M2-derive / M3-residual; "a parallel record the frozen conductor reads, binds no EvidenceUnit". | SP-6 at `6329d71` |
| `docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` and `..._routing_v0.md` | The SP-6 derivation architecture/routing precedent — match its shape. | verify in tree |
| The ECR-consolidation v0 plan (e.g. `docs/prompts/reviews/ecr_consolidation_v0_plan_cross_family_review_patch_prompt_v0.md` and its review output) | Where this slice slots in as "the next derived-record kind after SP-6". | verify in tree |
| `orca-harness/source_capture/models.py` | `VisibleFact` (honesty), `PacketTiming` (the 5 timing fields), `SourceCapturePacket`/`SourceCaptureSlice` (the keys you reference). | verify in tree |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | The boundary: reserved Evidence-Unit field architecture, JSG-01 frozen, Signal-Use ownership. | verify in tree |

## 4. Method Sequencing (Source-Gated Method Contract)

1. Read authority + operating instructions (§2).
2. **REFERENCE-LOAD** `workflow-architecture-planning` (and
   `workflow-deep-thinking` for framing the authored-input question). Do **not**
   APPLY yet — only prepare neutral source-reading lenses.
3. **SOURCE-LOAD** the §3 pack and build the working source context.
4. Declare `SOURCE_CONTEXT_READY` (or `SOURCE_CONTEXT_INCOMPLETE` with the gaps).
5. Only then **APPLY** architecture-planning to the loaded context and produce
   §6.
6. Synthesize and verify each claim against the source context.

## 5. The Load-Bearing Question (settle this first)

**Where does the authored `signal_family` + event-core come from, and what
happens when it is absent?** The brief likens it to SP-5's deferred finalizer,
which was deferred precisely because a provenance-bound authored input was not
available. So, against source, decide:

- Is the extraction an **authored** step (a model/human producing the
  classification + event-core), a **mechanical** M2-derive, or a split?
- What is the provenance binding of the authored input, and how is it carried
  (an authored-input record? a finalizer like SP-5)?
- What is the **residualize** path when the authored input is absent or
  low-confidence — `signal_family = RESIDUAL_FAMILY_UNRESOLVED`, `VisibleFact`
  unknown-with-reason for the content fields — so "not extracted" stays distinct
  from "no such content"?

Treat the **authored-input-exists** premise as a verify-against-source assumption
(an explicit pre-build assumption-gate item), not a given.

## 6. Output Contract — the architecture doc must contain

1. **Extraction contract**: inputs (the packet/slice + raw observation + any
   authored input), output (a filled `SignalContentRecord`), and the
   authored-vs-mechanical split from §5.
2. **Per-field M1/M2/M3 mapping**: for each `SignalContentRecord` field, whether
   it is carried (M1), derived (M2), or residual (M3), and from what source.
3. **Residualize + honesty rules**: unknown family -> `RESIDUAL_FAMILY_UNRESOLVED`;
   absent/uncertain content -> `VisibleFact` unknown-with-reason; never invent
   family or content. The `decision_relevance` tag stays a neutral mechanical
   routing tag (no graded Signal-Use verdict).
4. **Emit timing**: the deriver runs only AFTER a candidate is promoted and a
   `SourceCapturePacket` exists — NOT from Reddit candidate-intake discovery rows
   (those are upstream of capture).
5. **Re-derive lifecycle**: a derived/re-derivable read from the frozen raw
   observable; family-taxonomy change is a re-derive, never a stored-column
   migration. Read-checked `_vN`; additive family-enum growth.
6. **Bounded build scope it tees up** + what stays deferred (see §7).
7. **The smallest-complete next routing object** (architecture-planning's
   deliverable) — what the build lane receives.
8. A `direction_change_propagation` receipt (§8) and explicit non-claims.

## 7. Frozen Boundaries (DO NOT cross)

- **Scope = derivation architecture ONLY.** Explicitly NOT authorized here:
  the deriver build itself, persistence/finalizer, any packet->`EvidenceUnit`
  binding, Cleaning, Judgment, commits/pushes — each is a separate owner gate.
- The final Evidence Unit field architecture stays **owner-reserved**; **JSG-01
  stays FROZEN**; the prior #4 ratification covered the **MODEL only**, not the
  deriver/binding.
- **Never invent family or content.** Unknown -> residual; absent -> honest
  `VisibleFact`. No cross-source aggregate (sensitivity curve, sentiment trend,
  switching-is-accelerating) — those are Judgment-owned and never fields here.
- Content links to provenance/integrity **by key, never merged**.
- Wedge-agnostic: bake no wedge into the core; wedge richness lives in
  `family_detail` values only.

## 8. Doctrine Propagation (required)

This is `architecture_doctrine` + `lifecycle_boundary`. The architecture doc must
carry a `direction_change_propagation` receipt per
`.agents/workflow-overlay/source-of-truth.md`, with downstream surfaces to check
on finalize at least: the brief, the boundary doc, the IPF Evidence Unit
Standard, `source-of-truth.md`, `docs/workflows/orca_repo_map_v0.md`, and
`docs/workflows/data_capture_spine_consolidation_map_v0.md`. If you cannot bind
the receipt, return `direction_change_propagation_blocker` and stop before strict
closeout.

## 9. Fitness Reference

Anchor decision criteria to: **a content-extraction contract that stays honest
under absence** (residualizes, never invents) and is **re-derivable from frozen
raw**. The brief is the fitness anchor; if a checkable success bar is missing,
name the gap (`no checkable success bar bound`) rather than invent one.

## 10. Validation / Quality Gate

No code this turn. The doc passes when: it settles §5; every §6 item is present
and source-backed; the frozen boundaries (§7) are intact; the DCP receipt (§8)
is bound; and it **names the build's validation expectations** (e.g. the same
round-trip / closed-enum / residualize-honestly / key-integrity discipline the
existing model tests use — `orca-harness/tests/unit/test_signal_content_models.py`).
No readiness, validation-pass, JSG-01-unfreeze, or implementation claim.

## 11. Assumptions, Unknowns, Blocked Conditions

- **Assumption to verify (not trust):** a provenance-bound authored input for
  `signal_family` + event-core is producible. If source shows it is not (as for
  SP-5), the architecture must default to the residualize path and say so — that
  is a finding, not a blocker.
- **Unknown:** exact placement/slug of the architecture doc and how tightly the
  ECR-consolidation v0 plan wants this slice sequenced — resolve from the SP-6
  precedent + the consolidation plan.
- **Block** (`SOURCE_CONTEXT_INCOMPLETE`, `direction_change_propagation_blocker`,
  or `BLOCKED_BY_AUTHORIZATION`) rather than: inventing the authored-input
  contract, building the deriver, touching JSG-01 / Evidence-Unit binding, or
  committing.

Apply the shared Orca prompt behavior contract
(`docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`).
