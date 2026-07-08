# Reddit Pre-Commercial Capture Consolidation Success-Signal Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Architecture routing object (non-executing)
scope: >
  Non-executing architecture routing object that decides how to harden the
  success signals in the Reddit pre-commercial capture/consolidation planning
  thread so every Reddit capture/consolidation claim is checkable against Data
  Capture obligations, Source Capture Packet provenance, packet lifecycle,
  source-quality vocabulary, state-assembler boundaries, source-access hard
  stops, and commercial-transition triggers. Recommends patch clauses; applies
  none.
use_when:
  - Deciding how to add robust, checkable success signals to the Reddit
    pre-commercial capture/consolidation planning thread.
  - Checking which existing Source Capture Armory vocabulary Reddit
    capture/consolidation rows must reuse instead of forking.
  - Preventing Reddit capture/consolidation from becoming storage, broad
    crawling, source discovery, source-quality scoring, fixture admission, ECR,
    Cleaning, Judgment, validation, readiness, or commercial Reddit use by
    implication.
authority_boundary: planning_only
open_next:
  - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - docs/prompts/architecture/reddit_precommercial_capture_consolidation_success_signal_architecture_prompt_v0.md
  - docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
  - docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md
  - docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
stale_if:
  - The Reddit planning thread is patched so these success signals are already
    present, superseded, or moved.
  - The Mini God-Tier result-token set, packet lifecycle set, queue row-status
    set, or state-assembler census discipline changes.
  - The Data Capture obligation contract changes obligations, discharge
    vocabulary, or forbidden outputs.
  - The source-access boundary, hard stops, Reddit method order, CloakBrowser
    selection, or commercial-transition trigger changes.
  - The packet fixture/retention/sensitivity decision is amended or superseded.
```

## 1. Status And Non-Executing Boundary

Status: `REDDIT_CAPTURE_CONSOLIDATION_SUCCESS_SIGNAL_ARCHITECTURE_V0`.

Pass type: non-executing architecture-planning pass (advisory routing object).

Architecture result: `TARGET_RECOMMENDED` (see Section 10).

This artifact is design-only. It does not authorize or perform live Reddit
access, CloakBrowser/Patchright/Playwright/BeautifulSoup/PRAW installation or
execution, runner dispatch, parser implementation, storage, database, queue,
scheduler, dashboard, deployment, production monitoring, ECR, Cleaning,
Judgment, fixture admission, source-quality scoring, buyer proof, commercial
Reddit use, commits, pushes, or PRs.

It does not patch the Reddit planning thread. The current launch instruction
granted file-write for this architecture artifact only and did not grant patch
authority for
`docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`.
The recommended clauses in Section 12 are inputs to a later, separately
authorized patch, not applied edits.

It does not change Data Capture obligation doctrine, source-access boundary
doctrine, or Source Capture Armory lifecycle doctrine. It applies existing
doctrine to a Reddit success-signal question.

## 2. Source Readiness And Preflight Receipt

`SOURCE_CONTEXT_READY`.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Reddit capture/consolidation success-signal architecture pack
  workspace: C:\Users\vmon7\Desktop\projects\orca
  edit_permission: docs-write for this architecture artifact only
  output_mode: file-write
  target_scope:
    - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md
  source_target_read_only:
    - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  dirty_state_checked: yes
  controlling_source_state: dirty/untracked workspace; advisory planning claims only; no strict readiness/validation claim depends on a clean controlling source
  collision_check: target architecture artifact path absent before write (no collision)
  doctrine_change: no — advisory routing object; the later planning-thread patch is the doctrine-changing step and must carry its own propagation receipt
  blocked_if_missing_satisfied: yes
```

Required source pack read in full: `AGENTS.md`;
`.agents/workflow-overlay/README.md`, `artifact-folders.md`,
`prompt-orchestration.md`; `docs/workflows/data_capture_spine_consolidation_map_v0.md`;
`docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`;
`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`;
`docs/product/data_capture_spine_lane_product_thesis_v0.md`;
`docs/product/source_capture_toolbox/README.md`;
`docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`;
`docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`;
`docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md`;
`docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md`;
`docs/product/data_capture_source_access_boundary_decision_v0.md`;
`docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`;
`docs/product/data_capture_source_access_method_plan_v0.md`; and the target
planning thread.

