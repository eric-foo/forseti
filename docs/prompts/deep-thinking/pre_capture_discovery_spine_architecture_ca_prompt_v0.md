# Pre-Capture Discovery Spine — Architecture CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: >
  Prompt for a fresh Chief Architect lane to decide whether Orca's pre-capture
  discovery capability (WHERE-side: direction-driven exploration and venue
  knowledge — where signal lives, before any capture decision) should be
  chartered as its own spine/lane, and if so its charter, boundaries, and home.
  Carries the 2026-06-11 source-registry research findings, the owner-adopted
  exploration-procedure shape as constraints, and a contained owner-gated
  reverse-pointer task.
use_when:
  - Commissioning the pre-capture discovery spine decision in a fresh CA thread.
  - Locating the source pack and owner-decided constraints for that decision.
authority_boundary: retrieval_only
output_mode: paste-ready-chat
open_next:
  - docs/product/core_spine/orca_venue_exploration_procedure_v0.md # nonresolving: pending on unmerged lane
  - orca/product/spines/capture/source_capture_toolbox/capture_recon_index_v0.md
stale_if:
  - The commissioned lane returns its recommendation (that record supersedes this prompt as the operative source).
  - The owner re-opens the registry rejection or the exploration-procedure shape (constraints below would be stale).
```

Paste the body below into a fresh Chief Architect thread in this workspace.

---

You are the Chief Architect for Orca.

## Objective and intended decision

Decide whether Orca should charter a separate bounded **pre-capture discovery
spine** — the WHERE-side capability that, given a direction (a vertical, a
decision family, a case lead), explores toward signal and records where signal
lives, BEFORE any capture decision — and if so, what its charter, ownership,
boundaries, and home should be. The intended output is an architecture
recommendation for the owner, not a build.

Do not treat this prompt as the constraint source. Derive constraints from the
Orca sources named below. The prior-thread findings included here are
orientation to be re-verified against those sources, not truth.

## Preflight (make the start state checkable)

- Prompt artifact (input source):
  `docs/prompts/deep-thinking/pre_capture_discovery_spine_architecture_ca_prompt_v0.md`.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca` (same worktree assumed).
- Branch at authoring: `ecr-sp3-timing-deriver-slice1`, dirty; concurrent lanes
  share it; head drift alone is stale-reread, not blocked.
- Dirty-state allowance: untracked files ARE in scope — several load-bearing
  inputs below may be untracked (venue procedure, recon index, batch-1 ledger,
  research report). Verify each exists before relying on it.
- `AGENTS.md` and `.agents/workflow-overlay/README.md`: read them fresh in your
  thread (required reads below); the authoring thread had them supplied.
- Source pack: the bounded custom pack below, under
  `.agents/workflow-overlay/source-loading.md`.
- repo_map_decision: loaded; repo_map_reason: the decision spans product lanes
  and the structure binding, so routing needs the repo map.
- Doctrine change: chartering a new lane WOULD change structure doctrine
  (artifact-folders overlay + repo-structure.yaml + the Doctrine Change
  Propagation Contract in `.agents/workflow-overlay/source-of-truth.md`). This
  prompt authorizes the RECOMMENDATION only, never the doctrine change itself.
- Targets and edit permission: read-only, with two narrow exceptions —
  (a) docs-write for ONE durable recommendation artifact if your result needs
  one (name the path per output item 8); (b) the owner-gated reverse-pointer
  edit in the contained task below, applied only on explicit owner acceptance
  in your thread.
- Output mode: chat-first per the numbered contract below; file-write only per
  exception (a).
- Validation gates: prompt-validation gates plus DCP-if-doctrine; you make no
  validation, readiness, or lifecycle claims.
- External boundary: external workflow source is read-only; `jb` is not Orca
  authority. Live web fetching only as bounded policy checks, recorded as
  source context.

