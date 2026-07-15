# Creator Signal Multi-Creator Library Surface v0

```yaml
retrieval_header_version: 1
artifact_role: product_signal_surface_contract
scope: >
  Product-facing display contract for a multi-creator Creator Signal Library:
  how an operator or buyer may scan multiple creator_profile_current rows side
  by side, what sorting/filtering is allowed, and what claim boundaries must
  stay visible so the surface cannot read as a leaderboard, lead list, or
  buyer proof.
use_when:
  - Designing or reviewing the multi-creator Creator Signal library/catalog surface.
  - Deciding whether a multi-row scan/sort view over creator_profile_current is safe to build.
  - Checking whether a proposed multi-creator display or sort behavior is allowed or must be withheld.
  - Scoping the Step 3 static projection over creator_profile_current.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md
stale_if:
  - creator_profile_current_record_contract_v0.md changes the Metric Comparison
    Rules, posture/value coupling, or declared-deferred recipe semantics.
  - creator_intelligence_profile_surface_v0.md changes single-profile claim,
    limitation, or non-claim display policy in a way this surface must inherit.
  - creator_profile_current_view_v0.json platform mix, sample-support
    distribution, or declared-deferred metric postures materially change.
  - A later accepted contract authorizes cross-platform rollups or promotes
    posting_cadence/recent_velocity out of not_attempted.
```

## Status

`PR_REVIEW_PRODUCT_SURFACE_CONTRACT_V0`.

This is the proposed first Creator Signal multi-creator display contract for PR
#638. It becomes accepted only after owner/maintainer acceptance and merge. It is
product-document only. It does not create a dashboard, storage engine, live capture
flow, API, SQLite table, data-lake job, real creator rows beyond what already
exists in `creator_profile_current`, outreach mechanism, or runtime
implementation.

## Purpose

`creator_intelligence_profile_surface_v0.md` covers one creator profile at a
time. It explicitly defers multi-creator ranking, grid, shortlist, lead-list,
or outreach surfaces to "a separate accepted Creator Signal or successor
display contract." This is that contract.

It answers, for a surface that shows many `creator_profile_current` rows at
once:

```text
What may an operator or buyer scan side by side?
How may rows be sorted or filtered, and by what?
What must stay visible on every row so a sorted list cannot look like a
  merit ranking, a lead list, or buyer proof?
What is out of scope until a separate contract authorizes it?
```

This is a product interpretation over `creator_profile_current`, not a new
source of truth. It does not relax or replace
`creator_profile_current_record_contract_v0.md`'s Metric Comparison Rules or
`creator_intelligence_profile_surface_v0.md`'s single-profile claim rules; it
extends them to the multi-row case.

## Authority Boundary

This contract is not validation, readiness, buyer proof, product proof, SQLite
adoption, data-lake job authorization, dashboard implementation, live capture
authorization, identity-linkage authority, or outreach/lead-list authorization.
It does not authorize the Step 3 static projection named below by itself; Step
3 requires this contract to land first, then proceeds under its own
authorization.

## Source Basis

The row surface is derived from:

- `creator_profile_current_view_v0.json` (the committed read model).
- `creator_profile_current_record_contract_v0.md` (per-profile record contract,
  Sections 1-3: visible surface, consumer interpretation contract, and
  declared-deferred global metric recipes for `posting_cadence` and
  `recent_velocity`).
- `creator_intelligence_profile_surface_v0.md` (the accepted single-profile
  Creator Signal surface, whose required sections, claim rules, and
  first-screen guidance this contract inherits and extends for the
  multi-creator case).
- `creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md`
  (the adversarial review that named the four structural guards this contract
  pins: platform-scoped default sort, declared-deferred field visibility at
  scan-row granularity, a visible sample-support cue for ranked/sorted views,
  and a reachable `non_claims` mechanism as a precondition for any ranked
  default).

Recheck those sources before making strict claims if the view, the record
contract, or the Creator Signal single-profile surface changes.

## Current Data Posture

Reconfirmed against `creator_profile_current_view_v0.json` at
`origin/main@b09b7b907a851116cea2c41bf12cc6f0ac85ce2b` in this worktree:

