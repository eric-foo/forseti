```yaml
retrieval_header_version: 1
artifact_role: Capture-investigation method playbook (v0, REVIEW-HARDENED + RISK-POSTURE-AMENDED, non-authorizing doctrine)
scope: >
  The repeatable method for deciding whether and how a NEW source can be captured — within the
  owner-authorized capture boundary, and by the cheapest route. Converts the old runner "ladder"
  into a problem-indexed route catalog: read the problem, then point to the route. MVP scope is the
  risk posture + the read + the route catalog + the pointer + the guardrails. Per-source recipe
  cards are a growing tail authored BY probes, not here.
use_when:
  - Onboarding a new source/platform and deciding the cheapest working capture route.
  - Commissioning a capture probe lane (the probe runs this method, returns a recipe card, NO-GO, or CATALOG_GAP).
  - Checking whether a "blocked"/NO-GO call was made honestly (re-probed, logged, access-bounded).
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/capture_recon_index_v0.md
stale_if:
  - A probe surfaces a route the catalog lacks (CATALOG_GAP) -> amend the catalog.
  - The owner changes the risk posture (e.g. commercial/licensed phase begins, or the access-control line moves).
  - The existing per-source playbooks are formally re-homed as recipe cards under this method.
status: RISK_POSTURE_AMENDED_V0
review_provenance: >
  De-correlated adversarial artifact review by a non-Anthropic (GPT-family) controller against
  playbook v0 @ sha256 7FDA9AFDB16BCC6768A247C1F0E433D3503016D72052D49B261B5C65DDBEBA22, recon index
  @ sha256 ECDE5452...B7532 as context. Verdict ACCEPT_WITH_CHANGES; AR-01..AR-07 + 2 faithfulness
  items adjudicated-ACCEPTED and applied (hardened @ sha256 D5B4DCCE...18B388).
  POST-REVIEW OWNER AMENDMENT: the entitlement-first / never-bypass-ToS posture that the review
  covered was deliberately changed by an owner risk decision — see "Risk posture". That amendment is
  an owner's-prerogative risk acceptance, OUTSIDE the de-correlated review's scope; the review
  validated the method's structure under the prior (stricter) posture, not this one.
```

# Capture-Investigation Playbook (v0, review-hardened + risk-posture-amended)

## What this is — and is not

This is the **method** for one question about any new source: *can we get the real content, within
what we're allowed to take, by the cheapest route?* You hand it a target, it walks a diagnosis, and
a probe banks a reusable cheat-sheet for that source type.

It is **not** code, not a harness, not a guarantee any source is capturable. It can honestly
conclude **NO-GO**, **PARTIAL**, or **CATALOG_GAP** — those are successful diagnoses. It is
non-authorizing: it grants no capture/build/merge authority; each probe runs under its own bounded
authorization and per-operation network approval.

**MVP scope:** the risk posture + the read + the route catalog + the pointer + the guardrails.
Per-source **recipe cards** are authored BY probes and accumulate over time. TikTok is the first
*intended* probe target; the recon index shows TikTok/Instagram have no technical recon yet, so any
social card is speculative until probed.

## Risk posture (owner-authorized, pre-commercial)

The owner authorizes, for the pre-commercial proving phase, **capturing publicly-viewable content
even where a site's ToS forbids automation** — including **circumventing anti-bot measures**
(fingerprint / challenge handling, proxies, geo congruence) and **automated capture**. The owner
accepts the ToS / civil risk and will pursue licensed or commercial routes once the signal is proven
and resources justify it.

This authorization is **bounded — not blanket**:

- **Human-rate, targeted, and directed only.** No mass scraping, no crawl-at-scale, no DoS-level
  volume. One source, one bounded question at a time, at roughly the request rate a human reader
  would generate.
- **The access-control line still holds.** Do NOT defeat authentication or access control to reach
  content that is not publicly viewable, or that you are not entitled to (no logging in as someone
  else, no paywall / private-account / private-API bypass). Use your OWN entitled access where you
  hold it; otherwise that content stays out. *ToS-against-scraping is now accepted risk; defeating an
  auth gate is not — that is the line between civil/ToS exposure and unauthorized-access exposure.*
