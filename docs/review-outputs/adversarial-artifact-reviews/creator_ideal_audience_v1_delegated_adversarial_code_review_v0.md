# Creator Ideal Audience v1 — Delegated Adversarial Code Review and Bounded Patch (Repo Mode)

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated adversarial code review-and-patch return, repo access mode)
scope: >
  Cross-vendor adversarial code review of the media-neutral creator
  ideal-audience Judgment implementation at origin/main...19263b8, plus the
  bounded delegate-authored patch inside the commissioned 17-file set,
  validation evidence, and residual risk for home Chief Architect adjudication.
use_when:
  - Adjudicating the creator ideal-audience v1 delegated review-and-patch return.
  - Tracing why a bounded working-tree edit exists on codex/creator-ideal-audience-core.
authority_boundary: retrieval_only
```

## 1. Provenance

```yaml
provenance:
  reviewed_by: claude-fable-5
  authored_by: unrecorded (model id not supplied; author vendor OpenAI per commission)
  author_vendor: OpenAI
  delegate_vendor: Anthropic
  de_correlation_bar: cross_vendor_discovery
  commission: docs/prompts/reviews/creator_ideal_audience_v1_repo_delegated_adversarial_code_review_and_patch_prompt_v0.md
  review_method: workflow-code-review under the delegated_code_review_and_patch target kind
  target_worktree: C:/tmp/forseti-creator-ideal-audience-core
  repository: https://github.com/eric-foo/orca
  observed_branch: codex/creator-ideal-audience-core
  observed_head: b716ea57346b4e1e9e5307582cbf0dd61543ca0d
  required_revision: 19263b8595a943d42d9317d99e9bce49e45a92ce
  revision_mode: ancestor
  ancestor_check: git merge-base --is-ancestor 19263b8 HEAD exited 0 (ANCESTOR_OK)
  commits_after_required_revision: b716ea57 (adds this commission prompt only)
  initial_dirty_state: clean (git status --porcelain empty at bind)
  single_checkout: branch checked out only at the target worktree (git worktree list)
  direct_write_capability: proved by creating and removing .delegate_write_probe_claude.tmp inside the target worktree
  git_locks: none observed (no index.lock or HEAD.lock in the worktree gitdir)
  reviewed_diff: origin/main...19263b8595a943d42d9317d99e9bce49e45a92ce (18 files, +2042/-560), read in full
```

## 2. Review Summary

```yaml
review_summary:
  commission: repo-mode delegated adversarial code review and bounded patch of the creator ideal-audience v1 lane
  target: media-neutral creator-audience Judgment core (judgment/schemas/runners/evidence-binding/tests) plus the split method-deck product docs
  authority:
    - forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md (controlling contract)
    - .agents/workflow-overlay/delegated-review-patch.md and review-lanes.md (lane rules)
    - the real diff origin/main...19263b8 and live target sources
  decision_criteria: smallest complete fix for the prior slow TikTok judgment path without weakening evidence ceilings, provenance, registry compatibility, or failure visibility
  verdict: issues_found
  findings_total: 14
  severity_counts: {critical: 0, major: 6, minor: 8}
  patched_in_this_pass: [CIA-F1, CIA-F2, CIA-F3, CIA-F4, CIA-F5, CIA-F7, CIA-F8, CIA-F9, CIA-F10, CIA-F11, CIA-F14]
  report_only: [CIA-F6, CIA-F12, CIA-F13]
  patch_scope_compliance: all edits inside the commissioned 17-file set; dirty set is 12 named targets plus this report
  validation: focused and profile suites green post-patch; doc gates 22/22; full harness suite exit 1 on two contract failures proven pre-existing at the required revision (CIA-F6)
  next_authorized_action: home Chief Architect adjudication of findings, diff, verdict, and residuals
