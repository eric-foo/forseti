# Forseti Vertical Exploration Guide v0

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
  - forseti/product/spines/foundation/vertical_exploration/forseti_memorization_resistant_case_finder_frame_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md   # exemplar Screen Provenance block
  - docs/research/source_registry_practices_deep_research_report_v0.md       # evidence base for this shape
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md            # canonical capture-method playbook (HOW-side)
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md            # capture-seam counterpart (HOW-side)
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md            # Source Capture Armory entrypoint and screening-read service pointer
  - forseti/product/satellites/beauty/beauty_venue_card_set_v0.md                      # promoted beauty card-set (Step 0 reads it FIRST for beauty screens)
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md  # MGT intelligent-walk overlay and capture-request bridge
stale_if:
  - The finder frame is owner-signed (fold this procedure in or re-home it at that sign-off).
  - The promote-on-reuse trigger fires and the owner promotes a vertical's trail into an owned card-set.
  - The canonical Source Capture Playbook, Source Capture Armory screening-read service, or capture recon index materially changes screening read-escalation rules.
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

The walk an authorized batch screen takes from "we want cases in vertical (Vertical) X /
decision family Y" to "candidate cases (Case) plus the venues (Venue) that produced them."

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
- **Step 4 — stop / pivot.** Stop at the first of: the batch plan's candidate
  target is met; two consecutive exploration moves yield neither a new
  candidate nor a new productive venue (dry rule); the screen budget the batch
  plan set. For an explicitly declared MGT / intelligent-walk scan with
  multiple frontiers, the dry rule is branch-aware: repeated dry moves close
  the active branch, then the walk may pivot to a declared or newly surfaced
  frontier with non-trivial expected value while the run remains inside its
  caps. It stops globally when target, budget, policy boundary, or minimal/zero
  remaining frontier value fires.
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
packet-grade capture, hand off to the capture spine's canonical Source Capture
Playbook:
`forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`.
Its recon evidence base today is
`forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
(substrate-first diagnosis, route selection, honest NO-GO). The Source Capture
Armory README defines the orchestrator-only `screening_read` /
`screening_browser_read` seam for screen-light public reads. This procedure
designs no capture mechanics and authorizes no capture run.

## Walker Equipment Kit (canonical block — paste into every walk prompt)

No walker deploys without this block (2026-06-12 amendment; capture-seam sync
2026-06-22). It distills the capture lane's read-escalation patterns from the
canonical Source Capture Playbook, capture recon index, and Source Capture
Armory screening-read service for screening use, plus the rules this guide's
own screens earned. It updates by dated note as ledgers learn new walls.

> WALK CONTRACT (non-negotiable):
> 1. HARD STOP SELF-CHECK — keep a numbered move log; after EVERY move check
>    in order: (a) candidate target met -> STOP NOW; (b) ordinary walk: last
>    two moves both VENUE-DRY -> STOP NOW; explicitly declared MGT /
>    intelligent-walk scan: last two moves on the active branch both VENUE-DRY
>    -> close that branch and pivot only if another declared or surfaced
>    frontier has non-trivial expected value; otherwise STOP NOW; (c) move cap
>    reached -> STOP NOW. Show the check in the log (e.g. "a:no b:branch-close
>    pivot:yes c:no"). Continuing past a fired stop violates the walk contract.
> 2. YIELD CLASSES per move: CANDIDATE | EVIDENCE | INFLUENCE-OBS (hub,
>    pointing structure, wind-caller/detector) | VENUE-DRY (venue actually
>    read, zero yield) | ACCESS-NOTE (could not reach it — counts toward the
>    move cap, never toward the dry stop).
> 3. READ ESCALATION before any ACCESS-NOTE (screening posture only — public
>    logged-out pages, no logins, no bulk, URLs + short quotes): first classify
>    whether the target is public or access-controlled. If it is private,
>    paywalled, login-only, or still unknown after a good-faith look, record the
>    access boundary and stop that read. For public targets, try (i) a URL
>    variant (old./www., mobile, print view), (ii) search-snippet mining
>    (site:domain queries), (iii) an archived copy of the SPECIFIC page, and
>    (iv) when the orchestrator offers a bounded screening route,
>    `screening_read` or visible-text `screening_browser_read` before recording
>    a final ACCESS-NOTE. For browser reads, judge the visible text/title;
>    hidden full-DOM challenge residue alone is not a source wall. Record which
>    shapes you tried. "Blocked" is a hypothesis, not a verdict. (2026-07-02,
>    playbook Guardrail 4 sync: before recording VENUE-DRY off an empty or
>    erroring read, sanity-check the instrument on a known-good public page —
>    an erroring read is "read failed", not "venue empty".)
> 4. KNOWN WALLS (do not burn moves rediscovering): reddit.com is unreachable
>    via the agent fetch tool (tool-level block) AND unreliable in external
>    search indexes. For Reddit real reads, record the needed public locator or
>    query and let the orchestrator invoke the capture-harness
>    `screening_read` service; walkers never call it directly. For direct-fetch
>    Cloudflare/interstitial walls (Basenotes-class), snippet-mine and try
>    archives first; if that is not enough, the orchestrator may route
>    `screening_browser_read` for visible text only. Both services are
>    screening posture: public-only, logged-out, human-rate, one source / one
>    question, no packet, no manifest, no ECR. Basenotes.com 403s direct fetch
>    - snippets and archives work; browser-rung escalation is
>    orchestrator-mediated.
> 5. POLICY SKIPS (hard): LinkedIn, TikTok, Instagram — record pointers,
>    never follow in this walker. Capture-lane or source-family playbooks may
>    authorize separate public social capture/screening routes, but they do not
>    relax this kit. No logins anywhere. No capture: URLs + short quotes only.
> 6. HUB ORDER: brand-story trade press FIRST (outlets covering brands and
>    their decisions); ingredient/market trade press ONLY when hunting
>    regulatory forcing functions. US brands / US ecosystem by default (owner
>    direction 2026-06-12); flag incidental non-US finds.
> 7. EVERY claim URL-backed — found sources only, never your memory. Return
>    candidates, influence observations with receipts, the negative set, and
>    access notes in the structured shape the orchestrator specifies.

Orchestrator obligations (the contract's other half): supply direction,
targets, caps, and the exclusion list; collect access notes at batch close
and consult the capture seam (Source Capture Playbook / Source Capture Armory
screening-read service / recon index) on every unresolved wall BEFORE that
vertical's next screen; fold newly-diagnosed walls into this kit by dated note.

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
  market-movers ("wind callers" (WindCaller): the actors whose words or actions the
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
- 2026-06-11 (owner-accepted, in-thread; promote-on-reuse EXECUTED for
  beauty): the trigger fired at beauty's third screen and the owner promoted
  that vertical's trail into the bounded card-set
  `forseti/product/satellites/beauty/beauty_venue_card_set_v0.md` (binding terms:
  `docs/decisions/beauty_venue_card_set_promotion_decision_v0.md`). Delivery
  wiring: for a vertical with a promoted card-set, Step 0 reads the card-set
  FIRST, then runs the provenance grep as before. Cards are dated hints with
  review dates — fail-soft semantics unchanged. The registry rejection stands
  for every other vertical; this promotes ONE vertical's trail under the
  survival ingredients, nothing more.
- 2026-06-11 (owner-accepted, in-thread; two rules from screen 3 — the
  durable method records of the in-ledger acceptances):
  (i) DRY RULE — venue-dry counting: only a move that WALKED a venue and
  yielded nothing counts toward the two-consecutive-dry stop. A move whose
  access path failed (search/tool returned nothing reachable) is an ACCESS
  NOTE, not an exploration move; it still consumes the batch move cap (budget
  protection intact — a broken access path cannot extend a walk), but it
  cannot kill the walk. Walk prompts must carry the stop rule as a hard
  per-move self-check (screen 3 recorded an executor breach).
  (ii) SUBTLE-CLASS A-LEG — corroborated material change: when assembling
  subtle-class candidates and no brand statement exists, the brand-action leg
  may be satisfied by material evidence of the change from 2+ INDEPENDENT
  sources PLUS a community detection wave. A single source cannot mint a
  candidate; the wave requirement keeps candidates market-visible. Origin and
  first application (Xerjoff):
  `docs/decisions/beauty_subtle_decision_screen3_ledger_v0.md`.
- 2026-06-11 (owner-directed rename): this artifact is now the VERTICAL
  EXPLORATION GUIDE — renamed from `orca_venue_exploration_procedure_v0.md` to
  `forseti_vertical_exploration_guide_v0.md` (the walk explores a VERTICAL;
  venues are its waypoints). Path references in live artifacts updated the
  same turn; historical records (the commissioning prompt, past cleanup
  reports, dated ledger filenames) keep their original path text. Section-name
  grep contracts ("Screen Provenance" / "Venue Provenance") are unchanged.
- 2026-06-12 (owner direction, in-thread): screens DEFAULT TO US BRANDS AND
  THE US ECOSYSTEM until further owner direction (highest consumer spending;
  densest public signal layer). Non-US candidates surfaced incidentally are
  recorded but flagged non-US for the consuming batch. Pre-existing pool
  members affected (consuming batches treat per this direction): Purito (KR),
  Dear Klairs (KR), Manifesto (UK), Puredistance (NL), Xerjoff (IT); Bonjout
  and The Nue Co. are borderline (foreign-founded, US-market distribution).
- 2026-06-12 (owner-accepted, in-thread; walker equipment + trade-press fork
  + access-wall routing): (i) Step 2 move 1 FORKS — brand-story trade press
  (outlets covering brands and their decisions) is walked FIRST for
  candidates; ingredient/market trade press is consulted only for regulatory
  forcing functions (twice-observed: beauty + ingestible beauty). (ii) Access
  walls: walkers escalate the read shape within screening posture and record
  shapes tried; consulting the capture playbook/recon seam is the
  ORCHESTRATOR's job at batch close — every unresolved wall routes to the
  capture seam before that vertical's next screen. (iii) Every walk prompt
  must include the Walker Equipment Kit (section above) — walkers deploy
  equipped, not naked.
- 2026-06-21 (owner-invoked Mini God Tier target, in-thread; intelligent-walk
  overlay): scanning may use the MGT operating model at
  `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md`
  when the run is explicitly declared MGT / intelligent-walk. This adds
  frontier selection, branch-aware signal-decay handling, minimum evidence
  promotion, shared scanning vocabulary, and capture-request handoff language.
  It does not authorize a generic crawler, standing monitor, registry, atlas,
  packet-grade capture, route expansion, scan-core ratification, or live scan
  execution. Ordinary batch walks keep the original global dry stop unless the
  run declares the MGT branch-pivot contract up front.
- 2026-06-22 (capture-seam reconciliation): the Walker Equipment Kit now points
  at the canonical Source Capture Playbook, Source Capture Armory screening-read
  service, and capture recon index rather than the older capture-investigation
  wording alone. The kit adopts the playbook's Step 0 public-vs-access-control
  classification, problem-indexed route selection, visible-text browser honesty,
  and "blocked is a hypothesis" discipline for screening posture only. This
  does not import packet-grade capture, proxy/geo setup, packet-stage anti-bot
  routes, social live reads, logins, manifests, ECR, or capture authority
  into Walker work.
