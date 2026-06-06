# Source Capture — Anti-Blocking HTTP Ladder: Daimler Rung-Resolution Closeout — Delegated Adversarial Artifact Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch prompt (adversarial artifact review)
scope: >
  Commission prompt for a de-correlated, different-family adversarial ARTIFACT
  review-and-patch pass on the Daimler anti-block-ladder rung-resolution closeout;
  the commissioning home model (CA) adjudicates the returned edits.
use_when:
  - Running the delegated adversarial artifact review-and-patch pass on the Daimler rung-resolution closeout.
authority_boundary: retrieval_only
```

> Provisional Orca delegated review-and-patch convention
> (`.agents/workflow-overlay/delegated-review-patch.md`). This is a commissioned,
> bounded-executor pass on ONE authored artifact. Your edits + verdict are
> **decision input only** — not validation, not readiness, not a formal review
> verdict, not patch authorization. The commissioning Chief Architect (home model)
> adjudicates every change before anything is kept.

## De-correlation (who-constraint, not a model recommendation)

- The author / home model is **Claude, Opus-class**. To satisfy de-correlation you
  (the reviewer) must be a **different, non-Opus model family**. If you are an
  Opus-class or Claude-family model, **stop** and report that de-correlation is not
  satisfied rather than reviewing.
- Do **not** recommend, rank, or imply any runtime model in your output. Model
  choice is operator-owned (Orca review-lane model-neutrality).

## What this artifact is (judge against intent)

The target is a **durable toolbox closeout** recording a **live rung-resolution test** of
an already-committed anti-blocking HTTP capture arm against three public Daimler
investor-relations PDFs that returned HTTP `403` behind an Akamai edge. The arm itself
(adapter + runner + `block_shell` honesty guard) is **off-scope, committed at `3ca8090`,
and already passed a delegated code-review + CA adjudication** — do not reopen it.

The **anchor is honest representation**: determine the lowest rung that *honestly* beats
the `403`, never optimize toward "make the 403 disappear." The closeout must not let a
reader trust a capture more than the evidence supports. Specifically: a retrieved PDF is
at most a **"well-formed PDF container"**, never "authenticated / verified source content";
"still-blocked" would have been a fully valid honest outcome; and a single live result is
not a settled capability. Your job is to find where the closeout's wording, structure, or
omissions **overclaim, launder a limitation, or drift past the evidence**.

## Method (adopt this posture)

1. **First, frame the fake-pass / overclaim failure modes (deep-thinking posture).** Before
   listing findings, enumerate the concrete ways THIS closeout could mislead a future reader
   into trusting the capture more than the run proved — overstated wall inference, a
   discriminator that could pass a decoy, a missing or buried caveat, an over-read shortcut,
   or a header field that implies more than retrieval.
2. **Then perform an adversarial artifact review** (Orca `workflow-adversarial-artifact-review`
   posture) against the focus below, maximally adversarial about material, decision-relevant
   overclaim.
3. **Then propose the bounded patch** — edits to the single closeout file only.

## Preflight pins (state your posture before reviewing)

- worktree `C:\Users\vmon7\Desktop\projects\orca-wt-antiblock-http` · branch
  `feat/anti-block-http-ladder` · HEAD `3ca8090` · target file **untracked** (not committed).
- You have **no repo access**; the complete artifact under review is embedded verbatim below.
  Review it in place; do not request or assume a different checkout.
- The empirical facts in the closeout (HTTP statuses, byte sizes, `%PDF-` magic, SHA256s, the
  Akamai block-page markers) are the run's observed evidence. You are reviewing whether the
  closeout's **claims stay within that evidence**, not re-running the capture.

## Bounded patch scope (edit only this; everything else flag-only)

- `docs/product/source_capture_toolbox/source_capture_anti_blocking_http_ladder_daimler_rung_resolution_closeout_v0.md`

Everything else — the committed arm code (`orca-harness/source_capture/**`, `runners/**`,
`tests/**` at `3ca8090`), the Daimler receipt, all other `docs/` and
`.agents/workflow-overlay/` files — is **read-only / flag-only**. If the correct fix lies
off-scope, **flag it, do not edit it** (defer to `.agents/workflow-overlay/safety-rules.md`).
If the problem is **design-level** rather than wording-level, return `NEEDS_ARCHITECTURE_PASS`,
stop patching, and return findings only (quarantine any partial edit).

## Review focus (maximally adversarial on the overclaim / fake-pass surface)

1. **Wall-keying inference.** The closeout claims "Akamai keyed on request header/UA
   completeness, not TLS/JA3," inferred from a rung-0 (bot User-Agent, minimal headers, Python
   TLS) → `403` vs rung-1 (full Chrome headers, *same* Python TLS) → `200` flip. Is that
   inference warranted? It does **not** isolate User-Agent-alone from the fuller header set. Is
   the claim worded within the evidence, or does it overreach (e.g., imply a general Akamai
   mechanism rather than "this response, this config, this date")?
2. **PDF discriminator false-pass surface.** Sufficiency rests on {HTTP 2xx +
   `Content-Type: application/pdf` + leading `%PDF-` + `byte_count == Content-Length` +
   `Content-Encoding: identity`}. Could a block/challenge/decoy `200` still pass all six? Is the
   "well-formed PDF container, **not** content authenticity" boundary held **consistently**
   everywhere, or does any line (the table "verdict", "Result — lowest sufficient rung",
   "SUFFICIENT") read as verified/authentic source content?
3. **Non-claim completeness.** Are the version-identity limit (current 2022 body;
   post-`2019-05-21` cutoff; `pre_cutoff_identity_not_proven` stands) and the one-data-point
   limit (one Akamai config/origin/date; not "rung-1 beats Akamai"; not "capability settled")
   complete and prominent — or understated, buried, or missing a case?
4. **Same-origin control shortcut.** The rung-0 `403` control was run only on DSU-001, then
   assumed for DSU-002/003 (rung-1 succeeded on all three). Is that disclosed honestly, or does
   the table/prose imply DSU-002/003 were independently shown to be blocked at rung-0?
5. **Retrieval header + lifecycle hygiene.** Per `.agents/workflow-overlay/retrieval-metadata.md`:
   is the header correct (`retrieval_header_version: 1`; `authority_boundary: retrieval_only`; no
   forbidden fields — no approval/validation/readiness/lifecycle/edit-permission)? Does the
   artifact anywhere assert **validation, readiness, acceptance, or a registry update** (it must
   not)?

## The artifact under review (embedded verbatim)

````markdown
# Source Capture Anti-Blocking HTTP Ladder — Daimler Live Rung-Resolution Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Orca source-capture toolbox closeout (anti-block HTTP ladder live rung-resolution)
scope: >
  Live capture-ladder test of the committed rung-1 anti_blocking_http arm against the
  three Daimler DSU-001..003 Annual-Meeting 2019 PDFs that returned HTTP 403, to
  determine the lowest sufficient anti-block rung. Honest representation over
  "make the 403 disappear."
use_when:
  - Choosing an anti-block rung against a header/UA-keyed (Akamai-class) 403 wall.
  - Checking whether the rung-1 anti_blocking_http arm has been live-tested, and against what.
  - Before claiming rung-1 anti-block capability "settled" (this is one data point; see Non-Claims).
authority_boundary: retrieval_only
branch_or_commit: feat/anti-block-http-ladder @ 3ca8090 (the arm under test)
open_next:
  - docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
downstream_consumers:
  - Daimler DSU-001..003 source-body preservation + receipt/registry reconciliation pass (now unblocked; separate authorization).
  - Any future "rung-1 anti-block capability settled" claim (requires cross-family review).
stale_if:
  - The Mercedes-Benz/Akamai edge reconfigures to TLS/JA3 or behavioral bot checks (rung-1 may no longer suffice).
  - The rung-1 arm changes from 3ca8090.
```

## What this is

A live test of the **committed** rung-1 anti-block arm — not arm construction. The arm
(`anti_blocking_http` adapter + runner + `block_shell` honesty guard) was built,
delegate-reviewed, CA-adjudicated accept-in-full, and committed at `3ca8090`. This run
answers the one empirical question the build left open: **which ladder rung honestly
beats the documented Daimler HTTP 403** — captured as honest packets and this durable
rung-resolution lesson. Capture date: 2026-06-06.

## Result — lowest sufficient rung

**rung-1 (`anti_blocking_http`, profile `header_complete_stdlib`) is the lowest sufficient
rung for all three DSUs.** Each returned a well-formed PDF body that passed the
PDF-container discriminator (below).

| DSU | URL | rung-0 `direct_http` (control) | rung-1 `anti_blocking_http` | verdict |
|---|---|---|---|---|
| 001 | …/daimler-ir-am-agenda-2019.pdf | 403 Forbidden, `text/html`, 481 B — Akamai "Access Denied" page | 200, `application/pdf`, 2,689,478 B, `%PDF-1.4`, identity, `content_unverified` | **rung-1 SUFFICIENT** |
| 002 | …/daimler-ir-am-hivedownagreement-2019.pdf?r=dai | (control established on 001; same origin) | 200, `application/pdf`, 1,330,478 B, `%PDF-1.6`, identity, `content_unverified` | **rung-1 SUFFICIENT** |
| 003 | …/daimler-ir-am-hivedownreport-2019.pdf | (control established on 001) | 200, `application/pdf`, 4,121,124 B, `%PDF-1.6`, identity, `content_unverified` | **rung-1 SUFFICIENT** |

Durable evidence — SHA256 of each retrieved body (the scratch bytes are ephemeral; these
hashes are the durable record):

- DSU-001 rung-1 body: `ad2dd0669ebe1dbb5bfd7ba725ff811206f11f8e7ee49b87f623d27fd4c5a843` (2,689,478 B; `Last-Modified` 2022-11-30; `ETag "2909c6-5eea523c85b88"`)
- DSU-002 rung-1 body: `88adb707844353d2064adbe98c28288199ff3109c85645b5e8f008eb80e3b379` (1,330,478 B)
- DSU-003 rung-1 body: `e8d1c83d829a6926af75d0c1ef122110f56631795770244f3e4b10f63fe52a55` (4,121,124 B)
- DSU-001 rung-0 control body (Akamai block page): `bf5f796e1ae58b5927be2a0ddcd74676f8a1239edb5fd5673aa66be80a4ace06` (481 B)

## The wall

**Akamai.** The rung-0 control body is a textbook Akamai edge block: title "Access Denied",
`Reference #18.ed174b17.1780749963.234882d1`, and `https://errors.edgesuite.net/...`
(edgesuite.net is Akamai's domain).

**It keyed on request header/UA completeness, not TLS/JA3.** rung-1 shares rung-0's stdlib
(Python `urllib`) TLS fingerprint and differs *only* by sending the full desktop-Chrome
header profile (`User-Agent`, `Accept*`, `Sec-CH-UA*`, `Sec-Fetch-*`). That alone flipped
403→200. Therefore the higher rungs were unnecessary:

- **rung-2 `curl_cffi` (TLS/JA3 impersonation)** — not needed; the wall was not TLS-keyed here. (Remains gated behind an explicit owner dependency go.)
- **rung-3 `browser_snapshot`** — not run, and independently shape-mismatched for PDF byte capture: the runner preserves rendered DOM + visible text + screenshot with no raw-response-body path, so it cannot return `%PDF-` bytes. Demoted before the run.
- **rung-4 Patchright / rung-5 residential proxy / rung-6 cloakbrowser** — not reached. (cloakbrowser is another lane and off-limits.)

## How "sufficient" was decided — the PDF discriminator

`block_shell` classifies bodies as `BLOCK_SHELL` / `EMPTY` / `CONTENT_UNVERIFIED` with **no
positive CONTENT class**, so a binary PDF returns `content_unverified` (signal `null`) — that
is honest, not a miss. Sufficiency for a PDF target was decided by an **interpretation-layer
discriminator over already-recorded provenance — not by weakening `block_shell`**:

1. HTTP 2xx, **and**
2. no block-shell signature (`content_unverified`, signal `null`), **and**
3. `Content-Type: application/pdf`, **and**
4. body begins with `%PDF-`, **and**
5. `byte_count == Content-Length`, **and**
6. `Content-Encoding: identity` (preserved bytes are byte-faithful / hash-honest).

All three DSUs passed all six. This establishes that **a well-formed PDF container of plausible
size was retrieved** — it does **not** certify content authenticity.

## Non-claims / honest limits

- `content_unverified` stands. The PDFs were not parsed or validated for semantic content;
  no claim that these are the authentic agenda / hive-down agreement / hive-down report
  beyond container validity.
- **Version identity:** `Last-Modified` is 2022-11-30 (DSU-001). These are the **current**
  bodies, **post-cutoff** (case cutoff 2019-05-21). Capture does **not** prove pre-cutoff
  version identity; the receipt's `pre_cutoff_identity_not_proven` stands.
- **One data point.** One Akamai configuration, one origin, one date. This is **not** a general
  "rung-1 beats Akamai" claim — Akamai can be configured for JA3/behavioral checks that
  rung-1 would not beat. Elevating this to "rung-1 anti-block capability settled" requires
  cross-family review plus more targets/wall-classes.
- Not validation, readiness, acceptance, or a registry update. Not the Daimler source-body
  preservation pass.

## Receipt linkage

The receipt `daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md` records a
`stale_if` condition: "Official Mercedes-Benz Group PDF URLs become accessible and bodies are
captured." That condition is now **true** for rung-1. Reconciling the receipt + source
registry and actually preserving the bodies durably (with SHA256) is a **separate, now-unblocked
pass** (see `downstream_consumers`), requiring its own authorization. This closeout does not
perform it.

## Reproduce

From the worktree `orca-harness/`, per URL (public-content-only; live fetch needs
per-operation network approval, never standing):

```
python runners/run_source_capture_antiblock_http_packet.py \
  --url <pdf-url> \
  --decision-question "<question>" \
  --output <scratch-dir> \
  --source-family regulatory_filing \
  --max-bytes 50000000
```

Then apply the six-point discriminator to the preserved `*_response_body.bin` and
`*_response_metadata.json`. rung-0 (`run_source_capture_http_packet.py`) is the honest
control that reproduces the block.
````

## Return (paste-ready courier back to the commissioning CA)

Return all of:

- the **edited target file content** (or a **unified diff** of your working-tree edits to the
  single closeout file, **not committed**) implementing only the changes you would defend;
- **per-change source citations** — neutral in tone (factual line/evidence references, no
  advocacy or editorializing) but decision-sufficient in substance, so the CA's veto stays
  informed;
- a **verdict** and a **residual-risk note** (your argument lives here, not in the citations);
- a compact **`review_summary`** YAML: each finding with `severity` (`critical` | `major` |
  `minor`), `location`, `failure_mode`, `minimum_closure_condition`, `next_authorized_action`;
  plus overall `verdict` and `residual_risk`.

If the appropriate review lane is unavailable in your runtime, return
`BLOCKED_REVIEW_LANE_UNAVAILABLE` with the reason rather than improvising.

---
Model note: model choice is operator-owned; de-correlation is a who-constraint (a different,
non-Opus family), not a runtime-model recommendation.
