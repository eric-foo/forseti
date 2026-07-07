# Forseti Brand-Asset Acquisition Lane — Handoff Packet

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (workflow record)
scope: >
  Spins off a bounded lane to execute the Forseti brand-asset acquire-now
  checklist: trademark/collision screen, forsetihq.com control confirmation,
  @forsetihq handle registration, domain email setup, defensive-variant
  recommendation, and a dated outcomes note. Owner executes all purchases and
  account creations; the lane researches, prepares, and records. First durable
  record of the 2026-07-02 owner naming/carve-depth decisions (quoted verbatim
  in Frozen Decisions).
use_when:
  - Starting or resuming the Forseti brand-asset acquisition lane.
  - Checking what the owner decided about the Forseti name, carve depth, or near-term web posture before a decision record exists.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/product_lead/proof_charter/forseti_claim_defense_doctrine_v0.md
  - orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md
stale_if:
  - A Forseti brand-architecture decision record lands in docs/decisions/ (it then owns these decisions; this packet becomes history).
  - The owner amends the naming, carve-depth, or web-posture decisions.
```

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-02
- created_by_lane: Forseti company-design chat lane on worktree branch `claude/confident-mendeleev-a74e65` (provenance only; not an authority claim)
- workspace: the Orca repository (authored in worktree `.claude/worktrees/confident-mendeleev-a74e65`)
- handoff_path: `docs/workflows/forseti_brand_asset_acquisition_lane_handoff_v0.md`
- expected_branch: authored on `claude/confident-mendeleev-a74e65`; receiver normally reads this packet from `main` after the lane PR merges, or from the lane branch pre-merge
- expected_head: authoring base `04106660e4b8c6191f39859297eea3798e15b075`; the commit adding this packet advances the lane branch beyond that — verify the packet file exists at your HEAD rather than pinning this SHA
- expected_dirty_state_including_handoff_file: clean tree at authoring; this file is the only new artifact (untracked until the lane commit)
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

Derived from owner words in the sending thread (2026-07-02); no `workflow-goal-framing` artifact exists. Orientation, not authority — confirm with the owner at lane start (the owner is the courier).

- long_term_goal: Establish Forseti as the company brand carrying Orca's evidence-backed consumer-market decision-intelligence thesis, with the Creator Signal fragrance carve-out as a thin endorsed sub-brand.
- anchor_goal: Secure the Forseti brand assets that are cheap now and expensive or impossible later — name clearance, domain control, social handles, domain email — with zero customer-facing claims and zero agent-executed purchases.
- success_signal: Trademark/collision screen result reported to the owner; forsetihq.com confirmed under owner control; @forsetihq handles registered on the named platforms (or unavailability recorded with an owner-chosen fallback); domain email live with SPF/DKIM/DMARC; all outcomes recorded in a dated note in this repo.

## Open Decision / Fork

- decision: Defensive domain variants (e.g. forsetihq.io/.ai/.co, forseti.* alternatives) — buy which, if any?
  - options: none; minimal set (only trivially cheap ones); broad set
  - already constrained / off the table: nothing is bought by an agent; broad speculative shopping conflicts with smallest-complete
  - trade-offs: minimal spend vs. squatter risk on adjacent domains
  - owner of the call: owner, at purchase time
  - recommendation and why: minimal set, low priority — the moat is elsewhere; squatting risk on obscure variants is low
- decision: Handle fallback if `@forsetihq` is taken on a platform
  - options: platform-specific variant (e.g. `@forsetihq_`, `@useforsetihq`); skip that platform for now
  - owner of the call: owner; the lane prepares the availability facts and options
- Out of scope but named so it is not absorbed: the creator sub-brand name (and its domain/handles — the "second tranche") is a separate owner decision owned by the product lane, not this lane.

## Drift Guard

- No agent-executed payments, purchases, or unattended account creations. The lane researches, verifies, and prepares steps; the owner executes (or the agent acts only in an owner-attended session). Violating this breaches the financial-action and outward-facing-action boundaries.
- Trademark screen gates spend: if the screen finds a material collision (SaaS/business-intelligence space, US), stop and route to the owner before any further brand spend.
- No public marketing copy or claims. Near-term web posture is holding + waitlist only (owner decision below). Any placeholder text obeys the claim-defense doctrine's wording discipline ("built to" vs "proven at") — read that doctrine before writing ANY outward-facing copy. Willingness-to-pay is explicitly unvalidated; nothing may imply customers, validation, or readiness.
- No legal entity work. The owner decided brand/product-level carve-out only (Frozen Decisions).
- No sub-brand naming, no creator-product domain purchases (second tranche fires only after the owner's naming decision).
- Do not rename Orca→Forseti anywhere in this repository. "Orca" is the internal project codename throughout; that is intentional, not stale branding. The brand-architecture decision record (a product-lane follow-up, not this lane) is where the naming relationship gets recorded.
- This lane must not expand into capture, product, publishing, or website builds. The repo-wide time-sensitive asset is sustained niche capture, owned by other lanes.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` and `.agents/workflow-overlay/README.md` first, per project rule)
- targets to enter the ladder: `forseti/product/spines/product_lead/proof_charter/forseti_claim_defense_doctrine_v0.md` (before any copy); `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md` and `orca/product/spines/creator_signal/creator_signal_market_sizing_v0.md` (context for what the brand will carry)
- already loaded by sender (weak orientation, 2026-07-02, at base `04106660`; not authority): product thesis (`docs/decisions/forseti_product_thesis_consumer_demand_v0.md`), wedge record (`docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`), the two creator_signal docs above, CSB spine README
- must load first (before strict or actionable steps): `AGENTS.md`, overlay README; claim-defense doctrine before any outward-facing text
- load rule: receiver re-runs progressive source loading per overlay; this loaded-set only seeds the ladder

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

