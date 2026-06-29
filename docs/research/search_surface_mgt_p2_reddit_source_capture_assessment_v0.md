# Search-Surface MGT P2 Reddit Source Capture Assessment v0

```yaml
retrieval_header_version: 1
artifact_role: Research capture closeout
scope: P2 source-capture playbook run and per-source substantiality assessment for the three Priority A Reddit search-surface sources from the fragrance pilot.
use_when:
  - Checking whether the P1 Reddit screen-light reads were upgraded into packet-grade local source capture.
  - Deciding whether the Search-Surface MGT fragrance pilot produced enough Reddit information to route Capture and Scanning next steps.
  - Reviewing source-capture method, scratch packet lifecycle, hashes, sensitivity, and non-claims.
open_next:
  - docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/search_surface_mgt_p1_direct_source_capture_receipt_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md
stale_if:
  - The three Reddit threads are recaptured through a different route.
  - The scratch packet directories are deleted and a later user needs raw-body reinspection rather than this closeout.
  - A separate retention, fixture-admission, Judgment, or buyer-proof decision promotes or supersedes these packets.
authority_boundary: retrieval_only
```

## Boundary

This is a source-capture and information-substantiality closeout for P2. It is
not Judgment evidence, durable-demand proof, buyer proof, Product Lead action,
fixture admission, commercial-use clearance, or source-completeness proof.

The owner request was to use the source-capture playbook to access Reddit, then
determine whether the information gathered is substantial and why, assessed per
information source.

## Capture Unit

```yaml
unit_type: candidate_or_scouting
purpose: "Upgrade P1 screen-light Reddit reads into local source-capture packets and decide whether the gathered information is substantial enough to evaluate Search-Surface MGT capture efficacy."
decision_question: "Can the three Priority A Reddit search-surface sources provide packet-grade source language for evaluating Search-Surface MGT capture efficacy?"
access_classification: publicly_viewable_reddit_threads
route_selected: old_reddit_direct_http_batch
route_reason: "The Reddit operator playbook says exact old-Reddit Direct HTTP is the current cheapest complete path for supplied exact thread URLs."
volume_ceiling: 3
urls:
  - slot_id: p2_s01_fragrance_testing
    url: https://old.reddit.com/r/FragranceStories/comments/1mydzqk/how_do_you_test_a_fragrance_before_buying/
  - slot_id: p2_s04_santal_33_dupes
    url: https://old.reddit.com/r/fragrance/comments/15fp22s/what_is_the_best_alternative_to_santal_33_by_le/
  - slot_id: p2_s05_br540_dupes
    url: https://old.reddit.com/r/Colognes/comments/1nwmudi/im_looking_for_close_dupes_of_baccarat_rouge_540/
exclusions:
  - no subreddit crawl
  - no user or profile capture
  - no link following
  - no recommendations
  - no comment-link expansion
  - no monitoring
  - no proxy
  - no browser automation
commercial_use: no
```

Command run from
`C:\Users\vmon7\Desktop\projects\orca\worktrees\search-surface-mgt-p0-captures`:

```powershell
python orca-harness\runners\run_reddit_old_http_batch.py --url-list orca-harness\_test_runs\search_surface_mgt_p2_reddit_capture_v0\urls.json --output-root orca-harness\_test_runs\search_surface_mgt_p2_reddit_capture_v0\batch --decision-question "Can the three Priority A Reddit search-surface sources provide packet-grade source language for evaluating Search-Surface MGT capture efficacy?" --max-urls 3 --timeout-seconds 20 --max-bytes 5000000 --cadence-mode bounded_jitter --cadence-window-seconds 90 --cadence-min-gap-seconds 20 --cadence-max-gap-seconds 40 --cadence-random-seed 20260625
```

Local quality summary:

```powershell
python orca-harness\runners\run_reddit_batch_quality_summary.py --batch-summary orca-harness\_test_runs\search_surface_mgt_p2_reddit_capture_v0\batch\batch_summary.json --output-dir orca-harness\_test_runs\search_surface_mgt_p2_reddit_capture_v0\quality
```

