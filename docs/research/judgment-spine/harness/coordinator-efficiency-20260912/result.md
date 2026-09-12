# Coordinator efficiency samples — 2026-09-12

```yaml
retrieval_header_version: 1
artifact_role: Bounded implementation and dogfood record
scope: Coordinator return serialization and batched completed-task verification/accounting; bounded dogfood and unproven subscription impact.
use_when:
  - Assessing the coordinator-efficiency candidates, their behavioral evidence and measurement limits.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/coordinator-efficiency-20260912/measurement.json
```

The latest follow-up combines completed-task verification, accounting and saved
record readback in the existing importer. The earlier importer comparison's
final Astra/high coordinator completed three contrasting assessments in **one
post-intake tool round**, versus three for the baseline. Subscription-drain
savings remain unproven. The
follow-up contract and observations below supersede the earlier serialization
candidate as the behavioral-efficiency recommendation. The owner authorized a
fresh confirmation and conditional PR merge on 2026-09-13. Publication is scoped
to batching and reliable comparison setup; the serialization experiment is
excluded from the proposed production change.

The fresh post-review setup confirmation passed all six cases with no setup
repair or command retry. It used **402,161 native tokens versus 197,899** in the
previous successful setup sample, with eight tool rounds versus four. Extra
instruction reads and a baseline-only diagnostic read remain visible below.
This confirms the bounded setup/reporting behavior, not overall coordinator
efficiency or subscription savings.

## Earlier serialization candidate

The candidate preserves the complete `advance` return and removes JSON
indentation. Seven genuine CLI boundaries shrink from **85,886 to 81,211 UTF-8
bytes** (LF-normalized): **4,675 bytes / 5.44%**. Every parsed value and the final
native consumer view match. **Subscription quota savings are unproven. I would
not land this change solely as a quota-efficiency fix on this evidence.** The
serialization implementation and its two guidance additions have been removed
from the publication candidate; these historical measurements are preserved.

The initial baseline was already compact in substance: ready returns were mostly
complete generated worker instructions. Removing transitions would lose earlier
reconciliation-level bindings that the current artifact map does not retain.
There was no justified bulk-removal formatter or new artifact store to build.
That first candidate changed only serialization in the public CLI; the two actual
consumer guidance sources say to parse once, forward full worker prompts
unchanged, and load complete relevant evidence for source-dependent judgment.
Worker intake, schema, raw-write/submit instructions, immutable publication,
selection, grouping, default authoring and the 60-second wait ceiling are unchanged.

| Native boundary | Before bytes | Candidate bytes |
| --- | ---: | ---: |
| Ready extraction | 15,021 | 14,445 |
| Unchanged pending extraction | 15,020 | 14,444 |
| Invalid response, exit 2 | 8,933 | 8,404 |
| Verification ready | 16,292 | 15,597 |
| Reconciliation level 1 | 11,355 | 10,667 |
| Reconciliation level 2 | 12,365 | 11,566 |
| Completed view | 6,900 | 6,088 |

The sample reused the existing four-leaf alternate `_advance_replay_fixture`
with method v13, `input_order`, authoring v4, 30,000 prompt bytes and two
evidence items per work unit. These are deterministic native-valid fixture
answers, **not fresh generation or saved model-authored judgments**. Each arm
submitted six unchanged answers through native intake and immutable submission,
then read back the same accepted view and response hashes. One deliberately
invalid response was preserved outside the response directory before replaying
the valid answer in each arm. That equal preparation intervention does not
establish autonomous operator-rescue performance. The invalid return retained
its exact filename/batch-identity error, nonzero exit, and another ready request.

The implementation coordinator read the complete materialized source and view:
all four fixture leaves say “I did not find the balm drying during winter use.”
The view preserves that negation, winter condition, `descriptive_only` ceiling,
`not_checked` conflict and unavailable capture completeness. Completion therefore
does not support the opposite drying claim or global absence of opposition.
This is a bounded fixture assessment, not independent semantic qualification;
the historical neutral/approval/price campaign was not rerun because serialization
does not alter any of its evidence or judgment inputs.

