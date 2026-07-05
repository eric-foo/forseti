# Parfumo Cleaning Blocked-Capture Ack — Delegated Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated code review-and-patch, delegated_code_review_and_patch sibling mode)
scope: >
  Delegated cross-vendor code review of the parfumo empty-handles blocked-capture
  ack fix on branch claude/parfumo-empty-handles-fix (commit 199e7a03) --
  run_parfumo_cleaning_catchup.py's new ValidationError-handling branch plus its
  two regression tests.
commission: >
  Paste-ready-chat commission authored inline in the implementing thread (this
  lane); not separately filed as a docs/prompts/reviews/ artifact -- the
  commission text, focus areas, and bounded scope are reproduced verbatim below.
reviewed_by: OpenAI GPT-5 Codex (exact build unrecorded beyond operator's label)
authored_by: Claude Sonnet 5 (Anthropic)
de_correlation_bar: cross_vendor_discovery
review_lane: delegated_code_review_and_patch (workflow-code-review method), access=self-contained (embedded diff + context; reviewer's own repo access unconfirmed)
target_branch: claude/parfumo-empty-handles-fix
reviewed_diff_base: 0e475892f821e8aea711e8cdc3a7163838abcb60 (origin/main at fork)
patched_in_this_pass: true (patch proposed by the delegate, applied and adjudicated by the home model in this pass)
escalation: none (patch-level finding, not NEEDS_ARCHITECTURE_PASS)
authority_boundary: retrieval_only
```

## Actor / Model-Family Receipt

- `author_home_model_family`: Anthropic (Claude Sonnet 5) -- authored the original diff and adjudicates this review.
- `current_receiving_actor_role`: controller
- `controller_model_family`: OpenAI (GPT-5 Codex, per operator label)
- `dispatch_mode`: external-controller-courier -- the operator pasted the commission into the controller model and couriered the reply back.
- `de_correlation_status`: **satisfied** -- controller vendor (OpenAI) differs from author vendor (Anthropic). `de_correlation_bar = cross_vendor_discovery`.

## Commission (reproduced)

Target, bounded patch scope (cannot silently widen):

- `[parfumo-blocked-capture-fix]` `orca-harness/runners/run_parfumo_cleaning_catchup.py` -- bounded to the new `ValidationError`-handling branch, `_is_zero_handles_validation_error`, `_blocked_capture_evidence_or_none`, the new constant/imports, and the module-docstring paragraph. Not `_packet_obligation`, `_ack_packet`, `pending_packets`, the surface-gate branch, or `main()`/CLI.
- `[parfumo-blocked-capture-fix]` `orca-harness/tests/unit/test_parfumo_cleaning_catchup.py` -- bounded to the two new tests and the `_commit_family_packet` `access_posture` passthrough / fixture constants.

Why read-only review was insufficient: the change alters a fail-loud validation lane's exception handling on a shared cleaning contract boundary (`CleaningPacket.handles` `min_length=1`, shared with fragrantica/basenotes); a narrowing mistake could silently convert a future real extraction bug into an honest-looking ack -- the fake-success risk named by `docs/prompts/handoffs/parfumo_cleaning_empty_handles_packet_fix_handoff_v0.md`.

Focus areas commissioned: (1) precision of the `ValidationError` match; (2) whether the `access_posture` prefix check is correctly scoped to only the direct-HTTP producer, not accidentally matchable by the targeted-rendered surface or another lane's packets; (3) whether the re-read-failure path falls through to `derive_failed` with the original exception, never masking it; (4) whether the two new tests exercise the real code path and would catch a regression if the match were loosened.

## Source Context

`SOURCE_CONTEXT_READY` -- the commission embedded the full unified diff plus the relevant adjacent facts (the shared `CleaningPacket.handles` contract, the `run_source_capture_http_packet.py` producer convention, the targeted-rendered surface's separate code path) inline, since the controller's own repo access was not confirmed.

## Method

Per the Source-Gated Method Contract: the controller REFERENCE-LOADED `workflow-deep-thinking` and `workflow-code-review`, declared `SOURCE_CONTEXT_READY` against the embedded diff and context, then applied the review method.

---

## Finding

### F1 — The blocked-capture ack helper checked `access_posture` without also requiring direct-HTTP surface identity — **MAJOR**

- **Location:** `orca-harness/runners/run_parfumo_cleaning_catchup.py`, `_blocked_capture_evidence_or_none` (originally lines ~134-162, pre-patch).
- **Implementation evidence:** The original helper re-read the packet's `access_posture` and returned blocked-capture ack evidence whenever the value started with `"direct_http access_failed with HTTP "`, without checking that the *surface* (the `surface` parameter, or the freshly re-read `packet.source_surface`) was actually the direct-HTTP surface. `access_posture` is an intentionally open free-text `VisibleFact` field (Ob.11, `source_capture/models.py`); nothing in the schema prevents a differently-surfaced packet from carrying a similarly-worded value. `_PARFUMO_SURFACES` includes both `PARFUMO_DIRECT_HTTP_SOURCE_SURFACE` and `PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE`, and the caller passes whichever surface the packet actually has -- so a targeted-rendered packet whose access_posture happened to carry the same prefix (e.g. mis-tagged fixture data, a future producer change, or a malformed capture) would have been silently acked as "no cleanable content" instead of raising `derive_failed`, exactly the fake-success risk the commission was scoped to catch.
- **Authority/evidence basis:** The commission's own focus area 2 named this exact risk before review; the finding confirms it was not yet closed in the first-pass diff.
- **Impact:** Bounded to the parfumo direct-HTTP vs targeted-rendered fork; would not have affected fragrantica/basenotes (those are gated out earlier in `run_catchup` as known-out-of-scope surfaces, before this branch is ever reached).
- **`minimum_closure_condition`:** The ack path must require direct-HTTP surface identity (both the caller-supplied surface and the freshly re-read manifest's own `source_surface`), and a targeted-rendered zero-handle packet carrying the same access_posture prefix must still fail loud (`derive_failed`), never ack.
- **`next_authorized_action`:** Patch in the working tree and adjudicate; home model to verify with a regression test.
- **Patched in this pass:** Yes.

## Proposed patch (as delegated)

```diff
# [parfumo-blocked-capture-fix]
diff --git a/orca-harness/runners/run_parfumo_cleaning_catchup.py b/orca-harness/runners/run_parfumo_cleaning_catchup.py
@@
-failure whose packet manifest records a source-side access failure (e.g. a
-Cloudflare/anti-bot HTTP block) is an honest non-cleanable outcome, not a parser
-bug, and is acknowledged with explicit ``no_cleanable_content_for_blocked_capture``
-evidence naming the recorded access posture; any other zero-``handles`` shape still
-raises ``derive_failed`` unchanged. An ack write failure surfaces as ``ack_failed``.
+failure whose direct-HTTP packet manifest records a source-side access failure
+(e.g. a Cloudflare/anti-bot HTTP block) is an honest non-cleanable outcome, not a
+parser bug, and is acknowledged with explicit
+``no_cleanable_content_for_blocked_capture`` evidence naming the recorded access
+posture; any other zero-``handles`` shape still raises ``derive_failed`` unchanged.
+An ack write failure surfaces as ``ack_failed``.
@@
-    evidence when access_posture confirms a recorded source-side access failure
-    for this surface, else None. Any re-read failure returns None (never acks on
-    an uncertain classification)."""
+    evidence when a direct-HTTP packet's access_posture confirms a recorded
+    source-side access failure, else None. Any re-read failure returns None
+    (never acks on an uncertain classification)."""
+    if surface != PARFUMO_DIRECT_HTTP_SOURCE_SURFACE:
+        return None
@@
     except Exception:  # noqa: BLE001 - classification-only re-read; never surfaced as the cause
         return None
+    if packet.source_surface != PARFUMO_DIRECT_HTTP_SOURCE_SURFACE:
+        return None
     access_posture = packet.access_posture
```

```diff
# [parfumo-blocked-capture-fix]
diff --git a/orca-harness/tests/unit/test_parfumo_cleaning_catchup.py b/orca-harness/tests/unit/test_parfumo_cleaning_catchup.py
@@
-def test_blocked_capture_zero_handles_acked_no_cleanable_content(tmp_path) -> None:
+def test_blocked_capture_zero_handles_acks_only_direct_http_surface(tmp_path) -> None:
@@
     assert list((data_root.path / "derived").glob(f"*/{pid}/*")) == []
     assert pending_packets(data_root=data_root) == []
+
+    targeted_root = DataLakeRoot.for_test(tmp_path / "targeted_lake")
+    targeted = _commit_family_packet(
+        targeted_root,
+        tmp_path,
+        name="targetedblocked",
+        source_surface=PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
+        body_text=_BLOCKED_CAPTURE_BODY,
+        access_posture=_BLOCKED_CAPTURE_ACCESS_POSTURE,
+    )
+
+    targeted_results = run_catchup(data_root=targeted_root)
+    assert [r["status"] for r in targeted_results] == ["derive_failed"]
+    assert "too_short" in targeted_results[0]["error"]
+    assert find_acks(
+        targeted_root,
+        raw_anchor=targeted,
+        ack_namespace=PARFUMO_CLEANING_AUDIT_LANE,
+    ) == []
```

## Delegate's verdict and residual-risk note (as returned)

**Verdict:** accept only with this patch. The original diff was directionally correct, but the unpatched surface gap was exactly the kind of fake-success widening this commission was meant to catch. No architecture pass needed.

**Validation observed (by the delegate):** `python -m pytest -p no:cacheprovider --no-header --no-summary orca-harness\tests\unit\test_parfumo_cleaning_catchup.py -q` -> `............... [100%]`; `git diff --check` on the two target files -> exit 0, no output.

**Residual risk (as returned):** the delegate did not run the full repo test suite or a live packet replay; the pre-patch red state was inferred from the loaded helper logic rather than executed red-then-green.

## Home-model adjudication (claims, not premises)

- **F1 finding: accepted as real.** Independently re-derived: `access_posture` is genuinely open free text with no surface-identity coupling in the schema, and the pre-patch helper had no surface guard beyond the string-prefix match. The risk is real, not hypothetical.
- **Proposed patch: accepted verbatim**, no modification. It is the smallest complete fix -- adds exactly two early-return surface checks (caller-supplied `surface` and the freshly re-read manifest's `source_surface`, both independently, as defense-in-depth against an availability-index/manifest mismatch) and one cross-surface regression assertion. No scope widening beyond the commissioned two files.
- **Delegate's validation claim: independently re-verified, not merely trusted.** Ran `pytest orca-harness/tests/unit/test_parfumo_cleaning_catchup.py -v` after the patch: **15 passed** (all pre-existing tests plus the renamed/expanded cross-surface test and the second new test). Additionally ran the broader parfumo test surface (`test_parfumo_cleaning_catchup.py`, `test_parfumo_cleaning_projection_integration.py`, `test_parfumo_non_silver_record_roles.py`, `test_parfumo_mgt_capture_runner.py`, `test_parfumo_projection.py`): **37 passed**. Ran `git diff --check` on both target files: exit 0, no output.
- **Delegate's residual-risk disclosure: accepted as accurate and still open.** No live-lake replay against the real triggering packet (`01KWCG89CBFH90Z4ABKYWKF5VE`) has been performed in this pass -- that remains a separately owner-granted follow-up per the originating handoff packet's drift guard, not something this review or patch could close.
- **No other findings surfaced by the delegate; none independently found by the home model** beyond F1 in the bounded scope.

## Review-use boundary

These findings, the proposed patch, and the delegate's verdict are decision input only. They are not approval, validation, mandatory remediation, or executor-ready patch authority on their own -- the home model's adjudication above is what actually accepts the patch into the branch; the diff and verdict were claims to adjudicate, not premises to inherit.

## Validation evidence (home-model, post-adjudication)

- `python -m pytest orca-harness/tests/unit/test_parfumo_cleaning_catchup.py -v` -> **15 passed**.
- `python -m pytest orca-harness/tests/unit/test_parfumo_cleaning_catchup.py orca-harness/tests/unit/test_parfumo_cleaning_projection_integration.py orca-harness/tests/unit/test_parfumo_non_silver_record_roles.py orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py orca-harness/tests/unit/test_parfumo_projection.py -q` -> **37 passed**.
- `git diff --check -- orca-harness/runners/run_parfumo_cleaning_catchup.py orca-harness/tests/unit/test_parfumo_cleaning_catchup.py` -> exit 0, no output.
- Not run in this pass: a live-lake re-run against `F:\orca-data-lake` confirming packet `01KWCG89CBFH90Z4ABKYWKF5VE` acks and the seam cadence's post-sweep parfumo pending count reaches 0 -- deferred, requires a fresh owner-granted live-lake read/run per the originating handoff packet's drift guard.

## Not-proven boundaries

This review and its adjudication assert no formal `PASS`, readiness, or merge authorization. They confirm the patched code is internally consistent and covered by regression tests reachable from this repo's own test runner; they do not confirm behavior against the live data lake.
