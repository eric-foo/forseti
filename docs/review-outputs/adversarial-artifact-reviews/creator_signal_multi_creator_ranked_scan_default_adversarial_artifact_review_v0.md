# Creator Signal Multi-Creator Ranked Scan Default -- Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: adversarial_artifact_review_report
scope: >
  Adversarial artifact review of whether the proposed default multi-creator
  Creator Signal surface may safely be a contextual ranked scan table, and
  what display-contract guardrails must be settled before authoring or static
  projection.
use_when:
  - Deciding whether Batch 1 may proceed to author the multi-creator display
    contract with "contextual ranked scan table" as the stated default.
  - Checking what must be true before Batch 2 static projection over
    creator_profile_current.
authority_boundary: retrieval_only
generated_from_prompt: docs/prompts/reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_prompt_v0.md
```

## Commission

- **Review target:** the direction under review named in the commissioning
  prompt -- whether the default multi-creator Creator Signal surface may be a
  contextual ranked scan table (`creator_signal_multi_creator_contextual_ranked_scan_default`),
  plus its Batch 1/Batch 2 shape and the "leaderboard" terminology question.
- **Review purpose:** decide whether Batch 1 may safely specify the default
  multi-creator surface as a contextual ranked scan table, or whether
  leaderboard/ranking language should be blocked or deferred, per the
  commissioning prompt's `intended_decision`.
- **Worktree:** `codex/multi-creator-default-view-review` @ `612f2aa4`
  (one commit ahead of the expected floor `41f87dd7`, adding only the
  commissioning prompt itself). Confirmed clean via `git status --short
  --branch` before this write.
- **Fitness reference:** bound by the commissioning prompt's `intended_decision`
  plus the `docs/workflows/creator_registry_record_contract_handoff_v0.md`
  `long_term_goal` ("a live, self-sustaining creator-metric registry a
  downstream consumer can trust"). This review treats "does the default
  surface preserve that trust promise at multi-creator scale" as the
  alignment axis it must also attack, not a pass-if-matches bar.

## Provenance

```yaml
reviewed_by: claude-sonnet-5 (Claude Code, Anthropic)
authored_by: unrecorded
controller_family: Anthropic
de_correlation_bar: self_fallback
same_vendor_rationale: >
  Direct self-review commission (not a delegated-review-patch dispatch); no
  cross-vendor or same-vendor delegate was commissioned for this pass. The
  commissioning prompt does not request delegation.
