# Pre-Capture Discovery Spine — Charter Recommendation v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision-prep record (architecture recommendation; owner decision pending)
scope: >
  Commissioned Chief Architect recommendation on whether Orca should charter a
  separate pre-capture discovery spine (WHERE-side: direction-driven venue
  exploration and venue knowledge, before any capture decision). Result:
  DO_NOT_BUILD a new spine/lane now. The owner-adopted venue exploration
  procedure (Shape C) remains the operative WHERE-side capability in
  core_spine; chartering re-routes to the owner only via the promote-on-reuse
  trigger, which this record proposes widening to count cross-lane venue
  exploration. Carries two owner-gated dispositions (reverse retrieval
  pointer; trigger-widening dated note) and the seam gaps surfaced by the
  commissioned review.
use_when:
  - Re-asking whether pre-capture discovery should be chartered as a spine/lane.
  - Locating the operative WHERE-side ownership map and its capture-seam boundaries.
  - Deciding or executing the owner-gated dispositions proposed here.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/orca_venue_exploration_procedure_v0.md
  - docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md
  - docs/product/source_capture_toolbox/capture_recon_index_v0.md
  - docs/research/source_registry_practices_deep_research_report_v0.md
stale_if:
  - The owner accepts, rejects, or amends this recommendation (that decision supersedes this record as the operative source).
  - The promote-on-reuse trigger fires and the owner re-opens venue-structure promotion.
  - Finder-frame sign-off folds or re-homes the venue exploration procedure.
  - The capture-investigation doctrine lands and re-draws the WHERE/HOW seam.