Conditional `orca-harness/` reads were not loaded and are not load-bearing: this
is a product-method success-signal pass over a planning artifact that itself
defers all implementation, so no finding depends on runner reality.

Method sequence honored: `REFERENCE-LOAD` of `workflow-deep-thinking` and
`workflow-architecture-planning` preceded source loading; `APPLY` followed the
`SOURCE_CONTEXT_READY` declaration.

## 3. Evidence Mode

`delegated_three_subagents`.

Three advisory architecture subagents were launched (directional, adversarial,
grounding), each given the source pack and its own source-readiness gate, each
returning advisory input only. The main planner owns synthesis; subagent
agreement is not proof. No `plain_model_local_fallback` was needed.

Subagent receipts:

- SA-1 Directional: `SOURCE_CONTEXT_READY`; recommended a tiered success ladder
  plus gate verdicts; flagged that two clause bindings need the boundary and
  fixture/retention decisions (which the planner has read).
- SA-2 Adversarial: `SOURCE_CONTEXT_READY`; 13 failure modes, 10 hard gates,
  quote-ready closing clauses; surfaced the largest leak (bounded set laundering
  standing corpus) and the missing contamination stop.
- SA-3 Grounding: `SOURCE_CONTEXT_READY`; concrete field-to-owner mapping; caught
  that the prompt's own proposed bridge list uses non-existent field names and
  must bind to the real owners.

## 4. Subagent Summaries

### Directional (SA-1)

Strongest target: add an explicit, checkable success-signal set anchored by a
mandatory-first Decision-Frame-vs-candidate-intake classification gate, plus a
non-promoting tier ladder (planning / packet / parser / consolidation /
source-quality / batch), plus an Armory Bridge that reuses the existing closed
vocabularies. Accept 11 of the 13 candidate gates, modify 2
(`obligation_visibility_pass`, `lifecycle_sensitivity_pass`) to bind to existing
vocabulary, add `tier_no_silent_promotion_pass`. Recommends a hybrid of Options
B and C inline-patched into the one artifact; rejects A (insufficient), D
(over-built unless inline classification proves leaky), and E (sources
sufficient).

### Adversarial (SA-2)

Largest leaks, each tied to a source rule: (1) a "bounded source set" with no
Decision Frame launders standing/opportunistic corpus capture into
commissioned-only v0 — the single biggest risk; (2) monitored sets without a
mandatory paired stop date enable indefinite monitoring; (3) adaptive expansion
"with a re-named bound" is still source discovery; (4) "dataset / CSV / JSONL"
language drifts into durable storage/queue/scheduler; (5) packet existence or
`mini_god_tier_met` silently promotes to source-quality success or fixture
admission; (6) consolidation rows read as scoring / ECR / validation; (7) parser
`body_text` becomes canonical body at the row level; (8) blanket "login /
paywall / CAPTCHA" stop wording over-blocks in-bound methods and (9)
under-names the real hard stops; (10) the packet-contamination stop is absent
for the highest-contamination-risk source family; (11) commercial transition is
a soft consideration, not a hard stop-and-reroute. Specifies binding hard gates
and quote-ready closing clauses for each.

### Grounding (SA-3)

The consolidation table is already provenance-forward but floats free of the
queue/profile/assembler as named owners and is missing `row_status`,
`result_token`, `packet_lifecycle`, `sensitivity_note`, `retention_basis`,
`allowed_downstream_use`, an `operator_completion_required` flag, a
fixture-admission pointer, and a packet/manifest hash. Reuse the closed
vocabularies verbatim; mint nothing. Correction the synthesis must carry: the
prompt's proposed bridge field `operator_finalization_required` does not exist —
the real owners are the state assembler's `operator_completion_required` and
`result_token_finalization: operator_review_required`. Recommends Option C plus
a one-clause non-promotion statement, expressed through existing owners rather
than a new parallel ladder taxonomy; rejects D and E.

## 5. The Real Architecture Question

Not "how should Orca scrape Reddit." The real question is:

```text
What success-signal structure makes every Reddit capture/consolidation claim
checkable against existing Data Capture and Source Capture Armory authority — so
a future operator can tell, from concrete gates, whether a Reddit unit is
in-bounds, packet-owned, parser-separated, lifecycle-visible,
source-quality-compatible, and planning-only — WITHOUT the success signals
themselves becoming, or licensing by implication, broad crawling, indefinite
monitoring, storage, source discovery, source-quality scoring, fixture
admission, ECR, Cleaning, Judgment, validation, readiness, buyer proof, or
commercial Reddit use; and without forking a parallel vocabulary that competes
with the queue/profile/state-assembler the Armory already owns?
```