These owner decisions exist only in the sending chat; this packet is their first durable record. Compare target = the verbatim quotes in Frozen Decisions below; confirm the capsule with the owner at lane start before strict or actionable use.

- Forseti is the company name; forsetihq.com is the domain; owner is acquiring the domain personally.
- Carve depth: brand/product-level only; no legal entity split now (triggers for a later split: acquisition interest, dedicated outside funding, or a liability reason).
- Carve-out role: keep both futures open — entry-wedge-then-upsell AND standalone/acquisition path.
- Near-term web posture: holding + waitlist only; not fully public.
- Creator sub-brand naming deferred; recorded constraint: the name should stretch to beauty (fragrance scoped in the tagline, not baked into the name).
- Background (verify pointer): the carve-out itself is ratified as working goal in `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md` (Status section, PR #550, incl. Direction Update v0.1 foundation-first sequencing).

## Active Objective

Execute the Forseti brand-asset acquire-now checklist (screen, domain confirmation, handles, email, defensive-variant recommendation) with the owner executing every purchase and account creation, and record the outcomes durably in this repo.

## Exact Next Authorized Action

1. Run the trademark/collision screen for "Forseti": USPTO search in classes 35 and 42, plus a general web/company-registry scan for existing companies named Forseti (especially SaaS, data, analytics, intelligence). Research only. Report findings to the owner before any further brand spend.
2. Confirm with the owner that the forsetihq.com acquisition completed (owner said 2026-07-02 they are getting it first); record registrar and date in the outcomes note. Never store credentials in the repo.
3. Scan handle availability for `@forsetihq` on: LinkedIn (company page), X, Instagram, TikTok, YouTube, GitHub (org). Prepare exact registration steps per platform; the owner executes creation (or an owner-attended session does).
4. Prepare domain-email setup steps (e.g. Google Workspace on forsetihq.com) including an SPF/DKIM/DMARC checklist; the owner executes.
5. Deliver the defensive-variant recommendation (Open Decision above) as a short chat memo; the owner decides.
6. Write the dated outcomes note at `docs/workflows/forseti_brand_asset_acquisition_outcomes_v0.md` (retrieval header per `.agents/workflow-overlay/retrieval-metadata.md`) recording: what was acquired, when, where; unavailabilities and chosen fallbacks; screen result. Then commit/push/PR per the per-lane flow in `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.

Stop conditions: material trademark collision (stop, route to owner); any step requiring payment or unattended account creation (owner executes); any pressure to write public copy (out of scope; claim-defense doctrine unread by sender — see ledger).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (root), `.agents/workflow-overlay/README.md` and the overlay files it names.
- Overlay or equivalent authority: `.agents/workflow-overlay/artifact-folders.md` (this packet's folder, `docs/workflows/`, is an accepted workflow-records home).
- User constraints: owner executes all purchases/account creations; holding + waitlist web posture only; no entity split; no sub-brand work.
- Source-read ledger:
  - `forseti/product/spines/product_lead/proof_charter/forseti_claim_defense_doctrine_v0.md`
    - Role: wording discipline for ANY outward-facing copy
    - Load-bearing: yes (for step 6 phrasing and any placeholder text)
    - Compare target: reread-required — the SENDER DID NOT READ THIS FILE; it is cited by the thesis as owner-signed. Receiver must read it fresh before writing outward-facing words.
    - Last checked: not read by sender (referenced only)
    - Reuse rule: read fresh; do not act on this packet's one-line summary of it
  - `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md`
    - Role: context — what the brand will eventually carry (carve-out shape, foundation-first sequencing, PR #550 ratification)
    - Load-bearing: no (for this lane's mechanics)
    - Compare target: content at commit `04106660e4b8c6191f39859297eea3798e15b075`
    - Last checked: 2026-07-02
    - Reuse rule: orientation only; reread if the file changed past that commit
  - `docs/decisions/forseti_product_thesis_consumer_demand_v0.md`
    - Role: context — product boundary and claim-tier discipline the brand must not contradict
    - Load-bearing: no
    - Compare target: content at commit `04106660e4b8c6191f39859297eea3798e15b075`
    - Last checked: 2026-07-02
    - Reuse rule: orientation only
  - Owner decision capsule (this packet, Frozen Decisions)
    - Role: the naming/carve-depth/web-posture decisions this lane executes under
    - Load-bearing: yes
    - Compare target: verbatim quotes below; confirm with the owner at lane start
    - Last checked: 2026-07-02 (live in sending thread)
    - Reuse rule: owner confirmation supersedes; a later decision record in `docs/decisions/` supersedes both
- Source gaps: no decision record yet for the Forseti naming/brand architecture ("Forseti" appears nowhere else in the repo as of base `04106660`); claim-defense doctrine unread by sender.
- Strict-only blockers: none for the research steps; every purchase/creation step is owner-gated by design.
- Not-proven boundaries: nothing in this lane is validation, willingness-to-pay evidence, buyer proof, or readiness; a completed checklist proves asset control only.

## Current Task State

- Completed: company-design recommendation delivered and owner-ratified in the sending thread (see Frozen Decisions); this packet written.
- Partially completed: forsetihq.com acquisition (owner self-executing, unconfirmed at handoff).
- Broken or uncertain: none known.

## Workspace State

- Branch: `claude/confident-mendeleev-a74e65` (worktree)
- Head: `04106660e4b8c6191f39859297eea3798e15b075` at authoring (advances when this packet commits)
- Dirty or untracked state before handoff: clean
- Dirty or untracked state after writing the handoff file: this file untracked until the lane commit
- Target files or artifacts: this packet; the future `docs/workflows/forseti_brand_asset_acquisition_outcomes_v0.md`
- Related worktrees or branches: none required; the receiving lane is documentation-plus-external-research and may run as a fresh session with a branch off `main` (solo sequential writing) per the isolation rule in `AGENTS.md`

## Changed / Inspected / Tested Files

- `docs/workflows/forseti_brand_asset_acquisition_lane_handoff_v0.md`
  - Status: new (this packet)
  - Role: the handoff itself
  - Important observations: first durable record of the 2026-07-02 owner decisions
  - Symbols or sections: Frozen Decisions carries the owner-word quotes

## Frozen Decisions

Owner decisions, 2026-07-02, in the sending thread (verbatim quotes are the compare targets):

- Decision: Company name Forseti; domain forsetihq.com; not yet acquired at decision time; owner acquiring it personally.
  - Evidence: owner words — "we have decided (not acquired yet) forsetihq.com and Forseti as company name"; "im getting forsetihq.com first - what else do i need to get?"
  - Consequence: this lane clears and secures the surrounding assets; it does not buy the domain.
- Decision: Carve depth is brand/product-level only; no legal entity split now.
  - Evidence: owner asked for a recommendation ("recommend actually - this one i have no idea"), the sending lane recommended brand-only with named entity-split triggers, and the owner replied "1 - agree" to that recommendation in the follow-up turn.
  - Consequence: no entity, IP-assignment, or cap-table work anywhere in this lane.
- Decision: Near-term web posture is holding + waitlist only.
  - Evidence: owner words — "we probably dont need fully public yet so probably 1" (option 1 = holding + waitlist).
  - Consequence: no public product site, no marketing claims.
- Decision: Carve-out long-run role stays open (entry-wedge upsell AND standalone both preserved).
  - Evidence: owner selected "Keep both open (Recommended)" in the sending thread's decision questionnaire.
  - Consequence: brand assets must stay cleanly separable (own handles/domain per brand when the sub-brand exists).

## Mutable Questions

- Question: Which defensive domain variants, if any?
  - Why still mutable: owner call at purchase time; cost/benefit trivial either way
  - What would resolve it: the lane's short memo (step 5) plus owner word
- Question: Handle fallbacks where `@forsetihq` is unavailable
  - Why still mutable: availability unknown until scanned
  - What would resolve it: the step-3 scan plus owner choice
- Question: Should the outcomes note be promoted into (or referenced by) the future brand-architecture decision record?
  - Why still mutable: that record is a product-lane follow-up not yet authored
  - What would resolve it: the product lane authoring `docs/decisions/forseti_company_brand_architecture_v0.md` (or equivalent) and citing the outcomes note

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: treating "Orca" naming in repo artifacts as stale branding to clean up under the Forseti decision.
  - Why stale or dangerous: repo-wide renames would churn owner-locked records for zero product value; Orca remains the internal codename intentionally.
  - Current replacement: the Drift Guard's no-rename rule; naming relationship lands later in the brand-architecture decision record.

## Commands And Verification Evidence

- Command:
  ```bash
  git status --porcelain=v1 -b && git log -1 --format="%H %s"
  ```
  Result:
  - Passed/failed/not run: run 2026-07-02 at authoring
  - Important output: `## claude/confident-mendeleev-a74e65` (clean); `04106660e4b8c6191f39859297eea3798e15b075 Record owner ratification of Gate 1 and Gate 2, add post-ratification handoff (#579)`
  - Re-run target so the receiver can confirm rather than trust: run the same command in the receiving workspace; expect this packet present and tracked

## Blockers And Risks

- Blocker or risk: "Forseti" fails the trademark/collision screen.
  - Evidence: unscreened as of handoff; the name is a known Norse mythological figure and plausibly in commercial use somewhere.
  - Likely next action: stop, present findings and alternatives to the owner.
- Blocker or risk: `@forsetihq` unavailable on one or more platforms.
  - Evidence: unscanned as of handoff.
  - Likely next action: present fallback options (Open Decision).
- Blocker or risk: agent tooling pressure to complete purchases/creations directly.
  - Evidence: checklist items end in payment/account steps.
  - Likely next action: hand the prepared steps to the owner; never execute.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - The owner decision capsule (confirm with the owner at lane start — one message)
  - Claim-defense doctrine content (read fresh; sender never read it)
  - forsetihq.com control status (ask owner; do not assume acquired)
  - This packet's presence at your HEAD (it may have merged to `main` or still sit on the lane branch/PR)
- Compare target for each: verbatim quotes in Frozen Decisions; the doctrine file itself; owner word; `git log`/file presence.
- Load outcomes and what each means: `REUSE` (all verified — start at step 1), `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`, `BLOCKED_MISSING_PACKET`, `BLOCKED_UNVERIFIABLE` per the workflow-handoff load protocol; do not continue from an unverified packet.
- Sources that must be reread if drift is detected: `AGENTS.md`, overlay README, and any superseding decision record in `docs/decisions/` mentioning Forseti.

## Do Not Forget

- The screen (step 1) comes before everything else that costs money or creates public accounts — it is the one step that can invalidate the name.
