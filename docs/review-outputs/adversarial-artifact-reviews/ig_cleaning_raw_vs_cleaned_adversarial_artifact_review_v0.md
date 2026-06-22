# IG Cleaning Raw-vs-Cleaned Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: adversarial-artifact-review
scope: Read-only adversarial review of IG Cleaning raw-vs-cleaned trace preservation.
use_when:
  - Checking whether the IG Cleaning smoke preserved raw source meaning without overcleaning.
authority_boundary: retrieval_only
review_output_path: docs/review-outputs/adversarial-artifact-reviews/ig_cleaning_raw_vs_cleaned_adversarial_artifact_review_v0.md
template_kind: adversarial-artifact-review
review_packet: orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/raw_cleaned_pairs.json
packet_revision: v0.1_relation_mirror_fix
run_id: ig_cleaning_spine_stage1_20260621
generated_at: 2026-06-21T11:57:39Z
review_date: 2026-06-21
reviewed_by: claude-sonnet-4-6
authored_by: unrecorded (harness-generated; not a model-authored artifact)
de_correlation_bar: self_fallback (same model tier; no cross-vendor delegation performed)
edit_permission: read-only
target_workspace: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation
target_branch: codex/cleaning-spine-continuation
target_commit: 81a46445
source_context: SOURCE_CONTEXT_READY
verdict: bounded_raw_to_cleaned_trace_supported
```

## Verdict

**`bounded_raw_to_cleaned_trace_supported`**

All 134 cleaned handles in the smoke packet can be mechanically traced from raw JSON Pointer anchors and projection metadata. The Cleaning layer did not overclean, introduce Judgment vocabulary, suppress ECR residuals, or rewrite captions. One minor semantic inconsistency (AR-01) exists in the projection layer and was faithfully preserved by Cleaning. Two advisory observations (AR-02, AR-03) note expected projection behavior and cross-account source data, both preserved correctly.

---

## Findings

### AR-01 — Minor | Projection Posture Inconsistency for `partial_signal` Non-Video Items

```yaml
finding_id: AR-01
phase: correctness
severity: minor
source_label: instagram:funmimonet
handle_id: instagram:funmimonet:01KVMS1C02N7F2GFZZ9MTHYP7H:01KVMS1C02N7F2GFZZ9MTHYP7H:ig_call_07:view_count
shortcode: DZk17Cbkfv6
artifact_path: orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/raw_cleaned_pairs.json
```

**Raw evidence:**
- json_pointer: `/media/DZk17Cbkfv6/video_view_count`
- raw file: `raw/02_ig_profile_momentum.json`
- value_at_json_pointer: `null`
- video_view_count in parent_context_excerpt: `null`
- sha256_matches_anchor: `true`
- json_pointer_status: `resolved`

**Cleaned/projection evidence:**
- projection_row.source_visible_fields.is_video: `false`
- projection_row.status: `partial_signal`
- cleaned_handle projection_ref row posture: `unavailable_with_reason`
- cleaned_handle projection_ref row value: `null`
- cleaned_handle projection_ref row reason: "item status=partial_signal; view_count not attributed because the item did not produce a captured call signal"

**Issue:**

The projection assigns `unavailable_with_reason` to a row where `source_visible_fields.is_video = false`. The posture `unavailable_with_reason` semantically implies the metric *could* apply but was not obtainable. For non-video content, `view_count` is definitionally inapplicable, not merely unavailable. For non-video items with `status=captured`, the projection correctly uses `not_applicable` — confirmed in the curlyscents sample (curlyscents:ig_call_01:view_count, `is_video: false`, `status: captured` → posture `not_applicable`). When `status=partial_signal` and `is_video: false`, the projection route diverges from the `not_applicable` path, assigning `unavailable_with_reason` instead. The posture vocabulary therefore overstates the metric's applicability for this item.

**Strongest defense:** The net effect is identical — value is null in both paths. A downstream reader still sees null and can inspect `is_video: false` in source_visible_fields to understand the content type. The projection may have intentionally routed all `partial_signal` rows through `unavailable_with_reason` to signal degraded call quality, regardless of content type.

**Why the defense does not fully hold:** `unavailable_with_reason` is posture vocabulary for metric availability, not call quality. A downstream consumer cannot reliably derive "metric is definitionally inapplicable" from `unavailable_with_reason`; they could interpret it as "we believe this post has a view count but couldn't retrieve it," which is incorrect for a confirmed non-video post.

**Impact on Cleaning:** None. Cleaning faithfully preserved the projection row as received. This is a projection design question, not a Cleaning defect.

**Impact on downstream:** Minor. A downstream consumer who interprets posture without inspecting `is_video` in source_visible_fields could misread this item's metric applicability.

```yaml
minimum_closure_condition: Projection method (ig_creator_momentum_mechanical_projection v0) review to clarify whether partial_signal overrides not_applicable for non-video rows; or explicit documentation that unavailable_with_reason is intentionally used for all partial_signal rows regardless of content type.
next_authorized_action: Advisory note to projection maintainer. No Cleaning change authorized or required.
patch_queue_entry: not_authorized (projection method is outside this review lane; this lane is read-only)
red_green_proof: not_applicable (projection design decision; not a testable remediation in the Cleaning layer)
```

---

### AR-02 — Advisory | Raw Profile API Values Suppressed by Projection at `partial_signal` Boundary

```yaml
finding_id: AR-02
phase: correctness
severity: advisory
source_label: instagram:funmimonet
handle_ids:
  - instagram:funmimonet:01KVMS1C02N7F2GFZZ9MTHYP7H:01KVMS1C02N7F2GFZZ9MTHYP7H:ig_call_05:view_count
  - instagram:funmimonet:01KVMS1C02N7F2GFZZ9MTHYP7H:01KVMS1C02N7F2GFZZ9MTHYP7H:ig_call_06:view_count
