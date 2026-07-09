# Source Capture Adapter Author Contract

Status: `SOURCE_CAPTURE_ADAPTER_AUTHOR_CONTRACT_V0`.

This document **names conventions that already exist** in `forseti-harness/source_capture/`.
It is a reference for adding bounded source adapters, including the selected
CloakBrowser anti-blocking route when that implementation lane is opened. It
does not introduce a framework, base class, registry, or dispatcher, and it does
not authorize new build scope.

Architecture thesis it records: **uniformity lives in the packet (output), not in
an adapter interface (input).** Every adapter fills the same
`SourceCapturePacket` via the one writer; adapter inputs stay native and
divergent.

## What is frozen (call/match, do not redesign)

- `source_capture/models.py` — `SourceCapturePacket`, `SourceCaptureSlice`,
  `PacketTiming`, `VisibleFact` (status ∈ `known | unknown_with_reason |
  not_attempted | not_applicable` + free-text `value`/`reason`), `PreservedFile`,
  and the `validate_preserved_file_references` model validator (every preserved
  file referenced by exactly one slice; slice references must resolve).
- `source_capture/writer.py: write_local_source_capture_packet(...)` — the single
  packet sink. It owns ULID `packet_id`/`session_identity`, `capture_time`
  (`utc_now_z`), `raw/` copy + sha256, default-posture backfill, manifest
  (`json.dumps(..., indent=2, sort_keys=True)` + newline) and `receipt.md`.
  **Preserved-file IDs are assigned here**, by `_copy_preserved_files`, as
  `file_{index:02d}` (1-based) in `input_files` order; `raw/` filenames are
  `{index:02d}_{source_path.name}`.
- `source_capture/cli_support.py: build_optional_fact(...)` — the shared
  optional-flag → `VisibleFact` bridge (value/unknown/not_attempted/not_applicable;
  rejects more than one supplied).
- `source_capture/local_secret_store.py` — the **shared credential-store security
  core** every local credential store builds on: directory confinement
  (`assert_under_root`), label→filename sanitization with path-traversal and
  reserved-sidecar-suffix rejection (`label_to_filename`), the size-capped
  JSON-object read (`read_store_payload`, `DEFAULT_MAX_SECRET_STORE_BYTES`), and
  the `.meta.json` sidecar read/write mechanics. Confinement is enforced at path
  construction (`store_path_for_label`, `sidecar_path_for`); the read/write helpers
  assume constructor-derived paths.
- `source_capture/auth_state.py` — the **browser** specialization over that core
  (ignored `_auth_state/` store, `AuthenticatedSessionMode`, cookies/origins
  storage-state shape, `validate_auth_state_session_mode` mode-mismatch refusal).
- `source_capture/reddit_credentials.py` — the **Reddit API** specialization over
  that core (ignored `_reddit_credentials/` store, `RedditCredentialMode`
  [`owner_registered_script_app`; application-only `client_id`/`client_secret`
  read], secret-redacting `RedditCredentials.__repr__`, `load_reddit_credentials`
  mode-mismatch refusal; registered via
  `run_source_capture_reddit_credential_bootstrap.py`). Every credential store
  records only label/mode/loaded-boolean in packets, never secret material.

## The adapter convention (already practiced by all four adapters)

1. An adapter is a free function `fetch_*( ...native inputs... ) -> <Name>Success | <Name>Failure`.
   Inputs are source-specific (HTTP takes `url`; Reddit takes
   `subreddit/listing/post_id/limit`). **Do not unify inputs across adapters.**
2. `Success`/`Failure` are frozen dataclasses. Every result carries
   `warning_notes` and `limitation_notes` (or equivalent) — honest limitation
   reporting is a required field, not optional.
3. Adapters **never import the writer** and never construct a packet. The runner
   translates the adapter result into writer kwargs.
4. For testability, the adapter takes its transport behind an injected **Protocol
   seam** (precedent: `BrowserSnapshotEngine`). Unit tests inject the seam; no
   live network/API call runs in unit or contract tests.
