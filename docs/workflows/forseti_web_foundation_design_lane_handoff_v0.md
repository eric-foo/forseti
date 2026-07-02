# Forseti Web-Foundation Design Lane — Handoff Packet

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (workflow record; design-lane commission)
scope: >
  Commissions a bounded lane to execute ADR D8's near-term surface: the
  Forseti minimal identity kit and the forsetihq.com holding page (positioning
  line, "built to" paragraph, waitlist capture, privacy notice, contact),
  built as a static site in an external repository and deployed dark. No
  launch, no DNS pointing, no Aphrodite design. Owner executes all account
  creations, purchases, and DNS.
use_when:
  - Starting or resuming the Forseti web-foundation design lane.
  - Checking what the design lane may build, claim, and where its PR boundary sits.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_company_brand_architecture_v0.md
  - orca/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md
stale_if:
  - The owner amends ADR D8 or the brand-architecture record supersedes it.
  - The holding page ships publicly (this lane's job is then done; later site work needs a new commission).
```

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-02
- created_by_lane: Forseti company-design chat lane on worktree branch `claude/confident-mendeleev-a74e65` (provenance only; not an authority claim)
- workspace: the Orca repository (reads + one outcomes note only; the website build happens in an external repository, see Drift Guard)
- handoff_path: `docs/workflows/forseti_web_foundation_design_lane_handoff_v0.md`
- expected_branch: receiver normally reads this packet from `main` after its lane PR merges
- expected_head: verify the packet file and ADR D8 both exist at your HEAD rather than pinning a SHA (authoring branch head at packet write: `fd590e0a` + this packet's commit)
- expected_dirty_state_including_handoff_file: clean tree at authoring apart from this file (untracked until the lane commit)
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

Derived from owner words in the sending thread (2026-07-02); no `workflow-goal-framing` artifact exists. Orientation, not authority — confirm with the owner at lane start.

- long_term_goal: Establish Forseti as the company brand carrying Orca's evidence-backed consumer-market decision-intelligence thesis, with the Creator Signal fragrance carve-out as a thin endorsed sub-brand (ADR D1–D8).
- anchor_goal: Stand up the Forseti web foundation per ADR D8 — the minimal identity kit and the forsetihq.com holding page, built and deployed dark — launching nothing and claiming nothing beyond claim-defense-compliant wording.
- success_signal: Identity mini-kit delivered (text wordmark, 1–2 colors, 1–2 typefaces, calibrated/judicial register); holding page built as a static site in an external repo with positioning line, one "built to" paragraph, waitlist capture, minimal privacy notice, and contact; dark preview URL shared with the owner; all copy passes a fresh claim-defense wording check; outcomes note written in the Orca repo; DNS untouched.

## Open Decision / Fork

- decision: Positioning line + paragraph wording (outward-facing copy)
  - options: the lane drafts 2–3 claim-checked options
  - already constrained / off the table: anything implying customers, validation, readiness, or proof; feed/dashboard vocabulary
  - owner of the call: owner picks the final wording
- decision: Waitlist form provider and static host
  - options: lane recommends (free-tier static host such as Vercel/Netlify/Pages; simple swappable form provider)
  - already constrained / off the table: CMS, backend, auth, paid tiers without owner word
  - owner of the call: owner approves and creates the accounts
- decision: External repo name/location for the site code (suggestion: `forsetihq-web`)
  - owner of the call: owner creates the repo (or approves its creation in an attended step)

## Drift Guard

- **No launch.** Deployed dark (preview URL) only; pointing DNS or otherwise making anything public is owner-executed and out of this lane's authority.
- **No agent-executed purchases or unattended account creations** (host, form provider, GitHub org/repo creation included — owner executes or attends).
- **Claim discipline.** Read `orca/product/spines/product_lead/orca_claim_defense_doctrine_v0.md` — path per repo map; see ledger — FRESH before drafting any copy ("built to" vs "proven at"; tier labels). Willingness-to-pay is unvalidated; nothing may imply customers, demand, validation, or readiness. No feed/dashboard vocabulary anywhere on the forsetihq.com property (ADR D2/D8).
- **Website code never enters the Orca repository.** The Orca repo takes only reads and the outcomes note (docs-write). No `src/`, `app/`, or site scaffolding here.
- **No Aphrodite design work.** Its design fires at the Vetting v0 trigger (ADR D8 item 6). The only Aphrodite fact this lane needs: it will later live at aphrodite.forsetihq.com as a separable site project — do not structure the forsetihq site in a way that entangles it.
- **Identity stays minimal.** Text wordmark, 1–2 colors, 1–2 typefaces. No logo project, no brand book, no design-system buildout (ADR D8 item 4).
- **Privacy notice is mandatory** the moment the waitlist form exists (waitlist emails are personal data).
- **PR boundary (fixed at commissioning, per dev-workflow doctrine item 14):** this lane's Orca-repo edit permission is `docs-write`, limited to its outcomes note, landing as one small lane PR. Bounded implementation authority applies ONLY inside the external website repo. No other Orca-repo writes.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` and `.agents/workflow-overlay/README.md` first, per project rule)
- targets to enter the ladder: `docs/decisions/forseti_company_brand_architecture_v0.md` (D8 is this lane's contract; D1–D7 are its context); the claim-defense doctrine (before copy); `docs/decisions/orca_product_thesis_consumer_demand_v0.md` (source for positioning language — the value proposition and anti-positioning sections)
- already loaded by sender (weak orientation, 2026-07-02; not authority): the ADR (authored this session), thesis, wedge record, creator_signal architecture + sizing
- must load first (before strict or actionable steps): `AGENTS.md`, overlay README, the ADR, claim-defense doctrine
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- The full company design is decided in `docs/decisions/forseti_company_brand_architecture_v0.md` (D1–D8, owner-ratified 2026-07-02 with dated amendments). Verify D8 exists in the copy at your HEAD before acting; it is this lane's entire contract.
- The web posture is holding + waitlist only (D6); the sub-brand is Aphrodite on a subdomain later (D7 amendment + D8); Orca stays the internal repo codename (D1 — never rename).
- Compare target: the ADR file content at your HEAD; if D8 is absent, stop with `BLOCKED_DRIFT` (you are reading a pre-D8 copy).

## Active Objective

Design the Forseti minimal identity kit and build the forsetihq.com holding page per ADR D8, in an external repo, deployed dark, with owner-picked copy — then record outcomes in the Orca repo.

## Exact Next Authorized Action

1. Load authority: `AGENTS.md`, overlay README, the ADR (confirm D8 present), claim-defense doctrine (fresh read), thesis value-proposition section.
2. Draft and present to the owner in chat: (a) identity mini-kit proposal (wordmark treatment, palette, type); (b) 2–3 positioning-line options + the "built to" paragraph + privacy-notice text, each claim-checked. Owner picks.
3. Owner creates the external site repo (suggestion: `forsetihq-web`) and the static-host + form-provider accounts (or attends their creation).
4. Build the static holding page in that repo (no CMS/backend/auth); deploy dark; share the preview URL with the owner.
5. Write the outcomes note at `docs/workflows/forseti_web_foundation_outcomes_v0.md` (retrieval header per `.agents/workflow-overlay/retrieval-metadata.md`): what was built, where the repo/preview live, copy as approved, what remains owner-gated (DNS). Land it as this lane's one small Orca PR per the commissioning grant.
6. Stop conditions: copy that cannot be worded within claim-defense → route to owner; any payment or account creation → owner; any request to point DNS, publish, or start Aphrodite design → out of scope, route back.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (root), `.agents/workflow-overlay/README.md` and the overlay files it names.
- Overlay or equivalent authority: `.agents/workflow-overlay/artifact-folders.md` (outcomes note home: `docs/workflows/`); dev-workflow doctrine item 14 (PR boundary), `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.
- User constraints: owner executes all account creations/purchases/DNS; deploy dark only; minimal identity; site code external.
- Source-read ledger:
  - `docs/decisions/forseti_company_brand_architecture_v0.md`
    - Role: this lane's contract (D8) and context (D1–D7)
    - Load-bearing: yes
    - Compare target: file at receiver HEAD must contain the "## D8 — Web-presence foundation (2026-07-02)" section
    - Last checked: 2026-07-02 (authored this session)
    - Reuse rule: the file at your HEAD governs; if D8 absent → `BLOCKED_DRIFT`
  - claim-defense doctrine (`orca/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md`)
    - Role: wording discipline for all copy
    - Load-bearing: yes
    - Compare target: reread-required — the SENDER DID NOT READ THIS FILE (cited by the thesis as owner-signed); resolve the exact path via `docs/workflows/orca_repo_map_v0.md` if it moved
    - Last checked: not read by sender (referenced only)
    - Reuse rule: read fresh before any copy; do not act on this packet's summary of it
  - `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
    - Role: source of positioning language (value proposition, anti-positioning)
    - Load-bearing: yes (for copy content)
    - Compare target: reread-required (content at receiver HEAD governs)
    - Last checked: 2026-07-02
    - Reuse rule: draw wording from the live file, not this packet
- Source gaps: no design assets exist anywhere yet (greenfield); no external repo exists yet.
- Strict-only blockers: none for drafting; every account/DNS/publish step is owner-gated by design.
- Not-proven boundaries: nothing here is validation, willingness-to-pay evidence, buyer proof, or readiness; a deployed dark page proves plumbing only.

## Current Task State

- Completed: ADR D1–D8 ratified and recorded; acquisition lane commissioned separately (`docs/workflows/forseti_brand_asset_acquisition_lane_handoff_v0.md` — Forseti screen/handles/email; its Aphrodite tranche was emptied by D8).
- Partially completed: forsetihq.com purchase (owner self-executing; confirm before DNS-adjacent steps — though this lane touches no DNS).
- Broken or uncertain: none known.

## Workspace State

- Branch: authored on `claude/confident-mendeleev-a74e65`; receiver runs as a fresh session — Orca-repo work is one docs-write note, so a branch off `main` (solo sequential) satisfies the isolation rule in `AGENTS.md`
- Head: verify packet + ADR-with-D8 at your HEAD (see Load Contract)
- Dirty or untracked state before handoff: clean apart from this file
- Dirty or untracked state after writing the handoff file: this file untracked until the lane commit
- Target files or artifacts: external site repo (to be created); `docs/workflows/forseti_web_foundation_outcomes_v0.md`
- Related worktrees or branches: none required

## Changed / Inspected / Tested Files

- `docs/workflows/forseti_web_foundation_design_lane_handoff_v0.md`
  - Status: new (this packet)
  - Role: the handoff itself
  - Important observations: commissions the design lane; fixes its PR boundary per doctrine item 14
  - Symbols or sections: Drift Guard carries the edit-permission grant

## Frozen Decisions

- Decision: everything in ADR D1–D8 (owner-ratified 2026-07-02, with dated D7 amendment and D8).
  - Evidence: `docs/decisions/forseti_company_brand_architecture_v0.md` (owner words quoted per decision in that record — the record, not this packet, is the authority).
  - Consequence: this lane executes D8 items 3–7 for the forsetihq property only.
- Decision: design order forsetihq-first; Aphrodite design deferred to the Vetting v0 trigger.
  - Evidence: ADR D8 item 6.
  - Consequence: no Aphrodite creative work in this lane.

## Mutable Questions

- Question: final copy wording (positioning line, paragraph, privacy notice)
  - Why still mutable: outward-facing; owner picks from claim-checked drafts
  - What would resolve it: owner selection in step 2
- Question: host + form provider selection
  - Why still mutable: owner creates the accounts
  - What would resolve it: owner approval of the lane's recommendation
- Question: exact external repo name/visibility
  - Why still mutable: owner-owned outward-facing asset
  - What would resolve it: owner creating it in step 3

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: the sending thread's earlier suggestion that the acquisition lane prepare Aphrodite domain/handle availability ("second tranche").
  - Why stale or dangerous: ADR D8 emptied that tranche — no Aphrodite domain or handles are bought pre-launch; Aphrodite lives at aphrodite.forsetihq.com until the public-launch gate.
  - Current replacement: ADR D8 item 1; the public-launch gate bundles own-domain + handles + formal clearance.

## Commands And Verification Evidence

- Command:
  ```bash
  git log --oneline -3 origin/main
  ```
  Result:
  - Passed/failed/not run: run 2026-07-02 at authoring
  - Important output: `c289ecde Add Forseti brand-asset acquisition lane handoff packet (#584)` on main (the ADR through the D7 amendment is merged; D8 + this packet ride a follow-up PR)
  - Re-run target so the receiver can confirm rather than trust: confirm the ADR at your HEAD contains D8 (the Load Contract check)

## Blockers And Risks

- Blocker or risk: receiver reads a pre-D8 copy of the ADR (mid-merge window).
  - Evidence: D8 and this packet land via a PR that follows the already-merged #584.
  - Likely next action: `BLOCKED_DRIFT`; wait for the packet's own PR to merge or read from its lane branch.
- Blocker or risk: copy drift into claim territory (customers/validation/readiness implications).
  - Evidence: claim-defense doctrine unread by sender; wording pressure is normal in landing pages.
  - Likely next action: claim-check every draft against the fresh-read doctrine; route doubtful phrasing to the owner.
- Blocker or risk: scope creep into Aphrodite design, analytics, CMS, or brand-book work.
  - Evidence: classic "while we're at it" drift; ADR D8 forbids each.
  - Likely next action: route back to the owner; do not build.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - ADR contains D8 at your HEAD (else `BLOCKED_DRIFT`)
  - Claim-defense doctrine content (fresh read; sender never read it)
  - Owner confirmation of the goal capsule and forsetihq.com purchase state (one message at lane start)
- Compare target for each: the ADR file; the doctrine file; owner word.
- Load outcomes and what each means: `REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`, `BLOCKED_MISSING_PACKET`, `BLOCKED_UNVERIFIABLE` per the workflow-handoff load protocol; do not continue from an unverified packet.
- Sources that must be reread if drift is detected: `AGENTS.md`, overlay README, and any successor of the brand-architecture ADR in `docs/decisions/`.

## Do Not Forget

- Deployed dark means dark: the lane's success ends at a preview URL plus the outcomes note — the moment anything would become public, the action belongs to the owner.
