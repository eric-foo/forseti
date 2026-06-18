# CloakBrowser Packet Runner Architecture — Independent Pass v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture planning artifact (independent second pass / corroboration + refinement)
status: ARCHITECTURE_RECOMMENDATION_INDEPENDENT_PASS_V0
scope: >
  Non-executing architecture for exposing CloakBrowser to agents as a bounded
  Source Capture Packet runner rather than a freeform browser-control surface.
  Independent re-derivation of the same commission, produced to corroborate (or
  contest) the prior pass and to fold in four grounded refinements it did not yet
  carry. Designs contracts, tests, and runbook implications only.
use_when:
  - Owner is choosing which CloakBrowser runner architecture to treat as canonical.
  - Checking whether the prior pass's recommendation holds under an independent
    re-derivation, and what an independent pass would sharpen.
  - Scoping the CloakBrowser adapter contract and packet runner before any
    implementation pass.
authority_boundary: planning_only
open_next:
  - orca/product/spines/capture/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md
  - docs/prompts/architecture/cloakbrowser_packet_runner_architecture_prompt_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - orca-harness/docs/adapter_author_contract.md
  - orca-harness/docs/source_capture_agent_runbook.md
stale_if:
  - The owner accepts one CloakBrowser runner architecture as canonical and
    supersedes the other.
  - CloakBrowser API shape, install path, executable contract, or local
    availability becomes known and contradicts the adapter-first recommendation.
  - Reddit pre-commercial method ordering changes.
  - Source Capture Packet schema, packet writer, no-secret rules, packet
    lifecycle, or the runner exit-code convention change.
  - Orca authorizes storage, scheduler, queue, dashboard, deployment, production
    runtime, broad crawler behavior, or commercial Reddit use.
```

## 0. Relationship To The Prior Pass (read this first)

A prior pass already produced
`orca/product/spines/capture/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md`
(untracked at author time). This artifact does **not** overwrite or supersede it.
It is an **independent re-derivation** of the same commission — full source load
plus three fresh advisory subagents — written to an adjacent path at the owner's
instruction.

Two things matter for the owner:

1. **Corroboration.** This independent pass reached the **same required
   recommendation** (`RECOMMEND_ADAPTER_CONTRACT_FIRST`) and substantially the
   **same contract** (thin spec-driven runner; cloned adapter + injected engine
   seam; `reddit_old_html_thread` first; packet-before-parser; no-secret in
   adapter+runner; no-discovery / volume-ceiling / monitored-stop-date;
   commercial reroute). Independent convergence is corroboration, not proof — but
   it means the prior pass is sound and on-target, not a stub.

2. **Four grounded refinements** the prior `_v0.md` does not yet carry. Each is
   tied to a real harness fact, not a stylistic preference:

   - **R1 — Exit codes 4/5 vs a frozen convention.** The prior pass asserts new
     exit codes `4` (contamination) and `5` (dependency-unavailable). The prompt
     §7 invites distinguishing those, but
     `orca-harness/docs/adapter_author_contract.md` states the runner exit
     convention is "match **exactly**: `0`/`2`/`3`." So 4/5 is a **deliberate
     divergence from a currently-frozen convention** and must be flagged as an
     open owner decision (a convention amendment), not asserted silently. This
     pass keeps the distinction *visible* but routes it correctly (see §13).
   - **R2 — Disclosability inverse-test (missing).** The prior test list checks
     *too much* (no secrets in packet) but not *too little*: there is no test that
     **fails when an anti-detect / proxy / JS-challenge method was used but its
     category was not recorded** in the packet. Non-disclosure breaks Orca's
     trust story even with zero secret leak (the boundary's whole basis is
     disclosability). Added in §17.
   - **R3 — Two-sided proxy boundary + new contamination class.** Proxy
     *category* is disclosable provenance that must be **recorded**; proxy
     *endpoint / credentials / exit-IP* are secrets that must be **excluded** —
     and proxy credentials are a **new contamination class** the existing
     `auth_state.py` / `reddit_credentials.py` stores do not cover. If proxy is
     ever used it needs a new `local_secret_store.py` specialization, **not** a
     second credential subsystem. Sharpened in §12.
   - **R4 — Anonymous-only v0 engine seam.** State explicitly that the v0
     CloakBrowser engine seam takes **no `storage_state` / profile / cookie
     kwarg**. Authenticated/session cloaked capture is a separate later gate; a
     session kwarg on the seam is the leakage vector. Sharpened in §9.

The owner picks which artifact is canonical. The cleanest outcome is to treat the
prior `_v0.md` as canonical and absorb R1–R4 into it, or to treat this pass as the
superseding version — either way, only one should remain the live recommendation.

## 1. Status And Non-Executing Boundary

This is a planning-only architecture artifact produced from
`docs/prompts/architecture/cloakbrowser_packet_runner_architecture_prompt_v0.md`.

It does not implement a runner, install CloakBrowser, run live capture, open
Reddit, configure proxies, solve CAPTCHA, create credentials, create storage,
write parser code, alter the packet writer, stage commits, push, or create a PR.

Architecture result: `TARGET_RECOMMENDED`.

Required recommendation:

```text
RECOMMEND_ADAPTER_CONTRACT_FIRST
```

Precise form of the recommendation: the adapter **contract** (result dataclasses
+ failure-kind enum + injected engine `Protocol` seam + fake-engine tests) is
buildable and reviewable **now**, because the engine seam isolates the one
genuinely unknown piece. Only the live `_CloakBrowserEngine.capture()` body is
`BLOCKED_UNTIL_CLOAKBROWSER_API_KNOWN`. The first — and initially only —
consuming runner mode is a single supplied **old Reddit thread URL**. This folds
in the value of `RECOMMEND_REDDIT_REFERENCE_RUNNER_FIRST` without forking a
Reddit-specific adapter.

Owner intent preserved:

```text
agent supplies a bounded capture unit -> runner invokes CloakBrowser backend ->
runner writes a Source Capture Packet -> agent inspects manifest/receipt/raw ->
parser/consolidation consume preserved packet artifacts
```

Rejected shape:

```text
agent manually controls CloakBrowser like Computer Use
```

## 2. Source Readiness And Source Gaps

`SOURCE_CONTEXT_READY`.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom CloakBrowser packet-runner architecture pack
  workspace: C:\Users\vmon7\Desktop\projects\orca
  edit_permission: docs-write (this adjacent artifact only)
  output_mode: file-write
  target_scope:
    - orca/product/spines/capture/source_capture_toolbox/cloakbrowser_packet_runner_architecture_independent_pass_v0.md
  dirty_state_checked: yes
  controlling_source_state: >
    Working tree contained modified and untracked files before this pass,
    including required source-pack files (README.md, the Reddit planning thread,
    and the Data Capture consolidation map are modified; many decisions and the
    prior CloakBrowser artifact are untracked). Used as repo-visible advisory
    context only. This artifact makes no validation, readiness, acceptance, or
    clean-source claim.
  collision_check: >
    The default prompt target
    orca/product/spines/capture/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md
    already existed (untracked, complete). Per owner instruction this pass writes
    to the adjacent _independent_pass_v0 path instead of overwriting it.
  blocked_if_missing: none for architecture; live implementation remains blocked
    on the CloakBrowser API shape.
```

