```yaml
retrieval_header_version: 1
artifact_role: Decision record — screening Reddit read-route (capture-spine provider side; build-gated)
scope: >
  Records the Main-CA decision on how screening agents obtain Reddit reads, given the 2026-06-12
  tooling discovery that the WebFetch tool blocks reddit.com for screening agents while the
  capture-harness HTTP runners reach it fine (recon receipts). Adopts a layered route — snippets
  default / wire the capture runner as a bounded screening-read service / operator-manual fallback —
  and specifies the bounded service contract the wiring must honor. Decision only; the wiring is a
  separate authorized capture-lane build turn.
use_when:
  - A capture-lane build turn opens to wire the bounded screening-read service.
  - A screen orchestrator needs to know how Reddit origination reads are obtained today.
  - The Walker Equipment Kit's Reddit wall (KNOWN WALLS, point 4) is revisited.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
  - docs/decisions/ingestible_beauty_screen1_ledger_v0.md
stale_if:
  - The wiring lands (record the build; flip the kit's KNOWN WALLS Reddit line by dated note in the discovery lane).
  - The WebFetch tool changes its reddit.com policy (re-decide the default).
  - The owner changes the capture risk posture or the screening-read boundary.
```

# Screening Reddit Read-Route Decision (v0)

## Provenance and authority

Owner-couriered Main-CA commission, 2026-06-12 ("decide the screening Reddit read route").
Recommended by the pre-capture discovery lane (ingestible-beauty screen-1 ledger). Decided by the
Main CA as capture-spine owner (the provider side). This is a **route decision**, not a build
authorization: the wiring is a separate authorized capture-lane turn (see Build gate).

## The constraint (why this needed deciding)

Discovered 2026-06-12 (`docs/decisions/ingestible_beauty_screen1_ledger_v0.md`, "Tooling
Discovery"): the **WebFetch tool itself blocks `reddit.com`** ("Claude Code is unable to fetch from
old.reddit.com") for screening agents — both `old.reddit.com` and `www.reddit.com` — and
`site:reddit.com` search-operator queries return zero. This is an **agent-tooling** constraint, not a
Reddit-side block: the capture-harness HTTP runners reach these surfaces fine (recon receipts:
old.reddit listing HTTP 200 → 10 thread URLs; thread body HTTP 200 ~104 KB).

Consequence: the capture lane's GO Reddit read shape (`capture_recon_index_v0.md`, Forums/threads) is
GO **for the capture runner** but **unusable by WebFetch-based screening agents**. The outstanding
old.reddit search-surface receipt is therefore **not closable by a screening agent at all** — only by
the capture runner. So the only mechanized Reddit path for screening *is* the capture runner.

## Decision — a layered route (adopt the discovery lane's recommendation)

1. **DEFAULT — snippets-only.** Screening agents take Reddit origination signal from search snippets
   only. Already encoded in the Walker Equipment Kit (KNOWN WALLS: "reddit.com … snippet-mine only,
   and record what you needed so the orchestrator can route it"). This is the floor; no change needed.
2. **DURABLE REAL-READ — wire the capture runner as a bounded screening-read service.** When a screen
   needs real Reddit reads, its orchestrator invokes the capture runner under this contract:
   - **logged-out public reads only** (no logins, no entitled-account use for screening);
   - **per-screen bounded** — starts and stops with the screen; **no standing service, crawler,
     scheduler, or monitor**;
   - **invoked by the screen's orchestrator**, not by walkers directly;
   - **entitlement gate first** (playbook Step 0 / pattern 4): public content only, never defeat an
     auth/access-control gate; human-rate; full receipt per the playbook;
   - **first act = the outstanding receipt** — one bounded GET on
     `old.reddit.com/r/<sub>/search?q=…&restrict_sr=on&sort=new` recording status / bytes /
     `/comments/`-marker count + the `.json` rate ceiling, closing the capture-lane residual.
3. **FALLBACK — operator-manual.** The owner runs fetches for specific threads when the service is not
   available.

These are non-exclusive layers (graceful degradation), not a single all-in commitment.

## Build gate (load-bearing)

The wiring is a **separate authorized capture-lane build turn**. This decision authorizes no build,
no fetch, no service stand-up. The commission's boundaries bind that future turn: **no new
fetch/search infrastructure** (it wires the existing runner), **no standing crawler**, **no
entitlement bypass**.

The one structural line the build must hold: the service stays **per-screen-bounded and
entitlement-gated**. A *standing* screening-read service would be a standing crawler — the exact line
the owner has repeatedly held (capture risk posture; no farm). Bounded-invocation is the difference
between "the runner answers a screen's bounded question" and "a service that watches Reddit."

## Propagation (deferred, by design)

Until the wiring lands, the kit's KNOWN WALLS Reddit line (snippets-only + orchestrator-routes-it)
already reflects the current state, so **no kit amendment is made now**. When the build lands, the
discovery lane adds a dated note to the kit's KNOWN WALLS / READ ESCALATION block recording the wired
path, and the beauty card-set cards 4–6 caveat is replaced. Cross-lane ownership: the kit/screening
side is discovery-lane-owned (amend by dated note there); this record is the capture-spine provider
side.

## Non-claims

A route decision, not a build authorization, validation, readiness, or acceptance. No capture
performed or authorized here. The bounded screening-read service does not exist until a separate
authorized turn builds it; this record specifies its contract so that turn does not invent one.
