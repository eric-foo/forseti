# RaidRelay Discord research: first logged leveling trial

```yaml
retrieval_header_version: 1
artifact_role: Bounded research trial and operational closeout
scope: Aion2Global access, selected conversation capture, observed defects, and the next research check on 2026-10-03.
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

This first trial tested acquisition and the research diary. It did not produce
or verify an optimal leveling route. The next research pass must check current
Global applicability, prerequisites and the benefit/cost of each proposed step.

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

## Next bounded trial

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
