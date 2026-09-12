# Forseti efficiency measurement

```yaml
retrieval_header_version: 1
artifact_role: Operational measurement guide
scope: Complete-run usage collection, quality-bound comparisons, and repository size observations.
use_when:
  - Measuring a Forseti extraction, completed Codex task, or validation command.
  - Comparing an efficiency change against matched baseline work.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/efficiency/README.md
  - forseti-harness/runners/run_efficiency.py
  - docs/workflows/efficiency/forseti_efficiency_measurement_2026_09_05_evidence.json
```

## What this measures

The executable owners are `forseti-harness/harness_efficiency.py`, the
`forseti-harness/reports/efficiency_*.py` collectors/comparator, and
`forseti-harness/runners/run_efficiency.py`. This guide explains their scope;
existing project validation and product rules remain authoritative.

`provider_attempts.py` and `provider_execution.py` continue to own reserved,
immutable model-attempt streams, recovery and response publication. Their
required prompt/response artifacts and publication semantics serve that separate
consumer. Operational measurements neither replace those receipts nor require
ordinary validation commands to enter the model-publication lifecycle.

| Surface | Start and finish | Usage and quality boundary |
| --- | --- | --- |
| Provider transcript extraction | Transcript identity preparation through model request, parsing, Silver write and marker readback | Automatic metadata sidecar; observed provider usage; validated write and matching persisted hash. This oracle does not prove semantic accuracy. |
| Direct extractor call | Input preparation through quote/schema validation | Automatic sidecar with a narrower workflow name; never represented as a lake workflow. |
| Completed Desktop task | Observed task start through last attributed child/guardian completion | Unique response usage, checked against cumulative turn totals; metadata-linked child inventory. An independent output checker can supply quality evidence. |
| Fresh native CLI task | Process start through completion and optional independent checker | Fresh single-turn `codex exec --json`; observed delegation leaves coverage unknown because child usage is absent from this stream. |
| Validation command | Process start through exit and optional checker | Real outer wall time; token usage unknown when the command has no usage collector. |
| Repository size | One resolved Git commit | Logical blob bytes per tracked path; separate regular files, symlinks/gitlinks, static instruction-source bytes and current measurement-log bytes. Not physical Git storage or tokens. |

Native Desktop usage logs are already automatic. The importer derives a report
from a completed task when an efficiency comparison needs it; it adds no
per-turn reporting obligation. Use the session folder covering the complete
work interval (a date directory, or a wider explicit directory for work spanning
days). Only first-row session metadata is inventoried broadly; full records are
read only for the selected task and its linked descendants. Conversation text,
tool arguments, outputs, credentials and provider response bodies are excluded
from measurement records.

The Desktop adapter was exercised against schema version observed in Desktop
0.153.1. It uses per-response `token_usage_record.usage`, not repeated cumulative
`token_count` snapshots. Missing usage, active/incomplete boundaries, missing
children, conflicting duplicate responses and unmatched totals remain unknown.
Coverage describes the retained local telemetry contract, not a billing audit
or evidence that an unavailable platform event was logged.

## Run the commands

Run from `forseti-harness`. All commands have `--help`.

```text
python -m runners.run_efficiency import-codex --sessions-dir SESSION_FOLDER --thread-id THREAD --turn-id TURN --workflow agent_change --workload-id FIXTURE_SHA --output-dir memory/logs/efficiency --quality-command checker.json --cwd EXERCISE_FOLDER
python -m runners.run_efficiency measure --workflow validation --workload-id TREE_SHA --output-dir memory/logs/efficiency -- python ../.agents/hooks/check_map_links.py --strict
python -m runners.run_efficiency compare --baseline before1.json before2.json before3.json --candidate after1.json after2.json after3.json
python -m runners.run_efficiency repo-size --repo .. --revision HEAD --base BASE_REVISION
```

Uppercase names and numbered run filenames above are caller-supplied values,
not repository paths. `checker.json` is a JSON argv array, for example
`["python", "oracle.py"]`, referring to the independent checker in the selected
exercise directory. Checker identity includes its argv and referenced file
hashes. Imported historical duration stays unchanged; the later checker time is
reported separately. A completed task without a quality check remains
`unmeasured` for quality, even when all tokens are observed.

For a commissioned completed-task comparison, use `import-codex` with the
workload's existing `--quality-command` in one coordinator invocation. Its final
JSON includes usage and coverage issues, unique response counts, per-task usage,
tool-call event counts, observed model/effort, output diagnostic counts, checker
exit/status and the completion interval. The importer rereads the saved JSON
and checks it against the collected record before returning
`record_readback_matched: true`; a mismatch fails instead of returning success.
That fresh readback supports the persistence claim at this return boundary.
The detailed record remains at `record_path`. Read it or the selected source
only when a missing fact, diagnostic
or judgment requires it; do not reopen the same log separately for each metric.
Known independent checks can share the checker; ordered checks preserve their
individual failures and stop dependent work when a prerequisite fails.

