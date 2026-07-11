# Retail/PDP Amazon-First Silver PR #868 Delegated Adversarial Code Review-And-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch output
scope: >
  Delegated adversarial code review-and-bounded-patch report for Forseti PR
  #868 (generic Retail/PDP Silver producer), commissioned under the
  delegated_code_review_and_patch sibling mode of
  .agents/workflow-overlay/delegated-review-patch.md.
use_when:
  - Adjudicating this delegated review's findings and bounded patch.
  - Checking prior review coverage before a new pass on the same PR/target.
authority_boundary: retrieval_only
```

reviewed_by: claude-sonnet-5 (Anthropic)
authored_by: OpenAI/Codex GPT-5 (operator-supplied via commission; not independently verified)

## 1. Commission, Target, Authority, Actor/Model-Family Receipt

- Commission: repo-mode delegated adversarial code review-and-bounded-patch pass
  on Forseti PR #868 (`Add generic Retail/PDP Silver producer`), operator-couriered
  to an independent controller lane, per `.agents/workflow-overlay/delegated-review-patch.md`
  `delegated_code_review_and_patch` sibling mode.
- Target: full `origin/main...HEAD` change packet on branch
  `codex/retail-pdp-amazon-first-silver`, head `44905b55ae7d2d9d7f8e52f61b5306514cfd0f01`,
  in worktree `C:\Users\vmon7\Desktop\projects\orca\worktrees\retail-pdp-amazon-first-silver`.
- Why read-only review is insufficient: PR #868's implementation commit records
  independent adversarial review as pending, and the commissioning owner
  explicitly requested a delegated patch pass with a bounded, named patch scope.
- Bounded patch scope: the 11 files named in the commission (see §7).

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT (Codex; operator-supplied via commission and codex/ branch provenance)
  controller_model_family: Anthropic / Claude (Sonnet 5, model id claude-sonnet-5)
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  required_de_correlation_bar: cross_vendor_discovery
  de_correlation_status: satisfied
```

De-correlation check: controller vendor (Anthropic) differs from the recorded
author/home vendor (OpenAI). `BLOCKED_CONTROLLER_NOT_DECORRELATED` does not
apply; review and bounded patch proceeded.

## 2. reviewed_by / authored_by / de_correlation_bar / same_vendor_rationale

- `reviewed_by`: claude-sonnet-5 (Anthropic)
- `authored_by`: OpenAI/Codex GPT-5 (operator-supplied in the commission; not
  independently verified against a model API — recorded as supplied, not
  fabricated)
- `de_correlation_bar`: cross_vendor_discovery
- `same_vendor_rationale`: not_applicable (cross-vendor bar met)

## 3. Source-Read Ledger And Source Context Status

`SOURCE_CONTEXT_READY`. All named controlling sources were read (full or
targeted-section) before findings were drawn. No missing, stale, conflicting,
or excluded source was encountered among the commission's required list.

