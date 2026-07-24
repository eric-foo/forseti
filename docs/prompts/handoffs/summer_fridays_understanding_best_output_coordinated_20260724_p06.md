# Summer Fridays Understanding — Best-Output Coordinated Acquire & Seal p06

```yaml
retrieval_header_version: 1
artifact_role: Execution-ready cold handoff
scope: >
  Runs one Summer Fridays Understanding Turn A best-output treatment using
  exactly CO0-CO3. It does not run a standalone sibling, Turn B, Deliver, or
  the later blind control-versus-treatment adjudication.
use_when:
  - The owner authorizes the p06 best-output treatment.
  - The named worktree remains based on the required runtime revision.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/README.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
stale_if:
  - The Intelligence Cycle acquisition contract or CO0-CO3 route changes.
  - Retail portfolio onboarding v2 or a named capture interface is retired.
```

## Prompt Preflight

```yaml
output_mode: file-write
edit_permission: docs-write
input_prompt_source: docs/prompts/handoffs/summer_fridays_understanding_best_output_coordinated_20260724_p06.md
target_scope: named p06 prompt, commission board, specialist terminals, acquisition record, seal, and p06 data root
required_runtime_revision: 788d583db84c87ebf7a781c564e7f24d1fbdf3e6
revision_mode: required_revision_is_ancestor_and_runtime_base
branch: codex/sf-understanding-p06-best-output
workspace: C:\tmp\forseti-sf-understanding-dogfood-20260724-p06-worktree
repository_state_allowance: only the named p06 prompt and p06 output artifacts may become dirty
data_root: C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data
raw_input_manifest: C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\release\raw_input_manifest.json
raw_input_manifest_sha256: 50c03bf390253d7ee31bf608ed799e471e93901e8057452acc2c472200d8f9b0
commission_board: docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/commission_board.md
acquisition_record: docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/turn_a_acquisition_record.md
acquisition_seal: docs/workflows/summer_fridays_understanding_dogfood_20260724_p06/coordinated/acquisition_seal.md
later_company_output_validation: future_only
turn_b: forbidden
doctrine_change: none
```

The shared preflight constants remain owned by
`docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`.

## Goal

Produce a decision-neutral, evidence-accountable Summer Fridays substrate
through Turn A Acquire & Seal:

> What does current public evidence show about Summer Fridays as a company and
> brand system — its proposition, normalized owned and retailer-expressed
> portfolio architecture, markets and channels, strategic motion, material
> events, customer/community response, concentrations, contradictions, strong
> and weak links, and tensions warranting later Problem Framing?

```yaml
cycle_id: sf_understanding_20260724_p06_co
commission_id: sf_understanding_csb_20260724_p06_co
subject: Summer Fridays
phase: understanding
turn: acquire_and_seal
optimization_target: decision_useful_completeness
control: p05, observational comparison only, hidden from CO0-CO3
```

Compactness, token use, elapsed time, source count, and a passing validator are
not acquisition success criteria. Every material job must be supported,
contradicted, bounded, or honestly gapped.

## Isolation And Raw Reuse

The mechanical dispatcher supplies only the hash-pinned raw inputs in
`raw_input_manifest`. CO0-CO3 may fresh-read those named raw packets and their
own p06 artifacts. They must not read prior Summer Fridays prompts, commission
boards, actor returns, acquisition records, seals, conclusions, hero/depth
selections, comparison reviews, or token totals.

Raw reuse is not current-reality proof. Fresh-capture the official retailer
surface and refresh the admitted retailer grids. Reuse a PDP packet only when
its stable retailer-native identity remains on the refreshed grid; recapture
new, changed, or missing exact listings.

## Commission-Stage Gate

