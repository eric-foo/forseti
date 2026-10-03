# RaidRelay Discord research: logged leveling trials

```yaml
retrieval_header_version: 1
artifact_role: Bounded research trial and operational closeout
scope: Aion2Global capture trials and an Asmodian-only consolidation follow-up through 2026-10-04 Singapore time.
use_when:
  - Resuming the RaidRelay Global leveling research trial.
  - Comparing later Discord capture methods with this bounded first attempt.
authority_boundary: retrieval_only
```

## Question and outcome

Owner-selected scope: **Global, fresh character, general route**. Investigate
leveling that also earns worthwhile stats, unlocks and collections with the
least wasted effort overall, including later catch-up. No paid shortcuts are
assumed. Class-specific advice must remain conditional.

The first trial below tested acquisition and the research diary. It did not produce
or verify an optimal leveling route. Its follow-up called for checking current
Global applicability, prerequisites and the benefit/cost of proposed steps.
The second pass, recorded below, supplies a conditional route and the remaining
checks. The latest pass below narrows application to **Asmodian only**, adds
source maps and uses the maintained consolidation helper. Earlier passes remain
historical records. No pass includes a character playthrough or establishes
optimality.

## What actually ran

- Used the owner's entitled Chrome Discord session in Aion2Global, guild
  `1113589630122606594`. Completed mandatory onboarding with all nine class
  roles, as the owner explicitly requested. Optional news and faction choices
  were skipped; no messages or reactions were sent.
- Opened the indexed guide channel and retained one leveling guide. Its source
  body identifies Taiwan, is dated December 2025, and excludes Sorcerer from
  the author's claimed experience. It remains a historical verification lead.
- Searched `leveling after:2026-09-01` server-wide. Read the first displayed
  page of 25 results; the displayed total was 1,081 over 44 pages. These mutable
  interface counts do not establish coverage. Sort order was not verified.
- Opened a relevant result in `ingame-help` and retained eight messages from
  one question/answer chain, including the question, advice, follow-up,
  clarification and acknowledgement. Reply context missing from the search
  preview was recovered in the channel view.
- Acquisition used attended navigation and bounded DOM text reads, then the
  existing local-file Armory packet runner. No Discord adapter, bot, daemon,
  automatic research logger or model-backed Judgment run was implemented.

## Activity and decision record

The raw source file and researcher activity file remain separate. The latter
records observed actions, query, selected message, result, corrections and
timing limitations. It is an operator record, not exhaustive click telemetry.

| Observation | Decision and reason |
| --- | --- |
| The indexed guide has a different region and an old date. | Keep it as a lead; do not present its mechanics as verified Global advice. |
| The help conversation directly asks about avoiding later catch-up. | Preserve the question as one player's stated problem, with its answer chain. It does not establish prevalence. |
| The answer offers a sequence and numerical thresholds. | Keep them as claims to verify. A visible moderator role and a thank-you reply do not establish that the advice works or applies to Global. |
| The first content node inside a reply can be its quoted parent. | The initial extraction would attach two of eight messages to the wrong message ID. Retain quoted context and the reply body separately. |
| Screenshot attempts did not reliably frame the selected answer after navigation. | Exclude those images from the packet. Preserve the failed attempt in the activity record; source text and message references are the retained evidence. |

On the **same eight messages**, the first-node interpretation produced two
parent/reply identity mismatches. The corrected representation retains all
content nodes with their IDs, yielding eight distinct own-message IDs and two
quoted-parent references. A direct answer permalink and its author/text were
checked in Discord. This is a bounded identity check, not a generic parser
validation or a test of gameplay accuracy. Grouped continuation authors still
depend on conversation context.

The timed interval was `2026-10-03T14:04:19.359Z` through
`2026-10-03T14:14:42.113Z`: **622.754 seconds**. It includes instruction reads,
diagnostics and preparation interleaved with browser activity. Setup before the
timer, active research time and model cost were not measured. Packaging time
is separate. This first interval is not an efficiency benchmark.