Sources loaded (read in this session):

- `AGENTS.md`; `.agents/workflow-overlay/README.md`, `source-of-truth.md`,
  `source-loading.md`, `artifact-roles.md`, `validation-gates.md`.
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`.
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`.
- `docs/product/data_capture_source_access_boundary_decision_v0.md`.
- `docs/product/data_capture_source_access_method_plan_v0.md`.
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`.
- `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`.
- `orca/product/spines/capture/source_capture_toolbox/README.md`.
- `orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`.
- `orca/product/spines/capture/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`.
- `orca/product/spines/capture/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md` (the prior pass).
- `orca-harness/docs/source_capture_agent_runbook.md`; `orca-harness/docs/adapter_author_contract.md`.
- `orca-harness/source_capture/models.py`, `cli_support.py`, `packet_inspection.py`, `auth_state.py`.
- `orca-harness/source_capture/adapters/browser_snapshot.py`.
- `orca-harness/runners/run_source_capture_browser_packet.py`, `run_source_capture_authenticated_browser_packet.py`.
- Subagents additionally read `writer.py`, `packet_assembly.py`, `reddit_credentials.py`,
  `local_secret_store.py`, `adapters/reddit_api.py`, `adapters/direct_http.py`,
  `adapters/archive_org.py`, and the browser/reddit/packet-assembly tests.

Source gaps (honest, this session):

- **Skill source files not locatable on accessible paths this session.**
  `workflow-deep-thinking` and `workflow-architecture-planning` are present in the
  Skill manifest but their `SKILL.md` source files were not found under the repo
  or `~/.claude`. They were **APPLY-ed from their declared scope** (method
  disciplines), satisfying the prompt's REFERENCE-LOAD → APPLY sequence; the gap
  does not block the architecture. (The prior `_v0.md` reported reference-loading
  the method "from the available Agent Workflow plugin copy"; this pass could not
  reach that copy and is transparent about it.)
- **CloakBrowser local API shape is unknown from loaded source.** This is the one
  gap that bounds *live implementation* (not the contract).
- **No CloakBrowser adapter or runner exists** in the current harness.
- **No Reddit API packet runner exists**, though the Reddit API adapter and
  credential-store support are present; the mandatory runner-level
  no-secret-in-packet test (adapter-author contract "STEP-07") is still pending
  for the Reddit path too.

## 3. Evidence Mode And Subagent Receipts

Evidence mode: `delegated_three_advisory_subagents`. Three read-only advisory
subagents were launched in parallel, each given a bounded source capsule plus a
role-specific read list and its own source-readiness gate. Subagents are advisory
inputs only — not verdicts, implementation authority, validation, or readiness
proof. The Chief Architect (this pass) owns synthesis; subagent agreement is not
proof.

| Subagent | Readiness | Advisory result (faithful summary) |
| --- | --- | --- |
| SA-1 Runner Contract Architect | `SOURCE_CONTEXT_READY` | `RECOMMEND_ADAPTER_CONTRACT_FIRST`, realized through a single-URL `reddit_old_html_thread` reference runner. Proposed `run_source_capture_cloakbrowser_packet.py` + `adapters/cloakbrowser_snapshot.py`, batch-shaped like `reddit_api` for later fan-out. Split input contract: governance/bounding fields in a `--capture-unit` JSON spec, transport/tuning in CLI flags, `--output` as a flag. Closed `source_family_mode` enum; generic mode strictest. Flagged a proposed distinct dependency-unavailable exit code. |
| SA-2 Boundary & Contamination Adversary | `SOURCE_CONTEXT_READY` | 8 hard stops + 13 attacks + 10 must-fail tests. Largest: bounded-set laundering standing corpus (no Decision Frame); proxy/anti-detect **opacity** (disclosability failure even with zero leak); proxy credentials/exit-IP as a new contamination class; storage-state/cookie/header leakage; exit-0 false success over a block/challenge page; silent backend fallback to Patchright; generic-mode "browse anywhere". Stressed the **disclosability inverse-test** (fail if too little method provenance is recorded) and that the no-secret-in-packet test is mandatory before any credentialed/proxied variant ships. |
| SA-3 Implementation Grounding Integrator | `SOURCE_CONTEXT_READY` | Adapter-first sequence. Concrete file-touch map; place the adapter under `source_capture/adapters/` (out of the top-level no-runtime-import guard's glob); route the runner through `packet_assembly.stage_and_write_packet` + `staged_file_id_map` (not the inline `file_01` foot-gun); reuse the engine-Protocol-seam + closed-vocab + posture-honesty machinery. Reddit is a *use* of a generic CloakBrowser adapter, not a Reddit-specific adapter. Named one real test-surface gap: the `test_only_browser_snapshot_surfaces_name_playwright_dependency` allowlist guard needs an explicit edit for the CloakBrowser dependency name. |

## 4. Real Architecture Question

> What runner contract makes CloakBrowser reliable for Capture Spine use while
> preventing freeform browsing, source discovery, session leakage, packet
> contamination, hidden state, vague success claims, storage drift, parser-body
> promotion, and commercial-scale escalation?

Decisive invariant:

```text
Agents control only a bounded capture-unit spec. CloakBrowser execution is owned
by an injected adapter engine seam. Source Capture Packet writing is owned by the
existing single writer. Parser/consolidation output is derivative and never the
canonical source body. Anti-blocking method is disclosable (category recorded)
but never secret-bearing (no credentials/proxy endpoints/session state in the
packet).
```

The structural fact that makes it not-Computer-Use: the runner is a **batch CLI
transform** (spec → packet), identical in shape to
`run_source_capture_browser_packet.py` and the Reddit API runner — it never
returns an interactive browser handle to the model. There is no
`navigate`/`click`/`eval` surface and no "here's the page, what next?" loop.

## 5. Current State

CloakBrowser is the owner-selected **primary** third-tranche anti-blocking
backend (`data_capture_spine_source_access_tooling_build_authorization_v0.md`),
**authorized but not installed and not implemented**. Patchright is a
compatibility fallback only. Reddit pre-commercial order: CloakBrowser
anti-blocking first once implemented → old Reddit HTML where available →
low-volume bounded (subreddit/theme/query/thread-family/small-monitored-set)
capture → archive fallback; `.json` opportunistic-only; BeautifulSoup
parser-only after preservation; commercial/enterprise → sanctioned API/licensing.

The harness already has (verified in code):

- `SourceCapturePacket` model (manifest `source_capture_packet_manifest_v1`) and
  the single `write_local_source_capture_packet` writer;
- closed write-time-enforced postures — cutoff `{pre_cutoff, post_cutoff, mixed,
  unknown}`, archive `{archived, attempt_failed}`, recapture `{supersede,
  supplement, conflict, mixed}`; `access_posture` intentionally **open**;
  `PreservedFile.hash_basis` closed to `{raw_stored_bytes}`;
- referential-integrity validators (≥1 slice, ≥1 preserved file, every preserved
  file referenced, every slice reference resolves);
- `packet_assembly.stage_and_write_packet` + `staged_file_id_map` (removes the
  hand-written `file_01` foot-gun) and `validate_capture_posture_honesty`
  (no clean rollup over a limited slice);
- adapter convention: `fetch_*(...native...) -> Success | Failure` frozen
  dataclasses with `warning_notes`/`limitation_notes`; adapters never import the
  writer; transport behind an injected `Protocol` engine seam (precedent
  `BrowserSnapshotEngine`); module-level `*_NON_CLAIMS`;
- runner exit convention **`0`/`2`/`3`** ("match exactly", adapter-author contract);
- shared `local_secret_store.py` credential core with `auth_state.py` (browser)
  and `reddit_credentials.py` (Reddit) specializations; packets record only
  label/mode/loaded-boolean;
- runbook stating CloakBrowser is authorized but not implemented ("do not
  simulate it with the honest browser runner").

The harness does **not** yet have: a CloakBrowser adapter/engine seam; a
CloakBrowser packet runner; a known local CloakBrowser API contract; an
agent-facing runbook command; a runner-level no-secret-in-packet test for any
credentialed/proxied path.

## 6. Option Comparison

| Option | Verdict | Reason |
| --- | --- | --- |
| A — Minimal URL-only CloakBrowser packet runner | Adopted as the **first runner mode**, not as the first build step | The right first executable mode (one URL → one slice, identical shape to browser snapshot), but it needs the adapter result contract + engine seam to exist first. |
| B — Reddit reference runner first | Folded in, not separate | Reddit-first is correct as the first *use*, but a Reddit-specific *adapter* would bake Reddit semantics into the seam and violate "uniformity lives in the packet, inputs stay native." Reddit is a bounded use of the generic adapter. |
| C — Generic cloaked browser runner with source-family modes | Rejected for v0 normal-agent use | Generic mode trends to "browse anywhere." If ever authorized it must be single-URL-only with stricter rules than every Reddit mode (see §10). |
| D — Adapter contract first, runner later | **Selected** | Closes the biggest unknown (what CloakBrowser returns; how secrets/session are excluded; how dependency/API absence is reported) behind a seam that is buildable and reviewable now with fake-engine tests. |
| E — Manual CloakBrowser fallback only | Downgraded to exceptional operator-only | Manual use may remain an exceptional owner/operator action; it must not be the agent-facing Capture Spine path. |

## 7. Recommendation

`RECOMMEND_ADAPTER_CONTRACT_FIRST`.

This is the smallest complete route to the packet-runner goal: the current unknown
is not "how to write another runner" but "what contract safely contains
CloakBrowser so the runner cannot leak secrets, hide profile/session state,
become non-disclosable, or become manual browser control." The engine seam
isolates the one genuinely blocked piece (the live API body), so the contract +
fake-engine tests are buildable now and the live wiring later is a small bounded
change (implement one `Protocol` method).

Target path:

1. Define the CloakBrowser adapter result contract, failure-kind enum, and
   injected engine `Protocol` seam (anonymous-only — R4).
2. Prove with fake-engine tests that the adapter returns preserved HTML, visible
   text, screenshot bytes, **non-secret** metadata, access/anti-blocking/JS-
   challenge posture, source-set posture, warnings, limitations, and visible stop
   reasons **without constructing packets** and **without any secret-bearing
   field** — and that a used anti-blocking method is **recorded** (R2).
3. Build the runner only after the adapter contract is narrow enough to prevent
   hidden state and secret-bearing result fields; route it through
   `stage_and_write_packet`.
4. Start with one supplied old-Reddit-HTML thread (`reddit_old_html_thread`). Add
   a finite supplied thread-family list, then bounded listing/theme modes, only
   after no-discovery, volume-ceiling, cutoff, and stop-date tests exist.

## 8. Runner Contract

Runner name for a later implementation pass:

```text
orca-harness/runners/run_source_capture_cloakbrowser_packet.py
```

Normal agent-facing invocation is **spec-driven** (the spec is the control
surface; the CLI stays thin so agents cannot improvise browser behavior):

```powershell
python runners/run_source_capture_cloakbrowser_packet.py `
  --capture-unit "<capture-unit.json>" `
  --output "<fresh packet directory>"
