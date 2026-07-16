# Tool-Calling Dogfood Run — 2026-07-15 Cold-Agent Baseline

```yaml
retrieval_header_version: 1
artifact_role: Observed workflow-efficiency dogfood record
scope: Three isolated cold-agent runs of the fixed stale vendor-admission case, with correctness and end-to-end tool-economy findings.
use_when:
  - Reviewing the first observed baseline for tool_calling_dogfood_case_v0.
  - Distinguishing agent reasoning quality from recurring tool-substrate latency and failure.
authority_boundary: retrieval_only
branch_or_commit: fixture-local baseline 5bceef83b877ca37efc9a4f9dec98bb7563bef12
open_next:
  - docs/workflows/efficiency/tool_calling_dogfood_case_v0.md
  - docs/workflows/technical_difficulties_log_v0.md
```

## Use boundary

This record reports one three-run observation made on 2026-07-15. The fixed case
owns the scenario and oracle; Technical Diagnostics owns the recurring tooling
failure. This record does not establish a general model, harness, or tool-quality
benchmark.

## Fixed run setup

- Three separate local Git clones used the same oracle-free minimal fixture and
  fixture-local baseline commit shown in the retrieval header.
- Each agent started with `fork_turns=none` and received only the case courier
  plus its assigned snapshot path.
- The focused baseline passed; broader discovery failed only in the fixed
  unrelated export test.
- `notes/operator_draft.md` began untracked with SHA-256
  `E7025234292F8FD6FF7C0274B14B35A29184DC53186C103EAAA1A54586C40612`.
- After all three turns made no file change for several minutes, the operator
  interrupted them and applied the same non-oracular recovery instruction:
  bound waits, do not repeat an unchanged hanging call, and use bounded
  elevation when the scratch snapshot is sandbox-blocked.

## Observed results

| Run | Correct patch | Focused | Broader result | Note preserved | Logical rounds | Total tool invocations |
| --- | --- | --- | --- | --- | ---: | ---: |
| 1 | yes; three intended files | pass | fixed unrelated failure only | yes; same hash, untracked | 23 | 41 |
| 2 | yes; three intended files | pass | fixed unrelated failure only | yes; same hash, untracked | 22 | 35 |
| 3 | yes; three intended files | pass | fixed unrelated failure only | yes; same hash, untracked | 20 | 31 |

Fresh operator verification confirmed that every run changed only
`config/vendor_admission.yaml`, `src/vendor_adapter.py`, and
`tests/test_vendor_adapter.py`; selected `discovery_only`; retained both
provenance fields; kept registry admission disabled; passed `git diff --check`;
and preserved the unrelated failure and untracked-note hash.

Under the case rubric, each run scored **90/100**: correctness 45/45, evidence
20/20, patch completeness 15/15, failure integrity 10/10, and observed
end-to-end tool economy 0/10. The economy score describes the combined agent,
tool, and sandbox path; it is not an agent-only quality judgment.

## Findings

1. **Recurring critical tool-access failure (3/3).** Default shell calls against
   the assigned `C:\tmp` snapshots hung, including trivial diagnostic probes.
   Equivalent bounded elevated shell calls completed. Operator interruption was
   required before any run edited a file.
2. **Recurring critical edit-route failure (3/3).** The nested `apply_patch`
   route hung. Attempts to invoke its launcher or executable through elevated
   shell failed with access denial. Every run eventually required a `git apply`
   fallback.
3. **Fallback fragility (3/3).** Each first Git-patch fallback was malformed or
   mismatched and failed atomically before a corrected patch applied. The atomic
   failure preserved integrity, but added serial recovery rounds.
4. **Secondary batching gap.** Each ledger identified roughly two to four
   consolidatable read or verification rounds. That is real but materially
   smaller than the shared shell/edit-path failure.
5. **No correctness or failure-integrity gap observed.** All runs found current
   authority, produced the same semantic patch, and kept the unrelated failure
   visible.

## Decision and rerun trigger

- Record the recurring tool failure in Technical Diagnostics.
- Tighten the case reset instruction so the cold snapshot cannot contain its
  operator-only oracle.
- Add no checker, benchmark runtime, fixture package, or workflow doctrine from
  this one baseline.
- Rerun the same three cold trials after the default shell/edit route is fixed
  or materially changed. Improvement means preserving the 90 correctness and
  integrity points while returning near the case's five-round reference route.

## Non-claims

- Not proof of root cause in the sandbox, shell host, patch helper, or agent.
- Not a general comparison among models or harnesses.
- Not validation that every elevated call is necessary or safe.
- Not authority to normalize elevation as the default operating route.
- Not product, runtime, vendor, or repository readiness.