5. Composition is by plain call: `media_asset` and `archive_org` already call
   `fetch_direct_http_capture` directly. No interface is needed to compose.
6. Each runner defines a module-level `*_NON_CLAIMS` list and passes it as
   `receipt_non_claims`.

## The runner contract (the "last mile", staging → write → cleanup)

A network runner currently repeats this ritual (the target of the STEP-02
helper extraction):

1. Stage adapter bytes to `output_directory.parent` under explicit filenames,
   with a collision guard ("already exist; clear before rerunning").
2. Build `PacketTiming` and per-slice postures from the adapter result
   (source-specific).
3. Build `SourceCaptureSlice` objects; each slice's `preserved_file_ids` must
   reference the `file_{NN:02d}` the writer will assign **by `input_files`
   order** (today hand-written, e.g. `["file_01","file_02"]` — the foot-gun the
   helper removes).
4. Call `write_local_source_capture_packet(input_files=<staged paths in order>,
   source_slices=<slices>, ...)`.
5. `finally:` unlink the staged files.

Runner exit-code convention (match exactly): `0` = packet produced; `2` =
`ValueError`/bad input (via `parser.exit`); `3` = adapter/other failure (typed
failure returns `(3, message)`; uncaught exceptions map to `3`).

## Invariants every adapter+runner must preserve

- **No secrets in packets.** Credentials/tokens/cookies/storage-state live in
  ignored local config; the packet records only label/mode/loaded-boolean. Reuse
  the shared `local_secret_store.py` core (the `auth_state.py` browser store and
  `reddit_credentials.py` Reddit store both build on it); do not invent a second
  credential subsystem.
  **The `stage_and_write_packet` helper is NOT a secrecy boundary:** it forwards
  `staged_artifacts` bytes and `writer_kwargs` to the writer verbatim and cannot
  detect a secret embedded in adapter-produced metadata or raw bytes (a
  byte-scanner there would be fragile and is out of scope — do not add one).
  No-secrets enforcement therefore lives in the **adapter + runner**: (1) the
  adapter result type carries no secret fields (label/mode/loaded-boolean only —
  do not add token/cookie/header fields); (2) the runner must not stage request
  headers, `Authorization` values, cookies, or OAuth tokens into
  `staged_artifacts`, nor pass secret-bearing values through `writer_kwargs`;
  (3) **before any credentialed adapter (Reddit) uses this helper, a runner-level
  test MUST prove a credential-like field is absent from the written packet**
  (manifest, `raw/`, receipt) — precedent: the existing direct-HTTP / media
  `Set-Cookie`-absent assertions.
- **Packets stay scratch** unless a separate fixture-admission decision admits
  them.
- **Capture-support only.** Slices/postures carry locator + posture + limitations.
  No credibility, inclusion/exclusion, scoring, or Judgment meaning.
- **No rollup hides a failed/limited slice.** A slice is *limited* if it carries
  any `limitations`, OR if any of its four posture axes (`access_posture`,
  `archive_history_posture`, `media_modality_posture`, `re_capture_relationship`)
  has status `unknown_with_reason` — the "tried and could not establish" gap.
  `not_attempted` / `not_applicable` are honest scope statements and do **not**
  count as limited (so an ordinary direct-HTTP packet whose archive/media axes are
  `not_attempted` stays valid). A limited slice must be surfaced at the capture
  level: the capture-level `limitations` must be non-empty, OR — for an
  `unknown_with_reason` axis — the capture-level posture on that same axis must
  also be `unknown_with_reason`. `packet_assembly.validate_capture_posture_honesty`
  enforces this before the writer runs (tests: `tests/unit/test_packet_assembly.py`).
  The media runner already practices the limitation-string form (a failed asset →
  a slice with empty `preserved_file_ids` + a `limitation`, plus a capture-level
  "preserved X of Y" note).
- **Honest limitation reporting.** `warning_notes`/`limitation_notes` pass through
  to the packet; exit `0` is not a claim of content sufficiency.

## Not in scope (deferred)