Tool-output observations cover function and custom output events in the selected
turns. A truncation marker or nonzero command exit nominates investigation; it
does not establish unrecovered failure. Zero markers do not establish complete
intake, and quoted markers may be false alarms. Exact section/content/hash checks
belong in the bound workload checker. Unknown output shapes remain visible.
These observations neither change usage coverage nor certify semantic adequacy.
Per-task usage includes only observed responses; whole-task coverage and child
inventory remain controlling when any work is missing. Tool-call events,
output notifications and model responses are different counts.

For a fresh CLI task, `measure --codex-json --stdin-file REQUEST_FILE` accepts
a native `codex exec --json` argv after `--`. Supply the prompt through stdin;
Windows `.cmd`/`.bat` wrappers are rejected. Normal child stderr remains visible.
Timeouts terminate the launched process tree and record failure; cleanup that
cannot be confirmed remains an explicit measurement issue. The wrapper's
temporary raw event file is removed after collection; the source application's
own session retention is unchanged.

Extraction sidecars default to `forseti-harness/memory/logs/efficiency`, already
ignored by Git. `FORSETI_EFFICIENCY_DIR` selects an operational destination.
Records contain metadata, numeric usage and quality evidence; they do not enter
Silver schemas or alter derivation versions. Logging/readback failures are
visible and make the measurement unusable while preserving the original
product result or exception. Archive selected baseline records with the change's
evidence; routine operational records stay outside Git. `repo-size` exposes
their current growth; this command performs no deletion.

### Reusable coordinator closeout sample

The executing helper consumes a released `commands.json`. Execute its argv
arrays using their associated working directories, batch independent commands
and preserve each exit. Report each case's outcome, quality, accounting coverage
and unresolved issue. Use returned facts when they resolve the report; open
saved records when a required fact is missing or contradictory. Do not retry
into an existing destination. Unexpected setup failures require diagnosis.

The source-loading overlay owns this helper's validation reading route. Its
report does not approve the implementation or release a change. Keep fixture
source and `preparation.json` expectations outside its intake unless diagnosis
needs them. The commissioning actor owns preparation in the next section.

This example tests setup and the use of prepared commands. Its synthetic usage
is not real model consumption. It neither checks native chunk delivery nor
reassesses semantic quality; native delivery retains its existing owning tests.
It cannot establish token savings, model superiority or subscription drain.
Real task collection and comparability rules below remain controlling.

### Prepare a coordinator closeout sample

The commissioning actor prepares the existing synthetic example before
launching its helper. From `forseti-harness`:

```text
python tests/fixtures/efficiency_codex_closeout/prepare.py prepare --baseline-root BASELINE_CHECKOUT --candidate-root CANDIDATE_CHECKOUT --output-dir NEW_EXERCISE_DIRECTORY
```

Both roots are complete Git checkouts containing their own measurement runner;
select the intended revisions before preparation. Do not copy selected Python
modules or combine imports across checkouts. Uncommitted candidate edits are
allowed. The capsule retains `harness_diff_sha256` for tracked changes and adds
`untracked_harness_sha256` for the names and bytes of non-ignored untracked
harness files; a filename list alone cannot detect an edit to an existing file.
Ignored files and installed Python packages are outside these fingerprints.
The preparer uses each checkout's real `import-codex` command and records its
source commit. That commit alone does not identify an arm or uncommitted edits;
the capsule and separate destinations preserve those distinctions. It checks
three synthetic completed records in both versions before publishing
`commands.json`. The supplied byte-for-byte checker avoids a separate
Unicode/chunk decoder; it exits 7 only for content that does not match the
frozen bytes and 8 when the saved artifact cannot be read, so a broken setup
stays distinguishable from the intended damaged-content failure in the saved
`quality_return_code` alone.

Only an exit-zero `status: ready` return releases `commands.json` to the executing
helper under "Reusable coordinator closeout sample" above. The local examples
include a useful positive and two distinct failure conditions; a checker that
accepts damaged content must stop preparation rather than make the sample
appear ready.

Preparation and worker observations have different output directories. Reusing
a destination fails instead of overwriting evidence. Failures and process logs
remain in the exercise directory; no worker commands are published after a
failed local check. Reuse preparation only while the fixture, inputs and relevant
checkout state are unchanged, including untracked dependencies. The capsule
identifies observed state; it is not an automatic guard against later edits.
The 30-second child limits bound this small local fixture, not production work.

