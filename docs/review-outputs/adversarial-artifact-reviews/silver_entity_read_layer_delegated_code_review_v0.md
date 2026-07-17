# Silver Entity Read Layer Delegated Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated code review-and-patch report
scope: >
  Cross-vendor repository review of the Silver entity read layer change at
  ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f, including bounded working-tree
  repairs to native product identity handling, creator alias conflict
  visibility, lookup matching, generated-view integrity checks, tests, and the
  owning consumption-seam contract.
use_when:
  - Adjudicating the delegate findings and working-tree diff before deciding what to keep.
  - Verifying the observed validation evidence for this bounded review-and-patch pass.
authority_boundary: retrieval_only
reviewed_by: openai-gpt-5-codex
authored_by: unrecorded
author_vendor: Anthropic
delegate_vendor: OpenAI
de_correlation_bar: cross_vendor_discovery
de_correlation_status: satisfied
current_receiving_actor_role: controller
dispatch_mode: external-controller-courier
target_worktree: C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\silver-compatibility-registry-f01c62
target_branch: claude/silver-entity-read-layer
required_revision: ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f
observed_head: b7d7c51e452c5d252fcf43f8f6a106b0a42f7397
revision_mode: ancestor
initial_dirty_state: clean
reviewed_diff: 039171df173dbeedc9ed8cba6ec183b8ecee7219...ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f
```

## Review summary

```yaml
review_summary:
  status: issues_found
  recommendation: home_adjudication_required
  critical_findings: 0
  major_findings: 3
  minor_findings: 1
  patched_findings:
    - DRL-001
    - DRL-002
    - DRL-003
    - DRL-004
  needs_architecture_pass: false
  patch_scope_breached: false
  lifecycle_hard_stop_observed: true
  minimum_closure_condition: >
    The home Chief Architect adjudicates each finding and hunk, keeps,
    modifies, or rejects the working-tree changes, and preserves the observed
    validation and residual-risk boundaries.
  next_authorized_action: >
    Home Chief Architect adjudication only. The delegate must not commit,
    push, open or update a PR, merge, stash, reset, clean, or perform
    repository hygiene.
