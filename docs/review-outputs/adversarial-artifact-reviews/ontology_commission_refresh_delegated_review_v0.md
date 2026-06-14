# Ontology Commission Refresh — Delegated Review-And-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial artifact review-and-patch report
scope: >
  Repo-mode cross-vendor review-and-patch hardening pass for
  docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md.
authority_boundary: decision_input_only
reviewed_by: gpt-5 (OpenAI/Codex)
authored_by: claude-opus-4.8
de_correlation_bar: cross_vendor_discovery
access: repo
status: PATCHED_FOR_CA_ADJUDICATION
```

## Commission

- Original commission prompt: `docs/prompts/reviews/ontology_commission_refresh_delegated_review_patch_prompt_v0.md`
- Reviewed target / bounded editable scope: `docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md`
- Patch authority: delegated review-and-patch repo mode, target file only.
- Report destination: `docs/review-outputs/adversarial-artifact-reviews/ontology_commission_refresh_delegated_review_v0.md`
- Excluded scope: every other path. Source documents and overlay files were read-only / flag-only.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom — target prompt plus current-main demand grammar/gate sources
  repo_map_decision: loaded
  repo_map_reason: locate live grammar sources, gate sources, and proto-schema survey references
  workspace: C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\ontology-commission-refresh
  branch: ontology-commission-refresh
  start_head: d5456b9
  dirty_state_checked: yes
  dirty_state_before_patch: clean
  edit_permission: patch-only on the single target file; report write to commissioned destination
  output_mode: review-report
  external_source_boundary: jb is not Orca authority; no public web research used
```

`SOURCE_CONTEXT_READY` was declared after reading the target, `AGENTS.md`,
`.agents/workflow-overlay/README.md`, `decision-routing.md`,
`delegated-review-patch.md`, `prompt-orchestration.md`,
`source-loading.md`, and the required current-main source pack. I
REFERENCE-LOADed `workflow-deep-thinking` and
`workflow-adversarial-artifact-review` before source readiness, then APPLYed
them after source readiness.

Source basis used for findings:

- Target prompt, pre-patch and post-patch working tree:
  `docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md`
- Current `origin/main` demand-state sources:
  `docs/decisions/orca_product_thesis_consumer_demand_v0.md`,
  `docs/product/product_lead/orca_demand_read_taxonomy_v0.md`,
  `docs/product/product_lead/orca_demand_read_taxonomy_adjudication_v0.md`
- Current `origin/main` gate/wind-caller sources:
  `docs/product/product_lead/orca_buyer_proof_packet_v0.md`,
  `docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md`,
  `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md`,
  `docs/decisions/wind_caller_calibration_carveout_v0.md`

## Review Summary

```yaml
review_summary:
  recommendation: CA_ADJUDICATE_PATCH
  verdict: patched_two_major_findings_no_architecture_pass
  target: docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
  findings:
    - id: AR-01
      severity: major
      status: patched
      summary: Demand-state guidance flattened the two-axis model into a single enum.
    - id: AR-02
      severity: major
      status: patched
      summary: Gate-closure source was treated as proposed and outside the live freshness gate.
  off_scope_flags:
    - OF-01
  next_authorized_action: Home-model CA adjudicates the patch; keep, modify, or reject per change.
  non_claims:
    - not validation
    - not readiness
    - not approval
    - not owner adoption
    - not a source-of-truth promotion
```

## Findings

### AR-01 — Major — Demand-State Was Flattened Into A Single Enum

**Target and purpose.** The target commissions a fresh architecture lane to
design the ontology against the landed 2026-06-14 demand grammar.

**Artifact evidence.** The pre-patch target described `Read` / `Call` /
`Outcome` as carrying a `demand_state` dimension and later proposed
`{durable, transient, manufactured}` as the dimension set. That compressed the
current model's two independent axes into one enum.

**Source evidence.** The controlling thesis says the model has two axes:
durable vs transient for persistence and real vs manufactured for integrity,
with three actionable states and a calling sequence where durability is
observed, not predicted (`origin/main:docs/decisions/orca_product_thesis_consumer_demand_v0.md:81`,
`:86`, `:94`). The taxonomy records the same axis split and says "Hollow" is
retired (`origin/main:docs/product/product_lead/orca_demand_read_taxonomy_v0.md:47`,
`:53`) and later states the read types sort on the two axes before yielding
three actionable states (`origin/main:docs/product/product_lead/orca_demand_read_taxonomy_v0.md:132`).

