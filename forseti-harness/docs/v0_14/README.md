# v0.14 Source Anchor

This package implements the frozen v0.14 specs under:

- `docs/research/judgment-spine/harness/v0_14/`

The local code is the executable Step A rebuild. The docs remain the design authority.

Local runner pointers:

- `runners/run_case.py` executes the deterministic fixed-case scoring path.
- `runners/run_memorization_probe.py` builds a dry local memorization-probe
  receipt from pre-supplied probe input and response files. It implements the
  local receipt and gate-interpretation shape for
  `contestant_no_tools_execution_contract_v0.md` and
  `memorization_probe_protocol.md`; it does not execute a live model, call a
  provider, fetch sources, expose participant packets, score outputs, freeze a
  ledger, admit a fixture, or prove judgment quality.
- `runners/run_memorization_probe_raw_api.py` is the opt-in raw-API no-tools
  execution path for an already authorized memorization probe. It uses a direct
  provider HTTP request with no SDK imports, limits clean isolation to standard
  OpenAI Responses and Anthropic Messages endpoints, rejects arbitrary proxy or
  provider URLs, and rejects request bodies that expose tool, search, retrieval,
  browser, file, attachment, workspace, system, developer, or hidden-context
  fields. Its `raw_response_hash` covers the full provider response body. It
  does not itself authorize a probe, expose participant packets, score outputs,
  freeze a ledger, admit a fixture, or prove judgment quality.
- No-case smoke tests for the raw-API runner are plumbing-only and permanently
  non-gate-clearing. Use
  `../../../docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md`
  before any separately authorized `--allow-live-provider-call` smoke run.
