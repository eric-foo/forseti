# Reddit Candidate Intake Old Reddit Search Surface Handling v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handling note
scope: >
  Records practical handling rules for old Reddit search/listing HTML in
  bounded Reddit Candidate URL Intake, including the `search-title` surface
  discovered during the first operator-supplied pilot.
use_when:
  - Running no-live Reddit Candidate URL Intake from operator-supplied old
    Reddit HTML.
  - Interpreting empty results from old Reddit search/listing pages.
  - Scoping a follow-on candidate-subreddit discovery run from related,
    recommended, correlated, cross-post, or "more like this" surfaces.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/reddit_candidate_intake_operator_pilot_001_executed_closeout_v0.md
  - docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md
  - docs/workflows/reddit_candidate_intake_subreddit_projection_b2b_001_closeout_v0.md
  - docs/workflows/reddit_candidate_intake_subreddit_projection_seo_002_closeout_v0.md
  - docs/workflows/reddit_candidate_intake_operator_pilot_parameter_packet_v0.md
  - docs/product/data_capture_spine/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/product/data_capture_spine/data_capture_spine_candidate_url_intake_contract_v0.md
stale_if:
  - old Reddit search/listing HTML changes title-link classes.
  - Candidate URL Intake changes candidate row fields, cap semantics, or
    declared candidate surfaces.
  - A later implementation adds explicit candidate-subreddit volume fields.
```

## Status

Status: `ACTIVE_HANDLING_NOTE`.

This note is not a new architecture contract. It is a lane-side operating note
for future agents so they do not re-learn the same old Reddit search-surface
lesson.

## Access Lesson

The first real pilot did not prove that a Codex agent can freely access Reddit.
The operator accessed old Reddit in a browser and saved static HTML into the
workspace. Candidate URL Intake then consumed that local file.

That distinction is load-bearing:

- operator browser access happened outside Candidate URL Intake;
- Candidate URL Intake did not fetch Reddit;
- Candidate URL Intake did not invoke CloakBrowser/proxy;
- Candidate URL Intake did not call Reddit `.json`;
- Candidate URL Intake did not read a thread page as input.

If a future run fetches live old Reddit through CloakBrowser/proxy, it is a
separate live-access pilot, not this no-live operator-supplied HTML mode.

## Raw HTML Input Hygiene

Operator-supplied old Reddit HTML is an input, not a durable Capture Spine
output. It can contain more than visible listing links, including:

- logged-in account chrome;
- hidden page configuration;
- session-like fields;
- message or preference indicators;
- expanded snippets or body-like text from search results.

Candidate URL Intake must not persist any of that material into candidate output
or receipts. Future operators should prefer a logged-out or private-window old
Reddit save when possible. If a logged-in save is used, treat the raw HTML as
scratch input only: do not promote it, do not commit it, and do not treat it as
a source packet, fixture, corpus artifact, or Data Capture input.

## Old Reddit Search Title Rule

Old Reddit search pages can expose result links with:

```html
<a class="search-title may-blank" href="https://old.reddit.com/r/.../comments/.../">
```

Old Reddit subreddit listing pages can expose result links with:

```html
<a class="title may-blank" href="/r/.../comments/.../">
```

Candidate URL Intake should treat both `title` and `search-title` anchors as
candidate thread title anchors.

Candidate URL Intake should not treat these as candidate title anchors:

- `search-comments`;
- `comments`;
- thumbnail links;
- author/profile links;
- outbound links unless the outbound surface is explicitly declared and capped.

Reason: comment links and thumbnail links can point at the same thread, but
they are not the visible title signal. Accepting them would inflate or duplicate
candidate rows and make provenance weaker.

## Empty Result Discipline

An empty result is valid only after a surface-shape sanity check.

Before accepting `empty_result` from an old Reddit search/listing HTML input,
check whether the saved HTML contains any of:

- `/comments/`;
- `class="search-title`;
- `class="title`;
- `old.reddit.com/r/<subreddit>/comments/`;
- `/r/<subreddit>/comments/`.

If these markers exist but zero rows are emitted, treat the result as a parser
surface mismatch until proven otherwise. Do not record a final empty-result
pilot without noting the mismatch.

If the saved HTML lacks those markers or visibly contains a block/empty page,
`empty_result` or `blocked_result` may be the correct terminal outcome.

## Candidate Thread Intake Success Signal

For a thread-candidate pilot, success means:

- declared topic/subreddit/query before execution;
- old Reddit listing/search source URL used as provenance;
- saved/static HTML file supplied by the operator;
- candidate thread URL rows plus provenance only;
- visible stop reason;
- hard caps and `coverage_claim`;
- no raw HTML, parser output, body text, comments, user/profile/author data,
  Source Capture Packet, Source Capture Armory execution, Data Capture handoff,
  ECR, Cleaning, Judgment, fixture admission, source-quality score, or
  promotion claim.

`caps_reached` is a success signal for bounded extraction, not a coverage or
sufficiency claim.

## Candidate Subreddit Discovery Success Signal

The first `r/b2bmarketing` pilot satisfied candidate thread extraction. It did
not satisfy candidate subreddit discovery.