**Why the strongest defense fails.** The target did name the two axes in the
refresh note, so a careful architect might infer the enum is only shorthand.
But this is a launch prompt for a fresh lane reading only the prompt; the
candidate roster is where the downstream model will likely copy object
semantics. A single `demand_state` enum invites exactly the wrong physical
binding: treating manufactured as a persistence state rather than an integrity
axis that can constrain every real-demand read.

**Patch applied.** The target now says `Read` / `Call` / `Outcome` carry the
two-axis classification, with a derived action state only where useful, and
explicitly forbids collapsing integrity into persistence. Closure is visible at
`docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md:53`
and `:142`.

**Minimum closure condition.** The commission must preserve persistence and
integrity as separate ontology dimensions while allowing a derived action state
for downstream consumers.

**Next authorized action.** CA adjudication of the applied patch.

**Patch queue entry.** Not emitted. This was repo-mode patch execution, not a
read-only patch queue.

### AR-02 — Major — Gate Closures Were Treated As Proposed Instead Of Applied Live Inputs

**Target and purpose.** The target asks the architecture lane to encode G1/G2/G4
as ontology Gate actions/preconditions and to run a base freshness gate before
designing the backbone.

**Artifact evidence.** Pre-patch, the freshness gate only named the live demand
grammar sources, while the source list described
`orca_demand_gate_definition_closures_proposal_v0.md` as "PROPOSED
(owner-gated apply)" and "candidate gate semantics."

**Source evidence.** The gate-closures source is not merely proposed: its header
states the amendments are ratified, recheck-cleared, and applied to live
instruments (`origin/main:docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md:1`,
`:5`, `:20`). It defines G1 as de-correlation by origination rather than raw
venue count, G2 as a gradeable costly-behavior floor, and G4 as org-motion
corroboration separate from G1 (`origin/main:docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md:46`,
`:56`, `:84`). The buyer-proof packet carries the live gate: de-correlated
origination and verb-tiering by commitment (`origin/main:docs/product/product_lead/orca_buyer_proof_packet_v0.md:114`,
`:126`), costly-behavior floor (`origin/main:docs/product/product_lead/orca_buyer_proof_packet_v0.md:155`),
and one-origin/low-commitment vs two-origin/material-action tiering
(`origin/main:docs/product/product_lead/orca_buyer_proof_packet_v0.md:194`).
The discovery brief on current `origin/main` has the applied slot column and
qualification objective wording (`origin/main:docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md:66`,
`:75`, `:107`).

**Why the strongest defense fails.** The target's refresh note did mention
G1/G2/G4 and "now defined," so the architecture lane would probably discover
some live semantics. But the SOURCE-LOAD line is the operational instruction;
calling the source "PROPOSED" tells the lane to treat gate semantics as
candidates rather than live owner-applied constraints. That is materially wrong
for a backbone commission.

**Patch applied.** The base freshness gate now includes live demand-grammar /
gate sources and requires verification of both the 2026-06-14 demand-state
model and the applied gate-closure model. The source list now marks the gate
closure source as `LIVE (verify, don't pin)` and `APPLIED`, with stale raw
venue-count wording flagged for consumers. Closure is visible at
`docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md:190`
and `:228`.

**Minimum closure condition.** The commission must force the architecture lane
to treat G1/G2/G4 as live applied gate semantics, not a proposed candidate set,
and must verify current-main gate wording before launch.

**Next authorized action.** CA adjudication of the applied patch.

**Patch queue entry.** Not emitted. This was repo-mode patch execution, not a
read-only patch queue.

## Off-Scope Flags

### OF-01 — Source Corpus Retains Some Decay-Timing Residue

The target now avoids encoding the old decay-timing-confidence guardrail.
However, source documents still contain older residue in non-target areas: the
adjudication companion's dated update says decay-timing confidence caps the
transient ceiling (`origin/main:docs/product/product_lead/orca_demand_read_taxonomy_adjudication_v0.md:55`
through `:62`), while the controlling thesis body says that observe-don't-predict
supersedes that guardrail (`origin/main:docs/decisions/orca_product_thesis_consumer_demand_v0.md:94`
through `:99`). The thesis receipt also retains the older "under a
decay-timing confidence guardrail" phrasing
(`origin/main:docs/decisions/orca_product_thesis_consumer_demand_v0.md:129`
through `:136`). This is flag-only; those sources were outside the patch scope.

## Non-Findings

- No `NEEDS_ARCHITECTURE_PASS`: the defects were patch-level launch-readiness
  defects in the prompt, not a broken ontology commission design.
