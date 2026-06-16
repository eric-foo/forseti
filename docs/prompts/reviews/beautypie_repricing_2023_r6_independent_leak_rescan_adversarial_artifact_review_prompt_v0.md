# Beauty Pie Repricing 2023 — R6 Independent Leak Re-Scan (Adversarial Artifact Review) — Courier Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (adversarial artifact review — independent cross-vendor R6 leak re-scan)
scope: Commission an independent cross-vendor R6 leak re-scan of the AR-01-closed Beauty Pie paired packets; the verdict gates blind-contestant exposure (Phase 6).
use_when:
  - Couriering the post-AR-01-close Beauty Pie packet leak re-scan to a separate-vendor reviewer.
authority_boundary: retrieval_only
branch_or_commit: aec13c3
input_hashes:
  participant_packet_baseline.md: 912cc2843fa643cbffcdd0e77b258354c05ea0c6
  participant_packet_augmented.md: 2b679c59dc9dcd0443718a382e905a6132f3ee92
stale_if:
  - Either packet blob above changes (re-pin and re-issue this prompt).
  - The R6-AR-01 closure criterion in review-lanes / the R5 whitelist doctrine changes.
```

## Orca Start Preflight (prompt author)

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (S0 overlay + Judgment-Spine evidence-ladder subset + named case artifacts + prior R6 scan + band rubric)
  edit_permission: docs-write (this prompt artifact only; the reviewer is read-only)
  target_scope: docs/prompts/reviews/ (courier prompt); review target = the two Beauty Pie participant packets @ aec13c3
  dirty_state_checked: yes (branch ecr-sp3-timing-deriver-slice1, HEAD aec13c3; both packet blobs tracked + unchanged since the AR-01 close at e84ef47; this prompt file is new/untracked)
  blocked_if_missing: none (packets inlined below; prompt is self-contained for a repo-blind reviewer)
  doctrine_change: none (courier prompt for an existing pilot; no product/architecture/workflow/validation/review/output/lifecycle doctrine change)
```

---

## Commission

You are commissioned to perform **one read-only, independent leak re-scan** of the Beauty Pie #3 paired participant packets, after a home-model patch that closed a prior blocking finding (R6-AR-01). Your verdict gates whether these packets may be exposed to blind contestants.

- **Author of the reviewed artifact:** Claude (Anthropic). The packets and the prior R6 scan were authored/run inside the Claude home lane.
- **De-correlation who-constraint:** this is a **cross-vendor discovery** pass — you must be a **different vendor / model lineage than Anthropic/Claude** (vendor = the upstream model developer, not the host or wrapper). This is a commission who-constraint recorded for de-correlation; it is **not** a runtime-model recommendation. If you are an Anthropic/Claude-lineage model, **stop and return `BLOCKED_DE_CORRELATION`** — a same-vendor pass cannot claim the discovery / no-new-seam bar this re-scan exists to establish.
- **Why a re-scan (not the original):** the prior cross-vendor scan (`reviewed_by: codex-gpt-5`) returned `use_for_blind_contestant_exposure: no` on one blocking finding, R6-AR-01. The home model then patched both packets. A home-model self-check is not sufficient to re-establish the cross-vendor leak-free standard; an independent re-scan is required before blind exposure.

## Review target

The two paired participant packets for case `beautypie_repricing_2023_v0`:

- `orca-harness/cases/product_learning/beautypie_repricing_2023_v0/participant_packet_baseline.md` — blob `912cc2843fa643cbffcdd0e77b258354c05ea0c6` @ commit `aec13c3`
- `orca-harness/cases/product_learning/beautypie_repricing_2023_v0/participant_packet_augmented.md` — blob `2b679c59dc9dcd0443718a382e905a6132f3ee92` @ commit `aec13c3`

**If you have repo access:** read both files at the named blobs/commit and run the byte-identity check yourself (below). **If you do NOT have repo access:** review the **verbatim inlined copies in the Appendix** of this prompt — they are the exact files at the pinned blobs.

**Do NOT seek, request, infer, or reconstruct the sealed outcome.** The actual post-cutoff outcome lives ONLY in a sealed facilitator-only record that is deliberately out of scope; you must not ask for it and must not try to derive it. Reviewing leakage does not require knowing the outcome — it requires checking that the contestant-visible surfaces do not reveal or gesture at one.

## Review purpose