Before source-heavy work, CO0 writes the company-profile commission-stage CSB
with `run_boundary: COMMISSION_SEALED_PRE_SCAN` and runs:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py docs\research\summer_fridays_understanding_dogfood_20260724_p06\coordinated\commission_board.md
```

Repair findings or stop. This is the only company-output validator in Turn A.
The acquisition seal is manually adjudicated after acquisition.

## Actor Topology And Dependencies

Exactly four analytic evidence actors exist:

- `CO0`: whole-run Chief Architect, durable integration, and seal owner.
- `CO1`: owned company/high-yield core, current official-retailer board, and
  complete owned product-identity denominator.
- `CO2`: one unified authorized-retailer portfolio corpus, stable listing
  reconciliation, PDP baselines, provider identity, overlap, and depth pointers.
- `CO3`: mandatory customer/community scout, category-balanced retailer
  reviews/Q&A, Reddit, customer language, pain points, objections, complaints,
  workarounds, response patterns, and syndication ceilings.

The pair-release dispatcher is mechanical and is not an analytic actor. CO0
dispatches CO1-CO3 together as same-root collaboration subagents. Specialists
create no agents/tasks and perform no Git lifecycle actions.

```yaml
co1_terminal: docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/specialists/co1_company_core_identity.md
co2_terminal: docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/specialists/co2_retail_portfolio.md
co3_terminal: docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/specialists/co3_customer_community_depth.md
```

- CO1 publishes the official-retailer board and complete identity ledger.
- CO2 plans concurrently but waits for the board before final retailer
  admission and waits for the identity ledger before final reconciliation.
- CO3 starts its community scout immediately and waits only for CO2's final
  depth pointers before retailer depth.
- Each specialist writes one terminal return. Returns are pointers, never
  evidence. CO0 fresh-reads every seal-bearing artifact and disposition.
- Actor-local corrections stay in the same actor task. Do not replace or
  restart unaffected actors.

## CO1 — Owned Core And Product Identity

Capture and fresh-read the current official authorized-retailers surface first.
Sephora is the retail primary when officially named, US-admissible, and
route-complete. REVOLVE is the intended secondary when officially named and
route-complete. Do not probe Target, Amazon, or Ulta to satisfy a fixed quota;
use an unnamed retailer only for a named contradiction job, never as
authorization proof.

Classify every one of the 139 released owned source parents exactly once:

- normalized-family `PRIMARY_PARENT` only for an evidenced canonical parent;
- `VARIANT_AS_PARENT` for separately serialized shade, flavor, or sellable-size
  variants; a family may have no primary when every source parent is a variant;
- `BUNDLE_SET` for kits, routines, trios, and limited-edition sets;
- `SAMPLE_GIFT` for samples, GWP, birthday gifts, and non-sellable deluxe units;
- `MERCHANDISE` for pouches, tools, planners, totes, and gift cards;
- `LEGACY_OTHER` only for explicitly discontinued, hidden, or unavailable
  historical objects outside the current family denominator.

An exact franchise tag or retailer/owned variant relation may support a
grouping. Name/category similarity alone is candidate generation, never
admission. Sellable minis join a family only with formula/identity evidence.
Every disposition carries artifact path, SHA-256, and locator. Targeted capture
may close ambiguous IDs; do not guess.

Success requires all 139 IDs exactly once, zero unresolved IDs,
`family_denominator_state: COMPLETE`, and non-null `normalized_family_count`.
Persist the final ledger and machine-readable commission fragment under
`<data_root>\co1`.

## CO2 — Authorized Retail Portfolio

Use Sephora and REVOLVE when CO1 confirms both. Refresh their grids using the
current supported direct/no-VPN route first. A route-authorized owner VPN may be
used once after an observed access failure; preserve both outcomes. VPN state
is transport, not evidence.

Rehash released packets, reconcile refreshed grid rows to owned parents, merge
CO1's identity fragment into `retail_portfolio_onboarding_v2`, and preserve:

- stable native product identity and retailer placement;
- duplicate placements, exclusives, missing families, bundles, ambiguity,
  unmatched rows, and typed route/source failures;
- one raw PDP baseline for every exact non-bundle listing;
- review provider/corpus family and syndication/overlap limits.

ZIP or delivery context binds only the visible local fulfillment context. It is
not authorization or nationwide availability evidence.

Publish four depth pointers for current families:

1. Lip Butter Balm;
2. Jet Lag Mask;
3. Sunlit Vanilla;
4. Summer Skin Nourishing Body Lotion.

If one is not current/listed, use the same-category current family with the
highest captured review volume; break ties by newest launch date.

## CO3 — Customer And Community Depth

Start a bounded brand/product community scout immediately. Consume an already
terminal Reddit raw corpus only when its packet hashes are supplied in p06;
otherwise run the scout here without creating another lane.

After CO2 publishes depth pointers:

- Sephora: up to 50 Most Recent plus 25 Most Helpful reviews per family and up
  to 25 Q&A rows.
- REVOLVE: up to 50 Most Recent reviews per family; do not add Most
  Relevant/Helpful as a second corpus.
- Prefer non-incentivized recent rows. Preserve incentivized and unknown rows
  separately rather than silently discarding them.
- Require retailer, provider family, corpus family, normalized product family,
  sort/window, native row ID, incentive posture, and durable source pointer.
- Deduplicate native review IDs; otherwise use provider plus normalized
  text/date/rating fingerprint. Syndicated duplicates remain visible placements
  but count as one independent evidence family.

Target 25 unique recent non-incentivized rows per category. Proven lower source
volume is a typed limitation, not fabricated completion. Preserve customer
language and cluster counts without turning engagement into demand proof.

## Integration, Seal, And Return

CO0 integrates only after fresh-reading the commission board, identity ledger,
retailer onboarding record, review/community artifacts, and terminal returns.
The record includes actor/job attribution, routes, provenance, normalized
denominator, retailer crosswalk, baseline coverage, depth/linkage, material
seams/failures, owner-unblock status, and observed effort.

The seal may pass only when the current acquisition gate passes. Otherwise
write `BLOCKED_ACQUISITION_INCOMPLETE`, retain useful evidence, and name the
smallest genuine unblock. Do not author Turn B.

CO0 returns exact revision/base, actor roster, CSB validator result, terminal
paths, acquisition record/seal, gate and `deliver_allowed`, material failures,
route/VPN disposition, contamination status, observed task/session token data
or `not_observable`, descriptive runner effort, and observed
`turn_b_started: false`.

The later opposing-family comparison prompt is authored only after the p06
record and seal exist, using actual p05/p06 paths and fresh hashes. CO0-CO3 do
not perform that comparison or any repository lifecycle action.