```

Input contract is **split** (each field has exactly one home; no field is
duplicated across spec and flags):

- **Governance / provenance / bounding → `--capture-unit <json>` spec.** These
  bind to the Reddit planning thread's capture-unit field set and are what a
  reviewer/owner must see as one coherent commissioned object.
- **Transport / tuning → CLI flags** with defaults (reuse the browser-snapshot
  names): `--timeout-seconds`, `--wait-until`, `--viewport-width`,
  `--viewport-height`, `--max-artifact-bytes`. Plus `--output` (operator runtime
  choice) and an optional `--cutoff-posture` override.

Required capture-unit spec fields:

| Field | Requirement |
| --- | --- |
| `capture_unit_id` | Stable operator-supplied unit id. |
| `decision_question` | Operator-supplied capture question. |
| `capture_unit_intake_status` | `decision_frame_bound` or `candidate_or_scouting` (G1). |
| `decision_frame_id_or_none` | Non-empty id when `decision_frame_bound`; explicit `none` when `candidate_or_scouting`. Cross-field validation. |
| `source_family` | Initially `reddit`. |
| `source_family_mode` | Closed mode token; see §10. |
| `source_set_boundary` | Human-readable bounded source set. |
| `target_locator` / bounded fields | Supplied URL / finite list / subreddit+listing fields depending on mode. |
| `volume_ceiling` | Hard maximum; never inferred. Exceeded → refuse (do not silently truncate). |
| `cutoff_posture` | Closed posture where known, or unknown-with-reason. |
| `method_order` | Recorded provenance; CloakBrowser first; old Reddit where available; archive fallback; `.json` opportunistic only. Runner does not auto-chain fallbacks. |
| `operator_noncommercial_posture` | Must affirm pre-commercial posture; commercial pressure fails before adapter invocation. |
| `hard_stop_acknowledgement` | Explicit acknowledgement of source-access hard stops. Falsey/missing → refuse. |
| `packet_contamination_stop_acknowledgement` | Explicit acknowledgement of stop → contaminated scratch → no success claim. Falsey/missing → refuse. |

For monitored sets, both `monitoring_cadence` and a hard `stop_date` are required
(G2); a monitored set without a stop date fails input validation.

The agent controls **only** the spec + `--output`. The runner controls
CloakBrowser invocation, timeout/artifact caps, no-discovery behavior (fan-out is
bounded to the supplied list or the single listing page, never followed links),
staging cleanup, the packet writer call, and exit/visible-stop semantics.

## 9. Adapter Result Contract

Later adapter module:

```text
orca-harness/source_capture/adapters/cloakbrowser_snapshot.py
```

Shape (clone of `browser_snapshot.py`; batch-capable like `reddit_api.py` for
later fan-out modes):

```text
fetch_cloakbrowser_snapshot_capture(*, ...native inputs..., engine: CloakBrowserEngine | None = None)
  -> CloakBrowserSnapshotSuccess | CloakBrowserSnapshotFailure