```text
profiles_total=33
platform_account_profiles=33
creator_record_profiles=0
cross_platform_rollup_profiles=0
profiles_with_audience_triangulation=0
platforms=youtube:30,instagram:3
posting_cadence=not_attempted:33
recent_velocity=not_attempted:33
sample_adequacy=stronger_admitted_pool_n_8_plus:30,limited_n_4_to_7:1,thin_n_1_to_3:2
identity_state=single_platform_observed:33
link_state_or_none=null:33
review_state_or_none=null:33
```

No `creator_record` (cross-platform-linked) profile exists. Every profile is
`platform_account`-scoped. Two metric families
(`posting_cadence`, `recent_velocity`) are declared-deferred (`not_attempted`)
for every row. Three rows (2 thin-`n`, 1 limited-`n`) carry a
sample-adequacy posture weaker than the other 30 rows.

If a live baseline differs from these counts, re-derive this section's claims
from the live view before relying on it; the structural rules below do not
depend on the exact counts, only on the postures (`not_attempted`,
non-uniform `sample_adequacy`, `platform_account`-only subjects) they encode.

## Ownership Split

- **Capture/registry owns:** source rows, the current read model
  (`creator_profile_current`), posture/value coupling, sample-support
  computation, declared-deferred metric recipes, and source pointers. See
  `creator_profile_current_record_contract_v0.md`.
- **Creator Signal owns:** product display, library navigation, sort/filter
  behavior, claim-boundary language, and customer/operator scan behavior
  across multiple creator rows. This contract and
  `creator_intelligence_profile_surface_v0.md` together are that authority;
  this contract governs the multi-row case, the single-profile contract
  governs one opened profile.

## Default View: Creator Signal Library

The default multi-creator surface is named the **Creator Signal Library**. Do
not name it, brand it, or otherwise present it as a leaderboard, ranking,
lead list, or priority queue (see Forbidden Language below).

Structural rules for the default view:

1. **Platform-scoped by default.** The library organizes rows by platform
   through tabs, sections, or an equivalent mandatory platform filter. There
   is no single default list that spans platforms. A creator row's platform
   determines which section/tab it appears in; a user may not default-load a
   combined YouTube+Instagram sorted list. A "mandatory platform filter," if
   used instead of tabs/sections, must default to, and offer only,
   single-platform states — it must not default to or expose an
   all-platforms/combined option, since that would reproduce the exact
   combined list this rule forbids under a filter label.
2. **No mixed-platform global rank.** This contract does not define, and
   forbids defining, one global rank, score, or ordering that spans platforms.
   `platform_scope: cross_platform` metrics do not exist in the current data
   (`cross_platform_rollup_profiles: 0`) and this contract creates no path to
   synthesize one by combining per-platform values in the display layer.
3. **Unranked entry state is acceptable.** The library may open with an
   unranked or alphabetical/identity-ordered listing per platform section
   before a user selects a sort metric. A user-selected sort is not required
   to be pre-applied.

This closes the adversarial review's MC-01 finding as a structural rule, not
prose: platform separation is a required display mechanism (tab, section, or
mandatory filter), not an inference left to an implementer reading "compatible
platform/window/scope."

## Row Model

Every row in the Creator Signal Library must expose, or make immediately
reachable without opening the full profile:

- **Identity:** platform account handle and platform (inherited from
  `creator_profile_current` identity fields).
- **Current metric rollups:** the metric family the library is currently
  sorted or scanned by, plus any other metric families the row surfaces,
  each with its posture (`observed`, `unavailable_with_reason`,
  `out_of_window`, `not_attempted`, `not_applicable`).
- **Selected sort metric and posture:** which metric the library is currently
  sorted by (if any) and that metric's posture for this row.
- **Sample-support cue:** visible on every row (see Display Tiers below; this
  is not merely reachable, and it is required whenever the library is in a
  sorted state or presents a filtered/highlighted/selectively-ordered subset,
  not only a literal ranked state).
- **Freshness cue:** at minimum the metric computation timestamp or a
  stale/current/partial/blocked state.
- **Declared-deferred metric state:** `posting_cadence` and `recent_velocity`
  must render a visible "not yet available" state at scan-row granularity for
  every row, as its own always-visible item independent of the currently
  selected sort/scan metric (see Display Tiers, which names this explicitly
  rather than leaving it to this general statement alone; this closes MC-02).