- **No private personal data of individuals / no surveillance-grade harvesting** (unchanged separate
  legal line — see `data_capture_spine_future_exploration_lanes_v0.md`). Market-level signal
  (product/brand/hashtag/aggregate counts) is fine; building dossiers on individuals is not
  (exception: internal wind-caller calibration per `docs/decisions/wind_caller_calibration_carveout_v0.md`
  — bounded to ≤10 own operating/capture accounts (starting ≤5); subject-creator roster uncapped
  within the vertical; active capture: attended (human-initiated), faster-than-human pace;
  passive monitoring: human-initiated, time-bounded, self-terminating (no discovery during);
  public data only, pre-commercial, internal only; that carve-out does not change the general
  dossier prohibition).
- **No secrets, no exit-IP leak, per-operation network approval** (unchanged operational hygiene).

**The hard line moved from "ToS forbids it" to "it's behind an access-control gate you can't
legitimately pass."**

## The core shift: ladder -> catalog

The old "runner ladder" implied climbing rungs in order. This playbook replaces that with
**read the problem, then point to the route.** Routes are a menu indexed by the problem each
solves; the diagnosis selects the route. Blind climbing wastes probes and can mis-stop — a headless
403 is *not* "a browser won't help" (see Daimler in the recon index).

## Guardrails (these frame everything; non-negotiable)

1. **Access-control gate — first, always (executable as Step 0).** Before any technical attempt,
   classify whether the content is **publicly viewable** vs. **behind an access-control / auth
   gate**. Public content is in scope even against ToS, with anti-bot circumvention, under the Risk
   posture (human-rate, bounded). An auth/access-control gate is only passable with your own entitled
   access; never defeat it. No secrets recorded — endpoints-as-secrets, credentials, exit-IP never
   captured.
2. **Two-axis bar.** "Did we get through?" is the necessary **gate**; "is what we grabbed the real
   thing?" is the **win**. GO requires *checkable* source-native evidence (see Step 3) — reachable
   -but-paraphrase (WebFetch on M&I/BIWS) is **PARTIAL, not GO**. Never let the foot-in-the-door, or
   an asserted-but-unverifiable capture, pass as the real grab.
3. **The receipt.** Every run logs the full receipt (see Step 3) — access classification, routes
   tried *and skipped-with-reason*, evidence locators, fidelity evidence, why it stopped, the
   verdict, and the routes now forbidden without a new fact. An honest NO-GO records *what failed*.
   No receipt -> the verdict is not trustworthy and escalation is unbounded.
4. **"Blocked" is a symptom, not a verdict — but re-probing is bounded.** A 403 / empty body /
   failed headless / missing lazy content / anti-bot challenge is a hypothesis to re-probe at another
   route — not a NO-GO. Re-probe **only when the next route tests a different hypothesis**: repeating
   the same route class requires a new fact, changed approach, or a changed environment; stay
   human-rate; and never cross the access-control line. The recurring expensive error is a premature
   "blocked" that abandons capturable material (Daimler, Sephora, Teal, WSO); the opposite error is
   thrashing the same route forever, or escalating volume past human rate.

**Screening-side consumer (reverse pointer, 2026-06-12).** These read-escalation patterns
(Guardrail 4 + the Step 2 pointer) are distilled for *screening posture* — public pages, no logins,
no bulk, URLs + short quotes only — into the **Walker Equipment Kit** in
`docs/product/foundation/orca_vertical_exploration_guide_v0.md` (discovery-lane-owned). Keep them in
sync: when a route-escalation pattern here changes, the kit's READ ESCALATION / KNOWN WALLS block may
need a dated note. Packet-grade capture still routes through this method; the kit is screening-read
only. (Tooling note: WebFetch-based screening agents cannot fetch `reddit.com` at all — only the
capture runner can; see `docs/decisions/screening_reddit_read_route_decision_v0.md`.)

## Step 0 — The access-control gate (run before any technical probe)

Classify the target as one of: **publicly-viewable · publicly-viewable-but-ToS-restricted ·
authenticated/access-controlled · operator-supplied/manual-only · unknown.**