One Astra/high baseline coordinator replay launch failed on local Codex
configuration loading before generation. Authentication was not determined;
no model usage or provider response exists. After the owner clarified subscription
percentage drain as the economic target, the source coordinator instructed this
task to avoid additional attempts merely for API price comparison. The candidate
arm was not launched; the owner had not revoked the small dogfood authorization.
There is no measured token, Codex-credit, API-cost or quota delta. The
coordinator-supplied verified Codex credit rates are preserved only as an unused
proxy in [measurement.json](measurement.json); they do not establish a
mapping to this Pro account's usage percentage. Account-wide percentage changes
would also be confounded by another active task.

Focused advance/job/worker tests and the 18 harness coupling contract tests
exited zero. The real candidate replay passed exact parsed-state comparison at
all seven boundaries, native receipt readback and final view byte equality.
Preparation, development and this report are outside the recurring sample
denominator; their cost was not measured. No extra model worker, judge, helper,
repair or compaction was launched. No independent review, publication or landing
was performed. Full CI remains a publication concern for the source task.

The managed worktree is `C:/Users/vmon7/.codex/worktrees/f8e7/forseti`, branch
`codex/coordinator-efficiency-20260912`, initially clean at required baseline
`307e149ae80075e115abfd543e7ec4a43964166e`, with no other writer observed. The
advisory diagnosis and corrected measurement hashes matched and those files
were not edited. Exact inputs, source pins, errors, counts and raw artifact
pointers are in the measurement. Raw sample files remain under the worktree's
ignored `forseti-harness/_scratch/coordinator-efficiency-20260912/`; preserve
that directory for raw replay inspection. The record is stale for changed
serialization, worker transport, fixture bytes or quota-meter semantics.

Completion remains owned by source task `01a0955a-643a-7dc1-b747-da71e35b40f7`.
The unresolved outcome is lower subscription drain for the same completed unit;
the verified outcome here is only lossless, smaller coordinator delivery.


## Coordinator batching follow-up: success contract

Authorized 2026-09-12 by the owner: deep-think the smallest complete fix,
success-implement it, and dogfood a sample. The target is the same managed
worktree, initially clean at `cd184bdbd7dc2df6e2c99c4fcd94fdc5f461bad9`;
its earlier implementing task was observed idle. The current coordinator is
the sole source writer. Publication remains held.

Goal: remove extra coordinator resumptions needed to collect already-known
verification and accounting facts for a completed task. Extend the existing
`import-codex` return and route its use; no new batch framework or recurring
measurement obligation. Authority: current owner instruction, AGENTS SCI,
overlay decision-routing/validation-gates, and the existing efficiency owners.
Keep task/child completion boundaries, response de-duplication, quality-checker
exit status, unknown coverage, full durable records, source evidence, model
choice and the fixed wait constraint intact. Semantic judgment remains outside
the mechanical checker. No production-cycle or subscription-% claim follows
from a small closeout sample.

Signals (planned before source edits):
- Given a frozen completed native task and its bound result checker, one
  importer invocation exposes the observed usage, unique model-response count,
  tool-call events, model/effort, diagnostic observations, checker status/exit
  and historical completion interval. Compare against the old collector and
  frozen independently authored accounting/intake verification.
- Given a missing usage row or damaged intake, keep incomplete coverage or the
  checker's failure visible in that same return. A passing checker must not
  repair missing accounting; complete accounting must not repair failed quality.
- Preserve both function and custom tool-output observations, and do not treat
  ordinary discussion of truncation as a truncation marker. Marker observations
  are diagnostic only; exact intake preservation needs the bound checker.
- Reimporting a task remains the same observation and cannot overwrite an
  existing record. Baseline and candidate use identical saved work and checker;
  fresh coordinators use Astra/high. A fresh tie is a tie, even if history had
  missed batching. Count all sample calls, failures and recovery separately
  from implementation/preparation. No model downgrade or quota conversion.

Review checkpoint: the repository's conditional success-implement predicate
in `delegated-review-patch.md`. Independent baseline/native observations must
support affected boundaries; otherwise route the remaining uncertainty through
an operator-courier review prompt before any landing.


## Follow-up observed outcome