The decisive invariant the structure must protect: **a stronger claim is never
satisfied by a weaker one, and a claim is never expressed in a vocabulary the
Armory does not already own.**

## 6. Current Artifact Diagnosis

The Reddit planning thread is a sound architectural planning pass: it has a
Capture Unit Boundary with required fields, a Capture Flow, a Parser Handoff
that correctly keeps the parser derivative, a provenance-first Consolidation
Spine Shape, Implementation Plan stop conditions, and Non-Claims. Its weakness is
not what it says; it is what it leaves checkable only in prose, and three
structural gaps:

1. **No Decision-Frame binding.** It permits "subreddit-bounded, thematic,
   query-based, thread-family scoped, or a small monitored thread set" capture
   units but never states that a Reddit unit is Data Capture Spine work *only
   when bound to an existing Decision Frame*. A bounded source set is not a
   Decision Frame. As written, pre-decision corpus scouting can claim Data
   Capture handoff posture — exactly what the obligation contract routes out of
   v0 to a separate Candidate/Corpus Intake contract. This is the largest gap.

2. **No tiered non-promotion.** It never states that planning success, packet
   success, parser success, consolidation success, source-quality success, and
   batch state are different claims that must not silently promote. The fixture
   decision already says packet success / `mini_god_tier_met` clears nothing
   higher; the Reddit thread's silence lets the promotion happen by implication.

3. **No Armory Bridge.** The Consolidation Spine Shape lists provenance fields
   but does not name the Mini God-Tier profile, source-unit queue, or state
   assembler as the owners of `row_status`, `result_token`, `packet_lifecycle`,
   sensitivity/retention handling, or the census-not-verdict discipline. It also
   omits a packet/manifest hash field the retention rule requires. This invites a
   parallel Reddit vocabulary that forks the Armory.

Secondary defects (prose-level, but checkable-gate-worthy): the
Locked-Owner-Decisions and Implementation-Plan stop wording names blanket
"login / paywalled / CAPTCHA" stops that conflict with the accepted narrow
boundary (free/account-created login and in-browser JS-challenge handling are
in-bounds; only no-entitlement bypass, stolen/nonconsensual access, spillover,
and standalone paid CAPTCHA *services* are stops); it omits several boundary
hard stops including the disclosability stop; it carries no packet-contamination
stop despite the cloaked/authenticated-browser path being the highest
contamination risk; monitored sets lack a mandatory paired stop date; it does
not draw the one-off-table-vs-durable-storage line; and the commercial
transition is a plan-change note rather than a hard stop-and-reroute.

## 7. Options Compared

| Option | What it adds | Verdict | Why |
| --- | --- | --- | --- |
| **A. Success Signals section only** | A gate list. | Rejected | Leaves the row-shape and Decision-Frame ambiguity unfixed; cannot satisfy the no-silent-promotion requirement without the ladder or the bridge. |
| **B. Success Signals + Success/Non-Success Ladder** | Tiered non-promoting states. | Adopted in part | The ladder is needed, but a new standalone six-rung taxonomy with its own labels is itself a fork vector (SA-3). Adopt the ladder, express each tier through its existing owner. |
| **C. Success Signals + Armory Bridge** | Field-to-owner mapping; reuse closed vocabularies. | Adopted | Closes the actual fork risk where it lives — the Consolidation Spine Shape. |
| **D. Split into two artifacts** | Separate Decision-Frame-bound and candidate/scouting artifacts. | Rejected as default; retained as contingency | Heavier; justified only if inline classification proves leaky. The split is fully expressible inline as a mandatory-first classification gate plus a per-unit status field. If a later review shows inline classification does not hold, D is the fallback. |
| **E. No patch** | — | Rejected | Source context is sufficient; the open items are clause-wording bindings and policy knobs already owner-decided elsewhere, not unresolved doctrine. |

## 8. Recommended Architecture Result

`TARGET_RECOMMENDED`.

**Target architecture: a hybrid of Options B and C, inline-patched into the
single Reddit planning thread — a Success Signals gate set, a non-promoting tier
ladder expressed through existing vocabulary owners, and an Armory Bridge —
with Option D (artifact split) retained only as a named contingency if a later
review shows inline Decision-Frame classification is leaky.**

