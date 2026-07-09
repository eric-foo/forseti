# Archive.org Capture Runner — Resilience Learnings v0 (advisory; feeds a capture-lane hardening prompt)

```yaml
retrieval_header_version: 1
artifact_role: Learnings / failure-diagnosis note (advisory; produced by the demand-read lane to feed a future capture-lane hardening prompt; NOT capture doctrine, NOT validation, NOT a runner spec)
scope: >
  Diagnoses why the first archive.org binding capture (Topicals Faded PDP via
  run_source_capture_archive_packet.py) took four attempts despite the body being
  reliably retrievable throughout, and records the learnings + recommended fixes a
  capture-lane prompt should encode so it does not recur. Separates archive.org-side
  flakiness (external) from runner-default fragility (root cause, fixable) from
  operational pacing error (contributory).
use_when:
  - Authoring a capture-lane prompt to harden the archive.org runner.
  - Running an archive.org binding capture (apply the parameter + pacing learnings now).
  - Checking why an archive capture returned availability-only / attempt_failed.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md   # the capture method (human-rate, blocked-is-a-hypothesis, availability != body)
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md       # per-source recon; archive availability != body pattern
stale_if:
  - The archive runner gains retry/backoff, a larger default timeout, or a direct-body fallback (fold the fix in; this note becomes historical).
  - The capture-lane hardening prompt is authored and consumes these learnings.
status: ADVISORY_LEARNINGS_V0
```

## What happened (observed chronology, 2026-06-15)

Capturing the Topicals **Faded PDP** body (`mytopicals.com/collections/shop-all/products/faded`, ≤2021-03-15 cutoff) via `forseti-harness/runners/run_source_capture_archive_packet.py` into the case dir:

1. **Attempt 1 — PARTIAL.** Runner exit 0, but the CDX query returned **HTTP 503**; `snapshot_count 0`, `selected_snapshot null` → **no body**. Receipt honestly recorded `attempt_failed / access_failed:503 / availability-metadata parse_failed`.
2. **Diagnostic.** A standalone curl to the same CDX endpoint then returned **HTTP 000** (connection failed) — looked like an IP throttle from bursting.
3. **Attempt 2 (re-probe) — CDX 503 again,** still no body.
4. **Decisive diagnostic.** The **direct Wayback body route** (`web.archive.org/web/<ts>id_/<url>`, bypassing CDX) returned **HTTP 200, 230 KB, with the "54 Reviews" signal**; a fresh simpler CDX query returned **HTTP 200**. → CDX is **intermittently** flaky (503 on some requests, 200 on others), **not a hard IP ban**; the body-serving route is reliable.
5. **Attempt 3 (re-probe) — read timeout.** Runner exit 3, `read operation timed out` — the default `--timeout-seconds 20.0` is too short for archive.org's variable latency on the body fetch.
6. **Attempt 4 — GO.** With `--timeout-seconds 60`: body **242,414 bytes**, snapshot **20210210010815**, "Based on 54 Reviews" present, hash-pinned (`49b3ecab…`).

## Root-cause diagnosis (ranked)

1. **ROOT CAUSE — runner fragility to a known-flaky dependency (internal, fixable).** The capture failed not because the data was unreachable (the body was retrievable the whole time) but because the runner is not resilient to archive.org's intermittency. Sub-defects, leverage order:
   - **B1. No retry/backoff** on transient CDX **503 / timeout / connection** failures — a *single* transient failure kills the whole capture. (Highest leverage: alone would have saved attempts 1–2.)
   - **B2. Default timeout 20s too short** for archive.org's variable latency (60s succeeded). (Saved attempt 3.)
   - **B3. Hard CDX dependency for snapshot *selection*,** with no **direct-body fallback** even when gate-0 has already pinned the snapshot timestamp. CDX is needed to *discover* snapshots; once the ts is known, the reliable `id_` body route does not need CDX at all.
   - **B4. Conflates "CDX request failed (transient)" with "no snapshot exists (genuine)".** Both collapse to `selected_snapshot: null` / `snapshot_count 0`. A transient CDX failure must not read as a NO-GO — that is the named playbook failure ("a false 'blocked' abandons a capturable source"; cf. the Daimler genuine NO-GO, which was a *successful* CDX query returning no memento).