The smallest complete intervention extends `run_efficiency import-codex` rather
than installing another batch runner. The existing workload checker runs in the
same invocation as accounting; the returned summary now includes unique response
counts, observed settings, per-task usage, tool-call counts, output diagnostic
observations, quality exit/status and the historical interval. Before returning,
the importer rereads the saved JSON and compares it with the collected record.
A mismatch exits 2 without a successful readback claim. That last check was
necessary: the first candidate still made the coordinator spend a separate round
on required persistence verification.

The operational guide and the overlay's Orchestrator Context Economy section now
route this combined use only when measurement is commissioned. The recurring
cost is one local saved-record read within that existing operation; it catches
persisted-record mismatch and replaces a model resumption. No new registry,
reporting obligation, semantic judge, model default or wait policy was added.

Both baseline and final candidate used the same saved completed Sol/high worker
record and checker, plus two deliberate perturbations. The valid record retained
all 9 intake sections / 13 chunks / 63,321 UTF-8 bytes and the saved response.
Removing a usage row left quality passed and accounting unknown; removing an
interior intake chunk while retaining the final marker made the checker fail
with exit 7 while accounting remained complete. Candidate PowerShell/tool
wrappers reported outer exit 1 for that failure and preserved checker exit 7;
the importer invoked directly returned 7. Semantic adequacy was not reassessed.
Both fresh coordinators made the correct three-way assessment. Reimport could
not overwrite the prior observation (exit 2). A separate seeded persisted-record
corruption failed after a passing checker, proving the new readback boundary
rather than an unrelated earlier guard.

| Completed fresh Astra/high coordinator | Model responses | Tool rounds | Post-intake rounds | Input (cached subset) | Output | Total tokens | Elapsed seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 6 | 5 | 3 | 253,882 (222,080) | 2,453 | 256,335 | 115.068 |
| Intermediate candidate | 5 | 4 | 2 | 188,139 (175,232) | 1,288 | 189,427 | 68.596 |
| Final candidate with checked readback | 4 | 3 | 1 | 145,995 (100,480) | 1,058 | 147,053 | 53.631 |

The final native trace shows two intake/help rounds followed by one invocation
that batches all three case commands; it ends without reopening the records.
The baseline instead runs the importer, reads the records, then scans the native
logs for remaining accounting facts. This is evidence that the actual consumer
used the complete return. All coordinator tasks finished before collection;
response identities and cumulative counters reconcile, and metadata discovery
found no child tasks to add.

The raw token reduction is descriptive: autonomous source loading differed
(the baseline also read safety/claim-support sources), and cache fractions
changed. Final-candidate uncached input was **45,515**, versus **31,802** in the
baseline despite lower total input. There is no isolated cost-effect estimate,
Pro usage-percentage mapping, production-cycle proof or broad optimality claim.
The behavior result supports this bounded fix before considering a model change.

Sample setup failures remain in the record. The first model baseline stopped
on a missing unchanged baseline dependency and consumed **197,824 tokens**.
The host checker also initially mishandled section-end framing and JavaScript
UTF-16 offsets; the original native protocol resolved both before the fresh
comparison. All four model attempts, including setup failure and the intermediate
candidate, consumed **790,639 total tokens**. These are complete sample costs;
the active implementation coordinator and deterministic preparation are separate
and are not represented as a completed whole-work-unit saving.

Validation: 62 affected tests covered across the initial focused run and final
33-test runner run; 95 coupling/comparison/foundation checks passed. The original
native accounting and intake-verification records supplied independent expected
values. A second historical native trace independently produced two truncation
observations across five output events; those observations did not falsely turn
complete accounting into failed usage. No broad CI or publication was performed.

`review_routing_status: not_needed` under the repository's conditional
success-implement rule: the affected extraction/return, failure separation and
persistence boundaries have the native observations, preserved baseline,
contrasting cases and direct readback evidence above. No independent review is
claimed. Propagation was checked through AGENTS/CLAUDE, overlay source loading
and validation, the repo-map efficiency row and the efficiency README. Their
existing guide pointers remain correct; the scoped overlay route and owning
guide carry the change. No stale instruction requiring separate metric scans
was found in those routers.

The adjacent measurement preserves exact source paths/hashes, completed task
identities, counters, case records, checker/bridge source, setup failures and
raw artifact locations. It is stale if the importer/collector, checker, source
records, platform event format or coordinator instructions change. Full private
native logs remain host-local; this is a bounded evidence record, not a portable
operational archive. Publication remains held; subscription drain is unresolved.