Selection threshold (architecture-planning): met. The stable invariant is clear
(no stronger claim from a weaker one; no vocabulary the Armory does not own); the
core/satellite split is clear (success signals + bridge are core to this
artifact; the candidate-intake destination contract and runtime are satellite or
separate); non-goals are known (no storage, scoring, fixture admission, ECR,
Cleaning, Judgment, commercial use); and no unresolved upstream blocker changes
the target — the method order, backend selection, boundary, hard stops,
lifecycle, retention, sensitivity, and commercial trigger are all already
owner-decided in the loaded sources. The open owner questions in Section 14 set
*policy knobs the patch will encode* (keep monitored sets? keep `.json`? where
does a candidate unit hand off?); they do not change which architecture is
selectable.

Core invariants the later patch must preserve:

- The Source Capture Packet is the canonical source body and provenance owner;
  parser output is derivative and never canonical.
- Data Capture Spine v0 is commissioned-capture-only; only a Decision-Frame-bound
  unit may claim Data Capture handoff posture.
- Result tokens, packet lifecycle states, and row-status come only from their
  existing closed owners; no Reddit-local vocabulary.
- Every success claim names its tier and what it does not clear.
- Anti-blocking is a pre-commercial bridge under owner-accepted risk; commercial
  pressure halts it and reroutes to the sanctioned API/licensing path.

## 9. Recommended Success-Signal Structure

Add a `## Success Signals` section to the planning thread expressing the
following as concrete, checkable gates. Each gate is answerable as pass / fail /
visible-stop, and obligation-bearing items are discharged with one of the nine
existing discharge states (`met`, `partial`, `assessed_not_met`,
`cannot_assess`, `access_failed`, `blocked`, `unavailable_by_source`,
`not_applicable`, `not_attempted`) — never silently omitted.

The 13 candidate gates are accepted, with two bound to existing vocabulary and
three gates added. Gate G1 is mandatory-first.

| Gate | Disposition | Checkable requirement |
| --- | --- | --- |
| G1 `decision_frame_or_candidate_intake_classified` | Accept — mandatory-first | Each unit is `decision_frame_bound` (may claim Data Capture handoff posture) or `candidate_or_scouting` (pre-decision; must not claim Data Capture handoff, source-quality completeness, fixture admission, or ECR readiness). A bounded source set is explicitly not a Decision Frame. |
| G2 `bounded_source_set_pass` | Accept (tightened) | Named source set + purpose + exclusions + time cutoff + volume ceiling; for any monitored set, both `monitoring_cadence` and a hard `stop_date` are required, not optional. No stop date → fail. |
| G3 `method_order_observed` | Accept | Exact old Reddit Direct HTTP first for supplied thread URLs when current old Reddit HTML is the capture target and the bounded batch runner accepts the URL; CloakBrowser anti-blocking when Direct HTTP is unsuitable, blocked, or browser-visible anti-blocking capture is explicitly needed; old Reddit HTML where available; archive fallback; `.json` warm same-context enrichment only; commercial/API route after the commercial trigger. |
| G4 `method_provenance_recorded` | Accept | Capture method, source surface, backend, access posture, anti-blocking/JS-challenge category if used, fallback posture, packet path, raw file pointer, and limitations visible. |
| G5 `disclosability_pass` | Accept (bind wording to boundary) | Orca can disclose exactly how the source was obtained; none of the boundary hard stops occurred (see G12 wording). |
| G6 `packet_before_parser_pass` | Accept | Raw/body-equivalent preserved in a Source Capture Packet before any parser/consolidation output is trusted. |
| G7 `parser_derivative_pass` | Accept (row-level marker) | Parser output points back to the packet, carries warnings, is row-marked derivative, and never becomes canonical body. |
| G8 `obligation_visibility_pass` | Accept (bind to discharge vocabulary) | Contract version, operator/session provenance, mode/mode-changes, timing/cutoff, archive/access/visibility, recapture, and limitations each carry one of the nine discharge states or `unknown_with_reason`; recapture relationship uses the closed set `supersede`/`supplement`/`conflict`/`mixed`; cutoff and archive posture use their closed write-time-enforced sets. No parallel obligation vocabulary. |
| G9 `related_thread_context_pass` | Accept | Thread slice preserves parent/reply/correction/rebuttal/confirmation/moderator/official/lock/edit/delete/exclusion context enough for the ECR reconstruction floor and the fairness ceiling. |
| G10 `lifecycle_sensitivity_pass` | Accept (bind + mandatory note) | `packet_lifecycle` from the closed set defaulting to `scratch`; `sensitivity_note` is mandatory for Reddit rows (personal handles, user-authored posts, screenshots, raw third-party bodies); `retention_basis` and `allowed_downstream_use` visible; fixture-admission state cited or `none`. |
| G11 `source_quality_compatibility_pass` | Accept (name owner + precondition) | A row may claim source-quality only via a Mini God-Tier `result_token` (closed set), only after an operator-commissioned source-quality pass, and only with `operator_completion_required` honored. No source-quality scoring. |
| G12 `planning_only_pass` | Accept | No database, durable corpus, exported reusable dataset, queue, scheduler, dashboard, production monitor, fixture admission, ECR, Cleaning, Judgment, or client-facing role without separate authorization. |
| G13 `commercial_transition_check` | Accept (hard stop-and-reroute) | Client-funded, commercial, enterprise, buyer-facing durable use, scale pressure beyond low-volume bounded, or data-licensing pressure halts anti-blocking Reddit capture for that source and reroutes to the sanctioned commercial/enterprise API or data-licensing path. |
| G14 `tier_no_silent_promotion_pass` | **Add** (SA-1) | Each claim names its tier and that tier's non-claim; no tier is satisfied by a lower tier. |
| G15 `no_source_discovery_expansion` | **Add** (SA-2) | Capture must not follow links, users, comments, recommendations, or related/"more like this" surfaces to discover new units; re-bounding a hop does not make it in-bounds; new units are separately commissioned. |
| G16 `no_secret_bearing_packet` | **Add** (SA-2, contamination stop) | The packet never preserves credentials, cookies, raw browser-profile material, storage-state JSON, session sidecars, authorization headers, or secrets; if any appears, stop and treat the packet as contaminated scratch. Named on every Reddit unit. |

