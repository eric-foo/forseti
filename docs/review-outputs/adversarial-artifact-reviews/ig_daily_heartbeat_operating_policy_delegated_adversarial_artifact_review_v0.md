# IG Daily Heartbeat Operating Policy — Delegated Adversarial Artifact Review (v0)

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial artifact review output (decision input only)
scope: >
  Controller review-and-patch return for the IG Daily Heartbeat Operating Policy
  v0. Records findings, one bounded target-file patch, neutral citations, a
  controller recommendation, validation/readback evidence, off-scope flags, and a
  Chief Architect adjudication packet. Not owner acceptance and not a kept patch.
use_when:
  - Chief Architect adjudication of the IG daily heartbeat policy hardening pass.
  - Checking what the de-correlated controller changed, flagged, or defended.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
  - docs/prompts/reviews/ig_daily_heartbeat_operating_policy_delegated_adversarial_review_patch_prompt_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
stale_if:
  - The target policy is re-patched or its pinned hash changes before adjudication.
  - The owner pins the "2.5k/day" unit or reconciles the roster-ledger tier cadence, closing AR-02 or AR-03.
```

## 1. Commission, Lane Binding, and Actor / Model-Family Receipt

Commission: `workflow-delegated-review-patch`, `base-subagent` mode, one authored
target artifact, bounded patch scope (single target file plus this durable
report). Selected review lane: `workflow-adversarial-artifact-review`, invoked
after source readiness, with `workflow-deep-thinking` framing first. De-correlation
is a who-constraint only; no runtime-model routing or ranking is expressed.

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT-family Codex lane
  controller_model_family: Anthropic / Claude (Opus 4.8)
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  access_mode: repo
  de_correlation_status: satisfied
  de_correlation_bar: cross_vendor_discovery
```

```yaml
operator_fields_bound_at_courier_runtime:
  controller_model_family: Anthropic / Claude (Opus 4.8)
  access_mode: repo
  controller_report_destination_confirmed: yes
  reviewed_by_value_for_report: claude-opus-4.8
```

Provenance (operator/CA-set; observed record, never a model recommendation):

```yaml
reviewed_by: claude-opus-4.8
authored_by: openai gpt-family (Codex lane); exact version unrecorded
de_correlation_bar: cross_vendor_discovery
```

Method contract satisfied: `REFERENCE-LOAD` of the three methods, then
`SOURCE-LOAD`, then `SOURCE_CONTEXT_READY`, then `APPLY`. The review lane was
invoked, not silently emulated inline.

## 2. Source Context Status (SOURCE_CONTEXT_READY) and Target Hash Verification

Status: `SOURCE_CONTEXT_READY`.

Target hash verification at review start: the submitted target file SHA256 was
`37D5AD256D51A282B1DB145330AC649692E69DE834A7C29D7E5F1EC4B56DA7C5`, which matches
the pinned `target SHA256 at prompt creation` exactly. Not `SOURCE_STALE_TARGET_CHANGED`.
The pinned commit `280fddd7` is an ancestor of the branch HEAD (`482b51c7`), as the
commission anticipated. The post-patch target now differs from the pinned hash by
exactly the applied diff in section 5 (the authorized delegated change).

Workspace note: the controller was launched in a separate Claude review worktree
that does not contain the target; the review ran in place against the commission's
declared `.codex/worktrees/ig-daily-heartbeat-policy` workspace, where the target,
companions, and report path live on branch `codex/ig-daily-heartbeat-policy`. No
worktree was created, cloned, or switched. The workspace was clean before this pass.

Authority sources read: `AGENTS.md`; overlay `README.md`, `source-of-truth.md`,
`source-loading.md`, `delegated-review-patch.md`, `review-lanes.md`,
`prompt-orchestration.md`, `validation-gates.md`, `safety-rules.md`,
`communication-style.md`; templates `adversarial_artifact_review_v0.md` and the
`orca_preflight_defaults_v0.md` pointer. Target read in full. Companions read:
IG family `README.md`, grid DOM spec, at-scale envelope, creator monitoring policy
architecture, and the reels capture cadence/durability doctrine. One material
adjacent read was taken because a finding could not be assessed without it:
`ig_creator_roster_frontier_ledger_spec_v0.md` (surfaced by the breakout-tag and
roster-vocabulary greps).

