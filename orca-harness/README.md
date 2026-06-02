# Orca Harness

Step A rebuild of the v0.14 deterministic judgment harness.

This package is intentionally narrow:

- deterministic mapping and scoring only;
- fixed disk-backed TR/Casetext plumbing fixture only;
- local source-observability support checks only, not source acquisition;
- local dry memorization-probe receipt normalization only, not provider
  execution;
- opt-in raw-API no-tools memorization-probe execution plumbing only, not
  probe authorization;
- append-only scoring results and failure-event logging;
- explicit non-claim boundary: `plumbing works only; not judgment quality`.

The source-observability helper reports visible capture limitations in local
records. It does not fetch sources, retrieve archives, automate browsers, call
APIs, score source quality, validate Data Capture, or authorize downstream ECR,
Cleaning, or Judgment behavior.

## Source Capture Packet

Use the source-capture runner when an operator already has local source files
and needs a no-network packet directory with a manifest, preserved raw files,
SHA256 hashes, posture metadata, and a human-readable receipt:

```powershell
python runners/run_source_capture_packet.py --source-family "docs_page" --source-locator "C:\capture\vendor_pricing_page.html" --decision-question "What did the pricing page show before the decision cutoff?" --input-file "C:\capture\vendor_pricing_page.html" --source-publication-or-event "pricing page date visible in local artifact" --cutoff-posture "pre-decision local capture artifact" --access-posture "local_file_only" --archive-history-not-attempted-reason "local CLI does not query archives" --media-modality-not-attempted-reason "local CLI does not retrieve additional media" --output ".\_test_runs\example_source_capture_packet"
```

This first checkpoint is local-file-only. It does not fetch URLs, call APIs,
query archives, automate browsers, preserve additional media, or decide
credibility, inclusion, Signal Use, Decision Strength, Action Ceiling, buyer
proof, or commercial readiness.

Optional metadata flags let the operator carry already-known source timing,
cutoff, archive, media, actor, mode-change, access, and re-capture posture into
the packet. Omitted fields stay visible as unknown, not attempted, or not
applicable rather than disappearing.

For the packet directory shape and receipt details, see
[`docs/source_capture_packet.md`](docs/source_capture_packet.md).

Use the Direct HTTP runner when one ordinary HTTP URL should be captured into
the same packet shape:

```powershell
python runners/run_source_capture_http_packet.py --url "https://example.com/page" --decision-question "What did the page return before the decision cutoff?" --cutoff-posture "pre-cutoff direct HTTP capture requested by operator" --output ".\_test_runs\example_source_capture_http_packet"
```

This runner is still deliberately narrow. It uses stdlib `urllib` only, follows
normal redirects, preserves the raw response body plus provenance-safe response
metadata, and fails visibly on timeout, DNS/TLS failure, empty-body response,
or byte-cap breach. It does not use browser automation, API SDKs, archive
retrieval, media fetching, scraper frameworks, proxy/auth/session injection,
ECR logic, Cleaning, Judgment, buyer proof, or commercial-readiness logic.

Dry-run packet outputs under `reports/source_capture/` are local review evidence
unless a separate fixture-admission decision says otherwise. They can include
machine-specific `original_path` provenance values and copied raw source files;
do not treat them as canonical fixtures merely because they sit under
`reports/`.

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

Build a local dry memorization-probe receipt from pre-supplied probe input and
response files:

```powershell
python runners/run_memorization_probe.py --probe-input <probe_input.yaml> --raw-response <raw_response.yaml> --output <probe_receipt.yaml>
```

This runner does not call a model, provider SDK, browser, network, search, or
participant packet. It only normalizes local inputs into the v0.14
`contestant_execution_isolation` receipt shape and applies local gate
interpretation. A clean gate still requires structural no-tools evidence under
the v0.14 no-tools execution contract; prompt-only "do not search" language is
not enough.

Run an explicitly authorized raw-API no-tools memorization probe:

```powershell
python runners/run_memorization_probe_raw_api.py --probe-input <probe_input.yaml> --output <probe_receipt.yaml> --provider <openai_responses|anthropic_messages> --api-url <provider_url> --api-key-env <ENV_NAME> --allow-live-provider-call
```

The raw-API runner uses no provider SDK and requires the live-call flag so an
operator cannot accidentally call a model while doing local validation. Clean
no-tools isolation is limited to the standard OpenAI Responses endpoint and
Anthropic Messages endpoint named by the runner; arbitrary proxy or provider
URLs are rejected for clean isolation. The runner rejects request bodies with
tool, search, retrieval, browser, file, attachment, workspace, system,
developer, or hidden-context fields, and the receipt `raw_response_hash` covers
the full provider response body. The runner is still only execution plumbing;
using it for a real probe requires separate owner authorization for the exact
model/case pair.

No-case provider smoke tests are also non-gate-clearing. Before passing
`--allow-live-provider-call` for a synthetic smoke test, follow
`../docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md`
and capture the required out-of-band execution provenance. A smoke receipt must
not be cited as a clean memorization-probe pass for any real model/case pair.

## Generated TR/Casetext Scores

The runner writes score files under
`cases/plumbing/tr_casetext_2023_v0_14/scores/` and failure-event logs under
`memory/logs/`. Those paths are local generated outputs and are ignored by git.

If a generated score already exists for the same `(case_id, run_id,
contestant_id)` tuple, the runner refuses to write another score unless
`--allow-duplicate-score` is passed. Commit generated scores only under a
separate fixture-admission decision.