```

The implementation was structurally sound in its shared-classifier reuse,
reader posture, deterministic rebuild path, and authority boundary, but four
patch-level defects could misroute entity lookups or hide inconsistent identity
evidence. All four received bounded working-tree repairs and focused regression
coverage. This report does not approve or keep those repairs.

## Findings

### DRL-001 — Normalized substring matching can route the wrong brand or line

- severity: major
- confidence: high
- commissioned target and purpose: scoped read-only creator/product lookup that must avoid false positives across brands and creators
- reviewed target: `forseti-harness/runners/run_derived_retrieval_lookup.py`
- location: pre-patch required revision lines 101-113; repaired at current lines 109-130
- evidence: the pre-patch condition accepted `wanted in token`, so `grand` matched brand `Ariana Grande` even though it was neither the exact brand, exact line, nor exact combined identity. The red regression reproduced a successful but incorrect result.
- authority basis: the consumption-seam contract defines brand/line entity routing and exact stored identity strings; the commission explicitly requires normalized matching not to create cross-brand false positives.
- impact: a caller can receive the wrong product entity and its packet/Silver refs, turning a convenience lookup into incorrect routing.
- minimum_closure_condition: mention lookup admits only normalized exact brand, exact line, or exact combined brand+line identities, with a regression proving a partial token does not match.
- next_authorized_action: patched within scope; home Chief Architect adjudicates the exact-match behavior and test.
- verification expectation: same-check red-green proof.
- red-green proof: before repair, `test_lookup_runner_resolves_creator_and_mention` failed because `--mention grand` exited 0; after repair, the focused file passed 16/16.
- patch_queue_entry: not applicable; the authorized delegate applied the bounded patch directly.

### DRL-002 — Incomplete or tampered generated view pairs can be served as successful lookup data

- severity: major
- confidence: high
- commissioned target and purpose: lookup runner must surface generation provenance and use honest 0/1/2 exit semantics
- reviewed target: `forseti-harness/runners/run_derived_retrieval_lookup.py`
- location: pre-patch required revision lines 36-58 and 151-154; repaired at current lines 37-61 and 168-175
- evidence: the pre-patch loader accepted a view with no manifest, never checked manifest/view identity, schema agreement, or `view_sha256`, and returned exit 1 for `view_not_built`, conflating an unavailable generated read model with a valid no-match result.
- authority basis: the Silver generated-read-model contract requires paired manifest-backed views; the commission binds exit 0 to found, exit 1 to not found, and exit 2 to operational/data errors.
- impact: callers can consume altered or incomplete routing bytes while seeing a successful match, or misread a missing index as evidence that an entity is absent.
- minimum_closure_condition: the lookup fails closed unless both files exist, both are JSON objects for the requested view and schema, and the stored bytes match `manifest.view_sha256`; missing views and invalid pairs exit 2.
- next_authorized_action: patched within scope; home Chief Architect adjudicates the fail-closed loader and exit mapping.
- verification expectation: same-check red-green proof using both absent and tampered generated state.
- red-green proof: before repair, the absent view returned exit 1 and a tampered valid-JSON view remained usable; after repair, the regression exits 2 and names the hash mismatch.
- patch_queue_entry: not applicable; the authorized delegate applied the bounded patch directly.

### DRL-003 — Native product identity can be fabricated from partial rows or split across conflicting keys

- severity: major
- confidence: high
- commissioned target and purpose: native product pages must not conflate distinct products or fabricate identity from partial Fragrantica projection rows
- reviewed target: `forseti-harness/data_lake/derived_retrieval_views.py`
- location: pre-patch required revision lines 303-355; repaired at current lines 321-430
- evidence: a missing brand was converted to the literal key `unknown`; deduplication compared full entries only inside one `(brand, line)` bucket, so the same native `(anchor, source site, site id)` could appear under conflicting brand/line or URL values.
- authority basis: the consumption-seam contract says the section routes a brand/line entity to its own native product-page capture and remains non-authoritative; the commission explicitly forbids identity fabrication and conflation.
- impact: partial extraction can create a false entity, while conflicting projection rows can route one native product to multiple incompatible identities.
- minimum_closure_condition: rows without both brand and line are residual-only; one native identity key is bound once, conflicts remain residuals, and all contributing projection refs remain manifest-visible.
- next_authorized_action: patched within scope; home Chief Architect adjudicates the residual vocabulary and first-binding behavior.
- verification expectation: same-check red-green proof for missing brand and conflicting identity rows.
- red-green proof: before repair, the regression produced an `unknown` brand and accepted the conflicting identity; after repair, one entry remains and both incomplete/conflict residuals are present.
- patch_queue_entry: not applicable; the authorized delegate applied the bounded patch directly.

### DRL-004 — Conflicting account aliases are silently collapsed

- severity: minor
- confidence: high
- commissioned target and purpose: by_creator keys must avoid hidden merges/splits and preserve exact per-platform identity evidence
- reviewed target: `forseti-harness/data_lake/derived_retrieval_views.py`
- location: pre-patch required revision lines 198-204; repaired at current lines 198-224
- evidence: `setdefault` retained the first alias value for a `(namespace, native_id)` and discarded later contradictory values without any residual.
- authority basis: the by_creator contract preserves exact observed strings and forbids cross-platform identity unification; inconsistent aliases are evidence conflicts, not silently consistent metadata.
- impact: the view remains deterministic but hides an upstream identity contradiction, reducing operator confidence and making a secondary conflicting alias appear never observed.
- minimum_closure_condition: preserve the deterministic primary alias while exposing every contradictory value in a named residual for upstream adjudication.
- next_authorized_action: patched within scope; home Chief Architect adjudicates whether visible residualization is sufficient.
- verification expectation: focused deterministic test.
- red-green proof: before repair, no conflict residual existed; after repair, the view records both alias values under `account_alias_conflict`.
- patch_queue_entry: not applicable; the authorized delegate applied the bounded patch directly.

## Considered and defended

- Shared classifier fidelity survived. `_classified_silver_sweep` uses the same active `silver_envelope` registry, current envelope gate, `build_creator_metric_lineage_index`, and `classify_silver_vault_record_sources` call used by the census. No local authority-status grammar was found.
- Persisted account-subject coverage survived. Current producers and checked-in compatibility fixtures use `platform_public_account` subjects or `public_content_object` subjects with `published_by_account_native_id`; both shapes are handled. `public_comment` is not an account-subject shape and remains correctly excluded.
- Rebuildability survived. `prove_derived_retrieval_rebuildability` reloads stored generation stamps and product policy, regenerates from lake material, and byte-compares separately against stored view and manifest files. It does not compare a build to itself.
- Determinism survived. Active lanes, paths, account keys, statuses, residuals, product keys, and output entries are explicitly sorted; no new current-time value enters generated bytes when a stored stamp is supplied.
- Reader-selection posture survived. `inventory.py` declares `all_siblings`, matching the actual whole-active-lane classification sweep; the contract gate passed.
- Authority and write boundaries survived. The lookup runner reads only the generated view home. The builder remains confined by `root._reverify()` and `root._within(...)`; no pickup, retrieval-authority, SQL, cache, or live-lake fallback was introduced.
- Test closure survived. `BUILT_VIEWS`, schema versions, account subject families, native product identity, lookup status behavior, rebuild proof, and inventory/reader-policy gates have meaningful break-detecting assertions.

## Exact bounded delegate diff

```diff
diff --git a/forseti-harness/data_lake/derived_retrieval_views.py b/forseti-harness/data_lake/derived_retrieval_views.py
index db48041e..ae801e4c 100644
--- a/forseti-harness/data_lake/derived_retrieval_views.py
+++ b/forseti-harness/data_lake/derived_retrieval_views.py
@@ -197,11 +197,29 @@ def _classified_silver_sweep(root) -> dict[str, Any]:
             }
             for namespace, native_id, aliases in _account_subject_keys(record):
                 entry = accounts.setdefault(
-                    (namespace, native_id), {"aliases": {}, "refs_by_anchor": defaultdict(list)}
+                    (namespace, native_id),
+                    {
+                        "aliases": {},
+                        "alias_values": defaultdict(set),
+                        "refs_by_anchor": defaultdict(list),
+                    },
                 )
                 for alias_key, alias_value in aliases.items():
                     entry["aliases"].setdefault(alias_key, alias_value)