### Non-promoting tier ladder (Option B, expressed through existing owners)

Add a short `## Success / Non-Success Ladder` clause. Each tier is owned by an
existing surface; clearing a lower tier never clears a higher one:

| Tier | Claim | Owned/evidenced by (existing surface) | Does NOT clear |
| --- | --- | --- | --- |
| Planning | Unit is in-bounds to scope | G1–G2 + queue `row_status` (`planned`/`ready_for_tool_run`/`blocked_missing_input`) | Capture, packet, readiness |
| Packet | Packet exists and owns the body | packet path + manifest hash; obligations discharged (G6, G8) | Body-possession quality, parser, source-quality |
| Parser | Extraction ran, derivative | `parser_name_version` + `parse_warning`, row-marked derivative (G7) | That extraction is the body or is meaning-bearing |
| Consolidation | Rows assembled, pointing to packets | the planning/state table (G12) | Storage, ECR, dedupe, any cross-row verdict |
| Source-quality | Row meets Mini God-Tier | profile `result_token` after operator pass (G11) | Validation, fixture admission, credibility, Judgment |
| Batch | Multi-row state view | state-assembler **census, not verdict** | "all rows passed", rollup, ladder-complete, admission |

## 10. Exact Patch Clauses To Apply To The Reddit Planning Thread

Recommended drop-in clauses for a later, separately authorized patch of
`reddit_precommercial_capture_consolidation_planning_thread_v0.md`. These are
recommendations, not applied edits, and not patch authority.

**PC-1 — Decision-Frame binding (new clause; add `capture_unit_intake_status` to
the Capture Unit Boundary required fields):**
> "A Reddit capture unit is Data Capture Spine work only when bound to a specific,
> pre-existing Decision Frame. A bounded source set — subreddit, theme, query,
> thread family, or small monitored thread set — is not a Decision Frame and does
> not by itself satisfy the Data Capture Commissioning Gate. Each unit is
> classified `decision_frame_bound` (may claim Data Capture handoff posture) or
> `candidate_or_scouting` (pre-decision context; must not claim Data Capture
> handoff, source-quality completeness, fixture admission, or ECR readiness).
> Candidate/scouting units are corpus-intake context and must be rebound or
> recaptured under a Decision Frame before entering Data Capture Spine."