## Retained record

The existing `run_source_capture_packet.py` local-file runner exited `0` and
published the corrected packet `01M412D6ZDF471RVNE7RNGRF8C` at
`F:\forseti-data-lake\raw\c6f\01M412D6ZDF471RVNE7RNGRF8C`.
The canonical root was resolved through `DataLakeRoot.resolve` before use.

| Durable packet member | Purpose / verification |
| --- | --- |
| `manifest.json` | SHA256 `04783413798e5ac9162e7cd97d8cb8b6b766f23e25e03cf2a240d8c22a02cde7`; one slice, `slice_01`. |
| `receipt.md` | Observed on readback; preserves access, scope, limits and runner non-claims. |
| `raw/01_01_source_excerpts.json` | Source text, context, IDs and times; 9,451 bytes; SHA256 `54f956568e74931817fc662a77d9cb4558ac650e36484e8f8adae0bdc22c1cd9`. |
| `raw/02_activity-corrected-v2.json` | Researcher activity, timing and packaging corrections; 5,703 bytes; SHA256 `ac9f8c9ff274ffda105f1943c8b1a15c2f9b1370746373b976569d4dce728717`. |

Fresh readback from this lake packet rehashed both preserved files, checked all
eight expected own-message IDs and the two quoted-parent cases, and recomputed
622.754 seconds from the stored timestamps. All those checks passed. They
establish stored-byte integrity and these bounded record facts, not semantic
accuracy. Packaging completed after the research interval; its elapsed duration
was not instrumented.

One final readback check initially expected the follow-up to quote the first
answer. Inspection of the retained IDs and matching text showed it quotes the
answer's continuation, `1555933310415282268`. The expectation was corrected;
both actual parent/reply pairs and their quoted text then passed. No source
record was changed to satisfy the check.

**Metadata correction:** the first packet, `01M4122H8WPYF1HXK0ZTXM66CS`,
incorrectly recorded screenshots as `not_attempted`. It remains immutable
failure history. The successor above records **attempted but not retained**
in its manifest and receipt, with `re_capture_relationship: supersede` and
unchanged source bytes. Count these source observations once. Its activity
record also preserves an intervening rejected packaging attempt: explanatory
prose was passed to a field requiring a fixed relationship value, then corrected
to `supersede`. No screenshots or visual-fidelity claim were added.

Source cut-off is the end of the trial on 2026-10-03; the indexed historical
guide is deliberately separate from recent conversation. Archive/history was
not attempted; source versions and Global applicability remain unknown.
Engagement was not systematically captured and must not be interpreted as zero.
The packet's generic one-slice layout requires readers to retain each source's
own locator and timestamp in the JSON; it does not make the two sources one
conversation or credit the operator activity file as player evidence.

Lifecycle: `candidate_evidence`, retained to inspect this trial and compare
future capture methods. The source file contains selected account-visible
community text, handles, message IDs and times; the activity file contains
operator process notes and local provenance. Keep both internal. No private
messages, session secrets or unrelated server content are included. Retention
does not grant public quotation, fixture admission, verified gameplay advice
or commercial-use clearance; separate fixture admission remains undecided.

## Follow-up commissioned after the first trial

1. Reuse this channel map and retained conversation. Check the proposed route
   steps against current Global evidence, including material opposing advice.
   Record a supported, conditional or unresolved result for each step; do not
   convert unverified numerical thresholds into instructions.
2. Use observed topic terms and relevant channels to reduce search noise. Log
   the exact query/filter, context recovery, useful result or failure, and
   reason a candidate was kept, rejected or left unresolved.
3. Keep the two reply cases and ordinary messages as capture regression cases.
   Test a changed method on comparable inputs and fresh examples, preserving
   expected results before the run. Compare answer correctness and omissions
   before comparing effort. Change one material part at a time.
4. Produce the first source-linked `do now / do later / optional` route only
   when its important steps have an adequate basis. An unresolved dependency
   stays visible. This trial supplies no claim of complete search coverage,
   independent gameplay corroboration, saturation or improved search speed.