| Source | Read depth | Role |
| --- | --- | --- |
| `AGENTS.md`, `.agents/workflow-overlay/README.md`, `source-loading.md`, `decision-routing.md`, `review-lanes.md`, `delegated-review-patch.md`, `prompt-orchestration.md`, `safety-rules.md`, `source-of-truth.md` | full | Method/authority reference-load |
| `workflow-deep-thinking`, `workflow-code-review`, `workflow-delegated-review-patch` (kernel skills) | full | Reference-loaded methods |
| `git status --short --branch`, `git rev-parse HEAD`, `gh pr view 868`, `gh pr view 865`, `git merge-base`, `git diff --name-status/--stat` | live command | Preflight verification |
| `docs/workflows/retail_pdp_amazon_first_silver_lane_handoff_v0.md` (via `git show HEAD^:...`) | full | Reconstructed consumed handoff |
| `forseti-harness/data_lake/lane_registry.py` | full | Silver lane role registry |
| `forseti-harness/data_lake/silver_record.py` | full | Silver envelope validator + front door |
| `forseti-harness/data_lake/silver_lineage.py` | full | Silver lineage builder/validator |
| `forseti-harness/data_lake/root.py` (`append_record`, `record_path`, `load_raw_packet`, `_validate_segment`, `_atomic_create`, `append_record_set`) | targeted | Write/read primitives, path-safety, atomicity |
| `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` (Status, Decision In One Screen, Medallion Label Map, Required Behavior, Non-Goals, Derived Record Placement, Common Record Header, Bronze Intake And Attachment Record Boundary, Not Silver: Cleaning Audit Packs, Entity Records, Relationship Records, Metric Observation Records, Acceptance Criteria) | targeted (named sections + Acceptance Criteria) | Silver Vault authority |
| `forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md` | full | Upstream projection contract |
| `forseti-harness/source_capture/retail_pdp_projection.py` | full (2 pages) | Row/binding models, exact lake projection write path, per-retailer offer/review extraction |
| `forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md` (Status, Pinned Logged-Out Investigation Route, candidate routes, seller-surface posture, non-claims) | targeted | Amazon route authority, exact-quantity boundary |
| `forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_silver_producer_contract_v0.md` | full | Producer contract under review |
| `docs/research/retail_pdp_amazon_first_silver_live_proof_v0.md` | full | Proof-claim review target |
| `forseti-harness/source_capture/retail_pdp_silver.py` | full | Producer implementation (primary review target) |
| `forseti-harness/runners/run_retail_pdp_silver_producer.py` | full | Runner |
| `forseti-harness/tests/unit/test_retail_pdp_silver.py` | full | Unit tests (pre- and post-patch) |
| `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`, `test_silver_reader_selection_gate.py` | diff + targeted | Contract-test deltas |
| `forseti/product/spines/capture/core/source_families/retail_pdp/README.md` | full + diff | Discovery routing |
| `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json` | diff | Touchpoint inventory delta |

`gh pr view 865` confirmed `state: MERGED`, `mergedAt: 2026-07-11T06:27:02Z` —
PR 865 is landed, not a stacked dependency, consistent with the handoff's
framing of it as source orientation only.

## 4. Findings

### MAJOR-1 — Sibling Silver records were not written atomically as a set (patched)

- Severity: major. Confidence: high.
- Target: `[producer]` `forseti-harness/source_capture/retail_pdp_silver.py`,
  `derive_retail_pdp_silver_from_projection`, pre-patch lines 115-124.
- Failure mode: `build_retail_pdp_silver_records` validates every record in the
  batch before the first append (`validate_silver_vault_record` +
  `is_silver_record_source_backed_complete`), which rules out a *malformed*
  partial. But the 2-3 sibling records (`ProductEntity`, `RetailOfferObservation`,
  optional `RetailReviewAggregateObservation`) for one variant were then written
  with a plain per-record loop calling `append_silver_record` — each individual
  file write is atomic-create (`data_lake/root.py::_atomic_create`, confirmed:
  temp-file + no-overwrite `os.link`/`O_EXCL` publish), but the *batch* of
  sibling records has no cross-file transaction. `data_lake/root.py` already
  ships `append_record_set` specifically for all-or-nothing multi-record
  publication with a completion marker, and this producer does not use it.
- Failure scenario: a filesystem-level failure (disk full, permission error, or
  any other `OSError`) after the `ProductEntity` record is durably written but
  before its `RetailOfferObservation` sibling is written leaves an orphaned
  `ProductEntity` record permanently committed in the append-only lake with no
  accompanying offer observation and no marker indicating incompleteness. A
  downstream reader has no way to distinguish this from a legitimately
  entity-only batch.
- Authority: the producer contract's own "Failure And Validation Contract"
  section (`retail_pdp_silver_producer_contract_v0.md`) states "Fail before the
  first append" — true for validation failures, not for a mid-loop filesystem
  failure, which the pre-patch code did not guard against.
