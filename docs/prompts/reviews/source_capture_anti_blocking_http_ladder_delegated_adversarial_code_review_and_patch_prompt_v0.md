# Source Capture — Anti-Blocking HTTP Ladder (rung-1): Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch prompt
scope: >
  Commission prompt for a de-correlated, different-family adversarial code
  review-and-patch pass on the rung-1 anti-blocking HTTP capture slice
  (honesty surface), home model adjudicates.
use_when:
  - Running the delegated review-and-patch pass on the anti-block HTTP arm.
authority_boundary: retrieval_only
```

> Provisional Orca delegated review-and-patch convention
> (`.agents/workflow-overlay/delegated-review-patch.md`). This is a commissioned,
> bounded-executor pass. Your diff + verdict are **decision input only** — not
> validation, not readiness, not a formal review verdict, not patch
> authorization. The commissioning Chief Architect (home model) adjudicates every
> hunk before anything is kept.

## De-correlation (who-constraint, not a model recommendation)

- The author / home model is **Claude, Opus-class**. To satisfy de-correlation
  you (the reviewer) must be a **different, non-Opus model family**. If you are an
  Opus-class or Claude-family model, stop and report that de-correlation is not
  satisfied rather than reviewing.
- Do **not** recommend, rank, or imply any runtime model in your output. Model
  choice is operator-owned (Orca review-lane model-neutrality).

## What this code is (judge against intent)

This is **rung-1 of an anti-blocking capture ladder** for Orca's Source Capture
Armory: a header/User-Agent-complete **stdlib** HTTP fetch meant to get past
*naive* UA/header bot-sniffing on **public** sources that return `403` to a plain
bot client. It does **not** impersonate the TLS/JA3 fingerprint (that is a later
rung) and uses no proxy.

The **anchor goal is honest representation**: determine the lowest sufficient
rung that *honestly* beats a documented `403` — never optimize toward "make the
`403` disappear" over truthfully recording what was obtained. A returned body is
**never** to be claimed as real source content; the best honest state is
"`200`, body preserved, no block signature, content not certified." The whole
point of the slice is that it cannot fake success.

## Method (adopt this posture)

1. **First, frame failure modes (deep-thinking posture).** Before listing
   findings, enumerate the concrete ways this code could *fake-pass* — record a
   block/challenge or otherwise non-content body as if it were a
   successful/honest capture, or hide a limited capture behind a clean rollup.
2. **Then perform an adversarial code review** of the embedded diff against the
   focus below, maximally adversarial about material, decision-relevant failure
   modes (Orca `workflow-code-review` posture). Then propose the bounded patch.

## Preflight pins (state your posture before reviewing)

- worktree `C:\Users\vmon7\Desktop\projects\orca-wt-antiblock-http` · branch
  `feat/anti-block-http-ladder` · HEAD `7be0866` · target files **uncommitted**.
- Validation observed: full unit suite **237 passed / 1 skipped / exit 0** in
  isolation. The new code's own tests already pass — your job is to find what the
  tests **do not** catch.
- You have no repo access; the complete code under review is embedded as a
  unified diff at the end of this prompt. Review the embedded diff in place; do
  not request or assume a different checkout.

## Bounded patch scope (edit only these; everything else flag-only)

- `orca-harness/source_capture/block_shell.py`
- `orca-harness/source_capture/adapters/anti_blocking_http.py`
- `orca-harness/runners/run_source_capture_antiblock_http_packet.py`
- `orca-harness/tests/unit/test_block_shell.py`
- `orca-harness/tests/unit/test_anti_blocking_http_adapter.py`
- `orca-harness/source_capture/adapters/__init__.py` (export only)

Everything else — other Orca sources, `.agents/workflow-overlay/`, the worktree's
committed code, and any installed / external / `jb` folders — is **read-only /
flag-only**. If the correct fix lies off-scope, **flag it, do not edit it**
(defer to `.agents/workflow-overlay/safety-rules.md`).

## Context the runner depends on (committed, off-scope — do not patch)

- `source_capture.packet_assembly.validate_capture_posture_honesty` rejects a
  clean capture-level rollup that hides a limited slice: if any slice carries
  `limitations` (or an `unknown_with_reason` posture axis), the capture-level
  `limitations` must be non-empty (or the same axis must also be
  `unknown_with_reason`). The runner is expected to satisfy this by passing the
  same limitation list at both slice and capture level.
- `known_fact` / `not_attempted` / `not_applicable` / `unknown_with_reason`
  build `VisibleFact` posture values; `stage_and_write_packet` performs strict
  current-schema validation at write.

## Review focus (maximally adversarial on the fake-pass surface)

1. **False-negative gaps in `block_shell.classify_capture_body`.** Can a real
   block/challenge/interstitial shell be classified `CONTENT_UNVERIFIED`? Probe:
   the signature set (missing vendors/markers — e.g. Akamai "Reference #",
   generic "request blocked", AWS WAF, Imperva, Sucuri); header logic (key
   casing/folding, multi-valued headers); the 8192-byte decode-prefix scan (a
   marker located past byte 8192, or split across the scan boundary; a body whose
   real content begins with a benign substring that matches a signature →
   false-positive that mislabels real content as a block); `utf-8 errors=ignore`
   silently dropping marker bytes; `body.strip()` emptiness handling.
2. **Posture laundering in the runner.** Does any path map a `200`-with-shell, an
   empty/whitespace body, or a non-2xx into a success/content claim? Is the
   `CONTENT_UNVERIFIED` + 2xx wording genuinely non-committal, or does it read as
   a capture-success? Is the `BLOCK_SHELL` branch reachable for **every** shell
   the classifier can detect, and does a non-2xx **block-shell** surface both the
   block and the status honestly?
3. **`validate_capture_posture_honesty` satisfaction.** Are limitations surfaced
   at **both** slice and capture level for `block_shell` / `empty` / non-2xx?
   Could a limited slice ever ship with an empty capture-level `limitations` list
   and trip (or worse, slip past) the assembler guard?
4. **Honesty-invariant pinning.** Are "no positive `CONTENT` class" and "a `200`
   is never recorded as captured content" actually pinned by the tests, or could
   a future edit silently reintroduce a content claim while keeping the suite
   green? Do the tests assert the *honest* behavior, or only the happy path?
5. **Doctrine bounds.** Does anything imply TLS/JA3 or proxy capability (it must
   not — header-complete stdlib only)? Anything that reads as entitlement /
   paywall / login-gate bypass (forbidden)? Is the `Accept-Encoding: identity`
   rationale (hash-honest preserved bytes, since stdlib `urllib` does not
   transparently decompress) sound, or does it create a correctness/honesty
   problem (e.g. a server that ignores it and gzips anyway)?

## Return (paste-ready courier back to the commissioning CA)

Return all of:

- a **unified diff** (working-tree edits to the in-scope files, **not
  committed**) implementing only the changes you would defend;
- **per-change source citations** — neutral in tone (factual line/contract
  evidence, no advocacy or editorializing) but decision-sufficient in substance,
  so the CA's veto stays informed;
- a **verdict** and a **residual-risk note** (your argument lives here, not in
  the citations);
- a compact **`review_summary`** YAML: each finding with `severity`
  (`critical` | `major` | `minor`), `location`, `failure_mode`,
  `minimum_closure_condition`, `next_authorized_action`; plus overall `verdict`
  and `residual_risk`.

**Escalation valve.** If the core problem is design-level rather than
patch-level, return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial
diff, and return findings only — do not force a patch onto a broken design.

## Review-use boundary

Your findings and diff are **decision input only**. They are not approval,
validation, readiness, mandatory remediation, or executor-ready patch authority.
The commissioning Chief Architect adjudicates each hunk against your citations
and the anchor intent and may accept, modify, or reject any change — including
individually defensible ones — before anything is kept.

## Code under review (unified diff vs HEAD `7be0866`; new files shown in full)

```diff
diff --git a/orca-harness/runners/run_source_capture_antiblock_http_packet.py b/orca-harness/runners/run_source_capture_antiblock_http_packet.py
new file mode 100644
index 0000000..b171073
--- /dev/null
+++ b/orca-harness/runners/run_source_capture_antiblock_http_packet.py
@@ -0,0 +1,320 @@
+from __future__ import annotations
+
+import argparse
+import json
+import sys
+from pathlib import Path
+from typing import Sequence
+
+if __package__ in {None, ""}:
+    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
+
+from source_capture import (
+    CaptureModeCategory,
+    PacketTiming,
+    SourceCaptureSlice,
+    known_fact,
+    not_applicable,
+    not_attempted,
+    unknown_with_reason,
+)
+from source_capture.cli_support import build_optional_fact
+from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
+from source_capture.block_shell import CaptureBodyClass, classify_capture_body
+from source_capture.adapters import (
+    AntiBlockingHttpCaptureFailure,
+    fetch_anti_blocking_http_capture,
+)
+
+
+ANTI_BLOCKING_HTTP_NON_CLAIMS = [
+    "not the honest direct_http baseline",
+    "not anti-detect browser automation",
+    "not TLS/JA3 fingerprint impersonation",
+    "not proxy or session injection",
+    "not API SDK use",
+    "not archive retrieval",
+    "not media preservation",
+    "not scraper framework use",
+    "does not certify a returned body as real source content",
+    "not ECR design",
+    "not Cleaning implementation",
+    "not Judgment scoring",
+    "not buyer proof",
+    "not commercial-readiness logic",
+]
+
+
+def run_source_capture_antiblock_http_packet(
+    *,
+    url: str,
+    source_family: str,
+    source_surface: str,
+    decision_question: str,
+    output_directory: Path,
+    capture_context: str,
+    operator_category: str,
+    capture_mode: CaptureModeCategory,
+    session_id: str | None,
+    actor_audience_context,
+    visible_mode_changes: Sequence[str],
+    source_publication_or_event,
+    source_edit_or_version,
+    cutoff_posture,
+    recapture_time,
+    re_capture_relationship,
+    warnings: Sequence[str],
+    limitations: Sequence[str],
+    timeout_seconds: float,
+    max_bytes: int,
+) -> tuple[int, str]:
+    capture_result = fetch_anti_blocking_http_capture(
+        url=url,
+        timeout_seconds=timeout_seconds,
+        max_bytes=max_bytes,
+    )
+    if isinstance(capture_result, AntiBlockingHttpCaptureFailure):
+        return 3, capture_result.message
+
+    classification = classify_capture_body(
+        status=capture_result.status,
+        headers=capture_result.response_headers,
+        body=capture_result.body,
+    )
+    status_ok = 200 <= capture_result.status < 300
+
+    posture_limitations: list[str] = []
+    if classification.classification == CaptureBodyClass.BLOCK_SHELL:
+        access_posture = known_fact(
+            f"anti_blocking_http access blocked at HTTP {capture_result.status} "
+            f"{capture_result.reason or 'without reason'}: {classification.detail}; "
+            "block/challenge shell preserved, not source content"
+        )
+        posture_limitations.append(
+            "visible_capture_limitation: anti_blocking_http preserved a block/challenge shell "
+            f"({classification.signal}) at HTTP {capture_result.status}, not source body"
+        )
+    elif classification.classification == CaptureBodyClass.EMPTY:
+        access_posture = known_fact(
+            f"anti_blocking_http returned HTTP {capture_result.status} with an "
+            "empty/whitespace-only body; no source content preserved"
+        )
+        posture_limitations.append(
+            "visible_capture_limitation: anti_blocking_http preserved an "
+            "empty/whitespace-only body, no source content"
+        )
+    elif not status_ok:
+        access_posture = known_fact(
+            f"anti_blocking_http access_failed with HTTP {capture_result.status} "
+            f"{capture_result.reason or 'without reason'}; response body preserved"
+        )
+        posture_limitations.append(
+            f"access_failed: anti_blocking_http HTTP {capture_result.status}; response body preserved"
+        )
+    else:
+        access_posture = known_fact(
+            f"anti_blocking_http returned HTTP {capture_result.status}; body preserved; "
+            "no block/challenge signature detected; body not certified as source content"
+        )
+
+    packet_warnings = list(warnings) + capture_result.warning_notes
+    packet_limitations = list(limitations) + capture_result.limitation_notes + posture_limitations
+
+    metadata = dict(capture_result.metadata)
+    metadata["body_classification"] = classification.classification.value
+    metadata["body_classification_signal"] = classification.signal
+    metadata["body_classification_detail"] = classification.detail
+
+    artifacts: list[tuple[str, bytes]] = [
+        ("anti_blocking_http_response_body.bin", capture_result.body),
+        (
+            "anti_blocking_http_response_metadata.json",
+            (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode("utf-8"),
+        ),
+    ]
+    file_ids = staged_file_id_map(artifacts)
+
+    mode_changes = list(visible_mode_changes) + [
+        f"anti_blocking_http_profile:{capture_result.impersonation_profile}"
+    ]
+
+    timing = PacketTiming(
+        source_publication_or_event=source_publication_or_event
+        or unknown_with_reason("anti_blocking_http adapter did not infer source publication or event timing"),
+        source_edit_or_version=source_edit_or_version
+        or unknown_with_reason("anti_blocking_http adapter did not infer source edit or version timing"),
+        capture_time=known_fact(str(capture_result.metadata["capture_timestamp"])),
+        recapture_time=recapture_time
+        or not_applicable("anti_blocking_http packet did not model an earlier capture by default"),
+        cutoff_posture=cutoff_posture
+        or unknown_with_reason("anti_blocking_http runner did not receive cutoff posture metadata"),
+    )
+    archive_posture = not_attempted("anti_blocking_http adapter does not query archive or history services")
+    media_posture = not_attempted(
+        "anti_blocking_http adapter preserves the response body only and does not fetch linked media assets"
+    )
+    recapture_posture = re_capture_relationship or not_applicable(
+        "no prior source capture packet was supplied for this anti_blocking_http capture"
+    )
+
+    result = stage_and_write_packet(
+        output_directory=output_directory,
+        staged_artifacts=artifacts,
+        source_slices=[
+            SourceCaptureSlice(
+                slice_id="slice_01",
+                locator=known_fact(capture_result.final_url),
+                timing=timing,
+                access_posture=access_posture,
+                archive_history_posture=archive_posture,
+                media_modality_posture=media_posture,
+                re_capture_relationship=recapture_posture,
+                limitations=packet_limitations,
+                warning_notes=packet_warnings,
+                preserved_file_ids=[
+                    file_ids["anti_blocking_http_response_body.bin"],
+                    file_ids["anti_blocking_http_response_metadata.json"],
+                ],
+            )
+        ],
+        source_family=source_family,
+        source_surface=source_surface,
+        source_locator=known_fact(capture_result.requested_url),
+        decision_question=decision_question,
+        capture_context=capture_context,
+        actor_audience_context=actor_audience_context
+        or unknown_with_reason("actor or audience context was not supplied to the anti_blocking_http runner"),
+        capture_mode=capture_mode,
+        operator_category=operator_category,
+        session_identity=session_id,
+        visible_mode_changes=mode_changes,
+        source_publication_or_event=timing.source_publication_or_event,
+        source_edit_or_version=timing.source_edit_or_version,
+        cutoff_posture=timing.cutoff_posture,
+        recapture_time=timing.recapture_time,
+        access_posture=access_posture,
+        archive_history_posture=archive_posture,
+        media_modality_posture=media_posture,
+        re_capture_relationship=recapture_posture,
+        warnings=packet_warnings,
+        limitations=packet_limitations,
+        receipt_summary=(
+            f"anti_blocking_http packet ({capture_result.impersonation_profile}) for {source_family} "
+            f"with HTTP {capture_result.status}, body classification "
+            f"'{classification.classification.value}', {len(capture_result.body)} preserved body bytes."
+        ),
+        receipt_non_claims=ANTI_BLOCKING_HTTP_NON_CLAIMS,
+    )
+    return 0, result.output_directory
+
+
+def _build_parser() -> argparse.ArgumentParser:
+    parser = argparse.ArgumentParser(
+        description=(
+            "Fetch one HTTP URL with a full desktop-Chrome header profile "
+            "(anti_blocking_http rung-1) and write a Source Capture Packet, classifying the "
+            "body as block-shell vs uncertified content. Does not impersonate TLS and does "
+            "not certify a body as source content."
+        )
+    )
+    parser.add_argument("--url", required=True)
+    parser.add_argument("--source-family", default="web_page")
+    parser.add_argument("--source-surface", default="anti_blocking_http")
+    parser.add_argument("--decision-question", required=True)
+    parser.add_argument("--output", type=Path, required=True)
+    parser.add_argument(
+        "--capture-context",
+        default="anti-blocking HTTP source capture (header-complete stdlib, rung-1)",
+    )
+    parser.add_argument("--operator-category", default="anti_blocking_http_cli_operator")
+    parser.add_argument(
+        "--capture-mode",
+        choices=[item.value for item in CaptureModeCategory],
+        default=CaptureModeCategory.STRUCTURED_ACCESS.value,
+    )
+    parser.add_argument("--session-id", default=None)
+    parser.add_argument("--timeout-seconds", type=float, default=20.0)
+    parser.add_argument("--max-bytes", type=int, default=5_000_000)
+    parser.add_argument("--actor-audience-context", default=None)
+    parser.add_argument("--actor-audience-context-unknown-reason", default=None)
+    parser.add_argument("--visible-mode-change", action="append", default=[])
+    parser.add_argument("--source-publication-or-event", default=None)
+    parser.add_argument("--source-publication-or-event-unknown-reason", default=None)
+    parser.add_argument("--source-edit-or-version", default=None)
+    parser.add_argument("--source-edit-or-version-unknown-reason", default=None)
+    parser.add_argument("--cutoff-posture", default=None)
+    parser.add_argument("--cutoff-posture-unknown-reason", default=None)
+    parser.add_argument("--recapture-time", default=None)
+    parser.add_argument("--recapture-time-not-applicable-reason", default=None)
+    parser.add_argument("--recapture-relationship", default=None)
+    parser.add_argument("--recapture-relationship-not-applicable-reason", default=None)
+    parser.add_argument("--warning", action="append", default=[])
+    parser.add_argument("--limitation", action="append", default=[])
+    return parser
+
+
+def main(argv: Sequence[str] | None = None) -> int:
+    parser = _build_parser()
+    args = parser.parse_args(argv)
+    try:
+        exit_code, message = run_source_capture_antiblock_http_packet(
+            url=args.url,
+            source_family=args.source_family,
+            source_surface=args.source_surface,
+            decision_question=args.decision_question,
+            output_directory=args.output,
+            capture_context=args.capture_context,
+            operator_category=args.operator_category,
+            capture_mode=CaptureModeCategory(args.capture_mode),
+            session_id=args.session_id,
+            actor_audience_context=build_optional_fact(
+                label="actor/audience context",
+                value=args.actor_audience_context,
+                unknown_reason=args.actor_audience_context_unknown_reason,
+            ),
+            visible_mode_changes=args.visible_mode_change,
+            source_publication_or_event=build_optional_fact(
+                label="source publication or event timing",
+                value=args.source_publication_or_event,
+                unknown_reason=args.source_publication_or_event_unknown_reason,
+            ),
+            source_edit_or_version=build_optional_fact(
+                label="source edit or version timing",
+                value=args.source_edit_or_version,
+                unknown_reason=args.source_edit_or_version_unknown_reason,
+            ),
+            cutoff_posture=build_optional_fact(
+                label="cutoff posture",
+                value=args.cutoff_posture,
+                unknown_reason=args.cutoff_posture_unknown_reason,
+            ),
+            recapture_time=build_optional_fact(
+                label="re-capture timing",
+                value=args.recapture_time,
+                not_applicable_reason=args.recapture_time_not_applicable_reason,
+            ),
+            re_capture_relationship=build_optional_fact(
+                label="re-capture relationship",
+                value=args.recapture_relationship,
+                not_applicable_reason=args.recapture_relationship_not_applicable_reason,
+            ),
+            warnings=args.warning,
+            limitations=args.limitation,
+            timeout_seconds=args.timeout_seconds,
+            max_bytes=args.max_bytes,
+        )
+    except ValueError as exc:
+        parser.exit(status=2, message=f"source capture anti_blocking_http failed: {exc}\n")
+    except Exception as exc:  # noqa: BLE001 - surface any adapter/writer failure as exit 3
+        parser.exit(status=3, message=f"source capture anti_blocking_http failed: {exc}\n")
+
+    if exit_code == 0:
+        print(message)
+        return 0
+
+    parser.exit(status=exit_code, message=f"source capture anti_blocking_http failed: {message}\n")
+    return exit_code
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/orca-harness/source_capture/adapters/__init__.py b/orca-harness/source_capture/adapters/__init__.py
index 9fcc494..a094e1c 100644
--- a/orca-harness/source_capture/adapters/__init__.py
+++ b/orca-harness/source_capture/adapters/__init__.py
@@ -1,3 +1,12 @@
+from source_capture.adapters.anti_blocking_http import (
+    ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
+    AntiBlockingHttpCaptureFailure,
+    AntiBlockingHttpCaptureFailureKind,
+    AntiBlockingHttpCaptureResult,
+    AntiBlockingHttpCaptureSuccess,
+    fetch_anti_blocking_http_capture,
+    header_complete_profile,
+)
 from source_capture.adapters.archive_org import (
     ArchiveOrgCaptureFailure,
     ArchiveOrgCaptureResult,
@@ -40,6 +49,11 @@ from source_capture.adapters.reddit_api import (
 )
 
 __all__ = [
+    "ANTI_BLOCKING_HTTP_METHOD_CATEGORY",
+    "AntiBlockingHttpCaptureFailure",
+    "AntiBlockingHttpCaptureFailureKind",
+    "AntiBlockingHttpCaptureResult",
+    "AntiBlockingHttpCaptureSuccess",
     "ArchiveOrgCaptureFailure",
     "ArchiveOrgCaptureResult",
     "ArchiveOrgCaptureSuccess",
@@ -65,6 +79,8 @@ __all__ = [
     "RedditPostCapture",
     "RedditPostFailure",
     "build_reddit_oauth_client",
+    "fetch_anti_blocking_http_capture",
+    "header_complete_profile",
     "fetch_archive_org_capture",
     "fetch_browser_snapshot_capture",
     "fetch_direct_http_capture",
diff --git a/orca-harness/source_capture/adapters/anti_blocking_http.py b/orca-harness/source_capture/adapters/anti_blocking_http.py
new file mode 100644
index 0000000..fab0ca4
--- /dev/null
+++ b/orca-harness/source_capture/adapters/anti_blocking_http.py
@@ -0,0 +1,278 @@
+from __future__ import annotations
+
+from dataclasses import dataclass
+from enum import StrEnum
+from http.client import HTTPResponse
+from typing import TypeAlias
+from urllib.error import HTTPError, URLError
+from urllib.parse import urlparse
+from urllib.request import Request, urlopen
+
+from harness_utils import utc_now_z
+
+
+DEFAULT_TIMEOUT_SECONDS = 20.0
+DEFAULT_MAX_BYTES = 5_000_000
+
+ANTI_BLOCKING_HTTP_METHOD_CATEGORY = "anti_blocking_http"
+DEFAULT_IMPERSONATION_PROFILE = "header_complete_stdlib"
+
+_DEFAULT_CHROME_USER_AGENT = (
+    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
+    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
+)
+
+
+class AntiBlockingHttpCaptureFailureKind(StrEnum):
+    NETWORK_ERROR = "network_error"
+    TIMEOUT = "timeout"
+    NO_BODY = "no_body"
+    SIZE_CAP_EXCEEDED = "size_cap_exceeded"
+
+
+@dataclass(frozen=True)
+class AntiBlockingHttpCaptureSuccess:
+    requested_url: str
+    final_url: str
+    status: int
+    reason: str
+    impersonation_profile: str
+    method_category: str
+    response_headers: dict[str, str]
+    metadata: dict[str, object]
+    body: bytes
+    warning_notes: list[str]
+    limitation_notes: list[str]
+
+
+@dataclass(frozen=True)
+class AntiBlockingHttpCaptureFailure:
+    requested_url: str
+    failure_kind: AntiBlockingHttpCaptureFailureKind
+    message: str
+    impersonation_profile: str
+    final_url: str | None = None
+    status: int | None = None
+    reason: str | None = None
+
+
+AntiBlockingHttpCaptureResult: TypeAlias = (
+    AntiBlockingHttpCaptureSuccess | AntiBlockingHttpCaptureFailure
+)
+
+
+def header_complete_profile(user_agent: str = _DEFAULT_CHROME_USER_AGENT) -> dict[str, str]:
+    """Full desktop-Chrome request header set for the ``header_complete_stdlib`` rung.
+
+    ``Accept-Encoding: identity`` is deliberate: stdlib ``urllib`` does not
+    transparently decompress ``gzip``/``br`` responses, so requesting an
+    uncompressed body keeps the preserved bytes byte-identical to what the server
+    served (hash-honest). Negotiating compression is a rung-2 (``curl_cffi``)
+    concern, not this rung's.
+    """
+    return {
+        "User-Agent": user_agent,
+        "Accept": (
+            "text/html,application/xhtml+xml,application/xml;q=0.9,"
+            "image/avif,image/webp,image/apng,*/*;q=0.8"
+        ),
+        "Accept-Language": "en-US,en;q=0.9",
+        "Accept-Encoding": "identity",
+        "Upgrade-Insecure-Requests": "1",
+        "Sec-CH-UA": '"Chromium";v="126", "Google Chrome";v="126", "Not.A/Brand";v="24"',
+        "Sec-CH-UA-Mobile": "?0",
+        "Sec-CH-UA-Platform": '"Windows"',
+        "Sec-Fetch-Dest": "document",
+        "Sec-Fetch-Mode": "navigate",
+        "Sec-Fetch-Site": "none",
+        "Sec-Fetch-User": "?1",
+    }
+
+
+def fetch_anti_blocking_http_capture(
+    *,
+    url: str,
+    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
+    max_bytes: int = DEFAULT_MAX_BYTES,
+    user_agent: str = _DEFAULT_CHROME_USER_AGENT,
+) -> AntiBlockingHttpCaptureResult:
+    """Header/UA-complete stdlib HTTP fetch (rung-1 anti-blocking).
+
+    Anti-blocking method category, distinct from the honest ``direct_http``
+    baseline: it sends a full desktop-Chrome header profile to get past naive
+    User-Agent / header sniffing. It does NOT impersonate the TLS/JA3 fingerprint
+    (stdlib ``urllib`` carries Python's TLS signature) -- that is rung-2.
+
+    The body is preserved verbatim; this adapter makes no claim that a returned
+    body is real source content (a server may return a 200 challenge/block shell).
+    Body-honesty classification belongs to the runner via ``block_shell``.
+    """
+    profile = DEFAULT_IMPERSONATION_PROFILE
+    normalized_url = _validate_http_url(url)
+    if timeout_seconds <= 0:
+        raise ValueError("timeout_seconds must be greater than zero")
+    if max_bytes <= 0:
+        raise ValueError("max_bytes must be greater than zero")
+
+    request = Request(normalized_url, headers=header_complete_profile(user_agent), method="GET")
+
+    try:
+        with urlopen(request, timeout=timeout_seconds) as response:
+            return _capture_response(
+                requested_url=normalized_url,
+                response=response,
+                timeout_seconds=timeout_seconds,
+                max_bytes=max_bytes,
+                impersonation_profile=profile,
+            )
+    except HTTPError as exc:
+        return _capture_response(
+            requested_url=normalized_url,
+            response=exc,
+            timeout_seconds=timeout_seconds,
+            max_bytes=max_bytes,
+            impersonation_profile=profile,
+        )
+    except URLError as exc:
+        return AntiBlockingHttpCaptureFailure(
+            requested_url=normalized_url,
+            failure_kind=_failure_kind_from_url_error(exc),
+            message=f"anti_blocking_http request failed: {exc.reason}",
+            impersonation_profile=profile,
+        )
+
+
+def _capture_response(
+    *,
+    requested_url: str,
+    response: HTTPResponse | HTTPError,
+    timeout_seconds: float,
+    max_bytes: int,
+    impersonation_profile: str,
+) -> AntiBlockingHttpCaptureResult:
+    status = int(response.getcode())
+    reason = str(getattr(response, "reason", "") or "")
+    final_url = response.geturl()
+    headers = response.headers
+
+    content_length = _parse_optional_int(headers.get("Content-Length"))
+    if content_length is not None and content_length > max_bytes:
+        return AntiBlockingHttpCaptureFailure(
+            requested_url=requested_url,
+            final_url=final_url,
+            status=status,
+            reason=reason,
+            failure_kind=AntiBlockingHttpCaptureFailureKind.SIZE_CAP_EXCEEDED,
+            message=(
+                "anti_blocking_http response exceeded max-bytes cap before body read: "
+                f"{content_length} bytes > {max_bytes} bytes"
+            ),
+            impersonation_profile=impersonation_profile,
+        )
+
+    try:
+        body = _read_with_cap(response, max_bytes=max_bytes)
+    except _BodyTooLargeError as exc:
+        return AntiBlockingHttpCaptureFailure(
+            requested_url=requested_url,
+            final_url=final_url,
+            status=status,
+            reason=reason,
+            failure_kind=AntiBlockingHttpCaptureFailureKind.SIZE_CAP_EXCEEDED,
+            message=str(exc),
+            impersonation_profile=impersonation_profile,
+        )
+
+    if not body:
+        return AntiBlockingHttpCaptureFailure(
+            requested_url=requested_url,
+            final_url=final_url,
+            status=status,
+            reason=reason,
+            failure_kind=AntiBlockingHttpCaptureFailureKind.NO_BODY,
+            message=f"anti_blocking_http response returned HTTP {status} {reason or 'without reason'} with an empty body",
+            impersonation_profile=impersonation_profile,
+        )
+
+    warning_notes: list[str] = []
+    if final_url != requested_url:
+        warning_notes.append(
+            f"anti_blocking_http followed redirect from {requested_url} to {final_url}"
+        )
+
+    response_headers = {str(key): str(value) for key, value in headers.items()}
+    metadata: dict[str, object] = {
+        "requested_url": requested_url,
+        "final_url": final_url,
+        "status": status,
+        "reason": reason or None,
+        "method_category": ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
+        "impersonation_profile": impersonation_profile,
+        "content_type": headers.get("Content-Type"),
+        "content_length": content_length,
+        "content_encoding": headers.get("Content-Encoding"),
+        "date": headers.get("Date"),
+        "last_modified": headers.get("Last-Modified"),
+        "etag": headers.get("ETag"),
+        "response_headers": response_headers,
+        "capture_timestamp": utc_now_z(),
+        "timeout_seconds": timeout_seconds,
+        "byte_count": len(body),
+    }
+
+    return AntiBlockingHttpCaptureSuccess(
+        requested_url=requested_url,
+        final_url=final_url,
+        status=status,
+        reason=reason,
+        impersonation_profile=impersonation_profile,
+        method_category=ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
+        response_headers=response_headers,
+        metadata=metadata,
+        body=body,
+        warning_notes=warning_notes,
+        limitation_notes=[],
+    )
+
+
+def _validate_http_url(url: str) -> str:
+    parsed = urlparse(url)
+    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
+        raise ValueError("anti_blocking_http capture requires an absolute http:// or https:// URL")
+    return parsed.geturl()
+
+
+def _parse_optional_int(value: str | None) -> int | None:
+    if value is None:
+        return None
+    try:
+        return int(value)
+    except ValueError:
+        return None
+
+
+def _read_with_cap(response: HTTPResponse | HTTPError, *, max_bytes: int) -> bytes:
+    chunks: list[bytes] = []
+    total = 0
+    while True:
+        chunk = response.read(min(65536, max_bytes - total + 1))
+        if not chunk:
+            return b"".join(chunks)
+        total += len(chunk)
+        if total > max_bytes:
+            raise _BodyTooLargeError(
+                "anti_blocking_http response exceeded max-bytes cap during body read: "
+                f"{total} bytes > {max_bytes} bytes"
+            )
+        chunks.append(chunk)
+
+
+def _failure_kind_from_url_error(error: URLError) -> AntiBlockingHttpCaptureFailureKind:
+    reason_text = str(error.reason).lower()
+    if "timed out" in reason_text or "timeout" in reason_text:
+        return AntiBlockingHttpCaptureFailureKind.TIMEOUT
+    return AntiBlockingHttpCaptureFailureKind.NETWORK_ERROR
+
+
+class _BodyTooLargeError(ValueError):
+    pass
diff --git a/orca-harness/source_capture/block_shell.py b/orca-harness/source_capture/block_shell.py
new file mode 100644
index 0000000..edbac4f
--- /dev/null
+++ b/orca-harness/source_capture/block_shell.py
@@ -0,0 +1,127 @@
+from __future__ import annotations
+
+from dataclasses import dataclass
+from enum import StrEnum
+from typing import Mapping
+
+
+class CaptureBodyClass(StrEnum):
+    """Honest classification of a preserved capture body.
+
+    There is deliberately NO positive ``CONTENT`` member: this guard can detect
+    block/challenge shells and emptiness, but it cannot certify that an arbitrary
+    body IS the real source. The most a body earns is ``CONTENT_UNVERIFIED``.
+    """
+
+    BLOCK_SHELL = "block_shell"
+    EMPTY = "empty"
+    CONTENT_UNVERIFIED = "content_unverified"
+
+
+@dataclass(frozen=True)
+class CaptureBodyClassification:
+    classification: CaptureBodyClass
+    signal: str | None
+    detail: str
+
+
+# High-confidence interstitial / bot-wall body signatures, matched as lowercased
+# substrings against the decoded body prefix. Kept conservative: only well-known
+# challenge/block markers appear here. Anything else stays CONTENT_UNVERIFIED
+# rather than being claimed as real source content. Over-flagging real content as
+# a block_shell is the safe error direction (it under-claims, body is still
+# preserved); under-flagging a shell as content is the dangerous fake-pass.
+_BODY_BLOCK_SIGNATURES: tuple[tuple[str, str], ...] = (
+    ("just a moment", "cloudflare_interstitial"),
+    ("checking your browser", "cloudflare_interstitial"),
+    ("cdn-cgi/challenge-platform", "cloudflare_challenge"),
+    ("challenge-platform", "cloudflare_challenge"),
+    ("attention required", "cloudflare_block"),
+    ("access denied", "generic_access_denied"),
+    ("you have been blocked", "generic_block"),
+    ("verify you are human", "captcha_human_check"),
+    ("are you a robot", "captcha_human_check"),
+    ("recaptcha", "recaptcha"),
+    ("g-recaptcha", "recaptcha"),
+    ("hcaptcha", "hcaptcha"),
+    ("px-captcha", "perimeterx"),
+    ("perimeterx", "perimeterx"),
+    ("datadome", "datadome"),
+    ("incapsula", "incapsula"),
+    ("_incapsula_resource", "incapsula"),
+    ("unusual traffic", "google_unusual_traffic"),
+)
+
+# High-confidence block signals carried on response headers.
+_HEADER_BLOCK_SIGNATURES: tuple[tuple[str, str], ...] = (
+    ("cf-mitigated", "cloudflare_mitigated"),
+    ("x-datadome", "datadome_header"),
+    ("x-datadome-cid", "datadome_header"),
+)
+
+_BODY_SCAN_BYTES = 8192
+
+
+def classify_capture_body(
+    *,
+    status: int,
+    headers: Mapping[str, str] | None,
+    body: bytes,
+) -> CaptureBodyClassification:
+    """Classify a preserved capture body as block-shell, empty, or unverified content.
+
+    This is a conservative anti-fake-pass guard, not a content validator. It NEVER
+    asserts that a body IS the real source. The best result is
+    ``CONTENT_UNVERIFIED`` -- "no known block/challenge signature was detected and
+    a non-empty body was preserved; the body is not independently certified as the
+    source." Only high-confidence interstitial / bot-wall signatures yield
+    ``BLOCK_SHELL``.
+
+    ``status`` is accepted for caller symmetry but is intentionally NOT used to
+    decide the body class: HTTP-status posture (e.g. a 403 access_failed) is owned
+    by the runner and combined with this body classification separately.
+    """
+    _ = status  # status posture is owned by the runner, not this body guard
+
+    if not body or not body.strip():
+        return CaptureBodyClassification(
+            classification=CaptureBodyClass.EMPTY,
+            signal=None,
+            detail="preserved body is empty or whitespace-only",
+        )
+
+    if headers:
+        lowered_header_keys = {str(key).lower() for key in headers.keys()}
+        for header_key, signal in _HEADER_BLOCK_SIGNATURES:
+            if header_key in lowered_header_keys:
+                return CaptureBodyClassification(
+                    classification=CaptureBodyClass.BLOCK_SHELL,
+                    signal=signal,
+                    detail=f"response header '{header_key}' indicates a bot-mitigation / challenge response",
+                )
+
+    scanned = min(len(body), _BODY_SCAN_BYTES)
+    text_prefix = body[:_BODY_SCAN_BYTES].decode("utf-8", errors="ignore").lower()
+    for needle, signal in _BODY_BLOCK_SIGNATURES:
+        if needle in text_prefix:
+            return CaptureBodyClassification(
+                classification=CaptureBodyClass.BLOCK_SHELL,
+                signal=signal,
+                detail=f"body matched block/challenge signature '{needle}' ({signal})",
+            )
+
+    return CaptureBodyClassification(
+        classification=CaptureBodyClass.CONTENT_UNVERIFIED,
+        signal=None,
+        detail=(
+            f"no known block/challenge signature detected in first {scanned} bytes; "
+            "body preserved but not certified as source content"
+        ),
+    )
+
+
+__all__ = [
+    "CaptureBodyClass",
+    "CaptureBodyClassification",
+    "classify_capture_body",
+]
diff --git a/orca-harness/tests/unit/test_anti_blocking_http_adapter.py b/orca-harness/tests/unit/test_anti_blocking_http_adapter.py
new file mode 100644
index 0000000..501513c
--- /dev/null
+++ b/orca-harness/tests/unit/test_anti_blocking_http_adapter.py
@@ -0,0 +1,98 @@
+import pytest
+
+from source_capture.adapters.anti_blocking_http import (
+    ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
+    DEFAULT_IMPERSONATION_PROFILE,
+    AntiBlockingHttpCaptureFailure,
+    AntiBlockingHttpCaptureFailureKind,
+    AntiBlockingHttpCaptureSuccess,
+    _capture_response,
+    _validate_http_url,
+    header_complete_profile,
+)
+
+
+class _FakeResponse:
+    """Minimal duck-typed stand-in for an http.client response / HTTPError."""
+
+    def __init__(self, *, status, body, headers=None, url="https://example.test/"):
+        self._status = status
+        self._buf = body
+        self._off = 0
+        self.headers = dict(headers or {})
+        self._url = url
+        self.reason = "OK" if status == 200 else "Forbidden"
+
+    def getcode(self):
+        return self._status
+
+    def geturl(self):
+        return self._url
+
+    def read(self, size):
+        chunk = self._buf[self._off : self._off + size]
+        self._off += len(chunk)
+        return chunk
+
+
+def test_header_profile_is_browser_complete():
+    headers = header_complete_profile()
+    assert "Chrome/" in headers["User-Agent"]
+    # Accept-Encoding identity keeps preserved bytes == served bytes (hash-honest).
+    assert headers["Accept-Encoding"] == "identity"
+    assert headers["Accept-Language"].startswith("en-US")
+    assert "Sec-Fetch-Mode" in headers
+    assert headers["Sec-CH-UA-Mobile"] == "?0"
+
+
+def test_validate_http_url_rejects_non_http():
+    with pytest.raises(ValueError):
+        _validate_http_url("ftp://example.test/x")
+    with pytest.raises(ValueError):
+        _validate_http_url("not-a-url")
+
+
+def test_capture_response_success_records_provenance():
+    resp = _FakeResponse(status=200, body=b"<html>hello</html>", headers={"Content-Type": "text/html"})
+    result = _capture_response(
+        requested_url="https://example.test/",
+        response=resp,
+        timeout_seconds=10.0,
+        max_bytes=1_000_000,
+        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
+    )
+    assert isinstance(result, AntiBlockingHttpCaptureSuccess)
+    assert result.method_category == ANTI_BLOCKING_HTTP_METHOD_CATEGORY
+    assert result.impersonation_profile == DEFAULT_IMPERSONATION_PROFILE
+    assert result.body == b"<html>hello</html>"
+    assert result.metadata["method_category"] == ANTI_BLOCKING_HTTP_METHOD_CATEGORY
+    assert result.status == 200
+    assert result.response_headers.get("Content-Type") == "text/html"
+
+
+def test_capture_response_empty_body_is_no_body_failure():
+    resp = _FakeResponse(status=200, body=b"")
+    result = _capture_response(
+        requested_url="https://example.test/",
+        response=resp,
+        timeout_seconds=10.0,
+        max_bytes=1_000_000,
+        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
+    )
+    assert isinstance(result, AntiBlockingHttpCaptureFailure)
+    assert result.failure_kind is AntiBlockingHttpCaptureFailureKind.NO_BODY
+
+
+def test_capture_response_size_cap_via_content_length():
+    resp = _FakeResponse(
+        status=200, body=b"x" * 100, headers={"Content-Length": "10000000"}
+    )
+    result = _capture_response(
+        requested_url="https://example.test/",
+        response=resp,
+        timeout_seconds=10.0,
+        max_bytes=1000,
+        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
+    )
+    assert isinstance(result, AntiBlockingHttpCaptureFailure)
+    assert result.failure_kind is AntiBlockingHttpCaptureFailureKind.SIZE_CAP_EXCEEDED
diff --git a/orca-harness/tests/unit/test_block_shell.py b/orca-harness/tests/unit/test_block_shell.py
new file mode 100644
index 0000000..eb8561a
--- /dev/null
+++ b/orca-harness/tests/unit/test_block_shell.py
@@ -0,0 +1,63 @@
+from source_capture.block_shell import CaptureBodyClass, classify_capture_body
+
+
+def test_empty_body_is_empty():
+    result = classify_capture_body(status=200, headers={}, body=b"")
+    assert result.classification is CaptureBodyClass.EMPTY
+
+
+def test_whitespace_only_body_is_empty():
+    result = classify_capture_body(status=200, headers={}, body=b"   \n\t  ")
+    assert result.classification is CaptureBodyClass.EMPTY
+
+
+def test_cloudflare_interstitial_body_is_block_shell():
+    body = (
+        b"<html><head><title>Just a moment...</title></head>"
+        b"<body>Checking your browser before accessing the site.</body></html>"
+    )
+    result = classify_capture_body(status=200, headers={"Server": "cloudflare"}, body=body)
+    assert result.classification is CaptureBodyClass.BLOCK_SHELL
+    assert result.signal is not None
+
+
+def test_cf_mitigated_header_is_block_shell():
+    result = classify_capture_body(
+        status=403, headers={"cf-mitigated": "challenge"}, body=b"<html>anything</html>"
+    )
+    assert result.classification is CaptureBodyClass.BLOCK_SHELL
+    assert result.signal == "cloudflare_mitigated"
+
+
+def test_datadome_header_is_block_shell_case_insensitive():
+    result = classify_capture_body(
+        status=403, headers={"X-DataDome": "protected"}, body=b"<html>x</html>"
+    )
+    assert result.classification is CaptureBodyClass.BLOCK_SHELL
+    assert result.signal == "datadome_header"
+
+
+def test_captcha_body_is_block_shell():
+    body = b"<html><body>Please verify you are human by completing the hCaptcha challenge.</body></html>"
+    result = classify_capture_body(status=200, headers={}, body=body)
+    assert result.classification is CaptureBodyClass.BLOCK_SHELL
+
+
+def test_ordinary_html_is_content_unverified():
+    body = (
+        b"<html><head><title>Q3 Earnings</title></head>"
+        b"<body><article>Revenue rose 4 percent year over year.</article></body></html>"
+    )
+    result = classify_capture_body(status=200, headers={"Content-Type": "text/html"}, body=body)
+    assert result.classification is CaptureBodyClass.CONTENT_UNVERIFIED
+    assert result.signal is None
+
+
+def test_no_positive_content_class_exists():
+    # Honesty invariant: the guard never asserts a body IS the real source.
+    assert not hasattr(CaptureBodyClass, "CONTENT")
+    assert set(CaptureBodyClass) == {
+        CaptureBodyClass.BLOCK_SHELL,
+        CaptureBodyClass.EMPTY,
+        CaptureBodyClass.CONTENT_UNVERIFIED,
+    }
```
