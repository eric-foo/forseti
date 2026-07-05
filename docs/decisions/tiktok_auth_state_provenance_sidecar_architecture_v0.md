# TikTok Auth-State Provenance Sidecar Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti architecture decision record
scope: >
  Target architecture for extending the local ignored auth-state sidecar so
  TikTok sessioned capture can fail closed on source-access provenance claims
  without persisting cookies, storage-state contents, proxy endpoints, exit IPs,
  or other secrets.
use_when:
  - Implementing or reviewing TikTok session/auth-state provenance enforcement.
  - Deciding whether a TikTok run can claim a harness proxy-profile posture.
  - Checking why "no proxy" is not a v0 provenance claim.
open_next:
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/safety-rules.md
  - orca-harness/source_capture/auth_state.py
  - orca-harness/source_capture/local_secret_store.py
  - orca-harness/runners/run_source_capture_browser_user_data_export.py
  - orca-harness/runners/run_source_capture_cloakbrowser_profile_warmup.py
  - orca-harness/runners/run_source_capture_tiktok_live_batch_probe.py
  - orca-harness/source_capture/tiktok/live_batch_probe.py
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
authority_boundary: retrieval_only
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: architecture_doctrine for TikTok/auth-state source-access provenance; no runtime implementation
  dirty_state_checked: yes
  blocked_if_missing: auth_state sidecar source, export runner, warmup runner, live TikTok runner, validation-gates non-self-certification rule
