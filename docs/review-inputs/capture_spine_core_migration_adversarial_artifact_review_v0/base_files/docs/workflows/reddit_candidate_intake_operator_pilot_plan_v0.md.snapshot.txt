# Reddit Candidate Intake Operator Pilot Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow plan
scope: >
  Defines the layer above the no-live foundation for bounded Reddit Candidate
  URL Intake: a single operator pilot / bounded-run layer with explicit gates.
use_when:
  - Deciding what comes after the no-live dry-use foundation for Reddit Candidate URL Intake.
  - Preparing a bounded operator pilot without turning Candidate URL Intake into live capture, broad crawling, Armory execution, or Data Capture handoff.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/reddit_candidate_intake_no_live_dry_use_receipt_v0.md
  - docs/workflows/reddit_candidate_intake_operator_pilot_parameter_packet_v0.md
  - orca/product/spines/capture/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - orca/product/spines/capture/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
stale_if:
  - The no-live dry-use receipt is superseded.
  - The parent Candidate URL Intake contract changes run envelope, output, stop, cap, traversal, or promotion rules.
  - The Reddit Candidate URL Intake architecture/default policy changes old Reddit, .json, live access, candidate surfaces, or promotion gates.
```

## Status

Status: `OPERATOR_PILOT_LAYER_RECOMMENDED`.

This plan is the layer above foundation. It does not authorize live Reddit
access, CloakBrowser/proxy invocation, Source Capture Armory execution, Source
Capture Packet output, broad crawling, automatic promotion, Data Capture
handoff, ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or
commercial use.

## Layer Definition

The layer above foundation is the **operator pilot / bounded-run layer**.

Foundation proves the local lane can hold its own boundaries. The operator
pilot proves the lane can be used for one real operator decision:

```text
Given a declared topic/query and bounded old Reddit source surface, can Candidate
URL Intake produce planning-only candidate thread URL rows plus provenance,
with a visible stop reason and no forbidden capture behavior?
```

This layer is still not Source Capture Armory and not Data Capture. It ends at
candidate rows, run provenance, and an operator decision about whether any
candidate should later enter a separate promotion gate.

## Cynefin Routing

Smallest complete outcome: define one bounded pilot envelope and acceptance
gate so the next execution can test operator usefulness without widening scope.

Regime: complicated with a live-access edge.

Why: the local foundation and governing contracts exist, but live source access
adds source-access and anti-blocking variables that should not enter by
implication.

Decomposition: layer-based. Keep foundation, bounded-run pilot, promotion, and
downstream Armory capture separate.

Current bottleneck: choosing one pilot envelope and success gate before any
operator run creates candidate rows that could be overclaimed.

Riskiest assumption: a bounded old Reddit run can be useful without treating
`caps_reached` as coverage, following related surfaces, or promoting candidates
automatically.

Stop or pivot condition: if the pilot needs live fetch, proxy/CloakBrowser
execution, newly discovered subreddit traversal, outbound fetch, body/comment
capture, user/profile capture, or source-quality ranking to count as success,
the plan is trying to leave Candidate URL Intake and must be rerouted.

Allowed next move: run or scope one bounded pilot under this plan.

Disallowed next move: broad crawl, Reddit `.json` intake, Source Capture Packet
generation, Armory runner dispatch, Data Capture handoff, or live access by
implication.

## Pilot Envelope

Default pilot mode: `pilot_no_live_operator_supplied_html`.

This mode uses an operator-supplied old Reddit HTML listing/search page as
input. The operator may save the page outside Candidate URL Intake and pass the
HTML text into the existing static projection helper. Candidate URL Intake must
not fetch Reddit itself in this default pilot.

Required pilot envelope:

```yaml
run_id: reddit_candidate_pilot_001
run_purpose: bounded operator pilot for Candidate URL Intake
cap_type: probe
coverage_claim: bounded_probe_only
declared_topic_theme_query: <operator declares before run>
seed_subreddits: [] # optional; operator may supply 1-5
source_surface: reddit_search_listing | subreddit_listing
candidate_surface_allowlist:
  - reddit_search_listing | subreddit_listing