Determine whether the two packets are **leak-free and safe for blind-contestant exposure**, and specifically whether the prior blocking finding **R6-AR-01 is now closed**.

### What R6-AR-01 was, and the exact closure criterion

The prior scan found that contestant-visible text **enumerated later announcement / reaction / outcome as excluded categories** — e.g. wording like "excludes any later announcement, reaction, or outcome," plus E4/E5/`source_manifest` wording describing outcomes as excluded. Under the R6 lens, **naming forbidden/spoiler categories on a contestant-visible surface is itself a leak**: it tells the contestant which class of post-decision information was intentionally withheld, which can bias judgment even without revealing the outcome's direction. The information boundary must be **whitelist-only** ("decide using only the information in this brief"), never a blacklist of excluded categories.

`R6-AR-01.minimum_closure_condition` (verbatim from the prior scan): *contestant-visible packet text names only the allowed evidence boundary and cutoff rule, without enumerating excluded later announcement/reaction/outcome categories or explaining what kinds of post-cutoff material were withheld.*

### Fitness reference (this is an intent-bearing target — attack it, don't rubber-stamp it)

- **Goal:** the paired packets are leak-free and exposable to blind contestants, with the org-motion block as the **only** delta between the two arms.
- **Observable success signal:** `use_for_blind_contestant_exposure: yes`, with (a) byte-identity = exactly one content hunk (the "Organizational Motion Signal" section, augmented only), and (b) no enumerated forbidden-category lists and no sealed-outcome-derivable content on any contestant-visible surface.
- **Pointer (controlling):** the R6 leak-scan doctrine and the R5 whitelist / decision-framing decision (`docs/decisions/r5_whitelist_decision_framing_propagation_v0.md`); prior scan `docs/review-outputs/adversarial-artifact-reviews/beautypie_repricing_2023_r6_independent_leak_scan_v0.md`.
- This fitness reference is an **added axis you must also attack** (is the goal/signal itself right? is byte-identity the right bar? is "whitelist-only" sufficient?), never a pass-if-matches checkbox.

## Method

**If you are a repo- and skill-equipped Orca reviewer:** use `workflow-deep-thinking` first to frame failure modes and decision criteria, then `workflow-adversarial-artifact-review` after you declare `SOURCE_CONTEXT_READY`. Read the required authority sources (`AGENTS.md`, `.agents/workflow-overlay/README.md`, `review-lanes.md`, `prompt-orchestration.md`, `validation-gates.md`, `artifact-roles.md`, `communication-style.md`) and the two target packets. Do NOT `APPLY` any review judgment before `SOURCE_CONTEXT_READY`.

**If you are a cross-vendor / repo-blind reviewer (no Orca skills/overlay):** you cannot invoke those skills; run the **self-contained leak-scan method below** instead, and label your run **advisory-cross-vendor** (the home CA records provenance and adjudicates). The Orca portable review method (registry id `portable-adversarial-artifact-review-method`) is the fuller equivalent if it was shipped to you; the checklist below is the bounded form for this specific leak scan. Either way: **frame failure modes before listing findings; be maximally adversarial within this commission; do not widen the target.**

### Self-contained leak-scan checklist

Run all five checks against both packets:

1. **Blacklist scan (the R6-AR-01 check).** Does ANY contestant-visible surface — Decision Context, Evidence Units (incl. E4/E5), Known Uncertainties, `permitted_assumptions`, `information_boundary`, `source_manifest` entries — *enumerate* excluded categories (later announcement / reaction / outcome / walk-back / cancellations / later pricing / results / funding / headcount), or explain what kind of post-cutoff material was withheld? Any such enumeration = **AR-01 not closed**. The boundary must be whitelist-only.
2. **Sealed-outcome derivability.** Can a contestant infer the actual outcome (direction, magnitude, reaction) from anything visible — including the org-motion block, framing, or word choice? Flag anything that gestures at a known result.
3. **Byte-identity / single-delta.** The two packets must be byte-identical **except** for exactly one inserted section, "Organizational Motion Signal," present only in `participant_packet_augmented.md`. Repo-aware: run `git --no-pager diff --no-index <baseline> <augmented>` (or `git diff` between the two blobs) and confirm exactly one hunk. Repo-blind: diff the two inlined Appendix copies yourself. Any second delta = blocking finding.
4. **Org-motion block is pre-cutoff, NOT a spoiler.** The "Organizational Motion Signal" section reports public Greenhouse job postings at snapshots **on or before the 2023-01-31 archive snapshot / 2023-02-28 cutoff**, framed as gross hiring *intent*, not net headcount. Confirm it contains no post-cutoff content and makes no outcome claim. (It is legitimately present in the augmented arm; do not flag it merely for existing.)
5. **Over-strip check.** Confirm the de-leak did not strip evidence a contestant needs to decide among watch / hold / soften / phase-or-grandfather / commit (the decision question, role/authority frame, pricing structure, the £5→£10 doubling risk, cost-of-living context, retention-risk base rate, comparable-subscription proxy, and the stated uncertainty about Beauty Pie member tolerance). Over-stripping is a finding too.