2. **TRIGGER — archive.org CDX intermittent 503 (external, unavoidable).** Proximate, not root; CDX is intermittently overloaded by design. The response is resilience (item 1), not a fix to archive.org.
3. **CONTRIBUTORY — operational bursting (behavior, fixable).** Gate-0 enumeration + body fetch + multiple runner attempts + checks fired in seconds violated the human-rate guardrail and likely worsened 503 frequency. Note the perverse loop: **the runner's no-retry pushes the operator toward *more* manual re-probes — i.e., more bursting.** Fixing B1 is *more* human-rate-respecting than operator-driven rapid retries.

## What the runner did RIGHT (preserve — do not regress)

It recorded `attempt_failed / access_failed:503 / selected_snapshot:null` **honestly** — no fabricated body, no fake success path. Any hardening must add **resilience without masking**: bounded retries, then an **honest exhausted-failure** record. Resilience, not concealment.

## Learnings + recommended fixes (for the capture-lane prompt to encode)

**Parameter-level (immediate; no code change — apply now):**
- **L1.** Always pass **`--timeout-seconds >= 60`** for archive.org captures; the 20s default is too short. (Confirmed: 60s succeeded where 20s timed out.)

**Runner-hardening (capture-lane owns; a hardening commission):**
- **L2.** **Retry transient CDX failures** (HTTP 503 / read-timeout / connection-reset) with **bounded exponential backoff** (e.g., 3 tries, 2s/5s/10s) before declaring `attempt_failed`. (Highest-leverage fix.)
- **L3.** **Direct-body fallback when the snapshot timestamp is known:** fetch via the Wayback `id_` route, bypassing CDX selection. Scoped to the *fetch* step when the ts is pinned — **not** a replacement for CDX *discovery*. Same bytes, hash-pinnable (no fidelity loss).
- **L4.** **Distinguish CDX-request-failure from no-snapshot-exists.** Only a *successful* CDX query returning zero mementos is a genuine availability NO-GO; a transient CDX error must be retried (L2) and, if exhausted, recorded as an **infra `attempt_failed`, never a source-level NO-GO**.

**Operational (discipline; reinforces existing playbook guardrails):**
- **L5.** **Human-rate pacing** — never burst archive.org (enumeration + multiple captures + checks in seconds triggers throttling). One capture at a time, spaced; let in-runner retry (L2) absorb transients instead of operator-driven rapid re-probes.
- **L6.** **Gate-0 recon pins the exact snapshot timestamp(s)** per target so captures can use the direct-body route (L3) and a tight cutoff, minimizing CDX dependence. (This session's gate-0 *did* find `20210210010815`; the runner just didn't use it directly.)
- **L7.** **Preserve honest failure recording** — the hardening must not mask a genuine exhausted-retry failure; after bounded retries, the receipt still records the real reason.

## For the capture-lane prompt this feeds

Commission shape: **harden `run_source_capture_archive_packet.py` for archive.org intermittency** — add bounded retry/backoff on transient CDX failures (L2), raise/clarify the default timeout (L1/B2), add a known-timestamp direct-body fallback (L3), and split the failure-vs-absence outcome so a transient error never reads as a source NO-GO (L4) — **while preserving the honest failure-recording behavior (L7).** Route the prompt through `workflow-prompt-orchestrator` per overlay rules.

## Non-Claims

- Advisory learnings only; not capture doctrine, not a runner spec, not validation/readiness. The runner-hardening fixes are recommendations for the capture lane to scope and execute under its own authority, not changes made here.
- The Faded capture itself is a real GO (body hash-pinned); the resilience findings do not affect that capture's validity.
- `product_learning` context; mints no vocabulary; reuses the playbook's two-axis bar / human-rate / blocked-is-a-hypothesis guardrails.
```text
This is advisory diagnosis only. It is not validation, not a runner spec, and not
proof of readiness.
```