The owning method is
`forseti/product/spines/capture/core/source_capture_toolbox/README.md`.
`forseti/product/spines/judgment/claim_support/forseti_intelligence_claim_support_contract_v0.md`
governs promotion into advice;
`docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
governs retained source use. Neither the source receipt nor this closeout
certifies the advice.

## Second pass: Global applicability and a working route

Owner authorized the follow-up on 2026-10-03. Scope remains a fresh Global
character, general route, without paid shortcuts. This is a **candidate route
for testing**, not a verified fastest or least-total-effort route. At this
observation date, Global is in paid Advanced Access; the publisher schedules
the free-to-play launch for October 5. The route does not require buying access.
Live notices and the character's actual quest/reward screens take precedence
over these early-access observations.

### Do now / do later / optional

This ordering is an analyst decision for the owner's goal. It combines the
common ground in the advice with explicit stop conditions; no measured travel
or completion-time comparison establishes that it is optimal.

| When | Working action | Stop condition / uncertainty |
| --- | --- | --- |
| Do now | Use the main story as the route. Do the first story-embedded Stronghold and nearby progression activities that fit the current trip; pick up encountered feathers. | Avoid clearing an entire zone merely to make every marker disappear. A detour must have a visible reward relevant to the current character. Timing remains conditional: W3, W5, D0. |
| Do now, when blocked | Read the actual quest, gauge or entry requirement. Do enough nearby content or equipment improvement to remove that blocker, then continue. | No universal percentage of feathers, fixed number of side quests, or score needed simply to reach level 45 is established: W3, W4, D3. |
| Do later, at 45 | Continue unfinished story steps. Group remaining home-region quests, sealed dungeons and Strongholds into a deliberate cleanup pass for their relevant permanent rewards. | Some follow-up quests may remain locked until a story hand-in. Check the live quest state before plotting a complete cleanup circuit: W4, D3. Exact map order remains untested. |
| Optional for this first route | Extra collection for achievements after the relevant functional reward cap is reached. | Check what the remaining achievement actually awards. Home-region and Abyss collections are distinct; do not transfer one stopping rule to the other: D2, W6. This is not a claim that all achievements lack useful rewards. |

Temporary publisher warning, checked October 3: avoid opening **Map → Duty**
before level 45 while the known issue in W2 remains active. The notice says
doing so can delay access to Duties at 45 until the next day. Recheck that
notice before the actual run; this is not a permanent game rule.

### Evidence and source competence

All sources below were observed on 2026-10-03. Source-native engagement was
not systematically inspected (`engagement_unavailable`, not zero). Public
excerpts below are bounded source records, not full-page archives. Discord
body text, handles, exact UTC times and selected context are in the new lake
packet. Multiple pages from the same publisher or guide author count once as
an origin. Linked videos or client data not directly inspected receive no
independent corroboration credit.

| Ref | Source, actor, date and bounded observation | What it can support / limitation |
| --- | --- | --- |
| W1 | [Official Dungeon Live Gameplay Showcase](https://www.youtube.com/watch?v=S_TjiOh33a4), AION 2 Official; displayed September 5 in Singapore. Caption at 46:31: “Which max level at launch will be uh 45.” At 22:24–22:26: “when you hit max level. This will unlock at 45.” The latter follows the Conquest introduction. | Publisher's prelaunch cap and Conquest statements. Delegated reader opened the official source and exported captions; these lines were freshly read from that file. Auto-generated captions; no live-client test. |
| W2 | [Advanced Access Known Issues, Updated 10/2](https://store.steampowered.com/news/app/3393110/view/712288224875119580?l=english), publisher; browser displayed October 3 locally. “This issue can be avoided by not accessing the Duty tab until reaching level 45.” | Temporary publisher warning. Full article was read by the delegated reader in Steam's browser news modal. Root web extraction failed; that empty response was not treated as evidence. |
| W3 | [Global launch guide](https://aion2maps.com/guides/welcome/), MidirSkry / Aion 2 Maps, updated October 2. “Do what the story passes, what clears a story lock, and the first Stronghold while the story has you inside it.” | Author's route synthesis, combining Global client claims, creator advice and some Taiwan material. Source labels aid inspection but do not certify each mechanic or supply independent playthroughs. [Authorship and method](https://aion2maps.com/guides/about/) were checked. |
| W4 | [What to do at 45](https://aion2maps.com/guides/what-to-do-at-45/), same author, updated October 2. “The Abyss is the faction war zone, open from item level 1,000”. The page places Koro's story hand-in there. | Reported datamine supports a narrower interpretation of the score claim. Client files were not independently inspected. Same origin as W3. |
| W5 | [Global roadmap](https://www.reddit.com/user/GreekSaladTV/comments/1wgswwt/aion_2_season_1_roadmap_gear_enchanting/), GreekSaladTV. “I've been playing on the Taiwan servers and put together a full plan for global”. Recommends side quests, feathers, cubes and solo dungeons during leveling. | Firsthand Taiwan experience projected onto Global; material opposing timing advice. Exact publication date unresolved between search and rendered relative dates. Linked video was not viewed or counted separately. |
| W6 | [Feather discussion](https://www.reddit.com/r/Aion2/comments/1ww464s/i_hate_farming_abyss_feathers_who_ever_came_up/), Potato4LifeMyDude; relative timestamps only at capture. Advises stopping at Monolith 30 rather than collecting every feather. Another participant, mikeyeli, explicitly corrects confusion between home-region and Abyss feathers. | Community advice plus a scope warning. Exact client version and region unstated; search-snippet claims about four points per feather were absent from the opened excerpt and were not promoted. |
| W7 | [NC Japan Global page](https://aion2.ncsoft.jp/en/contents), publisher, update date unavailable: “Official Launch on October 5, 2026”. [Launch FAQ](https://store.steampowered.com/news/app/3393110/view/680761758839734961), September 30, 21:27 +08: “AION 2 is free to play with an optional monthly membership.” | Dates and access model, not route quality. FAQ read directly in the delegated browser; its web extraction returned a shell. Same publisher origin as W1/W2. |
| D0 | First packet's eight-message question/answer chain, October 3; retained earlier in this record. | Original nearby-activity advice and unverified 33% figure. Rediscovered results are not new origins. |
| D1 | [Collection question](https://discord.com/channels/1113589630122606594/1441497294271942696/1555165034953580576), Shizy, October 1; `discord-feather-question` in the new source file. | One player's uncertainty about feathers left after the Monolith. Nearby conversation was unrelated; no answer was attached by proximity. Not evidence of a mechanic. |
| D2 | [Monolith question and answers](https://discord.com/channels/1113589630122606594/1441497294271942696/1555687225830809631), Necarunerk and Hidden Cube Tito, October 3 local; `discord-monolith-stop`. | Tito advises stopping at 30 unless pursuing the achievement. Same advisor as D0, not another expert. Continuation authorship depends on adjacent context; no client test. |
| D3 | [Draupnir/Koro question and answer](https://discord.com/channels/1113589630122606594/1441497294271942696/1555364661212221531), Rawwad and Dragon3316, October 2 local; `discord-abyss-entry`. | Recovers what 1,000 was answering: entering the Abyss for a level-45 story quest. Dragon3316's expertise is unestablished; Rawwad's acknowledgment is not a successful retest. |

### Claim decisions

This table maps the claim-support contract's fields. `origins / observations`
means `independent_origin_count / source_observation_count`, counting only the
bounded assertion in that row. Evidence refs resolve above; source roles and
scope conditions travel with them. For every row, `engagement_evidence_refs`
and `behavior_evidence_refs` are empty: no endorsement or successful route
playthrough is credited. `causal_ceiling: descriptive_only`; no entry proves
that the route saves time. No conflicting gameplay evidence was inferred from
mere absence in publisher documentation.

| Bounded proposition | Support posture; origins / observations | Evidence refs; source roles | Conflict posture; counterevidence refs | Decision and material scope |
| --- | --- | --- | --- | --- |
| Publisher announces launch cap 45 and Conquest at 45. | `directly_observed`; 1 / 2 | W1; publisher | `none_observed`; [] in the bounded later-notice check | Supported as announced Global rules; prelaunch captions are not an independent live-client measurement. |
| Publisher lists a pre-45 Duty-tab issue and avoidance action. | `directly_observed`; 1 / 1 | W2; publisher | `none_observed`; [] in the checked notice | Supported as a current notice, with a recheck before play. |
| Two community accounts advise stopping home-region feather collection at Monolith 30. | `independently_repeated`; 2 / 2 | D2 answer, W6 Potato4LifeMyDude reply; community advisors | `none_observed`; [] within the checked home-region advice | Conditional reported advice. Two credited accounts, not two demonstrated Global tests. W6's correction limits transfer to Abyss. Live reward state determines the stopping point. |
| An Abyss-entry score of 1,000 is reported. | `independently_repeated`; 2 / 2 | D3 answer, W4; community advisor and guide/datamine author | `none_observed`; [] in the bounded check | Conditional. Region/build unstated in D3; raw client data uninspected in W4. Do not change this into a requirement merely to reach level 45. |
| Advice differs on when to clear side content. | `directly_observed`; 3 / 3 | D0, W3, W5; community advisors and guide author | `mixed`; W3 versus D0/W5 | No universal optimum. The route above is a testable choice for useful nearby progress and planned cleanup; complete-zone detours are not established as worthwhile. |

The original **33% feather claim remains unresolved**: no defined denominator,
reward milestone and verified Global basis were established. No instruction
uses it. Exact Ascension-gauge breakpoints, permanent-reward quantities,
class/faction travel order and missable collections were not fully verified.
Therefore this is not a complete collection checklist or a claim that nothing
important can be missed.

### Activity, comparison and retained result

Discord first required renewed login; the owner completed it while public-source
checks continued. Searches were `in:🙏｜ingame-help feathers after:2026-09-29`
(14 displayed/inspected hits) and `in:🙏｜ingame-help 1000 after:2026-09-29`
(4 displayed/inspected hits). Sort was not verified; displayed totals do not
establish exhaustion. Three selected windows yielded seven new text messages.
Unrelated adjacent conversations and an unrelated currency result with missing
reply context were excluded. Missing content was not reconstructed.

Timed acquisition interval: `2026-10-03T15:12:22.297Z` to
`2026-10-03T15:19:47.835Z`, **445.538 seconds**. Login wait and interleaved public
research are included; setup, full delegated effort, active time and cost are
not measured. Queries, channel and date scope changed together. This cannot
be compared with the first trial as evidence of faster or more accurate search.
The seven new messages contain no quoted-parent cases, so they do not extend
the first trial's reply-parser validation.

The existing local-file runner exited `0`. Supplementary packet:
`01M415R8WBKY91ERSDSQZRAV2W`, at
`F:\forseti-data-lake\raw\01d\01M415R8WBKY91ERSDSQZRAV2W`.

| Durable member | SHA256 |
| --- | --- |
| `manifest.json` | `97667b06ec693587e879bbef53cf458464dfd411f92b7f509d786bfe2b36e66f` |
| `raw/01_discord-sources.json` (4,991 bytes) | `c8975d325eb44f7874573e2571ff474e85f6d02f94b217f4c7b7d7bf71ec6621` |
| `raw/02_activity-complete.json` (4,856 bytes) | `f55cd4f0d03b1704f8b351c7f727825c7d33c88a99a431600f76e13a21656e23` |

Fresh lake readback verified both preserved-file hashes, all seven expected
own-message IDs, zero quoted-parent cases, elapsed time, receipt, supplementary
relationship and `not_attempted` media posture. No screenshots were taken in
this pass. The first failed runner-help path and its correction are recorded;
that failed invocation performed no capture. The source file remains separate
from the operator log. The first packet's internal `candidate_evidence`
retention and use limits also apply here; this packet adds no fixture admission,
publication clearance, automated adapter or gameplay certification.

The next useful improvement test is a real fresh-character run of this route:
record the requirement/reward actually shown at each stopping point, useful
permanent progress earned, detours and later return trips. A later route change
must be compared on the same goal and comparable class/faction/build. That
playthrough has not happened; this pass neither controls a game account nor
starts ongoing monitoring.

## Third pass: Asmodian maps and mixed-source consolidation

Owner selected Asmodian first to prevent faction mixing, asked for a targeted
capture followed by the latest PR'd consolidation method, and explicitly
authorized fixing source attribution before running it. PR
[1645](https://github.com/eric-foo/forseti/pull/1645) was freshly checked as merged
on September 29, with zero review threads returned and no further page. Its
baseline is `docs/workflows/customer_evidence_consolidation_baseline_v0.md`.

The current helper had treated every main text as customer testimony. The
bounded fix preserves explicit body speaker, original source role and family
through reading, citations, synthesis and saved outputs. New runs use
`paragraph_evidence_v3`; frozen legacy and v2 reconstruction stays unchanged.
Fifty-five focused offline tests passed after integration, including mixed-role
saved reports, same-origin guide/map counting, unknown attribution, image
pointers and frozen v2 bytes. This verifies the attribution mechanism, not the
truth of the source advice.

### Targeted capture and admission

Five supplementary lake packets retain the new captures. Each member preserves
its own source time and locator; a packet's packaging time is not a source
publication date. All preserved member sizes and hashes were read back from the
lake. Source content remains internal candidate evidence under the retention
limits above.

| Packet | Preserved material |
| --- | --- |
| `F:/forseti-data-lake/raw/c84/01M41DNNTWQY83PVJVB5DBP12V` | Asmodian Altgard/Ishalgen map DOM, 58 area rows, label positions, original and focused native screenshots, capture limits. |
| `F:/forseti-data-lake/raw/41e/01M41DNQA3HQK2TMR7QB783CDH` | Three complete Aion2Maps guide main bodies, source metadata and native screenshots; bounded community/guide excerpts remain distinct from analyst observations. |
| `F:/forseti-data-lake/raw/6b8/01M41DNRTM06HNY8GMSJK9V6JV` | Publisher notice excerpt and official prelaunch showcase frames at 21:58 and 22:15. Frames are not live-client or Asmodian quest tests. |
| `F:/forseti-data-lake/raw/dd5/01M41EEHHXNB796V7R402SMY08` | Complete Couga progression guide, native footer/source links, unobscured screenshots, and transparently marked obstructed attempts. Replaces earlier disconnected snippets in this corpus. |
| `F:/forseti-data-lake/raw/004/01M41EENQ6WYY6NH125ZCBRCCE` | Fresh Discord search/activity records and one native Asmodian Safe Haven question. Login failures remain in the record. |

After the owner signed in again in their Chrome, two intended searches ran in
`ingame-help`: `monolith after:2026-09-29` (5 displayed hits) and
`feathers after:2026-09-29` (15). All displayed hits were read; sort was not
verified. Existing advice was re-observed, not credited as new origins. The new
Safe Haven question explicitly states Asmodian; no answer was observed in the
bounded recovered window. Nearby unrelated replies were not attached to it.
An attempted query replacement retained Discord's old tokenized filters and
returned zero hits; that invalid combined query was corrected and is not
evidence of source absence. A failed named-button lookup was also retained.
No messages, reactions or further account-role changes were made.

The frozen corpus contains **86 native records**: 16 Discord messages, four
complete guide texts, three Reddit excerpts, 58 map area rows, two map DOM
transcripts, two publisher transcript excerpts and one publisher notice excerpt.
Fourteen source containers and two true quoted-parent contexts are preserved.
All 86 body values were checked against their decoded originals, with 54 file
pins across seven packets. The same guide author and maps share one origin;
account handles are not verified people. Repeated map records are not
independent corroboration. Historical Taiwan/Elyos advice, analyst prose,
duplicate search mentions and the unavailable GreekSaladTV original were not
admitted. Thus this set cannot establish exhaustive contrary-advice coverage.

### Map deliverable and limits

The [Asmodian zone atlas](C:/Users/vmon7/Desktop/projects/forseti/forseti-harness/_test_runs/raidrelay_asmodian_20261004/atlas/asmodian-zone-atlas.html)
embeds four unchanged source screenshots and a searchable area table. Saved
asset bytes match their lake originals. Its 58 source-defined area rows sum to
**559 Empyrean Trace markers**. The Altgard row contributes four Traces; its
other 61 entries are sealed dungeons and are not added to the Trace total.
The site labels the maps Asmodian and Global client data; its client files were
not inspected. Area groupings are not independently verified zone boundaries.
Browser preview of the local HTML was blocked, so rendering remains uninspected.

These are map inventory counts, not a count earned by following the MSQ.
No ordered quest path, unique on-route pickup list, pickup-to-point conversion
or ending feather inventory was established. Ishalgen's absent Collect tab
does not establish zero feathers. The atlas therefore draws no invented route
arrows. Native clipped screenshots preserve the original overview alongside
the tighter view; no generative image editing was used.

### Consolidation execution and current result

Run directory:
`C:/Users/vmon7/Desktop/projects/forseti/forseti-harness/_test_runs/raidrelay_asmodian_20261004/consolidation-run`.
Its question, corpus, semantic rules, assignments and source bindings are frozen.
Corpus SHA256:
`9cfac980ae18bbe124a1dad5caac9f686dbfb7a746a181ae9e363c1e6d5f9976`.
The installed helper prepared two complete reading units under its default
45,000-token request budget. Image references remain pointers; these text-only
model calls do not inspect image pixels.

The first native reading response failed exact-source
validation: one quotation changed "Your" to "The", one joined noncontiguous
table cells, and a later validation step found a scalar quote pointing at an
array. Home checked the frozen originals, restored literal text and the exact
array-element pointer, and explicitly revised the affected prose. The native
response remains unchanged; a separate source-bound home correction was
accepted. No paid reread was used. This is assisted recovery, not an autonomous
clean pass.

The second reading unit and fresh-context synthesis were accepted without home
correction. The helper delivered **`REPORT_SAVED_UNREVIEWED`**, with all 86
assignments accounted for exactly once and no pending reads or attempts needing
attention. The [consolidated draft](C:/Users/vmon7/Desktop/projects/forseti/forseti-harness/_test_runs/raidrelay_asmodian_20261004/consolidation-run/synthesis/report.md)
was freshly read from disk. Its 46 compiled citations retain source roles,
native locators and quoted originals in the adjacent `citations.json`,
`cited-originals.json`, `report-originals.md` and `source-bindings.json`.
Report SHA256:
`8ecfc68c9a94ea4418dc902cb98dbb72757bff494fb507b76e779793a12bc079`.

Three native calls reported 80,591 input tokens (zero cached), 6,560 output
tokens, and 781 reasoning-output tokens in the separate native field. Summed
native wall time was 174.329 seconds; this excludes capture, setup, home repairs
and review. These completed-turn fields do not measure the whole research cost,
hidden provider usage or dollars. The saved metrics and failed/native/corrected
artifacts remain beside the run. The brief is 837 whitespace-delimited words,
above the commissioned approximate 500–700-word target; it remains an internal
consolidation draft, not the concise player-facing guide.

The required external source review is still pending. The owning baseline
requires a proposal-only review through operator courier, then source-backed
home adjudication; structural acceptance alone does not certify a guide. No
efficiency gain, dollar saving, gameplay accuracy or optimal route is claimed
from this differently scoped trial. The next review must check source meaning,
material omissions and faction/unit boundaries before a final guide is built.