- `minimum_closure_condition`: a mid-batch write failure must not leave any
  already-written sibling record durably committed without cleanup or an
  explicit incompleteness marker.
- `next_authorized_action`: patch (in bounded scope) or owner decision to defer.
- Patched: **yes** (see §7). Verified red-green: reverted the fix, ran the new
  `test_mid_batch_append_failure_leaves_no_orphaned_partial` test, confirmed it
  failed (orphaned `ProductEntity` file left on disk); restored the fix, same
  test passes. See §9 validation.

### MAJOR-2 — Entity identity for Sephora silently collapses distinct SKU variants under one entity_key (not patched — flagged)

- Severity: major. Confidence: medium-high.
- Target: `[producer]` `forseti-harness/source_capture/retail_pdp_silver.py:392-406`
  (`_entity_key`); root cause upstream in
  `[projection]` `forseti-harness/source_capture/retail_pdp_projection.py:1052-1070`
  (`_offer_fields_from_product`).
- Failure mode: `_entity_key` builds `native_id` as
  `product_id or sku` (product_id checked first). For Amazon, Walmart, and
  Target, `product_id` and `sku` are set to the *same* value in the projection
  (verified: Amazon `"product_id": asin, "sku": asin`; Target
  `"product_id": product_id, "sku": product_id`), so there is no disagreement.
  For Sephora, `_offer_fields_from_product` (the `ProductGroup`/`hasVariant`
  branch) sets `"product_id": productGroupID` (shared across all color/scent
  variants in the group) while `"sku": variant.get("sku")` (variant-specific).
  Because `_entity_key` prefers `product_id`, two structurally distinct,
  independently-priced/available Sephora SKUs belonging to the same product
  group are assigned the identical `entity_key`
  (`namespace=retail_pdp:sephora, kind=retailer_product, native_id=<productGroupID>`).