- **Missingness/limitations cue:** a visible cue when a shown or sortable
  metric is non-observed, or when the row's rollup carries a limitation
  material to interpretation.
- **Claim-boundaries/non-claims affordance:** a reachable "what this table
  doesn't prove" affordance, visible from the library's first screen, not
  buried only inside each opened profile (see Non-Claims and Display Tiers;
  this closes MC-04 for the library level).
- **Source drill-back affordance:** a path from the row to the profile's
  `source_drill_back` pointers, consistent with
  `creator_profile_current_record_contract_v0.md`.

## Sorting Semantics

- Call this behavior **sorting or filtering inside a library**, never
  **ranking creators as winners**. Product and UI copy must not describe a
  sorted position as a rank, score, or competitive standing.
- A user may sort only by an **observed** metric. A metric that is
  `unavailable_with_reason`, `out_of_window`, `not_attempted`, or
  `not_applicable` is not a valid sort key.
- **`posting_cadence` and `recent_velocity` may not be offered as sort
  options while their posture is `not_attempted`.** They may render as a
  visible declared-deferred column/state (per Row Model), but selecting them
  as a sort basis is disabled until a later accepted contract records their
  first observed population, per
  `creator_profile_current_record_contract_v0.md` Section 3's First
  Population Rule.
- Sorting stays **platform-scoped by default** (see Default View). A future
  accepted contract may authorize a `cross_platform`-scoped sort only if it
  points to an actual `platform_scope: cross_platform` rollup; this contract
  does not create that rollup or that sort option.
- **Null, `unavailable_with_reason`, `out_of_window`, `not_attempted`, and
  `not_applicable` values must never be treated as zero** for sort ordering,
  display, or any derived summary. A non-observed row for the selected sort
  metric must be shown with its posture (e.g., pinned to a clearly-labeled
  "not available for this metric" group), never silently placed at the
  bottom as if it scored zero.
- **No composite scores.** This contract does not define, and forbids
  defining, any weighted or combined score across metrics, platforms, or
  audience fields. A later accepted contract may introduce one; this
  contract creates no such mechanism.

## Display Tiers

**Always-visible (first screen, per row):**

- platform;
- identity/handle;
- the metric family currently selected for sort or scan, with its posture;
- `posting_cadence` and `recent_velocity` declared-deferred state, rendered
  as a visibly-labeled "not yet available" item independent of whether
  either is the currently-selected sort/scan metric — they can never be
  that metric while `not_attempted` (Sorting Semantics forbids selecting
  them as a sort key in that state), so this item is required on its own,
  not inherited from the "currently selected metric" bullet above (this
  closes MC-02 at the layer that actually governs a collapsed row, not only
  in Row Model's general "every row" statement);
- sample-support cue, required whenever the row shows any metric rollup. When
  the library is in a sorted state **or** presents a filtered, highlighted, or
  otherwise selectively ordered subset of a platform's rows relative to that
  platform's full row set —
  not merely reachable, and not limited to a literal "sorted" state, since
  a filtered-but-unranked view carries the same false-merit-impression risk
  a sorted view does (this closes MC-03 including the unranked/filtered
  entry state Default View rule 3 permits);
- freshness cue;
- a visible missingness and limitations cue when any shown metric is non-observed
  or the row's rollup carries an interpretation-material limitation, including
  source-pool-limited, admitted-pool-only, or non-representative sample posture;
- a reachable claim-boundary cue (may be a compact affordance, e.g., an
  always-visible "what this doesn't prove" link, rather than the full text),
  placed adjacent to the sort control or shown at first sort-selection when
  the library is in a sorted state — location on the first screen alone is
  not sufficient in a sorted view specifically, since that is the context
  where an implied merit ranking is most likely to form unnoticed.

**Details drawer or equivalent (per row, on demand):**

- full `limitations`;
- full `non_claims`;
- `source_drill_back`;
- `calculation_recipe_version` and lineage;
- any additional metric families not shown on the first screen.

Progressive disclosure is permitted only under the same conditions
`creator_profile_current_record_contract_v0.md`'s Progressive Disclosure
Boundary sets for a single profile: the primary surface keeps visible trust
posture for every metric or summary it shows; the details panel exposes the
full limitations/non-claims/lineage; non-observed values stay null-with-reason
and are never displayed as zero, ranked, or averaged; and claim-boundary cues
are available from the start even when the full text is collapsed. This
contract requires that boundary to hold at scan-row granularity across every
row of the library, not only inside one opened profile.

## Non-Claims

The Creator Signal Library is not, and must not imply:

- a leaderboard, winner/loser ranking, or competitive standing;
- a lead list, outreach list, recommended-creators list, or priority queue;
- outreach or contact authorization;
- buyer proof or product proof;
- a performance guarantee or prediction;
- cross-platform identity proof or a linked `creator_record` where none
  exists;
- universal or channel-wide creator influence;
- dashboard readiness, API readiness, SQLite adoption, data-lake
  physicalization, or capture-job authorization.

This non-claims panel must be reachable from the library's first screen (see
Display Tiers), not only from within each opened profile. A library that
presents many creators' metrics side by side without a reachable non-claims
affordance at the library level inherits the single-profile
`creator_intelligence_profile_surface_v0.md` gap at a larger blast radius; this
contract closes that gap by requiring the affordance at the library level.