## Required reads (authority first)

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md` (run Cynefin routing before planning)
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `docs/workflows/orca_repo_map_v0.md`

## SOURCE-LOAD (minimum needed from these)

- `docs/product/core_spine/orca_venue_exploration_procedure_v0.md` — the
  owner-adopted WHERE-side method (2026-06-11): exploration walk + append-only
  provenance memory + promote-on-reuse trigger.
- `docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md`
  — the must-not boundary (no source map / inventory / monitor / scraper /
  standing intake); PROPOSED, pending owner sign-off.
- `docs/research/source_registry_practices_deep_research_report_v0.md` — the
  verified registry research: why the standing registry was rejected; open
  questions left for follow-up.
- `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` —
  its "Screen Provenance" section is the live memory-mechanism exemplar.
- `docs/product/source_capture_toolbox/capture_recon_index_v0.md` — HOW-side
  capture recon consolidation; seed of the planned capture-investigation
  doctrine; the seam this spine must not duplicate.
- `docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md`
  — deferred, legally-gated capture capabilities (boundary examples).
- `docs/prompts/deep-thinking/reddit_crawler_graph_exploration_architecture_ca_prompt_v0.md`
  — an earlier related commission (crawler-graph exploration); CHECK whether its
  lane ever ran and produced output before overlapping it.
- `docs/decisions/orca_repo_structure_binding_v0.md` and `repo-structure.yaml`
  — what chartering a new product lane requires.

## Owner-decided constraints (honor; you may recommend revisiting, never overturn)

1. A standing venue registry/atlas is REJECTED (owner, 2026-06-11,
   research-based). Revisiting is governed solely by the promote-on-reuse
   trigger inside the venue exploration procedure.
2. Adopted shape: thin exploration procedure + append-only per-batch provenance
   memory. No maintained present-state asset.
3. The finder frame's must-nots hold unless the owner amends them at that
   frame's sign-off.
4. Entitlement/legal gates precede technical capability everywhere: LinkedIn
   forbids automated capture regardless of reachability; TikTok and Instagram
   have no technical recon on record and the heaviest ToS posture.
5. Judgment-spine batch-1 execution is the active workstream elsewhere; this
   lane must not block, delay, or touch it (the ledger's execution rules bind).

## Prior-thread findings (orientation only — re-verify against the sources)

- Registry research (2 of 7 communities produced surviving claims): staleness
  is the evidenced top abandonment driver; honor-system upkeep rots even with
  tooling (82% dead links despite 94% automated checkers — unscheduled checking
  was the missing variable); usage is episodic (triggers: stuck, unfamiliar
  territory, referral); delivery into the moment of work — not content quality
  — is the binding constraint; bloat is the signature content failure;
  Bellingcat's counter-design = named per-entry owners, per-category guardians,
  enforced cadence, pre-publication gatekeeping (~21 months old, first-party,
  durability unproven). One refuted claim, do not repeat: tool-death is NOT the
  dominant failure mode — staleness is.
- Batch-1 screen evidence: candidate yield came almost entirely from long-tail
  venues (trade press, niche forums, trackers); among the big platforms only
  Reddit produced candidates or evidence.
- Hypothesis only (the research returned nothing on it): commons-scale venues
  may be over-represented in model training corpora — a recognition-risk angle
  for case sourcing.
- The existing seam: WHERE-side = the venue exploration procedure
  (case-screen-scoped); HOW-side = the capture recon index feeding a planned
  capture-investigation doctrine. The open architecture question is whether
  WHERE-side discovery generalizes beyond case screens (e.g., serving capture
  and demand lanes too) strongly enough to deserve first-class spine status.

## Workflow

1. Run Orca Cynefin routing (`.agents/workflow-overlay/decision-routing.md`)
   before planning.
2. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-architecture-planning`
   if available. Do not APPLY either before source readiness.
3. SOURCE-LOAD the pack above; declare `SOURCE_CONTEXT_READY` or
   `SOURCE_CONTEXT_INCOMPLETE` (with missing sources and gaps).
4. Only after that declaration, APPLY the methods to the loaded source context.
5. You may use up to three subagents, only after source readiness and only for
   independent constraint/risk discovery from assigned source capsules. Do not
   hand subagents a prewritten constraint list.

## Decision to evaluate, with required comparison

Should pre-capture discovery be chartered as its own spine? Compare at minimum:

- A. New product lane (a discovery / pre-capture spine under `docs/product/`):
  requires a repo-structure binding amendment, artifact-folders update, and a
  direction-change propagation receipt.
- B. Extension of `core_spine` (status quo home of the venue procedure).
- C. Sub-lane of `data_capture_spine` / `source_capture_toolbox` (WHERE folded
  into the capture side).
- D. No new structure until the promote-on-reuse trigger fires (status quo).
- Hybrid options.

## Contained task (small; owner-gated in your thread)

Propose the reverse retrieval pointer: add
`docs/product/core_spine/orca_venue_exploration_procedure_v0.md` to the
`open_next` list of the finder frame's retrieval header (one header line;
retrieval plumbing only — it changes no rule). The frame is pending owner
sign-off, so apply the edit only on explicit owner acceptance in your thread;
otherwise return it as a proposed edit in your output.

## Output contract (numbered, in chat)

1. Source context status (`SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE`
   with gaps).
2. Cynefin routing result.
3. Architecture recommendation: `TARGET_RECOMMENDED` | `NEEDS_OWNER_DECISION` |
   `BLOCKED_SOURCE_CONTEXT` | `DO_NOT_BUILD`.
4. Proposed charter, ownership, and relationships (venue exploration procedure,
   capture recon/doctrine, finder frame, batch Screen Provenance records,
   demand lanes).
5. Proposed outputs and explicit non-outputs.
6. Gates, caps, stop model, and policy/source-access checks.
7. Home decision, plus whether a repo-structure/artifact-folders amendment and
   direction-change propagation are required.
8. Required durable artifact path if a charter should be written.
9. Reverse-pointer disposition (applied-on-owner-acceptance | proposed |
   dropped-with-reason).
10. Open owner questions.
11. Next authorized step.

## Hard output boundary

- Do not implement, build, crawl, scrape, or run any capture.
- Do not edit any file except per the Preflight edit permission.
- Do not overturn the owner-decided constraints above.
- Do not claim validation, readiness, legal sufficiency, or lifecycle status.
- Do not touch judgment-spine batch-1 artifacts or execution.

## Thread operating target continuity

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: different_workstream
  changed_from_input: no
  lifecycle_status: the origin thread retains its batch-1 execution anchor (judgment spine); this prompt commissions a separate pre-capture discovery workstream
  if_changed_reason:
```