- **publicly-viewable** and **publicly-viewable-but-ToS-restricted**: **in scope.** Anti-bot
  circumvention and automated capture are authorized under the Risk posture (human-rate, targeted,
  bounded). ToS-against-automation is accepted risk, not a stop.
- **authenticated / access-controlled**: use only your OWN entitled access (your logged-in account,
  an API key you hold); do NOT defeat the gate. If you have no entitled access, that content is out.
- **operator-supplied/manual-only**: the owner supplies the bytes (entitled docs/PDF).
- **unknown** (after a good-faith look): determine public-vs-gated before running routes; if you
  genuinely cannot tell whether content is public, treat as gated and stop.
- Record the classification in the receipt. This gate fires first; nothing in Steps 1–3 runs before
  it.

## Step 1 — The read (substrate-first)

Locate **where the signal actually lives**, and name the blocker — *before* picking a tool.

- **Where does the signal live?** vendor API rendered first-party (Bazaarvoice); embedded
  page-state (`__APOLLO_STATE__` / `__NEXT_DATA__` / a JSON blob); rendered DOM; a download
  (PDF button); raw JSON (Reddit); an internal web API the page calls; **mobile/app-only** (no useful
  public web surface — flag loudly; the catalog may have no route -> CATALOG_GAP, not NO-GO).
- **What's blocking?** 403 / empty / lazy-load-not-fired / anti-bot challenge / login-wall /
  paraphrase-only. (A **login-wall** is an access-control gate — Step 0 governs it; an **anti-bot
  challenge** on public content is now a route problem, not a stop.)
- **Output:** a one-line problem statement — `<signal> lives in <substrate>; blocked by <symptom>`.

## Step 2 — The pointer (problem -> route)

Pick the cheapest route that fits the located substrate. A symptom quick-reference — a shortcut
**under** the substrate read, never instead of it:

| Symptom | Likely cause | First re-probe |
|---|---|---|
| 403 on direct fetch | headless/bot signature, or host block | real browser context; then visible browser + user action; then anti-bot route |
| empty / sparse body | content lazy-loads or is JS-rendered | progressive scroll to fire observers; locate embedded state |
| content present but reworded | tool returned paraphrase (fidelity fail) | a route that preserves bytes (browser page content / embedded-state extract) |
| 403 *and* headless also 403 | NOT "browser won't help" — visible-context / anti-bot detection | visible browser + user action (Daimler); then anti-bot fingerprint/challenge route |
| anti-bot challenge on PUBLIC content | bot detection (Kasada/Akamai/etc.) | anti-bot route (fingerprint/challenge handling, proxy/geo) — authorized, human-rate |
| login-wall | access-control gate (Step 0) | use OWN entitled access, or stop — do NOT defeat it |
| reviews/section missing | IntersectionObserver lazy-load not fired | progressive/incremental scroll (Sephora) |

## Step 2b — The route catalog (the de-laddered ladder)

Each route by what it solves / cost / fidelity it preserves / access note. **Not an order — a
menu.** Cheapest fit wins.

| Route | Solves | Cost | Fidelity preserved | Access note |
|---|---|---|---|---|
| archive.org / Wayback (cross-archive ladder rung 1) | historical / pre-cutoff state; current page gone/blocked | low | snapshot bytes, served-time-verified <= cutoff (availability != body — check both) | public |
| archive.today / Memento (ladder rung 2) | pre-cutoff state when Wayback misses; closes the single-archive SPOF for ordinary brand/retailer pages | low-med | memento bytes, served-time-verified <= cutoff (mirror-family host-anchored) | public; no-gate-defeat (CF/CAPTCHA challenge -> STOP; HTTP 429 -> retry/backoff) |
| publisher version-history (MediaWiki / GitHub) | pre-cutoff state of a doc/wiki/repo from the publisher's OWN version history | low | the publisher's exact revision bytes, served-time-verified <= cutoff | public API (needs explicit wiki/repo coordinates) |
| direct-HTTP | static first-party HTML/JSON | lowest | raw bytes | public |
| real browser (headless) | JS-rendered DOM | med | rendered bytes | public |
| visible browser + user action | headless-detected 403; user-gated download (PDF) | med-high | real bytes via the real UI path | public; own entitled access if gated |
| progressive / incremental scroll | lazy-load / IntersectionObserver content (reviews) | med | first-party-rendered bytes | public |
| anti-bot / cloakbrowser + proxy/geo | anti-bot challenge on public content; geo friction | high | rendered bytes *(expected, not yet demonstrated — see route maturity)* | public; authorized under Risk posture; human-rate; no secrets/exit-IP |
| vendor-API first-party render | reviews/widgets a vendor API renders into the DOM (Bazaarvoice) | low-med | the API's real values | public via the page |
| embedded-state / internal-API extract | signal in `__APOLLO_STATE__` / `__NEXT_DATA__` / a JSON blob / a public page's own internal API | low | exact embedded values (cite field+value) | public via the page (not an auth-gated private API) |
| operator-supplied | owner provides the bytes (entitled docs/PDF) | n/a | as-supplied (verify hash / magic bytes) | entitled |