```

## Human Summary

Adopt a typed, versioned provenance extension to the existing local ignored
`_auth_state/<label>.meta.json` sidecar. The extension must be produced at the
stage where facts are knowable, merged forward at export, and enforced by the
live TikTok runner before a requested provenance claim can clear.

The architecture intentionally does **not** create a blanket `no_proxy` proof.
Current code can prove only that the Source Capture harness did or did not load
and apply a label-indirected proxy profile. It cannot prove the entire machine
egress path had no VPN, OS proxy, corporate proxy, ISP proxy, or upstream
network translation. Therefore the v0 claim vocabulary is
`harness_proxy_profile_posture`, not `no_proxy`.

Architecture result: `TARGET_RECOMMENDED`.

## Problem

After the TikTok lane moved from logged-out probing toward sessioned/cookied
capture, operators need a way to reuse a warmed/login browser session while
keeping source-access provenance honest. Today:

- `auth_state.py` already writes a local ignored metadata sidecar binding an
  auth-state file name to `session_mode`.
- `run_source_capture_browser_user_data_export.py` exports a dedicated
  CloakBrowser user-data label into an auth-state label and atomically discards
  an unbound state file if validation or sidecar writing fails.
- `run_source_capture_cloakbrowser_profile_warmup.py` can load a
  label-indirected proxy profile, but the fact is currently only surfaced in
  operator text, not bound into the exported auth-state provenance.
- `run_source_capture_tiktok_live_batch_probe.py` and
  `source_capture/tiktok/live_batch_probe.py` validate `session_mode`, but they
  do not validate any typed provenance claim beyond that mode.

The risk is a cold agent or future runner treating a label such as
`tiktok-alt-noproxy-*` as proof. That violates the receipt-field provenance gate:
operator-authored strings do not clear a gate.

## Decision

Use the existing sidecar substrate. Extend it narrowly instead of creating a
central ledger or teaching future agents to infer truth from labels.

The target shape has three carriers:

1. **Browser user-data provenance sidecar** beside the ignored user-data label.
   The warmup runner emits it because warmup is where proxy-profile application
   and browser backend are knowable.
2. **Auth-state metadata sidecar extension** under `_auth_state/`. The export
   runner reads the user-data sidecar, validates it, computes local-only binding
   witnesses, and merges the category-only provenance forward.
3. **Live-runner enforcement predicate**. The TikTok live runner can require
   specific provenance claims and must fail closed when the auth-state sidecar
   lacks a matching produced/witnessed field.

Do not introduce a repo-wide session registry in v0. The current problem is
label-to-auth-state provenance for one runner family, and the existing
sidecar+validator pattern already fits it.

## Core Invariants

1. **No self-certification.** A label, CLI flag, operator note, or filename does
   not prove source-access posture. A claim clears only from a produced,
   provenance-bound, or re-derivable sidecar field.
2. **No raw secrets in durable evidence.** Cookies, storage-state contents,
   `msToken`, signature params, proxy endpoint/host/port, proxy credentials,
   exit IPs, device IDs, raw browser profile material, and auth-state file
   contents never enter packets, bronze lake records, reports, prompts, or
   committed docs.
3. **Local ignored binding is allowed.** The ignored local auth-state sidecar may
   carry category-only fields and local-only one-way binding witnesses needed to
   reject swapped or mismatched artifacts. Those witnesses must not be copied
   into SourceCapturePacket payloads, bronze lake records, or human reports.
4. **Harness proxy posture is not egress proof.** V0 can prove
   `no_proxy_profile_loaded` or `proxy_profile_loaded` by the harness. It cannot
   prove full-network `no_proxy` unless a later architecture adds an egress
   attestation design.
5. **Fail closed on requested claims.** Missing, unknown, mismatched,
   malformed, or forbidden-field provenance blocks the run or admission path
   that requested the claim. It is not downgraded to `INFO`.

## Field Contract

The auth-state metadata sidecar remains JSON. Existing sidecars with only
`auth_state_file` and `session_mode` remain readable for legacy mode checks, but
they do not satisfy any new provenance requirement.

Recommended v0 extension:

```json
{
  "auth_state_file": "<state-label>.json",
  "session_mode": "client_provided_session",
  "schema_version": 1,
  "source_access_provenance": {
    "source_access_posture": "client_provided_session",
    "browser_backend": "cloakbrowser",
    "harness_proxy_profile_posture": "no_proxy_profile_loaded",
    "proxy_category": "none",
    "warmup_user_data_label_sha256": "<sha256>",
    "state_content_sha256": "<sha256>",
    "no_secret_scan": "passed"
  }
}
```

Allowed values:

- `source_access_posture`: `public_logged_out`, `free_account_created_session`,
  `paid_entitled_session`, `client_provided_session`,
  `consenting_coworker_session`.
- `browser_backend`: current harness backend vocabulary, initially
  `cloakbrowser` or `playwright` where the launcher actually witnessed it.
- `harness_proxy_profile_posture`: `no_proxy_profile_loaded`,
  `proxy_profile_loaded`, or `unknown`.
- `proxy_category`: `none` or the existing `ProxyCategory` value when a proxy
  profile sidecar was loaded.
- `warmup_user_data_label_sha256`: one-way commitment to the source user-data
  label used at export; no path/root is recorded.
- `state_content_sha256`: local-only hash of the ignored storage-state JSON at
  export time, used for binding checks only; never copied into packets or
  reports.
- `no_secret_scan`: `passed` only after the sidecar payload is scanned for
  forbidden keys and forbidden value patterns.

Forbidden values anywhere in the sidecar payload include raw cookies,
storage-state contents, token names/values, proxy endpoint fragments, host:port
values, proxy credentials, exit IPs, device identifiers, absolute user-data
paths, and auth-state root paths.

## Enforcement Sites

**Warmup emitter.** `run_source_capture_cloakbrowser_profile_warmup.py` writes a
user-data provenance sidecar after a successful warmup. It derives
`harness_proxy_profile_posture` from whether `load_proxy_profile_by_label` was
used and records only category-level data. If proxy geo resolution fails, the
sidecar must not claim a successfully warmed proxy posture.

**Export merger.** `run_source_capture_browser_user_data_export.py` reads the
user-data sidecar, validates the binding, computes `state_content_sha256`, runs
the forbidden-field scan, and writes the extended auth-state sidecar. It reuses
the existing atomic cleanup rule: no state file survives without the expected
sidecar when extended provenance is being written.

**Live-runner enforcer.** `run_source_capture_tiktok_live_batch_probe.py`
resolves `--state-label` to the auth-state sidecar before probing. If a future
flag requests a provenance claim, such as
`--require-harness-proxy-posture no_proxy_profile_loaded`, the runner must
validate the sidecar and exit nonzero before live capture when the field is
missing, legacy-only, unknown, malformed, or mismatched.

## Option Comparison

| Option | Result |
| --- | --- |
| Label convention only | Rejected. A label is operator-authored and self-certifying. |
| Minimal untyped sidecar | Rejected as incomplete. It would store text without a fail-closed predicate. |
| Typed sidecar extension + validators | Selected. It reuses current code shape and gives future code a deterministic boundary. |
| Central registry/ledger | Deferred. It adds a new source of truth before a second consumer proves the need. |
| Full no-proxy egress attestation | Deferred. It may require external network observation and a separate privacy/secret-safe design. |

## Directional / Adversarial / Grounding Pass

Directional: the selected sidecar extension is the smallest architecture that
turns the existing `session_mode` binding pattern into a provenance carrier for
TikTok sessioned capture.

Adversarial: the phrase `no_proxy` is too broad and would become fake proof.
The v0 vocabulary must say `no_proxy_profile_loaded`, because current code does
not control or observe every possible egress layer. `state_content_sha256` is
also secret-adjacent and must stay local-only.

Grounding: the architecture stays inside existing harness modules
(`local_secret_store.py`, `auth_state.py`, warmup, export, live runner) and
does not create a new database, global registry, browser automation path, or
packet schema.

This adversarial pass is advisory input only. It is not a verdict, not
implementation authority, and not proof of readiness.

## Not Doing

- No CAPTCHA or slider solving.
- No browser-profile, cookie, token, storage-state, proxy endpoint, credential,
  exit-IP, or device-ID persistence in packets, lake records, reports, or docs.
- No claim that a warmed proxy session will remain valid without that proxy.
- No claim that `no_proxy_profile_loaded` proves full-network no-proxy egress.
- No logged-out durable sidecar carrier in v0; logged-out runs use their live
  staging receipt and cannot satisfy auth-state provenance requirements.
- No implementation, tests, CI gate, packet promotion, bronze admission change,
  or live TikTok run from this decision record alone.

## Deferred Implementation Implications

Implementation should be a narrow code slice:

- add a small provenance schema/validator near the auth-state/local-secret-store
  boundary;
- emit the user-data provenance sidecar during CloakBrowser warmup;
- merge and bind provenance during browser user-data export;
- add live-runner requirement flags only for claims the sidecar can prove;
- add tests for legacy sidecar rejection under a required claim, forbidden-field
  rejection, proxy-profile category preservation, and no-proxy-profile wording.

Do not implement a central registry, true egress attestation, or logged-out
carrier until a concrete consumer needs it.

## What Would Change This Decision

- A second runner family needs the same provenance enforcement and cannot share
  auth-state sidecars cleanly.
- The owner requires true full-network no-proxy proof rather than harness
  proxy-profile posture.
- A future privacy/security decision rejects local-only hashing of the
  storage-state file.
- Logged-out runs need the same durable provenance requirement without an
  auth-state artifact.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    TikTok sessioned capture provenance should be enforced through a typed,
    versioned extension of the existing local ignored auth-state metadata
    sidecar, with warmup/export/live-runner validators, and the allowed v0
    proxy claim is harness_proxy_profile_posture (for example
    no_proxy_profile_loaded), not blanket no_proxy egress proof.
  trigger: architecture_doctrine
  related_triggers:
    - validation_philosophy
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/tiktok_auth_state_provenance_sidecar_architecture_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/safety-rules.md
    - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
    - orca-harness/docs/source_capture_agent_runbook.md
    - orca-harness/docs/source_capture_packet.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
      reason: >
        The spec already says the live admission chain is not no-proxy
        provenance proof. This ADR refines the future implementation vocabulary
        before code changes; the spec should be updated in the implementation
        patch that actually adds the sidecar fields or runner flags.
    - path: orca-harness/docs/source_capture_agent_runbook.md
      reason: >
        Current runbook behavior remains true: existing runners validate
        session_mode only. Runbook commands should change with the code slice,
        not ahead of it.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The non-self-certification gate already owns the general rule. This ADR
        applies it to TikTok/auth-state provenance without changing the overlay
        rule.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Source-access safety and anti-blocking/proxy authorization boundaries
        are unchanged; this is a provenance architecture decision inside those
        boundaries.
  stale_language_search: >
    rg -n "no-proxy provenance proof|proxy_warmed|proxy-warmed|no_proxy|no proxy provenance|source_access_provenance|harness_proxy_profile_posture|no_proxy_profile_loaded"
    .agents docs orca-harness forseti/product/spines/capture/core/source_families/social_media/tiktok
    forseti/product/spines/capture/core/source_capture_toolbox
  stale_language_search_result: >
    Executed 2026-07-04. The live TikTok spec already carries the compatible
    non-claim "not no-proxy provenance proof". The direct_http no-proxy hits
    govern a separate adapter, review-input hits are historical snapshots, and
    the new ADR/repo-map hits are expected. No checked live surface claims a
    TikTok auth-state label proves blanket no-proxy egress.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not live capture success
    - not no-proxy egress proof
    - not CAPTCHA or slider-solving authorization
```