## Reusable comparison setup: success contract

Authorized 2026-09-12: success-implement the proposed reusable coordinator
comparison setup and dogfood one sample. Existing managed worktree, HEAD
`cd184bdbd7dc2df6e2c99c4fcd94fdc5f461bad9`, retains the eight earlier modified
files. The current coordinator remains the sole source writer; publication is
held. Source owners: AGENTS SCI, the existing efficiency guide/runner and the
repository's conditional success-implement review policy.

Goal: a fresh coordinator can run the prepared comparison without rebuilding
dependencies, paths or output interpretation. Add a synthetic executable fixture,
its tests and the existing guide route. Preserve earlier failed sample artifacts,
real usage/quality separation, complete-run accounting and production behavior.
No model/default change or whole-cycle/quota saving is commissioned.

Signals planned before implementation:
- Two complete selected checkouts execute their own real measurement command;
  valid saved content has complete usage, one absent response leaves usage
  unknown, and middle-damaged content fails with its final marker retained.
- A nested root and an actual missing Python dependency fail before worker
  commands are published. The missing-dependency test isolates Git admission
  so it must reach the intended interpreter import failure.
- A deliberately permissive checker cannot turn the damaged case into ready
  setup. Its process must actually exit zero before preparation rejects the
  incorrect success, excluding an unrelated earlier-guard explanation.
- Prepared commands use distinct worker destinations; repeat preparation and
  repeated imports cannot overwrite prior evidence. Unicode is checked by exact
  saved bytes, avoiding another implementation of the native chunk protocol.
- Only after local checks succeed, one fresh Astra/high coordinator receives
  the prepared capsule and reports the six results without constructing setup.
  Freeze the expected case distinctions before reading its response. This is
  an autonomous-use observation, not a model comparison or savings estimate.

The reusable example did not exist at intake (`Test-Path` false); there is no
fabricated pre-change red run. Existing preserved setup failures supply the
historical baseline. Direct counterexamples, two-checkout execution, established
collector behavior and the fresh consumer observation must support the affected
boundaries; any remaining material shared-assumption gap routes to an
operator-courier review prompt under the repository's conditional rule.

## Reusable comparison setup: observed result

Implemented the reusable synthetic example at
`forseti-harness/tests/fixtures/efficiency_codex_closeout/prepare.py`, with five
tests and the existing efficiency guide's "Reusable coordinator closeout sample"
route. Each complete checkout runs its own real measurement command. All six
local checks must agree with the frozen cases before worker commands are released.
This removes the need to rebuild the dependency/path/checker setup for each such
comparison. Its recurring cost is six small local commands per new preparation;
it adds no standing step to production intelligence work.

Validation: **85 passed** (5 new setup tests, 62 existing affected unit tests,
18 required coupling contract tests), no failures/errors/skips. The new tests
exercise real import failure, a checker that incorrectly accepts damaged content,
exact Unicode bytes, separate destinations and refusal to overwrite evidence.
The pre-existing failed attempts and their accounting remain above and in
`measurement.json`; none were replaced by the successful follow-up.

One fresh Astra/high coordinator completed task
`01a09620-92cc-79f1-9194-dbf0af927a32`, turn
`01a09620-93c9-74e3-a90c-d450fd35e61d`. The native public trace shows three intake
tool rounds followed by one parallel batch of all six supplied commands. There
were no sample setup errors or retries. Direct readback of all six saved records
matches the returned summaries:

| Case, in both checkouts | Exit | Quality | Usage coverage | Synthetic total |
| --- | ---: | --- | --- | ---: |
| Valid saved content | 0 | Passed | Complete | 36 |
| One usage response missing | 0 | Passed | Unknown | 23 observed |
| Middle damage, final marker retained | 7 | Failed | Complete | 36 |

The missing-usage case retained `turn_cumulative_reconciliation_failed`; both
damaged cases retained `saved_content_mismatch`. All three candidate returns
also reported matched durable readback. The two exit-7 results are intended
failures, not setup errors. The generic tool-output counter does not see these
nested exits; direct parsing of the six public command results does.

