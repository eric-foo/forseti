# Orca Venue Exploration Procedure v0

```yaml
retrieval_header_version: 1
artifact_role: Product method procedure (owner-adopted shape; subordinate to the case-finder doctrine frame)
scope: >
  The manual, batch-scoped procedure for finding case-candidate venues: given a
  direction (vertical x decision family), how a screen explores — prior-provenance
  read, defaults pass, hub-finding, expand-on-signal, stop conditions — and how
  venue knowledge compounds via append-only Screen Provenance records in batch
  ledgers instead of a maintained registry. WHERE-side only; feeds candidates to
  the finder frame's screen and hands capture to the capture spine.
use_when:
  - Starting a batch case screen (any vertical) and deciding where to explore.
  - Closing a batch and writing its Screen Provenance block.
  - Re-deciding whether a venue registry/atlas is warranted (see the promote-on-reuse trigger).
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md   # exemplar Screen Provenance block
  - docs/research/source_registry_practices_deep_research_report_v0.md       # evidence base for this shape
  - docs/product/source_capture_toolbox/capture_recon_index_v0.md            # capture-seam counterpart (HOW-side)
stale_if:
  - The finder frame is owner-signed (fold this procedure in or re-home it at that sign-off).
  - The promote-on-reuse trigger fires and the owner promotes a vertical's trail into an owned card-set.
  - The capture-investigation doctrine lands (re-point the capture seam at it).
```

## Status

`SHAPE_C_OWNER_ADOPTED` — a doc-local label, not an evidence-ladder state.
Owner adopted this shape in-thread 2026-06-11 after the source-registry
research (`docs/research/source_registry_practices_deep_research_report_v0.md`):
a standing registry/atlas was REJECTED (staleness is the evidenced top
abandonment driver; honor-system maintenance rots even with tooling), and a
memory-free pure procedure was REJECTED (forfeits compounding). Shape C = this
procedure plus append-only per-batch provenance memory. Subordinate to the
finder frame (`PROPOSED_DOCTRINE_FRAME_PENDING_SIGNOFF`); this doc does not
sign that frame off, alters none of its screen requirements, and does not trip
its deferred-architecture trigger — it is the frame's "doctrine applied
manually," for the WHERE side only.

## What this is — and is not

The walk an authorized batch screen takes from "we want cases in vertical X /
decision family Y" to "candidate cases plus the venues that produced them."

- It RUNS ONLY inside an authorized batch screen: it starts when the screen
  starts and stops when the screen stops. No step may run standing.