## 3. Findings (severity order: critical, major, minor)

No critical findings. The core boundaries — read-only write ban, fail-closed
challenge handling, additive time-series, onboarding separation, no-invisibility /
no-stealth / no-code-alignment honesty — are correctly and durably written.

Severity and confidence are priority labels only; they create no approval,
rejection, readiness, validation, or remediation authority.

### AR-01 — major — confidence high — correctness — PATCHED

- artifact: `[ig-heartbeat-policy]`
- location: "Deep Capture Boundary" section (breakout tag list).
- issue: The deep-capture gate depends on four post-level breakout tags
  (`spike_candidate`, `fresh_breakout_candidate`, `active_breakout_candidate`,
  `durable_breakout_candidate`) that are defined nowhere in the repository and are
  not pointer-bound to an owning/producing lane. The phrase "posts already tagged
  by monitoring" implies an existing tagging mechanism.
- evidence: A repo-wide grep for the four tag names returned hits only in the
  target itself and in the review prompt that quotes it — no defining source. The
  two most relevant companions use different vocabularies:
  `forseti_creator_monitoring_policy_architecture_v0.md` describes a PROPOSED
  hot-list / spike / promotion machinery (not those tag names), and
  `ig_creator_roster_frontier_ledger_spec_v0.md` uses `signal_state`
  (`rostered|windcaller_candidate|windcaller_active|not_signal_bearing`) and
  `roster_tier`, not the four `*_candidate` tags.