## Compare equivalent successful work

Keep the same fixture identity, model/settings, environment and quality oracle
across arms. Use at least three matched repetitions per case and alternate the
execution order. `--pair-id` provides explicit pairing; otherwise file order
within each case supplies the pairing and appears in the result. Normal, large
and failure workloads must remain separate cases. Reimporting the same Desktop
task is one observation, not an additional repetition.

The comparator reports `improved`, `regressed`, `inconclusive` or `unmeasured`
for wall time and total tokens. It checks case membership, repeats, configuration,
quality, output fingerprints when present, attempt totals, malformed values and
duplicate observations. It requires consistent paired direction and the stated
materiality threshold (default 5%); this is a screening rule, not a statistical
confidence claim. Mixed resource tradeoffs and insufficient evidence do not
become an overall efficiency win. Unknown tokens do not erase observed timing,
but they prevent a whole-efficiency improvement claim. Failed attempts remain
in costs; a successful retry cannot hide unobserved earlier usage.

OpenAI/Codex input already includes cache reads, and output already includes
reasoning. Anthropic's exclusive input/cache components are combined once.
Missing optional breakdowns stay null; unknown required components cannot
produce a zero total. No dollar estimate is emitted without a separate,
applicable billing basis. References: [Codex non-interactive events](https://learn.chatgpt.com/docs/non-interactive-mode)
and the [OpenAI exec event schema](https://github.com/openai/codex/blob/main/codex-rs/exec/src/exec_events.rs).

## Initial dogfood, 2026-09-05

The adjacent evidence JSON records observations from this implementation lane
based on `91fa10a0f502b79095f9670cdf346156bbdf0c65`; these are measurement
capability checks, not evidence that this change reduces task tokens or latency.

| Complete observed unit | Input | Cached input (included) | Output | Total | Wall seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Earlier completed task with three linked children | 2,078,349 | 1,876,224 | 15,268 | 2,093,617 | 348.474 |
| Live code exercise with independent oracle | 132,306 | 130,176 | 560 | 132,866 | 47.490 |
| Live subscription extraction through persisted Silver member | 242,532 | 234,624 | 911 | 243,443 | 98.735 |

The earlier task's parent alone reported 1,051,960 tokens: omitting children
would hide 1,041,657 tokens. These are inclusive usage counts, not uncached
input counts, context-window size, money or savings.

The recorder-only probe used three alternating pairs of 50 operations each.
Median added cost was 1.155 ms per record, including creation, aggregation,
serialization and the actual sidecar write. Transcript hashing, lake readback,
model calls and production workload latency are outside that overhead figure.

Reusable inputs live in `forseti-harness/tests/fixtures/efficiency_agent/`
(`task.py`, `oracle.py`, `request.txt`) and
`forseti-harness/tests/fixtures/efficiency_transcript.json`. Copy the agent
fixture to an isolated exercise directory before running its request; its
original implementation intentionally fails the independent oracle. The
transcript fixture is synthetic and has no production-representativeness claim.

The code fixture first failed its oracle, then passed ordering, unhashable,
iterator, empty-input and no-mutation checks after the live agent changed only
its implementation. The extraction used the actual production prompt and an
actual model response, followed by the existing `operator_codex_assisted`
parser/writer route into a test lake. It retained one supported Dior/Sauvage/
elixir mention, its exact source quote and 4000–8000 ms span, and a matching
persisted member/marker hash. It includes the subscription agent's preparation
and tool use; it is not a direct API-request timing or token estimate.

Native CLI execution could not be dogfooded here: CLI 0.144.4 rejected the current
configuration, and Windows denied execution of the Desktop-bundled binary.
Both attempts remained failed/unknown, and the existing Desktop route supplied
the real agent runs. Direct API credentials were not configured; provider
accounting and extraction-to-lake behavior were validated using real temporary
lake writes and fixed provider envelopes. No live API efficiency claim follows.

The independent extraction check initially looked in the wrong envelope location,
then incorrectly expected the concentration to be included in the product-line
atom. The preserved record actually separates line `Sauvage` and concentration
`elixir`, as allowed by the production contract. Correcting those oracle
assumptions required no model rerun or product change. The CLI retained the
failed-quality observation, and the final oracle also checks exact quote/timing.

Cheap correctness/accounting checks run in the existing test suite. Live model
comparisons remain explicit experiments. Full creator onboarding, capture, ASR
and whole-CI optimization claims require their own complete-workflow evidence;
this implementation does not infer them from the cases above.