## Output mode and return contract

Output mode: **`review-report`** (read-only; no patching, ever).

- **If you have repo write access:** write the full report to `docs/review-outputs/adversarial-artifact-reviews/beautypie_repricing_2023_r6_independent_leak_rescan_v0.md`, then return the compact `review_summary` YAML in chat.
- **If you are repo-blind:** **return the full report body paste-ready** (report-shaped: summary YAML + findings + closure checks), tagged for the home CA to place at that same path. Do not claim a `report_path` you did not write; use `review_location: chat_only_current_thread` in the YAML and name the intended path in `next_action`.

Lead with this YAML (fill it; `recommendation` ∈ accept | accept_with_friction | patch_before_acceptance | reject | blocked):

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/beautypie_repricing_2023_r6_independent_leak_rescan_v0.md   # or review_location: chat_only_current_thread if repo-blind
  recommendation:
  reviewed_by:        # your model+version, e.g. gpt-5.5 — operator/CA records this; never fabricate
  authored_by: claude
  de_correlation_bar: cross_vendor_discovery
  summary:
  findings_count:
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []   # list R6-AR-01 here only if you independently confirm it closed
  next_action:
```

Then state the verdict explicitly on its own line: **`use_for_blind_contestant_exposure: yes | no`**. Then give findings (severity: critical | major | minor; each with location, issue, evidence, impact, `minimum_closure_condition`, `next_authorized_action`, advisory remediation direction), then the five closure checks with pass/fail, then residual risks.

Severity labels are finding-priority only. Do **not** emit `patch_queue_entry` (this is read-only). Do not propose or apply edits.

## Hard constraints / non-claims

- Read-only. You flag; you do not patch. Patching is a separate home-lane action.
- Do not seek, request, or reconstruct the sealed outcome; do not ask for repo write access beyond the report path; do not access the web or recall outside knowledge about Beauty Pie's actual 2023 outcome.
- Your findings and verdict are **decision input only** — not approval, validation, fixture admission, source-capture, freeze, or product-proof readiness. The packets remain product-learning tier, N=1.
- If you cannot satisfy the cross-vendor who-constraint or cannot read the targets, return the nearest blocker (`BLOCKED_DE_CORRELATION` or a blocked `review_summary`) rather than reviewing a substitute or softening the bar.

---

## Appendix — Verbatim packet copies (for a repo-blind reviewer)

> These are the exact files at the pinned blobs (`baseline` 912cc28…, `augmented` 2b679c5…). A repo-aware reviewer should read the live blobs and treat these as a convenience copy only.

### A1 — `participant_packet_baseline.md` (blob 912cc2843fa643cbffcdd0e77b258354c05ea0c6)

````markdown
---
case_id: beautypie_repricing_2023_v0
decision_question: At the cutoff, how aggressively should Beauty Pie restructure its membership pricing — specifically whether to eliminate the £5/mo entry tier (moving those members to £10/mo, a doubling for them) and scrap the monthly spending limits — watch, hold, soften, phase/grandfather, or commit to the full elimination-and-doubling?
decision_date_or_cutoff: 2023-02-28
role_frame: Founder/CEO and commercial leadership of Beauty Pie, a UK factory-direct membership beauty brand, deciding how aggressively to restructure membership pricing on pre-cutoff public evidence only.
authority_constraints: Full founder-led pricing and membership-structure authority; the binding constraint is reversibility and member trust, not authority.
capability_constraints: Can ship any membership/pricing structure immediately; decides on pre-cutoff evidence, before any market response to the decision is observable.
permitted_assumptions:
  - Treat the packet as pre-cutoff only (on or before 2023-02-28).
  - Distinguish a pre-existing base rate from a reaction to this specific move.
  - Treat the prices, tiers, and monthly spending limits in the evidence as real.
  - Judge only on this packet; produce a single blind judgement from it alone.
information_boundary: Decide using only the evidence in this packet. Do not use, recall, or look up any outside or later knowledge about this company or this decision; base the judgement solely on the packet.
source_manifest:
  - source_id: E1
    source: 'Beauty Pie membership model — factory-direct; members pay a membership fee to buy products at cost (public brand/product description, pre-cutoff)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E2
    source: 'Beauty Pie membership structure at cutoff — £5/mo and £10/mo monthly tiers plus a £59/yr "Beauty Pie Plus" annual (2021 relaunch), each with monthly spending limits (public pricing, pre-cutoff)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E3
    source: 'UK cost-of-living / elevated-inflation context, early 2023 (neutral macro context bearing on discretionary spend)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E4
    source: 'General base rate — eliminating an entry tier / raising the floor price is a recognized retention-risk repricing lever (general base rate)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E5
    source: 'Generic comparable consumer-subscription repricings exist across the market (general base rate)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
---

# Participant Packet

## Decision Context

Beauty Pie is weighing a membership repricing. The live question, before any decision is announced, is **how aggressively to restructure its membership pricing** — specifically whether to **eliminate the £5/mo entry tier** (moving those members to £10/mo, a doubling for them) and **scrap the monthly spending limits**. The £5/mo tier is the lowest-commitment way into the membership, and the spending limits are part of the current structure. The packet is intentionally narrow: it presents only what was knowable on or before the cutoff (28 February 2023); decide using only the information in this brief. The options span watch / hold / soften / phase-or-grandfather / commit-to-the-full-elimination-and-doubling.

## Evidence Units

- `E1`: Beauty Pie's **membership business model** — factory-direct; members pay a membership fee to buy beauty products at cost. The membership fee is the revenue gate, and the cheapest tier is the low-commitment on-ramp into the model.
- `E2`: Beauty Pie's **membership structure at the cutoff** — two monthly tiers, £5/mo and £10/mo, plus a £59/yr annual "Beauty Pie Plus" (introduced in a 2021 relaunch), each carrying monthly spending limits. The £5/mo tier is the lowest-commitment entry point.
- `E3`: **UK cost-of-living pressure in early 2023** — elevated inflation and squeezed discretionary household spend — a neutral macro context bearing on price sensitivity for discretionary beauty.
- `E4`: Eliminating an entry tier or raising the floor price is a **recognized retention-risk repricing lever** in subscription/membership businesses — a documented general base rate.
- `E5`: **Comparable consumer-subscription repricings** exist across the market — a generic base rate.

## Known Uncertainties

- The evidence shows entry-tier removal and floor-price increases are a normal repricing lever **and** that raising the floor on the most price-sensitive members during a cost-of-living squeeze carries retention risk; it does not settle how far is too far.
- There is no pre-cutoff measurement of *Beauty Pie's own* members' tolerance for the doubling, or for scrapping the monthly spending limits specifically.
- Whether the second-order base rate (E3, E4, E5) is enough to *decide* the calibration in advance — versus only being legible in hindsight — is the crux of this decision.
````

### A2 — `participant_packet_augmented.md` (blob 2b679c59dc9dcd0443718a382e905a6132f3ee92)

> Identical to A1 except for the inserted "Organizational Motion Signal" section (the only intended delta).

````markdown
---
case_id: beautypie_repricing_2023_v0
decision_question: At the cutoff, how aggressively should Beauty Pie restructure its membership pricing — specifically whether to eliminate the £5/mo entry tier (moving those members to £10/mo, a doubling for them) and scrap the monthly spending limits — watch, hold, soften, phase/grandfather, or commit to the full elimination-and-doubling?
decision_date_or_cutoff: 2023-02-28
role_frame: Founder/CEO and commercial leadership of Beauty Pie, a UK factory-direct membership beauty brand, deciding how aggressively to restructure membership pricing on pre-cutoff public evidence only.
authority_constraints: Full founder-led pricing and membership-structure authority; the binding constraint is reversibility and member trust, not authority.
capability_constraints: Can ship any membership/pricing structure immediately; decides on pre-cutoff evidence, before any market response to the decision is observable.
permitted_assumptions:
  - Treat the packet as pre-cutoff only (on or before 2023-02-28).
  - Distinguish a pre-existing base rate from a reaction to this specific move.
  - Treat the prices, tiers, and monthly spending limits in the evidence as real.
  - Judge only on this packet; produce a single blind judgement from it alone.
information_boundary: Decide using only the evidence in this packet. Do not use, recall, or look up any outside or later knowledge about this company or this decision; base the judgement solely on the packet.
source_manifest:
  - source_id: E1
    source: 'Beauty Pie membership model — factory-direct; members pay a membership fee to buy products at cost (public brand/product description, pre-cutoff)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E2
    source: 'Beauty Pie membership structure at cutoff — £5/mo and £10/mo monthly tiers plus a £59/yr "Beauty Pie Plus" annual (2021 relaunch), each with monthly spending limits (public pricing, pre-cutoff)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E3
    source: 'UK cost-of-living / elevated-inflation context, early 2023 (neutral macro context bearing on discretionary spend)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E4
    source: 'General base rate — eliminating an entry tier / raising the floor price is a recognized retention-risk repricing lever (general base rate)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E5
    source: 'Generic comparable consumer-subscription repricings exist across the market (general base rate)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
---

# Participant Packet

## Decision Context

Beauty Pie is weighing a membership repricing. The live question, before any decision is announced, is **how aggressively to restructure its membership pricing** — specifically whether to **eliminate the £5/mo entry tier** (moving those members to £10/mo, a doubling for them) and **scrap the monthly spending limits**. The £5/mo tier is the lowest-commitment way into the membership, and the spending limits are part of the current structure. The packet is intentionally narrow: it presents only what was knowable on or before the cutoff (28 February 2023); decide using only the information in this brief. The options span watch / hold / soften / phase-or-grandfather / commit-to-the-full-elimination-and-doubling.

## Evidence Units

- `E1`: Beauty Pie's **membership business model** — factory-direct; members pay a membership fee to buy beauty products at cost. The membership fee is the revenue gate, and the cheapest tier is the low-commitment on-ramp into the model.
- `E2`: Beauty Pie's **membership structure at the cutoff** — two monthly tiers, £5/mo and £10/mo, plus a £59/yr annual "Beauty Pie Plus" (introduced in a 2021 relaunch), each carrying monthly spending limits. The £5/mo tier is the lowest-commitment entry point.
- `E3`: **UK cost-of-living pressure in early 2023** — elevated inflation and squeezed discretionary household spend — a neutral macro context bearing on price sensitivity for discretionary beauty.
- `E4`: Eliminating an entry tier or raising the floor price is a **recognized retention-risk repricing lever** in subscription/membership businesses — a documented general base rate.
- `E5`: **Comparable consumer-subscription repricings** exist across the market — a generic base rate.

## Organizational Motion Signal

A supplementary, lower-grade signal about the company's public hiring activity in the period leading up to the cutoff. Source: Beauty Pie's public Greenhouse jobs board (`boards.eu.greenhouse.io/beautypie`), read from dated archive snapshots on or before the cutoff.

- Across archived snapshots spanning ~January 2022 to January 2023, the number of roles posted on the board grew over the window.
- At the cutoff-proximate snapshot (31 January 2023), 8 roles were open:
  - Product Lead (Acquisition)
  - Product Lead (Core Shopping Experience)
  - Product Lead (Retention)
  - Demand Planning Analyst
  - Inventory Planning & Analysis Manager
  - Senior Engineer
  - Senior UX Designer
  - Mid-Weight Digital Designer (maternity-cover fixed-term contract)

Signal class: **hiring INTENT (open roles), base-rate-discounted — not confirmed net headcount adds.** Open postings are roles the company was seeking to fill at the snapshot date; they are gross hiring intent, not realized hires, and are not evidence of net headcount change.

## Known Uncertainties

- The evidence shows entry-tier removal and floor-price increases are a normal repricing lever **and** that raising the floor on the most price-sensitive members during a cost-of-living squeeze carries retention risk; it does not settle how far is too far.
- There is no pre-cutoff measurement of *Beauty Pie's own* members' tolerance for the doubling, or for scrapping the monthly spending limits specifically.
- Whether the second-order base rate (E3, E4, E5) is enough to *decide* the calibration in advance — versus only being legible in hindsight — is the crux of this decision.
````