+                    entry["alias_values"][alias_key].add(str(alias_value))
                 entry["refs_by_anchor"][anchor].append(ref)
+    for (namespace, native_id), entry in sorted(accounts.items()):
+        for alias_key, alias_values in sorted(entry["alias_values"].items()):
+            if len(alias_values) > 1:
+                residuals.append(
+                    {
+                        "status": "account_alias_conflict",
+                        "namespace": namespace,
+                        "native_id": native_id,
+                        "alias_key": alias_key,
+                        "alias_values": sorted(alias_values),
+                    }
+                )
     return {
         "anchor_lane_status": anchor_lane_status,
         "accounts": accounts,
@@ -300,12 +318,14 @@ def build_by_creator_view(root, *, sweep: dict | None = None) -> tuple[dict, lis
     return view, list(sweep["source_refs"])


-def _native_product_pages(root, sweep: dict) -> tuple[dict, list[str]]:
+def _native_product_pages(root, sweep: dict) -> tuple[dict, list[str], list[dict]]:
     """Native product-page identity rows from committed Fragrantica projections
     (view-only mechanical records used as identity ROUTING, never authority),
     each joined to its anchor's classified Silver record counts."""
-    pages: dict[str, dict[str, list[dict]]] = {}
+    pages: dict[str, dict[str, dict[tuple[str, str, str], dict]]] = {}
+    identity_bindings: dict[tuple[str, str, str], tuple[str, str, dict]] = {}
     source_refs: list[str] = []
+    residuals: list[dict[str, Any]] = []
     derived = root.path / "derived"
     for path in sorted(derived.glob(f"*/*/{FRAGRANTICA_PROJECTION_LANE}/*")):
         if not path.is_file():
@@ -321,17 +341,42 @@ def _native_product_pages(root, sweep: dict) -> tuple[dict, list[str]]:
         for row in rows:
             if not isinstance(row, dict) or row.get("row_kind") != FRAGRANTICA_PRODUCT_ROW_KIND:
                 continue
-            brand = str(row.get("brand_or_house") or "unknown")
-            line = str(row.get("source_object_name") or "")
-            if not line:
+            source_ref = f"{anchor}/{FRAGRANTICA_PROJECTION_LANE}/{path.name}"
+            source_refs.append(source_ref)
+            brand = str(row.get("brand_or_house") or "").strip()
+            line = str(row.get("source_object_name") or "").strip()
+            missing_fields = [
+                field
+                for field, value in (
+                    ("brand_or_house", brand),
+                    ("source_object_name", line),
+                )
+                if not value
+            ]
+            if missing_fields:
+                residuals.append(
+                    {
+                        "status": "native_product_page_identity_incomplete",
+                        "raw_anchor": anchor,
+                        "lane": FRAGRANTICA_PROJECTION_LANE,
+                        "record_id": path.name,
+                        "row_id": row.get("row_id"),
+                        "missing_fields": missing_fields,
+                    }
+                )
                 continue
             visible = row.get("source_visible_fields")
+            canonical_url = (
+                str(visible.get("canonical_url") or "").strip()
+                if isinstance(visible, dict)
+                else ""
+            )
+            site_native_id = str(row.get("source_object_site_id") or "").strip()
+            source_site = str(row.get("source_platform") or "fragrantica").strip()
             entry = {
-                "source_site": str(row.get("source_platform") or "fragrantica"),
-                "site_native_id": row.get("source_object_site_id"),
-                "canonical_url": (
-                    visible.get("canonical_url") if isinstance(visible, dict) else None
-                ),
+                "source_site": source_site,
+                "site_native_id": site_native_id or None,
+                "canonical_url": canonical_url or None,
                 "raw_anchor": anchor,
                 "identity_source": (
                     f"{FRAGRANTICA_PROJECTION_LANE} {FRAGRANTICA_PRODUCT_ROW_KIND} row "
@@ -342,17 +387,50 @@ def _native_product_pages(root, sweep: dict) -> tuple[dict, list[str]]:
                     for lane, statuses in sorted(sweep["anchor_lane_status"][anchor].items())
                 },
             }
-            entries = pages.setdefault(brand, {}).setdefault(line, [])
-            # An anchor may hold several projection records carrying the same
-            # snapshot row; one identity entry per (anchor, site id) is enough.
-            if entry not in entries:
-                entries.append(entry)
-            source_refs.append(f"{anchor}/{FRAGRANTICA_PROJECTION_LANE}/{path.name}")
+            identity_key = (anchor, source_site, site_native_id or canonical_url)
+            existing = identity_bindings.get(identity_key)
+            if existing is None:
+                identity_bindings[identity_key] = (brand, line, entry)
+                pages.setdefault(brand, {}).setdefault(line, {})[identity_key] = entry
+            elif existing != (brand, line, entry):
+                kept_brand, kept_line, kept_entry = existing
+                residuals.append(
+                    {
+                        "status": "native_product_page_identity_conflict",
+                        "raw_anchor": anchor,
+                        "lane": FRAGRANTICA_PROJECTION_LANE,
+                        "record_id": path.name,
+                        "row_id": row.get("row_id"),
+                        "brand": brand,
+                        "line": line,
+                        "source_site": source_site,
+                        "site_native_id": site_native_id or None,
+                        "kept_brand": kept_brand,
+                        "kept_line": kept_line,
+                        "kept_canonical_url": kept_entry.get("canonical_url"),
+                        "conflicting_canonical_url": canonical_url or None,
+                    }
+                )
     normalized = {
-        brand: {line: sorted(entries, key=lambda e: str(e["raw_anchor"])) for line, entries in sorted(lines.items())}
+        brand: {
+            line: sorted(
+                entries.values(),
+                key=lambda entry: (
+                    str(entry["raw_anchor"]),
+                    str(entry["source_site"]),
+                    str(entry["site_native_id"]),
+                    str(entry["canonical_url"]),
+                ),
+            )
+            for line, entries in sorted(lines.items())
+        }
         for brand, lines in sorted(pages.items())
     }
-    return normalized, sorted(set(source_refs))
+    return (
+        normalized,
+        sorted(set(source_refs)),
+        sorted(residuals, key=lambda row: json.dumps(row, sort_keys=True)),
+    )


 def build_by_mention_view(
@@ -383,7 +461,7 @@ def build_by_mention_view(
             refs = mentions.setdefault(brand, {}).setdefault(line, [])
             if ref not in refs:
                 refs.append(ref)
-    native_pages, native_refs = _native_product_pages(
+    native_pages, native_refs, native_residuals = _native_product_pages(
         root, sweep or _classified_silver_sweep(root)
     )
     view = {
@@ -404,8 +482,8 @@ def build_by_mention_view(
         },
         "native_product_pages": native_pages,
         "selected_record_count": len(selection.selected),
-        "residuals": list(selection.residuals),
-        "residual_count": len(selection.residuals),
+        "residuals": list(selection.residuals) + native_residuals,
+        "residual_count": len(selection.residuals) + len(native_residuals),
     }
     return view, sorted(set(selection.source_refs) | set(native_refs))

diff --git a/forseti-harness/runners/run_derived_retrieval_lookup.py b/forseti-harness/runners/run_derived_retrieval_lookup.py
index a5139c10..63bb95dd 100644
--- a/forseti-harness/runners/run_derived_retrieval_lookup.py
+++ b/forseti-harness/runners/run_derived_retrieval_lookup.py
@@ -16,6 +16,7 @@ A key absent from a view means "not captured or not indexed" — never zero.
 from __future__ import annotations

 import argparse
+import hashlib
 import json
 import re
 import sys
@@ -37,14 +38,26 @@ def _load_view(root: DataLakeRoot, view_name: str) -> tuple[dict | None, dict |
     core = root.path.joinpath(*SILVER_VAULT_CORE_PARTS)
     view_path = core / "query_tables" / f"{view_name}.json"
     manifest_path = core / "manifests" / f"{view_name}.json"
-    if not view_path.is_file():
+    view_exists = view_path.is_file()
+    manifest_exists = manifest_path.is_file()
+    if not view_exists and not manifest_exists:
         return None, None
-    view = json.loads(view_path.read_text(encoding="utf-8"))
-    manifest = (
-        json.loads(manifest_path.read_text(encoding="utf-8"))
-        if manifest_path.is_file()
-        else None
-    )
+    if not view_exists or not manifest_exists:
+        raise ValueError(f"{view_name} generated view/manifest pair is incomplete")
+    view_bytes = view_path.read_bytes()
+    view = json.loads(view_bytes.decode("utf-8"))
+    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
+    if not isinstance(view, dict) or not isinstance(manifest, dict):
+        raise ValueError(f"{view_name} generated view/manifest must both be JSON objects")
+    if view.get("view") != view_name or manifest.get("view") != view_name:
+        raise ValueError(f"{view_name} generated view/manifest identity mismatch")
+    if view.get("view_schema_version") != manifest.get("view_schema_version"):
+        raise ValueError(f"{view_name} generated view/manifest schema mismatch")
+    actual_sha256 = hashlib.sha256(view_bytes).hexdigest()
+    if manifest.get("view_sha256") != actual_sha256:
+        raise ValueError(
+            f"{view_name} view_sha256 mismatch: manifest does not match stored view bytes"
+        )
     return view, manifest


@@ -71,6 +84,8 @@ def lookup_creator(root: DataLakeRoot, query: str) -> dict[str, Any]:
         prefix, _, rest = query.partition(":")
         namespace_filter = _normalized(prefix)
         wanted = _normalized(rest)
+    if not wanted:
+        raise ValueError("creator query must contain a non-empty account id or alias")
     matches = []
     for namespace, ids in view.get("creators", {}).items():
         if namespace_filter and _normalized(namespace) != namespace_filter:
@@ -99,6 +114,8 @@ def lookup_mention(root: DataLakeRoot, query: str) -> dict[str, Any]:
             "hint": "run runners/run_data_lake_indexes_rebuild.py --target derived_retrieval",
         }
     wanted = _normalized(query)
+    if not wanted:
+        raise ValueError("mention query must contain a non-empty brand or line identity")
     matches: list[dict[str, Any]] = []
     for section in ("mentions", "native_product_pages"):
         for brand, lines in view.get(section, {}).items():
@@ -108,7 +125,7 @@ def lookup_mention(root: DataLakeRoot, query: str) -> dict[str, Any]:
                     _normalized(line),
                     _normalized(f"{brand} {line}"),
                 }
-                if wanted in tokens or any(wanted and wanted in token for token in tokens):
+                if wanted in tokens:
                     matches.append(
                         {"source_class": section, "brand": brand, "line": line, "refs": refs}
                     )
@@ -137,7 +154,7 @@ def main(argv: list[str] | None = None) -> int:
     )
     target.add_argument(
         "--mention",
-        help="Brand/line product entity query (normalized substring match).",
+        help="Brand/line product entity query (normalized exact brand, line, or combined identity).",
     )
     args = parser.parse_args(argv)
     try:
@@ -151,7 +168,11 @@ def main(argv: list[str] | None = None) -> int:
         print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
         return 2
     print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
-    return 0 if result["status"] == "found" else 1
+    if result["status"] == "found":
+        return 0
+    if result["status"] == "not_found":
+        return 1
+    return 2


 if __name__ == "__main__":
diff --git a/forseti-harness/tests/test_data_lake_indexes_rebuild.py b/forseti-harness/tests/test_data_lake_indexes_rebuild.py
index 04303dea..0411a38d 100644
--- a/forseti-harness/tests/test_data_lake_indexes_rebuild.py
+++ b/forseti-harness/tests/test_data_lake_indexes_rebuild.py
@@ -396,11 +396,17 @@ def _write_creator_metric_record(
     )


-def _write_fragrantica_projection(root: DataLakeRoot, raw_anchor: str) -> None:
+def _write_fragrantica_projection(
+    root: DataLakeRoot,
+    raw_anchor: str,
+    *,
+    record_id: str = "projection.json",
+    rows: list[dict] | None = None,
+) -> None:
     projection = {
         "packet_id": raw_anchor,
         "certification": "view_only; not_cleaned; not_normalized; not_judgment_ready",
-        "rows": [
+        "rows": rows or [
             {
                 "row_id": "slice_01:fragrantica:product_snapshot",
                 "row_kind": "fragrance_product_snapshot",
@@ -418,7 +424,7 @@ def _write_fragrantica_projection(root: DataLakeRoot, raw_anchor: str) -> None:
         subtree="derived",
         raw_anchor=raw_anchor,
         lane="projection_fragrantica",
-        record_id="projection.json",
+        record_id=record_id,
         data=canonical_record_bytes(projection),
     )

@@ -466,6 +472,40 @@ def test_by_creator_indexes_account_subjects_with_classified_authority(
     assert f"{pid}/creator_metric_silver/account_metric.json" in source_refs


+def test_by_creator_surfaces_conflicting_account_aliases(tmp_path: Path) -> None:
+    root = DataLakeRoot.for_test(tmp_path / "lake")
+    pid = _commit_packet(root, tmp_path, "creator-alias-conflict")
+    for record_id, account_id in (
+        ("first.json", "acct_ig_fixture_001"),
+        ("second.json", "acct_ig_fixture_002"),
+    ):
+        _write_creator_metric_record(
+            root,
+            pid,
+            record_id,
+            subject_ref={
+                "namespace": "instagram",
+                "kind": "platform_public_account",
+                "native_id": "fixture_creator",
+                "orca_platform_account_id": account_id,
+            },
+        )
+
+    view, _source_refs = build_by_creator_view(root)
+
+    assert view["creators"]["instagram"]["fixture_creator"]["aliases"] == {
+        "orca_platform_account_id": "acct_ig_fixture_001"
+    }
+    assert any(
+        residual["status"] == "account_alias_conflict"
+        and residual["namespace"] == "instagram"
+        and residual["native_id"] == "fixture_creator"
+        and residual["alias_values"]
+        == ["acct_ig_fixture_001", "acct_ig_fixture_002"]
+        for residual in view["residuals"]
+    )
+
+
 def test_by_mention_carries_native_product_page_identity(tmp_path: Path) -> None:
     root = DataLakeRoot.for_test(tmp_path / "lake")
     pid = _commit_packet(root, tmp_path, "product")
@@ -483,6 +523,70 @@ def test_by_mention_carries_native_product_page_identity(tmp_path: Path) -> None
     assert "never be read as an observed zero" in view["zero_rows_meaning"]


+def test_by_mention_rejects_partial_and_conflicting_native_product_identity(
+    tmp_path: Path,
+) -> None:
+    root = DataLakeRoot.for_test(tmp_path / "lake")
+    pid = _commit_packet(root, tmp_path, "product-identity")
+    base_row = {
+        "row_kind": "fragrance_product_snapshot",
+        "brand_or_house": "Ariana Grande",
+        "source_object_name": "Cloud",
+        "source_object_site_id": "50384",
+        "source_platform": "fragrantica",
+    }
+    _write_fragrantica_projection(
+        root,
+        pid,
+        record_id="first.json",
+        rows=[
+            {
+                **base_row,
+                "row_id": "first",
+                "source_visible_fields": {
+                    "canonical_url": "https://www.fragrantica.com/perfume/Ariana-Grande/Cloud-50384.html"
+                },
+            },
+            {
+                **base_row,
+                "row_id": "missing-brand",
+                "brand_or_house": None,
+                "source_object_name": "Cloud Pink",
+                "source_object_site_id": "81442",
+                "source_visible_fields": {
+                    "canonical_url": "https://www.fragrantica.com/perfume/Ariana-Grande/Cloud-Pink-81442.html"
+                },
+            },
+        ],
+    )
+    _write_fragrantica_projection(
+        root,
+        pid,
+        record_id="second.json",
+        rows=[
+            {
+                **base_row,
+                "row_id": "second",
+                "brand_or_house": "Impostor Brand",
+                "source_visible_fields": {
+                    "canonical_url": "https://www.fragrantica.com/perfume/Ariana-Grande/Cloud-50384.html?duplicate=1"
+                },
+            }
+        ],
+    )
+
+    view, source_refs = build_by_mention_view(root, product_mention_policy=_POLICY)
+
+    assert "unknown" not in view["native_product_pages"]
+    assert "Impostor Brand" not in view["native_product_pages"]
+    assert len(view["native_product_pages"]["Ariana Grande"]["Cloud"]) == 1
+    statuses = [residual["status"] for residual in view["residuals"]]
+    assert "native_product_page_identity_incomplete" in statuses
+    assert "native_product_page_identity_conflict" in statuses
+    assert f"{pid}/projection_fragrantica/first.json" in source_refs
+    assert f"{pid}/projection_fragrantica/second.json" in source_refs
+
+
 def test_lookup_runner_resolves_creator_and_mention(tmp_path: Path, capsys, monkeypatch) -> None:
     from runners.run_derived_retrieval_lookup import main as lookup_main

@@ -517,10 +621,48 @@ def test_lookup_runner_resolves_creator_and_mention(tmp_path: Path, capsys, monk
     assert mention["matches"][0]["source_class"] == "native_product_pages"
     assert mention["matches"][0]["brand"] == "Ariana Grande"

+    assert lookup_main(["--mention", "grand"]) == 1
+    assert json.loads(capsys.readouterr().out)["status"] == "not_found"
+
     assert lookup_main(["--creator", "nobody_here"]) == 1
     assert json.loads(capsys.readouterr().out)["status"] == "not_found"


+def test_lookup_runner_fails_closed_on_absent_or_tampered_view_pair(
+    tmp_path: Path, capsys, monkeypatch
+) -> None:
+    from runners.run_derived_retrieval_lookup import main as lookup_main
+
+    root = DataLakeRoot.for_test(tmp_path / "lake")
+    monkeypatch.setattr(DataLakeRoot, "resolve", staticmethod(lambda **_kwargs: root))
+
+    assert lookup_main(["--creator", "fixture_creator"]) == 2
+    assert json.loads(capsys.readouterr().out)["status"] == "view_not_built"
+
+    pid = _commit_packet(root, tmp_path, "tampered-view")
+    _write_fragrantica_projection(root, pid)
+    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
+    view_path = (
+        root.path
+        / "indexes"
+        / "derived_retrieval"
+        / "silver_vault"
+        / "core"
+        / "query_tables"
+        / "by_mention.json"
+    )
+    tampered = json.loads(view_path.read_text(encoding="utf-8"))
+    tampered["native_product_pages"]["Ariana Grande"]["Cloud"][0][
+        "canonical_url"
+    ] = "https://example.test/tampered"
+    view_path.write_bytes(canonical_record_bytes(tampered))
+
+    assert lookup_main(["--mention", "cloud"]) == 2
+    error = json.loads(capsys.readouterr().out)
+    assert error["status"] == "error"
+    assert "view_sha256" in error["error"]
+
+
 def test_runner_cli_fails_closed_on_in_repo_root(tmp_path: Path, capsys) -> None:
     # tmp_path lives inside the repo working tree; production resolution must
     # refuse it (write-boundary fail-closed rule), exit 2, and write nothing.
diff --git a/forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md b/forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
index 8fe9f89b..c9e98af6 100644
--- a/forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
+++ b/forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
@@ -229,7 +229,10 @@ does not accept an implicit current/latest policy.
   anchor (identity from the view-only Fragrantica projection product
   snapshot, labeled routing, never Silver authority) with the anchor's
   classified Silver record counts, so product entities resolve to native
-  product-page evidence, not only creator-content mentions.
+  product-page evidence, not only creator-content mentions. A projection row
+  missing brand or line is residual-only; one native `(anchor, source site,
+  site id or canonical URL)` identity cannot silently bind to conflicting
+  brand/line or URL values.
 - `by_creator` view: (platform namespace, observed public account native id)
   from account-bearing Silver subjects (`platform_public_account` subjects
   and `public_content_object` subjects naming their publishing account)
@@ -238,9 +241,14 @@ does not accept an implicit current/latest policy.
   `classify_silver_vault_record_sources` classifier. Per-platform
   object-level only — no cross-platform identity is unified. Exact observed
   strings preserved; absence of a key/packet/lane means not captured or not
-  indexed, never zero. The scoped read entry point is
+  indexed, never zero. Conflicting aliases for the same
+  `(platform namespace, native id)` are named residuals rather than silently
+  treated as consistent. The scoped read entry point is
   `runners/run_derived_retrieval_lookup.py` (`--creator` / `--mention`),
-  which reads only the generated views and reports generation provenance.
+  which reads only the generated views, requires a complete manifest pair
+  whose recorded view hash matches the stored bytes, reports generation
+  provenance, and matches mentions only by normalized exact brand, exact
+  line, or exact combined brand+line identity.
 - `--prove-rebuildability` regenerates every view from committed material
   under the generation stamps recorded in the existing manifest and
   byte-compares against the stored files; any mismatch or unreadable source
@@ -351,8 +359,12 @@ direction_change_propagation:
     brand/line entity to its own committed product-page capture anchor
     (identity from the view-only Fragrantica projection, labeled routing,
     never Silver authority); and runners/run_derived_retrieval_lookup.py is
-    the scoped read-only lookup entry point over the generated views. The
-    views stay rebuildable, non-authoritative, per-platform object-level, and
+    the scoped read-only lookup entry point over the generated views, with
+    exact normalized identity matching and fail-closed manifest-pair/hash
+    verification. Partial or conflicting native identity rows and conflicting
+    account aliases remain visible residuals rather than fabricated or
+    silently collapsed keys. The views stay rebuildable, non-authoritative,
+    per-platform object-level, and
     prove-rebuildability-covered; absence in a view is never zero; by-key
     discovery stays retrieval authority; the SQL query-lens stays behind the
     scan/query-latency trigger.
```

### Source citations per hunk

- DRL-004 hunk: `forseti-harness/data_lake/derived_retrieval_views.py:198-224`; source basis is the by_creator exact-string and per-platform identity contract at `core_spine_v0_data_lake_consumption_seam_contract_v0.md:233-250`.
- DRL-003 hunks: `forseti-harness/data_lake/derived_retrieval_views.py:321-430` and `:461-485`; source basis is the native product-page routing boundary at `core_spine_v0_data_lake_consumption_seam_contract_v0.md:227-236`.
- DRL-002 hunk: `forseti-harness/runners/run_derived_retrieval_lookup.py:37-61` and `:168-175`; source basis is the manifest-backed generated-read-model obligation at `core_spine_v0_data_lake_consumption_seam_contract_v0.md:200-214`.
- DRL-001 hunk: `forseti-harness/runners/run_derived_retrieval_lookup.py:109-130` and `:154-157`; source basis is the exact brand/line entity routing contract at `core_spine_v0_data_lake_consumption_seam_contract_v0.md:215-236`.
- Regression hunks: `forseti-harness/tests/test_data_lake_indexes_rebuild.py:475-673`; each test directly reproduces its paired finding and fails on the pre-patch implementation.
- Contract hunk: `core_spine_v0_data_lake_consumption_seam_contract_v0.md:229-252` and `:359-371`; it records the implemented behavior without expanding view scope, authority, or engine selection.

## Validation

| Command | Observed result |
| --- | --- |
| Red proof: `python -m pytest -p no:cacheprovider -q tests/test_data_lake_indexes_rebuild.py` after tests, before repairs | exit 1; 4 failed, 12 passed. Failures were the alias conflict, partial/conflicting native identity, substring false-positive, and absent-view exit-code regressions. |
| `python -m pytest -p no:cacheprovider -q tests/test_data_lake_indexes_rebuild.py` | exit 0; `................ [100%]` (16 passed). |
| `python -m pytest -p no:cacheprovider -q tests/contract/test_data_lake_inventory_gate.py tests/contract/test_silver_reader_selection_gate.py tests/contract/test_policy_module_version_pins.py` | exit 0; 26 passed. |
| `pwsh -NoProfile -File .github/scripts/run-doc-gates.ps1` | exit 0; 23/23 documentation gates passed locally. |
| `python -m pytest -p no:cacheprovider -q tests` from `forseti-harness/` | exit 0; suite completed to 100%. Warnings were existing unknown-mark and `datetime.utcnow()` deprecation warnings; no test failed. |
| `git diff --check` | exit 0. |
| `python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/silver_entity_read_layer_delegated_code_review_v0.md` | exit 0 after the complete report write. Because recording this result changes the report, the final rerun result is returned alongside the report. |

Live-lake rebuild, prove-rebuildability, census, and lookup commands were not
run. The commission explicitly forbids reading or writing the live data root;
the author-observed live evidence was checked only for plausibility against the
implementation and contracts.

## Verdict and residual risk

Verdict: `issues_found`.

The bounded patch removes the reproduced misrouting and hidden-conflict
behaviors without adding a query engine, cache, new view, fallback authority, or
off-scope edit. It remains decision input only.

Residual risks:

- Exact mention matching deliberately gives up fuzzy/partial lookup. A caller
  must supply the normalized exact brand, line, or combined identity; adding
  fuzzy search would require a separately governed disambiguation design.
- An account-alias conflict preserves the deterministic first alias and exposes
  all conflicting values as a residual. Secondary contradictory aliases are not
  promoted to accepted lookup keys until upstream identity evidence is
  adjudicated.
- View-byte hash verification detects incomplete or tampered stored pairs, but
  it does not prove the view is current against later lake writes. The manifest
  still surfaces `stale_if`; callers use the existing prove-rebuildability path
  when freshness matters.
- No live-lake evidence was independently rerun in this commission.
- Full-suite warnings remain outside this bounded patch because they are
  unrelated to the reviewed implementation.

## Adjudicator boundary

Every finding, edit, citation, verdict, and residual above is a claim for the
home Chief Architect to adjudicate. Nothing is kept merely because this report
recommends it. The home Chief Architect accepts, modifies, or rejects each
change against the cited authority and implementation intent, reverts rejected
hunks, and retains final veto authority.

Review findings are decision input only; they are not approval, validation,
mandatory remediation, or executor-ready patch authority until separately
accepted or authorized.

```yaml
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL:
  commission: silver_entity_read_layer_repo_delegated_code_review_and_patch
  target_revision: ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f
  reviewer_vendor: OpenAI
  author_vendor: Anthropic
  verdict: issues_found
  finding_ids: [DRL-001, DRL-002, DRL-003, DRL-004]
  working_tree_patch_present: true
  validation_summary: focused_green_contract_green_docs_green_full_suite_green_diff_check_green
  next_authorized_action: home_chief_architect_adjudication
  non_claims:
    - not approval
    - not readiness
    - not acceptance
    - not lifecycle authority
```