```

## 3. Findings

Commissioned target and purpose for every finding: the creator ideal-audience
v1 implementation diff above, judged for smallest-complete replacement of the
prior TikTok judgment path without weakening evidence ceilings, provenance,
registry compatibility, or failure visibility.

### CIA-F1 — Prompt omits the contract-bound 1-5 representative-evidence cap (major, confidence high) — patched

- reviewed_target: `forseti-harness/judgment/creator_audience.py` (`build_creator_audience_prompt`)
- evidence: pre-patch prompt text stated only "Use only evidence aliases in the compact view. For a missing claim, all evidence-alias arrays must be empty." Nothing states that a non-missing claim needs 1-5 representative aliases plus support, while `CreatorAudienceSemanticClaim.representative_evidence_aliases` enforces `max_length=5` (schemas/creator_audience_models.py) and the compiler rejects non-missing claims without support.
- authority: controlling contract "one to five representative evidence IDs" (creator_audience_triangulation_and_commercial_projection_v0.md:239); the retired v0 prompt stated "1-5 representative evidence IDs" inline (judgment/tiktok_audience_triangulation.py:60-61). Same defect class as the author-acknowledged omitted-axis-list cold-probe failure.
- impact: a cold agent citing six representative aliases produces a schema rejection and a wasted full cold-context run — the exact expensive failure mode this lane just paid for twice.
- minimum_closure_condition: the routine prompt states the representative cap and non-missing support requirement a cold agent must satisfy.
- next_authorized_action: closed by bounded patch (prompt text + regression assertion); home CA adjudicates.
- verification: `test_prompt_embeds_method_and_compact_view_but_not_named_examples` asserts the new instruction; red evidence is mechanical (guard string has zero hits in `git show 19263b8:forseti-harness/judgment/creator_audience.py`), weaker than an executed pre-patch failing run.

### CIA-F2 — Robustness-stamp truth rule dropped from the prompt (major, confidence high) — patched

- reviewed_target: `forseti-harness/judgment/creator_audience.py` (`build_creator_audience_prompt`)
- evidence: the v0 prompt instructed "robustness_stamp null unless a named ablation actually ran" (judgment/tiktok_audience_triangulation.py:64). The new prompt only shows `"robustness_stamp": None` in the JSON shape with no rule; the compiler checks the stamp only for majority/guarantee language and cannot verify that any ablation ran.
- authority: controlling contract Robustness Stamp section: the stamp may be used "only when those ablations were actually run ... Never manufacture a stability claim" (creator_audience_triangulation_and_commercial_projection_v0.md:253-264).
- impact: fail-open route for a cold agent to fabricate a buyer-visible stability receipt; a diff-introduced weakening of an evidence ceiling.
- minimum_closure_condition: the routine prompt carries the stamp rule (null unless a named ablation actually ran) so the only unverifiable truth field is instructed.
- next_authorized_action: closed by bounded patch (prompt text + regression assertion); home CA adjudicates.
- verification: same mechanism as CIA-F1 (string-absence red proof at 19263b8; green assertion post-patch).

### CIA-F3 — Compact view duplicated the full capability manifest into the prompt (major, confidence high) — patched

- reviewed_target: `forseti-harness/judgment/creator_audience.py` (`build_compact_judgment_view`)
- evidence: the view embedded `capability_manifest` with one entry per alias repeating kind, source_item_id, and the internal durable `evidence_id` — all already present or forbidden-to-use. Measured on synthetic bundles with the live module: 336 evidence items -> 150,807-byte prompt of which 51,639 bytes (34.2%) were the embedded manifest; 800 items -> 336,391 bytes with 122,631 bytes (36.5%) manifest. Post-patch the same shapes emit 99,607 and 214,199 bytes (-34.0% / -36.3%).
- authority: commission attack class "the compact prompt must materially reduce context while preserving every evidence text and decision field"; latency and ceremony are named part of correctness; the compiler independently rebuilds the manifest from the bundle, so the embedded copy carried no decision field beyond the per-comment `engagement_salience_eligible` flag already on each evidence row.
- impact: roughly one third of every routine Judgment prompt was redundant bytes, directly aggravating the cold-run latency residual; exposing internal evidence IDs also invites alias/ID confusion that the compiler would reject (another wasted cold run).
- minimum_closure_condition: the routine prompt carries each evidence text and decision field exactly once; internal durable evidence IDs stay out of model context.
- next_authorized_action: closed by bounded patch (view keeps per-comment eligibility flags plus one `engagement_salience_rule`; prompt wording repointed; view_version bumped to v2); home CA adjudicates.
- verification: new assertions (`"content-1" not in prompt`, `"capability_manifest" not in view`) are false pre-patch by construction (the manifest embedded `evidence_id: "content-1"`); measured byte reduction reported above. No executed pre-patch failing test run (weaker evidence).

### CIA-F4 — Legacy v0-response upgrade fabricated method-deck provenance (major, confidence high on mechanism) — patched

- reviewed_target: `forseti-harness/judgment/creator_audience.py` (`_upgrade_legacy_snapshot`)
- evidence: pre-patch, a v0-format response (judged under the old inline TikTok prompt, which never contained the method deck) was upgraded to a v1 snapshot stamped with `method_deck_path = METHOD_DECK_RELATIVE_PATH` and the live deck's sha256. The upgrade path is exercised by every `_response()`-based test in test_tiktok_audience_triangulation.py, so all upgraded snapshots claimed a method context their Judgment never saw.
- authority: contract runtime binding step 2 defines the deck fields as what the Judgment boundary emitted to the model (creator_audience_triangulation_and_commercial_projection_v0.md:108-110); AGENTS.md kernel: report only observed facts.
- impact: false provenance in a durable, registry-joined artifact; downstream consumers cannot distinguish deck-guided judgments from legacy ones.
- minimum_closure_condition: upgraded legacy snapshots carry truthful method provenance distinct from the live deck.
- next_authorized_action: closed by bounded patch (`LEGACY_V0_METHOD_PATH` / `"unrecorded:legacy_v0_response_upgrade"` markers + regression test `test_legacy_v0_upgrade_does_not_claim_current_method_deck`); home CA adjudicates the marker vocabulary.
- verification: pre-patch source at 19263b8 observably stamps `METHOD_DECK_RELATIVE_PATH` (red by construction); post-patch test green.

### CIA-F5 — Instagram runner accepted a fabricated primary raw anchor (major, confidence medium) — patched

- reviewed_target: `forseti-harness/runners/run_instagram_creator_audience_triangulation.py` (`prepare_instagram_subscription_judgment`)
- evidence: `--primary-raw-anchor` was never validated against anything; assembly receipts (and, at submit, Judgment outcomes keyed by the bundle's `raw_anchor`) were written under whatever anchor the caller typed. The shipped test enshrined this: evidence records lived under anchors `R1`/`R2` while receipts were written under the invented anchor `01INSTAGRAMAUDIENCE`.
- authority: commission attack class "anchor mismatches, stale lineage"; `DataLakeRoot.append_record` documents derived records as anchored at `<subtree>/<anchor_shard>/<raw_anchor>/...` (data_lake/root.py:575-580), and the TikTok lane always anchors under the real packet id.
- impact: derived-lake lineage records anchored to a raw anchor that references no admitted evidence; anchor-to-raw traceability silently broken for every Instagram judgment.
- minimum_closure_condition: the primary anchor provably references admitted evidence for the run.
- next_authorized_action: closed by bounded patch (primary anchor must be one of the loaded records' observed anchors; tests updated plus a rejection test). If the home CA intends a different anchoring policy (e.g., an account-level packet), that is an adjudication decision — the pre-patch behavior (any string) was not that policy either.
- verification: red is executed-by-inversion — the pre-patch test passed with the foreign anchor, and the new rejection test's guard string has zero hits at 19263b8; post-patch suite green.

### CIA-F6 — Full harness suite is red at the required revision: two undeclared lake-gate baselines (major, confidence high) — report-only, out of patch scope

- reviewed_target: `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py::test_non_raw_lake_touchpoint_inventory_is_explicit` and `forseti-harness/tests/contract/test_silver_reader_selection_gate.py::test_every_lane_dir_reader_declares_a_selection_posture`
- evidence: both fail with the new Instagram runner as the sole delta — `added={(runners/run_instagram_creator_audience_triangulation.py, append_record): 1, (…, lane_dir): 1, (…, record_path): 2}` and `['runners/run_instagram_creator_audience_triangulation.py']` undeclared. `git show 19263b8:` confirms neither the hardcoded `EXPECTED_NON_RAW_LAKE_TOUCHPOINTS` counter nor `SILVER_READER_SELECTION_POSTURES` in `forseti-harness/data_lake/inventory.py` contains any Instagram-runner entry, while the runner and its calls are tracked at that revision. The delegate patch adds no lake calls (flagged counts equal the pre-existing call sites), so the failures are pre-existing, and the commission's author-observed "full suite -> exit 0" is not reproducible at the reviewed revision. The author regenerated only the generated JSON inventory (which passes its own gate); the two hand-declared baselines were missed.
- impact: CI-visible red on main-bound work; the seam-coverage and reader-posture gates exist precisely to force classification of new lake touchpoints, and the new runner bypassed both.
- minimum_closure_condition: the three touchpoints are classified in the seam-coverage baseline and the runner declares its sibling-selection posture (it reads explicit caller-selected record paths; `lane_dir` is used only for path-shape validation), with both gates green.
- next_authorized_action: home CA closure — both files are outside the commissioned 17-file patch set, so the delegate did not touch them. Not a design-level blocker; two mechanical declarations.

### CIA-F7 — Prompt/validator mismatch on the 'ritual' ban scope (minor, confidence high) — patched

- one-line: prompt said "do not use 'ritual' on the first screen" while `_compile_semantic_response` rejects it in every projection point including briefing_instructions and wrong_hire_boundary — an avoidable blocked-cold-run route; prompt now says "never use 'ritual' anywhere in the buyer-facing projection" (matches the validator and the v0 prompt's stricter wording). Closure: instruction and validator agree. Closed by patch.

### CIA-F8 — Hire-verdict grammar is a hidden contract dependency (minor, confidence medium) — patched

- one-line: the contract mandates `Hire <creator> when <campaign job>.` as the panel's first line (creator_audience_triangulation_and_commercial_projection_v0.md:194) but neither the prompt nor the embedded method deck states it (the grammar line lives in the excluded examples appendix); pre-existing in the v0 prompt too, and no validator checks it. Prompt now states the grammar. Closure: cold context carries the grammar or a validator enforces it. Closed by patch (prompt line).

### CIA-F9 — V1 snapshot dropped v0's non-blank field validator (minor, confidence medium) — patched

- one-line: `CreatorAudienceTriangulationSnapshotV1` accepted blank identity/provenance fields that v0 rejected (v0 `snapshot_text_non_blank`, tiktok_audience_evidence_models.py:127-141); the only model-controlled path is `generated_at`, so a blank timestamp reached the registry silently. Restored as a reject-only validator (no strip — the compiler owns canonical bytes, and a transforming validator would desynchronize `snapshot_id`), plus `test_snapshot_rejects_blank_generated_at`. Closed by patch.

### CIA-F10 — Duplicate evidence_id silently mangled the compact view (minor, confidence medium) — patched

- one-line: two bundle rows with one evidence_id (e.g., a duplicated captured Instagram comment with identical comment_id and text — the IG adapter, unlike TikTok's attention-index uniqueness check, never rejects this) collided in the manifest/by_id join, duplicating one row and double-citing one durable ID; `build_capability_manifest` now fails closed on duplicate evidence_ids at both prompt build and compile, plus `test_manifest_fails_closed_on_duplicate_evidence_ids`. Closed by patch.

### CIA-F11 — Coordinator dead-ended persisted v0 outcomes (minor, confidence medium) — patched

- one-line: `complete_onboarding` validated outcomes with the v1-only model while `materialize.py:677-682` dispatches by schema_version, so a pre-cutover v0 outcome awaiting completion could neither complete nor be resubmitted (identical `record_id` derivation collides with "existing audience Judgment outcome differs"); the coordinator now mirrors the materializer's dispatch, plus `test_complete_onboarding_still_reads_persisted_v0_outcome` (red: pre-patch fails at outcome validation with a pydantic schema_version error; green: reaches the materialized-view check). Existence of stranded pre-cutover state in the real lake is unverified from the repo. Closed by patch.

### CIA-F12 — Method-deck hash is bound at submit time, not prompt time (minor, confidence medium) — report-only

- one-line: the compiled snapshot stamps `load_method_deck()` at submit, while the model saw the deck embedded at prepare; a deck edit between prepare and submit yields a snapshot claiming a deck revision the Judgment never saw. Complete closure needs the prepare-time hash carried through the bundle or outcome and verified at submit, which touches `evidence_binding/tiktok_audience_triangulation.py` (outside the named patch set). minimum_closure_condition: submit verifies the response against the prepare-time deck hash. next_authorized_action: home CA decision (re-commission or accept the narrow race as a named residual).

### CIA-F13 — Missing-relation claims compiled with contradictory labels (minor, confidence low) — report-only

- one-line: the compiler labels relation="missing" claims `modality: fused` / `support_scope: content_only` (judgment/creator_audience.py, the empty-support branch), which nominally overstates support, though relation plus the schema-enforced empty evidence lists are decisive and the labels match the established v0 test convention (test_tiktok_audience_triangulation.py:249-251). minimum_closure_condition: owner decides whether missing claims get dedicated none-valued labels. next_authorized_action: owner decision; left unpatched deliberately.

### CIA-F14 — Mechanical hygiene: missing EOF newlines and heading spacing (minor, confidence high) — patched

- one-line: eight new/modified in-scope files lacked a trailing newline and three docs lacked a blank line before a section heading (an artifact of the doc split/edit); fixed mechanically inside the patch scope. Closed by patch.

## 4. Considered And Defended

- Scratch-bundle tampering at submit — defended: `_verify_bundle_integrity` recomputes the bundle hash over content and requires the persisted assembly receipt to match (run_tiktok_creator_audience_triangulation.py:335-372), and the shipped test exercises the missing-receipt rejection.
- Lake path traversal / copied or renamed Silver envelopes — defended: resolve + root containment + shard-recomputed lane and record-path equality plus `current_deep_capture_record` source verification (run_instagram_creator_audience_triangulation.py:42-76; data_lake/root.py:765-787).
- TikTok engagement elevation silently lost under the shared manifest — defended: TikTok comment rows carry `temporal_alignment` and `comment_attention_record_id` from persisted Silver `_mechanics` (evidence_binding/tiktok_audience_triangulation.py:80-99), and the shared eligibility rule is stricter than v0 (every cited comment, not any).
- Model-controlled route into durable clerical fields — defended: the semantic response schema is strict-extra-forbid with no ID/modality/scope/hash/summary fields; the compiler derives all of them and `snapshot_id` is canonical over content.
- Cross-platform account fusion — defended: per-platform adapters, `platform_scope` Literal on the v1 snapshot, receipt-verified bundle identity, and the legacy upgrade path still enforces tiktok-only scope via the v0 relational checks.
- Private audit-path leakage into the prompt — defended: the compact view omits `source_pointer`, record ids, and cluster/audit fields; asserted by test.
- Prompt-instruction injection from evidence text — partially defended: evidence is JSON-encoded inside a data-labeled section under a data-not-instructions header; instruction-following is not mechanically provable and remains the same residual the v0 prompt carried.
- Duplicate-comment multiplicity loss in the compact view — defended: every duplicate evidence row remains individually present; `exact_duplicate_clusters` is audit-side.
- Arbitrary-JSON legacy Instagram Silver acceptance — defended within its declared boundary: legacy records must sit in the exact lane directory with a matching Reel anchor and are surfaced as `compatibility_residuals` with a count in the prepare result.
- Registry join spoofing of snapshot/outcome pairs — defended: `verify_audience_judgment_outcomes` enforces byte-hash, content, and identity equality between the snapshot document and the embedded outcome snapshot (materialize.py:659-705).
- Mixed-version wrapped snapshot documents — defended: per-item schema_version dispatch falls back to the strict v0 model, which rejects unknown versions.

## 5. Bounded Delegate Patch (unified diff)

Hunk-to-finding map with neutral citations:

- `.agents/skills/creator-audience-triangulation/SKILL.md` — CIA-F14 (EOF newline only).
- `forseti-harness/evidence_binding/instagram_audience_triangulation.py` — CIA-F14 (EOF newline only).
- `forseti-harness/judgment/creator_audience.py` — CIA-F10 (duplicate-evidence_id guard; commission compiler attack class), CIA-F3 (view slimming; measured 34-37% redundant prompt bytes), CIA-F1/F2/F7/F8 (prompt instruction parity with creator_audience_triangulation_and_commercial_projection_v0.md:194,239,253-264 and the retired v0 prompt judgment/tiktok_audience_triangulation.py:60-64), CIA-F4 (truthful legacy method markers; contract runtime binding step 2).
- `forseti-harness/runners/run_instagram_creator_audience_triangulation.py` — CIA-F5 (anchor membership; data_lake/root.py:575-580 anchor semantics), CIA-F14.
- `forseti-harness/runners/run_tiktok_creator_onboarding_coordinator.py` — CIA-F11 (schema_version dispatch mirroring materialize.py:677-682).
- `forseti-harness/schemas/creator_audience_models.py` — CIA-F9 (v0 parity validator, reject-only; tiktok_audience_evidence_models.py:127-141).
- `forseti-harness/tests/unit/test_creator_audience_judgment_v1.py` — regression coverage for CIA-F1/F2/F3/F5/F7/F8/F9/F10; CIA-F14.
- `forseti-harness/tests/unit/test_tiktok_audience_triangulation.py` — regression coverage for CIA-F4/F11.
- `forseti/product/spines/creator_signal/*.md` (four files) — CIA-F14 (EOF newlines; blank line before headings introduced by the doc split).

Trailing whitespace was stripped from the embedded diff lines below (blank
unified-diff context lines render as empty lines); the working tree holds the
exact bytes.

```diff
diff --git a/.agents/skills/creator-audience-triangulation/SKILL.md b/.agents/skills/creator-audience-triangulation/SKILL.md
index bb659725..7c6ec689 100644
--- a/.agents/skills/creator-audience-triangulation/SKILL.md
+++ b/.agents/skills/creator-audience-triangulation/SKILL.md
@@ -84,4 +84,4 @@ confirm no snapshot/registry write, and state whether recapture is required.
 - Negative triggers: comparing profiles, copy edits, comment-like inspection,
   Silver catch-up, or capture debugging.
 - Rollback: restore the prior firing-point source; do not alter user/global or
-  plugin skill sources.
\ No newline at end of file
+  plugin skill sources.
diff --git a/forseti-harness/evidence_binding/instagram_audience_triangulation.py b/forseti-harness/evidence_binding/instagram_audience_triangulation.py
index f56d72ac..e5bac18e 100644
--- a/forseti-harness/evidence_binding/instagram_audience_triangulation.py
+++ b/forseti-harness/evidence_binding/instagram_audience_triangulation.py
@@ -226,4 +226,4 @@ def build_instagram_creator_audience_evidence_bundle(
 __all__ = [
     "EVIDENCE_BUNDLE_SCHEMA_VERSION",
     "build_instagram_creator_audience_evidence_bundle",
-]
\ No newline at end of file
+]
diff --git a/forseti-harness/judgment/creator_audience.py b/forseti-harness/judgment/creator_audience.py
index cb42b996..a5e5511a 100644
--- a/forseti-harness/judgment/creator_audience.py
+++ b/forseti-harness/judgment/creator_audience.py
@@ -61,13 +61,18 @@ def _rows(bundle: Mapping[str, Any]) -> list[tuple[str, Mapping[str, Any]]]:

 def build_capability_manifest(bundle: Mapping[str, Any]) -> dict[str, Any]:
     evidence: dict[str, dict[str, Any]] = {}
+    seen_evidence_ids: set[str] = set()
     for index, (kind, row) in enumerate(
         sorted(_rows(bundle), key=lambda pair: str(pair[1].get("evidence_id"))),
         start=1,
     ):
+        evidence_id = str(row.get("evidence_id"))
+        if evidence_id in seen_evidence_ids:
+            raise ValueError(f"duplicate evidence_id in audience bundle: {evidence_id}")
+        seen_evidence_ids.add(evidence_id)
         alias = f"e{index:04d}"
         evidence[alias] = {
-            "evidence_id": str(row.get("evidence_id")),
+            "evidence_id": evidence_id,
             "source_item_id": str(row.get("video_id") or row.get("source_item_id") or ""),
             "kind": kind,
             "engagement_salience_eligible": bool(
@@ -118,7 +123,7 @@ def build_compact_judgment_view(bundle: Mapping[str, Any]) -> dict[str, Any]:
         evidence.append(compact)
     scope = bundle.get("capture_scope")
     return {
-        "view_version": "creator_audience_compact_judgment_view_v1",
+        "view_version": "creator_audience_compact_judgment_view_v2",
         "identity": {
             "creator_id": bundle.get("creator_id"),
             "profile_subject_id": bundle.get("profile_subject_id"),
@@ -128,7 +133,7 @@ def build_compact_judgment_view(bundle: Mapping[str, Any]) -> dict[str, Any]:
         "evidence_cutoff": bundle.get("evidence_cutoff"),
         "capture_scope": scope if isinstance(scope, Mapping) else {},
         "evidence": evidence,
-        "capability_manifest": manifest,
+        "engagement_salience_rule": manifest["engagement_rule"],
     }


@@ -186,11 +191,16 @@ def build_creator_audience_prompt(bundle: Mapping[str, Any]) -> str:
         "Return only semantic choices: never invent durable IDs, identity fields, "
         "modality, support scope, source-item closure, hashes, summaries, or snapshot "
         "IDs; the compiler derives them. Use only evidence aliases in the compact view. "
-        "For a missing claim, all evidence-alias arrays must be empty. Engagement changes "
-        "salience, not truth; set engagement_salience_relied_on true only when the "
-        "capability manifest permits every cited comment. Never claim audience prevalence, "
-        "demographics, guaranteed conversion, sales, or ROI. Draft commercially forceful "
-        "copy inside the evidence ceiling and do not use 'ritual' on the first screen.\n\n"
+        "Every non-missing claim cites 1-5 representative aliases and lists every "
+        "relied-on alias in all_support_evidence_aliases. For a missing claim, all "
+        "evidence-alias arrays must be empty. Engagement changes salience, not truth; "
+        "set engagement_salience_relied_on true only when every cited comment has "
+        "engagement_salience_eligible true in the compact view. Never claim audience "
+        "prevalence, demographics, guaranteed conversion, sales, or ROI. Write "
+        "hire_verdict as `Hire <creator> when <campaign job>`. Set robustness_stamp to "
+        "null unless a named ablation actually ran against this same evidence. Draft "
+        "commercially forceful copy inside the evidence ceiling and never use 'ritual' "
+        "anywhere in the buyer-facing projection.\n\n"
         f"METHOD_DECK_PATH: {METHOD_DECK_RELATIVE_PATH}\n"
         f"METHOD_DECK_SHA256: {method_hash}\n\n"
         "BEGIN_METHOD_DECK\n"
@@ -428,6 +438,12 @@ def _compile_semantic_response(
     return CreatorAudienceTriangulationSnapshotV1.model_validate(snapshot)


+LEGACY_V0_METHOD_PATH = (
+    "judgment/tiktok_audience_triangulation.py::build_triangulation_prompt"
+)
+LEGACY_V0_METHOD_SHA256 = "unrecorded:legacy_v0_response_upgrade"
+
+
 def _upgrade_legacy_snapshot(
     legacy: Any, bundle: Mapping[str, Any]
 ) -> CreatorAudienceTriangulationSnapshotV1:
@@ -439,13 +455,15 @@ def _upgrade_legacy_snapshot(
             "multi_video": "multi_item",
             "mixed_multi_video": "mixed_multi_item",
         }.get(claim["support_scope"], claim["support_scope"])
-    _, method_hash = load_method_deck()
+    # A v0 response was judged under the legacy inline prompt, never under the
+    # current method deck; stamping the live deck here would fabricate method
+    # provenance on a durable artifact.
     raw.update(
         {
             "schema_version": "creator_audience_triangulation_snapshot_v1",
             "snapshot_id": "",
-            "method_deck_path": METHOD_DECK_RELATIVE_PATH,
-            "method_deck_sha256": method_hash,
+            "method_deck_path": LEGACY_V0_METHOD_PATH,
+            "method_deck_sha256": LEGACY_V0_METHOD_SHA256,
         }
     )
     raw["snapshot_id"] = _snapshot_id(raw)
@@ -476,6 +494,8 @@ def parse_creator_audience_response(


 __all__ = [
+    "LEGACY_V0_METHOD_PATH",
+    "LEGACY_V0_METHOD_SHA256",
     "METHOD_DECK_RELATIVE_PATH",
     "build_capability_manifest",
     "build_compact_judgment_view",
diff --git a/forseti-harness/runners/run_instagram_creator_audience_triangulation.py b/forseti-harness/runners/run_instagram_creator_audience_triangulation.py
index 82d5da2d..4ddbb43f 100644
--- a/forseti-harness/runners/run_instagram_creator_audience_triangulation.py
+++ b/forseti-harness/runners/run_instagram_creator_audience_triangulation.py
@@ -41,7 +41,7 @@ def _load_object(path: Path) -> dict[str, Any]:

 def _load_admitted_silver_record(
     data_root: DataLakeRoot, path: Path, *, lane: str
-) -> dict[str, Any]:
+) -> tuple[dict[str, Any], str]:
     resolved = path.resolve(strict=True)
     try:
         resolved.relative_to(data_root.path.resolve())
@@ -73,7 +73,7 @@ def _load_admitted_silver_record(
             raise ValueError(f"Silver envelope is not current and source-valid: {path}")
     elif record.get("reel_shortcode") != raw_anchor:
         raise ValueError(f"legacy Silver record does not match its Reel anchor: {path}")
-    return record
+    return record, raw_anchor


 def prepare_instagram_subscription_judgment(
@@ -91,18 +91,27 @@ def prepare_instagram_subscription_judgment(
 ) -> dict[str, Any]:
     if bundle_out.resolve() == prompt_out.resolve():
         raise ValueError("bundle_out and prompt_out must be different files")
+    comment_loaded = [
+        _load_admitted_silver_record(data_root, path, lane=AUDIENCE_COMMENTS_LANE)
+        for path in comment_record_paths
+    ]
+    transcript_loaded = [
+        _load_admitted_silver_record(data_root, path, lane=REEL_TRANSCRIPT_LANE)
+        for path in transcript_record_paths
+    ]
+    observed_anchors = {anchor for _, anchor in [*comment_loaded, *transcript_loaded]}
+    if primary_raw_anchor.strip() not in observed_anchors:
+        raise ValueError(
+            "primary_raw_anchor must be the raw anchor of an admitted evidence "
+            f"record (observed anchors: {sorted(observed_anchors)!r}): "
+            f"{primary_raw_anchor!r}"
+        )
     bundle = build_instagram_creator_audience_evidence_bundle(
         creator_id=creator_id,
         profile_subject_id=profile_subject_id,
         primary_raw_anchor=primary_raw_anchor,
-        comment_records=[
-            _load_admitted_silver_record(data_root, path, lane=AUDIENCE_COMMENTS_LANE)
-            for path in comment_record_paths
-        ],
-        transcript_records=[
-            _load_admitted_silver_record(data_root, path, lane=REEL_TRANSCRIPT_LANE)
-            for path in transcript_record_paths
-        ],
+        comment_records=[record for record, _ in comment_loaded],
+        transcript_records=[record for record, _ in transcript_loaded],
         question=question,
         evidence_cutoff=evidence_cutoff,
     )
@@ -212,4 +221,4 @@ def main(argv: list[str] | None = None) -> int:


 if __name__ == "__main__":
-    raise SystemExit(main())
\ No newline at end of file
+    raise SystemExit(main())
diff --git a/forseti-harness/runners/run_tiktok_creator_onboarding_coordinator.py b/forseti-harness/runners/run_tiktok_creator_onboarding_coordinator.py
index d933b3c8..7fdba812 100644
--- a/forseti-harness/runners/run_tiktok_creator_onboarding_coordinator.py
+++ b/forseti-harness/runners/run_tiktok_creator_onboarding_coordinator.py
@@ -24,6 +24,7 @@ from runners.run_tiktok_creator_audience_triangulation import (
 )
 from runners.run_tiktok_grid_observation_producer import run_tiktok_grid_observations
 from schemas.creator_audience_models import CreatorAudienceJudgmentOutcomeV1
+from schemas.tiktok_audience_evidence_models import CreatorAudienceJudgmentOutcome


 _ALLOWED_SILVER_STATUSES = {"derived", "already_current"}
@@ -119,7 +120,13 @@ def complete_onboarding(
 ) -> dict[str, Any]:
     """Materialize and verify a candidate before atomically publishing it."""

-    outcome = CreatorAudienceJudgmentOutcomeV1.model_validate(load_json(outcome_path))
+    raw_outcome = load_json(outcome_path)
+    outcome_model = (
+        CreatorAudienceJudgmentOutcomeV1
+        if raw_outcome.get("schema_version") == "creator_audience_judgment_outcome_v1"
+        else CreatorAudienceJudgmentOutcome
+    )
+    outcome = outcome_model.model_validate(raw_outcome)
     output_path.parent.mkdir(parents=True, exist_ok=True)
     previous_output = output_path.read_bytes() if output_path.exists() else None
     with tempfile.NamedTemporaryFile(
diff --git a/forseti-harness/schemas/creator_audience_models.py b/forseti-harness/schemas/creator_audience_models.py
index 084a6f65..0bf72cb5 100644
--- a/forseti-harness/schemas/creator_audience_models.py
+++ b/forseti-harness/schemas/creator_audience_models.py
@@ -156,6 +156,26 @@ class CreatorAudienceTriangulationSnapshotV1(StrictModel):
     non_claims: list[str]
     actual_audience_demographics: Literal["not_estimated"] = "not_estimated"

+    @field_validator(
+        "snapshot_id",
+        "profile_subject_id",
+        "platform_account_id",
+        "creator_id",
+        "generated_at",
+        "evidence_cutoff",
+        "input_bundle_id",
+        "input_bundle_hash",
+        "method_deck_path",
+        "method_deck_sha256",
+    )
+    @classmethod
+    def snapshot_text_non_blank(cls, value: str) -> str:
+        # Reject-only (no strip): the compiler owns canonical bytes, and a
+        # transforming validator would desynchronize snapshot_id from content.
+        if not value.strip():
+            raise ValueError("snapshot field must be non-blank")
+        return value
+

 class CreatorAudienceJudgmentOutcomeV1(StrictModel):
     schema_version: Literal["creator_audience_judgment_outcome_v1"]
diff --git a/forseti-harness/tests/unit/test_creator_audience_judgment_v1.py b/forseti-harness/tests/unit/test_creator_audience_judgment_v1.py
index 69218241..3f3fe81d 100644
--- a/forseti-harness/tests/unit/test_creator_audience_judgment_v1.py
+++ b/forseti-harness/tests/unit/test_creator_audience_judgment_v1.py
@@ -4,6 +4,7 @@ import json
 from pathlib import Path

 import pytest
+from pydantic import ValidationError

 from data_lake.root import DataLakeRoot
 from evidence_binding.instagram_audience_triangulation import (
@@ -135,9 +136,17 @@ def test_prompt_embeds_method_and_compact_view_but_not_named_examples() -> None:
     assert "METHOD_DECK_SHA256: sha256:" in prompt
     assert "category_knowledge|purchase_decision_stage|price_value_posture" in prompt
     assert "one allowed axis" not in prompt
+    assert "1-5 representative aliases" in prompt
+    assert "robustness_stamp to null unless a named ablation" in prompt
+    assert "Hire <creator> when <campaign job>" in prompt
+    assert "anywhere in the buyer-facing projection" in prompt
     assert "Hire Funmi" not in prompt
     assert "Hire Noel" not in prompt
     assert "/private/audit/path/1" not in prompt
+    # Durable evidence IDs stay out of the model context: aliases only.
+    assert "content-1" not in prompt
+    assert "comment-1" not in prompt
+    assert "capability_manifest" not in view
     assert len(view["evidence"]) == 3
     assert {row["text"] for row in view["evidence"]} == {
         row["text"]
@@ -146,6 +155,24 @@ def test_prompt_embeds_method_and_compact_view_but_not_named_examples() -> None:
     }


+def test_manifest_fails_closed_on_duplicate_evidence_ids() -> None:
+    bundle = _bundle()
+    bundle["comment_evidence"] = [
+        *bundle["comment_evidence"],
+        dict(bundle["comment_evidence"][0]),
+    ]
+    with pytest.raises(ValueError, match="duplicate evidence_id"):
+        build_capability_manifest(bundle)
+
+
+def test_snapshot_rejects_blank_generated_at() -> None:
+    bundle = _bundle()
+    response = _semantic_response(bundle)
+    response["generated_at"] = "   "
+    with pytest.raises(ValidationError, match="non-blank"):
+        parse_creator_audience_response(json.dumps(response), bundle)
+
+
 def test_compiler_derives_clerical_fields_and_source_item_closure() -> None:
     bundle = _bundle()
     snapshot = parse_creator_audience_response(
@@ -267,7 +294,7 @@ def test_instagram_prepare_writes_prompt_bundle_and_assembly_receipt(tmp_path: P
         data_root=data_root,
         creator_id="instagram:@alpha",
         profile_subject_id="platform_account:instagram:alpha",
-        primary_raw_anchor="01INSTAGRAMAUDIENCE",
+        primary_raw_anchor="R1",
         comment_record_paths=comment_paths,
         transcript_record_paths=transcript_paths,
         question="Who should hire Alpha?",
@@ -282,12 +309,26 @@ def test_instagram_prepare_writes_prompt_bundle_and_assembly_receipt(tmp_path: P
     assert "BEGIN_METHOD_DECK" in prompt_path.read_text(encoding="utf-8")
     receipt = data_root.record_path(
         subtree="derived",
-        raw_anchor="01INSTAGRAMAUDIENCE",
+        raw_anchor="R1",
         lane="creator_audience_evidence_assembly_receipt",
         record_id=result["assembly_receipt_record_id"],
     )
     assert receipt.is_file()

+    with pytest.raises(ValueError, match="primary_raw_anchor must be the raw anchor"):
+        prepare_instagram_subscription_judgment(
+            data_root=data_root,
+            creator_id="instagram:@alpha",
+            profile_subject_id="platform_account:instagram:alpha",
+            primary_raw_anchor="01INSTAGRAMAUDIENCE",
+            comment_record_paths=comment_paths,
+            transcript_record_paths=transcript_paths,
+            question="Who should hire Alpha?",
+            evidence_cutoff="2026-07-16T00:00:00Z",
+            bundle_out=tmp_path / "foreign.bundle.json",
+            prompt_out=tmp_path / "foreign.prompt.txt",
+        )
+

 def test_instagram_prepare_rejects_records_outside_silver_lanes(tmp_path: Path) -> None:
     comments, transcripts = _instagram_records()
@@ -308,4 +349,4 @@ def test_instagram_prepare_rejects_records_outside_silver_lanes(tmp_path: Path)
             evidence_cutoff="2026-07-16T00:00:00Z",
             bundle_out=tmp_path / "bundle.json",
             prompt_out=tmp_path / "prompt.txt",
-        )
\ No newline at end of file
+        )
diff --git a/forseti-harness/tests/unit/test_tiktok_audience_triangulation.py b/forseti-harness/tests/unit/test_tiktok_audience_triangulation.py
index f5798f5e..13d30008 100644
--- a/forseti-harness/tests/unit/test_tiktok_audience_triangulation.py
+++ b/forseti-harness/tests/unit/test_tiktok_audience_triangulation.py
@@ -18,6 +18,12 @@ from evidence_binding.tiktok_audience_triangulation import (
     build_assembly_receipt,
     build_creator_audience_evidence_bundle,
 )
+from judgment.creator_audience import (
+    LEGACY_V0_METHOD_PATH,
+    LEGACY_V0_METHOD_SHA256,
+    METHOD_DECK_RELATIVE_PATH,
+    parse_creator_audience_response,
+)
 from judgment.tiktok_audience_triangulation import (
     TriangulationValidationError,
     build_triangulation_prompt,
@@ -734,3 +740,80 @@ def test_validator_rejects_source_video_ids_that_do_not_close_over_support() ->

     with pytest.raises(TriangulationValidationError, match="do not close over support"):
         validate_triangulation_snapshot(tampered, bundle)
+
+
+def test_legacy_v0_upgrade_does_not_claim_current_method_deck() -> None:
+    bundle = _bundle()
+    snapshot = parse_creator_audience_response(json.dumps(_response(bundle)), bundle)
+
+    assert snapshot.schema_version == "creator_audience_triangulation_snapshot_v1"
+    assert snapshot.method_deck_path == LEGACY_V0_METHOD_PATH
+    assert snapshot.method_deck_sha256 == LEGACY_V0_METHOD_SHA256
+    assert snapshot.method_deck_path != METHOD_DECK_RELATIVE_PATH
+
+
+def _legacy_v0_outcome(tmp_path: Path, bundle: dict) -> tuple[Path, Path]:
+    """Hand-build a persisted pre-cutover v0 Judgment outcome document."""
+
+    response_bytes = json.dumps(_response(bundle)).encode("utf-8")
+    snapshot = parse_triangulation_response(response_bytes.decode("utf-8"), bundle)
+    snapshot_document = snapshot.model_dump(mode="json")
+    snapshot_text = (
+        json.dumps(snapshot_document, ensure_ascii=False, indent=2, sort_keys=True)
+        + "\n"
+    )
+    outcome = {
+        "schema_version": "creator_audience_judgment_outcome_v0",
+        "record_id": "cajo_" + "0" * 20,
+        "raw_anchor": bundle["raw_anchor"],
+        "creator_id": bundle["creator_id"],
+        "profile_subject_id": bundle["profile_subject_id"],
+        "bundle_id": bundle["bundle_id"],
+        "bundle_hash": bundle["bundle_hash"],
+        "status": "validated",
+        "response_sha256": f"sha256:{hashlib.sha256(response_bytes).hexdigest()}",
+        "response_size_bytes": len(response_bytes),
+        "response_bytes_b64": base64.b64encode(response_bytes).decode("ascii"),
+        "validation_errors": [],
+        "snapshot_id_or_none": snapshot_document["snapshot_id"],
+        "snapshot_sha256_or_none": (
+            f"sha256:{hashlib.sha256(snapshot_text.encode('utf-8')).hexdigest()}"
+        ),
+        "snapshot_or_none": snapshot_document,
+        "model_api_calls": 0,
+    }
+    outcome_path = tmp_path / "outcome_v0.json"
+    outcome_path.write_text(
+        json.dumps(outcome, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
+        encoding="utf-8",
+    )
+    snapshot_path = tmp_path / "snapshot_v0.json"
+    snapshot_path.write_text(snapshot_text, encoding="utf-8")
+    return snapshot_path, outcome_path
+
+
+def test_complete_onboarding_still_reads_persisted_v0_outcome(
+    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
+) -> None:
+    snapshot_path, outcome_path = _legacy_v0_outcome(tmp_path, _bundle())
+    output_path = tmp_path / "creator_profile_current.json"
+
+    def fake_materialize(argv: list[str]) -> int:
+        candidate = Path(argv[argv.index("--output") + 1])
+        candidate.write_text('{"creator_profile_current_view":{}}', encoding="utf-8")
+        return 0
+
+    monkeypatch.setattr(onboarding_coordinator, "materialize_main", fake_materialize)
+    # Reaching the materialized-view check proves the v0 outcome document was
+    # accepted; before the version dispatch this failed at outcome validation.
+    with pytest.raises(ValueError, match="no profiles list"):
+        onboarding_coordinator.complete_onboarding(
+            snapshot_path=snapshot_path,
+            outcome_path=outcome_path,
+            output_path=output_path,
+            account_ledger_path=tmp_path / "ledger.json",
+            creator_registry_index_path=tmp_path / "registry.json",
+            metric_seed_paths=(),
+            generated_at_utc=None,
+            preflight_receipt_path=None,
+        )
diff --git a/forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md b/forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md
index c1f29f13..9d47bfbb 100644
--- a/forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md
+++ b/forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md
@@ -128,6 +128,7 @@ inference context. Both content/transcript and captured comments are mandatory;
 missing either ends as `INCOMPLETE_AUDIENCE_EVIDENCE` without a partial snapshot.
 On-demand refresh reuses existing complete evidence and does not recapture by
 default.
+
 ## Evidence And Inference Rules

 - Use all admissible captured top-level comments from the selected videos after
@@ -304,4 +305,4 @@ direction_change_propagation:
     rg -n -i "creator_commercial_projection_calibration_deck|TikTok onboarding|source_video_ids|snapshot_v0" forseti/product/spines/creator_signal .agents/skills/creator-audience-triangulation forseti-harness
   stale_language_search_result: "Executed 2026-07-16; live routes use the v1 shared core and renamed method deck, while v0/source_video_ids remain only in compatibility code and historical tests."
   non_claims: [not validation, not readiness, not buyer proof, not cross-platform audience fusion]
-```
\ No newline at end of file
+```
diff --git a/forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md b/forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md
index 9ed2a1ff..f00ecb23 100644
--- a/forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md
+++ b/forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md
@@ -17,4 +17,4 @@ stale_if:
 This filename is retained only for compatibility. Routine Judgment must open
 `creator_ideal_audience_distillation_deck_v0.md`. Named examples live separately
 in `creator_ideal_audience_calibration_examples_v0.md` and are not routine model
-context.
\ No newline at end of file
+context.
diff --git a/forseti/product/spines/creator_signal/creator_ideal_audience_calibration_examples_v0.md b/forseti/product/spines/creator_signal/creator_ideal_audience_calibration_examples_v0.md
index a1b44b6d..8b1ae67b 100644
--- a/forseti/product/spines/creator_signal/creator_ideal_audience_calibration_examples_v0.md
+++ b/forseti/product/spines/creator_signal/creator_ideal_audience_calibration_examples_v0.md
@@ -23,6 +23,7 @@ stale_if:
 `OWNER_ACCEPTED_CALIBRATION_APPENDIX_V0` — optional examples companion. Routine
 Judgment prompts must not load this file. A named example is contaminated for a
 cold test unless a leave-one-example-out source is recorded.
+
 ## Calibration Patterns, Not Creator Buckets

 The four patterns below show the required specificity and commercial force.
@@ -153,4 +154,4 @@ direction_change_propagation:
     rg -n "Accepted first-screen calibration|Good hiring line" forseti/product/spines/creator_signal
   stale_language_search_result: "Executed 2026-07-16; accepted named-example phrases are confined to this appendix."
   non_claims: [not validation, not readiness, not buyer proof]
-```
\ No newline at end of file
+```
diff --git a/forseti/product/spines/creator_signal/creator_ideal_audience_distillation_deck_v0.md b/forseti/product/spines/creator_signal/creator_ideal_audience_distillation_deck_v0.md
index ce81839c..d25905e3 100644
--- a/forseti/product/spines/creator_signal/creator_ideal_audience_distillation_deck_v0.md
+++ b/forseti/product/spines/creator_signal/creator_ideal_audience_distillation_deck_v0.md
@@ -138,6 +138,7 @@ Routine Judgment does not load named creator examples. When a human reviewer or
 explicit calibration exercise needs accepted examples, open
 `creator_ideal_audience_calibration_examples_v0.md`. Those examples calibrate
 force and specificity; they are never evidence for another creator.
+
 ## Acceptance Gates

 A commercial panel is not ready unless all of these pass:
@@ -253,4 +254,4 @@ direction_change_propagation:
     rg -n "creator_commercial_projection_calibration_deck|creator_ideal_audience_distillation_deck|creator_ideal_audience_calibration_examples" forseti/product/spines/creator_signal .agents/skills docs/workflows/forseti_repo_map_v0.md
   stale_language_search_result: "Executed 2026-07-16; routine routes resolve the method deck and named creator examples occur only in the calibration appendix."
   non_claims: [not validation, not readiness, not buyer proof, not runtime or model reliability]
-```
\ No newline at end of file
+```
```

## 6. Validation Commands And Observed Results

All commands ran in `C:/tmp/forseti-creator-ideal-audience-core` with `python` on Windows/PowerShell.

1. Pre-patch baseline — `python -m pytest -p no:cacheprovider -q forseti-harness/tests/unit/test_creator_audience_judgment_v1.py forseti-harness/tests/unit/test_tiktok_audience_triangulation.py` -> 28 passed, exit 0 (matches the author-observed baseline).
2. Post-patch focused — same command -> 32 passed (28 baseline + 4 new regression tests), exit 0.
3. `python -m pytest -p no:cacheprovider -q forseti-harness/tests/unit/test_creator_profile_current_static_view.py forseti-harness/tests/unit/test_creator_profile_materialize_preflight.py forseti-harness/tests/unit/test_schema_validation.py` -> 32 passed, exit 0.
4. `python -m pytest -p no:cacheprovider -q forseti-harness/tests/contract/test_data_lake_inventory_gate.py` -> 15 passed, exit 0.
5. `pwsh -NoProfile -File .github/scripts/run-doc-gates.ps1` -> 22/22 doc gates passed, exit 0.
6. `python -m pytest -p no:cacheprovider -q forseti-harness/tests` -> exit 1, run twice post-patch with the same result: exactly two failures, `test_capture_runner_lake_seam_coverage.py::test_non_raw_lake_touchpoint_inventory_is_explicit` and `test_silver_reader_selection_gate.py::test_every_lane_dir_reader_declares_a_selection_posture` (CIA-F6, proven pre-existing at 19263b8 via `git show` of both baselines; the total passed count was not captured from the tail). The operator, mid-commission, directed proceeding despite the known-red full suite; the observed result stands as reported. No other test failed.
7. `git diff --check` -> exit 0 (CRLF-normalization warnings only, from the repo's autocrlf checkout).
8. `git status --porcelain` -> 12 modified files, all inside the commissioned 17-file patch set; this report is the separately authorized 13th write.
9. Red-proof for new guards (weaker than executed red runs): `git show 19263b8:<file>` piped through pattern search returned zero hits for every new guard string (prompt constraints, `LEGACY_V0_METHOD`, `duplicate evidence_id`, `snapshot_text_non_blank` in the v1 model, `primary_raw_anchor must be the raw anchor`, coordinator `outcome_model`), and prompt-size measurements on identical synthetic bundles were taken pre-patch (150,807 B / 336,391 B) and post-patch (99,607 B / 214,199 B).

Not run: no live cold subscription Judgment was executed (no data-root or cold-context authority in this commission), so end-to-end cold success remains unclaimed, as in the commission.

## 7. Verdict And Residual Risk

```yaml
verdict: issues_found
basis: >
  The lane's core promises hold under attack — deterministic compiler ownership
  of clerical fields, fail-closed engagement salience, admitted-Silver-only
  Instagram intake, v0 readability with v1 writes, and example-free routine
  prompts — but the routine prompt shipped with contract-relevant instruction
  gaps and one-third redundant bytes, the legacy upgrade fabricated method
  provenance, Instagram lineage anchoring was unvalidated, and the broad
  contract suite is red at the reviewed revision. Eleven findings were closed
  by bounded in-scope patches; three route to the home CA.
residual_risk:
  - cold_use_latency: >
      Two corrected cold-agent retries produced no output within the bounded
      wait before this commission. Observed repo evidence: input burden was
      real and is now materially reduced (CIA-F3, -34% to -36% at realistic
      scale, on top of the author's 192,978 -> 90,071 byte reduction); output
      burden fell versus v0 by design (short aliases, no clerical copying);
      two instruction/validator mismatches (CIA-F1, CIA-F7) cause blocked
      retries but produce output, not silence. Silence within a bounded wait
      is therefore most consistent with execution/context-length latency, but
      the repo contains no evidence distinguishing host stall from model
      stall: the cause remains undetermined. Measuring a rerun with the
      slimmed prompt is the cheapest discriminator.
  - full_suite_red: two pre-existing contract-gate failures (CIA-F6) block any clean-CI claim until the out-of-scope baselines are declared.
  - method_deck_race: narrow prepare-to-submit deck-edit window (CIA-F12) accepted as a named residual unless the home CA re-commissions the bundle-level binding.
  - injection_surface: evidence-text instruction injection remains only prompt-mitigated, unchanged from v0.
  - unverified_lake_state: whether any pre-cutover v0 outcome is actually stranded awaiting completion (CIA-F11) was not observable from the repo.
non_claims: this report asserts no PASS, readiness, approval, deployment, or cold-run success.
```

## 8. Adjudicator Boundary

```yaml
review_use_boundary: >
  Findings, the bounded diff, the verdict, and the residuals above are claims
  and decision input for the home Chief Architect; they are not approval, not
  validation, not mandatory remediation, and not executor-ready patch
  authority. Nothing in this report is kept merely because it recommends
  itself: the home CA adjudicates each finding and each hunk, may veto any
  change judged net-negative, closes self-closable accepted issues during
  adjudication, and routes design-level blockers through
  NEEDS_ARCHITECTURE_PASS. Lifecycle actions (commit, push, PR, merge,
  cleanup) remain home-CA authority; the delegate performed working-tree edits
  and this report write only.
```
## 9. Home CA Adjudication

### Disposition

- Accepted and retained: CIA-F1 through CIA-F12, plus CIA-F14.
- Rejected: CIA-F13. The existing explicit `relation=missing` plus empty
  evidence representation already preserves the consumer's decision. Adding
  none-valued modality or support-scope enum variants would enlarge durable
  schema and compatibility surface without adding decision value.
- The delegate's historical verdict remains `issues_found`; home-CA closure is
  `closed` because every finding is now accepted-and-closed or explicitly
  rejected with rationale.

### CA-added closure: CIA-F6

The two hand-maintained Data Lake contracts now declare the Instagram runner:

- `EXPECTED_NON_RAW_LAKE_TOUCHPOINTS` records one `append_record`, one
  `lane_dir`, and two `record_path` calls.
- `SILVER_READER_SELECTION_POSTURES` declares
  `local:prepare_instagram_subscription_judgment` as the selection boundary.
  The caller supplies explicit admitted comment/transcript record paths; the
  runner verifies root containment, requested lane, canonical record path,
  raw-anchor identity, and current source validity. `lane_dir` is used only for
  path-shape validation and never to choose an arbitrary sibling.

### CA-added closure: CIA-F12

The prepare-time method revision is now part of both TikTok and Instagram
bundle identity:

- both bundle builders require nonblank `method_deck_path` and
  `method_deck_sha256` fields and include them before computing `bundle_hash`;
- both preparation runners load the method deck once and reuse that exact
  text/path/hash for bundle construction and prompt construction;
- prompt construction validates the bundle binding and rejects method text
  whose SHA-256 differs;
- semantic-response compilation reads the bundle binding and does not reload
  the method deck at submit time;
- the truthful CIA-F4 legacy-v0 upgrade markers remain unchanged.

Focused regressions prove submit-time compilation does not reload the method,
prompt construction rejects mismatched method text, and normal TikTok and
Instagram bundle construction carries the binding.

### Observed validation

All commands ran in `C:/tmp/forseti-creator-ideal-audience-core` against the
adjudicated dirty worktree:

1. Focused creator-audience suites: 35 passed, exit 0.
2. Profile/static-view/materialization/schema suites: 32 passed, exit 0.
3. Data Lake inventory, touchpoint, and reader-selection contract suites: 41
   passed, exit 0; both former CIA-F6 failures are closed.
4. Repository doc gates: 22/22 passed, exit 0.
5. Full `forseti-harness/tests` suite: exit 0.
6. `git diff --check`: exit 0; checkout EOL conversion warnings remain
   informational.

The strict review-output provenance check passed after this appended section was written (exit 0).
The Batch 0 tracker then validated the new receipt with `completed_count: 9`, `errors: []`, `notification_eligible: false`,
`threshold: 10`, and `valid: true` (exit 0).

### Residuals and not-run checks

- The delegate's cold-use latency residual remains unmeasured by this review
  closeout. No additional cold Judgment was commissioned here; the production
  AK onboarding after merge is the next real use of the slimmed path.
- Evidence-text instruction injection remains prompt-mitigated, unchanged from
  the reviewed design.
- No live or production creator judgment was executed during adjudication.
- No extra independent review was required: the current review-routing gate is
  satisfied by this delegated report. The conditional cold-dogfood gate is
  `/fused`-only and does not apply to this continuation.

### Landing disposition

`PROCEED_TO_LANDING_PENDING_GREEN_REQUIRED_CHECKS`: stage only this work unit,
commit and push `codex/creator-ideal-audience-core`, mark PR #995 ready as
appropriate, and merge only after required CI is green and the protected-action
guard permits it. This disposition is not a claim that push, CI, or merge has
already occurred.