```

## Source-Read Ledger

| Source | Disposition | Why read | Status |
| --- | --- | --- | --- |
| `AGENTS.md` (this worktree) | full | start preflight | clean |
| `.agents/workflow-overlay/README.md` | full | overlay entrypoint | clean |
| `.agents/workflow-overlay/source-of-truth.md` | full | required-read list, source hierarchy | clean |
| `.agents/workflow-overlay/source-loading.md` | full | required-read list, source-pack tiers | clean |
| `.agents/workflow-overlay/artifact-roles.md` | full | required-read list | clean |
| `.agents/workflow-overlay/review-lanes.md` | full | required-read list, review-lane doctrine, fitness-reference rule | clean |
| `.agents/workflow-overlay/prompt-orchestration.md` | full | required-read list, Source-Gated Method Contract | clean |
| `.agents/workflow-overlay/validation-gates.md` | full | required-read list | clean |
| `.agents/workflow-overlay/communication-style.md` | full | required-read list, courier YAML shape | clean |
| `.agents/workflow-overlay/template-registry.md` | full | required-read list | clean |
| Commissioning prompt (this review's target definition) | full | direction under review, assumption-gate snapshot, review questions | clean |
| `docs/workflows/creator_registry_record_contract_handoff_v0.md` | full | workstream goal, fitness reference, registry-vs-Silver boundary | clean |
| `creator_profile_current_record_contract_v0.md` | full | record contract Sections 1-3, comparison rules, declared-deferred recipes | clean |
| `creator_intelligence_profile_surface_v0.md` | full | the only accepted downstream Creator Signal display contract | clean |
| `creator_profile_current_view_spec_v0.md` | full | architecture contract, Dashboard Boundary, Aggregate Influence Rules | clean |
| `creator_profile_current_view_v0.json` | targeted (structural: `python -c "json.load(...)"` posture/platform/sample-support tabulation over all 33 profiles; too large at 333,504 bytes for a full read) | verify the assumption-gate snapshot's quoted counts and check limitations-array content directly | clean; counts verified exact match |
| `orca-harness/capture_spine/creator_profile_current/materialize.py` | targeted (`_profile_limitations`, `_build_platform_account_profile`, `_counts`) | posture/value coupling and limitations-content mechanics named by the prompt | clean |
| `orca-harness/capture_spine/creator_profile_current/validation.py` | targeted (`_validate_metric_values`, `_validate_sample_support`, `_validate_rollup_limitations`) | posture/value coupling enforcement, representativeness/sample-support validation | clean |
| `docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_record_contract_customer_surface_adversarial_artifact_review_v0.md` | full | prior review findings AR-01..AR-05 and residuals directly upstream of this commission | clean |

**Sources available, not read (non-decisive for this finding set):**
`creator_metric_silver_record_contract_v0.md`, `creator_profile_current_lake_native_record_mapping_v0.md`,
`creator_public_handle_linkage_ledger_spec_v0.md`, `creator_public_handle_linkage_ledger_v0.json`
(listed as "available but not default reads" by the commissioning prompt;
nothing in the loaded pack pointed to a gap only they could resolve -- this
review's findings concern display/default-sort semantics over the already-loaded
record contract and view data, not identity-linkage mechanics).

`SOURCE_CONTEXT_READY`.

## Deep-Thinking Frame (`workflow-deep-thinking`, applied)

The commissioning prompt frames the question as a terminology problem
("leaderboard" vs "contextual ranked scan table"). That framing is necessary
but not sufficient. The sharper question is: **does anything in the currently
loaded source pack -- including the direction under review itself -- give an
implementer a mechanical way to build a compliant "contextual" rank, or does
"contextual" collapse to "whatever the implementer assumes" the moment real
data is plugged in?**

Three sub-questions decompose that:

1. **Terminology risk (the prompt's stated frame).** Does the word
   "leaderboard" itself, independent of the underlying mechanics, invite an
   overclaim? Yes, but this is the easier half of the problem -- word choice is
   owner-decidable copy policy, not a source fact this review can resolve
   alone (Review Question 5 is explicitly product language per the
   commissioning prompt).
2. **Comparability risk (harder, source-checkable).** The direction's own
   `intended_customer_shape` already requires the default sort to stay
   "within compatible platform/window/scope" -- so the guard is written. But
   is that guard self-enforcing against the *actual* committed data, or does
   it depend on an implementer correctly inferring "compatible" from prose
   with no bound platform-compatibility rule? This is directly checkable
   against the live view and the record contract's Metric Comparison Rules,
   and the evidence below shows the guard is not self-enforcing: the data
   shape (91% YouTube, 9% Instagram) creates strong UX pressure toward a
   single mixed-platform list, which the record contract's own comparison
   rules would then forbid.
3. **Inherited-gap risk (carried from the immediately-prior review).** The
   sibling record-contract review (AR-01 through AR-04, read in full above)
   already found that `non_claims` has no required display surface anywhere
   downstream (AR-01), declared-deferred fields never appear in `limitations`
   even mechanically (AR-02, re-confirmed below at the code level), no
   display-tier vocabulary exists for what may collapse behind a click
   (AR-03), and -- most directly relevant here -- **no accepted display
   contract addresses the multi-creator ranking/shortlist surface at all**
   (AR-04). This commission's own direction already plans to close AR-04 by
   authoring the missing display contract (`batch_1.proposed_output`). The
   question this review must answer is whether that planned contract, as
   currently *scoped* by the direction under review, would also close AR-01
   through AR-03 for the multi-creator case, or would leave them open at a
   larger blast radius (many rows scanned side by side, rather than one
   profile opened at a time).

The evidence below shows sub-questions 2 and 3 are where the real risk
concentrates: the terminology question (1) is real but secondary, and the
directional guard for (2) is present in prose but unenforced against the
actual data shape, while (3) shows the inherited AR-01/AR-02/AR-03 gaps get
*worse*, not better, at multi-creator scan scale, because a scan surface is
exactly the surface where a customer reads many rows without opening any one
of them.

## Trigger Gate / Lane Collision / Artifact-Role Preflight / Validation Gate

- Trigger gate: satisfied -- the commissioning prompt explicitly names
  `adversarial artifact review` and requires invoking
  `workflow-adversarial-artifact-review` after source readiness.
- Lane collision: none. The review target is a product-direction/documentation
  question over docs-only artifacts (a commissioning prompt, a record
  contract, a display-surface contract); no code, installed-copy, postmortem,
  or prompt-orchestration scope collision.
- Artifact-role preflight: no single artifact-role verdict is claimed. The
  reviewed artifacts each self-declare their own `artifact_role` in their
  headers (`source_capture_family_architecture_contract`,
  `product_signal_surface_contract`); this review does not assert a formal
  role pass/fail.
- Validation gates: not applicable in the software sense. The commissioning
  prompt names no build/test/lint command as a required gate; the review's
  own gate is the `default_view_recommendation` enum it must populate.
- Review output mode: `filesystem-output`, `required_output_path` = this file.
- Dirty-source check: worktree `codex/multi-creator-default-view-review` @
  `612f2aa4` confirmed clean before this write; nothing relied on as authority
  was modified, untracked, or off the expected revision.

## Review Scope / Excluded Scope

**In scope:** whether "contextual ranked scan table" is a safe stated default
for Batch 1's planned display contract, what semantic/display guards it would
need, which default sort basis (if any) the current data supports without
violating the record contract's own comparison rules, how non-observed/
declared-deferred rows must display, whether "leaderboard" as customer-facing
vocabulary is itself unsafe, and what Batch 2's static projection can and
cannot exercise given the current data shape.

**Excluded:** implementation of any actual UI; buyer proof; capture cadence,
discovery-scale, or live-capture authorization; identity-linkage correctness
(the identity ledger is out of scope per the commissioning prompt); composite
scoring, cross-platform aggregate ranking, lead-list, or outreach design (all
explicitly forbidden Batch 1 shapes per the direction under review).

## Phase 1 -- Correctness Findings

### MC-01 (critical) -- the default-sort guard ("compatible platform/window/scope") is unenforced prose against a data shape that will almost certainly violate it

- **Location:** direction under review, `batch_1.intended_customer_shape`
  ("initially sorts creators by one selected, eligible, observed metric such
  as average_views within compatible platform/window/scope"); record contract
  `creator_profile_current_record_contract_v0.md` "Metric Comparison Rules"
  (comparison requires "platform scope and content-kind inclusion are
  compatible"); `creator_profile_current_view_spec_v0.md` "Aggregate Influence
  Rules" (`platform_scope` enum: `instagram`, `tiktok`, `youtube`,
  `cross_platform` -- four distinct values, not fungible).
- **Evidence:** the live committed view has 33 `platform_account` profiles: 30
  `youtube` and 3 `instagram` (`grep -o '"platform": "[a-z]*"'` over
  `creator_profile_current_view_v0.json`, cross-checked with a structural
  Python tabulation over every profile's `platform_accounts[0].platform`,
  which agrees exactly: `{'youtube': 30, 'instagram': 3}`). `average_views`
  is `observed` for all 33 rows regardless of platform. Nothing in the
  direction under review, the record contract, or the Creator Signal surface
  states a rule that a default multi-creator scan/rank must be split by
  platform (tabs, separate lists, or an explicit platform filter) rather than
  rendered as one combined list sorted by the selected metric. The record
  contract's own comparison rule ("platform scope ... compatible") would be
  violated by a single list ranking YouTube view counts against Instagram
  view counts side by side, since YouTube views and Instagram views are not
  the same measurement (different platform-native counting semantics), and
  the platform_scope enum treats them as distinct scopes requiring an
  explicit `cross_platform` designation this record contract never grants to
  `average_views`.
- **Strongest defense and why it fails:** one could argue "within compatible
  platform/window/scope" already tells an implementer to split by platform,
  so this is not a gap. This fails against the actual data shape: with 30
  YouTube rows and only 3 Instagram rows, the path of least resistance for a
  "scan table" implementation is one combined, sortable table (the more
  natural reading of "scan-first table/grid" in the direction's own wording)
  with a platform column, not four separate platform-scoped views for a
  9%-share platform. Nothing forces the harder, more fragmented
  implementation. The guard is real in prose but has no display-contract-level
  mechanism (e.g., a required platform filter/tab as a structural element,
  or an explicit prohibition on a single default-sorted list spanning
  platforms) forcing compliance.
- **Impact:** without an explicit structural rule, the single most likely
  naive implementation of "contextual ranked scan table" directly violates
  the record contract's own Metric Comparison Rules the moment it ships,
  because the visible default action (sort by average_views) would compare
  incompatible platform scopes across nearly all 33 rows.
- **`minimum_closure_condition`:** the new multi-creator display contract
  must state, as a structural (not merely prose) rule, that a default sort by
  an observed metric is scoped to one platform at a time (tabs, a mandatory
  platform filter, or per-platform sections) -- not a single list spanning
  platforms -- unless and until a `cross_platform` rollup is separately
  authorized for that metric.
- **`next_authorized_action`:** owner decision on the structural mechanism
  (tabs vs mandatory filter vs per-platform sections); this review lane has
  no patch authority over the direction or the future display contract.

### MC-02 (critical) -- declared-deferred fields (posting_cadence, recent_velocity) are mechanically absent from every profile's limitations array, so a scan-table default inherits AR-02 at full-roster scale

- **Location:** record contract Section 1 "limitations" subsection and
  Section 3 (posting_cadence, recent_velocity); `materialize.py`
  `_profile_limitations` (lines 306-326); live view `limitations` arrays.
- **Evidence:** `_profile_limitations` in `materialize.py` returns a fixed
  seven-item list (platform-scoping, admitted-pool-only, engagement caveat,
  audience-not-joined, cross-platform-blocked, sample-support instruction,
  fragrance-pool-selection-bias) that never references `posting_cadence` or
  `recent_velocity` by name or by any cadence/velocity synonym. A structural
  check across all 33 live profiles confirms this mechanically: `0` of 33
  profiles' `limitations` (profile-level or rollup-level) mention "cadence"
  or "velocity" in any form, even though `posting_cadence` and
  `recent_velocity` are always-present keys in every profile's
  `metric_rollups` block with `posture: not_attempted` (`33`/`33` for both
  fields). This directly re-confirms the immediately-prior review's AR-02
  finding, now shown to be a hardcoded property of the materializer, not an
  incidental gap in one sample row.
- **Strongest defense and why it fails:** one could argue a scan-table row
  would show each metric with its own posture badge, so a consumer scanning
  the row sees `posting_cadence: not_attempted` directly and does not need
  the `limitations` panel to repeat it. This is the record contract's
  posture/value coupling working as designed for a *full* per-metric render,
  but the direction under review's own `intended_customer_shape` explicitly
  plans to keep "posture, sample support, freshness, and claim-boundary cues
  visible **or immediately reachable**" -- i.e., it anticipates a collapsed
  scan row that may not render every metric's full posture object inline.
  Under a collapsed row (the design a "scan-first table" implies for
  scanability at 33+ rows), `limitations` is the one panel documented as
  required to "travel with the profile" (record contract Section 1, line
  154) -- and that panel structurally omits these two fields for every row.
- **Impact:** at single-profile scale (the prior review's scope) this was one
  finding about one document. At multi-creator scan scale it multiplies
  across every row a customer scans, and it compounds the terminology risk in
  Review Question 5: a scan table that never signals "two of seven metric
  columns are always empty for every creator, by design" reads as an
  incomplete leaderboard rather than a table with two declared-deferred
  columns -- exactly the "look formula-ready" overclaim the direction's
  Section-3-derived guard (Batch 1 forbidden shape: "ranking by
  posting_cadence or recent_velocity while they remain not_attempted") is
  trying to prevent, except the risk here is a silent column, not a
  mis-ranked one.
- **`minimum_closure_condition`:** either (a) the multi-creator display
  contract requires `posting_cadence`/`recent_velocity` to render as a
  visibly-labeled "not yet available" column/state at scan-row granularity
  (not silently omitted), or (b) `materialize.py`'s `_profile_limitations`
  is extended to name every non-observed metric so a `limitations`-driven
  collapsed view inherits the disclosure automatically. Either fix must be
  named; the current state satisfies neither.
- **`next_authorized_action`:** owner decision on (a) vs (b); (b) is a code
  change to `materialize.py` and is out of this review's read-only,
  no-implementation scope (the commissioning prompt forbids implementation,
  lake writes, and code changes).

### MC-03 (major) -- sample-support heterogeneity (2 thin-`n`, 1 limited-`n`, 30 strong-`n` rows) has no scan-row-level visible cue, and a naive default rank would surface it identically to strong-sample rows

- **Location:** record contract Section 1 "limitations" subsection ("A metric
  with a large value and a thin/source-limited sample is still
  source-limited"); `validation.py` `_validate_sample_support` (enforces the
  `sample_adequacy` enum but not its display); live view `sample_support`
  blocks across all 33 profiles.
- **Evidence:** a structural tabulation of `sample_support.sample_adequacy`
  across all 33 live profiles shows `stronger_admitted_pool_n_8_plus: 30`,
  `thin_n_1_to_3: 2`, `limited_n_4_to_7: 1`. All 33 profiles additionally
  carry `representativeness_posture:
  admitted_pool_only_not_representative_creator_average` (uniform across all
  rows -- this uniform caveat does not itself create a *differential*
  overclaim risk, but the `sample_adequacy` split does). The record contract
  requires "sample support and representativeness posture are visible" as a
  precondition for any comparison (Section 2, Metric Comparison Rules), and
  Creator Signal's "Aggregate influence rules" require the surface to show or
  make available "sample support and representativeness posture." Neither
  document specifies *how* that visibility must render in a multi-row scan
  context specifically (a per-row badge, a filter, a sort-suppression rule
  for thin rows), and the direction under review's Review Question 6 asks
  exactly this without the loaded pack answering it.
- **Strongest defense and why it fails:** one could argue the requirement is
  already satisfied by "visible or immediately reachable" per the direction's
  own wording. This is not fully defensible for a *default-sorted* view
  specifically: a default rank is an implicit claim of ordering by merit, and
  if a thin-`n`-2 profile's `average_views` happens to rank high, a
  consumer scanning a sorted list (not clicking into any row) has no
  mechanism, under "immediately reachable," to notice that row's sample
  support differs from its neighbors' unless the row itself carries a visible
  cue -- "reachable" without "visible-by-default" does not prevent a false
  merit impression in a ranked (as opposed to unranked/browsable) view
  specifically, because ranking is the one interaction mode that does not
  require the consumer to inspect each row individually before drawing a
  conclusion.
- **Impact:** concrete, evidence-backed instance of Review Question 6's risk,
  specific to *ranked* (not merely tabular) default presentation: 2 of 33
  rows (6%) could rank misleadingly high or low on a thin sample without any
  required scan-row-level signal.
- **`minimum_closure_condition`:** the multi-creator display contract must
  require a visible (not merely reachable) sample-support cue on every row of
  a default-sorted view specifically -- e.g., a badge or a suppressed/
  downgraded rank position for `thin_n_1_to_3` rows -- distinct from the
  general "visible or reachable" rule that is adequate for an unranked
  browsable table.
- **`next_authorized_action`:** owner decision on the specific cue mechanism;
  advisory only, no patch authority.

### MC-04 (major) -- `non_claims`'s unresolved display-surface gap (AR-01, still open) is more dangerous at ranked-scan scale specifically because of the word "leaderboard"

- **Location:** prior review AR-01 (unresolved, re-read in full above);
  Creator Signal "Required surface sections" table (no `non_claims` row);
  direction under review, Review Question 5 ("Does 'leaderboard' ...create a
  forbidden implication of winner/loser, buyer proof, performance guarantee,
  lead-list, or outreach priority even if the internal contract is
  careful?").
- **Evidence:** AR-01 established that `non_claims` -- which explicitly
  disclaims "buyer proof", "guaranteed creator performance", and
  "contact/outreach authorization" among other claims -- has no required
  display surface in either the record contract or the one accepted
  downstream display contract (Creator Signal). That finding is unchanged in
  this review's fresh read of both documents: the Creator Signal "Required
  surface sections" table still lists six rows and none is `non_claims`.
  Nothing in the direction under review adds a `non_claims` display
  requirement for the multi-creator case either -- `forbidden_batch_1_shape`
  lists "buyer proof, validation, readiness, or guaranteed performance" as
  forbidden *claims* the surface must not make, but does not require
  `non_claims` to be affirmatively rendered as the mechanism that prevents
  those claims from being *implied* by the visual framing.
- **Strongest defense and why it fails:** one could argue the
  `forbidden_batch_1_shape` list is itself sufficient guardrail language,
  since it directly prohibits the dangerous shapes. This addresses what the
  surface may *contain* but not what it may *imply through omission*: a
  ranked table of creators sorted by a performance-adjacent metric, with no
  required `non_claims` panel anywhere reachable, visually reads as
  "here is who performs best" regardless of what the underlying data
  technically claims -- the exact "winner/loser... performance guarantee"
  implication Review Question 5 names, and the one document that would
  contradict that implied reading (`non_claims`) still has no required
  display surface.
- **Impact:** this is the load-bearing reason "leaderboard" is riskier than a
  synonym-swap problem: even the direction's own preferred term ("contextual
  ranked scan table") carries the same implied-winner risk as long as
  `non_claims` remains unreachable by design (AR-01 unresolved). Renaming
  "leaderboard" to "ranked table" without closing AR-01 addresses the label,
  not the mechanism that would make the label misleading.
- **`minimum_closure_condition`:** AR-01's closure condition (a required,
  reachable `non_claims` display surface, in either the record contract or
  Creator Signal) is a precondition for *any* ranked default -- contextual or
  otherwise -- not merely a nice-to-have for the single-profile case it was
  originally raised in.
- **`next_authorized_action`:** the multi-creator display contract Batch 1
  is about to author should either close AR-01 itself (require a reachable
  `non_claims` affordance at the scan-table level, e.g., an always-visible
  "what this table doesn't prove" link) or explicitly state it depends on a
  separate AR-01 closure landing first; this review lane has no patch
  authority to force that ordering.

### MC-05 (minor) -- Batch 2's stated purpose ("exercise ... row treatment") cannot exercise the ideal-audience row case at all with current data

- **Location:** direction under review `batch_2.intended_use`; live view
  `counts.profiles_with_ideal_audience_profiles`.
- **Evidence:** the live view's own `counts` block reports
  `profiles_with_ideal_audience_profiles: 0` across all 33 profiles (verified
  by direct structural read of the `counts` dict, not inference). Creator
  Signal's "Required surface sections" table lists "Ideal/content-fit
  audience" as a required section with source owner "Capture ideal-audience
  inference + ballot taxonomy." Batch 2's `intended_use` states it will
  "Exercise customer-surface information architecture and row treatment
  before storage engine, dashboard, API, or capture/lake work" -- but with
  zero populated ideal-audience snapshots, the null/absent-field row
  treatment for that specific required section cannot be exercised by Batch
  2 against real data; it can only be exercised as a hypothetical empty-state
  mockup.
- **Strongest defense and why it fails:** one could argue an
  always-empty section is itself a valid row-treatment case to exercise (the
  "always null" state). This is a legitimate but narrower claim than the
  direction's own wording implies ("exercise ... row treatment" reads as
  exercising the *range* of states, not confirming one section is
  permanently in its one and only observed state for this data window).
- **Impact:** minor scope-accuracy issue only; does not block Batch 2, but
  Batch 2's closeout should not claim it "exercised" ideal-audience row
  treatment beyond the single always-null case, since no other case exists in
  the current committed data to exercise.
- **`minimum_closure_condition`:** Batch 2's closeout should name this gap
  explicitly (ideal-audience section exercised only in its null state) rather
  than implying full row-treatment coverage.
- **`next_authorized_action`:** advisory only; no patch authority.

## Phase 2 -- Friction Findings

None material beyond what is already folded into Phase 1 (MC-01 and MC-04
each have a direct correctness consequence, so they are reported there rather
than as separate friction items). The direction under review's own structure
(Batch 1 display contract before Batch 2 projection, explicit forbidden
shapes list, assumption-gate snapshot) is well-organized and does not itself
impose avoidable process burden.

## Non-Findings (plausible failure modes checked and ruled out)

- **NF-1 -- the zero-fill guard remains solid at multi-creator scale.**
  `validation.py`'s `_validate_metric_values` enforces
  `metric_value_for_non_observed_posture` and
  `missing_metric_posture_reason` errors for any non-observed metric that
  carries a non-null value or lacks a reason; a structural check across all
  33 live profiles confirms every `not_attempted`/`unavailable_with_reason`
  field carries `value_or_none: null`. This rules out the direction's named
  forbidden shape "ranking non-observed values as zero" for the currently
  committed data -- the underlying data cannot be zero-ranked even by
  accident, though the *display* gap in MC-02 remains (data correctness and
  display disclosure are separate properties).
- **NF-2 -- the representativeness-posture guard is uniform, not
  differential, so it does not itself create a false-comparison risk.** All
  33 profiles carry the identical
  `admitted_pool_only_not_representative_creator_average` posture
  (`_validate_sample_support` in `validation.py` hard-fails any other value).
  Because this caveat is uniform across every row, a scan table does not risk
  making one row look more "representative" than another on this specific
  axis -- the risk concentrated in `sample_adequacy` (MC-03) instead, which
  does vary per row.
- **NF-3 -- cross-platform aggregate rollups cannot appear in the current
  data regardless of display choices.** `counts.cross_platform_rollup_profiles:
  0` and `counts.creator_record_profiles: 0` confirm no `creator_record`
  (linked, cross-platform) subject exists in the committed view; every
  profile is `platform_account`-scoped. This closes off one version of
  MC-01's risk (a `cross_platform`-labeled composite rank) even though the
  *mixed-platform-in-one-list* version of MC-01 remains open, since
  `platform_account`-scoped rows from different platforms can still be
  combined into one naive list without ever touching the `cross_platform`
  enum value.

## Explicit Answer To The Commissioned Question

```yaml
default_view_recommendation: DEFAULT_CONTEXTUAL_RANKED_SCAN_TABLE
```

**Conditional, not unconditional.** A contextual ranked scan table is the
right target shape -- the direction's own forbidden-shapes list already rules
out the dangerous versions (universal rank, composite score, zero-ranking
non-observed values, ranking not-attempted metrics), and NF-1/NF-2/NF-3 show
the underlying data cannot currently produce those specific violations even
by accident. But "contextual" is not yet a self-enforcing property of the
current data plus the current source pack. Before Batch 1 may safely author
the multi-creator display contract with this as the stated default, four
guards need to be pinned as structural rules, not prose:

1. **Platform-scoped default sort, enforced structurally** (MC-01): a
   default sort by an observed metric must not span platforms in one list
   given the current 30-YouTube / 3-Instagram data shape, or it violates the
   record contract's own Metric Comparison Rules.
2. **Declared-deferred field visibility at scan-row granularity** (MC-02):
   `posting_cadence`/`recent_velocity` must not silently disappear from a
   collapsed scan row the way they currently disappear from every profile's
   `limitations` array.
3. **Visible (not merely reachable) sample-support cue specifically for
   ranked/sorted views** (MC-03): the 2 thin-sample and 1 limited-sample rows
   need a rank-specific disclosure a purely-browsable table would not
   require.
4. **A reachable `non_claims` mechanism as a precondition for any ranked
   default, not only a single-profile nicety** (MC-04): this closes the
   deeper reason "leaderboard" framing is unsafe even under a renamed,
   internally-careful "contextual ranked scan table."

If the owner is not ready to pin all four as part of Batch 1's display
contract, `DEFAULT_NEUTRAL_SCAN_TABLE` (unranked or user-selected sort,
platform-tabbed by default) is the safer interim shape, since it defers the
comparability and ranking-implies-merit risks (MC-01, MC-03) without
blocking Batch 2's other row-treatment testing goals.

On the terminology question specifically (Review Question 5): recommend
blocking the literal customer-facing word "leaderboard" regardless of which
recommendation above is chosen, because MC-04's `non_claims` gap means
nothing currently prevents the winner/loser implication "leaderboard" invites
by itself. "Ranked table" or "ranked scan" carries materially less of that
specific implication and should be preferred in customer-facing copy.

## Not-Proven Boundaries

- Whether an implementer would in practice default to a single mixed-platform
  list (MC-01) versus correctly inferring platform-tabbing from
  "compatible platform/window/scope" -- no implementation exists yet to
  check; this is a risk assessment from the data shape and prose specificity,
  not an observed failure.
- Whether the owner intends the new multi-creator display contract to close
  AR-01/AR-02/AR-03 itself, or to explicitly defer them as still-open
  residuals with a stated reason -- not stated anywhere in the loaded source
  pack.
- Whether Silver's near-term producer timeline would make MC-02 low-urgency
  in practice (e.g., if `posting_cadence` is expected to populate within one
  cycle) -- no Silver producer timeline is in the loaded source pack.
- Formal artifact-role pass/fail status for any reviewed artifact: not
  claimed.

## Review-Use Boundary

This is a read-only adversarial artifact review. Findings and non-findings
above are decision input only -- not approval, validation, mandatory
remediation, implementation authorization, dashboard authorization, live
capture authorization, lake-write authorization, identity-write authorization,
or outreach/lead-list authority. No `patch_queue_entry` is included (none
authorized by the commissioning prompt, which explicitly forbids it and
scopes this lane to read-only review). Closure of MC-01 through MC-05
requires an owner decision on the four named guards, followed by the Batch 1
display-contract authoring pass the direction under review already plans --
this review lane may not author that contract itself.