**PC-2 — Monitored cadence + stop date (tighten Capture Unit Boundary):**
> "Any monitored thread set must record both a named `monitoring_cadence` and a
> hard `stop_date`. A monitored unit without a stop date fails the capture-unit
> boundary gate. No monitored Reddit unit runs indefinitely."

**PC-3 — No discovery expansion (tighten Forbidden capture-unit shapes):**
> "Capture must not follow links, users, comments, recommendations, related, or
> 'more like this' surfaces to discover additional source units. Re-bounding a
> followed hop does not convert it into in-bounds commissioned capture; new units
> are separately commissioned, never continuations. Link/user/recommendation-
> driven expansion is source discovery and is out of bounds."

**PC-4 — One-off table vs durable storage line (new clause):**
> "The default consolidation artifact is a non-durable, in-place, locally-read
> planning/state table pointing back to packets and raw preserved files. It is
> not a database, durable corpus, reusable exported dataset, queue, scheduler,
> dashboard, or production monitor. Emitting a durable CSV/JSONL, persisting a
> corpus, or standing up any store/queue/scheduler/dashboard requires a separate,
> cited owner authorization. 'Dataset' never by itself authorizes durable
> storage."

**PC-5 — Tiered non-promotion (new clause):**
> "Reddit capture success is tiered and non-promoting: planning ≠ packet ≠ parser
> ≠ consolidation ≠ source-quality ≠ batch ≠ fixture admission ≠ ECR/Cleaning/
> Judgment. A preserved packet body, exit code 0, a screenshot, or
> `mini_god_tier_met` clears none of the higher tiers. A consolidation row is a
> planning/state row only — not a source-quality score, not semantic dedupe/
> clustering, not an ECR record, not validation, not readiness, not fixture
> admission, not buyer proof. No tier may be claimed by implication."

**PC-6 — Canonical body marker (tighten Consolidation Spine Shape):**
> "In every consolidation row, the packet `raw_html_file_id` is the canonical
> source body; `body_text` is parser-derivative only, row-marked derivative, and
> carries a live pointer to `raw_packet_path` and `raw_html_file_id`. A row
> without a resolvable packet pointer must not present `body_text` as the source
> body."

**PC-7 — Boundary-accurate stop wording (replace blanket login/paywall/CAPTCHA
wording in Locked Owner Decisions and Implementation Plan stop conditions):**
> "In-bounds and not stop conditions: free or account-created login; entitled
> paid, client, or consenting-coworker access; anti-detect/cloaked browser
> configuration; user-agent/fingerprint configuration; residential or rotating
> proxies; and in-browser JS-challenge handling. Hard stops (out of bounds):
> no-entitlement gate bypass; stolen or nonconsensual credentials, cookies, or
> sessions; security exploits; malware; credential stuffing; obvious cross-
> account/private/admin spillover once noticed; private or confidential account
> areas without consent; standalone CAPTCHA-solving services (paid solvers), as
> distinct from in-browser JS-challenge handling; and any method Orca would
> refuse to disclose internally. 'Login', 'paywall', and 'CAPTCHA' are not
> blanket stop labels; only the enumerated hard stops apply."

**PC-8 — Contamination stop (new clause, named on every Reddit unit):**
> "The Source Capture Packet must never preserve credentials, cookies, raw
> browser-profile material, Playwright/storage-state JSON, session sidecars,
> authorization headers, or secrets. Because Reddit capture commonly runs through
> a cloaked or authenticated browser, this stop is named on every Reddit unit. If
> such material appears, stop and treat the packet as contaminated scratch until
> a separate owner decision says how to dispose, redact, or isolate it. A
> contaminated packet clears nothing."

**PC-9 — Commercial stop-and-reroute (promote the existing commercial note to a
gate):**
> "Commercial/enterprise/client-funded status, buyer-facing durable use, scale
> pressure beyond low-volume bounded capture, or data-licensing pressure is a
> hard stop-and-reroute. On any such trigger, halt anti-blocking Reddit capture
> for that source and move it to the sanctioned commercial/enterprise Reddit API
> or data-licensing path before any further capture. The owner-accepted
> ToS/reputational/litigation risk posture for anti-blocking applies only to the
> pre-commercial/free phase."

**PC-10 — Fallback ceilings + posture (tighten `.json` and archive steps):**
> "`.json` and archive captures inherit the same volume/cadence ceiling and
> disclosability requirements as the primary route. Observing `.json` work in one
> bounded run does not promote it to a standing method; record its access posture
> against the disclosability gate each time. Archive captures record
> archive/history posture per relevant source slice per Obligation 10."