Finding recommended, correlated, or "most similar" B2B subreddits with visible
volume is a separate success signal and needs its own declared run or explicit
scope amendment.

Owner decision: `r/b2bmarketing` is acceptable as the seed candidate subreddit
for the follow-on discovery run. Candidate subreddit rows are the right output
shape. Visible subscriber count and visible active-user or online-user count are
acceptable volume/activity fields when the declared surface shows them.

The first pilot output had:

- `candidate_subreddits: 0`;
- `candidate_threads: 25`;
- `outbound_urls: 0`.

The saved source HTML contained subreddit links, but those links were not
accepted as candidate subreddit output because they came from navigation,
subscription, popular-subreddit, or page chrome surfaces rather than a declared
recommended/correlated subreddit surface. Do not reinterpret those links as B2B
recommendations after the fact.

Allowed shape:

```yaml
candidate_subreddit_discovery:
  source_surface:
    - related_subreddit
    - recommendation
    - more_like_this
    - cross_post
    - reddit_search_listing
  required_before_run:
    - declared_topic_theme_query
    - seed_subreddits
    - max_candidate_subreddits
    - max_pages_or_result_surfaces
    - time_window_or_listing_window_if_applicable
    - sort_or_surface_order_if_applicable
    - exclusions
    - cap_type
    - coverage_claim
  allowed_output:
    - candidate_subreddit_rows
    - visible_volume_or_activity_label_if_present_on_listing
    - method_provenance
    - stop_reason
```

The output may record visible volume or activity only when it is present on the
declared surface. Do not infer volume from memory, hidden metadata, unrelated
pages, search result order, or thread counts unless the run contract explicitly
defines that proxy.

Old Reddit subreddit sidebars can expose hand-authored subreddit links inside
the sidebar markdown/titlebox area rather than Reddit's own recommendation or
cross-post containers. These may be treated as `related_subreddit` candidates
only when the run declares that sidebar markdown surface, applies caps, and
excludes header navigation, popular bars, search forms, moderator-contact links,
the current subreddit self-link, footer links, and other page chrome.

This structural projection is not semantic filtering. If only one sidebar link
looks directly relevant to the operator's B2B theme, record that as a planning
or projection note after candidate emission. Do not suppress the other declared
surface rows inside Candidate URL Intake, and do not promote the apparently
relevant row without a separate gate.

Allowed visible volume/activity fields for Reddit candidate subreddit rows:

- `visible_subscriber_count_or_none`;
- `visible_active_user_count_or_none`;
- `visible_volume_signal_absent_reason_or_none`.

Projection should happen before candidate row emission. The projection step must
remove worthless subreddit links from header navigation, "my subreddits",
popular/all bars, footer links, account menus, preferences, moderator/report
templates, and other page chrome. The projection may keep only subreddit links
from the declared candidate surface, such as related subreddit, recommendation,
cross-post, "more like this", or subreddit search result.

Candidate subreddit rows must remain planning-only. A discovered subreddit must
not be entered for thread enumeration inside the same run. It can become a seed
for a later bounded run only through a new run or explicit scope amendment.

## Hard Stops

- Do not use a thread page as the intake input.
- Do not call Reddit `.json` in this lane.
- Do not broaden from candidate thread extraction into correlated subreddit
  discovery inside the same run unless that surface and cap were declared
  before execution.
- Do not treat search ranking as "recommended" unless the method provenance says
  the surface is search ranking, not Reddit recommendation.
- Do not invent volume. Record only visible volume/activity signals or mark
  volume as absent.
- Do not follow recommended or correlated subreddits in the same run.
- Do not promote subreddit or thread candidates without a separate promotion
  gate.

## Next Use

For a future B2B subreddit-discovery pilot, start with a new parameter packet or
scope amendment that declares candidate subreddit discovery as the target. The
existing thread-candidate pilot output can inform that run, but it does not
authorize same-run widening.

Smallest complete next run shape:

```yaml
run_id: reddit_candidate_subreddit_discovery_b2b_001
mode: pilot_no_live_operator_supplied_html
declared_topic_theme_query: "B2B marketing / sales meetings / outbound pipeline"
seed_subreddits:
  - b2bmarketing
source_surface: reddit_search_listing
candidate_surface_allowlist:
  - reddit_search_listing
  - related_subreddit
max_candidate_subreddits: 20
max_pages_or_result_surfaces: 2
coverage_claim: bounded_probe_only
allowed_outputs:
  - candidate_subreddit_rows
  - visible_subscriber_count_or_none
  - visible_active_user_count_or_none
  - visible_volume_signal_absent_reason_or_none
  - method_provenance
  - stop_reason
forbidden_outputs:
  - thread_body
  - comments
  - user_profile_or_author_data
  - raw_html
  - source_capture_packet
  - data_capture_handoff
```

## Non-Claims

This note is not validation, readiness, implementation authorization, live
Reddit authorization, CloakBrowser/proxy authorization, Source Capture Armory
authorization, Source Capture Packet output, Data Capture handoff, ECR,
Cleaning, Judgment, source-quality scoring, fixture admission, broad crawling,
commercial-use permission, promotion, capture authorization, deployment,
production runtime, commit authorization, push authorization, or PR
authorization.
