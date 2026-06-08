# Reddit Candidate Intake Operator Pilot Blocked Input Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow closeout
scope: >
  Records that the next Reddit Candidate URL Intake success signal could not
  run because the required operator-supplied old Reddit source URL and static
  HTML input are not present in the workspace.
use_when:
  - Resuming the first real no-live Reddit Candidate URL Intake operator pilot.
  - Distinguishing a blocked pilot from an empty-result pilot or a successful
    fixture-backed rehearsal.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/reddit_candidate_intake_operator_pilot_parameter_packet_v0.md
  - docs/workflows/reddit_candidate_intake_operator_pilot_plan_v0.md
  - docs/workflows/reddit_candidate_intake_fixture_backed_pilot_rehearsal_closeout_v0.md
stale_if:
  - The operator supplies the old Reddit source URL and saved/static HTML input.
  - The operator pilot plan changes the input gate or default pilot mode.
```

## Status

Status: `BLOCKED_PILOT_INPUT_MISSING`.

Adversarial review is not required for this blocked-input closeout. This closeout
does not change the architecture, policy contract, parser, writer, tests,
runtime boundary, or downstream promotion model. It records a stop condition for
an already-governed pilot gate.

## Cynefin Routing

Smallest complete outcome: preserve the stop reason for the real operator pilot
and name the exact missing input required to proceed.

Regime: clear with messy-worktree caution.

Why: the pilot contract already defines the execution gate; the workspace simply
lacks the required operator-supplied old Reddit URL and static HTML input.

Decomposition: gate-first execution discipline.

Current bottleneck: missing operator input, not missing architecture,
implementation, fixture, review, CloakBrowser/proxy setup, or Source Capture
Armory authority.

Riskiest assumption: treating the existing fixture-backed rehearsal as the real
operator pilot would overclaim success.

Stop or pivot condition: if the operator supplies a valid old Reddit listing or
search URL plus saved/static HTML input, this blocked closeout is superseded by
an executed pilot closeout.

Allowed next move: run `pilot_no_live_operator_supplied_html` through Candidate
URL Intake after the source URL and HTML input are supplied.

Disallowed next move: live fetch, Reddit `.json` intake, thread-page intake,
fixture substitution, Source Capture Armory invocation, Source Capture Packet
generation, Data Capture handoff, or promotion into capture units.

## Source Context Status

Read before this closeout:

- `.agents/workflow-overlay/README.md`;
- `.agents/workflow-overlay/decision-routing.md`;
- `docs/workflows/reddit_candidate_intake_operator_pilot_plan_v0.md`;
- `docs/workflows/reddit_candidate_intake_operator_pilot_parameter_packet_v0.md`.

Workspace search found no operator-supplied old Reddit HTML input for the real
pilot. The only old Reddit HTML file found was the local fixture:

```text
orca-harness/tests/fixtures/reddit_candidate_intake/old_reddit_listing_noisy.html
```

That fixture is valid for rehearsal and tests, but it is not a substitute for
the next success signal.

## Blocked Pilot Packet

```yaml
blocked_pilot:
  run_id: reddit_candidate_pilot_001
  intended_mode: pilot_no_live_operator_supplied_html
  status: BLOCKED_PILOT_INPUT_MISSING
  missing_required_inputs:
    - source_input.old_reddit_source_url
    - source_input.html_input.value
  required_source_shape:
    source_surface: reddit_search_listing | subreddit_listing
    host: old.reddit.com
    forbidden_input_shapes:
      - reddit_json_url
      - reddit_thread_page_as_input
      - live_fetch_by_candidate_url_intake
      - fixture_substitution_for_real_pilot
  retained_bounds:
    cap_type: probe
    coverage_claim: bounded_probe_only
    max_subreddits: 5
    max_threads_per_subreddit: 25
    max_pages_or_result_surfaces: 2
    time_window_days: 30
    sort_order: top
  stop_reason: blocked_result
```

## Next Success Signal

The next success signal is an executed real no-live operator pilot with:

1. one old Reddit listing or search URL used only as provenance;
2. the saved/static HTML for that same page supplied by the operator;
3. candidate URL rows plus provenance only;
4. a visible stop reason;
5. no raw HTML, body text, comments, user/profile/author data, Source Capture
   Packet, Armory invocation, Data Capture handoff, ECR, Cleaning, Judgment,
   fixture admission, source-quality score, or promotion claim.

## Non-Claims

This closeout is not an executed pilot, not an empty-result run, not a blocked
Reddit access result, not live Reddit authorization, not CloakBrowser/proxy
setup, not Source Capture Armory execution, not Source Capture Packet output,
not Data Capture handoff, not fixture admission, not promotion, not validation
of a real Reddit surface, not commercial-use permission, not commit
authorization, not push authorization, and not PR authorization.