- The v0 ontology spine was left intact: four-commitment frame, two-layer split,
  hard cap, MAP-not-rebuild, architecture-only boundary, output contract.
- The scan-core spec condition was not patched: `origin/main` does not contain
  `docs/product/core_spine/orca_demand_scan_core_spec_v0.md`, so the target's
  "if it is on main by dispatch, read it" wording remains correct.

## Unified Diff

```diff
diff --git a/docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md b/docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
index 37958f8..e74f741 100644
--- a/docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
+++ b/docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
@@ -54,7 +54,8 @@ The dispatched lane MUST design against the current grammar:
   **durable vs transient** (persistence) × **real vs manufactured** (integrity) —
   → three actionable states: durable (commit), transient (move, time-boxed),
   manufactured (discount/avoid). "Hollow" is RETIRED. `Read` (and `Call`/`Outcome`)
-  carry a `demand_state` dimension on these axes.
+  carry this two-axis classification, with a derived action state only where
+  useful; do not collapse the integrity axis into the persistence axis.
 - **Calling sequence = a `Read` lifecycle (governed Actions).** A read opens
   **transient** (act in-window), is **monitored**, then **earns** the upgrade to
   durable or **decays** — model it as the Read state machine
@@ -140,16 +141,19 @@ so cross-artifact references stop being path-and-prose.
 
 Demand-state machinery to evaluate (added 2026-06-14, under the same cap — these
 may be dimensions/actions on existing types rather than new types; the lane
-decides): a `demand_state` dimension `{durable, transient, manufactured}` on
-Read/Call/Outcome; the **Read lifecycle Actions** (`open_transient → monitor →
-earn_durable / decay`); an `ActionCeiling` enum (commit/move + the frozen ladder)
-as a governed transition; the **Gate** actions `G1`/`G2`/`G4` (demand-gate
-closures); the **never-a-feed** invariant as an action constraint on recurring
-reads; and a `claim_tier` dimension (evidence ladder) on Memo/Case/Outcome/Read.
-The `WindCaller` object encodes the carve-out boundary (non-permanent,
-platform-scoped capture cap, internal-use, external/product boundary unchanged)
-and calibration-gated trigger primacy (Q2). Respect the cap — fold these into
-existing types where they are dimensions, not new objects.
+decides): the two-axis demand-state classification on Read/Call/Outcome
+(`persistence_state: durable|transient`, `integrity_state: real|manufactured`),
+plus a derived action state (`durable`, `transient`, `manufactured`) only where
+that helps downstream consumers; the **Read lifecycle Actions**
+(`open_transient → monitor → earn_durable / decay`); an `ActionCeiling` enum
+(commit/move + the frozen ladder) as a governed transition; the **Gate** actions
+`G1`/`G2`/`G4` (demand-gate closures); the **never-a-feed** invariant as an
+action constraint on recurring reads; and a `claim_tier` dimension (evidence
+ladder) on Memo/Case/Outcome/Read. The `WindCaller` object encodes the carve-out
+boundary (non-permanent, platform-scoped capture cap, internal-use,
+external/product boundary unchanged) and calibration-gated trigger primacy (Q2).
+Respect the cap — fold these into existing types where they are dimensions, not
+new objects.
 
 **Layer 2 — Workflow ontology (MAP, do NOT rebuild).** Lanes, artifact roles,
 claim tiers, gates, receipts, folders ALREADY have owners in the overlay.
@@ -184,12 +188,14 @@ The venue card set is the proven antidote to ontology rot; adopt its kernel:
   isolation rule: fresh worktree or branch off `origin/main` (runs alongside
   many active lanes).
 - Base freshness gate: the sha-pinned stable sources must exist at the pinned
-  sha256 prefixes (first 16 hex). The LIVE demand-grammar sources (thesis,
-  taxonomy, adjudication companion, buyer-proof) are NOT sha-pinned — instead
-  verify the 2026-06-14 demand-state model + Q0–Q3 adjudication are present in the
-  current `main` text (durable/transient/manufactured + calling sequence, not the
-  retired durable-vs-hollow framing). Either check failing → `BLOCKED_STALE_BASE`,
-  report back.
+  sha256 prefixes (first 16 hex). The LIVE demand-grammar / gate sources
+  (thesis, taxonomy, adjudication companion, buyer-proof, demand-gate closures,
+  and discovery brief where surveyed) are NOT sha-pinned — instead verify the
+  2026-06-14 demand-state model + Q0–Q3 adjudication and the applied gate-closure
+  model are present in the current `main` text (durable/transient/manufactured +
+  calling sequence, not the retired durable-vs-hollow framing; G1 origination
+  independence, G2 costly-behavior floor, G4 org-motion corroboration). Either
+  check failing → `BLOCKED_STALE_BASE`, report back.
 - Dirty-state allowance: fresh worktree, clean; only the lane's own new files
   may be dirty/untracked. Never touch other lanes' files.
 - Edit permission: `docs-write`, limited to the deliverable path(s) below and
@@ -219,17 +225,18 @@ REFERENCE-LOAD, in this order, and do not APPLY any until
 
 SOURCE-LOAD (pins = sha256 first-16-hex at authoring, current base):
 
-Domain-defining (Layer 1 inputs). The demand-grammar docs (thesis, taxonomy,
-adjudication companion, buyer-proof) are LIVE and were amended 2026-06-14 (#78,
+Domain-defining and gate-defining (Layer 1 inputs). The demand-grammar docs
+(thesis, taxonomy, adjudication companion, buyer-proof) and the gate-closure /
+discovery sources named LIVE below were amended or applied 2026-06-14 (#78,
 #88): do NOT pin them to an old sha — read current `main` and verify the
-demand-state model + Q0–Q3 adjudication are present (NOT the retired
-durable-vs-hollow framing); if absent → `BLOCKED_STALE_BASE`. Stable docs keep
-their sha pins.
+demand-state model + Q0–Q3 adjudication and applied gate-closure model are
+present (NOT the retired durable-vs-hollow framing or stale raw venue-count gate
+wording); if absent → `BLOCKED_STALE_BASE`. Stable docs keep their sha pins.
 - `docs/decisions/orca_product_thesis_consumer_demand_v0.md` — LIVE (verify, don't pin) — the demand world's primitives (costly behavior, action ceilings, org motion, outcome-memory moat) + the 2026-06-14 demand-state amendment (durable/transient/manufactured, calling sequence, never-a-feed, differentiation floor).
 - `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` — `42787638E6185D4A` — the wedge (which entities matter first).
 - `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — LIVE (verify, don't pin) — the read grammar (Read, TrendVector, WindCaller, signal layers, read types, calling sequence); Q0–Q3 DECIDED, treat its types as DECIDED inputs (the artifact status line may still read PROPOSED).
 - `docs/product/product_lead/orca_demand_read_taxonomy_adjudication_v0.md` — LIVE (verify, don't pin) — the operative definitions (what-counts / anti-trigger / boundary per layer + read type) and the Q0–Q3 owner-decision outcomes; the firmest source for Read / WindCaller / Call definitions.
-- `docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md` — the G1 (independence by de-correlated origination) / G2 (costly-behavior floor) / G4 (org-motion corroboration, separate from G1) gate definitions to encode as Gate actions/preconditions. PROPOSED (owner-gated apply) — encode as candidate gate semantics and flag the status.
+- `docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md` — LIVE (verify, don't pin) — the APPLIED G1 (independence by de-correlated origination) / G2 (costly-behavior floor) / G4 (org-motion corroboration, separate from G1) gate definitions to encode as Gate actions/preconditions. Encode as live gate semantics and flag any consuming surface that still carries stale raw-venue-count wording.
 - `docs/product/core_spine/beauty_venue_card_set_v0.md` — `65E22CDAE5EDE781` — the best-engineered existing object type (Venue) + the kernel survival terms to steal.
 - `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — LIVE (verify, don't pin) — the Demand-Substrate Hard Gate (independence rests on `derived_from`, divergence/astroturf on `diverges_from`) + the never-a-feed invariant (Orca Promise) + Memo/Case semantics. (Carries some pre-2026-06-14 durable-vs-hollow wording flagged for realignment — read the current Hard Gate + Orca Promise, not the stale framing.)
 - `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md` — `19009D43A7C29858` — an existing Case/Candidate schema.
```

## Verdict And Residual Risk

Verdict: `PATCHED_FOR_CA_ADJUDICATION`. I found two major patch-level defects
and applied bounded target-file fixes. No design-level `NEEDS_ARCHITECTURE_PASS`
condition was found.

Residual risk: the target still depends on a broad architecture lane to make
good object-card choices under the hard cap. The patch prevents two known
misreads, but it does not validate the future ontology design, prove dispatch
readiness, or resolve off-scope source-corpus residue.

Review-use boundary: these findings, citations, patch, and verdict are decision
input only. The home-model / CA decides what is kept.