```

## Status

`NEEDS_OWNER_DECISION` on the dispositions below; the architecture recommendation
itself is `DO_NOT_BUILD` (no new spine/lane now). Produced 2026-06-11 by the
commissioned CA lane from
`docs/prompts/deep-thinking/pre_capture_discovery_spine_architecture_ca_prompt_v0.md`.
Per that prompt's own `stale_if`, this returned recommendation supersedes the
prompt as the operative source for this question. Branch at authoring:
`ecr-sp3-timing-deriver-slice1` (shared, dirty); this file untracked at creation.

## Decision evaluated and options compared

Should pre-capture discovery (venue-level WHERE: given a direction, explore
toward signal and record where signal lives, before any capture decision) be
chartered as its own spine? Options compared:

- **A. New product lane** (`docs/product/` discovery spine) — loses now: it is
  the same genus as the owner-rejected standing registry (a standing
  knowledge-home created ahead of proven reuse); it bypasses the
  promote-on-reuse trigger the owner adopted the same day; the chartering cost
  is real and asymmetric (tiered decision + artifact-folders amendment +
  repo-structure.yaml lane entry + DCP receipt; forward-only population; no
  lane-to-lane migration mechanism exists); the parent finder frame is unsigned
  and its sign-off is the designated re-homing moment; an early lane invites
  the research-evidenced failure pair (thin-and-stale, or bloat attractor).
- **B. Extension of core_spine (as growth)** — rejected as a growth program:
  the procedure's hard caps are load-bearing; growing it toward multi-consumer
  generality strains the caps and enlarges the surface that finder-frame
  sign-off must fold or re-home.
- **C. Fold into data_capture_spine / source_capture_toolbox** — loses
  cleanly: posture inversion (capture-grade entitlement gates would wrongly
  frame screening, or capture adjacency would normalize screening into
  intake); direction inversion (capture lanes consume already-chosen sources;
  WHERE consumes direction and feeds judgment-side screens); it would conflate
  venue-WHERE with substrate-WHERE ("where the signal lives" already means
  different things on each side); it inherits capture-side discovery-lane hard
  stops wholesale.
- **D. No new structure until the promote-on-reuse trigger fires** — **wins**,
  with the bounded hardening below. The owner-adopted shape already wires
  delivery into the moment of work (Step-0 grep at screen start) — per the
  registry research, delivery, not a home, is the binding constraint. A
  charter would add a home, not delivery.
- **Hybrid (recommended): D + seam hardening, retrieval plumbing only** — no
  new structure; widen the trigger so it cannot under-fire; add the reverse
  pointer; route the surfaced stale pointers to hygiene.

## Why D wins (decisive evidence)

1. No second consumer of venue-level WHERE knowledge exists today. Case
   screens are the only demonstrated consumer (batch-1 Screen Provenance). The
   demand lane's discovery (org-motion note, 2026-06-11) probed already-known
   surfaces for capturability/backtestability — substrate recon, not open
   venue exploration — and consumed no existing venue record.
2. The owner decided this space on 2026-06-11 with revisit triggers built in:
   standing registry REJECTED; Shape C adopted; promotion owner-routed on
   named triggers; the batch-1 ledger separately defers the venue-atlas
   decision to the next-batch rubric pass, owner-owned. No trigger has fired.
3. The chartering question will be decided better later, at a designated
   moment: finder-frame sign-off (scheduled fold-or-re-home) or trigger fire
   (proven reuse). Chartering now fixes the destination before the events
   designed to choose it, while the direction input itself (ICP/wedge) is
   undecided.
4. The real, present defects surfaced by review are seam and counting defects,
   fixable without structure: the trigger cannot see WHERE work done outside
   batch screens; WHERE knowledge produced outside screens lands in uncommitted
   research notes invisible to the Step-0 grep; cross-references between the
   three memory shapes (Screen Provenance / Graph Frontier Register / research
   notes) are absent; several retrieval pointers are already stale.

## Operative ownership and relationships (no new spine)

- **WHERE-side venue exploration:** owned by
  `docs/product/core_spine/orca_venue_exploration_procedure_v0.md` (Shape C;
  runs only inside an authorized batch screen; subordinate to the finder
  frame; fold-or-re-home at frame sign-off).
- **WHERE memory:** append-only `Screen Provenance` blocks in batch ledgers
  under `docs/decisions/` (verbatim section name is a grep contract; exemplar:
  `judgment_spine_backtest_batch1_ledger_declaration_v0.md`).
- **HOW-side capture recon:**
  `docs/product/source_capture_toolbox/capture_recon_index_v0.md`, feeding the
  planned capture-investigation doctrine — the seam's future anchor; the venue
  procedure re-points at it when it lands (already in its stale_if).
- **Reddit Graph Frontier** (`data_capture_spine`): platform-internal
  frontier planning for intake runs — not venue-WHERE; the two are currently
  mutually invisible (open question 5).
- **Demand lanes:** consume direction; today they produce WHERE facts ad hoc
  (org-motion note). The trigger widening below makes that activity countable.
- **Finder frame:** owns the must-not boundary (no source map / inventory /
  monitor / scraper / standing intake); unchanged and pending sign-off.

## Outputs and explicit non-outputs

Outputs (under the current shape): candidates into the batch screen/triage;
dated Screen Provenance blocks at batch close; if the widening is accepted,
dated venue-provenance blocks in non-case-screen lanes' durable artifacts.

Non-outputs: no registry, atlas, source map, source inventory, monitor,
scraper, or standing corpus intake; no maintained present-state venue asset;
no capture mechanics or capture runs; no crawler; no new lane folder; no new
skill, scheduler, or automation; no Evidence Unit, ECR, Cleaning, or Judgment
design.

## Gates, caps, stop model, policy checks (operative set, by pointer)

The venue procedure owns these: Step 0 prior-provenance read; defaults pass
(cap ≤8); hub-finding (≤6 moves); expand-on-signal (in-screen only); stop at
first of candidate target met / two consecutive dry moves / batch budget;
run-boundedness (no step may run standing). Policy/source-access: the commons
split — screening public content inside an authorized screen is legitimate;
capture is gated entitlement-first (LinkedIn forbids automated capture
regardless of reachability; TikTok/Instagram have no technical recon on record
and the heaviest ToS posture; commons never means standing automated intake).
Escalation gate: promote-on-reuse only; any promoted card-set must carry the
research's survival ingredients (one named owner, fixed review date per entry,
hard size cap, delivery into the screen step itself).

## Home decision and amendment requirements

No home change. The procedure stays in `docs/product/core_spine/`; memory
stays in `docs/decisions/` ledgers; recon stays in
`docs/product/source_capture_toolbox/`. No repo-structure.yaml amendment, no
artifact-folders.md amendment, and no direction-change-propagation receipt is
required, because no doctrine changes under this recommendation.

If the owner later charters (post-trigger), the required ceremony is: a tiered
decision record superseding the structure binding's lane parameter;
`.agents/workflow-overlay/artifact-folders.md` update; `repo-structure.yaml`
`product_lanes` entry; a DCP receipt (precedent primary trigger:
`output_authority`); plus a defined lane-to-lane migration mechanism, which
does not exist today and must be created at that point.

## Conditional durable paths (if promotion/charter ever fires)

- First promotion object (per the trigger's own language): a small owned
  card-set per vertical — e.g.
  `docs/product/core_spine/orca_venue_card_set_<vertical>_v0.md` plus its
  owner decision record in `docs/decisions/`.
- Full lane (only if multi-lane reuse and operator scale demand it):
  `docs/product/<lane>/` with lane name decided then — note "discovery"
  already binds capture-side obligations (the LinkedIn Discovery & Planning
  Lane vocabulary); prefer an unambiguous name such as
  `pre_capture_discovery/` or `venue_discovery/`.

## Owner-gated dispositions (proposed, not applied)

1. **Reverse retrieval pointer** (the commissioned contained task; one header
   line, retrieval plumbing only, changes no rule). In
   `docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md`,
   append to `open_next`:

   ```yaml
   - docs/product/core_spine/orca_venue_exploration_procedure_v0.md   # WHERE-side venue procedure (owner-adopted shape, subordinate to this frame)
   ```

   Disposition: **proposed** — the frame is pending owner sign-off and no
   owner acceptance occurred in the commissioning thread.

2. **Trigger-widening dated note** (amendment to the venue procedure via its
   own dated-note mechanism; severable halves):

   > Amendment (dated note, owner-accepted YYYY-MM-DD): (i) The
   > promote-on-reuse counters count direction-driven venue exploration
   > performed for any Orca lane (case screens, demand/wedge scouting, capture
   > seeding), not only batch case screens; a vertical's third exploration
   > across lanes routes the card-set decision to the owner. (ii) Severable:
   > a non-case-screen venue exploration records a dated venue-provenance
   > block in its own lane's durable artifact, so the count is checkable.

## Surfaced gaps for owner routing (not executed by this lane)

- `docs/research/source_registry_practices_deep_research_report_v0.md`
  `open_next`: points to a nonexistent pre-lane-move finder-frame path and
  omits the venue procedure entirely (a cold reader cannot see the atlas
  decision was taken); its `use_when`/`stale_if` only anticipate the
  Atlas-chosen branch, not the taken rejection branch.
- The registry REJECTION, Shape-C adoption, and trigger thresholds are owner
  decisions recorded only in a product doc's Status block; at finder-frame
  fold time they are at loss risk — consider lifting them into a standalone
  `docs/decisions/` record at sign-off.
- `repo-structure.yaml` lane comment states the planned/current rule backwards
  (values are correct); the structure binding lacks a dated note marking the
  Phase-2 apply against its own "not executed" non-claim.
- Finder frame's internal "untracked" dirty-state note is stale (the file is
  tracked and clean); its heavyweight-charter `open_next` path is pre-lane-move.

## Open owner questions

1. Accept the trigger-widening dated note — both halves, half (i) only, or
   neither?
2. Accept the reverse pointer now, or defer it to finder-frame sign-off?
3. Lift the registry rejection + thresholds into a standalone decision record
   now, or at frame sign-off?
4. Route the surfaced stale pointers to the hygiene queue?
5. Should venue-procedure Step 0 also read Graph Frontier Registers when a
   direction includes Reddit (compounding vs coupling)?
6. Should the future capture-investigation doctrine adopt explicit
   venue-WHERE vs substrate-WHERE vocabulary to dissolve the seam ambiguity?

## Owner direction recorded (2026-06-11, in-thread)

- Disposition 1 (reverse pointer): accepted and applied; committed `6696e3b`.
- Disposition 2 (trigger-widening dated note): declined for now — the owner
  chose an awareness prompt to the main CA thread as the disposition of open
  question 1. The venue procedure stays exactly as adopted; re-proposable if
  ungoverned cross-lane venue exploration recurs.
- Open questions 1–2 are thereby resolved; questions 3–6 remain open.

## Non-claims

Not an owner decision, not validation, readiness, acceptance, buyer proof, or
judgment-quality evidence; not legal sufficiency or rights clearance; not a
doctrine change (no DCP receipt required by this record); not finder-frame
sign-off; not a registry-decision reversal (the rejection stands; only the
trigger's counting rule is proposed for widening); authorizes no build, crawl,
scrape, capture, monitor, or standing intake; does not touch judgment-spine
batch-1 artifacts or execution.