**PC-11 — Armory Bridge fields (extend the Consolidation Spine Shape table; see
Section 11 for exact owners):** add `row_status`, `result_token`,
`packet_lifecycle`, `sensitivity_note`, `retention_basis`,
`allowed_downstream_use`, `operator_completion_required`,
`separate_fixture_admission_decision_or_none`, a packet/manifest `hash` field,
and rename the table's `limitations` to `visible_limitations`.

## 11. Armory Bridge — Vocabulary To Reuse And To Avoid

Add a `## Armory Bridge` subsection stating that the profile, queue, and state
assembler are the named vocabulary owners and that the Reddit thread defines no
parallel row-status, result-token, or lifecycle vocabulary.

### Reuse verbatim (closed sets — owners in parentheses)

- **Row-status** (source-unit queue template): `planned`, `ready_for_tool_run`,
  `blocked_missing_input`, `packet_written_needs_report`, `reported`.
- **Result tokens** (Mini God-Tier profile): `mini_god_tier_met`,
  `mini_god_tier_with_visible_limitations`, `current_body_standardized_only`,
  `archive_body_not_preserved`, `body_possession_not_proven`,
  `needs_separate_fixture_admission_decision`, `visible_stop`.
- **Packet lifecycle** (Mini God-Tier profile; retention-governed by the fixture/
  retention/sensitivity decision): `scratch`, `candidate_evidence`,
  `recommended_fixture_admission`, `separately_admitted` — `scratch` is the
  default; `recommended_fixture_admission` is a recommendation only, never
  admission; `separately_admitted` requires a cited decision.
- **Finalization/census** (state assembler): `suggested_result_token` vs
  `result_token_finalization: operator_review_required`,
  `operator_completion_required`, and "state census" (not verdict/rollup).
- **Retention/sensitivity** (fixture/retention/sensitivity decision):
  `sensitivity_note`, `retention_basis`, `allowed_downstream_use`,
  packet/manifest hash, "contaminated scratch", "durable closeout".
- **Recapture / cutoff / archive posture** (obligation contract, closed write-
  time-enforced facts): recapture `supersede`/`supplement`/`conflict`/`mixed`;
  cutoff `pre_cutoff`/`post_cutoff`/`mixed`/`unknown`; archive `archived`/
  `attempt_failed` with status-carried `not_attempted`/`not_applicable`.

### Field-to-owner mapping (Consolidation Spine Shape → existing owner)

- `capture_unit_id` → bridges to queue `case_or_slot` as the bounded-context
  anchor (Reddit-family analogue, not a parallel ID system).
- `access_posture` / `capture_method` / `surface` / `capture_time` /
  `source_time_visible` → Mini God-Tier "identity and provenance" criterion;
  reuse the profile's `access_status` field name in packet/report.
- `raw_packet_path` / `raw_html_file_id` → packet path + the required
  packet/manifest hash (retention rule); `raw_html_file_id` is canonical body.
- `limitations` → rename to `visible_limitations` (profile criterion).
- add `row_status` (queue), `result_token` (profile, empty pre-run), and
  `packet_lifecycle` (profile, default `scratch`) — the three most important
  missing bridge fields.
- add `sensitivity_note` / `retention_basis` / `allowed_downstream_use` (fixture
  decision), `operator_completion_required` (state assembler), and
  `separate_fixture_admission_decision_or_none` (default `none`).

### Avoid (would fork the Armory)

- Any new result token, lifecycle state, or row-status token (e.g.
  `reddit_captured`, `consolidated`, `done`).
- `operator_finalization_required` as a new field name — the prompt's own
  proposed bridge list uses it, but it does not exist; reuse the state
  assembler's `operator_completion_required` / `result_token_finalization`.
- "score" / "scored" / "ranking" applied to a Reddit row (the post's own
  `visible_score` is fine; a row-level quality score is forbidden).
- "validated" / "ready" / "admitted" / "complete" / "passed" applied to a row,
  batch, or consolidation (`recommended_fixture_admission` ≠ admitted; census ≠
  "all rows passed").
- "corpus" / "database" / "store" / "index" / "monitor" / "pipeline" /
  "dashboard" as standing nouns; "conductor" / "scorer" / "dispatcher" / "gate
  sequencer" for any Reddit assembler (inherit state-assembler "read-only
  census/router").