- impact: Directly threatens the fitness success signal ("translate the policy into
  runner metadata or implementation tasks without inventing missing behavior"): a
  downstream runner cannot resolve what qualifies a post and could synthesize its
  own breakout criteria, or leave the gate unimplementable.
- minimum_closure_condition: The breakout tag vocabulary and its producing lane are
  either bound to a defining source, or explicitly marked as a forward dependency
  not yet bound, so a downstream reader cannot mistake the tags for an existing,
  self-defined contract.
- next_authorized_action: Applied within the commissioned bounded patch scope
  (target-file wording only). CA adjudicates keep/modify/reject.
- patched: yes — a two-sentence clarification marks the tags as a forward
  dependency produced by the (proposed) creator monitoring lane, points to
  `forseti_creator_monitoring_policy_architecture_v0.md`, and forbids the runner
  from synthesizing its own breakout criteria. The clarification does not invent a
  definition for any tag. See the diff in section 5.

### AR-02 — major — confidence medium — correctness — FLAGGED (owner decision; not patched)

- artifact: `[ig-heartbeat-policy]`
- location: "Current Direction" fenced block (`2.5k/day serious posture = 2 distinct egress lanes`) and "Deferred" (`2.5k/day live test`).
- issue: "2.5k/day" is unitless and its composition is not pinned — creators,
  reads/requests, or captures — and it is not reconciled with the companion roster
  numbers. The `steady_state_registered_roster = daily heartbeat` line (one read
  per creator per day) sits beside "2.5k/day" without stating whether 2.5k is the
  roster size or the daily read volume.
- evidence: `forseti_creator_monitoring_policy_architecture_v0.md` and
  `ig_creator_roster_frontier_ledger_spec_v0.md` set the serious-v0 planning roster
  at 1,000 creators (gates 250 → 500 → 1,000); `ig_at_scale_operating_envelope_v0.md`
  models ~2,800–3,500 modeled IG requests/day for that 1,000-creator plan (which
  included multi-read momentum curves the daily-heartbeat policy removes). The
  envelope's own 2026-07-08 owner note also names "the current 2.5k/day steady
  daily-heartbeat target" without a unit. So the figure is ambiguous across the
  corpus, not only in the target.
- impact: A capacity- or roster-planning lane could read 2.5k as creators (a roster
  more than double the companion's 1,000 serious-v0 target) or as daily reads, and
  size egress/telemetry differently. The bound fitness reference itself embeds
  "two-egress 2.5k/day posture" as a goal element, so the goal is not independently
  checkable while the unit is open — this is also the answer to "attack the fitness
  reference": the reference is otherwise well-chosen, but this element is not yet a
  checkable quantity.
- minimum_closure_condition: The owner states what "2.5k/day" counts (creators vs
  daily reads vs captures) and how it relates to the registered roster size and the
  envelope's request budget.
- next_authorized_action: Owner decision. Not patched: pinning the unit requires
  owner input the controller cannot supply without fabricating a number.
- patched: no.

### AR-03 — major — confidence medium-high — correctness — OFF-SCOPE FLAG (companion; not patched)

- artifact: off-scope companion `ig_creator_roster_frontier_ledger_spec_v0.md` (the target is not the defect site).
- location: that spec's "Commercial Slice And Roster Gates" → "Tier meaning" block and required `roster_tier` field.
- issue: The roster/frontier ledger still encodes A/B/C tiers with
  differential-cadence meaning ("Tier A: dense monitoring… Tier C: cheap
  heartbeat") and requires `roster_tier`, and it did not receive the 2026-07-08
  daily-heartbeat override note that the three other companions all carry.
- evidence: `forseti_creator_monitoring_policy_architecture_v0.md` (Current IG
  Daily-Heartbeat Override + status line), `ig_reels_capture_cadence_durability_doctrine_v0.md`
  (status "superseded … by ig_daily_heartbeat_operating_policy_v0.md" + 2026-07-08
  owner update), and `ig_at_scale_operating_envelope_v0.md` (2026-07-08 owner
  update + roster-cap disclaimer) each explicitly defer to the target; the roster
  ledger has no equivalent note and its tier descriptions still read as sparse
  cadence.
- impact: This is exactly the revival hazard the target exists to prevent. A cold
  agent building the roster from the ledger could bake "Tier C = cheap/weekly
  heartbeat" into tooling, contradicting "all registered IG creators … daily for now."
- minimum_closure_condition: The roster ledger carries a daily-heartbeat override
  note (mirroring the other companions) clarifying that under current steady-state
  cadence `roster_tier` is a priority label, not a differential-cadence knob; or the
  target adds a reconciling pointer that the ledger's tier cadence is superseded.
- next_authorized_action: Off-scope for this commission (companion edit is barred).
  Route to an owner decision / a separate companion-lane patch. Flagged, not edited.
- patched: no (off-scope).

### AR-04 — minor — confidence medium — correctness — FLAGGED advisory (not patched)

- artifact: `[ig-heartbeat-policy]`
- location: "Current Direction" ("registered IG creators … one daily … heartbeat").
- issue: "registered IG creators" is not the roster-ledger vocabulary. The ledger's
  operational in-roster states are `roster_status: active` and `signal_state: rostered`;
  the daily-heartbeat population (which `roster_status`/`signal_state`, and whether it
  spans all A/B/C tiers) is not bound.
- evidence: `ig_creator_roster_frontier_ledger_spec_v0.md` `creator_roster_entry`
  fields (`roster_status`, `signal_state`, `roster_tier`); the term "registered"
  appears nowhere in that ledger.
- impact: A runner translating "all registered creators are daily" must guess the
  population set; low but real translation ambiguity.
- minimum_closure_condition: "registered" is bound to the roster-ledger vocabulary
  (e.g., active roster entries), or the intended population set is stated.
- next_authorized_action: Owner/author decision on the population set; advisory only.
- patched: no (defining the exact population is not a mechanical, non-inventing edit).

### AR-05 — minor — confidence low — correctness — FLAGGED advisory (not patched)

- artifact: `[ig-heartbeat-policy]`
- location: "Current Direction" ("The normal-grid target is `10-15s` end-to-end per creator").
- issue: The 10–15s end-to-end operating figure has no cited basis and is not
  reconciled with the envelope's stated planning numbers.
- evidence: `ig_at_scale_operating_envelope_v0.md` uses ~9s/request (an unvalidated
  planning target) and 2.5–4s minimum spacing; the grid spec notes a ~4.0s post-load
  settle window. 10–15s E2E is plausible as page-load + settle + parse + gap, but the
  target neither derives nor cites it.
- impact: Minor; the figure is labeled a "target" and the 2.5k/day live test is
  deferred, so it is partly hedged, but a capacity estimate could inherit an unsourced number.
- minimum_closure_condition: The figure is cited to a basis or marked an owner-set
  starting target to be tuned against telemetry.
- next_authorized_action: Owner/author decision; advisory only.
- patched: no.

### AR-06 — minor — confidence low — friction — FLAGGED advisory (not patched)

- artifact: `[ig-heartbeat-policy]`
- location: "Challenge / CAPTCHA Handling" ("keep the supervised browser/session open … wait for manual owner resolution only within a bounded operator window").
- issue: The hold-session-open-and-wait behavior is not explicitly reconciled with
  the companion envelope's "abort on any login redirect / interstitial / block; then
  fully quiet, not periodic probing." An implementer could be unsure whether to hold
  or drop a challenged session.
- evidence: `ig_at_scale_operating_envelope_v0.md` "Default session posture" (abort +
  fully quiet) vs the target's supervised bounded-wait model.
- impact: Low. The target already forbids auto-solve / route-around / retry-harder, so
  the automated-abuse risk is closed; the residual is only the hold-vs-drop and
  account-footprint question in supervised mode.
- minimum_closure_condition: The target notes that the supervised bounded-wait is a
  human handoff distinct from the envelope's unattended-egress abort/quiet rule.
- next_authorized_action: Owner/author decision; advisory only.
- patched: no.

### considered_and_defended (candidates the steelman defeated — not findings)

- "Aphrodite workflow memory" used without an inline gloss — defended: "Aphrodite"
  is a pervasive, bound project codename with its own `forseti/product/spines/creator_signal/`
  spine family (charter, capture-strategy, provenance-contract docs) and is
  resolvable via the repo map; grep found it across ~40 files. Not an unbound term.
- "no pagination / scroll expansion / item-page fan-out by default" softener —
  defended: the "by default" phrasing matches the grid spec's "unless the run
  explicitly enables a different mode and records it," and pagination / history
  backfill are explicitly in the Deferred list (not authorized), so the boundary is
  not actually left open.
- Egress lane-2 guidance looser than the envelope (omits "second physical laptop" and
  the no-VM rule) — defended: the load-bearing invariant (two distinct public
  egresses, verified by non-IG public-IP/provider checks) is preserved verbatim in
  the target; the physical-device and VM specifics are envelope-owned operational
  detail, appropriately not duplicated.
- Static-capture companion surface not mentioned — defended: static/profile-grid
  capture is onboarding / periodic-refresh / escalation scope per the grid spec,
  explicitly outside daily heartbeat; the target's onboarding-separation boundary
  already covers it.

### Optional hardening (optional, non-required — not blockers, not patch authority)

- OH-1: Cross-reference `ig_reels_capture_cadence_durability_doctrine_v0.md` for the
  exit-code → gap-record mechanics that operationalize the target's "missingness, not
  zero" rule, so an implementer can find the exit-5/exit-3 handling in one hop.
- OH-2: Add the roster/frontier ledger spec to the target's reconciliation so the
  "registered/rostered" population (AR-04) and the tier-label-vs-cadence relationship
  (AR-03) resolve from the target in one hop.

## 4. Finding Field Summary

| id | severity | confidence | phase | patched | next_authorized_action |
| --- | --- | --- | --- | --- | --- |
| AR-01 | major | high | correctness | yes | CA adjudicate applied diff |
| AR-02 | major | medium | correctness | no | owner decision (pin 2.5k/day unit) |
| AR-03 | major | medium-high | correctness | no (off-scope) | owner / companion-lane patch |
| AR-04 | minor | medium | correctness | no | owner/author decision |
| AR-05 | minor | low | correctness | no | owner/author decision |
| AR-06 | minor | low | friction | no | owner/author decision |

## 5. Unified Diff (target-file change for AR-01)

```diff
diff --git a/forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md b/forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
index 7e34c594..24c05560 100644
--- a/forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
+++ b/forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
@@ -126,6 +126,13 @@ monitoring as one of:
 - `active_breakout_candidate`;
 - `durable_breakout_candidate`.

+These breakout tags are produced by the creator monitoring lane, not by the
+heartbeat runner; the tagging machinery and exact tag vocabulary are a forward
+dependency not yet bound in a cited source (the proposed spike/hot-list/breakout
+machinery is in `forseti_creator_monitoring_policy_architecture_v0.md`). The
+heartbeat runner deep-captures only posts the monitoring lane has actually
+tagged and must not synthesize its own breakout criteria.
+
 If no tagged candidate exists for a creator, the steady-state daily heartbeat
 does not deep-capture that creator. Do not run random `0-2 per creator` deep
 captures as part of daily heartbeat.
```

## 6. Per-Change Neutral Source Citations

For the AR-01 patch (neutral, decision-sufficient; argument lives in the finding/verdict, not here):

- The four breakout tag names occur only in the target policy and the review prompt;
  a repo-wide grep found no defining source elsewhere.
- `forseti_creator_monitoring_policy_architecture_v0.md` status/header mark the
  spike / hot-list / promotion machinery as PROPOSED ("PROPOSED — creator monitoring
  policy"; "Resolved (owner, 2026-06-15) … Remaining build prerequisite: … unbuilt
  runtime work"), and it is already listed in the target's `open_next`.
- `ig_creator_roster_frontier_ledger_spec_v0.md` uses `signal_state`
  (`rostered|windcaller_candidate|windcaller_active|not_signal_bearing`) and
  `roster_tier`, not the four `*_candidate` tags — i.e., no companion binds them.
- `.agents/workflow-overlay/delegated-review-patch.md` bounds the patch to the single
  named target and requires the fix to be wording that makes the artifact coherent
  and non-misleading; the applied edit adds a forward-dependency note only and
  invents no tag definition.

## 7. Controller Verdict and Residual-Risk Note

Recommendation: `accept_with_friction` for the target policy — its core operating
boundaries are sound and honestly hedged, and the one clearly patchable coherence
defect (AR-01) was closed in-scope. The remaining items are decision input for CA
adjudication, not defects the controller can or should self-close:

- AR-02 (define the "2.5k/day" unit) and AR-04/AR-05 are owner/author decisions.
- AR-03 is an off-scope companion contradiction (roster-ledger tier cadence) that is
  the most system-material remaining item, because it can revive the exact stale
  posture this policy exists to prevent; it needs a separate companion-lane action.

Residual risk: (a) if the owner never pins 2.5k/day, downstream capacity/roster
translation stays ambiguous; (b) until the roster ledger gets its override note, a
cold roster-building lane can reintroduce Tier-C sparse cadence from that companion;
(c) the AR-01 patch documents a forward dependency but does not make the breakout
tagging lane exist — deep capture remains unimplementable until that lane is built and
its vocabulary bound (which the target already treats as deferred). This is a
cross-vendor discovery pass (Claude reviewing a GPT-family-authored artifact); it is
not a validation, readiness, or no-defect guarantee.

## 8. Validation / Readback Status (observed)

- `git diff --check`: exit 0 (clean). The only output was a benign Windows
  "LF will be replaced by CRLF" advisory, not a whitespace/conflict error.
- `git status --short`: exactly one modified path — the target file. No other file
  touched by the patch step; this report is the only added file.
- Patched-section readback: the `git diff` output in section 5 is the verbatim
  applied change; the added block sits between the breakout tag list and the
  "If no tagged candidate…" paragraph, as intended.
- Stale-language search (required token set) over the patched target: `A/B/C sparse
  cadence current`, `random 0-2`, `paginate`, `scroll expansion`, `DOM invisible`,
  `stealth`, `auto-solve`, `route around`, `platform write`, `onboarding top-band`,
  `code alignment`, `validated`, `account-safety proof`. Every occurrence is in a
  negated, forbidding, deferring, or non-claim sense (e.g., "Do not use A/B/C sparse
  cadence as the current operating default"; "Do not claim DOM reading is invisible";
  "do not auto-solve, route around, retry harder"; "not a stealth … claim"; "policy
  does not claim code alignment"; "not account-safety proof"). No token endorses a
  stale/revived posture. The AR-01 addition introduces no stale endorsement.

## 9. Off-Scope Flags

- AR-03: `ig_creator_roster_frontier_ledger_spec_v0.md` retains differential-cadence
  A/B/C tier meaning without the daily-heartbeat override note carried by the other
  companions. Flagged, not edited (companion edit barred by commission scope).
- Not inspected/patched, per commission hard stops: IG README, grid DOM spec,
  at-scale envelope, monitoring architecture, cadence doctrine, runner code, prompts,
  overlay files, tests, and any onboarding policy. No design-level defect was found in
  the target, so no `NEEDS_ARCHITECTURE_PASS` and no quarantined partial diff.

## 10. Chief Architect Adjudication Packet

The diff, citations, and verdict below are claims to adjudicate, not premises to
inherit. Nothing here is kept until the Chief Architect adjudicates it.

- AR-01 (applied): keep / modify / reject the forward-dependency clarification. Ready
  for accept/modify/reject adjudication. Closure condition: breakout tags are no
  longer readable as an existing self-defined contract.
- AR-02 (owner decision): pin the "2.5k/day" unit and its relation to the registered
  roster size and the envelope request budget. Not self-closable by the controller.
- AR-03 (off-scope, companion): add a daily-heartbeat override note to
  `ig_creator_roster_frontier_ledger_spec_v0.md` (or a reconciling pointer in the
  target). Needs a separate companion-lane action / owner decision.
- AR-04, AR-05, AR-06 (advisory refinements): bind "registered" to roster vocabulary;
  cite or mark the 10–15s figure as an owner-set starting target; note the supervised
  bounded-wait vs unattended abort/quiet distinction.
- OH-1, OH-2 (optional, non-required): cross-reference the cadence doctrine and the
  roster ledger for one-hop resolvability.

Adjudication closeout guidance (per `.agents/workflow-overlay/communication-style.md`
→ Review Adjudication Next Step): first adjudicate findings/diff/verdict/residuals as
claims; close self-closable items (e.g., keep/modify/reject AR-01, and — if the owner
supplies the 2.5k/day unit — apply AR-02) in the same turn; route AR-03 as a separate
companion-lane closure step; then batch commit/push/PR into one land step and
deep-think the material next moves.

## 11. Review-Use Boundary

These findings are decision input only for Chief Architect adjudication; they are not
approval, not validation, not mandatory remediation, and not executor-ready patch
authority, and nothing here — including the applied AR-01 diff — is kept, accepted,
validated, or ready until the Chief Architect adjudicates it. This review is not
owner acceptance, account-safety proof, platform permission, anti-detection proof,
live-capture authorization, runner implementation alignment, onboarding policy, or
source-capture authorization.

## Delegated Review Return Courier

```text
DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Adjudicate under the delegated-review-patch return contract.

- commission: harden the IG Daily Heartbeat Operating Policy v0; single target file;
  repo access mode; cross-vendor controller (Anthropic Claude vs OpenAI GPT/Codex author).
- reviewed artifact: forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
- bounded patch scope: the target file only (this report is the review output).
- findings: AR-01 (major, patched) breakout tags unbound; AR-02 (major, owner) 2.5k/day
  unitless; AR-03 (major, off-scope) roster-ledger tier cadence un-reconciled; AR-04/05/06
  (minor, advisory) registered vocabulary, 10-15s basis, challenge session hold-vs-drop.
- applied patch: one 7-line forward-dependency clarification for AR-01 (see section 5 diff).
- citations: section 6.
- reviewer verdict: accept_with_friction for the target; AR-02 and AR-03 need owner action.
- residual risk: unresolved 2.5k/day unit; companion revival hazard until the ledger note lands;
  deep capture unimplementable until the breakout tagging lane is built.
- blockers / off-scope / not-proven: AR-03 companion edit off-scope; no strict PASS/readiness/
  validation claimed; nothing kept without CA adjudication.
```