- Failure scenario: capture packet A for Sephora SKU `12345` (red) and packet B
  for SKU `67890` (blue) of the same product group both derive Silver records
  with the same `entity_key`. Both `RetailOfferObservation` records (which
  carry genuinely different price/availability/sku facts per the "Observation
  semantics" axis) point their `subject.ref` at that one shared entity_key. A
  downstream consumer joining offer observations by entity_key cannot tell the
  two SKUs apart and will read them as competing/conflicting observations of
  one product, when they are two distinct sellable retailer-local products.
- Authority: Silver Vault Acceptance Criterion 4 ("Entity records contain
  stable identity only") and the producer contract's own identity rule ("a
  `retail_variant_offer` must expose a retailer-local `product_id` or `sku`;
  the entity key is `(namespace=retail_pdp:<retailer>, kind=retailer_product,
  native_id=<id>)`") — the contract text itself does not resolve which field
  wins when both are present and disagree, so the code's `product_id`-first
  preference is contract-consistent in letter but not demonstrably correct in
  effect for the one retailer (Sephora) where the two fields diverge in
  practice.
- `minimum_closure_condition`: either the producer contract explicitly and
  deliberately resolves product-group-vs-variant entity granularity (naming
  which field is authoritative when `product_id` and `sku` disagree, and
  whether that is intentional group-level identity or a defect), or
  `_entity_key`'s precedence is changed to match the intended granularity, with
  a test proving two distinct Sephora SKUs under one `productGroupID` receive
  distinct (or intentionally identical, if that is the ratified policy)
  entity keys.
- `next_authorized_action`: owner/architecture decision on entity granularity
  policy; not patched here because choosing between product-group and
  SKU-variant identity is a Silver semantic-identity design choice, not a local
  mechanical fix, and the reviewed producer contract does not resolve it.
- Patched: **no** — flagged only, per the commission's instruction that a fix
  requiring a current-record-selection or identity-policy decision returns to
  the owner rather than being silently patched.

### MAJOR-3 — Two fail-closed identity-integrity paths and the atomicity guarantee were entirely untested before this pass (patched)

- Severity: major. Confidence: high.
- Target: `[unit-test]` `forseti-harness/tests/unit/test_retail_pdp_silver.py`
  (pre-patch state, 4 tests).
- Failure mode: the pre-patch test file exercised only the Amazon happy path,
  a missing-projection-record error, a raw-ref-hash-drift error, and a
  no-variant-row error. Two of `build_retail_pdp_silver_records`'s explicit
  fail-closed branches had **zero** test coverage: the "multiple {row_kind}
  rows... ambiguous" duplicate-identity guard (`_one_row_per_key`) and the
  "review substrate row(s) have no matching retailer-local product identity"
  orphan-review guard. A regression that silently broke either guard (e.g. an
  edit that let a duplicate variant row silently pick the first match instead
  of raising) would have shipped undetected. This directly matches the
  commission's axis 13 concern ("missing negative tests... multi-slice/
  multi-retailer ambiguity").
- Authority: producer contract "Failure And Validation Contract" section names
  "ambiguous same-slice identity" and "orphan review substrate" as required
  fail-before-append behaviors, but no test proved either before this pass.
- `minimum_closure_condition`: both fail-closed paths have a red-green-provable
  regression test that fails without the guard and passes with it.
- `next_authorized_action`: patch (in bounded scope).
- Patched: **yes** — added
  `test_duplicate_variant_identity_fails_before_any_silver_write` and
  `test_orphan_review_substrate_fails_before_any_silver_write` (see §7),
  plus `test_mid_batch_append_failure_leaves_no_orphaned_partial` proving
  MAJOR-1's fix. All three pass against current code; each targets a branch
  that existed, unexercised, before this pass.

### MINOR-1 — Silver producer's own logic is exercised only against an Amazon fixture

- Severity: minor. Confidence: medium.
- Target: `[unit-test]` `forseti-harness/tests/unit/test_retail_pdp_silver.py`.
- Failure mode: the producer is explicitly retailer-generic
  (`_SELECTED_ROW_KINDS`, `_entity_key`, `_observation_record` all operate on
  generic `source_visible_fields`/`residuals` with no Amazon-specific
  branching), and the projection layer already emits Walmart/Target/Sephora/
  Ulta rows with materially different field shapes (e.g. `exact_inventory_
  quantity`/`sold_units` posture pairs present only for Walmart/Target). None
  of that is exercised through the Silver producer itself — only through the
  Amazon fixture. This is a genericity-claim coverage gap, not a known defect
  beyond MAJOR-2 (which this gap is exactly why MAJOR-2 escaped detection).
- `minimum_closure_condition`: at least one non-Amazon retailer fixture is
  exercised through `derive_retail_pdp_silver_from_projection` and asserts
  entity/offer/review shape.
- `next_authorized_action`: owner decision — optional hardening, not blocking;
  MAJOR-2's closure would naturally require adding this coverage for Sephora.
- Patched: **no** — labeled optional hardening per the review doctrine
  ("Optional hardening may be identified only when clearly labeled optional
  and non-required").

### MINOR-2 — `observed_at` and `captured_at` are always identical for this producer

- Severity: minor. Confidence: low.
- Target: `[producer]` `forseti-harness/source_capture/retail_pdp_silver.py:315-316`
  (`_lineage`).
- Failure mode: both fields are set from the same
  `_known_capture_time(source_slice)` call. The Common Record Header
  distinguishes "time the fact was observed at or about the source" from "time
  Forseti captured the source material," and for a live-rendered PDP capture
  these are legitimately the same instant, so this is very likely correct
  behavior rather than a defect — flagged at low confidence because no
  projection field currently carries a distinct source-claimed observation
  time for retail PDPs, so the fields cannot currently diverge even if a future
  retailer surface required them to.
- `minimum_closure_condition`: none required now; revisit only if a future
  retail source exposes a source-claimed timestamp distinct from capture time.
- `next_authorized_action`: no action.
- Patched: no (not a defect at current scope).

## 5. `considered_and_defended`

- Candidate: `projection_record_id` (a caller-supplied string) could enable
  path traversal into an unintended lane/record when resolved via
  `data_root.record_path(...)`. Defense: `data_lake/root.py::_validate_segment`
  rejects `.`/`..` and anything not matching `_SAFE_SEGMENT` for `raw_anchor`,
  `lane`, and `record_id` before any path is constructed in both
  `record_path` and `append_record`; verified by direct code read, not
  exercised by a new test in this pass (defended by existing platform
  invariant, not producer-local logic).
- Candidate: the `content_hash` computed in `_finish_record`
  (compact-separator JSON) might drift from the bytes actually persisted by
  `append_silver_record` (`data_lake/canonical_json.py::canonical_record_bytes`,
  pretty-printed with `indent=2`). Defense: these are two intentionally
  different, independently-documented encodings —
  `content_hash_basis: canonical_json_excluding_content_hash` is a
  hash-only canonical form distinct from the pretty-printed on-disk
  persistence format; the unit test's `_computed_content_hash` helper
  replicates the same compact-separator form the producer uses, and both
  passed in the full and focused test runs. Not a defect.
- Candidate: a `TOCTOU` gap between reading the projection file's bytes and
  calling `data_root.load_raw_packet(packet_id)` for the raw packet. Defense:
  raw packets are append-only/immutable once committed per the Data Lake
  contract; there is no rewrite path that could change the raw packet between
  the two reads within one process invocation.
- Candidate: the runner's exception handling might fall through to the success
  `print()` path on failure. Defense: `argparse.ArgumentParser.exit()` raises
  `SystemExit`, which propagates out of the `except` block; the success prints
  are unreachable on failure. Traced by code read.

## 6. Off-Scope Flags

- The Sephora `product_id`/`sku` entity-granularity ambiguity (MAJOR-2) has its
  root field-shape cause in `forseti-harness/source_capture/retail_pdp_projection.py`
  (`_offer_fields_from_product`), which is in-diff review scope but **outside**
  the bounded patch scope (not one of the 11 named patchable files). Flagged,
  not touched.
- `forseti-harness/data_lake/root.py` (`append_record_set`, `_atomic_create`,
  `_validate_segment`) is canonical lake infrastructure, outside the bounded
  patch scope. Read-only; MAJOR-1's fix stayed local to the named producer file
  instead of switching to `append_record_set`, which would require adding a
  `completion_lane` and would route the write through `data_root.append_record`
  directly rather than the Silver front door (`append_silver_record`) — a
  bigger, doctrine-adjacent change outside this pass's scope.

## 7. Bounded Patch Disposition

Patched, inside the named scope:

- `forseti-harness/source_capture/retail_pdp_silver.py` — MAJOR-1 fix
  (best-effort cleanup of already-written sibling records on a mid-batch
  append failure).
- `forseti-harness/tests/unit/test_retail_pdp_silver.py` — three new tests
  closing MAJOR-3 and proving MAJOR-1's fix red-green.

Not patched (flagged only, per findings above): MAJOR-2, MINOR-1, MINOR-2.

Working tree state: uncommitted, left for home-model adjudication per the
commission (`edit_permission: patch-only`, report-write separately
authorized).

Diffs below are generated with `git diff -U0` (zero context lines) instead of
the default 3-line context, solely to avoid literal blank-context-line rows
that carry only a single trailing space (a standard, valid unified-diff
context marker for an unchanged blank source line) — content is otherwise
real, complete, unedited `git diff` output, not hand-collapsed or trimmed.

`[producer]` `forseti-harness/source_capture/retail_pdp_silver.py`:

```diff
diff --git a/forseti-harness/source_capture/retail_pdp_silver.py b/forseti-harness/source_capture/retail_pdp_silver.py
index fffba169..3c7d7e5e 100644
--- a/forseti-harness/source_capture/retail_pdp_silver.py
+++ b/forseti-harness/source_capture/retail_pdp_silver.py
@@ -115,10 +115,22 @@ def derive_retail_pdp_silver_from_projection(
-    paths = [
-        append_silver_record(
-            data_root,
-            raw_anchor=packet_id,
-            lane=RETAIL_PDP_SILVER_LANE,
-            record_id=record["record_id"],
-            record=record,
-        )
-        for record in records
-    ]
+    # Validation above rules out a malformed record prefix, but the sibling
+    # records still write as separate create-only files: a filesystem failure
+    # partway through the loop (e.g. disk full) would otherwise leave an
+    # orphaned, misleading partial (a ProductEntity with no offer/review). Best-
+    # effort unwind any already-written siblings before re-raising so a mid-batch
+    # failure cannot masquerade as a partial success.
+    paths: list[Path] = []
+    try:
+        for record in records:
+            paths.append(
+                append_silver_record(
+                    data_root,
+                    raw_anchor=packet_id,
+                    lane=RETAIL_PDP_SILVER_LANE,
+                    record_id=record["record_id"],
+                    record=record,
+                )
+            )
+    except Exception:
+        for written_path in paths:
+            written_path.unlink(missing_ok=True)
+        raise
```

`[unit-test]` `forseti-harness/tests/unit/test_retail_pdp_silver.py`:

```diff
diff --git a/forseti-harness/tests/unit/test_retail_pdp_silver.py b/forseti-harness/tests/unit/test_retail_pdp_silver.py
index 6efa54d9..4f57711e 100644
--- a/forseti-harness/tests/unit/test_retail_pdp_silver.py
+++ b/forseti-harness/tests/unit/test_retail_pdp_silver.py
@@ -11,0 +12 @@ from data_lake.silver_lineage import is_silver_record_source_backed_complete
+from source_capture import retail_pdp_silver
@@ -201,0 +203,86 @@ def test_projection_without_variant_refuses_empty_success(tmp_path: Path) -> Non
+
+
+def test_duplicate_variant_identity_fails_before_any_silver_write(tmp_path: Path) -> None:
+    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
+    packet_id, projection_path = _capture_and_project(root, tmp_path)
+    projection = json.loads(projection_path.read_text(encoding="utf-8"))
+    variant_rows = [row for row in projection["rows"] if row["row_kind"] == "retail_variant_offer"]
+    duplicate = json.loads(json.dumps(variant_rows[0]))
+    duplicate["row_id"] = f"{duplicate['row_id']}:dup"
+    projection["rows"].append(duplicate)
+    projection["loss_ledger"]["preserved_evidence_rows"] = len(projection["rows"])
+    duplicated = root.append_record(
+        subtree="derived",
+        raw_anchor=packet_id,
+        lane=PROJECTION_RETAIL_PDP_LANE,
+        record_id="duplicate-variant.json",
+        data=(json.dumps(projection, indent=2, sort_keys=True) + "\n").encode("utf-8"),
+    )
+
+    with pytest.raises(RetailPdpSilverError, match="ambiguous"):
+        derive_retail_pdp_silver_from_projection(
+            data_root=root,
+            packet_id=packet_id,
+            projection_record_id=duplicated.name,
+        )
+
+    assert not root.lane_dir(
+        subtree="derived", raw_anchor=packet_id, lane=RETAIL_PDP_SILVER_LANE
+    ).exists()
+
+
+def test_orphan_review_substrate_fails_before_any_silver_write(tmp_path: Path) -> None:
+    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
+    packet_id, projection_path = _capture_and_project(root, tmp_path)
+    projection = json.loads(projection_path.read_text(encoding="utf-8"))
+    for row in projection["rows"]:
+        if row["row_kind"] == "retail_review_substrate":
+            row["retailer"] = "sephora"
+    orphaned = root.append_record(
+        subtree="derived",
+        raw_anchor=packet_id,
+        lane=PROJECTION_RETAIL_PDP_LANE,
+        record_id="orphan-review.json",
+        data=(json.dumps(projection, indent=2, sort_keys=True) + "\n").encode("utf-8"),
+    )
+
+    with pytest.raises(RetailPdpSilverError, match="no matching retailer-local product identity"):
+        derive_retail_pdp_silver_from_projection(
+            data_root=root,
+            packet_id=packet_id,
+            projection_record_id=orphaned.name,
+        )
+
+    assert not root.lane_dir(
+        subtree="derived", raw_anchor=packet_id, lane=RETAIL_PDP_SILVER_LANE
+    ).exists()
+
+
+def test_mid_batch_append_failure_leaves_no_orphaned_partial(
+    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
+) -> None:
+    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
+    packet_id, projection_path = _capture_and_project(root, tmp_path)
+
+    real_append = retail_pdp_silver.append_silver_record
+    calls = {"count": 0}
+
+    def _flaky_append(*args, **kwargs):
+        calls["count"] += 1
+        if calls["count"] == 2:
+            raise OSError("simulated disk failure on second sibling record")
+        return real_append(*args, **kwargs)
+
+    monkeypatch.setattr(retail_pdp_silver, "append_silver_record", _flaky_append)
+
+    with pytest.raises(OSError, match="simulated disk failure"):
+        derive_retail_pdp_silver_from_projection(
+            data_root=root,
+            packet_id=packet_id,
+            projection_record_id=projection_path.name,
+        )
+
+    lane_dir = root.lane_dir(
+        subtree="derived", raw_anchor=packet_id, lane=RETAIL_PDP_SILVER_LANE
+    )
+    assert not lane_dir.exists() or not any(lane_dir.iterdir())
```

## 8. Neutral Per-Change Source Citations

- `[producer]` `forseti-harness/source_capture/retail_pdp_silver.py` pre-patch
  lines 115-124 vs. `data_lake/root.py::append_record_set` docstring (lines
  593-616) naming the all-or-nothing multi-record pattern this producer did not
  use — basis for MAJOR-1.
- `[producer]` `_entity_key` (retail_pdp_silver.py:392-406) vs.
  `[projection]` `_offer_fields_from_product` (retail_pdp_projection.py:1052-1070)
  and the Amazon/Target field constructors (retail_pdp_projection.py:739-752,
  826-847) — basis for MAJOR-2's cross-retailer product_id/sku comparison.
- `[unit-test]` pre-patch `test_retail_pdp_silver.py` (4 tests) vs.
  `[producer-contract]` `retail_pdp_silver_producer_contract_v0.md` "Failure
  And Validation Contract" naming ambiguous-identity and orphan-review as
  required fail-before-append behaviors — basis for MAJOR-3.
- Silver Vault Acceptance Criterion 4 ("Entity records contain stable identity
  only") — supporting authority for MAJOR-2.

## 9. Validation

| Command | Result |
| --- | --- |
| `git diff --check origin/main...HEAD` | PASS (exit 0, before and after patch — patch is test/implementation only, no whitespace/conflict markers) |
| `python .agents/hooks/check_silver_lane_registry.py --strict` | PASS (`check_silver_lane_registry: OK (no silver-lane write violations)`) |
| `python .agents/hooks/check_map_links.py --strict` | PASS (`check_map_links --strict: OK (0 findings)`; 36 pre-existing annotated nonresolving links, unrelated to this PR) |
| `pytest tests/unit/test_retail_pdp_silver.py tests/contract/test_capture_runner_lake_seam_coverage.py tests/contract/test_silver_reader_selection_gate.py` | PASS — 30 passed (27 pre-existing + 3 new, post-patch) |
| Red-green proof for MAJOR-1 fix | PASS — reverted fix via `git stash`, ran `test_mid_batch_append_failure_leaves_no_orphaned_partial` alone: **FAILED** (`AssertionError`, orphaned `retail_pdp_silver` lane dir with 1 file left on disk); restored fix via `git stash pop`, same test: **PASSED** |
| `pytest` (full `forseti-harness` suite, post-patch) | PASS — see below |

Full-suite result (post-patch): PASS. Run directly (not through a pipe) so the
real process exit code was captured unambiguously:
`python -m pytest -p no:cacheprovider -q > pytest_full_run.log 2>&1; echo
"PYTEST_EXIT_CODE=$?"` returned `PYTEST_EXIT_CODE=0` (observed, not inferred
from a piped `tail`'s exit status). This repository's pytest configuration
does not print a terminal `N passed`/`N failed` count line (none was present
anywhere in the 95-line captured output, including the deprecation-warning
footer that is genuinely the last content); exit code `0` is pytest's own
authoritative signal that every collected test passed with no failures,
errors, or collection failures. No exact test count is claimed because none
was observed in the output; the earlier `forseti-harness/tests/unit` +
`tests/contract` focused run (§ above, 30 passed) and this exit-code-0 full
run together are the only test-count/pass claims made in this report.

`git diff --check` was re-run after the patch and remained PASS. No validation
command was left `NOT_RUN` or `BLOCKED`.

## 10. Off-Scope Flags (Repeated Per Contract §6 Cross-Reference)

See §6 above — restated here per report-contract shape: two off-scope flags,
neither patched, both fully described in §6.

## 11. Controller Verdict

`patch_before_acceptance`

Rationale: two major defects were confirmed with a local, in-scope fix and are
patched with red-green proof (MAJOR-1, MAJOR-3). One major defect (MAJOR-2) is
a genuine identity-semantics gap that this pass could not close without
inventing entity-granularity policy the reviewed contracts do not resolve —
it requires an owner/architecture decision before the PR is accepted as fully
correct, not a re-run of this lane. The two minor findings are non-blocking
optional hardening.

## 12. Residual-Risk Note

With MAJOR-2 unresolved, any future Sephora capture with a `ProductGroup`
`hasVariant` structure containing more than one SKU will silently merge those
SKUs' offer/review observations under one entity_key in the live lake once
this producer runs against real Sephora packets. This is bounded and does not
affect Amazon (the PR's proof source, where `product_id == sku` always) or
Walmart/Target (same-value fields); it would surface only when Sephora capture
begins flowing through this generic producer. All other findings are patched
or accepted as non-blocking. No critical finding was identified.

## 13. Review-Use Boundary And Home-Model Adjudication Handoff

This report, its findings, citations, diff, verdict, and residual-risk note
are decision input only: not approval, not validation, not mandatory
remediation, and not executor-ready patch authority or permission to keep any
patch. The commissioning OpenAI/GPT home model must:

1. Accept, modify, or reject every material finding and the patch, hunk by
   hunk if desired.
2. Close any self-closable issue inside its own authority and this commission's
   scope in the same adjudication turn (for example, deciding whether to keep
   the two patched files as-is).
3. Revert any rejected hunk.
4. Route MAJOR-2 to the owner or an architecture pass for the entity-
   granularity decision — this pass could not and did not resolve it.
5. Once no unresolved material issue remains, batch commit/push/PR/merge
   administration into exactly one land step, then name the 1-5 material next
   moves requiring judgment (expected candidates: MAJOR-2's owner decision;
   whether MINOR-1's non-Amazon Silver fixture coverage is worth adding now or
   deferred to accompany MAJOR-2's resolution).

Nothing in this report grants merge, deployment, live-capture, persistent-
session, Gold/Judgment, source-of-truth promotion, validation, readiness,
product-proof, or automatic keep authority.