- Blanket "login" / "paywall" / "CAPTCHA" stop labels (narrow to the actual hard
  stops); ECR / Cleaning / Judgment / buyer proof / fixture admission as anything
  this artifact produces.

## 12. Open Owner Questions

1. **Does any current Reddit unit have a real Decision Frame?** If, in the
   pre-commercial personal-project phase, no Reddit unit is yet bound to a
   Decision Frame, then every current Reddit capture is candidate/scouting and is
   out of Data Capture Spine v0 by definition. The success signals can classify
   it, but the owner should confirm whether any unit can currently claim
   `decision_frame_bound`.

2. **Where does a `candidate_or_scouting` unit hand off?** The obligation
   contract routes standing/opportunistic capture to a separate Candidate Signal
   Intake / Corpus Intake contract that does not yet exist in the loaded sources.
   Until it exists, a candidate unit has nowhere compliant to hand off to — only
   "hold as planning-only / recapture under a future Decision Frame." Confirm
   whether to build that destination contract or keep candidate units
   planning-only.

3. **Inline classification (B+C) or artifact split (D)?** The recommendation is
   inline, contingent on G1 being binding and visible. If the owner judges the
   standing-corpus risk too large to patch inline, choose D.

4. **Keep monitored thread sets pre-commercial at all?** Monitoring is the
   highest-drift shape. The owner may prefer to defer monitored sets entirely
   until a Decision Frame and stop-date discipline exist, rather than gate them.

5. **Keep `.json` as a named fallback?** Given current 403/OAuth reality, the
   adversarial lean is to drop `.json` from the planned method order and keep it
   only as recorded-if-spontaneously-observed. Owner decides whether to retain it
   as a named fallback.

6. **Restate the full boundary hard-stop set verbatim?** The thread currently
   names only a subset and omits the disclosability stop. Confirm the full set
   (including "any method Orca would refuse to disclose internally" and
   spillover-once-noticed) should be restated in the Reddit thread.

## 13. Deferred Implementation Implications

Preserved as non-executable notes; none is authorized here.

- The CloakBrowser adapter, parser, runner, and any `.json`/archive path remain
  separately scoped by the source-access tooling build authorization; this pass
  changes none of them.
- A future Candidate Signal Intake / Corpus Intake contract (Open Question 2) is
  the natural home for `candidate_or_scouting` Reddit units; it is upstream of
  this artifact and not designed here.
- If durable consolidation output (CSV/JSONL, store, queue, scheduler, dashboard)
  is later wanted, it needs its own owner authorization with retention and
  sensitivity handling — out of scope here.
- A future source-quality pass over Reddit rows would run through the existing
  Mini God-Tier profile, queue, and state assembler; this pass only makes the
  Reddit rows compatible with them, it does not run them.

## 14. Non-Claims

This architecture routing object is not validation, readiness, source
completeness proof, fixture admission, source-quality scoring, legal
sufficiency, rights clearance, implementation execution, live Reddit capture
authorization, CloakBrowser installation proof, parser correctness proof,
storage/queue/scheduler/dashboard/deployment/production-runtime authorization,
broad-crawling authorization, commercial Reddit authorization, ECR design,
Cleaning design, Judgment design, buyer proof, or patch authority for the Reddit
planning thread. It does not amend Data Capture obligation doctrine,
source-access boundary doctrine, or Armory lifecycle doctrine. It does not
authorize commits, pushes, or PRs.

The recommended clauses become doctrine only if and when the owner authorizes a
patch of the Reddit planning thread; that patch is the doctrine-changing step and
must carry its own direction-change propagation receipt.

## 15. Smallest Complete Next Authorized Step

Owner review of this routing object and, if accepted, a separately authorized
**patch of the Reddit planning thread** applying PC-1 through PC-11 and the
Armory Bridge (Sections 10–11) under explicit docs-write patch authority for
`reddit_precommercial_capture_consolidation_planning_thread_v0.md` — answering
Open Questions 1–6 first, because they set the policy knobs the patch encodes.
That patch, not this artifact, carries the direction-change propagation receipt.

No implementation, runtime, live Reddit, storage, ECR, Cleaning, Judgment,
fixture-admission, source-quality-scoring, or commercial work is performed or
authorized by this pass.