max_subreddits: 5
max_threads_per_subreddit: 25
max_pages_or_result_surfaces: 2
time_window_days: 30
sort_order: top | new | hot | rising | controversial
method_category: static_old_reddit_html_operator_supplied
stop_condition: caps_reached | scope_exhausted | empty_result | blocked_result | operator_stop
exclusions: []
non_commercial_posture: pre_commercial
```

The pilot may choose lower caps. It must not exceed the `probe` defaults without
a new scope amendment or later owner decision.

## Inputs

Required before pilot execution:

- declared topic/theme/query;
- optional seed subreddits;
- one old Reddit listing/search source URL used as provenance;
- saved old Reddit HTML text supplied by the operator or fixture path;
- selected sort order;
- selected time window;
- explicit exclusions, even when empty;
- declared stop condition expectation;
- non-commercial posture.

Optional but useful:

- reason this topic/query matters to the next planning decision;
- what would make the operator promote one candidate later;
- known limitations of the saved HTML input, such as stale page, manual save,
  partial page, or visible block.

## Outputs

Allowed pilot outputs:

- candidate thread URL rows;
- optional candidate subreddit rows only if produced by a declared candidate
  surface in a later scoped pilot;
- run-level provenance receipt;
- local JSON/Markdown output written by the Candidate URL Intake writer;
- pilot closeout note summarizing row counts, stop reason, and non-claims.

Explicit non-outputs:

- raw HTML;
- parser output;
- thread bodies;
- comments;
- user names, authors, profiles, or ordinary-person data;
- outbound source bodies or summaries;
- Source Capture Packets;
- promotion receipts unless separately authorized;
- Data Capture handoff;
- ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or
  commercial-use claims.

## Acceptance Gate

The pilot is acceptable only if all of these are true:

- the run envelope is fully declared before execution;
- output contains candidate rows and provenance only;
- every candidate row remains `candidate_or_scouting`;
- every candidate row has `allowed_downstream_use = planning_only`;
- every candidate row has `same_run_traversal_authorized = false`;
- every run records a visible stop reason;
- `caps_reached` is not described as completion, sufficiency, or topic
  coverage;
- `.json` inputs remain refused;
- old Reddit thread pages remain candidate outputs, not intake inputs;
- raw HTML, parser output, body/comment text, user/profile/author data,
  outbound URL content, secrets, session state, and screenshots are absent from
  output artifacts;
- output non-claims include no live Reddit access, no Source Capture Packet,
  no Source Capture Armory execution, no auto-promotion, and no Data Capture
  handoff;
- empty-result and blocked-result remain valid outcomes if encountered.

## Live-Access Variant

A later live-access pilot may be scoped only after an explicit bounded
authorization names live old Reddit access as in scope.

If authorized, the live-access variant must still use the same run envelope and
acceptance gate. It additionally must bind:

- the current source-access tooling authorization;
- already-approved CloakBrowser/proxy posture;
- secrets and session-state boundary;
- no raw HTML persistence rule;
- no body/comment/profile capture rule;
- live-access validation evidence;
- stop conditions for block, empty result, commercial reroute, and hard stop.

This plan does not invoke that variant.

## Pilot Closeout Shape

A pilot closeout should record:

```yaml
pilot_closeout:
  run_id:
  mode: pilot_no_live_operator_supplied_html | live_old_reddit_authorized
  declared_topic_theme_query:
  seed_subreddits:
  source_surface:
  source_url:
  cap_type:
  coverage_claim:
  caps_applied:
  sort_order:
  time_window_days:
  exclusions:
  method_category:
  row_counts:
    candidate_subreddits:
    candidate_threads:
    outbound_urls:
  stop_reason:
  output_artifacts:
    json_path:
    receipt_path:
  forbidden_output_checks:
    raw_html_absent:
    body_comment_absent:
    user_profile_absent:
    source_capture_packet_absent:
    data_capture_handoff_absent:
  operator_decision:
    promote_candidate_now: yes | no | deferred
    reason:
  non_claims:
    - not live Reddit access unless live variant explicitly authorized
    - not broad crawling
    - not Source Capture Packet output
    - not Data Capture handoff
```

The operator decision is a planning decision only. If the operator wants to
promote a candidate, a separate promotion gate must be opened.

## Next Authorized Step

Next authorized step: complete
`docs/workflows/reddit_candidate_intake_operator_pilot_parameter_packet_v0.md`
for `pilot_no_live_operator_supplied_html`.

Minimum parameters:

1. `declared_topic_theme_query`;
2. `source_surface`: `reddit_search_listing` or `subreddit_listing`;
3. old Reddit source URL used for provenance;
4. saved/static HTML input path or operator-supplied HTML text;
5. cap values if lower than the default `probe` caps;
6. stop condition to record if no candidates are emitted.

After those are supplied, implementation may run the no-live pilot through the
existing Candidate URL Intake package and write the pilot closeout. Live
old.reddit/CloakBrowser/proxy execution remains separately gated.

## Non-Claims

This plan is not validation, readiness, source-access boundary amendment,
implementation execution, live Reddit authorization, CloakBrowser/proxy
authorization, Source Capture Armory authorization, Source Capture Packet
generation, Data Capture handoff, ECR, Cleaning, Judgment, source-quality
scoring, fixture admission, commercial-use permission, deployment, production
runtime, commit authorization, push authorization, or PR authorization.