The completed coordinator itself used **197,899 native tokens** across five
responses: 196,592 input (169,984 cached, included within input) and 1,307 output
(342 reasoning, included within output). Per-response sums reconcile with the
final native cumulative counters; the collector reports complete coverage, no
issues and no linked children. Observed start/end timestamps span 65.158 seconds.
This boundary excludes the still-active implementation coordinator and all earlier
attempts. The synthetic totals in the table are not additional model consumption.

Review routing: `not_needed` under the repository's conditional rule. Independent
runtime import failure, deliberately incorrect checker success, frozen literal
bytes, actual two-checkout execution and the fresh consumer's native trace support
the affected boundaries. No additional review task was launched.

This proves that one fresh coordinator could use the prepared route and preserve
both failure distinctions. It does not establish subscription savings, semantic
quality or reliability across the whole intelligence cycle. The two checkout
versions include other historical differences, so their outputs are not an
isolated causal comparison. Preparation must be regenerated after relevant source,
input or dependency changes; it records observed state rather than enforcing
future immutability. Source hashes, exact checkout revisions, test reports, native
accounting and all six saved-record fingerprints are in
`measurement.json` under `setup_followup`.

Implementation is present in the managed worktree. Publication remains held;
this follow-up has not been pushed or merged.

Correction, 2026-09-12: the paragraph above previously read "has not been
committed, pushed or merged". That was true when written and false at the
reviewed state: the batching and reusable-setup work is checkpointed in this
worktree as commit `21b59c43a8da6cac4f81626685966b5d0339b3e6` on branch
`codex/coordinator-efficiency-20260912`. Nothing was pushed or merged and
publication is still held.

## Reusable comparison setup: delegated review pass

The external reviewer reported Anthropic / Claude lineage and reviewed the
OpenAI-authored checkpoint `21b59c43`. The returned patch and its original
measurement are preserved under the adjudication evidence directory named in
`measurement.json`. The reviewer's findings and test claims are historical
proposal evidence; the home disposition below owns the final retained changes.

## Reusable comparison setup: home adjudication (2026-09-13)

| Finding | Decision | What remains |
| --- | --- | --- |
| F-1: unreadable content shared the damage exit | Accept | Unreadable artifacts persist exit 8; actual byte mismatch remains 7. |
| F-2: untracked harness changes were missed | Modify | Hash filenames AND contents. A real same-name, same-length content edit defeated the reviewer's status-only patch. Keep `harness_diff_sha256`; add `untracked_harness_sha256`. |
| F-3: missing source revision | Accept, narrow the claim | Records retain the source commit. Arm and dirty-state identity still come from the capsule and separate destinations. |
| F-4: stale uncommitted claim | Accept | The dated checkpoint correction above remains. |
| F-5 in chat / F-6 in reviewer JSON: extra private-save guard | Reject | The supported entrypoint already refuses an existing exercise directory. Remove the redundant guard/test and clarify the helper's scope. Public no-overwrite checks remain. |

Final verification: **86 passed** (6 setup, 62 existing affected unit, 18 coupling
contracts), no failures/errors/skips. The added real-Git content-change test first
failed for the intended unchanged-binding result against the reviewer builder,
then passed after correction. One review-added private-helper test was removed;
that explains the difference from the reviewer's 87-test total.

The final prepared commands reproduced all six outcomes (0, 0, 7 in each arm).
Repeated import exited 2 and preserved all prior saved records. A temporarily
missing artifact produced exit 8 in both arms' saved records; its original bytes
were restored afterward. All six saved input files remain byte-identical to the
original sample. These are local command checks, with no additional AI sample.

The three source/test/guide fingerprints, raw counterexample, test reports, eight
saved consumer records and original reviewer return are linked under
`setup_followup.home_adjudication`; its `operator_closeout_source` is the current
compact closeout. Earlier source hashes and the original completed-coordinator
accounting remain historical evidence for their original revision.

No material issue remains open within this five-file commission. The setup still
does not fingerprint ignored files or installed packages, enforce later state,
or support flattening both arms into one directory. Generic checker-output
persistence and record naming belong to the unchanged measurement runner. The
final patch has no new live-model observation, full-harness or broad-CI claim,
and establishes no subscription saving or whole-cycle reliability conclusion.