No adapter base class / `Protocol`-over-adapters / registry / dispatcher / auto
source-class routing. No second credential subsystem. Still in the deferred
build set (Scrapy/crawlers, commercial fetch, SERP,
storage/dashboard/scheduler/deployment/production runtime); anti-detect and proxy
moved to the third tranche of the source-access tooling build authorization
(build-authorized, used only inside the unchanged source-access boundary).
Selection stays the runbook table (agent reads it and invokes the named runner),
not code.

## Non-claims

This document is reference only. It is not validation, readiness, fixture
admission, a new contract type, or authorization for new build scope.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The source-capture adapter honesty rule is now precise and enforced in code
    (a slice is "limited" by any limitation OR an unknown_with_reason posture
    axis; not_attempted/not_applicable are honest scope and do not count), and the
    shared stage_and_write_packet helper is explicitly NOT a secrecy boundary --
    no-secrets enforcement is bound to the adapter/runner, with a mandatory
    no-secret-in-packet test required before any credentialed (Reddit) adapter
    uses the helper.
  trigger: architecture_doctrine
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - forseti-harness/docs/adapter_author_contract.md
    - forseti-harness/source_capture/packet_assembly.py
    - forseti-harness/tests/unit/test_packet_assembly.py
  downstream_surfaces_checked:
    - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
    - forseti-harness/docs/source_capture_agent_runbook.md
    - forseti-harness/runners/run_source_capture_http_packet.py
    - forseti-harness/runners/run_source_capture_media_packet.py
    - docs/hygiene/precompact_source_capture_adapter_step02_v0.md
  intentionally_not_updated:
    - path: docs/review-outputs/adversarial-artifact-reviews/source_capture_packet_assembly_step02_adversarial_code_review_v0.md
      reason: >
        Durable review record; it quotes the prior vague "non-`known` posture"
        wording as the AR-01 finding evidence and must preserve what it found.
    - path: docs/prompts/reviews/source_capture_packet_assembly_step02_adversarial_code_review_prompt_v0.md
      reason: >
        Point-in-time review commission that posed the open question AR-01
        resolved; not a forward-routing doctrine surface.
    - path: docs/hygiene/precompact_source_capture_adapter_step02_v0.md
      reason: >
        Point-in-time precompact snapshot, explicitly orientation-not-authority;
        its "OPEN for review" posture question is resolved here and in the
        controlling contract doc.
    - path: .codex/worktrees/data-capture-sourcing-architecture/**
      reason: >
        Separate git worktree / parallel pricing workstream; its "rollup hides
        per-slice variance" hits are bundled-offer doctrine, not the
        source-capture posture-honesty rule. Out of this patch's scope.
  stale_language_search: >
    rg -ni "non-.?known.? posture|rollup hides|clean rollup|hides a (failed|limited)|secrecy boundary|not a secrecy"
    (repo root)
  stale_language_search_result: >
    Run 2026-06-04 after the AR-01..AR-03 review patch. Live source hits are the
    updated contract doc and the new validator/messages/tests. Review report and
    review prompt hits are intentionally preserved historical records. The
    precompact hit is an orientation-only snapshot. .codex worktree hits are a
    separate pricing workstream. No live forward-routing surface still states the
    pre-patch vague "non-known posture" honesty rule or claims the helper
    structurally enforces no-secrets.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not fixture admission
    - not implementation authorization
```

## Direction Change Propagation - Shared Credential Store Core

```yaml
direction_change_propagation:
  doctrine_changed: >
    The source-capture credential-indirection pattern is now a shared
    local_secret_store.py security core (directory confinement incl. symlinked-root
    rejection, label sanitization with a reserved-sidecar-suffix guard, size-capped
    JSON-object read, .meta.json sidecar mechanics) that BOTH the auth_state.py
    browser store and the new reddit_credentials.py Reddit store build on. "Do not
    build a second credential subsystem" is satisfied by reusing that one core
    rather than copying auth_state.py. The Reddit store adds a closed
    RedditCredentialMode (owner_registered_script_app; application-only, exact
    client_id + client_secret shape with extra keys rejected), a both-fields-redacting
    credentials repr, and a no-secret-flag registration runner.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - forseti-harness/docs/adapter_author_contract.md
    - forseti-harness/source_capture/local_secret_store.py
    - forseti-harness/source_capture/auth_state.py
    - forseti-harness/source_capture/reddit_credentials.py
    - forseti-harness/runners/run_source_capture_reddit_credential_bootstrap.py
    - forseti-harness/source_capture/__init__.py
    - .gitignore
  review_clearance: >
    Cleared by independent CROSS-FAMILY adversarial review (different model family
    from the Claude author). First pass returned blocking-issues (client_id repr/str
    leak; credential shape accepting extra secret keys; symlinked-store-root
    confinement gap; an over-stated behavior-preservation claim) -- all patched; the
    bounded patch-recheck returned closed-clean with no new blocker/major in the
    touched scope. Prompts:
    docs/prompts/reviews/source_capture_step03_credential_store_cross_family_adversarial_code_review_prompt_v0.md
    and ..._rerun_prompt_v0.md. Review is decision input only, not validation/readiness.
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/source-of-truth.md
    - forseti-harness/docs/source_capture_agent_runbook.md
    - docs/product/source_capture_toolbox/README.md
    - docs/workflows/orca_repo_map_v0.md
    - forseti-harness/README.md
    - docs/source_capture_packet.md
    - docs/hygiene/precompact_source_capture_armory_resume_v1.md
  intentionally_not_updated:
    - path: forseti-harness/docs/source_capture_agent_runbook.md
      reason: >
        The credential store and registration runner are infrastructure, not yet
        agent-facing packet runners. The Reddit adapter (STEP-04) and Reddit packet
        runner (STEP-05) do not exist; the runbook Runner-Selection row and
        credential-registration command land with the agent-facing Reddit runner
        (STEP-06), not this step.
    - path: docs/product/source_capture_toolbox/README.md
      reason: >
        Armory component status, adapter boundaries, and hard stops are unchanged;
        the auth_state reference stays accurate (the browser store still exists) and
        no new agent-facing component was added.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map indexes the armory at a path level under the already-indexed
        source_capture/; local_secret_store.py and reddit_credentials.py are internal
        modules and add no new durable source family.
    - path: docs/source_capture_packet.md
      reason: >
        The packet contract is unchanged: packets still record only
        label/mode/loaded-boolean, never secret material.
    - path: docs/hygiene/precompact_source_capture_armory_resume_v1.md
      reason: >
        Point-in-time orientation snapshot (orientation-not-authority); not a
        forward-routing doctrine surface.
    - path: docs/review-outputs/**
      reason: >
        Durable point-in-time review records; preserve what they found at review time.
  stale_language_search: >
    rg -n "_assert_under_root|second credential subsystem|auth_state\.py pattern|MAX_AUTH_STATE_BYTES|reuse the .?auth_state"
    -g '!**/review-outputs/**' (repo root)
  stale_language_search_result: >
    Re-run 2026-06-04 after the cross-family review + patches cleared. No LIVE
    forward-routing surface carries the pre-refactor framing. Hits are all non-stale:
    (a) this doc's "No second credential subsystem" is the still-true rule (the shared
    core IS the one subsystem); (b) MAX_AUTH_STATE_BYTES in auth_state.py is a live
    backward-compatible alias of DEFAULT_MAX_SECRET_STORE_BYTES, no longer cited as
    THE cap in the frozen-list; (c) test_local_secret_store hits are the NEW public
    assert_under_root (no leading underscore), not the removed private; (d) the
    precompact line is an orientation-only snapshot; (e) the rerun review prompt is a
    point-in-time review record. No live surface tells a future agent to copy
    auth_state.py or names the removed _assert_under_root private as the confinement
    home.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not fixture admission
    - not implementation authorization
    - not the Reddit adapter (STEP-04) or Reddit packet runner (STEP-05)
    - not the mandatory no-secret-in-packet runtime test (STEP-07), still pending
```