**Route selection (not table order).** A route is "in catalog" for this probe only when its
Solves/Access cells match the **Step 0 classification** AND the **Step 1 substrate/problem**.
Do not advance by table order. If a route fails, that's a symptom -> re-read -> the next *matching*
route (under the Guardrail 4 bound, human-rate). If **no row matches**, stop as **CATALOG_GAP**
(record the missing-route candidate) — *unless* it's behind an access-control gate you can't pass,
which is NO-GO. Reach NO-GO only after the matching routes are exhausted, with the receipt.

**Route maturity (faithful to the recon index).** Progressive-scroll is *capture-proven* (Sephora
reviews; worktree-pending). The `anti-bot / cloakbrowser + proxy/geo` route is *setup/architecture-
ready, not yet end-to-end capture-proven* — treat its fidelity as **expected, not demonstrated**,
until a probe proves it. Don't cite an unproven route as evidence of capturability.

Proxy profiles are shared Source Capture browser-route configuration, not CloakBrowser-owned
state. A runner may opt into a registered proxy profile by label while keeping endpoint,
credentials, exit IP, and store path out of packets; CloakBrowser remains one possible
browser backend rather than the owner of proxy semantics.

### Cross-archive historical capture (the ladder + the runner)

For **pre-cutoff historical state**, the three archive rows above are wired into one bounded,
cheapest-first **LOCATE ladder** so a single archive is no longer a single point of failure:
`runners/run_source_capture_historical_packet.py` (orchestrator: `source_capture/historical_capture.py`).

- **Ladder order:** Wayback CDX -> archive.today TimeMap -> publisher version-history (the last *only*
  when the source is a doc/wiki/repo — it needs explicit MediaWiki/GitHub coordinates, not a plain URL).
  Stop at the **first served-time-verified pre-cutoff body**; a locate-hit whose body fails (transport,
  non-2xx, or served-time/identity verification) is a **PARTIAL that escalates** to the next rung,
  never a fake-success rollup.
- **No-lookahead (served-time, per rung):** selection filters to memento/revision timestamp <= cutoff,
  AND the *served* snapshot is re-verified <= cutoff (a replay redirect can serve a post-cutoff capture
  for a pre-cutoff request — that leak is rejected). A non-2xx body is not body-honesty and is rejected.
- **No-gate-defeat:** archive.today's anti-bot **challenge -> STOP** (never solved); a plain HTTP 429
  rate-limit -> retry/backoff (in-posture). Wayback is not Cloudflare-fronted; it simply throttles.
- **Honest NO-GO:** when every rung misses (or yields no clean pre-cutoff body), the run still writes
  a packet whose receipt records the full ladder trace, so exhaustion is auditable.
- **Receipt:** the selected rung's existing Source Capture Packet, plus a thin preserved
  `archive_locate_metadata.json` side-file recording `archives_tried` / `archive_selected` /
  `body_rung_used` as **neutral mechanical facts** (no scores or verdicts — INV-1).
- **Cutoff form:** the runner takes an ISO-8601 cutoff (e.g. `2024-06-01T00:00:00Z`).

Spec + provenance: `archive_org_refinement_and_source_family_gap_spec_v0.md` (slice E). This subsection
is a `stale_if` catalog amendment documenting landed code (added 2026-06-16); it is outside the
original de-correlated review's scope.

