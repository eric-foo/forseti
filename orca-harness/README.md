# Orca Harness

Step A rebuild of the v0.14 deterministic judgment harness.

This package is intentionally narrow:

- deterministic mapping and scoring only;
- fixed disk-backed TR/Casetext plumbing fixture only;
- local source-observability support checks only, not source acquisition;
- append-only scoring results and failure-event logging;
- explicit non-claim boundary: `plumbing works only; not judgment quality`.

The source-observability helper reports visible capture limitations in local
records. It does not fetch sources, retrieve archives, automate browsers, call
APIs, score source quality, validate Data Capture, or authorize downstream ECR,
Cleaning, or Judgment behavior.

## Source Observability Runner

Use the source-observability report runner when an operator has already authored
local posture records and wants a structured list of visible capture
limitations:

```powershell
python runners/run_source_observability_report.py <records.yaml> --output <report.json>
```

The input must be local YAML or JSON containing either a list of
`SourceObservabilityRecord`-compatible records or a mapping with `records`.
Those records are operator-authored observations, not extracted source truth.
The report output is support evidence for reviewing source-language,
source-structure, archive-body, media, access, locator, and cutoff limitations.

The report is not capture validation, capture readiness, categorical ECR
receipt, Cleaning output, Judgment output, source acquisition, archive
retrieval, browser automation, or source-quality scoring. Do not treat it as a
required capture gate or as proof that the underlying capture is complete.

For record-authoring guidance, see
[`docs/source_observability_operator_records.md`](docs/source_observability_operator_records.md).

## Commands

Run tests:

```powershell
python -m pytest -p no:cacheprovider
```

Run the TR/Casetext plumbing fixture from this directory:

```powershell
python -m runners.run_case cases/plumbing/tr_casetext_2023_v0_14
```

The script-style entrypoint is also supported:

```powershell
python runners/run_case.py cases/plumbing/tr_casetext_2023_v0_14
```

If a score already exists for the same `(case_id, run_id, contestant_id)`, the
runner refuses to write a duplicate unless `--allow-duplicate-score` is passed.
Mapping-version mismatches are a separate override:
`--allow-mapping-version-mismatch`.

## Canonical TR/Casetext Scores

The canonical fixture keeps one active score file under
`cases/plumbing/tr_casetext_2023_v0_14/scores/`. Extra score files created
during Step A debugging and review are archived under that directory so the
case report stays compact while the audit trail remains available.

Archived scores are not active report inputs and do not block a new run. If an
archived score matches the same `(case_id, run_id, contestant_id)` tuple, the
runner emits a warning so the operator can see that prior audit history exists.
