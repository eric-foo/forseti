# Retail/PDP Review-Record Capture — Capture-Spine Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff / commission prompt (routes the retail PDP review-record capture to the capture-spine lane; prepares + scopes the work, does not execute it)
scope: >
  Commissions the capture-spine lane to execute the retail PDP review-record capture defined in
  retail_pdp_review_capture_spec_v0.md — REUSING Orca's already-established retail capture lines
  first, extending the existing aggregate review-substrate to individual review_record Attachment
  Records, under measured-ToS / no-gate-defeat, with a bounded in-niche ego-graph corpus, no graph/
  dedup/identity/integrity at capture, Amazon recon first. Capture execution + landing to main stay
  owner-gated; the capture-spine lane owns the build under its own scoping.
use_when:
  - The owner hands the retail PDP review-record capture to the capture-spine lane.
  - Checking what the review capture must reuse, recon, and preserve before any build.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_review_capture_spec_v0.md          # the controlling spec (what to capture; branch-only, PR #302)
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md  # canonical content and review-substrate rows
  - forseti/product/spines/capture/core/source_families/retail_pdp/README.md                                   # current route and operator entrypoints
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md                   # Attachment Records (where review_record lands)
  - .agents/workflow-overlay/decision-routing.md                                                          # Cynefin routing (run before broad build)
stale_if:
  - The review-capture spec changes the per-review field set, the corpus-scope, or the storage shape.
  - The retail_pdp projection contract changes the review-substrate row or required bindings.
  - A retailer's review-substrate recon verdict (Sephora Bazaarvoice / Ulta Apollo / Amazon) lands or changes.