## Step 3 — The verdict + receipt

- **GO:** source-native content captured AND independently checkable — raw bytes/hash, magic bytes
  for files, a DOM/source excerpt with URL+timestamp, an embedded field+value anchor, or equivalent
  route-native evidence. Paraphrased / summarized / reconstructed / only-asserted -> **PARTIAL**.
- **PARTIAL:** reachable but fidelity-limited (paraphrase / asserted-only) or partial coverage
  (availability without body; first page only; bounded enumeration).
- **NO-GO:** not capturable within the access boundary — record *why* (matching routes tried; or the
  auth/access-control gate that can't be legitimately passed).
- **CATALOG_GAP:** capture is in-scope (public, not auth-gated) but this playbook has no matching
  route for the substrate/problem (e.g. mobile/app-only). Record the missing-route candidate; do
  **not** call it NO-GO.
- **Receipt (every run):** access classification · routes tried · routes considered-but-skipped and
  why · evidence locator for each attempt · fidelity evidence · request rate / volume · why it
  stopped · verdict · routes now forbidden without a new fact.

## The output: a recipe card (the growing tail — authored by probes, not here)

A probe banks a card: `{source, substrate, route that worked, triggers, content-anchor, candidate
adapter shape, access posture, request-rate ceiling, known false-diagnoses}`. Cards compound; the
method stays stable. TikTok is the first *intended* probe target — its card (or NO-GO / PARTIAL /
CATALOG_GAP) is authored by that probe, not here.

## Reuse the pin: probe once, then go direct (capture economy)

The banked recipe card / recon-index entry **is the pin**. Once a probe finds the working route for a
source (or the per-archive rung for historical capture), steady-state fetches go **direct to the
pinned route** — do not re-walk the catalog or re-climb rungs on every fetch. Re-probe (re-run the
method) when the pinned route fails **or its output degrades** (slice-G verification / quality
sub-floor — not just transport; a stale pin can still return HTTP 200) — then it is a fresh symptom
under Guardrail 4.
The catalog is a discovery tool, not a per-fetch cost. Distilled cell: `probe-then-pin-rung` in
`docs/decisions/distillation_binding_data_capture_v0.md` (held; the automated dispatcher form is
capture-spine spec slice F, pending build).

## Known gaps (honest)

- **No route for mobile/app-only substrate.** If a probe finds the signal lives only in a phone app
  with no public web surface, that's a **CATALOG_GAP / catalog amendment** (a new route), not a
  default NO-GO.
- **No technical recon for TikTok/Instagram, and no media/video capture recipe.** Any card for those
  surfaces is speculative until probed. (Under the amended posture their *public* surfaces are now
  in-scope; their login-walled surfaces remain access-gated.)
- **Anti-bot capability is authorized but not yet proven.** Authorization (Risk posture) is not the
  same as a working defeat of a given anti-bot system; whether a specific challenge can be passed
  at human-rate is an engineering question a probe answers.
- **Rate-limited / commercial / entitled APIs** are entitlement / API-contract routes, not anti-bot
  routes; use your own entitled access, don't defeat the auth.
- **Recipe cards are not yet authored.** This MVP is the method only.

## Non-claims

Method doctrine, MVP, review-hardened + owner-risk-amended draft. Not validation/readiness/
acceptance, not legal advice. The Risk posture is an owner risk decision, not a legal opinion;
legal/ToS exposure is real and owner-accepted for the pre-commercial phase. Grants no
capture/build/merge authority; per-operation network approval still required per probe. Distilled
from `capture_recon_index_v0.md`; worktree-pending recon is weaker than merged primary artifacts.

```yaml
direction_change_propagation_note_2026-06-15: >
  Downstream surface of carve-out 2026-06-15 cap-redefinition: cap now counts own
  operating/capture accounts (≤10, starting ≤5), not subject creators; subject-creator
  roster uncapped within the vertical; active capture = attended (human-initiated),
  faster-than-human pace; passive monitoring = human-initiated, time-bounded,
  self-terminating (no discovery during). Risk-posture footer (dossier carve-out
  exception line) updated accordingly. "That carve-out does not change the general
  dossier prohibition" preserved verbatim.
```