Local cleaned read views were generated with `run_reddit_agent_view.py` for each
derived `reddit_thread_consolidation.json`.

## Packet Lifecycle And Sensitivity

The generated Reddit packets remain `scratch` under the Source Capture Packet
fixture/retention decision. This closeout records packet facts and assessment
without committing raw third-party Reddit bodies.

Scratch packet root:
`orca-harness\_test_runs\search_surface_mgt_p2_reddit_capture_v0`.

Sensitivity note: the scratch packets and cleaned views contain user-authored
Reddit posts/comments, direct source bodies, raw HTML, machine-specific local
paths, and at least one source-visible personal contact string in user-authored
comment text. Do not quote, publish, client-share, treat as fixture evidence, or
promote into Judgment without a separate retention/admission/use decision.

## Capture Results

| Metric | Observed result |
| --- | --- |
| URL count / hard ceiling | 3 / 3 |
| Method | `old_reddit_direct_http` |
| Cadence | `bounded_jitter`, planned offsets `0.000`, `35.188`, `59.987` seconds |
| Capture success | 3 |
| Consolidation success | 3 |
| Usable yes | 2 |
| Usable needs review | 1 |
| Usable no | 0 |
| Proxy/browser/retry escalation | none |

## Hashes

| Scratch artifact | SHA256 |
| --- | --- |
| `batch\batch_summary.json` | `5459D145C10019D73463860B557B99D514626E9486F837EA1973F8984C9FA56C` |
| `quality\reddit_batch_quality_summary.json` | `B8CDF593F2D2AC0E139DEF732D4A88E35A6ADF03DA0152E81720E7AF564BA208` |
| `batch\p2_s01_fragrance_testing_packet\manifest.json` | `814001D9D1DD520DCAEFCE2333F7DF6BE208B2DB08831D6B87F435324286BDA9` |
| `batch\p2_s04_santal_33_dupes_packet\manifest.json` | `21FEB243A93AA27D78981971A2878F8FDC2C650B0EA88D632412F9C72E76EB49` |
| `batch\p2_s05_br540_dupes_packet\manifest.json` | `6ED483776445072256E595EFE0206CFFEED9F379811D0BB70AB03DA39485FA58` |
| `batch\p2_s01_fragrance_testing_derived\reddit_thread_consolidation.json` | `1C63840AD06C480F63C766B4C253936131006F2209DC06F8307AFC0A59DBB3BB` |
| `batch\p2_s04_santal_33_dupes_derived\reddit_thread_consolidation.json` | `F4FCD1EBE2F4ADD12964A967214DE662759495B015FC8D888E476EBFDD7B8FDA` |
| `batch\p2_s05_br540_dupes_derived\reddit_thread_consolidation.json` | `769CAF9BFBB17216EDC0F420ABE40822F7470FFC5D2E9E185F8B1CDB2A3A885F` |

## Per-Source Assessment

### `p2_s01_fragrance_testing`

Capture state:

- HTTP 200, `181045` bytes, `text/html; charset=UTF-8`.
- `39` comments parsed from `39` observable comment nodes.
- `38` author slots.
- `0` parser warnings, `0` limitations.
- Quality summary: `usable_for_downstream: yes`.

Information gathered: substantial for the `trial_to_full_bottle_behavior`
frontier.

Why: the captured source has dense buyer-origin process language, not just
generic interest. The comments repeatedly describe test sequences and purchase
thresholds: paper/strip first, skin chemistry, decants/samples, repeated wears,
travel size, 10ml/5ml/2ml quantities, full-bottle upgrade, blind-buy price
ceilings, and regret avoidance. Term-count probe over the cleaned view found:
`decant=28`, `sample=20`, `skin=31`, `paper=14`, `strip=11`,
`blind buy=13`, `10ml=8`, and `full bottle=6`.

Decision effect: this is enough to tell Capture/Scanning to pursue trial
mechanics as a real behavior path: sample/decant access, repeat-wear testing,
travel-size stepping stones, and retailer discovery-set shelves. It is not by
itself enough to prove durable demand or willingness to pay.

### `p2_s04_santal_33_dupes`

Capture state:

- HTTP 200, `266875` bytes, `text/html; charset=UTF-8`.
- `70` comments parsed from `70` observable comment nodes.
- `60` author slots.
- `2` parser warnings due to collapsed comments carried visibly.
- Quality summary: `usable_for_downstream: needs_review`.

Information gathered: substantial with visible review caveat for the
`premium_dupe_substitution_pressure` frontier.

Why: the captured source contains price-pressure motive, repeated named
alternatives, disagreement over closeness, use-case splitting, and original vs
dupe tradeoff language. Term-count probe over the cleaned view found:
`Santal 33=22`, `dupe=23`, `Bois de Balincourt=6`, `Dossier=8`,
`Cremo=2`, `Palo Santal=2`, `Costco=2`, `Montagne=2`, and `Dime=4`.

The `needs_review` flag does not invalidate the source for routing. It means the
collapsed-comment parser warnings should travel forward. The available body is
still strong enough to name follow-on capture targets and comparison axes:
closest alternative, cheaper everyday substitute, not-a-dupe disagreements,
longevity, smoother/fresher/dill-pickle/off-note language, and discount-channel
references.

Decision effect: this is enough to route product-page follow-up for repeated
alternatives and to preserve premium-dupe substitution as a Scanning/Capture
frontier. It is not enough for Judgment without review, source-cleaning, and
cross-source corroboration.

### `p2_s05_br540_dupes`

Capture state:

- HTTP 200, `576437` bytes, `text/html; charset=UTF-8`.
- `171` comments parsed from `171` observable comment nodes.
- `115` author slots.
- Source-visible postures include `169` present, `1` deleted, and `1` removed.
- `0` parser warnings, `0` limitations.
- Quality summary: `usable_for_downstream: yes`.

Information gathered: highly substantial for the
`premium_dupe_substitution_pressure` frontier.

Why: the captured source is materially richer than the P1 screen-light read. It
contains many named alternatives, direct positive/negative comparisons,
performance language, price/value tradeoffs, "close but not 1:1" distinctions,
clone/dupe vocabulary, and disagreement chains. Term-count probe over the
cleaned view found: `BR540=29`, `Baccarat=15`, `dupe=31`, `clone=19`,
`close=32`, `Untold=22`, `Armaf=11`, `Dossier=9`, `Al Haramain=5`,
`Amber Oud=6`, `Lattafa=6`, `Maison Alhambra=3`, and `Cloud=7`.

The source also contains noisy or risky user-authored material, including
removed/deleted states, promotional/sales-like comments, outbound links, and a
personal contact string. That noise should be filtered in any later Cleaning or
Judgment route; it does not erase the source's routing value.

Decision effect: this is enough to route repeated-alternative product checks and
dupe-comparison capture. It is not enough for Judgment because the thread mixes
recommendations, argument, personal preference, possible spam, and source-visible
removed/deleted states.

## Overall Verdict

`P2_REDDIT_CAPTURE_SUBSTANTIAL_FOR_ROUTING_AND_CAPTURE_EFFICACY`.

The Reddit packet-grade capture materially improves the Search-Surface MGT pilot:

- P1's screen-light Reddit observations were upgraded to local source-body
  possession through the current playbook route.
- The captured Reddit information is substantial for deciding what Capture and
  Scanning should do next.
- The two frontiers remain valid:
  - `trial_to_full_bottle_behavior`
  - `premium_dupe_substitution_pressure`
- The strongest next action is not more broad Google/Trends work. It is to hand
  these source-backed requests into Capture/Scanning, with raw packet retention
  left scratch unless separately admitted.

Do not promote this directly into Judgment. The correct next layer is source
selection, source cleaning/projection, and cross-source corroboration if the
owner wants buyer-proof or demand-strength claims.

## Non-Claims

- Not Judgment evidence.
- Not durable-demand proof.
- Not buyer proof.
- Not willingness-to-pay proof.
- Not Product Lead action.
- Not fixture admission.
- Not source completeness proof.
- Not source-quality scoring.
- Not commercial Reddit authority.
- Not broad Reddit crawl.
- Not monitoring.
- Not proxy, browser automation, retry escalation, or API behavior.