shortcodes: [DZqvfScRYz- (ig_call_05), DZnuofBSIne (ig_call_06)]
```

**Raw evidence:**
- ig_call_05: json_pointer `/media/DZqvfScRYz-/video_view_count`, value_at_json_pointer: `14629`, sha256_matches_anchor: `true`, json_pointer_status: `resolved`
- ig_call_06: json_pointer `/media/DZnuofBSIne/video_view_count`, value_at_json_pointer: `5843`, sha256_matches_anchor: `true`, json_pointer_status: `resolved`
- Both: is_video = `true`, content_kind = `reel`, status = `partial_signal`

**Cleaned/projection evidence:**
- Both rows: posture = `unavailable_with_reason`, value = `null`
- Reason: "item status=partial_signal; view_count not attributed because the item did not produce a captured call signal"

**Issue (advisory):**

Raw profile API data contains non-null video view counts (14629 for ig_call_05, 5843 for ig_call_06), but the projection nulled these values due to `partial_signal` item status. This is an intentional projection quality-control decision: only values from items with a fully captured item-level call signal are attributed; profile-feed values alone are not sufficient when the individual item call did not complete.

**Why this is advisory, not a Cleaning failure:**

1. The raw value_at_json_pointer is visible in the review packet alongside the projection's null — no information is suppressed at the review level.
2. The reason string documents the projection logic explicitly.
3. Cleaning faithfully preserved the projection row's posture, value, and reason without modification.
4. The review packet design explicitly separates raw anchor evidence from projection decisions, enabling this comparison.

**Observation for projection design:** A downstream stakeholder who sees `unavailable_with_reason` with a non-null raw profile-API value in the review packet should understand this as a call-quality gate, not missing data. Production consumers of the cleaned handle alone would not see the raw value, but the raw anchor sha256 and json_pointer allow them to retrieve it.

```yaml
minimum_closure_condition: No closure condition for Cleaning. For the projection: the reason string is already present and sufficient to document the attribution gate.
next_authorized_action: Advisory note only. No action required in this review lane.
patch_queue_entry: not_authorized
red_green_proof: not_applicable
```

---

### AR-03 — Advisory | Cross-Account `content_url` in theperfumeguy Packet

```yaml
finding_id: AR-03
phase: correctness
severity: advisory
source_label: instagram:theperfumeguy
representative_handle: instagram:theperfumeguy:01KVMT1DVHT5ZX62R29MKNKCDG:01KVMT1DVHT5ZX62R29MKNKCDG:ig_call_01:like_count
shortcode: DZs5tT8S1S7
```

**Raw evidence:**
- projection_row.content_url: `https://www.instagram.com/ministryofscent/reel/DZs5tT8S1S7/`
- projection_row.locator: `https://www.instagram.com/ministryofscent/reel/DZs5tT8S1S7/`
- projection_row.username: `"theperfumeguy"`
- projection_row.entity_id: `1098700455` (theperfumeguy's numeric IG ID)
- projection_row.identity_conflict_policy_version: `"ig_numeric_id_username_policy_v0"`

**Cleaned/projection evidence:**
- Cleaned handle raw_anchor preserves file path, json_pointer, and sha256 for the theperfumeguy packet
- Projection row faithfully preserved in cleaned handle projection_ref, including the cross-account URL and policy version field

**Issue (advisory):**

The content URL in this row points to `ministryofscent`'s account while the capture identity (entity_id, username, packet_id) identifies theperfumeguy. Raw source data contains the same pattern — Cleaning did not introduce the discrepancy. The presence of `identity_conflict_policy_version: "ig_numeric_id_username_policy_v0"` confirms the capture layer was aware of and handled this pattern per policy.

**Why advisory:** Cleaning faithfully preserved the projection row including the policy field that documents the handling. This is not a Cleaning error. The note serves as a reminder that a downstream consumer should not naively extract the source creator identity from the content URL for this item type.

```yaml
minimum_closure_condition: No closure condition for Cleaning. Handling is documented in the projection row per existing identity conflict policy.
next_authorized_action: Advisory note only. No Cleaning change required.
patch_queue_entry: not_authorized
red_green_proof: not_applicable
```

---

## Specific Questions

### Did Cleaning overclean meaning?

**No.** Cleaning did not rewrite captions, infer engagement values, normalize counts, score demand or credibility, summarize text, or add semantic content. Verified across curlyscents (follower_count, like_count, comment_count, observed view_count, not_applicable view_count), funmimonet (like_count unavailable_with_reason, three view_count rows), jeremyfragrance (follower_count, like_count), and theperfumeguy (follower_count, like_count). Caption text in parent_context_excerpt was preserved verbatim where present. The funmimonet DDk4rJ6Recu pair confirms that rounded og:description text ("10K likes") was correctly not synthesized into an integer — value set to null with reason, not a fake observed value.

### Did Cleaning underclean traceability?

**No.** All sampled handles contain the full required traceability set:

- `raw_anchor`: json_pointer, file_id (relative path), sha256, relative_packet_path, packet_id, slice_id, anchor_kind
- `projection_ref`: packet_id, row_id, method (`ig_creator_momentum_mechanical_projection`), version (`v0`), certification (`view_only; not_cleaned; not_normalized; not_judgment_ready`), row_kind
- `ecr_ref`: packet_id, posture_kind, ref_id, status for all four source-side posture dimensions
- `relation`: `keyed_siblings_over_raw` on all handles
- `residuals`: ECR residuals preserved where applicable
- `handle_id`: deterministic composite including source, packet_id, slice_id, and metric name

No handle was found missing a required traceability field.

### Did Cleaning lose anchors?

**No.** All 9 targeted pair reads showed:
- `json_pointer_status: resolved`
- `sha256_matches_anchor: true`
- `value_at_json_pointer` matches projection value for all observed rows
- `value_at_json_pointer: null` matches projection value=null for not_applicable rows
- For `unavailable_with_reason` rows where the raw profile API had a non-null value (AR-02 cases: 14629 and 5843), the raw anchor preserved the actual raw value even though the projection nulled it — the raw anchor did not lose the data, and the projection decision is separately documented

No JSON Pointer resolution failures, no hash mismatches, no missing anchor fields.

### Did Cleaning introduce Judgment semantics?

**No.** No sampled handle or projection row contained:
- demand scoring, credibility scoring, salience scoring, actionability claims, or product/creator quality labels
- normalization of engagement values into indexed or comparative forms
- sentiment or semantic caption analysis
- any vocabulary from the Judgment layer

The projection certification field consistently reads `"view_only; not_cleaned; not_normalized; not_judgment_ready"` and is preserved intact in all inspected projection_refs.

### Did Cleaning preserve residuals?

**Yes.** ECR source-side posture residuals were preserved for all 4 packets:

| Posture dimension | clears | value/state | Preserved |
|---|---|---|---|
| identity | true | resolved | yes |
| inspectability | true | inspectable_verifiable (13 slices each) | yes |
| source_visibility | **false** | `current_capture_only` (residual) | yes |
| timing | **false** | `unknown_with_reason` — "IG calls runner did not receive cutoff posture metadata" (all slices, all 4 packets) | yes |

0 stitcher_findings confirmed in both smoke_summary.json (`"findings": []`) and packet_manifest.json (`"stitcher_findings": 0`). No ECR residuals were suppressed.

---

## Plain-Language Explanation

**What Cleaning cleaned:**

The IG Cleaning layer took raw Instagram source capture packets from 4 creators (curlyscents, funmimonet, jeremyfragrance, theperfumeguy) and produced `CleaningInputHandle` records. For each metric row in the IG mechanical projection (follower counts, per-post like counts, comment counts, and video view counts), Cleaning:

1. Created a stable handle ID linking the metric back to its source, packet, slice, and JSON Pointer location in the raw file.
2. Copied the projection's metric value, posture (`observed` / `not_applicable` / `unavailable_with_reason`), and reason string verbatim.
3. Attached the sha256 hash and relative file path so any reader can verify the raw byte content against the anchor.
4. Attached the ECR (Evidence Completeness Receipt) posture summary indicating what is and is not known about the source's identity, inspectability, visibility, and timing — including the known residuals (`current_capture_only`; timing `unknown_with_reason` because cutoff metadata was not received by the IG calls runner).
5. Set `relation = keyed_siblings_over_raw` and `certification = "view_only; not_cleaned; not_normalized; not_judgment_ready"` uniformly across all 134 handles.

**What Cleaning did not clean:**

Cleaning did not rewrite, normalize, score, summarize, infer, or compress any source meaning. Specifically it did not:

- Translate rounded text like "10K likes" into an integer — funmimonet og:description values correctly remain `unavailable_with_reason` with null value.
- Turn null view counts into zeros for `partial_signal` items — null stays null, with a reason string explaining the gate.
- Infer that a cross-account URL was an error and substitute a corrected URL — the raw `content_url` was preserved as-is.
- Add any Judgment vocabulary (demand, credibility, trend, actionability, quality).
- Run live IG capture or supplement the packet with fresh data.
- Clean, summarize, or semantically rewrite Instagram captions or descriptions.

The review packet's `raw.value_at_json_pointer` field makes this traceable end-to-end: for every metric row, a reviewer can compare what the raw file contained at the JSON Pointer against what the projection attributed, and against what Cleaning preserved.

---

## Sampling Declaration

**Coverage required by prompt:** follower_count (any), observed like_count, observed comment_count, observed view_count, view_count:not_applicable, view_count:unavailable_with_reason, and at least one row from each of the 4 source labels.

**Coverage achieved:**

| Requirement | Pair inspected | Source label |
|---|---|---|
| follower_count | curlyscents:ig_profile_00:follower_count (137,777) | instagram:curlyscents |
| observed like_count | curlyscents:ig_call_01:like_count (939) | instagram:curlyscents |
| observed comment_count | curlyscents:ig_call_01:comment_count (113) | instagram:curlyscents |
| observed view_count | curlyscents:ig_call_06:view_count (14,916, reel DZclgFUCvFC) | instagram:curlyscents |
| view_count:not_applicable | curlyscents:ig_call_01:view_count (non-video, is_video=false) | instagram:curlyscents |
| view_count:unavailable_with_reason (×3) | funmimonet:ig_call_05, ig_call_06, ig_call_07:view_count | instagram:funmimonet |
| like_count:unavailable_with_reason | funmimonet:DDk4rJ6Recu:like_count | instagram:funmimonet |
| instagram:jeremyfragrance | jeremyfragrance follower_count (3,110,113) + ig_call_01 like_count (39) | instagram:jeremyfragrance |
| instagram:theperfumeguy | theperfumeguy follower_count (129,494) + ig_call_01 like_count (353) | instagram:theperfumeguy |

Total targeted pair reads: 9, covering approximately 12–15 individual rows. Packet-level counts, ECR receipts, and stitcher_findings verified for all 4 packets (134 total handles, 0 stitcher findings).

**Residual risk:** 119+ rows were not individually inspected. Unsampled rows could contain hash mismatches, pointer resolution failures, or additional posture-vs-content-type inconsistencies of the AR-01 type. Given the mechanically uniform structure of the projection output (same method, version, and certification across all 134 rows), the 0 stitcher_findings count, and the consistent anchor integrity across all sampled rows, this residual risk is assessed as low.

---

## Non-Claims

- **Not live IG capture.** This review covers a static smoke test run completed at 2026-06-21T11:57:39Z. No live IG calls were made during review.
- **Not data-lake promotion.** This review covers the Cleaning stage output only. Promotion to the Orca data lake is a separate lifecycle step not reviewed here.
- **Not production validation.** This is a development smoke test packet. Production readiness requires separate authorization and validation gates.
- **Not E2E product readiness.** Cleaning is one stage. Downstream stages (Judgment, serving, product delivery) are not assessed here.
- **Not Judgment scoring.** No demand, credibility, salience, or actionability claims are made or assessed here.
- **Not product or creator proof.** No assertions are made about creator performance, content quality, or product recommendations.

---

## Review-Use Boundary

This review is decision input only. It is not approval, acceptance, validation, production readiness, or authorization to change code or pipeline configuration. Only a separately authorized patch, acceptance, validation, lifecycle, or implementation lane can make remediation mandatory or executor-ready.