- It is NOT a source map, source inventory, registry, atlas, monitor, scraper,
  or standing corpus intake (the finder frame's must-not boundary, untouched).
- Its memory is append-only history (dated Screen Provenance records), never a
  maintained claim about the present. Stale hints fail soft: try, move on.

## The procedure

Given a direction (vertical x decision family) from the batch plan:

- **Step 0 — read prior provenance.** Find earlier batches' venue records:
  `rg -l "Screen Provenance" docs/decisions/` (or glob
  `docs/decisions/*backtest_batch*_ledger_declaration_*.md`). Treat entries as
  dated hints from past walks — worth trying first, never current-state claims.
- **Step 1 — defaults pass.** Sweep the commons for the vertical: general web
  search; Reddit (vertical subreddits); LinkedIn; TikTok; Instagram; Facebook.
  Screening sense only — see the commons split below. Cap: this list stays at
  8 entries or fewer; overflow belongs in batch provenance, never appended here.
- **Step 2 — hub-finding.** Ask "who aggregates this vertical?" and walk the
  long tail (6 moves maximum, same cap rule):
  1. vertical trade press (the outlets that cover this vertical's operators);
  2. niche trackers and review aggregators for the decision family;
  3. dedicated vertical community forums;
  4. vertical boards inside general-purpose forums;
  5. follow the bylines — who reported this vertical's known events;
  6. mine a productive venue's outbound links and cross-references.
- **Step 3 — expand on signal.** When a venue yields a candidate or strong
  evidence, mine that venue (and its cross-links) before moving on. In-screen
  only: this same rule applied standing would be a monitor — forbidden.
- **Step 4 — stop.** Stop at the first of: the batch plan's candidate target is
  met; two consecutive exploration moves yield neither a new candidate nor a
  new productive venue (dry rule); the screen budget the batch plan set.
- **Step 5 — output.** Deliver (a) candidates into the batch's screen/triage,
  and (b) a `Screen Provenance` block in the batch ledger: venues that produced
  candidates or evidence, the rejected negative set, and the boundary line that
  it is batch provenance, not a standing source map. Exemplar:
  `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
  ("Screen Provenance"). The section NAME is a contract: future Step 0 greps
  depend on it verbatim.

## Commons split (screening venues vs capture targets)

Two senses, never conflated:

- **Screening** — agents reading public content during an authorized screen to
  find candidates. The commons are legitimate screening venues. Batch-1
  evidence: yield came almost entirely from the long tail (trade press, niche
  forums, trackers); among the big platforms only Reddit produced candidates
  or evidence.
- **Capture** — pulling bytes into packets. Policy gates come FIRST (capture
  recon pattern: the entitlement/legal gate is orthogonal to the technical gate
  and precedes it): LinkedIn forbids automated capture regardless of technical
  reachability (entitled/manual routes only); TikTok and Instagram have no
  technical recon on record and the heaviest ToS posture. "We should be doing
  the commons" never means standing automated intake there.

Unproven but plausible (research open question; nothing survived verification):
commons-scale venues are likely over-represented in model training corpora, so
long-tail-sourced cases may carry lower memorization risk as well as fresher
signal. Treat as hypothesis, not finding.

## Capture seam

The walk collects URLs and quotes as screen evidence only. When a case needs
packet-grade capture, hand off to the capture spine's investigation doctrine —
its evidence base today is
`docs/product/source_capture_toolbox/capture_recon_index_v0.md`
(substrate-first diagnosis, escalation ladder, honest NO-GO). This procedure
designs no capture mechanics and authorizes no capture run.

## Promote-on-reuse trigger

Keeps the registry rejection honest, not permanent. Route a venue-registry
decision back to the owner ONLY when one of these fires:

- the same vertical is screened a THIRD time (its provenance trail is proven
  reusable — the candidate promotion is THAT trail into a small owned card-set,
  not a general atlas);
- screens become multi-operator, or sustained cadence exceeds about one screen
  per week (design thresholds set in-thread 2026-06-11; amend by dated note).

Until a trigger fires the registry stays rejected. If promoted, the card-set
must carry the research's survival ingredients: one named owner, a fixed review
date per entry, a hard size cap, delivery into the screen step itself.

## Must / must-not

Must: run only inside an authorized batch screen; read prior provenance first;
record a Screen Provenance block (verbatim section name) at batch close;
respect the list caps; hand capture to the capture spine.

Must not: become or imply a registry, source map, monitor, scraper, or standing
intake; alter the finder frame's screen requirements; run any step standing;
let the defaults or hub lists grow past their caps (overflow goes to provenance
records).

Amendments: dated notes only, like the batch ledger; fold or supersede at
finder-frame sign-off.

## Non-Claims

Not validation, readiness, buyer proof, or judgment-quality evidence. Not
finder-frame sign-off and not its deferred architecture pass (this is the
manual method; the trigger for an automated finder is untouched). Not capture
or live-API authorization. Not a registry-decision reversal — the registry
stays rejected unless the promote-on-reuse trigger routes it back to the owner.
Mints no ladder vocabulary; the Status label is doc-local.

## Amendments

- 2026-06-11 (owner-accepted, in-thread; resolves the spine charter
  recommendation's trigger-widening question, both halves): (i) venue
  exploration performed OUTSIDE batch case screens (e.g. a demand or capture
  lane exploring venues for its own direction, under its own authority) counts
  toward the promote-on-reuse trigger's same-vertical reuse count; (ii) any
  such non-case-screen exploration records a dated `Venue Provenance` block in
  its lane's durable artifact (venues that produced signal, rejected set, same
  fail-soft dated-hint semantics; the section name is a contract). Step 0's
  discovery grep widens accordingly:
  `rg -l "Screen Provenance|Venue Provenance" docs/`. Boundary unchanged: this
  widens what COUNTS as reuse and where memory may be recorded — it authorizes
  no exploration anywhere, and Steps 1–3 remain batch-screen-scoped here.
- 2026-06-11 (owner-accepted, in-thread; influence widening): vertical
  exploration's job includes seeing who holds influence and where they point —
  at two layers: venue topology (which venues are hubs; who cites whom) and
  market-movers ("wind callers": the actors whose words or actions the
  vertical visibly responds to; pointing chains terminate at them). Three
  changes, all batch-scoped:
  (i) yield widens — an exploration move counts productive if it produced a
  candidate, evidence, OR a material influence observation (a new hub, a
  repeated pointer, byline concentration, a traced market-mover); the dry
  rule's mechanics are unchanged;
  (ii) provenance blocks may carry dated influence observations (who points
  where; who called the wind this walk) under the same append-only fail-soft
  dated-hint semantics — observations are history, never current-state claims;
  (iii) the batch plan may set an influence target alongside the candidate
  target; when it does, Step 4's "target met" stop fires only when both are
  met.
  Boundary unchanged and load-bearing: in-screen observation only — standing
  observation of any actor or venue is a monitor (forbidden); no influencer
  registry, atlas, or card-set arises from this; consolidation of influence
  trails routes only through the promote-on-reuse trigger.