```

**R4 — the engine seam is anonymous-only in v0.** The `CloakBrowserEngine`
`Protocol` takes **no `storage_state` / profile / cookie kwarg** (unlike
`BrowserSnapshotEngine`, which has `storage_state_path` for the authenticated
variant). Authenticated/session cloaked capture is a separate later gate; giving
the v0 seam a session kwarg is the leakage vector and is forbidden here.

Frozen dataclasses; the adapter never imports the writer and never constructs a
packet. Success result fields:

- requested locator or bounded source-set descriptor; final locator;
- rendered HTML; visible text; screenshot bytes;
- **non-secret** browser metadata (byte counts, timings, mode — never headers,
  cookies, tokens, proxy endpoints);
- source-family mode; source-set posture (e.g. "captured N of ceiling M");
- `access_posture` note (free text — the open axis);
- **anti-blocking method posture** (category: backend id, anti-detect=true, proxy
  *category* if any, JS-challenge category) — this field is what makes the method
  **disclosable** (R2/R3);
- JS-challenge posture;
- per-unit captures + per-unit failures (failed unit → a `*_not_preserved`
  limitation string, never a silent drop);
- warning notes; limitation notes; visible stop reason if the run completes with
  limitations; a closed `no_secret_check` token asserting the structural
  guarantee.

Failure-kind enum (keep the browser-snapshot kinds identical; add anti-blocking
honesty kinds):

```text
dependency_unavailable | timeout | challenge_unsolved | access_blocked |
capture_failed | empty_rendered_dom | empty_screenshot | size_cap_exceeded
```

`challenge_unsolved` / `access_blocked` make "the wall won" an honest named
outcome, never silently mapped to generic failure and never exit 0.

The adapter must **not**: construct packets; decide source meaning; parse
semantic claims; select evidence; discover sources or follow links/users/
comments/recommendations/"more like this"; score source quality; finalize result
tokens; or expose credentials, cookies, tokens, authorization headers, **proxy
credentials/endpoints/exit-IP**, raw browser profiles, storage-state JSON, HAR
files, environment dumps, or secret-bearing logs.

## 10. Source-Family Modes

`source_family_mode` is a closed enum validated like `ALLOWED_WAIT_UNTIL`
(unknown → `ValueError` → exit 2). It is a **runner/spec-level bounding** control,
**not** Reddit semantics in the engine — the engine just renders a locator → DOM/
text/screenshot; "old Reddit" is a `source_surface`, not a separate adapter.

| Mode | Scope | Tranche |
| --- | --- | --- |
| `reddit_old_html_thread` | One supplied old Reddit thread URL → one slice. | First / smallest. |
| `reddit_thread_family_supplied` | Explicit finite list of supplied thread URLs → one slice each, capped by `volume_ceiling`. No discovery. | With/just after first. |
| `reddit_bounded_listing_seed` | Subreddit + listing filter + limit; fan-out **only** over the children present in the one listing response, capped by `volume_ceiling` and a code-level `MAX_*` (reuse `reddit_api`'s `MAX_LIMIT`). | Deferred until no-discovery + volume-ceiling + cutoff + stop-date tests exist. |

Do not expose a normal-agent `generic_cloaked_url` mode in v0. If later
authorized, it must be single-URL-only, `volume_ceiling == 1`, with no
listing/fan-out path reachable, and a baked-in limitation note that the operator
asserts the single URL is the entire bounded set. The broadest mode must also be
the narrowest in fan-out.

No mode reads links out of fetched content to decide what to fetch next (G15).
`volume_ceiling` is a hard refusal, not a soft target. One run = one capture unit
= one packet; multi-unit work is separately commissioned runs.

## 11. Packet Output Contract

On success the runner writes a normal Source Capture Packet through
`stage_and_write_packet` (which auto-derives `file_{NN:02d}` ids and runs the
posture-honesty validator) — not the inline `["file_01", ...]` hand-write the two
older browser runners still use. Filled fields:

- `manifest.json` / `receipt.md` / `raw/`;
- source family; source surface distinguishing the mode (e.g.
  `cloakbrowser_reddit_old_html_thread`); source locator (capture-level = the
  bounded-set descriptor; per-slice = each unit's final locator);
- capture mode `multimodal`; `access_posture` (open) = anti-blocking note +
  "content sufficiency, login-wall absence, and block-wall absence not asserted";
- `archive_history_posture` = `not_attempted` (closed vocab; honest scope, not a
  limitation); `media_modality_posture` = viewport screenshot note;
  `cutoff_posture` (closed) from spec; `re_capture_relationship` (closed) or
  `not_applicable`;
- per-slice preserved files; per-slice warnings/limitations; writer-owned hashes +
  `hash_basis=raw_stored_bytes`;
- receipt non-claims (at least): not validation; not readiness; not source
  completeness; not fixture admission; not source-quality scoring; not parser
  correctness; not ECR/Cleaning/Judgment/buyer-proof/commercial-readiness; not
  broad crawling; not source discovery; not storage/queue/scheduler/dashboard/
  deployment/production runtime; not commercial Reddit authorization; not legal
  sufficiency; not anti-detect-guarantee; not login-wall/block-wall absence proof.

Per-slice limits stay visible: a failed unit contributes **zero** preserved files
(so the referential-integrity validator holds) and surfaces as a capture-level
limitation; `validate_capture_posture_honesty` refuses to write a clean rollup
over any limited slice. "Captured 3 of 5" is visible as 3 slices + 2 limitation
lines + a `source_set_posture` count.

## 12. No-Secret And Contamination Boundary

The runner and adapter must forbid packets from preserving: credentials; cookies;
OAuth tokens; authorization headers; raw browser profiles; storage-state JSON;
session sidecars; **proxy credentials/endpoints/exit-IP**; environment-variable
dumps; HAR files or request logs containing headers unless a later explicit
design defines redaction.

`stage_and_write_packet` is **not** a secrecy boundary (the adapter-author
contract says so; it forwards bytes/kwargs verbatim and a byte-scanner there
would be fragile and is out of scope). No-secrets enforcement therefore lives in:
(1) the adapter result type carrying **no secret fields** (structural — the
strongest guarantee); (2) the runner never staging headers/cookies/tokens/proxy
material into `staged_artifacts` or `writer_kwargs`; (3) a **mandatory
runner-level no-secret-in-packet test** before any credentialed/proxied variant
ships (precedent: the authenticated-browser leakage test).

**R3 — the two-sided proxy boundary.** Proxy *category* (e.g.
`residential_rotating`) is **disclosable method provenance and MUST be recorded**
in the packet (the boundary's whole basis is disclosability — HS-6). Proxy
*endpoint / username:password / assigned exit-IP* are **secrets and MUST be
excluded** from every packet field. Proxy credentials are a **new contamination
class** the existing `auth_state.py` / `reddit_credentials.py` stores do not
cover; if proxy is used they must live in a **new `local_secret_store.py`
specialization** (reuse the shared core — do **not** build a second credential
subsystem). v0 recommendation: the default CloakBrowser run is **anonymous, no
proxy** — which sidesteps this class until proxy is separately scoped.

Contamination response:

```text
stop -> mark contaminated scratch if anything exists -> do not claim packet
success -> require owner decision for disposal, redaction, or isolation
```

A contaminated run must not produce a normal successful `manifest.json` /
`receipt.md`. Because `stage_and_write_packet` unlinks staged files in `finally`,
a contamination signal must be surfaced by the adapter **before** write (as a
`CloakBrowserSnapshotFailure`), not after. Detection is structural + sentinel-test
based, not a fragile content byte-scanner: the narrow exception is engine-reported
contamination (e.g. a captured DOM that is a storage-state/cookies-origins JSON
shape, detectable by the `auth_state` heuristic).

## 13. Exit Codes And Visible Stops

**R1 — preserve the frozen convention; route the extra distinctions correctly.**
The adapter-author contract freezes the runner exit convention to **`0`/`2`/`3`,
"match exactly."** The prompt §7 invites distinguishing a contamination stop and a
dependency/blocker absence. These two pulls conflict, so this is an **open owner
decision**, not a silent assertion.

Recommended default (convention-preserving):

| Exit | Meaning |
| --- | --- |
| `0` | Packet written; manifest/receipt/raw exist; post-run inspection still required. Not a content-sufficiency / block-wall-absence claim. |
| `2` | Bad input / boundary preflight failure: missing required spec field, invalid mode, invalid volume, missing monitored stop date, source-discovery request, generic-browsing request, commercial-posture conflict, missing hard-stop/contamination acknowledgement, `decision_frame_bound` with `decision_frame_id_or_none == none`, staging collision. |
| `3` | Adapter/runtime/source-access failure: navigation failed, timeout, empty DOM/screenshot, artifact cap exceeded, `challenge_unsolved`/`access_blocked`, **dependency/CloakBrowser absent**, contamination stop, or pre-success packet-write failure. **No packet.** |

To honor "avoid treating dependency absence as source failure" and "contamination
stop, if distinct" **without** breaking the frozen convention, the default keeps
exit `3` but **requires distinct, machine-readable report tokens** so the agent
report and runbook distinguish them:
`cloakbrowser_dependency_unavailable`, `cloakbrowser_contamination_stop`,
`cloakbrowser_access_blocked`. Dependency absence and contamination are then
distinguishable in the report even though they share exit `3`, and no automatic
backend fallback (e.g. to Patchright) may occur silently — switching backends
needs explicit operator authorization and method-provenance recording.

Owner-gated refinement (only if the owner amends the convention): split out
distinct exit codes — e.g. `4` = contamination stop, `5` = dependency/backend
unavailable. This is a real ergonomic win (the runbook already treats environment
refusals like `WinError 10061` differently from source results), but it is a
**convention amendment** that must be recorded against the adapter-author contract
and applied uniformly, not introduced for one runner in isolation.

## 14. Reddit Reference Behavior

For Reddit pre-commercial use: CloakBrowser first once implemented; old Reddit
HTML preferred where available; capture low-volume and bounded by supplied
thread, supplied thread-family, named subreddit/theme/query boundary, or small
monitored set **with stop date**; broad crawling, source discovery, link/user
walking, comment/recommendation/"more like this" expansion **forbidden**; archive
capture is fallback/historical posture support; `.json` opportunistic-only (record
access posture each time, never the spine); BeautifulSoup-style parsing only after
packet preservation; commercial/client-funded/enterprise/buyer-facing-durable/
scale/data-licensing pressure **stops** anti-blocking capture and reroutes to the
sanctioned commercial/enterprise API or data-licensing path.

First runner mode: `reddit_old_html_thread` (one supplied URL). Listing/theme
modes wait for no-discovery + volume-ceiling tests. Reddit is a bounded *use* of
the generic CloakBrowser adapter — the operator names the subreddit/theme/thread-
family — not a separate Reddit adapter.

## 15. Parser Handoff Boundary

The runner preserves source-visible artifacts; it does not parse source meaning.
A later, separately-gated BeautifulSoup-style parser may extract from
already-preserved packet files: submission title/body; comment body; visible
author labels; visible timestamps; visible score or score-hidden state;
permalinks and ids; parent/nesting cues; deleted/removed/collapsed/hidden/
unavailable/lock/edit/moderation posture where visible; outbound links and media
pointers; parser warnings.

Parser output is **derivative**. `raw_packet_path` + the raw file id are the
source-body ownership path; a row without a resolvable packet pointer must not
present `body_text` as canonical body. The parser never writes back into the
packet (the writer is the single sink) and introduces `bs4`, which is on every
forbidden-import guard list — so the parser is a separate gate with its own
dependency-extra + guard-allowlist decision. Do not bundle the parser into the
CloakBrowser runner.

## 16. Agent Runbook Update Requirements

Do **not** patch the runbook until the runner behavior exists. A later patch to
`orca-harness/docs/source_capture_agent_runbook.md` must:

- replace the current "Reddit pre-commercial anti-blocking capture | not
  implemented in this runbook state" row with a real runner-selection row;
- add required capture-unit spec fields and a `--capture-unit` + `--output`
  command example (plus the CloakBrowser install line as a separate gated step);
- add restricted-network/per-operation escalation discipline (keep the
  `WinError 10061` sandbox-refusal guidance);
- keep fresh-output-directory + scratch-by-default discipline;
- add post-run inspection fields and a `cloakbrowser_caveat` (viewport-only;
  anti-blocking does not prove content sufficiency, login-wall absence, or that
  blocking was actually evaded; record observed access posture honestly);
- add the exit-code rows + the distinct `dependency_unavailable` /
  `contamination_stop` / `access_blocked` report tokens (§13);
- add the no-secret caveat (and the two-sided proxy boundary if proxy is in
  scope);
- add Reddit old-HTML / low-volume / no-discovery / `.json`-opportunistic /
  parser-derivative / commercial-reroute caveats;
- keep "do not simulate CloakBrowser with the honest browser runner."

Parallel edits at implementation time: `orca/product/spines/capture/source_capture_toolbox/README.md`
build-order step 10 + "Overall Gaps"; and a Direction-Change-Propagation receipt
in `orca-harness/docs/adapter_author_contract.md` if the runner adopts the
`stage_and_write_packet` helper for the browser family.

## 17. Required Test And Review Gates

Required later tests before agent-facing reuse (place the adapter under
`source_capture/adapters/` so it stays out of the top-level no-runtime-import
guard's glob):

- adapter unit tests with an injected fake CloakBrowser engine (no live backend);
- failure-classification tests: dependency-missing, timeout, empty DOM, empty
  screenshot, size-cap, `challenge_unsolved`, `access_blocked`;
- embedded-credentials-URL rejection (reuse `_validate_http_url`);
- runner CLI/spec validation: required fields, invalid mode, invalid volume,
  monitored cadence without stop date, commercial-posture conflict, missing
  acknowledgements, `decision_frame_bound` without a frame id;
- packet-writing contract: raw HTML / visible text / screenshot / metadata, slice
  ids, staging cleanup, warnings/limitations, receipt non-claims;
- **no-secret-in-packet** across `manifest.json`, `receipt.md`, `raw/`, staged
  metadata, **and logs** — inject sentinel secrets (cookie value, proxy
  `user:pass`, exit-IP, token) and assert absence (mandatory before any
  credentialed/proxied variant);
- **R2 — disclosability inverse-test**: when an anti-detect / proxy / JS-challenge
  method is used, assert the method **category is recorded** in the manifest; a
  packet with anti-detect used but no method provenance must **fail**;
- no-broad-crawl / no-discovery: given a captured page containing outbound links,
  assert the engine seam was invoked only with supplied locators;
- per-slice limitation visibility (no rollup hides a limited slice);
- old-Reddit fixture preservation using **local saved HTML**, not live Reddit;
- dependency-missing visible-blocker test (distinct token, no packet, no silent
  backend fallback);
- the `test_only_browser_snapshot_surfaces_name_playwright_dependency` allowlist
  guard needs an explicit edit (or parallel guard) for the CloakBrowser
  dependency name — the one test-surface that does not cleanly clone;
- parser-handoff fixture test **only if** parser scope is included;
- runbook command smoke test after the runner exists;
- adversarial implementation (code) review before normal agents use it.

Do not claim validation or readiness from this architecture pass.

## 18. Implementation Sequence For A Later Authorized Pass

Separately authorized, in order:

1. Define CloakBrowser adapter dataclasses, failure kinds, and the anonymous-only
   injected engine `Protocol` (R4). Export from `adapters/__init__.py`. Declare a
   CloakBrowser optional-dependency extra in `pyproject.toml` (declaring ≠
   installing).
2. Add fake-engine adapter unit + contract tests proving non-secret result shape,
   recorded method provenance (R2), and visible failures — provable offline with
   zero CloakBrowser install.
3. Build the runner accepting `--capture-unit` + `--output`, mapping adapter
   results through `stage_and_write_packet`; define `CLOAKBROWSER_NON_CLAIMS`;
   put anti-blocking provenance in the open `access_posture` axis.
4. Add no-secret, disclosability-inverse, no-discovery, exit-code, and
   contamination tests **before** runbook exposure.
5. **GATE (separate):** CloakBrowser install + one live bounded dry-run + the
   adapter-author "one manual dry-run + adversarial review" before agent-facing
   reuse. The live `_CloakBrowserEngine.capture()` body is `BLOCKED_UNTIL_
   CLOAKBROWSER_API_KNOWN` until this gate.
6. Patch the runbook (and README/contract) with exact command, inputs, stops,
   inspection, report shape.
7. Add `reddit_thread_family_supplied`, then `reddit_bounded_listing_seed`, only
   after the minimal old-thread mode is closed enough to review.
8. **GATE (separate):** parser handoff (`bs4`) — its own dependency-extra,
   guard-allowlist decision, and tests. Not bundled into the runner.

## 19. Open Owner Decisions

- First implemented mode: only `reddit_old_html_thread`, or also a finite supplied
  thread-family list?
- Small monitored Reddit-set support in v0, or deferred until candidate intake
  exists?
- May `candidate_or_scouting` units run at all before a Candidate Signal Intake /
  Corpus Intake contract exists (none exists today, so they have no compliant
  Data Capture handoff destination)?
- Parser handoff in the same tranche as the runner, or a separate follow-on?
- Exact `volume_ceiling` acceptable for Reddit v0?
- LinkedIn fully out of this runner until the separate LinkedIn/Reddit
  concurrent-structure architecture is accepted?
- **R1 — runner exit-code convention:** keep frozen `0`/`2`/`3` with distinct
  report tokens (recommended default), or amend the adapter-author contract to add
  exit `4` (contamination) / `5` (dependency-unavailable) uniformly?
- What CloakBrowser API surface is actually available locally, and does its
  absence block implementation (it blocks the live engine body only)?
- Which artifact is canonical — this independent pass or the prior `_v0.md`?

## 20. Non-Claims

This artifact is not: implementation authorization; CloakBrowser install proof;
live capture authorization; scraping execution; broad-crawling authorization;
source-discovery authorization; storage/queue/scheduler/dashboard/deployment/
production-runtime design; credential/session/profile import authorization;
CAPTCHA-solving-service authorization; source-quality scoring; fixture admission;
ECR/Cleaning/Judgment/buyer-proof/commercial-evidence design; legal sufficiency;
or validation/readiness. It does not supersede the prior `_v0.md` unless the owner
says so, and it authorizes no commits, pushes, or PRs.

## 21. Closeout — Why No Direction-Change-Propagation Receipt Is Required

This pass **applies existing authority** (CloakBrowser selection and third-tranche
authorization; the discoverable-or-entitled + disclosable source-access boundary
and hard stops; the Source Capture Packet model, writer, closed vocabularies, and
posture-honesty rule; the adapter-author conventions; the Reddit planning thread's
capture-unit fields, G1–G16 gates, non-promoting ladder, and candidate-intake gap;
the packet fixture/retention/sensitivity decision) to a **new
implementation-architecture target** — the CloakBrowser runner contract. It is an
advisory routing object: it **recommends**, it does not change any durable rule
future agents must follow, and it authorizes nothing.

Therefore no `direction_change_propagation` receipt is required from this pass, on
the same basis as the sibling
`reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`
(`doctrine_change: no`). The **doctrine-changing step is a later, separately
authorized implementation/runbook patch** (and, if chosen, the exit-code
convention amendment in R1) — that step carries its own propagation receipt and
its own stale-language search.

Note for the owner: the prior `_v0.md` chose to record a full
`direction_change_propagation` receipt (trigger `architecture_doctrine`). Both
artifacts cannot be canonical; whichever the owner keeps should resolve this
single difference (record-a-receipt vs apply-existing-authority) so the live
recommendation is internally consistent.

## 22. Next Authorized Step

Owner review of (a) which CloakBrowser runner architecture is canonical — this
independent pass or the prior `_v0.md` — and (b) whether to absorb refinements
R1–R4. If accepted, the smallest complete next authorized step is a **bounded
implementation-scoping prompt for the CloakBrowser adapter contract only** — not
the runner, not parser handoff, not live capture, not runbook exposure.

Implementation scoping should return `BLOCKED` if the actual CloakBrowser API
surface is still unknown or cannot be represented without secret-bearing result
fields, hidden profile/session state, source discovery, or non-disclosable method
provenance.
```