## Forbidden Language

Do not use the literal customer-facing word **leaderboard** for this surface,
except in a forbidden-language/non-claim note (as in this section and the Hard
Constraints in the commissioning prompt for this contract). In customer-facing
copy, prefer **library** or **catalog**. **Ranked table** or **ranked scan** may
appear only as internal review/history/source terminology or as a non-customer
implementation note; they are not the customer-facing surface name.

## Static Projection Handoff Boundary (Step 3)

A static projection over `creator_profile_current` may be built only after
this contract lands. When built, it:

- **may** exercise current-row display, platform separation (tabs/sections),
  observed-metric sorting, sample-support cues, declared-deferred metric
  states (`posting_cadence`/`recent_velocity` shown as not-yet-available),
  and non-claims affordances, using the 33 rows currently committed;
- **may not** invent populated `audience_triangulation`, `creator_record`,
  cross-platform rollup, `posting_cadence`, or `recent_velocity` states, or
  any outreach/lead-list state, since none of those exist in the current data
  (`profiles_with_audience_triangulation: 0`,
  `creator_record_profiles: 0`, `cross_platform_rollup_profiles: 0`,
  `posting_cadence`/`recent_velocity` both `not_attempted: 33`);
- **may not** invent or imply resolution for a `candidate_public_account_link`
  or `rejected_public_account_link` `link_state_or_none`/`review_state_or_none`
  state, since the current data carries `null` for both on every row; if a
  future data refresh populates either field within this contract's existing
  schema, re-derive this boundary against the live view before Step 3 treats
  that row as anything more than single-platform-observed identity/
  disambiguation context, per
  `creator_profile_current_record_contract_v0.md`'s Identity And
  Cross-Platform Promise;
- must name explicitly, in its own closeout, that the ideal-audience section
  is exercised only in its always-null state given current data, rather than
  implying full row-treatment coverage across all possible states (per the
  adversarial review's MC-05).

This contract does not itself authorize Step 3; it only defines what Step 3
may and may not exercise once separately authorized.

## Accepted Residuals

- Global stats (`posting_cadence`, `recent_velocity`) remain declared-deferred
  at library scale, same as at single-profile scale.
- The library covers `platform_account`-scoped rows only; no `creator_record`
  or cross-platform view exists yet.
- Current rollups remain source-pool-limited, admitted-pool statistics, not
  representative channel-wide creator averages, at every row.
- This contract does not create a lake producer, dashboard, API, SQLite
  table, capture cadence policy, or live capture run.
- Whether an implementer will in practice honor the platform-tab/mandatory-filter
  structural rule (Default View, rule 1) once implementation is authorized is
  not tested by this docs-only contract; it is checkable at implementation
  review time against this contract's explicit structural language.

## Non-Claims (Contract-Level)

- not validation
- not readiness
- not buyer proof
- not product proof
- not implementation authorization
- not dashboard, API, SQLite, or data-lake authorization
- not live capture authorization
- not identity-linkage authority
- not outreach or lead-list authorization