At adjudication closeout the base checkpoint was `21b59c43` and the reviewed
changes were uncommitted. Publication and another model observation were held
at that stage. The owner's subsequent measurement-and-merge request supersedes
that hold under the bounded confirmation below.

## Post-review confirmation: success contract (2026-09-13)

Decision: land the reviewed setup and batched importer if a fresh coordinator
can use the prepared six commands without setup repair, retries or lost failure
visibility, and required PR checks pass. Exclude the earlier serialization
candidate from production; retain its measured history. No model downgrade is
part of this change.

Freeze one fresh Astra/high coordinator with no inherited author discussion,
fixture implementation or expected answers. Give it the prepared command
capsule and applicable operating sources. It reports each observed outcome,
quality and accounting coverage. Host-side expectations remain 0/0/7 exits and
complete/unknown/complete coverage in each arm; missing response usage must not
be silently counted complete and damaged bytes must fail quality. Six local
preparation checks must pass before launch. Use fresh worker destinations.

Measure completed native responses, intake and work tool rounds, setup errors,
repairs, retries, elapsed time and token counters. Compare with the previous
successful setup sample (one work batch, three intake rounds, zero repairs or
retries, five responses, 197,899 total tokens). A tie is a valid confirmation;
do not substitute the earlier setup failures as a baseline to claim improvement.
This is one fresh confirmation against a historical reference, not a randomized
new A/B or an independent six-run replication. Context/cache differences prevent
a causal token-saving conclusion. Estimated cost is one actor, about five
responses and 150–220k aggregate input plus 1–2k output tokens; no further sample
is needed once the bounded decision is resolved. Synthetic imported usage stays
separate from native actor usage and active-parent/whole-work-unit consumption.

## Post-review confirmation: observed result (2026-09-13)

The fresh Astra/high actor completed the six commands in one parallel batch at
source revision `6474ea817c9890f4601431b3250e30506810c847`. Every saved observation
matched its host-side expectation: valid content passed; missing response usage
remained unknown; damaged content failed with exit 7. All three candidate
returns reported matched durable readback. Setup errors, setup repairs and
command retries were zero. All six input files matched the historical sample.

| Completed coordinator observation | Previous successful setup | Fresh confirmation |
| --- | ---: | ---: |
| Instruction-intake tool rounds | 3 | 6 |
| Work tool rounds | 1 | 2 |
| Parallel command batches / commands | 1 / 6 | 1 / 6 |
| Setup repairs / command retries | 0 / 0 | 0 / 0 |
| Native responses | 5 | 9 |
| Native input tokens (cached subset) | 196,592 (169,984) | 400,469 (362,112) |
| Native output tokens (reasoning subset) | 1,307 (342) | 1,692 (167) |
| Native total tokens | 197,899 | 402,161 |
| Elapsed seconds | 65.158 | 82.277 |

The additional work round read only the baseline records to resolve accounting
details absent from the old return. The candidate needed no separate record
read. The three additional intake rounds loaded validation instructions; one
oversized request was rejected and repeated with a larger bound. Thus there was
**one instruction-read retry**, despite no setup-command retry. That avoidable
intake failure must not disappear into a zero-retries claim.

Observed native use increased by 204,262 tokens (103.22%). The prompt and loaded
context differed, including a request to report unresolved issues in both arms;
this is not a causal estimate of patch cost. It is evidence against calling
coordinator behavior efficient overall. Setup reliability tied the previous
success. No model downgrade, subscription-drain conclusion or whole-cycle
reliability claim follows.

The complete native boundary is task `01a09687-b8da-7e10-ae42-04a518c7e6bb`, turn
`01a09687-ba01-7ec1-a82b-c07eefd55f4d`, from
`2026-09-12T16:51:13.082Z` to `2026-09-12T16:52:35.359Z`, with nine response
records and no discovered descendants. The active parent and earlier attempts
are excluded. Source hashes, public calls, raw accounting and all six saved
records are bound in `measurement.json` under `post_review_confirmation`.

Landing decision: the tested setup and importer behavior are useful and meet
their frozen acceptance conditions; proceed with the bounded PR if required
checks are green. The total-cost regression remains explicit. This work unit
does not expand into another instruction-policy fix or launch another sample.
Publication and merge state belong to the PR's fresh remote readback.