```

## Orca Start Preflight (the receiving capture-spine lane must establish before work)

```yaml
orca_start_preflight:
  agents_read: required   # AGENTS.md + .agents/workflow-overlay/README.md in the current task context
  overlay_read: required
  source_pack: capture-spine review-record capture (this commission's Required Reads)
  repo_map_decision: loaded | not_needed | unavailable   # receiver records, + reason
  workspace: <capture-lane worktree off origin/main>      # receiver pins
  branch_or_revision: >
    CONTROLLING INPUTS ARE BRANCH-ONLY: the review-capture spec and the manufactured-demand design
    live on `claude/distracted-ishizaka-01eff5` (PR #302), NOT yet on origin/main. Read them from
    that branch, or after PR #302 merges. The established retail lines (projection contract,
    sidecar playbook, data-lake contracts) are on origin/main.
  dirty_state_allowance: receiver declares; untracked-in-scope only for new capture artifacts
  edit_permission: see "Authorization Boundary" below (recon + bounded build under capture-lane scoping; execution owner-gated)
  target_scope:
    - orca-harness/source_capture/** (review_record adapter extension — capture-lane owned)
    - orca/product/spines/capture/source_families/retail_pdp/** (recon verdicts / design notes)
  output_mode: file-write (capture-lane artifacts) + recon verdicts
  validation_gates: per-retailer recon GO/PARTIAL/NO-GO recorded; measured-ToS posture tagged; no gate defeated
  external_source_boundary: external workflow source is read-only; jb is not Orca authority; retailers are public pages under measured-ToS
  doctrine_change: none expected (consumes existing specs/contracts; if the build forces a schema/contract change, STOP and raise a propagation blocker)
  blocked_if_missing: yes — if the controlling spec is unreachable (branch + main both), STOP and report
```

## Objective & Intended Decision (what this is for / done looks like)

**Goal (pointer-preferred — controlling source: `retail_pdp_review_capture_spec_v0.md` §Purpose/§Required Behavior):**
preserve the **individual** retailer-PDP review records (reviewer id, rating, timestamp, verbatim
text, verified-purchase + syndication flags, exposed reviewer metadata) for a **bounded in-niche**
set, by **reusing and extending the existing retail capture lines** — so the demand read and the
**within-category co-review graph** have their raw substrate.

**Done looks like:** for each authorized retailer, a valid `review_record` capture lands as
`retail_pdp` **Attachment Records** keyed to the packet/slice, produced by **extending the existing
adapter/sidecar (not a fresh pipeline)**, with the per-retailer recon verdict recorded, the corpus
bounded to the in-niche ego-graph, and **no graph / identity / integrity label produced at
capture**, no gate defeated.

> This goal is the executor's **target + review axis-to-attack**, not a pass-bar graded against this
> prompt's wording (`work_unit_fitness_reference_v0`).

## Routing

```yaml
workflow_sequence_policy: overlay_owned
workflow_sequence_source: explicit_user_instruction (owner: route to capture lane) + accepted_project_artifact (the spec names the capture-spine lane as build owner)
workflow_sequence_status: bound
receiver: capture-spine lane
```

## Cynefin Routing (run before broad build)

This is **complex / risk-bearing** (live retailer source access under ToS; an unverified anti-bot
posture could over-reach). Run the router (`.agents/workflow-overlay/decision-routing.md`):
**risk-first probe** — settle **Amazon review recon (open)** and confirm the Bazaarvoice/Apollo
per-review field shape **before** any broad capture build. Do not build the adapter across all
retailers before the hardest recon (Amazon) returns an honest GO/PARTIAL/NO-GO. NO-GO is a
first-class successful diagnosis, not a failure.

## Required Reads (REFERENCE-LOAD the method/playbook; SOURCE-LOAD the task sources; then declare readiness)

`REFERENCE-LOAD` (procedural guidance only — do not APPLY before source readiness):
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` (probe-then-pin recon)
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md`

`SOURCE-LOAD` (the task sources):
- **Controlling:** `retail_pdp_review_capture_spec_v0.md` (the field table, corpus-scope, storage, non-goals) — **branch-only, PR #302**
- `retail_pdp_projection_contract_v0.md` (the established review-substrate row this extends; row kinds; residual discipline)
- `retail_pdp_sidecar_operator_playbook_v0.md` (current Amazon/Sephora/Ulta sidecar commands + inspection)
- `demand_durability_multi_retailer_rendered_capture_spec_v0.md` (per-retailer series, measured-ToS, substrate-first)
- `docs/prompts/handoffs/demand_durability_cadence_runner_step3_handoff_v0.md` (the cadence-runner seam, if a cadence is wired)
- `core_spine_v0_data_lake_core_contract_v0.md` + `core_spine_v0_data_lake_storage_contract_v0.md` (Attachment Records; raw-canonical; physicalization deferred)
- `data_capture_source_access_boundary_decision_v0.md` (measured-ToS / no-gate-defeat hard stops)
- `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md` (existing Sephora-Bazaarvoice / Ulta-Apollo recon)
- `orca/product/spines/judgment/demand_read/integrity/judgment_spine_manufactured_demand_detection_design_v0.md` (the DOWNSTREAM consumer — branch-only, PR #302)

Then declare **`SOURCE_CONTEXT_READY`** (or `SOURCE_CONTEXT_INCOMPLETE` with missing/gap/conflict).
Do **not** produce recon verdicts, adapter design, or a corpus plan before that declaration.

## The Work — reuse first, recon-first, then bounded build

**STEP 1 — INVENTORY & REUSE the already-established retail lines (FIRST, before any build).**
Audit what Orca already has and state what is **reusable** vs **genuinely new**: the Sephora/Ulta/
Amazon adapters behind the CloakBrowser packet runner; the projection contract's
`retail_review_substrate` row (count/rating today); the sidecar operator playbook; the
demand-durability cadence/series shape; the anti-block ladder; the existing Sephora-Bazaarvoice +
Ulta-Apollo recon. **The review capture EXTENDS the existing aggregate review-substrate to
individual `review_record` Attachment Records — it is not a fresh pipeline.** Reuse the existing
adapters, packet runner, per-retailer series, and anti-block ladder; build only the per-review
field extraction the spec adds.

**STEP 2 — Per-retailer recon (risk-first; Amazon FIRST).** For each candidate retailer, an honest
**GO / PARTIAL / NO-GO** for the *per-review-record* substrate under measured-ToS / no-gate-defeat:
- **Sephora (Bazaarvoice API + scroll)** and **Ulta (`__APOLLO_STATE__`)** — already recon'd at the
  aggregate level; **confirm the per-review fields** (stable author id, **syndication-source** flag,
  badges, verified-buyer). Do not assume the field shape — verify.
- **Amazon (rendered DOM, review pagination)** — **OPEN**; the hardest anti-bot + ToS case. Run the
  ladder, escalate-and-re-probe before NO-GO. Measured pre-commercial; commercial scale routes
  through a provider, not Orca's own path.
- **Target / Walmart** — **only if strong for *online* reviews in the target subniche** (Target ≈
  masstige/clean; Walmart ≈ drugstore/mass; per the spec's candidate-retailer note). Skip otherwise.

**STEP 3 — Bounded `review_record` capture (or design, if build is deferred).** Extend the existing
adapter to preserve the spec's per-review field set, landing as `retail_pdp` `review_record`
**Attachment Records** keyed to packet/slice. Corpus bounded to the **in-niche ego-graph** (seed =
candidate + close competitors → one hop along reviewers within-niche; **no** cross-industry, **no**
unbounded crawl). Per-retailer series. **Capture preserves source-visible facts + limits only.**

**STEP 4 — Honest limits + return** (see Return Contract).

## Hard Constraints / Forbidden

- **Measured-ToS / no-gate-defeat:** STOP at any auth / CAPTCHA / Cloudflare *challenge*, record the
  limitation; a first "blocked" is a hypothesis — escalate the ladder and re-probe before NO-GO.
- **Bounded in-niche ego-graph only** — no unbounded crawl, **no cross-industry / cross-product**
  corpus, **no standing crawler** (bounded attended / self-terminating runs only).
- **One series per retailer** (same SKU across retailers = parallel series, compared downstream).
- **Attachment Records only** — no new direct `SourceCaptureSlice`/`SourceCapturePacket` fields, no
  schema/manifest bump.
- **NO graph, dedup, reviewer-identity / entity resolution, integrity verdict, or scoring at
  capture** (INV-1 — all downstream). **No first-party submission telemetry** (IP/device/velocity —
  unreachable; out of scope). **No person-level dossier** in any sold or external surface.
- **No ECR / Cleaning / Judgment**, no salience/credibility/demand decision (projection-contract
  boundary).
- **No import** of `jb` policy, external workflow source as authority, or another project's paths.

## Output / Return Contract

`file-write` (capture-lane artifacts under its own scoping) + a **schema-bound chat return** to the
owner/CA — terse, one line per field, a `file:line` cite for every load-bearing claim, `unknown` for
absent fields (not a prose dump):

```yaml
reuse_inventory:        # what existing retail line is reused vs newly built (file:line cites)
recon_verdicts:         # per retailer: GO | PARTIAL | NO-GO + the substrate located + ToS posture
review_record_status:   # wired | designed-only | blocked, per retailer
corpus_bound:           # the in-niche seed + reviewer-hop cap actually used
honest_limits:          # what is undetectable / unreached (Amazon, syndication field, etc.)
boundary_kept:          # no graph/identity/integrity at capture; no gate defeated; Attachment Records
```

For any **source-changing** work (adapter edits), also return **lifecycle-verification** fields so
the owner can verify on a fresh read: `branch`, `base + commit SHA`, `push/PR state`, `merged`
(observed, never assumed), plus a per-surface change list with one `file:line` cite each.

## Authorization Boundary (load-bearing — this commission routes; it does not bypass the owner gate)

- The **capture-spine lane owns the adapter architecture + build under its own scoping** (the
  demand-durability precedent). This commission **scopes and routes**; it does not grant unbounded
  authority.
- **Recon** = source-access probing under **measured-ToS / no-gate-defeat** (capture-lane authority).
- **Build** = **bounded** `review_record` adapter extension, reusing the established lines.
- **Capture execution at volume and landing to `main` stay OWNER-GATED.** No standing monitor, broad
  crawler, or production pipeline is authorized. Pre-positioning a bounded in-niche corpus is the
  owner's gated call, executed in this lane — not started by this prompt.

## Assumptions / Unknowns / Blocked

- **Controlling spec + downstream design are branch-only (PR #302), not on origin/main** — read from
  the branch or after merge; if both are unreachable, `BLOCKED` and report.
- **Amazon review recon is open**; **Bazaarvoice per-review field shape is unconfirmed** — both are
  recon questions, not assumptions to bake in.
- Target/Walmart inclusion is **subniche-conditional** (online-review strength) — confirm, don't default.

## Non-Claims

- Commission **prompt artifact only** — it prepares and routes; it **executes no capture, build,
  recon, or scoring**. No readiness, validation, or buyer claim.
- Authorizes no schema change, no standing crawler, no ECR/Cleaning/Judgment, no integrity verdict.
- Caps at `product_learning`; the capture lane's own outputs carry their own claim classification.
- New prompt artifact; changes no other live doc, so no `direction_change_propagation` receipt is
  owed. On any forced contract/schema change during build, STOP and raise a propagation blocker.

```text
This is a commission prompt. It is not capture execution, not implementation authority, and not
proof of readiness. Capture execution at volume and landing to main remain owner-gated.
```
</content>
